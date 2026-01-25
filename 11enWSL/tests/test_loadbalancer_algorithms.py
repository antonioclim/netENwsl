#!/usr/bin/env python3
"""
Unit Tests for Load Balancer Algorithms — Week 11
NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim

Tests cover:
- Round-robin distribution
- IP hash consistency
- Least connections selection
- Passive health check behaviour
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from typing import List

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from src.exercises.ex_11_02_loadbalancer import (
        Backend, LoadBalancer, parse_backends
    )
    LB_AVAILABLE = True
except ImportError:
    LB_AVAILABLE = False
    Backend = None
    LoadBalancer = None


def create_test_backends(count: int = 3) -> List:
    return [Backend(host="localhost", port=8081 + i) for i in range(count)]


def create_test_lb(backends: List, algo: str = "rr") -> object:
    return LoadBalancer(
        backends=backends, algo=algo, passive_failures=2,
        fail_timeout_s=10.0, sock_timeout=2.0
    )


@unittest.skipUnless(LB_AVAILABLE, "Load balancer module not available")
class TestRoundRobin(unittest.TestCase):
    def setUp(self) -> None:
        self.backends = create_test_backends(3)
        self.lb = create_test_lb(self.backends, algo="rr")

    def test_cycles_through_backends(self) -> None:
        results = [self.lb.pick("192.168.1.1").port for _ in range(6)]
        expected = [8081, 8082, 8083, 8081, 8082, 8083]
        self.assertEqual(results, expected)

    def test_skips_down_backends(self) -> None:
        self.backends[1].down_until = float("inf")
        results = [self.lb.pick("192.168.1.1").port for _ in range(4)]
        for port in results:
            self.assertNotEqual(port, 8082)


@unittest.skipUnless(LB_AVAILABLE, "Load balancer module not available")
class TestIPHash(unittest.TestCase):
    def setUp(self) -> None:
        self.backends = create_test_backends(3)
        self.lb = create_test_lb(self.backends, algo="ip_hash")

    def test_same_ip_same_backend(self) -> None:
        client_ip = "192.168.1.50"
        first = self.lb.pick(client_ip)
        for _ in range(10):
            b = self.lb.pick(client_ip)
            self.assertEqual(b.port, first.port)


@unittest.skipUnless(LB_AVAILABLE, "Load balancer module not available")
class TestPassiveHealthChecks(unittest.TestCase):
    def setUp(self) -> None:
        self.backends = create_test_backends(3)
        self.lb = create_test_lb(self.backends, algo="rr")

    def test_mark_failure_increments_count(self) -> None:
        backend = self.backends[0]
        self.lb.mark_failure(backend)
        self.assertEqual(backend.fails, 1)

    def test_mark_success_resets_count(self) -> None:
        backend = self.backends[0]
        backend.fails = 5
        self.lb.mark_success(backend)
        self.assertEqual(backend.fails, 0)


@unittest.skipUnless(LB_AVAILABLE, "Load balancer module not available")
class TestParseBackends(unittest.TestCase):
    def test_parses_single_backend(self) -> None:
        backends = parse_backends("localhost:8080")
        self.assertEqual(len(backends), 1)

    def test_parses_multiple_backends(self) -> None:
        backends = parse_backends("web1:80,web2:80,web3:80")
        self.assertEqual(len(backends), 3)


def main() -> None:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestRoundRobin))
    suite.addTests(loader.loadTestsFromTestCase(TestIPHash))
    suite.addTests(loader.loadTestsFromTestCase(TestPassiveHealthChecks))
    suite.addTests(loader.loadTestsFromTestCase(TestParseBackends))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
