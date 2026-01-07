#!/usr/bin/env python3
"""
Docker Configuration Helper
NETWORKING class - ASE, Informatics | by Revolvix

Configures Docker Desktop settings for optimal laboratory performance.
"""

import json
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, Optional


def get_docker_config_path() -> Optional[Path]:
    """Get the Docker Desktop settings file path."""
    if platform.system() == "Windows":
        return Path.home() / "AppData" / "Roaming" / "Docker" / "settings.json"
    elif platform.system() == "Darwin":  # macOS
        return Path.home() / "Library" / "Group Containers" / "group.com.docker" / "settings.json"
    else:
        return None


def read_docker_settings() -> Dict[str, Any]:
    """Read current Docker Desktop settings."""
    config_path = get_docker_config_path()
    if config_path and config_path.exists():
        with open(config_path, "r") as f:
            return json.load(f)
    return {}


def print_current_config():
    """Display current Docker configuration."""
    print("\n\033[1mCurrent Docker Configuration:\033[0m")
    print("-" * 40)
    
    # Get Docker info
    try:
        result = subprocess.run(
            ["docker", "info", "--format", "{{json .}}"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            info = json.loads(result.stdout)
            
            print(f"  Docker Version: {info.get('ServerVersion', 'Unknown')}")
            print(f"  Storage Driver: {info.get('Driver', 'Unknown')}")
            print(f"  CPUs: {info.get('NCPU', 'Unknown')}")
            print(f"  Memory: {info.get('MemTotal', 0) / (1024**3):.1f} GB")
            print(f"  Operating System: {info.get('OperatingSystem', 'Unknown')}")
            print(f"  Kernel Version: {info.get('KernelVersion', 'Unknown')}")
            
            # WSL2 specific
            if "wsl" in info.get('KernelVersion', '').lower():
                print(f"  \033[92m✓ Running on WSL2 backend\033[0m")
        else:
            print(f"  Error getting Docker info: {result.stderr}")
    except Exception as e:
        print(f"  Error: {e}")


def print_recommended_settings():
    """Display recommended settings for the laboratory."""
    print("\n\033[1mRecommended Docker Desktop Settings:\033[0m")
    print("-" * 40)
    print("""
  \033[1mGeneral:\033[0m
    ☑ Start Docker Desktop when you log in
    ☑ Use the WSL 2 based engine
    
  \033[1mResources > WSL Integration:\033[0m
    ☑ Enable integration with my default WSL distro
    
  \033[1mResources > Advanced:\033[0m
    CPUs:    4 (minimum 2)
    Memory:  8 GB (minimum 4 GB)
    Swap:    1 GB
    
  \033[1mDocker Engine:\033[0m
    Add to daemon configuration:
    {
      "log-driver": "json-file",
      "log-opts": {
        "max-size": "10m",
        "max-file": "3"
      }
    }
    """)


def verify_docker_network():
    """Verify Docker network configuration."""
    print("\n\033[1mDocker Network Verification:\033[0m")
    print("-" * 40)
    
    try:
        # List networks
        result = subprocess.run(
            ["docker", "network", "ls", "--format", "{{.Name}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            networks = result.stdout.strip().split("\n")
            print(f"  Existing networks: {', '.join(networks)}")
            
            # Check for week8 network
            if "seminar8-network" in networks:
                print(f"  \033[92m✓ Week 8 network exists\033[0m")
            else:
                print(f"  \033[93m! Week 8 network not created yet (will be created on start)\033[0m")
        else:
            print(f"  Error: {result.stderr}")
            
    except Exception as e:
        print(f"  Error: {e}")


def verify_docker_compose():
    """Verify Docker Compose configuration."""
    print("\n\033[1mDocker Compose Verification:\033[0m")
    print("-" * 40)
    
    try:
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print(f"  {result.stdout.strip()}")
            print("  \033[92m✓ Docker Compose V2 is available\033[0m")
        else:
            print("  \033[91m✗ Docker Compose V2 not available\033[0m")
            print("  Trying legacy docker-compose...")
            
            result = subprocess.run(
                ["docker-compose", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                print(f"  {result.stdout.strip()}")
                print("  \033[93m! Using legacy docker-compose\033[0m")
                
    except Exception as e:
        print(f"  Error: {e}")


def validate_compose_file():
    """Validate the docker-compose.yml file."""
    print("\n\033[1mCompose File Validation:\033[0m")
    print("-" * 40)
    
    script_dir = Path(__file__).parent.parent
    compose_file = script_dir / "docker" / "docker-compose.yml"
    
    if not compose_file.exists():
        print(f"  \033[91m✗ Compose file not found: {compose_file}\033[0m")
        return
    
    try:
        result = subprocess.run(
            ["docker", "compose", "-f", str(compose_file), "config", "--quiet"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"  \033[92m✓ docker-compose.yml is valid\033[0m")
        else:
            print(f"  \033[91m✗ Validation failed:\033[0m")
            print(f"    {result.stderr}")
            
    except Exception as e:
        print(f"  Error: {e}")


def main():
    print("\033[1m")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║        Docker Configuration Helper - Week 8               ║")
    print("║        NETWORKING class - ASE, Informatics                ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print("\033[0m")
    
    # Check Docker availability
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            print("\n\033[91mError: Docker is not installed or not in PATH\033[0m")
            print("Please install Docker Desktop first.")
            return 1
    except FileNotFoundError:
        print("\n\033[91mError: Docker command not found\033[0m")
        print("Please install Docker Desktop first.")
        return 1
    
    # Display configuration
    print_current_config()
    verify_docker_compose()
    verify_docker_network()
    validate_compose_file()
    print_recommended_settings()
    
    print("\n\033[1mConfiguration Tips:\033[0m")
    print("-" * 40)
    print("""
  1. Open Docker Desktop
  2. Go to Settings (gear icon)
  3. Apply recommended settings above
  4. Click "Apply & Restart"
  5. Run this script again to verify
    """)
    
    print("\n\033[92mConfiguration check complete!\033[0m\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
