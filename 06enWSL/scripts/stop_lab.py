#!/usr/bin/env python3
"""
Week 6 Laboratory Shutdown
==========================
Computer Networks - Week 6 (WSL Environment)
ASE Bucharest | by ing. dr. Antonio Clim

This script gracefully stops all Docker containers while preserving data.

Usage:
    python scripts/stop_lab.py              # Graceful stop
    python scripts/stop_lab.py --force      # Force stop
    python scripts/stop_lab.py -t 60        # Custom timeout
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

logger = setup_logger("stop_lab")


# ═══════════════════════════════════════════════════════════════════════════════
# ARGUMENT_PARSING
# ═══════════════════════════════════════════════════════════════════════════════

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Stop Week 6 Laboratory Environment"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=30,
        help="Timeout in seconds for graceful shutdown (default: 30)"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force stop containers immediately"
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
    
    # ─────────────────────────────────────────────────────────────────────────
    # Locate Docker configuration
    # ─────────────────────────────────────────────────────────────────────────
    
    docker_dir = PROJECT_ROOT / "docker"
    
    try:
        docker = DockerManager(docker_dir)
    except FileNotFoundError as e:
        logger.error(f"Docker configuration not found: {e}")
        return 1
    
    # ─────────────────────────────────────────────────────────────────────────
    # Display banner
    # ─────────────────────────────────────────────────────────────────────────
    
    logger.info("=" * 60)
    logger.info("Stopping Week 6 Laboratory Environment")
    logger.info("=" * 60)
    
    try:
        # ─────────────────────────────────────────────────────────────────────
        # Show current status
        # ─────────────────────────────────────────────────────────────────────
        
        logger.info("Current running services:")
        status = docker.compose_ps()
        for name, info in status.items():
            state = info.get("State", "unknown")
            logger.info(f"  {name}: {state}")
        
        if not status:
            logger.info("  No services running")
            return 0
        
        # ─────────────────────────────────────────────────────────────────────
        # Stop services
        # ─────────────────────────────────────────────────────────────────────
        
        logger.info("")
        if args.force:
            logger.info("Force stopping all containers...")
        else:
            logger.info(f"Gracefully stopping containers (timeout: {args.timeout}s)...")
        
        # docker compose stop preserves volumes
        compose_file = docker_dir / "docker-compose.yml"
        
        cmd = ["docker", "compose", "-f", str(compose_file), "stop"]
        if args.timeout:
            cmd.extend(["-t", str(args.timeout)])
        
        result = subprocess.run(cmd, cwd=docker_dir)
        
        # ─────────────────────────────────────────────────────────────────────
        # Display results
        # ─────────────────────────────────────────────────────────────────────
        
        if result.returncode == 0:
            logger.info("")
            logger.info("=" * 60)
            logger.info("✓ All services stopped successfully")
            logger.info("")
            logger.info("Data in volumes has been preserved.")
            logger.info("To remove containers completely: python scripts/cleanup.py")
            logger.info("To restart: python scripts/start_lab.py")
            logger.info("=" * 60)
            return 0
        else:
            logger.error("Failed to stop some services")
            return 1
    
    except KeyboardInterrupt:
        print("\nShutdown interrupted")
        return 130
    except Exception as e:
        logger.error(f"Failed to stop laboratory: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
