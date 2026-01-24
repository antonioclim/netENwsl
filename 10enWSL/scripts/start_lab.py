#!/usr/bin/env python3
"""
Week 10 - Laboratory Startup Script
====================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

This script starts all Docker containers required for the Week 10 laboratory.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations
from typing import Optional, List, Dict, Tuple, Any

import argparse
import subprocess
import sys
import time
from pathlib import Path


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCKER_COMPOSE_FILE = PROJECT_ROOT / "docker" / "docker-compose.yml"

SERVICES = ["web", "dns-server", "ssh-server", "ftp-server", "debug"]

HEALTH_CHECKS = [
    ("Web Server", "localhost", 8000),
    ("DNS Server", "localhost", 5353),
    ("SSH Server", "localhost", 2222),
    ("FTP Server", "localhost", 2121),
]


# ═══════════════════════════════════════════════════════════════════════════════
# DOCKER_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def check_docker() -> bool:
    """Check if Docker is available and running."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def start_containers(compose_file: Path, services: list[str]) -> bool:
    """
    Start Docker containers using docker-compose.
    
    💭 PREDICTION: What happens if a port is already in use?
    """
    if not compose_file.exists():
        print(f"[ERROR] Docker Compose file not found: {compose_file}")
        return False
    
    print("[INFO] Starting Docker containers...")
    
    cmd = [
        "docker", "compose",
        "-f", str(compose_file),
        "up", "-d",
    ] + services
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
        )
        
        if result.returncode != 0:
            print(f"[ERROR] Failed to start containers:")
            print(result.stderr)
            return False
        
        print("[OK] Containers started")
        return True
    except subprocess.TimeoutExpired:
        print("[ERROR] Container startup timed out")
        return False


def wait_for_services(checks: list[tuple[str, str, int]], timeout: int = 30) -> bool:
    """
    Wait for services to become available.
    
    Args:
        checks: List of (name, host, port) tuples
        timeout: Maximum wait time in seconds
    
    Returns:
        True if all services are ready
    """
    import socket
    
    print(f"[INFO] Waiting for services (timeout: {timeout}s)...")
    
    start = time.time()
    pending = list(checks)
    
    while pending and (time.time() - start) < timeout:
        for check in pending[:]:
            name, host, port = check
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(1)
                    sock.connect((host, port))
                print(f"  [OK] {name} ({host}:{port})")
                pending.remove(check)
            except (socket.timeout, ConnectionRefusedError, OSError):
                pass
        
        if pending:
            time.sleep(1)
    
    if pending:
        print("[WARNING] Some services did not start:")
        for name, host, port in pending:
            print(f"  [FAIL] {name} ({host}:{port})")
        return False
    
    return True


def show_status(compose_file: Path) -> None:
    """Show status of running containers."""
    cmd = [
        "docker", "compose",
        "-f", str(compose_file),
        "ps",
    ]
    
    subprocess.run(cmd)


# ═══════════════════════════════════════════════════════════════════════════════
# ARGUMENT_PARSING
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Start Week 10 laboratory")
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Service startup timeout in seconds",
    )
    parser.add_argument(
        "--no-wait",
        action="store_true",
        help="Don't wait for services to become ready",
    )
    return parser.parse_args(argv)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main(argv: list[str]) -> int:
    """Main entry point."""
    args = parse_args(argv)
    
    print("=" * 60)
    print("Week 10 Laboratory Startup")
    print("=" * 60)
    
    # Check Docker
    if not check_docker():
        print("[ERROR] Docker is not available or not running")
        print("[HINT] Start Docker Desktop or run: sudo service docker start")
        return 1
    
    print("[OK] Docker is available")
    
    # Start containers
    if not start_containers(DOCKER_COMPOSE_FILE, SERVICES):
        return 1
    
    # Wait for services
    if not args.no_wait:
        if not wait_for_services(HEALTH_CHECKS, args.timeout):
            print("[WARNING] Some services may not be ready")
    
    # Show status
    print("\n" + "-" * 60)
    print("Container Status:")
    print("-" * 60)
    show_status(DOCKER_COMPOSE_FILE)
    
    print("\n" + "=" * 60)
    print("[OK] Laboratory environment is ready!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Run tests: python3 tests/smoke_test.py")
    print("  2. Start exercises: python3 src/exercises/ex_10_01_https.py serve")
    print("  3. Read documentation: docs/theory_summary.md")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
