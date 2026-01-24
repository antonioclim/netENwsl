#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  Exercise 3: TCP Tunnel (Port Forwarder)                                     ║
║  Week 3 — Computer Networks                                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

LEARNING OBJECTIVES:
    - Understanding the TCP proxy/tunnel concept
    - Bidirectional forwarding between two TCP connections
    - Using threads for full-duplex communication
    - Practical applications: NAT traversal, load balancing, debugging

ARCHITECTURE:
    ┌──────────┐     ┌──────────────────────────────┐     ┌──────────┐
    │  Client  │────►│         TUNNEL               │────►│  Server  │
    │          │     │  accept() ─► connect(target) │     │          │
    │          │◄────│  ◄── forward bidirectional ──►│◄────│          │
    └──────────┘     └──────────────────────────────┘     └──────────┘
    
    Client connects to tunnel (e.g., router:9090)
    Tunnel opens connection to target server (e.g., server:8080)
    Tunnel copies data in both directions

FORWARDING PATTERN:
    Thread 1: client_socket → target_socket
    Thread 2: target_socket → client_socket
    
    Both threads run in parallel for full-duplex communication.

PRACTICAL USES:
    1. NAT traversal: expose a service from a private network
    2. Simple load balancing: distribute connections
    3. Debugging: intercept and analyse traffic
    4. Protocol translation: adapt between protocols

PAIR PROGRAMMING:
    Driver: Examines tunnel code and tests connections
    Navigator: Monitors ss -tn output and Wireshark captures
    Swap after: Testing direct connection, then after tunnel test

USAGE (in Docker topology):
    # Echo server on week3_server:
    python3 echo_server.py --listen 0.0.0.0:8080

    # Tunnel on week3_router:
    python3 ex_3_03_tcp_tunnel.py --listen 0.0.0.0:9090 --target server:8080

    # Client from week3_client:
    echo "hello" | nc router 9090
