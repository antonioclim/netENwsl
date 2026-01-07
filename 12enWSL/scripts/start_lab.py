#!/usr/bin/env python3
"""
Week 12 Laboratory Launcher
NETWORKING class - ASE, Informatics | by Revolvix

This script starts all Docker containers and verifies the laboratory environment
for the Email Protocols and RPC exercises.
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
from scripts.utils.network_utils import check_port, wait_for_port
from scripts.utils.logger import setup_colour_logger

logger = setup_colour_logger("start_lab")

# Service configuration
SERVICES = {
    "smtp": {
        "container": "week12_lab",
        "port": 1025,
        "health_check": None,
        "startup_time": 3,
        "description": "SMTP Server",
    },
    "jsonrpc": {
        "container": "week12_lab",
        "port": 6200,
        "health_check": "http://localhost:6200",
        "startup_time": 2,
        "description": "JSON-RPC Server",
    },
    "xmlrpc": {
        "container": "week12_lab",
        "port": 6201,
        "health_check": "http://localhost:6201",
        "startup_time": 2,
        "description": "XML-RPC Server",
    },
    "grpc": {
        "container": "week12_lab",
        "port": 6251,
        "health_check": None,
        "startup_time": 3,
        "description": "gRPC Server",
    },
    "portainer": {
        "container": "week12_portainer",
        "port": 9443,
        "health_check": "https://localhost:9443",
        "startup_time": 5,
        "description": "Portainer CE",
    },
}


def start_single_service(service_name: str) -> bool:
    """
    Start a single service in standalone mode (without Docker).
    
    Args:
        service_name: Name of service to start (smtp, jsonrpc, xmlrpc, grpc)
    
    Returns:
        True if successful
    """
    service_commands = {
        "smtp": [
            sys.executable,
            str(PROJECT_ROOT / "src" / "apps" / "email" / "smtp_server.py"),
            "--host", "0.0.0.0",
            "--port", "1025",
            "--spool", str(PROJECT_ROOT / "docker" / "volumes" / "spool"),
        ],
        "jsonrpc": [
            sys.executable,
            str(PROJECT_ROOT / "src" / "apps" / "rpc" / "jsonrpc" / "jsonrpc_server.py"),
            "--host", "0.0.0.0",
            "--port", "6200",
        ],
        "xmlrpc": [
            sys.executable,
            str(PROJECT_ROOT / "src" / "apps" / "rpc" / "xmlrpc" / "xmlrpc_server.py"),
            "--host", "0.0.0.0",
            "--port", "6201",
        ],
        "grpc": [
            sys.executable,
            str(PROJECT_ROOT / "src" / "apps" / "rpc" / "grpc" / "grpc_server.py"),
            "--host", "0.0.0.0",
            "--port", "6251",
        ],
    }
    
    if service_name not in service_commands:
        logger.error(f"Unknown service: {service_name}")
        return False
    
    cmd = service_commands[service_name]
    logger.info(f"Starting {service_name} service...")
    
    try:
        # Start as background process
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        
        # Wait briefly and check if it started
        time.sleep(2)
        if process.poll() is None:
            logger.info(f"{service_name} started (PID: {process.pid})")
            return True
        else:
            _, stderr = process.communicate()
            logger.error(f"{service_name} failed to start: {stderr.decode()}")
            return False
    except Exception as e:
        logger.error(f"Failed to start {service_name}: {e}")
        return False


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Start Week 12 Laboratory Environment"
    )
    parser.add_argument(
        "--status", action="store_true",
        help="Check status only (don't start anything)"
    )
    parser.add_argument(
        "--rebuild", action="store_true",
        help="Force rebuild Docker images"
    )
    parser.add_argument(
        "--service", type=str,
        choices=["smtp", "jsonrpc", "xmlrpc", "grpc", "all"],
        default="all",
        help="Specific service to start (default: all via Docker)"
    )
    parser.add_argument(
        "--no-docker", action="store_true",
        help="Run services directly without Docker"
    )
    parser.add_argument(
        "--detach", "-d", action="store_true", default=True,
        help="Run in detached mode (default: True)"
    )
    
    args = parser.parse_args()
    
    docker_dir = PROJECT_ROOT / "docker"
    
    # Status check mode
    if args.status:
        docker = DockerManager(docker_dir)
        docker.show_status(SERVICES)
        return 0
    
    logger.info("=" * 60)
    logger.info("Starting Week 12 Laboratory Environment")
    logger.info("Email Protocols (SMTP) and Remote Procedure Call")
    logger.info("=" * 60)
    
    # Non-Docker mode (run services directly)
    if args.no_docker:
        if args.service == "all":
            for svc in ["smtp", "jsonrpc", "xmlrpc", "grpc"]:
                start_single_service(svc)
        else:
            start_single_service(args.service)
        
        logger.info("Services started. Press Ctrl+C to stop.")
        return 0
    
    # Docker mode
    try:
        docker = DockerManager(docker_dir)
        
        # Build if requested
        if args.rebuild:
            logger.info("Building Docker images...")
            if not docker.compose_build():
                logger.error("Build failed")
                return 1
        
        # Start containers
        logger.info("Starting containers...")
        if not docker.compose_up(detach=args.detach, build=not args.rebuild):
            logger.error("Failed to start containers")
            return 1
        
        # Wait for services to initialise
        logger.info("Waiting for services to initialise...")
        time.sleep(5)
        
        # Verify services
        all_healthy = True
        for name, config in SERVICES.items():
            port = config["port"]
            logger.info(f"Checking {name} ({config['description']})...")
            
            if wait_for_port("127.0.0.1", port, timeout=15):
                logger.info(f"  ✓ {name} responding on port {port}")
            else:
                logger.error(f"  ✗ {name} not responding on port {port}")
                all_healthy = False
        
        if all_healthy:
            logger.info("=" * 60)
            logger.info("Laboratory environment is ready!")
            logger.info("")
            logger.info("Access points:")
            logger.info("  Portainer:   https://localhost:9443")
            logger.info("  SMTP:        localhost:1025 (use nc or telnet)")
            logger.info("  JSON-RPC:    http://localhost:6200 (use curl)")
            logger.info("  XML-RPC:     http://localhost:6201 (use Python)")
            logger.info("  gRPC:        localhost:6251 (use grpc client)")
            logger.info("")
            logger.info("To stop: python scripts/stop_lab.py")
            logger.info("=" * 60)
            return 0
        else:
            logger.error("Some services failed to start. Check logs with:")
            logger.error("  docker compose -f docker/docker-compose.yml logs")
            return 1
    
    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {e}")
        return 1
    except Exception as e:
        logger.error(f"Failed to start laboratory: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
