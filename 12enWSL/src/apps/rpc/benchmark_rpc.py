#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_DOCSTRING
# ═══════════════════════════════════════════════════════════════════════════════
"""Week 12 — RPC benchmark (JSON-RPC versus XML-RPC).

This benchmark is intentionally simple and local:
- JSON-RPC: HTTP POST with a small JSON payload
- XML-RPC: HTTP POST with an XML payload via xmlrpc.client

It measures wall-clock time for a fixed number of calls to an 'add' method.

Recommended usage (auto-start wrapper):
  ./scripts/benchmark_rpc.sh --calls 2000

Direct usage (servers must already be running):
  python src/rpc/benchmark_rpc.py --jsonrpc-url http://127.0.0.1:6200 --xmlrpc-url http://127.0.0.1:6201 --calls 2000
"""


# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import http.client
from dataclasses import dataclass
from typing import Any
import xmlrpc.client


@dataclass

# ═══════════════════════════════════════════════════════════════════════════════
# BENCHRESULT_CLASS
# ═══════════════════════════════════════════════════════════════════════════════
class BenchResult:
    name: str
    calls: int
    seconds: float

    @property
    def calls_per_second(self) -> float:
        return self.calls / self.seconds if self.seconds > 0 else float("inf")

    @property
    def avg_ms(self) -> float:
        return (self.seconds / self.calls) * 1000 if self.calls > 0 else 0.0



# ═══════════════════════════════════════════════════════════════════════════════
# JSONRPC_CALL_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def jsonrpc_call(conn: http.client.HTTPConnection, path: str, a: int, b: int, req_id: int) -> Any:
    payload = {
        "jsonrpc": "2.0",
        "id": req_id,
        "method": "add",
        "params": [a, b],
    }
    body = json.dumps(payload).encode("utf-8")
    conn.request("POST", path, body=body, headers={"Content-Type": "application/json"})
    resp = conn.getresponse()
    data = resp.read()
    if resp.status != 200:
        raise RuntimeError(f"JSON-RPC HTTP {resp.status}: {data[:200]!r}")
    obj = json.loads(data.decode("utf-8"))
    if "error" in obj and obj["error"] is not None:
        raise RuntimeError(f"JSON-RPC error: {obj['error']!r}")
    return obj.get("result")



# ═══════════════════════════════════════════════════════════════════════════════
# BENCH_JSONRPC_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def bench_jsonrpc(url: str, calls: int, warmup: int = 10) -> BenchResult:
    parsed = urllib.parse.urlparse(url)
    if not parsed.hostname or not parsed.port:
        raise ValueError(f"Invalid JSON-RPC URL: {url!r} (expected http://host:port)")
    host = parsed.hostname
    port = parsed.port
    path = parsed.path or "/"

    conn = http.client.HTTPConnection(host, port, timeout=3)

    # Warmup
    for i in range(warmup):
        jsonrpc_call(conn, path, 1, 2, i)

    start = time.perf_counter()
    for i in range(calls):
        r = jsonrpc_call(conn, path, 10, 32, i + 1000)
        if r != 42:
            raise RuntimeError(f"Unexpected JSON-RPC result: {r!r}")
    end = time.perf_counter()
    conn.close()
    return BenchResult(name="JSON-RPC", calls=calls, seconds=end - start)



# ═══════════════════════════════════════════════════════════════════════════════
# BENCH_XMLRPC_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def bench_xmlrpc(url: str, calls: int, warmup: int = 10) -> BenchResult:
    # xmlrpc.client expects a full URL with scheme and host.
    proxy = xmlrpc.client.ServerProxy(url, allow_none=True)

    # Warmup
    for _ in range(warmup):
        proxy.add(1, 2)

    start = time.perf_counter()
    for _ in range(calls):
        r = proxy.add(10, 32)
        if r != 42:
            raise RuntimeError(f"Unexpected XML-RPC result: {r!r}")
    end = time.perf_counter()
    return BenchResult(name="XML-RPC", calls=calls, seconds=end - start)



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    ap = argparse.ArgumentParser(description="Benchmark JSON-RPC versus XML-RPC (Week 12).")
    ap.add_argument("--jsonrpc-url", required=True, help="JSON-RPC endpoint, e.g. http://127.0.0.1:6200")
    ap.add_argument("--xmlrpc-url", required=True, help="XML-RPC endpoint, e.g. http://127.0.0.1:6201")
    ap.add_argument("--calls", type=int, default=2000, help="Number of calls per protocol")
    args = ap.parse_args()

    calls = max(1, args.calls)

    print("Week 12 RPC benchmark")
    print(f"Calls per protocol: {calls}")
    print(f"JSON-RPC URL: {args.jsonrpc_url}")
    print(f"XML-RPC URL:  {args.xmlrpc_url}")
    print()

    jr = bench_jsonrpc(args.jsonrpc_url, calls=calls)
    xr = bench_xmlrpc(args.xmlrpc_url, calls=calls)

    for r in (jr, xr):
        print(f"{r.name}: {r.calls} calls in {r.seconds:.3f}s")
        print(f"  Throughput: {r.calls_per_second:.1f} calls/s")
        print(f"  Mean latency: {r.avg_ms:.3f} ms")
        print()

    faster = jr if jr.seconds < xr.seconds else xr
    print(f"Result: {faster.name} was faster in this run.")
    print("Note: Results depend on Python version, load, network stack and implementation details.")
    return 0



# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    raise SystemExit(main())
