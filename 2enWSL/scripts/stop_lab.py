#!/usr/bin/env python3
"""
Week 2 Laboratory Shutdown
NETWORKING class - ASE, Informatics | by Revolvix

This script gracefully stops all Docker containers while preserving data.
"""

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
        description="Stop Week 2 Laboratory Environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/stop_lab.py           # Stop all services
  python scripts/stop_lab.py --force   # Force stop (kill)
        """
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force stop containers (kill instead of stop)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    print()
    print("=" * 60)
    print("  Stopping Week 2 Laboratory Environment")
    print("=" * 60)
    print()
    
    try:
        docker = DockerManager(PROJECT_ROOT / "docker")
    except FileNotFoundError as e:
        logger.error(f"Docker configuration not found: {e}")
        return 1
    
    try:
        logger.info("Stopping containers...")
        
        if docker.compose_down(volumes=False):
            logger.info("All containers stopped successfully")
            print()
            print("Data has been preserved. To fully cleanup, run:")
            print("  python scripts/cleanup.py --full")
            print()
            return 0
        else:
            logger.error("Failed to stop some containers")
            return 1
    
    except KeyboardInterrupt:
        logger.info("Shutdown cancelled by user")
        return 130
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
