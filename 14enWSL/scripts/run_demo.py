#!/usr/bin/env python3
"""
run_demo.py - Automated Demonstration Script
Week 14 - Integrated Recap
NETWORKING class - ASE, Informatics | by Revolvix

Runs automated demonstrations of the laboratory environment.

Usage:
    python scripts/run_demo.py --demo full       # Complete demonstration
    python scripts/run_demo.py --demo failover   # Failover demonstration
    python scripts/run_demo.py --demo traffic    # Traffic generation only
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import subprocess
import sys
import time
import json
import argparse
from pathlib import Path
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError


PROJECT_ROOT = Path(__file__).parent.parent
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"


# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY_UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════
class Colours:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def log(level: str, message: str) -> None:
    """Print timestamped log message."""
    ts = datetime.now().strftime("%H:%M:%S")
    colours = {
        "INFO": Colours.BLUE,
        "OK": Colours.GREEN,
        "WARN": Colours.YELLOW,
        "ERROR": Colours.RED,
        "DEMO": Colours.CYAN,
    }
    colour = colours.get(level, Colours.RESET)
    print(f"[{ts}] {colour}[{level}]{Colours.RESET} {message}")


# ═══════════════════════════════════════════════════════════════════════════════
# HTTP_UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════
def http_get(url: str, timeout: float = 5.0) -> dict:
    """Perform HTTP GET."""
    try:
        req = Request(url, method="GET")
        start = time.time()
        with urlopen(req, timeout=timeout) as response:
            latency = (time.time() - start) * 1000
            headers = dict(response.getheaders())
            body = response.read().decode("utf-8", errors="replace")
            return {
                "success": True,
                "status": response.status,
                "headers": headers,
                "body": body,
                "latency_ms": round(latency, 2),
                "x_backend": headers.get("X-Backend"),
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# COMMAND_UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════
def run_command(cmd: list, timeout: int = 30) -> tuple:
    """Run command."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=PROJECT_ROOT
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO_FULL
# ═══════════════════════════════════════════════════════════════════════════════
def demo_full() -> bool:
    """Run complete demonstration."""
    print()
    print("=" * 70)
    print(f"  {Colours.BOLD}Week 14: Complete Demonstration{Colours.RESET}")
    print("=" * 70)
    print()

    # Ensure artifacts directory exists
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    report = {
        "timestamp": datetime.now().isoformat(),
        "demo": "full",
        "stages": [],
    }

    # Stage 1: Service Health Check
    log("DEMO", "Stage 1: Service Health Check")
    log("INFO", "Checking all services...")

    services = [
        ("Load Balancer", "http://localhost:8080/lb-status"),
        ("Backend 1", "http://localhost:8001/health"),
        ("Backend 2", "http://localhost:8002/health"),
    ]

    all_healthy = True
    for name, url in services:
        result = http_get(url)
        if result["success"]:
            log("OK", f"{name}: healthy")
        else:
            log("ERROR", f"{name}: {result.get('error', 'unhealthy')}")
            all_healthy = False

    report["stages"].append({
        "name": "health_check",
        "passed": all_healthy,
    })

    if not all_healthy:
        log("ERROR", "Not all services are healthy. Aborting demo.")
        return False

    time.sleep(1)

    # Stage 2: Load Balancer Distribution Test
    log("DEMO", "Stage 2: Load Balancer Distribution Test")
    log("INFO", "Sending 20 requests to load balancer...")

    requests_log = []
    backend_counts = {}

    for i in range(20):
        result = http_get("http://localhost:8080/")
        if result["success"]:
            backend = result.get("x_backend", "unknown")
            backend_counts[backend] = backend_counts.get(backend, 0) + 1
            requests_log.append({
                "request": i + 1,
                "backend": backend,
                "status": result["status"],
                "latency_ms": result["latency_ms"],
            })
            print(f"  req={i+1:02d} status={result['status']} "
                  f"backend={backend} latency={result['latency_ms']:.1f}ms")
        else:
            requests_log.append({
                "request": i + 1,
                "error": result.get("error"),
            })
            print(f"  req={i+1:02d} ERROR: {result.get('error')}")
        time.sleep(0.1)

    log("INFO", f"Distribution: {backend_counts}")

    report["stages"].append({
        "name": "load_balancer_test",
        "requests": len(requests_log),
        "distribution": backend_counts,
        "passed": len(backend_counts) >= 2,
    })

    # Save HTTP log
    http_log_path = ARTIFACTS_DIR / "http_requests.json"
    with open(http_log_path, "w") as f:
        json.dump(requests_log, f, indent=2)
    log("OK", f"Request log saved: {http_log_path}")

    time.sleep(1)

    # Stage 3: TCP Echo Test
    log("DEMO", "Stage 3: TCP Echo Test")
    log("INFO", "Testing TCP echo server...")

    import socket
    echo_tests = []

    for msg in ["hello", "week14", "demo"]:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(("localhost", 9090))

            start = time.time()
            sock.sendall((msg + "\n").encode())
            response = sock.recv(4096).decode().strip()
            latency = (time.time() - start) * 1000
            sock.close()

            passed = msg in response
            echo_tests.append({
                "message": msg,
                "response": response,
                "latency_ms": round(latency, 2),
                "passed": passed,
            })

            status = "OK" if passed else "FAIL"
            log(status, f"Echo '{msg}': {latency:.1f}ms")

        except Exception as e:
            echo_tests.append({
                "message": msg,
                "error": str(e),
                "passed": False,
            })
            log("ERROR", f"Echo '{msg}': {e}")

    echo_passed = all(t["passed"] for t in echo_tests)
    report["stages"].append({
        "name": "tcp_echo_test",
        "tests": echo_tests,
        "passed": echo_passed,
    })

    time.sleep(1)

    # Stage 4: Generate Report
    log("DEMO", "Stage 4: Generating Reports")

    # Get final LB status
    result = http_get("http://localhost:8080/lb-status")
    if result["success"]:
        try:
            lb_status = json.loads(result["body"])
            report["lb_final_status"] = lb_status
        except json.JSONDecodeError:
            pass

    # Calculate overall result
    all_passed = all(stage.get("passed", False) for stage in report["stages"])
    report["overall_passed"] = all_passed

    # Save main report
    report_path = ARTIFACTS_DIR / "demo_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    log("OK", f"Report saved: {report_path}")

    # Generate validation summary
    validation_path = ARTIFACTS_DIR / "validation.txt"
    with open(validation_path, "w") as f:
        f.write(f"Week 14 Demo Validation\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write("=" * 40 + "\n\n")
        for stage in report["stages"]:
            status = "PASS" if stage.get("passed") else "FAIL"
            f.write(f"{stage['name']}: {status}\n")
        f.write("\n" + "=" * 40 + "\n")
        f.write(f"Overall: {'PASS' if all_passed else 'FAIL'}\n")
    log("OK", f"Validation saved: {validation_path}")

    # Summary
    print()
    print("=" * 70)
    if all_passed:
        print(f"  {Colours.GREEN}{Colours.BOLD}Demo completed successfully!{Colours.RESET}")
    else:
        print(f"  {Colours.YELLOW}{Colours.BOLD}Demo completed with warnings{Colours.RESET}")
    print("=" * 70)
    print()
    print("Artifacts generated:")
    print(f"  - {report_path}")
    print(f"  - {http_log_path}")
    print(f"  - {validation_path}")
    print()

    return all_passed


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO_FAILOVER
# ═══════════════════════════════════════════════════════════════════════════════
def demo_failover() -> bool:
    """Demonstrate failover behaviour."""
    print()
    print("=" * 70)
    print(f"  {Colours.BOLD}Week 14: Failover Demonstration{Colours.RESET}")
    print("=" * 70)
    print()

    log("DEMO", "Phase 1: Normal operation")
    log("INFO", "Sending requests with both backends up...")

    for i in range(5):
        result = http_get("http://localhost:8080/")
        if result["success"]:
            print(f"  req={i+1} backend={result.get('x_backend', 'unknown')}")
        time.sleep(0.2)

    log("DEMO", "Phase 2: Stopping backend 1")
    log("INFO", "Stopping week14_app1 container...")

    success, _, _ = run_command(["docker", "stop", "week14_app1"])
    if success:
        log("OK", "Backend 1 stopped")
    else:
        log("ERROR", "Failed to stop backend 1")
        return False

    time.sleep(2)

    log("DEMO", "Phase 3: Requests during failure")
    log("INFO", "Sending requests with one backend down...")

    for i in range(5):
        result = http_get("http://localhost:8080/")
        if result["success"]:
            print(f"  req={i+1} backend={result.get('x_backend', 'unknown')} status={result['status']}")
        else:
            print(f"  req={i+1} ERROR: {result.get('error')}")
        time.sleep(0.5)

    log("DEMO", "Phase 4: Restoring backend 1")
    log("INFO", "Starting week14_app1 container...")

    success, _, _ = run_command(["docker", "start", "week14_app1"])
    if success:
        log("OK", "Backend 1 started")
    else:
        log("ERROR", "Failed to start backend 1")

    log("INFO", "Waiting for health check...")
    time.sleep(10)

    log("DEMO", "Phase 5: Recovered operation")
    log("INFO", "Sending requests after recovery...")

    for i in range(5):
        result = http_get("http://localhost:8080/")
        if result["success"]:
            print(f"  req={i+1} backend={result.get('x_backend', 'unknown')}")
        time.sleep(0.2)

    print()
    print("=" * 70)
    print(f"  {Colours.GREEN}Failover demonstration complete{Colours.RESET}")
    print("=" * 70)
    print()

    return True


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO_TRAFFIC
# ═══════════════════════════════════════════════════════════════════════════════
def demo_traffic() -> bool:
    """Generate traffic only."""
    print()
    print("=" * 70)
    print(f"  {Colours.BOLD}Week 14: Traffic Generation{Colours.RESET}")
    print("=" * 70)
    print()

    log("INFO", "Generating 50 HTTP requests...")

    for i in range(50):
        result = http_get("http://localhost:8080/")
        if result["success"]:
            print(f"  req={i+1:02d} backend={result.get('x_backend', 'unknown')} "
                  f"latency={result['latency_ms']:.1f}ms")
        else:
            print(f"  req={i+1:02d} ERROR")
        time.sleep(0.1)

    print()
    log("OK", "Traffic generation complete")

    return True


# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGUMENTS
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run Week 14 demonstrations"
    )
    parser.add_argument(
        "--demo", "-d",
        choices=["full", "failover", "traffic"],
        default="full",
        help="Demo type to run (default: full)"
    )
    return parser.parse_args()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    args = parse_args()

    demos = {
        "full": demo_full,
        "failover": demo_failover,
        "traffic": demo_traffic,
    }

    success = demos[args.demo]()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
