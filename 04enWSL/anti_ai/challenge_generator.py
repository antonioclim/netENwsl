#!/usr/bin/env python3
"""anti_ai.challenge_generator

Generates a per-student Week 4 challenge.

The challenge contains tokens that must appear in protocol-correct network traffic.
This makes copying between students costly and makes text-only submissions insufficient.

Typical workflow:
  1) Instructor or CI generates challenges and distributes them to students
  2) Student runs the lab, captures traffic and collects evidence
  3) Validator checks the evidence automatically

If ANTI_AI_SIGNING_SECRET is set, the generator signs the challenge with HMAC-SHA256.
"""

from __future__ import annotations

import argparse
import json
import os
import secrets
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import yaml


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _canonical_payload(payload: Dict[str, Any]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def _hmac_tag(payload: Dict[str, Any], secret: str) -> str:
    digest = hmac.new(secret.encode("utf-8"), _canonical_payload(payload), hashlib.sha256).hexdigest()
    return f"hmac-sha256:{digest}"


def generate_week04_challenge(
    student_id: str,
    host: str,
    ttl_hours: float,
    attempt_id: str | None = None,
) -> Dict[str, Any]:
    attempt_id = attempt_id or str(uuid.uuid4())
    issued_at = _utc_now()

    # Tokens are designed to be short enough for typing and visible in PCAPs.
    text_token = f"W4T-{secrets.token_hex(3)}"      # 3 bytes -> 6 hex
    binary_token = f"W4B-{secrets.token_hex(4)}"    # 4 bytes -> 8 hex

    # UDP location is limited to 10 bytes in the Week 4 sensor protocol.
    udp_location_tag = f"W4U{secrets.token_hex(3)}"[:10]

    # UDP sensor_id is a 32-bit integer.
    udp_sensor_id = secrets.randbelow(2**32)

    base: Dict[str, Any] = {
        "week": 4,
        "student_id": student_id,
        "attempt_id": attempt_id,
        "issued_at_utc": issued_at.isoformat().replace("+00:00", "Z"),
        "ttl_seconds": int(ttl_hours * 3600),
        "host": host,
        "text_port": 5400,
        "binary_port": 5401,
        "udp_port": 5402,
        "text_token": text_token,
        "binary_token": binary_token,
        "udp_location_tag": udp_location_tag,
        "udp_sensor_id": udp_sensor_id,
    }

    secret = os.environ.get("ANTI_AI_SIGNING_SECRET", "").strip()
    if secret:
        integrity_tag = _hmac_tag(base, secret)
    else:
        integrity_tag = "UNSIGNED"

    challenge: Dict[str, Any] = dict(base)
    challenge["integrity_tag"] = integrity_tag

    # Human-facing instructions to reduce mistakes.
    challenge["instructions"] = {
        "text": {
            "server": "python3 src/apps/text_proto_server.py --port 5400 --verbose",
            "client_example": f'python3 src/apps/text_proto_client.py --host {host} --port 5400 --command "SET anti_ai {text_token}" --command "GET anti_ai" --command "QUIT"',
            "required_substring": f"SET anti_ai {text_token}",
        },
        "binary": {
            "server": "python3 src/apps/binary_proto_server.py --port 5401 --verbose",
            "required_key": "anti_ai",
            "required_value": binary_token,
        },
        "udp_sensor": {
            "server": "python3 src/apps/udp_sensor_server.py --port 5402 --verbose",
            "client_example": f'python3 src/apps/udp_sensor_client.py --host {host} --port 5402 --sensor-id {udp_sensor_id} --temp 21.5 --location "{udp_location_tag}"',
            "required_location": udp_location_tag,
            "required_sensor_id": udp_sensor_id,
        },
        "capture_note": (
            "Capture the traffic with Wireshark or tcpdump and include the .pcap in your submission "
            "alongside evidence.json."
        ),
    }

    return challenge


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Week 4 anti-AI challenge (YAML)")
    parser.add_argument("--student-id", required=True, help="Student identifier (as used by the course)")
    parser.add_argument("--host", default="localhost", help="Host used in commands (default: localhost)")
    parser.add_argument("--ttl-hours", type=float, default=24.0, help="Validity window in hours (default: 24)")
    parser.add_argument("--attempt-id", default=None, help="Optional attempt UUID (default: random)")
    parser.add_argument(
        "--output",
        default="artifacts/anti_ai/week04_challenge.yaml",
        help="Output path (default: artifacts/anti_ai/week04_challenge.yaml)",
    )
    args = parser.parse_args()

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    ch = generate_week04_challenge(
        student_id=args.student_id,
        host=args.host,
        ttl_hours=args.ttl_hours,
        attempt_id=args.attempt_id,
    )

    out_path.write_text(yaml.safe_dump(ch, sort_keys=False), encoding="utf-8")
    print(f"Wrote challenge: {out_path}")
    if ch.get("integrity_tag") == "UNSIGNED":
        print("Note: ANTI_AI_SIGNING_SECRET not set, challenge is unsigned.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
