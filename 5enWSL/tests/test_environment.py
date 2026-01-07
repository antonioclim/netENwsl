#!/usr/bin/env python3
"""
Environment Validation Tests
NETWORKING class - ASE, Informatics | by Revolvix

Tests to verify the laboratory environment is correctly configured.
"""

import subprocess
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


class TestEnvironment(unittest.TestCase):
    """Test environment configuration."""
    
    def test_python_version(self):
        """Verify Python version is 3.10+."""
        self.assertGreaterEqual(
            sys.version_info[:2],
            (3, 10),
            "Python 3.10 or later is required"
        )
    
    def test_ipaddress_module(self):
        """Verify ipaddress module is available."""
        import ipaddress
        self.assertIsNotNone(ipaddress.ip_address)
    
    def test_project_structure(self):
        """Verify project directory structure."""
        required_dirs = [
            "docker",
            "scripts",
            "src",
            "src/exercises",
            "src/apps",
            "src/utils",
            "tests",
            "docs",
        ]
        
        for dir_name in required_dirs:
            dir_path = PROJECT_ROOT / dir_name
            self.assertTrue(
                dir_path.exists(),
                f"Directory {dir_name} should exist"
            )
    
    def test_docker_compose_exists(self):
        """Verify docker-compose.yml exists."""
        compose_file = PROJECT_ROOT / "docker" / "docker-compose.yml"
        self.assertTrue(
            compose_file.exists(),
            "docker-compose.yml should exist"
        )
    
    def test_exercise_files_exist(self):
        """Verify exercise files exist."""
        exercise_files = [
            "src/exercises/ex_5_01_cidr_flsm.py",
            "src/exercises/ex_5_02_vlsm_ipv6.py",
        ]
        
        for file_path in exercise_files:
            full_path = PROJECT_ROOT / file_path
            self.assertTrue(
                full_path.exists(),
                f"Exercise file {file_path} should exist"
            )


class TestDockerAvailability(unittest.TestCase):
    """Test Docker availability (may be skipped if Docker not running)."""
    
    @classmethod
    def setUpClass(cls):
        """Check if Docker is available."""
        try:
            result = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                timeout=10
            )
            cls.docker_available = result.returncode == 0
        except Exception:
            cls.docker_available = False
    
    def test_docker_running(self):
        """Verify Docker daemon is running."""
        if not self.docker_available:
            self.skipTest("Docker is not running")
        self.assertTrue(self.docker_available)
    
    def test_docker_compose_available(self):
        """Verify Docker Compose is available."""
        if not self.docker_available:
            self.skipTest("Docker is not running")
        
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True
        )
        self.assertEqual(
            result.returncode,
            0,
            "Docker Compose should be available"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
