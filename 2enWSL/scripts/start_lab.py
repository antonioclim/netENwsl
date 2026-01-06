#!/usr/bin/env python3
"""
Week 2 Laboratory Launcher
NETWORKING class - ASE, Informatics | by Revolvix

This script starts all Docker containers and verifies the laboratory environment.
"""

import argparse
import sys
import time
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.network_utils import NetworkUtils
from scripts.utils.logger import setup_logger

logger = setup_logger("start_lab")

# Service definitions
SERVICES = {
    "lab": {
        "container": "week2_lab",
        "port": 9090,
        "health_check": None,
        "startup_time": 5
    },
    "portainer": {
        "container": "week2_portainer",
        "port": 9443,
        "health_check": "https://localhost:9443",
        "startup_time": 10
    }
}


def print_banner() -> None:
    """Print startup banner."""
    print()
    print("=" * 60)
    print("  Week 2: Socket Programming Laboratory")
    print("  TCP and UDP Server/Client Implementation")
    print("  NETWORKING class - ASE, Informatics")
    print("=" * 60)
    print()


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Start Week 2 Laboratory Environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/start_lab.py              # Start all services
  python scripts/start_lab.py --status     # Check status only
  python scripts/start_lab.py --rebuild    # Rebuild images first
        """
    )
    parser.add_argument(
        "--status", "-s",
        action="store_true",
        help="Check status only, don't start services"
    )
    parser.add_argument(
        "--rebuild", "-r",
        action="store_true",
        help="Force rebuild of Docker images"
    )
    parser.add_argument(
        "--detach", "-d",
        action="store_true",
        default=True,
        help="Run containers in detached mode (default: True)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    try:
        docker = DockerManager(PROJECT_ROOT / "docker")
    except FileNotFoundError as e:
        logger.error(f"Docker configuration not found: {e}")
        return 1
    
    if args.status:
        print_banner()
        logger.info("Checking service status...")
        docker.show_status(SERVICES)
        return 0
    
    print_banner()
    
    try:
        # Build images if requested
        if args.rebuild:
            logger.info("Rebuilding Docker images...")
            if not docker.compose_build(no_cache=True):
                logger.error("Failed to build images")
                return 1
            logger.info("Images rebuilt successfully")
        
        # Start services
        logger.info("Starting laboratory services...")
        if not docker.compose_up(detach=args.detach, build=not args.rebuild):
            logger.error("Failed to start services")
            return 1
        
        # Wait for services to initialise
        logger.info("Waiting for services to initialise...")
        time.sleep(5)
        
        # Verify services
        logger.info("Verifying services...")
        all_healthy = docker.verify_services(SERVICES)
        
        if all_healthy:
            print()
            print("=" * 60)
            print("  Laboratory environment is ready!")
            print("=" * 60)
            print()
            print("  Access points:")
            print("    Portainer:    https://localhost:9443")
            print("    TCP Server:   localhost:9090 (start manually)")
            print("    UDP Server:   localhost:9091 (start manually)")
            print()
            print("  Quick start:")
            print("    docker exec -it week2_lab bash")
            print("    python3 src/exercises/ex_2_01_tcp.py server --port 9090")
            print()
            print("  Or run from host:")
            print("    python src/exercises/ex_2_01_tcp.py server --port 9090")
            print()
            print("=" * 60)
            return 0
        else:
            logger.error("Some services failed to start. Check logs:")
            logger.error("  docker compose -f docker/docker-compose.yml logs")
            return 1
    
    except KeyboardInterrupt:
        logger.info("Startup cancelled by user")
        return 130
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
