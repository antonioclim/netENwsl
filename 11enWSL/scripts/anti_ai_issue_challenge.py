#!/usr/bin/env python3
"""Issue an anti-AI challenge for Week 11.

This is intended for instructors. Students should receive the generated JSON
file and must include it unchanged with their submission artefacts.

If ANTI_AI_SECRET is set in the environment, the challenge will be signed.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from anti_ai import generate_challenge


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Issue Week 11 anti-AI challenge",
    )
    parser.add_argument("--student-id", required=True, help="Student identifier (e.g. email or matriculation number)")
    parser.add_argument("--ttl-minutes", type=int, default=45, help="Challenge lifetime in minutes")
    parser.add_argument("--min-http", type=int, default=10, help="Minimum number of token HTTP requests")
    parser.add_argument("--min-backends", type=int, default=2, help="Minimum distinct backends observed")
    parser.add_argument(
        "--out",
        default=str(PROJECT_ROOT / "artifacts" / "anti_ai" / "week11_challenge.json"),
        help="Output path for challenge JSON",
    )

    args = parser.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    challenge = generate_challenge(
        week=11,
        student_id=args.student_id,
        ttl_minutes=args.ttl_minutes,
        min_http_requests=args.min_http,
        min_distinct_backends=args.min_backends,
        secret=os.environ.get("ANTI_AI_SECRET"),
    )

    out_path.write_text(json.dumps(challenge, indent=2, sort_keys=True), encoding="utf-8")

    print(f"Wrote challenge: {out_path}")
    print(f"Challenge ID: {challenge['challenge_id']}")
    print(f"Expires at: {challenge['expires_at']}")
    print(f"DNS query name: {challenge['requirements']['dns_query_name']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
