# 🐍 Python for Computer Networks
## Elaborate Self-Study Guide

> **Supplementary material** for the Computer Networks course  
> **Repository:** [github.com/antonioclim/netENwsl](https://github.com/antonioclim/netENwsl)  
> **Status:** Optional, no assessment  
> **Environment:** WSL2 + Ubuntu 22.04 + Docker + Portainer

---

## 📋 Contents

1. [About This Guide](#about-this-guide)
2. [Repository Structure](#repository-structure)
3. [Learning Steps](#learning-steps)
   - [Step 1: Reading Python Code](#step-1-reading-python-code)
   - [Step 2: Data Types for Networking](#step-2-data-types-for-networking)
   - [Step 3: Socket Programming](#step-3-socket-programming)
   - [Step 4: Code Organisation](#step-4-code-organisation)
   - [Step 5: CLI Interfaces](#step-5-cli-interfaces)
   - [Step 6: Packet Analysis](#step-6-packet-analysis)
   - [Step 7: Concurrency](#step-7-concurrency)
   - [Step 8: HTTP and Application Protocols](#step-8-http-and-application-protocols)
   - [Step 9: Practices and Debugging](#step-9-practices-and-debugging)
4. [Exploration Exercises by Week](#exploration-exercises-by-week)
5. [Python-Networking Quick Reference](#python-networking-quick-reference)
6. [Further Resources](#further-resources)

---

## About This Guide

The Computer Networks laboratory exercises use **Python** as the primary implementation tool. This guide **is not compulsory** — the laboratories can be completed without it.

### Who Is This For?

- Students who want to understand *why* the code looks a certain way
- Those curious to modify or extend the existing exercises
- Programmers with experience in C/JavaScript/Java who want a rapid transition to Python

### How to Use This Guide

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  LABORATORY WEEK                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Compulsory exercises (weekly kit from NenWSL/)                      │   │
│  │ → Run the scripts, complete the TODOs                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              │                                              │
│                              ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ OPTIONAL: Corresponding step from this guide                        │   │
│  │ → Understand the Python concepts behind the code                    │   │
│  │ → Explore supplementary exercises for deeper understanding          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Repository Structure

The `netENwsl` repository has a consistent structure for each week:

```
netENwsl/
├── 1enWSL/                           # Week 1
│   ├── src/
│   │   ├── exercises/                # ← MAIN EXERCISES
│   │   │   ├── ex_1_01_ping_latency.py
│   │   │   ├── ex_1_02_tcp_server_client.py
│   │   │   ├── ex_1_03_parse_csv.py
│   │   │   ├── ex_1_04_pcap_stats.py
│   │   │   └── ex_1_05_transmission_delay.py
│   │   ├── apps/                     # Complete demonstrative applications
│   │   └── utils/                    # Reusable helper functions
│   │       └── net_utils.py
│   ├── scripts/                      # Orchestration scripts
│   │   ├── start_lab.py
│   │   ├── stop_lab.py
│   │   ├── capture_traffic.py
│   │   └── utils/
│   │       ├── docker_utils.py
│   │       ├── logger.py
│   │       └── network_utils.py
│   ├── docker/                       # Docker configurations
│   │   ├── Dockerfile.lab
│   │   └── docker-compose.yml
│   ├── docs/                         # Documentation
│   │   ├── theory_summary.md
│   │   ├── commands_cheatsheet.md
│   │   ├── troubleshooting.md
│   │   └── further_reading.md
│   ├── tests/                        # Automated tests
│   │   ├── test_exercises.py
│   │   ├── test_environment.py
│   │   └── smoke_test.py
│   ├── homework/                     # Homework assignments
│   └── README.md
├── 2enWSL/                           # Week 2
├── ...
└── 14enWSL/                          # Week 14
```

### Week Correspondence Table

| Folder | Week | Networking Topic | Correlated Python Step |
|--------|------|------------------|------------------------|
| `1enWSL` | W1-2 | Network fundamentals | Step 1: Reading code |
| `2enWSL` | W2-3 | TCP/UDP socket programming | Step 2 + Step 3: Types + Sockets |
| `3enWSL` | W3 | Broadcast, Multicast, Tunnel | Step 3: Advanced sockets |
| `4enWSL` | W4 | Physical/Data Link Layer | Step 4: Code organisation |
| `5enWSL` | W5 | Network Layer, IP, Subnetting | Step 5: CLI argparse |
| `6enWSL` | W6 | NAT/PAT, SDN | Step 6: Packet analysis |
| `7enWSL` | W7 | Packet filtering, Firewall | Step 6: Analysis (continued) |
| `8enWSL` | W8 | Transport Layer, HTTP | Step 7 + Step 8 |
| `9enWSL` | W9 | Session/Presentation Layer | Step 8: HTTP |
| `10enWSL` | W10 | Application Layer protocols | Step 8: Application protocols |
| `11enWSL` | W11 | Load balancing, DNS | Step 8: REST, DNS |
| `12enWSL` | W12 | Email, RPC | Step 8: Application protocols |
| `13enWSL` | W13 | IoT, Security | Step 7 + Step 9 |
| `14enWSL` | W14 | Recap, Projects | Step 9: Best practices |

---

## Learning Steps

### Step 1: Reading Python Code
**📅 Correlated with:** Weeks 1-2 (`1enWSL`, `2enWSL`)

#### Why It Matters

Before modifying the laboratory scripts, you need to be able to read and understand them. The exercises begin with functional code that you will adapt.

#### Reference Files

Open and study the structure of these files:
- `1enWSL/src/exercises/ex_1_01_ping_latency.py`
- `1enWSL/src/exercises/ex_1_02_tcp_server_client.py`

#### Key Concepts from the Code

**1. Shebang and Docstring**
```python
#!/usr/bin/env python3
"""Exercise 1.01: Measuring latency with ping (Week 1)

This script runs a small ping sample and extracts the average RTT...
"""
```
- The first line tells the shell which interpreter to use
- The docstring (between `"""`) documents the module

**2. Dataclasses — Data Structures**
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class PingResult:
    """Stores the result of a single ping."""
    sequence: int
    rtt_ms: Optional[float]
    success: bool
    message: str = ""
```
Compare with `struct` in C:
```c
// C equivalent
typedef struct {
    int sequence;
    float rtt_ms;  // can be NULL?
    bool success;
    char message[256];
} PingResult;
```

**3. Type Hints (Optional but Useful)**
```python
def measure_latency(host: str, count: int = 3) -> float:
    """Measure average latency to a host."""
    # implementation
    return average_ms
```
- `host: str` — the parameter is a string
- `count: int = 3` — optional parameter with default value
- `-> float` — the function returns a float

**4. Quick Syntax Comparison**

| Concept | C/Java | JavaScript | Python |
|---------|--------|------------|--------|
| Variable declaration | `int x = 5;` | `let x = 5;` | `x = 5` |
| Function | `int f(int x) {...}` | `function f(x) {...}` | `def f(x):` |
| Condition | `if (x > 0) {...}` | `if (x > 0) {...}` | `if x > 0:` |
| Loop | `for (int i=0; i<n; i++)` | `for (let i=0; i<n; i++)` | `for i in range(n):` |
| Array | `int arr[] = {1,2,3}` | `let arr = [1,2,3]` | `arr = [1, 2, 3]` |
| Dictionary | `HashMap<>` | `{key: value}` | `{key: value}` |

#### Practical Exploration

1. **Run** `ex_1_01_ping_latency.py`:
   ```bash
   cd /mnt/d/NETWORKING/netENwsl/1enWSL
   python3 src/exercises/ex_1_01_ping_latency.py --host 127.0.0.1 --count 5
   ```

2. **Identify** in the code:
   - What does the `@dataclass` decorator do?
   - What does `float | None` mean?
   - How does `subprocess.run()` work?

3. **Modify** the default parameter for `--count` from 3 to 10 and run again.

---

### Step 2: Data Types for Networking
**📅 Correlated with:** Weeks 2-3 (`2enWSL`, `3enWSL`)

#### Why It Matters

Networks transport **bytes**, not text. Python makes an explicit distinction between `str` (text) and `bytes` (raw data) — a critical distinction for networking.

#### Reference Files

- `2enWSL/src/exercises/ex_2_01_tcp.py`
- `2enWSL/src/exercises/ex_2_02_udp.py`

#### Key Concepts

**1. Bytes vs Strings**
```python
# String (text for humans)
text_message = "GET /index.html HTTP/1.1"

# Bytes (what is actually sent over the network)
bytes_message = b"GET /index.html HTTP/1.1"

# Conversion
bytes_message = text_message.encode('utf-8')
text_message = bytes_message.decode('utf-8')
```

**Why does this matter?** Sockets send and receive `bytes`. The console displays `str`. You must always convert.

**2. Dataclasses for Protocol Structures**
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

**3. List Comprehensions — Compact Processing**
```python
# Classic style (as in C/Java)
ports = []
for i in range(1, 101):
    if i % 2 == 0:
        ports.append(i)

# Idiomatic Python — a single line
ports = [i for i in range(1, 101) if i % 2 == 0]
```

**4. Dict Comprehensions for Parsing**
```python
# Parse HTTP headers in a single expression
raw = "Host: localhost\r\nContent-Type: text/html"
headers = {
    key: value 
    for line in raw.split('\r\n') 
    for key, value in [line.split(': ')]
}
# Result: {'Host': 'localhost', 'Content-Type': 'text/html'}
```

#### Practical Exploration

In `2enWSL/src/exercises/ex_2_01_tcp.py`:
1. Find where the `encode()`/`decode()` conversion occurs
2. Observe how `sendall()` vs `send()` is used
3. What happens if you send `str` instead of `bytes`?

---

### Step 3: Socket Programming
**📅 Correlated with:** Weeks 2-4 (`2enWSL`, `3enWSL`, `4enWSL`)

#### Why It Matters

Sockets are the foundation of network communication. The exercises implement TCP/UDP servers and clients.

#### Reference Files

- `2enWSL/src/exercises/ex_2_01_tcp.py` — TCP Server/Client
- `2enWSL/src/exercises/ex_2_02_udp.py` — UDP Server/Client
- `3enWSL/src/exercises/ex_3_01_udp_broadcast.py` — UDP Broadcast
- `3enWSL/src/exercises/ex_3_02_udp_multicast.py` — UDP Multicast
- `3enWSL/src/exercises/ex_3_03_tcp_tunnel.py` — TCP Tunnel

#### C vs Python Comparison

**TCP Client in C:**
```c
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

**TCP Client in Python:**
```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(("127.0.0.1", 8080))
    sock.sendall(b"Hello")
    response = sock.recv(1024)
# The socket is closed automatically upon exiting 'with'
```

#### Context Managers (`with`)

`with` guarantees that the resource is closed even if an exception occurs:
```python
# Without with (risk of leak)
sock = socket.socket(...)
sock.connect(...)
data = sock.recv(1024)  # What if an error occurs here?
sock.close()  # Never executed!

# With with (safe)
with socket.socket(...) as sock:
    sock.connect(...)
    data = sock.recv(1024)
# close() called automatically, regardless of errors
```

#### Minimal TCP Server

From `2enWSL/src/exercises/ex_2_01_tcp.py`:
```python
def run_server(host: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(5)
        print(f"Server started on {host}:{port}")
        
        while True:
            conn, addr = server.accept()
            with conn:
                data = conn.recv(1024)
                conn.sendall(b"OK: " + data.upper())
```

#### TCP vs UDP Differences

| Aspect | TCP (`SOCK_STREAM`) | UDP (`SOCK_DGRAM`) |
|--------|--------------------|--------------------|
| Connection | `connect()` required | No connection required |
| Sending | `send()`, `sendall()` | `sendto(data, addr)` |
| Receiving | `recv()` | `recvfrom()` → (data, addr) |
| Guarantees | Ordered, no loss | No guarantees |
| Overhead | Higher | Lower |

#### Practical Exploration

1. Run the TCP server and client:
   ```bash
   # Terminal 1 - Server
   python3 2enWSL/src/exercises/ex_2_01_tcp.py server --port 9090
   
   # Terminal 2 - Client
   python3 2enWSL/src/exercises/ex_2_01_tcp.py client --host 127.0.0.1 --port 9090 -m "test"
   ```

2. Compare `ex_2_01_tcp.py` and `ex_2_02_udp.py`:
   - Which methods differ?
   - What happens when the UDP server is not running?

---

### Step 4: Code Organisation
**📅 Correlated with:** Week 4 (`4enWSL`)

#### Why It Matters

The kits have a consistent structure: `src/`, `scripts/`, `utils/`. Understanding the organisation helps you navigate and reuse the code.

#### Reference Files

- `4enWSL/src/utils/io_utils.py`
- `4enWSL/src/utils/proto_common.py`
- `4enWSL/src/apps/binary_proto_server.py`
- `4enWSL/src/apps/text_proto_client.py`

#### Modular Structure

```
4enWSL/src/
├── __init__.py          # Makes src/ a Python "package"
├── exercises/
│   ├── __init__.py
│   ├── ex_4_01_tcp_proto.py
│   └── ex_4_02_udp_sensor.py
├── apps/                # Complete demonstrative applications
│   ├── __init__.py
│   ├── binary_proto_client.py
│   ├── binary_proto_server.py
│   ├── text_proto_client.py
│   ├── text_proto_server.py
│   ├── udp_sensor_client.py
│   └── udp_sensor_server.py
└── utils/               # Reusable helper functions
    ├── __init__.py
    ├── io_utils.py
    └── proto_common.py
```

#### What Does `__init__.py` Do?

It transforms a folder into an importable Python package:
```python
# src/utils/__init__.py
from .proto_common import calculate_crc, validate_frame
from .io_utils import format_mac, parse_ip

__all__ = ['calculate_crc', 'validate_frame', 'format_mac', 'parse_ip']
```

Then you can import:
```python
from src.utils import calculate_crc
```

#### Import Pattern

```python
# Import from the standard library
import socket
from dataclasses import dataclass

# Import from project packages
from src.utils.proto_common import calculate_crc
from scripts.utils.logger import setup_logger
```

#### Practical Exploration

1. Open `4enWSL/src/utils/proto_common.py` and see the available functions
2. Find where they are imported in the exercises
3. Add a new function and import it in an exercise

---

### Step 5: CLI Interfaces
**📅 Correlated with:** Week 5 (`5enWSL`)

#### Why It Matters

All exercises accept parameters from the command line (`--host`, `--port`, etc.). The `argparse` module handles this.

#### Reference Files

- `5enWSL/src/exercises/ex_5_01_cidr_flsm.py`
- `5enWSL/src/exercises/ex_5_02_vlsm_ipv6.py`
- `5enWSL/src/exercises/ex_5_03_quiz_generator.py`

#### Simple CLI

```python
import argparse

parser = argparse.ArgumentParser(description="Subnet calculator")
parser.add_argument("network", help="Network in CIDR format (e.g. 192.168.1.0/24)")
parser.add_argument("--subnets", "-s", type=int, default=4, help="Number of subnets")
parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

args = parser.parse_args()

print(f"Dividing {args.network} into {args.subnets} subnets")
if args.verbose:
    print("Verbose mode enabled")
```

Usage:
```bash
python calculator.py 192.168.1.0/24 --subnets 8 -v
```

#### Subcommands (Git Style)

```python
parser = argparse.ArgumentParser(prog="netutil")
subparsers = parser.add_subparsers(dest="command", required=True)

# netutil scan ...
scan_parser = subparsers.add_parser("scan", help="Port scanning")
scan_parser.add_argument("target", help="Target IP")
scan_parser.add_argument("--ports", default="1-1024")

# netutil calc ...
calc_parser = subparsers.add_parser("calc", help="Subnet calculator")
calc_parser.add_argument("cidr", help="CIDR network")

args = parser.parse_args()

if args.command == "scan":
    do_scan(args.target, args.ports)
elif args.command == "calc":
    do_calc(args.cidr)
```

#### Custom Validation

```python
import ipaddress

def valid_ip(value):
    """Validate that the value is a valid IP address."""
    try:
        ipaddress.ip_address(value)
        return value
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a valid IP address")

parser.add_argument("--ip", type=valid_ip, required=True)
```

#### Practical Exploration

1. Run `python3 ex_5_01_cidr_flsm.py --help` and examine the arguments
2. Add a new argument `--output-format` with options `text` or `json`
3. Modify the output to respect the chosen format

---

### Step 6: Packet Analysis
**📅 Correlated with:** Weeks 6-7 (`6enWSL`, `7enWSL`)

#### Why It Matters

Traffic capture and packet analysis laboratories use `struct` for binary parsing and Mininet topologies for simulation.

#### Reference Files

- `6enWSL/src/exercises/topo_nat.py` — NAT topology with Mininet
- `6enWSL/src/exercises/topo_sdn.py` — SDN topology
- `7enWSL/src/exercises/ex_7_01_baseline_capture.py` — Baseline capture
- `7enWSL/src/apps/packet_filter.py` — Packet filter

#### The `struct` Module — Binary Parsing

Network protocols have strict binary formats. `struct` converts between bytes and Python types.

```python
import struct

# Format: ! = network byte order (big-endian)
#         H = unsigned short (2 bytes)
#         I = unsigned int (4 bytes)
#         B = unsigned char (1 byte)

# Simplified TCP header parsing
data = b'\x00\x50\x1f\x90...'  # bytes from the network
src_port, dst_port = struct.unpack('!HH', data[:4])
print(f"Source port: {src_port}, Dest port: {dst_port}")

# Header construction
header = struct.pack('!HH', 8080, 443)
```

#### struct Format Table

| Format | C Type | Bytes | Python |
|--------|--------|-------|--------|
| `B` | unsigned char | 1 | int |
| `H` | unsigned short | 2 | int |
| `I` | unsigned int | 4 | int |
| `Q` | unsigned long long | 8 | int |
| `!` | network order | – | big-endian |
| `s` | char[] | n | bytes |

#### IP Header Parsing

```python
import struct
import socket

def parse_ip_header(raw: bytes) -> dict:
    """Extract information from IP header (20 bytes minimum)."""
    if len(raw) < 20:
        raise ValueError("Header too short")
    
    # First 20 bytes of the IP header
    fields = struct.unpack('!BBHHHBBHII', raw[:20])
    
    version_ihl = fields[0]
    version = version_ihl >> 4      # First 4 bits
    ihl = (version_ihl & 0x0F) * 4  # Header length in bytes
    
    return {
        'version': version,
        'header_length': ihl,
        'total_length': fields[2],
        'ttl': fields[5],
        'protocol': fields[6],
        'src_ip': socket.inet_ntoa(struct.pack('!I', fields[8])),
        'dst_ip': socket.inet_ntoa(struct.pack('!I', fields[9])),
    }
```

#### Practical Exploration

1. In `7enWSL/src/apps/packet_filter.py`, see how packets are filtered
2. Extend the parser to extract the "Type of Service" field as well
3. Test with captures from the `pcap/` directory

---

### Step 7: Concurrency
**📅 Correlated with:** Weeks 7-9 and 13 (`7enWSL`, `8enWSL`, `13enWSL`)

#### Why It Matters

Port scanning, multi-client servers and load tests use threading for parallelism.

#### Reference Files

- `13enWSL/src/exercises/ex_13_01_port_scanner.py` — Scanner with ThreadPoolExecutor
- `8enWSL/src/exercises/ex_8_01_http_server.py` — HTTP Server
- `8enWSL/src/exercises/ex_8_02_reverse_proxy.py` — Reverse Proxy

#### Why Threading for Networks?

Network operations are "I/O bound" — the CPU waits for responses. Threading allows simultaneous processing.

#### ThreadPoolExecutor

From `13enWSL/src/exercises/ex_13_01_port_scanner.py`:
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

def scan_ports(host: str, ports: list[int], workers: int = 100) -> list[int]:
    """Scan ports in parallel."""
    open_ports = []
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        # Launch all checks simultaneously
        futures = {executor.submit(check_port, host, p): p for p in ports}
        
        # Collect results as they arrive
        for future in as_completed(futures):
            port, is_open = future.result()
            if is_open:
                open_ports.append(port)
                print(f"Port {port} OPEN")
    
    return sorted(open_ports)
```

#### Server with Threading

```python
import threading

def handle_client(conn, addr):
    """Handler for a client."""
    try:
        data = conn.recv(1024)
        conn.sendall(b"OK: " + data.upper())
    finally:
        conn.close()

# In the main loop:
while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.daemon = True  # Stops when main stops
    thread.start()
```

#### Practical Exploration

1. Run the scanner on a local target:
   ```bash
   python3 13enWSL/src/exercises/ex_13_01_port_scanner.py \
       --target 127.0.0.1 --ports 1-1024 --workers 50
   ```

2. Experiment with different values for `--workers` and measure the time
3. Add a progress bar using `tqdm`

---

### Step 8: HTTP and Application Protocols
**📅 Correlated with:** Weeks 8-12 (`8enWSL` - `12enWSL`)

#### Why It Matters

Many exercises implement HTTP servers or REST clients. Understanding the protocol at socket level aids debugging.

#### Reference Files

- `8enWSL/src/exercises/ex_8_01_http_server.py` — Minimal HTTP server
- `8enWSL/src/exercises/ex_8_02_reverse_proxy.py` — Reverse Proxy
- `10enWSL/src/exercises/ex_10_01_https.py` — HTTPS
- `10enWSL/src/exercises/ex_10_02_rest_levels.py` — REST levels
- `11enWSL/src/exercises/ex_11_01_backend.py` — Backend server
- `11enWSL/src/exercises/ex_11_02_loadbalancer.py` — Load Balancer
- `12enWSL/src/exercises/ex_01_smtp.py` — SMTP
- `12enWSL/src/exercises/ex_02_rpc.py` — RPC

#### HTTP Anatomy

```
GET /index.html HTTP/1.1\r\n
Host: localhost\r\n
Connection: close\r\n
\r\n
```
- Request line: `METHOD PATH VERSION`
- Headers: `Key: Value`
- Empty line (`\r\n\r\n`) separates headers from body

#### Request Parsing (from `ex_8_01_http_server.py`)

```python
def parse_request(raw: bytes) -> tuple[str, str, str, dict[str, str]]:
    """
    Parse an HTTP request.
    
    Returns:
        (method, path, version, headers_dict)
    """
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

#### Response Construction

```python
def build_response(status: int, body: bytes, content_type: str = 'text/html') -> bytes:
    """Build an HTTP response."""
    status_text = {200: 'OK', 404: 'Not Found', 500: 'Internal Server Error'}
    
    headers = f"""HTTP/1.1 {status} {status_text.get(status, 'Unknown')}
Content-Type: {content_type}
Content-Length: {len(body)}
Connection: close

"""
    return headers.replace('\n', '\r\n').encode() + body
```

#### The requests Library

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

#### Practical Exploration

1. Complete the TODOs in `ex_8_01_http_server.py`
2. Test the server with `curl`:
   ```bash
   curl -v http://localhost:8080/index.html
   ```
3. Implement the HEAD method (returns only headers)

---

### Step 9: Practices and Debugging
**📅 Correlated with:** Weeks 11-14 (`11enWSL` - `14enWSL`)

#### Why It Matters

When you extend exercises or create your own tools, you need to write code that works and is easy to debug.

#### Reference Files

- `14enWSL/src/exercises/ex_14_01.py` — Integrated exercise
- `14enWSL/src/exercises/ex_14_02.py` — Advanced load balancer
- `14enWSL/src/exercises/ex_14_03.py` — PCAP analyser
- Any `tests/test_exercises.py`

#### Logging Instead of print

```python
import logging

# Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Usage
logger.info(f"Connecting to {host}:{port}")
logger.debug(f"Data received: {data!r}")  # debug does not appear by default
logger.warning(f"Timeout at {host}")
logger.error(f"Connection failed: {e}")
```

#### Handling Network Exceptions

```python
import socket

try:
    sock.connect((host, port))
    data = sock.recv(1024)
except socket.timeout:
    logger.warning(f"Timeout at {host}:{port}")
except ConnectionRefusedError:
    logger.warning(f"Connection refused by {host}:{port}")
except ConnectionResetError:
    logger.error(f"Connection reset by {host}")
except OSError as e:
    logger.error(f"OS error: {e}")
finally:
    sock.close()
```

#### Quick Debugging

```python
# Display variables with context (Python 3.8+)
x = complex_calculation()
print(f"{x=}")  # Displays: x=value

# Interactive breakpoint
import pdb; pdb.set_trace()  # Stops execution here
# or in Python 3.7+:
breakpoint()
```

#### Tests with pytest

From `tests/test_exercises.py`:
```python
import pytest
from src.exercises.ex_8_01_http_server import parse_request

def test_parse_request_get():
    raw = b"GET /index.html HTTP/1.1\r\nHost: localhost\r\n\r\n"
    method, path, headers = parse_request(raw)
    
    assert method == "GET"
    assert path == "/index.html"
    assert headers["host"] == "localhost"

def test_parse_request_invalid():
    with pytest.raises(ValueError):
        parse_request(b"invalid request")
```

Running:
```bash
cd 8enWSL
python3 -m pytest tests/test_exercises.py -v
```

#### Practical Exploration

1. Add logging to `ex_14_01.py` to trace execution flow
2. Write a test for an existing function
3. Use `breakpoint()` to inspect state during execution

---

## Exploration Exercises by Week

### Weeks 1-2: Fundamentals

| File | What to explore | Python concept |
|------|-----------------|----------------|
| `ex_1_01_ping_latency.py` | `@dataclass`, `subprocess.run()` | Dataclasses, subprocesses |
| `ex_1_02_tcp_server_client.py` | `socket`, `threading` | Basic sockets |
| `ex_1_03_parse_csv.py` | `csv` module, comprehensions | Data processing |
| `ex_1_04_pcap_stats.py` | Binary file reading | File I/O |
| `ex_1_05_transmission_delay.py` | Timing calculations | Mathematical functions |

### Weeks 2-3: Sockets

| File | What to explore | Python concept |
|------|-----------------|----------------|
| `ex_2_01_tcp.py` | `SOCK_STREAM`, `accept()` | TCP sockets |
| `ex_2_02_udp.py` | `SOCK_DGRAM`, `sendto()` | UDP sockets |
| `ex_3_01_udp_broadcast.py` | `SO_BROADCAST` | Socket options |
| `ex_3_02_udp_multicast.py` | `IP_ADD_MEMBERSHIP` | Multicast |
| `ex_3_03_tcp_tunnel.py` | Port forwarding | Threading + sockets |

### Weeks 4-5: Protocols and CLI

| File | What to explore | Python concept |
|------|-----------------|----------------|
| `ex_4_*.py` | Text/binary protocols | `struct`, protocol design |
| `ex_5_01_cidr_flsm.py` | `ipaddress` module | IP manipulation |
| `ex_5_02_vlsm_ipv6.py` | IPv6 handling | Network calculations |
| `ex_5_03_quiz_generator.py` | Interactive CLI | Advanced `argparse` |

### Weeks 6-9: NAT, Firewall, HTTP

| File | What to explore | Python concept |
|------|-----------------|----------------|
| `topo_nat.py`, `topo_sdn.py` | Mininet integration | Network simulation |
| `ex_7_01_baseline_capture.py` | Packet capture | Binary parsing |
| `ex_8_01_http_server.py` | HTTP from scratch | Protocol implementation |
| `ex_8_02_reverse_proxy.py` | Request forwarding | Proxy pattern |
| `ex_9_01_endianness.py` | Byte order | `struct` packing |
| `ex_9_02_pseudo_ftp.py` | FTP protocol | State machine |

### Weeks 10-14: Applications

| File | What to explore | Python concept |
|------|-----------------|----------------|
| `ex_10_01_https.py` | TLS/SSL | `ssl` module |
| `ex_10_02_rest_levels.py` | REST architecture | HTTP methods |
| `ex_11_02_loadbalancer.py` | Round-robin | Load balancing |
| `ex_11_03_dns_client.py` | DNS queries | UDP protocol |
| `ex_12_*` | SMTP, RPC | Application protocols |
| `ex_13_01_port_scanner.py` | Parallel scanning | `concurrent.futures` |
| `ex_13_02_mqtt_client.py` | MQTT protocol | IoT messaging |
| `ex_14_*` | Integration | All concepts |

---

## Python-Networking Quick Reference

### Essential Libraries

```python
# Basic networking
import socket                    # TCP/UDP sockets
import ssl                       # TLS/SSL wrapper
import struct                    # Binary packing/unpacking

# IP and addresses
import ipaddress                 # IP address manipulation

# CLI
import argparse                  # Command line arguments

# Concurrency
import threading                 # Thread-based parallelism
from concurrent.futures import ThreadPoolExecutor

# HTTP (client)
import requests                  # pip install requests

# Logging
import logging

# JSON
import json

# Processes
import subprocess
```

### Socket Cheatsheet

```python
# TCP Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 8080))
server.listen(5)
conn, addr = server.accept()
data = conn.recv(1024)
conn.sendall(b"response")
conn.close()

# TCP Client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8080))
client.sendall(b"request")
response = client.recv(1024)
client.close()

# UDP Server
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('0.0.0.0', 8080))
data, addr = server.recvfrom(1024)
server.sendto(b"response", addr)

# UDP Client
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(b"request", ('127.0.0.1', 8080))
response, _ = client.recvfrom(1024)
```

### struct Format Codes

```python
# Network byte order (big-endian): prefix with '!'
struct.pack('!H', 8080)         # unsigned short (2 bytes)
struct.pack('!I', 0xC0A80101)   # unsigned int (4 bytes)
struct.pack('!4s', b'\xC0\xA8\x01\x01')  # 4 bytes string

# Unpack
port, = struct.unpack('!H', data[:2])
ip_int, = struct.unpack('!I', data[2:6])
```

---

## Further Resources

### Official Documentation
- [Python Socket HOWTO](https://docs.python.org/3/howto/sockets.html)
- [struct Module](https://docs.python.org/3/library/struct.html)
- [ipaddress Module](https://docs.python.org/3/library/ipaddress.html)
- [argparse Tutorial](https://docs.python.org/3/howto/argparse.html)

### Practice
- [Exercism Python Track](https://exercism.org/tracks/python)
- [Build Your Own X - Network Stack](https://github.com/codecrafters-io/build-your-own-x)

### Books (Optional)
- "Black Hat Python" — Network security with Python
- "Foundations of Python Network Programming"

---

## FAQ

**Q: Do I need to complete all steps in order?**  
A: No. You can jump to the step relevant to your current laboratory week.

**Q: What if I do not understand something?**  
A: Run the code, modify values, observe what changes. Experimentation is the best teacher.

**Q: Do I need to memorise the syntax?**  
A: No. Use the documentation and examples from the kits.

**Q: How do I test whether I have understood?**  
A: Try modifying an existing exercise or adding a new feature.

---

*Material produced as optional support for the Computer Networks course.*  
*Repository: [github.com/antonioclim/netENwsl](https://github.com/antonioclim/netENwsl)*  
*Version: January 2025*
