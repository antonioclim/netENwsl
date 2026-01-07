#!/usr/bin/env python3
"""
Week 5 Laboratory Cleanup
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

WEEK_PREFIX = "week5"


def clean_artifacts(dry_run: bool = False) -> None:
    """Clean generated artifacts."""
    artifacts_dir = PROJECT_ROOT / "artifacts"
    
    if not artifacts_dir.exists():
        return
    
    for f in artifacts_dir.glob("*"):
        if f.name != ".gitkeep":
            if dry_run:
                logger.info(f"[DRY RUN] Would remove: {f}")
            else:
                f.unlink()
                logger.info(f"Removed: {f.name}")


def clean_pcap(dry_run: bool = False) -> None:
    """Clean packet capture files."""
    pcap_dir = PROJECT_ROOT / "pcap"
    
    if not pcap_dir.exists():
        return
    
    for f in pcap_dir.glob("*.pcap"):
        if dry_run:
            logger.info(f"[DRY RUN] Would remove: {f}")
        else:
            f.unlink()
            logger.info(f"Removed: {f.name}")


def main():
    parser = argparse.ArgumentParser(
        description="Cleanup Week 5 Laboratory Environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cleanup.py              Stop and remove containers
  python cleanup.py --full       Remove volumes and all data
  python cleanup.py --prune      Also prune unused Docker resources
  python cleanup.py --dry-run    Show what would be removed
"""
    )
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
    logger.info("Cleaning up Week 5 Laboratory Environment")
    logger.info("=" * 60)

    if args.dry_run:
        logger.info("[DRY RUN] No changes will be made")
        logger.info("")

    try:
        # Stop and remove containers
        logger.info("Stopping containers...")
        docker.compose_down(volumes=args.full, dry_run=args.dry_run)

        # Remove week-specific resources
        logger.info(f"Removing {WEEK_PREFIX}_* resources...")
        docker.remove_by_prefix(WEEK_PREFIX, dry_run=args.dry_run)

        # Clean local artifacts
        if args.full:
            logger.info("Cleaning artifacts directory...")
            clean_artifacts(dry_run=args.dry_run)

            logger.info("Cleaning pcap directory...")
            clean_pcap(dry_run=args.dry_run)

        # Optional system prune
        if args.prune and not args.dry_run:
            logger.info("Pruning unused Docker resources...")
            docker.system_prune()

        logger.info("")
        logger.info("=" * 60)
        logger.info("Cleanup complete!")
        if args.full:
            logger.info("System is ready for the next laboratory session.")
        else:
            logger.info("Containers removed. Use --full to also clean data and artifacts.")
        logger.info("=" * 60)
        return 0

    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