"""
from __future__ import annotations

import argparse
import socket
import sys
import threading
from datetime import datetime
from typing import Tuple


# ════════════════════════════════════════════════════════════════════════════
#  CONSTANTS
# ════════════════════════════════════════════════════════════════════════════

BUFFER_SIZE = 4096
DEFAULT_LISTEN = "0.0.0.0:9090"
DEFAULT_TARGET = "127.0.0.1:8080"


# ════════════════════════════════════════════════════════════════════════════
#  UTILITY FUNCTIONS
# ════════════════════════════════════════════════════════════════════════════

def timestamp() -> str:
    """Return current timestamp in HH:MM:SS.mmm format."""
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


def log(level: str, tunnel_id: str, message: str) -> None:
    """Display a log message with timestamp, level and tunnel ID."""
    print(f"[{timestamp()}] [{level}] [{tunnel_id}] {message}")


def parse_addr(addr_str: str) -> Tuple[str, int]:
    """
    Parse 'host:port' string into (host, port) tuple.
    
    Args:
        addr_str: Address string in 'host:port' format
        
    Returns:
        Tuple of (host, port)
        
    Raises:
        ValueError: If format is invalid
    """
    if ":" not in addr_str:
        raise ValueError(f"Invalid format: {addr_str}. Use 'host:port'.")
    host, port_str = addr_str.rsplit(":", 1)
    return host, int(port_str)


def prompt_prediction(question: str) -> str:
    """
    Ask student to predict outcome before execution.
    
    This implements Brown & Wilson Principle 4: Predictions.
    
    Args:
        question: The prediction question to ask
        
    Returns:
        The student's prediction as a string
    """
    print(f"\n💭 PREDICTION: {question}")
    prediction = input("Your answer: ")
    return prediction


# ════════════════════════════════════════════════════════════════════════════
#  UNIDIRECTIONAL FORWARDING
# ════════════════════════════════════════════════════════════════════════════

def forward_stream(
    src: socket.socket,
    dst: socket.socket,
    direction: str,
    tunnel_id: str,
    on_close: threading.Event
) -> None:
    """
    Copy data from src to dst until the connection closes.
    
    This is the fundamental pattern for proxy/tunnel:
    - Read chunks from src
    - Write them to dst
    - Stop when src returns 0 bytes (connection closed)
    
    Args:
        src: Source socket (to read from)
        dst: Destination socket (to write to)
        direction: Descriptive string (e.g., "client→target")
        tunnel_id: ID for logging
        on_close: Event to signal the other thread to stop
    """
    total_bytes = 0
    
    try:
        while not on_close.is_set():
            # Read data from source
            data = src.recv(BUFFER_SIZE)
            
            if not data:
                # 0 bytes = peer has closed the connection
                log("INFO", tunnel_id, f"{direction}: Connection closed by peer")
                break
            
            # Write data to destination
            dst.sendall(data)
            total_bytes += len(data)
            
            # Detailed logging (can be commented out for production)
            preview = data[:50].decode("utf-8", errors="replace")
            if len(data) > 50:
                preview += "..."
            log("DATA", tunnel_id, f"{direction}: {len(data)} bytes: {preview!r}")
            
    except ConnectionResetError:
        log("WARN", tunnel_id, f"{direction}: Connection reset by peer")
    except BrokenPipeError:
        log("WARN", tunnel_id, f"{direction}: Broken pipe (peer closed)")
    except OSError as e:
        if not on_close.is_set():
            log("ERROR", tunnel_id, f"{direction}: {e}")
    finally:
        # Signal the other thread to stop
        on_close.set()
        log("INFO", tunnel_id, f"{direction}: Forwarding stopped. Total: {total_bytes} bytes")


# ════════════════════════════════════════════════════════════════════════════
#  CLIENT CONNECTION HANDLER
# ════════════════════════════════════════════════════════════════════════════

def handle_client(
    client_socket: socket.socket,
    client_addr: Tuple[str, int],
    target_host: str,
    target_port: int,
    tunnel_id: str
) -> None:
    """
    Handle a client connection: open connection to target,
    start bidirectional forwarding.
    
    Steps:
    1. Open TCP connection to target server
    2. Start 2 threads for forwarding (client↔target)
    3. Wait for both directions to complete
    4. Close both connections
    
    Args:
        client_socket: Socket connected to client
        client_addr: Client's (ip, port) tuple
        target_host: Target server hostname/IP
        target_port: Target server port
        tunnel_id: ID for logging
    """
    log("INFO", tunnel_id, f"Client connected from {client_addr[0]}:{client_addr[1]}")
    
    target_socket = None
    
    try:
        # ─────────────────────────────────────────────────────────────────────
        # Step 1: Connect to target server
        # ─────────────────────────────────────────────────────────────────────
        target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target_socket.settimeout(10.0)  # Timeout for connect
        
        log("INFO", tunnel_id, f"Connecting to target {target_host}:{target_port}...")
        target_socket.connect((target_host, target_port))
        target_socket.settimeout(None)  # Disable timeout for transfer
        
        log("INFO", tunnel_id, f"Connection established with target {target_host}:{target_port}")
        
        # ─────────────────────────────────────────────────────────────────────
        # Step 2: Event for synchronisation between threads
        # ─────────────────────────────────────────────────────────────────────
        close_event = threading.Event()
        
        # ─────────────────────────────────────────────────────────────────────
        # Step 3: Start threads for bidirectional forwarding
        # ─────────────────────────────────────────────────────────────────────
        thread_client_to_target = threading.Thread(
            target=forward_stream,
            args=(client_socket, target_socket, "client→target", tunnel_id, close_event),
            daemon=True
        )
        
        thread_target_to_client = threading.Thread(
            target=forward_stream,
            args=(target_socket, client_socket, "target→client", tunnel_id, close_event),
            daemon=True
        )
        
        thread_client_to_target.start()
        thread_target_to_client.start()
        
        # ─────────────────────────────────────────────────────────────────────
        # Step 4: Wait for both threads to complete
        # ─────────────────────────────────────────────────────────────────────
        thread_client_to_target.join()
        thread_target_to_client.join()
        
    except ConnectionRefusedError:
        log("ERROR", tunnel_id, f"Target {target_host}:{target_port} refused connection")
    except socket.timeout:
        log("ERROR", tunnel_id, f"Timeout connecting to {target_host}:{target_port}")
    except OSError as e:
        log("ERROR", tunnel_id, f"Error: {e}")
    finally:
        # ─────────────────────────────────────────────────────────────────────
        # Step 5: Cleanup - close both sockets
        # ─────────────────────────────────────────────────────────────────────
        try:
            client_socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        client_socket.close()
        
        if target_socket:
            try:
                target_socket.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            target_socket.close()
        
        log("INFO", tunnel_id, "Tunnel closed")


# ════════════════════════════════════════════════════════════════════════════
#  MAIN SERVER (ACCEPT LOOP)
# ════════════════════════════════════════════════════════════════════════════

def run_tunnel(
    listen_host: str,
    listen_port: int,
    target_host: str,
    target_port: int,
    show_prediction: bool = True
) -> int:
    """
    Start the tunnel server that accepts connections and redirects them.
    
    For each client:
    1. Accept connection
    2. Start thread for handle_client
    3. Continue accepting other connections
    
    Args:
        listen_host: Host to listen on
        listen_port: Port to listen on
        target_host: Target server host
        target_port: Target server port
        show_prediction: Whether to show prediction prompts
        
    Returns:
        0 for success, 1 for error
    """
    # ─────────────────────────────────────────────────────────────────────────
    # PREDICTION CHECKPOINT
    # ─────────────────────────────────────────────────────────────────────────
    if show_prediction:
        prompt_prediction(
            "When a client connects through this tunnel, how many TCP connections will exist in total?"
        )
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((listen_host, listen_port))
        server_socket.listen(10)  # Backlog of 10 pending connections
        
        print(f"╔══════════════════════════════════════════════════════════════╗")
        print(f"║  TCP Tunnel active                                           ║")
        print(f"║  Listen: {listen_host}:{listen_port:<43}║")
        print(f"║  Target: {target_host}:{target_port:<43}║")
        print(f"╚══════════════════════════════════════════════════════════════╝")
        print(f"[{timestamp()}] [INFO] Waiting for connections... (Ctrl+C to stop)")
        
        tunnel_counter = 0
        
        while True:
            try:
                client_socket, client_addr = server_socket.accept()
                tunnel_counter += 1
                tunnel_id = f"T{tunnel_counter:04d}"
                
                # Start thread for this client
                client_thread = threading.Thread(
                    target=handle_client,
                    args=(client_socket, client_addr, target_host, target_port, tunnel_id),
                    daemon=True
                )
                client_thread.start()
                
            except OSError as e:
                log("ERROR", "MAIN", f"Accept error: {e}")
                break
                
    except KeyboardInterrupt:
        print(f"\n[{timestamp()}] [INFO] Stopping server (Ctrl+C)")
    except OSError as e:
        print(f"[{timestamp()}] [ERROR] Cannot bind on {listen_host}:{listen_port}: {e}")
        return 1
    finally:
        server_socket.close()
        print(f"[{timestamp()}] [INFO] Server socket closed")
    
    return 0


# ════════════════════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════════════════════

def main(argv: list[str] | None = None) -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="ex_3_03_tcp_tunnel.py",
        description="TCP Tunnel (Port Forwarder) for redirecting traffic.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Tunnel from localhost:9090 to server:8080
  python3 ex_3_03_tcp_tunnel.py --listen 0.0.0.0:9090 --target server:8080

  # Test with netcat
  echo "hello" | nc localhost 9090

Typical Docker topology:
  client ──► router:9090 (tunnel) ──► server:8080 (echo server)
        """
    )
    
    parser.add_argument(
        "--listen", default=DEFAULT_LISTEN,
        help=f"Listen address (host:port), default: {DEFAULT_LISTEN}"
    )
    parser.add_argument(
        "--target", default=DEFAULT_TARGET,
        help=f"Target server address (host:port), default: {DEFAULT_TARGET}"
    )
    parser.add_argument(
        "--no-predict", action="store_true",
        help="Skip prediction prompts (for automated testing)"
    )
    
    args = parser.parse_args(argv)
    
    try:
        listen_host, listen_port = parse_addr(args.listen)
        target_host, target_port = parse_addr(args.target)
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    
    return run_tunnel(listen_host, listen_port, target_host, target_port, not args.no_predict)


if __name__ == "__main__":
    sys.exit(main())
