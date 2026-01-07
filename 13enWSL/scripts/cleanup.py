#!/usr/bin/env python3
"""
Week 13 Laboratory Cleanup
NETWORKING class - ASE, Informatics | by Revolvix

This script removes all containers, networks, and optionally volumes
to prepare the system for the next laboratory session.
"""

import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger

logger = setup_logger("cleanup")

WEEK_PREFIX = "week13"


def clean_artifacts(dry_run: bool = False) -> None:
    """Remove generated artifacts."""
    artifacts_dir = PROJECT_ROOT / "artifacts"
    
    if not artifacts_dir.exists():
        return
    
    for f in artifacts_dir.glob("*"):
        if f.name == ".gitkeep":
            continue
        if dry_run:
            logger.info(f"[DRY RUN] Would remove: {f}")
        else:
            try:
                if f.is_file():
                    f.unlink()
                elif f.is_dir():
                    import shutil
                    shutil.rmtree(f)
            except Exception as e:
                logger.warning(f"Could not remove {f}: {e}")


def clean_pcap(dry_run: bool = False) -> None:
    """Remove packet capture files."""
    pcap_dir = PROJECT_ROOT / "pcap"
    
    if not pcap_dir.exists():
        return
    
    for f in pcap_dir.glob("*.pcap"):
        if dry_run:
            logger.info(f"[DRY RUN] Would remove: {f}")
        else:
            try:
                f.unlink()
            except Exception as e:
                logger.warning(f"Could not remove {f}: {e}")


def clean_pycache(dry_run: bool = False) -> None:
    """Remove Python cache directories."""
    for cache_dir in PROJECT_ROOT.rglob("__pycache__"):
        if dry_run:
            logger.info(f"[DRY RUN] Would remove: {cache_dir}")
        else:
            try:
                import shutil
                shutil.rmtree(cache_dir)
            except Exception as e:
                logger.warning(f"Could not remove {cache_dir}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Cleanup Week 13 Laboratory")
    parser.add_argument("--full", action="store_true",
                        help="Remove volumes and all data (use before next week)")
    parser.add_argument("--prune", action="store_true",
                        help="Also prune unused Docker resources")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be removed without removing")
    parser.add_argument("--artifacts-only", action="store_true",
                        help="Only clean artifacts directory")
    args = parser.parse_args()
    
    docker_dir = PROJECT_ROOT / "docker"
    docker = DockerManager(docker_dir)
    
    logger.info("=" * 60)
    logger.info("Cleaning up Week 13 Laboratory Environment")
    logger.info("=" * 60)
    
    if args.dry_run:
        logger.info("[DRY RUN] No changes will be made")
    
    try:
        if not args.artifacts_only:
            # Stop and remove containers
            logger.info("Stopping Docker containers...")
            docker.compose_down(volumes=args.full, dry_run=args.dry_run)
            
            # Remove week-specific resources
            logger.info(f"Removing {WEEK_PREFIX}_* Docker resources...")
            docker.remove_by_prefix(WEEK_PREFIX, dry_run=args.dry_run)
        
        # Clean artifacts
        if args.full or args.artifacts_only:
            logger.info("Cleaning artifacts directory...")
            clean_artifacts(dry_run=args.dry_run)
            
            logger.info("Cleaning pcap directory...")
            clean_pcap(dry_run=args.dry_run)
        
        # Clean Python cache
        logger.info("Cleaning Python cache...")
        clean_pycache(dry_run=args.dry_run)
        
        # Optional system prune
        if args.prune and not args.dry_run:
            logger.info("Pruning unused Docker resources...")
            docker.system_prune()
        
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
