"""Minimal PCAP and PCAPNG helpers.

The validator needs to find short ASCII strings (challenge tokens, HTTP headers
and DNS query names) inside captures. For this use case, we do not need full TCP
reassembly. We extract packet bytes in capture order and concatenate them.

Supported formats
-----------------
- classic libpcap (pcap)
- pcapng (Enhanced Packet Block and Simple Packet Block)

If a file is not recognised, the extractor returns the raw bytes which still
allows best-effort string searches.
"""

from __future__ import annotations

import struct
from pathlib import Path
from typing import Tuple

PCAP_MAGIC_LE = 0xD4C3B2A1
PCAP_MAGIC_BE = 0xA1B2C3D4
PCAPNG_MAGIC = 0x0A0D0D0A


def _read_u32(data: bytes, offset: int, endian: str) -> int:
    return struct.unpack_from(endian + "I", data, offset)[0]


def extract_packet_bytes(path: str | Path) -> bytes:
    """Extract and concatenate packet bytes from a pcap or pcapng file."""
    p = Path(path)
    data = p.read_bytes()
    if len(data) < 12:
        return data

    magic_bytes = data[:4]

    # Classic pcap magic numbers (microsecond and nanosecond variants)
    pcap_le = {b"\xd4\xc3\xb2\xa1", b"\x4d\x3c\xb2\xa1"}
    pcap_be = {b"\xa1\xb2\xc3\xd4", b"\xa1\xb2\x3c\x4d"}

    if magic_bytes in pcap_le:
        return _extract_pcap(data, "<")
    if magic_bytes in pcap_be:
        return _extract_pcap(data, ">")

    # pcapng starts with a Section Header Block (0x0A0D0D0A)
    block_type = struct.unpack_from("<I", data, 0)[0]
    if block_type == PCAPNG_MAGIC:
        return _extract_pcapng(data)

    return data


def _extract_pcap(data: bytes, endian: str) -> bytes:
    out = bytearray()
    # Global header is 24 bytes
    offset = 24
    while offset + 16 <= len(data):
        # record header: ts_sec, ts_usec, incl_len, orig_len
        incl_len = _read_u32(data, offset + 8, endian)
        offset += 16
        if incl_len <= 0 or offset + incl_len > len(data):
            break
        out.extend(data[offset : offset + incl_len])
        offset += incl_len
    return bytes(out)



def _extract_pcapng(data: bytes) -> bytes:
    out = bytearray()
    offset = 0
    # pcapng uses little-endian for block header fields
    while offset + 12 <= len(data):
        block_type = _read_u32(data, offset, "<")
        total_len = _read_u32(data, offset + 4, "<")
        if total_len < 12 or offset + total_len > len(data):
            break

        # Enhanced Packet Block (0x00000006)
        if block_type == 0x00000006 and total_len >= 32:
            cap_len = _read_u32(data, offset + 20, "<")
            pkt_start = offset + 28
            pkt_end = min(pkt_start + cap_len, offset + total_len)
            if pkt_start < pkt_end:
                out.extend(data[pkt_start:pkt_end])

        # Simple Packet Block (0x00000003)
        elif block_type == 0x00000003 and total_len >= 16:
            pkt_start = offset + 12
            pkt_end = offset + total_len - 4
            if pkt_start < pkt_end:
                out.extend(data[pkt_start:pkt_end])

        offset += total_len

    return bytes(out)
