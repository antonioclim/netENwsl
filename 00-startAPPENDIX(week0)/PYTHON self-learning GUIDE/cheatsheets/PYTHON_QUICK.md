# 🚀 Quick Python for C/JavaScript Programmers

## Syntax Equivalences

| C/JavaScript | Python | Notes |
|--------------|--------|-------|
| `int x = 5;` | `x = 5` | No type declaration |
| `if (x > 0) { }` | `if x > 0:` | Indentation instead of braces |
| `for (int i=0; i<n; i++)` | `for i in range(n):` | range() generates the sequence |
| `while (cond) { }` | `while cond:` | No parentheses |
| `true / false` | `True / False` | First letter capitalised |
| `null` | `None` | The null value |
| `&&` / `||` / `!` | `and` / `or` / `not` | Logical operators in words |
| `arr.length` | `len(arr)` | Global function |
| `arr.push(x)` | `arr.append(x)` | Append to list |
| `dict[key]` | `dict[key]` or `dict.get(key)` | get() returns None if missing |

## Minimal TCP Socket

```python
import socket

# Server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 8080))
    s.listen(5)
    conn, addr = s.accept()
    with conn:
        data = conn.recv(1024)
        conn.sendall(b"OK")

# Client
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('127.0.0.1', 8080))
    s.sendall(b"Hello")
    response = s.recv(1024)
```

## bytes vs str

```python
# String → Bytes (for sending over network)
text = "Hello"
octets = text.encode('utf-8')  # b'Hello'

# Bytes → String (for display)
octets = b"Hello"
text = octets.decode('utf-8')  # 'Hello'
```

## struct for Binary Parsing

```python
import struct

# ! = network byte order (big-endian)
# H = unsigned short (2 bytes)
# I = unsigned int (4 bytes)
# B = unsigned char (1 byte)

# Pack
header = struct.pack('!HH', 8080, 443)  # src_port, dst_port

# Unpack
src_port, dst_port = struct.unpack('!HH', data[:4])
```

## Minimal argparse

```python
import argparse

parser = argparse.ArgumentParser(description="Tool")
parser.add_argument("target", help="Target")
parser.add_argument("--port", "-p", type=int, default=80)
parser.add_argument("--verbose", "-v", action="store_true")
args = parser.parse_args()

print(f"{args.target}:{args.port}")
```

## ThreadPoolExecutor

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def task(x):
    return x * 2

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(task, i): i for i in range(100)}
    for future in as_completed(futures):
        result = future.result()
```

## Manual HTTP Request

```python
# Request format
request = b"GET /index.html HTTP/1.1\r\nHost: localhost\r\n\r\n"

# Response format
response = b"HTTP/1.1 200 OK\r\nContent-Length: 5\r\n\r\nHello"
```
