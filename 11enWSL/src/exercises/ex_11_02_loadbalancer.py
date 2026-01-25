#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
  Exercise 11.02 – Python Load Balancer (Reverse Proxy)
═══════════════════════════════════════════════════════════════════════════════

EDUCATIONAL PURPOSE:
  - See concretely what "accept, pick backend, forward, return response" means
  - Implement distribution algorithms (round-robin, least_conn, ip_hash)
  - Understand passive failover (similar to max_fails/fail_timeout in Nginx)

LEVEL: Intermediate
ESTIMATED TIME: 20 minutes

PAIR PROGRAMMING NOTES:
  - Driver: Start the load balancer, configure algorithms
  - Navigator: Monitor distribution pattern, calculate expected behaviour
  - Swap after: Testing each algorithm (rr, least_conn, ip_hash)

NOTE:
  - The proxy operates at simplified TCP/HTTP level (for common GET/HEAD)
  - Does not fully implement HTTP keep-alive/pipelining

USAGE (proxy):
  python3 ex_11_02_loadbalancer.py --listen 0.0.0.0:8080 \\
      --backends localhost:8081,localhost:8082,localhost:8083 \\
      --algo rr

USAGE (load generator):
  python3 ex_11_02_loadbalancer.py loadgen --url http://localhost:8080/ --n 200 --c 10

PREDICTION PROMPTS:
  💭 Before testing rr: If you send 9 requests to 3 backends, how many will each receive?
  💭 Before testing ip_hash: Will consecutive requests from localhost go to the same backend?
  💭 Before stopping a backend: What HTTP status code will the first failed request return?

ALGORITHMS:
  - rr (round-robin): Rotate through backends sequentially
  - least_conn: Route to backend with fewest active connections
  - ip_hash: Hash client IP for sticky sessions

