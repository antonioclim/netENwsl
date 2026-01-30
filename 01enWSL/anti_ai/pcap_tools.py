#!/usr/bin/env python3
"""PCAP inspection utilities used by the Week 1 anti-AI validator.

The primary intent is to make the submission depend on a binary artefact that
is difficult to fabricate convincingly without running the laboratory tasks.

The validator checks for:
- presence of a unique payload token in TCP and UDP payloads
- a minimal TCP three-way handshake pattern (SYN, SYN-ACK, ACK)

The implementation uses dpkt and attempts to handle common capture link types
(Ethernet, Linux cooked capture and raw IP).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Optional

import dpkt


@dataclass
class PcapInspection:
    """Summary of a PCAP inspection."""

    pcap_path: str
    linktype: Optional[int]
    packet_count: int
    ip_count: int
    tcp_count: int
    udp_count: int
    handshake_ok: bool
    payload_expected: Optional[str]
    payload_found: bool
    payload_found_in_tcp: bool
    payload_found_in_udp: bool
    first_ts: Optional[float]
    last_ts: Optional[float]
    errors: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "pcap_path": self.pcap_path,
            "linktype": self.linktype,
            "packet_count": self.packet_count,
            "ip_count": self.ip_count,
            "tcp_count": self.tcp_count,
            "udp_count": self.udp_count,
            "handshake_ok": self.handshake_ok,
            "payload_expected": self.payload_expected,
            "payload_found": self.payload_found,
            "payload_found_in_tcp": self.payload_found_in_tcp,
            "payload_found_in_udp": self.payload_found_in_udp,
            "first_ts": self.first_ts,
            "last_ts": self.last_ts,
            "errors": self.errors,
        }


def _try_parse_ip(buf: bytes, linktype: Optional[int]) -> Optional[dpkt.ip.IP]:
    """Try to parse raw packet bytes into an IP packet."""
    parsers: list[callable] = []

    # Common linktypes
    if linktype in (dpkt.pcap.DLT_EN10MB, 1, None):
        parsers.append(lambda b: dpkt.ethernet.Ethernet(b).data)
    if linktype in (getattr(dpkt.pcap, "DLT_LINUX_SLL", 113), 113, None):
        parsers.append(lambda b: dpkt.sll.SLL(b).data)
    if linktype in (getattr(dpkt.pcap, "DLT_RAW", 101), 101, None):
        parsers.append(lambda b: dpkt.ip.IP(b))

    # Fallbacks (order matters)
    parsers.extend([
        lambda b: dpkt.ethernet.Ethernet(b).data,
        lambda b: dpkt.sll.SLL(b).data,
        lambda b: dpkt.ip.IP(b),
    ])

    for parse in parsers:
        try:
            ip = parse(buf)
            if isinstance(ip, dpkt.ip.IP):
                return ip
        except (dpkt.UnpackError, ValueError):
            continue
    return None


def inspect_pcap(pcap_path: Path, expected_payload: Optional[str] = None) -> PcapInspection:
    """Inspect a PCAP for Week 1 proof tokens and basic protocol signals."""
    errors: list[str] = []

    packet_count = 0
    ip_count = 0
    tcp_count = 0
    udp_count = 0

    payload_found_tcp = False
    payload_found_udp = False

    seen_syn = False
    seen_synack = False
    seen_ack = False

    first_ts: Optional[float] = None
    last_ts: Optional[float] = None

    linktype: Optional[int] = None

    try:
        with open(pcap_path, "rb") as f:
            reader = dpkt.pcap.Reader(f)
            # dpkt exposes datalink() in most builds
            try:
                linktype = int(reader.datalink())
            except Exception:
                linktype = None

            expected_bytes = expected_payload.encode("utf-8") if expected_payload else None

            for ts, buf in reader:
                packet_count += 1
                if first_ts is None:
                    first_ts = ts
                last_ts = ts

                ip = _try_parse_ip(buf, linktype)
                if ip is None:
                    continue

                ip_count += 1

                if isinstance(ip.data, dpkt.tcp.TCP):
                    tcp_count += 1
                    tcp: dpkt.tcp.TCP = ip.data

                    flags = int(tcp.flags)
                    syn = bool(flags & dpkt.tcp.TH_SYN)
                    ack = bool(flags & dpkt.tcp.TH_ACK)

                    if syn and not ack:
                        seen_syn = True
                    elif syn and ack and seen_syn:
                        seen_synack = True
                    elif ack and not syn and seen_synack:
                        seen_ack = True

                    if expected_bytes and expected_bytes in (tcp.data or b""):
                        payload_found_tcp = True

                elif isinstance(ip.data, dpkt.udp.UDP):
                    udp_count += 1
                    udp: dpkt.udp.UDP = ip.data
                    if expected_bytes and expected_bytes in (udp.data or b""):
                        payload_found_udp = True

    except (OSError, dpkt.UnpackError) as exc:
        errors.append(f"Failed to read PCAP: {exc}")

    handshake_ok = seen_syn and seen_synack and seen_ack
    payload_found = payload_found_tcp or payload_found_udp

    # Last resort: scan raw bytes if parsing did not find payload
    if expected_payload and not payload_found:
        try:
            raw = pcap_path.read_bytes()
            if expected_payload.encode("utf-8") in raw:
                payload_found = True
                # do not guess protocol
        except OSError as exc:
            errors.append(f"Failed to scan raw PCAP bytes: {exc}")

    return PcapInspection(
        pcap_path=str(pcap_path),
        linktype=linktype,
        packet_count=packet_count,
        ip_count=ip_count,
        tcp_count=tcp_count,
        udp_count=udp_count,
        handshake_ok=handshake_ok,
        payload_expected=expected_payload,
        payload_found=payload_found,
        payload_found_in_tcp=payload_found_tcp,
        payload_found_in_udp=payload_found_udp,
        first_ts=first_ts,
        last_ts=last_ts,
        errors=errors,
    )


def sha256_bytes(data: bytes) -> str:
    """Convenience helper for tests."""
    return hashlib.sha256(data).hexdigest()

