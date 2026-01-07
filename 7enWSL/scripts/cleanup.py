#!/usr/bin/env python3
"""
Week 7 Laboratory Cleanup
NETWORKING class - ASE, Informatics | by Revolvix

This script removes all containers, networks, and optionally volumes
to prepare the system for the next laboratory session.
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

logger = setup_logger("cleanup")

WEEK_PREFIX = "week7"


def clean_directory(dir_path: Path, pattern: str = "*", keep_gitkeep: bool = True) -> int:
    """
    Clean files from a directory.
    
    Args:
        dir_path: Directory to clean
        pattern: Glob pattern for files to remove
        keep_gitkeep: Keep .gitkeep files
        
    Returns:
        Number of files removed
    """
    removed = 0
    if not dir_path.exists():
        return 0
    
    for f in dir_path.glob(pattern):
        if f.is_file():
            if keep_gitkeep and f.name == ".gitkeep":
                continue
            try:
                f.unlink()
                removed += 1
                logger.debug(f"Removed: {f}")
            except Exception as e:
                logger.warning(f"Could not remove {f}: {e}")
    
    return removed


def main() -> int:
    parser = argparse.ArgumentParser(description="Cleanup Week 7 Laboratory")
    parser.add_argument(
        "--full",
        action="store_true",
        help="Remove volumes and all data (use before next week)"
    )
    parser.add_argument(
        "--prune",
        action="store_true",
        help="Also prune unused Docker resources system-wide"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be removed without removing"
    )
    parser.add_argument(
        "--keep-artifacts",
        action="store_true",
        help="Keep artifacts directory contents"
    )
    parser.add_argument(
        "--keep-pcap",
        action="store_true",
        help="Keep packet capture files"
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
    logger.info("Cleaning up Week 7 Laboratory Environment")
    logger.info("=" * 60)

    if args.dry_run:
        logger.info("[DRY RUN] No changes will be made")

    try:
        # Stop and remove containers
        logger.info("Stopping and removing containers...")
        docker.compose_down(volumes=args.full, dry_run=args.dry_run)

        # Remove week-specific resources
        logger.info(f"Removing {WEEK_PREFIX}_* resources...")
        docker.remove_by_prefix(WEEK_PREFIX, dry_run=args.dry_run)

        # Clean artifacts directory
        if args.full and not args.keep_artifacts:
            artifacts_dir = PROJECT_ROOT / "artifacts"
            if args.dry_run:
                logger.info(f"[DRY RUN] Would clean: {artifacts_dir}")
            else:
                logger.info(f"Cleaning artifacts directory...")
                count = clean_directory(artifacts_dir, "*.log")
                count += clean_directory(artifacts_dir, "*.txt")
                count += clean_directory(artifacts_dir, "*.json")
                if count > 0:
                    logger.info(f"  Removed {count} artifact files")

        # Clean pcap directory
        if args.full and not args.keep_pcap:
            pcap_dir = PROJECT_ROOT / "pcap"
            if args.dry_run:
                logger.info(f"[DRY RUN] Would clean: {pcap_dir}")
            else:
                logger.info(f"Cleaning pcap directory...")
                count = clean_directory(pcap_dir, "*.pcap")
                count += clean_directory(pcap_dir, "*.pcapng")
                if count > 0:
                    logger.info(f"  Removed {count} capture files")

        # Optional system prune
        if args.prune:
            if args.dry_run:
                logger.info("[DRY RUN] Would prune unused Docker resources")
            else:
                logger.info("Pruning unused Docker resources...")
                docker.system_prune()

        logger.info("")
        logger.info("=" * 60)
        logger.info("Cleanup complete!")
        if args.full:
            logger.info("System is ready for the next laboratory session.")
        else:
            logger.info("Containers removed. Use --full to also remove data.")
        logger.info("=" * 60)
        
        return 0

    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
