#!/usr/bin/env python3
"""
Smoke Test - Quick Functionality Check
NETWORKING class - ASE, Informatics | by Revolvix

Performs rapid verification that the Week 14 laboratory environment
is functioning correctly. Designed to complete in under 60 seconds.

Tests:
1. Docker daemon accessibility
2. Required containers running
3. Network connectivity between services
4. HTTP endpoint responsiveness
5. TCP echo service functionality
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import sys
import time
import socket
import argparse
from pathlib import Path
from typing import Tuple, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY_UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════
class Colours:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_MODELS
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class TestResult:
    """Result of a single test."""
    name: str
    passed: bool
    duration_ms: float
    message: str = ""


@dataclass
class SmokeTestReport:
    """Complete smoke test report."""
    started: datetime = field(default_factory=datetime.now)
    ended: datetime = None
    results: List[TestResult] = field(default_factory=list)
    
    @property
    def total_tests(self) -> int:
        return len(self.results)
    
    @property
    def passed_tests(self) -> int:
        return sum(1 for r in self.results if r.passed)
    
    @property
    def failed_tests(self) -> int:
        return sum(1 for r in self.results if not r.passed)
    
    @property
    def total_duration_ms(self) -> float:
        return sum(r.duration_ms for r in self.results)
    
    @property
    def all_passed(self) -> bool:
        return all(r.passed for r in self.results)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_RUNNER
# ═══════════════════════════════════════════════════════════════════════════════
def run_test(name: str, test_fn) -> TestResult:
    """Execute a test function and return result."""
    start = time.time()
    try:
        passed, message = test_fn()
        duration = (time.time() - start) * 1000
        return TestResult(name, passed, duration, message)
    except Exception as e:
        duration = (time.time() - start) * 1000
        return TestResult(name, False, duration, str(e))


# ═══════════════════════════════════════════════════════════════════════════════
# DOCKER_TESTS
# ═══════════════════════════════════════════════════════════════════════════════
def test_docker_running() -> Tuple[bool, str]:
    """Check if Docker daemon is accessible."""
    import subprocess
    try:
        result = subprocess.run(
            ['docker', 'info'],
            capture_output=True,
            timeout=10
        )
        if result.returncode == 0:
            return True, "Docker daemon running"
        return False, "Docker daemon not responding"
    except subprocess.TimeoutExpired:
        return False, "Docker daemon timed out"
    except FileNotFoundError:
        return False, "Docker not installed"


def test_containers_running() -> Tuple[bool, str]:
    """Check if required containers are running."""
    import subprocess
    
    required = {'week14_app1', 'week14_app2', 'week14_lb', 'week14_client', 'week14_echo'}
    
    try:
        result = subprocess.run(
            ['docker', 'ps', '--format', '{{.Names}}'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return False, "Could not list containers"
        
        running = set(result.stdout.strip().split('\n')) if result.stdout.strip() else set()
        
        # Also check for alternative naming
        week14_running = {c for c in running if 'week14' in c.lower() or 'week-14' in c.lower()}
        
        # Check by role
        has_lb = any('lb' in c.lower() for c in week14_running)
        has_app = any('app' in c.lower() for c in week14_running)
        has_echo = any('echo' in c.lower() for c in week14_running)
        
        if has_lb and has_app and has_echo:
            return True, f"{len(week14_running)} containers running"
        
        missing = required - week14_running
        if missing:
            return False, f"Missing: {', '.join(sorted(missing)[:3])}"
        
        return True, f"{len(week14_running)} containers running"
        
    except Exception as e:
        return False, str(e)


def test_network_isolation() -> Tuple[bool, str]:
    """Verify Docker networks exist."""
    import subprocess
    
    try:
        result = subprocess.run(
            ['docker', 'network', 'ls', '--format', '{{.Name}}'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        networks = result.stdout.strip().split('\n') if result.stdout.strip() else []
        
        week14_nets = [n for n in networks if 'week14' in n.lower()]
        
        if len(week14_nets) >= 2:
            return True, f"Networks configured ({len(week14_nets)} found)"
        elif week14_nets:
            return True, f"Network found: {week14_nets[0]}"
        return False, "Week 14 networks not found"
        
    except Exception as e:
        return False, str(e)


# ═══════════════════════════════════════════════════════════════════════════════
# PORT_TESTS
# ═══════════════════════════════════════════════════════════════════════════════
def test_port_accessible(port: int, service: str) -> Tuple[bool, str]:
    """Check if a port is accessible."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    try:
        result = sock.connect_ex(('localhost', port))
        sock.close()
        if result == 0:
            return True, f"{service} accessible on port {port}"
        return False, f"{service} not accessible on port {port}"
    except Exception as e:
        return False, f"Port check failed: {e}"


def test_load_balancer() -> Tuple[bool, str]:
    """Test load balancer HTTP endpoint."""
    return test_port_accessible(8080, "Load Balancer")


def test_backend_app1() -> Tuple[bool, str]:
    """Test backend app1 HTTP endpoint."""
    return test_port_accessible(8001, "Backend App 1")


def test_backend_app2() -> Tuple[bool, str]:
    """Test backend app2 HTTP endpoint."""
    return test_port_accessible(8002, "Backend App 2")


def test_echo_server() -> Tuple[bool, str]:
    """Test TCP echo server."""
    return test_port_accessible(9090, "Echo Server")


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTIONALITY_TESTS
# ═══════════════════════════════════════════════════════════════════════════════
def test_http_response() -> Tuple[bool, str]:
    """Test HTTP response from load balancer."""
    try:
        import urllib.request
        with urllib.request.urlopen('http://localhost:8080/', timeout=5) as response:
            if response.status == 200:
                body = response.read().decode()
                if 'Hello' in body or 'app' in body.lower():
                    return True, "HTTP response received"
                return True, "HTTP 200 OK"
            return False, f"HTTP {response.status}"
    except urllib.error.URLError as e:
        return False, f"Connection failed: {e.reason}"
    except Exception as e:
        return False, str(e)


