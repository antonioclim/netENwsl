#!/usr/bin/env python3
"""
Week 10 Laboratory Demonstrations
NETWORKING class - ASE, Informatics | by Revolvix

Automated demonstrations for projector/teaching use.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import sys
import time
import argparse
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.logger import setup_logger
from scripts.utils.network_utils import NetworkTester

logger = setup_logger("run_demo")



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def demo_http() -> bool:
    """Demonstrate HTTP service."""
    logger.info("=" * 50)
    logger.info("DEMO: HTTP Service")
    logger.info("=" * 50)
    
    tester = NetworkTester()
    
    # Fetch index page
    logger.info("\n1. Fetching index.html...")
    status, body = tester.http_get("http://localhost:8000/")
    if status == 200:
        logger.info(f"   Status: {status} OK")
        logger.info(f"   Body preview: {body[:100]}...")
    else:
        logger.error(f"   Failed with status: {status}")
        return False
    
    # Fetch text file
    logger.info("\n2. Fetching hello.txt...")
    status, body = tester.http_get("http://localhost:8000/hello.txt")
    if status == 200:
        logger.info(f"   Status: {status} OK")
        logger.info(f"   Content: {body[:80]}")
    else:
        logger.error(f"   Failed with status: {status}")
        return False
    
    logger.info("\n✓ HTTP demo completed successfully")
    return True



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def demo_dns() -> bool:
    """Demonstrate DNS service."""
    logger.info("=" * 50)
    logger.info("DEMO: DNS Service")
    logger.info("=" * 50)
    
    queries = [
        ("myservice.lab.local", "10.10.10.10"),
        ("api.lab.local", "10.10.10.20"),
        ("web.lab.local", "172.20.0.10"),
    ]
    
    success = True
    for name, expected in queries:
        logger.info(f"\n  Query: {name}")
        result = subprocess.run(
            ["dig", "@127.0.0.1", "-p", "5353", name, "+short"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0 and expected in result.stdout:
            logger.info(f"  Response: {result.stdout.strip()}")
        else:
            logger.warning(f"  Expected: {expected}, Got: {result.stdout.strip() or 'error'}")
            success = False
    
    if success:
        logger.info("\n✓ DNS demo completed successfully")
    return success



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def demo_ssh() -> bool:
    """Demonstrate SSH service."""
    logger.info("=" * 50)
    logger.info("DEMO: SSH Service")
    logger.info("=" * 50)
    
    try:
        import paramiko
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        logger.info("\n1. Connecting to SSH server...")
        client.connect(
            hostname="127.0.0.1",
            port=2222,
            username="labuser",
            password="labpass",
            timeout=10
        )
        logger.info("   Connected successfully")
        
        logger.info("\n2. Executing remote command...")
        stdin, stdout, stderr = client.exec_command("hostname && whoami")
        output = stdout.read().decode().strip()
        logger.info(f"   Output: {output}")
        
        client.close()
        logger.info("\n✓ SSH demo completed successfully")
        return True
        
    except ImportError:
        logger.error("Paramiko not installed. Run: pip install paramiko")
        return False
    except Exception as e:
        logger.error(f"SSH demo failed: {e}")
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def demo_ftp() -> bool:
    """Demonstrate FTP service."""
    logger.info("=" * 50)
    logger.info("DEMO: FTP Service")
    logger.info("=" * 50)
    
    try:
        from ftplib import FTP
        
        logger.info("\n1. Connecting to FTP server...")
        ftp = FTP()
        ftp.connect("127.0.0.1", 2121, timeout=10)
        ftp.login("labftp", "labftp")
        logger.info(f"   Banner: {ftp.getwelcome()}")
        
        logger.info("\n2. Listing directory...")
        files = ftp.nlst()
        for f in files:
            logger.info(f"   - {f}")
        
        ftp.quit()
        logger.info("\n✓ FTP demo completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"FTP demo failed: {e}")
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def demo_all() -> bool:
    """Run all demonstrations."""
    results = []
    
    results.append(("HTTP", demo_http()))
    time.sleep(1)
    
    results.append(("DNS", demo_dns()))
    time.sleep(1)
    
    results.append(("SSH", demo_ssh()))
    time.sleep(1)
    
    results.append(("FTP", demo_ftp()))
    
    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("DEMO SUMMARY")
    logger.info("=" * 50)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        logger.info(f"  {name}: {status}")
        if not passed:
            all_passed = False
    
    return all_passed



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    parser = argparse.ArgumentParser(description="Run Week 10 Demonstrations")
    parser.add_argument("--demo", type=int, choices=[1, 2, 3, 4],
                        help="Run specific demo (1=All, 2=HTTP/HTTPS, 3=DNS, 4=SSH/FTP)")
    args = parser.parse_args()
    
    logger.info("Week 10 Laboratory Demonstrations")
    logger.info("NETWORKING class - ASE, Informatics")
    logger.info("")
    
    if args.demo == 1 or args.demo is None:
        success = demo_all()
    elif args.demo == 2:
        success = demo_http()
    elif args.demo == 3:
        success = demo_dns()
    elif args.demo == 4:
        success = demo_ssh() and demo_ftp()
    else:
        success = demo_all()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
