#!/usr/bin/env python3
"""
Week 1 Laboratory Shutdown
NETWORKING class - ASE, Informatics | by Revolvix

Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment

This script gracefully stops all laboratory containers while preserving data.

IMPORTANT: Portainer runs as a GLOBAL service on port 9000.
This script will NEVER stop Portainer - it must remain running for all weeks.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations
from typing import Optional, List, Dict, Tuple, Any

import subprocess
import sys
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger

logger = setup_logger("stop_lab")



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_portainer_status() -> tuple[bool, str]:
    """
    Check Portainer container status.
    
    Returns:
        Tuple of (is_running, status_message)
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
            return False, "Could not check Portainer status"
        
        output = result.stdout.strip()
        if not output:
            return False, "Portainer container not found"
        
        for line in output.split("\n"):
            if "portainer" in line.lower():
                parts = line.split("\t")
                if len(parts) >= 2:
                    return True, parts[1]
        
        return False, "Portainer status unknown"
        
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
        return False, f"Error: {e}"



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stop Week 1 Laboratory Environment (WSL2)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/stop_lab.py           # Stop lab containers gracefully
  python3 scripts/stop_lab.py --force   # Force stop immediately

Notes:
  - Portainer (port 9000) is NEVER stopped by this script
  - Portainer is a global service that should remain running
  - Use 'docker stop portainer' only if you specifically need to stop it
        """
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force stop containers immediately"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Timeout in seconds for graceful stop (default: 10)"
    )
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Stopping Week 1 Laboratory Environment")
    logger.info("(Portainer will NOT be stopped - it runs globally)")
    logger.info("=" * 60)

    docker_dir = PROJECT_ROOT / "docker"
    
    try:
        docker = DockerManager(docker_dir)
    except FileNotFoundError:
        logger.warning("docker-compose.yml not found, attempting direct stop...")
        # Try to stop lab container directly (but NEVER Portainer)
        try:
            if args.force:
                subprocess.run(["docker", "kill", "week1_lab"], capture_output=True)
            else:
                subprocess.run(
                    ["docker", "stop", "-t", str(args.timeout), "week1_lab"],
                    capture_output=True
                )
            logger.info("  Stopped week1_lab")
        except Exception:
            pass
        return 0

    try:
        logger.info("Stopping lab containers...")
        logger.info("(Portainer is preserved)")
        
        # Only stop lab service, NOT portainer
        if args.force:
            result = subprocess.run(
                ["docker", "compose", "-f", str(docker.compose_file), "kill"],
                cwd=docker_dir.parent,
                capture_output=True,
                text=True
            )
        else:
            result = subprocess.run(
                ["docker", "compose", "-f", str(docker.compose_file), 
                 "stop", "-t", str(args.timeout)],
                cwd=docker_dir.parent,
                capture_output=True,
                text=True
            )
        
        if result.returncode == 0:
            logger.info("\033[92mLab containers stopped.\033[0m")
        else:
            logger.warning(f"Stop command returned: {result.stderr}")
        
        # Verify lab containers are stopped
        logger.info("")
        logger.info("Verifying shutdown...")
        
        check_result = subprocess.run(
            ["docker", "ps", "--filter", "name=week1_", "--format", "{{.Names}}: {{.Status}}"],
            capture_output=True,
            text=True
        )
        
        running = check_result.stdout.strip()
        if running:
            logger.warning(f"Still running:\n{running}")
        else:
            logger.info("  All week1 containers stopped")
        
        # Confirm Portainer is still running
        portainer_running, portainer_status = check_portainer_status()
        if portainer_running:
            logger.info(f"  \033[92mPortainer still running:\033[0m {portainer_status}")
        else:
            logger.warning(f"  \033[93mPortainer not running:\033[0m {portainer_status}")
            logger.info("  To start Portainer: docker start portainer")
        
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
