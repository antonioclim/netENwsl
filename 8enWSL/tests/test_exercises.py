#!/usr/bin/env python3
"""
Exercise Verification Tests
NETWORKING class - ASE, Informatics | by Revolvix

Tests to verify that laboratory exercises are functioning correctly.
"""

import subprocess
import sys
import time
import socket
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
SRC_ROOT = PROJECT_ROOT / "src"


class TestExerciseFiles:
    """Tests for exercise file structure."""
    
    def test_exercise_01_exists(self):
        """Exercise 1 file should exist."""
        ex_file = SRC_ROOT / "exercises" / "ex_8_01_http_server.py"
        assert ex_file.is_file(), f"Exercise file not found: {ex_file}"
    
    def test_exercise_02_exists(self):
        """Exercise 2 file should exist."""
        ex_file = SRC_ROOT / "exercises" / "ex_8_02_reverse_proxy.py"
        assert ex_file.is_file(), f"Exercise file not found: {ex_file}"
    
    def test_exercise_files_syntax(self):
        """All exercise files should have valid Python syntax."""
        exercises_dir = SRC_ROOT / "exercises"
        for py_file in exercises_dir.glob("ex_*.py"):
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(py_file)],
                capture_output=True
            )
            assert result.returncode == 0, f"Syntax error in {py_file.name}: {result.stderr.decode()}"


class TestHTTPServer:
    """Tests for HTTP server functionality (requires Docker environment)."""
    
    @pytest.fixture(autouse=True)
    def check_docker_running(self):
        """Skip if Docker environment is not running."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex(("127.0.0.1", 8080))
                if result != 0:
                    pytest.skip("Docker environment not running (port 8080 closed)")
        except Exception:
            pytest.skip("Cannot check Docker environment")
    
    def test_nginx_responds(self):
        """nginx should respond on port 8080."""
        try:
            with urlopen("http://localhost:8080/", timeout=5) as response:
                assert response.status == 200
        except URLError as e:
            pytest.fail(f"nginx not responding: {e}")
    
    def test_health_endpoint(self):
        """Health endpoint should return 200."""
        try:
            with urlopen("http://localhost:8080/nginx-health", timeout=5) as response:
                assert response.status == 200
        except URLError as e:
            pytest.fail(f"Health endpoint not responding: {e}")
    
    def test_backend_headers_present(self):
        """Response should include backend identification headers."""
        try:
            with urlopen("http://localhost:8080/", timeout=5) as response:
                headers = dict(response.headers)
                # Check for at least one backend identification header
                backend_headers = [k for k in headers if 'backend' in k.lower() or 'served' in k.lower()]
                assert len(backend_headers) > 0, "No backend identification headers found"
        except URLError as e:
            pytest.fail(f"Cannot check headers: {e}")


class TestLoadBalancing:
    """Tests for load balancing functionality."""
    
    @pytest.fixture(autouse=True)
    def check_docker_running(self):
        """Skip if Docker environment is not running."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex(("127.0.0.1", 8080))
                if result != 0:
                    pytest.skip("Docker environment not running")
        except Exception:
            pytest.skip("Cannot check Docker environment")
    
    def test_round_robin_distribution(self):
        """Requests should be distributed across backends."""
        backends_seen = set()
        
        for _ in range(6):
            try:
                with urlopen("http://localhost:8080/", timeout=5) as response:
                    content = response.read().decode()
                    # Look for backend identifier in response
                    for i in range(1, 4):
                        if f"Backend {i}" in content or f"backend{i}" in content.lower():
                            backends_seen.add(i)
            except URLError:
                pass  # Continue testing even if one request fails
        
        # Should see at least 2 different backends in 6 requests with round-robin
        assert len(backends_seen) >= 2, f"Only saw backends: {backends_seen}"


class TestNetUtils:
    """Tests for network utilities module."""
    
    def test_net_utils_import(self):
        """net_utils module should be importable."""
        sys.path.insert(0, str(SRC_ROOT))
        try:
            from utils import net_utils
            assert net_utils is not None
        except ImportError as e:
            pytest.fail(f"Cannot import net_utils: {e}")
        finally:
            sys.path.pop(0)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
