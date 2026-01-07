#!/usr/bin/env python3
"""
Week 5 Laboratory Shutdown
NETWORKING class - ASE, Informatics | by Revolvix

This script gracefully stops all Docker containers.
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger

logger = setup_logger("stop_lab")


def main():
    parser = argparse.ArgumentParser(
        description="Stop Week 5 Laboratory Environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python stop_lab.py              Stop all containers
  python stop_lab.py --timeout 30 Allow 30 seconds for graceful shutdown
"""
    )
    parser.add_argument("--timeout", type=int, default=10,
                        help="Timeout for graceful shutdown (default: 10s)")
    args = parser.parse_args()

    docker_dir = PROJECT_ROOT / "docker"
    
    try:
        docker = DockerManager(docker_dir)
    except FileNotFoundError as e:
        logger.error(str(e))
        return 1

    logger.info("=" * 50)
    logger.info("Stopping Week 5 Laboratory Environment")
    logger.info("=" * 50)

    try:
        logger.info("Stopping containers (preserving data)...")
        if docker.compose_down(volumes=False):
            logger.info("All containers stopped successfully")
            logger.info("")
            logger.info("To restart: python scripts/start_lab.py")
            logger.info("To clean up: python scripts/cleanup.py --full")
            return 0
        else:
            logger.error("Failed to stop some containers")
            return 1

    except Exception as e:
        logger.error(f"Failed to stop laboratory: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
