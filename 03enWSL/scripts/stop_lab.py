#!/usr/bin/env python3
"""
Week 3 Laboratory Shutdown
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment

This script gracefully stops all laboratory containers while preserving data.

IMPORTANT: Portainer runs as a GLOBAL service on port 9000.
This script will NEVER stop Portainer - it must remain running for all weeks.
"""

# ════════════════════════════════════════════════════════════════════════════════
# IMPORTS AND CONFIGURATION
# ════════════════════════════════════════════════════════════════════════════════

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Tuple

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger

logger = setup_logger("stop_lab")


# ════════════════════════════════════════════════════════════════════════════════
# PORTAINER STATUS CHECK
# ════════════════════════════════════════════════════════════════════════════════

def check_portainer_status() -> Tuple[bool, str]:
    """Check Portainer container status."""
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


# ════════════════════════════════════════════════════════════════════════════════
# ARGUMENT PARSER
# ════════════════════════════════════════════════════════════════════════════════

def build_argument_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        description="Stop Week 3 Laboratory Environment (WSL2)",
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
    return parser


# ════════════════════════════════════════════════════════════════════════════════
# SHUTDOWN OPERATIONS
# ════════════════════════════════════════════════════════════════════════════════

def stop_containers_directly(force: bool, timeout: int) -> None:
    """Stop containers directly when compose file is not available."""
    containers = ["week3_client", "week3_router", "week3_server", "week3_receiver"]
    for container in containers:
        try:
            if force:
                subprocess.run(["docker", "kill", container], capture_output=True)
            else:
                subprocess.run(["docker", "stop", "-t", str(timeout), container],
                             capture_output=True)
            logger.info(f"  Stopped {container}")
        except Exception:
            pass


def verify_shutdown() -> bool:
    """Verify that all week3 containers have stopped."""
    check_result = subprocess.run(
        ["docker", "ps", "--filter", "name=week3_",
         "--format", "{{.Names}}: {{.Status}}"],
        capture_output=True,
        text=True
    )
    
    running = check_result.stdout.strip()
    if running:
        logger.warning(f"Still running:\n{running}")
        return False
    else:
        logger.info("  All week3 containers stopped")
        return True


def display_shutdown_summary(portainer_running: bool, portainer_status: str) -> None:
    """Display shutdown summary and next steps."""
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


# ════════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ════════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point."""
    parser = build_argument_parser()
    args = parser.parse_args()
    
    # ─────────────────────────────────────────────────────────────────────────
    # Step 1: Display banner
    # ─────────────────────────────────────────────────────────────────────────
    logger.info("=" * 60)
    logger.info("Stopping Week 3 Laboratory Environment")
    logger.info("(Portainer will NOT be stopped - it runs globally)")
    logger.info("=" * 60)
    
    # ─────────────────────────────────────────────────────────────────────────
    # Step 2: Initialise Docker manager
    # ─────────────────────────────────────────────────────────────────────────
    try:
        docker = DockerManager(PROJECT_ROOT / "docker")
    except FileNotFoundError:
        logger.warning("docker-compose.yml not found, attempting direct stop...")
        stop_containers_directly(args.force, args.timeout)
        return 0
    
    # ─────────────────────────────────────────────────────────────────────────
    # Step 3: Stop containers
    # ─────────────────────────────────────────────────────────────────────────
    try:
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
        # Step 4: Verify shutdown
        # ─────────────────────────────────────────────────────────────────────
        logger.info("")
        logger.info("Verifying shutdown...")
        verify_shutdown()
        
        # ─────────────────────────────────────────────────────────────────────
        # Step 5: Confirm Portainer status
        # ─────────────────────────────────────────────────────────────────────
        portainer_running, portainer_status = check_portainer_status()
        if portainer_running:
            logger.info(f"  \033[92mPortainer still running:\033[0m {portainer_status}")
        else:
            logger.warning(f"  \033[93mPortainer not running:\033[0m {portainer_status}")
            logger.info("  To start: docker start portainer")
        
        # ─────────────────────────────────────────────────────────────────────
        # Step 6: Display summary
        # ─────────────────────────────────────────────────────────────────────
        display_shutdown_summary(portainer_running, portainer_status)
        
        return 0
    
    except Exception as e:
        logger.error(f"Failed to stop laboratory: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
