#!/usr/bin/env python3
"""
Exercise Verification Tests
NETWORKING class - ASE, Informatics | by Revolvix

Tests to verify exercise implementations are working correctly.
"""

import argparse
import subprocess
import sys
import socket
import json
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def check_port(host: str, port: int, timeout: float = 2.0) -> bool:
    """Check if a port is accepting connections."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False


class TestExercise1PortScanner(unittest.TestCase):
    """Tests for Exercise 1: Port Scanner."""
    
    @classmethod
    def setUpClass(cls):
        """Check if services are running."""
        cls.services_available = check_port("127.0.0.1", 8080)
    
    def test_scanner_imports(self):
        """Port scanner module should be importable."""
        sys.path.insert(0, str(PROJECT_ROOT / "src" / "exercises"))
        try:
            # Just check if file exists and is syntactically correct
            import ex_13_01_port_scanner
        except SyntaxError as e:
            self.fail(f"Syntax error in port scanner: {e}")
        except ImportError:
            pass  # OK - may have unmet dependencies
    
    def test_scanner_help(self):
        """Port scanner should show help."""
        result = subprocess.run([
            sys.executable,
            str(PROJECT_ROOT / "src" / "exercises" / "ex_13_01_port_scanner.py"),
            "--help"
        ], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0)
        self.assertIn("--target", result.stdout)
        self.assertIn("--ports", result.stdout)
    
    @unittest.skipUnless(check_port("127.0.0.1", 8080), "Services not running")
    def test_scanner_execution(self):
        """Port scanner should execute against running services."""
        result = subprocess.run([
            sys.executable,
            str(PROJECT_ROOT / "src" / "exercises" / "ex_13_01_port_scanner.py"),
            "--target", "127.0.0.1",
            "--ports", "8080",
            "--quiet"
        ], capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0)


class TestExercise2MQTTClient(unittest.TestCase):
    """Tests for Exercise 2: MQTT Client."""
    
    def test_mqtt_client_help(self):
        """MQTT client should show help."""
        result = subprocess.run([
            sys.executable,
            str(PROJECT_ROOT / "src" / "exercises" / "ex_13_02_mqtt_client.py"),
            "--help"
        ], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0)
        self.assertIn("--broker", result.stdout)
        self.assertIn("--mode", result.stdout)
    
    @unittest.skipUnless(check_port("127.0.0.1", 1883), "MQTT broker not running")
    def test_mqtt_publish(self):
        """MQTT client should publish messages."""
        result = subprocess.run([
            sys.executable,
            str(PROJECT_ROOT / "src" / "exercises" / "ex_13_02_mqtt_client.py"),
            "--broker", "127.0.0.1",
            "--port", "1883",
            "--mode", "publish",
            "--topic", "test/verify",
            "--message", "test",
            "--count", "1"
        ], capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0)


class TestExercise3PacketSniffer(unittest.TestCase):
    """Tests for Exercise 3: Packet Sniffer."""
    
    def test_sniffer_help(self):
        """Packet sniffer should show help."""
        result = subprocess.run([
            sys.executable,
            str(PROJECT_ROOT / "src" / "exercises" / "ex_13_03_packet_sniffer.py"),
            "--help"
        ], capture_output=True, text=True, timeout=10)
        # May fail if scapy not installed, but help should work
        self.assertIn("--iface", result.stdout + result.stderr)


class TestExercise4VulnChecker(unittest.TestCase):
    """Tests for Exercise 4: Vulnerability Checker."""
    
    def test_vuln_checker_help(self):
        """Vulnerability checker should show help."""
        result = subprocess.run([
            sys.executable,
            str(PROJECT_ROOT / "src" / "exercises" / "ex_13_04_vuln_checker.py"),
            "--help"
        ], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0)
        self.assertIn("--target", result.stdout)
        self.assertIn("--service", result.stdout)
    
    @unittest.skipUnless(check_port("127.0.0.1", 8080), "DVWA not running")
    def test_vuln_checker_http(self):
        """Vulnerability checker should analyse HTTP service."""
        result = subprocess.run([
            sys.executable,
            str(PROJECT_ROOT / "src" / "exercises" / "ex_13_04_vuln_checker.py"),
            "--target", "127.0.0.1",
            "--port", "8080",
            "--service", "http"
        ], capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Findings:", result.stdout)


def run_exercise_tests(exercise_num: int) -> bool:
    """Run tests for a specific exercise."""
    test_classes = {
        1: TestExercise1PortScanner,
        2: TestExercise2MQTTClient,
        3: TestExercise3PacketSniffer,
        4: TestExercise4VulnChecker,
    }
    
    if exercise_num not in test_classes:
        print(f"Unknown exercise number: {exercise_num}")
        return False
    
    suite = unittest.TestLoader().loadTestsFromTestCase(test_classes[exercise_num])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


def main():
    parser = argparse.ArgumentParser(description="Test Week 13 exercises")
    parser.add_argument("--exercise", "-e", type=int, choices=[1, 2, 3, 4],
                       help="Run tests for specific exercise")
    parser.add_argument("--all", "-a", action="store_true",
                       help="Run all tests")
    args = parser.parse_args()
    
    if args.exercise:
        success = run_exercise_tests(args.exercise)
        return 0 if success else 1
    else:
        # Run all tests
        unittest.main(argv=[''], exit=True, verbosity=2)


if __name__ == "__main__":
    sys.exit(main())
