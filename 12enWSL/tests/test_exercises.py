#!/usr/bin/env python3
"""
Exercise Verification Tests
===========================
Computer Networks - Week 12 (WSL Environment)
ASE Bucharest | by ing. dr. Antonio Clim

Tests to verify that laboratory exercises complete successfully.
Run these after starting the laboratory environment.

Usage:
    python3 tests/test_exercises.py              # Run all tests
    python3 tests/test_exercises.py -e 1         # Run Exercise 1 tests only
    python3 tests/test_exercises.py -e 2         # Run Exercise 2 tests only
    python3 tests/test_exercises.py -v           # Verbose output
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import sys
import argparse
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any

import pytest

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT_UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════
from scripts.utils.network_utils import (
    SMTPTester,
    JSONRPCTester,
    XMLRPCTester,
    check_port,
)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_MARKERS
# ═══════════════════════════════════════════════════════════════════════════════
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


# ═══════════════════════════════════════════════════════════════════════════════
# EXERCISE_1_TESTS: SMTP Protocol (ex_12_01_explore_smtp.py)
# ═══════════════════════════════════════════════════════════════════════════════
class TestExercise1SMTP:
    """
    Tests for Exercise 12.01: Explore SMTP Protocol.
    
    These tests verify that the SMTP server is functioning correctly
    and that students can complete the manual SMTP dialogue.
    """
    
    @requires_smtp
    def test_smtp_connection(self) -> bool:
        """Should connect to SMTP server and receive 220 greeting."""
        tester = SMTPTester("127.0.0.1", 1025)
        try:
            greeting = tester.connect()
            assert greeting.code == 220, f"Expected 220, got {greeting.code}"
            assert "SMTP" in greeting.message or "ready" in greeting.message.lower()
        finally:
            tester.close()
    
    @requires_smtp
    def test_smtp_ehlo(self) -> bool:
        """Should respond to EHLO command with 250."""
        tester = SMTPTester("127.0.0.1", 1025)
        try:
            tester.connect()
            ehlo = tester.send_command("EHLO test.client")
            assert ehlo.code == 250, f"Expected 250, got {ehlo.code}"
        finally:
            tester.close()
    
    @requires_smtp
    def test_smtp_mail_transaction(self) -> bool:
        """Should complete a full mail transaction."""
        tester = SMTPTester("127.0.0.1", 1025)
        try:
            tester.connect()
            tester.send_command("EHLO test.client")
            
            mail_from = tester.send_command("MAIL FROM:<test@example.com>")
            assert mail_from.code == 250, f"MAIL FROM failed: {mail_from.code}"
            
            rcpt_to = tester.send_command("RCPT TO:<recipient@example.com>")
            assert rcpt_to.code == 250, f"RCPT TO failed: {rcpt_to.code}"
            
            data = tester.send_command("DATA")
            assert data.code == 354, f"DATA should return 354, got {data.code}"
            
            result = tester.send_data("Subject: Test\n\nTest message body")
            assert result.code == 250, f"Message not accepted: {result.code}"
        finally:
            tester.close()
    
    @requires_smtp
    def test_smtp_quit(self) -> bool:
        """Should respond correctly to QUIT command with 221."""
        tester = SMTPTester("127.0.0.1", 1025)
        try:
            tester.connect()
            quit_response = tester.send_command("QUIT")
            assert quit_response.code == 221, f"Expected 221, got {quit_response.code}"
        finally:
            tester.close()
    
    @requires_smtp
    def test_smtp_data_returns_354(self) -> bool:
        """
        DATA command should return 354, NOT 250.
        
        This is a common misconception — students expect all successful
        commands to return 250, but DATA returns 354 to indicate
        "ready for message content".
        """
        tester = SMTPTester("127.0.0.1", 1025)
        try:
            tester.connect()
            tester.send_command("EHLO test.client")
            tester.send_command("MAIL FROM:<test@example.com>")
            tester.send_command("RCPT TO:<recipient@example.com>")
            
            data = tester.send_command("DATA")
            assert data.code == 354, (
                f"DATA should return 354 (intermediate), not {data.code}. "
                "See docs/misconceptions.md for explanation."
            )
        finally:
            tester.close()


# ═══════════════════════════════════════════════════════════════════════════════
# EXERCISE_2_TESTS: RPC Protocols (ex_12_02_compare_rpc.py)
# ═══════════════════════════════════════════════════════════════════════════════
class TestExercise2JSONRPC:
    """
    Tests for Exercise 12.02: Compare RPC Protocols — JSON-RPC section.
    """
    
    @requires_jsonrpc
    def test_jsonrpc_add(self) -> bool:
        """Should correctly add two numbers."""
        tester = JSONRPCTester("http://127.0.0.1:6200")
        result = tester.call("add", [10, 32])
        assert result.success, f"Call failed: {result.error}"
        assert result.result == 42.0, f"Expected 42, got {result.result}"
    
    @requires_jsonrpc
    def test_jsonrpc_subtract(self) -> bool:
        """Should correctly subtract two numbers."""
        tester = JSONRPCTester("http://127.0.0.1:6200")
        result = tester.call("subtract", [100, 58])
        assert result.success, f"Call failed: {result.error}"
        assert result.result == 42.0, f"Expected 42, got {result.result}"
    
    @requires_jsonrpc
    def test_jsonrpc_multiply(self) -> bool:
        """Should correctly multiply two numbers."""
        tester = JSONRPCTester("http://127.0.0.1:6200")
        result = tester.call("multiply", [6, 7])
        assert result.success, f"Call failed: {result.error}"
        assert result.result == 42.0, f"Expected 42, got {result.result}"
    
    @requires_jsonrpc
    def test_jsonrpc_divide(self) -> bool:
        """Should correctly divide two numbers."""
        tester = JSONRPCTester("http://127.0.0.1:6200")
        result = tester.call("divide", [84, 2])
        assert result.success, f"Call failed: {result.error}"
        assert result.result == 42.0, f"Expected 42, got {result.result}"
    
    @requires_jsonrpc
    def test_jsonrpc_divide_by_zero(self) -> bool:
        """Should return error for division by zero."""
        tester = JSONRPCTester("http://127.0.0.1:6200")
        result = tester.call("divide", [1, 0])
        assert not result.success, "Expected error for division by zero"
        assert result.error is not None
    
    @requires_jsonrpc
    def test_jsonrpc_method_not_found(self) -> bool:
        """
        Should return error code -32601 for non-existent method.
        
        Note: This still returns HTTP 200! The error is in the JSON body.
        See docs/misconceptions.md for why.
        """
        tester = JSONRPCTester("http://127.0.0.1:6200")
        result = tester.call("nonexistent_method")
        assert not result.success, "Expected error for non-existent method"
        assert result.error is not None
        assert result.error.get("code") == -32601, (
            f"Expected error code -32601, got {result.error.get('code')}"
        )
    
    @requires_jsonrpc
    def test_jsonrpc_batch(self) -> bool:
        """Should handle batch requests correctly."""
        tester = JSONRPCTester("http://127.0.0.1:6200")
        results = tester.batch_call([
            ("add", [1, 2]),
            ("multiply", [3, 4]),
        ])
        assert len(results) == 2, f"Expected 2 results, got {len(results)}"
        assert results[0].success and results[0].result == 3.0
        assert results[1].success and results[1].result == 12.0


# ═══════════════════════════════════════════════════════════════════════════════
# EXERCISE_3_TESTS: XML-RPC (part of ex_12_02_compare_rpc.py)
# ═══════════════════════════════════════════════════════════════════════════════
class TestExercise3XMLRPC:
    """
    Tests for Exercise 12.02: Compare RPC Protocols — XML-RPC section.
    """
    
    @requires_xmlrpc
    def test_xmlrpc_add(self) -> bool:
        """Should correctly add two numbers."""
        tester = XMLRPCTester("http://127.0.0.1:6201")
        result = tester.call("add", 10, 32)
        assert result.success, f"Call failed: {result.error}"
        assert result.result == 42.0, f"Expected 42, got {result.result}"
    
    @requires_xmlrpc
    def test_xmlrpc_introspection(self) -> bool:
        """Should support introspection methods."""
        tester = XMLRPCTester("http://127.0.0.1:6201")
        result = tester.call("system.listMethods")
        assert result.success, f"Introspection failed: {result.error}"
        assert isinstance(result.result, list)
        assert "add" in result.result, "Expected 'add' in method list"


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_RUNNER
# ═══════════════════════════════════════════════════════════════════════════════
def run_exercise_tests(exercise: int = None) -> int:
    """
    Run tests for specific exercise or all exercises.
    
    Args:
        exercise: Exercise number (1, 2, or 3) or None for all
    
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


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
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
