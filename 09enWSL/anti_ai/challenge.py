"""
Challenge model and integrity helpers for Week 9 anti-AI workflow.
"""

from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional


def _canonical_json(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_utc_iso(value: str) -> datetime:
    """
    Parse an ISO-8601 timestamp.

    Supports both '+00:00' and 'Z' suffixes.
    """
    v = value.strip()
    if v.endswith("Z"):
        v = v[:-1] + "+00:00"
    return datetime.fromisoformat(v).astimezone(timezone.utc)


@dataclass(frozen=True)
class Challenge:
    schema_version: int
    course: str
    week: int
    student_id: str
    issued_at_utc: str
    expires_at_utc: str
    ttl_seconds: int
    seed: str
    payload_token: str
    report_token: str
    expected_control_port: int
    integrity_sha256: str
    integrity_hmac_sha256: str = ""

    @property
    def issued_at(self) -> datetime:
        return parse_utc_iso(self.issued_at_utc)

    @property
    def expires_at(self) -> datetime:
        return parse_utc_iso(self.expires_at_utc)

    def is_expired_at(self, when_utc: datetime) -> bool:
        return when_utc > self.expires_at

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "course": self.course,
            "week": self.week,
            "student_id": self.student_id,
            "issued_at_utc": self.issued_at_utc,
            "expires_at_utc": self.expires_at_utc,
            "ttl_seconds": self.ttl_seconds,
            "seed": self.seed,
            "tokens": {
                "payload_token": self.payload_token,
                "report_token": self.report_token,
            },
            "constraints": {
                "expected_control_port": self.expected_control_port,
            },
            "integrity": {
                "sha256": self.integrity_sha256,
                "hmac_sha256": self.integrity_hmac_sha256,
            },
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Challenge":
        tokens = data.get("tokens", {}) or {}
        constraints = data.get("constraints", {}) or {}
        integrity = data.get("integrity", {}) or {}

        return cls(
            schema_version=int(data.get("schema_version", 1)),
            course=str(data.get("course", "NETWORKING")),
            week=int(data.get("week", 9)),
            student_id=str(data.get("student_id", "")),
            issued_at_utc=str(data.get("issued_at_utc", "")),
            expires_at_utc=str(data.get("expires_at_utc", "")),
            ttl_seconds=int(data.get("ttl_seconds", 0)),
            seed=str(data.get("seed", "")),
            payload_token=str(tokens.get("payload_token", "")),
            report_token=str(tokens.get("report_token", "")),
            expected_control_port=int(constraints.get("expected_control_port", 0)),
            integrity_sha256=str(integrity.get("sha256", "")),
            integrity_hmac_sha256=str(integrity.get("hmac_sha256", "")),
        )


def compute_integrity_sha256(challenge_obj: dict[str, Any]) -> str:
    """
    Compute SHA-256 over a canonical JSON representation with `integrity` removed.
    """
    clean = dict(challenge_obj)
    clean.pop("integrity", None)
    return sha256_hex(_canonical_json(clean))


def compute_hmac_sha256(challenge_obj: dict[str, Any], secret: str) -> str:
    clean = dict(challenge_obj)
    clean.pop("integrity", None)
    msg = _canonical_json(clean)
    return hmac.new(secret.encode("utf-8"), msg=msg, digestmod=hashlib.sha256).hexdigest()


def load_challenge(path: Path) -> Challenge:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("Challenge file must contain a JSON object")
    return Challenge.from_dict(raw)


def save_challenge(path: Path, challenge_obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(challenge_obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_challenge(
    student_id: str,
    ttl_seconds: int,
    seed: str,
    payload_token: str,
    report_token: str,
    expected_control_port: int,
    course: str = "NETWORKING",
    week: int = 9,
    secret: Optional[str] = None,
) -> dict[str, Any]:
    issued = datetime.now(timezone.utc)
    expires = issued + timedelta(seconds=ttl_seconds)

    obj = {
        "schema_version": 1,
        "course": course,
        "week": week,
        "student_id": student_id,
        "issued_at_utc": issued.isoformat(timespec="seconds"),
        "expires_at_utc": expires.isoformat(timespec="seconds"),
        "ttl_seconds": ttl_seconds,
        "seed": seed,
        "tokens": {
            "payload_token": payload_token,
            "report_token": report_token,
        },
        "constraints": {
            "expected_control_port": expected_control_port,
        },
    }

    obj["integrity"] = {"sha256": compute_integrity_sha256(obj), "hmac_sha256": ""}
    if secret:
        obj["integrity"]["hmac_sha256"] = compute_hmac_sha256(obj, secret)

    return obj
