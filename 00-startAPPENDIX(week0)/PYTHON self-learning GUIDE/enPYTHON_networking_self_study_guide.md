# Python for Computer Networks
## Optional Self-Study Guide

> **Supplementary material** for the Computer Networks course  
> **Status:** Optional, no assessment  
> **Purpose:** Deepen understanding of Python within the laboratory exercises  
> **Audience:** Students who wish to better understand the Python code in the laboratory kits

---

## About This Guide

The Computer Networks laboratory exercises use Python as the primary tool. This guide **is not compulsory** — you can complete the laboratories without it. It is intended for those who:

- Want to understand *why* the code in the exercises looks the way it does
- Are curious to modify or extend the existing exercises
- Wish to build their own network diagnostic tools
- Have a background in other languages (C, JavaScript, Java) and want to make a rapid transition

**Format:** Each step is correlated with the laboratory weeks and can be completed independently at your own pace.

---

## How to Use This Guide

```
┌─────────────────────────────────────────────────────────────────┐
│  LABORATORY WEEK                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Compulsory exercises (weekly kit)                       │   │
│  │ → Run the scripts, complete the TODOs                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          │                                      │
│                          ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ OPTIONAL: Corresponding step from this guide            │   │
│  │ → Understand the Python concepts used                   │   │
│  │ → Explore supplementary exercises                       │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

**Estimated time per step:** 2–4 hours (flexible, depending on personal interest)

---

## Correlation with Laboratory Weeks

| Lab Week | Networking Topic | Correlated Python Step |
|----------|------------------|------------------------|
| W1–2 | Network fundamentals, Architectural models | Step 1: First steps |
| W2–3 | TCP/UDP socket programming | Step 2: Data types + Step 3: Sockets |
| W4 | Physical Layer, Data Link, Custom protocols | Step 4: Code organisation |
| W5 | Network Layer, IP, Subnetting | Step 5: CLI with argparse |
| W6 | NAT/PAT, SDN | Step 6: Packet analysis |
| W7 | Packet filtering, Firewall | Step 6: Packet analysis (continued) |
| W8 | Transport Layer, HTTP | Step 7: Concurrency + Step 8: HTTP |
| W9 | Session/Presentation Layer | Step 8: HTTP (continued) |
| W10–11 | Application Layer, REST, DNS, FTP | Step 8: HTTP & REST |
| W12 | Email, RPC | Step 8: Application protocols |
| W13 | IoT, Security | Step 9: Best practices |
| W14 | Recap, Projects | Step 9: Best practices |

---

## STEP 1: First Steps — Reading Python Code
**Correlated with:** Weeks 1–2 (Network fundamentals)

### Why It Matters

In the laboratory kits you will encounter scripts such as `ex_1_01_ping_latency.py`. Before modifying them, you need to be able to read them.

### What You Will Learn

- The structure of a Python script
- Syntactic differences from C/JavaScript
- How to run and modify script parameters

### Key Concepts Explained

**Shebang and encoding:**
```python
#!/usr/bin/env python3
"""Docstring - module description."""
```
The first line tells the shell which interpreter to use. Triple quotes are docstrings (documentation).

**Types without explicit declaration:**
```python
# C/Java
int port = 8080;
String host = "localhost";

# Python - the type is inferred automatically
port = 8080
host = "localhost"
```

**Indentation defines blocks:**
```python
# Python uses indentation, not braces
if port > 1024:
    print("Unprivileged port")
    print("Can be used without sudo")
else:
    print("Privileged port")
```

**Functions and type hints (optional but useful):**
```python
def measure_latency(host: str, count: int = 3) -> float:
    """Measure average latency to a host."""
    # implementation
    return average_ms
