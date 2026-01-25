#!/usr/bin/env python3
"""
Docker Configuration Helper for Week 11 Laboratory
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Assists with Docker Desktop configuration for WSL2.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import subprocess
import sys
import json
import platform
from pathlib import Path



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_header(text: str) -> None:
    """Print a formatted header."""
    print("")
    print("=" * 60)
    print(f" {text}")
    print("=" * 60)



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_docker_wsl_integration() -> bool:
    """Check if Docker is configured with WSL2 backend."""
    print("\nChecking Docker WSL2 Integration...")
    
    # Check Docker info for WSL2
    try:
        result = subprocess.run(
            ["docker", "info", "--format", "{{.OperatingSystem}}"],
            capture_output=True,
            text=True
        )
        
        os_info = result.stdout.strip()
        print(f"  Docker OS: {os_info}")
        
        if "WSL" in os_info or "Desktop" in os_info:
            print("  ✓ Docker appears to be using WSL2 backend")
            return True
        else:
            print("  ⚠ Docker may not be using WSL2 backend")
            return False
    
    except Exception as e:
        print(f"  Error checking Docker: {e}")
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_docker_resources() -> None:
    """Check Docker resource allocation."""
    print("\nDocker Resource Allocation:")
    
    try:
        result = subprocess.run(
            ["docker", "info", "--format", 
             "CPUs: {{.NCPU}}\nMemory: {{.MemTotal}}"],
            capture_output=True,
            text=True
        )
        
        for line in result.stdout.strip().split('\n'):
            print(f"  {line}")
        
        # Get memory in GB
        result = subprocess.run(
            ["docker", "info", "--format", "{{.MemTotal}}"],
            capture_output=True,
            text=True
        )
        mem_bytes = int(result.stdout.strip())
        mem_gb = mem_bytes / (1024**3)
        
        if mem_gb < 4:
            print("  ⚠ Memory allocation may be low for this lab")
            print("    Recommend: Increase Docker memory to 4GB+")
        else:
            print(f"  ✓ Memory allocation adequate ({mem_gb:.1f} GB)")
    
    except Exception as e:
        print(f"  Error checking resources: {e}")



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_docker_networks() -> None:
    """Check existing Docker networks."""
    print("\nDocker Networks:")
    
    try:
        result = subprocess.run(
            ["docker", "network", "ls", "--format", 
             "{{.Name}}\t{{.Driver}}\t{{.Scope}}"],
            capture_output=True,
            text=True
        )
        
        print("  Name                  Driver    Scope")
        print("  " + "-" * 45)
        for line in result.stdout.strip().split('\n'):
            if line:
                print(f"  {line}")
    
    except Exception as e:
        print(f"  Error listing networks: {e}")



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_wsl_config_recommendation() -> None:
    """Print recommended .wslconfig settings."""
    print("\nRecommended WSL2 Configuration:")
    print("-" * 50)
    print("""
Create/edit the file: %USERPROFILE%\\.wslconfig

[wsl2]
memory=8GB
processors=4
localhostForwarding=true

After editing, restart WSL:
  wsl --shutdown
  """)



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_docker_desktop_settings() -> None:
    """Print recommended Docker Desktop settings."""
    print("\nRecommended Docker Desktop Settings:")
    print("-" * 50)
    print("""
1. Open Docker Desktop
2. Go to Settings (gear icon)
3. General:
   - ✓ Use the WSL 2 based engine
   
4. Resources > WSL Integration:
   - ✓ Enable integration with my default WSL distro
   - Enable for any additional distros you use
   
5. Resources > Advanced:
   - Memory: 4GB minimum, 8GB recommended
   - CPUs: 2 minimum, 4 recommended
   - Swap: 1GB
   
6. Docker Engine:
   - No changes needed for this lab
""")



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_docker_compose() -> bool:
    """Test Docker Compose functionality."""
    print("\nTesting Docker Compose...")
    
    try:
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            text=True
        )
        
        print(f"  {result.stdout.strip()}")
        
        if result.returncode == 0:
            print("  ✓ Docker Compose is working")
            return True
        else:
            print("  ✗ Docker Compose not available")
            return False
    
    except Exception as e:
        print(f"  Error: {e}")
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    print_header("Docker Configuration Helper - Week 11")
    print("NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim")
    
    if platform.system() != "Windows":
        print("\nNote: This helper is designed for Windows with WSL2.")
        print("On Linux/macOS, Docker should work directly.\n")
    
    # Check Docker status
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        
        if result.returncode != 0:
            print("\n⚠ Docker is not running!")
            print("Please start Docker Desktop and try again.")
            return 1
    
    except FileNotFoundError:
        print("\n⚠ Docker is not installed!")
        print("Please install Docker Desktop from https://docker.com")
        return 1
    
    except Exception as e:
        print(f"\n⚠ Error checking Docker: {e}")
        return 1
    
    # Run checks
    check_docker_wsl_integration()
    check_docker_resources()
    check_docker_networks()
    test_docker_compose()
    
    # Print recommendations
    if platform.system() == "Windows":
        print_wsl_config_recommendation()
    
    print_docker_desktop_settings()
    
    print("\n" + "=" * 60)
    print("Configuration check complete!")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())


# ing. dr. Antonio Clim
