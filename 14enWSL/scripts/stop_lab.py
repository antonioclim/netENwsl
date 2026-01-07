#!/usr/bin/env python3
"""
stop_lab.py - Week 14 Laboratory Shutdown
NETWORKING class - ASE, Informatics | by Revolvix

Gracefully stops all laboratory containers.

Usage:
    python scripts/stop_lab.py
    python scripts/stop_lab.py --timeout 30
"""

from __future__ import annotations

import subprocess
import sys
import argparse
from pathlib import Path
from datetime import datetime


PROJECT_ROOT = Path(__file__).parent.parent
DOCKER_DIR = PROJECT_ROOT / "docker"
COMPOSE_FILE = DOCKER_DIR / "docker-compose.yml"


class Colours:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def log(level: str, message: str) -> None:
    """Print timestamped log message."""
    ts = datetime.now().strftime("%H:%M:%S")
    colours = {
        "INFO": Colours.BLUE,
        "OK": Colours.GREEN,
        "WARN": Colours.YELLOW,
        "ERROR": Colours.RED,
    }
    colour = colours.get(level, Colours.RESET)
    print(f"[{ts}] {colour}[{level}]{Colours.RESET} {message}")


def run_command(cmd: list, timeout: int = 60) -> tuple:
    """Run a command and return (success, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=PROJECT_ROOT
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


def docker_compose(*args) -> tuple:
    """Run docker compose command."""
    cmd = ["docker", "compose", "-f", str(COMPOSE_FILE)] + list(args)
    return run_command(cmd)


def main() -> int:
    """Stop the laboratory environment."""
    parser = argparse.ArgumentParser(description="Stop Week 14 Laboratory")
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=30,
        help="Timeout for stopping containers (default: 30s)"
    )

    args = parser.parse_args()

    print()
    print("=" * 60)
    print(f"  {Colours.BOLD}Stopping Week 14 Laboratory{Colours.RESET}")
    print("=" * 60)
    print()

    # Check if compose file exists
    if not COMPOSE_FILE.exists():
        log("WARN", f"Compose file not found: {COMPOSE_FILE}")
        log("INFO", "Attempting to stop containers by label...")

        # Try stopping containers by label
        success, stdout, stderr = run_command([
            "docker", "stop",
            "$(docker ps -q --filter label=week=14)"
        ])
        return 0

    log("INFO", "Stopping containers...")
    success, stdout, stderr = docker_compose("stop", "-t", str(args.timeout))

    if success:
        log("OK", "All containers stopped")
    else:
        log("WARN", f"Some containers may not have stopped cleanly: {stderr}")

    # Verify shutdown
    log("INFO", "Verifying shutdown...")
    success, stdout, _ = run_command([
        "docker", "ps", "-q", "--filter", "label=week=14"
    ])

    if stdout.strip():
        running = len(stdout.strip().split("\n"))
        log("WARN", f"{running} container(s) still running")
        return 1
    else:
        log("OK", "All Week 14 containers stopped")

    print()
    print("=" * 60)
    print(f"  {Colours.GREEN}Laboratory shutdown complete{Colours.RESET}")
    print("=" * 60)
    print()
    print("To restart: python scripts/start_lab.py")
    print("To cleanup:  python scripts/cleanup.py --full")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
