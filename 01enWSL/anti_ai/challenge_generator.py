#!/usr/bin/env python3
"""Anti-AI challenge generator for Week 1.

This module creates a per-student challenge file for the Week 1 homework.
The challenge is designed so that a valid submission must include artefacts
that are difficult to fabricate with a language model alone, especially a
PCAP file that contains a unique payload token.

The challenge file is not intended to be a cryptographic secret. It is an
individualisation and anti-reuse mechanism.

Usage
    python -m anti_ai.challenge_generator --student-id ABC123
    python -m anti_ai.challenge_generator --student-id ABC123 --output artifacts/anti_ai/challenge_ABC123.yaml

Outputs
- A YAML or JSON file containing:
  - metadata (student id, session token, validity window)
  - report token that must appear in the written report
  - payload token that must appear in the submitted PCAPs
  - a recommended port for traffic generation
"""

from __future__ import annotations

import argparse
import hashlib
import json
import secrets
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc


DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent.parent / "artifacts" / "anti_ai"
DEFAULT_VALID_HOURS = 24
PORT_RANGE = (10000, 10999)


def _sanitise_student_id(student_id: str) -> str:
    cleaned = "".join(c for c in student_id.strip() if c.isalnum() or c in "-_")
    return cleaned[:20]


def _verification_hash(student_id: str, session_token: str, generated_at: str) -> str:
    data = f"{student_id}:{session_token}:{generated_at}:week1"
    return hashlib.sha256(data.encode("utf-8")).hexdigest()[:16]


def _recommended_port(session_token: str) -> int:
    offset = int(session_token[:4], 16) % (PORT_RANGE[1] - PORT_RANGE[0] + 1)
    return PORT_RANGE[0] + offset


@dataclass
class Week1Challenge:
    """A per-student Week 1 challenge."""

    student_id: str
    valid_hours: int = DEFAULT_VALID_HOURS
    session_token: str = field(default_factory=lambda: secrets.token_hex(16))
    generated_at_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        student_id = _sanitise_student_id(self.student_id)
        session_token = self.session_token
        generated_at = self.generated_at_utc
        ver_hash = _verification_hash(student_id, session_token, generated_at)

        port = _recommended_port(session_token)

        report_token = f"W1-REPORT-{student_id}-{session_token[:8]}"
        payload_token = f"W1-PCAP-{student_id}-{session_token[:12]}"

        return {
            "metadata": {
                "week": 1,
                "student_id": student_id,
                "session_token": session_token,
                "generated_at_utc": generated_at,
                "valid_hours": int(self.valid_hours),
                "expires_at_utc": (datetime.fromisoformat(generated_at) + timedelta(hours=int(self.valid_hours))).isoformat(),
                "verification_hash": ver_hash,
            },
            "challenges": {
                "report": {
                    "token": report_token,
                    "instructions": "Include this token in your network_report.md in the Anti-AI Verification section.",
                },
                "pcap": {
                    "payload_token": payload_token,
                    "recommended_port": port,
                    "instructions": "Generate TCP and UDP traffic that contains the payload token and submit the resulting PCAPs.",
                },
                "submission": {
                    "required_files": [
                        "network_report.md",
                        "tcp_analysis.pcap",
                        "udp_analysis.pcap",
                        "evidence.json",
                    ]
                },
            },
        }


def _write_yaml(data: dict[str, Any], path: Path) -> None:
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


def _write_json(data: dict[str, Any], path: Path) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def generate_challenge(student_id: str, valid_hours: int = DEFAULT_VALID_HOURS) -> dict[str, Any]:
    """Generate a challenge dictionary."""
    challenge = Week1Challenge(student_id=student_id, valid_hours=valid_hours)
    return challenge.to_dict()


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Week 1 anti-AI challenge")
    parser.add_argument("--student-id", required=True, help="Student identifier (will be sanitised)")
    parser.add_argument("--valid-hours", type=int, default=DEFAULT_VALID_HOURS, help="Challenge validity window")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output file (.yaml or .json). Default: artifacts/anti_ai/challenge_<student>.yaml",
    )
    args = parser.parse_args()

    data = generate_challenge(student_id=args.student_id, valid_hours=args.valid_hours)

    DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    default_path = DEFAULT_OUTPUT_DIR / f"challenge_{data['metadata']['student_id']}.yaml"
    out_path: Path = args.output or default_path

    if out_path.suffix.lower() in {".yaml", ".yml"}:
        _write_yaml(data, out_path)
    elif out_path.suffix.lower() == ".json":
        _write_json(data, out_path)
    else:
        raise SystemExit("Output must end with .yaml, .yml or .json")

    print(f"[OK] Challenge written: {out_path}")
    print(f"      Report token: {data['challenges']['report']['token']}")
    print(f"      PCAP payload: {data['challenges']['pcap']['payload_token']}")
    print(f"      Recommended port: {data['challenges']['pcap']['recommended_port']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
