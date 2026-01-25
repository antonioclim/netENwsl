#!/usr/bin/env python3
"""
Environment Verification Script — Week 10
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Checks that all prerequisites are installed and configured correctly
for the Week 10 Application Layer Protocols laboratory.

WSL2 + Ubuntu 22.04 + Docker + Portainer Environment
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
# CHECKER_CLASS
# ═══════════════════════════════════════════════════════════════════════════════
class Checker:
    """Verification result collector with formatted output."""

    def __init__(self) -> None:
        self.passed = 0
        self.failed = 0
        self.warnings = 0

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

    def warn(self, name: str, message: str) -> None:
        """Record a warning."""
        print(f"  [\033[93mWARN\033[0m] {name}: {message}")
        self.warnings += 1

    def info(self, name: str, message: str) -> None:
        """Display informational message."""
        print(f"  [\033[94mINFO\033[0m] {name}: {message}")

    def summary(self) -> int:
        """Print summary and return exit code."""
        print()
        print("=" * 60)
        total = self.passed + self.failed
        print(f"Results: {self.passed}/{total} passed, "
              f"{self.failed} failed, {self.warnings} warnings")
        print()

        if self.failed == 0:
            self._print_success_message()
            return 0
        else:
            self._print_failure_message()
            return 1

    def _print_success_message(self) -> None:
        """Print success message with next steps."""
        print("\033[92m✓ Environment is ready for Week 10 laboratory!\033[0m")
        print()
        print("Next steps:")
        print("  1. Start the lab: python3 scripts/start_lab.py")
        print("  2. Test HTTP:     curl http://localhost:8000/")
        print("  3. Test DNS:      dig @127.0.0.1 -p 5353 web.lab.local")
        print()
        print("Access points:")
        print("  Portainer:    http://localhost:9000 (stud/studstudstud)")
        print("  HTTP Server:  http://localhost:8000")
        print("  DNS Server:   localhost:5353/udp")
        print("  SSH Server:   localhost:2222 (labuser/labpass)")
        print("  FTP Server:   localhost:2121 (labftp/labftp)")

    def _print_failure_message(self) -> None:
        """Print failure message with fix suggestion."""
        print("\033[91m✗ Please fix the issues above before proceeding.\033[0m")
        print()
        print("For automated fixes, try: python3 setup/install_prerequisites.py")


# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def get_command_output(cmd: list, timeout: int = 10) -> Tuple[bool, str]:
    """Execute command and return success status with output."""
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=timeout, text=True)
        output = result.stdout.strip() or result.stderr.strip()
        return result.returncode == 0, output
    except FileNotFoundError:
        return False, "Command not found"
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, str(e)


def check_command_exists(cmd: str) -> bool:
    """Check if command is available in PATH."""
    return shutil.which(cmd) is not None


# ═══════════════════════════════════════════════════════════════════════════════
# WSL_CHECKS
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


def get_wsl_distro_info() -> Tuple[str, str]:
    """Get WSL distribution name and version."""
    distro_name = os.environ.get("WSL_DISTRO_NAME", "Unknown")
    version = _get_ubuntu_version()
    return distro_name, version


def _get_ubuntu_version() -> str:
    """Extract Ubuntu version from system."""
    try:
        result = subprocess.run(
            ["lsb_release", "-rs"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    # Fallback to os-release
    try:
        with open("/etc/os-release", "r") as f:
            for line in f:
                if line.startswith("VERSION_ID="):
                    return line.split("=")[1].strip().strip('"')
    except Exception:
        pass
    return "Unknown"


def verify_wsl_environment(checker: Checker) -> bool:
    """Verify WSL2 environment."""
    print("\033[1mWSL2 Environment:\033[0m")
    is_wsl = check_running_in_wsl()
    checker.check("Running in WSL", is_wsl, "Run this script from WSL Ubuntu terminal")

    if is_wsl:
        distro_name, distro_version = get_wsl_distro_info()
        checker.info("WSL Distribution", distro_name)
        is_ubuntu_22 = distro_version.startswith("22.")
        checker.check(
            f"Ubuntu version {distro_version}",
            is_ubuntu_22,
            "Recommended: Ubuntu 22.04 LTS"
        )
    print()
    return is_wsl


# ═══════════════════════════════════════════════════════════════════════════════
# PYTHON_CHECKS
# ═══════════════════════════════════════════════════════════════════════════════
def check_python_version() -> Tuple[bool, str]:
    """Verify Python version meets requirements."""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    meets_req = version >= (3, 11)
    return meets_req, version_str


def check_python_package(package: str) -> bool:
    """Check if Python package is installed."""
    try:
        __import__(package.replace("-", "_"))
        return True
    except ImportError:
        return False


def verify_python_environment(checker: Checker) -> None:
    """Verify Python environment and packages."""
    print("\033[1mPython Environment:\033[0m")
    py_ok, py_version = check_python_version()
    checker.check(
        f"Python {py_version}", py_ok,
        "Install Python 3.11+: sudo apt install python3.11"
    )

    packages = {
        "docker": "pip install docker --break-system-packages",
        "requests": "pip install requests --break-system-packages",
        "flask": "pip install flask --break-system-packages",
    }
    for pkg, install_cmd in packages.items():
        installed = check_python_package(pkg)
        checker.check(f"Python package: {pkg}", installed, install_cmd)
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# DOCKER_CHECKS
# ═══════════════════════════════════════════════════════════════════════════════
def check_docker_running() -> Tuple[bool, str]:
    """Verify Docker daemon is running."""
    success, output = get_command_output(["docker", "info"])
    if success:
        return True, "Docker daemon is running"
    return False, output


def check_docker_compose() -> Tuple[bool, str]:
    """Verify Docker Compose is available."""
    success, output = get_command_output(["docker", "compose", "version"])
    if success:
        return True, output.split('\n')[0] if output else "Available"
    return False, "Docker Compose not found"


def try_start_docker() -> bool:
    """Attempt to start Docker service."""
    print("         \033[93mAttempting to start Docker...\033[0m")
    try:
        result = subprocess.run(
            ["sudo", "service", "docker", "start"],
            capture_output=True, timeout=30
        )
        if result.returncode == 0:
            import time
            time.sleep(2)
            success, _ = check_docker_running()
            return success
    except Exception:
        pass
    return False


def verify_docker_environment(checker: Checker) -> None:
    """Verify Docker environment."""
    print("\033[1mDocker Environment:\033[0m")
    checker.check(
        "Docker CLI installed",
        check_command_exists("docker"),
        "Install Docker: sudo apt install docker.io"
    )

    docker_ok, docker_msg = check_docker_running()
    if not docker_ok:
        docker_ok = try_start_docker()
        docker_msg = "Started successfully" if docker_ok else "Failed to start"

    checker.check(
        f"Docker daemon: {docker_msg[:40]}",
        docker_ok,
        "Start Docker: sudo service docker start"
    )

    compose_ok, compose_msg = check_docker_compose()
    checker.check(
        f"Docker Compose: {compose_msg[:40]}",
        compose_ok,
        "Included with docker.io package"
    )
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# PORTAINER_CHECKS
# ═══════════════════════════════════════════════════════════════════════════════
def check_portainer_running() -> Tuple[bool, str]:
    """Check if Portainer is running on port 9000."""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=portainer",
             "--format", "{{.Status}}"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            if "up" in result.stdout.lower():
                return True, result.stdout.strip()
        return False, "Not running"
    except Exception as e:
        return False, str(e)


def verify_portainer(checker: Checker) -> None:
    """Verify Portainer status."""
    print("\033[1mPortainer (Global Service - Port 9000):\033[0m")
    portainer_ok, portainer_msg = check_portainer_running()
    checker.check(
        f"Portainer: {portainer_msg}",
        portainer_ok,
        "Start: docker start portainer"
    )

    if portainer_ok:
        checker.info("Portainer URL", "http://localhost:9000")
        checker.info("Credentials", "stud / studstudstud")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK_TOOLS_CHECKS
# ═══════════════════════════════════════════════════════════════════════════════
def check_curl() -> Tuple[bool, str]:
    """Check for curl installation."""
    success, output = get_command_output(["curl", "--version"])
    if success:
        return True, output.split('\n')[0] if output else "Available"
    return False, "Not found"


def check_dig() -> Tuple[bool, str]:
    """Check for dig (DNS lookup) installation."""
    success, output = get_command_output(["dig", "-v"])
    if success or "DiG" in output:
        return True, "Available"
    return False, "Not found (install dnsutils)"


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


def verify_network_tools(checker: Checker) -> None:
    """Verify network diagnostic tools."""
    print("\033[1mNetwork Tools:\033[0m")

    curl_ok, curl_msg = check_curl()
    checker.check(f"curl: {curl_msg[:40]}", curl_ok, "Install: sudo apt install curl")

    dig_ok, dig_msg = check_dig()
    checker.check(f"dig: {dig_msg[:40]}", dig_ok, "Install: sudo apt install dnsutils")

    ws_ok, ws_msg = check_wireshark()
    checker.check(
        f"Wireshark: {ws_msg[:40]}", ws_ok,
        "Install on Windows from wireshark.org"
    )
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# PROJECT_STRUCTURE_CHECKS
# ═══════════════════════════════════════════════════════════════════════════════
def verify_project_structure(checker: Checker) -> None:
    """Verify project directory structure and files."""
    print("\033[1mProject Structure:\033[0m")
    project_root = Path(__file__).parent.parent

    required_dirs = ["docker", "src", "scripts", "tests"]
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        checker.check(f"Directory: {dir_name}/", dir_path.is_dir())

    required_files = [
        "docker/docker-compose.yml",
        "docker/www/index.html",
        "docker/dns-server/Dockerfile",
        "docker/ssh-server/Dockerfile",
        "docker/ftp-server/Dockerfile",
        "src/exercises/ex_10_01_tls_rest_crud.py",
        "src/exercises/ex_10_02_richardson_maturity.py",
    ]
    for file_path in required_files:
        full_path = project_root / file_path
        checker.check(f"File: {file_path}", full_path.is_file())


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def print_header() -> None:
    """Print verification header."""
    print()
    print("=" * 60)
    print("  Environment Verification for Week 10 Laboratory")
    print("  Application Layer Protocols: HTTP, REST, DNS, SSH, FTP")
    print("  Computer Networks — ASE, CSIE")
    print("  WSL2 + Ubuntu 22.04 + Docker + Portainer")
    print("=" * 60)
    print()


def main() -> int:
    """
    Main verification routine.

    💭 PREDICTION: Which check is most likely to fail on a fresh WSL install?
    """
    print_header()
    checker = Checker()

    verify_wsl_environment(checker)
    verify_python_environment(checker)
    verify_docker_environment(checker)
    verify_portainer(checker)
    verify_network_tools(checker)
    verify_project_structure(checker)

    return checker.summary()


if __name__ == "__main__":
    sys.exit(main())
