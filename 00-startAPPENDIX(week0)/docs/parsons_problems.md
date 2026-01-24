# 🧩 Parsons Problems — Week 0
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Reorder the code blocks to create a working solution.
> Each problem includes one **distractor block** that should NOT be used.

---

## How to Use These Problems

1. Read the task description carefully
2. Examine all code blocks (some are distractors!)
3. Arrange the correct blocks in the proper order
4. Check your solution against the hidden answer
5. Discuss with a partner why certain blocks are distractors

---

## Problem P1: TCP Client Connection

### Task

Create a TCP client that connects to a server, sends a message and receives a response.

### Scrambled Blocks

```python
# Block A
    response = sock.recv(1024)
    print(f"Received: {response.decode()}")

# Block B
def tcp_client(host: str, port: int, message: str) -> None:

# Block C
    sock.connect((host, port))
    sock.sendall(message.encode())

# Block D
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Block E
    sock.close()

# Block F (DISTRACTOR)
    sock.bind(('', 0))

# Block G (DISTRACTOR)
    sock.listen(5)
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block B
def tcp_client(host: str, port: int, message: str) -> None:

# Block D
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Block C
    sock.connect((host, port))
    sock.sendall(message.encode())

# Block A
    response = sock.recv(1024)
    print(f"Received: {response.decode()}")

# Block E
    sock.close()
```

**Distractors explained:**
- **Block F** (`bind()`) — Used by servers to bind to a local address, not by clients
- **Block G** (`listen()`) — Used by servers to start listening for connections, not by clients

**Key concept:** TCP clients use `connect()` to reach the server; `bind()` and `listen()` are server-side operations.

</details>

---

## Problem P2: Binary Protocol Header Parsing

### Task

Parse a simple binary protocol header using `struct.unpack()`. The header format is:
- Version: 1 byte (unsigned)
- Message type: 1 byte (unsigned)  
- Payload length: 2 bytes (unsigned, big-endian)
- Timestamp: 4 bytes (unsigned, big-endian)

### Scrambled Blocks

```python
# Block A
    return version, msg_type, length, timestamp

# Block B
def parse_header(data: bytes) -> tuple[int, int, int, int]:

# Block C
    version, msg_type, length, timestamp = struct.unpack('!BBHI', data[:8])

# Block D
    if len(data) < 8:
        raise ValueError("Header too short")

# Block E (DISTRACTOR)
    version, msg_type, length, timestamp = struct.unpack('BBHI', data[:8])

# Block F (DISTRACTOR)
    header = data.decode('utf-8')[:8]
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block B
def parse_header(data: bytes) -> tuple[int, int, int, int]:

# Block D
    if len(data) < 8:
        raise ValueError("Header too short")

# Block C
    version, msg_type, length, timestamp = struct.unpack('!BBHI', data[:8])

# Block A
    return version, msg_type, length, timestamp
```

**Distractors explained:**
- **Block E** — Missing `!` prefix for network byte order (big-endian). Without it, the system's native byte order is used, which may be wrong on little-endian machines.
- **Block F** — Binary data cannot be decoded as UTF-8; protocol headers are binary, not text.

**Key concept:** Network protocols use big-endian byte order. The `!` in struct format strings ensures correct byte order regardless of the local machine's architecture.

</details>

---

## Problem P3: TCP Server Socket Setup

### Task

Create and configure a TCP server socket that listens on a specified port and accepts one connection.

### Scrambled Blocks

```python
# Block A
    server_sock.listen(1)
    print(f"Server listening on port {port}")

# Block B
def create_server(port: int) -> socket.socket:

# Block C
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Block D
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Block E
    server_sock.bind(('', port))

# Block F
    return server_sock

# Block G (DISTRACTOR)
    server_sock.connect(('localhost', port))
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block B
def create_server(port: int) -> socket.socket:

# Block D
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Block C
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Block E
    server_sock.bind(('', port))

# Block A
    server_sock.listen(1)
    print(f"Server listening on port {port}")

# Block F
    return server_sock
```

