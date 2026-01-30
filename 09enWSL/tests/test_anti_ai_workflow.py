"""
Pytest checks for the Week 9 anti-AI toolkit.

These tests are designed to be fast and self-contained:
- generate a challenge
- build synthetic captures (PCAP and PCAPNG) containing the token in TCP payload
- collect evidence
- validate submission evidence
"""

from __future__ import annotations

import struct
import time
from pathlib import Path
from subprocess import run
import sys

import pytest

from anti_ai.challenge import load_challenge
from anti_ai.pcap_tools import pcap_contains_token


def _ipv4_checksum(header: bytes) -> int:
    if len(header) % 2 == 1:
        header += b"\x00"
    s = 0
    for i in range(0, len(header), 2):
        word = (header[i] << 8) + header[i + 1]
        s += word
        s = (s & 0xFFFF) + (s >> 16)
    return (~s) & 0xFFFF


def _build_ether_ipv4_tcp_frame(payload: bytes, dst_port: int, src_port: int = 12345) -> bytes:
    # Ethernet header
    eth = bytes.fromhex("00112233445566778899aabb0800")

    # IPv4 header (minimal, valid enough for parsing)
    ver_ihl = (4 << 4) | 5
    tos = 0
    total_len = 20 + 20 + len(payload)
    identification = 0x1234
    flags_frag = 0
    ttl = 64
    proto = 6
    checksum = 0
    src_ip = bytes([192, 168, 0, 1])
    dst_ip = bytes([192, 168, 0, 2])

    ipv4 = struct.pack(
        "!BBHHHBBH4s4s",
        ver_ihl,
        tos,
        total_len,
        identification,
        flags_frag,
        ttl,
        proto,
        checksum,
        src_ip,
        dst_ip,
    )
    csum = _ipv4_checksum(ipv4)
    ipv4 = struct.pack(
        "!BBHHHBBH4s4s",
        ver_ihl,
        tos,
        total_len,
        identification,
        flags_frag,
        ttl,
        proto,
        csum,
        src_ip,
        dst_ip,
    )

    # TCP header (no options)
    seq = 1
    ack = 1
    data_offset = 5
    flags = 0x18  # PSH+ACK
    window = 4096
    checksum_tcp = 0
    urg = 0
    tcp = struct.pack(
        "!HHIIHHHH",
        src_port,
        dst_port,
        seq,
        ack,
        (data_offset << 12) | flags,
        window,
        checksum_tcp,
        urg,
    )

    return eth + ipv4 + tcp + payload


def _build_pcap(frame: bytes, linktype: int = 1) -> bytes:
    global_hdr = struct.pack("<IHHIIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, linktype)
    ts = int(time.time())
    pkt_hdr = struct.pack("<IIII", ts, 0, len(frame), len(frame))
    return global_hdr + pkt_hdr + frame


def _build_pcapng(frame: bytes, linktype: int = 1) -> bytes:
    # Section Header Block
    shb_body = struct.pack("<IHHq", 0x1A2B3C4D, 1, 0, -1)
    shb_len = 8 + len(shb_body) + 4
    shb = struct.pack("<II", 0x0A0D0D0A, shb_len) + shb_body + struct.pack("<I", shb_len)

    # Interface Description Block
    idb_body = struct.pack("<HHI", linktype, 0, 65535)
    idb_len = 8 + len(idb_body) + 4
    idb = struct.pack("<II", 0x00000001, idb_len) + idb_body + struct.pack("<I", idb_len)

    # Enhanced Packet Block
    ts = int(time.time())
    ts_high = (ts >> 32) & 0xFFFFFFFF
    ts_low = ts & 0xFFFFFFFF
    cap_len = len(frame)
    pkt_len = len(frame)
    epb_body_prefix = struct.pack("<IIIII", 0, ts_high, ts_low, cap_len, pkt_len)

    # pad to 32-bit boundary
    pad = (4 - (cap_len % 4)) % 4
    frame_padded = frame + (b"\x00" * pad)
    epb_body = epb_body_prefix + frame_padded
    epb_len = 8 + len(epb_body) + 4
    epb = struct.pack("<II", 0x00000006, epb_len) + epb_body + struct.pack("<I", epb_len)

    return shb + idb + epb


@pytest.mark.parametrize("ext, builder", [("pcap", _build_pcap), ("pcapng", _build_pcapng)])
def test_pcap_tools_detects_token(tmp_path: Path, ext: str, builder) -> None:
    token = "W09P-TESTTOKEN"
    expected_port = 34567
    frame = _build_ether_ipv4_tcp_frame(token.encode("utf-8"), dst_port=expected_port)
    cap = builder(frame)
    cap_path = tmp_path / f"capture.{ext}"
    cap_path.write_bytes(cap)

    assert pcap_contains_token(cap_path, token, expected_port=expected_port)


def test_end_to_end_validator_passes(tmp_path: Path) -> None:
    """
    End-to-end check using CLI entrypoints with absolute paths.
    """
    repo_root = Path(__file__).parent.parent

    gen = run(
        [
            sys.executable,
            "-m",
            "anti_ai.challenge_generator",
            "--student-id",
            "TST",
            "--ttl-seconds",
            "3600",
            "--out",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
        check=True,
        cwd=str(repo_root),
    )

    challenge_path = Path(gen.stdout.strip())
    assert challenge_path.exists()

    challenge = load_challenge(challenge_path)
    token = challenge.payload_token
    report_token = challenge.report_token
    port = challenge.expected_control_port

    report_path = tmp_path / "report.md"
    report_path.write_text(f"Report token: {report_token}\n", encoding="utf-8")

    frame = _build_ether_ipv4_tcp_frame(token.encode("utf-8"), dst_port=port)
    cap_bytes = _build_pcap(frame)
    cap_path = tmp_path / "capture.pcap"
    cap_path.write_bytes(cap_bytes)

    ev = run(
        [
            sys.executable,
            "-m",
            "anti_ai.evidence_collector",
            "--challenge",
            str(challenge_path),
            "--pcap",
            str(cap_path),
            "--report",
            str(report_path),
            "--out",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
        check=True,
        cwd=str(repo_root),
    )

    evidence_path = Path(ev.stdout.strip())
    assert evidence_path.exists()

    val = run(
        [
            sys.executable,
            "-m",
            "anti_ai.submission_validator",
            "--challenge",
            str(challenge_path),
            "--evidence",
            str(evidence_path),
        ],
        capture_output=True,
        text=True,
        cwd=str(repo_root),
    )
    assert val.returncode == 0, val.stdout + "\n" + val.stderr
