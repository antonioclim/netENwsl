#!/usr/bin/env python3
"""
Smoke Test Script
NETWORKING class - ASE, Informatics | by Revolvix

Quick verification that the laboratory environment is working.
Run this after starting the lab to verify basic functionality.

Usage:
    python tests/smoke_test.py
"""

import sys
import time
import socket
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError

PROJECT_ROOT = Path(__file__).parent.parent

# ANSI colours
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_header():
    """Print test header."""
    print()
    print("=" * 60)
    print(f"{BOLD}Week 8 Laboratory - Smoke Test{RESET}")
    print("NETWORKING class - ASE, Informatics")
    print("=" * 60)
    print()


def test_result(name: str, passed: bool, message: str = "") -> bool:
    """Print test result."""
    if passed:
        print(f"  {GREEN}[PASS]{RESET} {name}")
    else:
        print(f"  {RED}[FAIL]{RESET} {name}")
        if message:
            print(f"         {message}")
    return passed


def check_port(host: str, port: int, timeout: float = 2.0) -> bool:
    """Check if a port is open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            return result == 0
    except Exception:
        return False


def check_http(url: str, timeout: float = 5.0) -> tuple:
    """Check HTTP endpoint. Returns (success, status_code, message)."""
    try:
        with urlopen(url, timeout=timeout) as response:
            return True, response.status, ""
    except URLError as e:
        return False, 0, str(e)
    except Exception as e:
        return False, 0, str(e)


def main() -> int:
    """Run smoke tests."""
    print_header()
    
    passed = 0
    failed = 0
    
    # Test 1: Port 8080 (nginx)
    print("Testing Network Connectivity:")
    if check_port("127.0.0.1", 8080):
        test_result("Port 8080 (nginx) is open", True)
        passed += 1
    else:
        test_result("Port 8080 (nginx) is open", False, 
                   "nginx not running - start with: python scripts/start_lab.py")
        failed += 1
        # If nginx isn't running, skip remaining HTTP tests
        print()
        print(f"{YELLOW}Skipping HTTP tests - nginx not available{RESET}")
        print()
        print_summary(passed, failed)
        return 1 if failed > 0 else 0
    
    # Test 2: HTTP GET /
    print()
    print("Testing HTTP Endpoints:")
    success, status, msg = check_http("http://localhost:8080/")
    if success and status == 200:
        test_result("GET / returns 200 OK", True)
        passed += 1
    else:
        test_result("GET / returns 200 OK", False, msg)
        failed += 1
    
    # Test 3: Health endpoint
    success, status, msg = check_http("http://localhost:8080/nginx-health")
    if success and status == 200:
        test_result("GET /nginx-health returns 200 OK", True)
        passed += 1
    else:
        test_result("GET /nginx-health returns 200 OK", False, msg)
        failed += 1
    
    # Test 4: Backend distribution
    print()
    print("Testing Load Balancing:")
    backends_seen = set()
    for i in range(6):
        try:
            with urlopen("http://localhost:8080/", timeout=5) as response:
                content = response.read().decode()
                for j in range(1, 4):
                    if f"Backend {j}" in content or f"backend{j}" in content.lower():
                        backends_seen.add(j)
        except Exception:
            pass
    
    if len(backends_seen) >= 2:
        test_result(f"Round-robin distributes to multiple backends (saw {len(backends_seen)})", True)
        passed += 1
    else:
        test_result("Round-robin distributes to multiple backends", False,
                   f"Only saw {len(backends_seen)} backend(s)")
        failed += 1
    
    # Test 5: Backend headers
    print()
    print("Testing Response Headers:")
    try:
        with urlopen("http://localhost:8080/", timeout=5) as response:
            headers = dict(response.headers)
            has_backend_header = any('backend' in k.lower() or 'served' in k.lower() 
                                    for k in headers)
            if has_backend_header:
                test_result("Backend identification headers present", True)
                passed += 1
            else:
                test_result("Backend identification headers present", False,
                           "No X-Backend-ID or similar header found")
                failed += 1
    except Exception as e:
        test_result("Backend identification headers present", False, str(e))
        failed += 1
    
    # Test 6: File structure
    print()
    print("Testing File Structure:")
    required_files = [
        "docker/docker-compose.yml",
        "docker/configs/nginx/nginx.conf",
        "scripts/start_lab.py",
        "scripts/stop_lab.py",
        "src/exercises/ex_8_01_http_server.py",
        "www/index.html"
    ]
    
    all_files_exist = True
    for rel_path in required_files:
        full_path = PROJECT_ROOT / rel_path
        if not full_path.exists():
            test_result(f"File exists: {rel_path}", False)
            failed += 1
            all_files_exist = False
    
    if all_files_exist:
        test_result("All required files present", True)
        passed += 1
    
    # Summary
    print_summary(passed, failed)
    
    return 1 if failed > 0 else 0


def print_summary(passed: int, failed: int):
    """Print test summary."""
    total = passed + failed
    print()
    print("=" * 60)
    if failed == 0:
        print(f"{GREEN}{BOLD}All {total} tests passed!{RESET}")
        print()
        print("The laboratory environment is ready for use.")
        print()
        print("Next steps:")
        print("  1. Open browser to http://localhost:8080/")
        print("  2. Start Wireshark to capture traffic")
        print("  3. Begin exercises in src/exercises/")
    else:
        print(f"{RED}{BOLD}{failed} of {total} tests failed{RESET}")
        print()
        print("Please fix the issues above before proceeding.")
        print("See docs/troubleshooting.md for common solutions.")
    print("=" * 60)
    print()


if __name__ == "__main__":
    sys.exit(main())
