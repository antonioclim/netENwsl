#!/usr/bin/env python3
"""
UDP Echo Server/Client for SDN connectivity testing
====================================================
Computer Networks - Week 6 (WSL Environment)
ASE Bucharest | by ing. dr. Antonio Clim

This application demonstrates basic UDP socket programming and is used
to verify SDN flow rules permit or block UDP traffic.

Usage:
    # Server
    python3 udp_echo.py server --bind 10.0.6.12 --port 9091
    
    # Client
    python3 udp_echo.py client --dst 10.0.6.12 --port 9091 --message "Hello UDP"

Pair Programming Notes:
    - Driver: Start server, then run client
    - Navigator: Note that UDP has no connection establishment
    - Swap after: Comparing UDP vs TCP behaviour
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS_AND_CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

import argparse
import socket
import sys
from typing import NoReturn

DEFAULT_PORT = 9091
BUFFER_SIZE = 1024
CONNECTION_TIMEOUT = 5


# ═══════════════════════════════════════════════════════════════════════════════
# SERVER_IMPLEMENTATION
# ═══════════════════════════════════════════════════════════════════════════════

def run_server(bind_addr: str, port: int) -> NoReturn:
    """
    UDP echo server - returns received datagrams.
    
    💭 PREDICTION: Unlike TCP, UDP has no accept(). Why?
    What does this mean for connection tracking in NAT?
    
    Args:
        bind_addr: IP address to bind to (0.0.0.0 for all interfaces)
        port: Port number to listen on
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        sock.bind((bind_addr, port))
        
        print(f"[UDP Echo Server]")
        print(f"Listening on {bind_addr}:{port}")
        print("-" * 40)
        
        # 💭 PREDICTION: Will each datagram show the same or different
        # source ports for the same client?
        
        while True:
            data, client_addr = sock.recvfrom(BUFFER_SIZE)
            message = data.decode("utf-8", errors="replace")
            print(f"Received from {client_addr[0]}:{client_addr[1]}: {message.strip()}")
            sock.sendto(data, client_addr)
                
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        sock.close()
    sys.exit(0)


# ═══════════════════════════════════════════════════════════════════════════════
# CLIENT_IMPLEMENTATION
# ═══════════════════════════════════════════════════════════════════════════════

def run_client(dst: str, port: int, message: str) -> int:
    """
    UDP client - sends datagram and displays response.
    
    💭 PREDICTION: If the server is not running, what happens?
    (Compare with TCP: connection refused vs ???)
    
    Args:
        dst: Destination IP address
        port: Destination port
        message: Message to send
        
    Returns:
        0 on success, 1 on failure
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(CONNECTION_TIMEOUT)
    
    try:
        print(f"[UDP Echo Client]")
        print(f"Sending to {dst}:{port}...")
        
        # 💭 PREDICTION: Does sendto() guarantee delivery?
        # What if the datagram is lost?
        
        sock.sendto(message.encode(), (dst, port))
        print(f"Sent: {message}")
        
        response, _ = sock.recvfrom(BUFFER_SIZE)
        response_str = response.decode("utf-8", errors="replace")
        print(f"Received: {response_str}")
        
        if response_str.strip() == message.strip():
            print("✓ Echo verified!")
        return 0
        
    except socket.timeout:
        print("✗ No response (timeout)!")
        print("  Check: Is the server running? Was the datagram dropped?")
        print("  Note: UDP has no 'connection refused' - just silence.")
        return 1
    finally:
        sock.close()


# ═══════════════════════════════════════════════════════════════════════════════
# ARGUMENT_PARSING
# ═══════════════════════════════════════════════════════════════════════════════

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="UDP Echo Server/Client")
    subparsers = parser.add_subparsers(dest="mode")
    
    srv = subparsers.add_parser("server")
    srv.add_argument("--bind", default="0.0.0.0")
    srv.add_argument("--port", type=int, default=DEFAULT_PORT)
    
    cli = subparsers.add_parser("client")
    cli.add_argument("--dst", required=True)
    cli.add_argument("--port", type=int, default=DEFAULT_PORT)
    cli.add_argument("--message", default="Hello UDP")
    
    return parser.parse_args()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point."""
    args = parse_arguments()
    
    if args.mode == "server":
        run_server(args.bind, args.port)
        return 0
    elif args.mode == "client":
        return run_client(args.dst, args.port, args.message)
    else:
        print("Usage: python udp_echo.py {server|client} [options]")
        print("  server: Start UDP echo server")
        print("  client: Send datagram to UDP echo server")
        return 1


if __name__ == "__main__":
    sys.exit(main())
