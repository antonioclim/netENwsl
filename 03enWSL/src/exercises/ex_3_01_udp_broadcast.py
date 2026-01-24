#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  Exercise 1: UDP Broadcast (IPv4)                                            ║
║  Week 3 — Computer Networks                                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

LEARNING OBJECTIVES:
    - Understanding the difference between unicast and broadcast at IP level
    - Using the SO_BROADCAST option on the UDP socket
    - Observing the "one-to-all" behaviour in an L2 domain
    - Capturing and analysing broadcast traffic with tcpdump

KEY CONCEPTS:
    1. Broadcast = sending to ALL hosts in a broadcast domain (L2)
    2. Address 255.255.255.255 = "limited broadcast" (does not cross routers)
    3. Address x.x.x.255 = "directed broadcast" (for a specific subnet)
    4. SO_BROADCAST = flag mandatory on socket to allow broadcast

PAIR PROGRAMMING:
    Driver: Types the socket code and runs sender/receiver
    Navigator: Monitors tcpdump output and verifies packet flow
    Swap after: Completing send function, then after recv function

USAGE:
    # Receiver (on week3_receiver and week3_client):
    python3 ex_3_01_udp_broadcast.py recv --port 5007 --count 5

    # Sender (on week3_client):
    python3 ex_3_01_udp_broadcast.py send --dst 255.255.255.255 --port 5007 --count 5

    # Traffic capture (on week3_receiver):
    tcpdump -ni eth0 'udp port 5007'

IMPORTANT NOTES:
    - Broadcast does NOT cross routers (limited to the L2 domain)
    - All hosts in the domain receive the frame at L2 level, regardless of whether
      they listen on that port or not (saturates the network)
    - It is inefficient at large scale — multicast or unicast is preferred
"""
from __future__ import annotations

import argparse
import socket
import sys
import time
from datetime import datetime
from typing import Callable


# ════════════════════════════════════════════════════════════════════════════
#  CONSTANTS AND CONFIGURATION
# ════════════════════════════════════════════════════════════════════════════

DEFAULT_BROADCAST_ADDR = "255.255.255.255"
DEFAULT_PORT = 5007
DEFAULT_MESSAGE = "HELLO_BCAST"
DEFAULT_INTERVAL = 1.0
BUFFER_SIZE = 65535


# ════════════════════════════════════════════════════════════════════════════
#  UTILITY FUNCTIONS
# ════════════════════════════════════════════════════════════════════════════

def timestamp() -> str:
    """Return the current timestamp in human-readable format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def log(level: str, message: str) -> None:
    """Display a message with timestamp and level."""
    print(f"[{timestamp()}] [{level}] {message}")


def prompt_prediction(question: str) -> str:
    """
    Ask student to predict outcome before execution.
    
    This implements Brown & Wilson Principle 4: Predictions.
    Making predictions before seeing results improves learning retention.
    
    Args:
        question: The prediction question to ask
        
    Returns:
        The student's prediction as a string
    """
    print(f"\n💭 PREDICTION: {question}")
    prediction = input("Your answer: ")
    return prediction


# ════════════════════════════════════════════════════════════════════════════
#  SENDER: UDP Broadcast Transmission
# ════════════════════════════════════════════════════════════════════════════

