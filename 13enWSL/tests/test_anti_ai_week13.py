#!/usr/bin/env python3
"""Tests for the Week 13 anti-AI workflow.

These tests are fully offline: they generate a challenge, generate synthetic artefacts (including
a minimal PCAP) and validate the submission end to end.
"""

from __future__ import annotations

import json
import struct
import tempfile
from pathlib import Path

import yaml

from anti_ai.challenge_generator import generate
from anti_ai.evidence_collector import _sha256_file  # noqa: SLF001
from anti_ai.submission_validator import main as validate_main
from anti_ai.pcap_tools import pcap_contains_tls_handshake, pcap_contains_token_on_port


def _ipv4_header(total_len: int, proto: int) -> bytes:
    version_ihl = (4 << 4) | 5
    tos = 0
    identification = 0
    flags_fragment = 0
    ttl = 64
    checksum = 0
    src = b"\x0a\x00\x00\x01"  # 10.0.0.1
    dst = b"\x0a\x00\x00\x02"  # 10.0.0.2
    return struct.pack(
        "!BBHHHBBH4s4s",
        version_ihl,
        tos,
        total_len,
        identification,
        flags_fragment,
        ttl,
        proto,
        checksum,
        src,
        dst,
    )


def _tcp_header(src_port: int, dst_port: int, flags: int, payload_len: int) -> bytes:
    seq = 0
    ack = 0
    data_offset = 5
    offset_reserved = (data_offset << 4)
    window = 1024
    checksum = 0
    urg_ptr = 0
    base = struct.pack(
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
    return base


def _eth_frame(payload: bytes, eth_type: int = 0x0800) -> bytes:
    dst_mac = b"\xaa\xbb\xcc\xdd\xee\xff"
    src_mac = b"\x11\x22\x33\x44\x55\x66"
    return dst_mac + src_mac + struct.pack("!H", eth_type) + payload


def _make_tcp_packet(src_port: int, dst_port: int, flags: int, app_payload: bytes) -> bytes:
    tcp = _tcp_header(src_port, dst_port, flags, len(app_payload)) + app_payload
    ip_total = 20 + len(tcp)
    ip = _ipv4_header(ip_total, proto=6)
    return _eth_frame(ip + tcp)


def _write_pcap(path: Path, frames: list[bytes]) -> None:
    # Classic PCAP little endian, Ethernet linktype
    gh = struct.pack(
        "<IHHIIII",
        0xA1B2C3D4,
        2,
        4,
        0,
        0,
        65535,
        1,
    )
    with path.open("wb") as f:
        f.write(gh)
        ts = 0
        for fr in frames:
            ph = struct.pack("<IIII", ts, 0, len(fr), len(fr))
            f.write(ph)
            f.write(fr)
            ts += 1


def test_validator_accepts_synthetic_submission(monkeypatch) -> None:
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)

        challenge = generate("TEST-STUDENT", ttl_seconds=3600, secret=None)
        challenge_path = base / "challenge.yaml"
        challenge_path.write_text(yaml.safe_dump(challenge.to_dict(), sort_keys=False), encoding="utf-8")

        report = base / "security_audit.json"
        report.write_text(json.dumps({"meta": {"report_token": challenge.report_token}}), encoding="utf-8")

        pcap = base / "capture.pcap"
        client_port = 50000
        frames = [
            _make_tcp_packet(client_port, challenge.mqtt_plain_port, 0x02, b""),  # SYN
            _make_tcp_packet(challenge.mqtt_plain_port, client_port, 0x12, b""),  # SYN-ACK
            _make_tcp_packet(client_port, challenge.mqtt_plain_port, 0x10, b""),  # ACK
            _make_tcp_packet(
                client_port,
                challenge.mqtt_plain_port,
                0x18,  # PSH+ACK
                ("PUBLISH " + challenge.payload_token).encode("utf-8"),
            ),
            _make_tcp_packet(client_port, challenge.mqtt_tls_port, 0x18, b"\x16\x03\x01\x00\x2eTLSHELLO"),
        ]
        _write_pcap(pcap, frames)

        assert pcap_contains_token_on_port(pcap, challenge.payload_token, challenge.mqtt_plain_port)
        assert pcap_contains_tls_handshake(pcap, challenge.mqtt_tls_port)

        evidence = {
            "meta": {
                "week_id": 13,
                "student_id": challenge.student_id,
                "challenge_id": challenge.challenge_id,
                "issued_at_utc": challenge.issued_at_utc,
                "collected_at_utc": challenge.issued_at_utc,
                "ttl_seconds": challenge.ttl_seconds,
                "fingerprint_hash": "deadbeefdeadbeef",
            },
            "artefacts": [
                {"path": str(report.name), "sha256": _sha256_file(report)},
                {"path": str(pcap.name), "sha256": _sha256_file(pcap)},
            ],
            "probes": {},
        }
        evidence_path = base / "evidence.json"
        evidence_path.write_text(json.dumps(evidence, indent=2), encoding="utf-8")

        monkeypatch.chdir(base)
        monkeypatch.setattr(
            "sys.argv",
            [
                "anti_ai.submission_validator",
                "--challenge",
                str(challenge_path),
                "--evidence",
                str(evidence_path),
                "--base-dir",
                str(base),
                "--require-tls",
            ],
        )
        assert validate_main() == 0
