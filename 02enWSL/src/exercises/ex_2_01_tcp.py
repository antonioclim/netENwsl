#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
 Week 2 – Exercise 1: Concurrent TCP Server and Client
═══════════════════════════════════════════════════════════════════════════════

 LEARNING OBJECTIVES:
 ────────────────────
 1. Understand sockets for TCP (SOCK_STREAM)
 2. Compare iterative server vs concurrent server (threading)
 3. Correlate TCP handshake (SYN-SYN/ACK-ACK) with application code
 4. Observe encapsulation: data → TCP segment → IP packet

 APPLICATION PROTOCOL:
 ─────────────────────
 Request:  <text message> (bytes)
 Response: b"OK: " + upper(message)

 USAGE:
   Server:  python ex_2_01_tcp.py server --port 9090
   Client:  python ex_2_01_tcp.py client --host 127.0.0.1 --port 9090 -m "test"
   Load:    python ex_2_01_tcp.py load --host 127.0.0.1 --port 9090 --clients 10

 NOTE: Students often forget SO_REUSEADDR and get stuck on
 "Address already in use" for several minutes. This is normal.

 NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim
═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import argparse
import socket
import sys
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
DEFAULT_PORT = 9090
DEFAULT_BIND = "0.0.0.0"
DEFAULT_BACKLOG = 32
DEFAULT_RECV_BUF = 1024
DEFAULT_TIMEOUT = 5.0


# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════
def timestamp() -> str:
    """Return current timestamp for logging."""
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


