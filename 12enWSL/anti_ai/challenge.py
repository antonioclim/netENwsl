#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_DOCSTRING
# ═══════════════════════════════════════════════════════════════════════════════
"""Challenge definition for Week 12 anti-AI checks.

The challenge is intentionally simple: it contains a small set of unique tokens
that must appear in real network traffic. Students are expected to:

- send an SMTP message whose *Subject* includes the SMTP token
- call RPC echo endpoints (JSON-RPC and XML-RPC) with the RPC token

The validator then searches captured traffic for these tokens.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _parse_utc(ts: str) -> datetime:
    """Parse an ISO-8601 timestamp with timezone.

    The generator writes UTC timestamps using the 'Z' suffix.
    """

    # Accept both 'Z' and explicit offsets.
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    return datetime.fromisoformat(ts)


def _format_utc(dt: datetime) -> str:
    dt = dt.astimezone(timezone.utc)
    return dt.isoformat(timespec="seconds").replace("+00:00", "Z")


@dataclass(frozen=True)
class Week12Challenge:
    """A short-lived challenge for Week 12."""

    week: int
    student_id: str
    issued_at_utc: str
    ttl_seconds: int

    # Tokens
    smtp_subject_token: str
    rpc_echo_token: str
    report_token: str

    # Expected service ports (kept fixed for this week)
    smtp_port: int = 1025
    jsonrpc_port: int = 6200
    xmlrpc_port: int = 6201
    grpc_port: int = 6251

    # Optional signature, if a secret key was used.
    signature_hmac_sha256: str | None = None

    @property
    def issued_at(self) -> datetime:
        return _parse_utc(self.issued_at_utc)

    @property
    def expires_at(self) -> datetime:
        return self.issued_at + timedelta(seconds=int(self.ttl_seconds))

    def is_expired(self, now: datetime | None = None) -> bool:
        now = now or _utc_now()
        return now >= self.expires_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "week": self.week,
            "student_id": self.student_id,
            "issued_at_utc": self.issued_at_utc,
            "ttl_seconds": int(self.ttl_seconds),
            "smtp_subject_token": self.smtp_subject_token,
            "rpc_echo_token": self.rpc_echo_token,
            "report_token": self.report_token,
            "ports": {
                "smtp": int(self.smtp_port),
                "jsonrpc": int(self.jsonrpc_port),
                "xmlrpc": int(self.xmlrpc_port),
                "grpc": int(self.grpc_port),
            },
            "signature_hmac_sha256": self.signature_hmac_sha256,
        }

    def to_yaml(self) -> str:
        """Serialise the challenge to YAML."""
        import yaml

        return yaml.safe_dump(self.to_dict(), sort_keys=False)

    @classmethod
    def from_yaml(cls, text: str) -> "Week12Challenge":
        """Load a challenge from YAML."""
        import yaml

        obj = yaml.safe_load(text) or {}
        if not isinstance(obj, dict):
            raise ValueError("Challenge YAML must contain a mapping at the root")
        return cls.from_dict(obj)

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "Week12Challenge":
        ports = obj.get("ports") or {}
        return cls(
            week=int(obj.get("week", 12)),
            student_id=str(obj.get("student_id", "")),
            issued_at_utc=str(obj.get("issued_at_utc", "")),
            ttl_seconds=int(obj.get("ttl_seconds", 0)),
            smtp_subject_token=str(obj.get("smtp_subject_token", "")),
            rpc_echo_token=str(obj.get("rpc_echo_token", "")),
            report_token=str(obj.get("report_token", "")),
            smtp_port=int(ports.get("smtp", 1025)),
            jsonrpc_port=int(ports.get("jsonrpc", 6200)),
            xmlrpc_port=int(ports.get("xmlrpc", 6201)),
            grpc_port=int(ports.get("grpc", 6251)),
            signature_hmac_sha256=obj.get("signature_hmac_sha256"),
        )


def make_challenge(
    *,
    student_id: str,
    ttl_seconds: int,
    smtp_subject_token: str,
    rpc_echo_token: str,
    report_token: str,
    signature_hmac_sha256: str | None = None,
) -> Week12Challenge:
    now = _utc_now()
    return Week12Challenge(
        week=12,
        student_id=student_id,
        issued_at_utc=_format_utc(now),
        ttl_seconds=int(ttl_seconds),
        smtp_subject_token=smtp_subject_token,
        rpc_echo_token=rpc_echo_token,
        report_token=report_token,
        signature_hmac_sha256=signature_hmac_sha256,
    )
