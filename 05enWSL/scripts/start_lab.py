#!/usr/bin/env python3
"""
Week 5 Laboratory Launcher
==========================
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment

This script starts all Docker containers and verifies the laboratory environment.

IMPORTANT: Portainer runs as a GLOBAL service on port 9000.
This script will NEVER start or stop Portainer.

Learning Objectives:
    - Understand container orchestration startup sequences
    - Verify service health in containerised environments

Pair Programming Notes:
    - Driver: Execute the start commands
    - Navigator: Monitor Portainer dashboard for container status
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import subprocess
import sys
import time
import os
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURE_MODULE_PATH
# ═══════════════════════════════════════════════════════════════════════════════
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT_UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════
from scripts.utils.docker_utils import DockerManager
from scripts.utils.network_utils import NetworkUtils
from scripts.utils.logger import setup_logger

logger = setup_logger("start_lab")

# ═══════════════════════════════════════════════════════════════════════════════
# DEFINE_SERVICE_CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
# Service definitions - Portainer is NOT included (runs globally on port 9000)
SERVICES = {
    "python": {
        "container": "week5_python",
        "port": None,
        "health_check": None,
        "startup_time": 3
    },
    "udp-server": {
        "container": "week5_udp-server",
        "port": 9999,
        "health_check": None,
        "startup_time": 3
    },
    "udp-client": {
        "container": "week5_udp-client",
        "port": None,
        "health_check": None,
        "startup_time": 5
    }
}


# ═══════════════════════════════════════════════════════════════════════════════
# CHECK_WSL_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
def check_running_in_wsl() -> bool:
    """
    Check if we're running inside WSL.
    
    Returns:
        True if running in WSL, False otherwise
    """
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


# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_DOCKER_DAEMON
# ═══════════════════════════════════════════════════════════════════════════════
def check_docker_running() -> bool:
    """
    Verify Docker daemon is available.
    
    Returns:
        True if Docker is running, False otherwise
    """
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
    """
    Attempt to start Docker service in WSL.
    
    Returns:
        True if Docker started successfully, False otherwise
    """
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


# ═══════════════════════════════════════════════════════════════════════════════
# CHECK_PORTAINER_STATUS
# ═══════════════════════════════════════════════════════════════════════════════
def check_portainer_status() -> tuple:
    """
    Check Portainer container status.
    
    Returns:
        Tuple of (is_running: bool, status_message: str)
    """
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


# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY_BANNER
# ═══════════════════════════════════════════════════════════════════════════════
def print_banner() -> None:
    """Print startup banner."""
    print()
    print("=" * 60)
    print("  Week 5: Network Layer – IP Addressing, Subnetting, VLSM")
    print("  CIDR, FLSM, VLSM, and IPv6 Operations")
    print("  NETWORKING class - ASE, Informatics")
    print("  WSL2 + Ubuntu 22.04 + Docker + Portainer")
    print("=" * 60)
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD_ARGUMENT_PARSER
# ═══════════════════════════════════════════════════════════════════════════════
def build_parser() -> argparse.ArgumentParser:
    """
    Build the command-line argument parser.
    
    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description="Start Week 5 Laboratory Environment (WSL2)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/start_lab.py              # Start all services
  python3 scripts/start_lab.py --status     # Check status only
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
    
    return parser


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """
    Main entry point for the laboratory launcher.
    
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    parser = build_parser()
    args = parser.parse_args()
    
    # ─────────────────────────────────────────────────────────────────────────
    # VERIFY_ENVIRONMENT
    # ─────────────────────────────────────────────────────────────────────────
    if not check_running_in_wsl():
        logger.warning("Not running in WSL - some features may not work correctly")
    
    # ─────────────────────────────────────────────────────────────────────────
    # VERIFY_DOCKER_AVAILABILITY
    # ─────────────────────────────────────────────────────────────────────────
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
    
    # ─────────────────────────────────────────────────────────────────────────
    # CHECK_PORTAINER
    # ─────────────────────────────────────────────────────────────────────────
    if not args.no_portainer_check:
        portainer_running, portainer_status = check_portainer_status()
        if not portainer_running:
            display_portainer_warning()
    
    # ─────────────────────────────────────────────────────────────────────────
    # HANDLE_STATUS_MODE
    # ─────────────────────────────────────────────────────────────────────────
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
        # ─────────────────────────────────────────────────────────────────────
        # BUILD_IMAGES
        # ─────────────────────────────────────────────────────────────────────
        if args.rebuild:
            logger.info("Rebuilding Docker images...")
            if not docker.compose_build(no_cache=True):
                logger.error("Failed to build images")
                return 1
            logger.info("Images rebuilt successfully")
        
        # ─────────────────────────────────────────────────────────────────────
        # START_SERVICES
        # ─────────────────────────────────────────────────────────────────────
        logger.info("Starting laboratory services...")
        logger.info("(Portainer runs globally and is not managed here)")
        
        if not docker.compose_up(detach=args.detach, build=not args.rebuild):
            logger.error("Failed to start services")
            return 1
        
        # ─────────────────────────────────────────────────────────────────────
        # WAIT_FOR_INITIALISATION
        # ─────────────────────────────────────────────────────────────────────
        logger.info("Waiting for services to initialise...")
        time.sleep(5)
        
        # ─────────────────────────────────────────────────────────────────────
        # VERIFY_SERVICES
        # ─────────────────────────────────────────────────────────────────────
        logger.info("Verifying services...")
        all_healthy = docker.verify_services(SERVICES)
        
        # Re-check Portainer
        portainer_running, _ = check_portainer_status()
        
        # ─────────────────────────────────────────────────────────────────────
        # DISPLAY_RESULTS
        # ─────────────────────────────────────────────────────────────────────
        if all_healthy:
            print()
            print("=" * 60)
            print("  \033[92mLaboratory environment is ready!\033[0m")
            print("=" * 60)
            print()
            print("  Access points:")
            if portainer_running:
                print("    \033[92mPortainer:    http://localhost:9000\033[0m")
                print("    Credentials:  stud / studstudstud")
            else:
                print("    \033[93mPortainer:    NOT RUNNING\033[0m")
                print("    Start with:   docker start portainer")
            print()
            print("    UDP Echo Server: localhost:9999/udp")
            print()
            print("  Quick start:")
            print("    docker exec -it week5_python bash")
            print("    python /app/src/exercises/ex_5_01_cidr_flsm.py analyse 192.168.10.14/26")
            print("    python /app/src/exercises/ex_5_02_vlsm_ipv6.py vlsm 172.16.0.0/24 60 20 10 2")
            print()
            print("=" * 60)
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