def log(tag: str, msg: str) -> None:
    """Log message with timestamp and tag."""
    print(f"[{timestamp()}][{tag:8s}] {msg}", flush=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PREDICTION PROMPTS (Brown & Wilson Principle 4)
# ═══════════════════════════════════════════════════════════════════════════════
def prompt_prediction(question: str, hint: str = "") -> None:
    """
    Display prediction prompt before key operations.
    
    Args:
        question: The prediction question to display
        hint: Optional hint for the answer
    """
    print()
    print(f"💭 PREDICTION: {question}")
    if hint:
        print(f"   (Hint: {hint})")
    input("   Press Enter after you've made your prediction... ")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class ServerConfig:
    """Configuration for TCP server."""
    bind: str = DEFAULT_BIND
    port: int = DEFAULT_PORT
    backlog: int = DEFAULT_BACKLOG
    recv_buf: int = DEFAULT_RECV_BUF
    mode: str = "threaded"
    interactive: bool = False


# ═══════════════════════════════════════════════════════════════════════════════
# CLIENT HANDLER — HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def _receive_data(conn: socket.socket, recv_buf: int) -> Optional[bytes]:
    """
    Receive data from client connection.
    
    Args:
        conn: Connected socket
        recv_buf: Buffer size for recv()
    
    Returns:
        Received bytes or None if connection closed
    """
    data = conn.recv(recv_buf)
    return data if data else None


def _process_message(data: bytes) -> bytes:
    """
    Process received message and generate response.
    
    Args:
        data: Raw received bytes
    
    Returns:
        Response bytes
    """
    data_clean = data.rstrip(b"\r\n")
    return b"OK: " + data_clean.upper()


def _close_connection(conn: socket.socket) -> None:
    """
    Gracefully close connection with shutdown.
    
    Args:
        conn: Socket to close
    """
    try:
        conn.shutdown(socket.SHUT_RDWR)
    except Exception:
        pass
    conn.close()


def handle_client(conn: socket.socket, addr: Tuple[str, int], recv_buf: int) -> None:
    """
    Process TCP connection from client.
    
    Args:
        conn: Connected socket (already established)
        addr: Client address tuple (ip, port)
        recv_buf: Receive buffer size
    """
    client_ip, client_port = addr
    thread_name = threading.current_thread().name
    
    try:
        data = _receive_data(conn, recv_buf)
        if not data:
            log(thread_name, f"{client_ip}:{client_port} disconnected (no data)")
            return
        
        response = _process_message(data)
        log(thread_name, f"RX {len(data):4d}B from {client_ip}:{client_port}")
        
        conn.sendall(response)
        log(thread_name, f"TX {len(response):4d}B to   {client_ip}:{client_port}")
        
    except socket.timeout:
        log(thread_name, f"TIMEOUT from {client_ip}:{client_port}")
    except ConnectionResetError:
        log(thread_name, f"Connection reset by {client_ip}:{client_port}")
    except Exception as exc:
        log(thread_name, f"Error handling {client_ip}:{client_port}: {exc}")
    finally:
        _close_connection(conn)


# ═══════════════════════════════════════════════════════════════════════════════
# SERVER — HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def _create_server_socket(bind: str, port: int, backlog: int) -> socket.socket:
    """
    Create and configure TCP server socket.
    
    Args:
        bind: Address to bind to
        port: Port number
        backlog: Listen backlog
    
    Returns:
        Configured server socket
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((bind, port))
    sock.listen(backlog)
    return sock


def _log_server_start(cfg: ServerConfig) -> None:
    """Log server startup information."""
    log("SERVER", f"TCP server listening on {cfg.bind}:{cfg.port}")
    log("SERVER", f"Mode: {cfg.mode} | Backlog: {cfg.backlog}")
    log("SERVER", "Waiting for connections... (Ctrl+C to stop)")
    print()


def _handle_threaded(conn: socket.socket, addr: Tuple[str, int], 
                     recv_buf: int, count: int) -> None:
    """Handle connection in new thread."""
    t = threading.Thread(
        target=handle_client,
        args=(conn, addr, recv_buf),
        name=f"Worker-{count}"
    )
    t.daemon = True
    t.start()


def _handle_iterative(conn: socket.socket, addr: Tuple[str, int], 
                      recv_buf: int) -> None:
    """Handle connection in main thread (blocking)."""
    handle_client(conn, addr, recv_buf)


def run_server(cfg: ServerConfig) -> None:
    """
    Start TCP server.
    
    Args:
        cfg: Server configuration
    """
    sock = _create_server_socket(cfg.bind, cfg.port, cfg.backlog)
    _log_server_start(cfg)
    
    if cfg.interactive:
        prompt_prediction(
            "What will Wireshark show when a client connects?",
            "Think about the TCP three-way handshake"
        )
    
    connection_count = 0
    
    try:
        while True:
            conn, addr = sock.accept()
            connection_count += 1
            log("MAIN", f"Connection #{connection_count} from {addr[0]}:{addr[1]}")
            
            if cfg.mode == "iterative":
                _handle_iterative(conn, addr, cfg.recv_buf)
            else:
                _handle_threaded(conn, addr, cfg.recv_buf, connection_count)
                
    except KeyboardInterrupt:
        log("SERVER", "Shutting down (Ctrl+C)")
    finally:
        sock.close()


# ═══════════════════════════════════════════════════════════════════════════════
# CLIENT — HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def _connect_and_send(host: str, port: int, message: bytes, 
                      timeout: float) -> Tuple[Optional[bytes], float]:
    """
    Connect to server and exchange message.
    
    Returns:
        Tuple of (response bytes or None, round-trip time in ms)
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        t0 = time.perf_counter()
        
        sock.connect((host, port))
        sock.sendall(message)
        response = sock.recv(4096)
        
        rtt = (time.perf_counter() - t0) * 1000
        return response, rtt


def tcp_client(
    host: str,
    port: int,
    message: bytes,
    timeout: float = DEFAULT_TIMEOUT,
    interactive: bool = False
) -> Optional[bytes]:
    """
    Send message to TCP server and receive response.
    
    Args:
        host: Server hostname or IP
        port: Server port
        message: Message to send
        timeout: Connection timeout in seconds
        interactive: Enable prediction prompts
    
    Returns:
        Server response or None on failure
    """
    if interactive:
        prompt_prediction(
            "How many TCP packets will this exchange generate?",
            "Count: handshake + data + teardown"
        )
    
    try:
        response, rtt = _connect_and_send(host, port, message, timeout)
        log("CLIENT", f"RX {len(response)}B in {rtt:.1f}ms: {response!r}")
        return response
        
    except socket.timeout:
        log("CLIENT", f"TIMEOUT connecting to {host}:{port}")
    except ConnectionRefusedError:
        log("CLIENT", f"Connection refused by {host}:{port}")
    except Exception as exc:
        log("CLIENT", f"Error: {exc}")
    return None


# ═══════════════════════════════════════════════════════════════════════════════
# LOAD TEST — HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def _create_worker(host: str, port: int, message: bytes, 
                   timeout: float, results: List[Optional[bytes]], 
                   index: int) -> threading.Thread:
    """Create worker thread for load testing."""
    def worker() -> None:
        results[index] = tcp_client(host, port, message, timeout)
    
    return threading.Thread(target=worker)


def _start_workers(threads: List[threading.Thread], stagger_ms: int) -> None:
    """Start worker threads with optional stagger delay."""
    for t in threads:
        t.start()
        if stagger_ms > 0:
            time.sleep(stagger_ms / 1000)


def _wait_for_workers(threads: List[threading.Thread]) -> None:
    """Wait for all worker threads to complete."""
    for t in threads:
        t.join()


def _report_results(results: List[Optional[bytes]], duration: float, 
                    num_clients: int, interactive: bool) -> None:
    """Report load test results."""
    successful = sum(1 for r in results if r is not None)
    
    print()
    log("LOAD", f"Results: {successful}/{num_clients} successful in {duration:.0f}ms")
    log("LOAD", f"Throughput: {successful / (duration/1000):.1f} req/sec")
    
    if interactive:
        print()
        print("📊 REFLECTION:")
        print("   Was your prediction correct?")
        print(f"   If the server was iterative, expected time ≈ {num_clients * 100}ms")
        print("   If the server was threaded, expected time ≈ 100ms + overhead")


