"""Evidence collection for Week 2 submissions.

Evidence is a machine‑readable manifest of artefacts plus a small amount of
environment metadata. It supports automated validation and makes it much harder
to submit plausible looking text without actually running the lab.

This is not a surveillance tool. Only minimal diagnostic information is recorded.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from anti_ai.challenge import Challenge
from anti_ai.fingerprint import compute_fingerprint


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_cmd(cmd: list[str], timeout: int = 5) -> dict[str, Any]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {
            "cmd": cmd,
            "returncode": p.returncode,
            "stdout": (p.stdout or "").strip(),
            "stderr": (p.stderr or "").strip(),
        }
    except Exception as exc:
        return {"cmd": cmd, "error": str(exc)}


def build_evidence(challenge: Challenge, base_dir: Path, artefacts: Iterable[Path], include_commands: bool) -> dict[str, Any]:
    fp = compute_fingerprint()

    artefact_entries: list[dict[str, Any]] = []
    for rel in artefacts:
        abs_path = (base_dir / rel).resolve()
        if not abs_path.exists():
            raise FileNotFoundError(f"Missing artefact: {rel}")
        artefact_entries.append({
            "path": str(rel).replace("\\", "/"),
            "sha256": sha256_file(abs_path),
            "bytes": abs_path.stat().st_size,
        })

    evidence: dict[str, Any] = {
        "meta": {
            "week_id": challenge.week_id,
            "challenge_id": challenge.challenge_id,
            "student_id": challenge.student_id,
            "issued_at_utc": challenge.issued_at_utc,
            "ttl_seconds": challenge.ttl_seconds,
            "collected_at_utc": utc_now_iso(),
            "challenge_payload_sha256": challenge.stable_hash(),
        },
        "environment": {
            "fingerprint": fp.to_dict(),
        },
        "artefacts": artefact_entries,
    }

    if include_commands:
        evidence["commands"] = [
            run_cmd(["python3", "--version"]),
            run_cmd(["uname", "-a"]),
            run_cmd(["id"]),
            run_cmd(["docker", "ps"], timeout=8),
        ]

    return evidence


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Collect Week 2 anti‑AI evidence into evidence.json")
    p.add_argument("--challenge", required=True, help="Path to challenge YAML")
    p.add_argument("--base-dir", default=".", help="Base directory for artefact paths")
    p.add_argument("--artefact", action="append", default=[], help="Artefact path relative to base-dir (repeatable)")
    p.add_argument("--output", default="evidence.json", help="Output evidence JSON path")
    p.add_argument("--include-commands", action="store_true", help="Include minimal command outputs for diagnostics")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    ch = Challenge.load_yaml(args.challenge)

    base_dir = Path(args.base_dir).resolve()
    artefacts = [Path(a) for a in args.artefact]

    evidence = build_evidence(ch, base_dir, artefacts, include_commands=bool(args.include_commands))

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"✓ Evidence written: {out_path} ({len(artefacts)} artefacts)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
