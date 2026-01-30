"""Challenge format for the Week 7 anti-AI workflow."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _parse_utc(ts: str) -> datetime:
    # Expected format: ISO 8601 with trailing Z or offset
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    return datetime.fromisoformat(ts)


def _iso_utc(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class AntiAIChallenge:
    """A per-student, per-attempt challenge."""

    week_id: int
    student_id: str
    attempt_id: str
    issued_at_utc: str
    ttl_seconds: int
    report_token: str
    payload_token: str
    tcp_port: int = 9090
    udp_port: int = 9091
    challenge_hash: str = ""

    @property
    def issued_at(self) -> datetime:
        return _parse_utc(self.issued_at_utc)

    @property
    def valid_until(self) -> datetime:
        return self.issued_at + timedelta(seconds=self.ttl_seconds)

    def is_expired(self, now: Optional[datetime] = None) -> bool:
        now = now or _utc_now()
        return now > self.valid_until

    def to_dict(self) -> Dict[str, Any]:
        return {
            "week_id": self.week_id,
            "student_id": self.student_id,
            "attempt_id": self.attempt_id,
            "issued_at_utc": self.issued_at_utc,
            "ttl_seconds": self.ttl_seconds,
            "report_token": self.report_token,
            "payload_token": self.payload_token,
            "tcp_port": self.tcp_port,
            "udp_port": self.udp_port,
            "challenge_hash": self.challenge_hash,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "AntiAIChallenge":
        return cls(
            week_id=int(d["week_id"]),
            student_id=str(d["student_id"]),
            attempt_id=str(d["attempt_id"]),
            issued_at_utc=str(d["issued_at_utc"]),
            ttl_seconds=int(d["ttl_seconds"]),
            report_token=str(d["report_token"]),
            payload_token=str(d["payload_token"]),
            tcp_port=int(d.get("tcp_port", 9090)),
            udp_port=int(d.get("udp_port", 9091)),
            challenge_hash=str(d.get("challenge_hash", "")),
        )


def compute_challenge_hash(challenge_dict: Dict[str, Any]) -> str:
    """Compute a stable SHA256 hash for a challenge dict."""
    d = dict(challenge_dict)
    d.pop("challenge_hash", None)
    payload = yaml.safe_dump(d, sort_keys=True).encode("utf-8")
    import hashlib

    return hashlib.sha256(payload).hexdigest()


def load_challenge(path: Path) -> AntiAIChallenge:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Challenge file must contain a mapping")
    chal = AntiAIChallenge.from_dict(data)

    expected = chal.challenge_hash
    computed = compute_challenge_hash(chal.to_dict())
    if expected and expected != computed:
        raise ValueError("Challenge hash mismatch: file may be corrupted or edited")
    if not expected:
        # If missing, accept but recommend regeneration
        pass
    return chal


def save_challenge(challenge: AntiAIChallenge, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    d = challenge.to_dict()
    if not d.get("challenge_hash"):
        d["challenge_hash"] = compute_challenge_hash(d)
    path.write_text(yaml.safe_dump(d, sort_keys=True), encoding="utf-8")
