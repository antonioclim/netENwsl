#!/usr/bin/env python3
"""
Tests for Unique Student Context — Week 8 Laboratory
=====================================================

These tests verify that students are using their UNIQUE context values
rather than hardcoded defaults or copied solutions.

Usage:
    make test-context
    
    Or directly:
    python -m pytest tests/test_unique_context.py -v

Prerequisites:
    Student context must be generated first (make init ID=...)

Course: Computer Networks — ASE, CSIE
"""

import json
import unittest
from pathlib import Path
from typing import Any


CONTEXT_FILE = Path("artifacts/student_context.json")


def load_student_context() -> dict[str, Any]:
    """Load student context or skip tests if not available."""
    if not CONTEXT_FILE.exists():
        raise unittest.SkipTest(
            "Student context not found. Run: make init ID=your_student_id"
        )
    
    with open(CONTEXT_FILE, encoding='utf-8') as f:
        return json.load(f)


class TestUniqueContextGenerated(unittest.TestCase):
    """Test that student context was properly generated."""
    
    @classmethod
    def setUpClass(cls):
        cls.context = load_student_context()
    
    def test_context_has_student_id(self):
        """Student ID must be present in context."""
        self.assertIn("student_id", self.context)
        self.assertIsInstance(self.context["student_id"], str)
        self.assertGreater(len(self.context["student_id"]), 2)
    
    def test_context_has_session_token(self):
        """Session token must be present for verification."""
        self.assertIn("session_token", self.context)
        self.assertEqual(len(self.context["session_token"]), 12)
    
    def test_context_has_http_server_config(self):
        """HTTP server configuration must be present."""
        self.assertIn("http_server", self.context)
        hs = self.context["http_server"]
        
        self.assertIn("port", hs)
        self.assertIn("secret_header_name", hs)
        self.assertIn("secret_header_value", hs)
        self.assertIn("custom_status_code", hs)
    
    def test_context_has_load_balancer_config(self):
        """Load balancer configuration must be present."""
        self.assertIn("load_balancer", self.context)
        lb = self.context["load_balancer"]
        
        self.assertIn("weights", lb)
        self.assertEqual(len(lb["weights"]), 3)
        
        # Weights should not all be equal (ensured by generator)
        weights = list(lb["weights"].values())
        self.assertFalse(
            all(w == weights[0] for w in weights),
            "Weights should not all be equal"
        )
    
    def test_context_has_required_captures(self):
        """Required PCAP captures must be defined."""
        self.assertIn("required_captures", self.context)
        captures = self.context["required_captures"]
        
        required_names = ["handshake", "http_exchange", "load_balance"]
        for name in required_names:
            self.assertIn(name, captures, f"Missing required capture: {name}")


class TestUniquePortNotDefault(unittest.TestCase):
    """Test that unique port is not a common default."""
    
    @classmethod
    def setUpClass(cls):
        cls.context = load_student_context()
    
    def test_port_not_8080(self):
        """Port should not be the common default 8080."""
        port = self.context["http_server"]["port"]
        self.assertNotEqual(port, 8080, "Port should not be default 8080")
    
    def test_port_not_80(self):
        """Port should not be privileged port 80."""
        port = self.context["http_server"]["port"]
        self.assertNotEqual(port, 80, "Port should not be privileged port 80")
    
    def test_port_not_9000(self):
        """Port should not conflict with Portainer (9000)."""
        port = self.context["http_server"]["port"]
        self.assertNotEqual(port, 9000, "Port 9000 is reserved for Portainer")
    
    def test_port_in_valid_range(self):
        """Port should be in the unique range (9100-9999)."""
        port = self.context["http_server"]["port"]
        self.assertGreaterEqual(port, 9100)
        self.assertLessEqual(port, 9999)


class TestWeightsNotTrivial(unittest.TestCase):
    """Test that load balancer weights are non-trivial."""
    
    @classmethod
    def setUpClass(cls):
        cls.context = load_student_context()
    
    def test_weights_not_all_ones(self):
        """Weights should not all be 1 (trivial round-robin)."""
        weights = list(self.context["load_balancer"]["weights"].values())
        self.assertFalse(
            all(w == 1 for w in weights),
            "Weights should not all be 1"
        )
    
    def test_weights_not_all_equal(self):
        """Weights should not all be equal."""
        weights = list(self.context["load_balancer"]["weights"].values())
        self.assertFalse(
            len(set(weights)) == 1,
            "Weights should not all be equal"
        )
    
    def test_total_weight_reasonable(self):
        """Total weight should be in reasonable range."""
        weights = list(self.context["load_balancer"]["weights"].values())
        total = sum(weights)
        self.assertGreater(total, 3, "Total weight too low")
        self.assertLess(total, 31, "Total weight too high")


class TestSecretHeaderUnique(unittest.TestCase):
    """Test that secret header is unique."""
    
    @classmethod
    def setUpClass(cls):
        cls.context = load_student_context()
    
    def test_header_has_student_identifier(self):
        """Secret header should contain student-specific value."""
        header_value = self.context["http_server"]["secret_header_value"]
        
        # Should start with STU- prefix
        self.assertTrue(
            header_value.startswith("STU-"),
            "Header should start with STU- prefix"
        )
        
        # Should have 8 hex characters after prefix
        suffix = header_value[4:]
        self.assertEqual(len(suffix), 8, "Header suffix should be 8 characters")
    
    def test_header_name_correct(self):
        """Header name should be X-Student-Token."""
        header_name = self.context["http_server"]["secret_header_name"]
        self.assertEqual(header_name, "X-Student-Token")


class TestPcapPathsUnique(unittest.TestCase):
    """Test that PCAP paths contain student identifier."""
    
    @classmethod
    def setUpClass(cls):
        cls.context = load_student_context()
    
    def test_pcap_paths_contain_student_segment(self):
        """PCAP filenames should contain student-specific segment."""
        captures = self.context["required_captures"]
        
        for name, info in captures.items():
            filename = info["filename"]
            # Path should be in pcap/ directory
            self.assertTrue(
                filename.startswith("pcap/"),
                f"PCAP {name} should be in pcap/ directory"
            )
            # Filename should not be generic
            self.assertNotIn(
                "student",
                filename.lower(),
                f"PCAP {name} should have unique filename, not 'student'"
            )


class TestContextDeterminism(unittest.TestCase):
    """Test that context generation is deterministic."""
    
    @classmethod
    def setUpClass(cls):
        cls.context = load_student_context()
    
    def test_verification_data_present(self):
        """Verification data should be present for instructor use."""
        self.assertIn("_verification", self.context)
        verify = self.context["_verification"]
        
        self.assertIn("seed", verify)
        self.assertIn("regeneration_command", verify)
    
    def test_seed_is_integer(self):
        """Seed should be a valid integer."""
        seed = self.context["_verification"]["seed"]
        self.assertIsInstance(seed, int)
        self.assertGreater(seed, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
