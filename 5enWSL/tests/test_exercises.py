#!/usr/bin/env python3
"""
Exercise Verification Tests
NETWORKING class - ASE, Informatics | by Revolvix

Tests to verify exercise implementations are correct.
"""

import subprocess
import sys
import unittest
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestCIDRAnalysis(unittest.TestCase):
    """Test Exercise 5.01: CIDR Analysis."""
    
    def test_analyze_basic(self):
        """Test basic CIDR analysis."""
        from src.utils.net_utils import analyze_ipv4_interface
        
        info = analyze_ipv4_interface("192.168.10.14/26")
        
        self.assertEqual(str(info.address), "192.168.10.14")
        self.assertEqual(str(info.network.network_address), "192.168.10.0")
        self.assertEqual(info.network.prefixlen, 26)
        self.assertEqual(str(info.broadcast), "192.168.10.63")
        self.assertEqual(info.usable_hosts, 62)
    
    def test_analyze_prefix_24(self):
        """Test /24 network analysis."""
        from src.utils.net_utils import analyze_ipv4_interface
        
        info = analyze_ipv4_interface("10.0.0.100/24")
        
        self.assertEqual(str(info.network.network_address), "10.0.0.0")
        self.assertEqual(str(info.broadcast), "10.0.0.255")
        self.assertEqual(info.usable_hosts, 254)
        self.assertTrue(info.is_private)
    
    def test_network_address_type(self):
        """Test network address detection."""
        from src.utils.net_utils import analyze_ipv4_interface
        
        info = analyze_ipv4_interface("192.168.1.0/24")
        self.assertEqual(info.address_type, "network")
    
    def test_broadcast_address_type(self):
        """Test broadcast address detection."""
        from src.utils.net_utils import analyze_ipv4_interface
        
        info = analyze_ipv4_interface("192.168.1.255/24")
        self.assertEqual(info.address_type, "broadcast")


class TestFLSM(unittest.TestCase):
    """Test Exercise 5.01: FLSM Subnetting."""
    
    def test_flsm_split_4(self):
        """Test splitting into 4 subnets."""
        from src.utils.net_utils import flsm_split
        
        subnets = flsm_split("192.168.100.0/24", 4)
        
        self.assertEqual(len(subnets), 4)
        self.assertEqual(str(subnets[0]), "192.168.100.0/26")
        self.assertEqual(str(subnets[1]), "192.168.100.64/26")
        self.assertEqual(str(subnets[2]), "192.168.100.128/26")
        self.assertEqual(str(subnets[3]), "192.168.100.192/26")
    
    def test_flsm_split_8(self):
        """Test splitting into 8 subnets."""
        from src.utils.net_utils import flsm_split
        
        subnets = flsm_split("10.0.0.0/24", 8)
        
        self.assertEqual(len(subnets), 8)
        # Each subnet should be /27 (32 addresses)
        for subnet in subnets:
            self.assertEqual(subnet.prefixlen, 27)
    
    def test_flsm_invalid_count(self):
        """Test FLSM with non-power-of-2 count."""
        from src.utils.net_utils import flsm_split
        
        with self.assertRaises(ValueError):
            flsm_split("192.168.0.0/24", 3)


class TestVLSM(unittest.TestCase):
    """Test Exercise 5.02: VLSM Allocation."""
    
    def test_vlsm_basic(self):
        """Test basic VLSM allocation."""
        from src.utils.net_utils import vlsm_allocate
        
        allocations = vlsm_allocate("172.16.0.0/24", [60, 20, 10, 2])
        
        self.assertEqual(len(allocations), 4)
        
        # Verify each allocation has enough hosts
        for alloc in allocations:
            self.assertGreaterEqual(alloc.usable_hosts, alloc.required_hosts)
    
    def test_vlsm_efficiency(self):
        """Test VLSM allocates optimal prefix lengths."""
        from src.utils.net_utils import vlsm_allocate, prefix_for_hosts
        
        requirements = [60, 20, 10, 2]
        allocations = vlsm_allocate("172.16.0.0/24", requirements)
        
        # Check that prefixes are optimal
        for alloc in allocations:
            optimal_prefix = prefix_for_hosts(alloc.required_hosts)
            self.assertEqual(alloc.allocated_prefix, optimal_prefix)
    
    def test_vlsm_insufficient_space(self):
        """Test VLSM with insufficient address space."""
        from src.utils.net_utils import vlsm_allocate
        
        with self.assertRaises(ValueError):
            # Try to allocate way more than available
            vlsm_allocate("192.168.0.0/28", [100, 50])


