#!/usr/bin/env python3
"""
Docker Configuration Helper
NETWORKING class - ASE, Informatics | by Revolvix

Assists with Docker Desktop configuration for laboratory use.
"""

import subprocess
import sys
import json
from pathlib import Path


def print_header(title: str):
    """Print a formatted section header."""
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)
    print()


def check_docker_running() -> bool:
    """Check if Docker daemon is running."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except Exception:
        return False


def get_docker_info() -> dict:
    """Get Docker system information."""
    try:
        result = subprocess.run(
            ["docker", "info", "--format", "{{json .}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception:
        pass
    return {}


def check_wsl2_backend() -> bool:
    """Check if Docker is using WSL2 backend (Windows)."""
    info = get_docker_info()
    
    # Check for WSL2 indicators
    os_type = info.get("OSType", "")
    kernel_version = info.get("KernelVersion", "")
    
    if "linux" in os_type.lower() and "microsoft" in kernel_version.lower():
        return True
    
    # Check for Hyper-V vs WSL2
    isolation = info.get("Isolation", "")
    if isolation == "hyperv":
        return False
    
    return True  # Assume WSL2 if not Hyper-V


def verify_network_settings():
    """Verify Docker network settings."""
    print_header("Docker Network Configuration")
    
    try:
        result = subprocess.run(
            ["docker", "network", "ls", "--format", "{{.Name}}"],
            capture_output=True,
            text=True
        )
        
        networks = result.stdout.strip().split('\n')
        print("  Available Docker networks:")
        for net in networks:
            print(f"    - {net}")
        print()
        
        # Check for bridge network
        if "bridge" in networks:
            print("  ✓ Default bridge network available")
        else:
            print("  ⚠ Default bridge network not found")
        
    except Exception as e:
        print(f"  ✗ Could not check networks: {e}")


def verify_resource_limits():
    """Check Docker resource allocation."""
    print_header("Docker Resource Limits")
    
    info = get_docker_info()
    
    memory_total = info.get("MemTotal", 0)
    cpus = info.get("NCPU", 0)
    
    if memory_total:
        memory_gb = memory_total / (1024 ** 3)
        print(f"  Available Memory: {memory_gb:.1f} GB")
        
        if memory_gb < 4:
            print("  ⚠ Warning: Less than 4 GB available")
            print("    Consider increasing Docker memory limit")
        else:
            print("  ✓ Memory allocation is sufficient")
    
    if cpus:
        print(f"  Available CPUs: {cpus}")
        if cpus < 2:
            print("  ⚠ Warning: Less than 2 CPUs allocated")
        else:
            print("  ✓ CPU allocation is sufficient")


def test_container_creation():
    """Test basic container creation."""
    print_header("Container Creation Test")
    
    print("  Creating test container...")
    
    try:
        # Run a simple test container
        result = subprocess.run(
            ["docker", "run", "--rm", "hello-world"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("  ✓ Container creation successful")
            print()
            print("  Test output (first few lines):")
            for line in result.stdout.split('\n')[:5]:
                if line.strip():
                    print(f"    {line}")
        else:
            print(f"  ✗ Container creation failed: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("  ✗ Container creation timed out")
    except Exception as e:
        print(f"  ✗ Error: {e}")


def show_recommended_settings():
    """Display recommended Docker Desktop settings."""
    print_header("Recommended Docker Desktop Settings")
    
    if sys.platform == "win32":
        print("  Windows (Docker Desktop):")
        print()
        print("  Settings > General:")
        print("    ☑ Use the WSL 2 based engine")
        print()
        print("  Settings > Resources > WSL Integration:")
        print("    ☑ Enable integration with default WSL distro")
        print()
        print("  Settings > Resources > Advanced:")
        print("    Memory: 4 GB minimum (8 GB recommended)")
        print("    CPUs: 2 minimum (4 recommended)")
        print("    Disk image size: 20 GB minimum")
    else:
        print("  Linux/macOS:")
        print()
        print("  Ensure sufficient resources:")
        print("    Memory: 4 GB minimum (8 GB recommended)")
        print("    Disk: 10 GB free minimum")


def main():
    print()
    print("=" * 60)
    print("  Docker Configuration Helper")
    print("  Week 5 Laboratory - NETWORKING class")
    print("=" * 60)
    print()
    
    # Check if Docker is running
    if not check_docker_running():
        print("  ✗ Docker is not running!")
        print()
        print("  Please start Docker Desktop and try again.")
        print()
        return 1
    
    print("  ✓ Docker is running")
    
    # Check WSL2 backend (Windows)
    if sys.platform == "win32":
        print()
        if check_wsl2_backend():
            print("  ✓ Docker is using WSL2 backend")
        else:
            print("  ⚠ Docker may be using Hyper-V backend")
            print("    WSL2 backend is recommended for better performance")
    
    # Show Docker info
    info = get_docker_info()
    if info:
        print()
        print(f"  Docker Version: {info.get('ServerVersion', 'Unknown')}")
        print(f"  Storage Driver: {info.get('Driver', 'Unknown')}")
    
    # Verify network settings
    verify_network_settings()
    
    # Check resource limits
    verify_resource_limits()
    
    # Test container creation
    test_container_creation()
    
    # Show recommendations
    show_recommended_settings()
    
    print_header("Configuration Complete")
    print("  Docker is ready for the Week 5 laboratory.")
    print()
    print("  Next steps:")
    print("    python scripts/start_lab.py")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
