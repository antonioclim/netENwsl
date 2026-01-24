#!/usr/bin/env python3
"""
Week 13 Laboratory Shutdown
===========================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment

This script gracefully stops all laboratory containers while preserving data.

IMPORTANT: Portainer runs as a GLOBAL service on port 9000.
This script will NEVER stop Portainer - it must remain running for all weeks.

USAGE:
    python3 scripts/stop_lab.py           # Stop lab containers
    python3 scripts/stop_lab.py --force   # Force stop immediately
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT_DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger

logger = setup_logger("stop_lab")


# ═══════════════════════════════════════════════════════════════════════════════
# PORTAINER_STATUS_CHECK
# ═══════════════════════════════════════════════════════════════════════════════

def check_portainer_status() -> tuple:
    """
    Check Portainer container status.
    
    💭 PREDICTION: Why do we check Portainer status in the stop script?
       (Answer: To confirm Portainer is still running after we stop lab containers,
       since Portainer should remain available for other weeks)
    
    Returns:
        Tuple of (is_running: bool, status_message: str)
    """
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=portainer",
             "--format", "{{.Names}}\t{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            return False, "Could not check status"
        
        output = result.stdout.strip()
        if not output:
            return False, "Not found"
        
        for line in output.split("\n"):
            if "portainer" in line.lower():
                parts = line.split("\t")
                if len(parts) >= 2:
                    return True, parts[1]
        
        return False, "Unknown"
    except Exception as e:
        return False, f"Error: {e}"


# ═══════════════════════════════════════════════════════════════════════════════
# DIRECT_CONTAINER_STOP
# ═══════════════════════════════════════════════════════════════════════════════

def stop_containers_directly(force: bool, timeout: int) -> None:
    """
    Stop containers directly without docker-compose.
    
    This is a fallback when docker-compose.yml is not found.
    
    Args:
        force: If True, use docker kill instead of docker stop
        timeout: Timeout for graceful stop (ignored if force=True)
    """
    containers = ["week13_mosquitto", "week13_dvwa", "week13_vsftpd"]
    
    for container in containers:
        try:
            if force:
                subprocess.run(
                    ["docker", "kill", container],
                    capture_output=True
                )
            else:
                subprocess.run(
                    ["docker", "stop", "-t", str(timeout), container],
                    capture_output=True
                )
            logger.info(f"  Stopped {container}")
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Stop Week 13 Laboratory Environment (WSL2)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/stop_lab.py           # Stop lab containers
  python3 scripts/stop_lab.py --force   # Force stop immediately

Notes:
  - Portainer (port 9000) is NEVER stopped by this script
  - Portainer is a global service that should remain running
        """
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force stop containers immediately"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=10,
        help="Timeout for graceful stop (default: 10s)"
    )
    
    args = parser.parse_args()
    
    # ─────────────────────────────────────────────────────────────────────────
    # DISPLAY_BANNER
    # ─────────────────────────────────────────────────────────────────────────
    logger.info("=" * 60)
    logger.info("Stopping Week 13 Laboratory Environment")
    logger.info("(Portainer will NOT be stopped - it runs globally)")
    logger.info("=" * 60)
    
    # ─────────────────────────────────────────────────────────────────────────
    # INITIALISE_DOCKER_MANAGER
    # ─────────────────────────────────────────────────────────────────────────
    try:
        docker = DockerManager(PROJECT_ROOT / "docker")
    except FileNotFoundError:
        logger.warning("docker-compose.yml not found, attempting direct stop...")
        stop_containers_directly(args.force, args.timeout)
        return 0
    
    try:
        # ─────────────────────────────────────────────────────────────────────
        # STOP_CONTAINERS
        # ─────────────────────────────────────────────────────────────────────
        logger.info("Stopping lab containers...")
        
        if args.force:
            result = subprocess.run(
                ["docker", "compose", "-f", str(docker.compose_file), "kill"],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True
            )
        else:
            result = subprocess.run(
                ["docker", "compose", "-f", str(docker.compose_file),
                 "stop", "-t", str(args.timeout)],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True
            )
        
        if result.returncode == 0:
            logger.info("\033[92mLab containers stopped.\033[0m")
        else:
            logger.warning(f"Stop command output: {result.stderr}")
        
        # ─────────────────────────────────────────────────────────────────────
        # VERIFY_SHUTDOWN
        # ─────────────────────────────────────────────────────────────────────
        logger.info("")
        logger.info("Verifying shutdown...")
        
        check_result = subprocess.run(
            ["docker", "ps", "--filter", "name=week13_",
             "--format", "{{.Names}}: {{.Status}}"],
            capture_output=True,
            text=True
        )
        
        running = check_result.stdout.strip()
        if running:
            logger.warning(f"Still running:\n{running}")
        else:
            logger.info("  All week13 containers stopped")
        
        # ─────────────────────────────────────────────────────────────────────
        # CONFIRM_PORTAINER_STATUS
        # ─────────────────────────────────────────────────────────────────────
        portainer_running, portainer_status = check_portainer_status()
        if portainer_running:
            logger.info(f"  \033[92mPortainer still running:\033[0m {portainer_status}")
        else:
            logger.warning(f"  \033[93mPortainer not running:\033[0m {portainer_status}")
            logger.info("  To start: docker start portainer")
        
        # ─────────────────────────────────────────────────────────────────────
        # DISPLAY_SUMMARY
        # ─────────────────────────────────────────────────────────────────────
        logger.info("")
        logger.info("=" * 60)
        logger.info("Shutdown complete.")
        logger.info("")
        logger.info("Data preserved in:")
        logger.info(f"  Artifacts: {PROJECT_ROOT / 'artifacts'}")
        logger.info(f"  Captures:  {PROJECT_ROOT / 'pcap'}")
        logger.info("")
        logger.info("To restart: python3 scripts/start_lab.py")
        if portainer_running:
            logger.info("Portainer:  http://localhost:9000 (still available)")
        logger.info("=" * 60)
        
        return 0
    
    except Exception as e:
        logger.error(f"Failed to stop laboratory: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
