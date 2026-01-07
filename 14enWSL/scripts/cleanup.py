#!/usr/bin/env python3
"""
cleanup.py - Week 14 Laboratory Cleanup
NETWORKING class - ASE, Informatics | by Revolvix

Removes all containers, networks, and optionally volumes to prepare
the system for the next laboratory session.

Usage:
    python scripts/cleanup.py              # Stop and remove containers
    python scripts/cleanup.py --full       # Also remove volumes and artifacts
    python scripts/cleanup.py --prune      # Also prune unused Docker resources
    python scripts/cleanup.py --dry-run    # Show what would be removed
"""

from __future__ import annotations

import subprocess
import sys
import argparse
import shutil
from pathlib import Path
from datetime import datetime


PROJECT_ROOT = Path(__file__).parent.parent
DOCKER_DIR = PROJECT_ROOT / "docker"
COMPOSE_FILE = DOCKER_DIR / "docker-compose.yml"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
PCAP_DIR = PROJECT_ROOT / "pcap"

WEEK_PREFIX = "week14"


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
        "DRY": Colours.YELLOW,
    }
    colour = colours.get(level, Colours.RESET)
    print(f"[{ts}] {colour}[{level}]{Colours.RESET} {message}")


def run_command(cmd: list, timeout: int = 120, dry_run: bool = False) -> tuple:
    """Run a command and return (success, stdout, stderr)."""
    if dry_run:
        log("DRY", f"Would run: {' '.join(cmd)}")
        return True, "", ""

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


def docker_compose(*args, dry_run: bool = False) -> tuple:
    """Run docker compose command."""
    cmd = ["docker", "compose", "-f", str(COMPOSE_FILE)] + list(args)
    return run_command(cmd, dry_run=dry_run)


def remove_containers_by_label(label: str, dry_run: bool = False) -> bool:
    """Remove all containers with a specific label."""
    # Get container IDs
    success, stdout, _ = run_command([
        "docker", "ps", "-aq", "--filter", f"label={label}"
    ])

    if not stdout.strip():
        log("INFO", "No containers found with label")
        return True

    container_ids = stdout.strip().split("\n")
    log("INFO", f"Found {len(container_ids)} container(s) to remove")

    if dry_run:
        for cid in container_ids:
            log("DRY", f"Would remove container: {cid[:12]}")
        return True

    # Stop containers first
    run_command(["docker", "stop"] + container_ids, timeout=60)

    # Remove containers
    success, _, stderr = run_command(["docker", "rm", "-f"] + container_ids)
    return success


def remove_networks_by_label(label: str, dry_run: bool = False) -> bool:
    """Remove all networks with a specific label."""
    success, stdout, _ = run_command([
        "docker", "network", "ls", "-q", "--filter", f"label={label}"
    ])

    if not stdout.strip():
        log("INFO", "No networks found with label")
        return True

    network_ids = stdout.strip().split("\n")
    log("INFO", f"Found {len(network_ids)} network(s) to remove")

    if dry_run:
        for nid in network_ids:
            log("DRY", f"Would remove network: {nid[:12]}")
        return True

    success, _, stderr = run_command(["docker", "network", "rm"] + network_ids)
    return success


def remove_volumes_by_prefix(prefix: str, dry_run: bool = False) -> bool:
    """Remove all volumes with a specific prefix."""
    success, stdout, _ = run_command([
        "docker", "volume", "ls", "-q", "--filter", f"name={prefix}"
    ])

    if not stdout.strip():
        log("INFO", "No volumes found with prefix")
        return True

    volume_names = stdout.strip().split("\n")
    log("INFO", f"Found {len(volume_names)} volume(s) to remove")

    if dry_run:
        for vname in volume_names:
            log("DRY", f"Would remove volume: {vname}")
        return True

    success, _, stderr = run_command(["docker", "volume", "rm"] + volume_names)
    return success


def clean_directory(directory: Path, keep_gitkeep: bool = True, dry_run: bool = False) -> int:
    """Clean all files in a directory. Returns number of files removed."""
    if not directory.exists():
        return 0

    count = 0
    for item in directory.iterdir():
        if keep_gitkeep and item.name == ".gitkeep":
            continue
        if item.name == "README.md":
            continue

        if dry_run:
            log("DRY", f"Would remove: {item}")
        else:
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        count += 1

    return count


