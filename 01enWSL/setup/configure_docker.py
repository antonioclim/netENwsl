#!/usr/bin/env python3
"""
Docker Configuration Helper
NETWORKING class - ASE, Informatics | by Revolvix

Assists with Docker Desktop configuration for best laboratory performance.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations
from typing import Optional, List, Dict, Tuple, Any

import json
import subprocess
import sys
from pathlib import Path



# ═══════════════════════════════════════════════════════════════════════════════
# CONTAINER_MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════
def get_docker_info() -> dict | None:
    """Retrieve Docker daemon information."""
    try:
        result = subprocess.run(
            ["docker", "info", "--format", "{{json .}}"],
            capture_output=True,
            text=True,
            timeout=15
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        pass
    return None



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_docker_resources(info: dict) -> None:
    """Check Docker resource allocation."""
    print("\n\033[1mDocker Resource Allocation:\033[0m")
    
    # Memory
    mem_total = info.get("MemTotal", 0)
    mem_gb = mem_total / (1024 ** 3)
    
    if mem_gb >= 8:
        status = "\033[92mOK\033[0m"
    elif mem_gb >= 4:
        status = "\033[93mLOW\033[0m"
    else:
        status = "\033[91mINSUFFICIENT\033[0m"
    
    print(f"  Memory: {mem_gb:.1f} GB [{status}]")
    
    if mem_gb < 8:
        print("    Recommendation: Allocate at least 8GB in Docker Desktop settings")
    
    # CPUs
    cpus = info.get("NCPU", 0)
    if cpus >= 4:
        status = "\033[92mOK\033[0m"
    elif cpus >= 2:
        status = "\033[93mLOW\033[0m"
    else:
        status = "\033[91mINSUFFICIENT\033[0m"
    
    print(f"  CPUs: {cpus} [{status}]")
    
    if cpus < 4:
        print("    Recommendation: Allocate at least 4 CPUs in Docker Desktop settings")



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_docker_backend(info: dict) -> None:
    """Check Docker backend configuration."""
    print("\n\033[1mDocker Backend:\033[0m")
    
    os_type = info.get("OSType", "unknown")
    print(f"  OS Type: {os_type}")
    
    # Check for WSL2 backend on Windows
    kernel_version = info.get("KernelVersion", "")
    if "microsoft" in kernel_version.lower() or "wsl" in kernel_version.lower():
        print(f"  Backend: WSL2 \033[92m(recommended)\033[0m")
    elif "hyperv" in kernel_version.lower():
        print(f"  Backend: Hyper-V \033[93m(WSL2 recommended)\033[0m")
        print("    To switch to WSL2:")
        print("    1. Open Docker Desktop Settings")
        print("    2. Go to General")
        print("    3. Enable 'Use the WSL 2 based engine'")
    else:
        print(f"  Kernel: {kernel_version[:50]}...")



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_network_configuration(info: dict) -> None:
    """Check Docker network configuration."""
    print("\n\033[1mNetwork Configuration:\033[0m")
    
    # List networks
    try:
        result = subprocess.run(
            ["docker", "network", "ls", "--format", "{{.Name}}: {{.Driver}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            networks = result.stdout.strip().split("\n")
            for net in networks[:5]:  # Show first 5
                print(f"  {net}")
            if len(networks) > 5:
                print(f"  ... and {len(networks) - 5} more")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("  Could not list networks")



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def provide_optimisation_tips() -> None:
    """Display Docker Desktop optimisation recommendations."""
    print("\n\033[1mOptimisation Tips:\033[0m")
    print("""
  1. Resource Allocation (Docker Desktop > Settings > Resources):
     - Memory: 8GB minimum, 16GB recommended
     - CPUs: 4 minimum
     - Swap: 2GB
     - Disk: 60GB minimum

  2. WSL2 Integration (Docker Desktop > Settings > Resources > WSL Integration):
     - Enable integration with your preferred WSL distribution

  3. Performance Tips:
     - Disable "Send usage statistics" if privacy is a concern
     - Enable "Use Docker Compose V2"
     - Consider disabling "Start Docker Desktop when you log in" if
       you don't always need Docker

  4. For this laboratory:
     - No special configuration required beyond defaults
     - Containers will use bridge networking
     - Volumes will bind-mount local directories
""")



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main configuration check flow."""
    print("=" * 60)
    print("Docker Configuration Helper")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
    print("=" * 60)
    
    # Check if Docker is running
    info = get_docker_info()
    
    if info is None:
        print("\n\033[91mError: Cannot connect to Docker daemon.\033[0m")
        print("\nPlease ensure Docker Desktop is running and try again.")
        print("\nIf Docker is not installed, run:")
        print("  python setup/install_prerequisites.py")
        return 1
    
    print(f"\n\033[92mDocker is running.\033[0m")
    print(f"Server Version: {info.get('ServerVersion', 'unknown')}")
    
    check_docker_resources(info)
    check_docker_backend(info)
    check_network_configuration(info)
    provide_optimisation_tips()
    
    print("\n" + "=" * 60)
    print("Configuration check complete.")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
