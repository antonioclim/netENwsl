#!/usr/bin/env python3
"""
Week 6 Laboratory Launcher
NETWORKING class - ASE, Informatics | by Revolvix

This script starts all Docker containers and verifies the laboratory environment
for NAT/PAT and SDN exercises.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger, ProgressLogger

logger = setup_logger("start_lab")

# Service definitions for Week 6
SERVICES = {
    "week6-lab": {
        "container": "week6_lab",
        "port": None,  # No exposed port (uses host networking)
        "health_check": None,
        "startup_time": 10,
        "description": "Main laboratory environment with Mininet"
    },
}

# Optional services (activated with profiles)
OPTIONAL_SERVICES = {
    "sdn-controller": {
        "container": "week6_controller",
        "port": 6633,
        "health_check": None,
        "startup_time": 5,
        "description": "SDN Controller (OS-Ken)",
        "profile": "controller"
    },
    "portainer": {
        "container": "week6_portainer",
        "port": 9443,
        "health_check": None,
        "startup_time": 15,
        "description": "Container management dashboard",
        "profile": "management"
    },
}


def print_banner():
    """Print startup banner."""
    print()
    print("=" * 60)
    print("  Week 6: NAT/PAT & SDN Laboratory")
    print("  NETWORKING class - ASE, Informatics | by Revolvix")
    print("=" * 60)
    print()


def print_access_info(services_started: dict):
    """Print access information for started services."""
    print()
    print("Access Points:")
    print("-" * 60)
    
    if "week6-lab" in services_started:
        print("  Main Lab:     docker exec -it week6_lab bash")
        print("                (or use docker compose run --rm week6-lab)")
    
    if "sdn-controller" in services_started:
        print("  Controller:   localhost:6633 (OpenFlow)")
    
    if "portainer" in services_started:
        print("  Portainer:    https://localhost:9443")
    
    print("-" * 60)
    print()
    print("Quick Start Commands (inside container):")
    print("  make nat-demo    - Start NAT topology")
    print("  make sdn-demo    - Start SDN topology")
    print("  make check       - Verify dependencies")
    print("  make clean       - Cleanup Mininet")
    print()


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Start Week 6 Laboratory Environment"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Check status only, don't start services"
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Force rebuild Docker images"
    )
    parser.add_argument(
        "--controller",
        action="store_true",
        help="Also start the SDN controller"
    )
    parser.add_argument(
        "--portainer",
        action="store_true",
        help="Also start Portainer management interface"
    )
    parser.add_argument(
        "--detach", "-d",
        action="store_true",
        default=False,
        help="Run containers in detached mode"
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
    
    # Locate docker-compose.yml
    docker_dir = PROJECT_ROOT / "docker"
    
    try:
        docker = DockerManager(docker_dir)
    except FileNotFoundError as e:
        logger.error(f"Docker configuration not found: {e}")
        return 1
    
    # Status check only
    if args.status:
        print_banner()
        all_services = {**SERVICES, **OPTIONAL_SERVICES}
        docker.show_status(all_services)
        return 0
    
    print_banner()
    
    # Determine which profiles to activate
    profiles = []
    services_to_start = dict(SERVICES)
    
    if args.controller:
        profiles.append("controller")
        services_to_start["sdn-controller"] = OPTIONAL_SERVICES["sdn-controller"]
    
    if args.portainer:
        profiles.append("management")
        services_to_start["portainer"] = OPTIONAL_SERVICES["portainer"]
    
    try:
        with ProgressLogger(logger, "Starting laboratory environment", 4) as progress:
            # Step 1: Build images
            if args.rebuild:
                progress.step("Building Docker images (--rebuild specified)")
                if not docker.compose_build(no_cache=args.rebuild):
                    logger.error("Failed to build Docker images")
                    return 1
            else:
                progress.step("Checking Docker images")
                docker.compose_build()  # Build if not exists
            
            # Step 2: Start services
            progress.step("Starting Docker containers")
            if not docker.compose_up(detach=args.detach or True, profiles=profiles if profiles else None):
                logger.error("Failed to start services")
                return 1
            
            # Step 3: Wait for startup
            progress.step("Waiting for services to initialise")
            time.sleep(5)
            
            # Step 4: Verify services
            progress.step("Verifying services")
            all_healthy = docker.verify_services(services_to_start)
        
        if all_healthy:
            print()
            print("=" * 60)
            print("  ✓ Laboratory environment is ready!")
            print("=" * 60)
            print_access_info(services_to_start)
            
            if not args.detach:
                print("Note: Run with -d/--detach to run in background")
            
            return 0
        else:
            logger.warning("Some services may not be fully ready")
            logger.info("Check logs with: docker compose -f docker/docker-compose.yml logs")
            return 1
    
    except KeyboardInterrupt:
        print("\nStartup interrupted")
        return 130
    except Exception as e:
        logger.error(f"Failed to start laboratory: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
