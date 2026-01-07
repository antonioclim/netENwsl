#!/usr/bin/env python3
"""
Week 10 Smoke Test
NETWORKING class - ASE, Informatics | by Revolvix

Quick functionality check that runs in under 60 seconds.
"""

import subprocess
import sys
import socket
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def check_port(host: str, port: int) -> bool:
    """Quick TCP port check."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            return s.connect_ex((host, port)) == 0
    except:
        return False


def main() -> int:
    print("=" * 50)
    print("Week 10 Smoke Test")
    print("=" * 50)
    print()
    
    errors = []
    
    # 1. Check project structure
    print("[1/5] Checking project structure...")
    required = ["docker/docker-compose.yml", "scripts/start_lab.py", "src/exercises"]
    for path in required:
        if not (PROJECT_ROOT / path).exists():
            errors.append(f"Missing: {path}")
    print("  ✓ Structure OK" if not errors else f"  ✗ {errors[-1]}")
    
    # 2. Check Python imports
    print("[2/5] Checking Python imports...")
    try:
        import flask
        import requests
        import yaml
        print("  ✓ Required packages installed")
    except ImportError as e:
        errors.append(f"Missing package: {e.name}")
        print(f"  ✗ {errors[-1]}")
    
    # 3. Check Docker
    print("[3/5] Checking Docker...")
    result = subprocess.run(["docker", "info"], capture_output=True)
    if result.returncode == 0:
        print("  ✓ Docker running")
    else:
        errors.append("Docker not running")
        print(f"  ✗ {errors[-1]}")
    
    # 4. Check exercise files syntax
    print("[4/5] Checking exercise syntax...")
    exercises = list((PROJECT_ROOT / "src" / "exercises").glob("*.py"))
    for ex in exercises:
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(ex)],
            capture_output=True
        )
        if result.returncode != 0:
            errors.append(f"Syntax error in {ex.name}")
    print(f"  ✓ {len(exercises)} exercises OK" if not errors else f"  ✗ {errors[-1]}")
    
    # 5. Check services (if running)
    print("[5/5] Checking services (if running)...")
    services = [
        ("HTTP", "127.0.0.1", 8000),
        ("SSH", "127.0.0.1", 2222),
        ("FTP", "127.0.0.1", 2121),
    ]
    running = sum(1 for _, h, p in services if check_port(h, p))
    print(f"  {running}/{len(services)} services running")
    
    # Summary
    print()
    print("=" * 50)
    if errors:
        print(f"SMOKE TEST: {len(errors)} issues found")
        for e in errors:
            print(f"  - {e}")
        return 1
    else:
        print("SMOKE TEST: PASSED")
        return 0


if __name__ == "__main__":
    sys.exit(main())
