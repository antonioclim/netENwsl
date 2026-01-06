#!/usr/bin/env python3
"""
Week 3 Laboratory Launcher
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

# Service definitions for Week 3
SERVICES = {
    "Echo Server": {
        "container": "week3_server",
        "port": 8080,
        "health_check": None,
        "startup_time": 3
    },
    "TCP Tunnel": {
        "container": "week3_router",
        "port": 9090,
        "health_check": None,
        "startup_time": 5
    },
    "Client": {
        "container": "week3_client",
        "port": None,
        "health_check": None,
        "startup_time": 2
    },
}


def print_banner():
    """Print startup banner."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     WEEK 3 — Network Programming Laboratory                 ║
║     UDP Broadcast/Multicast, TCP Tunnelling                  ║
║                                                              ║
║     NETWORKING class - ASE, Informatics                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Start Week 3 Laboratory Environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python start_lab.py              # Start all services
  python start_lab.py --status     # Check status only
  python start_lab.py --rebuild    # Force rebuild images
  python start_lab.py --broadcast  # Include broadcast receiver
        """
    )
    parser.add_argument(
        "--status", action="store_true",
        help="Check status only, don't start services"
    )
    parser.add_argument(
        "--rebuild", action="store_true",
        help="Force rebuild Docker images"
    )
    parser.add_argument(
        "--broadcast", action="store_true",
        help="Start broadcast receiver container"
    )
    parser.add_argument(
        "--portainer", action="store_true",
        help="Start Portainer management interface"
    )
    parser.add_argument(
        "-d", "--detach", action="store_true", default=True,
        help="Run in detached mode (default)"
    )
    args = parser.parse_args()

    print_banner()

    try:
        docker = DockerManager(PROJECT_ROOT / "docker")
    except FileNotFoundError as e:
        logger.error(str(e))
        return 1

    if args.status:
        logger.info("Checking laboratory status...")
        docker.show_status(SERVICES)
        return 0

    logger.info("=" * 60)
    logger.info("Starting Week 3 Laboratory Environment")
    logger.info("=" * 60)

    try:
        # Build images if requested
        if args.rebuild:
            logger.info("Rebuilding Docker images...")
            docker.compose_build()

        # Prepare compose command with profiles
        compose_args = ["up", "-d"]
        
        if args.broadcast:
            compose_args.extend(["--profile", "broadcast"])
        
        if args.portainer:
            compose_args.extend(["--profile", "management"])

        # Start containers
        logger.info("Starting containers...")
        subprocess.run(
            ["docker", "compose", "-f", str(PROJECT_ROOT / "docker" / "docker-compose.yml")] + compose_args,
            cwd=PROJECT_ROOT,
            check=True
        )

        # Wait for services to initialise
        max_startup_time = max(s.get('startup_time', 5) for s in SERVICES.values())
        logger.info(f"Waiting {max_startup_time} seconds for services to initialise...")
        time.sleep(max_startup_time)

        # Verify services
        all_healthy = docker.verify_services(SERVICES)

        if all_healthy:
            logger.info("=" * 60)
            logger.info("Laboratory environment is ready!")
            logger.info("")
            logger.info("Access points:")
            logger.info("  Portainer:    https://localhost:9443" if args.portainer else "  Portainer:    (not started)")
            logger.info("  Echo Server:  localhost:8080")
            logger.info("  TCP Tunnel:   localhost:9090")
            logger.info("")
            logger.info("Interactive client:")
            logger.info("  docker exec -it week3_client bash")
            logger.info("")
            logger.info("Quick test:")
            logger.info("  docker exec week3_client bash -c \"echo HELLO | nc server 8080\"")
            logger.info("=" * 60)
            return 0
        else:
            logger.warning("Some services may not be fully ready.")
            logger.info("Check logs with: docker compose -f docker/docker-compose.yml logs")
            return 0

    except subprocess.CalledProcessError as e:
        logger.error(f"Docker command failed: {e}")
        return 1
    except Exception as e:
        logger.error(f"Failed to start laboratory: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
