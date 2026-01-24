#!/usr/bin/env python3
"""
Environment Validation Tests for Week 9 Laboratory
NETWORKING class - ASE, Informatics | by Revolvix

Verifies that the laboratory environment is correctly configured
and all components are functioning.

Usage:
    python tests/test_environment.py
    python -m pytest tests/test_environment.py -v
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations
from typing import Optional, List, Dict, Tuple, Any

import subprocess
import sys
import socket
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class TestPythonEnvironment:
    """Tests for Python environment."""
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_python_version(self) -> bool:
        """Verify Python version is 3.8 or later."""
        assert sys.version_info >= (3, 8), \
            f"Python 3.8+ required, got {sys.version_info}"
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_required_packages(self) -> bool:
        """Verify required packages are installed."""
        packages = ["struct", "socket", "zlib", "argparse"]
        
        for pkg in packages:
            try:
                __import__(pkg)
            except ImportError:
                assert False, f"Required package not found: {pkg}"
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_optional_packages(self) -> bool:
        """Check optional packages (warnings only)."""
        optional = ["docker", "requests", "yaml"]
        missing = []
        
        for pkg in optional:
            try:
                __import__(pkg)
            except ImportError:
                missing.append(pkg)
        
        if missing:
            print(f"Warning: Optional packages not installed: {missing}")



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class TestDockerEnvironment:
    """Tests for Docker environment."""
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_docker_installed(self) -> bool:
        """Verify Docker is installed."""
        try:
            result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                timeout=5
            )
            assert result.returncode == 0, "Docker command failed"
        except FileNotFoundError:
            assert False, "Docker is not installed"
    

# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_docker_running(self) -> bool:
        """Verify Docker daemon is running."""
        try:
            result = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                timeout=10
            )
            assert result.returncode == 0, "Docker daemon is not running"
        except (subprocess.SubprocessError, FileNotFoundError):
            assert False, "Could not check Docker status"
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_docker_compose(self) -> bool:
        """Verify Docker Compose is available."""
        compose_found = False
        
        # Try docker compose (v2)
        try:
            result = subprocess.run(
                ["docker", "compose", "version"],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                compose_found = True
        except subprocess.SubprocessError:
            pass
        
        # Try docker-compose (v1)
        if not compose_found:
            try:
                result = subprocess.run(
                    ["docker-compose", "--version"],
                    capture_output=True,
                    timeout=5
                )
                if result.returncode == 0:
                    compose_found = True
            except (subprocess.SubprocessError, FileNotFoundError):
                pass
        
        assert compose_found, "Docker Compose is not available"



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class TestProjectStructure:
    """Tests for project file structure."""
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_compose_file_exists(self) -> bool:
        """Verify docker-compose.yml exists."""
        compose_file = PROJECT_ROOT / "docker" / "docker-compose.yml"
        assert compose_file.exists(), f"Missing: {compose_file}"
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_exercise_files_exist(self) -> bool:
        """Verify exercise Python files exist."""
        exercises = PROJECT_ROOT / "src" / "exercises"
        
        required_files = [
            "ex_9_01_endianness.py",
            "ex_9_02_pseudo_ftp.py"
        ]
        
        for filename in required_files:
            filepath = exercises / filename
            assert filepath.exists(), f"Missing exercise: {filepath}"
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_script_files_exist(self) -> bool:
        """Verify management scripts exist."""
        scripts = PROJECT_ROOT / "scripts"
        
        required_scripts = [
            "start_lab.py",
            "stop_lab.py",
            "cleanup.py"
        ]
        
        for filename in required_scripts:
            filepath = scripts / filename
            assert filepath.exists(), f"Missing script: {filepath}"



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class TestNetworkCapabilities:
    """Tests for network capabilities."""
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_localhost_resolution(self) -> bool:
        """Verify localhost resolves correctly."""
        try:
            ip = socket.gethostbyname("localhost")
            assert ip == "127.0.0.1", f"localhost resolved to {ip}"
        except socket.gaierror:
            assert False, "Could not resolve localhost"
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_port_availability(self) -> bool:
        """Check if default ports are available."""
        test_ports = [2121, 60000]
        
        for port in test_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex(('localhost', port))
                sock.close()
                
                # Port should be closed (available) initially
                # or open if services are running
                # Either is acceptable for this test
            except socket.error:
                pass  # Port not accessible, which is fine



# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
def run_tests() -> None:
    """Run all tests and report results."""
    print("=" * 60)
    print("Week 9 Laboratory - Environment Tests")
    print("=" * 60)
    print()
    
    test_classes = [
        TestPythonEnvironment,
        TestDockerEnvironment,
        TestProjectStructure,
        TestNetworkCapabilities
    ]
    
    passed = 0
    failed = 0
    
    for test_class in test_classes:
        print(f"\n{test_class.__name__}:")
        print("-" * 40)
        
        instance = test_class()
        
        for name in dir(instance):
            if name.startswith("test_"):
                try:
                    getattr(instance, name)()
                    print(f"  [PASS] {name}")
                    passed += 1
                except AssertionError as e:
                    print(f"  [FAIL] {name}: {e}")
                    failed += 1
                except Exception as e:
                    print(f"  [ERROR] {name}: {e}")
                    failed += 1
    
    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_tests())
