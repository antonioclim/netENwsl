#!/usr/bin/env python3
"""
TCP Client for Week 7 Demonstrations
====================================
Computer Networks - ASE Bucharest, CSIE | by ing. dr. Antonio Clim

Sends a single message to a TCP server and checks the echo response.
Used for baseline connectivity tests and filtering demonstrations.

The server is intentionally small and predictable:
- Connects to specified host:port
- Sends message with newline terminator
- Waits for echo response
- Verifies response matches sent message
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import socket
import time
from pathlib import Path
from typing import Optional


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
        description="Simple TCP client for Week 7 demonstrations.",
        epilog="Exit codes: 0=success, 2=no response, 3=mismatch, 4=timeout, 5=refused, 6=error"
    )
    p.add_argument(
        "--host", 
        required=True, 
        help="Server address or hostname"
    )
    p.add_argument(
        "--port", 
        type=int, 
        default=9090, 
        help="Server port (default: 9090)"
    )
    p.add_argument(
        "--message", 
        default="hello", 
        help="Message to send (default: hello)"
    )
    p.add_argument(
        "--timeout", 
        type=float, 
        default=3.0, 
        help="Timeout in seconds (default: 3)"
    )
    p.add_argument(
        "--log", 
        default="", 
        help="Optional log file path"
    )
    p.add_argument(
        "--predict",
        action="store_true",
        help="Enable prediction prompt before connection"
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
# PREDICTION_PROMPT
# ═══════════════════════════════════════════════════════════════════════════════
def prompt_prediction() -> None:
    """
    Display prediction prompt before connection attempt.
    
    Implements Brown & Wilson Principle 4: Predictions.
    """
    print()
    print("💭 PREDICTION: What will happen when we try to connect?")
    print("   Consider: Is the server running? Is there a firewall rule?")
    print("   Options: (a) Success  (b) Timeout  (c) Connection refused")
    input("   Press Enter after making your prediction...")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_CONNECTION_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """
    Main entry point for TCP client.
    
    Returns:
        Exit code indicating result:
        - 0: Success (echo matched)
        - 2: No response received
        - 3: Echo mismatch
        - 4: Timeout
        - 5: Connection refused
        - 6: Other error
    """
    args = build_parser().parse_args()
    log_path = Path(args.log) if args.log else None

    # ═══════════════════════════════════════════════════════════════════════════
    # OPTIONAL_PREDICTION
    # ═══════════════════════════════════════════════════════════════════════════
    if args.predict:
        prompt_prediction()

    # ═══════════════════════════════════════════════════════════════════════════
    # CREATE_SOCKET
    # ═══════════════════════════════════════════════════════════════════════════
    msg_bytes = (args.message + "\n").encode("utf-8")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(args.timeout)

    # ═══════════════════════════════════════════════════════════════════════════
    # CONNECT_AND_EXCHANGE
    # ═══════════════════════════════════════════════════════════════════════════
    try:
        log_line(log_path, f"connecting to {args.host}:{args.port}")
        s.connect((args.host, args.port))
        
        s.sendall(msg_bytes)
        
        data = s.recv(4096)
        if not data:
            log_line(log_path, "no response received")
            return 2
            
        echoed = data.decode("utf-8", errors="replace").strip()
        log_line(log_path, f"received: {echoed}")
        
        # ═══════════════════════════════════════════════════════════════════════
        # VERIFY_RESPONSE
        # ═══════════════════════════════════════════════════════════════════════
        if echoed != args.message:
            log_line(log_path, "echo mismatch")
            return 3
            
        log_line(log_path, "ok")
        return 0
        
    except socket.timeout:
        log_line(log_path, "timeout (possible DROP rule or server not responding)")
        return 4
    except ConnectionRefusedError:
        log_line(log_path, "connection refused (port closed or REJECT rule)")
        return 5
    except Exception as exc:
        log_line(log_path, f"error: {exc}")
        return 6
        
    # ═══════════════════════════════════════════════════════════════════════════
    # CLEANUP
    # ═══════════════════════════════════════════════════════════════════════════
    finally:
        try:
            s.close()
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
