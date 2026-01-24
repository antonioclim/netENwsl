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

 PREDICTION CHECKPOINTS (Brown & Wilson Principle 4):
 ────────────────────────────────────────────────────
 Before running, ask yourself:
 
 □ Server start: How many TCP packets does listen() generate?
   → Answer: Zero! listen() only marks the socket as passive.
 
 □ Client connect: What packets will Wireshark show?
   → Answer: SYN → SYN-ACK → ACK (three-way handshake)
 
 □ Load test (10 clients, threaded): How many threads will exist?
   → Answer: 11 (main + 10 workers)
 
 □ Load test (10 clients, iterative): Total time if each takes 100ms?
   → Answer: ~1000ms (sequential processing)

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
from typing import Optional, List

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
DEFAULT_PORT = 9090
DEFAULT_BIND = "0.0.0.0"
DEFAULT_BACKLOG = 32
DEFAULT_RECV_BUF = 1024
DEFAULT_TIMEOUT = 5.0


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
    
    Implements Brown & Wilson Principle 4: asking students to predict
    outcomes before execution builds deeper understanding.
    
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


@dataclass
class ServerConfig:
    """Configuration for TCP server."""
    bind: str = DEFAULT_BIND
    port: int = DEFAULT_PORT
    backlog: int = DEFAULT_BACKLOG
    recv_buf: int = DEFAULT_RECV_BUF
    mode: str = "threaded"
    interactive: bool = False  # Enable prediction prompts


# ═══════════════════════════════════════════════════════════════════════════════
# CLIENT HANDLER
# ═══════════════════════════════════════════════════════════════════════════════
def handle_client(conn: socket.socket, addr: tuple[str, int], recv_buf: int) -> None:
    """
    Process TCP connection from client.
    
    Protocol:
      - Receive message from client
      - Transform to uppercase
      - Respond with "OK: " prefix
    
    Analogy (CPA - Concrete):
        Think of this like a phone call handler:
        1. Phone rings (accept gave us conn)
        2. Listen to caller (recv)
        3. Respond appropriately (send)
        4. Hang up (close)
    
    Args:
        conn: Connected socket (already established)
        addr: Client address tuple (ip, port)
        recv_buf: Receive buffer size
    """
    client_ip, client_port = addr
    thread_name = threading.current_thread().name
    
    try:
        # ─── RECEIVE DATA ───
        # Prediction: Will recv() return immediately or block?
        # Answer: It blocks until data arrives or connection closes
        data = conn.recv(recv_buf)
        if not data:
            log(thread_name, f"{client_ip}:{client_port} disconnected (no data)")
            return
        
        # ─── PROCESS MESSAGE ───
        data_clean = data.rstrip(b"\r\n")
        response = b"OK: " + data_clean.upper()
        
        # ─── SEND RESPONSE ───
        log(thread_name, f"RX {len(data):4d}B from {client_ip}:{client_port}: {data_clean!r}")
        conn.sendall(response)
        log(thread_name, f"TX {len(response):4d}B to   {client_ip}:{client_port}: {response!r}")
        
    except socket.timeout:
        log(thread_name, f"TIMEOUT from {client_ip}:{client_port}")
    except ConnectionResetError:
        log(thread_name, f"Connection reset by {client_ip}:{client_port}")
    except Exception as exc:
        log(thread_name, f"Error handling {client_ip}:{client_port}: {exc}")
    finally:
        # ─── CLEANUP ───
        # Graceful shutdown: send FIN, wait for ACK
        try:
            conn.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        conn.close()


# ═══════════════════════════════════════════════════════════════════════════════
# SERVER
# ═══════════════════════════════════════════════════════════════════════════════
def run_server(cfg: ServerConfig) -> None:
    """
    Start TCP server.
    
    Modes:
      - threaded: One thread per connection (concurrent)
      - iterative: Handle one client at a time (sequential)
    
    What to observe in Wireshark:
      - Server start: No packets (bind/listen are local operations)
      - Client connects: SYN → SYN-ACK → ACK
      - Data exchange: PSH-ACK packets with payload
      - Client disconnects: FIN → ACK → FIN → ACK
    
    Args:
        cfg: Server configuration
    """
    # ─── CREATE SOCKET ───
    # Prediction: What does SOCK_STREAM mean?
    # Answer: TCP (reliable, ordered, connection-oriented)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # ─── BIND AND LISTEN ───
    # Prediction: Does bind() send any packets?
    # Answer: No! It's purely a local operation
    sock.bind((cfg.bind, cfg.port))
    sock.listen(cfg.backlog)
    
    log("SERVER", f"TCP server listening on {cfg.bind}:{cfg.port}")
    log("SERVER", f"Mode: {cfg.mode} | Backlog: {cfg.backlog}")
    log("SERVER", "Waiting for connections... (Ctrl+C to stop)")
    print()
    
    if cfg.interactive:
        prompt_prediction(
            "What will Wireshark show when a client connects?",
            "Think about the TCP three-way handshake"
        )
    
    connection_count = 0
    
    try:
        while True:
            # ─── ACCEPT CONNECTION ───
            # This blocks until a client connects
            # Prediction: What creates the SYN-ACK response?
            # Answer: The OS kernel, automatically during accept()
            conn, addr = sock.accept()
            connection_count += 1
            log("MAIN", f"Connection #{connection_count} from {addr[0]}:{addr[1]}")
            
            if cfg.mode == "iterative":
                # Handle synchronously (blocks next connection)
                # Prediction: If 3 clients connect now, how long until all served?
                # Answer: 3 × handler_time (sequential)
                handle_client(conn, addr, cfg.recv_buf)
            else:
                # Handle in separate thread
                # Prediction: Can the main thread accept more connections immediately?
                # Answer: Yes! Thread handles client independently
                t = threading.Thread(
                    target=handle_client,
                    args=(conn, addr, cfg.recv_buf),
                    daemon=True,
                    name=f"Worker-{addr[1]}"
                )
                t.start()
                
    except KeyboardInterrupt:
        print()
        log("SERVER", f"Shutting down... Total connections: {connection_count}")
    finally:
        sock.close()


