#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  Exercise 2: UDP Multicast (IPv4)                                            ║
║  Week 3 — Computer Networks                                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

LEARNING OBJECTIVES:
    - Understanding the difference between broadcast and multicast
    - Using IP_ADD_MEMBERSHIP to join a multicast group
    - Controlling TTL for multicast datagram scope
    - Observing IGMP messages with tcpdump

KEY CONCEPTS:
    1. Multicast = Sending to a GROUP of hosts (not all, like broadcast)
    2. Multicast addresses: 224.0.0.0 – 239.255.255.255 (Class D)
       - 224.0.0.x = link-local (TTL=1, does not cross routers)
       - 239.x.x.x = administratively scoped (organisation/LAN)
    3. Receivers must explicitly JOIN (IP_ADD_MEMBERSHIP)
    4. IGMP (Internet Group Management Protocol) manages membership
    5. TTL controls the "distance" a multicast datagram can travel

DIFFERENCES BROADCAST vs MULTICAST:
    ┌────────────────────┬─────────────────────┬─────────────────────┐
    │ Aspect             │ Broadcast           │ Multicast           │
    ├────────────────────┼─────────────────────┼─────────────────────┤
    │ Who receives       │ ALL in L2 domain    │ Only group members  │
    │ Explicit join      │ No                  │ Yes (IGMP)          │
    │ Crosses routers    │ No                  │ Yes (with config)   │
    │ Network overhead   │ High                │ Optimised           │
    │ Destination addr   │ 255.255.255.255     │ 224.x.x.x-239.x.x.x │
    │ MAC destination    │ ff:ff:ff:ff:ff:ff   │ 01:00:5e:xx:xx:xx   │
    └────────────────────┴─────────────────────┴─────────────────────┘

PAIR PROGRAMMING:
    Driver: Configures multicast sockets and runs sender/receiver
    Navigator: Captures IGMP traffic and verifies group membership
    Swap after: Setting up receiver with join, then after sender test

USAGE:
    # Receiver that JOINs the group:
    python3 ex_3_02_udp_multicast.py recv --group 239.1.1.1 --port 5008 --count 5

    # Sender:
    python3 ex_3_02_udp_multicast.py send --group 239.1.1.1 --port 5008 --count 5 --ttl 1

    # Verify membership:
    ip maddr show dev eth0

    # Capture IGMP and multicast:
    tcpdump -ni eth0 'igmp or (udp port 5008)'
"""
from __future__ import annotations

import argparse
import socket
import struct
import sys
import time
from datetime import datetime


# ════════════════════════════════════════════════════════════════════════════
#  CONSTANTS
# ════════════════════════════════════════════════════════════════════════════

DEFAULT_GROUP = "239.1.1.1"  # Administratively scoped (for private networks)
DEFAULT_PORT = 5008
DEFAULT_MESSAGE = "HELLO_MCAST"
DEFAULT_TTL = 1  # 1 = link-local, does not cross the first router
BUFFER_SIZE = 65535


# ════════════════════════════════════════════════════════════════════════════
#  UTILITY FUNCTIONS
# ════════════════════════════════════════════════════════════════════════════

def timestamp() -> str:
    """Return current timestamp in human-readable format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def log(level: str, message: str) -> None:
    """Display a message with timestamp and level."""
    print(f"[{timestamp()}] [{level}] {message}")


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


def is_multicast_addr(ip: str) -> bool:
    """
    Check if IP address is in the multicast range (224.0.0.0 - 239.255.255.255).
    
    Args:
        ip: IP address string in dotted notation
        
    Returns:
        True if address is multicast, False otherwise
    """
    try:
        octets = list(map(int, ip.split(".")))
        return 224 <= octets[0] <= 239
    except (ValueError, IndexError):
        return False


# ════════════════════════════════════════════════════════════════════════════
#  SENDER MULTICAST
# ════════════════════════════════════════════════════════════════════════════

