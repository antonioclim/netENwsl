#!/usr/bin/env python3
"""
Week 1 Laboratory Shutdown Script
NETWORKING class - ASE, Informatics | by Revolvix

This script stops all Week 1 lab containers while preserving data volumes.

ADAPTED FOR: WSL2 + Ubuntu 22.04 + Docker (in WSL) + Portainer Global
NOTE: Portainer is NOT stopped by this script - it runs globally on port 9000
"""

from __future__ import annotations

import subprocess
import sys
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger

logger = setup_logger("stop_lab")


def check_portainer_running() -> bool:
    """Check if global Portainer is running."""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=portainer", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return "portainer" in result.stdout.lower()
    except:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stop Week 1 Laboratory Environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/stop_lab.py              # Stop lab containers
  python scripts/stop_lab.py --remove     # Stop and remove containers
  python scripts/stop_lab.py --volumes    # Also remove volumes (data loss!)

NOTE: Portainer runs globally and is NOT stopped by this script.
      It remains accessible at http://localhost:9000
        """
    )
    parser.add_argument(
        "--remove",
        action="store_true",
        help="Remove containers after stopping"
    )
    parser.add_argument(
        "--volumes",
        action="store_true",
        help="Also remove volumes (WARNING: data loss!)"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force stop without confirmation"
    )
    args = parser.parse_args()

    docker_dir = PROJECT_ROOT / "docker"
    
    try:
        docker = DockerManager(docker_dir)
    except FileNotFoundError as e:
        logger.error(str(e))
        return 1

    logger.info("=" * 60)
    logger.info("Stopping Week 1 Laboratory Environment")
    logger.info("NETWORKING class - ASE, Informatics | by Revolvix")
    logger.info("=" * 60)

    try:
        # Confirm volume removal if requested
        if args.volumes and not args.force:
            response = input("\n⚠️  WARNING: This will delete all lab data! Continue? [y/N]: ")
            if response.lower() != 'y':
                logger.info("Cancelled.")
                return 0

        # Stop containers
        logger.info("Stopping lab containers...")
        
        if args.remove or args.volumes:
            # Use docker-compose down
            cmd = ["docker-compose", "-f", str(docker.compose_file), "down"]
            if args.volumes:
                cmd.append("-v")
            
            result = subprocess.run(
                cmd,
                cwd=docker_dir.parent,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                logger.error(f"Failed to stop containers: {result.stderr}")
                return 1
        else:
            # Just stop containers (preserve volumes)
            if not docker.compose_stop():
                logger.error("Failed to stop containers")
                return 1

        logger.info("")
        logger.info("\033[92mLab containers stopped successfully.\033[0m")
        
        # Remind about Portainer
        logger.info("")
        logger.info("=" * 60)
        logger.info("NOTE: Portainer is still running (global service)")
        if check_portainer_running():
            logger.info("  Status: \033[92mRUNNING\033[0m at http://localhost:9000")
        else:
            logger.warning("  Status: \033[91mNOT RUNNING\033[0m")
        logger.info("")
        logger.info("Portainer is intentionally NOT stopped to remain")
        logger.info("available for other laboratory sessions.")
        logger.info("=" * 60)
        
        return 0

    except Exception as e:
        logger.error(f"Failed to stop laboratory: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
