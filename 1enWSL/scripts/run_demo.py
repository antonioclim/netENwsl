#!/usr/bin/env python3
"""
Week 1 Demonstration Runner
NETWORKING class - ASE, Informatics | by Revolvix

This script runs automated demonstrations that can be displayed on a projector
during laboratory sessions.
"""

from __future__ import annotations

import subprocess
import sys
import argparse
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.logger import setup_logger

logger = setup_logger("run_demo")

CONTAINER = "week1_lab"


def check_container_running() -> bool:
    """Check if the lab container is running."""
    try:
        result = subprocess.run(
            ["docker", "inspect", "--format", "{{.State.Running}}", CONTAINER],
            capture_output=True,
            text=True
        )
        return result.stdout.strip() == "true"
    except Exception:
        return False


def run_in_container(command: str, show_command: bool = True) -> tuple[int, str]:
    """Execute a command in the lab container."""
    if show_command:
        print(f"\n\033[94m$ {command}\033[0m")
    
    result = subprocess.run(
        ["docker", "exec", CONTAINER, "bash", "-c", command],
        capture_output=True,
        text=True
    )
    
    output = result.stdout
    if result.stderr:
        output += result.stderr
    
    if output.strip():
        print(output)
    
    return result.returncode, output


def pause(message: str = "Press Enter to continue..."):
    """Pause for instructor/student interaction."""
    try:
        input(f"\n\033[93m{message}\033[0m")
    except (EOFError, KeyboardInterrupt):
        print()


def demo_1_network_diagnostics():
    """Demo 1: Complete network diagnostic sequence."""
    print("\n" + "=" * 70)
    print("  DEMO 1: Network Diagnostic Sequence")
    print("  Demonstrates fundamental network inspection commands")
    print("=" * 70)
    
    pause("Ready to begin Demo 1?")
    
    # Step 1: Interface inspection
    print("\n\033[1m--- Step 1: Network Interface Inspection ---\033[0m")
    print("The 'ip addr' command shows all network interfaces and their addresses.")
    run_in_container("ip -br addr show")
    pause()
    
    print("\nDetailed view with 'ip addr show':")
    run_in_container("ip addr show eth0 2>/dev/null || ip addr show | head -20")
    pause()
    
    # Step 2: Routing table
    print("\n\033[1m--- Step 2: Routing Table ---\033[0m")
    print("The routing table determines where packets are sent.")
    run_in_container("ip route show")
    pause()
    
    # Step 3: Socket inspection
    print("\n\033[1m--- Step 3: Socket State Inspection ---\033[0m")
    print("The 'ss' command shows socket statistics.")
    print("\nListening TCP sockets:")
    run_in_container("ss -tlnp")
    pause()
    
    print("\nAll sockets (TCP + UDP):")
    run_in_container("ss -tunap | head -15")
    pause()
    
    # Step 4: Connectivity testing
    print("\n\033[1m--- Step 4: Connectivity Testing ---\033[0m")
    
    print("\nTesting loopback (TCP/IP stack verification):")
    run_in_container("ping -c 3 127.0.0.1")
    pause()
    
    print("\nTesting external connectivity:")
    run_in_container("ping -c 3 8.8.8.8 2>/dev/null || echo 'External ping may be blocked in container'")
    pause()
    
    # Summary
    print("\n" + "=" * 70)
    print("  DEMO 1 COMPLETE")
    print("  Key commands: ip addr, ip route, ss, ping")
    print("=" * 70)


