#!/usr/bin/env python3
"""
Week 5 Demonstration Script
===========================
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Automated demonstrations for classroom presentation.

Learning Objectives:
    - Observe CIDR analysis in action
    - Compare FLSM and VLSM approaches
    - Understand IPv6 address operations
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import sys
import time
import argparse
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURE_MODULE_PATH
# ═══════════════════════════════════════════════════════════════════════════════
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT_UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════
from scripts.utils.logger import setup_logger

logger = setup_logger("run_demo")


# ═══════════════════════════════════════════════════════════════════════════════
# CONTAINER_EXECUTION_HELPER
# ═══════════════════════════════════════════════════════════════════════════════
def run_in_container(container: str, cmd: str, timeout: int = 30) -> tuple:
    """
    Execute a command in a container and return output.
    
    Args:
        container: Name of the Docker container
        cmd: Command to execute
        timeout: Maximum execution time in seconds
        
    Returns:
        Tuple of (return_code, stdout, stderr)
    """
    full_cmd = ["docker", "exec", container] + cmd.split()
    try:
        result = subprocess.run(full_cmd, capture_output=True, text=True, timeout=timeout)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out"


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO_CIDR_ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
def demo_cidr_analysis():
    """Demo 1: CIDR Analysis and Binary Representation."""
    logger.info("=" * 70)
    logger.info("DEMO 1: CIDR Analysis and Binary Representation")
    logger.info("=" * 70)
    print()
    
    addresses = [
        "192.168.10.14/26",
        "10.0.0.100/24",
        "172.16.50.1/28",
        "192.168.1.1/30"
    ]
    
    for addr in addresses:
        logger.info(f"Analysing: {addr}")
        print("-" * 50)
        
        code, stdout, stderr = run_in_container(
            "week5_python",
            f"python /app/src/exercises/ex_5_01_cidr_flsm.py analyse {addr}"
        )
        
        if code == 0:
            print(stdout)
        else:
            logger.error(f"Failed: {stderr}")
        
        time.sleep(1)
    
    # Show binary representation
    logger.info("Binary representation of 192.168.10.14:")
    code, stdout, stderr = run_in_container(
        "week5_python",
        "python /app/src/exercises/ex_5_01_cidr_flsm.py binary 192.168.10.14"
    )
    if code == 0:
        print(stdout)


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO_FLSM_VS_VLSM
# ═══════════════════════════════════════════════════════════════════════════════
def demo_flsm_vs_vlsm():
    """Demo 2: FLSM vs VLSM Comparison."""
    logger.info("=" * 70)
    logger.info("DEMO 2: FLSM vs VLSM Comparison")
    logger.info("=" * 70)
    print()
    
    base_network = "192.168.100.0/24"
    requirements = [60, 20, 10, 2]
    
    # FLSM approach
    logger.info(f"Scenario: {base_network} needs networks for {requirements} hosts")
    print()
    
    logger.info("FLSM Approach: Split into 4 equal subnets")
    print("-" * 50)
    
    code, stdout, stderr = run_in_container(
        "week5_python",
        f"python /app/src/exercises/ex_5_01_cidr_flsm.py flsm {base_network} 4"
    )
    if code == 0:
        print(stdout)
    
    time.sleep(2)
    
    # VLSM approach
    logger.info("VLSM Approach: Variable-sized subnets")
    print("-" * 50)
    
    reqs_str = " ".join(map(str, requirements))
    code, stdout, stderr = run_in_container(
        "week5_python",
        f"python /app/src/exercises/ex_5_02_vlsm_ipv6.py vlsm {base_network} {reqs_str}"
    )
    if code == 0:
        print(stdout)
    
    logger.info("Key observation: VLSM achieves better address utilisation efficiency")


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO_IPV6
# ═══════════════════════════════════════════════════════════════════════════════
def demo_ipv6():
    """Demo 3: IPv6 Address Operations."""
    logger.info("=" * 70)
    logger.info("DEMO 3: IPv6 Address Operations")
    logger.info("=" * 70)
    print()
    
    # Show address types
    logger.info("IPv6 Address Types:")
    print("-" * 50)
    
    code, stdout, stderr = run_in_container(
        "week5_python",
        "python /app/src/exercises/ex_5_02_vlsm_ipv6.py ipv6-types"
    )
    if code == 0:
        print(stdout)
    
    time.sleep(1)
    
    # Compression demonstration
    full_addr = "2001:0db8:0000:0000:0000:0000:0000:0001"
    logger.info(f"Compressing: {full_addr}")
    print("-" * 50)
    
    code, stdout, stderr = run_in_container(
        "week5_python",
        f"python /app/src/exercises/ex_5_02_vlsm_ipv6.py ipv6 {full_addr}"
    )
    if code == 0:
        print(stdout)
    
    time.sleep(1)
    
    # Generate subnets
    logger.info("Generating /64 subnets from /48 allocation:")
    print("-" * 50)
    
    code, stdout, stderr = run_in_container(
        "week5_python",
        "python /app/src/exercises/ex_5_02_vlsm_ipv6.py ipv6-subnets 2001:db8:10::/48 64 5"
    )
    if code == 0:
        print(stdout)


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO_UDP_COMMUNICATION
# ═══════════════════════════════════════════════════════════════════════════════
def demo_udp_communication():
    """Demo 4: UDP Communication in Docker Network."""
    logger.info("=" * 70)
    logger.info("DEMO 4: UDP Communication in Docker Network")
    logger.info("=" * 70)
    print()
    
    # Show container IP addresses
    logger.info("Container IP addresses in 10.5.0.0/24 network:")
    print("-" * 50)
    
    containers = ["week5_python", "week5_udp-server"]
    for container in containers:
        code, stdout, stderr = run_in_container(
            container,
            "ip addr show eth0"
        )
        if code == 0:
            # Extract IP address line
            for line in stdout.split('\n'):
                if 'inet ' in line:
                    logger.info(f"{container}: {line.strip()}")
    
    print()
    
    # Start a manual UDP exchange
    logger.info("Sending UDP message to server...")
    
    code, stdout, stderr = run_in_container(
        "week5_python",
        "python /app/src/apps/udp_echo.py client --host 10.5.0.20 --port 9999 --count 3 --message 'Hello from demo'"
    )
    if code == 0:
        print(stdout)
    else:
        logger.warning("UDP demo requires udp-server container to be running")


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD_ARGUMENT_PARSER
# ═══════════════════════════════════════════════════════════════════════════════
def build_parser() -> argparse.ArgumentParser:
    """
    Build the command-line argument parser.
    
    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description="Run Week 5 demonstrations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Demonstrations:
  1 - CIDR Analysis and Binary Representation
  2 - FLSM vs VLSM Comparison
  3 - IPv6 Address Operations
  4 - UDP Communication in Docker Network
  all - Run all demonstrations

