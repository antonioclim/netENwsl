#!/usr/bin/env python3
"""
Week 1 Laboratory Cleanup
NETWORKING class - ASE, Informatics | by Revolvix

This script removes all containers, networks, and optionally volumes
to prepare the system for the next laboratory session.
"""

from __future__ import annotations

import subprocess
import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger

logger = setup_logger("cleanup")

WEEK_PREFIX = "week1"


def confirm_action(message: str) -> bool:
    """Prompt user for confirmation."""
    try:
        response = input(f"\n{message} [y/N]: ").strip().lower()
        return response in ("y", "yes")
    except (EOFError, KeyboardInterrupt):
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Cleanup Week 1 Laboratory Environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/cleanup.py              # Basic cleanup (stop containers)
  python scripts/cleanup.py --full       # Remove volumes and all data
  python scripts/cleanup.py --prune      # Also prune unused Docker resources
  python scripts/cleanup.py --dry-run    # Show what would be removed
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
        "--force", "-f",
        action="store_true",
        help="Skip confirmation prompts"
    )
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Cleaning up Week 1 Laboratory Environment")
    logger.info("NETWORKING class - ASE, Informatics | by Revolvix")
    logger.info("=" * 60)

    if args.dry_run:
        logger.info("\033[93m[DRY RUN] No changes will be made\033[0m")
    
    if args.full and not args.dry_run and not args.force:
        if not confirm_action("This will remove all data and volumes. Continue?"):
            logger.info("Cleanup cancelled.")
            return 0

    docker_dir = PROJECT_ROOT / "docker"
    
    try:
        docker = DockerManager(docker_dir)
    except FileNotFoundError:
        logger.warning("docker-compose.yml not found, performing manual cleanup...")
        docker = None

    try:
        # Stop and remove containers
        logger.info("\nStopping containers...")
        
        if docker:
            docker.compose_down(volumes=args.full, dry_run=args.dry_run)
        else:
            # Manual cleanup
            containers = ["week1_lab", "week1_portainer"]
            for container in containers:
                if args.dry_run:
                    logger.info(f"  Would remove: {container}")
                else:
                    subprocess.run(["docker", "rm", "-f", container], capture_output=True)
                    logger.info(f"  Removed: {container}")

        # Remove week-specific resources
        logger.info(f"\nRemoving {WEEK_PREFIX}_* resources...")
        
        if docker:
            docker.remove_by_prefix(WEEK_PREFIX, dry_run=args.dry_run)
        else:
            # Manual network cleanup
            try:
                result = subprocess.run(
                    ["docker", "network", "ls", "--filter", f"name={WEEK_PREFIX}",
                     "--format", "{{.Name}}"],
                    capture_output=True,
                    text=True
                )
                for network in result.stdout.strip().split("\n"):
                    if network:
                        if args.dry_run:
                            logger.info(f"  Would remove network: {network}")
                        else:
                            subprocess.run(["docker", "network", "rm", network],
                                         capture_output=True)
                            logger.info(f"  Removed network: {network}")
            except Exception:
                pass

        # Clean artifacts directory
        if args.full and not args.dry_run:
            logger.info("\nCleaning artifacts directory...")
            artifacts_dir = PROJECT_ROOT / "artifacts"
            if artifacts_dir.exists():
                for f in artifacts_dir.iterdir():
                    if f.name != ".gitkeep":
                        if f.is_file():
                            f.unlink()
                            logger.info(f"  Removed: {f.name}")

            logger.info("\nCleaning pcap directory...")
            pcap_dir = PROJECT_ROOT / "pcap"
            if pcap_dir.exists():
                for f in pcap_dir.glob("*.pcap"):
                    f.unlink()
                    logger.info(f"  Removed: {f.name}")

        # Remove volumes
        if args.full and not args.dry_run:
            logger.info("\nRemoving Docker volumes...")
            try:
                result = subprocess.run(
                    ["docker", "volume", "ls", "--filter", f"name={WEEK_PREFIX}",
                     "--format", "{{.Name}}"],
                    capture_output=True,
                    text=True
                )
                for volume in result.stdout.strip().split("\n"):
                    if volume:
                        subprocess.run(["docker", "volume", "rm", volume],
                                     capture_output=True)
                        logger.info(f"  Removed volume: {volume}")
            except Exception as e:
                logger.warning(f"Could not remove volumes: {e}")

        # Optional system prune
        if args.prune and not args.dry_run:
            logger.info("\nPruning unused Docker resources...")
            if docker:
                docker.system_prune()
            else:
                subprocess.run(["docker", "system", "prune", "-f"], capture_output=True)
                logger.info("  Pruned unused resources")

        # Summary
        logger.info("")
        logger.info("=" * 60)
        if args.dry_run:
            logger.info("Dry run complete. No changes were made.")
        else:
            logger.info("\033[92mCleanup complete!\033[0m")
            if args.full:
                logger.info("\nSystem is ready for the next laboratory session.")
            else:
                logger.info("\nContainers stopped. Data preserved.")
                logger.info("Use --full to remove all data.")
        logger.info("=" * 60)
        
        return 0

    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
