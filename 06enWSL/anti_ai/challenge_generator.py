#!/usr/bin/env python3
"""Generate an anti-AI challenge for Week 6.

Typical use (student practice)
    python -m anti_ai.challenge_generator --student-id ABC123

Instructor or CI use (signed challenge)
    export ANTI_AI_SECRET="...long random string..."
    python -m anti_ai.challenge_generator --student-id ABC123 --sign

The challenge defines
- a report token that must appear in a text artefact
- a payload token that must appear in a binary PCAP payload
- TCP and UDP ports that must match the capture
- probe commands for NAT and SDN live verification
"""

from __future__ import annotations

import argparse
import os
import secrets
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from anti_ai.challenge import AntiAIChallenge


DEFAULT_TTL_SECONDS = 6 * 60 * 60  # 6 hours


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _make_token(prefix: str) -> str:
    # Short but non-guessable token for lab artefacts.
    return f"{prefix}-{secrets.token_hex(4).upper()}"


def generate_challenge(
    student_id: str,
    ttl_seconds: int = DEFAULT_TTL_SECONDS,
    secret: Optional[str] = None,
    sign: bool = False,
) -> AntiAIChallenge:
    issued = _utc_now()
    challenge_id = str(uuid.uuid4())

    report_token = _make_token("W6-REPORT")
    payload_token = _make_token("W6-PAYLOAD")

    tcp_port = secrets.choice(range(20000, 60000))
    udp_port = secrets.choice(range(20000, 60000))

    nat_probe = "rnat iptables -t nat -L POSTROUTING -n -v | grep -i MASQ"
    sdn_probe = "ovs-ofctl -O OpenFlow13 dump-flows s1 | wc -l"

    # Compute integrity and optional signature on a canonical representation.
    tmp = AntiAIChallenge(
        week_id=6,
        student_id=student_id,
        challenge_id=challenge_id,
        issued_at_utc=issued,
        ttl_seconds=ttl_seconds,
        report_token=report_token,
        payload_token=payload_token,
        tcp_port=tcp_port,
        udp_port=udp_port,
        nat_probe_command=nat_probe,
        sdn_probe_command=sdn_probe,
        integrity_sha256="",
        signature_hmac_sha256=None,
    )
    data_wo = tmp.to_dict(include_integrity=False)
    integrity = AntiAIChallenge.compute_integrity(data_wo)

    signature = None
    if sign:
        if not secret:
            raise ValueError("Cannot sign challenge without a secret")
        signature = AntiAIChallenge.compute_signature(secret, data_wo)

    return AntiAIChallenge(
        **{**tmp.__dict__, "integrity_sha256": integrity, "signature_hmac_sha256": signature}
    )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate Week 6 anti-AI challenge")
    p.add_argument("--student-id", required=True, help="Student identifier used for this challenge")
    p.add_argument(
        "--ttl-seconds",
        type=int,
        default=DEFAULT_TTL_SECONDS,
        help="Validity window in seconds (default: 6 hours)",
    )
    p.add_argument(
        "--output",
        default="",
        help="Output YAML path. Default: artifacts/anti_ai/challenge_<student-id>.yaml",
    )
    p.add_argument(
        "--sign",
        action="store_true",
        help="Sign challenge using a secret from ANTI_AI_SECRET (recommended for CI)",
    )
    p.add_argument(
        "--secret-env",
        default="ANTI_AI_SECRET",
        help="Environment variable name that holds the signing secret",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()

    secret = os.environ.get(args.secret_env)
    challenge = generate_challenge(
        student_id=args.student_id,
        ttl_seconds=args.ttl_seconds,
        secret=secret,
        sign=bool(args.sign),
    )

    if args.output:
        out_path = Path(args.output)
    else:
        out_path = Path("artifacts") / "anti_ai" / f"challenge_{args.student_id}.yaml"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    challenge.save_yaml(str(out_path))

    print(f"Challenge written to: {out_path}")
    print(f"Report token:  {challenge.report_token}")
    print(f"Payload token: {challenge.payload_token}")
    print(f"TCP port:      {challenge.tcp_port}")
    print(f"UDP port:      {challenge.udp_port}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
