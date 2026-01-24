#!/usr/bin/env python3
"""
User-Space TCP Proxy Filter for Week 7 Demonstrations
======================================================
Computer Networks - ASE Bucharest, CSIE | by ing. dr. Antonio Clim

This is an educational tool demonstrating:
- Interception at the application layer (user space)
- Allow/block lists based on source IP
- Bidirectional TCP proxying

It is NOT a replacement for iptables-based filtering:
- iptables works at kernel level (faster, more secure)
- This proxy only sees connections that reach it
- Real firewalls should use iptables, nftables, or similar

Use cases:
- Understanding application-layer filtering
- Logging and inspecting traffic
- Simple access control without root privileges
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import socket
import threading
import time
from pathlib import Path
from typing import Optional, Set, Tuple


# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGUMENTS
# ═══════════════════════════════════════════════════════════════════════════════
def build_parser() -> argparse.ArgumentParser:
    """
    Build command-line argument parser.
    
    Returns:
        Configured ArgumentParser instance
    """
    p = argparse.ArgumentParser(
        description="TCP proxy filter for Week 7 demonstrations.",
        epilog="Forwards connections to upstream server with optional IP filtering."
    )
    p.add_argument(
        "--listen-host", 
        default="0.0.0.0", 
        help="Proxy bind address (default: 0.0.0.0)"
    )
    p.add_argument(
        "--listen-port", 
        type=int, 
        default=8888, 
        help="Proxy bind port (default: 8888)"
    )
    p.add_argument(
        "--upstream-host", 
        required=True, 
        help="Upstream server host"
    )
    p.add_argument(
        "--upstream-port", 
        type=int, 
        default=9090, 
        help="Upstream server port (default: 9090)"
    )
    p.add_argument(
        "--allow", 
        default="", 
        help="Comma-separated allowed source IPs (empty = allow all)"
    )
    p.add_argument(
        "--block", 
        default="", 
        help="Comma-separated blocked source IPs (empty = block none)"
    )
    p.add_argument(
        "--log", 
        default="", 
        help="Optional log file path"
    )
    p.add_argument(
        "--timeout", 
        type=float, 
        default=5.0, 
        help="Socket timeout in seconds (default: 5)"
    )
    return p


# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def parse_ip_set(s: str) -> Set[str]:
    """
    Parse comma-separated IP list into a set.
    
    Args:
        s: Comma-separated string of IP addresses
        
    Returns:
        Set of IP address strings
    """
    out: Set[str] = set()
    for part in s.split(","):
        part = part.strip()
        if part:
            out.add(part)
    return out


def log_line(path: Optional[Path], line: str) -> None:
    """
    Log a message to console and optionally to file.
    
    Args:
        path: Optional path to log file (None for console only)
        line: Message to log
    """
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{stamp}] {line}"
    print(msg, flush=True)
    if path:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as f:
            f.write(msg + "\n")


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_FORWARDING
# ═══════════════════════════════════════════════════════════════════════════════
def pipe(src: socket.socket, dst: socket.socket, buf: int = 4096) -> None:
    """
    Forward data from source socket to destination socket.
    
    Runs until source closes or error occurs.
    
    Args:
        src: Source socket to read from
        dst: Destination socket to write to
        buf: Buffer size for reads
    """
    try:
        while True:
            data = src.recv(buf)
            if not data:
                break
            dst.sendall(data)
    except Exception:
        pass
    finally:
        try:
            dst.shutdown(socket.SHUT_WR)
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════════════════════════
# CONNECTION_HANDLER
# ═══════════════════════════════════════════════════════════════════════════════
def handle(
    conn: socket.socket, 
    addr: Tuple[str, int], 
    upstream: Tuple[str, int], 
    allow: Set[str], 
    block: Set[str], 
    log_path: Optional[Path], 
    timeout: float
) -> None:
    """
    Handle a single client connection.
    
    Checks allow/block lists, then forwards traffic bidirectionally
    between client and upstream server.
    
    Args:
        conn: Client socket
        addr: Client address (ip, port)
        upstream: Upstream server (host, port)
        allow: Set of allowed IPs (empty = allow all)
        block: Set of blocked IPs
        log_path: Optional log file path
        timeout: Socket timeout
    """
    src_ip = addr[0]
    conn.settimeout(timeout)

    # ═══════════════════════════════════════════════════════════════════════════
    # CHECK_ACCESS_POLICY
    # ═══════════════════════════════════════════════════════════════════════════
    if src_ip in block or (allow and src_ip not in allow):
        log_line(log_path, f"BLOCKED connection from {src_ip}:{addr[1]}")
        try:
            conn.close()
        except Exception:
            pass
        return

    log_line(log_path, f"ALLOWED connection from {src_ip}:{addr[1]} -> {upstream[0]}:{upstream[1]}")

    # ═══════════════════════════════════════════════════════════════════════════
    # CONNECT_TO_UPSTREAM
    # ═══════════════════════════════════════════════════════════════════════════
    up = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    up.settimeout(timeout)
    try:
        up.connect(upstream)
    except Exception as exc:
        log_line(log_path, f"upstream connect failed: {exc}")
        try:
            conn.close()
        except Exception:
            pass
        return

    # ═══════════════════════════════════════════════════════════════════════════
    # BIDIRECTIONAL_FORWARDING
    # ═══════════════════════════════════════════════════════════════════════════
    t1 = threading.Thread(target=pipe, args=(conn, up), daemon=True)
    t2 = threading.Thread(target=pipe, args=(up, conn), daemon=True)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    # ═══════════════════════════════════════════════════════════════════════════
    # CLEANUP_CONNECTIONS
    # ═══════════════════════════════════════════════════════════════════════════
    try:
        conn.close()
    except Exception:
        pass
    try:
        up.close()
    except Exception:
        pass

    log_line(log_path, f"connection closed for {src_ip}:{addr[1]}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_PROXY_LOOP
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """
    Main entry point for proxy filter.
    
    Creates listening socket and accepts client connections.
    Each client is handled in a separate thread.
    
    Returns:
        Exit code (always 0)
    """
    args = build_parser().parse_args()
    allow = parse_ip_set(args.allow)
    block = parse_ip_set(args.block)
    log_path = Path(args.log) if args.log else None

    # ═══════════════════════════════════════════════════════════════════════════
    # CREATE_PROXY_SOCKET
    # ═══════════════════════════════════════════════════════════════════════════
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((args.listen_host, args.listen_port))
    srv.listen(50)

    upstream = (args.upstream_host, args.upstream_port)
    log_line(
        log_path, 
        f"proxy listening on {args.listen_host}:{args.listen_port} -> {upstream[0]}:{upstream[1]}"
    )
    
    if allow:
        log_line(log_path, f"allow list: {', '.join(sorted(allow))}")
    if block:
        log_line(log_path, f"block list: {', '.join(sorted(block))}")

    # ═══════════════════════════════════════════════════════════════════════════
    # ACCEPT_LOOP
    # ═══════════════════════════════════════════════════════════════════════════
    try:
        while True:
            conn, addr = srv.accept()
            th = threading.Thread(
                target=handle, 
                args=(conn, addr, upstream, allow, block, log_path, args.timeout), 
                daemon=True
            )
            th.start()
    except KeyboardInterrupt:
        log_line(log_path, "interrupted")
        
    # ═══════════════════════════════════════════════════════════════════════════
    # CLEANUP_PROXY
    # ═══════════════════════════════════════════════════════════════════════════
    finally:
        try:
            srv.close()
        except Exception:
            pass
        log_line(log_path, "proxy stopped")
        
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
