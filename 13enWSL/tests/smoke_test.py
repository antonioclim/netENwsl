#!/usr/bin/env python3
"""
Smoke Test
NETWORKING class - ASE, Informatics | by Revolvix

Quick functionality check to verify the laboratory kit is operational.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import sys
import socket
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_port(host: str, port: int, timeout: float = 2.0) -> bool:
    """Check if a port is accepting connections."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
def run_smoke_test() -> int:
    """Run quick smoke tests."""
    print("=" * 60)
    print("Week 13 Smoke Test")
    print("NETWORKING class - ASE, Informatics")
    print("=" * 60)
    print()
    
    passed = 0
    failed = 0
    skipped = 0
    
    # Test 1: Python version
    print("[TEST] Python version...")
    if sys.version_info >= (3, 11):
        print("  [PASS] Python 3.11+")
        passed += 1
    else:
        print(f"  [FAIL] Python {sys.version_info[0]}.{sys.version_info[1]}")
        failed += 1
    
    # Test 2: Docker available
    print("[TEST] Docker availability...")
    result = subprocess.run(["docker", "--version"], capture_output=True)
    if result.returncode == 0:
        print("  [PASS] Docker available")
        passed += 1
    else:
        print("  [FAIL] Docker not found")
        failed += 1
    
    # Test 3: Project structure
    print("[TEST] Project structure...")
    required = ["docker/docker-compose.yml", "scripts/start_lab.py", "src/exercises"]
    all_exist = True
    for path in required:
        if not (PROJECT_ROOT / path).exists():
            print(f"  [FAIL] Missing: {path}")
            all_exist = False
    if all_exist:
        print("  [PASS] Structure complete")
        passed += 1
    else:
        failed += 1
    
    # Test 4: Service connectivity (if running)
    print("[TEST] Service connectivity...")
    services = [
        ("MQTT", 1883),
        ("DVWA", 8080),
        ("FTP", 2121),
    ]
    any_running = False
    for name, port in services:
        if check_port("127.0.0.1", port):
            print(f"  [PASS] {name} on port {port}")
            any_running = True
        else:
            print(f"  [SKIP] {name} not running on port {port}")
            skipped += 1
    
    if any_running:
        passed += 1
    
    # Test 5: Port scanner syntax
    print("[TEST] Port scanner syntax...")
    result = subprocess.run([
        sys.executable, "-m", "py_compile",
        str(PROJECT_ROOT / "src" / "exercises" / "ex_13_01_port_scanner.py")
    ], capture_output=True)
    if result.returncode == 0:
        print("  [PASS] Port scanner syntax valid")
        passed += 1
    else:
        print("  [FAIL] Port scanner has syntax errors")
        failed += 1
    
    # Summary
    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed, {skipped} skipped")
    
    if failed == 0:
        print("Smoke test PASSED")
        return 0
    else:
        print("Smoke test FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(run_smoke_test())
