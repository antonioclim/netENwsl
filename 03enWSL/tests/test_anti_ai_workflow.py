#!/usr/bin/env python3
"""Unit tests for the Week 3 anti-AI workflow.

These tests do not require Docker. They create synthetic artefacts that exercise:
- challenge serialisation and integrity checks
- evidence hashing
- PCAP parsing and token detection for UDP and TCP, including handshake detection
- end-to-end submission validation

The goal is to keep the anti-AI mechanism testable in CI without relying on
containerised network traffic.
"""

from __future__ import annotations

import json
import os
import tempfile
import time
import unittest
from pathlib import Path

from anti_ai.challenge import Challenge, compute_integrity, save_challenge
from anti_ai.evidence_collector import main as evidence_main
from anti_ai.submission_validator import validate as validate_submission


def _ip_bytes(ip: str) -> bytes:
    return bytes(int(x) for x in ip.split("."))


def _ipv4_header(src: str, dst: str, proto: int, total_len: int, ident: int = 0x1234) -> bytes:
    # Minimal IPv4 header with checksum set to 0 (verification does not require it)
    ver_ihl = (4 << 4) | 5
    tos = 0
    flags_frag = 0
    ttl = 64
    checksum = 0
    return (
        bytes([ver_ihl, tos])
        + total_len.to_bytes(2, "big")
        + ident.to_bytes(2, "big")
        + flags_frag.to_bytes(2, "big")
        + bytes([ttl, proto])
        + checksum.to_bytes(2, "big")
        + _ip_bytes(src)
        + _ip_bytes(dst)
    )


def _udp_packet(src_ip: str, dst_ip: str, src_port: int, dst_port: int, payload: bytes) -> bytes:
    import struct

    udp_len = 8 + len(payload)
    ip_total = 20 + udp_len
    ip = _ipv4_header(src_ip, dst_ip, proto=17, total_len=ip_total)
    udp = struct.pack("!HHHH", src_port, dst_port, udp_len, 0)
    eth = b"\xff\xff\xff\xff\xff\xff" + b"\x00\x11\x22\x33\x44\x55" + b"\x08\x00"
    return eth + ip + udp + payload


def _tcp_header(src_port: int, dst_port: int, seq: int, ack: int, flags: int) -> bytes:
    import struct

    data_offset = 5  # 20 bytes
    offset_res = (data_offset << 4) & 0xF0
    window = 65535
    checksum = 0
    urg_ptr = 0
    return struct.pack("!HHIIBBHHH", src_port, dst_port, seq, ack, offset_res, flags, window, checksum, urg_ptr)


def _tcp_packet(src_ip: str, dst_ip: str, src_port: int, dst_port: int, seq: int, ack: int, flags: int, payload: bytes = b"") -> bytes:
    tcp = _tcp_header(src_port, dst_port, seq, ack, flags) + payload
    ip_total = 20 + len(tcp)
    ip = _ipv4_header(src_ip, dst_ip, proto=6, total_len=ip_total)
    eth = b"\xaa\xbb\xcc\xdd\xee\xff" + b"\x00\x11\x22\x33\x44\x55" + b"\x08\x00"
    return eth + ip + tcp


