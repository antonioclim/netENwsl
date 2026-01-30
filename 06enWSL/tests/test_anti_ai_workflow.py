#!/usr/bin/env python3
"""Tests for Week 6 anti-AI workflow.

These tests do not require Mininet or Docker.
They validate the challenge–evidence–validator pipeline including PCAP token checks.
"""

from __future__ import annotations

import json
import struct
import tempfile
from pathlib import Path

from anti_ai.challenge_generator import generate_challenge
from anti_ai.submission_validator import validate_submission
from anti_ai.evidence_collector import sha256_file


def _ip4(addr: str) -> bytes:
    parts = [int(p) for p in addr.split(".")]
    return bytes(parts)


def _ethernet_frame(payload: bytes) -> bytes:
    dst = b"\xaa\xbb\xcc\xdd\xee\xff"
    src = b"\x11\x22\x33\x44\x55\x66"
    ether_type = b"\x08\x00"  # IPv4
    return dst + src + ether_type + payload


def _ipv4_packet(src: str, dst: str, proto: int, l4: bytes) -> bytes:
    version_ihl = 0x45
    tos = 0
    total_len = 20 + len(l4)
    identification = 0
    flags_frag = 0
    ttl = 64
    checksum = 0
    header = struct.pack(
        "!BBHHHBBH4s4s",
        version_ihl,
        tos,
        total_len,
        identification,
        flags_frag,
        ttl,
        proto,
        checksum,
        _ip4(src),
        _ip4(dst),
    )
    return header + l4


def _udp_segment(src_port: int, dst_port: int, payload: bytes) -> bytes:
    length = 8 + len(payload)
    checksum = 0
    header = struct.pack("!HHHH", src_port, dst_port, length, checksum)
    return header + payload


def _tcp_segment(src_port: int, dst_port: int, flags: int, payload: bytes = b"") -> bytes:
    seq = 1
    ack = 0
    data_off_flags = (5 << 12) | (flags & 0x01FF)
    window = 1024
    checksum = 0
    urg_ptr = 0
    header = struct.pack("!HHIIHHHH", src_port, dst_port, seq, ack, data_off_flags, window, checksum, urg_ptr)
    return header + payload


def _write_pcap(path: Path, frames: list[bytes]) -> None:
    # Classic PCAP, little-endian
    gh = struct.pack("<IHHIIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1)
    with open(path, "wb") as f:
        f.write(gh)
        ts_sec = 1700000000
        ts_usec = 0
        for frame in frames:
            ph = struct.pack("<IIII", ts_sec, ts_usec, len(frame), len(frame))
            f.write(ph)
            f.write(frame)
            ts_sec += 1


def _build_udp_token_pcap(challenge) -> bytes:
    payload = f"TOKEN:{challenge.payload_token}".encode("utf-8")
    udp = _udp_segment(40000, challenge.udp_port, payload)
    ip = _ipv4_packet("192.168.1.10", "203.0.113.2", 17, udp)
    return _ethernet_frame(ip)


def _build_tcp_token_pcap_frames(challenge) -> list[bytes]:
    # Basic handshake and a data packet containing the token on the expected TCP port.
    frames: list[bytes] = []

    client_ip = "192.168.1.10"
    server_ip = "203.0.113.2"
    client_port = 41000
    server_port = challenge.tcp_port

    syn = _tcp_segment(client_port, server_port, flags=0x002)
    synack = _tcp_segment(server_port, client_port, flags=0x012)
    ack = _tcp_segment(client_port, server_port, flags=0x010)

    data_payload = f"PAYLOAD:{challenge.payload_token}".encode("utf-8")
    data = _tcp_segment(client_port, server_port, flags=0x018, payload=data_payload)

    for seg, src, dst in [
        (syn, client_ip, server_ip),
        (synack, server_ip, client_ip),
        (ack, client_ip, server_ip),
        (data, client_ip, server_ip),
    ]:
        ip = _ipv4_packet(src, dst, 6, seg)
        frames.append(_ethernet_frame(ip))

    return frames


def test_validator_accepts_udp_and_tcp_token_pcaps() -> None:
    challenge = generate_challenge(student_id="TEST", ttl_seconds=3600, secret=None, sign=False)

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)

        # Write challenge
        challenge_path = root / "challenge.yaml"
        challenge.save_yaml(str(challenge_path))

        # Write report containing report token
        report = root / "report.md"
        report.write_text(f"# Report\n\nReport token: {challenge.report_token}\n", encoding="utf-8")

        # Write PCAPs
        udp_pcap = root / "udp_capture.pcap"
        tcp_pcap = root / "tcp_capture.pcap"

        _write_pcap(udp_pcap, [_build_udp_token_pcap(challenge)])
        _write_pcap(tcp_pcap, _build_tcp_token_pcap_frames(challenge))

        evidence = {
            "meta": {
                "week_id": 6,
                "student_id": challenge.student_id,
                "challenge_id": challenge.challenge_id,
                "issued_at_utc": challenge.issued_at_iso,
                "ttl_seconds": challenge.ttl_seconds,
                "collected_at_utc": challenge.issued_at_iso,
            },
            "environment": {"fingerprint_hash": "deadbeefdeadbeef", "platform": "posix"},
            "artefacts": [
                {"path": "report.md", "sha256": sha256_file(report), "size_bytes": report.stat().st_size},
                {"path": "udp_capture.pcap", "sha256": sha256_file(udp_pcap), "size_bytes": udp_pcap.stat().st_size},
                {"path": "tcp_capture.pcap", "sha256": sha256_file(tcp_pcap), "size_bytes": tcp_pcap.stat().st_size},
            ],
            "probes": {"status": "not_run"},
            "note": "",
        }

        evidence_path = root / "evidence.json"
        evidence_path.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")

        res = validate_submission(
            challenge_path=challenge_path,
            evidence_path=evidence_path,
            base_dir=root,
            secret=None,
            require_signature=False,
            ignore_expiry=True,
            verbose=False,
        )
        assert res.ok, f"Expected ok, got errors: {res.errors}"


def test_validator_rejects_missing_report_token() -> None:
    challenge = generate_challenge(student_id="TEST", ttl_seconds=3600, secret=None, sign=False)

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        challenge_path = root / "challenge.yaml"
        challenge.save_yaml(str(challenge_path))

        report = root / "report.md"
        report.write_text("# Report\n\nNo token here\n", encoding="utf-8")

        pcap = root / "udp_capture.pcap"
        _write_pcap(pcap, [_build_udp_token_pcap(challenge)])

        evidence = {
            "meta": {
                "week_id": 6,
                "student_id": challenge.student_id,
                "challenge_id": challenge.challenge_id,
                "issued_at_utc": challenge.issued_at_iso,
                "ttl_seconds": challenge.ttl_seconds,
                "collected_at_utc": challenge.issued_at_iso,
            },
            "environment": {"fingerprint_hash": "deadbeefdeadbeef", "platform": "posix"},
            "artefacts": [
                {"path": "report.md", "sha256": sha256_file(report), "size_bytes": report.stat().st_size},
                {"path": "udp_capture.pcap", "sha256": sha256_file(pcap), "size_bytes": pcap.stat().st_size},
            ],
            "probes": {"status": "not_run"},
            "note": "",
        }

        evidence_path = root / "evidence.json"
        evidence_path.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")

        res = validate_submission(
            challenge_path=challenge_path,
            evidence_path=evidence_path,
            base_dir=root,
            secret=None,
            require_signature=False,
            ignore_expiry=True,
            verbose=False,
        )
        assert not res.ok
        assert any("Report token" in e for e in res.errors)
