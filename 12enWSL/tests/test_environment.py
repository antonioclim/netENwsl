#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_DOCSTRING
# ═══════════════════════════════════════════════════════════════════════════════
"""
Environment Validation Tests
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Tests to verify the laboratory environment is correctly configured.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import sys
import socket
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any

import pytest

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))



# ═══════════════════════════════════════════════════════════════════════════════
# TESTPYTHONENVIRONMENT_CLASS
# ═══════════════════════════════════════════════════════════════════════════════
class TestPythonEnvironment:
    """Tests for Python environment configuration."""
    
    def test_python_version(self) -> bool:
        """Python version should be 3.11 or later."""
        assert sys.version_info >= (3, 11), "Python 3.11+ required"
    
    def test_grpc_import(self) -> bool:
        """gRPC should be importable."""
        import grpc
        assert grpc is not None
    
    def test_protobuf_import(self) -> bool:
        """Protocol Buffers should be importable."""
        import google.protobuf
        assert google.protobuf is not None
    
    def test_xmlrpc_import(self) -> bool:
        """XML-RPC client should be importable."""
        import xmlrpc.client
        assert xmlrpc.client is not None



# ═══════════════════════════════════════════════════════════════════════════════
# TESTPROJECTSTRUCTURE_CLASS
# ═══════════════════════════════════════════════════════════════════════════════
class TestProjectStructure:
    """Tests for project directory structure."""
    
    def test_readme_exists(self) -> bool:
        """README.md should exist."""
        readme = PROJECT_ROOT / "README.md"
        assert readme.exists(), "README.md not found"
    
    def test_docker_compose_exists(self) -> bool:
        """Docker Compose file should exist."""
        compose = PROJECT_ROOT / "docker" / "docker-compose.yml"
        assert compose.exists(), "docker-compose.yml not found"
    
    def test_smtp_server_exists(self) -> bool:
        """SMTP server implementation should exist."""
        smtp_server = PROJECT_ROOT / "src" / "apps" / "email" / "smtp_server.py"
        assert smtp_server.exists(), "smtp_server.py not found"
    
    def test_jsonrpc_server_exists(self) -> bool:
        """JSON-RPC server implementation should exist."""
        jsonrpc_server = PROJECT_ROOT / "src" / "apps" / "rpc" / "jsonrpc" / "jsonrpc_server.py"
        assert jsonrpc_server.exists(), "jsonrpc_server.py not found"



# ═══════════════════════════════════════════════════════════════════════════════
# TESTPORTAVAILABILITY_CLASS
# ═══════════════════════════════════════════════════════════════════════════════
class TestPortAvailability:
    """Tests for port availability (can be skipped if services are running)."""
    
    @pytest.fixture
    def check_port(self) -> bool:
        """Port availability checker."""
        def _check(port: int) -> bool:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    result = s.connect_ex(("127.0.0.1", port))
                    return result == 0
            except Exception:
                return False
        return _check
    
    def test_smtp_port_or_available(self, check_port) -> bool:
        """SMTP port should be in use (running) or available."""
        # This test passes if port is either in use (service running) or free
        port = 1025
        in_use = check_port(port)
        # We just want to know the status, not fail
        if in_use:
            print(f"Port {port} is in use (SMTP server may be running)")
        else:
            print(f"Port {port} is available")
    
    def test_jsonrpc_port_or_available(self, check_port) -> bool:
        """JSON-RPC port should be in use (running) or available."""
        port = 6200
        in_use = check_port(port)
        if in_use:
            print(f"Port {port} is in use (JSON-RPC server may be running)")
        else:
            print(f"Port {port} is available")



# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
