#!/usr/bin/env python3
"""
test_exercises.py - Exercise Verification Tests
Week 14 - Integrated Recap
NETWORKING class - ASE, Informatics | by Revolvix

Verifies that laboratory exercises produce expected results.

Usage:
    python tests/test_exercises.py --exercise 1
    python tests/test_exercises.py --exercise 2
    python tests/test_exercises.py --all
"""

from __future__ import annotations

import argparse
import json
import socket
import sys
import time
from collections import Counter
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError


PROJECT_ROOT = Path(__file__).parent.parent


class Colours:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def log(level: str, message: str) -> None:
    """Print log message."""
    colours = {
        "INFO": Colours.BLUE,
        "OK": Colours.GREEN,
        "WARN": Colours.YELLOW,
        "FAIL": Colours.RED,
    }
    colour = colours.get(level, Colours.RESET)
    print(f"  {colour}[{level}]{Colours.RESET} {message}")


def http_get(url: str, timeout: float = 5.0) -> dict:
    """Perform HTTP GET and return response info."""
    try:
        req = Request(url, method="GET")
        start = time.time()
        with urlopen(req, timeout=timeout) as response:
            latency = time.time() - start
            headers = dict(response.getheaders())
            body = response.read().decode("utf-8", errors="replace")
            return {
                "success": True,
                "status": response.status,
                "headers": headers,
                "body": body,
                "latency": latency,
                "x_backend": headers.get("X-Backend"),
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


def test_exercise_1() -> bool:
    """Exercise 1: Environment Verification and Service Discovery."""
    print()
    print(f"{Colours.BOLD}Exercise 1: Environment Verification{Colours.RESET}")
    print("-" * 50)

    passed = 0
    failed = 0

    # Test load balancer
    log("INFO", "Testing load balancer...")
    result = http_get("http://localhost:8080/")
    if result["success"] and result["status"] == 200:
        log("OK", "Load balancer responding (HTTP 200)")
        passed += 1
    else:
        log("FAIL", f"Load balancer not responding: {result.get('error', result.get('status'))}")
        failed += 1

    # Test backends directly
    for port, name in [(8001, "Backend 1"), (8002, "Backend 2")]:
        log("INFO", f"Testing {name}...")
        result = http_get(f"http://localhost:{port}/info")
        if result["success"] and result["status"] == 200:
            try:
                info = json.loads(result["body"])
                log("OK", f"{name} responding: id={info.get('id')}")
                passed += 1
            except json.JSONDecodeError:
                log("WARN", f"{name} responded but invalid JSON")
                passed += 1
        else:
            log("FAIL", f"{name} not responding")
            failed += 1

    # Test LB status endpoint
    log("INFO", "Testing LB status endpoint...")
    result = http_get("http://localhost:8080/lb-status")
    if result["success"] and result["status"] == 200:
        try:
            status = json.loads(result["body"])
            backends = status.get("backends", [])
            log("OK", f"LB status available: {len(backends)} backends configured")
            passed += 1
        except json.JSONDecodeError:
            log("WARN", "LB status endpoint returned invalid JSON")
            passed += 1
    else:
        log("FAIL", "LB status endpoint not responding")
        failed += 1

    print()
    print(f"Result: {Colours.GREEN}{passed} passed{Colours.RESET}, "
          f"{Colours.RED}{failed} failed{Colours.RESET}")

    return failed == 0


def test_exercise_2() -> bool:
    """Exercise 2: Load Balancer Behaviour Analysis."""
    print()
    print(f"{Colours.BOLD}Exercise 2: Load Balancer Behaviour{Colours.RESET}")
    print("-" * 50)

    # Send multiple requests and track backend selection
    log("INFO", "Sending 10 requests through load balancer...")

    backends_selected = []
    for i in range(10):
        result = http_get("http://localhost:8080/")
        if result["success"] and result.get("x_backend"):
            backends_selected.append(result["x_backend"])
            log("INFO", f"Request {i+1}: Backend = {result['x_backend']}")
        else:
            log("WARN", f"Request {i+1}: No X-Backend header")

    print()

    if len(backends_selected) < 8:
        log("FAIL", "Too few successful requests")
        return False

    # Check distribution
    counter = Counter(backends_selected)
    log("INFO", f"Distribution: {dict(counter)}")

    # Verify round-robin pattern (both backends should be used)
    if len(counter) >= 2:
        log("OK", "Both backends are being used")

        # Check for alternation
        alternations = 0
        for i in range(1, len(backends_selected)):
            if backends_selected[i] != backends_selected[i-1]:
                alternations += 1

        if alternations >= 7:
            log("OK", f"Round-robin pattern detected ({alternations} alternations)")
        else:
            log("WARN", f"Limited alternation ({alternations} alternations)")

        return True
    else:
        log("FAIL", "Only one backend is being used - check load balancer configuration")
        return False


def test_exercise_3() -> bool:
    """Exercise 3: TCP Echo Protocol Testing."""
    print()
    print(f"{Colours.BOLD}Exercise 3: TCP Echo Protocol{Colours.RESET}")
    print("-" * 50)

    passed = 0
    failed = 0

    test_messages = [
        "hello",
        "week14",
        "networking",
        "A" * 50,
    ]

    for msg in test_messages:
        log("INFO", f"Testing echo: '{msg[:20]}{'...' if len(msg) > 20 else ''}'")

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(("localhost", 9000))

            sock.sendall((msg + "\n").encode())
            response = sock.recv(4096).decode().strip()
            sock.close()

            if msg in response:
                log("OK", f"Echo valid (received {len(response)} bytes)")
                passed += 1
            else:
                log("FAIL", f"Echo mismatch: sent '{msg}', got '{response}'")
                failed += 1

        except socket.timeout:
            log("FAIL", "Connection timed out")
            failed += 1
        except ConnectionRefusedError:
            log("FAIL", "Connection refused - is echo server running?")
            failed += 1
        except Exception as e:
            log("FAIL", f"Error: {e}")
            failed += 1

    print()
    print(f"Result: {Colours.GREEN}{passed} passed{Colours.RESET}, "
          f"{Colours.RED}{failed} failed{Colours.RESET}")

    return failed == 0


def test_exercise_4() -> bool:
    """Exercise 4: Packet Capture and Analysis."""
    print()
    print(f"{Colours.BOLD}Exercise 4: Packet Capture Verification{Colours.RESET}")
    print("-" * 50)

    pcap_dir = PROJECT_ROOT / "pcap"
    pcap_files = list(pcap_dir.glob("*.pcap"))

    if not pcap_files:
        log("WARN", "No PCAP files found in pcap/ directory")
        log("INFO", "Run: python scripts/capture_traffic.py --duration 30 --output pcap/test.pcap")
        return False

    log("INFO", f"Found {len(pcap_files)} PCAP file(s)")

    for pcap_file in pcap_files[:3]:  # Check first 3 files
        size = pcap_file.stat().st_size
        log("INFO", f"  {pcap_file.name}: {size} bytes")

        if size < 100:
            log("WARN", f"  {pcap_file.name} appears to be empty")

    log("OK", "PCAP files present for analysis")
    log("INFO", "Open in Wireshark: wireshark pcap/<filename>.pcap")

    return True


def main() -> int:
    """Run exercise tests."""
    parser = argparse.ArgumentParser(description="Test Week 14 exercises")
    parser.add_argument(
        "--exercise", "-e",
        type=int,
        choices=[1, 2, 3, 4],
        help="Run specific exercise test"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Run all exercise tests"
    )

    args = parser.parse_args()

    print()
    print("=" * 60)
    print(f"  {Colours.BOLD}Exercise Verification - Week 14{Colours.RESET}")
    print("=" * 60)

    tests = {
        1: test_exercise_1,
        2: test_exercise_2,
        3: test_exercise_3,
        4: test_exercise_4,
    }

    results = {}

    if args.all:
        for num, test_func in tests.items():
            results[num] = test_func()
    elif args.exercise:
        results[args.exercise] = tests[args.exercise]()
    else:
        parser.print_help()
        print("\nExamples:")
        print("  python tests/test_exercises.py --exercise 1")
        print("  python tests/test_exercises.py --all")
        return 0

    # Summary
    print()
    print("=" * 60)
    print(f"  {Colours.BOLD}Summary{Colours.RESET}")
    print("=" * 60)

    all_passed = True
    for num, passed in results.items():
        status = f"{Colours.GREEN}PASS{Colours.RESET}" if passed else f"{Colours.RED}FAIL{Colours.RESET}"
        print(f"  Exercise {num}: {status}")
        if not passed:
            all_passed = False

    print()

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
