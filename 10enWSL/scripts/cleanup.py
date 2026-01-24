#!/usr/bin/env python3
"""
Week 10 - Laboratory Cleanup Script
====================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

This script stops and removes all Docker containers for the Week 10 laboratory.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations
from typing import Optional, List, Dict, Tuple, Any

import argparse
import subprocess
import sys
from pathlib import Path


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCKER_COMPOSE_FILE = PROJECT_ROOT / "docker" / "docker-compose.yml"


# ═══════════════════════════════════════════════════════════════════════════════
# CLEANUP_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def stop_containers(compose_file: Path, remove_volumes: bool = False) -> bool:
    """
    Stop and remove Docker containers.
    
    Args:
        compose_file: Path to docker-compose.yml
        remove_volumes: If True, also remove volumes
    
    Returns:
        True if cleanup succeeded
    """
    if not compose_file.exists():
        print(f"[WARNING] Docker Compose file not found: {compose_file}")
        return True
    
    print("[INFO] Stopping Docker containers...")
    
    cmd = [
        "docker", "compose",
        "-f", str(compose_file),
        "down",
    ]
    
    if remove_volumes:
        cmd.append("-v")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
        )
        
        if result.returncode != 0:
            print(f"[ERROR] Failed to stop containers:")
            print(result.stderr)
            return False
        
        print("[OK] Containers stopped and removed")
        return True
    except subprocess.TimeoutExpired:
        print("[ERROR] Cleanup timed out")
        return False


def remove_output_files(output_dir: Path) -> None:
    """Remove generated output files."""
    if not output_dir.exists():
        return
    
    print(f"[INFO] Removing generated files in {output_dir}...")
    
    # Remove TLS certificates
    tls_dir = output_dir / "tls"
    if tls_dir.exists():
        for f in tls_dir.glob("*"):
            f.unlink()
            print(f"  Removed: {f}")


# ═══════════════════════════════════════════════════════════════════════════════
# ARGUMENT_PARSING
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Clean up Week 10 laboratory")
    parser.add_argument(
        "--volumes",
        action="store_true",
        help="Also remove Docker volumes",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Remove all generated files (including certificates)",
    )
    return parser.parse_args(argv)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main(argv: list[str]) -> int:
    """Main entry point."""
    args = parse_args(argv)
    
    print("=" * 60)
    print("Week 10 Laboratory Cleanup")
    print("=" * 60)
    
    # Stop containers
    if not stop_containers(DOCKER_COMPOSE_FILE, args.volumes):
        return 1
    
    # Remove generated files if requested
    if args.all:
        output_dir = PROJECT_ROOT / "output"
        remove_output_files(output_dir)
    
    print("\n[OK] Cleanup complete!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
