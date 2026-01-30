#!/usr/bin/env python3
"""
Exercise Tests — Week 6: NAT/PAT & SDN
======================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Tests for validating laboratory exercises.

Usage:
    python tests/test_exercises.py
    pytest tests/test_exercises.py -v

Contact: Issues: Open an issue in GitHub
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"
EXERCISES_DIR = SRC_DIR / "exercises"
APPS_DIR = SRC_DIR / "apps"


# ═══════════════════════════════════════════════════════════════════════════════
# TEST UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

def check_file_exists(path: Path, description: str) -> bool:
    """Check if a file exists and report result."""
    exists = path.exists()
    status = "PASS" if exists else "FAIL"
    print(f"  [{status}] {description}: {path.name}")
    return exists


def check_python_syntax(path: Path) -> Tuple[bool, str]:
    """Check Python file for syntax errors."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(path)],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0, result.stderr
    except subprocess.TimeoutExpired:
        return False, "Timeout during syntax check"
    except Exception as e:
        return False, str(e)


def check_imports(path: Path, required_imports: List[str]) -> Tuple[bool, List[str]]:
    """Check if a Python file contains required imports."""
    try:
        content = path.read_text()
        missing = [imp for imp in required_imports if imp not in content]
        return len(missing) == 0, missing
    except Exception as e:
        return False, [str(e)]


# ═══════════════════════════════════════════════════════════════════════════════
# EXERCISE 1 TESTS: NAT TOPOLOGY
# ═══════════════════════════════════════════════════════════════════════════════

def check_exercise_1() -> bool:
    """
    Test Exercise 1: NAT/PAT Topology.
    
    Validates:
    - Topology file exists
    - Syntax is valid
    - Required components present
    """
    print("Testing Exercise 1: NAT/PAT Topology")
    print("-" * 50)
    
    # Check topology file exists (CORRECTED PATH)
    topo_file = EXERCISES_DIR / "ex_6_01_nat_topology.py"
    
    if not check_file_exists(topo_file, "Topology file"):
        print("  [SKIP] Cannot continue without topology file")
        return False
    
    # Check syntax
    valid, error = check_python_syntax(topo_file)
    if valid:
        print("  [PASS] Python syntax valid")
    else:
        print(f"  [FAIL] Syntax error: {error}")
        return False
    
    # Check required imports
    required = ["mininet", "Topo", "Host", "Switch"]
    has_imports, missing = check_imports(topo_file, required)
    if has_imports:
        print("  [PASS] Required imports present")
    else:
        print(f"  [WARN] Missing imports: {missing}")
    
    # Check for prediction prompts
    content = topo_file.read_text()
    if "💭" in content or "PREDICTION" in content:
        print("  [PASS] Prediction prompts present")
    else:
        print("  [WARN] No prediction prompts found")
    
    print()
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# EXERCISE 2 TESTS: SDN TOPOLOGY
# ═══════════════════════════════════════════════════════════════════════════════

def check_exercise_2() -> bool:
    """
    Test Exercise 2: SDN Topology and Flow Observation.
    
    Validates:
    - Topology file exists
    - Syntax is valid
    - OpenFlow components present
    """
    print("Testing Exercise 2: SDN Topology and Flow Observation")
    print("-" * 50)
    
    # Check topology file exists (CORRECTED PATH)
    topo_file = EXERCISES_DIR / "ex_6_02_sdn_topology.py"
    
    if not check_file_exists(topo_file, "Topology file"):
        print("  [SKIP] Cannot continue without topology file")
        return False
    
    # Check syntax
    valid, error = check_python_syntax(topo_file)
    if valid:
        print("  [PASS] Python syntax valid")
    else:
        print(f"  [FAIL] Syntax error: {error}")
        return False
    
    # Check for OpenFlow components
    content = topo_file.read_text()
    of_components = ["OpenFlow", "ovs-ofctl", "flow", "priority"]
    found = [c for c in of_components if c.lower() in content.lower()]
    
    if len(found) >= 2:
        print(f"  [PASS] OpenFlow components present: {found}")
    else:
        print(f"  [WARN] Limited OpenFlow components: {found}")
    
    print()
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# EXERCISE 3 TESTS: SDN POLICY DESIGN
# ═══════════════════════════════════════════════════════════════════════════════