def demo_2_tcp_vs_udp():
    """Demo 2: TCP vs UDP comparison."""
    print("\n" + "=" * 70)
    print("  DEMO 2: TCP vs UDP Comparison")
    print("  Demonstrates the fundamental differences between TCP and UDP")
    print("=" * 70)
    
    pause("Ready to begin Demo 2?")
    
    # TCP demonstration
    print("\n\033[1m--- TCP Communication ---\033[0m")
    print("TCP is connection-oriented. It requires a handshake before data transfer.")
    
    print("\n1. Starting TCP server on port 9095:")
    # Start server in background
    run_in_container("timeout 10 nc -l -p 9095 > /tmp/tcp_received.txt &")
    time.sleep(1)
    
    print("\n2. Sending message via TCP:")
    run_in_container("echo 'Hello TCP!' | nc localhost 9095")
    time.sleep(1)
    
    print("\n3. Message received by server:")
    run_in_container("cat /tmp/tcp_received.txt")
    pause()
    
    # UDP demonstration
    print("\n\033[1m--- UDP Communication ---\033[0m")
    print("UDP is connectionless. Data is sent immediately without handshake.")
    
    print("\n1. Starting UDP server on port 9096:")
    run_in_container("timeout 5 nc -u -l -p 9096 > /tmp/udp_received.txt &")
    time.sleep(1)
    
    print("\n2. Sending message via UDP:")
    run_in_container("echo 'Hello UDP!' | nc -u -w 1 localhost 9096")
    time.sleep(2)
    
    print("\n3. Message received by server:")
    run_in_container("cat /tmp/udp_received.txt")
    pause()
    
    # Key differences
    print("\n\033[1m--- Key Differences ---\033[0m")
    print("""
    ┌─────────────────┬──────────────────────┬──────────────────────┐
    │ Characteristic  │        TCP           │        UDP           │
    ├─────────────────┼──────────────────────┼──────────────────────┤
    │ Connection      │ Required (handshake) │ Not required         │
    │ Reliability     │ Guaranteed delivery  │ Best effort          │
    │ Ordering        │ Preserved            │ Not guaranteed       │
    │ Overhead        │ Higher               │ Lower                │
    │ Use cases       │ HTTP, FTP, SSH       │ DNS, VoIP, streaming │
    └─────────────────┴──────────────────────┴──────────────────────┘
    """)
    pause()
    
    print("\n" + "=" * 70)
    print("  DEMO 2 COMPLETE")
    print("  TCP: Connection-oriented, reliable, ordered")
    print("  UDP: Connectionless, fast, no guarantees")
    print("=" * 70)


def demo_3_python_sockets():
    """Demo 3: Python socket programming."""
    print("\n" + "=" * 70)
    print("  DEMO 3: Python Socket Programming")
    print("  Demonstrates TCP client-server communication using Python")
    print("=" * 70)
    
    pause("Ready to begin Demo 3?")
    
    print("\n\033[1m--- Running Python TCP Exercise ---\033[0m")
    print("The exercise creates a server and client in the same process.")
    
    run_in_container("python /work/src/exercises/ex_1_02_tcp_server_client.py --port 9097")
    pause()
    
    print("\n\033[1m--- Ping Latency Measurement ---\033[0m")
    print("Python can also be used to analyse ping results programmatically.")
    
    run_in_container("python /work/src/exercises/ex_1_01_ping_latency.py --host 127.0.0.1 --count 5")
    pause()
    
    print("\n" + "=" * 70)
    print("  DEMO 3 COMPLETE")
    print("  Python's socket library provides full control over network I/O")
    print("=" * 70)


DEMOS = {
    1: ("Network Diagnostics", demo_1_network_diagnostics),
    2: ("TCP vs UDP Comparison", demo_2_tcp_vs_udp),
    3: ("Python Sockets", demo_3_python_sockets),
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run Week 1 Laboratory Demonstrations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available Demos:
  1 - Network Diagnostics (ip, ss, ping)
  2 - TCP vs UDP Comparison
  3 - Python Socket Programming

Examples:
  python scripts/run_demo.py --demo 1
  python scripts/run_demo.py --demo 2
  python scripts/run_demo.py --list
        """
    )
    parser.add_argument(
        "--demo", "-d",
        type=int,
        choices=DEMOS.keys(),
        help="Demo number to run"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available demos"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Run all demos in sequence"
    )
    args = parser.parse_args()

    if args.list:
        print("\nAvailable Demonstrations:")
        print("-" * 50)
        for num, (name, _) in DEMOS.items():
            print(f"  {num}. {name}")
        print("-" * 50)
        print("\nUsage: python scripts/run_demo.py --demo <number>")
        return 0

    if not check_container_running():
        logger.error(f"Container '{CONTAINER}' is not running.")
        logger.info("Start the lab first: python scripts/start_lab.py")
        return 1

    if args.all:
        print("\n" + "=" * 70)
        print("  WEEK 1: All Demonstrations")
        print("  NETWORKING class - ASE, Informatics | by Revolvix")
        print("=" * 70)
        
        for num, (name, func) in DEMOS.items():
            func()
            if num < len(DEMOS):
                pause(f"Demo {num} complete. Press Enter for next demo...")
        
        print("\n\033[92mAll demonstrations complete.\033[0m")
        return 0

    if args.demo:
        name, func = DEMOS[args.demo]
        print("\n" + "=" * 70)
        print(f"  WEEK 1: {name}")
        print("  NETWORKING class - ASE, Informatics | by Revolvix")
        print("=" * 70)
        
        func()
        return 0

    # No arguments - show help
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
