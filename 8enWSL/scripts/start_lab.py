#!/usr/bin/env python3
"""
Week 8 Laboratory Launcher
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
from scripts.utils.network_utils import check_port_open, wait_for_port, check_http_health
from scripts.utils.logger import setup_logger, print_banner

logger = setup_logger("start_lab")

# Service configuration
SERVICES = {
    "nginx": {
        "container": "week8-nginx-proxy",
        "port": 8080,
        "health_check": "http://localhost:8080/nginx-health",
        "startup_time": 5,
    },
    "backend1": {
        "container": "week8-backend-1",
        "port": None,  # Internal only
        "health_check": None,
        "startup_time": 3,
    },
    "backend2": {
        "container": "week8-backend-2",
        "port": None,
        "health_check": None,
        "startup_time": 3,
    },
    "backend3": {
        "container": "week8-backend-3",
        "port": None,
        "health_check": None,
        "startup_time": 3,
    },
}


def check_docker_available() -> bool:
    """Check if Docker is available and running."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except Exception:
        return False


def print_access_info():
    """Print service access information."""
    print("\n" + "=" * 60)
    print("Access Points:")
    print("=" * 60)
    print(f"""
  nginx Proxy (HTTP):   http://localhost:8080/
  nginx Proxy (HTTPS):  https://localhost:8443/ (self-signed)
  
  Load Balancing Algorithms:
    Round-Robin:        http://localhost:8080/
    Weighted:           http://localhost:8080/weighted/
    Least Connections:  http://localhost:8080/least-conn/
    IP Hash (Sticky):   http://localhost:8080/sticky/
  
  Health Check:         http://localhost:8080/nginx-health
  nginx Status:         http://localhost:8080/nginx-status
  
  Portainer:            https://localhost:9443/ (if enabled)
                        Start with: docker compose --profile management up -d
    """)
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Start Week 8 Laboratory Environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/start_lab.py           # Start all services
  python scripts/start_lab.py --status  # Check status only
  python scripts/start_lab.py --rebuild # Rebuild images before starting
  python scripts/start_lab.py --portainer # Include Portainer
        """
    )
    parser.add_argument(
        "--status", "-s",
        action="store_true",
        help="Check status only, don't start containers"
    )
    parser.add_argument(
        "--rebuild", "-r",
        action="store_true",
        help="Force rebuild of Docker images"
    )
    parser.add_argument(
        "--portainer", "-p",
        action="store_true",
        help="Include Portainer management interface"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show verbose output"
    )
    
    args = parser.parse_args()
    
    print_banner(
        "Week 8 Laboratory Environment",
        "Transport Layer: HTTP Server and Reverse Proxies"
    )
    
    # Check Docker availability
    if not check_docker_available():
        logger.error("Docker is not running!")
        logger.error("Please start Docker Desktop and try again.")
        return 1
    
    # Initialise Docker manager
    docker = DockerManager(PROJECT_ROOT / "docker")
    
    # Status only mode
    if args.status:
        docker.show_status(SERVICES)
        
        # Also check HTTP endpoints
        print("\nHTTP Health Checks:")
        print("-" * 40)
        
        if check_port_open("localhost", 8080):
            if check_http_health("http://localhost:8080/nginx-health"):
                print("  nginx:    \033[92m✓ Healthy\033[0m")
            else:
                print("  nginx:    \033[93m! Port open but unhealthy\033[0m")
        else:
            print("  nginx:    \033[91m✗ Not reachable\033[0m")
        
        return 0
    
    # Start containers
    logger.info("Starting laboratory environment...")
    
    try:
        # Build images if requested
        if args.rebuild:
            logger.info("Rebuilding Docker images...")
            if not docker.compose_build():
                logger.error("Failed to build images")
                return 1
        
        # Start containers
        logger.info("Starting containers...")
        
        # Prepare compose command
        compose_args = ["up", "-d"]
        if args.portainer:
            compose_args.extend(["--profile", "management"])
        
        result = subprocess.run(
            ["docker", "compose", "-f", str(docker.compose_file)] + compose_args,
            cwd=docker.compose_dir,
            capture_output=not args.verbose
        )
        
        if result.returncode != 0:
            logger.error("Failed to start containers")
            if not args.verbose:
                logger.error("Run with --verbose for details")
            return 1
        
        # Wait for services to initialise
        logger.info("Waiting for services to initialise...")
        time.sleep(3)
        
        # Wait for nginx to be ready
        logger.info("Checking nginx availability...")
        if not wait_for_port("localhost", 8080, timeout=30):
            logger.error("nginx did not become available within 30 seconds")
            return 1
        
        # Verify health endpoints
        logger.info("Verifying service health...")
        time.sleep(2)
        
        all_healthy = True
        for name, svc in SERVICES.items():
            health_url = svc.get("health_check")
            if health_url:
                if check_http_health(health_url):
                    logger.info(f"  ✓ {name}: healthy")
                else:
                    logger.warning(f"  ! {name}: health check failed")
                    all_healthy = False
            else:
                # Check container status for internal services
                status = docker.get_container_status()
                container = svc.get("container", name)
                if container in status:
                    state = status[container].get("state", "unknown")
                    if state == "running":
                        logger.info(f"  ✓ {name}: running")
                    else:
                        logger.warning(f"  ! {name}: {state}")
                        all_healthy = False
        
        if all_healthy:
            logger.info("\n✓ Laboratory environment is ready!")
            print_access_info()
            
            print("\nQuick Test Commands:")
            print("-" * 40)
            print("  # Test round-robin distribution")
            print("  for i in {1..6}; do curl -s http://localhost:8080/ | grep -o 'Backend-[A-Za-z]*'; done")
            print()
            print("  # Check backend headers")
            print("  curl -v http://localhost:8080/ 2>&1 | grep -i x-backend")
            print()
            
            return 0
        else:
            logger.warning("Some services may not be fully healthy")
            logger.warning("Check logs with: docker compose logs")
            print_access_info()
            return 1
            
    except KeyboardInterrupt:
        logger.info("\nStartup cancelled by user")
        return 130
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