# ═══════════════════════════════════════════════════════════════════════════════
# CLIENT
# ═══════════════════════════════════════════════════════════════════════════════
def tcp_client(
    host: str, 
    port: int, 
    message: bytes, 
    timeout: float,
    interactive: bool = False
) -> Optional[bytes]:
    """
    Simple TCP client.
    
    What to observe in Wireshark:
      1. connect() → SYN, SYN-ACK, ACK
      2. send() → PSH-ACK with payload
      3. recv() → PSH-ACK from server
      4. close() → FIN, ACK, FIN, ACK
    
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
            f"How many TCP packets will this exchange generate?",
            "Count: handshake + data + teardown"
        )
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            t0 = time.perf_counter()
            
            # ─── CONNECT ───
            # Prediction: What happens if the server isn't running?
            # Answer: ConnectionRefusedError (RST packet received)
            sock.connect((host, port))
            
            # ─── SEND ───
            sock.sendall(message)
            
            # ─── RECEIVE ───
            response = sock.recv(4096)
            
            rtt = (time.perf_counter() - t0) * 1000
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
# LOAD TEST
# ═══════════════════════════════════════════════════════════════════════════════
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
    
    Prediction exercise:
      - Threaded server, 10 clients, 100ms each: ~100ms total
      - Iterative server, 10 clients, 100ms each: ~1000ms total
    
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
    
    def worker(i: int) -> None:
        results[i] = tcp_client(host, port, message, timeout)
    
    threads = []
    t0 = time.perf_counter()
    
    # Start clients
    for i in range(num_clients):
        t = threading.Thread(target=worker, args=(i,))
        t.start()
        threads.append(t)
        if stagger_ms > 0:
            time.sleep(stagger_ms / 1000)
    
    # Wait for all to complete
    for t in threads:
        t.join()
    
    duration = (time.perf_counter() - t0) * 1000
    successful = sum(1 for r in results if r is not None)
    
    print()
    log("LOAD", f"Results: {successful}/{num_clients} successful in {duration:.0f}ms")
    log("LOAD", f"Throughput: {successful / (duration/1000):.1f} req/sec")
    
    # Post-test reflection
    if interactive:
        print()
        print("📊 REFLECTION:")
        print(f"   Was your prediction correct?")
        print(f"   If the server was iterative, expected time ≈ {num_clients * 100}ms")
        print(f"   If the server was threaded, expected time ≈ 100ms + overhead")


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Week 2 – TCP Server/Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start server in threaded mode
  python ex_2_01_tcp.py server --port 9090 --mode threaded
  
  # Start server with prediction prompts
  python ex_2_01_tcp.py server --port 9090 --interactive
  
  # Send a message
  python ex_2_01_tcp.py client --host 127.0.0.1 --port 9090 -m "Hello"
  
  # Load test with 20 clients
  python ex_2_01_tcp.py load --host 127.0.0.1 --port 9090 --clients 20
        """
    )
    
    subparsers = parser.add_subparsers(dest="cmd", required=True)
    
    # Server subcommand
    server_parser = subparsers.add_parser("server", help="Start TCP server")
    server_parser.add_argument("--bind", default=DEFAULT_BIND,
                               help=f"Bind address (default: {DEFAULT_BIND})")
    server_parser.add_argument("--port", type=int, default=DEFAULT_PORT,
                               help=f"Listen port (default: {DEFAULT_PORT})")
    server_parser.add_argument("--backlog", type=int, default=DEFAULT_BACKLOG,
                               help=f"Connection backlog (default: {DEFAULT_BACKLOG})")
    server_parser.add_argument("--recv-buf", type=int, default=DEFAULT_RECV_BUF,
                               help=f"Receive buffer size (default: {DEFAULT_RECV_BUF})")
    server_parser.add_argument("--mode", choices=["threaded", "iterative"],
                               default="threaded",
                               help="Server mode (default: threaded)")
    server_parser.add_argument("--interactive", "-i", action="store_true",
                               help="Enable prediction prompts for learning")
    
    # Client subcommand
    client_parser = subparsers.add_parser("client", help="Run TCP client")
    client_parser.add_argument("--host", required=True, help="Server hostname/IP")
    client_parser.add_argument("--port", type=int, required=True, help="Server port")
    client_parser.add_argument("--message", "-m", required=True, help="Message to send")
    client_parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                               help=f"Timeout in seconds (default: {DEFAULT_TIMEOUT})")
    client_parser.add_argument("--interactive", "-i", action="store_true",
                               help="Enable prediction prompts for learning")
    
    # Load test subcommand
    load_parser = subparsers.add_parser("load", help="Run load test")
    load_parser.add_argument("--host", required=True, help="Server hostname/IP")
    load_parser.add_argument("--port", type=int, required=True, help="Server port")
    load_parser.add_argument("--clients", "-n", type=int, default=10,
                             help="Number of concurrent clients (default: 10)")
    load_parser.add_argument("--message", "-m", default="ping",
                             help="Message to send (default: ping)")
    load_parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                             help=f"Per-client timeout (default: {DEFAULT_TIMEOUT})")
    load_parser.add_argument("--stagger-ms", type=int, default=50,
                             help="Delay between client starts in ms (default: 50)")
    load_parser.add_argument("--interactive", "-i", action="store_true",
                             help="Enable prediction prompts for learning")
    
    return parser.parse_args()


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
