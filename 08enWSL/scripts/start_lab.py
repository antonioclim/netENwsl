#!/usr/bin/env python3
"""
Laboratory Startup Script — Week 8: Transport Layer

This script initialises and starts the Week 8 laboratory environment,
including nginx reverse proxy and Python backend servers.

Author: ing. dr. Antonio Clim
Course: Computer Networks - ASE, CSIE
"""

import subprocess
import sys
import time
import argparse
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

DOCKER_COMPOSE_FILE = "docker/docker-compose.yml"
EXPECTED_CONTAINERS = [
    "week8-nginx-proxy",
    "week8-backend-1",
    "week8-backend-2", 
    "week8-backend-3",
]

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: ENVIRONMENT VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════

def check_docker_running() -> bool:
    """
    Verify Docker daemon is running.
    
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


def check_compose_file() -> bool:
    """
    Verify docker-compose.yml exists.
    
    Returns:
        True if file exists, False otherwise
    """
    return Path(DOCKER_COMPOSE_FILE).exists()


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: CONTAINER MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

def start_containers(rebuild: bool = False) -> bool:
    """
    Start the laboratory containers using Docker Compose.
    
    Args:
        rebuild: If True, rebuild images before starting
        
    Returns:
        True if successful, False otherwise
    """
    # 💭 PREDICTION: What happens if port 8080 is already in use?
    #    Which container will fail to start?
    
    print("Starting laboratory containers...")
    
    cmd = ["docker", "compose", "-f", DOCKER_COMPOSE_FILE, "up", "-d"]
    
    if rebuild:
        cmd.append("--build")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode != 0:
            print(f"Error starting containers:\n{result.stderr}")
            return False
            
        return True
        
    except subprocess.TimeoutExpired:
        print("Timeout waiting for containers to start")
        return False


def get_container_status() -> dict:
    """
    Get the status of all laboratory containers.
    
    Returns:
        Dictionary mapping container name to status
    """
    # 💭 PREDICTION: What status values can a container have?
    #    (Hint: running, exited, restarting...)
    
    status = {}
    
    try:
        result = subprocess.run(
            ["docker", "ps", "-a", "--format", "{{.Names}}\t{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if line and '\t' in line:
                    name, state = line.split('\t', 1)
                    if name.startswith("week8"):
                        status[name] = state
                        
    except (subprocess.TimeoutExpired, Exception) as e:
        print(f"Error getting container status: {e}")
    
    return status


def wait_for_containers(timeout: int = 60) -> bool:
    """
    Wait for all containers to be healthy.
    
    Args:
        timeout: Maximum seconds to wait
        
    Returns:
        True if all containers healthy, False on timeout
    """
    print("Waiting for containers to be ready", end="", flush=True)
    
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        status = get_container_status()
        
        all_running = True
        for container in EXPECTED_CONTAINERS:
            if container not in status:
                all_running = False
                break
            if "Up" not in status[container]:
                all_running = False
                break
        
        if all_running:
            print(" Ready!")
            return True
        
        print(".", end="", flush=True)
        time.sleep(2)
    
    print(" Timeout!")
    return False


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: STATUS DISPLAY
# ═══════════════════════════════════════════════════════════════════════════════

def display_status() -> None:
    """Display the current status of laboratory components."""
    print("\n" + "=" * 60)
    print("WEEK 8 LABORATORY STATUS")
    print("=" * 60)
    
    status = get_container_status()
    
    print("\nContainers:")
    for container in EXPECTED_CONTAINERS:
        if container in status:
            state = status[container]
            icon = "✅" if "Up" in state else "❌"
            print(f"  {icon} {container}: {state}")
        else:
            print(f"  ❌ {container}: Not found")
    
    print("\nEndpoints:")
    print("  • nginx proxy:     http://localhost:8080")
    print("  • nginx HTTPS:     https://localhost:8443")
    print("  • Portainer:       http://localhost:9000")
    
    print("\nQuick test:")
    print("  curl http://localhost:8080/")
    print("=" * 60)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point for laboratory startup."""
    parser = argparse.ArgumentParser(
        description="Start Week 8 Laboratory Environment"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show status only, don't start containers"
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Rebuild container images before starting"
    )
    
    args = parser.parse_args()
    
    # Status only mode
    if args.status:
        display_status()
        return 0
    
    print("=" * 60)
    print("WEEK 8: Transport Layer — HTTP Server & Reverse Proxies")
    print("=" * 60)
    
    # Pre-flight checks
    print("\nPre-flight checks:")
    
    if not check_docker_running():
        print("  ❌ Docker is not running!")
        print("     Run: sudo service docker start")
        return 1
    print("  ✅ Docker is running")
    
    if not check_compose_file():
        print(f"  ❌ {DOCKER_COMPOSE_FILE} not found!")
        print("     Are you in the correct directory?")
        return 1
    print(f"  ✅ {DOCKER_COMPOSE_FILE} found")
    
    # Start containers
    print()
    if not start_containers(rebuild=args.rebuild):
        print("Failed to start containers")
        return 1
    
    # Wait for ready
    if not wait_for_containers():
        print("Some containers failed to start")
        display_status()
        return 1
    
    # Show final status
    display_status()
    
    print("\n✅ Laboratory environment is ready!")
    print("\nNext steps:")
    print("  1. Open Wireshark and select 'vEthernet (WSL)' interface")
    print("  2. Test with: curl http://localhost:8080/")
    print("  3. Start Exercise 8.01 in src/exercises/")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
