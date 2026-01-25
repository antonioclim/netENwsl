#!/usr/bin/env python3
"""Automated Demonstration Script — Week 14.

NETWORKING class — ASE, CSIE | Computer Networks Laboratory
by ing. dr. Antonio Clim

Runs automated demonstrations of the laboratory environment.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.error import URLError
from urllib.request import Request, urlopen

PROJECT_ROOT = Path(__file__).parent.parent


def log(level: str, message: str) -> None:
    """Print timestamped log message."""
    ts = datetime.now().strftime("%H:%M:%S")
    colours = {"INFO": "\033[94m", "WARN": "\033[93m", "ERROR": "\033[91m", "OK": "\033[92m", "DEMO": "\033[96m"}
    print(f"[{ts}] {colours.get(level, '')}{level}\033[0m {message}")


def section_header(title: str) -> None:
    """Display a section header."""
    print(f"\n\033[96m{'=' * 60}\033[0m")
    print(f"\033[1m  {title}\033[0m")
    print(f"\033[96m{'=' * 60}\033[0m\n")


def http_get(url: str, timeout: int = 5) -> Optional[Dict[str, Any]]:
    """Send HTTP GET request and return response info."""
    try:
        req = Request(url, method="GET")
        start = time.time()
        with urlopen(req, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            latency = (time.time() - start) * 1000
            return {"status": response.status, "body": body[:500], "latency_ms": round(latency, 2)}
    except URLError as e:
        return {"error": str(e.reason)}
    except Exception as e:
        return {"error": str(e)}


def demo_round_robin(count: int = 6) -> List[str]:
    """
    Demonstrate round-robin load balancing.
    
    In my seminars, I've noticed students often expect random distribution
    instead of the deterministic alternating pattern.
    """
    section_header("Round-Robin Load Balancing Demo")
    log("DEMO", f"Sending {count} requests to load balancer...")
    backends = []

    for i in range(1, count + 1):
        result = http_get("http://localhost:8080/")
        if result and "error" not in result:
            body = result.get("body", "")
            backend = "app1" if "app1" in body.lower() else ("app2" if "app2" in body.lower() else "unknown")
            backends.append(backend)
            log("OK", f"Request {i}: → {backend} ({result.get('latency_ms', 0):.0f}ms)")
        else:
            log("ERROR", f"Request {i}: Failed - {result.get('error', 'unknown')}")
            backends.append("failed")
        time.sleep(0.3)

    print()
    log("INFO", "Distribution analysis:")
    dist = Counter(backends)
    for backend, cnt in dist.items():
        log("INFO", f"  {backend}: {cnt} requests ({(cnt / len(backends)) * 100:.0f}%)")
    return backends


def demo_failover() -> None:
    """Demonstrate load balancer failover behaviour."""
    section_header("Failover Demonstration")

    log("DEMO", "Checking initial state...")
    for i in range(3):
        http_get("http://localhost:8080/")
        time.sleep(0.2)

    log("DEMO", "Stopping app1...")
    subprocess.run(["docker", "stop", "week14_app1"], capture_output=True, timeout=30)
    time.sleep(2)

    log("DEMO", "Testing with app1 down...")
    for i in range(4):
        result = http_get("http://localhost:8080/")
        if result and "error" not in result:
            body = result.get("body", "")
            log("OK", f"Request {i+1}: → {'app2' if 'app2' in body.lower() else 'unknown'}")
        else:
            log("WARN", f"Request {i+1}: Failed (expected during failover)")
        time.sleep(0.3)

    log("DEMO", "Restarting app1...")
    subprocess.run(["docker", "start", "week14_app1"], capture_output=True, timeout=30)
    time.sleep(5)
    log("OK", "Failover demo complete")


def demo_traffic_generation(count: int = 20) -> None:
    """Generate traffic for Wireshark capture."""
    section_header("Traffic Generation")
    log("INFO", "Start Wireshark capture BEFORE continuing!")
    input("\n  Press Enter when ready to generate traffic...\n")

    log("DEMO", f"Generating {count} HTTP requests...")
    for i in range(1, count + 1):
        http_get("http://localhost:8080/")
        print(f"  [{i:2d}/{count}]", end="\r")
        time.sleep(0.1)

    print()
    log("OK", f"Generated {count} requests")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run Week 14 laboratory demonstrations",
        epilog="NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim",
    )
    parser.add_argument("--demo", choices=["full", "round-robin", "failover", "traffic"], default="full")
    parser.add_argument("--count", type=int, default=6)
    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("  Week 14 Laboratory Demonstration")
    print("  NETWORKING class — ASE, CSIE")
    print("=" * 60)

    demos = {
        "full": lambda: (demo_round_robin(args.count), demo_failover(), demo_traffic_generation(10)),
        "round-robin": lambda: demo_round_robin(args.count),
        "failover": demo_failover,
        "traffic": lambda: demo_traffic_generation(args.count),
    }

    try:
        demos.get(args.demo, demos["full"])()
        return 0
    except KeyboardInterrupt:
        log("WARN", "Demo interrupted")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
