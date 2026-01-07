#!/usr/bin/env python3
"""
Week 10 Laboratory Launcher
NETWORKING class - ASE, Informatics | by Revolvix

This script starts all Docker containers and verifies the laboratory environment.
"""

import subprocess
import sys
import time
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.network_utils import NetworkTester, wait_for_service
from scripts.utils.logger import setup_logger

logger = setup_logger("start_lab")

SERVICES = {
    "web": {
        "container": "week10_web",
        "port": 8000,
        "health_check": "http://localhost:8000/",
        "startup_time": 5
    },
    "dns-server": {
        "container": "week10_dns",
        "port": 5353,
        "health_check": None,  # UDP service
        "startup_time": 3
    },
    "ssh-server": {
        "container": "week10_ssh",
        "port": 2222,
        "health_check": None,
        "startup_time": 5
    },
    "ftp-server": {
        "container": "week10_ftp",
        "port": 2121,
        "health_check": None,
        "startup_time": 3
    },
    "portainer": {
        "container": "week10_portainer",
        "port": 9443,
        "health_check": None,
        "startup_time": 10
    }
}


def verify_prerequisites() -> bool:
    """Verify Docker is available and running."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        if result.returncode != 0:
            logger.error("Docker daemon is not running. Please start Docker Desktop.")
            return False
        return True
    except FileNotFoundError:
        logger.error("Docker not found. Please install Docker Desktop.")
        return False
    except Exception as e:
        logger.error(f"Docker check failed: {e}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Start Week 10 Laboratory")
    parser.add_argument("--status", action="store_true", help="Check status only")
    parser.add_argument("--rebuild", action="store_true", help="Force rebuild images")
    parser.add_argument("--detach", "-d", action="store_true", default=True,
                        help="Run in detached mode (default)")
    args = parser.parse_args()

    docker_dir = PROJECT_ROOT / "docker"
    
    try:
        docker = DockerManager(docker_dir)
    except FileNotFoundError as e:
        logger.error(str(e))
        return 1

    if args.status:
        logger.info("Checking service status...")
        docker.show_status(SERVICES)
        return 0

    # Verify prerequisites
    if not verify_prerequisites():
        return 1

    logger.info("=" * 60)
    logger.info("Starting Week 10 Laboratory Environment")
    logger.info("=" * 60)

    try:
        # Build and start containers
        if args.rebuild:
            logger.info("Rebuilding Docker images...")
            if not docker.compose_build():
                logger.error("Build failed")
                return 1

        logger.info("Starting Docker Compose services...")
        if not docker.compose_up(detach=args.detach):
            logger.error("Failed to start services")
            return 1

        # Wait for services
        logger.info("Waiting for services to initialise...")
        time.sleep(5)

        # Verify services
        tester = NetworkTester()
        all_healthy = True

        for name, config in SERVICES.items():
            port = config["port"]
            if tester.check_tcp_port("127.0.0.1", port):
                logger.info(f"  ✓ {name}: Ready on port {port}")
            else:
                # For UDP services (DNS), we can't easily check
                if name == "dns-server":
                    logger.info(f"  ✓ {name}: Started on UDP port {port}")
                else:
                    logger.warning(f"  ✗ {name}: Not responding on port {port}")
                    all_healthy = False

        if all_healthy:
            logger.info("=" * 60)
            logger.info("Laboratory environment is ready!")
            logger.info("")
            logger.info("Access points:")
            logger.info("  Web Server:  http://localhost:8000")
            logger.info("  Portainer:   https://localhost:9443")
            logger.info("  SSH Server:  ssh -p 2222 labuser@localhost (password: labpass)")
            logger.info("  FTP Server:  ftp://labftp:labftp@localhost:2121")
            logger.info("  DNS Server:  dig @127.0.0.1 -p 5353 myservice.lab.local")
            logger.info("")
            logger.info("To stop: python scripts/stop_lab.py")
            logger.info("=" * 60)
            return 0
        else:
            logger.warning("Some services may not be ready. Check Docker logs.")
            return 1

    except Exception as e:
        logger.error(f"Failed to start laboratory: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
