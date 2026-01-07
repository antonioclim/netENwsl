#!/usr/bin/env python3
"""
Prerequisites Installation Helper
NETWORKING class - ASE, Informatics | by Revolvix

Assists with installing and configuring prerequisites for Week 12 laboratory.
This script provides guidance and automation where possible.
"""

import subprocess
import sys
import os
import platform
from pathlib import Path
from typing import Optional


def print_header(title: str) -> None:
    """Print a formatted section header."""
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def print_step(step: str) -> None:
    """Print a step indicator."""
    print(f"\n>>> {step}")


def run_command(cmd: list[str], check: bool = True) -> bool:
    """Run a command and return success status."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"    [\033[92mOK\033[0m] {' '.join(cmd)}")
            return True
        else:
            print(f"    [\033[91mFAIL\033[0m] {' '.join(cmd)}")
            if result.stderr:
                print(f"         Error: {result.stderr[:200]}")
            return False
    except FileNotFoundError:
        print(f"    [\033[91mFAIL\033[0m] Command not found: {cmd[0]}")
        return False
    except Exception as e:
        print(f"    [\033[91mFAIL\033[0m] {e}")
        return False


def install_python_packages() -> bool:
    """Install required Python packages."""
    print_step("Installing Python packages")
    
    packages = [
        "grpcio>=1.50.0",
        "grpcio-tools>=1.50.0",
        "protobuf>=4.21.0",
        "dnspython>=2.4.0",
        "pytest>=7.0.0",
        "pytest-timeout>=2.0.0",
        "colorama>=0.4.6",
        "pyyaml>=6.0",
        "requests>=2.28.0",
    ]
    
    # First upgrade pip
    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=False)
    
    success = True
    for package in packages:
        if not run_command([sys.executable, "-m", "pip", "install", package], check=False):
            success = False
    
    return success


def create_directories() -> bool:
    """Create required directories."""
    print_step("Creating required directories")
    
    base = Path(__file__).parent.parent
    directories = [
        base / "docker" / "volumes" / "spool",
        base / "pcap",
        base / "artifacts",
        base / "logs",
    ]
    
    for d in directories:
        try:
            d.mkdir(parents=True, exist_ok=True)
            print(f"    [\033[92mOK\033[0m] Created {d}")
        except Exception as e:
            print(f"    [\033[91mFAIL\033[0m] Failed to create {d}: {e}")
            return False
    
    return True


def check_docker_desktop() -> bool:
    """Provide guidance for Docker Desktop installation."""
    print_step("Checking Docker Desktop")
    
    try:
        result = subprocess.run(["docker", "info"], capture_output=True, timeout=15)
        if result.returncode == 0:
            print("    [\033[92mOK\033[0m] Docker Desktop is running")
            return True
    except Exception:
        pass
    
    print("    [\033[93mWARN\033[0m] Docker Desktop not detected")
    print()
    print("    To install Docker Desktop:")
    print("    1. Download from: https://www.docker.com/products/docker-desktop/")
    print("    2. Run the installer")
    print("    3. During setup, enable 'Use WSL 2 based engine'")
    print("    4. Start Docker Desktop")
    print("    5. Wait for the engine to initialise (whale icon stops animating)")
    print()
    
    return False


def configure_wsl2() -> bool:
    """Provide guidance for WSL2 configuration."""
    print_step("WSL2 Configuration")
    
    if platform.system() != "Windows":
        print("    Not running on Windows - skipping WSL2 configuration")
        return True
    
    try:
        result = subprocess.run(["wsl", "--status"], capture_output=True, timeout=10)
        output = result.stdout.decode(errors="replace") + result.stderr.decode(errors="replace")
        
        if "WSL 2" in output or "Default Version: 2" in output:
            print("    [\033[92mOK\033[0m] WSL2 is configured")
            return True
    except Exception:
        pass
    
    print("    [\033[93mWARN\033[0m] WSL2 may not be fully configured")
    print()
    print("    To configure WSL2:")
    print("    1. Open PowerShell as Administrator")
    print("    2. Run: wsl --install")
    print("    3. Restart your computer")
    print("    4. Run: wsl --set-default-version 2")
    print()
    
    return False


def setup_wireshark_guidance() -> None:
    """Provide guidance for Wireshark installation."""
    print_step("Wireshark Installation")
    
    wireshark_paths = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe"),
    ]
    
    for p in wireshark_paths:
        if p.exists():
            print(f"    [\033[92mOK\033[0m] Wireshark found at {p}")
            return
    
    print("    [\033[93mWARN\033[0m] Wireshark not found")
    print()
    print("    To install Wireshark:")
    print("    1. Download from: https://www.wireshark.org/download.html")
    print("    2. Run the installer")
    print("    3. During installation, allow Npcap installation (required for capture)")
    print("    4. Optionally install USBPcap for USB traffic capture")
    print()


def generate_proto_stubs() -> bool:
    """Generate gRPC stubs from Protocol Buffer definitions."""
    print_step("Generating gRPC stubs")
    
    base = Path(__file__).parent.parent
    proto_dir = base / "src" / "apps" / "rpc" / "grpc"
    proto_file = proto_dir / "calculator.proto"
    
    if not proto_file.exists():
        print(f"    [\033[93mWARN\033[0m] Proto file not found: {proto_file}")
        print("    Stubs will be generated when proto file is created")
        return True
    
    cmd = [
        sys.executable, "-m", "grpc_tools.protoc",
        f"-I{proto_dir}",
        f"--python_out={proto_dir}",
        f"--grpc_python_out={proto_dir}",
        str(proto_file)
    ]
    
    return run_command(cmd, check=False)


def main() -> int:
    """Run installation and configuration steps."""
    print_header("Week 12 Prerequisites Installation")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
    
    # Track overall success
    all_ok = True
    
    # Step 1: Python packages
    if not install_python_packages():
        all_ok = False
    
    # Step 2: Create directories
    if not create_directories():
        all_ok = False
    
    # Step 3: Docker Desktop
    if not check_docker_desktop():
        all_ok = False
    
    # Step 4: WSL2 (Windows only)
    if platform.system() == "Windows":
        if not configure_wsl2():
            all_ok = False
    
    # Step 5: Wireshark guidance
    setup_wireshark_guidance()
    
    # Step 6: Generate proto stubs
    generate_proto_stubs()
    
    # Summary
    print_header("Installation Summary")
    
    if all_ok:
        print("\033[92mAll automated steps completed successfully!\033[0m")
        print()
        print("Next steps:")
        print("  1. Ensure Docker Desktop is running")
        print("  2. Run: python setup/verify_environment.py")
        print("  3. Start the lab: python scripts/start_lab.py")
    else:
        print("\033[93mSome steps require manual intervention.\033[0m")
        print()
        print("Please review the output above and complete any manual steps.")
        print("Then run: python setup/verify_environment.py")
    
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
