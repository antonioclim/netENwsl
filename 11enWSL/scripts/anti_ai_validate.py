#!/usr/bin/env python3
"""Validate Week 11 anti-AI artefacts.

This is useful both for students (self-check) and staff (batch validation).

Exit codes
----------
0 - validation passed
1 - validation failed
2 - missing inputs
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from anti_ai import validate_week11


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Week 11 anti-AI artefacts")
    parser.add_argument(
        "--challenge",
        default=str(PROJECT_ROOT / "artifacts" / "anti_ai" / "week11_challenge.json"),
        help="Challenge JSON path",
    )
    parser.add_argument(
        "--evidence",
        default=str(PROJECT_ROOT / "artifacts" / "anti_ai" / "week11_evidence.json"),
        help="Evidence JSON path",
    )
    parser.add_argument(
        "--pcap",
        default=str(PROJECT_ROOT / "pcap" / "week11_capture.pcap"),
        help="Capture file path (pcap or pcapng)",
    )
    parser.add_argument(
        "--secret",
        default=os.environ.get("ANTI_AI_SECRET"),
        help="Optional secret for signature verification (defaults to ANTI_AI_SECRET)",
    )

    args = parser.parse_args()

    result = validate_week11(
        challenge_path=args.challenge,
        evidence_path=args.evidence,
        pcap_path=args.pcap,
        secret=args.secret,
    )

    if result.ok:
        print("PASS")
    else:
        print("FAIL")

    if result.errors:
        print("\nErrors:")
        for e in result.errors:
            print(f"- {e}")

    if result.warnings:
        print("\nWarnings:")
        for w in result.warnings:
            print(f"- {w}")

    if result.metrics:
        print("\nMetrics:")
        print(json.dumps(result.metrics, indent=2, sort_keys=True))

    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
