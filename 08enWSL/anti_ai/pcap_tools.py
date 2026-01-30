"""PCAP parsing utilities (no external dependencies).

This module supports classic PCAP and PCAPNG captures with Ethernet + IPv4
frames.

It is intentionally not a full protocol stack, it extracts enough information
to validate:
  - ports and basic TCP flags (handshake)
  - presence of student-specific header values in HTTP payloads

If `tshark` is available you should prefer using it, but this module is useful
as a fallback in constrained environments.
"""

from __future__ import annotations

import re
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Tuple


PCAP_MAGIC_BE = 0xA1B2C3D4
PCAP_MAGIC_LE = 0xD4C3B2A1
PCAP_MAGIC_BE_NS = 0xA1B23C4D
PCAP_MAGIC_LE_NS = 0x4D3CB2A1
PCAPNG_BLOCK_TYPE_SHB = 0x0A0D0D0A


@dataclass(frozen=True)
class TcpSegment:
    ts: float
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    flags: int
    seq: int
    payload: bytes


def _read_u32(buf: bytes, offset: int, endian: str) -> int:
    return struct.unpack_from(endian + "I", buf, offset)[0]


def _read_u16(buf: bytes, offset: int, endian: str) -> int:
    return struct.unpack_from(endian + "H", buf, offset)[0]


def _inet_ntoa(b: bytes) -> str:
    return ".".join(str(x) for x in b)


def _parse_ethernet(frame: bytes) -> Tuple[int, int]:
    """Return (ethertype, payload_offset). Supports 802.1Q VLAN."""
    if len(frame) < 14:
        return 0, 0

    ethertype = struct.unpack_from("!H", frame, 12)[0]
    offset = 14

    # VLAN tag
    if ethertype == 0x8100 and len(frame) >= 18:
        ethertype = struct.unpack_from("!H", frame, 16)[0]
        offset = 18

    return ethertype, offset


def _parse_ipv4(packet: bytes, offset: int) -> Optional[Tuple[str, str, int, int]]:
    """Return (src_ip, dst_ip, proto, header_len)."""
    if len(packet) < offset + 20:
        return None
    vihl = packet[offset]
    version = vihl >> 4
    if version != 4:
        return None
    ihl = (vihl & 0x0F) * 4
    if ihl < 20 or len(packet) < offset + ihl:
        return None

    proto = packet[offset + 9]
    src_ip = _inet_ntoa(packet[offset + 12 : offset + 16])
    dst_ip = _inet_ntoa(packet[offset + 16 : offset + 20])
    return src_ip, dst_ip, proto, ihl


def _parse_tcp(packet: bytes, offset: int) -> Optional[Tuple[int, int, int, int, bytes]]:
    """Return (src_port, dst_port, flags, seq, payload)."""
    if len(packet) < offset + 20:
        return None
    src_port, dst_port = struct.unpack_from("!HH", packet, offset)
    seq = struct.unpack_from("!I", packet, offset + 4)[0]
    data_offset = (packet[offset + 12] >> 4) * 4
    flags = packet[offset + 13]
    if data_offset < 20 or len(packet) < offset + data_offset:
        return None
    payload = packet[offset + data_offset :]
    return src_port, dst_port, flags, seq, payload


def _iter_pcap_packets(path: Path) -> Iterator[Tuple[float, bytes]]:
    data = path.read_bytes()
    if len(data) < 24:
        return

    magic = struct.unpack_from("!I", data, 0)[0]
    if magic in {PCAP_MAGIC_BE, PCAP_MAGIC_BE_NS}:
        endian = ">"
    elif magic in {PCAP_MAGIC_LE, PCAP_MAGIC_LE_NS}:
        endian = "<"
    else:
        return

    ns = magic in {PCAP_MAGIC_BE_NS, PCAP_MAGIC_LE_NS}

    offset = 24
    while offset + 16 <= len(data):
        ts_sec = _read_u32(data, offset, endian)
        ts_sub = _read_u32(data, offset + 4, endian)
        incl_len = _read_u32(data, offset + 8, endian)
        # orig_len = _read_u32(data, offset + 12, endian)
        offset += 16
        if offset + incl_len > len(data):
            break
        frame = data[offset : offset + incl_len]
        offset += incl_len

        ts = float(ts_sec) + (ts_sub / (1_000_000_000 if ns else 1_000_000))
        yield ts, frame


