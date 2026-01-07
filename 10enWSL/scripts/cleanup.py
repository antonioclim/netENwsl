#!/usr/bin/env python3
"""
Week 10 Laboratory Cleanup
NETWORKING class - ASE, Informatics | by Revolvix

This script removes all containers, networks, and optionally volumes
to prepare the system for the next laboratory session.
"""

import subprocess
import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger

logger = setup_logger("cleanup")

WEEK_PREFIX = "week10"


def clean_artifacts(dry_run: bool = False) -> None:
    """Clean generated artifacts and captures."""
    artifacts_dir = PROJECT_ROOT / "artifacts"
    pcap_dir = PROJECT_ROOT / "pcap"
    
    for directory in [artifacts_dir, pcap_dir]:
        if directory.exists():
            for f in directory.glob("*"):
                if f.name != ".gitkeep" and f.name != "README.md":
                    if dry_run:
                        logger.info(f"[DRY RUN] Would delete: {f}")
                    else:
                        if f.is_file():
                            f.unlink()
                            logger.info(f"Deleted: {f.name}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Cleanup Week 10 Laboratory")
    parser.add_argument("--full", action="store_true",
                        help="Remove volumes and all data (use before next week)")
    parser.add_argument("--prune", action="store_true",
                        help="Also prune unused Docker resources")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be removed without removing")
    args = parser.parse_args()

    docker_dir = PROJECT_ROOT / "docker"
    
    try:
        docker = DockerManager(docker_dir)
    except FileNotFoundError as e:
        logger.error(str(e))
        return 1

    logger.info("=" * 60)
    logger.info("Cleaning up Week 10 Laboratory Environment")
    logger.info("=" * 60)

    if args.dry_run:
        logger.info("[DRY RUN] No changes will be made")

    try:
        # Stop containers
        logger.info("Stopping containers...")
        docker.compose_down(volumes=args.full, dry_run=args.dry_run)

        # Remove week-specific resources
        logger.info(f"Removing {WEEK_PREFIX}_* resources...")
        docker.remove_by_prefix(WEEK_PREFIX, dry_run=args.dry_run)

        # Clean artifacts
        if args.full and not args.dry_run:
            logger.info("Cleaning artifacts directory...")
            clean_artifacts(dry_run=args.dry_run)

        # Optional system prune
        if args.prune and not args.dry_run:
            logger.info("Pruning unused Docker resources...")
            docker.system_prune()

        logger.info("=" * 60)
        logger.info("Cleanup complete!")
        if args.full:
            logger.info("System is ready for the next laboratory session.")
        else:
            logger.info("Containers stopped. Use --full to remove all data.")
        logger.info("=" * 60)
        return 0

    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
