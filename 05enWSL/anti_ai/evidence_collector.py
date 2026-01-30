#!/usr/bin/env python3
"""
Evidence collector for Week 5 submissions.

This script creates an `evidence.json` file that records:
- which challenge was used
- hashes of the submitted artefacts
- a minimal environment fingerprint (hashed)

Usage
-----
    python -m anti_ai.evidence_collector \
        --challenge artifacts/anti_ai/challenge_ABC123.yaml \
        --artefact subnet_plan_ABC123.json \
        --artefact ipv6_report_ABC123.json \
        --output evidence_ABC123.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Dict, List

from anti_ai.challenge import load_challenge, utc_now_iso
from anti_ai.fingerprint import compute_fingerprint


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Collect evidence for a Week 5 anti-AI submission.")
    p.add_argument("--challenge", type=Path, required=True, help="Path to the challenge YAML")
    p.add_argument(
        "--artefact",
        type=Path,
        action="append",
        required=True,
        help="Artefact file path to include (repeat for multiple files)",
    )
    p.add_argument("--output", type=Path, default=None, help="Output evidence JSON path")
    p.add_argument("--base-dir", type=Path, default=Path("."), help="Base directory for relative paths")
    return p


def main() -> int:
    args = build_arg_parser().parse_args()
    base_dir: Path = args.base_dir.resolve()

    challenge = load_challenge(args.challenge)
    fp = compute_fingerprint()

    artefacts: List[Dict[str, str]] = []
    for f in args.artefact:
        abs_path = (base_dir / f).resolve() if not f.is_absolute() else f.resolve()
        if not abs_path.exists():
            raise SystemExit(f"[ERROR] Missing artefact: {abs_path}")
        rel = str(abs_path.relative_to(base_dir)) if abs_path.is_relative_to(base_dir) else str(abs_path)
        artefacts.append({"path": rel, "sha256": sha256_file(abs_path)})

    out = args.output
    if out is None:
        out = base_dir / challenge.outputs["evidence_json"]

    evidence = {
        "meta": {
            "week": challenge.week,
            "student_id": challenge.student_id,
            "challenge_sha256": challenge.compute_integrity(),
            "issued_at_utc": challenge.issued_at_utc,
            "collected_at_utc": utc_now_iso(),
        },
        "environment": {
            "fingerprint_sha256": fp.fingerprint_sha256,
            "signals": fp.inputs,
        },
        "artefacts": artefacts,
    }

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(evidence, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] Evidence written to: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
