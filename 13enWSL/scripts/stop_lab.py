#!/usr/bin/env python3
"""
Week 13 Laboratory Shutdown
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


def main():
    parser = argparse.ArgumentParser(description="Stop Week 13 Laboratory")
    parser.add_argument("--timeout", type=int, default=30,
                        help="Timeout for graceful shutdown (default: 30s)")
    parser.add_argument("--force", action="store_true",
                        help="Force immediate shutdown")
    args = parser.parse_args()
    
    docker_dir = PROJECT_ROOT / "docker"
    docker = DockerManager(docker_dir)
    
    logger.info("=" * 60)
    logger.info("Stopping Week 13 Laboratory Environment")
    logger.info("=" * 60)
    
    try:
        logger.info("Stopping containers (preserving data)...")
        
        # Stop containers without removing volumes
        if docker.compose_down(volumes=False):
            logger.info("=" * 60)
            logger.info("Laboratory environment stopped successfully")
            logger.info("")
            logger.info("Data has been preserved. To fully clean up:")
            logger.info("  python scripts/cleanup.py --full")
            logger.info("=" * 60)
            return 0
        else:
            logger.error("Failed to stop containers")
            return 1
    
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user")
        return 130
    
    except Exception as e:
        logger.error(f"Failed to stop laboratory: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
