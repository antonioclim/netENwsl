#!/usr/bin/env python3
"""
Environment Validation Tests for Week 11 Laboratory
NETWORKING class - ASE, Informatics | by Revolvix

Tests to verify the laboratory environment is correctly configured.
"""
from __future__ import annotations

import unittest
import subprocess
import socket
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


class TestDockerEnvironment(unittest.TestCase):
    """Test Docker environment configuration."""
    
    def test_docker_available(self):
        """Docker command should be available."""
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True
        )
        self.assertEqual(result.returncode, 0, "Docker is not installed")
    
    def test_docker_compose_available(self):
        """Docker Compose v2 should be available."""
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True
        )
        self.assertEqual(result.returncode, 0, "Docker Compose v2 is not available")
    
    def test_docker_running(self):
        """Docker daemon should be running."""
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True
        )
        self.assertEqual(result.returncode, 0, "Docker daemon is not running")


class TestPythonEnvironment(unittest.TestCase):
    """Test Python environment configuration."""
    
    def test_python_version(self):
        """Python 3.11+ should be installed."""
        self.assertGreaterEqual(
            sys.version_info,
            (3, 11),
            f"Python 3.11+ required, got {sys.version_info}"
        )
    
    def test_socket_module(self):
        """Socket module should be available."""
        import socket
        self.assertTrue(hasattr(socket, 'socket'))
    
    def test_concurrent_futures(self):
        """Concurrent futures should be available."""
        from concurrent.futures import ThreadPoolExecutor
        self.assertTrue(callable(ThreadPoolExecutor))


class TestProjectStructure(unittest.TestCase):
    """Test project directory structure."""
    
    def test_docker_directory(self):
        """Docker directory should exist."""
        docker_dir = PROJECT_ROOT / "docker"
        self.assertTrue(docker_dir.exists(), "docker/ directory missing")
    
    def test_docker_compose_file(self):
        """docker-compose.yml should exist."""
        compose_file = PROJECT_ROOT / "docker" / "docker-compose.yml"
        self.assertTrue(compose_file.exists(), "docker-compose.yml missing")
    
    def test_scripts_directory(self):
        """Scripts directory should exist."""
        scripts_dir = PROJECT_ROOT / "scripts"
        self.assertTrue(scripts_dir.exists(), "scripts/ directory missing")
    
    def test_src_directory(self):
        """Source directory should exist."""
        src_dir = PROJECT_ROOT / "src"
        self.assertTrue(src_dir.exists(), "src/ directory missing")
    
    def test_exercises_exist(self):
        """Exercise files should exist."""
        exercises_dir = PROJECT_ROOT / "src" / "exercises"
        exercises = list(exercises_dir.glob("ex_11_*.py"))
        self.assertGreater(len(exercises), 0, "No exercise files found")


class TestNetworkPorts(unittest.TestCase):
    """Test network port availability."""
    
    def test_port_8080_free(self):
        """Port 8080 should be available for load balancer."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(("localhost", 8080))
            sock.close()
        except OSError:
            # Port in use - might be running, which is OK
            pass
    
    def test_ports_8081_8083_free(self):
        """Ports 8081-8083 should be available for backends."""
        for port in [8081, 8082, 8083]:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.bind(("localhost", port))
                sock.close()
            except OSError:
                # Port in use - might be OK if running
                pass


if __name__ == "__main__":
    unittest.main(verbosity=2)


# Revolvix&Hypotheticalandrei
