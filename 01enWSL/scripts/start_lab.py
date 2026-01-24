#!/usr/bin/env python3
"""
Week 1 Laboratory Launcher
==========================
Computer Networks - ASE, CSIE | by ing. dr. Antonio Clim

Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment

This script starts all Docker containers and verifies the laboratory environment
is ready for networking exercises.

IMPORTANT: Portainer runs as a GLOBAL service on port 9000.
This script will NEVER start or stop Portainer.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations
from typing import Optional, List, Dict, Tuple, Any

import subprocess
import sys
import time
import argparse
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger

logger = setup_logger("start_lab")


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
# Service definitions for Week 1
# NOTE: Portainer is NOT included - it runs globally on port 9000
SERVICES = {
    "lab": {
        "container": "week1_lab",
        "port": 9090,
        "health_check": None,
        "startup_time": 5
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# ENVIRONMENT_CHECKS
# ═══════════════════════════════════════════════════════════════════════════════
def check_running_in_wsl() -> bool:
    """Check if we're running inside WSL."""
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


def check_docker_running() -> bool:
    """Verify Docker daemon is available."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def try_start_docker_service() -> bool:
    """Attempt to start Docker service in WSL."""
    logger.info("Docker not running. Attempting to start Docker service...")
    try:
        result = subprocess.run(
            ["sudo", "service", "docker", "start"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            logger.info("Docker service started successfully")
            time.sleep(2)  # Give Docker time to initialise
            return check_docker_running()
        else:
            logger.error(f"Failed to start Docker: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        logger.error("Timeout starting Docker service")
        return False
    except FileNotFoundError:
        logger.error("sudo not found - cannot start Docker service")
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# PORTAINER_STATUS
# ═══════════════════════════════════════════════════════════════════════════════
def check_portainer_status() -> tuple[bool, str]:
    """Check Portainer container status."""
    try:
        result = subprocess.run(
            ["docker", "ps", "-a", "--filter", "name=portainer", 
             "--format", "{{.Names}}\t{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return False, "Could not check Portainer status"
        
        output = result.stdout.strip()
        if not output:
            return False, "Portainer container not found"
        
        for line in output.split("\n"):
            if "portainer" in line.lower():
                parts = line.split("\t")
                if len(parts) >= 2:
                    status = parts[1].lower()
                    if "up" in status:
                        return True, "Portainer is running"
                    else:
                        return False, f"Portainer is stopped: {parts[1]}"
        
        return False, "Portainer status unknown"
        
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
        return False, f"Error checking Portainer: {e}"


def display_portainer_warning() -> None:
    """Display warning and instructions when Portainer is not running."""
    logger.warning("")
    logger.warning("=" * 60)
    logger.warning("\033[93mWARNING: Portainer is not running!\033[0m")
    logger.warning("Portainer provides the web-based Docker management interface.")
    logger.warning("")
    logger.warning("To start Portainer:")
    logger.warning("  docker start portainer")
    logger.warning("")
    logger.warning("If Portainer container doesn't exist, create it:")
    logger.warning("  docker run -d -p 9000:9000 --name portainer --restart=always \\")
    logger.warning("    -v /var/run/docker.sock:/var/run/docker.sock \\")
    logger.warning("    -v portainer_data:/data portainer/portainer-ce:latest")
    logger.warning("=" * 60)
    logger.warning("")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Start Week 1 Laboratory Environment (WSL2)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/start_lab.py              # Start lab containers
  python3 scripts/start_lab.py --status     # Check status only
  python3 scripts/start_lab.py --rebuild    # Force rebuild images
  python3 scripts/start_lab.py --shell      # Open shell after starting

Notes:
  - Portainer runs globally on port 9000 and is NOT managed by this script
  - Access Portainer at: http://localhost:9000
  - Credentials: stud / studstudstud
        """
    )
    parser.add_argument("--status", action="store_true", help="Check status only")
    parser.add_argument("--rebuild", action="store_true", help="Force rebuild images")
    parser.add_argument("--detach", "-d", action="store_true", default=True)
    parser.add_argument("--shell", action="store_true", help="Open shell after starting")
    parser.add_argument("--no-portainer-check", action="store_true")
    args = parser.parse_args()

    if not check_running_in_wsl():
        logger.warning("Not running in WSL - some features may not work correctly")

    if not check_docker_running():
        if not try_start_docker_service():
            logger.error("Docker is not running. Please start: sudo service docker start")
            return 1

    docker_dir = PROJECT_ROOT / "docker"
    
    try:
        docker = DockerManager(docker_dir)
    except FileNotFoundError as e:
        logger.error(str(e))
        return 1

    if not args.no_portainer_check:
        portainer_running, _ = check_portainer_status()
        if not portainer_running:
            display_portainer_warning()

    if args.status:
        logger.info("=" * 60)
        logger.info("Service Status Check")
        logger.info("=" * 60)
        docker.show_status(SERVICES)
        portainer_running, portainer_status = check_portainer_status()
        status_colour = "\033[92m" if portainer_running else "\033[91m"
        logger.info(f"  portainer (global): {status_colour}{portainer_status}\033[0m (port 9000)")
        return 0

    logger.info("=" * 60)
    logger.info("Starting Week 1 Laboratory Environment")
    logger.info("NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim")
    logger.info("WSL2 + Ubuntu 22.04 + Docker + Portainer")
    logger.info("=" * 60)

    try:
        (PROJECT_ROOT / "artifacts").mkdir(exist_ok=True)
        (PROJECT_ROOT / "pcap").mkdir(exist_ok=True)

        if args.rebuild:
            logger.info("Building container images...")
            if not docker.compose_build(no_cache=True):
                logger.error("Failed to build images")
                return 1

        logger.info("Starting lab containers...")
        if not docker.compose_up(detach=args.detach, services=["lab"]):
            logger.error("Failed to start containers")
            return 1

        logger.info("Waiting for services to initialise...")
        time.sleep(3)

        all_healthy = docker.verify_services(SERVICES)
        portainer_running, _ = check_portainer_status()

        if all_healthy:
            logger.info("")
            logger.info("=" * 60)
            logger.info("\033[92mLaboratory environment is ready!\033[0m")
            logger.info("")
            logger.info("Access points:")
            logger.info("  Lab Container:    docker exec -it week1_lab bash")
            logger.info("  TCP Test Port:    localhost:9090")
            logger.info("  UDP Test Port:    localhost:9091")
            logger.info("")
            if portainer_running:
                logger.info("  \033[92mPortainer:       http://localhost:9000\033[0m")
                logger.info("  Credentials:      stud / studstudstud")
            else:
                logger.warning("  \033[93mPortainer:       NOT RUNNING\033[0m")
            logger.info("=" * 60)
            
            if args.shell:
                subprocess.run(["docker", "exec", "-it", "week1_lab", "bash"])
            return 0
        else:
            logger.error("Some services failed to start.")
            return 1

    except Exception as e:
        logger.error(f"Failed to start laboratory: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
