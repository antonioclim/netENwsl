#!/usr/bin/env python3
"""Generate Week 11 anti-AI evidence.

This script is intended for students.

Typical workflow
----------------
1) Start the required services (your load balancer and backends)
2) Start a capture in another terminal, for example:
   ./scripts/capture_traffic.py --filter "tcp port 8080 or udp port 53" -o pcap/week11_capture.pcap
3) Run this script which sends tokenised HTTP requests and a DNS query
4) Stop the capture then run scripts/anti_ai_validate.py to self-check

The script writes an evidence JSON which the staff validator consumes.
"""

from __future__ import annotations

import argparse
import json
import socket
import sys
import time
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List, Optional
import urllib.request
import urllib.error

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from anti_ai.challenge import parse_iso8601, is_challenge_expired


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _sha256_file(path: Path) -> str:
    h = sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def http_get_with_header(url: str, header_name: str, token: str, timeout: float = 5.0) -> Dict[str, Any]:
    """HTTP GET with a single extra header."""
    start = time.time()
    req = urllib.request.Request(url, method="GET")
    req.add_header('User-Agent', 'Week11-AntiAI/1.0')
    req.add_header(header_name, token)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode('utf-8', errors='replace')
            return {
                'status': resp.status,
                'headers': dict(resp.headers.items()),
                'body': body,
                'latency_ms': (time.time() - start) * 1000,
            }
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        return {
            'status': e.code,
            'headers': dict(e.headers.items()),
            'body': body,
            'latency_ms': (time.time() - start) * 1000,
            'error': 'HTTPError',
        }
    except Exception as e:
        return {
            'status': 0,
            'headers': {},
            'body': '',
            'latency_ms': (time.time() - start) * 1000,
            'error': str(e),
        }


def _build_dns_query(qname: str, qtype: int = 1) -> bytes:
    """Build a minimal DNS query (standard query, one question)."""
    import random

    def encode_name(name: str) -> bytes:
        out = bytearray()
        for label in name.strip('.').split('.'):
            b = label.encode('ascii', errors='ignore')
            out.append(len(b))
            out.extend(b)
        out.append(0)
        return bytes(out)

    txid = random.randint(0, 0xFFFF)
    flags = 0x0100  # recursion desired
    qdcount = 1
    header = txid.to_bytes(2, 'big') + flags.to_bytes(2, 'big') + qdcount.to_bytes(2, 'big') + b"\x00\x00\x00\x00\x00\x00"
    question = encode_name(qname) + qtype.to_bytes(2, 'big') + (1).to_bytes(2, 'big')  # class IN
    return header + question


def send_dns_query(server: str, port: int, qname: str, timeout: float = 3.0) -> Dict[str, Any]:
    """Send a DNS query and return basic metadata."""
    query = _build_dns_query(qname)
    start = time.time()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.sendto(query, (server, port))
            data, _ = sock.recvfrom(4096)
            return {
                'ok': True,
                'bytes': len(data),
                'latency_ms': (time.time() - start) * 1000,
            }
        except Exception as e:
            return {
                'ok': False,
                'error': str(e),
                'latency_ms': (time.time() - start) * 1000,
            }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Week 11 anti-AI evidence")
    parser.add_argument(
        "--challenge",
        default=str(PROJECT_ROOT / "artifacts" / "anti_ai" / "week11_challenge.json"),
        help="Path to challenge JSON",
    )
    parser.add_argument(
        "--pcap",
        default=str(PROJECT_ROOT / "pcap" / "week11_capture.pcap"),
        help="Path to capture file you created (pcap)",
    )
    parser.add_argument(
        "--lb-url",
        default="http://localhost:8080/",
        help="Load balancer URL",
    )
    parser.add_argument(
        "--requests",
        type=int,
        default=12,
        help="Number of HTTP requests to send",
    )
    parser.add_argument("--dns-server", default="8.8.8.8", help="DNS server to query")
    parser.add_argument("--dns-port", type=int, default=53, help="DNS server port")
    parser.add_argument(
        "--out",
        default=str(PROJECT_ROOT / "artifacts" / "anti_ai" / "week11_evidence.json"),
        help="Output path for evidence JSON",
    )

    args = parser.parse_args()

    challenge_path = Path(args.challenge)
    if not challenge_path.exists():
        print(f"Challenge not found: {challenge_path}", file=sys.stderr)
        return 2

    challenge = json.loads(challenge_path.read_text(encoding="utf-8"))
    if int(challenge.get('week', 0)) != 11:
        print("Challenge is not for Week 11", file=sys.stderr)
        return 2

    if is_challenge_expired(challenge):
        print("Challenge has expired. Ask the instructor for a new one.", file=sys.stderr)
        return 3

    req = challenge.get('requirements', {}) or {}
    token = str(challenge.get('token', '')).strip()
    header_name = str(req.get('http_header_name', 'X-AI-Challenge'))
    dns_name = str(req.get('dns_query_name', '')).strip()

    http_results: List[Dict[str, Any]] = []
    for _ in range(max(1, int(args.requests))):
        http_results.append(http_get_with_header(args.lb_url, header_name, token))

    # Minimal extraction of backend indicators
    backends = set()
    served_by = set()
    for r in http_results:
        headers = {k.lower(): v for k, v in (r.get('headers') or {}).items()}
        if 'x-backend-id' in headers:
            backends.add(str(headers['x-backend-id']).strip())
        if 'x-served-by' in headers:
            served_by.add(str(headers['x-served-by']).strip())

    dns_result = {}
    if dns_name:
        dns_result = send_dns_query(args.dns_server, int(args.dns_port), dns_name)

    pcap_path = Path(args.pcap)
    pcap_sha = ""
    if pcap_path.exists():
        pcap_sha = _sha256_file(pcap_path)
    else:
        print(f"Warning: capture file not found at {pcap_path}. You can still submit but validation will fail.")

    evidence = {
        'challenge_id': str(challenge.get('challenge_id', '')).strip(),
        'token': token,
        'created_at': _utc_now_iso(),
        'lb_url': args.lb_url,
        'http_requests_sent': len(http_results),
        'http_successful': sum(1 for r in http_results if int(r.get('status', 0)) == 200),
        'distinct_x_backend_id': sorted(backends),
        'distinct_x_served_by': sorted(served_by),
        'dns_query_name': dns_name,
        'dns_server': args.dns_server,
        'dns_port': int(args.dns_port),
        'dns_ok': bool(dns_result.get('ok')) if dns_result else False,
        'pcap_path': str(pcap_path),
        'pcap_sha256': pcap_sha,
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(evidence, indent=2, sort_keys=True), encoding='utf-8')

    print(f"Wrote evidence: {out_path}")
    if dns_result:
        print(f"DNS query: {dns_name} -> ok={dns_result.get('ok')} latency_ms={dns_result.get('latency_ms'):.2f}")
    print(f"HTTP requests sent: {len(http_results)} successful={evidence['http_successful']}")

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
