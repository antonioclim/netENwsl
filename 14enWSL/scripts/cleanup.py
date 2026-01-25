#!/usr/bin/env python3
"""Week 14 Laboratory Cleanup.

NETWORKING class — ASE, CSIE | Computer Networks Laboratory
by ing. dr. Antonio Clim

Removes all containers, networks and optionally volumes.
Portainer will NEVER be removed.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

PROJECT_ROOT = Path(__file__).parent.parent
WEEK_PREFIX = "week14_"
PROTECTED_CONTAINERS = ["portainer"]


def is_protected(name: str) -> bool:
    """Check if a resource name is protected."""
    return any(p in name.lower() for p in PROTECTED_CONTAINERS)


def cleanup_containers(prefix: str = WEEK_PREFIX) -> int:
    """Remove containers matching prefix, excluding protected."""
    try:
        result = subprocess.run(
            ["docker", "ps", "-a", "--format", "{{.Names}}"],
            capture_output=True, text=True, timeout=30,
        )
        containers = result.stdout.strip().split("\n")
        removed = 0
        for container in containers:
            if not container or is_protected(container):
                continue
            if prefix and not container.startswith(prefix):
                continue
            subprocess.run(["docker", "rm", "-f", container], capture_output=True, timeout=30)
            removed += 1
            print(f"    Removed container: {container}")
        return removed
    except subprocess.TimeoutExpired:
        return 0


def cleanup_networks(prefix: str = WEEK_PREFIX) -> int:
    """Remove networks matching prefix."""
    try:
        result = subprocess.run(
            ["docker", "network", "ls", "--format", "{{.Name}}"],
            capture_output=True, text=True, timeout=30,
        )
        networks = result.stdout.strip().split("\n")
        protected = ["bridge", "host", "none"]
        removed = 0
        for network in networks:
            if not network or network in protected:
                continue
            if prefix and not network.startswith(prefix):
                continue
            subprocess.run(["docker", "network", "rm", network], capture_output=True, timeout=30)
            removed += 1
        return removed
    except subprocess.TimeoutExpired:
        return 0


def cleanup_volumes(prefix: str = WEEK_PREFIX) -> int:
    """Remove volumes matching prefix."""
    try:
        result = subprocess.run(
            ["docker", "volume", "ls", "--format", "{{.Name}}"],
            capture_output=True, text=True, timeout=30,
        )
        volumes = result.stdout.strip().split("\n")
        protected = ["portainer_data"]
        removed = 0
        for volume in volumes:
            if not volume or volume in protected or is_protected(volume):
                continue
            if prefix and not volume.startswith(prefix):
                continue
            subprocess.run(["docker", "volume", "rm", volume], capture_output=True, timeout=30)
            removed += 1
        return removed
    except subprocess.TimeoutExpired:
        return 0


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Clean up Week 14 laboratory resources",
        epilog="NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim",
    )
    parser.add_argument("--volumes", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("  Week 14 Laboratory Cleanup")
    print("  NETWORKING class — ASE, CSIE")
    print("=" * 60)
    print("\n  ⚠️  Portainer will NOT be affected\n")

    print("  Cleaning containers...")
    containers = 0 if args.dry_run else cleanup_containers()
    print(f"    Removed: {containers} containers")

    print("  Cleaning networks...")
    networks = 0 if args.dry_run else cleanup_networks()
    print(f"    Removed: {networks} networks")

    if args.volumes or args.all:
        print("  Cleaning volumes...")
        volumes = 0 if args.dry_run else cleanup_volumes()
        print(f"    Removed: {volumes} volumes")

    print("\n  ✓ Cleanup complete\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