═══════════════════════════════════════════════════════════════════════════════
NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim
═══════════════════════════════════════════════════════════════════════════════
"""
from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import argparse
import socket
import threading
import time
import urllib.parse
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

try:
    from src.utils.net_utils import (
        recv_until, parse_http_content_length, recv_exact,
        connect_tcp, set_timeouts, now_s
    )
except ImportError:
    from python.utils.net_utils import (
        recv_until, parse_http_content_length, recv_exact,
        connect_tcp, set_timeouts, now_s
    )


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
BUFFER_SIZE = 4096
MAX_RESPONSE_SIZE = 5_000_000


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Backend:
    """
    Represents a backend server with health tracking.

    Attributes:
        host: Backend hostname or IP address
        port: Backend port number
        active: Current number of active connections (for least_conn)
        fails: Consecutive failure count
        down_until: Timestamp until which backend is considered down
    """
    host: str
    port: int
    active: int = 0
    fails: int = 0
    down_until: float = 0.0

    def addr(self) -> Tuple[str, int]:
        """Return (host, port) tuple."""
        return (self.host, self.port)

    def is_down(self, t: float) -> bool:
        """Check if backend is currently marked as down."""
        return t < self.down_until


# ═══════════════════════════════════════════════════════════════════════════════
# LOAD_BALANCER_CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class LoadBalancer:
    """
    Load balancer with multiple distribution algorithms.

    Supports:
    - Round-robin (rr): Cycle through backends sequentially
    - Least connections (least_conn): Route to least busy backend
    - IP hash (ip_hash): Consistent hashing for session affinity
    """

    def __init__(self,
                 backends: List[Backend],
                 algo: str,
                 passive_failures: int,
                 fail_timeout_s: float,
                 sock_timeout: float):
        """
        Initialise the load balancer.

        Args:
            backends: List of Backend objects
            algo: Algorithm name ('rr', 'least_conn', 'ip_hash')
            passive_failures: Failures before marking backend down
            fail_timeout_s: Seconds to keep backend marked down
            sock_timeout: Socket timeout for backend connections
        """
        self.backends = backends
        self.algo = algo
        self.passive_failures = passive_failures
        self.fail_timeout_s = fail_timeout_s
        self.sock_timeout = sock_timeout
        self._rr_idx = 0
        self._lock = threading.Lock()

    # ─── ALGORITHM: ROUND-ROBIN ─────────────────────────────────────────────
    def _pick_rr(self, client_ip: str) -> Optional[Backend]:
        """Select next backend using round-robin."""
        with self._lock:
            n = len(self.backends)
            for _ in range(n):
                b = self.backends[self._rr_idx]
                self._rr_idx = (self._rr_idx + 1) % n
                if not b.is_down(now_s()):
                    return b
        return None

    # ─── ALGORITHM: LEAST CONNECTIONS ───────────────────────────────────────
    def _pick_least_conn(self, client_ip: str) -> Optional[Backend]:
        """Select backend with fewest active connections."""
        with self._lock:
            alive = [b for b in self.backends if not b.is_down(now_s())]
            if not alive:
                return None
            alive.sort(key=lambda b: (b.active, b.fails, b.host, b.port))
            return alive[0]

    # ─── ALGORITHM: IP HASH ─────────────────────────────────────────────────
    def _pick_ip_hash(self, client_ip: str) -> Optional[Backend]:
        """Select backend using client IP hash (sticky sessions)."""
        with self._lock:
            alive = [b for b in self.backends if not b.is_down(now_s())]
            if not alive:
                return None
            h = 0
            for ch in client_ip:
                h = (h * 131 + ord(ch)) & 0xFFFFFFFF
            return alive[h % len(alive)]

    # ─── BACKEND SELECTION ──────────────────────────────────────────────────
    def pick(self, client_ip: str) -> Optional[Backend]:
        """Select a backend using the configured algorithm."""
        if self.algo == "rr":
            return self._pick_rr(client_ip)
        if self.algo == "least_conn":
            return self._pick_least_conn(client_ip)
        if self.algo == "ip_hash":
            return self._pick_ip_hash(client_ip)
        raise ValueError(f"Unknown algorithm: {self.algo}")

    # ─── HEALTH TRACKING ────────────────────────────────────────────────────
    def mark_success(self, b: Backend) -> None:
        """Mark backend as healthy after successful request."""
        with self._lock:
            b.fails = 0

    def mark_failure(self, b: Backend) -> None:
        """Record backend failure and mark down if threshold reached."""
        with self._lock:
            b.fails += 1
            if self.passive_failures > 0 and b.fails >= self.passive_failures:
                b.down_until = now_s() + self.fail_timeout_s

    def inc_active(self, b: Backend) -> None:
        """Increment active connection count."""
        with self._lock:
            b.active += 1

    def dec_active(self, b: Backend) -> None:
        """Decrement active connection count."""
        with self._lock:
            b.active = max(0, b.active - 1)


# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_BACKENDS
# ═══════════════════════════════════════════════════════════════════════════════

def parse_backends(s: str) -> List[Backend]:
    """Parse backend string into list of Backend objects."""
    out: List[Backend] = []
    for item in s.split(","):
        item = item.strip()
        if not item:
            continue
        host, port_s = item.split(":")
        out.append(Backend(host=host, port=int(port_s)))
    if not out:
        raise ValueError("Backend list is empty.")
    return out


# ═══════════════════════════════════════════════════════════════════════════════
# REQUEST_HANDLING_HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def _read_client_request(client_sock: socket.socket) -> Optional[bytes]:
    """Read complete HTTP request from client socket."""
    req_head = recv_until(client_sock)
    if not req_head:
        return None
    content_len = parse_http_content_length(req_head)
    body = b""
    if content_len > 0:
        body = recv_exact(client_sock, content_len)
    return req_head + body


def _send_error_response(client_sock: socket.socket,
                         status: int, message: str) -> None:
    """Send HTTP error response to client."""
    status_messages = {502: "Bad Gateway", 503: "Service Unavailable"}
    status_text = status_messages.get(status, "Error")
    response = (
        f"HTTP/1.1 {status} {status_text}\r\n"
        f"Connection: close\r\n\r\n"
        f"{message}\n"
    ).encode("utf-8")
    client_sock.sendall(response)


def _forward_to_backend(request_data: bytes, backend: Backend,
                        timeout: float) -> Optional[bytes]:
    """Forward request to backend and return response."""
    try:
        with connect_tcp(backend.host, backend.port, timeout=timeout) as be:
            be.sendall(request_data)
            response = b""
            while True:
                chunk = be.recv(BUFFER_SIZE)
                if not chunk:
                    break
                response += chunk
                if len(response) > MAX_RESPONSE_SIZE:
                    break
            return response
    except Exception:
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# FORWARD_REQUEST
# ═══════════════════════════════════════════════════════════════════════════════

def forward_one_request(client_sock: socket.socket,
                        client_addr: Tuple[str, int],
                        lb: LoadBalancer) -> None:
    """Read an HTTP request and forward it to a selected backend."""
    client_ip = client_addr[0]
    set_timeouts(client_sock, lb.sock_timeout)

    # ─── READ_CLIENT_REQUEST ────────────────────────────────────────────────
    request_data = _read_client_request(client_sock)
    if not request_data:
        return

    # ─── SELECT_BACKEND ─────────────────────────────────────────────────────
    backend = lb.pick(client_ip)
    if backend is None:
        _send_error_response(client_sock, 503, "No backends available")
        return

    # ─── FORWARD_WITH_RETRY ─────────────────────────────────────────────────
    lb.inc_active(backend)
    try:
        _try_forward_with_retry(client_sock, request_data, backend, lb, client_ip)
    finally:
        lb.dec_active(backend)


def _try_forward_with_retry(client_sock: socket.socket, request_data: bytes,
                            backend: Backend, lb: LoadBalancer,
                            client_ip: str) -> None:
    """Attempt to forward request with one retry on failure."""
    for attempt in (1, 2):
        response = _forward_to_backend(request_data, backend, lb.sock_timeout)
        if response is not None:
            client_sock.sendall(response)
            lb.mark_success(backend)
            return

        lb.mark_failure(backend)
        if attempt == 2:
            _send_error_response(client_sock, 502, "Bad Gateway")
            return

        backend = lb.pick(client_ip)
        if backend is None:
            _send_error_response(client_sock, 503, "No backends available")
            return


# ═══════════════════════════════════════════════════════════════════════════════
# RUN_PROXY_SERVER
# ═══════════════════════════════════════════════════════════════════════════════

def run_proxy(args: argparse.Namespace) -> None:
    """Start the load balancer proxy server."""
    backends = parse_backends(args.backends)
    lb = LoadBalancer(
        backends=backends,
        algo=args.algo,
        passive_failures=args.passive_failures,
        fail_timeout_s=args.fail_timeout,
        sock_timeout=args.sock_timeout,
    )
    host, port_s = args.listen.split(":")
    port = int(port_s)

    # ─── DISPLAY_CONFIGURATION ──────────────────────────────────────────────
    print(f"[LB] listen {host}:{port} | algo={args.algo} | "
          f"backends={[(b.host, b.port) for b in backends]}")
    print(f"[LB] passive_failures={args.passive_failures} "
          f"fail_timeout={args.fail_timeout}s sock_timeout={args.sock_timeout}s")

    # ─── ACCEPT_LOOP ────────────────────────────────────────────────────────
    _run_accept_loop(host, port, lb)


def _run_accept_loop(host: str, port: int, lb: LoadBalancer) -> None:
    """Run the main accept loop for incoming connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(128)
        while True:
            client_sock, client_addr = s.accept()
            t = threading.Thread(
                target=_handle_client,
                args=(client_sock, client_addr, lb),
                daemon=True
            )
            t.start()


