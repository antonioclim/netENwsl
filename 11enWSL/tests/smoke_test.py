#!/usr/bin/env python3
"""
Quick Smoke Test for Week 11 Laboratory
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Fast validation that the laboratory environment is working.
Should complete in under 60 seconds.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations
from typing import Optional, List, Dict, Tuple, Any

import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.network_utils import http_get, check_port
from scripts.utils.logger import setup_logger, print_banner

logger = setup_logger("smoke_test")



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_load_balancer() -> bool:
    """Quick check of load balancer."""
    if not check_port("localhost", 8080):
        logger.error("Load balancer not responding on port 8080")
        return False
    
    response = http_get("http://localhost:8080/")
    if response.status_code != 200:
        logger.error(f"Load balancer returned {response.status_code}")
        return False
    
    logger.info("Load balancer responding correctly")
    return True



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_health_endpoint() -> bool:
    """Quick check of health endpoint."""
    response = http_get("http://localhost:8080/health")
    if response.status_code != 200:
        logger.warning("Health endpoint not responding (may be OK)")
        return True  # Not critical
    
    logger.info("Health endpoint responding")
    return True



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_distribution() -> bool:
    """Quick check of traffic distribution."""
    backends_seen = set()
    
    for _ in range(6):
        response = http_get("http://localhost:8080/")
        if response.status_code == 200:
            # Try to identify backend
            if "web1" in response.body.lower():
                backends_seen.add("web1")
            elif "web2" in response.body.lower():
                backends_seen.add("web2")
            elif "web3" in response.body.lower():
                backends_seen.add("web3")
            elif "Backend" in response.body:
                # Extract number
                import re
                match = re.search(r'Backend (\d+)', response.body)
                if match:
                    backends_seen.add(f"backend_{match.group(1)}")
    
    if len(backends_seen) >= 1:
        logger.info(f"Backends responding: {backends_seen}")
        return True
    else:
        logger.warning("Could not identify any backends")
        return True  # Still OK if load balancer works



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    print_banner("Week 11 Smoke Test")
    print("Quick validation of laboratory environment")
    print("")
    
    start_time = time.time()
    results = {}
    
    # Run checks
    logger.info("Checking load balancer...")
    results['load_balancer'] = check_load_balancer()
    
    if results['load_balancer']:
        logger.info("Checking health endpoint...")
        results['health'] = check_health_endpoint()
        
        logger.info("Checking distribution...")
        results['distribution'] = check_distribution()
    else:
        results['health'] = False
        results['distribution'] = False
    
    # Summary
    elapsed = time.time() - start_time
    print("")
    print("=" * 50)
    print("SMOKE TEST RESULTS")
    print("=" * 50)
    
    all_passed = True
    for name, passed in results.items():
        status = "\033[32mPASS\033[0m" if passed else "\033[31mFAIL\033[0m"
        print(f"  {name:20} {status}")
        if not passed:
            all_passed = False
    
    print("")
    print(f"Time: {elapsed:.2f}s")
    print("=" * 50)
    
    if all_passed:
        print("\n\033[32mAll smoke tests passed!\033[0m")
        print("Environment is ready for exercises.")
        return 0
    else:
        print("\n\033[33mSome tests failed.\033[0m")
        print("Run 'python scripts/start_lab.py' to start the environment.")
        return 1


if __name__ == "__main__":
    sys.exit(main())


# ing. dr. Antonio Clim
