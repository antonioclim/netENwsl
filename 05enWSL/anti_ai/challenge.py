#!/usr/bin/env python3
"""
Week 5 Anti-AI challenge model and helpers.

Computer Networks Laboratory (WSL kit)

This module defines the challenge format used to individualise Week 5 homework
and to support evidence-based validation.

Design intent
-------------
The goal is not to ban AI tools. The goal is to ensure that copying a static
answer is not sufficient because each student receives a unique problem
instance and must submit artefacts that can be validated automatically.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required. Install it with: pip install pyyaml") from exc


def _canonical_json(obj: Any) -> str:
    """Serialise an object into a canonical JSON string for stable hashing."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_of_object(obj: Any) -> str:
    """Return the SHA256 hex digest of a Python object."""
    payload = _canonical_json(obj).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def utc_now_iso() -> str:
    """Return current time as an ISO 8601 string in UTC."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_utc_iso(iso_ts: str) -> datetime:
    """Parse an ISO 8601 timestamp that should include timezone information."""
    dt = datetime.fromisoformat(iso_ts)
    if dt.tzinfo is None:
        raise ValueError("Timestamp must include timezone information, for example 2026-01-28T12:00:00+00:00")
    return dt.astimezone(timezone.utc)


@dataclass(frozen=True)
class DepartmentSpec:
    name: str
    required_hosts: int
    description: str


@dataclass(frozen=True)
class DualStackHostSpec:
    hostname: str
    ipv4_address: str
    ipv6_global: str
    ipv6_link_local: str
    description: str


@dataclass
class Week5Challenge:
    """Week 5 anti-AI challenge.

    All fields are intentionally plain data so that the challenge file can be
    stored as YAML and audited.
    """

    version: int
    week: int
    student_id: str
    issued_at_utc: str
    valid_for_hours: int
    session_token: str

    tokens: Dict[str, str]
    outputs: Dict[str, str]

    vlsm_task: Dict[str, Any]
    ipv6_task: Dict[str, Any]

    integrity: Dict[str, str]

    def to_payload_dict(self) -> Dict[str, Any]:
        """Return the dict used for integrity computation (excludes integrity)."""
        return {
            "version": self.version,
            "week": self.week,
            "student_id": self.student_id,
            "issued_at_utc": self.issued_at_utc,
            "valid_for_hours": self.valid_for_hours,
            "session_token": self.session_token,
            "tokens": self.tokens,
            "outputs": self.outputs,
            "vlsm_task": self.vlsm_task,
            "ipv6_task": self.ipv6_task,
        }

    def compute_integrity(self) -> str:
        """Compute the integrity SHA256 over the payload."""
        return sha256_of_object(self.to_payload_dict())

    def to_dict(self) -> Dict[str, Any]:
        """Serialise to a dict ready for YAML dumping."""
        payload = self.to_payload_dict()
        payload["integrity"] = {
            "sha256": self.compute_integrity(),
        }
        return payload

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Week5Challenge":
        """Construct from YAML-loaded data."""
        required = [
            "version",
            "week",
            "student_id",
            "issued_at_utc",
            "valid_for_hours",
            "session_token",
            "tokens",
            "outputs",
            "vlsm_task",
            "ipv6_task",
            "integrity",
        ]
        missing = [k for k in required if k not in data]
        if missing:
            raise ValueError(f"Challenge is missing required keys: {missing}")

        return cls(
            version=int(data["version"]),
            week=int(data["week"]),
            student_id=str(data["student_id"]),
            issued_at_utc=str(data["issued_at_utc"]),
            valid_for_hours=int(data["valid_for_hours"]),
            session_token=str(data["session_token"]),
            tokens=dict(data["tokens"]),
            outputs=dict(data["outputs"]),
            vlsm_task=dict(data["vlsm_task"]),
            ipv6_task=dict(data["ipv6_task"]),
            integrity=dict(data["integrity"]),
        )

    def verify_integrity(self) -> None:
        """Raise ValueError if the integrity hash does not match."""
        expected = self.compute_integrity()
        actual = str(self.integrity.get("sha256", "")).strip()
        if not actual:
            raise ValueError("Challenge integrity is missing 'integrity.sha256'")
        if actual != expected:
            raise ValueError("Challenge integrity check failed. The file may have been modified.")


def load_challenge(path: Path) -> Week5Challenge:
    """Load a challenge YAML file."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Challenge YAML must contain a mapping at the top level")
    challenge = Week5Challenge.from_dict(data)
    challenge.verify_integrity()
    return challenge


def save_challenge(challenge: Week5Challenge, path: Path) -> None:
    """Save a challenge to YAML."""
    path.parent.mkdir(parents=True, exist_ok=True)
    # We dump without sorting keys so the file reads naturally, but hashing uses canonical JSON.
    yaml_text = yaml.safe_dump(challenge.to_dict(), sort_keys=False, allow_unicode=True)
    path.write_text(yaml_text, encoding="utf-8")
