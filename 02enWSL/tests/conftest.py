"""
pytest configuration and fixtures — Week 2

Provides shared fixtures and configuration for all tests.

NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim
"""

import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent


@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory."""
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def src_dir(project_root):
    """Return the src directory."""
    return project_root / "src"


@pytest.fixture(scope="session")
def exercises_dir(src_dir):
    """Return the exercises directory."""
    return src_dir / "exercises"


@pytest.fixture
def free_tcp_port():
    """Find and return a free TCP port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


@pytest.fixture
def free_udp_port():
    """Find and return a free UDP port."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    return port


@pytest.fixture
def tcp_server(exercises_dir, free_tcp_port):
    """
    Start a TCP server for testing and yield the port.
    
    Server is automatically terminated after the test.
    """
    server_script = exercises_dir / "ex_2_01_tcp.py"
    
    if not server_script.exists():
        pytest.skip(f"TCP exercise not found: {server_script}")
    
    proc = subprocess.Popen(
        [sys.executable, str(server_script), "server", 
         "--port", str(free_tcp_port), "--mode", "threaded"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    
    # Wait for server to start
    time.sleep(0.5)
    
    # Verify server is running
    if proc.poll() is not None:
        output = proc.stdout.read().decode() if proc.stdout else ""
        pytest.fail(f"TCP server failed to start: {output}")
    
    yield free_tcp_port
    
    # Cleanup
    proc.terminate()
    try:
        proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        proc.kill()


@pytest.fixture
def udp_server(exercises_dir, free_udp_port):
    """
    Start a UDP server for testing and yield the port.
    
    Server is automatically terminated after the test.
    """
    server_script = exercises_dir / "ex_2_02_udp.py"
    
    if not server_script.exists():
        pytest.skip(f"UDP exercise not found: {server_script}")
    
    proc = subprocess.Popen(
        [sys.executable, str(server_script), "server",
         "--port", str(free_udp_port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    
    # Wait for server to start
    time.sleep(0.5)
    
    # Verify server is running
    if proc.poll() is not None:
        output = proc.stdout.read().decode() if proc.stdout else ""
        pytest.fail(f"UDP server failed to start: {output}")
    
    yield free_udp_port
    
    # Cleanup
    proc.terminate()
    try:
        proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        proc.kill()


def pytest_configure(config):
    """Configure custom markers."""
    config.addinivalue_line("markers", "slow: marks test as slow")
    config.addinivalue_line("markers", "integration: requires Docker")
    config.addinivalue_line("markers", "smoke: quick sanity check")


def pytest_collection_modifyitems(config, items):
    """Add markers based on test location and name."""
    for item in items:
        # Mark tests in smoke_test.py as smoke tests
        if "smoke_test" in str(item.fspath):
            item.add_marker(pytest.mark.smoke)
        
        # Mark tests with 'docker' in name as integration
        if "docker" in item.name.lower():
            item.add_marker(pytest.mark.integration)
