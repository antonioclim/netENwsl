#!/usr/bin/env python3
"""
Exercise 7.1: Baseline Traffic Capture
NETWORKING class - ASE, Informatics | by Revolvix

This exercise establishes baseline TCP and UDP connectivity and
captures evidence of successful communication.
"""

from __future__ import annotations

import argparse
import socket
import sys
import time
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def tcp_echo_test(host: str, port: int, message: str, timeout: float = 5.0) -> tuple[bool, str]:
    """
    Test TCP echo functionality.
    
    Args:
        host: Server hostname or IP
        port: Server port
        message: Message to send
        timeout: Socket timeout
        
    Returns:
        Tuple of (success, response_or_error)
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        print(f"Connecting to {host}:{port}...")
        sock.connect((host, port))
        
        print(f"Sending: {message}")
        sock.sendall(message.encode("utf-8"))
        
        response = sock.recv(4096).decode("utf-8")
        print(f"Received: {response}")
        
        sock.close()
        
        if response.strip() == message:
            return True, response.strip()
        else:
            return False, f"Unexpected response: {response}"
            
    except Exception as e:
        return False, str(e)


def udp_send_test(host: str, port: int, message: str) -> tuple[bool, str]:
    """
    Test UDP send functionality.
    
    Args:
        host: Receiver hostname or IP
        port: Receiver port
        message: Message to send
        
    Returns:
        Tuple of (success, status_message)
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        print(f"Sending UDP to {host}:{port}: {message}")
        sock.sendto(message.encode("utf-8"), (host, port))
        sock.close()
        
        return True, "Datagram sent"
        
    except Exception as e:
        return False, str(e)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Exercise 7.1: Baseline Traffic Capture",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
This exercise verifies baseline connectivity for both TCP and UDP protocols.

Steps:
1. Ensure the laboratory environment is running (python scripts/start_lab.py)
2. Start a traffic capture in another terminal
3. Run this exercise to generate test traffic
4. Analyse the capture in Wireshark

Expected observations:
- TCP: Complete three-way handshake (SYN, SYN-ACK, ACK)
- TCP: Echo request and response payloads
- UDP: Datagram with payload, no connection establishment
"""
    )
    parser.add_argument(
        "--tcp-host",
        default="localhost",
        help="TCP server host (default: localhost)"
    )
    parser.add_argument(
        "--tcp-port",
        type=int,
        default=9090,
        help="TCP server port (default: 9090)"
    )
    parser.add_argument(
        "--udp-host",
        default="localhost",
        help="UDP receiver host (default: localhost)"
    )
    parser.add_argument(
        "--udp-port",
        type=int,
        default=9091,
        help="UDP receiver port (default: 9091)"
    )
    parser.add_argument(
        "--message",
        default="exercise_7_1_baseline",
        help="Test message to send"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("Exercise 7.1: Baseline Traffic Capture")
    print("NETWORKING class - ASE, Informatics")
    print("=" * 60)
    print()

    results = []

    # TCP test
    print("[TCP Echo Test]")
    print("-" * 40)
    success, response = tcp_echo_test(
        args.tcp_host,
        args.tcp_port,
        args.message + "_tcp"
    )
    results.append(("TCP Echo", success))
    print()

    # Brief pause between tests
    time.sleep(0.5)

    # UDP test
    print("[UDP Send Test]")
    print("-" * 40)
    success, status = udp_send_test(
        args.udp_host,
        args.udp_port,
        args.message + "_udp"
    )
    results.append(("UDP Send", success))
    print()

    # Summary
    print("=" * 60)
    print("Results Summary")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} {name}")
        if not passed:
            all_passed = False

    print()
    if all_passed:
        print("Baseline connectivity verified successfully.")
        print()
        print("Next steps:")
        print("1. Stop the traffic capture")
        print("2. Open the .pcap file in Wireshark")
        print("3. Apply filter: tcp.port == 9090")
        print("4. Identify the TCP handshake packets")
        print("5. Apply filter: udp.port == 9091")
        print("6. Observe the UDP datagram")
        return 0
    else:
        print("Some tests failed. Check that services are running:")
        print("  python scripts/start_lab.py --status")
        return 1


if __name__ == "__main__":
    sys.exit(main())
