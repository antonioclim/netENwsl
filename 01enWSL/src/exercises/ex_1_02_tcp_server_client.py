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


# ═══════════════════════════════════════════════════════════════════════════════
# PREDICTION_PROMPTS
# ═══════════════════════════════════════════════════════════════════════════════
def prompt_server_prediction(host: str, port: int) -> None:
    """Ask student to predict server behaviour (Brown & Wilson Principle 4)."""
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
    """Ask student to predict client connection behaviour."""
    print("\n" + "=" * 60)
    print("💭 PREDICTION: CLIENT CONNECTION")
    print("=" * 60)
    print(f"A TCP client will connect to {host}:{port}")
    print()
    print("Predict:")
    print("  1. How many packets are exchanged for the TCP handshake?")
    print("  2. After connection, what state will both sockets show?")
    print("=" * 60)
    input("Press Enter to continue...")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# SERVER_IMPLEMENTATION
# ═══════════════════════════════════════════════════════════════════════════════
def _create_server_socket(host: str, port: int) -> socket.socket:
    """Create and configure a TCP server socket."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(1)
    s.settimeout(0.5)
    return s


def _handle_client_connection(conn: socket.socket) -> None:
    """Receive data and echo back with ACK prefix."""
    with conn:
        data = conn.recv(4096)
        conn.sendall(b"ACK:" + data)


def run_server(host: str, port: int, ready: threading.Event, stop: threading.Event) -> None:
    """
    Run a simple TCP echo server.
    
    Args:
        host: IP address to bind to
        port: Port number to listen on
        ready: Event to signal when server is ready
        stop: Event to signal server should stop
    """
    with _create_server_socket(host, port) as s:
        ready.set()
        while not stop.is_set():
            try:
                conn, _ = s.accept()
                _handle_client_connection(conn)
                break
            except socket.timeout:
                continue


# ═══════════════════════════════════════════════════════════════════════════════
# CLIENT_IMPLEMENTATION
# ═══════════════════════════════════════════════════════════════════════════════
def run_client(host: str, port: int, payload: bytes, timeout_s: float) -> bytes:
    """
    Run a simple TCP client.
    
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
def _print_exchange_header(host: str, port: int, elapsed_ms: float) -> None:
    """Print the results header."""
    print("\n" + "=" * 60)
    print("📊 TCP EXCHANGE RESULTS")
    print("=" * 60)
    print(f"  Server:   {host}:{port}")
    print(f"  RTT:      {elapsed_ms:.2f} ms")


def _verify_echo(request: str, response: str) -> None:
    """Verify the server echoed correctly."""
    if response.startswith("ACK:"):
        print("  ✅ Server acknowledged the message correctly")
        echoed = response[4:]
        if echoed.strip() == request.strip():
            print("  ✅ Echo matches original message")
        else:
            print("  ⚠️  Echo differs from original (check encoding)")
    else:
        print("  ❌ Unexpected response format")


def display_results(host: str, port: int, elapsed_ms: float, 
                    request: str, response: str) -> None:
    """Display the exchange results with interpretation."""
    _print_exchange_header(host, port, elapsed_ms)
    print(f"  Sent:     {request!r}")
    print(f"  Received: {response!r}")
    print()
    _verify_echo(request, response)
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
# MAIN_HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def _start_server_thread(host: str, port: int) -> tuple[threading.Thread, threading.Event, threading.Event]:
    """Start the server in a background thread."""
    ready = threading.Event()
    stop = threading.Event()
    thread = threading.Thread(target=run_server, args=(host, port, ready, stop), daemon=True)
    thread.start()
    return thread, ready, stop


def _wait_for_server(ready: threading.Event, timeout: float = 2.0) -> bool:
    """Wait for server to become ready."""
    return ready.wait(timeout=timeout)


def _run_client_exchange(host: str, port: int, message: str, timeout_s: float) -> tuple[bytes, float]:
    """Execute client exchange and measure time."""
    payload = (message + "\n").encode("utf-8")
    start = time.time()
    response = run_client(host, port, payload, timeout_s)
    elapsed_ms = (time.time() - start) * 1000.0
    return response, elapsed_ms


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    args = parse_args()
    
    if not args.no_predict:
        prompt_server_prediction(args.host, args.port)
    
    print(f"Starting TCP server on {args.host}:{args.port}...")
    thread, ready, stop = _start_server_thread(args.host, args.port)
    
    if not _wait_for_server(ready):
        print("❌ TCP server failed to start")
        return 1
    
    print("✅ Server is listening")
    
    if not args.no_predict:
        prompt_client_prediction(args.host, args.port)
    
    print(f"Connecting client to {args.host}:{args.port}...")
    response, elapsed_ms = _run_client_exchange(args.host, args.port, args.message, args.timeout_s)
    
    stop.set()
    thread.join(timeout=1.0)
    
    response_str = response.decode("utf-8", errors="replace").strip()
    display_results(args.host, args.port, elapsed_ms, args.message, response_str)
    
    # Legacy format for test compatibility
    print(f"\nTCP host={args.host} port={args.port} rtt_ms={elapsed_ms:.2f} response={response_str}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