class TestIPv6(unittest.TestCase):
    """Test Exercise 5.02: IPv6 Operations."""
    
    def test_ipv6_compress(self):
        """Test IPv6 compression."""
        from src.utils.net_utils import ipv6_compress
        
        compressed = ipv6_compress("2001:0db8:0000:0000:0000:0000:0000:0001")
        self.assertEqual(compressed, "2001:db8::1")
    
    def test_ipv6_expand(self):
        """Test IPv6 expansion."""
        from src.utils.net_utils import ipv6_expand
        
        expanded = ipv6_expand("2001:db8::1")
        self.assertEqual(expanded, "2001:0db8:0000:0000:0000:0000:0000:0001")
    
    def test_ipv6_info(self):
        """Test IPv6 info extraction."""
        from src.utils.net_utils import ipv6_info
        
        info = ipv6_info("2001:db8::1")
        
        self.assertEqual(info.compressed, "2001:db8::1")
        self.assertIn("global", info.address_type.lower())


class TestPrefixCalculations(unittest.TestCase):
    """Test prefix calculations."""
    
    def test_prefix_for_hosts(self):
        """Test calculating prefix for host count."""
        from src.utils.net_utils import prefix_for_hosts
        
        # 60 hosts needs /26 (62 usable)
        self.assertEqual(prefix_for_hosts(60), 26)
        
        # 20 hosts needs /27 (30 usable)
        self.assertEqual(prefix_for_hosts(20), 27)
        
        # 2 hosts needs /30 (2 usable)
        self.assertEqual(prefix_for_hosts(2), 30)
    
    def test_prefix_to_netmask(self):
        """Test prefix to netmask conversion."""
        from src.utils.net_utils import prefix_to_netmask
        
        self.assertEqual(prefix_to_netmask(24), "255.255.255.0")
        self.assertEqual(prefix_to_netmask(26), "255.255.255.192")
        self.assertEqual(prefix_to_netmask(30), "255.255.255.252")


def run_exercise_tests(exercise_num: int = None):
    """Run tests for specific exercise or all exercises."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    test_classes = {
        1: [TestCIDRAnalysis, TestFLSM],
        2: [TestFLSM],
        3: [TestVLSM],
        4: [TestIPv6],
    }
    
    if exercise_num:
        if exercise_num in test_classes:
            for test_class in test_classes[exercise_num]:
                suite.addTests(loader.loadTestsFromTestCase(test_class))
        else:
            print(f"Unknown exercise number: {exercise_num}")
            return 1
    else:
        # Run all tests
        suite.addTests(loader.loadTestsFromTestCase(TestCIDRAnalysis))
        suite.addTests(loader.loadTestsFromTestCase(TestFLSM))
        suite.addTests(loader.loadTestsFromTestCase(TestVLSM))
        suite.addTests(loader.loadTestsFromTestCase(TestIPv6))
        suite.addTests(loader.loadTestsFromTestCase(TestPrefixCalculations))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


def main():
    parser = argparse.ArgumentParser(
        description="Run exercise verification tests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_exercises.py               Run all tests
  python test_exercises.py --exercise 1  Run Exercise 1 tests only
  python test_exercises.py --exercise 3  Run Exercise 3 tests only
"""
    )
    parser.add_argument(
        "--exercise", "-e",
        type=int,
        choices=[1, 2, 3, 4],
        help="Run tests for specific exercise (1-4)"
    )
    args = parser.parse_args()
    
    return run_exercise_tests(args.exercise)


if __name__ == "__main__":
    sys.exit(main())
