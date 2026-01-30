#!/usr/bin/env python3
"""
Challenge generator for Week 9 anti-AI workflow.

This produces a time-bounded, student-specific challenge file containing:
- a payload token (expected to appear in captured traffic)
- a report token (expected to appear in the written report)
- an expected control port for the pseudo-FTP session

The challenge can optionally be HMAC-signed if ANTI_AI_SECRET is set.
"""

from __future__ import annotations

import argparse
import os
import secrets
from pathlib import Path

from anti_ai.challenge import build_challenge, save_challenge


def _make_token(prefix: str, n_bytes: int = 12) -> str:
    return f"{prefix}-{secrets.token_hex(n_bytes)}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Week 9 anti-AI challenge file")
    parser.add_argument("--student-id", required=True, help="Student ID (used for naming and provenance)")
    parser.add_argument(
        "--ttl-seconds",
        type=int,
        default=90 * 60,
        help="Challenge time-to-live in seconds (default: 90 minutes)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("artifacts/anti_ai"),
        help="Output directory (default: artifacts/anti_ai)",
    )
    parser.add_argument(
        "--secret-env",
        default="ANTI_AI_SECRET",
        help="Environment variable holding optional HMAC secret (default: ANTI_AI_SECRET)",
    )

    args = parser.parse_args()

    student_id = args.student_id.strip()
    out_dir: Path = args.out
    ttl_seconds = int(args.ttl_seconds)

    secret = None
    if args.secret_env:
        secret = (os.environ.get(args.secret_env) or "").strip()  # type: ignore[attr-defined]
        if not secret:
            secret = None

    seed = secrets.token_hex(16)
    payload_token = _make_token("W09P")
    report_token = _make_token("W09R")

    # Randomised but sensible for local testing (avoid privileged ports)
    expected_control_port = 30000 + secrets.randbelow(8000)

    challenge_obj = build_challenge(
        student_id=student_id,
        ttl_seconds=ttl_seconds,
        seed=seed,
        payload_token=payload_token,
        report_token=report_token,
        expected_control_port=expected_control_port,
        secret=secret,
    )

    out_path = out_dir / f"challenge_week09_{student_id}.json"
    save_challenge(out_path, challenge_obj)

    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
