"""Minimal PCAP reader utilities.

This reader supports classic PCAP (not PCAPNG). It is intentionally conservative:
- Ethernet linktype is assumed
- IPv4 is fully supported
- IPv6 is supported for basic TCP/UDP extraction

It is sufficient for validating the presence of a student-specific token in MQTT plaintext
traffic and for detecting a TLS handshake pattern in the first application bytes.
"""

from __future__ import annotations

import dataclasses
import struct
from pathlib import Path
from typing import Iterable, Iterator, Optional


@dataclasses.dataclass(frozen=True)
class PacketView:
    """A minimal decoded view of a captured packet."""

    proto: str  # "tcp" or "udp"
    src_port: int
    dst_port: int
    tcp_flags: Optional[int]
    payload: bytes


def _read_exact(f, n: int) -> bytes:
    b = f.read(n)
    if len(b) != n:
        raise EOFError
    return b


def iter_packets(pcap_path: str | Path) -> Iterator[PacketView]:
    """Yield PacketView entries from a PCAP file."""
    p = Path(pcap_path)
    with p.open("rb") as f:
        gh = f.read(24)
        if len(gh) < 24:
            return
        magic = gh[:4]
        if magic == b"\xd4\xc3\xb2\xa1":
            endian = "<"  # little
        elif magic == b"\xa1\xb2\xc3\xd4":
            endian = ">"  # big
        elif magic == b"\x4d\x3c\xb2\xa1":  # ns little
            endian = "<"
        elif magic == b"\xa1\xb2\x3c\x4d":  # ns big
            endian = ">"
        else:
            return

        # linktype is at offset 20
        linktype = struct.unpack(endian + "I", gh[20:24])[0]
        if linktype != 1:
            # Only Ethernet supported
            return

        ph_fmt = endian + "IIII"
        while True:
            try:
                ph = _read_exact(f, 16)
            except EOFError:
                break
            ts_sec, ts_sub, incl_len, orig_len = struct.unpack(ph_fmt, ph)
            try:
                data = _read_exact(f, incl_len)
            except EOFError:
                break

            view = _decode_ethernet_ipv4_ipv6(data)
            if view:
                yield view


def _decode_ethernet_ipv4_ipv6(frame: bytes) -> Optional[PacketView]:
    if len(frame) < 14:
        return None
    eth_type = struct.unpack("!H", frame[12:14])[0]
    payload = frame[14:]
    if eth_type == 0x0800:
        return _decode_ipv4(payload)
    if eth_type == 0x86DD:
        return _decode_ipv6(payload)
    return None


def _decode_ipv4(pkt: bytes) -> Optional[PacketView]:
    if len(pkt) < 20:
        return None
    ver_ihl = pkt[0]
    ver = ver_ihl >> 4
    ihl = (ver_ihl & 0x0F) * 4
    if ver != 4 or ihl < 20 or len(pkt) < ihl:
        return None
    proto = pkt[9]
    payload = pkt[ihl:]
    if proto == 6:
        return _decode_tcp(payload)
    if proto == 17:
        return _decode_udp(payload)
    return None


def _decode_ipv6(pkt: bytes) -> Optional[PacketView]:
    if len(pkt) < 40:
        return None
    ver = pkt[0] >> 4
    if ver != 6:
        return None
    next_header = pkt[6]
    payload = pkt[40:]
    if next_header == 6:
        return _decode_tcp(payload)
    if next_header == 17:
        return _decode_udp(payload)
    return None


def _decode_tcp(seg: bytes) -> Optional[PacketView]:
    if len(seg) < 20:
        return None
    src_port, dst_port = struct.unpack("!HH", seg[0:4])
    data_offset = (seg[12] >> 4) * 4
    if data_offset < 20 or len(seg) < data_offset:
        return None
    flags = seg[13]
    payload = seg[data_offset:]
    return PacketView(proto="tcp", src_port=src_port, dst_port=dst_port, tcp_flags=flags, payload=payload)


def _decode_udp(dat: bytes) -> Optional[PacketView]:
    if len(dat) < 8:
        return None
    src_port, dst_port, length = struct.unpack("!HHH", dat[0:6])
    payload = dat[8:]
    return PacketView(proto="udp", src_port=src_port, dst_port=dst_port, tcp_flags=None, payload=payload)


def pcap_contains_token_on_port(pcap_path: str | Path, token: str, port: int) -> bool:
    t = token.encode("utf-8")
    for pkt in iter_packets(pcap_path):
        if pkt.proto != "tcp":
            continue
        if pkt.src_port != port and pkt.dst_port != port:
            continue
        if t in pkt.payload:
            return True
    return False


def pcap_contains_tls_handshake(pcap_path: str | Path, port: int) -> bool:
    """Detect a TLS handshake record header on a TCP flow to or from port."""
    for pkt in iter_packets(pcap_path):
        if pkt.proto != "tcp":
            continue
        if pkt.src_port != port and pkt.dst_port != port:
            continue
        if len(pkt.payload) < 5:
            continue
        # TLS record header: 0x16 0x03 0x00..0x03
        if pkt.payload[0] == 0x16 and pkt.payload[1] == 0x03 and pkt.payload[2] in (0x00, 0x01, 0x02, 0x03, 0x04):
            return True
    return False


def pcap_has_basic_tcp_handshake(pcap_path: str | Path, port: int) -> bool:
    """Heuristic: check that SYN, SYN-ACK and ACK flags appear for the port."""
    saw_syn = False
    saw_synack = False
    saw_ack = False
    for pkt in iter_packets(pcap_path):
        if pkt.proto != "tcp":
            continue
        if pkt.src_port != port and pkt.dst_port != port:
            continue
        if pkt.tcp_flags is None:
            continue
        flags = pkt.tcp_flags
        syn = bool(flags & 0x02)
        ack = bool(flags & 0x10)
        if syn and not ack:
            saw_syn = True
        elif syn and ack:
            saw_synack = True
        elif ack and not syn:
            saw_ack = True
    return saw_syn and saw_synack and saw_ack
