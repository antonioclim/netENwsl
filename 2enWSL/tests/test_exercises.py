#!/usr/bin/env python3
"""
Week 2 Exercise Tests
NETWORKING class - ASE, Informatics | by Revolvix

Verifies correct operation of TCP and UDP exercises.
"""

import subprocess
import sys
import time
import threading
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


class TestRunner:
    """Exercise test runner."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.src = PROJECT_ROOT / "src" / "exercises"
    
    def check(self, name: str, condition: bool, detail: str = "") -> bool:
        """Record test result."""
        if condition:
            print(f"  ✓ {name}")
            self.passed += 1
        else:
            print(f"  ✗ {name}")
            if detail:
                print(f"    {detail}")
            self.failed += 1
        return condition
    
    def test_tcp_exercise(self) -> bool:
        """Test Exercise 1: TCP server and client."""
        print("\n─ Exercise 1: TCP Server/Client ─")
        
        # Start server
        server = subprocess.Popen(
            [sys.executable, str(self.src / "ex_2_01_tcp.py"),
             "server", "--port", "19090", "--mode", "threaded"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        time.sleep(1)
        
        try:
            # Test client
            result = subprocess.run(
                [sys.executable, str(self.src / "ex_2_01_tcp.py"),
                 "client", "--host", "127.0.0.1", "--port", "19090",
                 "-m", "test message"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            self.check(
                "TCP client connects and receives response",
                result.returncode == 0 and "OK: TEST MESSAGE" in result.stdout,
                result.stdout
            )
            
            # Test uppercase transformation
            result = subprocess.run(
                [sys.executable, str(self.src / "ex_2_01_tcp.py"),
                 "client", "--host", "127.0.0.1", "--port", "19090",
                 "-m", "Hello World"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            self.check(
                "TCP server transforms to uppercase",
                "HELLO WORLD" in result.stdout
            )
            
            return True
            
        finally:
            server.terminate()
            server.wait(timeout=2)
    
    def test_udp_exercise(self) -> bool:
        """Test Exercise 2: UDP server and client."""
        print("\n─ Exercise 2: UDP Server/Client ─")
        
        # Start server
        server = subprocess.Popen(
            [sys.executable, str(self.src / "ex_2_02_udp.py"),
             "server", "--port", "19091"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        time.sleep(1)
        
        try:
            # Test ping
            result = subprocess.run(
                [sys.executable, str(self.src / "ex_2_02_udp.py"),
                 "client", "--host", "127.0.0.1", "--port", "19091",
                 "-o", "ping"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            self.check(
                "UDP ping returns PONG",
                result.returncode == 0 and "PONG" in result.stdout
            )
            
            # Test upper command
            result = subprocess.run(
                [sys.executable, str(self.src / "ex_2_02_udp.py"),
                 "client", "--host", "127.0.0.1", "--port", "19091",
                 "-o", "upper:hello"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            self.check(
                "UDP upper command works",
                "HELLO" in result.stdout
            )
            
            # Test reverse command
            result = subprocess.run(
                [sys.executable, str(self.src / "ex_2_02_udp.py"),
                 "client", "--host", "127.0.0.1", "--port", "19091",
                 "-o", "reverse:abc"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            self.check(
                "UDP reverse command works",
                "cba" in result.stdout
            )
            
            # Test time command
            result = subprocess.run(
                [sys.executable, str(self.src / "ex_2_02_udp.py"),
                 "client", "--host", "127.0.0.1", "--port", "19091",
                 "-o", "time"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            self.check(
                "UDP time command returns timestamp",
                result.returncode == 0 and ":" in result.stdout  # HH:MM:SS format
            )
            
            return True
            
        finally:
            server.terminate()
            server.wait(timeout=2)
    
    def test_capture_setup(self) -> bool:
        """Test Exercise 3: Capture environment."""
        print("\n─ Exercise 3: Traffic Capture Setup ─")
        
        # Check pcap directory exists
        pcap_dir = PROJECT_ROOT / "pcap"
        self.check(
            "PCAP directory exists",
            pcap_dir.exists() and pcap_dir.is_dir()
        )
        
        return True
    
    def summary(self) -> int:
        """Print summary and return exit code."""
        total = self.passed + self.failed
        print()
        print("=" * 50)
        print(f"Results: {self.passed}/{total} tests passed")
        
        if self.failed == 0:
            print("All tests passed!")
            return 0
        else:
            print(f"{self.failed} test(s) failed")
            return 1


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Test Week 2 exercises")
    parser.add_argument("--exercise", "-e", type=int, choices=[1, 2, 3],
                       help="Test specific exercise only")
    args = parser.parse_args()
    
    print()
    print("=" * 50)
    print("  Week 2 Exercise Tests")
    print("=" * 50)
    
    runner = TestRunner()
    
    try:
        if args.exercise is None or args.exercise == 1:
            runner.test_tcp_exercise()
        
        if args.exercise is None or args.exercise == 2:
            runner.test_udp_exercise()
        
        if args.exercise is None or args.exercise == 3:
            runner.test_capture_setup()
        
    except Exception as e:
        print(f"\nTest error: {e}")
        return 1
    
    return runner.summary()


if __name__ == "__main__":
    sys.exit(main())
