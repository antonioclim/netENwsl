#!/usr/bin/env python3
"""
Week 1 Laboratory Launcher
NETWORKING class - ASE, Informatics | by Revolvix

This script starts all Docker containers and verifies the laboratory environment
is ready for networking exercises.

ADAPTED FOR: WSL2 + Ubuntu 22.04 + Docker (in WSL) + Portainer Global
NOTE: Portainer is NOT started by this script - it runs globally on port 9000
"""

from __future__ import annotations

import subprocess
import sys
import time
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger

logger = setup_logger("start_lab")

# Service definitions for Week 1
# NOTE: Portainer is NOT included - it runs as a global service
SERVICES = {
    "lab": {
        "container": "week1_lab",
        "port": 9090,
        "health_check": None,
        "startup_time": 5
    },
}

# Global Portainer service (for status checks only, NOT started by this script)
PORTAINER_GLOBAL = {
    "portainer": {
        "container": "portainer",
        "port": 9000,
        "health_check": "http://localhost:9000",
        "startup_time": 0  # Already running
    }
}


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


def start_docker_service() -> bool:
    """Attempt to start Docker service (WSL environment)."""
    try:
        result = subprocess.run(
            ["sudo", "service", "docker", "start"],
            capture_output=True,
            timeout=30
        )
        time.sleep(2)  # Wait for service to start
        return check_docker_running()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def check_portainer_running() -> bool:
    """Check if global Portainer is running."""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=portainer", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return "portainer" in result.stdout.lower()
    except:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Start Week 1 Laboratory Environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/start_lab.py              # Start lab containers
  python scripts/start_lab.py --status     # Check status only
  python scripts/start_lab.py --rebuild    # Force rebuild images
  python scripts/start_lab.py --shell      # Open shell after starting

NOTE: Portainer runs globally on port 9000 and is NOT managed by this script.
      Access Portainer at: http://localhost:9000 (stud/studstudstud)
        """
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Check status of services without starting"
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Force rebuild container images"
    )
    parser.add_argument(
        "--detach", "-d",
        action="store_true",
        default=True,
        help="Run in detached mode (default: True)"
    )
    parser.add_argument(
        "--shell",
        action="store_true",
        help="Open interactive shell in lab container after starting"
    )
    args = parser.parse_args()

    # Verify Docker is running
    if not check_docker_running():
        logger.warning("Docker is not running. Attempting to start...")
        if start_docker_service():
            logger.info("Docker service started successfully.")
        else:
            logger.error("Failed to start Docker. Please run: sudo service docker start")
            return 1

    docker_dir = PROJECT_ROOT / "docker"
    
    try:
        docker = DockerManager(docker_dir)
    except FileNotFoundError as e:
        logger.error(str(e))
        return 1

    # Status check only
    if args.status:
        logger.info("Checking service status...")
        docker.show_status(SERVICES)
        
        # Also show Portainer status
        logger.info("")
        logger.info("Global Portainer status:")
        if check_portainer_running():
            logger.info("  [\033[92mRUNNING\033[0m] Portainer on http://localhost:9000")
        else:
            logger.warning("  [\033[91mSTOPPED\033[0m] Portainer - start with: docker start portainer")
        return 0

    logger.info("=" * 60)
    logger.info("Starting Week 1 Laboratory Environment")
    logger.info("NETWORKING class - ASE, Informatics | by Revolvix")
    logger.info("=" * 60)
    logger.info("")
    logger.info("Environment: WSL2 + Ubuntu 22.04 + Docker + Portainer Global")
    logger.info("")

    # Check global Portainer
    if not check_portainer_running():
        logger.warning("Global Portainer is not running!")
        logger.warning("Start it with: docker start portainer")
        logger.warning("Or deploy fresh with:")
        logger.warning("  docker run -d -p 9000:9000 --name portainer --restart=always \\")
        logger.warning("    -v /var/run/docker.sock:/var/run/docker.sock \\")
        logger.warning("    -v portainer_data:/data portainer/portainer-ce:latest")
        logger.info("")

    try:
        # Create necessary directories
        (PROJECT_ROOT / "artifacts").mkdir(exist_ok=True)
        (PROJECT_ROOT / "pcap").mkdir(exist_ok=True)

        # Build images if requested
        if args.rebuild:
            logger.info("Building container images...")
            if not docker.compose_build(no_cache=True):
                logger.error("Failed to build images")
                return 1

        # Start lab containers (NOT Portainer)
        logger.info("Starting lab containers...")
        if not docker.compose_up(detach=args.detach, services=["lab"]):
            logger.error("Failed to start containers")
            return 1

        # Wait for services to initialise
        logger.info("Waiting for services to initialise...")
        time.sleep(3)

        # Verify services
        logger.info("Checking service status...")
        all_healthy = docker.verify_services(SERVICES)

        if all_healthy:
            logger.info("")
            logger.info("=" * 60)
            logger.info("\033[92mLaboratory environment is ready!\033[0m")
            logger.info("")
            logger.info("Access points:")
            logger.info(f"  Lab Container: docker exec -it week1_lab bash")
            logger.info(f"  TCP Test Port: localhost:9090")
            logger.info(f"  UDP Test Port: localhost:9091")
            logger.info(f"  Portainer:     http://localhost:9000 (stud/studstudstud)")
            logger.info("")
            logger.info("Quick start:")
            logger.info("  docker exec -it week1_lab bash")
            logger.info("=" * 60)
            
            # Open shell if requested
            if args.shell:
                logger.info("\nOpening interactive shell...")
                subprocess.run(["docker", "exec", "-it", "week1_lab", "bash"])
            
            return 0
        else:
            logger.error("Some services failed to start. Check logs above.")
            logger.info("\nTroubleshooting:")
            logger.info("  docker-compose -f docker/docker-compose.yml logs")
            return 1

    except Exception as e:
        logger.error(f"Failed to start laboratory: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