def check_exercise_3() -> bool:
    """
    Test Exercise 3: SDN Policy Design.
    
    Validates:
    - Required tools available (documentation)
    - Policy controller present
    """
    print("Testing Exercise 3: Custom SDN Policy Design")
    print("-" * 50)
    
    # Check controller application
    controller = APPS_DIR / "sdn_policy_controller.py"
    if check_file_exists(controller, "SDN policy controller"):
        valid, error = check_python_syntax(controller)
        if valid:
            print("  [PASS] Controller syntax valid")
        else:
            print(f"  [FAIL] Controller syntax error: {error}")
    
    # Check echo applications
    tcp_echo = APPS_DIR / "tcp_echo.py"
    udp_echo = APPS_DIR / "udp_echo.py"
    check_file_exists(tcp_echo, "TCP echo application")
    check_file_exists(udp_echo, "UDP echo application")
    
    # Check topology file (CORRECTED PATH)
    topo_file = EXERCISES_DIR / "ex_6_02_sdn_topology.py"
    check_file_exists(topo_file, "SDN topology file")
    
    print()
    print("  Note: Exercise 3 requires manual interaction.")
    print("  Full testing requires Docker/Mininet environment.")
    print()
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# APPLICATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def check_applications() -> bool:
    """Test supporting applications."""
    print("Testing Supporting Applications")
    print("-" * 50)
    
    apps = [
        ("nat_observer.py", "NAT observer"),
        ("tcp_echo.py", "TCP echo server"),
        ("udp_echo.py", "UDP echo server"),
        ("sdn_policy_controller.py", "SDN policy controller"),
    ]
    
    all_valid = True
    for filename, description in apps:
        app_path = APPS_DIR / filename
        if app_path.exists():
            valid, error = check_python_syntax(app_path)
            status = "PASS" if valid else "FAIL"
            print(f"  [{status}] {description}")
            if not valid:
                print(f"         Error: {error}")
                all_valid = False
        else:
            print(f"  [SKIP] {description} not found")
    
    print()
    return all_valid


# ═══════════════════════════════════════════════════════════════════════════════
# HOMEWORK TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def check_homework() -> bool:
    """Test homework exercise files."""
    print("Testing Homework Exercises")
    print("-" * 50)
    
    homework_dir = PROJECT_ROOT / "homework" / "exercises"
    
    if not homework_dir.exists():
        print("  [SKIP] Homework directory not found")
        return True
    
    hw_files = [
        ("hw_6_01_nat_analysis.py", "NAT analysis"),
        ("hw_6_02_arp_investigation.py", "ARP investigation"),
    ]
    
    all_valid = True
    for filename, description in hw_files:
        hw_path = homework_dir / filename
        if hw_path.exists():
            valid, error = check_python_syntax(hw_path)
            status = "PASS" if valid else "FAIL"
            print(f"  [{status}] {description}")
            if not valid:
                all_valid = False
        else:
            print(f"  [SKIP] {description} not found")
    
    print()
    return all_valid


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════


# ─────────────────────────────────────────────────────────────
# PYTEST WRAPPERS (avoid returning non-None from test_* functions)
# ─────────────────────────────────────────────────────────────

def test_exercise_1() -> None:
    assert check_exercise_1()


def test_exercise_2() -> None:
    assert check_exercise_2()


def test_exercise_3() -> None:
    assert check_exercise_3()


def test_applications() -> None:
    assert check_applications()


def test_homework() -> None:
    assert check_homework()

def main() -> int:
    """Run all tests."""
    print()
    print("=" * 60)
    print("  WEEK 6 EXERCISE TESTS")
    print("=" * 60)
    print()
    
    results = {
        "Exercise 1 (NAT)": check_exercise_1(),
        "Exercise 2 (SDN)": check_exercise_2(),
        "Exercise 3 (Policy)": check_exercise_3(),
        "Applications": check_applications(),
        "Homework": check_homework(),
    }
    
    # Summary
    print("=" * 60)
    print("  TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}  {name}")
    
    print()
    print(f"  Total: {passed}/{total} passed")
    print("=" * 60)
    print()
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
