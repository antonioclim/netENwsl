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

 PREDICTION CHECKPOINTS (Brown & Wilson Principle 4):
 ────────────────────────────────────────────────────
 Before running, ask yourself:
 
 □ Server start: Does bind() generate any network traffic?
   → Answer: No! It's purely a local operation.
 
 □ Client sends "ping": How many packets in Wireshark?
   → Answer: 2 (request datagram + response datagram). No handshake!
 
 □ Server down: What happens when client sends message?
   → Answer: sendto() succeeds (fire-and-forget), but recvfrom() times out.
 
 □ Compare with TCP: What's missing from the capture?
   → Answer: No SYN, SYN-ACK, ACK, FIN packets. Just data!

 NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim
═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import argparse
import socket
import sys
import time
from dataclasses import dataclass, field
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
    """Configuration for UDP server."""
    bind: str = DEFAULT_BIND
    port: int = DEFAULT_PORT
    recv_buf: int = 1024
    interactive: bool = False


# ═══════════════════════════════════════════════════════════════════════════════
# PROTOCOL IMPLEMENTATION
# ═══════════════════════════════════════════════════════════════════════════════
def process_command(data: bytes) -> bytes:
    """
    Process command according to application protocol.
    
    Each datagram is independent — unlike TCP, there's no session state.
    The server must handle each message completely on its own.
    
    Args:
        data: Raw bytes from client
    
    Returns:
        Response bytes
    """
    try:
        cmd = data.decode("utf-8").strip()
        cmd_lower = cmd.lower()
        
        if cmd_lower == "ping":
            return b"PONG"
        
        if cmd_lower == "time":
            return datetime.now().strftime("%H:%M:%S").encode()
        
        if cmd_lower == "help":
            return HELP_TEXT.encode()
        
        if cmd_lower.startswith("upper:"):
            text = cmd[6:]
            return text.upper().encode()
        
        if cmd_lower.startswith("lower:"):
            text = cmd[6:]
            return text.lower().encode()
        
        if cmd_lower.startswith("reverse:"):
            text = cmd[8:]
            return text[::-1].encode()
        
        if cmd_lower.startswith("echo:"):
            text = cmd[5:]
            return text.encode()
        
        return b"UNKNOWN COMMAND - Type 'help' for available commands"
        
    except UnicodeDecodeError:
        return b"ERROR: Invalid UTF-8 encoding"
    except Exception as e:
        return f"ERROR: {e}".encode()


# ═══════════════════════════════════════════════════════════════════════════════
# SERVER
# ═══════════════════════════════════════════════════════════════════════════════
def run_server(cfg: ServerConfig) -> None:
    """
    Start UDP server.
    
    The server receives datagrams, processes commands and sends responses.
    No connection establishment — each datagram is independent.
    
    Analogy (CPA - Concrete):
        UDP server is like a postal worker:
        - Letters (datagrams) arrive independently
        - Each letter has a return address
        - Reply to each letter without remembering previous ones
        - No "conversation" — just individual exchanges
    
    What to observe in Wireshark:
        - No handshake packets (unlike TCP)
        - Each exchange is just: request datagram → response datagram
        - Source port on client side is ephemeral (random high port)
    
    Args:
        cfg: Server configuration
    """
    # ─── CREATE UDP SOCKET ───
    # Prediction: What's different about SOCK_DGRAM vs SOCK_STREAM?
    # Answer: SOCK_DGRAM = UDP (unreliable, message-oriented)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((cfg.bind, cfg.port))
    
    log("SERVER", f"UDP server listening on {cfg.bind}:{cfg.port}")
    log("SERVER", "Waiting for datagrams... (Ctrl+C to stop)")
    print()
    
    if cfg.interactive:
        prompt_prediction(
            "What will you see in Wireshark when a client sends 'ping'?",
            "Compare with the TCP handshake from Exercise 1"
        )
    
    datagram_count = 0
    
    try:
        while True:
            # ─── RECEIVE DATAGRAM ───
            # Prediction: Does recvfrom() need a prior accept()?
            # Answer: No! UDP is connectionless — just wait for any datagram
            data, addr = sock.recvfrom(cfg.recv_buf)
            datagram_count += 1
            
            # ─── PROCESS COMMAND ───
            response = process_command(data)
            
            # ─── LOG AND RESPOND ───
            log("SERVER", f"#{datagram_count:4d} RX {len(data):4d}B from {addr[0]}:{addr[1]}: {data!r}")
            
            # Prediction: How does server know where to send response?
            # Answer: addr from recvfrom() contains client's IP and port
            sock.sendto(response, addr)
            log("SERVER", f"#{datagram_count:4d} TX {len(response):4d}B to   {addr[0]}:{addr[1]}: {response!r}")
            
    except KeyboardInterrupt:
        print()
        log("SERVER", f"Shutting down... Total datagrams: {datagram_count}")
    finally:
        sock.close()


# ═══════════════════════════════════════════════════════════════════════════════
# CLIENT
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class ClientStats:
    """Statistics tracker for client session."""
    sent: int = 0
    received: int = 0
    timeouts: int = 0
    total_rtt: float = 0.0
    
    @property
    def avg_rtt(self) -> float:
        """Calculate average round-trip time."""
        return self.total_rtt / self.received if self.received > 0 else 0.0


