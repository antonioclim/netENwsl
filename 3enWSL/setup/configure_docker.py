#!/usr/bin/env python3
"""
Docker Configuration Helper
NETWORKING class - ASE, Informatics | by Revolvix

Assists with configuring Docker Desktop for optimal laboratory performance.
"""

import subprocess
import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional


class DockerConfigurator:
    """Configures Docker Desktop for the laboratory environment."""

    def __init__(self):
        self.docker_available = self._check_docker()

    def _check_docker(self) -> bool:
        """Verify Docker is installed and running."""
        try:
            result = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                timeout=10
            )
            return result.returncode == 0
        except Exception:
            return False

    def get_docker_info(self) -> Optional[Dict[str, Any]]:
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
        return None

    def print_current_config(self) -> None:
        """Display current Docker configuration."""
        print("\n" + "=" * 60)
        print("Current Docker Configuration")
        print("=" * 60)
        
        if not self.docker_available:
            print("\n[ERROR] Docker is not running or not installed.")
            print("Please start Docker Desktop and try again.")
            return
        
        info = self.get_docker_info()
        if info:
            print(f"\nDocker Version: {info.get('ServerVersion', 'Unknown')}")
            print(f"Operating System: {info.get('OperatingSystem', 'Unknown')}")
            print(f"Architecture: {info.get('Architecture', 'Unknown')}")
            print(f"CPUs: {info.get('NCPU', 'Unknown')}")
            print(f"Total Memory: {info.get('MemTotal', 0) / (1024**3):.1f} GB")
            print(f"Docker Root Dir: {info.get('DockerRootDir', 'Unknown')}")
            
            # Check for WSL2 backend
            if "microsoft" in info.get('KernelVersion', '').lower():
                print("\n✓ Using WSL2 backend (recommended)")
            
            # Storage driver
            print(f"\nStorage Driver: {info.get('Driver', 'Unknown')}")
            
            # Network info
            plugins = info.get('Plugins', {})
            networks = plugins.get('Network', [])
            print(f"Network Plugins: {', '.join(networks)}")
        else:
            print("\nCould not retrieve Docker configuration.")
            print("Running basic docker info...")
            subprocess.run(["docker", "info"])

    def check_resources(self) -> None:
        """Check if Docker has sufficient resources."""
        print("\n" + "=" * 60)
        print("Resource Recommendations")
        print("=" * 60)
        
        info = self.get_docker_info()
        if not info:
            print("\nCould not check resources. Ensure Docker is running.")
            return
        
        # Memory check
        mem_gb = info.get('MemTotal', 0) / (1024**3)
        print(f"\nAllocated Memory: {mem_gb:.1f} GB")
        
        if mem_gb < 4:
            print("  [WARNING] Memory below 4GB may cause issues.")
            print("  Recommendation: Allocate at least 4GB to Docker.")
        elif mem_gb < 8:
            print("  [OK] Memory sufficient for basic labs.")
            print("  Recommendation: 8GB+ for better performance.")
        else:
            print("  [GOOD] Memory allocation is adequate.")
        
        # CPU check
        cpus = info.get('NCPU', 0)
        print(f"\nAllocated CPUs: {cpus}")
        
        if cpus < 2:
            print("  [WARNING] Less than 2 CPUs may cause slow performance.")
            print("  Recommendation: Allocate at least 2 CPUs.")
        else:
            print("  [GOOD] CPU allocation is adequate.")
        
        print("""
To adjust Docker Desktop resources:
1. Open Docker Desktop
2. Go to Settings (gear icon)
3. Select "Resources"
4. Adjust Memory and CPU sliders
5. Click "Apply & Restart"

For WSL2 backend, you may also need to configure .wslconfig:
  Create/edit %USERPROFILE%\\.wslconfig with:
  
  [wsl2]
  memory=8GB
  processors=4
""")

    def test_network(self) -> None:
        """Test Docker networking capabilities."""
        print("\n" + "=" * 60)
        print("Docker Network Test")
        print("=" * 60)
        
        if not self.docker_available:
            print("\n[ERROR] Docker is not available.")
            return
        
        print("\nListing existing networks...")
        subprocess.run(["docker", "network", "ls"])
        
        print("\nCreating test network (week3_test)...")
        result = subprocess.run(
            ["docker", "network", "create", "--driver", "bridge", "week3_test"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("  ✓ Network created successfully")
            
            # Clean up
            print("\nRemoving test network...")
            subprocess.run(
                ["docker", "network", "rm", "week3_test"],
                capture_output=True
            )
            print("  ✓ Test network removed")
        else:
            if "already exists" in result.stderr:
                print("  Network already exists (OK)")
                subprocess.run(
                    ["docker", "network", "rm", "week3_test"],
                    capture_output=True
                )
            else:
                print(f"  [ERROR] {result.stderr}")

    def pull_base_image(self) -> None:
        """Pre-pull the base Docker image."""
        print("\n" + "=" * 60)
        print("Pulling Base Image")
        print("=" * 60)
        
        if not self.docker_available:
            print("\n[ERROR] Docker is not available.")
            return
        
        print("\nPulling ubuntu:22.04 base image...")
        print("This may take a few minutes on first run.\n")
        
        result = subprocess.run(["docker", "pull", "ubuntu:22.04"])
        
        if result.returncode == 0:
            print("\n✓ Base image pulled successfully")
        else:
            print("\n[ERROR] Failed to pull base image")

    def build_week3_image(self) -> None:
        """Build the Week 3 Docker image."""
        print("\n" + "=" * 60)
        print("Building Week 3 Image")
        print("=" * 60)
        
        if not self.docker_available:
            print("\n[ERROR] Docker is not available.")
            return
        
        project_root = Path(__file__).parent.parent
        docker_dir = project_root / "docker"
        
        if not (docker_dir / "docker-compose.yml").exists():
            print(f"\n[ERROR] docker-compose.yml not found in {docker_dir}")
            return
        
        print(f"\nBuilding from {docker_dir}...")
        
        result = subprocess.run(
            ["docker", "compose", "-f", str(docker_dir / "docker-compose.yml"), "build"],
            cwd=project_root
        )
        
        if result.returncode == 0:
            print("\n✓ Week 3 image built successfully")
        else:
            print("\n[ERROR] Failed to build image")


def main() -> int:
    """Main configuration routine."""
    print("=" * 60)
    print("Docker Configuration Helper")
    print("Week 3 Laboratory - NETWORKING class")
    print("ASE, Informatics | by Revolvix")
    print("=" * 60)
    
    configurator = DockerConfigurator()
    
    if not configurator.docker_available:
        print("\n[ERROR] Docker is not running or not installed.")
        print("Please ensure Docker Desktop is running and try again.")
        return 1
    
    print("""
Select an option:
  1. Show current Docker configuration
  2. Check resource allocation
  3. Test Docker networking
  4. Pull base image (ubuntu:22.04)
  5. Build Week 3 image
  6. Run all checks
  0. Exit
""")
    
    while True:
        try:
            choice = input("\nEnter choice (0-6): ").strip()
            
            if choice == "0":
                print("Exiting.")
                return 0
            elif choice == "1":
                configurator.print_current_config()
            elif choice == "2":
                configurator.check_resources()
            elif choice == "3":
                configurator.test_network()
            elif choice == "4":
                configurator.pull_base_image()
            elif choice == "5":
                configurator.build_week3_image()
            elif choice == "6":
                configurator.print_current_config()
                configurator.check_resources()
                configurator.test_network()
            else:
                print("Invalid choice. Please enter 0-6.")
                
        except KeyboardInterrupt:
            print("\n\nInterrupted by user.")
            return 1
        except EOFError:
            return 0


if __name__ == "__main__":
    sys.exit(main())
