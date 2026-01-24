#!/usr/bin/env python3
"""
Week 13 Laboratory Launcher
===========================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment

This script starts all Docker containers and verifies the laboratory environment.

IMPORTANT: Portainer runs as a GLOBAL service on port 9000.
This script will NEVER start or stop Portainer.

SECURITY WARNING: This lab includes intentionally vulnerable services.
Do not expose to public networks.

USAGE:
    python3 scripts/start_lab.py              # Start all services
    python3 scripts/start_lab.py --status     # Check status only
    python3 scripts/start_lab.py --rebuild    # Rebuild images first
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT_DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import subprocess
import sys
import time
import os
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger

logger = setup_logger("start_lab")


# ═══════════════════════════════════════════════════════════════════════════════
# SERVICE_DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════════

# Service definitions - Portainer is NOT included (runs globally on port 9000)
SERVICES = {
    "mosquitto": {
        "container": "week13_mosquitto",
        "ports": [1883, 8883],
        "health_check": None,
        "startup_time": 10
    },
    "dvwa": {
        "container": "week13_dvwa",
        "ports": [8080],
        "health_check": None,
        "startup_time": 30
    },
    "vsftpd": {
        "container": "week13_vsftpd",
        "ports": [2121, 6200],
        "health_check": None,
        "startup_time": 10
    }
}


# ═══════════════════════════════════════════════════════════════════════════════
# ENVIRONMENT_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════

def check_running_in_wsl() -> bool:
    """
    Check if we're running inside WSL.
    
    💭 PREDICTION: What files/environment variables indicate WSL?
       (Answer: /proc/sys/fs/binfmt_misc/WSLInterop, WSL_DISTRO_NAME env var,
       or "microsoft" in /proc/version)
    
    Returns:
        True if running in WSL, False otherwise
    """
    # Check for WSL interop file
    if os.path.exists("/proc/sys/fs/binfmt_misc/WSLInterop"):
        return True
    
    # Check for WSL environment variable
    if "WSL_DISTRO_NAME" in os.environ:
        return True
    
    # Check /proc/version for Microsoft signature
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


# ═══════════════════════════════════════════════════════════════════════════════
# PORTAINER_STATUS_CHECK
# ═══════════════════════════════════════════════════════════════════════════════

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


# ═══════════════════════════════════════════════════════════════════════════════
# USER_INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def print_banner() -> None:
    """Print startup banner."""
    print()
    print("=" * 65)
    print("  Week 13: IoT and Security in Computer Networks")
    print("  MQTT, Port Scanning, Vulnerability Assessment")
    print("  Computer Networks — ASE, CSIE")
    print("  WSL2 + Ubuntu 22.04 + Docker + Portainer")
    print("=" * 65)
    print()
    print("  \033[93mSECURITY WARNING: This lab contains vulnerable services!\033[0m")
    print("  \033[93mDo not expose to public networks.\033[0m")
    print()


def print_success_message(portainer_running: bool) -> None:
    """Print success message with access points."""
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
    print("    DVWA:            http://localhost:8080 (admin/password)")
    print("    MQTT (plain):    localhost:1883")
    print("    MQTT (TLS):      localhost:8883")
    print("    FTP (vsftpd):    localhost:2121 (anonymous)")
    print("    Backdoor stub:   localhost:6200 (educational)")
    print()
    print("  Quick start:")
    print("    python3 src/exercises/ex_13_01_port_scanner.py --target 127.0.0.1 --ports 1-1024")
    print()
    print("  Pedagogical resources:")
    print("    docs/pair_programming_guide.md  - Collaboration guide")
    print("    docs/misconceptions.md          - Common errors to avoid")
    print("    docs/peer_instruction.md        - Self-assessment questions")
    print()
    print("=" * 65)


# ═══════════════════════════════════════════════════════════════════════════════
# ARGUMENT_PARSING
# ═══════════════════════════════════════════════════════════════════════════════

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Start Week 13 Laboratory Environment (WSL2)",
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
  - This lab contains VULNERABLE services for educational purposes only!
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
    
    return parser.parse_args()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point."""
    args = parse_arguments()
    
    # ─────────────────────────────────────────────────────────────────────────
    # VERIFY_WSL_ENVIRONMENT
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
    # CHECK_PORTAINER_STATUS
    # ─────────────────────────────────────────────────────────────────────────
    if not args.no_portainer_check:
        portainer_running, portainer_status = check_portainer_status()
        if not portainer_running:
            display_portainer_warning()
    
    # ─────────────────────────────────────────────────────────────────────────
    # STATUS_CHECK_MODE
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
        # BUILD_IMAGES (if requested)
        # ─────────────────────────────────────────────────────────────────────
        if args.rebuild:
            logger.info("Rebuilding Docker images...")
            if not docker.compose_build(no_cache=True):
                logger.error("Failed to build images")
                return 1
            logger.info("Images rebuilt successfully")
        
        # ─────────────────────────────────────────────────────────────────────
        # START_CONTAINERS
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
        time.sleep(15)
        
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
            print_success_message(portainer_running)
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
