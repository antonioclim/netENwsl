#!/usr/bin/env python3
"""
Week 12 Laboratory Shutdown
NETWORKING class - ASE, Informatics | by Revolvix

This script gracefully stops all Docker containers for the Week 12 laboratory.
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_colour_logger

logger = setup_colour_logger("stop_lab")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Stop Week 12 Laboratory Environment"
    )
    parser.add_argument(
        "--volumes", "-v", action="store_true",
        help="Also remove volumes (loses stored data)"
    )
    parser.add_argument(
        "--timeout", type=int, default=10,
        help="Timeout for graceful shutdown (default: 10 seconds)"
    )
    
    args = parser.parse_args()
    
    docker_dir = PROJECT_ROOT / "docker"
    
    logger.info("=" * 60)
    logger.info("Stopping Week 12 Laboratory Environment")
    logger.info("=" * 60)
    
    try:
        docker = DockerManager(docker_dir)
        
        # Stop containers
        logger.info("Stopping containers...")
        if docker.compose_down(volumes=args.volumes):
            logger.info("Containers stopped successfully")
        else:
            logger.warning("Some containers may not have stopped cleanly")
        
        # Show final status
        logger.info("")
        docker.show_status({
            "lab": {"port": 1025, "container": "week12_lab"},
            "portainer": {"port": 9443, "container": "week12_portainer"},
        })
        
        if args.volumes:
            logger.info("Volumes have been removed")
        else:
            logger.info("Volumes preserved. Use --volumes to remove them.")
        
        logger.info("=" * 60)
        logger.info("Laboratory environment stopped")
        logger.info("=" * 60)
        return 0
    
    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {e}")
        return 1
    except Exception as e:
        logger.error(f"Failed to stop laboratory: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