```
Type hints (`host: str`, `-> float`) are not compulsory but aid comprehension.

### Exploration Exercise

Open `1enWSL/src/exercises/ex_1_01_ping_latency.py` and identify:
1. What does the `@dataclass` decorator do?
2. What does `float | None` mean?
3. How does `subprocess.run()` work?

### Further Resources

- [Python for Programmers](https://docs.python.org/3/tutorial/) — official tutorial
- Compare syntax: [Learn X in Y minutes – Python](https://learnxinyminutes.com/docs/python/)

---

## STEP 2: Data Types for Networking
**Correlated with:** Weeks 2–3 (Socket programming)

### Why It Matters

Networks transport **bytes**, not text. Python makes an explicit distinction between `str` (text) and `bytes` (raw data).

### Key Concepts Explained

**Bytes vs Strings:**
```python
# String (text for humans)
text_message = "GET /index.html HTTP/1.1"

# Bytes (what is actually sent over the network)
bytes_message = b"GET /index.html HTTP/1.1"

# Conversion
bytes_message = text_message.encode('utf-8')
text_message = bytes_message.decode('utf-8')
```

**Why does this matter?** When you receive data from a socket, you receive `bytes`. When you display in the console, you need `str`.

**Dataclasses — modern structs:**
```python
from dataclasses import dataclass

@dataclass
class PacketInfo:
    src_ip: str
    dst_ip: str
    protocol: int
    length: int

# Creating an instance
pkt = PacketInfo("192.168.1.1", "8.8.8.8", 6, 1500)
print(pkt.src_ip)  # 192.168.1.1
```
Similar to `struct` in C, but with more automatic features.

**List comprehensions — compact processing:**
```python
# Classic style (as in C/Java)
ports = []
for i in range(1, 101):
    if i % 2 == 0:
        ports.append(i)

# Idiomatic Python
ports = [i for i in range(1, 101) if i % 2 == 0]
```

**Dict comprehensions for parsing:**
```python
# Parse HTTP headers in a single expression
raw = "Host: localhost\r\nContent-Type: text/html"
headers = {
    k: v 
    for line in raw.split('\r\n') 
    for k, v in [line.split(': ')]
}
# {'Host': 'localhost', 'Content-Type': 'text/html'}
```

### Exploration Exercise

In `2enWSL/src/exercises/`, find how the conversion between bytes and string is performed in the TCP/UDP code.

---

## STEP 3: Socket Programming in Python
**Correlated with:** Weeks 2–4 (TCP/UDP, Network communication)

### Why It Matters

The laboratory exercises implement TCP/UDP servers and clients. Understanding the Python socket API helps you modify their behaviour.

### Key Concepts Explained

**C vs Python comparison:**

```c
// C - TCP Client (many lines, manual management)
int sock = socket(AF_INET, SOCK_STREAM, 0);
struct sockaddr_in serv_addr;
serv_addr.sin_family = AF_INET;
serv_addr.sin_port = htons(8080);
inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr);
connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr));
send(sock, "Hello", 5, 0);
char buffer[1024];
recv(sock, buffer, 1024, 0);
close(sock);
```

```python
# Python - TCP Client (compact, automatic cleanup)
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(("127.0.0.1", 8080))
    sock.sendall(b"Hello")
    response = sock.recv(1024)
# The socket is closed automatically upon exiting 'with'
```

**Context managers (`with`):**

`with` guarantees that the resource is closed even if an exception occurs. It is the equivalent of RAII in C++ or try-with-resources in Java.

```python
# Without with (risk of leak)
sock = socket.socket(...)
sock.connect(...)
data = sock.recv(1024)  # What if an error occurs here?
sock.close()  # This line is never executed!

# With with (safe)
with socket.socket(...) as sock:
    sock.connect(...)
    data = sock.recv(1024)
# close() called automatically, regardless of errors
```

**Minimal TCP server:**
```python
import socket

