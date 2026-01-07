#!/usr/bin/env python3
"""
Week 9 Laboratory Launcher
NETWORKING class - ASE, Informatics | by Revolvix

This script starts all Docker containers and verifies the laboratory environment
for the Session Layer (L5) and Presentation Layer (L6) exercises.

The laboratory includes:
- FTP server (pyftpdlib-based) for file transfer exercises
- Multiple client containers for concurrent testing
- Network configuration for traffic capture and analysis

Usage:
    python scripts/start_lab.py              # Start all services
    python scripts/start_lab.py --status     # Check status only
    python scripts/start_lab.py --rebuild    # Force rebuild images
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager, check_docker_running
from scripts.utils.network_utils import check_port, wait_for_port
from scripts.utils.logger import setup_logger, print_banner

logger = setup_logger("start_lab")

# =============================================================================
# Service Configuration
# =============================================================================

SERVICES = {
    "ftp-server": {
        "container": "s9_ftp_server",
        "port": 2121,
        "health_check": None,
        "startup_time": 5,
        "description": "FTP server (pyftpdlib)"
    },
    "client1": {
        "container": "s9_client1",
        "port": None,
        "health_check": None,
        "startup_time": 3,
        "description": "FTP client 1"
    },
    "client2": {
        "container": "s9_client2",
        "port": None,
        "health_check": None,
        "startup_time": 3,
        "description": "FTP client 2"
    }
}

# =============================================================================
# Main Functions
# =============================================================================

def verify_prerequisites() -> bool:
    """Check that all prerequisites are met."""
    logger.info("Verifying prerequisites...")
    
    # Check Docker
    if not check_docker_running():
        logger.error("Docker is not running. Please start Docker Desktop.")
        return False
    
    logger.info("Docker is running")
    
    # Check compose file exists
    compose_file = PROJECT_ROOT / "docker" / "docker-compose.yml"
    if not compose_file.exists():
        logger.error(f"Docker Compose file not found: {compose_file}")
        return False
    
    logger.info("Docker Compose file found")
    
    return True


def create_directories() -> None:
    """Create necessary directories for the lab."""
    dirs = [
        PROJECT_ROOT / "docker" / "server-files",
        PROJECT_ROOT / "docker" / "client1-files",
        PROJECT_ROOT / "docker" / "client2-files",
        PROJECT_ROOT / "pcap",
        PROJECT_ROOT / "artifacts"
    ]
    
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    
    # Create sample files for transfer testing
    server_files = PROJECT_ROOT / "docker" / "server-files"
    
    hello_file = server_files / "hello.txt"
    if not hello_file.exists():
        hello_file.write_text(
            "Hello from Week 9 FTP Laboratory!\n"
            "This file demonstrates file transfer protocols.\n"
            "NETWORKING class - ASE, Informatics\n"
        )
        logger.info(f"Created sample file: {hello_file}")
    
    binary_file = server_files / "sample.bin"
    if not binary_file.exists():
        import os
        binary_file.write_bytes(os.urandom(1024))
        logger.info(f"Created binary sample: {binary_file}")


def start_services(docker: DockerManager, rebuild: bool = False) -> bool:
    """Start all Docker services."""
    logger.info("Starting Docker containers...")
    
    if rebuild:
        logger.info("Rebuilding images (--rebuild flag set)...")
        if not docker.compose_build():
            return False
    
    if not docker.compose_up(detach=True):
        return False
    
    logger.info("Waiting for services to initialise...")
    time.sleep(3)
    
    return True


def verify_services() -> bool:
    """Verify all services are healthy."""
    all_healthy = True
    
    for name, svc in SERVICES.items():
        port = svc.get("port")
        
        if port:
            # Wait for port to be available
            if wait_for_port("localhost", port, timeout=15):
                logger.info(f"  [OK] {name} is listening on port {port}")
            else:
                logger.error(f"  [FAIL] {name} is not responding on port {port}")
                all_healthy = False
        else:
            logger.info(f"  [OK] {name} started (no port check)")
    
    return all_healthy


def show_access_info() -> None:
    """Display access information for the laboratory."""
    print()
    print("=" * 60)
    print("Week 9 Laboratory Environment is Ready!")
    print("=" * 60)
    print()
    print("Access Points:")
    print(f"  FTP Server:    localhost:2121")
    print(f"  FTP User:      test")
    print(f"  FTP Password:  12345")
    print()
    print("Portainer (if installed):")
    print(f"  URL:           https://localhost:9443")
    print()
    print("Quick Commands:")
    print("  python scripts/run_demo.py          # Run demonstration")
    print("  python scripts/capture_traffic.py   # Capture traffic")
    print("  python scripts/stop_lab.py          # Stop environment")
    print()
    print("Manual FTP Test:")
    print("  python src/exercises/ftp_demo_client.py \\")
    print("      --host localhost --port 2121 \\")
    print("      --user test --password 12345 list")
    print()
    print("=" * 60)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Start Week 9 Laboratory Environment",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--status", "-s",
        action="store_true",
        help="Check status only, don't start services"
    )
    parser.add_argument(
        "--rebuild", "-r",
        action="store_true",
        help="Force rebuild of Docker images"
    )
    parser.add_argument(
        "--detach", "-d",
        action="store_true",
        default=True,
        help="Run in detached mode (default: True)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Initialise Docker manager
    docker = DockerManager(PROJECT_ROOT / "docker")
    
    # Status check only
    if args.status:
        print_banner("Week 9 Laboratory Status")
        docker.show_status(SERVICES)
        return 0
    
    # Full startup
    print_banner("Week 9 Laboratory Launcher")
    
    try:
        # Step 1: Verify prerequisites
        if not verify_prerequisites():
            return 1
        
        # Step 2: Create directories
        create_directories()
        
        # Step 3: Start services
        if not start_services(docker, rebuild=args.rebuild):
            logger.error("Failed to start services")
            return 1
        
        # Step 4: Verify services
        print()
        logger.info("Verifying services...")
        if not verify_services():
            logger.warning("Some services may not be fully operational")
            logger.info("Check logs with: docker compose -f docker/docker-compose.yml logs")
        
        # Step 5: Show access information
        show_access_info()
        
        return 0
        
    except KeyboardInterrupt:
        logger.warning("\nInterrupted by user")
        return 130
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
