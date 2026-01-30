#!/usr/bin/env python3
"""Evidence collection for Week 6 anti-AI workflow.

The collector writes an evidence JSON file which lists artefacts and their hashes,
includes a minimal fingerprint hash and can optionally run live probes.

Live probes
- NAT: iptables MASQUERADE counters inside the Mininet container
- SDN: OVS flow count inside the Mininet container

This tool is designed to be robust:
- If Docker is not available it records probe status as unavailable.
- If commands fail it records stderr for debugging.
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
from typing import Any, Dict, List, Optional, Sequence, Tuple

from anti_ai.challenge import AntiAIChallenge
from anti_ai.fingerprint import compute_fingerprint_hash


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _run_cmd(cmd: Sequence[str], timeout: int = 20) -> Tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except FileNotFoundError:
        return 127, "", f"Command not found: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return 124, "", "Command timed out"
    except Exception as e:  # pragma: no cover
        return 1, "", str(e)


def _docker_exec(container: str, command: str) -> Dict[str, Any]:
    rc, out, err = _run_cmd(["docker", "exec", container, "bash", "-lc", command], timeout=30)
    return {"returncode": rc, "stdout": out, "stderr": err, "command": command}


def collect_probes(challenge: AntiAIChallenge, docker_container: str) -> Dict[str, Any]:
    probes: Dict[str, Any] = {}
    probes["nat_probe"] = _docker_exec(docker_container, challenge.nat_probe_command)
    probes["sdn_probe"] = _docker_exec(docker_container, challenge.sdn_probe_command)
    return probes


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Collect Week 6 anti-AI evidence")
    p.add_argument("--challenge", required=True, help="Path to a challenge YAML")
    p.add_argument(
        "--artefact",
        action="append",
        default=[],
        help="Artefact path to include (repeatable)",
    )
    p.add_argument(
        "--output",
        default="evidence.json",
        help="Evidence JSON output path",
    )
    p.add_argument(
        "--base-dir",
        default=".",
        help="Base directory for resolving relative artefact paths",
    )
    p.add_argument(
        "--run-probes",
        action="store_true",
        help="Run NAT and SDN live probes using docker exec",
    )
    p.add_argument(
        "--docker-container",
        default="week6_lab",
        help="Docker container name used for probes",
    )
    p.add_argument(
        "--note",
        default="",
        help="Optional free-text note that will be included in evidence",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    base_dir = Path(args.base_dir).resolve()

    challenge = AntiAIChallenge.load_yaml(args.challenge)

    evidence: Dict[str, Any] = {
        "meta": {
            "week_id": challenge.week_id,
            "student_id": challenge.student_id,
            "challenge_id": challenge.challenge_id,
            "issued_at_utc": challenge.issued_at_iso,
            "ttl_seconds": challenge.ttl_seconds,
            "collected_at_utc": _utc_now().replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        },
        "environment": {
            "fingerprint_hash": compute_fingerprint_hash(salt=challenge.challenge_id),
            "platform": os.name,
        },
        "artefacts": [],
        "probes": {},
        "note": args.note,
    }

    artefacts: List[str] = list(args.artefact or [])
    for item in artefacts:
        rel = Path(item)
        full = (base_dir / rel).resolve()
        if not full.exists():
            raise SystemExit(f"Artefact not found: {rel}")
        evidence["artefacts"].append(
            {
                "path": str(rel).replace("\\", "/"),
                "sha256": sha256_file(full),
                "size_bytes": full.stat().st_size,
            }
        )

    if args.run_probes:
        evidence["probes"] = collect_probes(challenge, args.docker_container)
    else:
        evidence["probes"] = {"status": "not_run"}

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(evidence, indent=2, sort_keys=False) + "\n", encoding="utf-8")

    print(f"Evidence written to: {out_path}")
    print(f"Artefacts listed: {len(evidence['artefacts'])}")
    if args.run_probes:
        print("Live probes: executed")
    else:
        print("Live probes: not run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
