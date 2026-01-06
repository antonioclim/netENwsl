#!/usr/bin/env python3
"""
Week 3 Laboratory Shutdown
NETWORKING class - ASE, Informatics | by Revolvix

This script gracefully stops all Docker containers while preserving data.
"""

import subprocess
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
    parser = argparse.ArgumentParser(
        description="Stop Week 3 Laboratory Environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python stop_lab.py           # Stop all containers
  python stop_lab.py --status  # Show status after stopping
        """
    )
    parser.add_argument(
        "--status", action="store_true",
        help="Show status after stopping"
    )
    parser.add_argument(
        "--logs", action="store_true",
        help="Show recent logs before stopping"
    )
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Stopping Week 3 Laboratory Environment")
    logger.info("=" * 60)

    try:
        docker = DockerManager(PROJECT_ROOT / "docker")

        # Show logs if requested
        if args.logs:
            logger.info("Recent container logs:")
            docker.compose_logs(tail=20)
            print()

        # Stop containers
        logger.info("Stopping containers (preserving volumes)...")
        docker.compose_down(volumes=False)

        logger.info("=" * 60)
        logger.info("Laboratory environment stopped.")
        logger.info("Data in volumes has been preserved.")
        logger.info("")
        logger.info("To restart: python scripts/start_lab.py")
        logger.info("To cleanup:  python scripts/cleanup.py --full")
        logger.info("=" * 60)

        # Show status if requested
        if args.status:
            subprocess.run(["docker", "ps", "-a", "--filter", "name=week3"])

        return 0

    except Exception as e:
        logger.error(f"Failed to stop laboratory: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
