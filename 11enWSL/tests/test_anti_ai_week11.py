#!/usr/bin/env python3
"""Unit tests for the Week 11 anti-AI validator.

These tests do not require Docker or network access.
"""

from __future__ import annotations

import json
import os
import tempfile
from hashlib import sha256
from pathlib import Path

import unittest

PROJECT_ROOT = Path(__file__).parent.parent
import sys
sys.path.insert(0, str(PROJECT_ROOT))

from anti_ai.challenge import generate_challenge
from anti_ai.week11_validator import validate_week11


def _write_pcap_with_payload(path: Path, payload: bytes) -> None:
    """Write a minimal classic pcap file containing a single packet record."""
    # Classic pcap global header (little-endian)
    # magic, version_major, version_minor, thiszone, sigfigs, snaplen, network
    global_header = (
        b"\xd4\xc3\xb2\xa1"  # magic
        + (2).to_bytes(2, 'little')
        + (4).to_bytes(2, 'little')
        + (0).to_bytes(4, 'little')
        + (0).to_bytes(4, 'little')
        + (65535).to_bytes(4, 'little')
        + (1).to_bytes(4, 'little')
    )

    incl_len = len(payload)
    record_header = (
        (0).to_bytes(4, 'little')  # ts_sec
        + (0).to_bytes(4, 'little')  # ts_usec
        + incl_len.to_bytes(4, 'little')
        + incl_len.to_bytes(4, 'little')
    )

    path.write_bytes(global_header + record_header + payload)


class TestAntiAIWeek11(unittest.TestCase):
    def test_validator_passes_on_valid_capture(self) -> None:
        challenge = generate_challenge(week=11, student_id='s1', ttl_minutes=60, min_http_requests=2, min_distinct_backends=2)
        token = challenge['token']
        header_name = challenge['requirements']['http_header_name']
        dns_name = challenge['requirements']['dns_query_name']

        payload = (
            f"GET / HTTP/1.1\r\nHost: localhost\r\n{header_name}: {token}\r\n\r\n".encode('ascii')
            + b"HTTP/1.1 200 OK\r\nX-Served-By: 172.18.0.2:80\r\nX-netENwsl-Week: 11\r\n\r\n"
            + b"Backend 1\n"
            + f"GET / HTTP/1.1\r\nHost: localhost\r\n{header_name}: {token}\r\n\r\n".encode('ascii')
            + b"HTTP/1.1 200 OK\r\nX-Served-By: 172.18.0.3:80\r\nX-netENwsl-Week: 11\r\n\r\n"
            + b"Backend 2\n"
            + dns_name.encode('ascii')
        )

        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            ch_path = td_path / 'challenge.json'
            ev_path = td_path / 'evidence.json'
            pcap_path = td_path / 'capture.pcap'

            ch_path.write_text(json.dumps(challenge), encoding='utf-8')
            _write_pcap_with_payload(pcap_path, payload)

            pcap_sha = sha256(pcap_path.read_bytes()).hexdigest()
            evidence = {
                'challenge_id': challenge['challenge_id'],
                'token': token,
                'pcap_sha256': pcap_sha,
            }
            ev_path.write_text(json.dumps(evidence), encoding='utf-8')

            result = validate_week11(challenge_path=ch_path, evidence_path=ev_path, pcap_path=pcap_path)
            self.assertTrue(result.ok, msg=f"Expected PASS but got errors: {result.errors}")

    def test_validator_fails_when_token_missing(self) -> None:
        challenge = generate_challenge(week=11, student_id='s1', ttl_minutes=60, min_http_requests=1, min_distinct_backends=1)
        token = challenge['token']

        payload = b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"  # no token

        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            ch_path = td_path / 'challenge.json'
            ev_path = td_path / 'evidence.json'
            pcap_path = td_path / 'capture.pcap'

            ch_path.write_text(json.dumps(challenge), encoding='utf-8')
            _write_pcap_with_payload(pcap_path, payload)

            pcap_sha = sha256(pcap_path.read_bytes()).hexdigest()
            evidence = {
                'challenge_id': challenge['challenge_id'],
                'token': token,
                'pcap_sha256': pcap_sha,
            }
            ev_path.write_text(json.dumps(evidence), encoding='utf-8')

            result = validate_week11(challenge_path=ch_path, evidence_path=ev_path, pcap_path=pcap_path)
            self.assertFalse(result.ok)
            self.assertIn('Token not found in capture', result.errors)


if __name__ == '__main__':
    unittest.main()
