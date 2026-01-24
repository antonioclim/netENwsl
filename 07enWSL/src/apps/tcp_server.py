#!/usr/bin/env python3
"""
TCP Echo Server for Week 7 Demonstrations
==========================================
Computer Networks - ASE Bucharest, CSIE | by ing. dr. Antonio Clim

The server is intentionally small and predictable:
- Logs each connection and message
- Echoes back exactly what it receives
- Can stop after one connection (useful for Docker Compose demos)
- Handles multiple concurrent clients via threading

Used for:
- Baseline connectivity tests
- Filtering demonstrations (blocked vs allowed traffic)
- Packet capture analysis (visible handshake and data)
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
from typing import Optional, Tuple


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
        description="Simple TCP echo server for Week 7 demonstrations.",
        epilog="Server echoes back all received data verbatim."
    )
    p.add_argument(
        "--host", 
        default="0.0.0.0", 
        help="Bind address (default: 0.0.0.0 = all interfaces)"
    )
    p.add_argument(
        "--port", 
        type=int, 
        default=9090, 
        help="Bind port (default: 9090)"
    )
    p.add_argument(
        "--log", 
        default="", 
        help="Optional log file path"
    )
    p.add_argument(
        "--once", 
        action="store_true", 
        help="Exit after handling a single client"
    )
    p.add_argument(
        "--timeout", 
        type=float, 
        default=10.0, 
        help="Socket timeout in seconds (default: 10)"
    )
    return p


# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING_UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════
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
# CLIENT_HANDLER
# ═══════════════════════════════════════════════════════════════════════════════
def handle_client(
    conn: socket.socket, 
    addr: Tuple[str, int], 
    log_path: Optional[Path], 
    timeout: float
) -> None:
    """
    Handle a single client connection.
    
    Receives data from client and echoes it back verbatim.
    Runs in a separate thread for each client.
    
    Args:
        conn: Connected client socket
        addr: Client address tuple (ip, port)
        log_path: Optional path for logging
        timeout: Socket timeout in seconds
    """
    conn.settimeout(timeout)
    log_line(log_path, f"client connected from {addr[0]}:{addr[1]}")
    
    try:
        # ═══════════════════════════════════════════════════════════════════════
        # RECEIVE_DATA
        # ═══════════════════════════════════════════════════════════════════════
        data = conn.recv(4096)
        if not data:
            log_line(log_path, "client sent no data")
            return
            
        # Log received data (decode for display only)
        try:
            text = data.decode("utf-8", errors="replace").strip()
        except Exception:
            text = "<decode error>"
        log_line(log_path, f"received: {text}")
        
        # ═══════════════════════════════════════════════════════════════════════
        # ECHO_RESPONSE
        # ═══════════════════════════════════════════════════════════════════════
        conn.sendall(data)
        log_line(log_path, "echoed back data")
        
    except socket.timeout:
        log_line(log_path, "client read timed out")
    except Exception as exc:
        log_line(log_path, f"error: {exc}")
        
    # ═══════════════════════════════════════════════════════════════════════════
    # CLEANUP_CONNECTION
    # ═══════════════════════════════════════════════════════════════════════════
    finally:
        try:
            conn.close()
        except Exception:
            pass
        log_line(log_path, "client connection closed")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_SERVER_LOOP
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """
    Main entry point for TCP server.
    
    Creates listening socket and accepts client connections.
    Each client is handled in a separate thread.
    
    Returns:
        Exit code (always 0)
    """
    args = build_parser().parse_args()
    log_path = Path(args.log) if args.log else None

    # ═══════════════════════════════════════════════════════════════════════════
    # CREATE_SERVER_SOCKET
    # ═══════════════════════════════════════════════════════════════════════════
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((args.host, args.port))
    srv.listen(50)
    log_line(log_path, f"listening on {args.host}:{args.port}")

    # ═══════════════════════════════════════════════════════════════════════════
    # ACCEPT_LOOP
    # ═══════════════════════════════════════════════════════════════════════════
    handled = 0
    try:
        while True:
            conn, addr = srv.accept()
            th = threading.Thread(
                target=handle_client, 
                args=(conn, addr, log_path, args.timeout), 
                daemon=True
            )
            th.start()
            handled += 1
            
            if args.once and handled >= 1:
                # Give the handler a moment to flush logs
                time.sleep(0.2)
                break
                
    except KeyboardInterrupt:
        log_line(log_path, "interrupted")
        
    # ═══════════════════════════════════════════════════════════════════════════
    # CLEANUP_SERVER
    # ═══════════════════════════════════════════════════════════════════════════
    finally:
        try:
            srv.close()
        except Exception:
            pass
        log_line(log_path, "server stopped")
        
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
