#!/usr/bin/env python3
"""
Smoke Test
NETWORKING class - ASE, Informatics | by Revolvix

Quick functionality check that runs in under 60 seconds.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))



# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
def test_import_net_utils() -> bool:
    """Test that net_utils can be imported."""
    print("Testing net_utils import...")
    try:
        from src.utils.net_utils import (
            analyze_ipv4_interface,
            flsm_split,
            vlsm_allocate,
            ipv6_compress,
        )
        print("  ✓ net_utils imported successfully")
        return True
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_cidr_analysis() -> bool:
    """Test basic CIDR analysis."""
    print("Testing CIDR analysis...")
    try:
        from src.utils.net_utils import analyze_ipv4_interface
        
        info = analyze_ipv4_interface("192.168.10.14/26")
        
        assert str(info.network.network_address) == "192.168.10.0"
        assert info.usable_hosts == 62
        
        print("  ✓ CIDR analysis working correctly")
        return True
    except Exception as e:
        print(f"  ✗ CIDR analysis failed: {e}")
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_flsm() -> bool:
    """Test FLSM subnetting."""
    print("Testing FLSM subnetting...")
    try:
        from src.utils.net_utils import flsm_split
        
        subnets = flsm_split("10.0.0.0/24", 4)
        
        assert len(subnets) == 4
        assert subnets[0].prefixlen == 26
        
        print("  ✓ FLSM subnetting working correctly")
        return True
    except Exception as e:
        print(f"  ✗ FLSM failed: {e}")
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_vlsm() -> bool:
    """Test VLSM allocation."""
    print("Testing VLSM allocation...")
    try:
        from src.utils.net_utils import vlsm_allocate
        
        allocations = vlsm_allocate("172.16.0.0/24", [60, 20, 10, 2])
        
        assert len(allocations) == 4
        for alloc in allocations:
            assert alloc.usable_hosts >= alloc.required_hosts
        
        print("  ✓ VLSM allocation working correctly")
        return True
    except Exception as e:
        print(f"  ✗ VLSM failed: {e}")
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_ipv6() -> bool:
    """Test IPv6 operations."""
    print("Testing IPv6 operations...")
    try:
        from src.utils.net_utils import ipv6_compress, ipv6_expand
        
        compressed = ipv6_compress("2001:0db8:0000:0000:0000:0000:0000:0001")
        assert compressed == "2001:db8::1"
        
        expanded = ipv6_expand("2001:db8::1")
        assert "0000" in expanded
        
        print("  ✓ IPv6 operations working correctly")
        return True
    except Exception as e:
        print(f"  ✗ IPv6 operations failed: {e}")
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_exercise_cli() -> bool:
    """Test exercise CLI is executable."""
    print("Testing exercise CLI...")
    try:
        exercise_path = PROJECT_ROOT / "src" / "exercises" / "ex_5_01_cidr_flsm.py"
        
        result = subprocess.run(
            [sys.executable, str(exercise_path), "analyse", "10.0.0.1/24", "--json"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0 and '"network":' in result.stdout:
            print("  ✓ Exercise CLI working correctly")
            return True
        else:
            print(f"  ✗ CLI returned unexpected output")
            return False
    except Exception as e:
        print(f"  ✗ CLI test failed: {e}")
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    print("=" * 50)
    print("Week 5 WSL Kit - Smoke Test")
    print("NETWORKING class - ASE, Informatics")
    print("=" * 50)
    print()
    
    start_time = time.time()
    
    tests = [
        test_import_net_utils,
        test_cidr_analysis,
        test_flsm,
        test_vlsm,
        test_ipv6,
        test_exercise_cli,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
    
    elapsed = time.time() - start_time
    
    print()
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print(f"Time: {elapsed:.2f} seconds")
    
    if failed == 0:
        print("All smoke tests passed!")
        return 0
    else:
        print("Some tests failed. Check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
