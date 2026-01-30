#!/usr/bin/env python3
"""
Anti-AI workflow tests (Week 4).

These tests validate that:
- challenges can be generated
- evidence can be collected
- submissions can be validated using a synthetic PCAP
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

from anti_ai.challenge_generator import generate_week04_challenge
from scripts.generate_pcap_samples import (
    PCAPWriter,
    TCP_ACK,
    TCP_PSH,
    ETH_TYPE_IPV4,
    IP_PROTO_TCP,
    IP_PROTO_UDP,
    build_ethernet_header,
    build_ip_header,
    build_tcp_header,
    build_udp_header,
)
from src.utils.proto_common import TYPE_PUT_REQ, encode_kv, pack_bin_message, pack_udp_sensor


def _tcp_frame(payload: bytes, src_port: int, dst_port: int) -> bytes:
    src_mac = b"\xaa\xbb\xcc\xdd\xee\x01"
    dst_mac = b"\xaa\xbb\xcc\xdd\xee\x02"
    eth = build_ethernet_header(src_mac, dst_mac, ETH_TYPE_IPV4)

    tcp = build_tcp_header(
        src_port=src_port,
        dst_port=dst_port,
        seq=1000,
        ack=0,
        flags=TCP_PSH | TCP_ACK,
        payload=payload,
    )
    ip = build_ip_header("10.0.0.2", "10.0.0.1", IP_PROTO_TCP, len(tcp))
    return eth + ip + tcp


def _udp_frame(payload: bytes, src_port: int, dst_port: int) -> bytes:
    src_mac = b"\xaa\xbb\xcc\xdd\xee\x03"
    dst_mac = b"\xaa\xbb\xcc\xdd\xee\x04"
    eth = build_ethernet_header(src_mac, dst_mac, ETH_TYPE_IPV4)

    udp = build_udp_header(src_port, dst_port, payload)
    ip = build_ip_header("10.0.0.2", "10.0.0.1", IP_PROTO_UDP, len(udp))
    return eth + ip + udp


def test_week04_validator_accepts_synthetic_pcap(tmp_path: Path) -> None:
    # Generate a challenge
    ch = generate_week04_challenge(student_id="s12345", host="localhost", ttl_hours=24.0)

    ch_path = tmp_path / "challenge.yaml"
    ch_path.write_text(yaml.safe_dump(ch, sort_keys=False), encoding="utf-8")

    # Build a PCAP that includes all required tokens
    pcap_path = tmp_path / "capture.pcap"
    w = PCAPWriter(str(pcap_path))

    # TEXT: framed message carrying token
    cmd = f"SET anti_ai {ch['text_token']}".encode("utf-8")
    framed = f"{len(cmd)} ".encode("ascii") + cmd
    w.add_packet(_tcp_frame(framed, src_port=40000, dst_port=int(ch["text_port"])))

    # BINARY: PUT_REQ with token, CRC verified by validator
    payload = encode_kv("anti_ai", ch["binary_token"])
    msg = pack_bin_message(TYPE_PUT_REQ, payload, seq=1)
    w.add_packet(_tcp_frame(msg, src_port=40001, dst_port=int(ch["binary_port"])))

    # UDP sensor: CRC verified by validator
    udp_payload = pack_udp_sensor(int(ch["udp_sensor_id"]), 21.5, ch["udp_location_tag"])
    w.add_packet(_udp_frame(udp_payload, src_port=40002, dst_port=int(ch["udp_port"])))

    w.write()

    # Collect evidence using the CLI to exercise the public interface
    evidence_path = tmp_path / "evidence.json"
    project_root = Path(__file__).parent.parent

    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "anti_ai.evidence_collector",
            "--challenge",
            str(ch_path.relative_to(tmp_path)),
            "--artefact",
            str(ch_path.relative_to(tmp_path)),
            "--artefact",
            str(pcap_path.relative_to(tmp_path)),
            "--output",
            str(evidence_path.relative_to(tmp_path)),
            "--base-dir",
            str(tmp_path),
        ],
        cwd=project_root,
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, res.stdout + "\n" + res.stderr

    # Validate evidence and PCAP tokens
    res2 = subprocess.run(
        [
            sys.executable,
            "-m",
            "anti_ai.submission_validator",
            "--challenge",
            str(ch_path),
            "--evidence",
            str(evidence_path),
            "--base-dir",
            str(tmp_path),
        ],
        cwd=project_root,
        capture_output=True,
        text=True,
    )
    assert res2.returncode == 0, res2.stdout + "\n" + res2.stderr


def test_week04_validator_rejects_wrong_token(tmp_path: Path) -> None:
    ch = generate_week04_challenge(student_id="s12345", host="localhost", ttl_hours=24.0)
    ch_path = tmp_path / "challenge.yaml"
    ch_path.write_text(yaml.safe_dump(ch, sort_keys=False), encoding="utf-8")

    # PCAP missing the binary token
    pcap_path = tmp_path / "capture.pcap"
    w = PCAPWriter(str(pcap_path))

    cmd = f"SET anti_ai {ch['text_token']}".encode("utf-8")
    framed = f"{len(cmd)} ".encode("ascii") + cmd
    w.add_packet(_tcp_frame(framed, src_port=40000, dst_port=int(ch["text_port"])))

    # Wrong binary token
    payload = encode_kv("anti_ai", "W4B-deadbeef")
    msg = pack_bin_message(TYPE_PUT_REQ, payload, seq=1)
    w.add_packet(_tcp_frame(msg, src_port=40001, dst_port=int(ch["binary_port"])))

    udp_payload = pack_udp_sensor(int(ch["udp_sensor_id"]), 21.5, ch["udp_location_tag"])
    w.add_packet(_udp_frame(udp_payload, src_port=40002, dst_port=int(ch["udp_port"])))

    w.write()

    evidence_path = tmp_path / "evidence.json"
    project_root = Path(__file__).parent.parent

    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "anti_ai.evidence_collector",
            "--challenge",
            str(ch_path.relative_to(tmp_path)),
            "--artefact",
            str(ch_path.relative_to(tmp_path)),
            "--artefact",
            str(pcap_path.relative_to(tmp_path)),
            "--output",
            str(evidence_path.relative_to(tmp_path)),
            "--base-dir",
            str(tmp_path),
        ],
        cwd=project_root,
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, res.stdout + "\n" + res.stderr

    res2 = subprocess.run(
        [
            sys.executable,
            "-m",
            "anti_ai.submission_validator",
            "--challenge",
            str(ch_path),
            "--evidence",
            str(evidence_path),
            "--base-dir",
            str(tmp_path),
        ],
        cwd=project_root,
        capture_output=True,
        text=True,
    )
    assert res2.returncode != 0
