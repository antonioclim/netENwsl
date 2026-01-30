"""Challenge file generation and verification.

A Week 2 anti‑AI challenge ties a submission to:
- a specific student identifier
- a time window (TTL)
- unique payload tokens
- recommended TCP and UDP ports used for proof traffic

For production use, challenges should be *signed* using an instructor‑controlled
secret key (HMAC‑SHA256). The secret key must not be distributed to students.

If the key is absent, an unsigned challenge can still be generated for practice.
"""

from __future__ import annotations

import dataclasses
import hashlib
import hmac
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping

import yaml


SIGNATURE_PREFIX = "hmac-sha256:"
SCHEMA_VERSION = 1


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def to_iso_utc(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso_utc(value: str) -> datetime:
    # Accept the exact format we emit.
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def _canonical_json(data: Mapping[str, Any]) -> str:
    """Canonical JSON for signing and verification."""
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _hmac_sha256_hex(key: bytes, message: str) -> str:
    return hmac.new(key, message.encode("utf-8"), hashlib.sha256).hexdigest()


def get_master_key_from_env() -> bytes | None:
    """Return master key bytes if ANTI_AI_MASTER_KEY is set."""
    raw = os.environ.get("ANTI_AI_MASTER_KEY", "").strip()
    if not raw:
        return None
    return raw.encode("utf-8")


@dataclass(frozen=True)
class Challenge:
    """Represents a Week 2 anti‑AI challenge."""

    schema_version: int
    week_id: int
    challenge_id: str
    student_id: str
    issued_at_utc: str
    ttl_seconds: int
    tcp_port: int
    udp_port: int
    payload_token: str
    signature: str | None = None
    notes: str | None = None

    def to_unsigned_dict(self) -> dict[str, Any]:
        data = dataclasses.asdict(self)
        data.pop("signature", None)
        return data

    def canonical_payload(self) -> str:
        return _canonical_json(self.to_unsigned_dict())

    def compute_signature(self, key: bytes) -> str:
        digest = _hmac_sha256_hex(key, self.canonical_payload())
        return f"{SIGNATURE_PREFIX}{digest}"

    def with_signature(self, key: bytes) -> "Challenge":
        return dataclasses.replace(self, signature=self.compute_signature(key))

    def verify_signature(self, key: bytes) -> bool:
        if not self.signature or not self.signature.startswith(SIGNATURE_PREFIX):
            return False
        expected = self.compute_signature(key)
        return hmac.compare_digest(self.signature, expected)

    def issued_at_datetime(self) -> datetime:
        return parse_iso_utc(self.issued_at_utc)

    def is_expired(self, now: datetime | None = None) -> bool:
        now = now or utc_now()
        age = (now - self.issued_at_datetime()).total_seconds()
        return age > float(self.ttl_seconds)

    def short_id(self) -> str:
        return self.challenge_id.split("-")[0]

    def stable_hash(self) -> str:
        """A stable hash of the unsigned challenge payload (for quick integrity checks)."""
        return hashlib.sha256(self.canonical_payload().encode("utf-8")).hexdigest()

    @staticmethod
    def from_mapping(data: Mapping[str, Any]) -> "Challenge":
        required = [
            "schema_version",
            "week_id",
            "challenge_id",
            "student_id",
            "issued_at_utc",
            "ttl_seconds",
            "tcp_port",
            "udp_port",
            "payload_token",
        ]
        for k in required:
            if k not in data:
                raise ValueError(f"Missing required key: {k}")

        return Challenge(
            schema_version=int(data["schema_version"]),
            week_id=int(data["week_id"]),
            challenge_id=str(data["challenge_id"]),
            student_id=str(data["student_id"]),
            issued_at_utc=str(data["issued_at_utc"]),
            ttl_seconds=int(data["ttl_seconds"]),
            tcp_port=int(data["tcp_port"]),
            udp_port=int(data["udp_port"]),
            payload_token=str(data["payload_token"]),
            signature=str(data.get("signature")) if data.get("signature") else None,
            notes=str(data.get("notes")) if data.get("notes") else None,
        )

    @staticmethod
    def load_yaml(path: str) -> "Challenge":
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            raise ValueError("Challenge YAML must be a mapping")
        return Challenge.from_mapping(data)

    def save_yaml(self, path: str) -> None:
        data = dataclasses.asdict(self)
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
