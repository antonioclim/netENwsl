#!/usr/bin/env python3
"""
Week 4 Laboratory Shutdown
NETWORKING class - ASE, Informatics | by Revolvix

This script gracefully stops all Docker containers and services.
"""

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


def stop_native_processes():
    """Stop any natively running server processes."""
    import signal
    import os
    
    # Find Python processes running our servers
    try:
        result = subprocess.run(
            ["pgrep", "-f", "proto_server.py|sensor_server.py"],
            capture_output=True,
            text=True
        )
        
        pids = result.stdout.strip().split()
        
        for pid in pids:
            if pid:
                try:
                    os.kill(int(pid), signal.SIGTERM)
                    logger.info(f"Stopped process {pid}")
                except (ProcessLookupError, PermissionError) as e:
                    logger.warning(f"Could not stop process {pid}: {e}")
    
    except FileNotFoundError:
        # pgrep not available, try alternative
        logger.debug("pgrep not available, skipping native process check")


def main():
    parser = argparse.ArgumentParser(
        description="Stop Week 4 Laboratory Environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python stop_lab.py           # Stop all services
  python stop_lab.py --native  # Stop native processes only
  python stop_lab.py --force   # Force stop (kill containers)
        """
    )
    
    parser.add_argument("--native", action="store_true",
                        help="Stop native processes only (no Docker)")
    parser.add_argument("--force", "-f", action="store_true",
                        help="Force stop containers")
    parser.add_argument("--timeout", "-t", type=int, default=30,
                        help="Timeout for graceful shutdown (default: 30s)")
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("Stopping Week 4 Laboratory Environment")
    logger.info("=" * 60)
    
    # Stop native processes
    if args.native:
        stop_native_processes()
        logger.info("Native processes stopped")
        return 0
    
    # Stop Docker services
    docker_dir = PROJECT_ROOT / "docker"
    
    try:
        docker = DockerManager(docker_dir)
        
        logger.info("Stopping Docker Compose services...")
        
        if args.force:
            # Force kill containers
            result = subprocess.run(
                ["docker", "compose", "-f", str(docker_dir / "docker-compose.yml"),
                 "kill"],
                capture_output=True
            )
        else:
            # Graceful shutdown
            result = subprocess.run(
                ["docker", "compose", "-f", str(docker_dir / "docker-compose.yml"),
                 "stop", "-t", str(args.timeout)],
                capture_output=True
            )
        
        if result.returncode == 0:
            logger.info("Services stopped successfully")
        else:
            logger.warning("Some services may not have stopped cleanly")
        
        # Also stop any native processes
        stop_native_processes()
        
        # Show final status
        logger.info("")
        logger.info("Verifying shutdown...")
        
        status = docker.compose_ps()
        if "running" not in status.lower():
            logger.info("All services stopped")
        else:
            logger.warning("Some containers still running:")
            print(status)
        
        logger.info("")
        logger.info("=" * 60)
        logger.info("Laboratory environment stopped")
        logger.info("")
        logger.info("To fully clean up, run: python scripts/cleanup.py --full")
        logger.info("=" * 60)
        
        return 0
    
    except FileNotFoundError as e:
        logger.error(f"Configuration error: {e}")
        # Still try to stop native processes
        stop_native_processes()
        return 1
    except Exception as e:
        logger.error(f"Failed to stop laboratory: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
