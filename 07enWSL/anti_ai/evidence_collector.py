"""Evidence collector for the Week 7 anti-AI workflow."""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from .challenge import load_challenge
from .fingerprint import fingerprint_hash


def sha256_file(path: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run_probe(cmd: str, timeout: int = 8) -> Dict[str, Any]:
    try:
        p = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "cmd": cmd,
            "returncode": p.returncode,
            "stdout": (p.stdout or "").strip(),
            "stderr": (p.stderr or "").strip(),
        }
    except Exception as exc:
        return {"cmd": cmd, "error": str(exc)}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Collect submission evidence (Week 7 anti-AI).")
    p.add_argument("--challenge", required=True, type=Path, help="Path to challenge YAML")
    p.add_argument("--artefact", action="append", default=[], type=Path, help="Artefact file path (repeatable)")
    p.add_argument("--probe", action="append", default=[], help="Optional probe command (repeatable)")
    p.add_argument("--output", required=True, type=Path, help="Output evidence JSON")
    p.add_argument("--base-dir", default=Path("."), type=Path, help="Base directory for relative paths")
    return p


def main() -> int:
    args = build_parser().parse_args()
    chal = load_challenge(args.challenge)

    base = args.base_dir.resolve()
    artefacts: List[Dict[str, str]] = []
    missing: List[str] = []

    for a in args.artefact:
        ap = (base / a).resolve() if not a.is_absolute() else a
        if not ap.exists():
            missing.append(str(a))
            continue
        artefacts.append(
            {
                "path": str(ap.relative_to(base) if ap.is_relative_to(base) else ap),
                "sha256": sha256_file(ap),
                "bytes": str(ap.stat().st_size),
            }
        )

    probes = [run_probe(cmd) for cmd in args.probe]

    evidence: Dict[str, Any] = {
        "meta": {
            "week_id": chal.week_id,
            "student_id": chal.student_id,
            "attempt_id": chal.attempt_id,
            "issued_at_utc": chal.issued_at_utc,
            "ttl_seconds": chal.ttl_seconds,
            "challenge_hash": chal.challenge_hash,
        },
        "environment": {
            "fingerprint_hash": fingerprint_hash(),
        },
        "artefacts": artefacts,
        "probes": probes,
        "collector": {
            "version": "w7-1",
        },
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8")

    if missing:
        print("Warning: missing artefacts:")
        for m in missing:
            print("  -", m)

    print(f"Wrote evidence to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
