#!/usr/bin/env python3
"""
Week 5 Laboratory Cleanup
NETWORKING class - ASE, Informatics | by Revolvix

Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment

This script removes all containers, networks, and optionally volumes
to prepare the system for the next laboratory session.

IMPORTANT: Portainer runs as a GLOBAL service on port 9000.
This script will NEVER remove Portainer - it must remain running for all weeks.
"""

import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger

logger = setup_logger("cleanup")

WEEK_PREFIX = "week5"
PROTECTED_CONTAINERS = ["portainer"]


def is_protected(name: str) -> bool:
    """Check if a resource name is protected."""
    name_lower = name.lower()
    return any(protected in name_lower for protected in PROTECTED_CONTAINERS)


def clean_directory(directory: Path, pattern: str = "*", keep: list = None) -> int:
    """Clean files from a directory."""
    keep = keep or [".gitkeep", "README.md"]
    count = 0
    
    if not directory.exists():
        return 0
    
    for item in directory.glob(pattern):
        if item.name not in keep and item.is_file():
            item.unlink()
            count += 1
    
    return count


def check_portainer_status() -> tuple:
    """Check Portainer container status."""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=portainer",
             "--format", "{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.stdout.strip() and "up" in result.stdout.lower():
            return True, result.stdout.strip()
        return False, "Not running"
    except Exception:
        return False, "Unknown"


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Cleanup Week 5 Laboratory Environment (WSL2)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/cleanup.py              # Basic cleanup
  python3 scripts/cleanup.py --full       # Full cleanup including volumes
  python3 scripts/cleanup.py --dry-run    # Show what would be removed

Notes:
  - Portainer is NEVER removed (global service on port 9000)
  - Use 'docker stop portainer' only if you specifically need to stop it
        """
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Remove volumes and all data"
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
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    print()
    print("=" * 60)
    print("  Cleaning up Week 5 Laboratory Environment")
    print("  (Portainer will NOT be removed - it runs globally)")
    print("=" * 60)
    print()
    
    if args.dry_run:
        logger.info("[DRY RUN] No changes will be made")
        print()
    
    try:
        docker = DockerManager(PROJECT_ROOT / "docker")
    except FileNotFoundError as e:
        logger.error(f"Docker configuration not found: {e}")
        return 1
    
    try:
        # Stop and remove containers (NOT Portainer)
        logger.info("Stopping and removing lab containers...")
        logger.info("(Portainer is preserved)")
        docker.compose_down(volumes=args.full, dry_run=args.dry_run)
        
        # Remove week-specific resources
        logger.info(f"Removing {WEEK_PREFIX}_* resources...")
        docker.remove_by_prefix(WEEK_PREFIX, dry_run=args.dry_run)
        
        # Clean local directories
        if args.full and not args.dry_run:
            logger.info("Cleaning artifacts directory...")
            count = clean_directory(PROJECT_ROOT / "artifacts", "*.log")
            count += clean_directory(PROJECT_ROOT / "artifacts", "*.txt")
            count += clean_directory(PROJECT_ROOT / "artifacts", "*.json")
            if count > 0:
                logger.info(f"  Removed {count} artifact files")
            
            logger.info("Cleaning pcap directory...")
            count = clean_directory(PROJECT_ROOT / "pcap", "*.pcap")
            count += clean_directory(PROJECT_ROOT / "pcap", "*.pcapng")
            if count > 0:
                logger.info(f"  Removed {count} capture files")
        elif args.full and args.dry_run:
            logger.info("[DRY RUN] Would clean artifacts and pcap directories")
        
        # Optional system prune
        if args.prune and not args.dry_run:
            logger.info("Pruning unused Docker resources...")
            docker.system_prune()
        elif args.prune and args.dry_run:
            logger.info("[DRY RUN] Would prune Docker system")
        
        print()
        print("=" * 60)
        print("  \033[92mCleanup complete!\033[0m")
        if args.full:
            print("  System is ready for the next laboratory session.")
        
        # Confirm Portainer status
        portainer_running, portainer_status = check_portainer_status()
        if portainer_running:
            print(f"\n  \033[92mPortainer still running:\033[0m http://localhost:9000")
        else:
            print(f"\n  \033[93mPortainer is not running.\033[0m")
            print("  Start with: docker start portainer")
        
        print("=" * 60)
        print()
        
        return 0
    
    except KeyboardInterrupt:
        logger.info("Cleanup cancelled by user")
        return 130
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
