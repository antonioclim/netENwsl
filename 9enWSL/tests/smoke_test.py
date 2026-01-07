#!/usr/bin/env python3
"""
Quick Smoke Test for Week 9 Laboratory
NETWORKING class - ASE, Informatics | by Revolvix

Performs a quick functionality check to verify the laboratory
environment is working correctly.

Usage:
    python tests/smoke_test.py
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def check_docker():
    """Check if Docker is running."""
    print("Checking Docker...", end=" ", flush=True)
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        if result.returncode == 0:
            print("OK")
            return True
        else:
            print("FAIL")
            return False
    except Exception as e:
        print(f"FAIL ({e})")
        return False


def check_exercises():
    """Check if exercise files are valid Python."""
    print("Checking exercise files...", end=" ", flush=True)
    
    exercises = PROJECT_ROOT / "src" / "exercises"
    
    for pyfile in exercises.glob("*.py"):
        try:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(pyfile)],
                capture_output=True,
                timeout=10
            )
            if result.returncode != 0:
                print(f"FAIL ({pyfile.name})")
                return False
        except Exception as e:
            print(f"FAIL ({e})")
            return False
    
    print("OK")
    return True


def check_endianness_demo():
    """Run the endianness demo as a quick test."""
    print("Running endianness demo...", end=" ", flush=True)
    
    exercise = PROJECT_ROOT / "src" / "exercises" / "ex_9_01_endianness.py"
    
    if not exercise.exists():
        print("SKIP (file not found)")
        return True
    
    try:
        result = subprocess.run(
            [sys.executable, str(exercise), "--selftest"],
            capture_output=True,
            timeout=30,
            cwd=PROJECT_ROOT
        )
        if result.returncode == 0:
            print("OK")
            return True
        else:
            print("FAIL")
            print(result.stderr.decode()[:200])
            return False
    except Exception as e:
        print(f"FAIL ({e})")
        return False


def check_docker_compose():
    """Validate docker-compose.yml syntax."""
    print("Validating docker-compose.yml...", end=" ", flush=True)
    
    compose_file = PROJECT_ROOT / "docker" / "docker-compose.yml"
    
    if not compose_file.exists():
        print("SKIP (file not found)")
        return True
    
    try:
        result = subprocess.run(
            ["docker", "compose", "-f", str(compose_file), "config"],
            capture_output=True,
            timeout=10
        )
        if result.returncode == 0:
            print("OK")
            return True
        else:
            print("FAIL")
            return False
    except Exception as e:
        print(f"FAIL ({e})")
        return False


def main():
    print("=" * 50)
    print("Week 9 Laboratory - Smoke Test")
    print("=" * 50)
    print()
    
    start_time = time.time()
    
    checks = [
        ("Docker", check_docker),
        ("Exercise Files", check_exercises),
        ("Endianness Demo", check_endianness_demo),
        ("Docker Compose", check_docker_compose)
    ]
    
    results = []
    for name, check_func in checks:
        results.append(check_func())
    
    elapsed = time.time() - start_time
    
    print()
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Results: {passed}/{total} checks passed")
    print(f"Time: {elapsed:.1f}s")
    
    if all(results):
        print("\033[32mSmoke test PASSED\033[0m")
        return 0
    else:
        print("\033[31mSmoke test FAILED\033[0m")
        return 1


if __name__ == "__main__":
    sys.exit(main())
