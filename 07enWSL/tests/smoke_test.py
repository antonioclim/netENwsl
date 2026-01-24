#!/usr/bin/env python3
"""
Smoke Test for Week 7 Laboratory
NETWORKING class - ASE, Informatics | by Revolvix

Quick functionality check that completes in under 60 seconds.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations
from typing import Optional, List, Dict, Tuple, Any

import socket
import subprocess
import sys
import time
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def smoke_test() -> int:
    """Run a quick smoke test of the laboratory environment."""
    print("=" * 60)
    print("Week 7 Smoke Test")
    print("NETWORKING class - ASE, Informatics")
    print("=" * 60)
    print()
    
    start_time = time.time()
    failures = []
    
    # Test 1: Docker compose file exists
    print("[1/5] Checking docker-compose.yml...")
    compose_file = PROJECT_ROOT / "docker" / "docker-compose.yml"
    if compose_file.exists():
        print("  [OK] docker-compose.yml found")
    else:
        print("  [FAIL] docker-compose.yml not found")
        failures.append("docker-compose.yml missing")
    
    # Test 2: Check Docker is running
    print("[2/5] Checking Docker daemon...")
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        if result.returncode == 0:
            print("  [OK] Docker daemon running")
        else:
            print("  [FAIL] Docker daemon not responding")
            failures.append("Docker not running")
    except Exception as e:
        print(f"  [FAIL] Docker check failed: {e}")
        failures.append("Docker check failed")
    
    # Test 3: Check TCP server connectivity
    print("[3/5] Checking TCP server (localhost:9090)...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(("localhost", 9090))
        sock.close()
        
        if result == 0:
            print("  [OK] TCP server is responding")
        else:
            print(f"  [WARN] TCP server not available (errno {result})")
            print("         Run: python scripts/start_lab.py")
    except Exception as e:
        print(f"  [WARN] TCP check failed: {e}")
    
    # Test 4: Check source files
    print("[4/5] Checking source files...")
    required_apps = [
        "tcp_server.py",
        "tcp_client.py",
        "udp_sender.py",
        "udp_receiver.py",
        "port_probe.py",
    ]
    
    apps_dir = PROJECT_ROOT / "src" / "apps"
    missing = []
    for app in required_apps:
        if not (apps_dir / app).exists():
            missing.append(app)
    
    if not missing:
        print(f"  [OK] All {len(required_apps)} application files found")
    else:
        print(f"  [FAIL] Missing files: {', '.join(missing)}")
        failures.append("Missing source files")
    
    # Test 5: Check artifact directories
    print("[5/5] Checking directories...")
    required_dirs = ["artifacts", "pcap"]
    for d in required_dirs:
        dir_path = PROJECT_ROOT / d
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  [OK] Created {d}/")
        else:
            print(f"  [OK] {d}/ exists")
    
    # Summary
    elapsed = time.time() - start_time
    print()
    print("=" * 60)
    print(f"Smoke test completed in {elapsed:.1f} seconds")
    print("=" * 60)
    
    if failures:
        print(f"FAILURES ({len(failures)}):")
        for f in failures:
            print(f"  - {f}")
        return 1
    else:
        print("All checks passed")
        return 0


if __name__ == "__main__":
    sys.exit(smoke_test())
