#!/usr/bin/env python3
"""
Week 2 Smoke Test
NETWORKING class - ASE, CSIE Bucharest | by ing. dr. Antonio Clim

Quick functionality check that completes in under 60 seconds.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any

PROJECT_ROOT = Path(__file__).parent.parent



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Run smoke test."""
    print()
    print("=" * 50)
    print("  Week 2 Smoke Test")
    print("=" * 50)
    print()
    
    start_time = time.time()
    errors = []
    
    # Check Python syntax
    print("Checking Python syntax...")
    src_dir = PROJECT_ROOT / "src"
    for py_file in src_dir.rglob("*.py"):
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(py_file)],
            capture_output=True
        )
        if result.returncode != 0:
            errors.append(f"Syntax error: {py_file.name}")
    
    scripts_dir = PROJECT_ROOT / "scripts"
    for py_file in scripts_dir.rglob("*.py"):
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(py_file)],
            capture_output=True
        )
        if result.returncode != 0:
            errors.append(f"Syntax error: {py_file.name}")
    

    anti_ai_dir = PROJECT_ROOT / "anti_ai"
    for py_file in anti_ai_dir.rglob("*.py"):
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(py_file)],
            capture_output=True
        )
        if result.returncode != 0:
            errors.append(f"Syntax error: {py_file.name}")
    print(f"  ✓ Python syntax check complete")
    
    # Check imports
    print("Checking imports...")
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from src.exercises import ex_2_01_tcp
        from src.exercises import ex_2_02_udp
        from anti_ai import challenge
        from anti_ai import proof_runner
        from anti_ai import submission_validator
        print(f"  ✓ Anti‑AI modules import successfully")
        print(f"  ✓ Exercise modules import successfully")
    except ImportError as e:
        errors.append(f"Import error: {e}")
    
    # Quick TCP test
    print("Running quick TCP test...")
    tcp_script = PROJECT_ROOT / "src" / "exercises" / "ex_2_01_tcp.py"
    
    server = subprocess.Popen(
        [sys.executable, str(tcp_script), "server", "--port", "29090"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    time.sleep(0.5)
    
    result = subprocess.run(
        [sys.executable, str(tcp_script), "client",
         "--host", "127.0.0.1", "--port", "29090", "-m", "smoke"],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    server.terminate()
    server.wait(timeout=2)
    
    if result.returncode == 0 and "SMOKE" in result.stdout:
        print(f"  ✓ TCP server/client functional")
    else:
        errors.append("TCP server/client failed")
    
    # Quick UDP test
    print("Running quick UDP test...")
    udp_script = PROJECT_ROOT / "src" / "exercises" / "ex_2_02_udp.py"
    
    server = subprocess.Popen(
        [sys.executable, str(udp_script), "server", "--port", "29091"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    time.sleep(0.5)
    
    result = subprocess.run(
        [sys.executable, str(udp_script), "client",
         "--host", "127.0.0.1", "--port", "29091", "-o", "ping"],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    server.terminate()
    server.wait(timeout=2)
    
    if result.returncode == 0 and "PONG" in result.stdout:
        print(f"  ✓ UDP server/client functional")
    else:
        errors.append("UDP server/client failed")
    
    # Summary
    elapsed = time.time() - start_time
    print()
    print("=" * 50)
    
    if errors:
        print(f"  SMOKE TEST FAILED ({elapsed:.1f}s)")
        for error in errors:
            print(f"  ✗ {error}")
        return 1
    else:
        print(f"  SMOKE TEST PASSED ({elapsed:.1f}s)")
        return 0


if __name__ == "__main__":
    sys.exit(main())
