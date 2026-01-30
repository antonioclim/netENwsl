"""CLI to generate Week 13 anti-AI challenges."""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import secrets
import uuid
from pathlib import Path
from typing import Optional

import yaml

from .challenge import Challenge, compute_integrity_tag


def _utc_now() -> str:
    return _dt.datetime.now(tz=_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _stable_seed(student_id: str, secret: Optional[str]) -> int:
    base = (student_id + (secret or "")).encode("utf-8")
    digest = hashlib.sha256(base).digest()
    return int.from_bytes(digest[:4], "big")


def generate(student_id: str, ttl_seconds: int, secret: Optional[str]) -> Challenge:
    seed = _stable_seed(student_id, secret)
    slug = hashlib.sha256(student_id.encode("utf-8")).hexdigest()[:8]
    topic = f"iot/{slug}/telemetry/{seed % 10000:04d}"

    report_token = f"W13-REPORT-{secrets.token_hex(8)}"
    payload_token = f"W13-MQTT-{secrets.token_hex(8)}"

    base = {
        "week_id": 13,
        "student_id": student_id,
        "challenge_id": str(uuid.uuid4()),
        "issued_at_utc": _utc_now(),
        "ttl_seconds": int(ttl_seconds),
        "mqtt_topic": topic,
        "mqtt_plain_port": 1883,
        "mqtt_tls_port": 8883,
        "report_token": report_token,
        "payload_token": payload_token,
    }
    alg, tag = compute_integrity_tag(base, secret)
    full = dict(base)
    full["integrity_alg"] = alg
    full["integrity_tag"] = tag
    return Challenge(**full)  # type: ignore[arg-type]


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Generate Week 13 anti-AI challenge")
    p.add_argument("--student-id", required=True, help="Student identifier (e.g. LMS ID)")
    p.add_argument("--ttl-seconds", type=int, default=6 * 60 * 60, help="Challenge validity window")
    p.add_argument("--output", default=None, help="Output YAML path")
    p.add_argument("--secret-env", default="ANTI_AI_SECRET", help="Environment variable name for HMAC secret")
    return p


def main() -> int:
    args = build_arg_parser().parse_args()
    secret = None
    if args.secret_env:
        import os
        secret = os.environ.get(args.secret_env)

    challenge = generate(args.student_id, args.ttl_seconds, secret)
    out = Path(args.output) if args.output else Path("artifacts/anti_ai") / f"challenge_{args.student_id}.yaml"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(yaml.safe_dump(challenge.to_dict(), sort_keys=False), encoding="utf-8")

    print(f"[OK] Challenge written to {out}")
    print(f"     MQTT topic: {challenge.mqtt_topic}")
    print(f"     Plain MQTT port: {challenge.mqtt_plain_port} and TLS port: {challenge.mqtt_tls_port}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
