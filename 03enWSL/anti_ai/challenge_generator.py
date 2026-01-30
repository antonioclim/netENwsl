#!/usr/bin/env python3
"""Challenge generator for Week 3.

This script generates a per-student challenge file used by the anti-AI
submission validator.

Intended use:
  python -m anti_ai.challenge_generator --student-id ABC123

Output:
  artifacts/anti_ai/challenge_ABC123.yaml

Notes:
- If you set ANTI_AI_HMAC_KEY in CI, the challenge will include an HMAC tag.
  The validator will verify it, which prevents student-side tampering.
- If the HMAC key is not set, the challenge will still include a SHA-256 tag.
"""

from __future__ import annotations

import argparse
import os
import random
import secrets
from pathlib import Path

from anti_ai.challenge import Challenge, compute_integrity, save_challenge, utc_now_iso


DEFAULT_VALID_HOURS = 24
DEFAULT_MULTICAST_GROUP = "239.0.0.10"


def _stable_seed(student_id: str, week: int) -> int:
    """Derive a stable seed from *student_id* and *week*.

    The seed is not a secret. It exists to provide per-student variation.
    """
    return abs(hash(f"{week}:{student_id}")) % (2**31)


def _pick_port(rng: random.Random, low: int, high: int, avoid: set[int]) -> int:
    """Pick a port in [low, high] avoiding any in *avoid*."""
    for _ in range(1000):
        port = rng.randint(low, high)
        if port not in avoid:
            return port
    raise RuntimeError("Unable to select a port. Please adjust the range.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a Week 3 anti-AI challenge file")
    parser.add_argument("--student-id", required=True, help="Student identifier (as used in the LMS)")
    parser.add_argument(
        "--valid-hours",
        type=int,
        default=DEFAULT_VALID_HOURS,
        help=f"Validity window in hours (default: {DEFAULT_VALID_HOURS})",
    )
    parser.add_argument(
        "--out",
        default="artifacts/anti_ai",
        help="Output directory (default: artifacts/anti_ai)",
    )
    parser.add_argument(
        "--random-ports",
        action="store_true",
        help="Use per-student random ports rather than the standard ports (5007, 5008, 9090)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    student_id = args.student_id.strip()
    issued_at = utc_now_iso()

    rng = random.Random(_stable_seed(student_id, week=3))
    if not args.random_ports:
        broadcast_port = 5007
        multicast_port = 5008
        tunnel_port = 9090
    else:
        avoid = {5007, 5008, 8080, 9090, 9000, 9001, 9002}
        broadcast_port = _pick_port(rng, 40000, 49999, avoid)
        avoid.add(broadcast_port)
        multicast_port = _pick_port(rng, 40000, 49999, avoid)
        avoid.add(multicast_port)
        tunnel_port = _pick_port(rng, 9000, 9999, avoid)

    payload_token = f"W03-{student_id}-{secrets.token_hex(6)}"
    report_token = f"RPT-{student_id}-{secrets.token_hex(6)}"

    hmac_key = os.environ.get("ANTI_AI_HMAC_KEY")
    payload = {
        "meta": {
            "week": 3,
            "student_id": student_id,
            "issued_at_utc": issued_at,
            "valid_for_hours": int(args.valid_hours),
        },
        "tokens": {"payload_token": payload_token, "report_token": report_token},
        "recommended": {
            "broadcast": {"port": broadcast_port},
            "multicast": {"group": DEFAULT_MULTICAST_GROUP, "port": multicast_port},
            "tunnel": {"listen_port": tunnel_port},
        },
    }
    sha, mac = compute_integrity(payload, hmac_key)

    challenge = Challenge(
        week=3,
        student_id=student_id,
        issued_at_utc=issued_at,
        valid_for_hours=int(args.valid_hours),
        payload_token=payload_token,
        report_token=report_token,
        broadcast_port=broadcast_port,
        multicast_group=DEFAULT_MULTICAST_GROUP,
        multicast_port=multicast_port,
        tunnel_listen_port=tunnel_port,
        integrity_sha256=sha,
        integrity_hmac=mac,
    )

    out_dir = Path(args.out)
    out_path = out_dir / f"challenge_{student_id}.yaml"
    save_challenge(challenge, out_path)

    print(f"Challenge written to: {out_path}")
    print("")
    print("Recommended parameters for this attempt:")
    print(f"  Broadcast port:  {broadcast_port}")
    print(f"  Multicast group: {DEFAULT_MULTICAST_GROUP}")
    print(f"  Multicast port:  {multicast_port}")
    print(f"  Tunnel port:     {tunnel_port}")
    print("")
    print("Tokens (do not publish them):")
    print(f"  payload_token: {payload_token}")
    print(f"  report_token:  {report_token}")

    if hmac_key:
        print("")
        print("Integrity: HMAC enabled (ANTI_AI_HMAC_KEY is set).")
    else:
        print("")
        print("Integrity: HMAC disabled (ANTI_AI_HMAC_KEY is not set).")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
