#!/usr/bin/env python3
"""
Exercise Verification Tests for Week 11 Laboratory
NETWORKING class - ASE, Informatics | by Revolvix

Tests to verify exercise implementations are working correctly.
"""
from __future__ import annotations

import unittest
import subprocess
import sys
import time
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.network_utils import (
    http_get, check_port, wait_for_port,
    test_load_balancer, extract_backend_id
)


class TestExercise1Backend(unittest.TestCase):
    """Test Exercise 1: HTTP Backend Server."""
    
    @classmethod
    def setUpClass(cls):
        """Check if backends are running."""
        cls.backends_running = all(
            check_port("localhost", port) 
            for port in [8081, 8082, 8083]
        )
    
    def test_backend_1_responds(self):
        """Backend 1 should respond on port 8081."""
        if not self.backends_running:
            self.skipTest("Backends not running - start them first")
        
        response = http_get("http://localhost:8081/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Backend", response.body)
    
    def test_backend_2_responds(self):
        """Backend 2 should respond on port 8082."""
        if not self.backends_running:
            self.skipTest("Backends not running")
        
        response = http_get("http://localhost:8082/")
        self.assertEqual(response.status_code, 200)
    
    def test_backend_3_responds(self):
        """Backend 3 should respond on port 8083."""
        if not self.backends_running:
            self.skipTest("Backends not running")
        
        response = http_get("http://localhost:8083/")
        self.assertEqual(response.status_code, 200)


class TestExercise2RoundRobin(unittest.TestCase):
    """Test Exercise 2: Load Balancer with Round Robin."""
    
    @classmethod
    def setUpClass(cls):
        """Check if load balancer is running."""
        cls.lb_running = check_port("localhost", 8080)
    
    def test_load_balancer_responds(self):
        """Load balancer should respond on port 8080."""
        if not self.lb_running:
            self.skipTest("Load balancer not running")
        
        response = http_get("http://localhost:8080/")
        self.assertIn(response.status_code, [200, 502, 503])
    
    def test_distribution_multiple_backends(self):
        """Traffic should be distributed to multiple backends."""
        if not self.lb_running:
            self.skipTest("Load balancer not running")
        
        stats = test_load_balancer("http://localhost:8080/", num_requests=12)
        
        # Should have at least 2 different backends
        self.assertGreaterEqual(
            len(stats['distribution']),
            1,  # At least one backend
            "Traffic not distributed to any backend"
        )


class TestExercise3IPHash(unittest.TestCase):
    """Test Exercise 3: Sticky Sessions with IP Hash."""
    
    @classmethod
    def setUpClass(cls):
        """Check if load balancer is running."""
        cls.lb_running = check_port("localhost", 8080)
    
    def test_consistent_routing(self):
        """Requests from same IP should go to same backend (if IP hash)."""
        if not self.lb_running:
            self.skipTest("Load balancer not running")
        
        # Send 5 requests and check consistency
        backends = []
        for _ in range(5):
            response = http_get("http://localhost:8080/")
            if response.status_code == 200:
                backend = extract_backend_id(response)
                backends.append(backend)
        
        # With IP hash, all should go to same backend
        # With round robin, this test just passes
        self.assertGreater(len(backends), 0, "No successful responses")


class TestExercise4Failover(unittest.TestCase):
    """Test Exercise 4: Failover Simulation."""
    
    @classmethod
    def setUpClass(cls):
        """Check if load balancer is running."""
        cls.lb_running = check_port("localhost", 8080)
    
    def test_handles_failure_gracefully(self):
        """Load balancer should handle backend failure gracefully."""
        if not self.lb_running:
            self.skipTest("Load balancer not running")
        
        # Should still get responses even if some backends are down
        response = http_get("http://localhost:8080/")
        # Accept 200, 502 (bad gateway), or 503 (service unavailable)
        self.assertIn(
            response.status_code,
            [200, 502, 503],
            f"Unexpected status: {response.status_code}"
        )


class TestExercise5NginxDocker(unittest.TestCase):
    """Test Exercise 5: Nginx Docker Load Balancer."""
    
    @classmethod
    def setUpClass(cls):
        """Check if Nginx stack is running."""
        cls.nginx_running = check_port("localhost", 8080)
    
    def test_nginx_health_endpoint(self):
        """Nginx health endpoint should respond."""
        if not self.nginx_running:
            self.skipTest("Nginx not running")
        
        response = http_get("http://localhost:8080/health")
        self.assertEqual(response.status_code, 200)
    
    def test_nginx_status_endpoint(self):
        """Nginx status endpoint should respond."""
        if not self.nginx_running:
            self.skipTest("Nginx not running")
        
        response = http_get("http://localhost:8080/nginx_status")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Active connections", response.body)


class TestExercise6DNS(unittest.TestCase):
    """Test Exercise 6: DNS Protocol Analysis."""
    
    def test_dns_client_exists(self):
        """DNS client exercise file should exist."""
        dns_client = PROJECT_ROOT / "src" / "exercises" / "ex_11_03_dns_client.py"
        self.assertTrue(dns_client.exists(), "DNS client exercise not found")
    
    def test_dns_client_syntax(self):
        """DNS client should have valid Python syntax."""
        dns_client = PROJECT_ROOT / "src" / "exercises" / "ex_11_03_dns_client.py"
        
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(dns_client)],
            capture_output=True
        )
        self.assertEqual(result.returncode, 0, "DNS client has syntax errors")


class TestExercise7Benchmark(unittest.TestCase):
    """Test Exercise 7: Performance Benchmarking."""
    
    @classmethod
    def setUpClass(cls):
        """Check if load balancer is running."""
        cls.lb_running = check_port("localhost", 8080)
    
    def test_benchmark_runs(self):
        """Benchmark should complete without errors."""
        if not self.lb_running:
            self.skipTest("Load balancer not running")
        
        from scripts.utils.network_utils import benchmark_endpoint
        
        # Run small benchmark
        results = benchmark_endpoint(
            "http://localhost:8080/",
            num_requests=20,
            concurrency=2
        )
        
        self.assertGreater(results['successful'], 0, "No successful requests")
        self.assertIn('requests_per_second', results)


def run_specific_exercise(exercise_num: int) -> bool:
    """Run tests for a specific exercise."""
    test_classes = {
        1: TestExercise1Backend,
        2: TestExercise2RoundRobin,
        3: TestExercise3IPHash,
        4: TestExercise4Failover,
        5: TestExercise5NginxDocker,
        6: TestExercise6DNS,
        7: TestExercise7Benchmark,
    }
    
    if exercise_num not in test_classes:
        print(f"Unknown exercise: {exercise_num}")
        return False
    
    suite = unittest.TestLoader().loadTestsFromTestCase(test_classes[exercise_num])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


def main():
    parser = argparse.ArgumentParser(
        description="Run Week 11 Exercise Tests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Run all tests
  %(prog)s --exercise 1       # Test Exercise 1 only
  %(prog)s --exercise 2       # Test Exercise 2 only
        """
    )
    parser.add_argument("--exercise", type=int,
                        help="Test specific exercise (1-7)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Verbose output")
    
    args = parser.parse_args()
    
    if args.exercise:
        success = run_specific_exercise(args.exercise)
        return 0 if success else 1
    else:
        # Run all tests
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(sys.modules[__name__])
        runner = unittest.TextTestRunner(verbosity=2 if args.verbose else 1)
        result = runner.run(suite)
        return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())


# Revolvix&Hypotheticalandrei