def cmd_send(args: argparse.Namespace) -> int:
    """
    Send UDP datagrams to a multicast group.
    
    Steps:
    1. Create UDP socket
    2. Set multicast TTL (IP_MULTICAST_TTL)
    3. Optional: set outgoing interface (IP_MULTICAST_IF)
    4. Transmit with sendto() to the group address
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        0 for success, 1 for error
    """
    group = args.group
    port = args.port
    base_message = args.message
    interval = args.interval
    count = args.count
    ttl = args.ttl

    # Validate address
    if not is_multicast_addr(group):
        log("ERROR", f"Address {group} is not in the multicast range (224-239)!")
        return 1

    # ─────────────────────────────────────────────────────────────────────────
    # PREDICTION CHECKPOINT
    # ─────────────────────────────────────────────────────────────────────────
    if not args.no_predict:
        prompt_prediction(
            f"With TTL={ttl}, how many router hops can this multicast packet cross?"
        )

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # ─────────────────────────────────────────────────────────────────────────
    # TTL (Time To Live) for multicast:
    # - TTL=1: Packet does NOT cross the first router (link-local)
    # - TTL>1: Packet can traverse routers (requires IGMP routing)
    # ─────────────────────────────────────────────────────────────────────────
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    # Optional: Disable loopback (do not receive own messages)
    if args.no_loopback:
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)

    # Optional: Specify outgoing interface
    if args.iface:
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(args.iface))
        log("INFO", f"Outgoing interface set: {args.iface}")

    log("INFO", f"Multicast Sender started → {group}:{port} (TTL={ttl})")
    log("INFO", f"Parameters: interval={interval}s, count={count}")

    counter = 0
    try:
        while count == 0 or counter < count:
            payload = f"{base_message} #{counter}".encode("utf-8")
            sock.sendto(payload, (group, port))
            log("SEND", f"{len(payload):4d} bytes → {group}:{port} :: {payload.decode()!r}")
            counter += 1
            time.sleep(interval)

    except KeyboardInterrupt:
        log("INFO", "Interrupted by user.")
    except OSError as e:
        log("ERROR", f"Socket error: {e}")
        return 1
    finally:
        sock.close()
        log("INFO", f"Socket closed. Total sent: {counter}")

    return 0


# ════════════════════════════════════════════════════════════════════════════
#  RECEIVER MULTICAST (with JOIN)
# ════════════════════════════════════════════════════════════════════════════

def cmd_recv(args: argparse.Namespace) -> int:
    """
    Receive UDP multicast datagrams after joining the group.
    
    Steps:
    1. Create UDP socket
    2. SO_REUSEADDR for port sharing between processes
    3. Bind to port (and optionally to group address)
    4. JOIN the group with IP_ADD_MEMBERSHIP
    5. Loop recvfrom() to receive datagrams
    6. LEAVE the group on exit (optional, OS does this automatically on close)
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        0 for success, 1 for error
    """
    group = args.group
    port = args.port
    count = args.count
    iface = args.iface
    timeout_sec = args.timeout

    if not is_multicast_addr(group):
        log("ERROR", f"Address {group} is not multicast!")
        return 1

    # ─────────────────────────────────────────────────────────────────────────
    # PREDICTION CHECKPOINT
    # ─────────────────────────────────────────────────────────────────────────
    if not args.no_predict:
        prompt_prediction(
            "What IGMP message type will be sent when you join the multicast group?"
        )

    # Create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # On some systems, SO_REUSEPORT is also needed
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    except AttributeError:
        pass  # Not available on all platforms

    # ─────────────────────────────────────────────────────────────────────────
    # Bind: for multicast, usually bind to ("", port) or (group, port)
    # Binding to the group address restricts to only that group's packets.
    # ─────────────────────────────────────────────────────────────────────────
    bind_addr = args.bind_group and group or ""
    sock.bind((bind_addr, port))
    log("INFO", f"Socket bound on {bind_addr or '*'}:{port}")

    # ─────────────────────────────────────────────────────────────────────────
    # JOIN the GROUP (IP_ADD_MEMBERSHIP)
    # Structure mreq: 4 bytes IP group + 4 bytes IP interface (or INADDR_ANY)
    # This sends an IGMP Membership Report to routers/switches
    # ─────────────────────────────────────────────────────────────────────────
    if iface:
        # Join on a specific interface
        mreq = socket.inet_aton(group) + socket.inet_aton(iface)
        log("INFO", f"JOIN group {group} on interface {iface}")
    else:
        # Join on any interface (INADDR_ANY)
        mreq = socket.inet_aton(group) + struct.pack("=I", socket.INADDR_ANY)
        log("INFO", f"JOIN group {group} on all interfaces")

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    if timeout_sec > 0:
        sock.settimeout(timeout_sec)

    log("INFO", f"Multicast Receiver active. Waiting for datagrams on {group}:{port}...")

    accepted = 0
    try:
        while count == 0 or accepted < count:
            try:
                data, (sender_ip, sender_port) = sock.recvfrom(BUFFER_SIZE)
            except socket.timeout:
                log("WARN", f"Timeout after {timeout_sec}s. Stopping.")
                break

            text = data.decode("utf-8", errors="replace")
            accepted += 1
            log("RECV", f"{len(data):4d} bytes from {sender_ip}:{sender_port} → {text!r}")

    except KeyboardInterrupt:
        log("INFO", "Interrupted by user.")
    finally:
        # ─────────────────────────────────────────────────────────────────────
        # LEAVE the group (optional - kernel does this on close())
        # Sends IGMP Leave Group message
        # ─────────────────────────────────────────────────────────────────────
        try:
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
            log("INFO", f"LEAVE group {group}")
        except OSError:
            pass
        sock.close()
        log("INFO", f"Socket closed. Received: {accepted} datagrams.")

    return 0


