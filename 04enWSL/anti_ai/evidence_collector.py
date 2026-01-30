#!/usr/bin/env python3
"""anti_ai.evidence_collector

Collects submission evidence into a single JSON file.

Evidence contains:
- a hash of the challenge file
- hashes of user-provided artefacts (pcap, code, reports)
- a privacy-aware environment fingerprint

This design keeps the grading workflow deterministic and automatable.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from anti_ai.fingerprint import as_dict as fingerprint_as_dict
from anti_ai.fingerprint import collect_fingerprint


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _safe_run(cmd: List[str], timeout_s: int = 3) -> Dict[str, Any]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s)
        return {
            "cmd": cmd,
            "returncode": p.returncode,
            "stdout": p.stdout.strip(),
            "stderr": p.stderr.strip(),
        }
    except FileNotFoundError:
        return {"cmd": cmd, "returncode": None, "stdout": "", "stderr": "not found"}
    except subprocess.TimeoutExpired:
        return {"cmd": cmd, "returncode": None, "stdout": "", "stderr": "timeout"}


def collect_artefacts(base_dir: Path, artefact_paths: List[str]) -> List[Dict[str, Any]]:
    artefacts: List[Dict[str, Any]] = []
    for p_str in artefact_paths:
        p = (base_dir / p_str).resolve()
        if not p.exists():
            raise FileNotFoundError(f"Artefact not found: {p_str}")
        if p.is_dir():
            # Walk directories and hash files deterministically.
            for file_path in sorted(p.rglob("*")):
                if file_path.is_file():
                    rel = str(file_path.relative_to(base_dir))
                    artefacts.append(
                        {
                            "path": rel,
                            "size_bytes": file_path.stat().st_size,
                            "sha256": _sha256_file(file_path),
                            "mtime_utc": datetime.fromtimestamp(file_path.stat().st_mtime, tz=timezone.utc)
                            .isoformat()
                            .replace("+00:00", "Z"),
                        }
                    )
        else:
            rel = str(p.relative_to(base_dir))
            artefacts.append(
                {
                    "path": rel,
                    "size_bytes": p.stat().st_size,
                    "sha256": _sha256_file(p),
                    "mtime_utc": datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc)
                    .isoformat()
                    .replace("+00:00", "Z"),
                }
            )
    return artefacts


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect Week 4 submission evidence (JSON)")
    parser.add_argument(
        "--challenge",
        required=True,
        help="Path to the challenge YAML used for the submission",
    )
    parser.add_argument(
        "--artefact",
        action="append",
        default=[],
        help=(
            "Artefact path relative to the project root. "
            "Repeat --artefact for multiple files and directories."
        ),
    )
    parser.add_argument(
        "--output",
        default="artifacts/anti_ai/evidence.json",
        help="Output JSON path (default: artifacts/anti_ai/evidence.json)",
    )
    parser.add_argument(
        "--base-dir",
        default=".",
        help="Project root directory (default: current directory)",
    )
    parser.add_argument(
        "--include-commands",
        action="store_true",
        help="Include a small set of diagnostic command outputs",
    )
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    challenge_path = (base_dir / args.challenge).resolve()
    out_path = (base_dir / args.output).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not challenge_path.exists():
        raise FileNotFoundError(f"Challenge not found: {args.challenge}")

    # Default artefacts: include challenge itself plus common places for pcaps.
    artefacts_in = list(args.artefact)
    if not artefacts_in:
        # Make it hard to forget the PCAP.
        artefacts_in = [args.challenge]
        for candidate in [
            "pcap",
            "artifacts",
        ]:
            if (base_dir / candidate).exists():
                artefacts_in.append(candidate)

    fp = collect_fingerprint(extra_salt=str(challenge_path.name))
    artefacts = collect_artefacts(base_dir, artefacts_in)

    evidence: Dict[str, Any] = {
        "week": 4,
        "created_at_utc": _utc_now_iso(),
        "challenge_path": str(Path(args.challenge)),
        "challenge_sha256": _sha256_file(challenge_path),
        "fingerprint": fingerprint_as_dict(fp),
        "artefacts": artefacts,
    }

    if args.include_commands:
        evidence["commands"] = [
            _safe_run(["python3", "--version"]),
            _safe_run(["uname", "-a"]),
            _safe_run(["id"]),
            _safe_run(["ip", "addr"]),
            _safe_run(["ss", "-tulpn"]),
            _safe_run(["docker", "ps"]),
        ]

    out_path.write_text(json.dumps(evidence, indent=2, sort_keys=False), encoding="utf-8")
    print(f"Wrote evidence: {out_path}")
    print(f"Hashed {len(artefacts)} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
