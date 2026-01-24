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
import sys
import unittest
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any

PROJECT_ROOT = Path(__file__).parent.parent



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class TestEnvironment(unittest.TestCase):
    """Test environment configuration."""
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_python_version(self) -> bool:
        """Verify Python version is 3.10+."""
        self.assertGreaterEqual(
            sys.version_info[:2],
            (3, 10),
            "Python 3.10 or later is required"
        )
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_ipaddress_module(self) -> bool:
        """Verify ipaddress module is available."""
        import ipaddress
        self.assertIsNotNone(ipaddress.ip_address)
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_project_structure(self) -> bool:
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
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_docker_compose_exists(self) -> bool:
        """Verify docker-compose.yml exists."""
        compose_file = PROJECT_ROOT / "docker" / "docker-compose.yml"
        self.assertTrue(
            compose_file.exists(),
            "docker-compose.yml should exist"
        )
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_exercise_files_exist(self) -> bool:
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



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class TestDockerAvailability(unittest.TestCase):
    """Test Docker availability (may be skipped if Docker not running)."""
    
    @classmethod


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
    def setUpClass(cls) -> None:
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
    

# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_docker_running(self) -> bool:
        """Verify Docker daemon is running."""
        if not self.docker_available:
            self.skipTest("Docker is not running")
        self.assertTrue(self.docker_available)
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_docker_compose_available(self) -> bool:
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
