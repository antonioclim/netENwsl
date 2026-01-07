#!/usr/bin/env python3
"""
Week 10 Exercise Verification Tests
NETWORKING class - ASE, Informatics | by Revolvix

Tests that verify each laboratory exercise works correctly.
"""

import subprocess
import socket
import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def check_tcp_port(host: str, port: int, timeout: float = 5.0) -> bool:
    """Check if a TCP port is open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return result == 0
    except Exception:
        return False


def test_exercise_1():
    """Test Exercise 1: HTTP Service."""
    print("Testing Exercise 1: HTTP Service")
    
    if not check_tcp_port("127.0.0.1", 8000):
        print("  ✗ HTTP server not running on port 8000")
        return False
    
    try:
        import urllib.request
        with urllib.request.urlopen("http://localhost:8000/", timeout=5) as response:
            if response.getcode() == 200:
                print("  ✓ HTTP server responding")
                return True
    except Exception as e:
        print(f"  ✗ HTTP request failed: {e}")
    
    return False


def test_exercise_2():
    """Test Exercise 2: DNS Service."""
    print("Testing Exercise 2: DNS Service")
    
    try:
        result = subprocess.run(
            ["dig", "@127.0.0.1", "-p", "5353", "myservice.lab.local", "+short"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if "10.10.10.10" in result.stdout:
            print("  ✓ DNS server responding correctly")
            return True
        else:
            print(f"  ✗ Unexpected DNS response: {result.stdout.strip()}")
    except FileNotFoundError:
        print("  ✗ dig command not found (install bind-tools)")
    except Exception as e:
        print(f"  ✗ DNS test failed: {e}")
    
    return False


def test_exercise_3():
    """Test Exercise 3: SSH Service."""
    print("Testing Exercise 3: SSH Service")
    
    if not check_tcp_port("127.0.0.1", 2222):
        print("  ✗ SSH server not running on port 2222")
        return False
    
    try:
        import paramiko
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname="127.0.0.1",
            port=2222,
            username="labuser",
            password="labpass",
            timeout=10
        )
        
        stdin, stdout, stderr = client.exec_command("echo test")
        output = stdout.read().decode().strip()
        client.close()
        
        if output == "test":
            print("  ✓ SSH server accepting connections and commands")
            return True
        else:
            print(f"  ✗ Unexpected SSH output: {output}")
    except ImportError:
        print("  ✗ paramiko not installed")
    except Exception as e:
        print(f"  ✗ SSH test failed: {e}")
    
    return False


def test_exercise_4():
    """Test Exercise 4: FTP Service."""
    print("Testing Exercise 4: FTP Service")
    
    if not check_tcp_port("127.0.0.1", 2121):
        print("  ✗ FTP server not running on port 2121")
        return False
    
    try:
        from ftplib import FTP
        
        ftp = FTP()
        ftp.connect("127.0.0.1", 2121, timeout=10)
        ftp.login("labftp", "labftp")
        ftp.pwd()
        ftp.quit()
        
        print("  ✓ FTP server accepting connections")
        return True
    except Exception as e:
        print(f"  ✗ FTP test failed: {e}")
    
    return False


def test_exercise_5():
    """Test Exercise 5: HTTPS Service."""
    print("Testing Exercise 5: HTTPS Service (selftest)")
    
    exercise_path = PROJECT_ROOT / "src" / "exercises" / "ex_10_01_https.py"
    
    if not exercise_path.exists():
        print(f"  ✗ Exercise file not found: {exercise_path}")
        return False
    
    result = subprocess.run(
        [sys.executable, str(exercise_path), "selftest"],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode == 0:
        print("  ✓ HTTPS selftest passed")
        return True
    else:
        print(f"  ✗ HTTPS selftest failed: {result.stderr}")
        return False


def test_exercise_6():
    """Test Exercise 6: REST Maturity Levels."""
    print("Testing Exercise 6: REST Maturity Levels (selftest)")
    
    exercise_path = PROJECT_ROOT / "src" / "exercises" / "ex_10_02_rest_levels.py"
    
    if not exercise_path.exists():
        print(f"  ✗ Exercise file not found: {exercise_path}")
        return False
    
    result = subprocess.run(
        [sys.executable, str(exercise_path), "selftest"],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode == 0:
        print("  ✓ REST maturity selftest passed")
        return True
    else:
        print(f"  ✗ REST selftest failed: {result.stderr}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Test Week 10 Exercises")
    parser.add_argument("--exercise", "-e", type=int, choices=[1, 2, 3, 4, 5, 6],
                        help="Test specific exercise only")
    args = parser.parse_args()
    
    print("=" * 50)
    print("Week 10 Exercise Verification Tests")
    print("=" * 50)
    print()
    
    tests = {
        1: test_exercise_1,
        2: test_exercise_2,
        3: test_exercise_3,
        4: test_exercise_4,
        5: test_exercise_5,
        6: test_exercise_6,
    }
    
    if args.exercise:
        tests = {args.exercise: tests[args.exercise]}
    
    passed = 0
    failed = 0
    
    for num, test in tests.items():
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ✗ Exercise {num}: Unexpected error: {e}")
            failed += 1
        print()
    
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
