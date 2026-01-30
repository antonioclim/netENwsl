"""Generate a Week 2 anti‑AI challenge file.

In a real course, the instructor should generate challenges and distribute them
to students. When ANTI_AI_MASTER_KEY is set the challenge will be signed.

When the key is not set, the generator still produces a valid challenge for
practice. The validator can be configured to accept unsigned challenges if
explicitly allowed.
"""

from __future__ import annotations

import argparse
import os
import random
import socket
import string
import uuid
from datetime import datetime, timezone
from pathlib import Path

from anti_ai.challenge import Challenge, SCHEMA_VERSION, get_master_key_from_env, to_iso_utc


def pick_free_port(sock_type: int) -> int:
    # Bind to port 0 to let the OS pick a free port.
    with socket.socket(socket.AF_INET, sock_type) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


def random_token(prefix: str, length: int = 18) -> str:
    alphabet = string.ascii_uppercase + string.digits
    body = "".join(random.choice(alphabet) for _ in range(length))
    return f"{prefix}{body}"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate Week 2 anti‑AI challenge YAML")
    p.add_argument("--student-id", required=True, help="Student identifier used to personalise the challenge")
    p.add_argument("--ttl-seconds", type=int, default=6 * 60 * 60, help="Validity window in seconds (default: 6h)")
    p.add_argument("--tcp-port", type=int, default=0, help="TCP port (0 = pick free port)")
    p.add_argument("--udp-port", type=int, default=0, help="UDP port (0 = pick free port)")
    p.add_argument("--out", default="", help="Output challenge file path")
    p.add_argument("--force", action="store_true", help="Overwrite existing output file")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    tcp_port = int(args.tcp_port) if int(args.tcp_port) > 0 else pick_free_port(socket.SOCK_STREAM)
    udp_port = int(args.udp_port) if int(args.udp_port) > 0 else pick_free_port(socket.SOCK_DGRAM)

    ch = Challenge(
        schema_version=SCHEMA_VERSION,
        week_id=2,
        challenge_id=str(uuid.uuid4()),
        student_id=str(args.student_id),
        issued_at_utc=to_iso_utc(datetime.now(timezone.utc)),
        ttl_seconds=int(args.ttl_seconds),
        tcp_port=tcp_port,
        udp_port=udp_port,
        payload_token=random_token("W2-"),
        signature=None,
        notes="Signed if ANTI_AI_MASTER_KEY is set. Unsigned challenges are for practice only.",
    )

    key = get_master_key_from_env()
    if key is not None:
        ch = ch.with_signature(key)

    out = Path(args.out) if args.out else Path("artifacts/anti_ai") / f"challenge_{args.student_id}.yaml"
    out = out.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    if out.exists() and not args.force:
        print(f"✗ Refusing to overwrite existing file: {out} (use --force)")
        return 2

    ch.save_yaml(str(out))
    status = "signed" if ch.signature else "unsigned"
    print(f"✓ Challenge generated ({status}): {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
