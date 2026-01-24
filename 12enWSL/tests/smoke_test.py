#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_DOCSTRING
# ═══════════════════════════════════════════════════════════════════════════════
"""
Smoke Test
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Quick functionality check to verify basic laboratory operation.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import sys
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.network_utils import check_port
from scripts.utils.logger import setup_colour_logger

logger = setup_colour_logger("smoke_test")



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Run smoke tests."""
    logger.info("Week 12 Smoke Test")
    logger.info("=" * 40)
    
    results = []
    
    # Check required services
    services = [
        ("SMTP", 1025),
        ("JSON-RPC", 6200),
        ("XML-RPC", 6201),
        ("gRPC", 6251),
    ]
    
    for name, port in services:
        if check_port("127.0.0.1", port):
            logger.info(f"  ✓ {name} (port {port})")
            results.append(True)
        else:
            logger.error(f"  ✗ {name} (port {port}) - not responding")
            results.append(False)
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    logger.info("=" * 40)
    logger.info(f"Result: {passed}/{total} services responding")
    
    if all(results):
        logger.info("✓ All smoke tests passed")
        return 0
    else:
        logger.error("✗ Some smoke tests failed")
        return 1



# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    sys.exit(main())
