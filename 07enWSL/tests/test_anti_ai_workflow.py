"""Unit tests for the Week 7 anti-AI workflow."""

from __future__ import annotations

import json
import struct
from datetime import datetime, timezone
from pathlib import Path

import pytest

from anti_ai.challenge import AntiAIChallenge, save_challenge
from anti_ai.evidence_collector import sha256_file
from anti_ai.submission_validator import validate


def _pcap_global_header() -> bytes:
    # Little-endian PCAP, Ethernet linktype (1)
    return struct.pack(
        "<IHHIIII",
        0xA1B2C3D4,  # magic -> bytes: d4 c3 b2 a1 (little-endian)
        2,
        4,
        0,
        0,
        65535,
        1,
    )


def _pcap_record(pkt: bytes, ts_sec: int = 1, ts_usec: int = 0) -> bytes:
    return struct.pack("<IIII", ts_sec, ts_usec, len(pkt), len(pkt)) + pkt


def _eth_ipv4(payload: bytes) -> bytes:
    dst = b"\xaa\xbb\xcc\xdd\xee\xff"
    src = b"\x00\x11\x22\x33\x44\x55"
    eth_type = b"\x08\x00"  # IPv4
    return dst + src + eth_type + payload


def _ipv4_header(proto: int, src_ip: bytes, dst_ip: bytes, l4: bytes) -> bytes:
    ver_ihl = 0x45
    dscp_ecn = 0
    total_len = 20 + len(l4)
    identification = 0
    flags_frag = 0
    ttl = 64
    checksum = 0
    return struct.pack(
        "!BBHHHBBH4s4s",
        ver_ihl,
        dscp_ecn,
        total_len,
        identification,
        flags_frag,
        ttl,
        proto,
        checksum,
        src_ip,
        dst_ip,
    ) + l4


def _tcp_segment(src_port: int, dst_port: int, seq: int, ack: int, flags: int, payload: bytes = b"") -> bytes:
    data_offset = 5  # 20 bytes
    offset_reserved = (data_offset << 4) & 0xF0
    window = 65535
    checksum = 0
    urg_ptr = 0
    header = struct.pack(
        "!HHIIBBHHH",
        src_port,
        dst_port,
        seq,
        ack,
        offset_reserved,
        flags,
        window,
        checksum,
        urg_ptr,
    )
    return header + payload


def _udp_segment(src_port: int, dst_port: int, payload: bytes) -> bytes:
    length = 8 + len(payload)
    checksum = 0
    return struct.pack("!HHHH", src_port, dst_port, length, checksum) + payload


def _make_token_pcap(path: Path, tcp_port: int, udp_port: int, token: str, *, include_udp: bool = True) -> None:
    token_b = token.encode("utf-8")

    src_ip = b"\x0a\x00\x07\x0b"  # 10.0.7.11
    dst_ip = b"\x0a\x00\x07\x64"  # 10.0.7.100

    client_port = 50000
    # TCP handshake + data
    syn = _eth_ipv4(_ipv4_header(6, src_ip, dst_ip, _tcp_segment(client_port, tcp_port, 1000, 0, 0x02)))
    synack = _eth_ipv4(_ipv4_header(6, dst_ip, src_ip, _tcp_segment(tcp_port, client_port, 2000, 1001, 0x12)))
    data = _eth_ipv4(
        _ipv4_header(
            6,
            src_ip,
            dst_ip,
            _tcp_segment(client_port, tcp_port, 1001, 2001, 0x18, payload=b"MSG:" + token_b),
        )
    )

    packets = [_pcap_record(syn), _pcap_record(synack, ts_sec=2), _pcap_record(data, ts_sec=3)]

    if include_udp:
        udp = _eth_ipv4(_ipv4_header(17, src_ip, dst_ip, _udp_segment(50001, udp_port, payload=b"UDP:" + token_b)))
        packets.append(_pcap_record(udp, ts_sec=4))

    blob = _pcap_global_header() + b"".join(packets)
    path.write_bytes(blob)


def test_anti_ai_validation_roundtrip(tmp_path: Path) -> None:
    chal_path = tmp_path / "challenge.yaml"
    report_path = tmp_path / "report.md"
    pcap_path = tmp_path / "tokens.pcap"
    evidence_path = tmp_path / "evidence.json"

    chal = AntiAIChallenge(
        week_id=7,
        student_id="unit",
        attempt_id="attempt-1",
        issued_at_utc=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        ttl_seconds=24 * 3600,
        report_token="W7R-UNITTESTTOKEN",
        payload_token="W7P-UNITTESTTOKEN",
        tcp_port=9090,
        udp_port=9091,
        challenge_hash="",
    )
    save_challenge(chal, chal_path)

    report_path.write_text(f"# Report\n\nReport token: {chal.report_token}\n", encoding="utf-8")
    _make_token_pcap(pcap_path, chal.tcp_port, chal.udp_port, chal.payload_token)

    evidence = {
        "meta": {
            "week_id": chal.week_id,
            "student_id": chal.student_id,
            "attempt_id": chal.attempt_id,
            "issued_at_utc": chal.issued_at_utc,
            "ttl_seconds": chal.ttl_seconds,
            "challenge_hash": chal.challenge_hash,
        },
        "artefacts": [
            {"path": str(report_path.relative_to(tmp_path)), "sha256": sha256_file(report_path), "bytes": str(report_path.stat().st_size)},
            {"path": str(pcap_path.relative_to(tmp_path)), "sha256": sha256_file(pcap_path), "bytes": str(pcap_path.stat().st_size)},
        ],
    }
    evidence_path.write_text(json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8")

    ok, issues = validate(chal_path, evidence_path, tmp_path, ignore_ttl=False)
    assert ok, "\n".join(f"{i.level}: {i.message}" for i in issues)


def test_anti_ai_missing_udp_token_fails(tmp_path: Path) -> None:
    chal_path = tmp_path / "challenge.yaml"
    report_path = tmp_path / "report.md"
    pcap_path = tmp_path / "tokens.pcap"
    evidence_path = tmp_path / "evidence.json"

    chal = AntiAIChallenge(
        week_id=7,
        student_id="unit",
        attempt_id="attempt-2",
        issued_at_utc=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        ttl_seconds=24 * 3600,
        report_token="W7R-UNITTESTTOKEN2",
        payload_token="W7P-UNITTESTTOKEN2",
        tcp_port=9090,
        udp_port=9091,
        challenge_hash="",
    )
    save_challenge(chal, chal_path)

    report_path.write_text(f"Token {chal.report_token}\n", encoding="utf-8")
    _make_token_pcap(pcap_path, chal.tcp_port, chal.udp_port, chal.payload_token, include_udp=False)

    evidence = {
        "meta": {"week_id": chal.week_id},
        "artefacts": [
            {"path": str(report_path.relative_to(tmp_path)), "sha256": sha256_file(report_path), "bytes": str(report_path.stat().st_size)},
            {"path": str(pcap_path.relative_to(tmp_path)), "sha256": sha256_file(pcap_path), "bytes": str(pcap_path.stat().st_size)},
        ],
    }
    evidence_path.write_text(json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8")

    ok, issues = validate(chal_path, evidence_path, tmp_path, ignore_ttl=False)
    assert not ok
    assert any("UDP payload" in i.message for i in issues if i.level == "error")
