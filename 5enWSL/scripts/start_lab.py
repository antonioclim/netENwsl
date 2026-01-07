#!/usr/bin/env python3
"""
Week 5 Laboratory Launcher
NETWORKING class - ASE, Informatics | by Revolvix

This script starts all Docker containers and verifies the laboratory environment.
"""

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

SERVICES = {
    "python": {
        "container": "week5_python",
        "port": 0,  # No exposed port, interactive only
        "health_check": None,
        "startup_time": 3
    },
    "udp-server": {
        "container": "week5_udp-server",
        "port": 9999,
        "health_check": None,
        "startup_time": 5
    },
    "udp-client": {
        "container": "week5_udp-client",
        "port": 0,
        "health_check": None,
        "startup_time": 2
    }
}


def check_docker_available() -> bool:
    """Verify Docker is available and running."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except Exception as e:
        logger.error(f"Docker check failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Start Week 5 Laboratory Environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python start_lab.py           Start all services
  python start_lab.py --status  Check status only
  python start_lab.py --rebuild Force rebuild images
"""
    )
    parser.add_argument("--status", action="store_true", help="Check status only")
    parser.add_argument("--rebuild", action="store_true", help="Force rebuild images")
    parser.add_argument("--detach", "-d", action="store_true", default=True,
                        help="Run in detached mode (default)")
    parser.add_argument("--logs", action="store_true", help="Show logs after starting")
    args = parser.parse_args()

    docker_dir = PROJECT_ROOT / "docker"
    
    # Verify Docker is available
    if not check_docker_available():
        logger.error("Docker is not available. Please ensure Docker Desktop is running.")
        logger.info("On Windows, check that Docker Desktop is started and WSL2 integration is enabled.")
        return 1
    
    try:
        docker = DockerManager(docker_dir)
    except FileNotFoundError as e:
        logger.error(str(e))
        return 1

    if args.status:
        docker.show_status(SERVICES)
        return 0

    logger.info("=" * 60)
    logger.info("Starting Week 5 Laboratory Environment")
    logger.info("Topic: Network Layer - IP Addressing, Subnetting, VLSM")
    logger.info("=" * 60)

    try:
        # Build images if requested
        if args.rebuild:
            logger.info("Rebuilding Docker images...")
            if not docker.compose_build(no_cache=True):
                logger.error("Failed to build images")
                return 1
        
        # Start containers
        logger.info("Starting containers...")
        if not docker.compose_up(detach=args.detach, build=not args.rebuild):
            logger.error("Failed to start containers")
            return 1

        # Wait for services to initialise
        logger.info("Waiting for services to initialise...")
        time.sleep(5)

        # Verify services
        all_healthy = docker.verify_services(SERVICES)

        if all_healthy:
            logger.info("=" * 60)
            logger.info("Laboratory environment is ready!")
            logger.info("")
            logger.info("Access points:")
            logger.info("  Portainer:    https://localhost:9443")
            logger.info("  UDP Server:   localhost:9999/udp")
            logger.info("")
            logger.info("Quick commands:")
            logger.info("  docker exec -it week5_python bash")
            logger.info("  docker exec week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py --help")
            logger.info("=" * 60)
            
            if args.logs:
                logger.info("")
                logger.info("Recent logs:")
                print(docker.compose_logs(tail=20))
            
            return 0
        else:
            logger.error("Some services failed to start. Check logs above.")
            logger.info("Try: python scripts/cleanup.py --full && python scripts/start_lab.py --rebuild")
            return 1

    except Exception as e:
        logger.error(f"Failed to start laboratory: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
