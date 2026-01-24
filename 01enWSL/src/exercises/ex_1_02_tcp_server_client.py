#!/usr/bin/env python3
"""
Exercise 1.02: Local TCP Server and Client
==========================================
Computer Networks - Week 1 (WSL Environment)
ASE Bucharest | by ing. dr. Antonio Clim

Objectives:
- Explain how TCP sockets work (bind, listen, accept, connect)
- Demonstrate bidirectional communication over TCP
- Analyse the client-server exchange pattern

Prerequisites:
- Python 3.11+ with socket module
- Port 9090 available (or specify different port)

Level: Beginner
Estimated time: 15 minutes

Pair Programming Notes:
- Driver: Implement the server socket setup
- Navigator: Predict what socket states will be visible in ss output
- Swap after: Server is listening, before client connects

The demo runs the server and client in the same process using a background thread
to keep execution deterministic for automated validation.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import socket
import sys
import threading
import time
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════════
# PREDICTION_PROMPTS
# ═══════════════════════════════════════════════════════════════════════════════
def prompt_server_prediction(host: str, port: int) -> None:
    """
    Ask student to predict server behaviour (Brown & Wilson Principle 4).
    """
    print("\n" + "=" * 60)
    print("💭 PREDICTION: SERVER SETUP")
    print("=" * 60)
    print(f"A TCP server will bind to {host}:{port}")
    print()
    print("Predict:")
    print("  1. What socket state will ss show after bind() and listen()?")
    print("     (LISTEN / ESTABLISHED / SYN_SENT)")
    print("  2. Can two servers bind to the same port simultaneously?")
    print("     (yes / no)")
    print("=" * 60)
    input("Press Enter to continue...")
    print()


def prompt_client_prediction(host: str, port: int) -> None:
    """
    Ask student to predict client connection behaviour.
    """
    print("\n" + "=" * 60)
    print("💭 PREDICTION: CLIENT CONNECTION")
    print("=" * 60)
    print(f"A TCP client will connect to {host}:{port}")
    print()
    print("Predict:")
    print("  1. How many packets are exchanged for the TCP handshake?")
    print("     (1 / 2 / 3 / 4)")
    print("  2. After connection, what state will both sockets show?")
    print("     (LISTEN / ESTABLISHED / TIME_WAIT)")
    print("=" * 60)
    input("Press Enter to continue...")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# SERVER_IMPLEMENTATION
# ═══════════════════════════════════════════════════════════════════════════════
def run_server(host: str, port: int, ready: threading.Event, stop: threading.Event) -> None:
    """
    Run a simple TCP echo server.
    
    The server:
    1. Binds to the specified address and port
    2. Listens for incoming connections
    3. Accepts one connection
    4. Receives data and echoes it back with "ACK:" prefix
    5. Closes the connection
    
    Args:
        host: IP address to bind to
        port: Port number to listen on
        ready: Event to signal when server is ready
        stop: Event to signal server should stop
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Allow address reuse (avoids "Address already in use" errors)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind to address and start listening
        s.bind((host, port))
        s.listen(1)  # backlog of 1 connection
        ready.set()  # Signal that server is ready
        
        # Set timeout to allow periodic stop checks
        s.settimeout(0.5)
        
        while not stop.is_set():
            try:
                conn, client_addr = s.accept()
            except socket.timeout:
                continue
            
            with conn:
                # Receive data from client
                data = conn.recv(4096)
                # Echo back with acknowledgement prefix
                conn.sendall(b"ACK:" + data)
                break  # Handle one connection then exit


# ═══════════════════════════════════════════════════════════════════════════════
# CLIENT_IMPLEMENTATION
# ═══════════════════════════════════════════════════════════════════════════════
def run_client(host: str, port: int, payload: bytes, timeout_s: float) -> bytes:
    """
    Run a simple TCP client.
    
    The client:
    1. Connects to the server (three-way handshake happens here)
    2. Sends the payload
    3. Receives the response
    4. Closes the connection
    
    Args:
        host: Server IP address
        port: Server port number
        payload: Data to send
        timeout_s: Connection timeout in seconds
        
    Returns:
        Response received from server
    """
    with socket.create_connection((host, port), timeout=timeout_s) as c:
        c.sendall(payload)
        return c.recv(4096)


