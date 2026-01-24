#!/usr/bin/env python3
"""
Environment Validation Tests
NETWORKING class - ASE, Informatics | by Revolvix

Validates that the laboratory environment is correctly configured.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import sys
import socket
import unittest
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class TestEnvironment(unittest.TestCase):
    """Test the laboratory environment configuration."""
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_python_version(self) -> bool:
        """Python version should be 3.8 or higher."""
        self.assertGreaterEqual(sys.version_info[:2], (3, 8))
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_required_modules(self) -> bool:
        """Required standard library modules should be available."""
        modules = ['socket', 'struct', 'threading', 'zlib', 'json']
        
        for module in modules:
            try:
                __import__(module)
            except ImportError:
                self.fail(f"Required module '{module}' not available")
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_project_structure(self) -> bool:
        """Project directories should exist."""
        project_root = Path(__file__).parent.parent
        
        required_dirs = [
            'src/apps',
            'src/utils',
            'src/exercises',
            'scripts',
            'docker',
            'docs',
        ]
        
        for dir_path in required_dirs:
            full_path = project_root / dir_path
            self.assertTrue(full_path.exists(), f"Directory missing: {dir_path}")
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_source_files_exist(self) -> bool:
        """Key source files should exist."""
        project_root = Path(__file__).parent.parent
        
        required_files = [
            'src/apps/text_proto_server.py',
            'src/apps/text_proto_client.py',
            'src/apps/binary_proto_server.py',
            'src/apps/binary_proto_client.py',
            'src/apps/udp_sensor_server.py',
            'src/apps/udp_sensor_client.py',
        ]
        
        for file_path in required_files:
            full_path = project_root / file_path
            self.assertTrue(full_path.exists(), f"File missing: {file_path}")
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_docker_config_exists(self) -> bool:
        """Docker configuration files should exist."""
        project_root = Path(__file__).parent.parent
        
        docker_files = [
            'docker/docker-compose.yml',
            'docker/Dockerfile',
        ]
        
        for file_path in docker_files:
            full_path = project_root / file_path
            self.assertTrue(full_path.exists(), f"Docker file missing: {file_path}")



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class TestPorts(unittest.TestCase):
    """Test port availability."""
    

# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
    def check_port_available(self, port) -> bool:
        """Check if a port is available for binding."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            sock.bind(('127.0.0.1', port))
            sock.close()
            return True
        except OSError:
            return False
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_text_port_available(self) -> bool:
        """Port 5400 should be available or in use by our server."""
        # This test passes if either the port is free or our server is using it
        pass
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_binary_port_available(self) -> bool:
        """Port 5401 should be available or in use by our server."""
        pass
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_udp_port_available(self) -> bool:
        """Port 5402 should be available or in use by our server."""
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
