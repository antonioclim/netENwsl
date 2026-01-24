#!/usr/bin/env python3
"""
Exercise 12.02: Compare RPC Protocols
=====================================
Computer Networks - Week 12 (WSL Environment)
ASE Bucharest | by ing. dr. Antonio Clim

Objectives:
- UNDERSTAND the RPC abstraction and serialisation formats
- APPLY JSON-RPC, XML-RPC and gRPC client calls
- ANALYSE protocol differences through packet captures and benchmarks
- EVALUATE trade-offs between RPC frameworks

Prerequisites:
- Docker running in WSL
- Lab containers started (make start or python3 scripts/start_lab.py)
- All three RPC servers running (JSON-RPC, XML-RPC, gRPC)

Level: Intermediate
Estimated time: 50 minutes

Pair Programming Notes:
- Driver: Executes curl commands and Python clients
- Navigator: Records payload sizes and latencies, checks documentation
- Swap after: Completing JSON-RPC section
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations
from typing import Optional, List, Dict, Tuple, Any

import sys
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# EXERCISE_DOCUMENTATION
# ═══════════════════════════════════════════════════════════════════════════════

EXERCISE_TEXT = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    EXERCISE 12.02: COMPARE RPC PROTOCOLS                      ║
╚═══════════════════════════════════════════════════════════════════════════════╝

This exercise compares JSON-RPC, XML-RPC and gRPC through hands-on testing
and performance analysis.

───────────────────────────────────────────────────────────────────────────────
PART A: JSON-RPC 2.0
───────────────────────────────────────────────────────────────────────────────

💭 PREDICTION: What will the server return for a method that doesn't exist?
   - A) HTTP 404 Not Found
   - B) HTTP 200 with a JSON error object
   - C) HTTP 500 Internal Server Error

Start the JSON-RPC server (if not running):
  python3 scripts/start_lab.py --service jsonrpc

Test basic operations with curl:

  # Addition (positional parameters)
  curl -s -X POST http://localhost:6200 \\
    -H "Content-Type: application/json" \\
    -d '{"jsonrpc":"2.0","method":"add","params":[10,32],"id":1}'

  # Subtraction (named parameters)
  curl -s -X POST http://localhost:6200 \\
    -H "Content-Type: application/json" \\
    -d '{"jsonrpc":"2.0","method":"subtract","params":{"a":100,"b":58},"id":2}'

Record the results:
┌───────────────────────────────────────────────────────────────────────────────┐
│ Operation      │ Expected Result │ Actual Result │ Match? │
├───────────────────────────────────────────────────────────────────────────────┤
│ add(10, 32)    │ 42              │ _____________ │ ______ │
│ subtract(100,58)│ 42             │ _____________ │ ______ │
└───────────────────────────────────────────────────────────────────────────────┘

Test error handling:

  # Division by zero
  curl -s -X POST http://localhost:6200 \\
    -H "Content-Type: application/json" \\
    -d '{"jsonrpc":"2.0","method":"divide","params":[42,0],"id":3}'

  # Method not found
  curl -s -X POST http://localhost:6200 \\
    -H "Content-Type: application/json" \\
    -d '{"jsonrpc":"2.0","method":"power","params":[2,8],"id":4}'

💭 PREDICTION: What error code is returned for "method not found"?
   (Check docs/misconceptions.md for the answer)

Test batch requests:

  curl -s -X POST http://localhost:6200 \\
    -H "Content-Type: application/json" \\
    -d '[
      {"jsonrpc":"2.0","method":"add","params":[1,2],"id":1},
      {"jsonrpc":"2.0","method":"multiply","params":[3,4],"id":2},
      {"jsonrpc":"2.0","method":"divide","params":[10,0],"id":3}
    ]'

How many responses do you get? _____ (Answer: 3)
How many are errors? _____ (Answer: 1 — the division by zero)

───────────────────────────────────────────────────────────────────────────────
PART B: XML-RPC
───────────────────────────────────────────────────────────────────────────────

💭 PREDICTION: How much larger (in bytes) will an XML-RPC request be compared
   to the equivalent JSON-RPC request?

Start the XML-RPC server (if not running):
  python3 scripts/start_lab.py --service xmlrpc

Test using Python's built-in client:

  python3 -c "
  import xmlrpc.client
  proxy = xmlrpc.client.ServerProxy('http://localhost:6201', allow_none=True)
  print('add(10, 32) =', proxy.add(10, 32))
  print('Available methods:', proxy.system.listMethods())
  "

Test using curl (to see the XML payload):

  curl -s -X POST http://localhost:6201 \\
    -H "Content-Type: text/xml" \\
    -d '<?xml version="1.0"?>
  <methodCall>
    <methodName>add</methodName>
    <params>
      <param><value><double>10</double></value></param>
      <param><value><double>32</double></value></param>
    </params>
  </methodCall>'

Compare payload sizes:

  # JSON-RPC payload
  echo '{"jsonrpc":"2.0","method":"add","params":[10,32],"id":1}' | wc -c
  # Result: ~56 bytes

  # XML-RPC payload (minified)
  echo '<?xml version="1.0"?><methodCall><methodName>add</methodName><params><param><value><double>10</double></value></param><param><value><double>32</double></value></param></params></methodCall>' | wc -c
  # Result: ~195 bytes

Record the difference:
┌───────────────────────────────────────────────────────────────────────────────┐
│ Protocol    │ Request Size (bytes) │ Response Size (bytes) │
├───────────────────────────────────────────────────────────────────────────────┤
│ JSON-RPC    │ ____________________ │ _____________________ │
│ XML-RPC     │ ____________________ │ _____________________ │
│ Ratio       │ ____________________ │ _____________________ │
└───────────────────────────────────────────────────────────────────────────────┘

───────────────────────────────────────────────────────────────────────────────
PART C: gRPC with Protocol Buffers
───────────────────────────────────────────────────────────────────────────────

💭 PREDICTION: Can you read a gRPC request payload in Wireshark like JSON-RPC?

Examine the Protocol Buffer definition:
  cat src/apps/rpc/grpc/calculator.proto

Key observations:
- Fields have numeric tags (1, 2) not names
- Types are explicit (double, string)
- Service methods are defined formally

Start the gRPC server (if not running):
  python3 scripts/start_lab.py --service grpc
  # Or: python3 src/apps/rpc/grpc/grpc_server.py

Run the gRPC client:
  python3 src/apps/rpc/grpc/grpc_client.py --demo

Record the results:
┌───────────────────────────────────────────────────────────────────────────────┐
│ Operation      │ Expected Result │ Actual Result │ Match? │
├───────────────────────────────────────────────────────────────────────────────┤
│ Add(10, 32)    │ 42.0            │ _____________ │ ______ │
│ Divide(10, 0)  │ Error           │ _____________ │ ______ │
└───────────────────────────────────────────────────────────────────────────────┘

Observe gRPC error handling:
- What status code is returned for division by zero? _______________
- How does this differ from JSON-RPC error codes? _______________

───────────────────────────────────────────────────────────────────────────────
PART D: Performance Benchmark
───────────────────────────────────────────────────────────────────────────────

💭 PREDICTION: Rank the protocols by latency (fastest to slowest):
   [ ] JSON-RPC  [ ] XML-RPC  [ ] gRPC

Run the automated benchmark:
  python3 src/apps/rpc/benchmark_rpc.py --iterations 100

Or run the demo script:
  python3 scripts/run_demo.py --demo benchmark

Record the results:
┌───────────────────────────────────────────────────────────────────────────────┐
│ Protocol    │ Avg Latency (ms) │ Min (ms) │ Max (ms) │ Req/sec │
├───────────────────────────────────────────────────────────────────────────────┤
│ JSON-RPC    │ ________________ │ ________ │ ________ │ _______ │
│ XML-RPC     │ ________________ │ ________ │ ________ │ _______ │
│ gRPC        │ ________________ │ ________ │ ________ │ _______ │
└───────────────────────────────────────────────────────────────────────────────┘

Factors affecting results:
1. Serialisation overhead (JSON < XML < Protobuf in CPU, reverse in size)
2. HTTP version (HTTP/1.1 vs HTTP/2 multiplexing)
3. Connection reuse (keep-alive)
4. Python GIL limitations

───────────────────────────────────────────────────────────────────────────────
PART E: Wireshark Analysis (Optional)
───────────────────────────────────────────────────────────────────────────────

Capture traffic from all three protocols:
  python3 scripts/capture_traffic.py --duration 60 --ports 6200,6201,6251

While capturing, run operations on all three servers.

In Wireshark, compare:
1. Filter: tcp.port == 6200 → JSON-RPC (can read JSON in payload)
2. Filter: tcp.port == 6201 → XML-RPC (can read XML in payload)
3. Filter: tcp.port == 6251 → gRPC (binary, HTTP/2 frames)

───────────────────────────────────────────────────────────────────────────────
DELIVERABLES
───────────────────────────────────────────────────────────────────────────────

1. Completed tables from Parts A, B, C, D
2. Brief comparison summary: Which protocol for which use case?
3. (Optional) Wireshark screenshot showing payload differences

───────────────────────────────────────────────────────────────────────────────
REFLECTION QUESTIONS
───────────────────────────────────────────────────────────────────────────────

1. You're building a public API for a web application. Which RPC protocol
   would you choose and why?

2. You're building internal microservices where bandwidth is critical.
   Which protocol would you choose and why?

3. Why does JSON-RPC return HTTP 200 even for application errors?

4. What are the advantages of Protocol Buffers' schema requirement?
   What are the disadvantages?

5. XML-RPC is often considered "obsolete", yet it's still used in WordPress.
   Why might legacy compatibility matter?

───────────────────────────────────────────────────────────────────────────────
PROTOCOL SELECTION CHEAT SHEET
───────────────────────────────────────────────────────────────────────────────

┌───────────────────────────────────────────────────────────────────────────────┐
│ Use Case                    │ Recommended │ Reason                           │
├───────────────────────────────────────────────────────────────────────────────┤
│ Public web API              │ JSON-RPC    │ Human-readable, easy debugging   │
│ Browser client              │ JSON-RPC    │ Native JSON support              │
│ Internal microservices      │ gRPC        │ Performance, strong contracts    │
│ Legacy system integration   │ XML-RPC     │ Compatibility                    │
│ Mobile app backend          │ gRPC        │ Bandwidth efficiency             │
│ Blockchain/crypto           │ JSON-RPC    │ Industry standard                │
│ Real-time streaming         │ gRPC        │ Bidirectional streaming          │
└───────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
"""


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """
    Display exercise instructions for RPC protocol comparison.
    
    This exercise guides students through testing JSON-RPC, XML-RPC
    and gRPC to understand their differences.
    
    Returns:
        int: Exit code (0 for success)
    """
    print(EXERCISE_TEXT)
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    raise SystemExit(main())
