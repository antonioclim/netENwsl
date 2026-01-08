#!/usr/bin/env python3
"""
Week 12 Laboratory Launcher
NETWORKING class - ASE, Informatics | by Revolvix

Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment

This script starts all Docker containers and verifies the laboratory environment.

IMPORTANT: Portainer runs as a GLOBAL service on port 9000.
This script will NEVER start or stop Portainer.
"""

import argparse
import subprocess
import sys
import time
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger

logger = setup_logger("start_lab")

# Service definitions - Portainer is NOT included (runs globally on port 9000)
SERVICES = {
    "lab": {
        "container": "week12_lab",
        "ports": [1025, 6200, 6201, 6251],
        "health_check": None,
        "startup_time": 10
    }
}


def check_running_in_wsl() -> bool:
    """Check if we're running inside WSL."""
    if os.path.exists("/proc/sys/fs/binfmt_misc/WSLInterop"):
        return True
    if "WSL_DISTRO_NAME" in os.environ:
        return True
    try:
        with open("/proc/version", "r") as f:
            version = f.read().lower()
            return "microsoft" in version or "wsl" in version
    except (FileNotFoundError, IOError):
        pass
    return False


def check_docker_running() -> bool:
    """Verify Docker daemon is available."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def try_start_docker_service() -> bool:
    """Attempt to start Docker service in WSL."""
    logger.info("Docker not running. Attempting to start Docker service...")
    try:
        result = subprocess.run(
            ["sudo", "service", "docker", "start"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            logger.info("Docker service started successfully")
            time.sleep(2)
            return check_docker_running()
        else:
            logger.error(f"Failed to start Docker: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        logger.error("Timeout starting Docker service")
        return False
    except FileNotFoundError:
        logger.error("sudo not found")
        return False


def check_portainer_status() -> tuple:
    """Check Portainer container status."""
    try:
        result = subprocess.run(
            ["docker", "ps", "-a", "--filter", "name=portainer",
             "--format", "{{.Names}}\t{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            return False, "Could not check Portainer status"
        
        output = result.stdout.strip()
        if not output:
            return False, "Portainer container not found"
        
        for line in output.split("\n"):
            if "portainer" in line.lower():
                parts = line.split("\t")
                if len(parts) >= 2:
                    status = parts[1].lower()
                    if "up" in status:
                        return True, "Portainer is running"
                    else:
                        return False, f"Portainer is stopped: {parts[1]}"
        
        return False, "Portainer status unknown"
    except Exception as e:
        return False, f"Error checking Portainer: {e}"


def display_portainer_warning() -> None:
    """Display warning when Portainer is not running."""
    logger.warning("")
    logger.warning("=" * 60)
    logger.warning("\033[93mWARNING: Portainer is not running!\033[0m")
    logger.warning("To start Portainer: docker start portainer")
    logger.warning("=" * 60)


def print_banner() -> None:
    """Print startup banner."""
    print()
    print("=" * 65)
    print("  Week 12: Email Protocols and Remote Procedure Call")
    print("  SMTP, JSON-RPC, XML-RPC, gRPC")
    print("  NETWORKING class - ASE, Informatics")
    print("  WSL2 + Ubuntu 22.04 + Docker + Portainer")
    print("=" * 65)
    print()


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Start Week 12 Laboratory Environment (WSL2)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/start_lab.py              # Start all services
  python3 scripts/start_lab.py --status     # Check status only
  python3 scripts/start_lab.py --service smtp   # Start SMTP only
  python3 scripts/start_lab.py --rebuild    # Rebuild images first

Notes:
  - Portainer runs globally on port 9000 and is NOT managed by this script
  - Access Portainer at: http://localhost:9000
  - Credentials: stud / studstudstud
        """
    )
    parser.add_argument(
        "--status", "-s",
        action="store_true",
        help="Check status only, don't start services"
    )
    parser.add_argument(
        "--service",
        choices=["smtp", "jsonrpc", "xmlrpc", "grpc", "all"],
        default="all",
        help="Service to start (default: all)"
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
        help="Run containers in detached mode (default: True)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--no-portainer-check",
        action="store_true",
        help="Skip Portainer status check"
    )
    parser.add_argument(
        "--smtp-port",
        type=int,
        default=1025,
        help="SMTP server port (default: 1025)"
    )
    
    args = parser.parse_args()
    
    # Check if running in WSL
    if not check_running_in_wsl():
        logger.warning("Not running in WSL - some features may not work correctly")
    
    # Check Docker
    if not check_docker_running():
        if not try_start_docker_service():
            logger.error("")
            logger.error("Docker is not running and could not be started.")
            logger.error("Please start Docker manually: sudo service docker start")
            return 1
    
    try:
        docker = DockerManager(PROJECT_ROOT / "docker")
    except FileNotFoundError as e:
        logger.error(f"Docker configuration not found: {e}")
        return 1
    
    # Check Portainer status
    if not args.no_portainer_check:
        portainer_running, portainer_status = check_portainer_status()
        if not portainer_running:
            display_portainer_warning()
    
    if args.status:
        print_banner()
        logger.info("Checking service status...")
        docker.show_status(SERVICES)
        
        # Show Portainer status separately
        portainer_running, portainer_status = check_portainer_status()
        status_colour = "\033[92m" if portainer_running else "\033[91m"
        logger.info(f"  portainer (global): {status_colour}{portainer_status}\033[0m (port 9000)")
        return 0
    
    print_banner()
    
    try:
        # Build images if requested
        if args.rebuild:
            logger.info("Rebuilding Docker images...")
            if not docker.compose_build(no_cache=True):
                logger.error("Failed to build images")
                return 1
            logger.info("Images rebuilt successfully")
        
        # Start services (NOT Portainer)
        logger.info("Starting laboratory services...")
        logger.info("(Portainer runs globally and is not managed here)")
        
        if not docker.compose_up(detach=args.detach, build=not args.rebuild):
            logger.error("Failed to start services")
            return 1
        
        # Wait for services to initialise
        logger.info("Waiting for services to initialise...")
        time.sleep(12)
        
        # Verify services
        logger.info("Verifying services...")
        all_healthy = docker.verify_services(SERVICES)
        
        # Re-check Portainer
        portainer_running, _ = check_portainer_status()
        
        if all_healthy:
            print()
            print("=" * 65)
            print("  \033[92mLaboratory environment is ready!\033[0m")
            print("=" * 65)
            print()
            print("  Access points:")
            if portainer_running:
                print("    \033[92mPortainer:       http://localhost:9000\033[0m")
                print("    Credentials:     stud / studstudstud")
            else:
                print("    \033[93mPortainer:       NOT RUNNING\033[0m")
                print("    Start with:      docker start portainer")
            print()
            print("    SMTP Server:     localhost:1025")
            print("    JSON-RPC:        http://localhost:6200")
            print("    XML-RPC:         http://localhost:6201")
            print("    gRPC:            localhost:6251")
            print()
            print("  Quick start:")
            print("    nc localhost 1025                      # SMTP test")
            print("    curl -X POST http://localhost:6200 ... # JSON-RPC")
            print()
            print("=" * 65)
            return 0
        else:
            logger.error("Some services failed to start. Check logs:")
            logger.error("  docker compose -f docker/docker-compose.yml logs")
            return 1
    
    except KeyboardInterrupt:
        logger.info("Startup cancelled by user")
        return 130
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
