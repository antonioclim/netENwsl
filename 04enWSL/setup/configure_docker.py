#!/usr/bin/env python3
"""
Docker Configuration Helper
NETWORKING class - ASE, Informatics | by Revolvix

Assists with Docker Desktop configuration for best Week 4 laboratory experience.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import sys
import json
import os
from pathlib import Path



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_header(text: str) -> None:
    """Print a formatted header."""
    print()
    print("=" * 60)
    print(f" {text}")
    print("=" * 60)



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_docker_running() -> bool:
    """Check if Docker daemon is running."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=15
        )
        return result.returncode == 0
    except Exception:
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# CONTAINER_MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════
def get_docker_info() -> dict:
    """Get Docker system information."""
    try:
        result = subprocess.run(
            ["docker", "info", "--format", "{{json .}}"],
            capture_output=True,
            timeout=15,
            text=True
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception:
        pass
    return {}



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_wsl2_backend() -> bool:
    """Check if Docker is using WSL2 backend."""
    info = get_docker_info()
    # Check for WSL2 indicators
    os_type = info.get("OSType", "")
    kernel_version = info.get("KernelVersion", "")
    
    return "linux" in os_type.lower() and "wsl" in kernel_version.lower()



# ═══════════════════════════════════════════════════════════════════════════════
# CONTAINER_MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════
def show_docker_status():
    """Display current Docker status."""
    print_header("Docker Status")
    
    if not check_docker_running():
        print("\n  \033[91mDocker is not running!\033[0m")
        print("\n  Please start Docker Desktop and try again.")
        return False
    
    print("\n  \033[92mDocker daemon is running\033[0m")
    
    info = get_docker_info()
    
    # Display key information
    print(f"\n  Server Version: {info.get('ServerVersion', 'Unknown')}")
    print(f"  OS Type: {info.get('OSType', 'Unknown')}")
    print(f"  Kernel Version: {info.get('KernelVersion', 'Unknown')}")
    print(f"  Total Memory: {info.get('MemTotal', 0) // (1024**3)} GB")
    print(f"  CPUs: {info.get('NCPU', 'Unknown')}")
    
    # Check WSL2 backend
    if check_wsl2_backend():
        print("\n  \033[92mWSL2 backend: Enabled\033[0m")
    else:
        print("\n  \033[93mWSL2 backend: Not detected\033[0m")
        print("  Consider enabling WSL2 backend in Docker Desktop settings.")
    
    # Check resource allocation
    mem_gb = info.get('MemTotal', 0) // (1024**3)
    if mem_gb < 4:
        print(f"\n  \033[93mWarning: Low memory allocation ({mem_gb} GB)\033[0m")
        print("  Recommended: At least 4 GB for Docker")
    
    return True



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def show_recommended_settings():
    """Display recommended Docker Desktop settings."""
    print_header("Recommended Docker Desktop Settings")
    
    print("""
    For best Week 4 laboratory experience, configure Docker Desktop:
    
    General:
    --------
    ☑ Start Docker Desktop when you log in (optional)
    ☑ Use the WSL 2 based engine (required)
    
    Resources > WSL Integration:
    ----------------------------
    ☑ Enable integration with my default WSL distro
    ☑ Enable integration with additional distros (if using multiple)
    
    Resources > Advanced (WSL2 mode uses .wslconfig):
    -------------------------------------------------
    Create/edit ~/.wslconfig in Windows home directory:
    
    [wsl2]
    memory=4GB
    processors=2
    swap=2GB
    
    Docker Engine (Settings > Docker Engine):
    -----------------------------------------
    Ensure the following in daemon.json:
    {
      "features": {
        "buildkit": true
      },
      "log-driver": "json-file",
      "log-opts": {
        "max-size": "10m",
        "max-file": "3"
      }
    }
    """)



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def verify_compose():
    """Verify Docker Compose configuration."""
    print_header("Docker Compose Verification")
    
    try:
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            timeout=10,
            text=True
        )
        
        if result.returncode == 0:
            print(f"\n  \033[92mDocker Compose available\033[0m")
            print(f"  {result.stdout.strip()}")
            return True
        else:
            print("\n  \033[91mDocker Compose not available\033[0m")
            print("  Docker Compose V2 should be included with Docker Desktop.")
            return False
            
    except Exception as e:
        print(f"\n  \033[91mError checking Docker Compose: {e}\033[0m")
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_network_creation():
    """Test Docker network creation capability."""
    print_header("Network Creation Test")
    
    test_network = "week4_test_network"
    
    try:
        # Try to create a test network
        result = subprocess.run(
            ["docker", "network", "create", "--driver", "bridge", test_network],
            capture_output=True,
            timeout=30,
            text=True
        )
        
        if result.returncode == 0:
            print(f"\n  \033[92mNetwork creation: OK\033[0m")
            
            # Clean up test network
            subprocess.run(
                ["docker", "network", "rm", test_network],
                capture_output=True,
                timeout=10
            )
            return True
        else:
            print(f"\n  \033[91mNetwork creation failed\033[0m")
            print(f"  Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"\n  \033[91mError testing network: {e}\033[0m")
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    """Main configuration helper."""
    print()
    print("╔════════════════════════════════════════════════════════════╗")
    print("║       Docker Configuration Helper - Week 4 Laboratory      ║")
    print("║       NETWORKING class - ASE, Informatics | by Revolvix    ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    while True:
        print("\n" + "-" * 60)
        print("Select an option:")
        print("  1) Show Docker status")
        print("  2) Show recommended settings")
        print("  3) Verify Docker Compose")
        print("  4) Test network creation")
        print("  5) Run all checks")
        print("  q) Quit")
        print("-" * 60)
        
        choice = input("\nEnter choice [1-5, q]: ").strip().lower()
        
        if choice == '1':
            show_docker_status()
        elif choice == '2':
            show_recommended_settings()
        elif choice == '3':
            verify_compose()
        elif choice == '4':
            test_network_creation()
        elif choice == '5':
            all_ok = True
            all_ok = show_docker_status() and all_ok
            verify_compose()
            all_ok = test_network_creation() and all_ok
            show_recommended_settings()
            
            print_header("Summary")
            if all_ok:
                print("\n  \033[92mDocker configuration looks good!\033[0m")
            else:
                print("\n  \033[93mSome issues detected. Review the output above.\033[0m")
        elif choice == 'q':
            print("\nGoodbye!")
            break
        else:
            print("\n  Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