def send_recv(
    sock: socket.socket,
    msg: bytes,
    addr: Tuple[str, int],
    timeout: float
) -> Tuple[Optional[bytes], float]:
    """
    Send datagram and wait for response.
    
    Key insight: sendto() can "succeed" even if no server is listening!
    UDP is fire-and-forget — only recvfrom() reveals if anyone responded.
    
    Args:
        sock: UDP socket
        msg: Message to send
        addr: Destination (host, port)
        timeout: Receive timeout in seconds
    
    Returns:
        Tuple of (response_bytes or None, round_trip_time_ms)
    """
    sock.settimeout(timeout)
    try:
        t0 = time.perf_counter()
        # Prediction: Will sendto() fail if server is down?
        # Answer: No! UDP doesn't check — it just sends the packet
        sock.sendto(msg, addr)
        response, _ = sock.recvfrom(4096)
        rtt = (time.perf_counter() - t0) * 1000
        return response, rtt
    except socket.timeout:
        return None, 0.0


def run_interactive(
    host: str, 
    port: int, 
    timeout: float,
    show_predictions: bool = False
) -> None:
    """
    Run interactive UDP client.
    
    Provides a REPL-like interface for sending commands to the server.
    
    Args:
        host: Server hostname or IP
        port: Server port
        timeout: Response timeout in seconds
        show_predictions: Enable prediction prompts
    """
    addr = (host, port)
    stats = ClientStats()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    print()
    log("CLIENT", f"UDP interactive client → {host}:{port}")
    log("CLIENT", "Type 'help' for commands, 'exit' to quit")
    print()
    
    if show_predictions:
        prompt_prediction(
            "You'll send 'ping' to the server. How many packets will Wireshark show?",
            "Remember: UDP has no handshake"
        )
    
    try:
        while True:
            try:
                # Get user input
                inp = input("> ").strip()
                if not inp:
                    continue
                if inp.lower() == "exit":
                    break
                
                # Send and receive
                stats.sent += 1
                response, rtt = send_recv(sock, inp.encode(), addr, timeout)
                
                if response:
                    stats.received += 1
                    stats.total_rtt += rtt
                    try:
                        print(f"  ← {response.decode()} ({rtt:.1f}ms)")
                    except UnicodeDecodeError:
                        print(f"  ← {response!r} ({rtt:.1f}ms)")
                else:
                    stats.timeouts += 1
                    print("  ← [TIMEOUT - no response]")
                    # Prediction prompt for failed request
                    if show_predictions and stats.timeouts == 1:
                        print()
                        print("  💭 Why might the server not respond?")
                        print("     - Server not running?")
                        print("     - Wrong port?")
                        print("     - Firewall blocking UDP?")
                        print()
                    
            except (EOFError, KeyboardInterrupt):
                print()
                break
                
    finally:
        sock.close()
        print()
        log("CLIENT", f"Session statistics:")
        log("CLIENT", f"  Sent: {stats.sent} | Received: {stats.received} | "
                      f"Timeouts: {stats.timeouts}")
        log("CLIENT", f"  Average RTT: {stats.avg_rtt:.1f}ms")


def run_once(
    host: str, 
    port: int, 
    cmd: str, 
    timeout: float,
    show_predictions: bool = False
) -> int:
    """
    Send single command and display response.
    
    Args:
        host: Server hostname or IP
        port: Server port
        cmd: Command to send
        timeout: Response timeout in seconds
        show_predictions: Enable prediction prompts
    
    Returns:
        0 on success, 1 on failure
    """
    if show_predictions:
        prompt_prediction(
            f"You're about to send '{cmd}' via UDP. What will happen?",
            "Think about: packets sent, response expected"
        )
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        response, rtt = send_recv(sock, cmd.encode(), (host, port), timeout)
        if response:
            log("CLIENT", f"TX: {cmd!r}")
            try:
                log("CLIENT", f"RX: {response.decode()} ({rtt:.1f}ms)")
            except UnicodeDecodeError:
                log("CLIENT", f"RX: {response!r} ({rtt:.1f}ms)")
            return 0
        else:
            log("CLIENT", "TIMEOUT - no response from server")
            return 1
    finally:
        sock.close()


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Week 2 – UDP Server/Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start server
  python ex_2_02_udp.py server --port 9091
  
  # Start server with prediction prompts
  python ex_2_02_udp.py server --port 9091 --interactive
  
  # Interactive client
  python ex_2_02_udp.py client --host 127.0.0.1 --port 9091 -i
  
  # Single command
  python ex_2_02_udp.py client --host 127.0.0.1 --port 9091 -o "upper:hello"
        """
    )
    
    subparsers = parser.add_subparsers(dest="cmd", required=True)
    
    # Server subcommand
    server_parser = subparsers.add_parser("server", help="Start UDP server")
    server_parser.add_argument("--bind", default=DEFAULT_BIND,
                               help=f"Bind address (default: {DEFAULT_BIND})")
    server_parser.add_argument("--port", type=int, default=DEFAULT_PORT,
                               help=f"Listen port (default: {DEFAULT_PORT})")
    server_parser.add_argument("--recv-buf", type=int, default=1024,
                               help="Receive buffer size (default: 1024)")
    server_parser.add_argument("--interactive", action="store_true",
                               help="Enable prediction prompts for learning")
    
    # Client subcommand
    client_parser = subparsers.add_parser("client", help="Run UDP client")
    client_parser.add_argument("--host", required=True, help="Server hostname/IP")
    client_parser.add_argument("--port", type=int, required=True, help="Server port")
    client_parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                               help=f"Timeout in seconds (default: {DEFAULT_TIMEOUT})")
    client_parser.add_argument("--predictions", "-p", action="store_true",
                               help="Enable prediction prompts for learning")
    
    # Client mode selection
    mode_group = client_parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--interactive", "-i", action="store_true",
                           help="Interactive mode (REPL)")
    mode_group.add_argument("--once", "-o", metavar="CMD",
                           help="Send single command")
    
    return parser.parse_args()


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
        show_pred = getattr(args, 'predictions', False)
        if args.interactive:
            run_interactive(args.host, args.port, args.timeout, show_pred)
        else:
            return run_once(args.host, args.port, args.once, args.timeout, show_pred)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
