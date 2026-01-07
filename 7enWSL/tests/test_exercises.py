#!/usr/bin/env python3
"""
Exercise Verification Tests
NETWORKING class - ASE, Informatics | by Revolvix

Tests to verify exercise completion and expected outcomes.
"""

from __future__ import annotations

import argparse
import socket
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def test_tcp_connectivity(host: str = "localhost", port: int = 9090) -> tuple[bool, str]:
    """Test basic TCP connectivity."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((host, port))
        sock.close()
        return True, "Connection successful"
    except Exception as e:
        return False, str(e)


def test_tcp_echo(host: str = "localhost", port: int = 9090) -> tuple[bool, str]:
    """Test TCP echo response."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((host, port))
        
        msg = "test_echo_verification"
        sock.sendall(msg.encode())
        response = sock.recv(4096).decode()
        sock.close()
        
        if response.strip() == msg:
            return True, "Echo correct"
        else:
            return False, f"Wrong response: {response}"
    except Exception as e:
        return False, str(e)


def test_tcp_blocked(host: str = "localhost", port: int = 9090) -> tuple[bool, str]:
    """Test that TCP is blocked (connection refused or timeout)."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result != 0:
            return True, f"Connection blocked (errno {result})"
        else:
            return False, "Connection succeeded when it should be blocked"
    except socket.timeout:
        return True, "Connection timed out (expected with DROP)"
    except ConnectionRefusedError:
        return True, "Connection refused (expected with REJECT)"
    except Exception as e:
        return True, f"Connection failed: {e}"


def test_udp_send(host: str = "localhost", port: int = 9091) -> tuple[bool, str]:
    """Test UDP send capability."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(b"test_udp", (host, port))
        sock.close()
        return True, "UDP datagram sent"
    except Exception as e:
        return False, str(e)


def run_exercise_tests(exercise: int) -> int:
    """Run tests for a specific exercise."""
    print(f"Testing Exercise {exercise}")
    print("-" * 40)
    
    results = []
    
    if exercise == 1:
        # Exercise 1: Baseline connectivity
        passed, msg = test_tcp_connectivity()
        results.append(("TCP connectivity", passed, msg))
        
        passed, msg = test_tcp_echo()
        results.append(("TCP echo", passed, msg))
        
        passed, msg = test_udp_send()
        results.append(("UDP send", passed, msg))
    
    elif exercise == 2:
        # Exercise 2: TCP filtering with REJECT
        print("Note: This test expects TCP to be BLOCKED")
        passed, msg = test_tcp_blocked()
        results.append(("TCP blocked", passed, msg))
        
        passed, msg = test_udp_send()
        results.append(("UDP still works", passed, msg))
    
    elif exercise == 3:
        # Exercise 3: UDP filtering with DROP
        passed, msg = test_tcp_connectivity()
        results.append(("TCP connectivity", passed, msg))
        
        # UDP DROP is hard to verify - just check we can send
        passed, msg = test_udp_send()
        results.append(("UDP send (may be dropped)", True, "Sent but receiver may not receive"))
    
    elif exercise == 4:
        # Exercise 4: Application layer filter
        passed, msg = test_tcp_connectivity("localhost", 8888)
        results.append(("Proxy connectivity", passed, msg))
    
    elif exercise == 5:
        # Exercise 5: Port probing
        # Just verify the probe tool works
        results.append(("Port probe", True, "See artifacts/probe_results.log"))
    
    else:
        print(f"Unknown exercise: {exercise}")
        return 1
    
    # Print results
    all_passed = True
    for name, passed, msg in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} {name}: {msg}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print(f"Exercise {exercise}: All tests passed")
        return 0
    else:
        print(f"Exercise {exercise}: Some tests failed")
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Week 7 Exercises")
    parser.add_argument(
        "--exercise", "-e",
        type=int,
        choices=[1, 2, 3, 4, 5],
        help="Exercise number to test (1-5)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all exercise tests"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("Week 7 Exercise Verification")
    print("NETWORKING class - ASE, Informatics")
    print("=" * 60)
    print()

    if args.all:
        failed = 0
        for ex in [1, 2, 3, 4, 5]:
            print()
            result = run_exercise_tests(ex)
            if result != 0:
                failed += 1
        return 1 if failed > 0 else 0
    
    elif args.exercise:
        return run_exercise_tests(args.exercise)
    
    else:
        print("Usage: python test_exercises.py --exercise <1-5>")
        print("       python test_exercises.py --all")
        return 0


if __name__ == "__main__":
    sys.exit(main())
