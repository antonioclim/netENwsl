#!/usr/bin/env python3
"""
Week 11 Laboratory Launcher
NETWORKING class - ASE, Informatics | by Revolvix

This script starts all Docker containers and verifies the laboratory environment.
"""
from __future__ import annotations

import subprocess
import sys
import time
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger, print_banner
from scripts.utils.network_utils import wait_for_port, test_load_balancer, print_distribution

logger = setup_logger("start_lab")

# Service definitions for Week 11
SERVICES = {
    "nginx_lb": {
        "container": "s11_nginx_lb",
        "port": 8080,
        "health_check": "/health",
        "startup_time": 3
    },
    "backend_1": {
        "container": "s11_backend_1",
        "port": 80,  # Internal port
        "health_check": None,
        "startup_time": 2
    },
    "backend_2": {
        "container": "s11_backend_2",
        "port": 80,
        "health_check": None,
        "startup_time": 2
    },
    "backend_3": {
        "container": "s11_backend_3",
        "port": 80,
        "health_check": None,
        "startup_time": 2
    },
}


def start_docker_stack(docker: DockerManager, 
                       rebuild: bool = False,
                       detach: bool = True) -> bool:
    """Start the Docker Compose stack."""
    logger.info("Starting Docker Compose stack...")
    
    if rebuild:
        logger.info("Rebuilding images...")
        docker.compose_build()
    
    return docker.compose_up(detach=detach, build=rebuild)


def verify_load_balancer(url: str = "http://localhost:8080/") -> bool:
    """Verify load balancer is distributing traffic correctly."""
    logger.info("Testing load balancer distribution...")
    
    try:
        stats = test_load_balancer(url, num_requests=12, concurrency=1)
        
        if stats['successful'] < 10:
            logger.error(f"Too many failed requests: {stats['failed']}/{stats['total_requests']}")
            return False
        
        # Check distribution
        distribution = stats['distribution']
        if len(distribution) >= 2:
            logger.info("Load balancer is distributing traffic across backends")
            print_distribution(distribution, stats['successful'])
            return True
        else:
            logger.warning("Traffic not distributed across multiple backends")
            return True  # May be using IP hash
    
    except Exception as e:
        logger.error(f"Load balancer verification failed: {e}")
        return False


def print_access_info() -> None:
    """Display access information for services."""
    print("")
    print("=" * 60)
    print(" ACCESS INFORMATION")
    print("=" * 60)
    print("")
    print("  Load Balancer:     http://localhost:8080/")
    print("  Health Check:      http://localhost:8080/health")
    print("  Nginx Status:      http://localhost:8080/nginx_status")
    print("")
    print("  Backend 1:         http://localhost:8080/ (via LB)")
    print("  Backend 2:         http://localhost:8080/ (via LB)")
    print("  Backend 3:         http://localhost:8080/ (via LB)")
    print("")
    print("  Portainer:         https://localhost:9443")
    print("                     (if installed separately)")
    print("")
    print("=" * 60)
    print("")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Start Week 11 Laboratory Environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Start all services
  %(prog)s --status           # Check status only
  %(prog)s --rebuild          # Force rebuild images
  %(prog)s --nginx-only       # Start only Nginx stack
        """
    )
    parser.add_argument("--status", action="store_true",
                        help="Check status only, don't start services")
    parser.add_argument("--rebuild", action="store_true",
                        help="Force rebuild Docker images")
    parser.add_argument("--detach", "-d", action="store_true", default=True,
                        help="Run in detached mode (default)")
    parser.add_argument("--nginx-only", action="store_true",
                        help="Start only the Nginx stack (no Python backends)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose output")
    
    args = parser.parse_args()
    
    docker_dir = PROJECT_ROOT / "docker"
    
    try:
        docker = DockerManager(docker_dir)
    except FileNotFoundError as e:
        logger.error(f"Docker configuration not found: {e}")
        return 1
    
    if args.status:
        docker.show_status(SERVICES)
        return 0
    
    print_banner("Week 11 Laboratory Environment")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
    print("")
    
    logger.info("Starting Week 11 Laboratory Environment")
    logger.info(f"Docker directory: {docker_dir}")
    
    try:
        # Start Docker stack
        if not start_docker_stack(docker, rebuild=args.rebuild, detach=args.detach):
            logger.error("Failed to start Docker stack")
            return 1
        
        # Wait for services to initialise
        logger.info("Waiting for services to initialise...")
        time.sleep(5)
        
        # Wait for load balancer port
        logger.info("Waiting for load balancer to become available...")
        if not wait_for_port("localhost", 8080, timeout=30):
            logger.error("Load balancer did not start within timeout")
            return 1
        
        # Verify services
        logger.info("Verifying services...")
        all_healthy = docker.verify_services({
            "nginx_lb": SERVICES["nginx_lb"]
        })
        
        if not all_healthy:
            logger.warning("Some services may not be healthy")
        
        # Test load balancing
        time.sleep(2)  # Additional wait for backends
        verify_load_balancer()
        
        # Print access information
        print_access_info()
        
        logger.info("Laboratory environment is ready!")
        return 0
    
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user")
        return 130
    
    except Exception as e:
        logger.error(f"Failed to start laboratory: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())


# Revolvix&Hypotheticalandrei
