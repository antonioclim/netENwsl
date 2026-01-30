"""Week 11 anti-AI validator.

Week 11 is about load balancing and DNS therefore validation focuses on
captured traffic.

Inputs
------
- challenge JSON (issued by staff)
- evidence JSON (produced by the student)
- pcap/pcapng file (captured while running the required interactions)

What is validated
-----------------
- challenge TTL (expires_at)
- token consistency (challenge vs evidence vs traffic)
- pcap integrity (SHA-256 matches evidence)
- minimum number of HTTP requests carrying the challenge header
- evidence that more than one backend handled traffic (via X-Served-By or X-Backend-ID)
- DNS query name containing the token present in traffic
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .challenge import is_challenge_expired, verify_challenge_signature
from .pcap_tools import extract_packet_bytes


@dataclass
class ValidationResult:
    ok: bool
    errors: List[str]
    warnings: List[str]
    metrics: Dict[str, Any]


def _sha256_file(path: Path) -> str:
    h = sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def _lower_headers_bytes(data: bytes) -> bytes:
    # HTTP header names are ASCII; lowercasing bytes simplifies matching
    return data.lower()


def _count_occurrences(haystack: bytes, needle: bytes) -> int:
    if not needle:
        return 0
    count = 0
    start = 0
    while True:
        idx = haystack.find(needle, start)
        if idx == -1:
            return count
        count += 1
        start = idx + len(needle)


def _extract_header_values(data: bytes, header_name: str) -> List[str]:
    # header_name should be lower-case already
    values: List[str] = []
    pattern = re.compile(rb"\r\n" + re.escape(header_name.encode('ascii')) + rb":\s*([^\r\n]+)")
    for m in pattern.finditer(data):
        try:
            values.append(m.group(1).decode('utf-8', errors='replace').strip())
        except Exception:
            continue
    return values


def validate_week11(
    *,
    challenge_path: str | Path,
    evidence_path: str | Path,
    pcap_path: str | Path,
    secret: Optional[str] = None,
) -> ValidationResult:
    """Validate Week 11 submission artefacts."""

    errors: List[str] = []
    warnings: List[str] = []
    metrics: Dict[str, Any] = {}

    challenge_p = Path(challenge_path)
    evidence_p = Path(evidence_path)
    pcap_p = Path(pcap_path)

    if not challenge_p.exists():
        return ValidationResult(False, [f"Missing challenge file: {challenge_p}"], [], {})
    if not evidence_p.exists():
        return ValidationResult(False, [f"Missing evidence file: {evidence_p}"], [], {})
    if not pcap_p.exists():
        return ValidationResult(False, [f"Missing capture file: {pcap_p}"], [], {})

    challenge = json.loads(challenge_p.read_text(encoding='utf-8'))
    evidence = json.loads(evidence_p.read_text(encoding='utf-8'))

    if int(challenge.get('week', 0)) != 11:
        errors.append("Challenge is not for Week 11")

    if not verify_challenge_signature(challenge, secret=secret):
        warnings.append("Challenge signature is missing or invalid")

    if is_challenge_expired(challenge):
        errors.append("Challenge has expired (expires_at)")

    # Token consistency
    token = str(challenge.get('token', '')).strip()
    if not token:
        errors.append("Challenge token missing")

    if str(evidence.get('token', '')).strip() != token:
        errors.append("Evidence token does not match challenge token")

    if str(evidence.get('challenge_id', '')).strip() != str(challenge.get('challenge_id', '')).strip():
        errors.append("Evidence challenge_id does not match challenge")

    # PCAP integrity
    actual_hash = _sha256_file(pcap_p)
    declared_hash = str(evidence.get('pcap_sha256', '')).strip()
    metrics['pcap_sha256'] = actual_hash
    if declared_hash and declared_hash != actual_hash:
        errors.append("PCAP SHA-256 does not match evidence")
    if not declared_hash:
        warnings.append("Evidence pcap_sha256 missing")

    # Extract packet bytes and search
    raw_packets = extract_packet_bytes(pcap_p)
    raw_lower = _lower_headers_bytes(raw_packets)

    token_bytes = token.encode('ascii', errors='ignore').lower()
    if token_bytes and token_bytes not in raw_lower:
        errors.append("Token not found in capture")

    req = challenge.get('requirements', {}) or {}
    header_name = str(req.get('http_header_name', 'X-AI-Challenge'))
    header_name_lower = header_name.lower().encode('ascii', errors='ignore')

    # Count token-carrying HTTP headers
    http_header_needle = b"\r\n" + header_name_lower + b": " + token_bytes
    http_token_count = _count_occurrences(raw_lower, http_header_needle)
    metrics['http_token_headers'] = http_token_count

    min_http = int(req.get('min_http_requests', 0) or 0)
    if min_http and http_token_count < min_http:
        errors.append(f"Too few token HTTP requests: {http_token_count} < {min_http}")

    # Backends evidence
    served_by = set(_extract_header_values(raw_lower, 'x-served-by'))
    backend_ids = set(_extract_header_values(raw_lower, 'x-backend-id'))
    metrics['distinct_x_served_by'] = len(served_by)
    metrics['distinct_x_backend_id'] = len(backend_ids)

    distinct = max(len(served_by), len(backend_ids))
    min_backends = int(req.get('min_distinct_backends', 0) or 0)
    if min_backends and distinct < min_backends:
        errors.append(
            f"Too few distinct backends observed: {distinct} < {min_backends}"
        )

    # DNS evidence
    dns_query_name = str(req.get('dns_query_name', '')).strip().lower()
    if dns_query_name:
        dns_bytes = dns_query_name.encode('ascii', errors='ignore')
        if dns_bytes not in raw_lower:
            errors.append("DNS query name not found in capture")

    ok = len(errors) == 0
    return ValidationResult(ok, errors, warnings, metrics)
