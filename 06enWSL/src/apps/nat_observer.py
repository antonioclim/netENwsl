#!/usr/bin/env python3
"""
NAT Observer — Application for observing NAT/PAT translation
=============================================================
Computer Networks - Week 6 (WSL Environment)
ASE Bucharest | by ing. dr. Antonio Clim

This application demonstrates how a "public" server sees connections
from behind a NAT. All connections from private hosts appear
as coming from the NAT router's public IP, differentiated by ports.

Educational purpose:
- Visualise PAT (Port Address Translation) in action
- Understand that private addresses are never visible externally
- Observe how the NAT router allocates unique source ports

Usage:
    # On server (h3 - in the public network)
    python3 nat_observer.py server --bind 203.0.113.2 --port 5000
    
    # On clients (h1, h2 - in the private network)
    python3 nat_observer.py client --host 203.0.113.2 --port 5000 --msg "Hello from h1"

What we observe:
- The server sees all connections as coming from 203.0.113.1 (the NAT IP)
- Each connection has a different source port (the essence of PAT)
- Private addresses (192.168.1.x) are not visible from outside

💭 PREDICTION: What source IP will the server see when h1 connects?
"""

from __future__ import annotations

import argparse
import socket
import sys
from datetime import datetime
from typing import Tuple, NoReturn


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION_CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

DEFAULT_PORT = 5000
DEFAULT_BIND = "0.0.0.0"
BUFFER_SIZE = 1024
CONNECTION_TIMEOUT = 10
LISTEN_BACKLOG = 5


# ═══════════════════════════════════════════════════════════════════════════════
# SERVER_MODE
# ═══════════════════════════════════════════════════════════════════════════════

def run_server(bind_addr: str, port: int) -> NoReturn:
    """
    Start a TCP server that displays source IP:port for each connection.
    
    Args:
        bind_addr: Address to bind to (e.g., "0.0.0.0" for all interfaces)
        port: Port number to listen on
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        sock.bind((bind_addr, port))
        sock.listen(LISTEN_BACKLOG)
        
        print(f"[NAT Observer Server]")
        print(f"Listening on {bind_addr}:{port}")
        print(f"Waiting for connections...")
        print("-" * 60)
        
        while True:
            client_sock, client_addr = sock.accept()
            handle_client_connection(client_sock, client_addr)
                
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        sock.close()
    
    sys.exit(0)


def handle_client_connection(
    client_sock: socket.socket, 
    client_addr: Tuple[str, int]
) -> None:
    """Handle a single client connection."""
    client_ip, client_port = client_addr
    
    try:
        data = client_sock.recv(BUFFER_SIZE)
        message = data.decode("utf-8", errors="replace").strip()
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Connection from {client_ip}:{client_port}")
        print(f"            Message: {message}")
        print()
        
        response = f"Received from {client_ip}:{client_port}\n"
        client_sock.sendall(response.encode())
        
    finally:
        client_sock.close()


# ═══════════════════════════════════════════════════════════════════════════════
# CLIENT_MODE
# ═══════════════════════════════════════════════════════════════════════════════

def run_client(host: str, port: int, message: str) -> int:
    """
    Connect to server and send a message.
    
    Args:
        host: Server address to connect to
        port: Server port
        message: Message to send
    
    Returns:
        0 on success, 1 on failure
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(CONNECTION_TIMEOUT)
    
    try:
        print(f"[NAT Observer Client]")
        print(f"Connecting to {host}:{port}...")
        
        sock.connect((host, port))
        
        local_addr = sock.getsockname()
        print(f"Local address: {local_addr[0]}:{local_addr[1]}")
        
        sock.sendall(message.encode())
        print(f"Sent: {message}")
        
        response = sock.recv(BUFFER_SIZE).decode("utf-8", errors="replace")
        print(f"Server response: {response}")
        
        return 0
        
    except socket.timeout:
        print("Connection timed out!")
        return 1
    except ConnectionRefusedError:
        print("Connection refused! Is the server running?")
        return 1
    finally:
        sock.close()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="NAT Observer - PAT translation demonstration"
    )
    
    subparsers = parser.add_subparsers(dest="mode", help="Operating mode")
    
    server_parser = subparsers.add_parser("server", help="Start the server")
    server_parser.add_argument("--bind", default=DEFAULT_BIND)
    server_parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    
    client_parser = subparsers.add_parser("client", help="Start the client")
    client_parser.add_argument("--host", required=True)
    client_parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    client_parser.add_argument("--msg", "--message", default="Hello from NAT client")
    
    args = parser.parse_args()
    
    if args.mode == "server":
        run_server(args.bind, args.port)
        return 0
    elif args.mode == "client":
        return run_client(args.host, args.port, args.msg)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
