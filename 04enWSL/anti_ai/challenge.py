#!/usr/bin/env python3
"""anti_ai.challenge

Defines the on-disk challenge format used by Week 4 submissions.

A challenge is a small YAML document that contains per-submission tokens and constraints.
The validator checks that submitted artefacts contain those tokens in protocol-correct ways.

Notes on design:
- Tokens are not secrets. They exist to prevent replay between students and attempts.
- If you want tamper-evidence for challenges, set ANTI_AI_SIGNING_SECRET in CI.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict

import yaml


@dataclass(frozen=True)
class Week04Challenge:
    """Represents a Week 4 anti-AI challenge."""

    week: int
    student_id: str
    attempt_id: str

    issued_at_utc: datetime
    ttl_seconds: int

    host: str
    text_port: int
    binary_port: int
    udp_port: int

    # Tokens and protocol-specific parameters
    text_token: str
    binary_token: str
    udp_location_tag: str
    udp_sensor_id: int

    integrity_tag: str  # HMAC-SHA256 over canonical payload or 'UNSIGNED'

    @property
    def expires_at_utc(self) -> datetime:
        return self.issued_at_utc + timedelta(seconds=self.ttl_seconds)


def _parse_dt(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def load_challenge(path: str | Path) -> Dict[str, Any]:
    """Load a challenge YAML as a dict."""
    p = Path(path)
    data = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Challenge must be a YAML mapping")
    return data


def normalise_challenge_dict(ch: Dict[str, Any]) -> Dict[str, Any]:
    """Return a dict with required keys validated and types normalised."""
    required = [
        "week",
        "student_id",
        "attempt_id",
        "issued_at_utc",
        "ttl_seconds",
        "host",
        "text_port",
        "binary_port",
        "udp_port",
        "text_token",
        "binary_token",
        "udp_location_tag",
        "udp_sensor_id",
        "integrity_tag",
    ]
    missing = [k for k in required if k not in ch]
    if missing:
        raise ValueError(f"Challenge missing keys: {missing}")

    ch2: Dict[str, Any] = dict(ch)
    ch2["week"] = int(ch2["week"])
    ch2["ttl_seconds"] = int(ch2["ttl_seconds"])
    ch2["text_port"] = int(ch2["text_port"])
    ch2["binary_port"] = int(ch2["binary_port"])
    ch2["udp_port"] = int(ch2["udp_port"])
    ch2["udp_sensor_id"] = int(ch2["udp_sensor_id"])
    ch2["issued_at_utc"] = _parse_dt(str(ch2["issued_at_utc"]))
    ch2["student_id"] = str(ch2["student_id"])
    ch2["attempt_id"] = str(ch2["attempt_id"])
    ch2["host"] = str(ch2["host"])
    ch2["text_token"] = str(ch2["text_token"])
    ch2["binary_token"] = str(ch2["binary_token"])
    ch2["udp_location_tag"] = str(ch2["udp_location_tag"])
    ch2["integrity_tag"] = str(ch2["integrity_tag"])
    return ch2