**Distractor explained:**
- **Block G** (`connect()`) — This is a client operation. Servers do not connect to themselves; they `bind()` and `listen()`.

**Key concept:** Server socket sequence is always: create → setsockopt → bind → listen. The `SO_REUSEADDR` option allows immediate port reuse after server restart.

</details>

---

## Problem P4: Bytes to String Encoding

### Task

Create a function that safely converts bytes to a string, handling potential encoding errors gracefully.

### Scrambled Blocks

```python
# Block A
    except UnicodeDecodeError:
        return data.decode('utf-8', errors='replace')

# Block B
def safe_decode(data: bytes) -> str:

# Block C
    try:
        return data.decode('utf-8')

# Block D (DISTRACTOR)
    return str(data)

# Block E (DISTRACTOR)
    return data.encode('utf-8')
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block B
def safe_decode(data: bytes) -> str:

# Block C
    try:
        return data.decode('utf-8')

# Block A
    except UnicodeDecodeError:
        return data.decode('utf-8', errors='replace')
```

**Distractors explained:**
- **Block D** (`str(data)`) — This produces `"b'...'"` representation, not the actual decoded string
- **Block E** (`encode()`) — This converts strings TO bytes, not bytes to strings (opposite direction)

**Key concept:** `decode()` converts bytes→str, `encode()` converts str→bytes. Using `errors='replace'` substitutes invalid bytes with the Unicode replacement character (�).

</details>

---

## Problem P5: struct.pack() for Network Protocol

### Task

Create a function that packs a network message with a 2-byte port number (big-endian) followed by a 4-byte IP address (as integer, big-endian).

### Scrambled Blocks

```python
# Block A
    return struct.pack('!HI', port, ip_int)

# Block B
def pack_address(port: int, ip_int: int) -> bytes:

# Block C
    if not (0 <= port <= 65535):
        raise ValueError("Port must be 0-65535")

# Block D (DISTRACTOR)
    return struct.pack('HI', port, ip_int)

# Block E (DISTRACTOR)
    return f"{port}:{ip_int}".encode()
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block B
def pack_address(port: int, ip_int: int) -> bytes:

# Block C
    if not (0 <= port <= 65535):
        raise ValueError("Port must be 0-65535")

# Block A
    return struct.pack('!HI', port, ip_int)
```

**Distractors explained:**
- **Block D** — Missing `!` for network byte order. Would produce incorrect byte order on little-endian systems.
- **Block E** — Creates a text representation, not binary protocol data. Network protocols need exact binary formats, not human-readable strings.

**Key concept:** The `!` prefix in struct format is essential for network protocols. `H` = unsigned short (2 bytes), `I` = unsigned int (4 bytes).

</details>

---

## Summary: Common Patterns

### Server vs Client Operations

| Operation | Server | Client |
|-----------|--------|--------|
| `socket()` | ✅ | ✅ |
| `bind()` | ✅ | ❌ (usually) |
| `listen()` | ✅ | ❌ |
| `accept()` | ✅ | ❌ |
| `connect()` | ❌ | ✅ |

### Encoding Direction

| Operation | Direction | Example |
|-----------|-----------|---------|
| `encode()` | str → bytes | `"hello".encode()` → `b'hello'` |
| `decode()` | bytes → str | `b'hello'.decode()` → `"hello"` |

### struct Format Characters

| Char | Type | Size | Network order |
|------|------|------|---------------|
| `B` | unsigned char | 1 byte | N/A |
| `H` | unsigned short | 2 bytes | `!H` |
| `I` | unsigned int | 4 bytes | `!I` |
| `!` | network (big-endian) | prefix | Required for protocols |

---

## Self-Assessment

After completing these problems, you should be able to:

- [ ] Distinguish between client and server socket operations
- [ ] Use `struct.pack()` and `struct.unpack()` with correct byte order
- [ ] Handle bytes↔string conversion safely
- [ ] Identify common networking code mistakes

---

*Parsons Problems — Week 0 | Computer Networks | ASE-CSIE*
