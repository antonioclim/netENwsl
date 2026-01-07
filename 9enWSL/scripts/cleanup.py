#!/usr/bin/env python3
"""
Week 9 Laboratory Cleanup
NETWORKING class - ASE, Informatics | by Revolvix

This script removes all containers, networks, and optionally volumes
to prepare the system for the next laboratory session.

Usage:
    python scripts/cleanup.py           # Basic cleanup (stop + remove)
    python scripts/cleanup.py --full    # Full cleanup including volumes
    python scripts/cleanup.py --prune   # Also prune unused Docker resources
    python scripts/cleanup.py --dry-run # Show what would be removed
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger, print_banner

logger = setup_logger("cleanup")

WEEK_PREFIX = "s9"


def clean_artifacts(dry_run: bool = False) -> None:
    """Clean generated artifacts and temporary files."""
    artifacts_dir = PROJECT_ROOT / "artifacts"
    pcap_dir = PROJECT_ROOT / "pcap"
    
    # Clean artifacts
    if artifacts_dir.exists():
        for f in artifacts_dir.glob("*"):
            if f.name != ".gitkeep":
                if dry_run:
                    logger.info(f"[DRY RUN] Would remove: {f}")
                else:
                    try:
                        f.unlink()
                        logger.debug(f"Removed: {f}")
                    except OSError as e:
                        logger.warning(f"Could not remove {f}: {e}")
    
    # Clean pcap files
    if pcap_dir.exists():
        for f in pcap_dir.glob("*.pcap"):
            if dry_run:
                logger.info(f"[DRY RUN] Would remove: {f}")
            else:
                try:
                    f.unlink()
                    logger.debug(f"Removed: {f}")
                except OSError as e:
                    logger.warning(f"Could not remove {f}: {e}")


def clean_client_files(dry_run: bool = False) -> None:
    """Clean downloaded files in client directories."""
    client_dirs = [
        PROJECT_ROOT / "docker" / "client1-files",
        PROJECT_ROOT / "docker" / "client2-files"
    ]
    
    for client_dir in client_dirs:
        if client_dir.exists():
            for f in client_dir.iterdir():
                if f.name != ".gitkeep":
                    if dry_run:
                        logger.info(f"[DRY RUN] Would remove: {f}")
                    else:
                        try:
                            if f.is_file():
                                f.unlink()
                            logger.debug(f"Removed: {f}")
                        except OSError as e:
                            logger.warning(f"Could not remove {f}: {e}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Cleanup Week 9 Laboratory Environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/cleanup.py              # Stop and remove containers
  python scripts/cleanup.py --full       # Full cleanup including volumes
  python scripts/cleanup.py --prune      # Also prune unused Docker resources
  python scripts/cleanup.py --dry-run    # Preview what would be removed
        """
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Remove volumes and all data (use before next week)"
    )
    parser.add_argument(
        "--prune",
        action="store_true",
        help="Also prune unused Docker resources"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be removed without removing"
    )
    parser.add_argument(
        "--keep-server-files",
        action="store_true",
        help="Keep server files when doing full cleanup"
    )
    
    args = parser.parse_args()
    
    print_banner("Week 9 Laboratory Cleanup")
    
    if args.dry_run:
        logger.info("[DRY RUN] No changes will be made")
        print()
    
    docker = DockerManager(PROJECT_ROOT / "docker")
    
    try:
        # Step 1: Stop and remove containers
        logger.info("Stopping and removing containers...")
        docker.compose_down(
            volumes=args.full,
            dry_run=args.dry_run
        )
        
        # Step 2: Remove week-specific resources by prefix
        logger.info(f"Removing {WEEK_PREFIX}_* resources...")
        docker.remove_by_prefix(WEEK_PREFIX, dry_run=args.dry_run)
        
        # Step 3: Clean artifacts and pcap files
        if args.full:
            logger.info("Cleaning artifacts directory...")
            clean_artifacts(dry_run=args.dry_run)
            
            logger.info("Cleaning client files...")
            clean_client_files(dry_run=args.dry_run)
            
            if not args.keep_server_files:
                server_dir = PROJECT_ROOT / "docker" / "server-files"
                if server_dir.exists():
                    logger.info("Cleaning server files...")
                    for f in server_dir.iterdir():
                        if f.name != ".gitkeep":
                            if args.dry_run:
                                logger.info(f"[DRY RUN] Would remove: {f}")
                            else:
                                try:
                                    f.unlink()
                                except OSError:
                                    pass
        
        # Step 4: Optional system prune
        if args.prune and not args.dry_run:
            logger.info("Pruning unused Docker resources...")
            docker.system_prune()
        
        # Summary
        print()
        print("=" * 60)
        print("Cleanup Complete!")
        print("=" * 60)
        
        if args.dry_run:
            print("\n[DRY RUN] No changes were made")
        elif args.full:
            print("\nFull cleanup performed:")
            print("  - All containers removed")
            print("  - All volumes removed")
            print("  - Artifacts and pcap files cleaned")
            print("\nSystem is ready for the next laboratory session.")
        else:
            print("\nBasic cleanup performed:")
            print("  - Containers stopped and removed")
            print("  - Networks removed")
            print("\nTo perform full cleanup: python scripts/cleanup.py --full")
        
        print()
        print("=" * 60)
        
        return 0
        
    except KeyboardInterrupt:
        logger.warning("\nInterrupted by user")
        return 130
    
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
