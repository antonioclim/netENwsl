#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
 Week 2 – Exercise 2: UDP Server and Client with Application Protocol
═══════════════════════════════════════════════════════════════════════════════

 LEARNING OBJECTIVES:
 ────────────────────
 1. Understand socket programming with UDP (SOCK_DGRAM)
 2. Compare connectionless communication with TCP
 3. Implement application-layer protocol over UDP
 4. Observe the difference in Wireshark captures

 APPLICATION PROTOCOL:
 ─────────────────────
   ping           → PONG
   upper:<text>   → <TEXT>
   lower:<text>   → <text>
   reverse:<text> → <txet>
   echo:<text>    → <text>
   time           → HH:MM:SS
   help           → List of commands

 USAGE:
   Server:      python ex_2_02_udp.py server --port 9091
   Interactive: python ex_2_02_udp.py client --host 127.0.0.1 --port 9091 -i
   One command: python ex_2_02_udp.py client --host 127.0.0.1 --port 9091 -o "ping"

 NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim
═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import argparse
import socket
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
DEFAULT_PORT = 9091
DEFAULT_BIND = "0.0.0.0"
DEFAULT_TIMEOUT = 2.0

HELP_TEXT = """Commands:
  ping           - Test connectivity (returns PONG)
  upper:<text>   - Convert text to uppercase
  lower:<text>   - Convert text to lowercase
  reverse:<text> - Reverse the text
  echo:<text>    - Echo back the text
  time           - Get server time (HH:MM:SS)
  help           - Show this help
  exit           - Close interactive client"""


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
# PREDICTION PROMPTS
# ═══════════════════════════════════════════════════════════════════════════════
def prompt_prediction(question: str, hint: str = "") -> None:
    """Display prediction prompt before key operations."""
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
    """Configuration for UDP server."""
    bind: str = DEFAULT_BIND
    port: int = DEFAULT_PORT
    recv_buf: int = 1024
    interactive: bool = False


# ═══════════════════════════════════════════════════════════════════════════════
# PROTOCOL — HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def _handle_simple_commands(cmd_lower: str) -> Optional[bytes]:
    """Handle simple commands without arguments."""
    if cmd_lower == "ping":
        return b"PONG"
    if cmd_lower == "time":
        return datetime.now().strftime("%H:%M:%S").encode()
    if cmd_lower == "help":
        return HELP_TEXT.encode()
    return None


def _handle_text_commands(cmd: str, cmd_lower: str) -> Optional[bytes]:
    """Handle commands that transform text."""
    if cmd_lower.startswith("upper:"):
        return cmd[6:].upper().encode()
    if cmd_lower.startswith("lower:"):
        return cmd[6:].lower().encode()
    if cmd_lower.startswith("reverse:"):
        return cmd[8:][::-1].encode()
    if cmd_lower.startswith("echo:"):
        return cmd[5:].encode()
    return None


def process_command(data: bytes) -> bytes:
    """
    Process command according to application protocol.
    
    Args:
        data: Raw bytes from client
    
    Returns:
        Response bytes
    """
    try:
        cmd = data.decode("utf-8").strip()
        cmd_lower = cmd.lower()
        
        result = _handle_simple_commands(cmd_lower)
        if result is not None:
            return result
        
        result = _handle_text_commands(cmd, cmd_lower)
        if result is not None:
            return result
        
        return f"ERROR: Unknown command: {cmd}".encode()
        
    except UnicodeDecodeError:
        return b"ERROR: Invalid UTF-8 encoding"
    except Exception as exc:
        return f"ERROR: {exc}".encode()


# ═══════════════════════════════════════════════════════════════════════════════
# SERVER — HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def _create_udp_socket(bind: str, port: int) -> socket.socket:
    """Create and bind UDP socket."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((bind, port))
    return sock


def _log_server_start(cfg: ServerConfig) -> None:
    """Log server startup information."""
    log("SERVER", f"UDP server listening on {cfg.bind}:{cfg.port}")
    log("SERVER", "Waiting for datagrams... (Ctrl+C to stop)")
    print()


def _handle_datagram(sock: socket.socket, data: bytes, 
                     addr: Tuple[str, int]) -> None:
    """Process and respond to a single datagram."""
    client_ip, client_port = addr
    log("SERVER", f"RX {len(data):4d}B from {client_ip}:{client_port}: {data!r}")
    
    response = process_command(data)
    sock.sendto(response, addr)
    log("SERVER", f"TX {len(response):4d}B to   {client_ip}:{client_port}: {response!r}")


def run_server(cfg: ServerConfig) -> None:
    """
    Start UDP server.
    
    Args:
        cfg: Server configuration
    """
    sock = _create_udp_socket(cfg.bind, cfg.port)
    _log_server_start(cfg)
    
    if cfg.interactive:
        prompt_prediction(
            "How many packets per command in Wireshark?",
            "Compare with TCP's handshake overhead"
        )
    
    request_count = 0
    
    try:
        while True:
            data, addr = sock.recvfrom(cfg.recv_buf)
            request_count += 1
            _handle_datagram(sock, data, addr)
            
    except KeyboardInterrupt:
        log("SERVER", f"Shutting down after {request_count} requests")
    finally:
        sock.close()


# ═══════════════════════════════════════════════════════════════════════════════
# CLIENT — HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def _create_client_socket(timeout: float) -> socket.socket:
    """Create UDP client socket with timeout."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    return sock


