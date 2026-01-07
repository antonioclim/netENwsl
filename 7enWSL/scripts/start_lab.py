#!/usr/bin/env python3
"""
Week 7 Laboratory Launcher
NETWORKING class - ASE, Informatics | by Revolvix

This script starts all Docker containers and verifies the laboratory environment.
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
from scripts.utils.network_utils import NetworkUtils
from scripts.utils.logger import setup_logger

logger = setup_logger("start_lab")

# Service definitions
SERVICES = {
    "tcp_server": {
        "container": "week7_tcp_server",
        "port": 9090,
        "health_check": "tcp",
        "startup_time": 5
    },
    "udp_receiver": {
        "container": "week7_udp_receiver",
        "port": 9091,
        "health_check": None,  # UDP, no easy check
        "startup_time": 3
    },
}

OPTIONAL_SERVICES = {
    "packet_filter": {
        "container": "week7_packet_filter",
        "port": 8888,
        "health_check": "tcp",
        "startup_time": 3,
        "profile": "proxy"
    },
}


def verify_tcp_service(host: str, port: int, timeout: int = 10) -> bool:
    """Verify a TCP service is responding."""
    net = NetworkUtils()
    return net.wait_for_port(host, port, timeout=timeout)


def main() -> int:
    parser = argparse.ArgumentParser(description="Start Week 7 Laboratory")
    parser.add_argument(
        "--status",
        action="store_true",
        help="Check status only, do not start services"
    )
    parser.add_argument(
        "--rebuild",
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
        "--proxy",
        action="store_true",
        help="Also start the packet filter proxy service"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run in demo mode (include client services)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    args = parser.parse_args()

    try:
        docker = DockerManager(PROJECT_ROOT / "docker")
    except FileNotFoundError as e:
        logger.error(f"Configuration error: {e}")
        return 1

    if args.status:
        docker.show_status(SERVICES)
        return 0

    logger.info("=" * 60)
    logger.info("Starting Week 7 Laboratory Environment")
    logger.info("NETWORKING class - ASE, Informatics")
    logger.info("=" * 60)

    try:
        # Build images if requested
        if args.rebuild:
            logger.info("Rebuilding Docker images...")
            docker.compose_build()

        # Determine which profiles to enable
        profiles = []
        if args.proxy:
            profiles.append("proxy")
        if args.demo:
            profiles.append("demo")

        # Start services
        docker.compose_up(
            detach=args.detach,
            profiles=profiles if profiles else None
        )

        # Wait for services to initialise
        logger.info("Waiting for services to initialise...")
        time.sleep(3)

        # Verify core services
        all_healthy = True
        
        for name, svc in SERVICES.items():
            port = svc["port"]
            health_type = svc.get("health_check")
            
            if health_type == "tcp":
                if verify_tcp_service("localhost", port, timeout=15):
                    logger.info(f"  [OK] {name} (port {port})")
                else:
                    logger.error(f"  [FAIL] {name} (port {port})")
                    all_healthy = False
            else:
                # For UDP, just assume it started
                logger.info(f"  [OK] {name} (port {port}) - assumed running")

        # Verify optional services if enabled
        if args.proxy:
            proxy_svc = OPTIONAL_SERVICES["packet_filter"]
            if verify_tcp_service("localhost", proxy_svc["port"], timeout=10):
                logger.info(f"  [OK] packet_filter (port {proxy_svc['port']})")
            else:
                logger.warning(f"  [WARN] packet_filter may not be ready")

        if all_healthy:
            logger.info("")
            logger.info("=" * 60)
            logger.info("Laboratory environment is ready!")
            logger.info("")
            logger.info("Access points:")
            logger.info("  TCP Echo Server: localhost:9090")
            logger.info("  UDP Receiver: localhost:9091")
            if args.proxy:
                logger.info("  Packet Filter Proxy: localhost:8888")
            logger.info("")
            logger.info("To view logs: docker compose -f docker/docker-compose.yml logs -f")
            logger.info("To stop: python scripts/stop_lab.py")
            logger.info("=" * 60)
            return 0
        else:
            logger.error("Some services failed to start. Check logs:")
            logger.error("  docker compose -f docker/docker-compose.yml logs")
            return 1

    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"Failed to start laboratory: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