def _iter_pcapng_packets(path: Path) -> Iterator[Tuple[float, bytes]]:
    data = path.read_bytes()
    if len(data) < 12:
        return

    offset = 0
    endian = "<"  # default until SHB sets it
    linktype = None

    while offset + 12 <= len(data):
        block_type = struct.unpack_from(endian + "I", data, offset)[0]
        block_total_len = struct.unpack_from(endian + "I", data, offset + 4)[0]
        if block_total_len < 12 or offset + block_total_len > len(data):
            break

        if block_type == PCAPNG_BLOCK_TYPE_SHB:
            # SHB has byte-order magic at offset + 8 in the block
            bom = struct.unpack_from("<I", data, offset + 8)[0]
            if bom == 0x1A2B3C4D:
                endian = "<"
            else:
                bom_be = struct.unpack_from(">I", data, offset + 8)[0]
                if bom_be == 0x1A2B3C4D:
                    endian = ">"

        elif block_type == 0x00000001:
            # Interface Description Block
            # linktype at offset + 8 (u16)
            if block_total_len >= 20:
                lt = _read_u16(data, offset + 8, endian)
                linktype = int(lt)

        elif block_type == 0x00000006:
            # Enhanced Packet Block
            if linktype != 1 and linktype is not None:
                # Only Ethernet supported
                pass
            else:
                iface_id = _read_u32(data, offset + 8, endian)
                ts_high = _read_u32(data, offset + 12, endian)
                ts_low = _read_u32(data, offset + 16, endian)
                cap_len = _read_u32(data, offset + 20, endian)
                # pkt_len = _read_u32(data, offset + 24, endian)

                pkt_offset = offset + 28
                pkt_end = pkt_offset + cap_len
                if pkt_end <= offset + block_total_len - 4 and pkt_end <= len(data):
                    frame = data[pkt_offset:pkt_end]
                    # Timestamp unit is nominally microseconds without tsresol
                    ts = float((ts_high << 32) | ts_low) / 1_000_000
                    _ = iface_id
                    yield ts, frame

        elif block_type == 0x00000003:
            # Simple Packet Block
            if linktype != 1 and linktype is not None:
                pass
            else:
                pkt_len = _read_u32(data, offset + 8, endian)
                pkt_offset = offset + 12
                pkt_end = min(pkt_offset + pkt_len, offset + block_total_len - 4)
                if pkt_offset < pkt_end <= len(data):
                    frame = data[pkt_offset:pkt_end]
                    yield 0.0, frame

        offset += block_total_len


def iter_tcp_segments(path: Path) -> Iterator[TcpSegment]:
    """Iterate TCP segments in a capture."""
    raw = path.read_bytes()[:4]
    if len(raw) < 4:
        return

    first_u32_be = struct.unpack("!I", raw)[0]

    if first_u32_be in {PCAP_MAGIC_BE, PCAP_MAGIC_BE_NS, PCAP_MAGIC_LE, PCAP_MAGIC_LE_NS}:
        pkt_iter = _iter_pcap_packets(path)
    elif first_u32_be == PCAPNG_BLOCK_TYPE_SHB:
        pkt_iter = _iter_pcapng_packets(path)
    else:
        return

    for ts, frame in pkt_iter:
        ethertype, l3off = _parse_ethernet(frame)
        if ethertype != 0x0800:
            continue

        ipv4 = _parse_ipv4(frame, l3off)
        if not ipv4:
            continue
        src_ip, dst_ip, proto, ihl = ipv4
        if proto != 6:
            continue

        tcp = _parse_tcp(frame, l3off + ihl)
        if not tcp:
            continue
        src_port, dst_port, flags, seq, payload = tcp

        yield TcpSegment(
            ts=ts,
            src_ip=src_ip,
            dst_ip=dst_ip,
            src_port=src_port,
            dst_port=dst_port,
            flags=flags,
            seq=seq,
            payload=payload,
        )


def capture_mentions_port(path: Path, port: int) -> bool:
    for seg in iter_tcp_segments(path):
        if seg.src_port == port or seg.dst_port == port:
            return True
    return False


def capture_contains_ascii(path: Path, needle: str, port: Optional[int] = None) -> bool:
    n = needle.encode("utf-8")
    for seg in iter_tcp_segments(path):
        if port is not None and seg.src_port != port and seg.dst_port != port:
            continue
        if n in seg.payload:
            return True
    return False


def count_http_header_values(path: Path, header_name: str, port: Optional[int] = None) -> Dict[str, int]:
    """Count occurrences of HTTP header values in TCP payloads.

    This is a best-effort scan of payloads. It does not perform full TCP stream
    reassembly but works reliably for small HTTP responses typical for the lab.
    """

    pattern = re.compile(rb"\r\n" + re.escape(header_name.encode("utf-8")) + rb":\s*([^\r\n]+)")
    counts: Dict[str, int] = {}
    for seg in iter_tcp_segments(path):
        if port is not None and seg.src_port != port and seg.dst_port != port:
            continue
        for m in pattern.finditer(seg.payload):
            value = m.group(1).decode("iso-8859-1", errors="replace").strip()
            counts[value] = counts.get(value, 0) + 1
    return counts


def has_basic_tcp_handshake(path: Path, port: int) -> bool:
    """Heuristically verify a TCP three-way handshake occurred on a port."""

    # Flags
    SYN = 0x02
    ACK = 0x10

    syn_seen = False
    synack_seen = False
    ack_seen = False

    for seg in iter_tcp_segments(path):
        if seg.src_port != port and seg.dst_port != port:
            continue

        flags = seg.flags
        if flags & SYN and not (flags & ACK):
            syn_seen = True
        elif (flags & SYN) and (flags & ACK):
            synack_seen = True
        elif (flags & ACK) and not (flags & SYN):
            # This will catch many ACKs, we just need at least one.
            ack_seen = True

        if syn_seen and synack_seen and ack_seen:
            return True

    return False
