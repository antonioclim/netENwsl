#!/usr/bin/env python3
"""
Week 4 Laboratory Cleanup
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

WEEK_PREFIX = "week4"


def clean_directory(directory: Path, pattern: str = "*", 
                    exclude: list = None, dry_run: bool = False) -> int:
    """
    Clean files from a directory.
    
    Args:
        directory: Path to directory
        pattern: Glob pattern for files to remove
        exclude: List of filenames to exclude
        dry_run: If True, only show what would be removed
    
    Returns:
        Number of files removed
    """
    if not directory.exists():
        return 0
    
    exclude = exclude or [".gitkeep", "README.md"]
    removed = 0
    
    for file_path in directory.glob(pattern):
        if file_path.is_file() and file_path.name not in exclude:
            if dry_run:
                logger.info(f"  [DRY RUN] Would remove: {file_path}")
            else:
                file_path.unlink()
                logger.debug(f"  Removed: {file_path}")
            removed += 1
    
    return removed


def main():
    parser = argparse.ArgumentParser(
        description="Cleanup Week 4 Laboratory Environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cleanup.py              # Basic cleanup (stop containers)
  python cleanup.py --full       # Full cleanup including volumes
  python cleanup.py --dry-run    # Show what would be removed
  python cleanup.py --prune      # Also prune unused Docker resources
        """
    )
    
    parser.add_argument("--full", action="store_true",
                        help="Remove volumes and all data (use before next week)")
    parser.add_argument("--prune", action="store_true",
                        help="Also prune unused Docker resources")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be removed without removing")
    parser.add_argument("--keep-portainer", action="store_true",
                        help="Keep Portainer container and data")
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("Cleaning up Week 4 Laboratory Environment")
    logger.info("=" * 60)
    
    if args.dry_run:
        logger.info("[DRY RUN] No changes will be made")
    
    docker_dir = PROJECT_ROOT / "docker"
    
    try:
        # Docker cleanup
        logger.info("")
        logger.info("Docker cleanup:")
        
        docker = DockerManager(docker_dir)
        
        # Stop and remove containers
        logger.info("  Stopping containers...")
        docker.compose_down(volumes=args.full, dry_run=args.dry_run)
        
        # Remove week-specific resources
        if not args.dry_run:
            logger.info(f"  Removing {WEEK_PREFIX}_* resources...")
            docker.remove_by_prefix(WEEK_PREFIX, dry_run=args.dry_run)
        
        # Keep Portainer if requested
        if args.keep_portainer:
            logger.info("  Keeping Portainer container and data")
        
    except FileNotFoundError:
        logger.warning("Docker Compose file not found, skipping Docker cleanup")
    except Exception as e:
        logger.warning(f"Docker cleanup error: {e}")
    
    # File cleanup
    logger.info("")
    logger.info("File cleanup:")
    
    # Clean artifacts directory
    artifacts_dir = PROJECT_ROOT / "artifacts"
    count = clean_directory(artifacts_dir, "*", dry_run=args.dry_run)
    logger.info(f"  Artifacts: {count} files {'would be ' if args.dry_run else ''}removed")
    
    # Clean pcap directory
    pcap_dir = PROJECT_ROOT / "pcap"
    count = clean_directory(pcap_dir, "*.pcap", dry_run=args.dry_run)
    logger.info(f"  Packet captures: {count} files {'would be ' if args.dry_run else ''}removed")
    
    # Clean Python cache
    if args.full:
        logger.info("  Cleaning Python cache...")
        if not args.dry_run:
            for cache_dir in PROJECT_ROOT.rglob("__pycache__"):
                if cache_dir.is_dir():
                    import shutil
                    shutil.rmtree(cache_dir)
            
            for pyc_file in PROJECT_ROOT.rglob("*.pyc"):
                pyc_file.unlink()
    
    # Docker system prune
    if args.prune and not args.dry_run:
        logger.info("")
        logger.info("Pruning unused Docker resources...")
        result = subprocess.run(
            ["docker", "system", "prune", "-f"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            logger.info("  Docker prune completed")
            # Parse reclaimed space from output
            if "reclaimed" in result.stdout.lower():
                for line in result.stdout.split("\n"):
                    if "reclaimed" in line.lower():
                        logger.info(f"  {line.strip()}")
    
    # Summary
    logger.info("")
    logger.info("=" * 60)
    if args.dry_run:
        logger.info("Dry run complete. Run without --dry-run to apply changes.")
    else:
        logger.info("Cleanup complete!")
        if args.full:
            logger.info("System is ready for the next laboratory session.")
    logger.info("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
