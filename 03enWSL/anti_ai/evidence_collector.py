#!/usr/bin/env python3
"""Evidence collector for the Week 3 anti-AI workflow.

The collector creates an `evidence.json` file with:
- challenge metadata
- a minimal environment fingerprint (hash only)
- SHA-256 hashes for all submitted artefacts
- optional command transcripts (useful for auditing and debugging)

This file is intended to be submitted together with the artefacts listed inside it.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from anti_ai.challenge import load_challenge, sha256_hex
from anti_ai.fingerprint import compute_fingerprint


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _file_sha256(path: Path) -> str:
    h = sha256_hex(b"")
    # implement streaming
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _run_command(cmd: str, timeout_s: int = 20) -> dict[str, Any]:
    """Run a shell command and capture stdout, stderr and return code."""
    try:
        completed = subprocess.run(
            cmd,
            shell=True,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
        return {
            "cmd": cmd,
            "returncode": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        }
    except subprocess.TimeoutExpired:
        return {"cmd": cmd, "returncode": None, "stdout": "", "stderr": "TIMEOUT"}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Collect evidence for Week 3 submissions")
    p.add_argument("--challenge", required=True, help="Path to the challenge YAML file")
    p.add_argument(
        "--artefact",
        action="append",
        default=[],
        help="File to include in evidence (repeatable)",
    )
    p.add_argument(
        "--command",
        action="append",
        default=[],
        help="Shell command to record in evidence (repeatable)",
    )
    p.add_argument(
        "--output",
        default="evidence.json",
        help="Output evidence JSON file (default: evidence.json)",
    )
    p.add_argument(
        "--base-dir",
        default=".",
        help="Base directory for artefact paths (default: .)",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    challenge_path = Path(args.challenge)
    challenge = load_challenge(challenge_path)

    base_dir = Path(args.base_dir).resolve()
    artefact_paths: list[Path] = []
    for a in args.artefact:
        artefact_paths.append((base_dir / a).resolve())

    missing = [str(p) for p in artefact_paths if not p.exists()]
    if missing:
        print("ERROR: Missing artefacts:")
        for p in missing:
            print(f"  - {p}")
        return 2

    fp = compute_fingerprint(extra={"week": challenge.week})
    evidence: dict[str, Any] = {
        "meta": {
            "week": challenge.week,
            "student_id": challenge.student_id,
            "challenge_file": str(challenge_path.as_posix()),
            "created_at_utc": _utc_now_iso(),
        },
        "environment": {
            "fingerprint_sha256": fp.hash_hex,
        },
        "artefacts": [],
        "commands": [],
    }

    for pth in artefact_paths:
        evidence["artefacts"].append(
            {
                "path": str(pth.relative_to(base_dir).as_posix()),
                "sha256": _file_sha256(pth),
                "bytes": pth.stat().st_size,
            }
        )

    for cmd in args.command:
        evidence["commands"].append(_run_command(cmd))

    out_path = (base_dir / args.output).resolve()
    out_path.write_text(json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Evidence written to: {out_path}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
