#!/usr/bin/env python3
"""
Week 1 Laboratory Launcher
NETWORKING class - ASE, Informatics | by Revolvix

This script starts all Docker containers and verifies the laboratory environment
is ready for networking exercises.
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
SERVICES = {
    "lab": {
        "container": "week1_lab",
        "port": 9090,
        "health_check": None,
        "startup_time": 5
    },
}

PORTAINER_SERVICE = {
    "portainer": {
        "container": "week1_portainer",
        "port": 9443,
        "health_check": "https://localhost:9443",
        "startup_time": 10
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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Start Week 1 Laboratory Environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/start_lab.py              # Start lab containers
  python scripts/start_lab.py --status     # Check status only
  python scripts/start_lab.py --rebuild    # Force rebuild images
  python scripts/start_lab.py --portainer  # Also start Portainer
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
        "--portainer",
        action="store_true",
        help="Also start Portainer management interface"
    )
    parser.add_argument(
        "--shell",
        action="store_true",
        help="Open interactive shell in lab container after starting"
    )
    args = parser.parse_args()

    # Verify Docker is running
    if not check_docker_running():
        logger.error("Docker is not running. Please start Docker Desktop.")
        return 1

    docker_dir = PROJECT_ROOT / "docker"
    
    try:
        docker = DockerManager(docker_dir)
    except FileNotFoundError as e:
        logger.error(str(e))
        return 1

    # Status check only
    if args.status:
        services = SERVICES.copy()
        if args.portainer:
            services.update(PORTAINER_SERVICE)
        docker.show_status(services)
        return 0

    logger.info("=" * 60)
    logger.info("Starting Week 1 Laboratory Environment")
    logger.info("NETWORKING class - ASE, Informatics | by Revolvix")
    logger.info("=" * 60)

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

        # Determine which services to start
        services_to_start = ["lab"]
        if args.portainer:
            services_to_start = None  # Start all including Portainer

        # Start containers
        logger.info("Starting containers...")
        if args.portainer:
            # Use --profile management to include Portainer
            result = subprocess.run(
                ["docker", "compose", "-f", str(docker.compose_file),
                 "--profile", "management", "up", "-d"],
                cwd=docker_dir.parent,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                logger.error(f"Failed to start containers: {result.stderr}")
                return 1
        else:
            if not docker.compose_up(detach=args.detach, services=services_to_start):
                logger.error("Failed to start containers")
                return 1

        # Wait for services to initialise
        logger.info("Waiting for services to initialise...")
        time.sleep(3)

        # Verify services
        services = SERVICES.copy()
        if args.portainer:
            services.update(PORTAINER_SERVICE)
        
        logger.info("Checking service status...")
        all_healthy = docker.verify_services(services)

        if all_healthy:
            logger.info("")
            logger.info("=" * 60)
            logger.info("\033[92mLaboratory environment is ready!\033[0m")
            logger.info("")
            logger.info("Access points:")
            logger.info(f"  Lab Container: docker exec -it week1_lab bash")
            logger.info(f"  TCP Test Port: localhost:9090")
            logger.info(f"  UDP Test Port: localhost:9091")
            if args.portainer:
                logger.info(f"  Portainer:     https://localhost:9443")
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
            logger.info("  docker compose -f docker/docker-compose.yml logs")
            return 1

    except Exception as e:
        logger.error(f"Failed to start laboratory: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
