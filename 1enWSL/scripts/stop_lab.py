#!/usr/bin/env python3
"""
Week 1 Laboratory Shutdown
NETWORKING class - ASE, Informatics | by Revolvix

This script gracefully stops all laboratory containers while preserving data.
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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stop Week 1 Laboratory Environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/stop_lab.py           # Stop all containers
  python scripts/stop_lab.py --force   # Force stop immediately
        """
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force stop containers immediately"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Timeout in seconds for graceful stop (default: 10)"
    )
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Stopping Week 1 Laboratory Environment")
    logger.info("=" * 60)

    docker_dir = PROJECT_ROOT / "docker"
    
    try:
        docker = DockerManager(docker_dir)
    except FileNotFoundError:
        logger.warning("docker-compose.yml not found, attempting direct stop...")
        # Try to stop containers directly
        containers = ["week1_lab", "week1_portainer"]
        for container in containers:
            try:
                if args.force:
                    subprocess.run(["docker", "kill", container], capture_output=True)
                else:
                    subprocess.run(
                        ["docker", "stop", "-t", str(args.timeout), container],
                        capture_output=True
                    )
                logger.info(f"  Stopped {container}")
            except Exception:
                pass
        return 0

    try:
        logger.info("Stopping containers...")
        
        if args.force:
            # Force stop
            result = subprocess.run(
                ["docker", "compose", "-f", str(docker.compose_file),
                 "--profile", "management", "kill"],
                cwd=docker_dir.parent,
                capture_output=True,
                text=True
            )
        else:
            # Graceful stop
            result = subprocess.run(
                ["docker", "compose", "-f", str(docker.compose_file),
                 "--profile", "management", "stop", "-t", str(args.timeout)],
                cwd=docker_dir.parent,
                capture_output=True,
                text=True
            )
        
        if result.returncode == 0:
            logger.info("\033[92mAll containers stopped.\033[0m")
        else:
            logger.warning(f"Stop command returned: {result.stderr}")
        
        # Verify containers are stopped
        logger.info("")
        logger.info("Verifying shutdown...")
        
        check_result = subprocess.run(
            ["docker", "ps", "--filter", "name=week1_", "--format", "{{.Names}}: {{.Status}}"],
            capture_output=True,
            text=True
        )
        
        running = check_result.stdout.strip()
        if running:
            logger.warning(f"Still running:\n{running}")
        else:
            logger.info("  All week1 containers stopped")
        
        logger.info("")
        logger.info("=" * 60)
        logger.info("Shutdown complete.")
        logger.info("")
        logger.info("Data preserved in:")
        logger.info(f"  Artifacts: {PROJECT_ROOT / 'artifacts'}")
        logger.info(f"  Captures:  {PROJECT_ROOT / 'pcap'}")
        logger.info("")
        logger.info("To restart: python scripts/start_lab.py")
        logger.info("=" * 60)
        
        return 0

    except Exception as e:
        logger.error(f"Failed to stop laboratory: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
