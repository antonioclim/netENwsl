#!/usr/bin/env python3
"""
Week 8 Laboratory Shutdown
NETWORKING class - ASE, Informatics | by Revolvix

This script gracefully stops all laboratory containers.
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger, print_banner

logger = setup_logger("stop_lab")


def main():
    parser = argparse.ArgumentParser(
        description="Stop Week 8 Laboratory Environment"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=10,
        help="Timeout in seconds for container shutdown (default: 10)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show verbose output"
    )
    
    args = parser.parse_args()
    
    print_banner(
        "Stopping Week 8 Laboratory",
        "Transport Layer: HTTP Server and Reverse Proxies"
    )
    
    try:
        docker = DockerManager(PROJECT_ROOT / "docker")
        
        # Show current status
        logger.info("Current container status:")
        status = docker.get_container_status()
        
        if not status:
            logger.info("  No containers are running.")
            return 0
        
        for name, info in status.items():
            state = info.get("state", "unknown")
            logger.info(f"  {name}: {state}")
        
        # Stop containers
        logger.info("\nStopping containers...")
        
        if docker.compose_down(volumes=False):
            logger.info("\n✓ All containers stopped successfully")
            logger.info("  Data and volumes are preserved.")
            logger.info("  Run 'python scripts/cleanup.py --full' to remove everything.")
            return 0
        else:
            logger.error("Failed to stop some containers")
            return 1
            
    except FileNotFoundError as e:
        logger.error(f"Compose file not found: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
