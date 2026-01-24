#!/usr/bin/env python3
"""
Exercise Test Suite — Week 8: Transport Layer

This module provides automated tests for Week 8 exercises with
pedagogical feedback messages explaining what went wrong.

Author: ing. dr. Antonio Clim
Course: Computer Networks - ASE, CSIE
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import unittest
import sys
import argparse
from pathlib import Path
from typing import Optional

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class TestExercise1HTTPServer(unittest.TestCase):
    """Tests for Exercise 8.01: HTTP Server Implementation."""
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_parse_request_basic(self) -> None:
        """Test basic HTTP request parsing."""
        try:
            from exercises.ex_8_01_http_server import parse_request
        except ImportError:
            self.skipTest("Exercise 1 not implemented yet")
        
        raw: bytes = b"GET /index.html HTTP/1.1\r\nHost: localhost\r\n\r\n"
        result: Optional[dict] = parse_request(raw)
        
        self.assertIsNotNone(
            result,
            "parse_request() returned None. "
            "Check: Are you decoding bytes correctly? "
            "Are you splitting on \\r\\n?"
        )
        
        self.assertEqual(
            result.get('method'), 'GET',
            "Method should be 'GET'. "
            "Check: Are you extracting the first word of the request line?"
        )
        
        self.assertEqual(
            result.get('path'), '/index.html',
            "Path should be '/index.html'. "
            "Check: Are you extracting the second word of the request line?"
        )
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_parse_request_headers_lowercase(self) -> None:
        """Test that headers are normalised to lowercase."""
        try:
            from exercises.ex_8_01_http_server import parse_request
        except ImportError:
            self.skipTest("Exercise 1 not implemented yet")
        
        raw: bytes = b"GET / HTTP/1.1\r\nHost: localhost\r\nUser-Agent: test\r\n\r\n"
        result: Optional[dict] = parse_request(raw)
        
        self.assertIn(
            'host', result.get('headers', {}),
            "Headers should be lowercase. "
            "HTTP headers are case-insensitive, so normalise to lowercase."
        )
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_is_safe_path_basic(self) -> None:
        """Test safe path validation."""
        try:
            from exercises.ex_8_01_http_server import is_safe_path
        except ImportError:
            self.skipTest("Exercise 1 not implemented yet")
        
        self.assertTrue(
            is_safe_path('/index.html', '/var/www'),
            "'/index.html' should be safe within '/var/www'. "
            "Check your path normalisation logic."
        )
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_is_safe_path_traversal_blocked(self) -> None:
        """Test that directory traversal is blocked."""
        try:
            from exercises.ex_8_01_http_server import is_safe_path
        except ImportError:
            self.skipTest("Exercise 1 not implemented yet")
        
        self.assertFalse(
            is_safe_path('/../etc/passwd', '/var/www'),
            "'/../etc/passwd' should be BLOCKED (not safe). "
            "This is a directory traversal attack! "
            "Check: Are you normalising BEFORE joining with docroot?"
        )
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_build_response_format(self) -> None:
        """Test HTTP response format."""
        try:
            from exercises.ex_8_01_http_server import build_response
        except ImportError:
            self.skipTest("Exercise 1 not implemented yet")
        
        response: bytes = build_response(200, {"Content-Type": "text/plain"}, b"Hello")
        
        self.assertTrue(
            response.startswith(b"HTTP/1.1 200 OK\r\n"),
            "Response should start with 'HTTP/1.1 200 OK\\r\\n'. "
            "Check your status line format."
        )
        
        self.assertIn(
            b"\r\n\r\n",
            response,
            "Response must have blank line (\\r\\n\\r\\n) between headers and body. "
            "This is REQUIRED by HTTP specification!"
        )
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_handle_request_head_no_body(self) -> None:
        """Test that HEAD requests return no body."""
        try:
            from exercises.ex_8_01_http_server import handle_request
        except ImportError:
            self.skipTest("Exercise 1 not implemented yet")
        
        # Create minimal docroot
        import tempfile
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test file
            test_file = Path(tmpdir) / "test.txt"
            test_file.write_text("Hello World")
            
            raw: bytes = b"HEAD /test.txt HTTP/1.1\r\nHost: localhost\r\n\r\n"
            response: bytes = handle_request(raw, tmpdir)
            
            # Find where body starts
            header_end: int = response.find(b"\r\n\r\n")
            body: bytes = response[header_end + 4:]
            
            self.assertEqual(
                len(body), 0,
                "HEAD request should return EMPTY body. "
                "Headers should include Content-Length of what GET would return, "
                "but the body itself must be empty."
            )



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class TestExercise2ReverseProxy(unittest.TestCase):
    """Tests for Exercise 8.02: Reverse Proxy."""
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_round_robin_balancer_init(self) -> None:
        """Test RoundRobinBalancer initialisation."""
        try:
            from exercises.ex_8_02_reverse_proxy import RoundRobinBalancer
        except ImportError:
            self.skipTest("Exercise 2 not implemented yet")
        
        backends: list[tuple[str, int]] = [('localhost', 9001), ('localhost', 9002)]
        balancer = RoundRobinBalancer(backends)
        
        self.assertIsNotNone(
            balancer,
            "RoundRobinBalancer should be created successfully."
        )
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_round_robin_balancer_cycling(self) -> None:
        """Test that balancer cycles through backends."""
        try:
            from exercises.ex_8_02_reverse_proxy import RoundRobinBalancer
        except ImportError:
            self.skipTest("Exercise 2 not implemented yet")
        
        backends: list[tuple[str, int]] = [('a', 1), ('b', 2), ('c', 3)]
        balancer = RoundRobinBalancer(backends)
        
        results: list = [balancer.next_backend() for _ in range(6)]
        expected: list = [('a', 1), ('b', 2), ('c', 3), ('a', 1), ('b', 2), ('c', 3)]
        
        self.assertEqual(
            results, expected,
            f"Round-robin should cycle: A→B→C→A→B→C. "
            f"Got: {results}. "
            "Check: Are you using modulo (%) for wraparound?"
        )
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_round_robin_empty_backends(self) -> None:
        """Test balancer with no backends."""
        try:
            from exercises.ex_8_02_reverse_proxy import RoundRobinBalancer
        except ImportError:
            self.skipTest("Exercise 2 not implemented yet")
        
        balancer = RoundRobinBalancer([])
        result = balancer.next_backend()
        
        self.assertIsNone(
            result,
            "next_backend() should return None when no backends available. "
            "Check: Are you handling the empty list case?"
        )
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_add_proxy_headers_xff(self) -> None:
        """Test X-Forwarded-For header injection."""
        try:
            from exercises.ex_8_02_reverse_proxy import add_proxy_headers
        except ImportError:
            self.skipTest("Exercise 2 not implemented yet")
        
        original: str = "GET / HTTP/1.1\r\nHost: backend\r\n\r\n"
        modified: str = add_proxy_headers(original, "192.168.1.100")
        
        self.assertIn(
            "X-Forwarded-For: 192.168.1.100",
            modified,
            "Modified request should include X-Forwarded-For header. "
            "This tells the backend the original client IP."
        )
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_add_proxy_headers_chain(self) -> None:
        """Test X-Forwarded-For appending to existing chain."""
        try:
            from exercises.ex_8_02_reverse_proxy import add_proxy_headers
        except ImportError:
            self.skipTest("Exercise 2 not implemented yet")
        
        original: str = "GET / HTTP/1.1\r\nX-Forwarded-For: 10.0.0.1\r\n\r\n"
        modified: str = add_proxy_headers(original, "192.168.1.100")
        
        self.assertIn(
            "X-Forwarded-For: 10.0.0.1, 192.168.1.100",
            modified,
            "When X-Forwarded-For exists, APPEND to it, don't replace. "
            "This creates a chain showing all proxies."
        )



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class TestEnvironment(unittest.TestCase):
    """Tests for laboratory environment."""
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_docker_available(self) -> None:
        """Test Docker is accessible."""
        import subprocess
        
        try:
            result = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                timeout=10
            )
            self.assertEqual(
                result.returncode, 0,
                "Docker is not running. Start it with: sudo service docker start"
            )
        except FileNotFoundError:
            self.fail("Docker not installed. Install Docker first.")
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_compose_file_exists(self) -> None:
        """Test docker-compose.yml exists."""
        compose_file: Path = Path(__file__).parent.parent / "docker" / "docker-compose.yml"
        
        self.assertTrue(
            compose_file.exists(),
            f"docker-compose.yml not found at {compose_file}. "
            "Are you in the correct directory?"
        )
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_www_directory_exists(self) -> None:
        """Test www/ directory exists with content."""
        www_dir: Path = Path(__file__).parent.parent / "www"
        
        self.assertTrue(
            www_dir.exists(),
            "www/ directory not found. This is the document root for Exercise 1."
        )
        
        index_file: Path = www_dir / "index.html"
        self.assertTrue(
            index_file.exists(),
            "www/index.html not found. Create it for testing."
        )



# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
def run_exercise_tests(exercise_num: Optional[int] = None) -> int:
    """
    Run tests for specific exercise or all exercises.
    
    Args:
        exercise_num: 1 or 2 for specific exercise, None for all
        
    Returns:
        0 if all tests passed, 1 otherwise
    """
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    if exercise_num == 1:
        suite.addTests(loader.loadTestsFromTestCase(TestExercise1HTTPServer))
    elif exercise_num == 2:
        suite.addTests(loader.loadTestsFromTestCase(TestExercise2ReverseProxy))
    else:
        suite.addTests(loader.loadTestsFromTestCase(TestExercise1HTTPServer))
        suite.addTests(loader.loadTestsFromTestCase(TestExercise2ReverseProxy))
        suite.addTests(loader.loadTestsFromTestCase(TestEnvironment))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run Week 8 Exercise Tests")
    parser.add_argument(
        "--exercise",
        type=int,
        choices=[1, 2],
        help="Run tests for specific exercise (1 or 2)"
    )
    
    args = parser.parse_args()
    
    return run_exercise_tests(args.exercise)


if __name__ == "__main__":
    sys.exit(main())