def cmd_send(args: argparse.Namespace) -> int:
    """
    Send UDP datagrams to a broadcast address.
    
    Steps:
    1. Create UDP socket (SOCK_DGRAM)
    2. Enable SO_BROADCAST (mandatory!)
    3. Periodic transmission with sendto()
    
    Args:
        args: Parsed arguments (dst, port, message, interval, count, bind)
    
    Returns:
        0 for success, 1 for error
    """
    dst = args.dst
    port = args.port
    base_message = args.message
    interval = args.interval
    count = args.count

    # ─────────────────────────────────────────────────────────────────────────
    # PREDICTION CHECKPOINT
    # ─────────────────────────────────────────────────────────────────────────
    if not args.no_predict:
        prompt_prediction(
            f"How many hosts on the subnet will receive messages sent to {dst}?"
        )

    # ─────────────────────────────────────────────────────────────────────────
    # Step 1: Create UDP socket
    # ─────────────────────────────────────────────────────────────────────────
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # ─────────────────────────────────────────────────────────────────────────
    # Step 2: Enable SO_BROADCAST
    # CRITICAL: Without this option, sendto() to a broadcast address will fail
    #           with PermissionError or "Operation not permitted" on most OS.
    # ─────────────────────────────────────────────────────────────────────────
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Optional: bind to a specific interface (useful when you have multiple interfaces)
    if args.bind:
        sock.bind((args.bind, 0))
        log("INFO", f"Socket bound to interface: {args.bind}")

    log("INFO", f"UDP Broadcast Sender started → {dst}:{port}")
    log("INFO", f"Parameters: interval={interval}s, count={count} (0=infinite)")

    counter = 0
    try:
        while count == 0 or counter < count:
            # Build payload with sequence number
            payload = f"{base_message} #{counter}".encode("utf-8")

            # ─────────────────────────────────────────────────────────────────
            # Step 3: Transmit datagram
            # sendto() specifies the destination for each datagram (UDP is
            # connectionless, so there is no persistent "connection").
            # ─────────────────────────────────────────────────────────────────
            sock.sendto(payload, (dst, port))
            log("SEND", f"{len(payload):4d} bytes → {dst}:{port} :: {payload.decode()!r}")

            counter += 1
            time.sleep(interval)

    except KeyboardInterrupt:
        log("INFO", "Interrupted by user (Ctrl+C).")
    except OSError as e:
        log("ERROR", f"Socket error: {e}")
        return 1
    finally:
        sock.close()
        log("INFO", f"Socket closed. Total sent: {counter} datagrams.")

    return 0


# ════════════════════════════════════════════════════════════════════════════
#  RECEIVER: UDP Broadcast Reception
# ════════════════════════════════════════════════════════════════════════════

def cmd_recv(args: argparse.Namespace) -> int:
    """
    Receive UDP datagrams (including broadcast).
    
    Steps:
    1. Create UDP socket
    2. Enable SO_REUSEADDR (for quick restart during tests)
    3. Bind to port (and optionally to a specific address)
    4. Loop recvfrom() to receive datagrams
    
    Args:
        args: Parsed arguments (bind_addr, port, count, prefix, timeout)
    
    Returns:
        0 for success
    """
    bind_addr = args.bind_addr
    port = args.port
    count = args.count
    prefix = args.prefix
    timeout_sec = args.timeout

    # ─────────────────────────────────────────────────────────────────────────
    # PREDICTION CHECKPOINT
    # ─────────────────────────────────────────────────────────────────────────
    if not args.no_predict:
        prompt_prediction(
            "What source IP address will appear in the received datagrams?"
        )

    # ─────────────────────────────────────────────────────────────────────────
    # Step 1: Create UDP socket
    # ─────────────────────────────────────────────────────────────────────────
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # ─────────────────────────────────────────────────────────────────────────
    # Step 2: SO_REUSEADDR allows port reuse immediately after closing.
    # Useful during tests when you frequently restart the programme.
    # ─────────────────────────────────────────────────────────────────────────
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # ─────────────────────────────────────────────────────────────────────────
    # Step 3: Bind to address and port
    # bind_addr="" (empty string) = INADDR_ANY = listen on all interfaces
    # This is necessary to receive broadcast!
    # ─────────────────────────────────────────────────────────────────────────
    sock.bind((bind_addr, port))

    # Optional: timeout to avoid blocking indefinitely
    if timeout_sec > 0:
        sock.settimeout(timeout_sec)

    log("INFO", f"UDP Broadcast Receiver started on {bind_addr or '*'}:{port}")
    log("INFO", f"Parameters: count={count} (0=infinite), prefix={prefix!r}, timeout={timeout_sec}s")

    accepted = 0
    total = 0

    try:
        while count == 0 or accepted < count:
            try:
                # ─────────────────────────────────────────────────────────────
                # Step 4: recvfrom() - blocks until it receives a datagram
                # Returns (data, (source_ip, source_port))
                # ─────────────────────────────────────────────────────────────
                data, (sender_ip, sender_port) = sock.recvfrom(BUFFER_SIZE)
            except socket.timeout:
                log("WARN", f"Timeout after {timeout_sec}s without data. Stopping.")
                break

            total += 1
            text = data.decode("utf-8", errors="replace")

            # Optional filtering by prefix
            if prefix and not text.startswith(prefix):
                log("SKIP", f"From {sender_ip}:{sender_port} → {text!r} (does not start with {prefix!r})")
                continue

            accepted += 1
            log("RECV", f"{len(data):4d} bytes from {sender_ip}:{sender_port} → {text!r}")

    except KeyboardInterrupt:
        log("INFO", "Interrupted by user (Ctrl+C).")
    finally:
        sock.close()
        log("INFO", f"Socket closed. Accepted: {accepted}/{total} datagrams.")

    return 0


