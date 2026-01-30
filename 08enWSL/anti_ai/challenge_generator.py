"""Generate a student-specific anti-AI challenge for Week 8."""

from __future__ import annotations

import json
from datetime import timedelta
from pathlib import Path
from typing import Any, Dict, Optional

from .challenge import challenge_from_context, save_challenge
from .files import sha256_file
from .signing import sign_dict


DEFAULT_CONTEXT = Path("artifacts/student_context.json")
DEFAULT_OUT = Path("artifacts/anti_ai/challenge_week08.json")


def load_student_context(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def generate_week08_challenge(
    *,
    context_path: Path = DEFAULT_CONTEXT,
    output_path: Path = DEFAULT_OUT,
    ttl_hours: int = 12,
    secret: Optional[str] = None,
) -> Path:
    """Generate and write the challenge file.

    If a secret is provided, the challenge is signed (HMAC-SHA256) and the
    signature can be validated later in CI.
    """

    if not context_path.exists():
        raise FileNotFoundError(
            "Student context not found. Run: make init ID=your_student_id"
        )

    ctx = load_student_context(context_path)
    ctx_hash = sha256_file(context_path)

    unsigned = challenge_from_context(
        week="08enWSL",
        student_context=ctx,
        context_sha256=ctx_hash,
        ttl=timedelta(hours=ttl_hours),
        signature=None,
    )

    signature = None
    if secret:
        d = unsigned.as_dict()
        d.pop("signature", None)
        signature = sign_dict(d, secret)

    challenge = challenge_from_context(
        week="08enWSL",
        student_context=ctx,
        context_sha256=ctx_hash,
        ttl=timedelta(hours=ttl_hours),
        signature=signature,
    )

    save_challenge(challenge, output_path)
    return output_path


def main() -> int:
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Generate Week 8 anti-AI challenge")
    parser.add_argument(
        "--context",
        default=str(DEFAULT_CONTEXT),
        help="Path to student_context.json",
    )
    parser.add_argument(
        "--out",
        default=str(DEFAULT_OUT),
        help="Output path for challenge JSON",
    )
    parser.add_argument(
        "--ttl-hours",
        type=int,
        default=12,
        help="Challenge time-to-live in hours",
    )
    parser.add_argument(
        "--sign",
        action="store_true",
        help="Sign the challenge with ANTI_AI_SECRET if available",
    )

    args = parser.parse_args()
    secret = os.environ.get("ANTI_AI_SECRET") if args.sign else None

    out = generate_week08_challenge(
        context_path=Path(args.context),
        output_path=Path(args.out),
        ttl_hours=int(args.ttl_hours),
        secret=secret,
    )
    print(f"Challenge written to: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
