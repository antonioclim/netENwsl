#!/usr/bin/env python3
"""
Exercise 7.1: Baseline Traffic Capture
======================================
Computer Networks - Week 7 (WSL Environment)
ASE Bucharest, CSIE | by ing. dr. Antonio Clim

Objectives:
- Identify TCP and UDP packet fields in captured traffic
- Explain the difference between TCP handshake and UDP connectionless nature
- Apply tcpdump/Wireshark filters to isolate specific traffic

Prerequisites:
- Docker running in WSL
- Portainer accessible at http://localhost:9000
- Lab containers started (python scripts/start_lab.py)

Level: Beginner
Estimated time: 20 minutes

Pair Programming Notes:
- Driver: Execute commands and observe output
- Navigator: Verify packet counts match expectations
- Swap after: TCP test complete, before UDP test
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import socket
import sys
import time
from pathlib import Path
from typing import Tuple

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# ═══════════════════════════════════════════════════════════════════════════════
# PREDICTION_PROMPTS
# ═══════════════════════════════════════════════════════════════════════════════
def prompt_prediction(question: str) -> str:
    """
    Ask student to predict outcome before execution.
    
    Implements Brown & Wilson Principle 4: Predictions.
    Students learn more effectively when they commit to a prediction
    before seeing the result.
    
    Args:
        question: The prediction question to display
        
    Returns:
        The student's prediction (for logging purposes)
    """
    print(f"\n💭 PREDICTION: {question}")
    print("   (Think about your answer before pressing Enter)")
    prediction = input("   Your prediction: ")
    return prediction


# ═══════════════════════════════════════════════════════════════════════════════
# TCP_ECHO_TEST
# ═══════════════════════════════════════════════════════════════════════════════
def tcp_echo_test(
    host: str, 
    port: int, 
    message: str, 
    timeout: float = 5.0
) -> Tuple[bool, str]:
    """
    Test TCP echo functionality by connecting and sending a message.
    
    Creates a TCP socket, connects to the server, sends a message,
    and verifies the echoed response matches the original.
    
    Args:
        host: Server hostname or IP address
        port: Server port number
        message: Message string to send
        timeout: Socket timeout in seconds
        
    Returns:
        Tuple of (success: bool, response_or_error: str)
        
    Raises:
        No exceptions raised; all errors returned in tuple
    """
    try:
        # Create TCP socket (SOCK_STREAM = connection-oriented)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        print(f"   Connecting to {host}:{port}...")
        sock.connect((host, port))
        
        print(f"   Sending: {message}")
        sock.sendall(message.encode("utf-8"))
        
        response = sock.recv(4096).decode("utf-8")
        print(f"   Received: {response}")
        
        sock.close()
        
        if response.strip() == message:
            return True, response.strip()
        else:
            return False, f"Unexpected response: {response}"
            
    except socket.timeout:
        return False, "Connection timed out"
    except ConnectionRefusedError:
        return False, "Connection refused"
    except Exception as e:
        return False, str(e)


# ═══════════════════════════════════════════════════════════════════════════════
# UDP_SEND_TEST
# ═══════════════════════════════════════════════════════════════════════════════
def udp_send_test(
    host: str, 
    port: int, 
    message: str
) -> Tuple[bool, str]:
    """
    Test UDP send functionality by sending a datagram.
    
    Creates a UDP socket and sends a message. Note that UDP is
    connectionless, so we cannot verify delivery at the socket level.
    
    Args:
        host: Receiver hostname or IP address
        port: Receiver port number
        message: Message string to send
        
    Returns:
        Tuple of (success: bool, status_message: str)
        Note: 'success' only indicates the send call completed,
        not that the receiver got the packet.
    """
    try:
        # Create UDP socket (SOCK_DGRAM = connectionless)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        print(f"   Sending UDP to {host}:{port}: {message}")
        sock.sendto(message.encode("utf-8"), (host, port))
        sock.close()
        
        return True, "Datagram sent (delivery not guaranteed)"
        
    except Exception as e:
        return False, str(e)


# ═══════════════════════════════════════════════════════════════════════════════
# VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def verify_result(test_name: str, success: bool, details: str) -> None:
    """
    Display test result with clear pass/fail indication.
    
    Args:
        test_name: Name of the test for display
        success: Whether the test passed
        details: Additional details or error message
    """
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"   {status}: {test_name}")
    if not success:
        print(f"   Details: {details}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """
    Main entry point for Exercise 7.1.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    # ═══════════════════════════════════════════════════════════════════════════
    # PARSE_ARGUMENTS
    # ═══════════════════════════════════════════════════════════════════════════
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
    parser.add_argument(
        "--skip-predictions",
        action="store_true",
        help="Skip prediction prompts (for automated testing)"
    )
    args = parser.parse_args()

    # ═══════════════════════════════════════════════════════════════════════════
    # DISPLAY_HEADER
    # ═══════════════════════════════════════════════════════════════════════════
    print("=" * 70)
    print("Exercise 7.1: Baseline Traffic Capture")
    print("Computer Networks - Week 7 | ASE Bucharest, CSIE")
    print("=" * 70)
    print()
    print("This exercise generates TCP and UDP traffic for capture analysis.")
    print("Ensure you have started a packet capture before proceeding.")
    print()

    results = []

    # ═══════════════════════════════════════════════════════════════════════════
    # TCP_TEST_WITH_PREDICTION
    # ═══════════════════════════════════════════════════════════════════════════
    print("[1/2] TCP Echo Test")
    print("-" * 50)
    
    if not args.skip_predictions:
        prompt_prediction(
            "How many packets will Wireshark show for a successful TCP echo?\n"
            "   (Hint: consider handshake + data + acknowledgements)"
        )
    
    print()
    success, response = tcp_echo_test(
        args.tcp_host,
        args.tcp_port,
        args.message + "_tcp"
    )
    verify_result("TCP Echo", success, response)
    results.append(("TCP Echo", success))
    print()

    # Brief pause between tests for clearer packet separation
    time.sleep(0.5)

    # ═══════════════════════════════════════════════════════════════════════════
    # UDP_TEST_WITH_PREDICTION
    # ═══════════════════════════════════════════════════════════════════════════
    print("[2/2] UDP Send Test")
    print("-" * 50)
    
    if not args.skip_predictions:
        prompt_prediction(
            "How many packets will Wireshark show for the UDP test?\n"
            "   (Hint: UDP is connectionless - no handshake)"
        )
    
    print()
    success, status = udp_send_test(
        args.udp_host,
        args.udp_port,
        args.message + "_udp"
    )
    verify_result("UDP Send", success, status)
    results.append(("UDP Send", success))
    print()

    # ═══════════════════════════════════════════════════════════════════════════
    # SUMMARY_AND_NEXT_STEPS
    # ═══════════════════════════════════════════════════════════════════════════
    print("=" * 70)
    print("Results Summary")
    print("=" * 70)
    
    all_passed = True
    for name, passed in results:
        status = "✅" if passed else "❌"
        print(f"  {status} {name}")
        if not passed:
            all_passed = False

    print()
    if all_passed:
        print("✅ Baseline connectivity verified successfully.")
        print()
        print("Next steps:")
        print("  1. Stop the traffic capture")
        print("  2. Open the .pcap file in Wireshark")
        print("  3. Apply filter: tcp.port == 9090")
        print("  4. Identify the TCP handshake packets (SYN, SYN-ACK, ACK)")
        print("  5. Apply filter: udp.port == 9091")
        print("  6. Observe the UDP datagram (single packet, no handshake)")
        print()
        print("Questions to answer:")
        print("  - How many TCP packets before data transfer begins?")
        print("  - What is the payload size in the UDP packet?")
        print("  - Which protocol has more overhead?")
        return 0
    else:
        print("❌ Some tests failed. Check that services are running:")
        print("     python scripts/start_lab.py --status")
        return 1


if __name__ == "__main__":
    sys.exit(main())