Examples:
  python run_demo.py --demo 1
  python run_demo.py --demo all
"""
    )
    parser.add_argument("--demo", "-d", default="all",
                        help="Demo number (1-4) or 'all' (default: all)")
    parser.add_argument("--pause", "-p", action="store_true",
                        help="Pause between demos")
    return parser


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """
    Main entry point for the demonstration script.
    
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    parser = build_parser()
    args = parser.parse_args()
    
    demos = {
        "1": demo_cidr_analysis,
        "2": demo_flsm_vs_vlsm,
        "3": demo_ipv6,
        "4": demo_udp_communication,
    }
    
    # ─────────────────────────────────────────────────────────────────────────
    # VERIFY_CONTAINERS_RUNNING
    # ─────────────────────────────────────────────────────────────────────────
    result = subprocess.run(
        ["docker", "ps", "--filter", "name=week5_python", "--format", "{{.Names}}"],
        capture_output=True,
        text=True
    )
    if "week5_python" not in result.stdout:
        logger.error("Laboratory containers are not running.")
        logger.info("Start them with: python scripts/start_lab.py")
        return 1
    
    # ─────────────────────────────────────────────────────────────────────────
    # RUN_SELECTED_DEMOS
    # ─────────────────────────────────────────────────────────────────────────
    logger.info("Week 5: Network Layer - IP Addressing Demonstrations")
    logger.info("NETWORKING class - ASE, Informatics")
    print()
    
    if args.demo.lower() == "all":
        for demo_num, demo_func in demos.items():
            demo_func()
            if args.pause and demo_num != "4":
                input("\nPress Enter to continue to next demo...")
            print("\n")
    elif args.demo in demos:
        demos[args.demo]()
    else:
        logger.error(f"Unknown demo: {args.demo}")
        logger.info(f"Available demos: {', '.join(demos.keys())}, all")
        return 1
    
    # ─────────────────────────────────────────────────────────────────────────
    # DISPLAY_COMPLETION
    # ─────────────────────────────────────────────────────────────────────────
    logger.info("=" * 70)
    logger.info("Demonstrations complete")
    logger.info("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
