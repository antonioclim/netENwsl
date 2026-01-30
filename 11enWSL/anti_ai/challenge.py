"""Challenge format and signing helpers.

This module uses only the Python standard library.

Design goal
-----------
A challenge should be:
- short lived (TTL)
- unique per student / attempt
- verifiable by staff (optional HMAC signature)

If the environment variable ANTI_AI_SECRET is set, challenges are signed and the
validator can detect tampering.
"""

from __future__ import annotations

import hmac
import json
import os
import secrets
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from typing import Any, Dict, Optional


ISO_Z_SUFFIX = "Z"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _isoformat_z(dt: datetime) -> str:
    """Return an ISO 8601 string with a trailing Z."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    dt = dt.astimezone(timezone.utc)
    return dt.isoformat(timespec="seconds").replace("+00:00", ISO_Z_SUFFIX)


def parse_iso8601(value: str) -> datetime:
    """Parse ISO 8601 with optional Z suffix."""
    v = value.strip()
    if v.endswith(ISO_Z_SUFFIX):
        v = v[:-1] + "+00:00"
    return datetime.fromisoformat(v)


def _canonical_json(data: Dict[str, Any]) -> bytes:
    """Canonical JSON bytes for signing."""
    return json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")


def compute_signature(payload: Dict[str, Any], secret: str) -> str:
    """Compute HMAC-SHA256 signature over canonical JSON."""
    mac = hmac.new(secret.encode("utf-8"), _canonical_json(payload), sha256)
    return mac.hexdigest()


def verify_challenge_signature(challenge: Dict[str, Any], secret: Optional[str] = None) -> bool:
    """Verify challenge signature if present.

    Returns True when:
    - no signature is present (unsigned challenge) or
    - signature is present and valid

    Returns False when:
    - signature is present but secret is missing or invalid
    """
    signature = (challenge.get("signature") or "").strip()
    if not signature:
        return True

    secret = secret or os.environ.get("ANTI_AI_SECRET")
    if not secret:
        return False

    payload = dict(challenge)
    payload.pop("signature", None)
    expected = compute_signature(payload, secret)
    return hmac.compare_digest(expected, signature)


def generate_challenge(
    *,
    week: int,
    student_id: str,
    ttl_minutes: int = 45,
    min_http_requests: int = 10,
    min_distinct_backends: int = 2,
    secret: Optional[str] = None,
    now: Optional[datetime] = None,
) -> Dict[str, Any]:
    """Generate a new anti-AI challenge dictionary."""
    if week <= 0:
        raise ValueError("week must be positive")
    if ttl_minutes <= 0:
        raise ValueError("ttl_minutes must be positive")

    now_dt = now or _utc_now()
    issued_at = _isoformat_z(now_dt)
    expires_at = _isoformat_z(now_dt + timedelta(minutes=ttl_minutes))

    seed = secrets.token_hex(16)
    token = secrets.token_hex(12)  # domain-safe

    # Week 11 uses a domain-safe token in a query name to make DNS evidence easy to spot.
    dns_query_name = f"ai-{token}.invalid"

    challenge: Dict[str, Any] = {
        "challenge_id": str(uuid.uuid4()),
        "week": int(week),
        "student_id": str(student_id),
        "issued_at": issued_at,
        "expires_at": expires_at,
        "seed": seed,
        "token": token,
        "requirements": {
            "min_http_requests": int(min_http_requests),
            "min_distinct_backends": int(min_distinct_backends),
            "dns_query_name": dns_query_name,
            "http_header_name": "X-AI-Challenge",
        },
    }

    secret = secret or os.environ.get("ANTI_AI_SECRET")
    if secret:
        payload = dict(challenge)
        challenge["signature"] = compute_signature(payload, secret)

    return challenge


def is_challenge_expired(challenge: Dict[str, Any], now: Optional[datetime] = None) -> bool:
    """Return True if the challenge is expired."""
    now_dt = now or _utc_now()
    expires = parse_iso8601(str(challenge.get("expires_at", "")))
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)
    return now_dt.astimezone(timezone.utc) > expires.astimezone(timezone.utc)
