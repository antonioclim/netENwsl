#!/usr/bin/env python3
"""
Environment Validation Tests
NETWORKING class - ASE, Informatics | by Revolvix

Tests to verify the laboratory environment is correctly configured.
"""

import subprocess
import sys
import socket
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


class TestEnvironment(unittest.TestCase):
    """Test environment prerequisites."""
    
    def test_python_version(self):
        """Python version should be 3.11 or higher."""
        version = sys.version_info
        self.assertGreaterEqual(version[:2], (3, 11),
                               f"Python 3.11+ required, got {version[0]}.{version[1]}")
    
    def test_docker_available(self):
        """Docker command should be available."""
        result = subprocess.run(["docker", "--version"],
                               capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, "Docker not found")
    
    def test_docker_compose_available(self):
        """Docker Compose should be available."""
        result = subprocess.run(["docker", "compose", "version"],
                               capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, "Docker Compose not available")
    
    def test_project_structure(self):
        """Required project directories should exist."""
        required_dirs = ["docker", "scripts", "src", "tests", "docs"]
        for dir_name in required_dirs:
            dir_path = PROJECT_ROOT / dir_name
            self.assertTrue(dir_path.is_dir(),
                           f"Directory missing: {dir_name}")
    
    def test_compose_file_exists(self):
        """Docker compose file should exist."""
        compose_file = PROJECT_ROOT / "docker" / "docker-compose.yml"
        self.assertTrue(compose_file.is_file(),
                       "docker-compose.yml not found")


class TestPythonPackages(unittest.TestCase):
    """Test required Python packages."""
    
    def test_docker_package(self):
        """docker package should be importable."""
        try:
            import docker
        except ImportError:
            self.fail("docker package not installed")
    
    def test_yaml_package(self):
        """yaml package should be importable."""
        try:
            import yaml
        except ImportError:
            self.fail("pyyaml package not installed")
    
    def test_requests_package(self):
        """requests package should be importable."""
        try:
            import requests
        except ImportError:
            self.fail("requests package not installed")


class TestServiceConnectivity(unittest.TestCase):
    """Test service connectivity (requires running containers)."""
    
    def _check_port(self, port: int, timeout: float = 2.0) -> bool:
        """Check if port is accepting connections."""
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=timeout):
                return True
        except Exception:
            return False
    
    def test_mqtt_plaintext_port(self):
        """MQTT plaintext port should be accessible."""
        if not self._check_port(1883):
            self.skipTest("MQTT service not running on port 1883")
    
    def test_mqtt_tls_port(self):
        """MQTT TLS port should be accessible."""
        if not self._check_port(8883):
            self.skipTest("MQTT TLS service not running on port 8883")
    
    def test_dvwa_port(self):
        """DVWA HTTP port should be accessible."""
        if not self._check_port(8080):
            self.skipTest("DVWA service not running on port 8080")
    
    def test_ftp_port(self):
        """FTP port should be accessible."""
        if not self._check_port(2121):
            self.skipTest("FTP service not running on port 2121")


if __name__ == "__main__":
    unittest.main(verbosity=2)
