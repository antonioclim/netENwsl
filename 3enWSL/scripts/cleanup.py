#!/usr/bin/env python3
"""
Week 3 Laboratory Cleanup
NETWORKING class - ASE, Informatics | by Revolvix

This script removes all containers, networks, and optionally volumes
to prepare the system for the next laboratory session.
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

logger = setup_logger("cleanup")

WEEK_PREFIX = "week3"


def clean_artifacts(dry_run: bool = False) -> None:
    """Remove generated artifacts and temporary files."""
    artifacts_dir = PROJECT_ROOT / "artifacts"
    pcap_dir = PROJECT_ROOT / "pcap"
    
    for directory, pattern in [(artifacts_dir, "*"), (pcap_dir, "*.pcap")]:
        if not directory.exists():
            continue
        
        for f in directory.glob(pattern):
            if f.name in [".gitkeep", "README.md"]:
                continue
            
            if dry_run:
                logger.info(f"[DRY RUN] Would remove: {f}")
            else:
                try:
                    f.unlink()
                    logger.info(f"Removed: {f.name}")
                except Exception as e:
                    logger.warning(f"Could not remove {f}: {e}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Cleanup Week 3 Laboratory Environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cleanup.py              # Stop containers, preserve data
  python cleanup.py --full       # Remove everything including volumes
  python cleanup.py --prune      # Also prune unused Docker resources
  python cleanup.py --dry-run    # Show what would be removed
        """
    )
    parser.add_argument(
        "--full", action="store_true",
        help="Remove volumes and all data (use before next week)"
    )
    parser.add_argument(
        "--prune", action="store_true",
        help="Also prune unused Docker resources"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would be removed without removing"
    )
    parser.add_argument(
        "--artifacts-only", action="store_true",
        help="Only clean artifacts directory, don't stop containers"
    )
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Cleaning up Week 3 Laboratory Environment")
    logger.info("=" * 60)

    if args.dry_run:
        logger.info("[DRY RUN] No changes will be made")

    try:
        if not args.artifacts_only:
            docker = DockerManager(PROJECT_ROOT / "docker")

            # Stop and remove containers
            logger.info("Stopping containers...")
            docker.compose_down(volumes=args.full, dry_run=args.dry_run)

            # Remove week-specific resources
            logger.info(f"Removing {WEEK_PREFIX}_* resources...")
            docker.remove_by_prefix(WEEK_PREFIX, dry_run=args.dry_run)

        # Clean artifacts
        if args.full or args.artifacts_only:
            logger.info("Cleaning artifacts and captures...")
            clean_artifacts(dry_run=args.dry_run)

        # Optional system prune
        if args.prune and not args.dry_run:
            logger.info("Pruning unused Docker resources...")
            subprocess.run(["docker", "system", "prune", "-f"])

        logger.info("=" * 60)
        logger.info("Cleanup complete!")
        if args.full:
            logger.info("System is ready for the next laboratory session.")
        logger.info("=" * 60)
        return 0

    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
