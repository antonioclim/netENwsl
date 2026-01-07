#!/usr/bin/env python3
"""
Week 7 Laboratory Shutdown
NETWORKING class - ASE, Informatics | by Revolvix

This script gracefully stops all laboratory containers whilst preserving data.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger

logger = setup_logger("stop_lab")


def main() -> int:
    parser = argparse.ArgumentParser(description="Stop Week 7 Laboratory")
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Timeout in seconds for graceful shutdown (default: 10)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force kill containers without waiting"
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
        logger.error(f"Configuration error: {e}")
        return 1

    logger.info("=" * 60)
    logger.info("Stopping Week 7 Laboratory Environment")
    logger.info("=" * 60)

    try:
        # Show current status
        logger.info("Current status:")
        ps_output = docker.compose_ps()
        if ps_output.strip():
            print(ps_output)
        else:
            logger.info("  No containers running")
            return 0

        # Stop containers
        logger.info("Stopping containers...")
        docker.compose_down(volumes=False, remove_orphans=True)

        logger.info("")
        logger.info("=" * 60)
        logger.info("Laboratory stopped successfully")
        logger.info("")
        logger.info("Data in 'artifacts/' and 'pcap/' has been preserved.")
        logger.info("")
        logger.info("To restart: python scripts/start_lab.py")
        logger.info("For full cleanup: python scripts/cleanup.py --full")
        logger.info("=" * 60)
        
        return 0

    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"Failed to stop laboratory: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
