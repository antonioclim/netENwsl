#!/usr/bin/env python3
"""
Exercise Verification Tests
NETWORKING class - ASE, Informatics | by Revolvix

Tests to verify that laboratory exercises complete successfully.
Run these after starting the laboratory environment.
"""

import sys
import argparse
from pathlib import Path

import pytest

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.network_utils import (
    SMTPTester,
    JSONRPCTester,
    XMLRPCTester,
    check_port,
)


# Markers for conditional test execution
requires_smtp = pytest.mark.skipif(
    not check_port("127.0.0.1", 1025),
    reason="SMTP server not running on port 1025"
)
requires_jsonrpc = pytest.mark.skipif(
    not check_port("127.0.0.1", 6200),
    reason="JSON-RPC server not running on port 6200"
)
requires_xmlrpc = pytest.mark.skipif(
    not check_port("127.0.0.1", 6201),
    reason="XML-RPC server not running on port 6201"
)


class TestExercise1SMTP:
    """Tests for Exercise 1: SMTP Protocol."""
    
    @requires_smtp
    def test_smtp_connection(self):
        """Should connect to SMTP server and receive greeting."""
        tester = SMTPTester("127.0.0.1", 1025)
        try:
            greeting = tester.connect()
            assert greeting.code == 220, f"Expected 220, got {greeting.code}"
            assert "SMTP" in greeting.message or "ready" in greeting.message.lower()
        finally:
            tester.close()
    
    @requires_smtp
    def test_smtp_ehlo(self):
        """Should respond to EHLO command."""
        tester = SMTPTester("127.0.0.1", 1025)
        try:
            tester.connect()
            ehlo = tester.send_command("EHLO test.client")
            assert ehlo.code == 250, f"Expected 250, got {ehlo.code}"
        finally:
            tester.close()
    
    @requires_smtp
    def test_smtp_mail_transaction(self):
        """Should complete a full mail transaction."""
        tester = SMTPTester("127.0.0.1", 1025)
        try:
            tester.connect()
            tester.send_command("EHLO test.client")
            
            mail_from = tester.send_command("MAIL FROM:<test@example.com>")
            assert mail_from.code == 250
            
            rcpt_to = tester.send_command("RCPT TO:<recipient@example.com>")
            assert rcpt_to.code == 250
            
            data = tester.send_command("DATA")
            assert data.code == 354
            
            result = tester.send_data("Subject: Test\n\nTest message body")
            assert result.code == 250
        finally:
            tester.close()
    
    @requires_smtp
    def test_smtp_quit(self):
        """Should respond correctly to QUIT command."""
        tester = SMTPTester("127.0.0.1", 1025)
        try:
            tester.connect()
            quit_response = tester.send_command("QUIT")
            assert quit_response.code == 221
        finally:
            tester.close()


class TestExercise2JSONRPC:
    """Tests for Exercise 2: JSON-RPC Implementation."""
    
    @requires_jsonrpc
    def test_jsonrpc_add(self):
        """Should correctly add two numbers."""
        tester = JSONRPCTester("http://127.0.0.1:6200")
        result = tester.call("add", [10, 32])
        assert result.success, f"Call failed: {result.error}"
        assert result.result == 42.0
    
    @requires_jsonrpc
    def test_jsonrpc_subtract(self):
        """Should correctly subtract two numbers."""
        tester = JSONRPCTester("http://127.0.0.1:6200")
        result = tester.call("subtract", [100, 58])
        assert result.success
        assert result.result == 42.0
    
    @requires_jsonrpc
    def test_jsonrpc_multiply(self):
        """Should correctly multiply two numbers."""
        tester = JSONRPCTester("http://127.0.0.1:6200")
        result = tester.call("multiply", [6, 7])
        assert result.success
        assert result.result == 42.0
    
    @requires_jsonrpc
    def test_jsonrpc_divide(self):
        """Should correctly divide two numbers."""
        tester = JSONRPCTester("http://127.0.0.1:6200")
        result = tester.call("divide", [84, 2])
        assert result.success
        assert result.result == 42.0
    
    @requires_jsonrpc
    def test_jsonrpc_divide_by_zero(self):
        """Should return error for division by zero."""
        tester = JSONRPCTester("http://127.0.0.1:6200")
        result = tester.call("divide", [1, 0])
        assert not result.success, "Expected error for division by zero"
        assert result.error is not None
    
    @requires_jsonrpc
    def test_jsonrpc_method_not_found(self):
        """Should return error for non-existent method."""
        tester = JSONRPCTester("http://127.0.0.1:6200")
        result = tester.call("nonexistent_method")
        assert not result.success
        assert result.error is not None
        assert result.error.get("code") == -32601  # Method not found
    
    @requires_jsonrpc
    def test_jsonrpc_batch(self):
        """Should handle batch requests."""
        tester = JSONRPCTester("http://127.0.0.1:6200")
        results = tester.batch_call([
            ("add", [1, 2]),
            ("multiply", [3, 4]),
        ])
        assert len(results) == 2
        assert results[0].success and results[0].result == 3.0
        assert results[1].success and results[1].result == 12.0


class TestExercise3XMLRPC:
    """Tests for Exercise 3: XML-RPC Comparison."""
    
    @requires_xmlrpc
    def test_xmlrpc_add(self):
        """Should correctly add two numbers."""
        tester = XMLRPCTester("http://127.0.0.1:6201")
        result = tester.call("add", 10, 32)
        assert result.success
        assert result.result == 42.0
    
    @requires_xmlrpc
    def test_xmlrpc_introspection(self):
        """Should support introspection methods."""
        tester = XMLRPCTester("http://127.0.0.1:6201")
        result = tester.call("system.listMethods")
        assert result.success
        assert isinstance(result.result, list)
        assert "add" in result.result


def run_exercise_tests(exercise: int = None) -> int:
    """
    Run tests for specific exercise or all exercises.
    
    Args:
        exercise: Exercise number (1-3) or None for all
    
    Returns:
        Exit code (0 for success)
    """
    args = [__file__, "-v"]
    
    if exercise == 1:
        args.append("TestExercise1SMTP")
    elif exercise == 2:
        args.append("TestExercise2JSONRPC")
    elif exercise == 3:
        args.append("TestExercise3XMLRPC")
    
    return pytest.main(args)


def main() -> int:
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description="Verify Week 12 exercises"
    )
    parser.add_argument(
        "--exercise", "-e",
        type=int,
        choices=[1, 2, 3],
        help="Specific exercise to test (default: all)"
    )
    
    args = parser.parse_args()
    return run_exercise_tests(args.exercise)


if __name__ == "__main__":
    sys.exit(main())