def _write_pcap(path: Path, packets: list[bytes], linktype: int = 1) -> None:
    import struct

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        # global header: magic, v2.4, thiszone=0, sigfigs=0, snaplen=65535, linktype
        f.write(struct.pack("<IHHIIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, linktype))
        ts = int(time.time())
        for i, data in enumerate(packets):
            ts_sec = ts + i
            ts_usec = 0
            f.write(struct.pack("<IIII", ts_sec, ts_usec, len(data), len(data)))
            f.write(data)


class TestAntiAIWorkflow(unittest.TestCase):
    def test_end_to_end_validation_passes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)

            sid = "TEST123"
            payload_token = "W03-TEST123-abcdef"
            report_token = "RPT-TEST123-123456"

            # Standard ports match the docker-compose defaults
            broadcast_port = 5007
            multicast_port = 5008
            tunnel_port = 9090

            issued_at = "2030-01-01T00:00:00+00:00"
            payload = {
                "meta": {"week": 3, "student_id": sid, "issued_at_utc": issued_at, "valid_for_hours": 99999},
                "tokens": {"payload_token": payload_token, "report_token": report_token},
                "recommended": {
                    "broadcast": {"port": broadcast_port},
                    "multicast": {"group": "239.0.0.10", "port": multicast_port},
                    "tunnel": {"listen_port": tunnel_port},
                },
            }
            sha, mac = compute_integrity(payload, hmac_key=None)

            ch = Challenge(
                week=3,
                student_id=sid,
                issued_at_utc=issued_at,
                valid_for_hours=99999,
                payload_token=payload_token,
                report_token=report_token,
                broadcast_port=broadcast_port,
                multicast_group="239.0.0.10",
                multicast_port=multicast_port,
                tunnel_listen_port=tunnel_port,
                integrity_sha256=sha,
                integrity_hmac=mac,
            )

            challenge_path = base / "artifacts" / "anti_ai" / f"challenge_{sid}.yaml"
            save_challenge(ch, challenge_path)

            # Report
            report_path = base / "artifacts" / "anti_ai" / f"w03_report_{sid}.md"
            report_path.write_text(f"Report token: {report_token}\n", encoding="utf-8")

            # Broadcast PCAP with token in UDP payload
            bc_path = base / "artifacts" / "anti_ai" / f"w03_broadcast_{sid}.pcap"
            bc_pkt = _udp_packet("172.20.0.100", "255.255.255.255", 40000, broadcast_port, (payload_token + " broadcast").encode("utf-8"))
            _write_pcap(bc_path, [bc_pkt])

            # Multicast PCAP with token in UDP payload
            mc_path = base / "artifacts" / "anti_ai" / f"w03_multicast_{sid}.pcap"
            mc_pkt = _udp_packet("172.20.0.100", "239.0.0.10", 40001, multicast_port, (payload_token + " multicast").encode("utf-8"))
            _write_pcap(mc_path, [mc_pkt])

            # Tunnel PCAP: handshake + payload
            tn_path = base / "artifacts" / "anti_ai" / f"w03_tunnel_{sid}.pcap"
            c_ip = "172.20.0.100"
            r_ip = "172.20.0.254"
            c_port = 45000
            r_port = tunnel_port

            syn = _tcp_packet(c_ip, r_ip, c_port, r_port, seq=1000, ack=0, flags=0x02)
            synack = _tcp_packet(r_ip, c_ip, r_port, c_port, seq=2000, ack=1001, flags=0x12)
            ack = _tcp_packet(c_ip, r_ip, c_port, r_port, seq=1001, ack=2001, flags=0x10)
            data = _tcp_packet(c_ip, r_ip, c_port, r_port, seq=1001, ack=2001, flags=0x18, payload=(payload_token + " tunnel").encode("utf-8"))
            _write_pcap(tn_path, [syn, synack, ack, data])

            # Evidence file via CLI entrypoint (to cover hashing)
            evidence_path = base / "artifacts" / "anti_ai" / f"evidence_{sid}.json"
            rc = evidence_main([
                "--challenge", str(challenge_path),
                "--base-dir", str(base),
                "--output", str(evidence_path.relative_to(base)),
                "--artefact", str(report_path.relative_to(base)),
                "--artefact", str(bc_path.relative_to(base)),
                "--artefact", str(mc_path.relative_to(base)),
                "--artefact", str(tn_path.relative_to(base)),
            ])
            self.assertEqual(rc, 0)

            # Validate
            result = validate_submission(
                challenge_path=challenge_path,
                evidence_path=evidence_path,
                base_dir=base,
                verbose=True,
                ignore_expiry=True,
                require_hmac=False,
            )
            self.assertTrue(result.ok, "\n".join(result.messages))

    def test_validation_fails_if_token_missing(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            sid = "TEST123"
            payload_token = "W03-TEST123-abcdef"
            report_token = "RPT-TEST123-123456"

            broadcast_port = 5007
            multicast_port = 5008
            tunnel_port = 9090
            issued_at = "2030-01-01T00:00:00+00:00"

            payload = {
                "meta": {"week": 3, "student_id": sid, "issued_at_utc": issued_at, "valid_for_hours": 99999},
                "tokens": {"payload_token": payload_token, "report_token": report_token},
                "recommended": {
                    "broadcast": {"port": broadcast_port},
                    "multicast": {"group": "239.0.0.10", "port": multicast_port},
                    "tunnel": {"listen_port": tunnel_port},
                },
            }
            sha, mac = compute_integrity(payload, hmac_key=None)

            ch = Challenge(
                week=3,
                student_id=sid,
                issued_at_utc=issued_at,
                valid_for_hours=99999,
                payload_token=payload_token,
                report_token=report_token,
                broadcast_port=broadcast_port,
                multicast_group="239.0.0.10",
                multicast_port=multicast_port,
                tunnel_listen_port=tunnel_port,
                integrity_sha256=sha,
                integrity_hmac=mac,
            )
            challenge_path = base / "artifacts" / "anti_ai" / f"challenge_{sid}.yaml"
            save_challenge(ch, challenge_path)

            report_path = base / "artifacts" / "anti_ai" / f"w03_report_{sid}.md"
            report_path.write_text(f"Report token: {report_token}\n", encoding="utf-8")

            # Broadcast PCAP without token
            bc_path = base / "artifacts" / "anti_ai" / f"w03_broadcast_{sid}.pcap"
            bc_pkt = _udp_packet("172.20.0.100", "255.255.255.255", 40000, broadcast_port, b"no token here")
            _write_pcap(bc_path, [bc_pkt])

            # Multicast PCAP with token
            mc_path = base / "artifacts" / "anti_ai" / f"w03_multicast_{sid}.pcap"
            mc_pkt = _udp_packet("172.20.0.100", "239.0.0.10", 40001, multicast_port, (payload_token + " multicast").encode("utf-8"))
            _write_pcap(mc_path, [mc_pkt])

            # Tunnel PCAP with token
            tn_path = base / "artifacts" / "anti_ai" / f"w03_tunnel_{sid}.pcap"
            c_ip = "172.20.0.100"
            r_ip = "172.20.0.254"
            c_port = 45000
            r_port = tunnel_port
            syn = _tcp_packet(c_ip, r_ip, c_port, r_port, seq=1000, ack=0, flags=0x02)
            synack = _tcp_packet(r_ip, c_ip, r_port, c_port, seq=2000, ack=1001, flags=0x12)
            ack = _tcp_packet(c_ip, r_ip, c_port, r_port, seq=1001, ack=2001, flags=0x10)
            data = _tcp_packet(c_ip, r_ip, c_port, r_port, seq=1001, ack=2001, flags=0x18, payload=(payload_token + " tunnel").encode("utf-8"))
            _write_pcap(tn_path, [syn, synack, ack, data])

            evidence_path = base / "artifacts" / "anti_ai" / f"evidence_{sid}.json"
            rc = evidence_main([
                "--challenge", str(challenge_path),
                "--base-dir", str(base),
                "--output", str(evidence_path.relative_to(base)),
                "--artefact", str(report_path.relative_to(base)),
                "--artefact", str(bc_path.relative_to(base)),
                "--artefact", str(mc_path.relative_to(base)),
                "--artefact", str(tn_path.relative_to(base)),
            ])
            self.assertEqual(rc, 0)

            result = validate_submission(
                challenge_path=challenge_path,
                evidence_path=evidence_path,
                base_dir=base,
                verbose=False,
                ignore_expiry=True,
                require_hmac=False,
            )
            self.assertFalse(result.ok)
            joined = "\n".join(result.messages)
            self.assertIn("broadcast PCAP", joined)