def send_recv(
    sock: socket.socket, 
    message: bytes, 
    server_addr: Tuple[str, int]
) -> Tuple[Optional[bytes], float]:
    """
    Send message and receive response.
    
    Returns:
        Tuple of (response or None, round-trip time in ms)
    """
    t0 = time.perf_counter()
    sock.sendto(message, server_addr)
    
    try:
        response, _ = sock.recvfrom(4096)
        rtt = (time.perf_counter() - t0) * 1000
        return response, rtt
    except socket.timeout:
        return None, 0.0


def _print_response(response: Optional[bytes], rtt: float) -> None:
    """Print response to user."""
    if response is None:
        print("  [TIMEOUT - no response]")
    else:
        text = response.decode("utf-8", errors="replace")
        for line in text.split("\n"):
            print(f"  {line}")
        print(f"  [RTT: {rtt:.1f}ms]")


def run_interactive(host: str, port: int, timeout: float) -> None:
    """
    Run interactive UDP client session.
    
    Args:
        host: Server hostname
        port: Server port
        timeout: Response timeout
    """
    server_addr = (host, port)
    sock = _create_client_socket(timeout)
    
    print(f"UDP Client → {host}:{port}")
    print("Type 'help' for commands, 'exit' to quit\n")
    
    try:
        while True:
            try:
                cmd = input("> ").strip()
            except EOFError:
                break
            
            if not cmd:
                continue
            if cmd.lower() == "exit":
                print("Goodbye!")
                break
            
            response, rtt = send_recv(sock, cmd.encode(), server_addr)
            _print_response(response, rtt)
            
    except KeyboardInterrupt:
        print("\nInterrupted")
    finally:
        sock.close()


def run_once(host: str, port: int, command: str, timeout: float) -> bool:
    """
    Send single command and print response.
    
    Returns:
        True if response received, False on timeout
    """
    server_addr = (host, port)
    sock = _create_client_socket(timeout)
    
    try:
        log("CLIENT", f"TX: {command}")
        response, rtt = send_recv(sock, command.encode(), server_addr)
        
        if response is None:
            log("CLIENT", "TIMEOUT - no response")
            return False
        
        log("CLIENT", f"RX in {rtt:.1f}ms: {response!r}")
        return True
        
    finally:
        sock.close()


# ═══════════════════════════════════════════════════════════════════════════════
# CLI — HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def _add_server_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add server subcommand."""
    p = subparsers.add_parser("server", help="Start UDP server")
    p.add_argument("--bind", default=DEFAULT_BIND,
                   help=f"Bind address (default: {DEFAULT_BIND})")
    p.add_argument("--port", type=int, default=DEFAULT_PORT,
                   help=f"Listen port (default: {DEFAULT_PORT})")
    p.add_argument("--recv-buf", type=int, default=1024,
                   help="Receive buffer size (default: 1024)")
    p.add_argument("--interactive", "-i", action="store_true",
                   help="Enable prediction prompts")


def _add_client_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add client subcommand."""
    p = subparsers.add_parser("client", help="Run UDP client")
    p.add_argument("--host", required=True, help="Server hostname/IP")
    p.add_argument("--port", type=int, required=True, help="Server port")
    p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                   help=f"Response timeout (default: {DEFAULT_TIMEOUT})")
    
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("-i", "--interactive", action="store_true",
                      help="Interactive mode")
    mode.add_argument("-o", "--once", metavar="CMD",
                      help="Send single command")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Week 2 – UDP Server/Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ex_2_02_udp.py server --port 9091
  python ex_2_02_udp.py client --host 127.0.0.1 --port 9091 -i
  python ex_2_02_udp.py client --host 127.0.0.1 --port 9091 -o "ping"
        """
    )
    
    subparsers = parser.add_subparsers(dest="cmd", required=True)
    _add_server_parser(subparsers)
    _add_client_parser(subparsers)
    
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
            recv_buf=args.recv_buf,
            interactive=args.interactive
        ))
    elif args.cmd == "client":
        if args.interactive:
            run_interactive(args.host, args.port, args.timeout)
        else:
            success = run_once(args.host, args.port, args.once, args.timeout)
            return 0 if success else 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
