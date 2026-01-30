#!/usr/bin/env python3
"""Challenge file model and helpers.

The challenge is a small YAML document intended to be:
- unique per student (seeded by student id)
- time-bounded (validity window)
- tied to verifiable artefacts (tokens that must appear in captures and reports)

The challenge can optionally include an HMAC integrity tag. The HMAC key should be
provided via an environment variable in CI. If the key is not available the
validator falls back to a plain SHA-256 integrity check, which protects against
accidental corruption but not against a determined adversary.

This module depends only on PyYAML which is already used elsewhere in the kit.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import hashlib
import hmac
import json

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required. Install it with: pip install pyyaml") from exc


def utc_now_iso() -> str:
    """Return a timezone-aware UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def canonical_json(data: dict[str, Any]) -> str:
    """Serialise *data* deterministically for hashing and signing."""
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_hex(data: str | bytes) -> str:
    """Compute a SHA-256 hex digest for *data* (string or bytes)."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def hmac_sha256_hex(key: str, message: str) -> str:
    """Compute an HMAC-SHA256 hex digest."""
    mac = hmac.new(key.encode("utf-8"), message.encode("utf-8"), hashlib.sha256)
    return mac.hexdigest()


@dataclass(frozen=True, slots=True)
class Challenge:
    """In-memory representation of a Week 3 challenge."""

    week: int
    student_id: str
    issued_at_utc: str
    valid_for_hours: int

    payload_token: str
    report_token: str

    broadcast_port: int
    multicast_group: str
    multicast_port: int
    tunnel_listen_port: int

    integrity_sha256: str
    integrity_hmac: str | None = None

    def issued_at(self) -> datetime:
        """Return the issue timestamp as a timezone-aware datetime."""
        issued = datetime.fromisoformat(self.issued_at_utc)
        if issued.tzinfo is None:
            issued = issued.replace(tzinfo=timezone.utc)
        return issued.astimezone(timezone.utc)

    def expires_at(self) -> datetime:
        """Return the expiry timestamp as a timezone-aware datetime."""
        return self.issued_at() + timedelta(hours=self.valid_for_hours)

    def to_payload(self) -> dict[str, Any]:
        """Return the canonical payload that is signed and hashed."""
        return {
            "meta": {
                "week": self.week,
                "student_id": self.student_id,
                "issued_at_utc": self.issued_at_utc,
                "valid_for_hours": self.valid_for_hours,
            },
            "tokens": {
                "payload_token": self.payload_token,
                "report_token": self.report_token,
            },
            "recommended": {
                "broadcast": {"port": self.broadcast_port},
                "multicast": {"group": self.multicast_group, "port": self.multicast_port},
                "tunnel": {"listen_port": self.tunnel_listen_port},
            },
        }

    def to_dict(self) -> dict[str, Any]:
        """Serialise to a YAML-friendly dictionary."""
        d = self.to_payload()
        d["integrity"] = {
            "sha256": self.integrity_sha256,
            "hmac_sha256": self.integrity_hmac,
            "hmac_env_var": "ANTI_AI_HMAC_KEY",
        }
        return d


def compute_integrity(payload: dict[str, Any], hmac_key: str | None) -> tuple[str, str | None]:
    """Compute integrity tags for *payload*.

    Returns (sha256, hmac_sha256_or_none).
    """
    canon = canonical_json(payload)
    sha = sha256_hex(canon)
    mac = hmac_sha256_hex(hmac_key, canon) if hmac_key else None
    return sha, mac


def load_challenge(path: str | Path) -> Challenge:
    """Load a challenge YAML file."""
    path = Path(path)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Challenge file is not a mapping")

    meta = data.get("meta") or {}
    tokens = data.get("tokens") or {}
    rec = data.get("recommended") or {}
    integ = data.get("integrity") or {}

    broadcast = rec.get("broadcast") or {}
    multicast = rec.get("multicast") or {}
    tunnel = rec.get("tunnel") or {}

    return Challenge(
        week=int(meta["week"]),
        student_id=str(meta["student_id"]),
        issued_at_utc=str(meta["issued_at_utc"]),
        valid_for_hours=int(meta["valid_for_hours"]),
        payload_token=str(tokens["payload_token"]),
        report_token=str(tokens["report_token"]),
        broadcast_port=int(broadcast["port"]),
        multicast_group=str(multicast["group"]),
        multicast_port=int(multicast["port"]),
        tunnel_listen_port=int(tunnel["listen_port"]),
        integrity_sha256=str(integ.get("sha256", "")),
        integrity_hmac=(str(integ["hmac_sha256"]) if integ.get("hmac_sha256") else None),
    )


def save_challenge(challenge: Challenge, path: str | Path) -> None:
    """Save a challenge YAML file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(challenge.to_dict(), f, sort_keys=False)


def verify_integrity(challenge: Challenge, hmac_key: str | None) -> tuple[bool, str]:
    """Verify SHA-256 and optionally HMAC integrity tags.

    Returns (ok, message).
    """
    payload = challenge.to_payload()
    canon = canonical_json(payload)
    expected_sha = sha256_hex(canon)
    if expected_sha != challenge.integrity_sha256:
        return False, "Challenge SHA-256 does not match. The file may be corrupted."

    if hmac_key:
        expected_hmac = hmac_sha256_hex(hmac_key, canon)
        if challenge.integrity_hmac != expected_hmac:
            return False, "Challenge HMAC does not match. The file may be tampered with."
        return True, "Integrity verified (SHA-256 and HMAC)."

    return True, "Integrity verified (SHA-256). No HMAC key was provided."
