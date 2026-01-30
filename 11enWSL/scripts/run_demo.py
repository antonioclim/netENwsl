#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
  Automated Demonstration Script for Week 11 Laboratory
═══════════════════════════════════════════════════════════════════════════════

NETWORKING class - ASE, Informatics | by Revolvix
This script runs automated demonstrations of load balancing and failover.
═══════════════════════════════════════════════════════════════════════════════
"""
from __future__ import annotations


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════

import subprocess
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger, print_banner, print_section
from scripts.utils.network_utils import (
    http_get, probe_load_balancer, benchmark_endpoint,
    print_distribution, print_benchmark_results, wait_for_port
)

logger = setup_logger("run_demo")


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO_LOAD_BALANCING
# ═══════════════════════════════════════════════════════════════════════════════

def demo_load_balancing(url: str = "http://localhost:8080/") -> bool:
    """
    Demo 1: Load Balancing Distribution
    
    Shows how traffic is distributed across backends.
    """
    print_section("Demo 1: Load Balancing Distribution")
    
    logger.info(f"Sending 12 requests to {url}")
    logger.info("Observing round-robin distribution...")
    print("")
    
    stats = probe_load_balancer(url, num_requests=12, concurrency=1)
    
    if stats['successful'] < 10:
        logger.error(f"Too many failures: {stats['failed']}/{stats['total_requests']}")
        return False
    
    print_distribution(stats['distribution'], stats['successful'])
    
    # Verify distribution is reasonably balanced
    distribution = stats['distribution']
    if len(distribution) >= 2:
        counts = list(distribution.values())
        if max(counts) - min(counts) <= 2:
            logger.info("✓ Traffic is evenly distributed (round-robin working)")
        else:
            logger.info("Traffic distribution appears weighted or using IP hash")
    else:
        logger.warning("Traffic going to single backend (check configuration)")
    
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO_HEADERS_INSPECTION
# ═══════════════════════════════════════════════════════════════════════════════

def demo_headers_inspection(url: str = "http://localhost:8080/") -> bool:
    """
    Demo: Inspect HTTP headers from load balancer
    """
    print_section("Header Inspection")
    
    logger.info("Checking response headers...")
    
    response = http_get(url)
    
    if response.status_code != 200:
        logger.error(f"Request failed with status {response.status_code}")
        return False
    
    print("\nResponse Headers:")
    print("-" * 40)
    for key, value in response.headers.items():
        if key.lower().startswith('x-'):
            print(f"  {key}: {value}")
    print("-" * 40)
    
    print(f"\nResponse Body:\n  {response.body.strip()}")
    print(f"\nLatency: {response.latency_ms:.2f}ms")
    
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO_FAILOVER
# ═══════════════════════════════════════════════════════════════════════════════

def demo_failover(docker: DockerManager, 
                  url: str = "http://localhost:8080/") -> bool:
    """
    Demo 2: Failover Simulation
    
    Demonstrates automatic failover when a backend fails.
    """
    print_section("Demo 2: Failover Simulation")
    
    logger.info("Phase 1: Baseline distribution")
    baseline = probe_load_balancer(url, num_requests=6, concurrency=1)
    print_distribution(baseline['distribution'], baseline['successful'])
    
    logger.info("\nPhase 2: Stopping Backend 2...")
    
    # Stop backend 2
    try:
        subprocess.run(
            ["docker", "stop", "s11_backend_2"],
            capture_output=True,
            check=True
        )
        logger.info("Backend 2 stopped")
    except Exception as e:
        logger.warning(f"Could not stop backend: {e}")
        return False
    
    time.sleep(2)  # Allow health check to detect failure
    
    logger.info("\nPhase 3: Distribution with Backend 2 down")
    failover = probe_load_balancer(url, num_requests=6, concurrency=1)
    print_distribution(failover['distribution'], failover['successful'])
    
    # Verify backend 2 is not receiving traffic
    if 'web2' in failover['distribution'] or 'backend_2' in failover['distribution']:
        logger.warning("Backend 2 still receiving traffic (health check may be slow)")
    else:
        logger.info("✓ Traffic successfully rerouted away from failed backend")
    
    logger.info("\nPhase 4: Recovering Backend 2...")
    
    # Start backend 2
    try:
        subprocess.run(
            ["docker", "start", "s11_backend_2"],
            capture_output=True,
            check=True
        )
        logger.info("Backend 2 started")
    except Exception as e:
        logger.warning(f"Could not start backend: {e}")
    
    time.sleep(3)  # Allow recovery
    
    logger.info("\nPhase 5: Distribution after recovery")
    recovery = probe_load_balancer(url, num_requests=6, concurrency=1)
    print_distribution(recovery['distribution'], recovery['successful'])
    
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO_BENCHMARK
# ═══════════════════════════════════════════════════════════════════════════════

def demo_benchmark(url: str = "http://localhost:8080/") -> bool:
    """
    Demo: Performance Benchmark
    """
    print_section("Performance Benchmark")
    
    logger.info(f"Benchmarking {url}")
    logger.info("Sending 200 requests with 10 concurrent workers...")
    print("")
    
    results = benchmark_endpoint(url, num_requests=200, concurrency=10)
    print_benchmark_results(results)
    
    return results['successful'] > 150


def demo_health_check(url: str = "http://localhost:8080/health") -> bool:
    """
    Demo: Health Check Endpoint
    """
    print_section("Health Check Endpoint")
    
    logger.info(f"Checking {url}")
    
    response = http_get(url)
    
    print(f"\nStatus: {response.status_code}")
    print(f"Body: {response.body.strip()}")
    print(f"Latency: {response.latency_ms:.2f}ms")
    
    if response.status_code == 200:
        logger.info("✓ Health check passed")
        return True
    else:
        logger.error("✗ Health check failed")
        return False


def run_full_demo(docker: DockerManager) -> bool:
    """Run the complete demonstration."""
    url = "http://localhost:8080/"
    
    # Verify environment
    logger.info("Verifying environment...")
    if not wait_for_port("localhost", 8080, timeout=10):
        logger.error("Load balancer not available on port 8080")
        logger.error("Run 'python scripts/start_lab.py' first")
        return False
    
    results = {
        'load_balancing': demo_load_balancing(url),
        'headers': demo_headers_inspection(url),
        'health_check': demo_health_check(),
        'failover': demo_failover(docker, url),
        'benchmark': demo_benchmark(url),
    }
    
    # Summary
    print_section("Demo Summary")
    
    for name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        colour = "\033[32m" if passed else "\033[31m"
        reset = "\033[0m"
        print(f"  {name:20} {colour}{status}{reset}")
    
    all_passed = all(results.values())
    
    if all_passed:
        logger.info("\nAll demonstrations completed successfully!")
    else:
        logger.warning("\nSome demonstrations had issues. Check the output above.")
    
    return all_passed


def save_demo_log(output_dir: Path) -> None:
    """Save demo output to log file."""
    log_file = output_dir / f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    # Note: In a real implementation, we'd redirect stdout to a tee
    logger.info(f"Demo log would be saved to: {log_file}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run Week 11 Laboratory Demonstrations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Demonstrations:
  1: Load Balancing Distribution
  2: Failover Simulation
  3: Performance Benchmark
  4: Health Check
  all: Run all demonstrations (default)

Examples:
  %(prog)s                    # Run all demos
  %(prog)s --demo 1           # Run only load balancing demo
  %(prog)s --demo 2           # Run only failover demo
        """
    )
    parser.add_argument("--demo", type=str, default="all",
                        choices=["1", "2", "3", "4", "all"],
                        help="Specific demo to run (default: all)")
    parser.add_argument("--url", default="http://localhost:8080/",
                        help="Load balancer URL")
    parser.add_argument("--save-log", action="store_true",
                        help="Save demo output to artifacts/")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose output")
    
    args = parser.parse_args()
    
    print_banner("Week 11 Laboratory Demonstrations")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
    print("")
    
    docker_dir = PROJECT_ROOT / "docker"
    
    try:
        docker = DockerManager(docker_dir)
    except FileNotFoundError:
        docker = None
    
    try:
        if args.demo == "all":
            if docker is None:
                logger.error("Docker configuration not found")
                return 1
            success = run_full_demo(docker)
        elif args.demo == "1":
            success = demo_load_balancing(args.url)
        elif args.demo == "2":
            if docker is None:
                logger.error("Docker configuration required for failover demo")
                return 1
            success = demo_failover(docker, args.url)
        elif args.demo == "3":
            success = demo_benchmark(args.url)
        elif args.demo == "4":
            success = demo_health_check()
        else:
            logger.error(f"Unknown demo: {args.demo}")
            return 1
        
        if args.save_log:
            artifacts_dir = PROJECT_ROOT / "artifacts"
            artifacts_dir.mkdir(exist_ok=True)
            save_demo_log(artifacts_dir)
        
        return 0 if success else 1
    
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user")
        return 130
    
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())


# Revolvix&Hypotheticalandrei
