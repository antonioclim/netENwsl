#!/usr/bin/env python3
"""
Smoke Test
NETWORKING class - ASE, Informatics | by Revolvix

Quick functionality verification that completes in under 60 seconds.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations
from typing import Optional, List, Dict, Tuple, Any

import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    print("=" * 60)
    print("Week 1 Smoke Test")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
    print("=" * 60)
    
    start_time = time.time()
    
    checks = []
    
    # Check 1: Project structure
    print("\n[1/5] Checking project structure...")
    required_files = [
        "README.md",
        "docker/docker-compose.yml",
        "scripts/start_lab.py",
        "src/exercises/ex_1_01_ping_latency.py",
    ]
    all_exist = True
    for f in required_files:
        path = PROJECT_ROOT / f
        if path.exists():
            print(f"  [OK] {f}")
        else:
            print(f"  [FAIL] {f}")
            all_exist = False
    checks.append(("Project Structure", all_exist))
    
    # Check 2: Docker available
    print("\n[2/5] Checking Docker...")
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            timeout=10
        )
        if result.returncode == 0:
            print(f"  [OK] Docker available")
            checks.append(("Docker Available", True))
        else:
            print(f"  [FAIL] Docker not responding")
            checks.append(("Docker Available", False))
    except Exception as e:
        print(f"  [FAIL] {e}")
        checks.append(("Docker Available", False))
    
    # Check 3: Python exercises syntax
    print("\n[3/5] Checking Python syntax...")
    exercises = list((PROJECT_ROOT / "src" / "exercises").glob("*.py"))
    syntax_ok = True
    for ex in exercises:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(ex)],
                capture_output=True,
                timeout=10
            )
            if result.returncode == 0:
                print(f"  [OK] {ex.name}")
            else:
                print(f"  [FAIL] {ex.name}")
                syntax_ok = False
        except Exception as e:
            print(f"  [FAIL] {ex.name}: {e}")
            syntax_ok = False
    checks.append(("Python Syntax", syntax_ok))
    
    # Check 4: Docker Compose valid
    print("\n[4/5] Checking docker-compose.yml...")
    compose_file = PROJECT_ROOT / "docker" / "docker-compose.yml"
    try:
        result = subprocess.run(
            ["docker", "compose", "-f", str(compose_file), "config", "-q"],
            capture_output=True,
            timeout=15
        )
        if result.returncode == 0:
            print("  [OK] docker-compose.yml valid")
            checks.append(("Docker Compose", True))
        else:
            print(f"  [FAIL] Invalid configuration")
            checks.append(("Docker Compose", False))
    except Exception as e:
        print(f"  [FAIL] {e}")
        checks.append(("Docker Compose", False))
    
    # Check 5: Loopback test
    print("\n[5/5] Testing loopback...")
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.bind(("127.0.0.1", 0))
        sock.close()
        print("  [OK] Loopback working")
        checks.append(("Loopback", True))
    except Exception as e:
        print(f"  [FAIL] {e}")
        checks.append(("Loopback", False))
    
    # Summary
    elapsed = time.time() - start_time
    passed = sum(1 for _, ok in checks if ok)
    failed = len(checks) - passed
    
    print("\n" + "=" * 60)
    print(f"Smoke Test Results ({elapsed:.1f}s)")
    print("-" * 60)
    
    for name, ok in checks:
        status = "\033[92mPASS\033[0m" if ok else "\033[91mFAIL\033[0m"
        print(f"  {name}: {status}")
    
    print("-" * 60)
    print(f"Total: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("\n\033[92mSmoke test passed!\033[0m")
        return 0
    else:
        print("\n\033[91mSmoke test failed.\033[0m")
        return 1


if __name__ == "__main__":
    sys.exit(main())
