#!/usr/bin/env python3
"""
Week 6 Laboratory Cleanup
=========================
Computer Networks - Week 6 (WSL Environment)
ASE Bucharest | by ing. dr. Antonio Clim

This script removes all containers, networks and optionally volumes
to prepare the system for the next laboratory session.

Usage:
    python scripts/cleanup.py           # Standard cleanup
    python scripts/cleanup.py --full    # Remove all data
    python scripts/cleanup.py --prune   # Also prune Docker resources
"""

from __future__ import annotations
from typing import Optional, List, Dict, Tuple, Any

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS_AND_SETUP
# ═══════════════════════════════════════════════════════════════════════════════

import argparse
import subprocess
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger

logger = setup_logger("cleanup")

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

WEEK_PREFIX = "week6"


# ═══════════════════════════════════════════════════════════════════════════════
# MININET_CLEANUP
# ═══════════════════════════════════════════════════════════════════════════════

def cleanup_mininet() -> bool:
    """
    Clean up Mininet residual state.
    
    Mininet can leave behind network namespaces, virtual interfaces
    and OVS bridges if not properly shut down.
    
    Returns:
        True if successful
    """
    logger.info("Cleaning up Mininet state...")
    
    try:
        # Run mn -c to clean Mininet
        result = subprocess.run(
            ["sudo", "mn", "-c"],
            capture_output=True,
            timeout=30
        )
        if result.returncode == 0:
            logger.info("  ✓ Mininet cleanup successful")
            return True
        else:
            logger.warning("  ! Mininet cleanup returned non-zero (may be OK)")
            return True
    except subprocess.TimeoutExpired:
        logger.warning("  ! Mininet cleanup timed out")
        return False
    except FileNotFoundError:
        logger.debug("  Mininet not installed (cleanup skipped)")
        return True
    except Exception as e:
        logger.warning(f"  ! Mininet cleanup error: {e}")
        return True  # Not critical


# ═══════════════════════════════════════════════════════════════════════════════
# OVS_CLEANUP
# ═══════════════════════════════════════════════════════════════════════════════

