#!/usr/bin/env python3
"""
Week 11 Laboratory Shutdown
NETWORKING class - ASE, Informatics | by Revolvix

This script gracefully stops all Docker containers.
"""
from __future__ import annotations

import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger, print_banner

logger = setup_logger("stop_lab")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stop Week 11 Laboratory Environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s              # Stop all services (preserve data)
  %(prog)s --logs       # Show logs before stopping
        """
    )
    parser.add_argument("--logs", action="store_true",
                        help="Show logs before stopping")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose output")
    
    args = parser.parse_args()
    
    docker_dir = PROJECT_ROOT / "docker"
    
    try:
        docker = DockerManager(docker_dir)
    except FileNotFoundError as e:
        logger.error(f"Docker configuration not found: {e}")
        return 1
    
    print_banner("Stopping Week 11 Laboratory")
    
    try:
        # Show logs if requested
        if args.logs:
            logger.info("Fetching logs...")
            logs = docker.get_logs(tail=50)
            print("\n--- Recent Logs ---")
            print(logs)
            print("--- End of Logs ---\n")
        
        # Stop containers
        logger.info("Stopping Docker Compose stack...")
        if docker.compose_down(volumes=False):
            logger.info("Laboratory environment stopped successfully")
            logger.info("Data volumes have been preserved")
            logger.info("")
            logger.info("To fully clean up, run: python scripts/cleanup.py --full")
            return 0
        else:
            logger.error("Failed to stop some services")
            return 1
    
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user")
        return 130
    
    except Exception as e:
        logger.error(f"Failed to stop laboratory: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())


# Revolvix&Hypotheticalandrei
