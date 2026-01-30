#!/usr/bin/env python3
"""Collect Week 8 anti-AI evidence.

This creates `artifacts/anti_ai/evidence.json` which records hashes and basic
metadata for:
  - artifacts/student_context.json
  - all required PCAP files (as defined in the context)

It is safe to run multiple times, it will overwrite the evidence file.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure repository root is on sys.path when running as a script
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from anti_ai.evidence_collector import collect_evidence


def load_context(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Collect Week 8 anti-AI evidence")
    parser.add_argument(
        "--context",
        default="artifacts/student_context.json",
        help="Path to student_context.json",
    )
    parser.add_argument(
        "--out",
        default="artifacts/anti_ai/evidence.json",
        help="Output path for evidence.json",
    )
    parser.add_argument(
        "--notes",
        default="",
        help="Optional notes (kept in evidence.json)",
    )

    args = parser.parse_args()
    root = Path(".").resolve()
    ctx_path = root / args.context

    if not ctx_path.exists():
        print("Error: student context not found. Run: make init ID=your_student_id")
        return 1

    ctx = load_context(ctx_path)
    required_paths: list[Path] = []
    for info in (ctx.get("required_captures") or {}).values():
        fname = (info or {}).get("filename")
        if fname:
            required_paths.append(root / str(fname))

    collect_evidence(
        project_root=root,
        required_paths=required_paths,
        context_file=ctx_path,
        output_path=root / args.out,
        extra_notes=str(args.notes),
    )

    print(f"Evidence written to: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
