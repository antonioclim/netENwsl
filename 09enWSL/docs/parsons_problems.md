# 🧩 Parsons Problems — Week 9
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Reorder the code blocks to create a working solution.

Parsons Problems help you understand code structure without the cognitive load of syntax. Focus on the LOGIC and ORDER of operations.

---

## How to Solve Parsons Problems

1. **Read** the task description carefully
2. **Identify** the first and last blocks (often obvious)
3. **Group** related blocks together
4. **Order** blocks within each group
5. **Watch out** for distractors (blocks that shouldn't be used)
6. **Verify** by tracing through mentally

---

## Problem P1: Pack a Network Message

### Task

Create a function that packs a payload into a network message with:
- 4-byte magic number "NET9"
- 4-byte payload length (network byte order)
- 4-byte CRC-32 checksum
- The payload bytes

### Scrambled Blocks

```python
# Block A
    return header + payload

# Block B
def pack_message(payload: bytes) -> bytes:

# Block C
    crc = zlib.crc32(payload) & 0xFFFFFFFF

# Block D
    header = struct.pack(">4sII", magic, length, crc)

# Block E
import struct
import zlib

# Block F
    length = len(payload)

# Block G
    magic = b"NET9"

# Block H (DISTRACTOR - not needed)
    payload = payload.encode("utf-8")

# Block I (DISTRACTOR - not needed)
    header = struct.pack("<4sII", magic, length, crc)
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block E - Imports must come first
import struct
import zlib

# Block B - Function definition
def pack_message(payload: bytes) -> bytes:

# Block G - Define magic bytes
    magic = b"NET9"

# Block F - Calculate length
    length = len(payload)

# Block C - Calculate CRC
    crc = zlib.crc32(payload) & 0xFFFFFFFF

# Block D - Pack header (big-endian!)
    header = struct.pack(">4sII", magic, length, crc)

# Block A - Return combined message
    return header + payload
```

**Why these blocks are wrong:**
- **Block H:** The function already takes `bytes`, no encoding needed
- **Block I:** Uses little-endian (`<`) instead of network byte order (`>`)

**Key insight:** Network protocols use big-endian byte order. The magic, length and CRC form a 12-byte header.

</details>

---

## Problem P2: Receive Exactly N Bytes

### Task

Create a function that receives exactly `n` bytes from a socket, handling the case where `recv()` returns fewer bytes than requested.

### Scrambled Blocks

```python
# Block A
def recv_exactly(sock, n: int) -> bytes:

# Block B
    while len(data) < n:

# Block C
        data += chunk

# Block D
    data = b""

# Block E
    return data

# Block F
        chunk = sock.recv(n - len(data))

# Block G
        if not chunk:
            raise ConnectionError("Connection closed")

# Block H (DISTRACTOR)
    return sock.recv(n)

# Block I (DISTRACTOR)
        chunk = sock.recv(1024)
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block A - Function definition
def recv_exactly(sock, n: int) -> bytes:

# Block D - Initialise empty buffer
    data = b""

# Block B - Loop until we have enough
    while len(data) < n:

# Block F - Request only remaining bytes
        chunk = sock.recv(n - len(data))

# Block G - Handle connection closure
        if not chunk:
            raise ConnectionError("Connection closed")

# Block C - Append received data
        data += chunk

# Block E - Return complete buffer
    return data
```

**Why these blocks are wrong:**
- **Block H:** `recv(n)` may return FEWER than n bytes — TCP doesn't guarantee message boundaries
- **Block I:** Using fixed buffer size 1024 might receive MORE than needed if another message follows

**Key insight:** TCP is a byte stream. You must loop and accumulate until you have exactly the bytes you need.

</details>

---

## Problem P3: Parse FTP PASV Response

### Task

Create a function that parses an FTP PASV response like:
`"227 Entering Passive Mode (192,168,1,5,234,100)"`

And returns a tuple of (ip_address, port_number).

### Scrambled Blocks

```python
# Block A
def parse_pasv(response: str) -> tuple[str, int]:

# Block B
    start = response.index("(") + 1
    end = response.index(")")

# Block C
    parts = inner.split(",")

# Block D
    ip = f"{parts[0]}.{parts[1]}.{parts[2]}.{parts[3]}"

# Block E
    port = int(parts[4]) * 256 + int(parts[5])

# Block F
    return ip, port

# Block G
    inner = response[start:end]

# Block H (DISTRACTOR)
    port = int(parts[4]) + int(parts[5])

# Block I (DISTRACTOR)
    ip = parts[0:4].join(".")

# Block J (DISTRACTOR)
    port = int(parts[4]) * 255 + int(parts[5])
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block A - Function definition
def parse_pasv(response: str) -> tuple[str, int]:

# Block B - Find parentheses positions
    start = response.index("(") + 1
    end = response.index(")")

# Block G - Extract content between parentheses
    inner = response[start:end]

# Block C - Split by comma
    parts = inner.split(",")

# Block D - Build IP address
    ip = f"{parts[0]}.{parts[1]}.{parts[2]}.{parts[3]}"

# Block E - Calculate port
    port = int(parts[4]) * 256 + int(parts[5])

# Block F - Return result
    return ip, port
```

**Why these blocks are wrong:**
- **Block H:** Port = p1 + p2 is wrong; correct formula is p1 × 256 + p2
- **Block I:** Syntax error — should be `".".join(parts[0:4])`
- **Block J:** Port = p1 × 255 + p2 is wrong; byte range is 0-255 so multiplier is 256

**Key insight:** The PASV port encoding uses two bytes: port = high_byte × 256 + low_byte. This allows ports 0-65535.

</details>

---

## Problem P4: FTP Session Login

### Task

Create a function that logs into an FTP server using the control connection. The function should send USER and PASS commands and verify the responses.

### Scrambled Blocks

```python
# Block A
def ftp_login(sock, username: str, password: str) -> bool:

# Block B
    sock.sendall(f"USER {username}\r\n".encode())

# Block C
    response = sock.recv(1024).decode()

# Block D
    if not response.startswith("331"):
        return False

# Block E
    sock.sendall(f"PASS {password}\r\n".encode())

# Block F
    response = sock.recv(1024).decode()

# Block G
    return response.startswith("230")

# Block H (DISTRACTOR)
    if not response.startswith("220"):
        return False

# Block I (DISTRACTOR)
    sock.sendall(f"USER {username}\n".encode())

# Block J (DISTRACTOR)
    return response.startswith("200")
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block A - Function definition
def ftp_login(sock, username: str, password: str) -> bool:

# Block B - Send USER command
    sock.sendall(f"USER {username}\r\n".encode())

# Block C - Receive response
    response = sock.recv(1024).decode()

# Block D - Check for 331 (password required)
    if not response.startswith("331"):
        return False

# Block E - Send PASS command
    sock.sendall(f"PASS {password}\r\n".encode())

# Block F - Receive response
    response = sock.recv(1024).decode()

# Block G - Check for 230 (login successful)
    return response.startswith("230")
```

**Why these blocks are wrong:**
- **Block H:** 220 is the welcome banner, not the USER response
- **Block I:** FTP uses `\r\n` (CRLF) line endings, not just `\n`
- **Block J:** 200 is "Command OK", not "Login successful" (which is 230)

**Key insight:** FTP response codes follow a pattern:
- 2xx = Success
- 3xx = Need more info (like password)
- 4xx/5xx = Error

</details>

---

## Bonus Problem P5: Session State Tracking

### Task

Complete a Session class that tracks authentication state and current directory. The `change_dir` method should prevent directory traversal attacks.

### Scrambled Blocks

```python
# Block A
class Session:

# Block B
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.authenticated = False
        self.cwd = Path("/")

# Block C
    def is_authenticated(self) -> bool:
        return self.authenticated

# Block D
    def change_dir(self, path: str) -> bool:
        try:
            new_path = (self.root / self.cwd / path).resolve()

# Block E
            new_path.relative_to(self.root)  # Raises if outside root

# Block F
            if new_path.is_dir():
                self.cwd = new_path.relative_to(self.root)
                return True
        except (ValueError, FileNotFoundError):
            pass
        return False

# Block G (DISTRACTOR)
            self.cwd = Path(path)  # Allows escape!
            return True

# Block H (DISTRACTOR)
            new_path = Path(path).resolve()  # Ignores root!
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block A - Class definition
class Session:

# Block B - Constructor
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.authenticated = False
        self.cwd = Path("/")

# Block C - Authentication check
    def is_authenticated(self) -> bool:
        return self.authenticated

# Block D - Start of change_dir
    def change_dir(self, path: str) -> bool:
        try:
            new_path = (self.root / self.cwd / path).resolve()

# Block E - Security check
            new_path.relative_to(self.root)  # Raises if outside root

# Block F - Update state if valid
            if new_path.is_dir():
                self.cwd = new_path.relative_to(self.root)
                return True
        except (ValueError, FileNotFoundError):
            pass
        return False
```

**Why these blocks are wrong:**
- **Block G:** Directly assigns path without validation — allows `../../etc/passwd`
- **Block H:** Resolves path without considering root — allows absolute path escape

**Key insight:** Path traversal prevention requires:
1. Resolve the full path (handle `..` and symlinks)
2. Verify result is still within the allowed root
3. Use `relative_to()` which raises ValueError if path is outside

</details>

---

## Self-Assessment Checklist

After completing these problems, verify you understand:

- [ ] Network byte order is big-endian (`>` in struct)
- [ ] TCP recv() may return fewer bytes than requested
- [ ] FTP PASV port = p1 × 256 + p2
- [ ] FTP uses CRLF (`\r\n`) line endings
- [ ] FTP response 331 = need password, 230 = success
- [ ] Path traversal prevention requires explicit validation

---

## Tips for Future Parsons Problems

1. **Imports always first** — Look for `import` statements
2. **Function def before body** — `def` comes before its implementation
3. **Indentation matters** — Group blocks by indent level
4. **Watch for off-by-one** — Common in byte order multipliers (255 vs 256)
5. **Protocol details** — Line endings, response codes, byte order

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Week 9: Session Layer and Presentation Layer*
