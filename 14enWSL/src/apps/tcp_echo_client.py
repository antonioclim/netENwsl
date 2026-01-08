#!/usr/bin/env python3
"""tcp_echo_client.py — TCP echo client for demonstrations.

Features:
  - Connects to a TCP server
  - Sends a message and verifies the echo
  - Reports latency and validity

Usage:
  python3 tcp_echo_client.py --host localhost --port 9090 --message "hello"

NOTE: Port 9090 is used for TCP Echo (port 9000 is reserved for Portainer)
"""

from __future__ import annotations

import argparse
import socket
import sys
import time
from datetime import datetime


def log(msg: str) -> None:
    """Logging with timestamp."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print(f"[{ts}] [echo-client] {msg}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TCP Echo Client")
    parser.add_argument("--host", required=True, help="Server address")
    parser.add_argument("--port", type=int, default=9090, help="Server port (default: 9090)")
    parser.add_argument("--message", default="hello", help="Message to send")
    parser.add_argument("--timeout", type=float, default=5.0, help="Timeout (s)")
    parser.add_argument("--repeat", type=int, default=1, help="Number of times to repeat")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    
    success_count = 0
    
    for i in range(args.repeat):
        if args.repeat > 1:
            log(f"--- Iteration {i + 1}/{args.repeat} ---")
        
        log(f"Connecting to {args.host}:{args.port}...")
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(args.timeout)
        
        try:
            start = time.time()
            sock.connect((args.host, args.port))
            connect_time = (time.time() - start) * 1000
            log(f"Connected (connect time: {connect_time:.2f} ms)")
            
            message = args.message.encode("utf-8")
            log(f"Sending: {message!r}")
            
            start = time.time()
            sock.sendall(message)
            
            response = sock.recv(4096)
            rtt = (time.time() - start) * 1000
            
            log(f"Received: {response!r}")
            log(f"RTT: {rtt:.2f} ms")
            
            if response == message:
                log("✓ Echo valid")
                success_count += 1
            else:
                log("✗ Echo mismatch!")
        
        except socket.timeout:
            log("✗ Connection timeout")
        except ConnectionRefusedError:
            log("✗ Connection refused")
        except Exception as e:
            log(f"✗ Error: {e}")
        finally:
            sock.close()
    
    if args.repeat > 1:
        log(f"Results: {success_count}/{args.repeat} successful")
    
    return 0 if success_count == args.repeat else 1


if __name__ == "__main__":
    raise SystemExit(main())