def main() -> int:
    """Run cleanup operations."""
    parser = argparse.ArgumentParser(description="Cleanup Week 14 Laboratory")
    parser.add_argument(
        "--full",
        action="store_true",
        help="Remove volumes and all data (use before next week)"
    )
    parser.add_argument(
        "--prune",
        action="store_true",
        help="Also prune unused Docker resources system-wide"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be removed without removing"
    )

    args = parser.parse_args()

    print()
    print("=" * 60)
    print(f"  {Colours.BOLD}Cleaning up Week 14 Laboratory{Colours.RESET}")
    print("=" * 60)
    print()

    if args.dry_run:
        log("INFO", "DRY RUN - No changes will be made")
        print()

    errors = 0

    # =========================================================================
    # Stop and remove containers via compose
    # =========================================================================
    if COMPOSE_FILE.exists():
        log("INFO", "Stopping containers via docker compose...")
        if args.full:
            success, _, stderr = docker_compose("down", "-v", "--remove-orphans", dry_run=args.dry_run)
        else:
            success, _, stderr = docker_compose("down", "--remove-orphans", dry_run=args.dry_run)

        if success:
            log("OK", "Docker compose cleanup complete")
        else:
            log("WARN", f"Docker compose cleanup had issues: {stderr}")
            errors += 1

    # =========================================================================
    # Remove any remaining containers by label
    # =========================================================================
    log("INFO", f"Removing {WEEK_PREFIX}_* containers...")
    if not remove_containers_by_label(f"week=14", dry_run=args.dry_run):
        errors += 1

    # =========================================================================
    # Remove networks by label
    # =========================================================================
    log("INFO", f"Removing {WEEK_PREFIX}_* networks...")
    if not remove_networks_by_label(f"week=14", dry_run=args.dry_run):
        errors += 1

    # =========================================================================
    # Remove volumes (if --full)
    # =========================================================================
    if args.full:
        log("INFO", f"Removing {WEEK_PREFIX}_* volumes...")
        if not remove_volumes_by_prefix(WEEK_PREFIX, dry_run=args.dry_run):
            errors += 1

    # =========================================================================
    # Clean artifacts and pcap directories (if --full)
    # =========================================================================
    if args.full:
        log("INFO", "Cleaning artifacts directory...")
        count = clean_directory(ARTIFACTS_DIR, dry_run=args.dry_run)
        if count > 0:
            log("OK", f"Removed {count} file(s) from artifacts/")

        log("INFO", "Cleaning pcap directory...")
        count = clean_directory(PCAP_DIR, dry_run=args.dry_run)
        if count > 0:
            log("OK", f"Removed {count} file(s) from pcap/")

    # =========================================================================
    # System prune (if --prune)
    # =========================================================================
    if args.prune and not args.dry_run:
        log("INFO", "Pruning unused Docker resources...")
        success, stdout, _ = run_command([
            "docker", "system", "prune", "-f"
        ])
        if success:
            log("OK", "Docker system prune complete")
            # Parse and display space reclaimed
            if "reclaimed" in stdout.lower():
                for line in stdout.split("\n"):
                    if "reclaimed" in line.lower():
                        log("INFO", line.strip())
    elif args.prune and args.dry_run:
        log("DRY", "Would run: docker system prune -f")

    # =========================================================================
    # Summary
    # =========================================================================
    print()
    print("=" * 60)

    if errors == 0:
        print(f"  {Colours.GREEN}{Colours.BOLD}Cleanup complete!{Colours.RESET}")
        if args.full:
            print(f"  System is ready for the next laboratory session.")
    else:
        print(f"  {Colours.YELLOW}{Colours.BOLD}Cleanup completed with {errors} warning(s){Colours.RESET}")

    print("=" * 60)
    print()

    if not args.dry_run:
        # Show current Docker disk usage
        log("INFO", "Current Docker disk usage:")
        run_command(["docker", "system", "df"])

    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
