#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
  Exercise 11.01 – Simple HTTP Backend Server
═══════════════════════════════════════════════════════════════════════════════

EDUCATIONAL PURPOSE:
  - Understanding the HTTP request-response model
  - Implementing a minimal HTTP server
  - Observing behaviour from the backend perspective

LEVEL: Beginner
ESTIMATED TIME: 10 minutes

PAIR PROGRAMMING NOTES:
  - Driver: Start backends one by one, verify each responds
  - Navigator: Watch for port conflicts, verify output format
  - Swap after: All three backends are running

FEATURES:
  - Simple HTTP server on configurable port
  - Responds with backend ID (to observe load balancing)
  - Support for delay simulation (for least_conn tests)
  - Minimal logging for debugging

ARCHITECTURE:
  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Client  ──────►  Load Balancer  ──────►  Backend (this server)        │
  │          ◄──────                 ◄──────                               │
  └─────────────────────────────────────────────────────────────────────────┘

USAGE:
  python3 ex_11_01_backend.py --id 1 --port 8081
  python3 ex_11_01_backend.py --id 2 --port 8082
  python3 ex_11_01_backend.py --id 3 --port 8083 --delay 0.5

TESTING:
  curl http://localhost:8081/
  # Response: Backend 1 | Host: hostname | Time: 2025-01-01T12:00:00

PREDICTION PROMPTS:
  💭 Before starting: How many connections can a single backend handle?
  💭 Before testing: What will the response body contain?
  💭 With delay=0.5: How will this affect load balancer behaviour?

