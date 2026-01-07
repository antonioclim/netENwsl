#!/usr/bin/env python3
"""
Week 10 Laboratory Shutdown
NETWORKING class - ASE, Informatics | by Revolvix

This script gracefully stops all Docker containers while preserving data.
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Stop Week 10 Laboratory")
    parser.add_argument("--timeout", type=int, default=30,
                        help="Timeout for stopping containers (default: 30s)")
    args = parser.parse_args()

    docker_dir = PROJECT_ROOT / "docker"
    
    try:
        docker = DockerManager(docker_dir)
    except FileNotFoundError as e:
        logger.error(str(e))
        return 1

    logger.info("=" * 60)
    logger.info("Stopping Week 10 Laboratory Environment")
    logger.info("=" * 60)

    try:
        # Stop containers (preserve volumes)
        if docker.compose_down(volumes=False):
            logger.info("✓ All containers stopped successfully")
            logger.info("")
            logger.info("Data volumes have been preserved.")
            logger.info("To remove volumes, use: python scripts/cleanup.py --full")
            logger.info("")
            logger.info("To restart: python scripts/start_lab.py")
            return 0
        else:
            logger.error("Failed to stop containers")
            return 1

    except Exception as e:
        logger.error(f"Shutdown failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
