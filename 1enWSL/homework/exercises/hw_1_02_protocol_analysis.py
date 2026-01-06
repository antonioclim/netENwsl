#!/usr/bin/env python3
"""
Homework 1.02: Protocol Analysis Helper
NETWORKING class - ASE, Informatics | by Revolvix

This starter script helps you capture and analyse TCP/UDP traffic.
Complete the exercises and use this to generate your analysis.

Usage:
    python hw_1_02_protocol_analysis.py --mode tcp --output tcp_analysis.pcap
    python hw_1_02_protocol_analysis.py --mode udp --output udp_analysis.pcap
    python hw_1_02_protocol_analysis.py --analyse tcp_analysis.pcap
"""

from __future__ import annotations

import argparse
import subprocess
import socket
import threading
import time
from pathlib import Path
from typing import Optional


def create_tcp_traffic(host: str, port: int, messages: int = 5) -> None:
    """Generate TCP traffic for capture."""
    
    # Start server in background
    server_ready = threading.Event()
    
    def server():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            s.listen(1)
            server_ready.set()
            conn, addr = s.accept()
            with conn:
                for _ in range(messages):
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(b"ACK:" + data)
    
    server_thread = threading.Thread(target=server, daemon=True)
    server_thread.start()
    server_ready.wait(timeout=5)
    
    # Client sends messages
    time.sleep(0.5)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        for i in range(messages):
            msg = f"Message {i+1}\n".encode()
            s.sendall(msg)
            response = s.recv(1024)
            print(f"Sent: {msg.decode().strip()} | Received: {response.decode().strip()}")
            time.sleep(0.2)
    
    server_thread.join(timeout=2)


def create_udp_traffic(host: str, port: int, messages: int = 5) -> None:
    """Generate UDP traffic for capture."""
    
    # Start server in background
    server_ready = threading.Event()
    
    def server():
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
    
    # Client sends messages
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


def start_capture(interface: str, port: int, output: Path, duration: int = 10) -> subprocess.Popen:
    """Start tcpdump capture in background."""
    cmd = [
        "tcpdump",
        "-i", interface,
        "-w", str(output),
        f"port {port}",
        "-c", "100"  # Max packets
    ]
    
    print(f"Starting capture: {' '.join(cmd)}")
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def analyse_pcap(pcap_file: Path) -> None:
    """Analyse a PCAP file and display statistics."""
    
    if not pcap_file.exists():
        print(f"Error: File not found: {pcap_file}")
        return
    
    print(f"\n{'='*60}")
    print(f"Analysis of: {pcap_file}")
    print(f"{'='*60}\n")
    
    # Basic packet count
    print("1. Packet Summary:")
    result = subprocess.run(
        ["tshark", "-r", str(pcap_file), "-q", "-z", "io,stat,0"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    
    # Protocol breakdown
    print("\n2. Protocol Hierarchy:")
    result = subprocess.run(
        ["tshark", "-r", str(pcap_file), "-q", "-z", "io,phs"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    
    # TCP conversation (if applicable)
    print("\n3. Conversations:")
    result = subprocess.run(
        ["tshark", "-r", str(pcap_file), "-q", "-z", "conv,tcp"],
        capture_output=True,
        text=True
    )
    if result.stdout.strip():
        print(result.stdout)
    else:
        result = subprocess.run(
            ["tshark", "-r", str(pcap_file), "-q", "-z", "conv,udp"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
    
    # First 10 packets
    print("\n4. First 10 Packets:")
    result = subprocess.run(
        ["tshark", "-r", str(pcap_file), "-c", "10"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    
    # TCP flags (if TCP)
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


def main() -> int:
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
    args = parser.parse_args()
    
    if args.analyse:
        analyse_pcap(args.analyse)
        return 0
    
    if not args.mode or not args.output:
        parser.print_help()
        return 1
    
    print(f"\n{'='*60}")
    print(f"Protocol Analysis Helper - {args.mode.upper()} Mode")
    print(f"{'='*60}\n")
    
    # Start capture
    print(f"Starting capture on {args.interface}, port {args.port}...")
    print("(Run with sudo if permission denied)\n")
    
    try:
        capture = start_capture(args.interface, args.port, args.output)
        time.sleep(1)  # Let capture start
        
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
        
        print(f"\nCapture saved to: {args.output}")
        
        # Analyse the capture
        analyse_pcap(args.output)
        
    except PermissionError:
        print("\nError: Permission denied. Run with sudo:")
        print(f"  sudo python {__file__} --mode {args.mode} --output {args.output}")
        return 1
    except FileNotFoundError:
        print("\nError: tcpdump not found. Install it or use Wireshark for capture.")
        return 1
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
