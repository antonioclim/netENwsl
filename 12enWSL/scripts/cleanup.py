#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_DOCSTRING
# ═══════════════════════════════════════════════════════════════════════════════
"""
Week 12 Laboratory Cleanup
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment

This script removes all containers, networks and optionally volumes
to prepare the system for the next laboratory session.

IMPORTANT: Portainer runs as a GLOBAL service on port 9000.
This script will NEVER remove Portainer - it must remain running for all weeks.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger

logger = setup_logger("cleanup")

WEEK_PREFIX = "week12_"
PROTECTED_CONTAINERS = ["portainer"]



# ═══════════════════════════════════════════════════════════════════════════════
# IS_PROTECTED_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def is_protected(name: str) -> bool:
    """Check if a resource name is protected."""
    name_lower = name.lower()
    return any(protected in name_lower for protected in PROTECTED_CONTAINERS)



# ═══════════════════════════════════════════════════════════════════════════════
# CLEAN_DIRECTORY_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
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



# ═══════════════════════════════════════════════════════════════════════════════
# CHECK_PORTAINER_STATUS_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
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


# ═══════════════════════════════════════════════════════════════════════════════
# CLEANUP_HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def _stop_lab_containers(docker: DockerManager, full: bool, dry_run: bool) -> None:
    """Stop and remove lab containers (preserving Portainer)."""
    logger.info("Stopping and removing lab containers...")
    logger.info("(Portainer is preserved)")
    docker.compose_down(volumes=full, dry_run=dry_run)


def _remove_week_resources(docker: DockerManager, dry_run: bool) -> None:
    """Remove week-specific Docker resources."""
    logger.info(f"Removing {WEEK_PREFIX}* resources...")
    docker.remove_by_prefix(WEEK_PREFIX, dry_run=dry_run)


def _clean_local_directories(dry_run: bool) -> None:
    """Clean spool, pcap and artifacts directories."""
    if dry_run:
        logger.info("[DRY RUN] Would clean spool, pcap and artifacts directories")
        return
    
    logger.info("Cleaning spool directory...")
    count = clean_directory(PROJECT_ROOT / "docker/volumes/spool", "*.eml")
    if count > 0:
        logger.info(f"  Removed {count} email files")
    
    logger.info("Cleaning pcap directory...")
    count = clean_directory(PROJECT_ROOT / "pcap", "*.pcap")
    count += clean_directory(PROJECT_ROOT / "pcap", "*.pcapng")
    if count > 0:
        logger.info(f"  Removed {count} capture files")
    
    logger.info("Cleaning artifacts directory...")
    count = clean_directory(PROJECT_ROOT / "artifacts", "*.log")
    count += clean_directory(PROJECT_ROOT / "artifacts", "*.json")
    if count > 0:
        logger.info(f"  Removed {count} artifact files")


def _run_system_prune(docker: DockerManager, dry_run: bool) -> None:
    """Prune unused Docker resources."""
    if dry_run:
        logger.info("[DRY RUN] Would prune Docker system")
        return
    logger.info("Pruning unused Docker resources...")
    docker.system_prune()


def _print_completion_summary(full: bool) -> None:
    """Print cleanup completion summary."""
    print()
    print("=" * 60)
    print("  \033[92mCleanup complete!\033[0m")
    if full:
        print("  System is ready for the next laboratory session.")
    
    portainer_running, _ = check_portainer_status()
    if portainer_running:
        print(f"\n  \033[92mPortainer still running:\033[0m http://localhost:9000")
    else:
        print(f"\n  \033[93mPortainer is not running.\033[0m")
        print("  Start with: docker start portainer")
    
    print("=" * 60)
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGUMENTS
# ═══════════════════════════════════════════════════════════════════════════════
def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Cleanup Week 12 Laboratory Environment (WSL2)",
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
    
    return parser.parse_args()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    args = parse_arguments()
    
    print()
    print("=" * 60)
    print("  Cleaning up Week 12 Laboratory Environment")
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
        _stop_lab_containers(docker, args.full, args.dry_run)
        _remove_week_resources(docker, args.dry_run)
        
        if args.full:
            _clean_local_directories(args.dry_run)
        
        if args.prune:
            _run_system_prune(docker, args.dry_run)
        
        _print_completion_summary(args.full)
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



# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    sys.exit(main())
