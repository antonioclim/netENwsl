#!/usr/bin/env python3
"""
Week 12 Laboratory Cleanup
NETWORKING class - ASE, Informatics | by Revolvix

This script removes all containers, networks, and optionally volumes
to prepare the system for the next laboratory session.
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_colour_logger

logger = setup_colour_logger("cleanup")

WEEK_PREFIX = "week12"


def clean_artifacts() -> None:
    """Clean generated artifacts directory."""
    artifacts_dir = PROJECT_ROOT / "artifacts"
    if artifacts_dir.exists():
        for f in artifacts_dir.glob("*"):
            if f.name != ".gitkeep":
                try:
                    f.unlink()
                    logger.info(f"Removed: {f}")
                except Exception as e:
                    logger.warning(f"Could not remove {f}: {e}")


def clean_pcap() -> None:
    """Clean packet capture directory."""
    pcap_dir = PROJECT_ROOT / "pcap"
    if pcap_dir.exists():
        for f in pcap_dir.glob("*.pcap"):
            try:
                f.unlink()
                logger.info(f"Removed: {f}")
            except Exception as e:
                logger.warning(f"Could not remove {f}: {e}")


def clean_spool() -> None:
    """Clean SMTP spool directory."""
    spool_dir = PROJECT_ROOT / "docker" / "volumes" / "spool"
    if spool_dir.exists():
        for f in spool_dir.glob("*.eml"):
            try:
                f.unlink()
                logger.info(f"Removed: {f}")
            except Exception as e:
                logger.warning(f"Could not remove {f}: {e}")


def clean_logs() -> None:
    """Clean logs directory."""
    logs_dir = PROJECT_ROOT / "logs"
    if logs_dir.exists():
        for f in logs_dir.glob("*.log"):
            try:
                f.unlink()
                logger.info(f"Removed: {f}")
            except Exception as e:
                logger.warning(f"Could not remove {f}: {e}")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Cleanup Week 12 Laboratory Environment"
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
        "--keep-volumes", action="store_true",
        help="Keep Docker volumes even with --full"
    )
    
    args = parser.parse_args()
    
    docker_dir = PROJECT_ROOT / "docker"
    
    logger.info("=" * 60)
    logger.info("Cleaning up Week 12 Laboratory Environment")
    logger.info("=" * 60)
    
    if args.dry_run:
        logger.info("[DRY RUN] No changes will be made")
    
    try:
        docker = DockerManager(docker_dir)
        
        # Stop containers
        logger.info("Stopping containers...")
        docker.compose_down(
            volumes=args.full and not args.keep_volumes,
            dry_run=args.dry_run
        )
        
        # Remove week-specific resources
        logger.info(f"Removing {WEEK_PREFIX}_* resources...")
        docker.remove_by_prefix(WEEK_PREFIX, dry_run=args.dry_run)
        
        # Clean local files if full cleanup
        if args.full and not args.dry_run:
            logger.info("Cleaning local directories...")
            clean_artifacts()
            clean_pcap()
            clean_spool()
            clean_logs()
        elif args.full and args.dry_run:
            logger.info("[DRY RUN] Would clean: artifacts/, pcap/, spool/, logs/")
        
        # Optional system prune
        if args.prune and not args.dry_run:
            logger.info("Pruning unused Docker resources...")
            docker.system_prune()
        elif args.prune and args.dry_run:
            logger.info("[DRY RUN] Would run: docker system prune -f")
        
        logger.info("=" * 60)
        logger.info("Cleanup complete!")
        if args.full:
            logger.info("System is ready for the next laboratory session.")
        else:
            logger.info("For complete cleanup, use: python scripts/cleanup.py --full")
        logger.info("=" * 60)
        return 0
    
    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {e}")
        return 1
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
