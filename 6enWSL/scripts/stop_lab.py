#!/usr/bin/env python3
"""
Week 6 Laboratory Shutdown
NETWORKING class - ASE, Informatics | by Revolvix

This script gracefully stops all Docker containers while preserving data.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger

logger = setup_logger("stop_lab")


def main() -> int:
    """Main entry point."""
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
    args = parser.parse_args()
    
    if args.verbose:
        from scripts.utils.logger import set_verbose
        set_verbose(logger, True)
    
    docker_dir = PROJECT_ROOT / "docker"
    
    try:
        docker = DockerManager(docker_dir)
    except FileNotFoundError as e:
        logger.error(f"Docker configuration not found: {e}")
        return 1
    
    logger.info("=" * 60)
    logger.info("Stopping Week 6 Laboratory Environment")
    logger.info("=" * 60)
    
    try:
        # Show current status
        logger.info("Current running services:")
        status = docker.compose_ps()
        for name, info in status.items():
            state = info.get("State", "unknown")
            logger.info(f"  {name}: {state}")
        
        if not status:
            logger.info("  No services running")
            return 0
        
        # Stop services
        logger.info("")
        if args.force:
            logger.info("Force stopping all containers...")
        else:
            logger.info(f"Gracefully stopping containers (timeout: {args.timeout}s)...")
        
        # docker compose stop preserves volumes
        import subprocess
        compose_file = docker_dir / "docker-compose.yml"
        
        cmd = ["docker", "compose", "-f", str(compose_file), "stop"]
        if args.timeout:
            cmd.extend(["-t", str(args.timeout)])
        
        result = subprocess.run(cmd, cwd=docker_dir)
        
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
