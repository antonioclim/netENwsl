"""Generate proof artefacts for Week 2.

This script runs the *provided* Week 2 reference exercises:
- TCP server/client (ex_2_01_tcp.py)
- UDP server/client (ex_2_02_udp.py)

It sends a per‑student payload token from the challenge file and captures
the resulting logs. A language model can explain what to do but it cannot
generate these logs without actually running the programs.

Note: This does not require Docker.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from anti_ai.challenge import Challenge


PYTHON = sys.executable

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_cmd_capture(cmd: list[str], out_path: Path, timeout: int) -> int:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        out_path.write_text((p.stdout or "") + (p.stderr or ""), encoding="utf-8")
        return int(p.returncode)
    except subprocess.TimeoutExpired as exc:
        out_path.write_text(f"ERROR: timeout after {timeout}s\n{exc}\n", encoding="utf-8")
        return 124


def start_process_to_file(cmd: list[str], out_path: Path) -> subprocess.Popen:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    f = open(out_path, "w", encoding="utf-8")
    # We keep the file handle open; it will be closed on process termination.
    return subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT, text=True)


def terminate_process(proc: subprocess.Popen, grace: float = 2.0) -> None:
    if proc.poll() is not None:
        return
    try:
        proc.terminate()
        proc.wait(timeout=grace)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Week 2 proof traffic and capture logs")
    p.add_argument("--challenge", required=True, help="Path to challenge YAML")
    p.add_argument("--out-dir", default="", help="Output directory for proof artefacts")
    p.add_argument("--timeout", type=int, default=8, help="Timeout for each client run in seconds")
    p.add_argument("--startup-wait", type=float, default=0.4, help="Wait time after starting servers")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    ch = Challenge.load_yaml(args.challenge)

    out_dir = Path(args.out_dir) if args.out_dir else Path("artifacts/anti_ai") / f"proof_{ch.student_id}_{ch.short_id()}"
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    tcp_server_log = out_dir / "tcp_server.txt"
    tcp_client_log = out_dir / "tcp_client.txt"
    udp_server_log = out_dir / "udp_server.txt"
    udp_client_log = out_dir / "udp_client.txt"

    tcp_server_cmd = [PYTHON, "src/exercises/ex_2_01_tcp.py", "server", "--bind", "127.0.0.1", "--port", str(ch.tcp_port)]
    udp_server_cmd = [PYTHON, "src/exercises/ex_2_02_udp.py", "server", "--bind", "127.0.0.1", "--port", str(ch.udp_port)]

    tcp_client_cmd = [PYTHON, "src/exercises/ex_2_01_tcp.py", "client", "--host", "127.0.0.1", "--port", str(ch.tcp_port), "-m", ch.payload_token]
    udp_once = f"upper:{ch.payload_token}"
    udp_client_cmd = [PYTHON, "src/exercises/ex_2_02_udp.py", "client", "--host", "127.0.0.1", "--port", str(ch.udp_port), "--once", udp_once]

    summary: dict[str, Any] = {
        "meta": {
            "week_id": ch.week_id,
            "challenge_id": ch.challenge_id,
            "student_id": ch.student_id,
            "collected_at_utc": utc_now_iso(),
            "tcp_port": ch.tcp_port,
            "udp_port": ch.udp_port,
        },
        "commands": {
            "tcp_server": tcp_server_cmd,
            "tcp_client": tcp_client_cmd,
            "udp_server": udp_server_cmd,
            "udp_client": udp_client_cmd,
        },
        "results": {},
    }

    tcp_server = start_process_to_file(tcp_server_cmd, tcp_server_log)
    udp_server = start_process_to_file(udp_server_cmd, udp_server_log)

    time.sleep(float(args.startup_wait))

    try:
        rc_tcp = run_cmd_capture(tcp_client_cmd, tcp_client_log, timeout=int(args.timeout))
        rc_udp = run_cmd_capture(udp_client_cmd, udp_client_log, timeout=int(args.timeout))
        summary["results"]["tcp_client_returncode"] = rc_tcp
        summary["results"]["udp_client_returncode"] = rc_udp
    finally:
        terminate_process(tcp_server)
        terminate_process(udp_server)

    (out_dir / "proof_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    ok = summary["results"].get("tcp_client_returncode") == 0 and summary["results"].get("udp_client_returncode") == 0
    if ok:
        print(f"✓ Proof logs generated: {out_dir}")
        return 0

    print(f"✗ Proof generation failed, see: {out_dir}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