# ════════════════════════════════════════════════════════════════════════════
#  ARGUMENT PARSER
# ════════════════════════════════════════════════════════════════════════════

def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser with send and recv subcommands."""
    parser = argparse.ArgumentParser(
        prog="ex_3_02_udp_multicast.py",
        description="UDP Multicast sender/receiver with JOIN/LEAVE group.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Receiver with JOIN to group 239.1.1.1:
  python3 ex_3_02_udp_multicast.py recv --group 239.1.1.1 --port 5008 --count 5

  # Sender to multicast group:
  python3 ex_3_02_udp_multicast.py send --group 239.1.1.1 --port 5008 --count 5 --ttl 1

  # Verify membership on interface:
  ip maddr show dev eth0
        """
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Sender
    ps = subparsers.add_parser("send", help="Send datagrams to multicast group")
    ps.add_argument("--group", default=DEFAULT_GROUP, help=f"Multicast group address (default: {DEFAULT_GROUP})")
    ps.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Destination port (default: {DEFAULT_PORT})")
    ps.add_argument("--message", default=DEFAULT_MESSAGE, help="Message to send")
    ps.add_argument("--interval", type=float, default=1.0, help="Interval between messages (seconds)")
    ps.add_argument("--count", type=int, default=0, help="Number of messages (0=infinite)")
    ps.add_argument("--ttl", type=int, default=DEFAULT_TTL, help=f"Multicast TTL (default: {DEFAULT_TTL})")
    ps.add_argument("--iface", default="", help="Outgoing interface IP (optional)")
    ps.add_argument("--no-loopback", action="store_true", help="Disable local loopback")
    ps.add_argument("--no-predict", action="store_true", help="Skip prediction prompts")
    ps.set_defaults(func=cmd_send)

    # Receiver
    pr = subparsers.add_parser("recv", help="Receive multicast datagrams (with JOIN)")
    pr.add_argument("--group", default=DEFAULT_GROUP, help="Multicast group to JOIN")
    pr.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port to listen on")
    pr.add_argument("--count", type=int, default=0, help="Number of messages to receive (0=infinite)")
    pr.add_argument("--iface", default="", help="Interface IP for JOIN (optional)")
    pr.add_argument("--timeout", type=float, default=0.0, help="Timeout for recvfrom (0=infinite)")
    pr.add_argument("--bind-group", action="store_true", help="Bind to group address (not '')")
    pr.add_argument("--no-predict", action="store_true", help="Skip prediction prompts")
    pr.set_defaults(func=cmd_recv)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
