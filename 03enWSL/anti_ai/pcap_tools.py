#!/usr/bin/env python3
"""Minimal PCAP parsing utilities.

This module intentionally avoids third-party packet libraries so that the kit
remains easy to install in WSL and CI.

Supported formats:
- classic PCAP (not PCAP-NG)
- link types: Ethernet (1) and Linux cooked capture v1 (113) and RAW IP (101)

The parser is designed for verification tasks:
- locate a token in UDP payloads for given ports and optional destination IP
- locate a token in TCP payloads and detect a basic 3-way handshake

It does not attempt full protocol correctness, checksum validation or TCP stream reassembly.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Optional

import struct


LINKTYPE_ETHERNET = 1
LINKTYPE_RAW_IP = 101
LINKTYPE_LINUX_SLL = 113

ETHERTYPE_IPV4 = 0x0800


@dataclass(frozen=True, slots=True)
class ParsedPacket:
    """A parsed packet record."""

    ts_sec: int
    ts_subsec: int
    proto: str | None  # "udp", "tcp" or None
    src_ip: str | None
    dst_ip: str | None
    src_port: int | None
    dst_port: int | None
    tcp_flags: int | None
    payload: bytes


def _ip_to_str(raw: bytes) -> str:
    return ".".join(str(b) for b in raw)


def _read_pcap_global_header(f) -> tuple[str, int, bool]:
    """Return (endian, linktype, nanosecond_ts)."""
    magic_raw = f.read(4)
    if len(magic_raw) != 4:
        raise ValueError("PCAP file is too short")

    magic = struct.unpack("<I", magic_raw)[0]
    # little-endian magic values
    if magic == 0xA1B2C3D4:
        endian = "<"
        ns = False
    elif magic == 0xA1B23C4D:
        endian = "<"
        ns = True
    # big-endian variants
    elif magic == 0xD4C3B2A1:
        endian = ">"
        ns = False
    elif magic == 0x4D3CB2A1:
        endian = ">"
        ns = True
    else:
        raise ValueError(f"Unsupported PCAP magic: 0x{magic:08x}")

    hdr = f.read(20)
    if len(hdr) != 20:
        raise ValueError("PCAP global header is incomplete")

    _ver_major, _ver_minor, _thiszone, _sigfigs, _snaplen, linktype = struct.unpack(
        endian + "HHiiii", hdr
    )
    return endian, linktype, ns


def iter_parsed_packets(path: str | Path) -> Iterator[ParsedPacket]:
    """Iterate over parsed packets in a classic PCAP file."""
    path = Path(path)
    with path.open("rb") as f:
        endian, linktype, ns = _read_pcap_global_header(f)

        rec_hdr_fmt = endian + "IIII"
        while True:
            rec_hdr = f.read(16)
            if not rec_hdr:
                break
            if len(rec_hdr) != 16:
                break
            ts_sec, ts_sub, incl_len, _orig_len = struct.unpack(rec_hdr_fmt, rec_hdr)
            data = f.read(incl_len)
            if len(data) != incl_len:
                break

            parsed = _parse_record(ts_sec, ts_sub, data, linktype)
            if parsed:
                yield parsed
            else:
                # still yield an unparsed packet so token search can fall back to raw scanning
                yield ParsedPacket(
                    ts_sec=ts_sec,
                    ts_subsec=ts_sub,
                    proto=None,
                    src_ip=None,
                    dst_ip=None,
                    src_port=None,
                    dst_port=None,
                    tcp_flags=None,
                    payload=data,
                )


def _parse_record(ts_sec: int, ts_sub: int, data: bytes, linktype: int) -> ParsedPacket | None:
    """Parse link + IPv4 + UDP/TCP and return a ParsedPacket."""
    ip_offset = None
    if linktype == LINKTYPE_ETHERNET:
        if len(data) < 14:
            return None
        ethertype = struct.unpack("!H", data[12:14])[0]
        if ethertype != ETHERTYPE_IPV4:
            return None
        ip_offset = 14
    elif linktype == LINKTYPE_LINUX_SLL:
        # Linux cooked capture v1 header is 16 bytes, protocol is last 2 bytes
        if len(data) < 16:
            return None
        proto = struct.unpack("!H", data[14:16])[0]
        if proto != ETHERTYPE_IPV4:
            return None
        ip_offset = 16
    elif linktype == LINKTYPE_RAW_IP:
        ip_offset = 0
    else:
        return None

    if len(data) < ip_offset + 20:
        return None

    v_ihl = data[ip_offset]
    version = v_ihl >> 4
    ihl = (v_ihl & 0x0F) * 4
    if version != 4 or ihl < 20:
        return None
    if len(data) < ip_offset + ihl:
        return None

    proto_num = data[ip_offset + 9]
    src_ip = _ip_to_str(data[ip_offset + 12 : ip_offset + 16])
    dst_ip = _ip_to_str(data[ip_offset + 16 : ip_offset + 20])

    l4_offset = ip_offset + ihl
    if proto_num == 17:  # UDP
        if len(data) < l4_offset + 8:
            return None
        src_port, dst_port, length = struct.unpack("!HHH", data[l4_offset : l4_offset + 6])
        payload_offset = l4_offset + 8
        payload_end = min(len(data), payload_offset + max(0, length - 8))
        payload = data[payload_offset:payload_end]
        return ParsedPacket(
            ts_sec=ts_sec,
            ts_subsec=ts_sub,
            proto="udp",
            src_ip=src_ip,
            dst_ip=dst_ip,
            src_port=src_port,
            dst_port=dst_port,
            tcp_flags=None,
            payload=payload,
        )
    if proto_num == 6:  # TCP
        if len(data) < l4_offset + 20:
            return None
        src_port, dst_port = struct.unpack("!HH", data[l4_offset : l4_offset + 4])
        data_offset = (data[l4_offset + 12] >> 4) * 4
        if data_offset < 20:
            return None
        if len(data) < l4_offset + data_offset:
            return None
        flags = data[l4_offset + 13]
        payload = data[l4_offset + data_offset :]
        return ParsedPacket(
            ts_sec=ts_sec,
            ts_subsec=ts_sub,
            proto="tcp",
            src_ip=src_ip,
            dst_ip=dst_ip,
            src_port=src_port,
            dst_port=dst_port,
            tcp_flags=flags,
            payload=payload,
        )

    return None


def pcap_contains_token(
    pcap_path: str | Path,
    token: str,
    *,
    proto: str | None = None,
    port: int | None = None,
    dst_ip: str | None = None,
    require_handshake: bool = False,
) -> tuple[bool, dict[str, object]]:
    """Search for *token* in a PCAP file.

    Parameters:
        proto: "udp" or "tcp" to constrain the search, or None for any.
        port: source or destination port to constrain the search.
        dst_ip: destination IPv4 address to constrain the search (best effort).
        require_handshake: for TCP only, require a basic SYN/SYN-ACK/ACK pattern.

    Returns (found, details).
    """
    token_b = token.encode("utf-8")
    details: dict[str, object] = {
        "pcap": str(Path(pcap_path)),
        "proto": proto,
        "port": port,
        "dst_ip": dst_ip,
        "token_found": False,
        "handshake_ok": None,
        "matches": [],
    }

    handshake_state: dict[tuple[str, int, str, int], set[str]] = {}
    found = False

    for pkt in iter_parsed_packets(pcap_path):
        # Filter by protocol if possible
        if proto and pkt.proto and pkt.proto != proto:
            continue
        if proto and pkt.proto is None:
            # unparsed: cannot safely constrain
            continue

        # Filter by port if possible
        if port is not None and pkt.src_port is not None and pkt.dst_port is not None:
            if pkt.src_port != port and pkt.dst_port != port:
                continue

        # Filter by destination IP if possible
        if dst_ip and pkt.dst_ip and pkt.dst_ip != dst_ip:
            continue

        # Token in payload
        if token_b in pkt.payload:
            found = True
            details["token_found"] = True
            details["matches"].append(
                {
                    "ts_sec": pkt.ts_sec,
                    "proto": pkt.proto,
                    "src": f"{pkt.src_ip}:{pkt.src_port}" if pkt.src_ip and pkt.src_port else None,
                    "dst": f"{pkt.dst_ip}:{pkt.dst_port}" if pkt.dst_ip and pkt.dst_port else None,
                    "payload_len": len(pkt.payload),
                }
            )

        # Handshake tracking
        if require_handshake and pkt.proto == "tcp" and pkt.tcp_flags is not None:
            if pkt.src_ip and pkt.dst_ip and pkt.src_port and pkt.dst_port:
                flow = (pkt.src_ip, pkt.src_port, pkt.dst_ip, pkt.dst_port)
                # Normalise flow direction to treat both directions together
                rev = (pkt.dst_ip, pkt.dst_port, pkt.src_ip, pkt.src_port)
                key = min(flow, rev)

                state = handshake_state.setdefault(key, set())
                flags = pkt.tcp_flags
                syn = bool(flags & 0x02)
                ack = bool(flags & 0x10)

                if syn and not ack:
                    state.add("syn")
                elif syn and ack:
                    state.add("synack")
                elif ack and not syn:
                    state.add("ack")

    if require_handshake and (proto == "tcp" or proto is None):
        ok = any({"syn", "synack", "ack"}.issubset(v) for v in handshake_state.values())
        details["handshake_ok"] = ok
    return found, details
