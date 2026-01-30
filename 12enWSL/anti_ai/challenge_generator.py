#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_DOCSTRING
# ═══════════════════════════════════════════════════════════════════════════════
"""Anti-AI challenge generator for Week 12.

This generator produces a short-lived challenge YAML file containing tokens that must
appear in real protocol traffic.

Recommended usage:
    python scripts/anti_ai_issue_challenge.py --student-id ABC123

Teacher-side hardening (optional):
    export WEEK12_CHALLENGE_HMAC_KEY='a long random secret'
    python scripts/anti_ai_issue_challenge.py --student-id ABC123 --strict

If the HMAC key is provided, the generated challenge includes a signature and the
validator can refuse unsigned or tampered challenges in strict mode.
"""

from __future__ import annotations

import argparse
import hmac
import json
import os
import secrets
import sys
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict

try:
    import yaml
except ImportError:  # pragma: no cover
    print("[ERROR] PyYAML is required: pip install pyyaml")
    raise

from .challenge import Week12Challenge, make_challenge


DEFAULT_TTL_HOURS = 8


def _canonical_payload(challenge: Week12Challenge) -> bytes:
    """Return canonical JSON used for signing."""

    obj = challenge.to_dict()
    # Never include signature field in the signed payload.
    obj.pop("signature_hmac_sha256", None)
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sign(payload: bytes, key: str) -> str:
    mac = hmac.new(key.encode("utf-8"), payload, sha256)
    return mac.hexdigest()


def generate_challenge(*, student_id: str, ttl_hours: int, strict: bool) -> Week12Challenge:
    ttl_seconds = int(max(1, ttl_hours) * 3600)

    smtp_token = f"W12-SMTP-{secrets.token_hex(6)}"
    rpc_token = f"W12-RPC-{secrets.token_hex(6)}"
    report_token = f"W12-REPORT-{secrets.token_hex(6)}"

    key = os.getenv("WEEK12_CHALLENGE_HMAC_KEY")
    signature: str | None = None

    base = make_challenge(
        student_id=student_id,
        ttl_seconds=ttl_seconds,
        smtp_subject_token=smtp_token,
        rpc_echo_token=rpc_token,
        report_token=report_token,
    )

    if key:
        signature = _sign(_canonical_payload(base), key)
    elif strict:
        raise SystemExit(
            "Strict mode requested but WEEK12_CHALLENGE_HMAC_KEY is not set. "
            "Either set the environment variable or omit --strict."
        )

    return Week12Challenge.from_dict({**base.to_dict(), "signature_hmac_sha256": signature})


def write_challenge(challenge: Week12Challenge, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(yaml.safe_dump(challenge.to_dict(), sort_keys=False), encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Generate an anti-AI challenge (Week 12)")
    ap.add_argument("--student-id", required=True, help="Student identifier")
    ap.add_argument(
        "--ttl-hours",
        type=int,
        default=DEFAULT_TTL_HOURS,
        help=f"Challenge validity window in hours (default: {DEFAULT_TTL_HOURS})",
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output YAML path (default: artifacts/anti_ai/challenge_<student-id>.yaml)",
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Require an HMAC signing key and write a signed challenge",
    )
    return ap.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    student_id = str(args.student_id).strip()
    if not student_id:
        print("[ERROR] --student-id cannot be empty")
        return 2

    output: Path
    if args.output:
        output = args.output
    else:
        output = Path("artifacts") / "anti_ai" / f"challenge_{student_id}.yaml"

    challenge = generate_challenge(student_id=student_id, ttl_hours=int(args.ttl_hours), strict=bool(args.strict))
    write_challenge(challenge, output)

    print("Week 12 anti-AI challenge generated")
    print(f"Student ID: {challenge.student_id}")
    print(f"Issued (UTC): {challenge.issued_at_utc}")
    print(f"Valid for: {int(challenge.ttl_seconds) // 3600} hour(s)")
    print(f"SMTP subject token: {challenge.smtp_subject_token}")
    print(f"RPC echo token: {challenge.rpc_echo_token}")
    print(f"Report token: {challenge.report_token}")
    print(f"Output: {output}")

    if challenge.signature_hmac_sha256:
        print("Signature: present")
    else:
        print("Signature: not present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
