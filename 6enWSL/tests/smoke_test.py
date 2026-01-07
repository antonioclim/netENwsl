#!/usr/bin/env python3
"""
Smoke Test
NETWORKING class - ASE, Informatics | by Revolvix

Quick functionality check for the Week 6 laboratory environment.
Should complete in under 60 seconds.
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def check_python_imports() -> tuple[bool, str]:
    """Check that required Python modules can be imported."""
    required = ["socket", "argparse", "subprocess", "pathlib"]
    
    for module in required:
        try:
            __import__(module)
        except ImportError:
            return False, f"Failed to import {module}"
    
    return True, "All required modules available"


def check_source_files() -> tuple[bool, str]:
    """Check that source files exist."""
    required_files = [
        "src/exercises/topo_nat.py",
        "src/exercises/topo_sdn.py",
        "src/apps/tcp_echo.py",
        "src/apps/udp_echo.py",
        "src/apps/nat_observer.py",
    ]
    
    missing = []
    for rel_path in required_files:
        full_path = PROJECT_ROOT / rel_path
        if not full_path.exists():
            missing.append(rel_path)
    
    if missing:
        return False, f"Missing files: {', '.join(missing)}"
    return True, "All source files present"


def check_docker() -> tuple[bool, str]:
    """Check Docker availability."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        if result.returncode == 0:
            return True, "Docker is running"
        return False, "Docker not responding"
    except FileNotFoundError:
        return False, "Docker not installed"
    except subprocess.TimeoutExpired:
        return False, "Docker check timed out"


def check_network_tools() -> tuple[bool, str]:
    """Check network tool availability."""
    tools = {
        "ping": False,
        "ip": False,
    }
    
    for tool in tools:
        try:
            result = subprocess.run(
                ["which", tool],
                capture_output=True,
                timeout=5
            )
            tools[tool] = result.returncode == 0
        except Exception:
            pass
    
    available = [t for t, ok in tools.items() if ok]
    missing = [t for t, ok in tools.items() if not ok]
    
    if missing:
        return False, f"Missing: {', '.join(missing)}; Available: {', '.join(available)}"
    return True, "All network tools available"


def check_syntax() -> tuple[bool, str]:
    """Check Python file syntax."""
    python_files = list((PROJECT_ROOT / "src").rglob("*.py"))
    python_files += list((PROJECT_ROOT / "scripts").rglob("*.py"))
    
    errors = []
    for py_file in python_files:
        try:
            with open(py_file, "r") as f:
                compile(f.read(), py_file, "exec")
        except SyntaxError as e:
            errors.append(f"{py_file.name}: {e.msg}")
    
    if errors:
        return False, f"Syntax errors: {'; '.join(errors[:3])}"
    return True, f"All {len(python_files)} Python files have valid syntax"


def main() -> int:
    """Run smoke tests."""
    print()
    print("=" * 60)
    print("Week 6 Smoke Test")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
    print("=" * 60)
    print()
    
    start_time = time.time()
    
    tests = [
        ("Python imports", check_python_imports),
        ("Source files", check_source_files),
        ("Docker", check_docker),
        ("Network tools", check_network_tools),
        ("Python syntax", check_syntax),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            passed, message = test_func()
            results.append((name, passed, message))
        except Exception as e:
            results.append((name, False, str(e)))
    
    # Print results
    for name, passed, message in results:
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {name}: {message}")
    
    elapsed = time.time() - start_time
    
    # Summary
    print()
    print("-" * 60)
    passed_count = sum(1 for _, p, _ in results if p)
    total_count = len(results)
    print(f"Results: {passed_count}/{total_count} passed in {elapsed:.2f}s")
    
    if passed_count == total_count:
        print("✓ All smoke tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
