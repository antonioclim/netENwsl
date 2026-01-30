#!/usr/bin/env python3
"""Evidence collector for Week 1 anti-AI workflow.

The evidence file is a machine-readable summary of submitted artefacts and
(optional) command outputs. It allows an automated validator to check that
required files exist, file hashes match and proof tokens are present.

The evidence file does not claim to be tamper-proof. It is paired with a
challenge file and validated by `anti_ai.submission_validator`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc

from anti_ai.fingerprint import build_fingerprint


COMMAND_TIMEOUT_SECONDS = 10
MAX_COMMAND_OUTPUT_CHARS = 8000


def _load_structured_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, encoding="utf-8") as f:
        if path.suffix.lower() in {".yaml", ".yml"}:
            return yaml.safe_load(f)
        if path.suffix.lower() == ".json":
            return json.load(f)

    raise ValueError("Unsupported file type. Use .yaml, .yml or .json")


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _run_cmd(cmd: list[str], timeout: int = COMMAND_TIMEOUT_SECONDS) -> str:
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        out = res.stdout if res.returncode == 0 else res.stderr
        out = (out or "").strip()
        if len(out) > MAX_COMMAND_OUTPUT_CHARS:
            return out[:MAX_COMMAND_OUTPUT_CHARS] + "\n[TRUNCATED]"
        return out
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as exc:
        return f"[ERROR] {exc}"


def collect_default_commands() -> dict[str, str]:
    """Collect a small, Week 1 relevant command transcript."""
    return {
        "ip_br_addr": _run_cmd(["ip", "-br", "addr", "show"]),
        "ip_route": _run_cmd(["ip", "route", "show"]),
        "ss_tunap": _run_cmd(["ss", "-tunap"]),
        "resolv_conf": _run_cmd(["cat", "/etc/resolv.conf"]),
    }


def build_evidence(
    *,
    challenge: dict[str, Any],
    artefacts: list[Path],
    base_dir: Path,
    include_commands: bool = False,
) -> dict[str, Any]:
    """Build an evidence dictionary.

    Args:
        challenge: Loaded challenge dictionary.
        artefacts: List of file paths to hash and include.
        base_dir: Base directory used to compute relative paths.
        include_commands: Whether to include command transcripts.

    Returns:
        Evidence dictionary.
    """
    meta = challenge.get("metadata", {})
    fp = build_fingerprint(include_features=False)

    files: list[dict[str, Any]] = []
    for p in artefacts:
        if not p.exists():
            raise FileNotFoundError(f"Missing artefact: {p}")
        if p.is_absolute():
            try:
                rel = str(p.resolve().relative_to(base_dir.resolve()))
            except ValueError:
                rel = str(p)
        else:
            rel = str(p)
        files.append(
            {
                "path": rel,
                "sha256": _sha256_file(p),
                "size_bytes": p.stat().st_size,
            }
        )

    evidence: dict[str, Any] = {
        "meta": {
            "week": 1,
            "student_id": meta.get("student_id"),
            "session_token": meta.get("session_token"),
            "challenge_generated_at_utc": meta.get("generated_at_utc"),
            "challenge_verification_hash": meta.get("verification_hash"),
            "collected_at_utc": datetime.now(timezone.utc).isoformat(),
        },
        "environment": {
            "fingerprint_hash": fp["fingerprint_hash"],
        },
        "artefacts": files,
    }

    if include_commands:
        evidence["commands"] = collect_default_commands()

    return evidence


def write_evidence_json(evidence: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w", encoding="utf-8") as f:
        json.dump(evidence, f, indent=2, ensure_ascii=False)


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect Week 1 anti-AI evidence")
    parser.add_argument("--challenge", type=Path, required=True, help="Challenge file (.yaml/.json)")
    parser.add_argument(
        "--artefact",
        type=Path,
        action="append",
        default=[],
        help="Artefact path to include (repeatable)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("evidence.json"),
        help="Evidence output path (default: evidence.json)",
    )
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=Path.cwd(),
        help="Base directory for relative paths (default: current directory)",
    )
    parser.add_argument(
        "--include-commands",
        action="store_true",
        help="Include command transcripts (ip, ss, resolv.conf)",
    )
    args = parser.parse_args()

    if not args.artefact:
        raise SystemExit("Provide at least one --artefact")

    challenge = _load_structured_file(args.challenge)
    evidence = build_evidence(
        challenge=challenge,
        artefacts=[p if p.is_absolute() else (args.base_dir / p) for p in args.artefact],
        base_dir=args.base_dir,
        include_commands=args.include_commands,
    )
    write_evidence_json(evidence, args.output)

    print(f"[OK] Evidence written: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
