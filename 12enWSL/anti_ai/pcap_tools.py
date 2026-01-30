#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_DOCSTRING
# ═══════════════════════════════════════════════════════════════════════════════
"""Minimal PCAP and PCAPNG parsing utilities.

The validator needs only two capabilities:

1. Extract packet timestamps.
2. Search packet payload bytes for challenge tokens and attribute hits to TCP ports.

To avoid heavy third-party dependencies, this module implements a small subset
of PCAP and PCAPNG.

Supported link types (common in WSL and Wireshark captures):
 - 1   (DLT_EN10MB) Ethernet
 - 0   (DLT_NULL) BSD loopback
 - 101 (DLT_RAW) Raw IP
 - 113 (DLT_LINUX_SLL) Linux cooked capture
 - 276 (DLT_LINUX_SLL2) Linux cooked capture v2
"""

from __future__ import annotations

import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, List, Optional, Tuple


PCAP_MAGIC_LE = 0xA1B2C3D4
PCAP_MAGIC_BE = 0xD4C3B2A1
PCAPNG_MAGIC = 0x0A0D0D0A


@dataclass(frozen=True)
class PacketHit:
    """A token hit located in a packet."""

    timestamp_epoch: float
    src_port: Optional[int]
    dst_port: Optional[int]
    context: str


@dataclass(frozen=True)
class CaptureSummary:
    packet_count: int
    first_ts: Optional[float]
    last_ts: Optional[float]
    linktypes: List[int]


class PcapParseError(RuntimeError):
    pass


def _u16be(b: bytes, off: int) -> int:
    return int.from_bytes(b[off : off + 2], "big")


def _read_file_bytes(path: Path) -> bytes:
    return path.read_bytes()


def _iter_pcap_packets(data: bytes) -> Tuple[int, Iterator[Tuple[float, bytes]]]:
    if len(data) < 24:
        raise PcapParseError("Truncated PCAP global header")

    magic = struct.unpack("<I", data[0:4])[0]
    if magic == PCAP_MAGIC_LE:
        endian = "<"
    elif magic == PCAP_MAGIC_BE:
        endian = ">"
    else:
        raise PcapParseError("Not a PCAP file")

    # Global header: magic (I) version_major (H) version_minor (H) thiszone (i)
    # sigfigs (I) snaplen (I) network (I)
    _, _, _, _, _, _, network = struct.unpack(endian + "IHHiiii", data[0:24])

    offset = 24

    def it() -> Iterator[Tuple[float, bytes]]:
        nonlocal offset
        # Per-packet header: ts_sec (I) ts_usec (I) incl_len (I) orig_len (I)
        while offset + 16 <= len(data):
            ts_sec, ts_usec, incl_len, _orig_len = struct.unpack(endian + "IIII", data[offset : offset + 16])
            offset += 16
            pkt = data[offset : offset + incl_len]
            offset += incl_len
            if len(pkt) != incl_len:
                break
            yield (float(ts_sec) + float(ts_usec) / 1_000_000.0, pkt)

    return int(network), it()


def _align4(n: int) -> int:
    return (n + 3) & ~3


def _iter_pcapng_packets(data: bytes) -> Tuple[List[int], Iterator[Tuple[float, bytes, int]]]:
    """Yield (timestamp, packet_bytes, linktype) tuples."""

    offset = 0
    linktypes: List[int] = []
    if_ts_res: List[int] = []

    def it() -> Iterator[Tuple[float, bytes, int]]:
        nonlocal offset
        current_iface = 0
        while offset + 12 <= len(data):
            block_type, block_total_length = struct.unpack("<II", data[offset : offset + 8])
            if block_total_length < 12:
                raise PcapParseError("Invalid PCAPNG block length")
            block = data[offset : offset + block_total_length]
            offset += block_total_length

            # Section Header Block
            if block_type == PCAPNG_MAGIC:
                continue

            # Interface Description Block
            if block_type == 0x00000001:
                if len(block) < 20:
                    continue
                linktype = struct.unpack("<H", block[8:10])[0]
                linktypes.append(int(linktype))
                if_ts_res.append(1_000_000)  # default microseconds

                # Parse options for if_tsresol (code 9)
                # Options start at offset 16 and run until code 0.
                opt_off = 16
                while opt_off + 4 <= len(block) - 4:
                    code, length = struct.unpack("<HH", block[opt_off : opt_off + 4])
                    opt_off += 4
                    if code == 0:
                        break
                    value = block[opt_off : opt_off + length]
                    opt_off += _align4(length)
                    if code == 9 and length == 1:
                        # If the msb is 1 then base 2, else base 10.
                        v = value[0]
                        if v & 0x80:
                            # base2 exponent
                            exp = v & 0x7F
                            if_ts_res[-1] = 1 << exp
                        else:
                            # base10 exponent
                            exp = v
                            if_ts_res[-1] = 10**exp
                continue

            # Enhanced Packet Block
            if block_type == 0x00000006:
                if len(block) < 32:
                    continue
                iface_id, ts_high, ts_low, cap_len, _orig_len = struct.unpack("<IIIII", block[8:28])
                pkt_data = block[28 : 28 + cap_len]
                current_iface = int(iface_id)
                lt = linktypes[current_iface] if 0 <= current_iface < len(linktypes) else 1
                resol = if_ts_res[current_iface] if 0 <= current_iface < len(if_ts_res) else 1_000_000
                ts = ((int(ts_high) << 32) | int(ts_low)) / float(resol)
                yield (ts, pkt_data, lt)
                continue

            # Simple Packet Block (rare)
            if block_type == 0x00000003:
                if len(block) < 16:
                    continue
                orig_len = struct.unpack("<I", block[8:12])[0]
                pkt_data = block[12 : 12 + orig_len]
                lt = linktypes[0] if linktypes else 1
                yield (0.0, pkt_data, lt)

    # Ensure we have at least one interface to satisfy consumers.
    return linktypes or [1], it()


