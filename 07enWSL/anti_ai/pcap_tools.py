"""Minimal PCAP utilities for token validation.

This module supports *classic* PCAP files (tcpdump -w), not PCAPNG.
It is intentionally dependency-free to keep the kit lightweight.

Supported:
- Ethernet (linktype 1)
- IPv4
- TCP and UDP parsing sufficient for extracting payload bytes
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, List, Optional, Tuple

import struct


class PcapFormatError(ValueError):
    pass


@dataclass(frozen=True)
class PacketView:
    ts_sec: int
    ts_usec: int
    eth_type: int
    ip_proto: int
    src_ip: str
    dst_ip: str
    src_port: Optional[int]
    dst_port: Optional[int]
    tcp_flags: Optional[int]
    payload: bytes


def _u32(b: bytes, endian: str) -> int:
    return struct.unpack(endian + "I", b)[0]


def _u16(b: bytes, endian: str) -> int:
    return struct.unpack(endian + "H", b)[0]


def _ip4(addr: bytes) -> str:
    return ".".join(str(x) for x in addr)


def iter_packets(path: Path) -> Iterator[PacketView]:
    raw = path.read_bytes()
    if len(raw) < 24:
        raise PcapFormatError("File too small for PCAP global header")

    magic = raw[:4]
    if magic == b"\xd4\xc3\xb2\xa1":
        endian = "<"
    elif magic == b"\xa1\xb2\xc3\xd4":
        endian = ">"  # rare
    else:
        # PCAPNG magic is 0x0A0D0D0A
        if magic == b"\x0a\x0d\x0d\x0a":
            raise PcapFormatError("PCAPNG is not supported. Use tcpdump -w file.pcap")
        raise PcapFormatError("Unrecognised PCAP magic")

    # global header
    # magic(4), vmaj(2), vmin(2), thiszone(4), sigfigs(4), snaplen(4), network(4)
    network = _u32(raw[20:24], endian)
    if network != 1:
        raise PcapFormatError(f"Unsupported linktype {network} (expected Ethernet=1)")

    off = 24
    while off + 16 <= len(raw):
        ts_sec = _u32(raw[off : off + 4], endian)
        ts_usec = _u32(raw[off + 4 : off + 8], endian)
        incl_len = _u32(raw[off + 8 : off + 12], endian)
        orig_len = _u32(raw[off + 12 : off + 16], endian)
        off += 16
        if off + incl_len > len(raw):
            break
        frame = raw[off : off + incl_len]
        off += incl_len

        if len(frame) < 14:
            continue
        eth_type = struct.unpack(">H", frame[12:14])[0]
        if eth_type != 0x0800:
            continue  # IPv4 only

        # IPv4 header
        if len(frame) < 14 + 20:
            continue
        ip = frame[14:]
        ver_ihl = ip[0]
        ihl = (ver_ihl & 0x0F) * 4
        if len(ip) < ihl:
            continue
        ip_proto = ip[9]
        src_ip = _ip4(ip[12:16])
        dst_ip = _ip4(ip[16:20])

        l4 = ip[ihl:]
        src_port = None
        dst_port = None
        flags = None
        payload = b""

        if ip_proto == 6 and len(l4) >= 20:  # TCP
            src_port = struct.unpack(">H", l4[0:2])[0]
            dst_port = struct.unpack(">H", l4[2:4])[0]
            data_offset = (l4[12] >> 4) * 4
            flags = l4[13]
            if len(l4) >= data_offset:
                payload = l4[data_offset:]
        elif ip_proto == 17 and len(l4) >= 8:  # UDP
            src_port = struct.unpack(">H", l4[0:2])[0]
            dst_port = struct.unpack(">H", l4[2:4])[0]
            payload = l4[8:]

        yield PacketView(
            ts_sec=ts_sec,
            ts_usec=ts_usec,
            eth_type=eth_type,
            ip_proto=ip_proto,
            src_ip=src_ip,
            dst_ip=dst_ip,
            src_port=src_port,
            dst_port=dst_port,
            tcp_flags=flags,
            payload=payload,
        )


def find_payload_token(
    packets: Iterable[PacketView],
    token: bytes,
    *,
    tcp_port: Optional[int] = None,
    udp_port: Optional[int] = None,
) -> Tuple[bool, bool]:
    """Return (tcp_found, udp_found) for token presence in payload."""
    tcp_found = False
    udp_found = False
    for p in packets:
        if not p.payload:
            continue
        if token not in p.payload:
            continue
        if p.ip_proto == 6 and p.dst_port is not None:
            if tcp_port is None or p.dst_port == tcp_port:
                tcp_found = True
        if p.ip_proto == 17 and p.dst_port is not None:
            if udp_port is None or p.dst_port == udp_port:
                udp_found = True
        if tcp_found and udp_found:
            break
    return tcp_found, udp_found


def has_tcp_handshake(packets: Iterable[PacketView], *, port: int) -> bool:
    """Heuristic: detect a SYN, SYN-ACK and ACK for a given TCP destination port."""
    syn = False
    synack = False
    ack = False

    # Track by (client_ip, client_port, server_ip, server_port) with minimal state
    for p in packets:
        if p.ip_proto != 6 or p.tcp_flags is None:
            continue
        if p.src_port is None or p.dst_port is None:
            continue
        if p.dst_port == port:
            # client -> server
            if p.tcp_flags & 0x02 and not (p.tcp_flags & 0x10):  # SYN without ACK
                syn = True
        if p.src_port == port:
            # server -> client
            if (p.tcp_flags & 0x12) == 0x12:  # SYN + ACK
                synack = True
        # any ACK towards server
        if p.dst_port == port and (p.tcp_flags & 0x10):
            ack = True

        if syn and synack and ack:
            return True
    return False