def cleanup_ovs() -> bool:
    """
    Clean up Open vSwitch bridges.
    
    OVS bridges persist across Mininet restarts if not explicitly deleted.
    This function removes all OVS bridges to ensure a clean state.
    
    Returns:
        True if successful
    """
    logger.info("Cleaning up OVS bridges...")
    
    try:
        # List OVS bridges
        result = subprocess.run(
            ["sudo", "ovs-vsctl", "list-br"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            logger.debug("  OVS not available (cleanup skipped)")
            return True
        
        bridges = result.stdout.strip().split('\n')
        bridges = [b for b in bridges if b]
        
        for bridge in bridges:
            logger.info(f"  Removing bridge: {bridge}")
            subprocess.run(
                ["sudo", "ovs-vsctl", "--if-exists", "del-br", bridge],
                capture_output=True,
                timeout=10
            )
        
        logger.info("  ✓ OVS cleanup successful")
        return True
    except FileNotFoundError:
        logger.debug("  OVS not installed (cleanup skipped)")
        return True
    except Exception as e:
        logger.warning(f"  ! OVS cleanup error: {e}")
        return True  # Not critical


# ═══════════════════════════════════════════════════════════════════════════════
# ARTIFACTS_CLEANUP
# ═══════════════════════════════════════════════════════════════════════════════

def cleanup_artifacts(full: bool = False) -> None:
    """
    Clean up generated artifacts.
    
    Args:
        full: Whether to remove all artifacts including pcap files
    """
    logger.info("Cleaning up artifacts...")
    
    artifacts_dir = PROJECT_ROOT / "artifacts"
    pcap_dir = PROJECT_ROOT / "pcap"
    
    if not full:
        logger.info("  Keeping artifacts (use --full to remove)")
        return
    
    # Clean artifacts directory
    if artifacts_dir.exists():
        for f in artifacts_dir.glob("*"):
            if f.name != ".gitkeep":
                if f.is_file():
                    f.unlink()
                    logger.debug(f"  Removed: {f.name}")
        logger.info("  ✓ Artifacts cleaned")
    
    # Clean pcap directory
    if pcap_dir.exists():
        for f in pcap_dir.glob("*.pcap"):
            f.unlink()
            logger.debug(f"  Removed: {f.name}")
        logger.info("  ✓ Packet captures cleaned")


# ═══════════════════════════════════════════════════════════════════════════════
# ARGUMENT_PARSING
# ═══════════════════════════════════════════════════════════════════════════════

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Cleanup Week 6 Laboratory Environment"
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
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    return parser.parse_args()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point."""
    args = parse_arguments()
    
    if args.verbose:
        from scripts.utils.logger import set_verbose
        set_verbose(logger, True)
    
    docker_dir = PROJECT_ROOT / "docker"
    
    try:
        docker = DockerManager(docker_dir)
    except FileNotFoundError as e:
        logger.error(f"Docker configuration not found: {e}")
        return 1
    
    # ─────────────────────────────────────────────────────────────────────────
    # Display cleanup mode
    # ─────────────────────────────────────────────────────────────────────────
    
    logger.info("=" * 60)
    logger.info("Cleaning up Week 6 Laboratory Environment")
    if args.full:
        logger.info("Mode: FULL cleanup (removes all data)")
    else:
        logger.info("Mode: Standard cleanup (preserves data)")
    logger.info("=" * 60)
    
    if args.dry_run:
        logger.info("[DRY RUN] No changes will be made")
        logger.info("")
    
    # ─────────────────────────────────────────────────────────────────────────
    # Confirmation for full cleanup
    # ─────────────────────────────────────────────────────────────────────────
    
    if args.full and not args.force and not args.dry_run:
        print()
        print("WARNING: Full cleanup will remove all data including:")
        print("  - Docker volumes")
        print("  - Packet captures")
        print("  - Generated artifacts")
        print()
        response = input("Are you sure? (yes/no): ")
        if response.lower() not in ("yes", "y"):
            print("Cleanup cancelled")
            return 0
    
    # ─────────────────────────────────────────────────────────────────────────
    # Execute cleanup steps
    # ─────────────────────────────────────────────────────────────────────────
    
    try:
        # Step 1: Stop Docker Compose services
        logger.info("")
        logger.info("Stopping Docker services...")
        docker.compose_down(volumes=args.full, dry_run=args.dry_run)
        
        # Step 2: Remove week-specific Docker resources
        logger.info("")
        logger.info(f"Removing {WEEK_PREFIX}_* resources...")
        docker.remove_by_prefix(WEEK_PREFIX, dry_run=args.dry_run)
        
        # Step 3: Clean Mininet (if available)
        if not args.dry_run:
            logger.info("")
            cleanup_mininet()
        
        # Step 4: Clean OVS (if available)
        if not args.dry_run:
            logger.info("")
            cleanup_ovs()
        
        # Step 5: Clean artifacts
        if not args.dry_run:
            logger.info("")
            cleanup_artifacts(full=args.full)
        
        # Step 6: Prune Docker (optional)
        if args.prune and not args.dry_run:
            logger.info("")
            logger.info("Pruning unused Docker resources...")
            docker.system_prune()
        
        # ─────────────────────────────────────────────────────────────────────
        # Summary
        # ─────────────────────────────────────────────────────────────────────
        
        logger.info("")
        logger.info("=" * 60)
        if args.dry_run:
            logger.info("[DRY RUN] Cleanup simulation complete")
        else:
            logger.info("✓ Cleanup complete!")
            if args.full:
                logger.info("System is ready for the next laboratory session.")
            else:
                logger.info("Containers removed, data preserved.")
                logger.info("Use --full to remove all data.")
        logger.info("=" * 60)
        
        return 0
    
    except KeyboardInterrupt:
        print("\nCleanup interrupted")
        return 130
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
