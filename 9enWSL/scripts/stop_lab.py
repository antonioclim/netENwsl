#!/usr/bin/env python3
"""
Week 9 Laboratory Shutdown
NETWORKING class - ASE, Informatics | by Revolvix

This script gracefully stops all Docker containers used in the laboratory.
Data in mounted volumes is preserved for later sessions.

Usage:
    python scripts/stop_lab.py           # Graceful shutdown
    python scripts/stop_lab.py --force   # Force stop if graceful fails
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger, print_banner

logger = setup_logger("stop_lab")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stop Week 9 Laboratory Environment",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force stop containers without graceful shutdown"
    )
    parser.add_argument(
        "--remove-volumes", "-v",
        action="store_true",
        help="Also remove volumes (deletes data)"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=10,
        help="Timeout for graceful shutdown (default: 10s)"
    )
    
    args = parser.parse_args()
    
    print_banner("Week 9 Laboratory Shutdown")
    
    docker = DockerManager(PROJECT_ROOT / "docker")
    
    try:
        logger.info("Stopping containers...")
        
        if args.remove_volumes:
            logger.warning("Volumes will be removed (data will be lost)")
        
        success = docker.compose_down(
            volumes=args.remove_volumes,
            remove_orphans=True
        )
        
        if success:
            logger.info("All containers stopped successfully")
            
            print()
            print("=" * 50)
            print("Laboratory environment stopped")
            
            if args.remove_volumes:
                print("Volumes have been removed")
            else:
                print("Data has been preserved in mounted volumes")
            
            print()
            print("To restart: python scripts/start_lab.py")
            print("=" * 50)
            
            return 0
        else:
            logger.error("Failed to stop some containers")
            return 1
            
    except KeyboardInterrupt:
        logger.warning("\nInterrupted by user")
        return 130
    
    except Exception as e:
        logger.error(f"Shutdown failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
