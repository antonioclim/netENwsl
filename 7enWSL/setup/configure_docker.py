#!/usr/bin/env python3
"""
Docker Configuration Helper
NETWORKING class - ASE, Informatics | by Revolvix

Configures Docker Desktop settings and validates the environment
for the Week 7 laboratory.
"""

from __future__ import annotations

import subprocess
import sys
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


def print_header(text: str) -> None:
    """Print a formatted header."""
    print()
    print("=" * 60)
    print(text)
    print("=" * 60)


def run_docker(args: list[str], capture: bool = True) -> tuple[int, str, str]:
    """Run a docker command and return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            ["docker"] + args,
            capture_output=capture,
            text=True,
            timeout=60
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"
    except FileNotFoundError:
        return -1, "", "docker not found"
    except Exception as e:
        return -1, "", str(e)


def check_docker_info() -> Optional[Dict[str, Any]]:
    """Get Docker daemon information."""
    rc, stdout, stderr = run_docker(["info", "--format", "{{json .}}"])
    if rc != 0:
        return None
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return None


def validate_docker_config() -> bool:
    """Validate Docker configuration for Week 7 requirements."""
    print("\nValidating Docker configuration...")
    
    info = check_docker_info()
    if info is None:
        print("  [FAIL] Cannot connect to Docker daemon")
        print("         Please start Docker Desktop")
        return False
    
    print("  [OK] Docker daemon is accessible")
    
    # Check memory allocation
    mem_total = info.get("MemTotal", 0)
    mem_gb = mem_total / (1024 ** 3)
    if mem_gb >= 4:
        print(f"  [OK] Memory: {mem_gb:.1f} GB available")
    else:
        print(f"  [WARN] Memory: {mem_gb:.1f} GB (recommend 4+ GB)")
    
    # Check storage driver
    storage_driver = info.get("Driver", "unknown")
    print(f"  [INFO] Storage driver: {storage_driver}")
    
    # Check operating system type
    os_type = info.get("OSType", "unknown")
    print(f"  [INFO] OS type: {os_type}")
    
    # Check if running in WSL2
    kernel_version = info.get("KernelVersion", "")
    if "microsoft" in kernel_version.lower() or "wsl" in kernel_version.lower():
        print("  [OK] WSL2 backend detected")
    
    return True


def create_docker_network() -> bool:
    """Create the week7net Docker network if it doesn't exist."""
    print("\nConfiguring Docker network...")
    
    # Check if network exists
    rc, stdout, stderr = run_docker(["network", "ls", "--filter", "name=week7net", "--format", "{{.Name}}"])
    
    if "week7net" in stdout:
        print("  [OK] Network 'week7net' already exists")
        return True
    
    # Create network
    rc, stdout, stderr = run_docker([
        "network", "create",
        "--driver", "bridge",
        "--subnet", "10.0.7.0/24",
        "--gateway", "10.0.7.1",
        "week7net"
    ])
    
    if rc == 0:
        print("  [OK] Created network 'week7net' (10.0.7.0/24)")
        return True
    else:
        print(f"  [FAIL] Could not create network: {stderr}")
        return False


def pull_base_images() -> bool:
    """Pull required Docker images."""
    print("\nPulling required Docker images...")
    
    images = [
        "python:3.11-slim",
    ]
    
    all_ok = True
    for image in images:
        print(f"  Pulling {image}...")
        rc, stdout, stderr = run_docker(["pull", image], capture=False)
        if rc == 0:
            print(f"    [OK] {image}")
        else:
            print(f"    [FAIL] {image}")
            all_ok = False
    
    return all_ok


def verify_compose_file() -> bool:
    """Verify the docker-compose.yml file is valid."""
    print("\nVerifying docker-compose.yml...")
    
    script_dir = Path(__file__).resolve().parent.parent
    compose_file = script_dir / "docker" / "docker-compose.yml"
    
    if not compose_file.exists():
        print(f"  [FAIL] File not found: {compose_file}")
        return False
    
    rc, stdout, stderr = run_docker(["compose", "-f", str(compose_file), "config", "--quiet"])
    
    if rc == 0:
        print("  [OK] docker-compose.yml is valid")
        return True
    else:
        print(f"  [FAIL] Invalid docker-compose.yml: {stderr}")
        return False


def test_container_run() -> bool:
    """Test that containers can be started."""
    print("\nTesting container execution...")
    
    rc, stdout, stderr = run_docker([
        "run", "--rm",
        "python:3.11-slim",
        "python", "-c", "print('Hello from container')"
    ])
    
    if rc == 0 and "Hello from container" in stdout:
        print("  [OK] Containers can execute Python")
        return True
    else:
        print(f"  [FAIL] Container test failed: {stderr}")
        return False


def print_configuration_summary() -> None:
    """Print configuration summary and next steps."""
    print_header("Configuration Summary")
    
    print("""
Docker environment configured for Week 7 laboratory.

Network: week7net (10.0.7.0/24)
  - Gateway: 10.0.7.1
  - TCP Server: assigned dynamically
  - UDP Receiver: assigned dynamically

Services defined in docker-compose.yml:
  - tcp_server (port 9090)
  - tcp_client
  - udp_receiver (port 9091)
  - udp_sender

Next steps:
  1. Start the laboratory:
     python scripts/start_lab.py

  2. Run the baseline demonstration:
     python scripts/run_demo.py --demo baseline

  3. Access Portainer (if installed):
     https://localhost:9443
""")


def main() -> int:
    """Main Docker configuration routine."""
    print_header("Docker Configuration for Week 7 Laboratory")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
    
    # Validate Docker is working
    if not validate_docker_config():
        return 1
    
    # Create network
    if not create_docker_network():
        return 1
    
    # Pull images
    if not pull_base_images():
        print("  [WARN] Some images failed to pull, continuing anyway")
    
    # Verify compose file
    if not verify_compose_file():
        return 1
    
    # Test container execution
    if not test_container_run():
        return 1
    
    print_configuration_summary()
    
    print("\n[OK] Docker configuration complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
