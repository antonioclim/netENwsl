"""Challenge schema and integrity helpers for Week 13."""

from __future__ import annotations

import dataclasses
import datetime as _dt
import hashlib
import hmac
import json
from typing import Any, Dict, Optional


@dataclasses.dataclass(frozen=True)
class Challenge:
    """A per-student challenge for Week 13.

    The key idea is to require at least one capture artefact that contains a unique payload token
    on a well-defined port (MQTT plaintext on 1883). A secondary requirement is a TLS handshake
    capture on 8883, which demonstrates that encrypted MQTT was attempted even though payload
    inspection is not possible.
    """

    week_id: int
    student_id: str
    challenge_id: str
    issued_at_utc: str
    ttl_seconds: int

    mqtt_topic: str
    mqtt_plain_port: int
    mqtt_tls_port: int

    report_token: str
    payload_token: str

    integrity_alg: str
    integrity_tag: str

    @property
    def expires_at_utc(self) -> str:
        issued = _parse_utc(self.issued_at_utc)
        return (issued + _dt.timedelta(seconds=self.ttl_seconds)).strftime("%Y-%m-%dT%H:%M:%SZ")

    def to_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)


def _parse_utc(value: str) -> _dt.datetime:
    return _dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=_dt.timezone.utc)


def _canonical_json(obj: Dict[str, Any]) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def compute_integrity_tag(payload: Dict[str, Any], secret: Optional[str]) -> tuple[str, str]:
    """Return (algorithm, tag) for a challenge payload."""
    data = _canonical_json(payload)
    if secret:
        digest = hmac.new(secret.encode("utf-8"), data, hashlib.sha256).hexdigest()
        return "HMAC-SHA256", digest
    digest = hashlib.sha256(data).hexdigest()
    return "SHA256", digest


def verify_integrity(payload: Dict[str, Any], secret: Optional[str]) -> bool:
    """Verify the integrity tag in a loaded challenge mapping."""
    integrity_alg = payload.get("integrity_alg")
    integrity_tag = payload.get("integrity_tag")
    if not integrity_alg or not integrity_tag:
        return False

    base = dict(payload)
    base.pop("integrity_alg", None)
    base.pop("integrity_tag", None)
    expected_alg, expected_tag = compute_integrity_tag(base, secret if integrity_alg == "HMAC-SHA256" else None)
    return integrity_alg == expected_alg and hmac.compare_digest(str(integrity_tag), str(expected_tag))
