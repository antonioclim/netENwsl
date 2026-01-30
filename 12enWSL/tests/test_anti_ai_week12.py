"""Tests for Week 12 anti-AI tooling.

These tests avoid external tools (tcpdump, tshark). Instead, they generate small synthetic
PCAP files containing the challenge tokens and verify the validator logic.
"""

from __future__ import annotations

import json
import hashlib
import struct
from datetime import datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from anti_ai.challenge import Week12Challenge
from anti_ai.validator import Week12SubmissionValidator


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _write_pcap(path: Path, packets: list[tuple[float, bytes]]) -> None:
    """Write a minimal PCAP file with Ethernet frames."""

    # PCAP global header (little-endian)
    # magic, version_major, version_minor, thiszone, sigfigs, snaplen, network
    gh = struct.pack("<IHHiiii", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1)
    out = bytearray(gh)

    for ts, frame in packets:
        sec = int(ts)
        usec = int((ts - sec) * 1_000_000)
        incl = len(frame)
        ph = struct.pack("<IIII", sec, usec, incl, incl)
        out.extend(ph)
        out.extend(frame)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(bytes(out))


def _ether_ipv4_tcp_frame(*, src_port: int, dst_port: int, payload: bytes) -> bytes:
    """Construct an Ethernet + IPv4 + TCP frame.

    Checksums are set to zero because the validator does not validate them.
    """

    # Ethernet
    eth = b"\xaa\xbb\xcc\xdd\xee\xff" + b"\x11\x22\x33\x44\x55\x66" + b"\x08\x00"

    # IPv4 header (20 bytes)
    ver_ihl = (4 << 4) | 5
    tos = 0
    total_len = 20 + 20 + len(payload)
    identification = 0
    flags_frag = 0
    ttl = 64
    proto = 6  # TCP
    checksum = 0
    src_ip = b"\x7f\x00\x00\x01"  # 127.0.0.1
    dst_ip = b"\x7f\x00\x00\x01"
    ip = struct.pack(
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

    # TCP header (20 bytes)
    seq = 1
    ack = 1
    data_offset = 5  # 20 bytes
    flags = 0x18  # PSH + ACK
    window = 8192
    tcp_checksum = 0
    urg = 0
    tcp = struct.pack(
        "!HHIIHHHH",
        int(src_port),
        int(dst_port),
        seq,
        ack,
        (data_offset << 12) | flags,
        window,
        tcp_checksum,
        urg,
    )

    return eth + ip + tcp + payload


def test_validator_accepts_tokens_on_required_ports() -> None:
    with TemporaryDirectory() as td:
        td = Path(td)

        issued = datetime.now(timezone.utc)
        ch = Week12Challenge(
            week=12,
            student_id="S123",
            issued_at_utc=issued.strftime("%Y-%m-%dT%H:%M:%SZ"),
            ttl_seconds=3600,
            smtp_subject_token="SMTP_TOKEN_123",
            rpc_echo_token="RPC_TOKEN_456",
            report_token="REPORT_TOKEN_789",
            smtp_port=1025,
            jsonrpc_port=6200,
            xmlrpc_port=6201,
            grpc_port=6251,
        )

        challenge_path = td / "challenge.yaml"
        challenge_path.write_text(ch.to_yaml(), encoding="utf-8")

        ts = issued.timestamp() + 1
        pcap_path = td / "capture.pcap"
        packets = [
            (ts, _ether_ipv4_tcp_frame(src_port=40000, dst_port=1025, payload=b"Subject: " + ch.smtp_subject_token.encode())),
            (ts + 0.1, _ether_ipv4_tcp_frame(src_port=40001, dst_port=6200, payload=b"{" + ch.rpc_echo_token.encode() + b"}")),
            (ts + 0.2, _ether_ipv4_tcp_frame(src_port=40002, dst_port=6201, payload=b"<methodCall>" + ch.rpc_echo_token.encode() + b"</methodCall>")),
        ]
        _write_pcap(pcap_path, packets)

        evidence_path = td / "evidence.json"
        evidence = {
            "meta": {"student_id": "S123"},
            "artifacts": {
                "pcaps": [str(pcap_path)],
                "report": None,
                "sha256": {str(pcap_path): _sha256_file(pcap_path)},
            },
        }
        evidence_path.write_text(json.dumps(evidence), encoding="utf-8")

        v = Week12SubmissionValidator(strict=False)
        rep = v.validate(challenge_path=challenge_path, evidence_path=evidence_path)

        assert rep.ok, f"Expected ok but failed: {[c.__dict__ for c in rep.checks]}"


def test_validator_rejects_missing_xmlrpc_token() -> None:
    with TemporaryDirectory() as td:
        td = Path(td)

        issued = datetime.now(timezone.utc)
        ch = Week12Challenge(
            week=12,
            student_id="S123",
            issued_at_utc=issued.strftime("%Y-%m-%dT%H:%M:%SZ"),
            ttl_seconds=3600,
            smtp_subject_token="SMTP_TOKEN_123",
            rpc_echo_token="RPC_TOKEN_456",
            report_token="REPORT_TOKEN_789",
            smtp_port=1025,
            jsonrpc_port=6200,
            xmlrpc_port=6201,
            grpc_port=6251,
        )

        challenge_path = td / "challenge.yaml"
        challenge_path.write_text(ch.to_yaml(), encoding="utf-8")

        ts = issued.timestamp() + 1
        pcap_path = td / "capture.pcap"
        packets = [
            (ts, _ether_ipv4_tcp_frame(src_port=40000, dst_port=1025, payload=b"Subject: " + ch.smtp_subject_token.encode())),
            (ts + 0.1, _ether_ipv4_tcp_frame(src_port=40001, dst_port=6200, payload=b"{" + ch.rpc_echo_token.encode() + b"}")),
        ]
        _write_pcap(pcap_path, packets)

        evidence_path = td / "evidence.json"
        evidence = {
            "meta": {"student_id": "S123"},
            "artifacts": {"pcaps": [str(pcap_path)], "report": None, "sha256": {}},
        }
        evidence_path.write_text(json.dumps(evidence), encoding="utf-8")

        v = Week12SubmissionValidator(strict=False)
        rep = v.validate(challenge_path=challenge_path, evidence_path=evidence_path)

        assert not rep.ok
        assert any(c.name == "rpc_token_xmlrpc_port" and not c.passed for c in rep.checks)
