#!/usr/bin/env python3
"""
Environment Verification Script
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment

Checks that all prerequisites are installed and configured correctly
for the Week 11 FTP, DNS, SSH & Load Balancing laboratory.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import sys
import shutil
import os
from pathlib import Path
from typing import Tuple



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class Checker:
    """Verification result collector with formatted output."""
    

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
    

# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
    def check(self, name: str, condition: bool, fix_hint: str = "") -> bool:
        """Record a check result."""
        if condition:
            print(f"  [\033[92mPASS\033[0m] {name}")
            self.passed += 1
        else:
            print(f"  [\033[91mFAIL\033[0m] {name}")
            if fix_hint:
                print(f"         \033[93mFix:\033[0m {fix_hint}")
            self.failed += 1
        return condition
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def warn(self, name: str, message: str) -> None:
        """Record a warning."""
        print(f"  [\033[93mWARN\033[0m] {name}: {message}")
        self.warnings += 1
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def info(self, name: str, message: str) -> None:
        """Display informational message."""
        print(f"  [\033[94mINFO\033[0m] {name}: {message}")
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def summary(self) -> int:
        """Print summary and return exit code."""
        print()
        print("=" * 60)
        total = self.passed + self.failed
        print(f"Results: {self.passed}/{total} passed, {self.failed} failed, {self.warnings} warnings")
        print()
        
        if self.failed == 0:
            print("\033[92m✓ Environment is ready for Week 11 laboratory!\033[0m")
            print()
            print("Next steps:")
            print("  1. Start the lab: python3 scripts/start_lab.py")
            print("  2. Test LB:       curl http://localhost:8080/")
            print("  3. Run demo:      python3 scripts/run_demo.py --demo 1")
            print()
            print("Access points:")
            print("  Portainer:    http://localhost:9000 (stud/studstudstud)")
            print("  Nginx LB:     http://localhost:8080")
            print("  Health:       http://localhost:8080/health")
            return 0
        else:
            print("\033[91m✗ Please fix the issues above before proceeding.\033[0m")
            print()
            print("For automated fixes, try: python3 setup/install_prerequisites.py")
            return 1



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_running_in_wsl() -> bool:
    """Check if we're running inside WSL."""
    if os.path.exists("/proc/sys/fs/binfmt_misc/WSLInterop"):
        return True
    if "WSL_DISTRO_NAME" in os.environ:
        return True
    try:
        with open("/proc/version", "r") as f:
            version = f.read().lower()
            return "microsoft" in version or "wsl" in version
    except (FileNotFoundError, IOError):
        pass
    return False



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def get_wsl_distro_info() -> Tuple[str, str]:
    """Get WSL distribution name and version."""
    distro_name = os.environ.get("WSL_DISTRO_NAME", "Unknown")
    version = "Unknown"
    try:
        result = subprocess.run(
            ["lsb_release", "-rs"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip()
    except Exception:
        try:
            with open("/etc/os-release", "r") as f:
                for line in f:
                    if line.startswith("VERSION_ID="):
                        version = line.split("=")[1].strip().strip('"')
                        break
        except Exception:
            pass
    return distro_name, version



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def get_command_output(cmd: list, timeout: int = 10) -> Tuple[bool, str]:
    """Execute command and return success status with output."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=timeout,
            text=True
        )
        output = result.stdout.strip() or result.stderr.strip()
        return result.returncode == 0, output
    except FileNotFoundError:
        return False, "Command not found"
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, str(e)



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_command_exists(cmd: str) -> bool:
    """Check if command is available in PATH."""
    return shutil.which(cmd) is not None



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_python_version() -> Tuple[bool, str]:
    """Verify Python version meets requirements."""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    meets_req = version >= (3, 11)
    return meets_req, version_str



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_python_package(package: str) -> bool:
    """Check if Python package is installed."""
    try:
        __import__(package.replace("-", "_"))
        return True
    except ImportError:
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_docker_running() -> Tuple[bool, str]:
    """Verify Docker daemon is running."""
    success, output = get_command_output(["docker", "info"])
    if success:
        return True, "Docker daemon is running"
    return False, output



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_docker_compose() -> Tuple[bool, str]:
    """Verify Docker Compose is available."""
    success, output = get_command_output(["docker", "compose", "version"])
    if success:
        return True, output.split('\n')[0] if output else "Available"
    return False, "Docker Compose not found"



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_portainer_running() -> Tuple[bool, str]:
    """Check if Portainer is running on port 9000."""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=portainer",
             "--format", "{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            if "up" in result.stdout.lower():
                return True, result.stdout.strip()
        return False, "Not running"
    except Exception as e:
        return False, str(e)



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_wireshark() -> Tuple[bool, str]:
    """Check for Wireshark installation."""
    windows_paths = [
        Path("/mnt/c/Program Files/Wireshark/Wireshark.exe"),
        Path("/mnt/c/Program Files (x86)/Wireshark/Wireshark.exe"),
    ]
    
    for path in windows_paths:
        if path.exists():
            return True, str(path)
    
    if check_command_exists("wireshark"):
        return True, "Available in PATH"
    
    if check_command_exists("tshark"):
        return True, "tshark available (CLI mode)"
    
    return False, "Not found"



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_curl() -> Tuple[bool, str]:
    """Check for curl installation."""
    success, output = get_command_output(["curl", "--version"])
    if success:
        return True, output.split('\n')[0] if output else "Available"
    return False, "Not found"



# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
def try_start_docker() -> bool:
    """Attempt to start Docker service."""
    print("         \033[93mAttempting to start Docker...\033[0m")
    try:
        result = subprocess.run(
            ["sudo", "service", "docker", "start"],
            capture_output=True,
            timeout=30
        )
        if result.returncode == 0:
            import time
            time.sleep(2)
            success, _ = check_docker_running()
            return success
    except Exception:
        pass
    return False



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main verification routine."""
    print()
    print("=" * 60)
    print("  Environment Verification for Week 11 Laboratory")
    print("  FTP, DNS, SSH & Load Balancing")
    print("  NETWORKING class - ASE, Informatics")
    print("  WSL2 + Ubuntu 22.04 + Docker + Portainer")
    print("=" * 60)
    print()
    
    c = Checker()
    
    # WSL2 Environment
    print("\033[1mWSL2 Environment:\033[0m")
    is_wsl = check_running_in_wsl()
    c.check(
        "Running in WSL",
        is_wsl,
        "Run this script from WSL Ubuntu terminal"
    )
    
    if is_wsl:
        distro_name, distro_version = get_wsl_distro_info()
        c.info("WSL Distribution", distro_name)
        is_ubuntu_22 = distro_version.startswith("22.")
        c.check(
            f"Ubuntu version {distro_version}",
            is_ubuntu_22,
            "Recommended: Ubuntu 22.04 LTS"
        )
    
    print()
    
    # Python Environment
    print("\033[1mPython Environment:\033[0m")
    py_ok, py_version = check_python_version()
    c.check(
        f"Python {py_version}",
        py_ok,
        "Install Python 3.11+: sudo apt install python3.11"
    )
    
    optional_packages = {
        "docker": "pip install docker --break-system-packages",
        "requests": "pip install requests --break-system-packages",
    }
    
    for pkg, install_cmd in optional_packages.items():
        if check_python_package(pkg):
            c.check(f"Python package: {pkg}", True)
        else:
            c.check(f"Python package: {pkg}", False, install_cmd)
    
    print()
    
    # Docker Environment
    print("\033[1mDocker Environment:\033[0m")
    c.check(
        "Docker CLI installed",
        check_command_exists("docker"),
        "Install Docker: sudo apt install docker.io"
    )
    
    docker_ok, docker_msg = check_docker_running()
    if not docker_ok:
        docker_ok = try_start_docker()
        docker_msg = "Started successfully" if docker_ok else "Failed to start"
    
    c.check(
        f"Docker daemon: {docker_msg[:40]}",
        docker_ok,
        "Start Docker: sudo service docker start"
    )
    
    compose_ok, compose_msg = check_docker_compose()
    c.check(
        f"Docker Compose: {compose_msg[:40]}",
        compose_ok,
        "Included with docker.io package"
    )
    
    print()
    
    # Portainer (Global Service)
    print("\033[1mPortainer (Global Service - Port 9000):\033[0m")
    portainer_ok, portainer_msg = check_portainer_running()
    c.check(
        f"Portainer: {portainer_msg}",
        portainer_ok,
        "Start: docker start portainer"
    )
    
    if portainer_ok:
        c.info("Portainer URL", "http://localhost:9000")
        c.info("Credentials", "stud / studstudstud")
    
    print()
    
    # Network Tools
    print("\033[1mNetwork Tools:\033[0m")
    curl_ok, curl_msg = check_curl()
    c.check(
        f"curl: {curl_msg[:40]}",
        curl_ok,
        "Install: sudo apt install curl"
    )
    
    ws_ok, ws_msg = check_wireshark()
    c.check(
        f"Wireshark: {ws_msg[:40]}",
        ws_ok,
        "Install on Windows from wireshark.org"
    )
    
    print()
    
    # Project Structure
    print("\033[1mProject Structure:\033[0m")
    project_root = Path(__file__).parent.parent
    
    required_dirs = ["docker", "src", "scripts", "tests"]
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        c.check(f"Directory: {dir_name}/", dir_path.is_dir())
    
    required_files = [
        "docker/docker-compose.yml",
        "docker/configs/nginx.conf",
        "src/exercises/ex_11_01_backend.py",
        "src/exercises/ex_11_02_loadbalancer.py",
        "src/exercises/ex_11_03_dns_client.py",
    ]
    for file_path in required_files:
        full_path = project_root / file_path
        c.check(f"File: {file_path}", full_path.is_file())
    
    return c.summary()


if __name__ == "__main__":
    sys.exit(main())
