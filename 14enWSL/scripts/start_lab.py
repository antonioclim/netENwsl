#!/usr/bin/env python3
"""Week 14 Laboratory Launcher.

NETWORKING class — ASE, CSIE | Computer Networks Laboratory
by ing. dr. Antonio Clim

Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment

This script starts all Docker containers and verifies the laboratory environment.

IMPORTANT: Portainer runs as a GLOBAL service on port 9000.
This script will NEVER start or stop Portainer.

NOTE: TCP Echo server runs on port 9090 (port 9000 is reserved for Portainer).

Usage:
    python scripts/start_lab.py
    python scripts/start_lab.py --quick
    python scripts/start_lab.py --verify-only
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from scripts.utils.docker_utils import DockerManager
    from scripts.utils.logger import setup_logger
    logger = setup_logger("start_lab")
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("start_lab")


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
SERVICES: Dict[str, Dict[str, Any]] = {
    "app1": {
        "container": "week14_app1",
        "ports": [8001],
        "health_check": "http://localhost:8001/health",
        "startup_time": 5,
    },
    "app2": {
        "container": "week14_app2",
        "ports": [8002],
        "health_check": "http://localhost:8002/health",
        "startup_time": 5,
    },
    "lb": {
        "container": "week14_lb",
        "ports": [8080],
        "health_check": "http://localhost:8080/lb-status",
        "startup_time": 10,
    },
    "echo": {
        "container": "week14_echo",
        "ports": [9090],
        "health_check": None,
        "startup_time": 5,
    },
    "client": {
        "container": "week14_client",
        "ports": [],
        "health_check": None,
        "startup_time": 5,
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# ENVIRONMENT_DETECTION
# ═══════════════════════════════════════════════════════════════════════════════
def check_running_in_wsl() -> bool:
    """Check if we are running inside WSL."""
    if os.path.exists("/proc/sys/fs/binfmt_misc/WSLInterop"):
        return True
    if "WSL_DISTRO_NAME" in os.environ:
        return True
    try:
        with open("/proc/version", "r") as f:
            version = f.read().lower()
            return "microsoft" in version or "wsl" in version
    except (FileNotFoundError, IOError):
        pass
    return False


# ═══════════════════════════════════════════════════════════════════════════════
# DOCKER_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def check_docker_running() -> bool:
    """Verify Docker daemon is available."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def check_portainer_status() -> Tuple[bool, str]:
    """Check Portainer container status."""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=portainer", "--format", "{{.Names}}\t{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return False, "Could not check status"

        output = result.stdout.strip()
        if not output:
            return False, "Not found"

        for line in output.split("\n"):
            if "portainer" in line.lower():
                parts = line.split("\t")
                if len(parts) >= 2:
                    return True, parts[1]
                return True, "Running"
        return False, "Not found"
    except subprocess.TimeoutExpired:
        return False, "Timeout"


# ═══════════════════════════════════════════════════════════════════════════════
# COMPOSE_OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════
def start_compose(compose_file: Path, detached: bool = True) -> bool:
    """Start services defined in docker-compose.yml."""
    cmd = ["docker", "compose", "-f", str(compose_file), "up"]
    if detached:
        cmd.append("-d")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            logger.error(f"Compose failed: {result.stderr}")
            return False
        return True
    except subprocess.TimeoutExpired:
        logger.error("Compose startup timed out")
        return False


def verify_services_healthy(timeout: int = 60) -> Dict[str, bool]:
    """Verify all services are running and healthy."""
    results: Dict[str, bool] = {}
    start_time = time.time()

    for name, config in SERVICES.items():
        container = config["container"]
        try:
            result = subprocess.run(
                ["docker", "ps", "-q", "-f", f"name={container}"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            is_running = bool(result.stdout.strip())
        except subprocess.TimeoutExpired:
            is_running = False

        results[name] = is_running

        if time.time() - start_time > timeout:
            logger.warning("Verification timeout reached")
            break

    return results


# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY_STATUS
# ═══════════════════════════════════════════════════════════════════════════════
def display_startup_banner() -> None:
    """Display startup information banner."""
    print("\n" + "=" * 60)
    print("  Week 14 Laboratory Environment")
    print("  NETWORKING class — ASE, CSIE")
    print("=" * 60)

    is_wsl = check_running_in_wsl()
    print(f"\n  Environment: {'WSL2' if is_wsl else 'Native Linux'}")

    portainer_ok, portainer_status = check_portainer_status()
    status_icon = "✓" if portainer_ok else "✗"
    print(f"  Portainer: {status_icon} {portainer_status}")
    print()


def display_service_status(results: Dict[str, bool]) -> None:
    """Display service status table."""
    print("\n  Service Status:")
    print("  " + "-" * 40)

    for name, is_healthy in results.items():
        icon = "✓" if is_healthy else "✗"
        config = SERVICES.get(name, {})
        ports = config.get("ports", [])
        port_str = f":{ports[0]}" if ports else ""
        print(f"  {icon} {name:12} {port_str}")

    print("  " + "-" * 40)

    healthy_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    print(f"\n  Total: {healthy_count}/{total_count} services running")


# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGUMENTS
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Start Week 14 laboratory environment",
        epilog="NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Skip health checks after startup",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Only verify existing services, do not start",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Timeout for service verification (default: 60s)",
    )
    return parser.parse_args()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point for laboratory launcher."""
    args = parse_args()

    display_startup_banner()

    if not check_docker_running():
        logger.error("Docker is not running!")
        print("\n  ✗ Docker daemon not available")
        print("  Run: sudo service docker start")
        return 1

    compose_file = PROJECT_ROOT / "docker" / "docker-compose.yml"

    if not args.verify_only:
        logger.info("Starting lab environment...")
        print("  Starting containers...")

        if not start_compose(compose_file):
            logger.error("Failed to start compose services")
            return 1

        # From my experience, containers need about 5-10 seconds to initialise
        wait_time = 5 if args.quick else 10
        print(f"  Waiting {wait_time}s for services to initialise...")
        time.sleep(wait_time)

    if not args.quick:
        print("  Verifying services...")
        results = verify_services_healthy(timeout=args.timeout)
        display_service_status(results)

        if not all(results.values()):
            logger.warning("Some services failed to start")
            return 1

    print("\n  ✓ Lab environment ready!")
    print("\n  Access points:")
    print("    - Load Balancer: http://localhost:8080")
    print("    - Backend 1:     http://localhost:8001")
    print("    - Backend 2:     http://localhost:8002")
    print("    - TCP Echo:      localhost:9090")
    print("    - Portainer:     http://localhost:9000")
    print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
