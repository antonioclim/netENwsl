#!/usr/bin/env python3
"""
Homework 1.02: Protocol Analysis Helper
=======================================
Computer Networks - Week 1 (WSL Environment)
ASE Bucharest | by ing. dr. Antonio Clim

This starter script helps you capture and analyse TCP/UDP traffic.
Complete the exercises and use this to generate your analysis.

Objectives:
- Demonstrate TCP and UDP traffic generation
- Apply packet capture techniques using tcpdump
- Analyse protocol behaviour using tshark
- Compare TCP and UDP communication patterns

Prerequisites:
- tcpdump and tshark installed
- Root/sudo access for packet capture
- Understanding of TCP/UDP differences

Level: Intermediate
Estimated time: 45-60 minutes

Pair Programming Notes:
- Driver: Run capture commands and observe output
- Navigator: Predict packet counts and flag sequences
- Swap after: Completing TCP analysis, before UDP

Usage:
    python hw_1_02_protocol_analysis.py --mode tcp --output tcp_analysis.pcap
    python hw_1_02_protocol_analysis.py --mode udp --output udp_analysis.pcap
    python hw_1_02_protocol_analysis.py --analyse tcp_analysis.pcap
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import subprocess
import socket
import threading
import time
from pathlib import Path
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════════
# PREDICTION_PROMPT
# ═══════════════════════════════════════════════════════════════════════════════
def prompt_prediction(mode: str, messages: int) -> None:
    """
    Ask student to predict traffic patterns before capture.
    
    Implements Brown & Wilson Principle 4: Building mental models
    through prediction.
    """
    print("\n" + "=" * 60)
    print("💭 PREDICTION TIME")
    print("=" * 60)
    print(f"You are about to generate {messages} {mode.upper()} messages.")
    print()
    if mode == "tcp":
        print("Before capture, predict:")
        print("  1. How many packets for the handshake? (hint: 3-way)")
        print("  2. How many data packets for 5 messages + responses?")
        print("  3. How many packets to close the connection?")
        print("  4. What TCP flags will you see? (SYN, ACK, FIN, PSH)")
    else:
        print("Before capture, predict:")
        print("  1. Will there be a handshake? (compare to TCP)")
        print("  2. How many packets for 5 messages + responses?")
        print("  3. What happens if a packet is lost?")
    print("=" * 60)
    input("Press Enter to continue and verify your predictions...")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# TCP_TRAFFIC_GENERATION
# ═══════════════════════════════════════════════════════════════════════════════
def create_tcp_traffic(host: str, port: int, messages: int = 5) -> None:
    """
    Generate TCP traffic by running a simple echo server and client.
    
    Creates a TCP server in a background thread, then connects a client
    that sends multiple messages and receives responses.
    
    Args:
        host: Address to bind/connect (usually 127.0.0.1)
        port: Port number for communication
        messages: Number of messages to exchange
    """
    # Event to signal server is ready
    server_ready = threading.Event()
    
    # ─────────────────────────────────────────────────────────────────────────
    # SERVER THREAD
    # ─────────────────────────────────────────────────────────────────────────
    def server():
        """TCP echo server that responds to each message."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Allow port reuse to avoid "Address already in use"
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            s.listen(1)
            server_ready.set()  # Signal that server is listening
            
            conn, addr = s.accept()
            with conn:
                for _ in range(messages):
                    data = conn.recv(1024)
                    if not data:
                        break
                    # Echo back with ACK prefix
                    conn.sendall(b"ACK:" + data)
    
    # Start server in background
    server_thread = threading.Thread(target=server, daemon=True)
    server_thread.start()
    server_ready.wait(timeout=5)
    
    # ─────────────────────────────────────────────────────────────────────────
    # CLIENT COMMUNICATION
    # ─────────────────────────────────────────────────────────────────────────
    time.sleep(0.5)  # Brief delay for server setup
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        for i in range(messages):
            msg = f"Message {i+1}\n".encode()
            s.sendall(msg)
            response = s.recv(1024)
            print(f"Sent: {msg.decode().strip()} | Received: {response.decode().strip()}")
            time.sleep(0.2)  # Small delay between messages
    
    server_thread.join(timeout=2)