def run_server(host: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(5)
        print(f"Listening on {host}:{port}")
        
        while True:
            conn, addr = server.accept()
            with conn:
                data = conn.recv(1024)
                conn.sendall(b"OK: " + data.upper())
```

### Exploration Exercise

Compare `ex_2_01_tcp.py` and `ex_2_02_udp.py`. What differences do you observe between `SOCK_STREAM` (TCP) and `SOCK_DGRAM` (UDP)?

---

## STEP 4: Code Organisation
**Correlated with:** Week 4 (Physical Layer, Custom protocols)

### Why It Matters

The laboratory kits have a consistent structure: `src/`, `scripts/`, `utils/`. Understanding the organisation helps you navigate and reuse the code.

### Key Concepts Explained

**Structure of a laboratory kit:**
```
week_N/
├── src/
│   ├── __init__.py      ← makes src/ a Python "package"
│   ├── exercises/       ← main exercises
│   │   ├── __init__.py
│   │   └── ex_N_01.py
│   └── utils/           ← reusable helper functions
│       ├── __init__.py
│       └── net_utils.py
├── scripts/             ← orchestration scripts (start_lab, etc.)
├── docker/              ← container configurations
└── tests/               ← automated tests
```

**Imports:**
```python
# Import from the standard library
import socket
from dataclasses import dataclass

# Import from project packages
from src.utils.net_utils import format_mac
from src.utils.logger import log
```

**`__init__.py` — what does it do?**

It turns a folder into an importable Python "package". It can be empty or can export functions:
```python
# src/utils/__init__.py
from .net_utils import format_mac, parse_ip
from .logger import log

__all__ = ['format_mac', 'parse_ip', 'log']
```

### Exploration Exercise

Open `scripts/utils/` from any week and see how the helper functions are organised.

---

## STEP 5: CLI Interfaces with argparse
**Correlated with:** Week 5 (Network Layer, IP, Subnetting)

### Why It Matters

All exercises accept parameters from the command line (`--host`, `--port`, etc.). The `argparse` module handles this.

### Key Concepts Explained

**Simple CLI:**
```python
import argparse

parser = argparse.ArgumentParser(description="Port scanner")
parser.add_argument("target", help="Target IP address")
parser.add_argument("--port", "-p", type=int, default=80, help="Port (default: 80)")
parser.add_argument("--timeout", type=float, default=1.0)
parser.add_argument("--verbose", "-v", action="store_true")

args = parser.parse_args()

print(f"Scanning {args.target}:{args.port}")
if args.verbose:
    print(f"Timeout: {args.timeout}s")
```

```bash
# Usage
python scanner.py 192.168.1.1 --port 443 -v
```

**Subcommands (git style):**
```python
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command", required=True)

# python tool.py scan ...
scan_parser = subparsers.add_parser("scan")
scan_parser.add_argument("target")

# python tool.py discover ...
discover_parser = subparsers.add_parser("discover")
discover_parser.add_argument("--network")

args = parser.parse_args()
if args.command == "scan":
    do_scan(args.target)
elif args.command == "discover":
    do_discover(args.network)
```

**Automatic help:**
```bash
python scanner.py --help
# Displays the description and all arguments
```

### Exploration Exercise

Run `python3 ex_5_01_cidr_flsm.py --help` and examine how the arguments are defined in the code.

---

## STEP 6: Packet Analysis and Binary Data
**Correlated with:** Weeks 6–7 (NAT, Firewall, Packet filtering)

### Why It Matters

Traffic capture and packet analysis laboratories use `struct` for binary parsing and sometimes `scapy` for advanced analysis.

### Key Concepts Explained

**The struct module — binary parsing:**

Network protocols have strict binary formats. `struct` converts between bytes and Python types.

```python
import struct

# Format: ! = network byte order (big-endian)
#         H = unsigned short (2 bytes)
#         I = unsigned int (4 bytes)

# Simplified header parsing
data = b'\x00\x50\x1f\x90...'  # bytes from the network

src_port, dst_port = struct.unpack('!HH', data[:4])
print(f"Source port: {src_port}, Dest port: {dst_port}")

# Header construction
header = struct.pack('!HH', 8080, 443)
```

**Struct format table:**
| Format | C Type | Bytes | Python |
|--------|--------|-------|--------|
| `B` | unsigned char | 1 | int |
| `H` | unsigned short | 2 | int |
| `I` | unsigned int | 4 | int |
| `Q` | unsigned long long | 8 | int |
| `!` | network order | – | big-endian |

**IP header parsing (simplified example):**
```python
def parse_ip_header(raw: bytes) -> dict:
    """Extract information from IP header."""
    if len(raw) < 20:
        raise ValueError("Header too short")
    
    # First 20 bytes of the IP header
    fields = struct.unpack('!BBHHHBBHII', raw[:20])
    
    version_ihl = fields[0]
    version = version_ihl >> 4  # First 4 bits
    
    return {
        'version': version,
        'ttl': fields[5],
        'protocol': fields[6],
        'src_ip': socket.inet_ntoa(struct.pack('!I', fields[8])),
        'dst_ip': socket.inet_ntoa(struct.pack('!I', fields[9])),
    }
```

**Scapy (if installed):**
```python
from scapy.all import rdpcap, IP, TCP

# Read PCAP file
packets = rdpcap('capture.pcap')

for pkt in packets:
    if IP in pkt:
        print(f"{pkt[IP].src} -> {pkt[IP].dst}")
```

### Exploration Exercise

In `7enWSL/src/exercises/`, see how packet capture and filtering is performed.

---

## STEP 7: Concurrency for Network Operations
**Correlated with:** Weeks 7–9 (Firewall, HTTP, Transport Layer)

### Why It Matters

Port scanning, multi-client servers and load tests use threading for parallelism.

### Key Concepts Explained

**Why threading for networks?**

Network operations are "I/O bound" — the CPU waits for responses. Threading allows simultaneous processing of multiple connections.

**ThreadPoolExecutor — simple parallelism:**
```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import socket

def check_port(host: str, port: int) -> tuple[int, bool]:
    """Check whether a port is open."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    try:
        result = sock.connect_ex((host, port))
        return (port, result == 0)
    finally:
        sock.close()

def scan_ports(host: str, ports: list[int]) -> list[int]:
    """Scan ports in parallel."""
    open_ports = []
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        # Launch all checks simultaneously
        futures = {executor.submit(check_port, host, p): p for p in ports}
        
        # Collect results as they arrive
        for future in as_completed(futures):
            port, is_open = future.result()
            if is_open:
                open_ports.append(port)
                print(f"Port {port} OPEN")
    
    return sorted(open_ports)

# Usage
open_ports = scan_ports("192.168.1.1", range(1, 1025))
```

**Server with threading:**
```python
import threading

def handle_client(conn, addr):
    """Handler for a client."""
    try:
        data = conn.recv(1024)
        conn.sendall(b"OK")
    finally:
        conn.close()

# In the main server loop:
while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.daemon = True  # Stops when the main programme stops
    thread.start()
```

### Exploration Exercise

In `13enWSL/src/exercises/ex_13_01_port_scanner.py`, observe how `ThreadPoolExecutor` is used for parallel scanning.

---

## STEP 8: HTTP and Application Protocols
**Correlated with:** Weeks 8–12 (HTTP, REST, DNS, FTP, Email)

### Why It Matters

Many exercises implement HTTP servers or REST clients. Understanding the protocol at socket level aids debugging.

### Key Concepts Explained

**Anatomy of an HTTP request:**
```
GET /index.html HTTP/1.1\r\n
Host: localhost\r\n
Connection: close\r\n
\r\n
```
- Request line: `METHOD PATH VERSION`
- Headers: `Key: Value`
- Empty line (`\r\n\r\n`) separates headers from body

**Request parsing (from W8 exercises):**
```python
def parse_request(raw: bytes) -> tuple[str, str, dict]:
    """Parse HTTP request."""
    text = raw.decode('utf-8')
    lines = text.split('\r\n')
    
    # First line: GET /path HTTP/1.1
    method, path, version = lines[0].split(' ')
    
    # Headers
    headers = {}
    for line in lines[1:]:
        if ': ' in line:
            key, value = line.split(': ', 1)
            headers[key.lower()] = value
    
    return method, path, headers
```

**Response construction:**
```python
def build_response(status: int, body: bytes, content_type: str = 'text/html') -> bytes:
    """Construct HTTP response."""
    status_texts = {200: 'OK', 404: 'Not Found', 500: 'Internal Server Error'}
    
    headers = f"""HTTP/1.1 {status} {status_texts.get(status, 'Unknown')}
Content-Type: {content_type}
Content-Length: {len(body)}
Connection: close

"""
    return headers.replace('\n', '\r\n').encode() + body
```

**The requests library for clients:**
```python
import requests

# Simple GET
response = requests.get('http://httpbin.org/get')
print(response.status_code)
print(response.json())

# POST with JSON
response = requests.post(
    'http://httpbin.org/post',
    json={'key': 'value'},
    timeout=5.0
)
```

### Exploration Exercise

Complete the TODOs in `8enWSL/src/exercises/ex_8_01_http_server.py` to understand how a minimal HTTP server works.

---

## STEP 9: Code Practices and Debugging
**Correlated with:** Weeks 11–14 (Projects, Recap)

### Why It Matters

When you extend exercises or create your own tools, you need to write code that works and is easy to debug.

### Key Concepts Explained

**Logging instead of print:**
```python
import logging

# Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Usage
logger.info(f"Connecting to {host}:{port}")
logger.debug(f"Data received: {data!r}")  # debug does not appear by default
logger.error(f"Connection failed: {e}")
```

**Handling network exceptions:**
```python
import socket

try:
    sock.connect((host, port))
except socket.timeout:
    logger.warning(f"Timeout at {host}:{port}")
except ConnectionRefusedError:
    logger.warning(f"Connection refused by {host}:{port}")
except OSError as e:
    logger.error(f"OS error: {e}")
finally:
    sock.close()
```

**Quick debugging:**
```python
# Display variables with context
x = some_complex_expression()
print(f"{x=}")  # Displays: x=value_of_x

# Interactive breakpoint
import pdb; pdb.set_trace()  # Stops execution here
# or in Python 3.7+:
breakpoint()
```

**Type hints for clarity:**
```python
from typing import Optional, List, Tuple

def scan_host(
    target: str,
    ports: List[int],
    timeout: float = 0.5
) -> Tuple[List[int], int]:
    """
    Scan a host's ports.
    
    Returns:
        Tuple with (open_ports, closed_ports)
    """
    ...
```

---

## Useful Libraries

| Library | Purpose | Installation |
|---------|---------|--------------|
| `socket` | Low-level socket programming | *included in Python* |
| `struct` | Binary parsing | *included in Python* |
| `argparse` | CLI | *included in Python* |
| `ipaddress` | IP/CIDR validation | *included in Python* |
| `threading` | Concurrency | *included in Python* |
| `concurrent.futures` | Thread pools | *included in Python* |
| `logging` | Structured logging | *included in Python* |
| `scapy` | Packet crafting | `pip install scapy` |
| `requests` | HTTP client | `pip install requests` |

---

## Resources for Further Learning

### Documentation
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Socket Programming HOWTO](https://docs.python.org/3/howto/sockets.html)
- [Scapy Documentation](https://scapy.readthedocs.io/)

### Practice
- [Exercism Python Track](https://exercism.org/tracks/python) — progressive exercises
- [Build Your Own X](https://github.com/codecrafters-io/build-your-own-x#build-your-own-network-stack) — hands-on projects

### Books (optional)
- "Black Hat Python" — network security with Python
- "Foundations of Python Network Programming" — comprehensive reference

---

## Frequently Asked Questions

**Q: Do I need to complete all steps in order?**  
A: No. You can jump directly to the step relevant to your current laboratory week.

**Q: What if I do not understand something?**  
A: Try running the code and modifying values. Experimentation is the best teacher. You can also ask questions during laboratories.

**Q: Do I need to memorise the syntax?**  
A: No. Use the documentation and examples from the kits. Over time it becomes natural.

**Q: How do I test whether I have understood?**  
A: Try modifying an existing exercise or adding a new feature.

---

*Material produced as optional support for the Computer Networks course.*  
*Version: January 2025*
