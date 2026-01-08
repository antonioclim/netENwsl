#!/usr/bin/env python3
"""
Week 3 Smoke Test
NETWORKING class - ASE, Informatics | by Revolvix

Quick functionality verification that completes in under 60 seconds.
Tests basic connectivity, container status, and exercise functionality.

Usage:
    python tests/smoke_test.py [--verbose]
"""

import subprocess
import socket
import sys
import time
import argparse
from pathlib import Path
from typing import Tuple, List

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
TIMEOUT_SECONDS = 60
DOCKER_COMPOSE_PATH = PROJECT_ROOT / "docker" / "docker-compose.yml"

# Expected containers and ports
CONTAINERS = {
    "week3_server": {"port": 8080, "ip": "172.20.0.10"},
    "week3_router": {"port": 9090, "ip": "172.20.0.254"},
    "week3_client": {"port": None, "ip": "172.20.0.100"},
}

class SmokeTest:
    """Quick smoke test suite for Week 3 laboratory."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.passed = 0
        self.failed = 0
        self.start_time = time.time()
    
    def log(self, message: str) -> None:
        """Print message if verbose mode."""
        if self.verbose:
            print(f"  > {message}")
    
    def check(self, name: str, condition: bool, detail: str = "") -> bool:
        """Record test result."""
        if condition:
            print(f"  [PASS] {name}")
            self.passed += 1
        else:
            print(f"  [FAIL] {name}")
            if detail:
                print(f"         {detail}")
            self.failed += 1
        return condition
    
    def run_command(self, cmd: List[str], timeout: int = 10) -> Tuple[bool, str]:
        """Run command and return success status and output."""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.returncode == 0, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except Exception as e:
            return False, str(e)
    
    def test_docker_available(self) -> bool:
        """Test Docker is available and running."""
        success, output = self.run_command(["docker", "info"])
        return self.check("Docker daemon running", success, 
                         "Start Docker Desktop")
    
    def test_compose_valid(self) -> bool:
        """Test docker-compose.yml is valid."""
        success, output = self.run_command([
            "docker", "compose", "-f", str(DOCKER_COMPOSE_PATH), "config"
        ])
        return self.check("docker-compose.yml valid", success,
                         "Check YAML syntax")
    
    def test_containers_running(self) -> bool:
        """Test required containers are running."""
        all_running = True
        
        for container_name in CONTAINERS:
            success, output = self.run_command([
                "docker", "inspect", "-f", "{{.State.Running}}", container_name
            ])
            running = success and "true" in output.lower()
            
            if not self.check(f"Container {container_name} running", running,
                             f"Run: python scripts/start_lab.py"):
                all_running = False
        
        return all_running
    
    def test_network_exists(self) -> bool:
        """Test Docker network is created."""
        success, output = self.run_command([
            "docker", "network", "inspect", "week3_network"
        ])
        return self.check("Network week3_network exists", success,
                         "Run: python scripts/start_lab.py")
    
    def test_echo_server(self) -> bool:
        """Test TCP echo server is responding."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(("localhost", 8080))
            
            test_message = b"SMOKE_TEST"
            sock.sendall(test_message)
            response = sock.recv(1024)
            sock.close()
            
            return self.check("Echo server responding", response == test_message,
                             f"Expected {test_message}, got {response}")
        except Exception as e:
            return self.check("Echo server responding", False, str(e))
    
    def test_tunnel_connectivity(self) -> bool:
        """Test TCP tunnel is forwarding correctly."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(("localhost", 9090))
            
            test_message = b"TUNNEL_TEST"
            sock.sendall(test_message)
            response = sock.recv(1024)
            sock.close()
            
            return self.check("Tunnel forwarding to echo server", 
                             response == test_message,
                             f"Expected {test_message}, got {response}")
        except Exception as e:
            return self.check("Tunnel forwarding to echo server", False, str(e))
    
    def test_broadcast_port(self) -> bool:
        """Test broadcast port is open in container."""
        success, output = self.run_command([
            "docker", "exec", "week3_client", 
            "python3", "-c", 
            "import socket; s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); "
            "s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1); "
            "print('OK')"
        ])
        return self.check("Broadcast socket creation works", 
                         success and "OK" in output,
                         "Check Python socket module in container")
    
    def test_multicast_support(self) -> bool:
        """Test multicast group join works."""
        success, output = self.run_command([
            "docker", "exec", "week3_client",
            "python3", "-c",
            "import socket,struct; "
            "s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); "
            "s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1); "
            "s.bind(('',5008)); "
            "mreq=struct.pack('4s4s',socket.inet_aton('239.0.0.1'),socket.inet_aton('0.0.0.0')); "
            "s.setsockopt(socket.IPPROTO_IP,socket.IP_ADD_MEMBERSHIP,mreq); "
            "print('OK'); s.close()"
        ])
        return self.check("Multicast group join works",
                         success and "OK" in output,
                         "Check IGMP support in container")
    
    def test_tcpdump_available(self) -> bool:
        """Test tcpdump is available in containers."""
        success, output = self.run_command([
            "docker", "exec", "week3_client", "which", "tcpdump"
        ])
        return self.check("tcpdump available in containers",
                         success and "tcpdump" in output,
                         "Rebuild container image")
    
    def test_python_exercises_syntax(self) -> bool:
        """Test exercise Python files have valid syntax."""
        exercises_dir = PROJECT_ROOT / "src" / "exercises"
        all_valid = True
        
        for py_file in exercises_dir.glob("*.py"):
            success, output = self.run_command([
                sys.executable, "-m", "py_compile", str(py_file)
            ])
            if not success:
                self.check(f"Syntax: {py_file.name}", False, output)
                all_valid = False
        
        if all_valid:
            self.check("All exercise files have valid syntax", True)
        
        return all_valid
    
    def run_all(self) -> int:
        """Run all smoke tests."""
        print("=" * 60)
        print("Week 3 Smoke Test")
        print("=" * 60)
        print()
        
        # Infrastructure tests
        print("Infrastructure:")
        docker_ok = self.test_docker_available()
        
        if docker_ok:
            self.test_compose_valid()
            containers_ok = self.test_containers_running()
            self.test_network_exists()
        else:
            print("  [SKIP] Skipping container tests - Docker not available")
            containers_ok = False
        
        print()
        
        # Connectivity tests
        print("Connectivity:")
        if containers_ok:
            self.test_echo_server()
            self.test_tunnel_connectivity()
        else:
            print("  [SKIP] Skipping connectivity tests - containers not running")
        
        print()
        
        # Functionality tests
        print("Functionality:")
        if containers_ok:
            self.test_broadcast_port()
            self.test_multicast_support()
            self.test_tcpdump_available()
        else:
            print("  [SKIP] Skipping functionality tests - containers not running")
        
        print()
        
        # Code tests
        print("Code Quality:")
        self.test_python_exercises_syntax()
        
        # Summary
        elapsed = time.time() - self.start_time
        print()
        print("=" * 60)
        print(f"Results: {self.passed} passed, {self.failed} failed")
        print(f"Time: {elapsed:.1f}s (limit: {TIMEOUT_SECONDS}s)")
        
        if elapsed > TIMEOUT_SECONDS:
            print(f"WARNING: Test exceeded {TIMEOUT_SECONDS}s time limit")
        
        if self.failed == 0:
            print("Status: READY FOR LABORATORY")
            return 0
        else:
            print("Status: ISSUES DETECTED - Fix before proceeding")
            return 1


def main():
    parser = argparse.ArgumentParser(description="Week 3 Smoke Test")
    parser.add_argument('--verbose', '-v', action='store_true',
                       help="Show detailed output")
    args = parser.parse_args()
    
    test = SmokeTest(verbose=args.verbose)
    return test.run_all()


if __name__ == "__main__":
    sys.exit(main())
