#!/usr/bin/env python3
"""
Docker Configuration Helper
NETWORKING class - ASE, Informatics | by Revolvix

Helps configure Docker Desktop settings for optimal laboratory
environment operation.

Usage:
    python setup/configure_docker.py
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def print_header(title: str) -> None:
    """Print a section header."""
    print()
    print("=" * 60)
    print(f" {title}")
    print("=" * 60)
    print()


def check_docker_status() -> dict:
    """Check Docker status and return info."""
    info = {
        "installed": False,
        "running": False,
        "version": None,
        "compose_version": None,
        "wsl2_backend": False
    }
    
    try:
        # Check version
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            info["installed"] = True
            info["version"] = result.stdout.strip()
        
        # Check if running
        result = subprocess.run(
            ["docker", "info", "--format", "{{json .}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            info["running"] = True
            
            try:
                docker_info = json.loads(result.stdout)
                
                # Check for WSL2
                isolation = docker_info.get("Isolation", "")
                os_type = docker_info.get("OSType", "")
                if os_type == "linux":
                    info["wsl2_backend"] = True
                    
            except json.JSONDecodeError:
                pass
        
        # Check Compose version
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            info["compose_version"] = result.stdout.strip()
            
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    
    return info


def print_status(info: dict) -> None:
    """Print Docker status information."""
    print_header("Docker Status")
    
    print(f"  Installed:     {'✓' if info['installed'] else '✗'}")
    print(f"  Running:       {'✓' if info['running'] else '✗'}")
    print(f"  Version:       {info['version'] or 'N/A'}")
    print(f"  Compose:       {info['compose_version'] or 'N/A'}")
    print(f"  WSL2 Backend:  {'✓' if info['wsl2_backend'] else '?'}")


def print_recommendations() -> None:
    """Print Docker Desktop configuration recommendations."""
    print_header("Recommended Settings")
    
    print("Open Docker Desktop Settings (gear icon) and configure:")
    print()
    
    print("General:")
    print("  ✓ Start Docker Desktop when you log in (optional)")
    print("  ✓ Use the WSL 2 based engine")
    print()
    
    print("Resources > WSL Integration:")
    print("  ✓ Enable integration with your default WSL distro")
    print()
    
    print("Resources > Advanced:")
    print("  Memory: At least 4 GB (8 GB recommended)")
    print("  CPUs: At least 2")
    print("  Swap: 1 GB")
    print()
    
    print("Docker Engine (JSON configuration):")
    print('  "log-driver": "json-file"')
    print('  "log-opts": {"max-size": "10m", "max-file": "3"}')
    print()


def test_docker_network() -> bool:
    """Test Docker networking."""
    print_header("Network Test")
    
    print("Testing Docker network connectivity...")
    print()
    
    try:
        # Pull a small test image
        print("  Pulling alpine:latest...", end=" ", flush=True)
        result = subprocess.run(
            ["docker", "pull", "alpine:latest"],
            capture_output=True,
            timeout=60
        )
        
        if result.returncode != 0:
            print("✗")
            print("  Could not pull image. Check internet connection.")
            return False
        
        print("✓")
        
        # Run a simple network test
        print("  Testing container networking...", end=" ", flush=True)
        result = subprocess.run(
            ["docker", "run", "--rm", "alpine:latest", "ping", "-c", "1", "8.8.8.8"],
            capture_output=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✓")
            print()
            print("Docker networking is working correctly!")
            return True
        else:
            print("✗")
            print("  Container cannot reach the internet.")
            print("  This may affect pulling images and updates.")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ (timeout)")
        return False
    except subprocess.SubprocessError as e:
        print(f"✗ ({e})")
        return False


def test_port_binding() -> bool:
    """Test port binding capability."""
    print_header("Port Binding Test")
    
    test_port = 19999
    
    print(f"Testing port binding on port {test_port}...")
    print()
    
    try:
        # Run a container with port binding
        print(f"  Starting container on port {test_port}...", end=" ", flush=True)
        
        result = subprocess.run(
            [
                "docker", "run", "-d", "--rm",
                "--name", "week9_port_test",
                "-p", f"{test_port}:80",
                "nginx:alpine"
            ],
            capture_output=True,
            timeout=60
        )
        
        if result.returncode != 0:
            print("✗")
            error = result.stderr.decode() if result.stderr else "Unknown error"
            if "port is already allocated" in error.lower():
                print(f"  Port {test_port} is already in use")
            else:
                print(f"  Error: {error[:100]}")
            return False
        
        print("✓")
        
        import time
        time.sleep(2)
        
        # Test connection
        print(f"  Testing connection to localhost:{test_port}...", end=" ", flush=True)
        
        import socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(("localhost", test_port))
            sock.close()
            print("✓")
            success = True
        except socket.error:
            print("✗")
            print("  Could not connect to the container port")
            success = False
        
        # Cleanup
        subprocess.run(
            ["docker", "stop", "week9_port_test"],
            capture_output=True,
            timeout=10
        )
        
        if success:
            print()
            print("Port binding is working correctly!")
        
        return success
        
    except subprocess.SubprocessError as e:
        print(f"✗ ({e})")
        return False


def main() -> int:
    print("=" * 60)
    print(" Docker Configuration Helper - Week 9 Laboratory")
    print(" NETWORKING class - ASE, Informatics")
    print("=" * 60)
    
    # Check status
    info = check_docker_status()
    print_status(info)
    
    if not info["running"]:
        print()
        print("Docker is not running. Please start Docker Desktop first.")
        return 1
    
    # Print recommendations
    print_recommendations()
    
    # Run tests
    response = input("Run Docker tests? [Y/n]: ")
    if response.lower() != 'n':
        test_docker_network()
        test_port_binding()
    
    print_header("Complete")
    print("Docker configuration check complete.")
    print()
    print("Next step: python setup/verify_environment.py")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
