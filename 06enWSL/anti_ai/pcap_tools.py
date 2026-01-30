#!/usr/bin/env python3
"""Minimal PCAP parsing utilities.

This parser supports classic PCAP (not PCAPNG).
It is intentionally minimal and does not validate checksums.
The validator uses it to look for a payload token in UDP or TCP payloads.

Frame support
- Ethernet II
- IPv4
- UDP and TCP
"""

from __future__ import annotations

import ipaddress
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Tuple


PCAP_MAGIC_LE = 0xA1B2C3D4
PCAP_MAGIC_BE = 0xD4C3B2A1


@dataclass(frozen=True)
class ParsedPacket:
    ts_seconds: int
    ts_useconds: int
    proto: str  # "tcp" or "udp" or "other"
    src_ip: str
    dst_ip: str
    src_port: Optional[int]
    dst_port: Optional[int]
    tcp_flags: Optional[int]
    payload: bytes


def iter_pcap_packets(path: Path) -> Iterator[Tuple[int, int, bytes]]:
    """Yield raw packet bytes from a PCAP file."""
    with open(path, "rb") as f:
        global_header = f.read(24)
        if len(global_header) != 24:
            raise ValueError("PCAP file is too short")
        magic = struct.unpack("<I", global_header[:4])[0]
        if magic == PCAP_MAGIC_LE:
            endian = "<"
        elif magic == PCAP_MAGIC_BE:
            endian = ">"
        else:
            raise ValueError("Unsupported PCAP magic value")

        # Skip the rest of the global header fields.

        pkt_hdr_struct = struct.Struct(endian + "IIII")
        while True:
            hdr = f.read(16)
            if not hdr:
                break
            if len(hdr) != 16:
                raise ValueError("Truncated PCAP packet header")
            ts_sec, ts_usec, incl_len, _orig_len = pkt_hdr_struct.unpack(hdr)
            data = f.read(incl_len)
            if len(data) != incl_len:
                raise ValueError("Truncated PCAP packet data")
            yield ts_sec, ts_usec, data


def _mac_len_ok(frame: bytes) -> bool:
    return len(frame) >= 14


def _parse_ether_type(frame: bytes) -> int:
    return struct.unpack("!H", frame[12:14])[0]


def _parse_ipv4_header(pkt: bytes) -> Tuple[int, int, str, str]:
    if len(pkt) < 20:
        raise ValueError("IPv4 packet too short")
    ver_ihl = pkt[0]
    version = ver_ihl >> 4
    if version != 4:
        raise ValueError("Not an IPv4 packet")
    ihl = (ver_ihl & 0x0F) * 4
    if ihl < 20 or len(pkt) < ihl:
        raise ValueError("Invalid IPv4 header length")
    proto = pkt[9]
    src = str(ipaddress.IPv4Address(pkt[12:16]))
    dst = str(ipaddress.IPv4Address(pkt[16:20]))
    return ihl, proto, src, dst


def _parse_udp(pkt: bytes, ip_header_len: int) -> Tuple[int, int, bytes]:
    off = ip_header_len
    if len(pkt) < off + 8:
        raise ValueError("UDP packet too short")
    src_port, dst_port, length, _csum = struct.unpack("!HHHH", pkt[off:off + 8])
    payload = pkt[off + 8:off + length] if length >= 8 else b""
    return src_port, dst_port, payload


def _parse_tcp(pkt: bytes, ip_header_len: int) -> Tuple[int, int, int, bytes]:
    off = ip_header_len
    if len(pkt) < off + 20:
        raise ValueError("TCP packet too short")
    src_port, dst_port, _seq, _ack, data_off_flags = struct.unpack("!HHIIH", pkt[off:off + 14])
    data_offset = ((data_off_flags >> 12) & 0xF) * 4
    flags = data_off_flags & 0x01FF  # lower 9 bits
    if data_offset < 20 or len(pkt) < off + data_offset:
        raise ValueError("Invalid TCP data offset")
    payload = pkt[off + data_offset:]
    return src_port, dst_port, flags, payload


def parse_pcap(path: Path) -> List[ParsedPacket]:
    parsed: List[ParsedPacket] = []
    for ts_sec, ts_usec, frame in iter_pcap_packets(path):
        if not _mac_len_ok(frame):
            continue
        ether_type = _parse_ether_type(frame)
        if ether_type != 0x0800:
            continue  # only IPv4
        ip_pkt = frame[14:]
        try:
            ip_hlen, proto, src, dst = _parse_ipv4_header(ip_pkt)
        except ValueError:
            continue

        if proto == 17:  # UDP
            try:
                sp, dp, payload = _parse_udp(ip_pkt, ip_hlen)
            except ValueError:
                continue
            parsed.append(
                ParsedPacket(ts_sec, ts_usec, "udp", src, dst, sp, dp, None, payload)
            )
        elif proto == 6:  # TCP
            try:
                sp, dp, flags, payload = _parse_tcp(ip_pkt, ip_hlen)
            except ValueError:
                continue
            parsed.append(
                ParsedPacket(ts_sec, ts_usec, "tcp", src, dst, sp, dp, flags, payload)
            )
        else:
            parsed.append(
                ParsedPacket(ts_sec, ts_usec, "other", src, dst, None, None, None, b"")
            )
    return parsed


def find_payload_token(
    packets: List[ParsedPacket],
    token: str,
    expected_tcp_port: Optional[int] = None,
    expected_udp_port: Optional[int] = None,
) -> Dict[str, bool]:
    """Search for token occurrences in parsed packets."""
    token_bytes = token.encode("utf-8")
    found_tcp = False
    found_udp = False

    for p in packets:
        if p.proto == "tcp" and p.payload:
            if expected_tcp_port is not None and (p.src_port != expected_tcp_port and p.dst_port != expected_tcp_port):
                continue
            if token_bytes in p.payload:
                found_tcp = True
        if p.proto == "udp" and p.payload:
            if expected_udp_port is not None and (p.src_port != expected_udp_port and p.dst_port != expected_udp_port):
                continue
            if token_bytes in p.payload:
                found_udp = True

    return {"tcp": found_tcp, "udp": found_udp}


def has_tcp_handshake(
    packets: List[ParsedPacket],
    expected_port: Optional[int] = None,
) -> bool:
    """Detect a basic TCP handshake (SYN, SYN-ACK, ACK) for any flow."""
    # Group by unordered endpoint pair and port pair.
    state: Dict[Tuple[str, str, int, int], Dict[str, bool]] = {}

    def key(p: ParsedPacket) -> Optional[Tuple[str, str, int, int]]:
        if p.proto != "tcp" or p.src_port is None or p.dst_port is None or p.tcp_flags is None:
            return None
        if expected_port is not None and (p.src_port != expected_port and p.dst_port != expected_port):
            return None
        a = (p.src_ip, p.src_port)
        b = (p.dst_ip, p.dst_port)
        if a <= b:
            return (a[0], b[0], a[1], b[1])
        return (b[0], a[0], b[1], a[1])

    for p in packets:
        k = key(p)
        if k is None:
            continue
        flags = p.tcp_flags or 0
        syn = bool(flags & 0x002)
        ack = bool(flags & 0x010)
        if k not in state:
            state[k] = {"syn": False, "synack": False, "ack": False}

        if syn and not ack:
            state[k]["syn"] = True
        elif syn and ack:
            state[k]["synack"] = True
        elif ack and not syn:
            state[k]["ack"] = True

    return any(v["syn"] and v["synack"] and v["ack"] for v in state.values())
