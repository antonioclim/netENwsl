"""Evidence collector for Week 13.

The collector is intentionally simple: it hashes the artefacts that will be submitted and stores
minimal environment metadata. This enables the validator to confirm that files were not changed
after evidence generation and supports a clean audit trail.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import platform
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml


def _utc_now() -> str:
    return _dt.datetime.now(tz=_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _fingerprint_hash() -> str:
    data = "|".join(
        [
            platform.system(),
            platform.release(),
            platform.machine(),
            platform.python_version(),
        ]
    ).encode("utf-8")
    return hashlib.sha256(data).hexdigest()[:16]


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Collect Week 13 anti-AI evidence")
    p.add_argument("--challenge", required=True, help="Path to challenge YAML")
    p.add_argument("--artefact", action="append", default=[], help="Artefact path (repeatable)")
    p.add_argument("--base-dir", default=".", help="Base directory for relative paths")
    p.add_argument("--output", default="evidence.json", help="Evidence JSON output path")
    p.add_argument("--include-commands", action="store_true", help="Include selected command outputs")
    p.add_argument("--command", action="append", default=[], help="Command to execute and store output")
    return p


def main() -> int:
    args = build_arg_parser().parse_args()
    base_dir = Path(args.base_dir).resolve()

    challenge_path = Path(args.challenge)
    challenge = yaml.safe_load(challenge_path.read_text(encoding="utf-8"))
    artefacts: List[Dict[str, Any]] = []

    for rel in args.artefact:
        p = (base_dir / rel).resolve()
        if not p.exists():
            raise SystemExit(f"[ERROR] Artefact not found: {rel}")
        artefacts.append({"path": str(Path(rel)), "sha256": _sha256_file(p)})

    probes: Dict[str, Any] = {}
    if args.include_commands:
        import subprocess

        for cmd in args.command:
            try:
                completed = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
                probes[cmd] = (completed.stdout + completed.stderr).strip()
            except Exception as exc:  # pragma: no cover
                probes[cmd] = f"[ERROR] {exc}"

    evidence = {
        "meta": {
            "week_id": 13,
            "student_id": str(challenge.get("student_id", "")),
            "challenge_id": str(challenge.get("challenge_id", "")),
            "issued_at_utc": str(challenge.get("issued_at_utc", "")),
            "collected_at_utc": _utc_now(),
            "ttl_seconds": int(challenge.get("ttl_seconds", 0)),
            "fingerprint_hash": _fingerprint_hash(),
        },
        "artefacts": artefacts,
        "probes": probes,
    }

    out = Path(args.output)
    out.write_text(json.dumps(evidence, indent=2, sort_keys=False), encoding="utf-8")
    print(f"[OK] Evidence written to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
