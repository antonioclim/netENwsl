#!/usr/bin/env python3
"""
Week 8 Laboratory Cleanup
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
from scripts.utils.logger import setup_logger, print_banner

logger = setup_logger("cleanup")

WEEK_PREFIX = "week8"


def clean_artifacts():
    """Clean the artifacts directory."""
    artifacts_dir = PROJECT_ROOT / "artifacts"
    count = 0
    
    for f in artifacts_dir.glob("*"):
        if f.name != ".gitkeep":
            try:
                f.unlink()
                count += 1
            except Exception as e:
                logger.warning(f"Could not remove {f}: {e}")
    
    return count


def clean_pcap():
    """Clean the pcap directory."""
    pcap_dir = PROJECT_ROOT / "pcap"
    count = 0
    
    for f in pcap_dir.glob("*.pcap"):
        try:
            f.unlink()
            count += 1
        except Exception as e:
            logger.warning(f"Could not remove {f}: {e}")
    
    return count


def main():
    parser = argparse.ArgumentParser(
        description="Cleanup Week 8 Laboratory Environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/cleanup.py            # Stop containers only
  python scripts/cleanup.py --full     # Remove everything
  python scripts/cleanup.py --prune    # Also prune Docker system
  python scripts/cleanup.py --dry-run  # Show what would be done
        """
    )
    parser.add_argument(
        "--full", "-f",
        action="store_true",
        help="Remove volumes, artifacts, and all data"
    )
    parser.add_argument(
        "--prune",
        action="store_true",
        help="Also prune unused Docker resources"
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show what would be removed without removing"
    )
    parser.add_argument(
        "--yes", "-y",
        action="store_true",
        help="Skip confirmation prompts"
    )
    
    args = parser.parse_args()
    
    print_banner(
        "Cleaning Week 8 Laboratory",
        "Transport Layer: HTTP Server and Reverse Proxies"
    )
    
    if args.dry_run:
        logger.info("[DRY RUN] No changes will be made\n")
    
    # Confirm full cleanup
    if args.full and not args.dry_run and not args.yes:
        print("WARNING: This will remove all data including:")
        print("  - Docker volumes (persistent data)")
        print("  - Artifact files")
        print("  - Packet captures")
        print()
        response = input("Are you sure? [y/N]: ").strip().lower()
        if response != "y":
            logger.info("Cleanup cancelled")
            return 0
    
    try:
        docker = DockerManager(PROJECT_ROOT / "docker")
        
        # Stop and remove containers
        logger.info("Stopping containers...")
        docker.compose_down(volumes=args.full, dry_run=args.dry_run)
        
        # Remove week-specific resources
        logger.info(f"\nRemoving {WEEK_PREFIX}-* resources...")
        docker.remove_by_prefix(WEEK_PREFIX, dry_run=args.dry_run)
        
        # Clean directories
        if args.full:
            logger.info("\nCleaning artifact directory...")
            if not args.dry_run:
                count = clean_artifacts()
                logger.info(f"  Removed {count} artifact files")
            else:
                artifacts = list((PROJECT_ROOT / "artifacts").glob("*"))
                logger.info(f"  [DRY RUN] Would remove {len(artifacts)} files")
            
            logger.info("Cleaning pcap directory...")
            if not args.dry_run:
                count = clean_pcap()
                logger.info(f"  Removed {count} capture files")
            else:
                pcaps = list((PROJECT_ROOT / "pcap").glob("*.pcap"))
                logger.info(f"  [DRY RUN] Would remove {len(pcaps)} files")
        
        # Optional system prune
        if args.prune and not args.dry_run:
            logger.info("\nPruning unused Docker resources...")
            docker.system_prune()
        elif args.prune and args.dry_run:
            logger.info("\n[DRY RUN] Would prune unused Docker resources")
        
        # Summary
        print()
        print("=" * 50)
        if args.dry_run:
            print("Dry run complete - no changes made")
        else:
            print("✓ Cleanup complete!")
            if args.full:
                print("  System is ready for the next laboratory session.")
            else:
                print("  Containers stopped. Run with --full to remove all data.")
        print("=" * 50)
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"Compose file not found: {e}")
        return 1
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
