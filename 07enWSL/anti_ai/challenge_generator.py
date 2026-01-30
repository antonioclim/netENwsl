"""Challenge generator for the Week 7 anti-AI workflow."""

from __future__ import annotations

import argparse
import secrets
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .challenge import AntiAIChallenge, save_challenge


def _iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _token(prefix: str) -> str:
    # Short, copy-friendly token that still has good entropy
    body = secrets.token_urlsafe(12).replace("-", "").replace("_", "")
    return f"{prefix}{body[:18]}"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Generate a per-student anti-AI challenge (Week 7).")
    p.add_argument("--student-id", required=True, help="Student identifier (will be stored in challenge file)")
    p.add_argument("--ttl-hours", type=int, default=24, help="Time-to-live in hours (default: 24)")
    p.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output file path (default: artifacts/anti_ai/challenge_<student>.yaml)",
    )
    return p


def main() -> int:
    args = build_parser().parse_args()
    out = args.output
    if out is None:
        out = Path("artifacts/anti_ai") / f"challenge_{args.student_id}.yaml"

    chal = AntiAIChallenge(
        week_id=7,
        student_id=str(args.student_id),
        attempt_id=str(uuid.uuid4()),
        issued_at_utc=_iso_utc_now(),
        ttl_seconds=int(args.ttl_hours) * 3600,
        report_token=_token("W7R-"),
        payload_token=_token("W7P-"),
        tcp_port=9090,
        udp_port=9091,
        challenge_hash="",
    )

    save_challenge(chal, out)
    print(f"Wrote challenge to {out}")
    print(f"Report token: {chal.report_token}")
    print(f"Payload token: {chal.payload_token}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