def _handle_client(client_sock: socket.socket, client_addr,
                   lb: LoadBalancer) -> None:
    """Handle a single client connection."""
    try:
        forward_one_request(client_sock, client_addr, lb)
    except Exception:
        _send_internal_error(client_sock)
    finally:
        _close_socket_safely(client_sock)


def _send_internal_error(client_sock: socket.socket) -> None:
    """Send 500 Internal Server Error response."""
    try:
        client_sock.sendall(
            b"HTTP/1.1 500 Internal Server Error\r\n"
            b"Connection: close\r\n\r\n"
            b"Internal Error\n"
        )
    except Exception:
        pass


def _close_socket_safely(sock: socket.socket) -> None:
    """Close socket ignoring any errors."""
    try:
        sock.close()
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════════════════════
# LOAD_GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════

def http_get_once(url: str, timeout: float = 2.5) -> Tuple[int, float]:
    """Perform a single HTTP GET request."""
    u = urllib.parse.urlparse(url)
    host = u.hostname or "127.0.0.1"
    port = u.port or (443 if u.scheme == "https" else 80)
    path = u.path or "/"
    if u.query:
        path += "?" + u.query

    t0 = time.time()
    status, _ = _execute_http_get(host, port, path, timeout)
    return status, (time.time() - t0)