═══════════════════════════════════════════════════════════════════════════════
"""
from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import socket
import threading
import time
from datetime import datetime


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def get_hostname() -> str:
    """Get hostname or a fallback."""
    try:
        return socket.gethostname()
    except Exception:
        return "unknown"


def prompt_prediction(question: str) -> None:
    """
    Display a prediction prompt for educational purposes.
    
    Brown & Wilson Principle 4: Students learn better when they
    predict outcomes before seeing results.
    """
    print(f"\n💭 PREDICTION: {question}")
    input("   Press Enter after making your prediction...")


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD_HTTP_RESPONSE
# ═══════════════════════════════════════════════════════════════════════════════

def build_response(backend_id: int, request_count: int) -> bytes:
    """
    Build the HTTP response.
    
    The response format includes:
    - Backend ID (for load balancing verification)
    - Container/machine hostname
    - Current timestamp
    - Processed request number
    
    Args:
        backend_id: Unique identifier for this backend
        request_count: Number of requests processed so far
        
    Returns:
        Complete HTTP response as bytes
    """
    hostname = get_hostname()
    timestamp = datetime.now().isoformat(timespec='seconds')
    
    body = f"Backend {backend_id} | Host: {hostname} | Time: {timestamp} | Request #{request_count}\n"
    body_bytes = body.encode("utf-8")
    
    response = (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: text/plain; charset=utf-8\r\n"
        b"Connection: close\r\n"
        b"X-Backend-ID: " + str(backend_id).encode() + b"\r\n"
        b"X-netENwsl-Week: 11\r\n"
        b"Content-Length: " + str(len(body_bytes)).encode() + b"\r\n"
        b"\r\n"
    ) + body_bytes
    
    return response


# ═══════════════════════════════════════════════════════════════════════════════
# HANDLE_CLIENT_CONNECTION
# ═══════════════════════════════════════════════════════════════════════════════

def handle_client(client_sock: socket.socket, 
                  client_addr: tuple,
                  backend_id: int,
                  delay: float,
                  request_counter: list,
                  verbose: bool) -> None:
    """
    Process an HTTP request from a connected client.
    
    This function runs in a separate thread for each connection,
    allowing the server to handle multiple concurrent requests.
    
    Args:
        client_sock: Client socket connection
        client_addr: Client address tuple (ip, port)
        backend_id: This backend's unique ID
        delay: Artificial delay in seconds (for testing)
        request_counter: Shared counter list (thread-safe via lock)
        verbose: Enable detailed logging
    """
    try:
        # ─── READ_REQUEST ───────────────────────────────────────────────
        request = b""
        client_sock.settimeout(5.0)
        
        while True:
            chunk = client_sock.recv(4096)
            if not chunk:
                break
            request += chunk
            if b"\r\n\r\n" in request:
                break
        
        # ─── UPDATE_COUNTER ─────────────────────────────────────────────
        with threading.Lock():
            request_counter[0] += 1
            count = request_counter[0]
        
        # ─── SIMULATE_PROCESSING_DELAY ──────────────────────────────────
        if delay > 0:
            time.sleep(delay)
        
        # ─── SEND_RESPONSE ──────────────────────────────────────────────
        response = build_response(backend_id, count)
        client_sock.sendall(response)
        
        # ─── LOG_REQUEST ────────────────────────────────────────────────
        if verbose:
            method = request.split(b" ", 1)[0].decode("ascii", errors="replace")
            print(f"[Backend {backend_id}] {client_addr[0]}:{client_addr[1]} - {method} - #{count}")
    
    except Exception as e:
        if verbose:
            print(f"[Backend {backend_id}] Error: {e}")
    
    finally:
        # ─── CLEANUP ────────────────────────────────────────────────────
        try:
            client_sock.close()
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════════════════════════
# RUN_SERVER
# ═══════════════════════════════════════════════════════════════════════════════

def run_server(backend_id: int, 
               host: str, 
               port: int, 
               delay: float,
               verbose: bool) -> None:
    """
    Start the HTTP server and accept connections.
    
    Creates a TCP socket, binds to the specified address,
    and spawns a thread for each incoming connection.
    
    Args:
        backend_id: Unique ID of this backend (shown in responses)
        host: Bind address (0.0.0.0 for all interfaces)
        port: Listening port number
        delay: Artificial delay per request in seconds
        verbose: Enable detailed logging
    """
    request_counter = [0]  # List for thread-safe mutation
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        # ─── CONFIGURE_SOCKET ───────────────────────────────────────────
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((host, port))
        server_sock.listen(128)
        
        # ─── DISPLAY_STARTUP_INFO ───────────────────────────────────────
        print(f"[Backend {backend_id}] Listening on {host}:{port}")
        if delay > 0:
            print(f"[Backend {backend_id}] Delay per request: {delay}s")
        print(f"[Backend {backend_id}] Press Ctrl+C to stop")
        print("")
        
        # ─── ACCEPT_LOOP ────────────────────────────────────────────────
        try:
            while True:
                client_sock, client_addr = server_sock.accept()
                thread = threading.Thread(
                    target=handle_client,
                    args=(client_sock, client_addr, backend_id, delay, request_counter, verbose),
                    daemon=True
                )
                thread.start()
        
        except KeyboardInterrupt:
            # ─── GRACEFUL_SHUTDOWN ──────────────────────────────────────
            print(f"\n[Backend {backend_id}] Shutting down...")
            print(f"[Backend {backend_id}] Total requests served: {request_counter[0]}")


# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGUMENTS
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Parse command-line arguments and start the server."""
    parser = argparse.ArgumentParser(
        description="Simple HTTP backend server for load balancing demonstrations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --id 1 --port 8081
  %(prog)s --id 2 --port 8082 --delay 0.2
  %(prog)s --id 3 --port 8083 -v
        """
    )
    
    parser.add_argument("--id", type=int, default=1,
                        help="Backend ID (default: 1)")
    parser.add_argument("--host", type=str, default="0.0.0.0",
                        help="Bind address (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8081,
                        help="Listening port (default: 8081)")
    parser.add_argument("--delay", type=float, default=0.0,
                        help="Artificial delay per request in seconds (default: 0)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Detailed logging")
    
    args = parser.parse_args()
    
    run_server(
        backend_id=args.id,
        host=args.host,
        port=args.port,
        delay=args.delay,
        verbose=args.verbose
    )


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()