def test_echo_functionality() -> Tuple[bool, str]:
    """Test TCP echo server functionality."""
    test_message = "SMOKE_TEST_PING"
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(('localhost', 9090))
        sock.sendall(f"{test_message}\n".encode())
        response = sock.recv(1024).decode().strip()
        sock.close()
        
        if test_message in response:
            return True, "Echo server functional"
        return False, f"Unexpected response: {response[:50]}"
        
    except socket.timeout:
        return False, "Echo server timed out"
    except ConnectionRefusedError:
        return False, "Echo server connection refused"
    except Exception as e:
        return False, str(e)


def test_round_robin() -> Tuple[bool, str]:
    """Quick test of round-robin distribution."""
    try:
        import urllib.request
        backends_seen = set()
        
        for _ in range(4):
            with urllib.request.urlopen('http://localhost:8080/', timeout=3) as response:
                body = response.read().decode()
                if 'app1' in body.lower():
                    backends_seen.add('app1')
                elif 'app2' in body.lower():
                    backends_seen.add('app2')
        
        if len(backends_seen) >= 2:
            return True, "Round-robin working (both backends used)"
        elif len(backends_seen) == 1:
            return False, f"Only {list(backends_seen)[0]} responding"
        return False, "Could not determine backend distribution"
        
    except Exception as e:
        return False, str(e)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════
def run_smoke_tests(verbose: bool = False) -> SmokeTestReport:
    """Execute all smoke tests."""
    report = SmokeTestReport()
    
    tests = [
        ("Docker Running", test_docker_running),
        ("Containers Running", test_containers_running),
        ("Network Configuration", test_network_isolation),
        ("Load Balancer Port", test_load_balancer),
        ("Backend App 1 Port", test_backend_app1),
        ("Backend App 2 Port", test_backend_app2),
        ("Echo Server Port", test_echo_server),
        ("HTTP Response", test_http_response),
        ("Echo Functionality", test_echo_functionality),
        ("Round-Robin Distribution", test_round_robin),
    ]
    
    print(f"\n{Colours.CYAN}Running smoke tests...{Colours.ENDC}\n")
    
    for name, test_fn in tests:
        result = run_test(name, test_fn)
        report.results.append(result)
        
        # Print result
        status = f"{Colours.GREEN}PASS{Colours.ENDC}" if result.passed else f"{Colours.RED}FAIL{Colours.ENDC}"
        duration = f"({result.duration_ms:.0f}ms)"
        
        if verbose or not result.passed:
            print(f"  [{status}] {name} {duration}")
            if result.message and (verbose or not result.passed):
                print(f"         {result.message}")
        else:
            print(f"  [{status}] {name} {duration}")
    
    report.ended = datetime.now()
    return report


# ═══════════════════════════════════════════════════════════════════════════════
# REPORTING
# ═══════════════════════════════════════════════════════════════════════════════
def print_report(report: SmokeTestReport) -> None:
    """Print smoke test summary report."""
    print(f"\n{'=' * 50}")
    print(f"{Colours.BOLD}Smoke Test Summary{Colours.ENDC}")
    print(f"{'=' * 50}")
    
    print(f"\nTests: {report.passed_tests}/{report.total_tests} passed")
    print(f"Duration: {report.total_duration_ms:.0f}ms")
    
    if report.failed_tests > 0:
        print(f"\n{Colours.RED}Failed tests:{Colours.ENDC}")
        for result in report.results:
            if not result.passed:
                print(f"  - {result.name}: {result.message}")
    
    print()
    if report.failed_tests == 0:
        print(f"{Colours.GREEN}✓ All smoke tests passed!{Colours.ENDC}")
        print(f"{Colours.CYAN}The laboratory environment is ready.{Colours.ENDC}")
    else:
        print(f"{Colours.RED}✗ Some tests failed.{Colours.ENDC}")
        print(f"{Colours.YELLOW}Run 'python scripts/start_lab.py' to start the environment.{Colours.ENDC}")


# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGUMENTS
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Week 14 Smoke Test - Quick Functionality Check",
        epilog="NETWORKING class - ASE, Informatics | by Revolvix"
    )
    
    parser.add_argument('-v', '--verbose', action='store_true', help='Show detailed output')
    parser.add_argument('-q', '--quiet', action='store_true', help='Only show summary')
    parser.add_argument('--json', action='store_true', help='Output results as JSON')
    
    return parser.parse_args()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    args = parse_args()
    
    if not args.quiet:
        print(f"\n{Colours.BOLD}Week 14 Laboratory - Smoke Test{Colours.ENDC}")
        print("NETWORKING class - ASE, Informatics | by Revolvix")
    
    # Run tests
    report = run_smoke_tests(verbose=args.verbose and not args.quiet)
    
    if args.json:
        import json
        output = {
            'passed': report.passed_tests,
            'failed': report.failed_tests,
            'total': report.total_tests,
            'duration_ms': report.total_duration_ms,
            'results': [
                {
                    'name': r.name,
                    'passed': r.passed,
                    'duration_ms': r.duration_ms,
                    'message': r.message
                }
                for r in report.results
            ]
        }
        print(json.dumps(output, indent=2))
    elif not args.quiet:
        print_report(report)
    
    # Return exit code
    return 0 if report.failed_tests == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