# ════════════════════════════════════════════════════════════════════════════
#  ARGUMENT PARSER
# ════════════════════════════════════════════════════════════════════════════

def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser with send and recv subcommands."""
    parser = argparse.ArgumentParser(
        prog="ex_3_01_udp_broadcast.py",
        description="UDP Broadcast sender/receiver for network demonstrations.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start receiver on port 5007, receive 5 messages:
  python3 ex_3_01_udp_broadcast.py recv --port 5007 --count 5

  # Start sender to broadcast, 5 messages, interval 0.5s:
  python3 ex_3_01_udp_broadcast.py send --dst 255.255.255.255 --port 5007 --count 5 --interval 0.5

  # Run without prediction prompts (for automated testing):
  python3 ex_3_01_udp_broadcast.py send --no-predict --count 3
        """
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help="Command to execute")

    # ─────────────────────────────────────────────────────────────────────────
    # Subcommand: send
    # ─────────────────────────────────────────────────────────────────────────
    parser_send = subparsers.add_parser("send", help="Send UDP broadcast datagrams")
    parser_send.add_argument(
        "--dst", default=DEFAULT_BROADCAST_ADDR,
        help=f"Destination broadcast address (default: {DEFAULT_BROADCAST_ADDR})"
    )
    parser_send.add_argument(
        "--port", type=int, default=DEFAULT_PORT,
        help=f"Destination UDP port (default: {DEFAULT_PORT})"
    )
    parser_send.add_argument(
        "--message", default=DEFAULT_MESSAGE,
        help=f"Message to send (default: {DEFAULT_MESSAGE})"
    )
    parser_send.add_argument(
        "--interval", type=float, default=DEFAULT_INTERVAL,
        help=f"Interval between datagrams in seconds (default: {DEFAULT_INTERVAL})"
    )
    parser_send.add_argument(
        "--count", type=int, default=0,
        help="Number of datagrams to send (0 = infinite)"
    )
    parser_send.add_argument(
        "--bind", default="",
        help="Local IP address to bind (optional, for multi-homed hosts)"
    )
    parser_send.add_argument(
        "--no-predict", action="store_true",
        help="Skip prediction prompts (for automated testing)"
    )
    parser_send.set_defaults(func=cmd_send)

    # ─────────────────────────────────────────────────────────────────────────
    # Subcommand: recv
    # ─────────────────────────────────────────────────────────────────────────
    parser_recv = subparsers.add_parser("recv", help="Receive UDP broadcast datagrams")
    parser_recv.add_argument(
        "--bind-addr", default="",
        help="Address to bind (default: '' = all interfaces)"
    )
    parser_recv.add_argument(
        "--port", type=int, default=DEFAULT_PORT,
        help=f"UDP port to listen on (default: {DEFAULT_PORT})"
    )
    parser_recv.add_argument(
        "--count", type=int, default=0,
        help="Number of messages to accept (0 = infinite)"
    )
    parser_recv.add_argument(
        "--prefix", default="",
        help="Filtering: accept only messages starting with this prefix"
    )
    parser_recv.add_argument(
        "--timeout", type=float, default=0.0,
        help="Socket timeout in seconds (0 = no timeout)"
    )
    parser_recv.add_argument(
        "--no-predict", action="store_true",
        help="Skip prediction prompts (for automated testing)"
    )
    parser_recv.set_defaults(func=cmd_recv)

    return parser


# ════════════════════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════════════════════

def main(argv: list[str] | None = None) -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
