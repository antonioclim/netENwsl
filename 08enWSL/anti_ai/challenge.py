"""Challenge definitions for Week 8 anti-AI workflow."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Optional


SCHEMA_VERSION = "networking.anti_ai.challenge.v1"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class Challenge:
    """A student-specific challenge.

    The challenge is derived from the generated student context, with a short
    time-to-live so artefacts are harder to reuse.
    """

    schema: str
    week: str
    issued_at_utc: str
    expires_at_utc: str
    ttl_seconds: int
    student_id: str
    student_hash: str
    context_sha256: str
    http_port: int
    secret_header_name: str
    secret_header_value: str
    required_captures: Dict[str, Any]
    signature: Optional[str] = None

    def as_dict(self) -> Dict[str, Any]:
        return {
            "schema": self.schema,
            "week": self.week,
            "issued_at_utc": self.issued_at_utc,
            "expires_at_utc": self.expires_at_utc,
            "ttl_seconds": self.ttl_seconds,
            "student_id": self.student_id,
            "student_hash": self.student_hash,
            "context_sha256": self.context_sha256,
            "http_port": self.http_port,
            "secret_header_name": self.secret_header_name,
            "secret_header_value": self.secret_header_value,
            "required_captures": self.required_captures,
            "signature": self.signature,
        }

    def is_expired(self, now: Optional[datetime] = None) -> bool:
        now_dt = now or datetime.now(timezone.utc)
        expires_dt = datetime.fromisoformat(self.expires_at_utc)
        return now_dt > expires_dt


def challenge_from_context(
    *,
    week: str,
    student_context: Dict[str, Any],
    context_sha256: str,
    ttl: timedelta = timedelta(hours=12),
    signature: Optional[str] = None,
) -> Challenge:
    """Create a Challenge from an existing student context."""

    issued = datetime.now(timezone.utc)
    expires = issued + ttl

    http_server = student_context.get("http_server") or {}

    return Challenge(
        schema=SCHEMA_VERSION,
        week=week,
        issued_at_utc=issued.isoformat(),
        expires_at_utc=expires.isoformat(),
        ttl_seconds=int(ttl.total_seconds()),
        student_id=str(student_context.get("student_id", "")),
        student_hash=str(student_context.get("student_hash", "")),
        context_sha256=context_sha256,
        http_port=int(http_server.get("port", 0)),
        secret_header_name=str(http_server.get("secret_header_name", "")),
        secret_header_value=str(http_server.get("secret_header_value", "")),
        required_captures=dict(student_context.get("required_captures", {})),
        signature=signature,
    )


def save_challenge(challenge: Challenge, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(challenge.as_dict(), indent=2), encoding="utf-8")


def load_challenge(path: Path) -> Challenge:
    data = json.loads(path.read_text(encoding="utf-8"))
    return Challenge(
        schema=data["schema"],
        week=data["week"],
        issued_at_utc=data["issued_at_utc"],
        expires_at_utc=data["expires_at_utc"],
        ttl_seconds=int(data["ttl_seconds"]),
        student_id=data["student_id"],
        student_hash=data["student_hash"],
        context_sha256=data["context_sha256"],
        http_port=int(data["http_port"]),
        secret_header_name=data["secret_header_name"],
        secret_header_value=data["secret_header_value"],
        required_captures=dict(data.get("required_captures") or {}),
        signature=data.get("signature"),
    )