# ═══════════════════════════════════════════════════════════════════════════════
# OUTPUT_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def display_results(host: str, port: int, elapsed_ms: float, 
                    request: str, response: str) -> None:
    """
    Display the exchange results with interpretation.
    """
    print("\n" + "=" * 60)
    print("📊 TCP EXCHANGE RESULTS")
    print("=" * 60)
    print(f"  Server:   {host}:{port}")
    print(f"  RTT:      {elapsed_ms:.2f} ms")
    print(f"  Sent:     {request!r}")
    print(f"  Received: {response!r}")
    print()
    
    # Verify echo behaviour
    if response.startswith("ACK:"):
        print("  ✅ Server acknowledged the message correctly")
        echoed = response[4:]  # Remove "ACK:" prefix
        if echoed.strip() == request.strip():
            print("  ✅ Echo matches original message")
        else:
            print("  ⚠️  Echo differs from original (check encoding)")
    else:
        print("  ❌ Unexpected response format")
    
    print()
    print("💡 To see socket states during exchange, run in another terminal:")
    print(f"   ss -tn | grep {port}")
    print("=" * 60)


# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGUMENTS
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    ap = argparse.ArgumentParser(
        description="Run a deterministic local TCP server and client exchange.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 ex_1_02_tcp_server_client.py --port 9095
  python3 ex_1_02_tcp_server_client.py --message "Hello, TCP!"
  python3 ex_1_02_tcp_server_client.py --no-predict
        """
    )
    ap.add_argument("--host", default="127.0.0.1", 
                    help="Bind and connect host (default: 127.0.0.1)")
    ap.add_argument("--port", type=int, default=9090, 
                    help="TCP port to use (default: 9090)")
    ap.add_argument("--message", default="hello", 
                    help="Payload message (default: hello)")
    ap.add_argument("--timeout-s", type=float, default=2.0, 
                    help="Client connection timeout in seconds (default: 2.0)")
    ap.add_argument("--no-predict", action="store_true",
                    help="Skip prediction prompts")
    return ap.parse_args()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """
    Main entry point.
    
    Orchestrates the server/client exchange:
    1. Start server in background thread
    2. Wait for server to be ready
    3. Connect client and exchange data
    4. Stop server and display results
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    args = parse_args()
    
    # Prediction prompts (pedagogical feature)
    if not args.no_predict:
        prompt_server_prediction(args.host, args.port)
    
    # Thread synchronisation events
    ready = threading.Event()
    stop = threading.Event()
    
    # Start server in background
    print(f"Starting TCP server on {args.host}:{args.port}...")
    server_thread = threading.Thread(
        target=run_server, 
        args=(args.host, args.port, ready, stop), 
        daemon=True
    )
    server_thread.start()
    
    # Wait for server to be ready
    if not ready.wait(timeout=2.0):
        print("❌ TCP server failed to start")
        return 1
    
    print("✅ Server is listening")
    
    # Client prediction
    if not args.no_predict:
        prompt_client_prediction(args.host, args.port)
    
    # Connect and exchange
    print(f"Connecting client to {args.host}:{args.port}...")
    payload = (args.message + "\n").encode("utf-8")
    
    start = time.time()
    response = run_client(args.host, args.port, payload, args.timeout_s)
    elapsed_ms = (time.time() - start) * 1000.0
    
    # Cleanup
    stop.set()
    server_thread.join(timeout=1.0)
    
    # Display results
    display_results(
        args.host, 
        args.port, 
        elapsed_ms,
        args.message,
        response.decode("utf-8", errors="replace").strip()
    )
    
    # Legacy format for test compatibility
    print(f"\nTCP host={args.host} port={args.port} rtt_ms={elapsed_ms:.2f} response={response.decode('utf-8', errors='replace').strip()}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
