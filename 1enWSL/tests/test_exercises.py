#!/usr/bin/env python3
"""
Exercise Verification Tests
NETWORKING class - ASE, Informatics | by Revolvix

Verifies that laboratory exercises complete successfully.
"""

from __future__ import annotations

import subprocess
import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

CONTAINER = "week1_lab"


def check_container_running() -> bool:
    """Check if the lab container is running."""
    try:
        result = subprocess.run(
            ["docker", "inspect", "--format", "{{.State.Running}}", CONTAINER],
            capture_output=True,
            text=True
        )
        return result.stdout.strip() == "true"
    except Exception:
        return False


def run_in_container(command: str) -> tuple[int, str, str]:
    """Execute a command in the lab container."""
    result = subprocess.run(
        ["docker", "exec", CONTAINER, "bash", "-c", command],
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr


def test_exercise_1():
    """Test Exercise 1: Network Interface Inspection."""
    print("\n  Testing: Network Interface Inspection")
    
    # Check ip command works
    retcode, stdout, stderr = run_in_container("ip addr show")
    assert retcode == 0, f"ip addr failed: {stderr}"
    assert "inet" in stdout, "No IP addresses found"
    print("    [PASS] ip addr show")
    
    # Check ip route works
    retcode, stdout, stderr = run_in_container("ip route show")
    assert retcode == 0, f"ip route failed: {stderr}"
    print("    [PASS] ip route show")
    
    print("  Exercise 1: PASSED")


def test_exercise_2():
    """Test Exercise 2: Ping Connectivity."""
    print("\n  Testing: Ping Connectivity")
    
    # Test loopback ping
    retcode, stdout, stderr = run_in_container("ping -c 2 127.0.0.1")
    assert retcode == 0, f"Loopback ping failed: {stderr}"
    assert "2 received" in stdout or "2 packets transmitted, 2" in stdout, \
        "Ping packets lost"
    print("    [PASS] Loopback ping")
    
    # Test Python ping exercise
    retcode, stdout, stderr = run_in_container(
        "python /work/src/exercises/ex_1_01_ping_latency.py --host 127.0.0.1 --count 2"
    )
    assert retcode == 0, f"Python ping exercise failed: {stderr}"
    assert "PING" in stdout, "Unexpected output from ping exercise"
    print("    [PASS] Python ping exercise")
    
    print("  Exercise 2: PASSED")


def test_exercise_3():
    """Test Exercise 3: TCP Communication."""
    print("\n  Testing: TCP Communication")
    
    # Test netcat is available
    retcode, stdout, stderr = run_in_container("which nc")
    assert retcode == 0, "netcat not installed"
    print("    [PASS] netcat available")
    
    # Test Python TCP exercise
    retcode, stdout, stderr = run_in_container(
        "python /work/src/exercises/ex_1_02_tcp_server_client.py --port 9098"
    )
    assert retcode == 0, f"Python TCP exercise failed: {stderr}"
    assert "TCP" in stdout and "response=" in stdout, "Unexpected output from TCP exercise"
    print("    [PASS] Python TCP exercise")
    
    print("  Exercise 3: PASSED")


def test_exercise_4():
    """Test Exercise 4: Traffic Capture."""
    print("\n  Testing: Traffic Capture")
    
    # Test tcpdump is available
    retcode, stdout, stderr = run_in_container("which tcpdump")
    assert retcode == 0, "tcpdump not installed"
    print("    [PASS] tcpdump available")
    
    # Test tshark is available
    retcode, stdout, stderr = run_in_container("which tshark")
    assert retcode == 0, "tshark not installed"
    print("    [PASS] tshark available")
    
    # Test capture directory exists
    retcode, stdout, stderr = run_in_container("test -d /work/pcap && echo OK")
    assert "OK" in stdout, "pcap directory not mounted"
    print("    [PASS] pcap directory accessible")
    
    print("  Exercise 4: PASSED")


def test_exercise_5():
    """Test Exercise 5: PCAP Analysis."""
    print("\n  Testing: PCAP Analysis")
    
    # Test Python packages for PCAP analysis
    retcode, stdout, stderr = run_in_container(
        "python -c 'import dpkt; print(\"dpkt OK\")'"
    )
    # dpkt is optional, so just log if not available
    if retcode == 0:
        print("    [PASS] dpkt available")
    else:
        print("    [SKIP] dpkt not installed (optional)")
    
    # Test CSV parser exercise exists
    csv_parser = PROJECT_ROOT / "src" / "exercises" / "ex_1_03_parse_csv.py"
    assert csv_parser.exists(), "CSV parser exercise not found"
    print("    [PASS] CSV parser exercise exists")
    
    print("  Exercise 5: PASSED")


EXERCISE_TESTS = {
    1: ("Network Interface Inspection", test_exercise_1),
    2: ("Ping Connectivity", test_exercise_2),
    3: ("TCP Communication", test_exercise_3),
    4: ("Traffic Capture", test_exercise_4),
    5: ("PCAP Analysis", test_exercise_5),
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify Week 1 Laboratory Exercises",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--exercise", "-e",
        type=int,
        choices=EXERCISE_TESTS.keys(),
        help="Specific exercise to test"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Test all exercises"
    )
    args = parser.parse_args()
    
    print("=" * 60)
    print("Exercise Verification Tests")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
    print("=" * 60)
    
    # Check container is running
    if not check_container_running():
        print(f"\n\033[91mError: Container '{CONTAINER}' is not running.\033[0m")
        print("Start the lab first: python scripts/start_lab.py")
        return 1
    
    print(f"\nUsing container: {CONTAINER}")
    
    tests_to_run = []
    
    if args.exercise:
        tests_to_run = [args.exercise]
    elif args.all or (not args.exercise):
        tests_to_run = list(EXERCISE_TESTS.keys())
    
    passed = 0
    failed = 0
    
    for ex_num in tests_to_run:
        name, test_func = EXERCISE_TESTS[ex_num]
        print(f"\nExercise {ex_num}: {name}")
        print("-" * 50)
        
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            failed += 1
            print(f"  \033[91mFAILED: {e}\033[0m")
        except Exception as e:
            failed += 1
            print(f"  \033[91mERROR: {e}\033[0m")
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("\033[92mAll exercise tests passed!\033[0m")
        return 0
    else:
        print("\033[91mSome tests failed.\033[0m")
        return 1


if __name__ == "__main__":
    sys.exit(main())
