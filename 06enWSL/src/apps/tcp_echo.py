#!/usr/bin/env python3
"""
TCP Echo Server/Client for SDN connectivity testing
====================================================
Computer Networks - Week 6 (WSL Environment)
ASE Bucharest | by ing. dr. Antonio Clim

This application demonstrates basic TCP socket programming and is used
to verify SDN flow rules permit or block TCP traffic.

Usage:
    # Server
    python3 tcp_echo.py server --bind 10.0.6.12 --port 9090
    
    # Client
    python3 tcp_echo.py client --dst 10.0.6.12 --port 9090 --message "Hello TCP"

Pair Programming Notes:
    - Driver: Start server, then run client
    - Navigator: Verify echo response matches sent message
    - Swap after: Testing from different hosts
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS_AND_CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

import argparse
import socket
import sys
from typing import NoReturn

DEFAULT_PORT = 9090
BUFFER_SIZE = 1024
CONNECTION_TIMEOUT = 5


# ═══════════════════════════════════════════════════════════════════════════════
# SERVER_IMPLEMENTATION
# ═══════════════════════════════════════════════════════════════════════════════

def run_server(bind_addr: str, port: int) -> NoReturn:
    """
    TCP echo server - returns received messages.
    
    💭 PREDICTION: What happens if you try to bind to an address
    that doesn't belong to this host?
    
    Args:
        bind_addr: IP address to bind to (0.0.0.0 for all interfaces)
        port: Port number to listen on
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        sock.bind((bind_addr, port))
        sock.listen(5)
        
        print(f"[TCP Echo Server]")
        print(f"Listening on {bind_addr}:{port}")
        print("-" * 40)
        
        # 💭 PREDICTION: Will the server see the client's real IP
        # or the NAT-translated IP?
        
        while True:
            client_sock, client_addr = sock.accept()
            print(f"Connection from {client_addr[0]}:{client_addr[1]}")
            
            try:
                while True:
                    data = client_sock.recv(BUFFER_SIZE)
                    if not data:
                        break
                    message = data.decode("utf-8", errors="replace")
                    print(f"  Received: {message.strip()}")
                    client_sock.sendall(data)
            finally:
                client_sock.close()
                print(f"Connection closed.\n")
                
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
    TCP client - sends message and displays response.
    
    💭 PREDICTION: If the SDN switch has no flow rule for this traffic,
    will the connection succeed or fail?
    
    Args:
        dst: Destination IP address
        port: Destination port
        message: Message to send
        
    Returns:
        0 on success, 1 on failure
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(CONNECTION_TIMEOUT)
    
    try:
        print(f"[TCP Echo Client]")
        print(f"Connecting to {dst}:{port}...")
        
        # 💭 PREDICTION: What happens during connect() at the TCP level?
        # (Think: SYN, SYN-ACK, ACK)
        
        sock.connect((dst, port))
        print(f"Connected!")
        
        sock.sendall(message.encode())
        print(f"Sent: {message}")
        
        response = sock.recv(BUFFER_SIZE).decode("utf-8", errors="replace")
        print(f"Received: {response}")
        
        if response.strip() == message.strip():
            print("✓ Echo verified!")
        return 0
        
    except socket.timeout:
        print("✗ Connection timed out!")
        print("  Check: Is the server running? Are SDN flows installed?")
        return 1
    except ConnectionRefusedError:
        print("✗ Connection refused!")
        print("  Check: Is the server listening on this port?")
        return 1
    finally:
        sock.close()


# ═══════════════════════════════════════════════════════════════════════════════
# ARGUMENT_PARSING
# ═══════════════════════════════════════════════════════════════════════════════

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="TCP Echo Server/Client")
    subparsers = parser.add_subparsers(dest="mode")
    
    srv = subparsers.add_parser("server")
    srv.add_argument("--bind", default="0.0.0.0")
    srv.add_argument("--port", type=int, default=DEFAULT_PORT)
    
    cli = subparsers.add_parser("client")
    cli.add_argument("--dst", required=True)
    cli.add_argument("--port", type=int, default=DEFAULT_PORT)
    cli.add_argument("--message", default="Hello TCP")
    
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
        print("Usage: python tcp_echo.py {server|client} [options]")
        print("  server: Start TCP echo server")
        print("  client: Connect to TCP echo server")
        return 1


if __name__ == "__main__":
    sys.exit(main())
