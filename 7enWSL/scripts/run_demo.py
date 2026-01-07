#!/usr/bin/env python3
"""
Week 7 Demonstration Runner
NETWORKING class - ASE, Informatics | by Revolvix

Runs automated demonstrations for classroom presentation and verification.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.network_utils import NetworkUtils
from scripts.utils.logger import setup_logger

logger = setup_logger("demo")


class DemoRunner:
    """Runs demonstration scenarios for Week 7."""
    
    def __init__(self) -> None:
        self.docker = DockerManager(PROJECT_ROOT / "docker")
        self.network = NetworkUtils()
        self.artifacts_dir = PROJECT_ROOT / "artifacts"
        self.artifacts_dir.mkdir(exist_ok=True)
        self.src_dir = PROJECT_ROOT / "src"
    
    def run_python(self, script: str, args: list[str], timeout: int = 30) -> tuple[int, str, str]:
        """Run a Python script from src directory."""
        cmd = [sys.executable, str(self.src_dir / script)] + args
        logger.debug(f"Running: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=PROJECT_ROOT
        )
        return result.returncode, result.stdout, result.stderr
    
    def demo_baseline(self) -> bool:
        """
        Demonstrate baseline TCP and UDP connectivity.
        
        Returns:
            True if successful
        """
        logger.info("-" * 50)
        logger.info("Demo: Baseline Connectivity")
        logger.info("-" * 50)
        
        # Wait for services
        logger.info("Checking service availability...")
        if not self.network.wait_for_port("localhost", 9090, timeout=15):
            logger.error("TCP server not available")
            return False
        
        # TCP echo test
        logger.info("Testing TCP echo (localhost:9090)...")
        success, response = self.network.tcp_echo_test(
            "localhost", 9090, "baseline_test_message", timeout=5
        )
        
        if success:
            logger.info(f"  [OK] TCP echo response: {response}")
        else:
            logger.error(f"  [FAIL] TCP test failed: {response}")
            return False
        
        # UDP send test (can't easily verify receipt without modifying receiver)
        logger.info("Testing UDP send (localhost:9091)...")
        success, status = self.network.udp_send_test("localhost", 9091, "baseline_udp_test")
        
        if success:
            logger.info(f"  [OK] UDP datagram sent")
        else:
            logger.error(f"  [FAIL] UDP send failed: {status}")
            return False
        
        logger.info("")
        logger.info("[SUCCESS] Baseline connectivity verified")
        return True
    
    def demo_tcp_client(self) -> bool:
        """
        Demonstrate TCP client sending a message.
        
        Returns:
            True if successful
        """
        logger.info("-" * 50)
        logger.info("Demo: TCP Client")
        logger.info("-" * 50)
        
        rc, stdout, stderr = self.run_python(
            "apps/tcp_client.py",
            [
                "--host", "localhost",
                "--port", "9090",
                "--message", "hello_from_demo",
                "--timeout", "5",
                "--log", str(self.artifacts_dir / "demo_tcp_client.log")
            ]
        )
        
        if rc == 0:
            logger.info("[OK] TCP client completed successfully")
            if stdout.strip():
                for line in stdout.strip().split("\n")[-5:]:
                    logger.info(f"  {line}")
            return True
        else:
            logger.error(f"[FAIL] TCP client failed (rc={rc})")
            if stderr.strip():
                logger.error(f"  {stderr.strip()}")
            return False
    
    def demo_udp_sender(self) -> bool:
        """
        Demonstrate UDP sender sending datagrams.
        
        Returns:
            True if successful
        """
        logger.info("-" * 50)
        logger.info("Demo: UDP Sender")
        logger.info("-" * 50)
        
        rc, stdout, stderr = self.run_python(
            "apps/udp_sender.py",
            [
                "--host", "localhost",
                "--port", "9091",
                "--message", "hello_udp_from_demo",
                "--count", "3",
                "--log", str(self.artifacts_dir / "demo_udp_sender.log")
            ]
        )
        
        if rc == 0:
            logger.info("[OK] UDP sender completed successfully")
            return True
        else:
            logger.error(f"[FAIL] UDP sender failed (rc={rc})")
            return False
    
    def demo_port_probe(self) -> bool:
        """
        Demonstrate port probing functionality.
        
        Returns:
            True if successful
        """
        logger.info("-" * 50)
        logger.info("Demo: Port Probe")
        logger.info("-" * 50)
        
        rc, stdout, stderr = self.run_python(
            "apps/port_probe.py",
            [
                "--host", "localhost",
                "--ports", "22,80,443,8080,9090,9091",
                "--timeout", "1",
                "--log", str(self.artifacts_dir / "demo_port_probe.log")
            ]
        )
        
        if stdout.strip():
            for line in stdout.strip().split("\n"):
                logger.info(f"  {line}")
        
        return True  # Port probe doesn't really "fail"
    
    def demo_full(self) -> bool:
        """
        Run complete demonstration sequence.
        
        Returns:
            True if all demos pass
        """
        logger.info("=" * 60)
        logger.info("Week 7 Full Demonstration")
        logger.info("NETWORKING class - ASE, Informatics")
        logger.info("=" * 60)
        
        results = []
        
        # Baseline connectivity
        results.append(("Baseline", self.demo_baseline()))
        time.sleep(1)
        
        # TCP client
        results.append(("TCP Client", self.demo_tcp_client()))
        time.sleep(1)
        
        # UDP sender
        results.append(("UDP Sender", self.demo_udp_sender()))
        time.sleep(1)
        
        # Port probe
        results.append(("Port Probe", self.demo_port_probe()))
        
        # Summary
        logger.info("")
        logger.info("=" * 60)
        logger.info("Demonstration Summary")
        logger.info("=" * 60)
        
        all_passed = True
        for name, passed in results:
            status = "[PASS]" if passed else "[FAIL]"
            logger.info(f"  {status} {name}")
            if not passed:
                all_passed = False
        
        logger.info("")
        logger.info(f"Artifacts saved to: {self.artifacts_dir}")
        
        return all_passed


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Week 7 Demonstrations")
    parser.add_argument(
        "--demo",
        choices=["baseline", "tcp", "udp", "probe", "full", "reject_vs_drop"],
        default="full",
        help="Demo to run (default: full)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    args = parser.parse_args()

    runner = DemoRunner()
    
    try:
        if args.demo == "baseline":
            success = runner.demo_baseline()
        elif args.demo == "tcp":
            success = runner.demo_tcp_client()
        elif args.demo == "udp":
            success = runner.demo_udp_sender()
        elif args.demo == "probe":
            success = runner.demo_port_probe()
        elif args.demo == "reject_vs_drop":
            logger.info("REJECT vs DROP demonstration")
            logger.info("This demo requires manual firewall profile changes.")
            logger.info("See README.md Exercise 2 and Exercise 3 for instructions.")
            success = True
        else:  # full
            success = runner.demo_full()
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
