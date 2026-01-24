#!/usr/bin/env python3
"""
Exercise Verification Tests
NETWORKING class - ASE, Informatics | by Revolvix

Tests to verify that laboratory exercises have been completed correctly.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations
from typing import Optional, List, Dict, Tuple, Any

import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_exercise_1() -> bool:
    """
    Test Exercise 1: NAT/PAT Configuration.
    
    Verifies:
    - NAT topology can start
    - MASQUERADE rule is configured
    - Private hosts can reach public host
    """
    print("Testing Exercise 1: NAT/PAT Configuration")
    print("-" * 50)
    
    topo_file = PROJECT_ROOT / "src" / "exercises" / "topo_nat.py"
    
    if not topo_file.exists():
        print("  [FAIL] Topology file not found")
        return False
    
    try:
        result = subprocess.run(
            ["sudo", "python3", str(topo_file), "--test"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        output = result.stdout + result.stderr
        
        # Check for expected outputs
        checks = [
            ("NAT topology started", "topology" in output.lower() or "nat" in output.lower()),
            ("MASQUERADE present", "MASQUERADE" in output or "masquerade" in output.lower()),
            ("Tests passed", "PASS" in output or "passed" in output.lower()),
        ]
        
        all_passed = True
        for name, passed in checks:
            status = "PASS" if passed else "FAIL"
            print(f"  [{status}] {name}")
            if not passed:
                all_passed = False
        
        if result.returncode != 0 and all_passed:
            print(f"  [WARN] Exit code {result.returncode} but tests passed")
        
        return all_passed
        
    except subprocess.TimeoutExpired:
        print("  [FAIL] Test timed out")
        return False
    except FileNotFoundError:
        print("  [FAIL] sudo/python3 not available")
        return False
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_exercise_2() -> bool:
    """
    Test Exercise 2: SDN Topology and Flow Observation.
    
    Verifies:
    - SDN topology can start
    - Flow rules are installed
    - Permitted traffic succeeds
    - Blocked traffic fails
    """
    print("Testing Exercise 2: SDN Topology and Flow Observation")
    print("-" * 50)
    
    topo_file = PROJECT_ROOT / "src" / "exercises" / "topo_sdn.py"
    
    if not topo_file.exists():
        print("  [FAIL] Topology file not found")
        return False
    
    try:
        result = subprocess.run(
            ["sudo", "python3", str(topo_file), "--test", "--install-flows"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        output = result.stdout + result.stderr
        
        # Check for expected outputs
        checks = [
            ("SDN topology started", "sdn" in output.lower() or "topology" in output.lower()),
            ("h1 ↔ h2 connectivity (PERMIT)", "PERMIT" in output or "0% packet loss" in output),
            ("h1 → h3 blocked (DROP)", "DROP" in output or "100% packet loss" in output),
            ("Flow table present", "flow" in output.lower() or "dump-flows" in output.lower()),
        ]
        
        all_passed = True
        for name, passed in checks:
            status = "PASS" if passed else "FAIL"
            print(f"  [{status}] {name}")
            if not passed:
                all_passed = False
        
        return all_passed
        
    except subprocess.TimeoutExpired:
        print("  [FAIL] Test timed out")
        return False
    except FileNotFoundError:
        print("  [FAIL] sudo/python3 not available")
        return False
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_exercise_3() -> bool:
    """
    Test Exercise 3: SDN Policy Modification.
    
    This is a manual exercise, so we just verify prerequisites.
    """
    print("Testing Exercise 3: SDN Policy Modification (prerequisites)")
    print("-" * 50)
    
    # Check that ovs-ofctl is available
    try:
        result = subprocess.run(
            ["which", "ovs-ofctl"],
            capture_output=True,
            timeout=5
        )
        ovs_available = result.returncode == 0
    except Exception:
        ovs_available = False
    
    print(f"  [{'PASS' if ovs_available else 'FAIL'}] ovs-ofctl available")
    
    # Check topology file
    topo_file = PROJECT_ROOT / "src" / "exercises" / "topo_sdn.py"
    print(f"  [{'PASS' if topo_file.exists() else 'FAIL'}] SDN topology file present")
    
    # Check apps
    tcp_echo = PROJECT_ROOT / "src" / "apps" / "tcp_echo.py"
    udp_echo = PROJECT_ROOT / "src" / "apps" / "udp_echo.py"
    print(f"  [{'PASS' if tcp_echo.exists() else 'FAIL'}] TCP echo application present")
    print(f"  [{'PASS' if udp_echo.exists() else 'FAIL'}] UDP echo application present")
    
    print()
    print("  Note: Exercise 3 requires manual interaction.")
    print("  Run: python scripts/run_demo.py --demo sdn")
    
    return ovs_available and topo_file.exists()



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Verify Week 6 Laboratory Exercises"
    )
    parser.add_argument(
        "--exercise", "-e",
        type=int,
        choices=[1, 2, 3],
        help="Specific exercise to test (1, 2, or 3)"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Run all tests"
    )
    args = parser.parse_args()
    
    print()
    print("=" * 60)
    print("Week 6 Exercise Verification")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
    print("=" * 60)
    print()
    
    tests = {
        1: test_exercise_1,
        2: test_exercise_2,
        3: test_exercise_3,
    }
    
    results = {}
    
    if args.exercise:
        # Run specific test
        test_func = tests.get(args.exercise)
        if test_func:
            results[args.exercise] = test_func()
    elif args.all:
        # Run all tests
        for num, test_func in tests.items():
            print()
            results[num] = test_func()
    else:
        print("Usage:")
        print("  python tests/test_exercises.py --exercise 1")
        print("  python tests/test_exercises.py --all")
        return 0
    
    # Summary
    print()
    print("=" * 60)
    print("Summary:")
    
    all_passed = True
    for num, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"  Exercise {num}: [{status}]")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
