#!/usr/bin/env python3
"""Exercise 02 — RPC (Week 12)

Learning goals
- Understand RPC as a design pattern for distributed systems
- Compare JSON-RPC and XML-RPC over HTTP
- Observe gRPC over HTTP/2 and Protocol Buffers
- Capture and inspect protocol differences at packet level (optional)

Prerequisites
- Run `make setup` and `make verify` in the Week 12 directory.

---

Part A — JSON-RPC

Terminal 1
  make jsonrpc-server

Terminal 2
  make jsonrpc-client

Manual JSON-RPC call with curl:
  curl -s -X POST "http://127.0.0.1:6200" \
    -H "Content-Type: application/json" \
    -d '{"jsonrpc":"2.0","id":1,"method":"add","params":[10,32]}'

Expected result: 42

---

Part B — XML-RPC

Terminal 1
  make xmlrpc-server

Terminal 2
  make xmlrpc-client

Manual XML-RPC call with Python:
  python - <<'PY'
  import xmlrpc.client
  p = xmlrpc.client.ServerProxy("http://127.0.0.1:6201", allow_none=True)
  print(p.add(10, 32))
  PY

Expected result: 42

---

Part C — gRPC

Terminal 1
  make grpc-server

Terminal 2
  make grpc-client

Observe the error behaviour:
- Divide(1, 0) should return a gRPC INVALID_ARGUMENT status.

If you modify `src/rpc/grpc/calculator.proto`, regenerate stubs:
  make proto-gen

---

Part D — Benchmark (local)

Run a simple local benchmark which starts servers automatically:
  make benchmark-rpc

Discuss:
- payload overhead (JSON versus XML)
- serialisation cost
- throughput and mean latency

---

Part E — Capture and inspect (optional)

Capture while running short demos:
  sudo make capture

Inspect quickly:
  make analyse

In Wireshark, compare:
- HTTP headers and payload size (JSON-RPC versus XML-RPC)
- request/response structure
- how gRPC traffic differs (binary framing and HTTP/2)

---

Deliverables (typical)
1. One example request/response for JSON-RPC and XML-RPC
2. A short discussion of observed differences (payload size and readability)
3. (Optional) a Wireshark screenshot illustrating one key difference

"""

from __future__ import annotations


def main() -> int:
    print(__doc__)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