def run_load_test(
    host: str,
    port: int,
    num_clients: int,
    message: bytes,
    timeout: float,
    stagger_ms: int,
    interactive: bool = False
) -> None:
    """
    Load test with N concurrent clients.
    
    Args:
        host: Server hostname or IP
        port: Server port
        num_clients: Number of concurrent clients
        message: Message for each client to send
        timeout: Per-client timeout
        stagger_ms: Delay between client starts (milliseconds)
        interactive: Enable prediction prompts
    """
    if interactive:
        prompt_prediction(
            f"With {num_clients} concurrent clients, what's the expected total time?",
            "Consider: Is the server threaded or iterative?"
        )
    
    log("LOAD", f"Starting load test: {num_clients} clients → {host}:{port}")
    
    results: List[Optional[bytes]] = [None] * num_clients
    threads = [
        _create_worker(host, port, message, timeout, results, i)
        for i in range(num_clients)
    ]
    
    t0 = time.perf_counter()
    _start_workers(threads, stagger_ms)
    _wait_for_workers(threads)
    duration = (time.perf_counter() - t0) * 1000
    
    _report_results(results, duration, num_clients, interactive)


# ═══════════════════════════════════════════════════════════════════════════════
# CLI — HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def _add_server_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add server subcommand to argument parser."""
    p = subparsers.add_parser("server", help="Start TCP server")
    p.add_argument("--bind", default=DEFAULT_BIND,
                   help=f"Bind address (default: {DEFAULT_BIND})")
    p.add_argument("--port", type=int, default=DEFAULT_PORT,
                   help=f"Listen port (default: {DEFAULT_PORT})")
    p.add_argument("--backlog", type=int, default=DEFAULT_BACKLOG,
                   help=f"Connection backlog (default: {DEFAULT_BACKLOG})")
    p.add_argument("--recv-buf", type=int, default=DEFAULT_RECV_BUF,
                   help=f"Receive buffer size (default: {DEFAULT_RECV_BUF})")
    p.add_argument("--mode", choices=["threaded", "iterative"],
                   default="threaded", help="Server mode (default: threaded)")
    p.add_argument("--interactive", "-i", action="store_true",
                   help="Enable prediction prompts for learning")


def _add_client_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add client subcommand to argument parser."""
    p = subparsers.add_parser("client", help="Run TCP client")
    p.add_argument("--host", required=True, help="Server hostname/IP")
    p.add_argument("--port", type=int, required=True, help="Server port")
    p.add_argument("--message", "-m", required=True, help="Message to send")
    p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                   help=f"Timeout in seconds (default: {DEFAULT_TIMEOUT})")
    p.add_argument("--interactive", "-i", action="store_true",
                   help="Enable prediction prompts for learning")


def _add_load_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add load test subcommand to argument parser."""
    p = subparsers.add_parser("load", help="Run load test")
    p.add_argument("--host", required=True, help="Server hostname/IP")
    p.add_argument("--port", type=int, required=True, help="Server port")
    p.add_argument("--clients", "-n", type=int, default=10,
                   help="Number of concurrent clients (default: 10)")
    p.add_argument("--message", "-m", default="ping",
                   help="Message to send (default: ping)")
    p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                   help=f"Per-client timeout (default: {DEFAULT_TIMEOUT})")
    p.add_argument("--stagger-ms", type=int, default=50,
                   help="Delay between client starts in ms (default: 50)")
    p.add_argument("--interactive", "-i", action="store_true",
                   help="Enable prediction prompts for learning")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Week 2 – TCP Server/Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ex_2_01_tcp.py server --port 9090 --mode threaded
  python ex_2_01_tcp.py client --host 127.0.0.1 --port 9090 -m "Hello"
  python ex_2_01_tcp.py load --host 127.0.0.1 --port 9090 --clients 20
        """
    )
    
    subparsers = parser.add_subparsers(dest="cmd", required=True)
    _add_server_parser(subparsers)
    _add_client_parser(subparsers)
    _add_load_parser(subparsers)
    
    return parser.parse_args()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    args = parse_args()
    
    if args.cmd == "server":
        run_server(ServerConfig(
            bind=args.bind,
            port=args.port,
            backlog=args.backlog,
            recv_buf=args.recv_buf,
            mode=args.mode,
            interactive=args.interactive
        ))
    elif args.cmd == "client":
        response = tcp_client(
            args.host, 
            args.port, 
            args.message.encode(), 
            args.timeout,
            interactive=args.interactive
        )
        return 0 if response else 1
    elif args.cmd == "load":
        run_load_test(
            args.host,
            args.port,
            args.clients,
            args.message.encode(),
            args.timeout,
            args.stagger_ms,
            interactive=args.interactive
        )
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
