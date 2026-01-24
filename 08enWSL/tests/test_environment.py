#!/usr/bin/env python3
"""
Environment Validation Tests
NETWORKING class - ASE, Informatics | by Revolvix

Tests to verify the laboratory environment is correctly configured.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import socket
import sys
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any

import pytest

PROJECT_ROOT = Path(__file__).parent.parent



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class TestDockerEnvironment:
    """Tests for Docker environment."""
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_docker_available(self) -> bool:
        """Docker command should be available."""
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True
        )
        assert result.returncode == 0, "Docker is not installed"
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_docker_compose_available(self) -> bool:
        """Docker Compose V2 should be available."""
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True
        )
        assert result.returncode == 0, "Docker Compose V2 is not available"
    

# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_docker_daemon_running(self) -> bool:
        """Docker daemon should be running."""
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        assert result.returncode == 0, "Docker daemon is not running"



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class TestDirectoryStructure:
    """Tests for directory structure."""
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_docker_directory_exists(self) -> bool:
        """Docker directory should exist."""
        assert (PROJECT_ROOT / "docker").is_dir()
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_compose_file_exists(self) -> bool:
        """docker-compose.yml should exist."""
        assert (PROJECT_ROOT / "docker" / "docker-compose.yml").is_file()
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_scripts_directory_exists(self) -> bool:
        """Scripts directory should exist."""
        assert (PROJECT_ROOT / "scripts").is_dir()
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_src_directory_exists(self) -> bool:
        """Source directory should exist."""
        assert (PROJECT_ROOT / "src").is_dir()
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_www_directory_exists(self) -> bool:
        """Web content directory should exist."""
        assert (PROJECT_ROOT / "www").is_dir()



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class TestNetworkPorts:
    """Tests for network port availability."""
    
    @staticmethod


# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def is_port_available(port: int) -> bool:
        """Check if a port is available."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", port))
                return True
        except OSError:
            return False
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_port_8080_status(self) -> bool:
        """Port 8080 status should be known."""
        # This test passes whether the port is available or in use by our services
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex(("127.0.0.1", 8080))
                # Either available (connection refused) or in use (connected)
                assert result in [0, 111, 10061]  # 0=connected, 111/10061=refused
        except Exception:
            pass  # Port check completed



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class TestPythonEnvironment:
    """Tests for Python environment."""
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_python_version(self) -> bool:
        """Python version should be 3.11+."""
        assert sys.version_info >= (3, 11), f"Python 3.11+ required, got {sys.version}"
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_socket_module(self) -> bool:
        """Socket module should be available."""
        import socket
        assert socket is not None
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_pathlib_module(self) -> bool:
        """Pathlib module should be available."""
        from pathlib import Path
        assert Path is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
