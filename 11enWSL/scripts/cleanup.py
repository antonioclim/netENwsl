#!/usr/bin/env python3
"""
Week 11 Laboratory Cleanup
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
from scripts.utils.logger import setup_logger, print_banner

logger = setup_logger("cleanup")

WEEK_PREFIX = "s11"


def clean_artifacts(dry_run: bool = False) -> None:
    """Clean the artifacts directory."""
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
                    logger.info(f"Removed: {f.name}")
            except Exception as e:
                logger.warning(f"Failed to remove {f}: {e}")


def clean_pcap(dry_run: bool = False) -> None:
    """Clean the pcap directory."""
    pcap_dir = PROJECT_ROOT / "pcap"
    
    if not pcap_dir.exists():
        return
    
    for f in pcap_dir.glob("*.pcap"):
        if dry_run:
            logger.info(f"[DRY RUN] Would remove: {f}")
        else:
            try:
                f.unlink()
                logger.info(f"Removed: {f.name}")
            except Exception as e:
                logger.warning(f"Failed to remove {f}: {e}")


def kill_python_processes() -> None:
    """Kill any lingering Python backend/loadbalancer processes."""
    import os
    import signal
    
    try:
        # Find Python processes related to exercises
        result = subprocess.run(
            ["pgrep", "-f", "ex_11_"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid:
                    try:
                        os.kill(int(pid), signal.SIGTERM)
                        logger.info(f"Terminated Python process: {pid}")
                    except ProcessLookupError:
                        pass
                    except PermissionError:
                        logger.warning(f"Permission denied to kill process {pid}")
    except Exception:
        # pgrep may not exist on Windows
        pass


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Cleanup Week 11 Laboratory Environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s              # Basic cleanup (containers only)
  %(prog)s --full       # Full cleanup including volumes
  %(prog)s --prune      # Also prune unused Docker resources
  %(prog)s --dry-run    # Show what would be removed
        """
    )
    parser.add_argument("--full", action="store_true",
                        help="Remove volumes and all data (use before next week)")
    parser.add_argument("--prune", action="store_true",
                        help="Also prune unused Docker resources")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be removed without removing")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose output")
    
    args = parser.parse_args()
    
    docker_dir = PROJECT_ROOT / "docker"
    
    try:
        docker = DockerManager(docker_dir)
    except FileNotFoundError as e:
        logger.error(f"Docker configuration not found: {e}")
        return 1
    
    print_banner("Week 11 Laboratory Cleanup")
    
    if args.dry_run:
        logger.info("[DRY RUN] No changes will be made")
        print("")
    
    try:
        # Kill Python processes
        if not args.dry_run:
            logger.info("Terminating any Python processes...")
            kill_python_processes()
        
        # Stop containers
        logger.info("Stopping Docker Compose stack...")
        docker.compose_down(volumes=args.full, dry_run=args.dry_run)
        
        # Remove week-specific resources
        logger.info(f"Removing {WEEK_PREFIX}_* resources...")
        docker.remove_by_prefix(WEEK_PREFIX, dry_run=args.dry_run)
        
        # Clean artifacts
        if args.full:
            logger.info("Cleaning artifacts directory...")
            clean_artifacts(dry_run=args.dry_run)
            
            logger.info("Cleaning pcap directory...")
            clean_pcap(dry_run=args.dry_run)
        
        # Optional system prune
        if args.prune and not args.dry_run:
            logger.info("Pruning unused Docker resources...")
            docker.system_prune()
        
        # Summary
        print("")
        print("=" * 60)
        if args.dry_run:
            logger.info("[DRY RUN] Cleanup simulation complete")
        else:
            logger.info("Cleanup complete!")
            if args.full:
                logger.info("System is ready for the next laboratory session.")
            else:
                logger.info("For full cleanup, run with --full flag")
        print("=" * 60)
        
        return 0
    
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user")
        return 130
    
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())


# Revolvix&Hypotheticalandrei
