#!/usr/bin/env python3
"""anti_ai.pcap_tools

Minimal PCAP reader and IPv4/TCP/UDP parser.

Design constraints:
- pure Python, no external dependencies
- enough robustness for typical tcpdump and Wireshark captures in WSL
- focuses on extracting L4 payloads rather than full dissection

Supported link types:
- Ethernet (DLT_EN10MB = 1)
- Raw IP (DLT_RAW = 101)
- Linux cooked capture (DLT_LINUX_SLL = 113)
"""

from __future__ import annotations

import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Optional, Tuple


DLT_EN10MB = 1
DLT_RAW = 101
DLT_LINUX_SLL = 113

ETH_HDR_LEN = 14
SLL_HDR_LEN = 16


@dataclass(frozen=True)
class PcapInfo:
    endianness: str  # "<" or ">"
    snaplen: int
    linktype: int


@dataclass(frozen=True)
class IPv4Packet:
    src_ip: str
    dst_ip: str
    protocol: int
    payload: bytes


@dataclass(frozen=True)
class TCPDatagram:
    src_port: int
    dst_port: int
    flags: int
    payload: bytes


@dataclass(frozen=True)
class UDPDatagram:
    src_port: int
    dst_port: int
    payload: bytes


def _read_exact(f, n: int) -> bytes:
    b = f.read(n)
    if len(b) != n:
        raise EOFError
    return b


def read_pcap_info(path: str | Path) -> PcapInfo:
    p = Path(path)
    with p.open("rb") as f:
        magic = f.read(4)
        if len(magic) != 4:
            raise ValueError("Not a PCAP file (too short)")

        magic_u = struct.unpack("<I", magic)[0]
        if magic_u == 0xA1B2C3D4:
            end = "<"
        elif magic_u == 0xD4C3B2A1:
            end = ">"
        elif magic_u == 0xA1B23C4D:
            end = "<"  # ns resolution
        elif magic_u == 0x4D3CB2A1:
            end = ">"
        else:
            # Try big-endian read of the same bytes
            magic_u_be = struct.unpack(">I", magic)[0]
            if magic_u_be in (0xA1B2C3D4, 0xA1B23C4D):
                end = ">"
            else:
                raise ValueError("Unsupported PCAP magic")

        # Version major/minor, thiszone, sigfigs, snaplen, linktype
        hdr = _read_exact(f, 20)
        ver_major, ver_minor, _thiszone, _sigfigs, snaplen, linktype = struct.unpack(
            f"{end}HHiiii", hdr
        )
        return PcapInfo(endianness=end, snaplen=snaplen, linktype=linktype)


def iter_pcap_packets(path: str | Path) -> Iterator[Tuple[float, bytes, PcapInfo]]:
    p = Path(path)
    info = read_pcap_info(p)

    with p.open("rb") as f:
        # Skip global header (24 bytes total)
        f.seek(24)

        while True:
            rec_hdr = f.read(16)
            if not rec_hdr:
                break
            if len(rec_hdr) != 16:
                break

            ts_sec, ts_subsec, incl_len, _orig_len = struct.unpack(f"{info.endianness}IIII", rec_hdr)
            data = f.read(incl_len)
            if len(data) != incl_len:
                break

            ts = float(ts_sec) + (float(ts_subsec) / 1_000_000.0)
            yield ts, data, info


def _strip_link_header(frame: bytes, linktype: int) -> Optional[bytes]:
    if linktype == DLT_RAW:
        return frame

    if linktype == DLT_EN10MB:
        if len(frame) < ETH_HDR_LEN:
            return None
        ethertype = struct.unpack(">H", frame[12:14])[0]
        if ethertype != 0x0800:
            return None
        return frame[ETH_HDR_LEN:]

    if linktype == DLT_LINUX_SLL:
        if len(frame) < SLL_HDR_LEN:
            return None
        proto = struct.unpack(">H", frame[14:16])[0]
        if proto != 0x0800:
            return None
        return frame[SLL_HDR_LEN:]

    # Unknown link type, best-effort: try to find an IPv4 header start
    for off in range(0, min(64, len(frame))):
        if (frame[off] >> 4) == 4:
            return frame[off:]
    return None


def parse_ipv4(packet: bytes) -> Optional[IPv4Packet]:
    if len(packet) < 20:
        return None
    ver_ihl = packet[0]
    ver = ver_ihl >> 4
    if ver != 4:
        return None
    ihl = (ver_ihl & 0x0F) * 4
    if ihl < 20 or len(packet) < ihl:
        return None

    total_len = struct.unpack(">H", packet[2:4])[0]
    protocol = packet[9]
    src_ip = ".".join(str(b) for b in packet[12:16])
    dst_ip = ".".join(str(b) for b in packet[16:20])

    if total_len <= ihl:
        payload = b""
    else:
        payload = packet[ihl:total_len] if total_len <= len(packet) else packet[ihl:]
    return IPv4Packet(src_ip=src_ip, dst_ip=dst_ip, protocol=protocol, payload=payload)


def parse_tcp(segment: bytes) -> Optional[TCPDatagram]:
    if len(segment) < 20:
        return None
    src_port, dst_port = struct.unpack(">HH", segment[:4])
    data_offset = (segment[12] >> 4) * 4
    if data_offset < 20 or len(segment) < data_offset:
        return None
    flags = segment[13]
    payload = segment[data_offset:]
    return TCPDatagram(src_port=src_port, dst_port=dst_port, flags=flags, payload=payload)


def parse_udp(datagram: bytes) -> Optional[UDPDatagram]:
    if len(datagram) < 8:
        return None
    src_port, dst_port, length = struct.unpack(">HHH", datagram[:6])
    if length < 8:
        return None
    payload = datagram[8:length] if length <= len(datagram) else datagram[8:]
    return UDPDatagram(src_port=src_port, dst_port=dst_port, payload=payload)


def iter_tcp_from_pcap(path: str | Path) -> Iterator[TCPDatagram]:
    for _ts, frame, info in iter_pcap_packets(path):
        ip_bytes = _strip_link_header(frame, info.linktype)
        if not ip_bytes:
            continue
        ip = parse_ipv4(ip_bytes)
        if not ip or ip.protocol != 6:
            continue
        tcp = parse_tcp(ip.payload)
        if tcp:
            yield tcp


def iter_udp_from_pcap(path: str | Path) -> Iterator[UDPDatagram]:
    for _ts, frame, info in iter_pcap_packets(path):
        ip_bytes = _strip_link_header(frame, info.linktype)
        if not ip_bytes:
            continue
        ip = parse_ipv4(ip_bytes)
        if not ip or ip.protocol != 17:
            continue
        udp = parse_udp(ip.payload)
        if udp:
            yield udp
