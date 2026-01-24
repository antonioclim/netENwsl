#!/usr/bin/env python3
"""
Week 3 Demonstration Runner
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Runs automated demonstrations for projector display and verification.
"""

# ════════════════════════════════════════════════════════════════════════════════
# IMPORTS AND CONFIGURATION
# ════════════════════════════════════════════════════════════════════════════════

import subprocess
import sys
import time
import argparse
from pathlib import Path
from typing import Dict, Tuple, Callable

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.logger import setup_logger
from scripts.utils.network_utils import tcp_echo_test, check_port_open

logger = setup_logger("demo")


# ════════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ════════════════════════════════════════════════════════════════════════════════

def run_in_container(container: str, command: str, 
                     capture: bool = True) -> subprocess.CompletedProcess:
    """Execute a command in a Docker container."""
    cmd = ["docker", "exec", container, "bash", "-c", command]
    
    if capture:
        return subprocess.run(cmd, capture_output=True, text=True)
    else:
        return subprocess.run(cmd)


def print_section(title: str) -> None:
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


# ════════════════════════════════════════════════════════════════════════════════
# DEMO: UDP BROADCAST
# ════════════════════════════════════════════════════════════════════════════════

def demo_broadcast() -> bool:
    """Demonstrate UDP broadcast communication."""
    print_section("Demo 1: UDP Broadcast")
    
    print("UDP broadcast sends datagrams to all hosts in a Layer 2 domain.")
    print("The address 255.255.255.255 is a 'limited broadcast'.\n")
    
    # Start receiver in background
    logger.info("Starting broadcast receiver on client...")
    recv_proc = subprocess.Popen([
        "docker", "exec", "week3_client",
        "python3", "/app/src/exercises/ex_3_01_udp_broadcast.py",
        "recv", "--port", "5007", "--count", "3", "--timeout", "10",
        "--no-predict"
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    time.sleep(1)
    
    # Send broadcast messages
    logger.info("Sending 3 broadcast messages...")
    run_in_container(
        "week3_client",
        "python3 /app/src/exercises/ex_3_01_udp_broadcast.py send "
        "--dst 255.255.255.255 --port 5007 --count 3 --interval 0.5 --no-predict"
    )
    
    # Wait for receiver
    try:
        stdout, _ = recv_proc.communicate(timeout=15)
        print("\nReceiver output:")
        print(stdout)
    except subprocess.TimeoutExpired:
        recv_proc.kill()
        logger.warning("Receiver timed out")
    
    print("\nObservations:")
    print("  • All hosts on the network segment receive the broadcast")
    print("  • SO_BROADCAST option must be set on the sender socket")
    print("  • Broadcast does not cross router boundaries")
    
    return True


# ════════════════════════════════════════════════════════════════════════════════
# DEMO: UDP MULTICAST
# ════════════════════════════════════════════════════════════════════════════════

def demo_multicast() -> bool:
    """Demonstrate UDP multicast communication."""
    print_section("Demo 2: UDP Multicast")
    
    print("UDP multicast delivers to hosts that have joined a group address.")
    print("Group addresses are in the range 224.0.0.0 - 239.255.255.255.\n")
    
    multicast_group = "239.1.1.1"
    port = "5008"
    
    # Start receiver
    logger.info(f"Starting multicast receiver on group {multicast_group}...")
    recv_proc = subprocess.Popen([
        "docker", "exec", "week3_client",
        "python3", "/app/src/exercises/ex_3_02_udp_multicast.py",
        "recv", "--group", multicast_group, "--port", port, 
        "--count", "3", "--timeout", "10", "--no-predict"
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    time.sleep(2)  # Allow time for IGMP join
    
    # Send multicast messages
    logger.info("Sending 3 multicast messages...")
    run_in_container(
        "week3_server",
        f"python3 /app/src/exercises/ex_3_02_udp_multicast.py send "
        f"--group {multicast_group} --port {port} --count 3 --interval 0.5 "
        f"--ttl 4 --no-predict"
    )
    
    # Wait for receiver
    try:
        stdout, _ = recv_proc.communicate(timeout=15)
        print("\nReceiver output:")
        print(stdout)
    except subprocess.TimeoutExpired:
        recv_proc.kill()
        logger.warning("Receiver timed out")
    
    print("\nObservations:")
    print("  • Receiver sends IGMP Membership Report when joining group")
    print("  • Only subscribed receivers get the multicast data")
    print("  • TTL controls how many router hops multicast can traverse")
    
    return True


# ════════════════════════════════════════════════════════════════════════════════
# DEMO: TCP TUNNEL
# ════════════════════════════════════════════════════════════════════════════════

def demo_tunnel() -> bool:
    """Demonstrate TCP tunnel (port forwarding)."""
    print_section("Demo 3: TCP Tunnel")
    
    print("TCP tunnel relays connections between endpoints.")
    print("Client → Tunnel (router:9090) → Server (server:8080)\n")
    
    # Test direct connection
    logger.info("Testing direct connection to echo server...")
    result = run_in_container(
        "week3_client",
        "echo 'DIRECT_TEST' | nc -w 2 server 8080"
    )
    print(f"Direct response: {result.stdout.strip()}")
    
    # Test through tunnel
    logger.info("Testing connection through tunnel...")
    result = run_in_container(
        "week3_client",
        "echo 'TUNNEL_TEST' | nc -w 2 router 9090"
    )
    print(f"Tunnel response: {result.stdout.strip()}")
    
    # Show tunnel logs
    logger.info("Tunnel activity (from router logs):")
    subprocess.run([
        "docker", "logs", "--tail", "10", "week3_router"
    ])
    
    print("\nObservations:")
    print("  • Tunnel accepts connection on port 9090")
    print("  • Opens new connection to server:8080")
    print("  • Forwards data bidirectionally between connections")
    print("  • Two separate TCP sessions visible in captures")
    
    return True


# ════════════════════════════════════════════════════════════════════════════════
# DEMO: ECHO TEST
# ════════════════════════════════════════════════════════════════════════════════

def demo_echo_test() -> bool:
    """Quick echo server functionality test."""
    print_section("Echo Server Test")
    
    # Test using Python directly
    success, response = tcp_echo_test("localhost", 8080, "HELLO_FROM_HOST")
    
    if success:
        logger.info(f"Echo server response: {response}")
        return True
    else:
        logger.warning(f"Echo test failed: {response}")
        # Try via container
        result = run_in_container(
            "week3_client",
            "echo 'HELLO' | nc -w 2 server 8080"
        )
        if result.stdout:
            logger.info(f"Via container: {result.stdout.strip()}")
            return True
        return False


# ════════════════════════════════════════════════════════════════════════════════
# DEMO REGISTRY
# ════════════════════════════════════════════════════════════════════════════════

DEMOS: Dict[str, Callable[[], bool]] = {
    "broadcast": demo_broadcast,
    "multicast": demo_multicast,
    "tunnel": demo_tunnel,
    "echo": demo_echo_test,
}


# ════════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ════════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run Week 3 Laboratory Demonstrations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available demos:
  broadcast   UDP broadcast sender and receiver
  multicast   UDP multicast with group membership
  tunnel      TCP tunnel (port forwarding)
  echo        Quick echo server test
  all         Run all demos in sequence

Examples:
  python run_demo.py --demo broadcast
  python run_demo.py --demo all
        """
    )
    parser.add_argument(
        "-d", "--demo", default="all",
        choices=list(DEMOS.keys()) + ["all"],
        help="Demo to run (default: all)"
    )
    parser.add_argument(
        "--pause", action="store_true",
        help="Pause between demos"
    )
    args = parser.parse_args()

    # ─────────────────────────────────────────────────────────────────────────
    # Step 1: Display banner
    # ─────────────────────────────────────────────────────────────────────────
    print("""
╔══════════════════════════════════════════════════════════════╗
║     WEEK 3 — Network Programming Demonstrations             ║
║     NETWORKING class - ASE, Informatics                     ║
╚══════════════════════════════════════════════════════════════╝
""")

    # ─────────────────────────────────────────────────────────────────────────
    # Step 2: Check containers are running
    # ─────────────────────────────────────────────────────────────────────────
    result = subprocess.run(
        ["docker", "ps", "-q", "--filter", "name=week3_client"],
        capture_output=True,
        text=True
    )
    if not result.stdout.strip():
        logger.error("Week 3 containers are not running!")
        logger.error("Start them with: python scripts/start_lab.py")
        return 1

    # ─────────────────────────────────────────────────────────────────────────
    # Step 3: Run selected demos
    # ─────────────────────────────────────────────────────────────────────────
    demos_to_run = list(DEMOS.keys()) if args.demo == "all" else [args.demo]
    
    results: Dict[str, bool] = {}
    for demo_name in demos_to_run:
        try:
            success = DEMOS[demo_name]()
            results[demo_name] = success
            
            if args.pause and demo_name != demos_to_run[-1]:
                input("\nPress Enter to continue to next demo...")
                
        except Exception as e:
            logger.error(f"Demo {demo_name} failed: {e}")
            results[demo_name] = False

    # ─────────────────────────────────────────────────────────────────────────
    # Step 4: Display summary
    # ─────────────────────────────────────────────────────────────────────────
    print_section("Demo Summary")
    
    for name, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {status}  {name}")
    
    failed = sum(1 for s in results.values() if not s)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
