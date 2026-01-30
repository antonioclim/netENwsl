#!/usr/bin/env python3
"""Challenge schema for Week 6 anti-AI workflow.

Design goals
- A student can use an LLM for explanations and debugging.
- A submission still needs verifiable artefacts from real execution.
- Tokens are unique per student and attempt and are validated against binary captures.

Notes
- This file supports optional HMAC signing if a secret is available in CI.
- In local practice mode, the challenge can be unsigned.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import hashlib
import hmac
import json

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None  # type: ignore


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _to_iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _from_iso(value: str) -> datetime:
    # Accept either Z or an explicit offset.
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value).astimezone(timezone.utc)


def _canonical_json(data: Dict[str, Any]) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _hmac_sha256_hex(secret: str, data: bytes) -> str:
    return hmac.new(secret.encode("utf-8"), data, hashlib.sha256).hexdigest()


@dataclass(frozen=True)
class AntiAIChallenge:
    """Anti-AI challenge parameters for Week 6."""

    week_id: int
    student_id: str
    challenge_id: str
    issued_at_utc: datetime
    ttl_seconds: int

    report_token: str
    payload_token: str

    tcp_port: int
    udp_port: int

    nat_probe_command: str
    sdn_probe_command: str

    integrity_sha256: str
    signature_hmac_sha256: Optional[str] = None

    @property
    def issued_at_iso(self) -> str:
        return _to_iso(self.issued_at_utc)

    def to_dict(self, include_integrity: bool = True) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "week_id": self.week_id,
            "student_id": self.student_id,
            "challenge_id": self.challenge_id,
            "issued_at_utc": self.issued_at_iso,
            "ttl_seconds": self.ttl_seconds,
            "report_token": self.report_token,
            "payload_token": self.payload_token,
            "tcp_port": self.tcp_port,
            "udp_port": self.udp_port,
            "nat_probe_command": self.nat_probe_command,
            "sdn_probe_command": self.sdn_probe_command,
        }
        if include_integrity:
            data["integrity_sha256"] = self.integrity_sha256
            if self.signature_hmac_sha256:
                data["signature_hmac_sha256"] = self.signature_hmac_sha256
        return data

    @staticmethod
    def compute_integrity(data_without_integrity: Dict[str, Any]) -> str:
        return _sha256_hex(_canonical_json(data_without_integrity))

    @staticmethod
    def compute_signature(secret: str, data_without_integrity: Dict[str, Any]) -> str:
        return _hmac_sha256_hex(secret, _canonical_json(data_without_integrity))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AntiAIChallenge":
        issued = _from_iso(str(data["issued_at_utc"]))
        return cls(
            week_id=int(data["week_id"]),
            student_id=str(data["student_id"]),
            challenge_id=str(data["challenge_id"]),
            issued_at_utc=issued,
            ttl_seconds=int(data["ttl_seconds"]),
            report_token=str(data["report_token"]),
            payload_token=str(data["payload_token"]),
            tcp_port=int(data["tcp_port"]),
            udp_port=int(data["udp_port"]),
            nat_probe_command=str(data["nat_probe_command"]),
            sdn_probe_command=str(data["sdn_probe_command"]),
            integrity_sha256=str(data.get("integrity_sha256", "")),
            signature_hmac_sha256=(str(data["signature_hmac_sha256"]) if data.get("signature_hmac_sha256") else None),
        )

    @classmethod
    def load_yaml(cls, path: str) -> "AntiAIChallenge":
        if yaml is None:  # pragma: no cover
            raise RuntimeError("PyYAML is required to load challenge files")
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            raise ValueError("Challenge file is not a mapping")
        return cls.from_dict(data)

    def save_yaml(self, path: str) -> None:
        if yaml is None:  # pragma: no cover
            raise RuntimeError("PyYAML is required to write challenge files")
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(self.to_dict(), f, sort_keys=False)

    def verify_integrity(self, secret: Optional[str] = None) -> None:
        """Verify integrity and optional signature.

        Raises ValueError if any check fails.
        """
        data_wo = self.to_dict(include_integrity=False)
        expected_integrity = self.compute_integrity(data_wo)
        if self.integrity_sha256 and self.integrity_sha256 != expected_integrity:
            raise ValueError("Challenge integrity hash does not match contents")

        if secret is not None:
            expected_sig = self.compute_signature(secret, data_wo)
            if not self.signature_hmac_sha256:
                raise ValueError("Challenge is not signed but signature is required")
            if self.signature_hmac_sha256 != expected_sig:
                raise ValueError("Challenge signature is invalid")

    def is_expired(self, now_utc: Optional[datetime] = None, grace_seconds: int = 60) -> bool:
        if now_utc is None:
            now_utc = _utc_now()
        age = (now_utc - self.issued_at_utc).total_seconds()
        return age > (self.ttl_seconds + grace_seconds)