# ═══════════════════════════════════════════════════════════════════════════════
# UDP_TRAFFIC_GENERATION
# ═══════════════════════════════════════════════════════════════════════════════
def create_udp_traffic(host: str, port: int, messages: int = 5) -> None:
    """
    Generate UDP traffic by running a simple echo server and client.
    
    Unlike TCP, UDP has no connection establishment — packets are
    sent immediately without handshake.
    
    Args:
        host: Address to bind/connect
        port: Port number for communication
        messages: Number of messages to exchange
    """
    server_ready = threading.Event()
    
    # ─────────────────────────────────────────────────────────────────────────
    # SERVER THREAD
    # ─────────────────────────────────────────────────────────────────────────
    def server():
        """UDP echo server — no connection, just receive and respond."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((host, port))
            s.settimeout(5)
            server_ready.set()
            try:
                for _ in range(messages):
                    data, addr = s.recvfrom(1024)
                    s.sendto(b"ACK:" + data, addr)
            except socket.timeout:
                pass
    
    server_thread = threading.Thread(target=server, daemon=True)
    server_thread.start()
    server_ready.wait(timeout=5)
    
    # ─────────────────────────────────────────────────────────────────────────
    # CLIENT COMMUNICATION
    # ─────────────────────────────────────────────────────────────────────────
    time.sleep(0.5)
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(2)
        for i in range(messages):
            msg = f"Message {i+1}\n".encode()
            s.sendto(msg, (host, port))
            try:
                response, _ = s.recvfrom(1024)
                print(f"Sent: {msg.decode().strip()} | Received: {response.decode().strip()}")
            except socket.timeout:
                print(f"Sent: {msg.decode().strip()} | No response (timeout)")
            time.sleep(0.2)
    
    server_thread.join(timeout=2)


# ═══════════════════════════════════════════════════════════════════════════════
# PACKET_CAPTURE
# ═══════════════════════════════════════════════════════════════════════════════
def start_capture(interface: str, port: int, output: Path, duration: int = 10) -> subprocess.Popen:
    """
    Start tcpdump capture in background.
    
    Args:
        interface: Network interface to capture on (e.g., 'lo', 'eth0')
        port: Port to filter for
        output: Path to write pcap file
        duration: Not used directly — capture stops on max packets
        
    Returns:
        Popen object for the running tcpdump process
    """
    cmd = [
        "tcpdump",
        "-i", interface,
        "-w", str(output),
        f"port {port}",
        "-c", "100"  # Max packets to capture
    ]
    
    print(f"Starting capture: {' '.join(cmd)}")
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# ═══════════════════════════════════════════════════════════════════════════════
# TRAFFIC_ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
def analyse_pcap(pcap_file: Path) -> None:
    """
    Analyse a PCAP file using tshark and display statistics.
    
    Runs multiple tshark commands to extract different views of the
    captured traffic.
    
    Args:
        pcap_file: Path to the pcap file to analyse
    """
    if not pcap_file.exists():
        print(f"Error: File not found: {pcap_file}")
        return
    
    print(f"\n{'='*60}")
    print(f"Analysis of: {pcap_file}")
    print(f"{'='*60}\n")
    
    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 1: Packet Summary
    # ─────────────────────────────────────────────────────────────────────────
    print("1. Packet Summary:")
    result = subprocess.run(
        ["tshark", "-r", str(pcap_file), "-q", "-z", "io,stat,0"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    
    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 2: Protocol Hierarchy
    # ─────────────────────────────────────────────────────────────────────────
    print("\n2. Protocol Hierarchy:")
    result = subprocess.run(
        ["tshark", "-r", str(pcap_file), "-q", "-z", "io,phs"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    
    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 3: Conversations
    # ─────────────────────────────────────────────────────────────────────────
    print("\n3. Conversations:")
    result = subprocess.run(
        ["tshark", "-r", str(pcap_file), "-q", "-z", "conv,tcp"],
        capture_output=True,
        text=True
    )
    if result.stdout.strip():
        print(result.stdout)
    else:
        # Try UDP if no TCP conversations
        result = subprocess.run(
            ["tshark", "-r", str(pcap_file), "-q", "-z", "conv,udp"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
    
    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 4: First 10 Packets
    # ─────────────────────────────────────────────────────────────────────────
    print("\n4. First 10 Packets:")
    result = subprocess.run(
        ["tshark", "-r", str(pcap_file), "-c", "10"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    
    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 5: TCP Flags (if applicable)
    # ─────────────────────────────────────────────────────────────────────────
    print("\n5. TCP Flags (if applicable):")
    result = subprocess.run(
        ["tshark", "-r", str(pcap_file), "-Y", "tcp", "-T", "fields",
         "-e", "frame.number", "-e", "tcp.flags.str"],
        capture_output=True,
        text=True
    )
    if result.stdout.strip():
        print("Frame\tFlags")
        print("-" * 30)
        for line in result.stdout.strip().split("\n")[:15]:
            print(line)
    else:
        print("No TCP packets found")
    
    print(f"\n{'='*60}")
    print("Analysis complete. Use Wireshark for detailed inspection.")
    print(f"{'='*60}\n")


# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGUMENTS
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Protocol Analysis Helper for Homework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate and capture TCP traffic
  python hw_1_02_protocol_analysis.py --mode tcp --output tcp_analysis.pcap
  
  # Generate and capture UDP traffic
  python hw_1_02_protocol_analysis.py --mode udp --output udp_analysis.pcap
  
  # Analyse an existing capture
  python hw_1_02_protocol_analysis.py --analyse tcp_analysis.pcap
  
  # Skip prediction prompt
  python hw_1_02_protocol_analysis.py --mode tcp --output tcp.pcap --no-predict
        """
    )
    parser.add_argument(
        "--mode",
        choices=["tcp", "udp"],
        help="Traffic mode to generate"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output PCAP file"
    )
    parser.add_argument(
        "--analyse", "-a",
        type=Path,
        help="Analyse existing PCAP file"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=9999,
        help="Port to use (default: 9999)"
    )
    parser.add_argument(
        "--interface", "-i",
        default="lo",
        help="Interface to capture on (default: lo)"
    )
    parser.add_argument(
        "--no-predict",
        action="store_true",
        help="Skip the prediction prompt"
    )
    return parser.parse_args()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point for the homework helper."""
    args = parse_args()
    
    # Analysis mode — just analyse existing file
    if args.analyse:
        analyse_pcap(args.analyse)
        return 0
    
    # Generation mode — need mode and output
    if not args.mode or not args.output:
        print("Error: Specify --mode and --output, or use --analyse")
        return 1
    
    print(f"\n{'='*60}")
    print(f"Protocol Analysis Helper - {args.mode.upper()} Mode")
    print(f"{'='*60}\n")
    
    # Prediction prompt
    if not args.no_predict:
        prompt_prediction(args.mode, 5)
    
    # Start capture
    print(f"Starting capture on {args.interface}, port {args.port}...")
    print("(Run with sudo if permission denied)\n")
    
    try:
        capture = start_capture(args.interface, args.port, args.output)
        time.sleep(1)  # Let capture initialise
        
        # Generate traffic
        print(f"\nGenerating {args.mode.upper()} traffic...\n")
        
        if args.mode == "tcp":
            create_tcp_traffic("127.0.0.1", args.port)
        else:
            create_udp_traffic("127.0.0.1", args.port)
        
        # Wait for capture to complete
        time.sleep(2)
        capture.terminate()
        capture.wait(timeout=5)
        
        print(f"\n✅ Capture saved to: {args.output}")
        
        # Analyse the capture
        analyse_pcap(args.output)
        
    except PermissionError:
        print("\n❌ Error: Permission denied. Run with sudo:")
        print(f"  sudo python {__file__} --mode {args.mode} --output {args.output}")
        return 1
    except FileNotFoundError:
        print("\n❌ Error: tcpdump not found. Install it or use Wireshark for capture.")
        return 1
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
