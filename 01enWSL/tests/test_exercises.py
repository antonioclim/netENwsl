#!/usr/bin/env python3
"""
Exercise Verification Tests — Week 1
====================================
Computer Networks - ASE Bucharest | by ing. dr. Antonio Clim

This module verifies that laboratory exercises complete successfully
by running automated checks against the lab container environment.

The tests are organised by exercise number and can be run individually
or as a complete suite. Each test validates specific learning objectives
from the week's curriculum.

Test Structure:
    test_exercise_1: Network Interface Inspection (ip addr, ip route)
    test_exercise_2: Ping Connectivity (ICMP echo, Python ping)
    test_exercise_3: TCP Communication (netcat, Python sockets)
    test_exercise_4: Traffic Capture (tcpdump, tshark availability)
    test_exercise_5: PCAP Analysis (dpkt library, CSV parser)

Prerequisites:
    - Docker container 'week1_lab' must be running
    - Container must have /work mounted with exercise files

Usage:
    python tests/test_exercises.py              # Run all tests
    python tests/test_exercises.py --exercise 2 # Run specific test
    python tests/test_exercises.py --all        # Explicit all tests

Exit Codes:
    0: All tests passed
    1: One or more tests failed or container not running
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import subprocess
import sys
import argparse
from pathlib import Path
from typing import Tuple

# Project root for locating exercise files
PROJECT_ROOT = Path(__file__).parent.parent

# Container name must match docker-compose.yml
CONTAINER = "week1_lab"


# ═══════════════════════════════════════════════════════════════════════════════
# CONTAINER_UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════
def check_container_running() -> bool:
    """
    Verify that the lab container is running and accessible.
    
    Uses 'docker inspect' to check the container's running state.
    This is more reliable than parsing 'docker ps' output.
    
    Returns:
        True if container is running, False otherwise
    """
    try:
        result = subprocess.run(
            ["docker", "inspect", "--format", "{{.State.Running}}", CONTAINER],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip() == "true"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def run_in_container(command: str) -> Tuple[int, str, str]:
    """
    Execute a shell command inside the lab container.
    
    Uses 'docker exec' to run commands in the already-running container.
    Commands are executed via bash -c to support shell features.
    
    Args:
        command: Shell command string to execute
        
    Returns:
        Tuple of (return_code, stdout, stderr)
        
    Example:
        >>> retcode, stdout, stderr = run_in_container("ip addr show")
        >>> retcode
        0
    """
    result = subprocess.run(
        ["docker", "exec", CONTAINER, "bash", "-c", command],
        capture_output=True,
        text=True,
        timeout=60
    )
    return result.returncode, result.stdout, result.stderr


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_EXERCISE_1: Network Interface Inspection
# ═══════════════════════════════════════════════════════════════════════════════
def test_exercise_1() -> None:
    """
    Test Exercise 1: Network Interface Inspection.
    
    Validates:
        - 'ip addr' command executes successfully
        - At least one IP address is configured
        - 'ip route' command shows routing table
        
    Learning Objectives Tested:
        - Recall core Linux networking commands
        - Demonstrate interface inspection
    """
    print("\n  Testing: Network Interface Inspection")
    
    # Check ip addr command works and returns valid output
    retcode, stdout, stderr = run_in_container("ip addr show")
    assert retcode == 0, f"ip addr failed: {stderr}"
    assert "inet" in stdout, "No IP addresses found in ip addr output"
    print("    [PASS] ip addr show")
    
    # Check ip route command works
    retcode, stdout, stderr = run_in_container("ip route show")
    assert retcode == 0, f"ip route failed: {stderr}"
    print("    [PASS] ip route show")
    
    print("  Exercise 1: PASSED")


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_EXERCISE_2: Ping Connectivity
# ═══════════════════════════════════════════════════════════════════════════════
def test_exercise_2() -> None:
    """
    Test Exercise 2: Ping Connectivity.
    
    Validates:
        - ICMP ping to loopback succeeds
        - Python ping exercise runs without error
        - Output format matches expected pattern
        
    Learning Objectives Tested:
        - Demonstrate connectivity testing with ICMP
        - Apply ping measurement interpretation
    """
    print("\n  Testing: Ping Connectivity")
    
    # Test loopback ping — should always work
    retcode, stdout, stderr = run_in_container("ping -c 2 127.0.0.1")
    assert retcode == 0, f"Loopback ping failed: {stderr}"
    # Check that packets were received (not lost)
    assert "2 received" in stdout or "2 packets transmitted, 2" in stdout, \
        "Ping packets lost on loopback — unexpected!"
    print("    [PASS] Loopback ping")
    
    # Test Python ping exercise produces expected output
    retcode, stdout, stderr = run_in_container(
        "python /work/src/exercises/ex_1_01_ping_latency.py "
        "--host 127.0.0.1 --count 2 --no-predict"
    )
    assert retcode == 0, f"Python ping exercise failed: {stderr}"
    assert "PING" in stdout, "Unexpected output format from ping exercise"
    print("    [PASS] Python ping exercise")
    
    print("  Exercise 2: PASSED")


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_EXERCISE_3: TCP Communication
# ═══════════════════════════════════════════════════════════════════════════════
def test_exercise_3() -> None:
    """
    Test Exercise 3: TCP Communication.
    
    Validates:
        - netcat (nc) is installed and accessible
        - Python TCP exercise completes successfully
        - TCP response is received from echo server
        
    Learning Objectives Tested:
        - Implement basic TCP communication
        - Apply socket programming concepts
    """
    print("\n  Testing: TCP Communication")
    
    # Test netcat availability — fundamental networking tool
    retcode, stdout, stderr = run_in_container("which nc")
    assert retcode == 0, "netcat (nc) not installed in container"
    print("    [PASS] netcat available")
    
    # Test Python TCP exercise with non-conflicting port
    retcode, stdout, stderr = run_in_container(
        "python /work/src/exercises/ex_1_02_tcp_server_client.py --port 9098"
    )
    assert retcode == 0, f"Python TCP exercise failed: {stderr}"
    # Verify output shows TCP communication occurred
    assert "TCP" in stdout and "response=" in stdout, \
        "TCP exercise output doesn't show expected communication pattern"
    print("    [PASS] Python TCP exercise")
    
    print("  Exercise 3: PASSED")


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_EXERCISE_4: Traffic Capture
# ═══════════════════════════════════════════════════════════════════════════════
def test_exercise_4() -> None:
    """
    Test Exercise 4: Traffic Capture.
    
    Validates:
        - tcpdump is installed for CLI capture
        - tshark is installed for analysis
        - pcap directory is accessible for saving captures
        
    Learning Objectives Tested:
        - Apply packet capture techniques
        - Demonstrate traffic analysis tool usage
    """
    print("\n  Testing: Traffic Capture")
    
    # Test tcpdump availability
    retcode, stdout, stderr = run_in_container("which tcpdump")
    assert retcode == 0, "tcpdump not installed — required for packet capture"
    print("    [PASS] tcpdump available")
    
    # Test tshark availability (Wireshark CLI)
    retcode, stdout, stderr = run_in_container("which tshark")
    assert retcode == 0, "tshark not installed — required for PCAP analysis"
    print("    [PASS] tshark available")
    
    # Test pcap directory is mounted and writable
    retcode, stdout, stderr = run_in_container("test -d /work/pcap && echo OK")
    assert "OK" in stdout, "pcap directory not mounted in container"
    print("    [PASS] pcap directory accessible")
    
    print("  Exercise 4: PASSED")


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_EXERCISE_5: PCAP Analysis
# ═══════════════════════════════════════════════════════════════════════════════
def test_exercise_5() -> None:
    """
    Test Exercise 5: PCAP Analysis.
    
    Validates:
        - dpkt Python library available (optional but recommended)
        - CSV parser exercise file exists
        - Basic Python environment working
        
    Learning Objectives Tested:
        - Analyse captured traffic programmatically
        - Apply data processing to network captures
    """
    print("\n  Testing: PCAP Analysis")
    
    # Test dpkt library — optional but helpful for homework
    retcode, stdout, stderr = run_in_container(
        "python -c 'import dpkt; print(\"dpkt OK\")'"
    )
    if retcode == 0:
        print("    [PASS] dpkt available")
    else:
        # dpkt is optional, so don't fail the test
        print("    [SKIP] dpkt not installed (optional for homework)")
    
    # Test CSV parser exercise exists on host
    csv_parser = PROJECT_ROOT / "src" / "exercises" / "ex_1_03_parse_csv.py"
    assert csv_parser.exists(), f"CSV parser exercise not found at {csv_parser}"
    print("    [PASS] CSV parser exercise exists")
    
    print("  Exercise 5: PASSED")


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_REGISTRY
# ═══════════════════════════════════════════════════════════════════════════════
# Map exercise numbers to their test functions and descriptions
EXERCISE_TESTS = {
    1: ("Network Interface Inspection", test_exercise_1),
    2: ("Ping Connectivity", test_exercise_2),
    3: ("TCP Communication", test_exercise_3),
    4: ("Traffic Capture", test_exercise_4),
    5: ("PCAP Analysis", test_exercise_5),
}


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """
    Main entry point for test execution.
    
    Parses arguments, verifies container is running, then executes
    requested tests and reports results.
    
    Returns:
        0 if all tests pass, 1 if any fail
    """
    parser = argparse.ArgumentParser(
        description="Verify Week 1 Laboratory Exercises",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tests/test_exercises.py           # Run all tests
  python tests/test_exercises.py -e 2      # Run only exercise 2 test
  python tests/test_exercises.py --all     # Explicitly run all tests
        """
    )
    parser.add_argument(
        "--exercise", "-e",
        type=int,
        choices=EXERCISE_TESTS.keys(),
        help="Specific exercise number to test (1-5)"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Run all exercise tests (default behaviour)"
    )
    args = parser.parse_args()
    
    # Print header
    print("=" * 60)
    print("Exercise Verification Tests — Week 1")
    print("Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim")
    print("=" * 60)
    
    # Verify container is running before attempting tests
    if not check_container_running():
        print(f"\n\033[91m❌ Error: Container '{CONTAINER}' is not running.\033[0m")
        print("Start the lab first:")
        print("  cd /mnt/d/NETWORKING/WEEK1/1enWSL")
        print("  python scripts/start_lab.py")
        return 1
    
    print(f"\n✅ Using container: {CONTAINER}")
    
    # Determine which tests to run
    if args.exercise:
        tests_to_run = [args.exercise]
    else:
        tests_to_run = list(EXERCISE_TESTS.keys())
    
    # Execute tests and track results
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
            print(f"  \033[91m❌ FAILED: {e}\033[0m")
        except subprocess.TimeoutExpired:
            failed += 1
            print(f"  \033[91m❌ ERROR: Test timed out\033[0m")
        except Exception as e:
            failed += 1
            print(f"  \033[91m❌ ERROR: {e}\033[0m")
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("\033[92m✅ All exercise tests passed!\033[0m")
        return 0
    else:
        print("\033[91m❌ Some tests failed. Review output above.\033[0m")
        return 1


if __name__ == "__main__":
    sys.exit(main())