def _execute_http_get(host: str, port: int, path: str,
                      timeout: float) -> Tuple[int, bytes]:
    """Execute HTTP GET and return status code and body."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        s.connect((host, port))
        req = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"User-Agent: s11-loadgen/0.1\r\n"
            f"Connection: close\r\n\r\n"
        ).encode("ascii", errors="replace")
        s.sendall(req)
        head = recv_until(s, max_bytes=65536)
        status = _parse_status_code(head)
        _consume_response_body(s)
        return status, head


def _parse_status_code(head: bytes) -> int:
    """Parse HTTP status code from response header."""
    try:
        line = head.split(b"\r\n", 1)[0].decode("ascii", errors="replace")
        return int(line.split()[1])
    except Exception:
        return 0


def _consume_response_body(sock: socket.socket) -> None:
    """Read and discard remaining response body."""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break


def run_loadgen(args: argparse.Namespace) -> None:
    """Run the load generator for benchmarking."""
    url, n, c, timeout = args.url, args.n, args.c, args.timeout
    latencies: List[float] = []
    statuses: Dict[int, int] = {}
    lock = threading.Lock()
    counter = {"sent": 0}
    start = time.time()

    def worker():
        while True:
            with lock:
                if counter["sent"] >= n:
                    return
                counter["sent"] += 1
            st, lat = http_get_once(url, timeout=timeout)
            with lock:
                latencies.append(lat)
                statuses[st] = statuses.get(st, 0) + 1

    threads = [threading.Thread(target=worker) for _ in range(c)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    _display_loadgen_results(url, n, c, time.time() - start, latencies, statuses)


def _display_loadgen_results(url: str, n: int, c: int, dur: float,
                             latencies: List[float],
                             statuses: Dict[int, int]) -> None:
    """Display load generator results."""
    latencies_sorted = sorted(latencies)

    def pct(p: float) -> float:
        if not latencies_sorted:
            return 0.0
        idx = int((p / 100.0) * (len(latencies_sorted) - 1))
        return latencies_sorted[idx]

    rps = (n / dur) if dur > 0 else 0.0
    print(f"[loadgen] url={url}")
    print(f"[loadgen] n={n} c={c} duration={dur:.3f}s rps={rps:.2f}")
    print(f"[loadgen] status_counts={dict(sorted(statuses.items()))}")
    print(f"[loadgen] latency_s: p50={pct(50):.4f} p90={pct(90):.4f} "
          f"p95={pct(95):.4f} p99={pct(99):.4f}")


# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGUMENTS
# ═══════════════════════════════════════════════════════════════════════════════

def build_argparser() -> argparse.ArgumentParser:
    """Build command-line argument parser."""
    p = argparse.ArgumentParser(
        description="Python Load Balancer with multiple algorithms",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start load balancer with round-robin
  %(prog)s --backends localhost:8081,localhost:8082,localhost:8083 --algo rr

  # Start with IP hash for sticky sessions
  %(prog)s --backends localhost:8081,localhost:8082,localhost:8083 --algo ip_hash

  # Run load generator
  %(prog)s loadgen --url http://localhost:8080/ --n 500 --c 20
        """
    )
    sub = p.add_subparsers(dest="cmd")
    p.add_argument("--listen", type=str, default="0.0.0.0:8080",
                   help="Listen address (default: 0.0.0.0:8080)")
    p.add_argument("--backends", type=str,
                   default="localhost:8081,localhost:8082,localhost:8083",
                   help="Comma-separated backend list (host:port)")
    p.add_argument("--algo", type=str, choices=["rr", "least_conn", "ip_hash"],
                   default="rr", help="Load balancing algorithm")
    p.add_argument("--passive-failures", type=int, default=1,
                   help="Failures before marking backend down")
    p.add_argument("--fail-timeout", type=float, default=10.0,
                   help="Seconds to keep backend marked down")
    p.add_argument("--sock-timeout", type=float, default=2.5,
                   help="Socket timeout for backend connections")

    p_lg = sub.add_parser("loadgen", help="Run load generator")
    p_lg.add_argument("--url", type=str, required=True, help="Target URL")
    p_lg.add_argument("--n", type=int, default=200, help="Number of requests")
    p_lg.add_argument("--c", type=int, default=10, help="Concurrency level")
    p_lg.add_argument("--timeout", type=float, default=2.5, help="Request timeout")

    return p


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    """Entry point."""
    p = build_argparser()
    args = p.parse_args()
    if args.cmd == "loadgen":
        run_loadgen(args)
        return
    run_proxy(args)


if __name__ == "__main__":
    main()
