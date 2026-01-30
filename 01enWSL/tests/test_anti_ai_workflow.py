#!/usr/bin/env python3
"""Tests for the Week 1 anti-AI workflow.

These tests intentionally avoid Docker and privileged operations. They generate
small synthetic PCAP files using dpkt so the validator can be tested in a
portable way.
"""

from __future__ import annotations

import socket
from pathlib import Path
from typing import Any

import dpkt

from anti_ai.challenge_generator import generate_challenge
from anti_ai.evidence_collector import build_evidence, write_evidence_json
from anti_ai.submission_validator import SubmissionValidator


def _ip_bytes(ip: str) -> bytes:
    return socket.inet_aton(ip)


def _tcp_packet(
    *,
    src: str,
    dst: str,
    sport: int,
    dport: int,
    seq: int,
    ack: int,
    flags: int,
    payload: bytes = b"",
) -> bytes:
    tcp = dpkt.tcp.TCP(
        sport=sport,
        dport=dport,
        seq=seq,
        ack=ack,
        flags=flags,
        win=8192,
        data=payload,
    )
    tcp.off = 5

    ip = dpkt.ip.IP(src=_ip_bytes(src), dst=_ip_bytes(dst), p=dpkt.ip.IP_PROTO_TCP, ttl=64)
    ip.data = tcp
    ip.len = len(ip)

    return bytes(ip)


def _udp_packet(*, src: str, dst: str, sport: int, dport: int, payload: bytes) -> bytes:
    udp = dpkt.udp.UDP(sport=sport, dport=dport, data=payload)
    udp.ulen = len(udp)

    ip = dpkt.ip.IP(src=_ip_bytes(src), dst=_ip_bytes(dst), p=dpkt.ip.IP_PROTO_UDP, ttl=64)
    ip.data = udp
    ip.len = len(ip)

    return bytes(ip)


def _write_minimal_tcp_pcap(path: Path, payload_token: str) -> None:
    client = "127.0.0.1"
    server = "127.0.0.1"
    sport = 50000
    dport = 10001

    syn = _tcp_packet(src=client, dst=server, sport=sport, dport=dport, seq=100, ack=0, flags=dpkt.tcp.TH_SYN)
    synack = _tcp_packet(
        src=server,
        dst=client,
        sport=dport,
        dport=sport,
        seq=200,
        ack=101,
        flags=dpkt.tcp.TH_SYN | dpkt.tcp.TH_ACK,
    )
    ack = _tcp_packet(
        src=client,
        dst=server,
        sport=sport,
        dport=dport,
        seq=101,
        ack=201,
        flags=dpkt.tcp.TH_ACK,
    )
    data = _tcp_packet(
        src=client,
        dst=server,
        sport=sport,
        dport=dport,
        seq=101,
        ack=201,
        flags=dpkt.tcp.TH_ACK | dpkt.tcp.TH_PUSH,
        payload=(f"MSG|{payload_token}\n").encode("utf-8"),
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        writer = dpkt.pcap.Writer(f, linktype=getattr(dpkt.pcap, "DLT_RAW", 101))
        ts = 1.0
        for pkt in (syn, synack, ack, data):
            writer.writepkt(pkt, ts=ts)
            ts += 0.05


def _write_minimal_udp_pcap(path: Path, payload_token: str) -> None:
    client = "127.0.0.1"
    server = "127.0.0.1"
    sport = 50001
    dport = 10002

    pkt = _udp_packet(
        src=client,
        dst=server,
        sport=sport,
        dport=dport,
        payload=(f"MSG|{payload_token}\n").encode("utf-8"),
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        writer = dpkt.pcap.Writer(f, linktype=getattr(dpkt.pcap, "DLT_RAW", 101))
        writer.writepkt(pkt, ts=1.0)


def test_end_to_end_validation(tmp_path: Path) -> None:
    # 1) Generate challenge
    challenge: dict[str, Any] = generate_challenge("ABC123", valid_hours=24)

    # 2) Write challenge to YAML
    challenge_path = tmp_path / "artifacts" / "anti_ai" / "challenge_ABC123.yaml"
    challenge_path.parent.mkdir(parents=True, exist_ok=True)

    import yaml  # imported here to keep test imports minimal

    challenge_path.write_text(yaml.safe_dump(challenge, sort_keys=False), encoding="utf-8")

    # 3) Create artefacts
    report_path = tmp_path / "network_report.md"
    report_token = challenge["challenges"]["report"]["token"]
    report_path.write_text(f"# Report\n\nToken: {report_token}\n", encoding="utf-8")

    payload = challenge["challenges"]["pcap"]["payload_token"]
    tcp_pcap = tmp_path / "tcp_analysis.pcap"
    udp_pcap = tmp_path / "udp_analysis.pcap"
    _write_minimal_tcp_pcap(tcp_pcap, payload)
    _write_minimal_udp_pcap(udp_pcap, payload)

    # 4) Build evidence
    evidence = build_evidence(
        challenge=challenge,
        artefacts=[report_path, tcp_pcap, udp_pcap],
        base_dir=tmp_path,
        include_commands=False,
    )
    evidence_path = tmp_path / "evidence.json"
    write_evidence_json(evidence, evidence_path)

    # 5) Validate
    validator = SubmissionValidator(
        challenge_file=challenge_path,
        evidence_file=evidence_path,
        base_dir=tmp_path,
        verbose=False,
    )
    report = validator.validate_all()

    assert report.all_passed, report.to_dict()


def test_report_token_missing_fails(tmp_path: Path) -> None:
    challenge: dict[str, Any] = generate_challenge("ABC123", valid_hours=24)

    challenge_path = tmp_path / "challenge.yaml"
    import yaml

    challenge_path.write_text(yaml.safe_dump(challenge, sort_keys=False), encoding="utf-8")

    report_path = tmp_path / "network_report.md"
    report_path.write_text("# Report without token\n", encoding="utf-8")

    payload = challenge["challenges"]["pcap"]["payload_token"]
    tcp_pcap = tmp_path / "tcp_analysis.pcap"
    udp_pcap = tmp_path / "udp_analysis.pcap"
    _write_minimal_tcp_pcap(tcp_pcap, payload)
    _write_minimal_udp_pcap(udp_pcap, payload)

    evidence = build_evidence(
        challenge=challenge,
        artefacts=[report_path, tcp_pcap, udp_pcap],
        base_dir=tmp_path,
        include_commands=False,
    )
    evidence_path = tmp_path / "evidence.json"
    write_evidence_json(evidence, evidence_path)

    validator = SubmissionValidator(
        challenge_file=challenge_path,
        evidence_file=evidence_path,
        base_dir=tmp_path,
        verbose=False,
    )
    report = validator.validate_all()

    assert not report.all_passed
    assert any(r.name == "report_token" and not r.passed for r in report.results)
