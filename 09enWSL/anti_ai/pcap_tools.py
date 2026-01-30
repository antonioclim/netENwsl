"""
PCAP and PCAPNG parsing utilities (minimal, standard library only).

The intent is not to fully decode every capture format. The intent is to:
- iterate packets
- extract TCP payload
- search for embedded challenge tokens
"""

from __future__ import annotations

import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Optional


class PcapError(Exception):
    pass


@dataclass(frozen=True)
class TcpPayload:
    src_port: int
    dst_port: int
    payload: bytes


# ──────────────────────────────────────────────────────────────────────────────
# Helpers: Ethernet/IP/TCP parsing (enough for token search)
# ──────────────────────────────────────────────────────────────────────────────

def _parse_tcp_payload_from_linktype(linktype: int, frame: bytes) -> Optional[TcpPayload]:
    """
    Extract TCP payload from a captured frame, if possible.

    Supported linktypes:
    - 1: Ethernet
    - 101: Raw IP (no link-layer header)

    Returns None if the frame is not TCP or not parseable.
    """
    ip = frame

    if linktype == 1:
        if len(frame) < 14:
            return None
        eth_type = struct.unpack("!H", frame[12:14])[0]
        if eth_type == 0x0800:  # IPv4
            ip = frame[14:]
        elif eth_type == 0x86DD:  # IPv6
            ip = frame[14:]
        else:
            return None
    elif linktype == 101:
        ip = frame
    else:
        return None

    if len(ip) < 1:
        return None

    version = (ip[0] >> 4) & 0x0F
    if version == 4:
        if len(ip) < 20:
            return None
        ihl = (ip[0] & 0x0F) * 4
        if len(ip) < ihl + 20:
            return None
        proto = ip[9]
        if proto != 6:
            return None
        tcp = ip[ihl:]
    elif version == 6:
        if len(ip) < 40:
            return None
        next_header = ip[6]
        if next_header != 6:
            return None
        tcp = ip[40:]
    else:
        return None

    if len(tcp) < 20:
        return None

    src_port, dst_port = struct.unpack("!HH", tcp[:4])
    data_offset = (tcp[12] >> 4) * 4
    if len(tcp) < data_offset:
        return None
    payload = tcp[data_offset:]
    return TcpPayload(src_port=src_port, dst_port=dst_port, payload=payload)


# ──────────────────────────────────────────────────────────────────────────────
# PCAP (classic)
# ──────────────────────────────────────────────────────────────────────────────

def iter_pcap_packets(path: Path) -> Iterator[tuple[int, bytes]]:
    data = path.read_bytes()
    if len(data) < 24:
        raise PcapError("PCAP too small")

    magic = struct.unpack("<I", data[:4])[0]
    if magic == 0xA1B2C3D4:
        endian = "<"
    elif magic == 0xD4C3B2A1:
        endian = ">"
    elif magic == 0xA1B23C4D:  # nanosecond-resolution
        endian = "<"
    elif magic == 0x4D3CB2A1:
        endian = ">"
    else:
        raise PcapError("Not a PCAP file (unknown magic)")

    # global header: 24 bytes
    # We do not need most fields, but we want linktype (network)
    if len(data) < 24:
        raise PcapError("PCAP missing global header")
    network = struct.unpack(endian + "I", data[20:24])[0]

    offset = 24
    while offset + 16 <= len(data):
        # per-packet header: ts_sec, ts_usec, incl_len, orig_len
        _, _, incl_len, _ = struct.unpack(endian + "IIII", data[offset:offset + 16])
        offset += 16
        if offset + incl_len > len(data):
            break
        pkt = data[offset:offset + incl_len]
        offset += incl_len
        yield (network, pkt)


# ──────────────────────────────────────────────────────────────────────────────
# PCAPNG (minimal)
# ──────────────────────────────────────────────────────────────────────────────

PCAPNG_SECTION_HEADER = 0x0A0D0D0A
PCAPNG_INTERFACE_DESC = 0x00000001
PCAPNG_ENHANCED_PACKET = 0x00000006


def iter_pcapng_packets(path: Path) -> Iterator[tuple[int, bytes]]:
    data = path.read_bytes()
    offset = 0

    linktypes: list[int] = []

    while offset + 12 <= len(data):
        block_type, block_total_length = struct.unpack("<II", data[offset:offset + 8])
        if block_total_length < 12 or offset + block_total_length > len(data):
            break

        block_body = data[offset + 8: offset + block_total_length - 4]

        if block_type == PCAPNG_SECTION_HEADER:
            # section header has its own endianness marker, but almost all captures are LE.
            # We treat it as LE and continue.
            pass

        elif block_type == PCAPNG_INTERFACE_DESC:
            # linktype: 2 bytes, reserved: 2 bytes, snaplen: 4 bytes
            if len(block_body) >= 8:
                linktype = struct.unpack("<H", block_body[0:2])[0]
                linktypes.append(int(linktype))

        elif block_type == PCAPNG_ENHANCED_PACKET:
            # interface_id: 4, ts_high:4, ts_low:4, cap_len:4, pkt_len:4, then packet data
            if len(block_body) >= 20:
                interface_id = struct.unpack("<I", block_body[0:4])[0]
                cap_len = struct.unpack("<I", block_body[12:16])[0]
                pkt_data = block_body[20:20 + cap_len]
                linktype = linktypes[interface_id] if interface_id < len(linktypes) else 1
                yield (linktype, pkt_data)

        offset += block_total_length


def iter_packets(path: Path) -> Iterator[tuple[int, bytes]]:
    """
    Yield packets as (linktype, raw_frame_bytes).

    Detects PCAP vs PCAPNG by magic.
    """
    # Peek header
    head = path.read_bytes()[:12]
    if len(head) < 4:
        raise PcapError("Capture too small")

    # PCAPNG starts with 0A0D0D0A (LE in file) at the beginning
    if struct.unpack("<I", head[:4])[0] == PCAPNG_SECTION_HEADER:
        yield from iter_pcapng_packets(path)
        return

    # Else assume PCAP
    for linktype, pkt in iter_pcap_packets(path):
        yield linktype, pkt


def iter_tcp_payloads(path: Path) -> Iterator[TcpPayload]:
    for linktype, frame in iter_packets(path):
        item = _parse_tcp_payload_from_linktype(linktype, frame)
        if item and item.payload:
            yield item


def pcap_contains_token(
    path: Path,
    token: str,
    expected_port: Optional[int] = None,
) -> bool:
    needle = token.encode("utf-8")
    for tp in iter_tcp_payloads(path):
        if expected_port is not None and expected_port not in (tp.src_port, tp.dst_port):
            continue
        if needle in tp.payload:
            return True
    return False
