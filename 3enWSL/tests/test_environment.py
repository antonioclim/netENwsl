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

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestDockerEnvironment(unittest.TestCase):
    """Test Docker container configuration."""

    def test_docker_available(self):
        """Docker command should be available."""
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True
        )
        self.assertEqual(result.returncode, 0, "Docker is not available")

    def test_docker_compose_available(self):
        """Docker Compose should be available."""
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True
        )
        self.assertEqual(result.returncode, 0, "Docker Compose is not available")

    def test_compose_file_valid(self):
        """docker-compose.yml should be valid YAML."""
        compose_file = PROJECT_ROOT / "docker" / "docker-compose.yml"
        self.assertTrue(compose_file.exists(), "docker-compose.yml not found")
        
        result = subprocess.run(
            ["docker", "compose", "-f", str(compose_file), "config", "-q"],
            capture_output=True
        )
        self.assertEqual(
            result.returncode, 0,
            f"Invalid docker-compose.yml: {result.stderr.decode()}"
        )


class TestContainerStatus(unittest.TestCase):
    """Test running containers."""

    def test_server_container_running(self):
        """Server container should be running."""
        result = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Running}}", "week3_server"],
            capture_output=True,
            text=True
        )
        self.assertEqual(
            result.stdout.strip(), "true",
            "Server container is not running"
        )

    def test_router_container_running(self):
        """Router container should be running."""
        result = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Running}}", "week3_router"],
            capture_output=True,
            text=True
        )
        self.assertEqual(
            result.stdout.strip(), "true",
            "Router container is not running"
        )

    def test_client_container_running(self):
        """Client container should be running."""
        result = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Running}}", "week3_client"],
            capture_output=True,
            text=True
        )
        self.assertEqual(
            result.stdout.strip(), "true",
            "Client container is not running"
        )


class TestNetworkConnectivity(unittest.TestCase):
    """Test network connectivity between containers."""

    def test_client_can_reach_server(self):
        """Client should be able to ping server."""
        result = subprocess.run(
            ["docker", "exec", "week3_client", "ping", "-c", "1", "-W", "2", "server"],
            capture_output=True
        )
        self.assertEqual(
            result.returncode, 0,
            "Client cannot reach server"
        )

    def test_client_can_reach_router(self):
        """Client should be able to ping router."""
        result = subprocess.run(
            ["docker", "exec", "week3_client", "ping", "-c", "1", "-W", "2", "router"],
            capture_output=True
        )
        self.assertEqual(
            result.returncode, 0,
            "Client cannot reach router"
        )


class TestProjectStructure(unittest.TestCase):
    """Test project directory structure."""

    def test_required_directories_exist(self):
        """All required directories should exist."""
        required_dirs = [
            "docker",
            "scripts",
            "src",
            "src/exercises",
            "src/apps",
            "tests",
            "docs",
            "pcap",
        ]
        
        for dir_name in required_dirs:
            dir_path = PROJECT_ROOT / dir_name
            self.assertTrue(
                dir_path.is_dir(),
                f"Directory not found: {dir_name}"
            )

    def test_exercise_files_exist(self):
        """Exercise Python files should exist."""
        exercises_dir = PROJECT_ROOT / "src" / "exercises"
        
        expected_files = [
            "ex_3_01_udp_broadcast.py",
            "ex_3_02_udp_multicast.py",
            "ex_3_03_tcp_tunnel.py",
        ]
        
        for filename in expected_files:
            file_path = exercises_dir / filename
            self.assertTrue(
                file_path.is_file(),
                f"Exercise file not found: {filename}"
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
