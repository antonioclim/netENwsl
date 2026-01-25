#!/usr/bin/env python3
"""Week 14 Laboratory Shutdown.

NETWORKING class — ASE, CSIE | Computer Networks Laboratory
by ing. dr. Antonio Clim

Gracefully stops all laboratory containers while preserving data.

IMPORTANT: Portainer will NEVER be stopped — it must remain running for all weeks.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Tuple

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def check_portainer_status() -> Tuple[bool, str]:
    """Check Portainer container status."""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=portainer", "--format", "{{.Names}}\t{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        output = result.stdout.strip()
        if not output:
            return False, "Not found"
        for line in output.split("\n"):
            if "portainer" in line.lower():
                parts = line.split("\t")
                return True, parts[1] if len(parts) >= 2 else "Running"
        return False, "Not found"
    except subprocess.TimeoutExpired:
        return False, "Timeout"


def stop_compose(compose_file: Path, remove_volumes: bool = False) -> bool:
    """Stop services defined in docker-compose.yml."""
    cmd = ["docker", "compose", "-f", str(compose_file), "down"]
    if remove_volumes:
        cmd.append("--volumes")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Stop Week 14 laboratory environment",
        epilog="NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim",
    )
    parser.add_argument("--remove-volumes", "-v", action="store_true")
    parser.add_argument("--force", "-f", action="store_true")
    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("  Week 14 Laboratory Shutdown")
    print("  NETWORKING class — ASE, CSIE")
    print("=" * 60)

    portainer_ok, portainer_status = check_portainer_status()
    print(f"\n  Portainer: {'✓' if portainer_ok else '✗'} {portainer_status} (will NOT be stopped)\n")

    compose_file = PROJECT_ROOT / "docker" / "docker-compose.yml"

    if args.remove_volumes and not args.force:
        print("  ⚠️  Warning: --remove-volumes will delete all data!")
        response = input("  Continue? [y/N]: ").strip().lower()
        if response != "y":
            print("  Cancelled.")
            return 0

    print("  Stopping containers...")
    if stop_compose(compose_file, remove_volumes=args.remove_volumes):
        print("\n  ✓ Lab environment stopped")
    else:
        print("\n  ✗ Failed to stop environment")
        return 1

    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