def iter_packets(path: Path) -> Tuple[List[int], Iterator[Tuple[float, bytes, int]]]:
    """Return (linktypes, iterator) where iterator yields (timestamp, packet_bytes, linktype)."""

    data = _read_file_bytes(path)
    if len(data) < 4:
        raise PcapParseError("Empty capture")

    magic_le = struct.unpack("<I", data[0:4])[0]
    if magic_le in (PCAP_MAGIC_LE, PCAP_MAGIC_BE):
        linktype, it = _iter_pcap_packets(data)

        def wrap() -> Iterator[Tuple[float, bytes, int]]:
            for ts, pkt in it:
                yield (ts, pkt, int(linktype))

        return [int(linktype)], wrap()

    if magic_le == PCAPNG_MAGIC:
        return _iter_pcapng_packets(data)

    raise PcapParseError("Unknown capture format (expected PCAP or PCAPNG)")


def summarise_capture(path: Path) -> CaptureSummary:
    linktypes, it = iter_packets(path)
    first: Optional[float] = None
    last: Optional[float] = None
    count = 0
    for ts, _pkt, _lt in it:
        count += 1
        if first is None:
            first = ts
        last = ts
    return CaptureSummary(packet_count=count, first_ts=first, last_ts=last, linktypes=linktypes)


def _strip_link_layer(frame: bytes, linktype: int) -> Optional[bytes]:
    """Return the IP packet bytes if possible."""

    if linktype == 1:  # Ethernet
        if len(frame) < 14:
            return None
        eth_type = _u16be(frame, 12)
        if eth_type == 0x0800 or eth_type == 0x86DD:
            return frame[14:]
        return None

    if linktype == 0:  # DLT_NULL
        if len(frame) < 4:
            return None
        return frame[4:]

    if linktype == 101:  # RAW
        return frame

    if linktype == 113:  # Linux SLL
        if len(frame) < 16:
            return None
        proto = _u16be(frame, 14)
        if proto in (0x0800, 0x86DD):
            return frame[16:]
        return None

    if linktype == 276:  # Linux SLL2
        if len(frame) < 20:
            return None
        proto = _u16be(frame, 18)
        if proto in (0x0800, 0x86DD):
            return frame[20:]
        return None

    # Unknown
    return None


def _parse_tcp_payload(ip: bytes) -> Optional[Tuple[int, int, bytes]]:
    """Return (src_port, dst_port, payload) if the packet is TCP."""

    if len(ip) < 1:
        return None

    version = (ip[0] >> 4) & 0xF
    if version == 4:
        if len(ip) < 20:
            return None
        ihl = (ip[0] & 0x0F) * 4
        if len(ip) < ihl:
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
    src_port = int.from_bytes(tcp[0:2], "big")
    dst_port = int.from_bytes(tcp[2:4], "big")
    data_offset = ((tcp[12] >> 4) & 0xF) * 4
    if len(tcp) < data_offset:
        return None
    payload = tcp[data_offset:]
    return src_port, dst_port, payload


def find_token_hits(path: Path, token: str, max_hits: int = 50) -> List[PacketHit]:
    token_bytes = token.encode("utf-8")
    hits: List[PacketHit] = []

    _linktypes, it = iter_packets(path)
    for ts, frame, linktype in it:
        if token_bytes not in frame:
            continue

        ip = _strip_link_layer(frame, linktype)
        sp: Optional[int] = None
        dp: Optional[int] = None
        if ip:
            parsed = _parse_tcp_payload(ip)
            if parsed:
                sp, dp, payload = parsed
                # Extract a short context around the token from payload if present
                if token_bytes in payload:
                    idx = payload.find(token_bytes)
                    start = max(0, idx - 20)
                    end = min(len(payload), idx + len(token_bytes) + 20)
                    ctx = payload[start:end]
                else:
                    ctx = token_bytes
            else:
                ctx = token_bytes
        else:
            ctx = token_bytes

        try:
            ctx_str = ctx.decode("utf-8", errors="replace")
        except Exception:
            ctx_str = "(binary)"

        hits.append(PacketHit(timestamp_epoch=float(ts), src_port=sp, dst_port=dp, context=ctx_str))
        if len(hits) >= max_hits:
            break

    return hits
