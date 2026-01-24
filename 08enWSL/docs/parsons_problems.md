# 🧩 Parsons Problems — Week 8
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Reorder the code blocks to create a working solution.
> Some blocks may be distractors (not needed).

---

## How to Solve Parsons Problems

1. **Read the task description** carefully
2. **Identify the goal** — what should the code accomplish?
3. **Look for dependencies** — which blocks need data from others?
4. **Watch for distractors** — blocks that look relevant but aren't needed
5. **Check indentation** — Python indentation matters!

---

## Problem P1: TCP Server Setup

### Task

Create a TCP server that:
1. Creates a socket
2. Allows address reuse
3. Binds to port 8080
4. Listens for connections
5. Accepts one client

### Scrambled Blocks

```python
# Block A
server.listen(5)

# Block B
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Block C
client, address = server.accept()

# Block D
server.bind(('0.0.0.0', 8080))

# Block E
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Block F (DISTRACTOR)
server.connect(('localhost', 8080))

# Block G
import socket

# Block H (DISTRACTOR)
server.sendall(b'Hello')
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block G - import first
import socket

# Block B - create socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Block E - set options before bind
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Block D - bind to address
server.bind(('0.0.0.0', 8080))

# Block A - start listening
server.listen(5)

# Block C - accept connection
client, address = server.accept()
```

**Distractors:**
- **Block F** (`connect`) — That's for clients, not servers!
- **Block H** (`sendall`) — We haven't received anything yet

**Order reasoning:**
1. Import must come first
2. Create socket before using it
3. Set options before bind (SO_REUSEADDR won't work after)
4. Bind before listen
5. Listen before accept
</details>

---

## Problem P2: HTTP Response Builder

### Task

Build an HTTP 200 OK response with:
- Status line
- Content-Type header
- Content-Length header
- Blank line separator
- Body content

### Scrambled Blocks

```python
# Block A
response = status_line + headers + blank_line + body

# Block B
blank_line = "\r\n"

# Block C
body = "<h1>Welcome</h1>"

# Block D
status_line = "HTTP/1.1 200 OK\r\n"

# Block E
headers = f"Content-Type: text/html\r\nContent-Length: {len(body)}\r\n"

# Block F (DISTRACTOR)
headers = "Content-Type: text/html\n"

# Block G (DISTRACTOR)
blank_line = "\n\n"

# Block H
return response.encode('utf-8')
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block C - define body first (needed for Content-Length)
body = "<h1>Welcome</h1>"

# Block D - status line
status_line = "HTTP/1.1 200 OK\r\n"

# Block E - headers (uses len(body))
headers = f"Content-Type: text/html\r\nContent-Length: {len(body)}\r\n"

# Block B - blank line separator
blank_line = "\r\n"

# Block A - combine all parts
response = status_line + headers + blank_line + body

# Block H - encode for network transmission
return response.encode('utf-8')
```

**Distractors:**
- **Block F** — Uses `\n` instead of `\r\n` (HTTP requires CRLF)
- **Block G** — Uses `\n\n` instead of `\r\n` (wrong line ending)

**Key insight:** Body must be defined BEFORE headers because Content-Length needs `len(body)`.
</details>

---

## Problem P3: Round-Robin Next Backend

### Task

Implement `next_backend()` that:
1. Acquires a thread lock
2. Checks if any backends exist
3. Gets the current backend
4. Increments index with wraparound
5. Returns the selected backend

### Scrambled Blocks

```python
# Block A
def next_backend(self):

# Block B
    with self.lock:

# Block C
        return None

# Block D
        if not self.backends:

# Block E
        backend = self.backends[self.index]

# Block F
        self.index = (self.index + 1) % len(self.backends)

# Block G
        return backend

# Block H (DISTRACTOR)
        self.index = self.index + 1

# Block I (DISTRACTOR)
    backend = self.backends[0]
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block A - function definition
def next_backend(self):

# Block B - acquire lock (context manager)
    with self.lock:

# Block D - check for empty list
        if not self.backends:

# Block C - return None if empty
            return None

# Block E - get current backend
        backend = self.backends[self.index]

# Block F - increment with wraparound
        self.index = (self.index + 1) % len(self.backends)

# Block G - return selected backend
        return backend
```

**Distractors:**
- **Block H** — No wraparound! Would cause IndexError after first cycle
- **Block I** — Always returns first backend (no round-robin)

**Key insight:** The modulo `%` operation is essential for wraparound:
- Index 0 → 1 → 2 → 0 → 1 → 2 → ... (with 3 backends)
</details>

---

## Problem P4: Safe Path Validation

### Task

Check if a requested path is safe (within document root):
1. Normalise the path to remove `..` and `.`
2. Build the full path
3. Get absolute paths
4. Check if full path starts with docroot

### Scrambled Blocks

```python
# Block A
def is_safe_path(requested, docroot):

# Block B
    normalised = os.path.normpath(requested)

# Block C
    full_path = os.path.join(docroot, normalised.lstrip('/'))

# Block D
    abs_docroot = os.path.abspath(docroot)

# Block E
    abs_full = os.path.abspath(full_path)

# Block F
    return abs_full.startswith(abs_docroot)

# Block G (DISTRACTOR)
    return requested.startswith(docroot)

# Block H (DISTRACTOR)
    if '..' in requested:
        return False

# Block I
    import os
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block I - import
import os

# Block A - function definition
def is_safe_path(requested, docroot):

# Block B - normalise to collapse .. and .
    normalised = os.path.normpath(requested)

# Block C - build full path (strip leading / to join correctly)
    full_path = os.path.join(docroot, normalised.lstrip('/'))

# Block D - get absolute docroot
    abs_docroot = os.path.abspath(docroot)

# Block E - get absolute full path
    abs_full = os.path.abspath(full_path)

# Block F - check containment
    return abs_full.startswith(abs_docroot)
```

**Distractors:**
- **Block G** — Compares unnormalised paths (vulnerable to `..\` attacks)
- **Block H** — Simple string check is bypassable (encoded `..`, etc.)

**Why normalise BEFORE joining?**
```
Path: /../../../etc/passwd
After normpath: /etc/passwd
After lstrip('/'): etc/passwd
After join with /var/www: /var/www/etc/passwd ✓ (safe)
```
</details>

---

## Problem P5: Forward Request to Backend

### Task

Forward an HTTP request to a backend server:
1. Create a socket
2. Set timeout
3. Connect to backend
4. Send request
5. Receive response
6. Close socket
7. Return response

### Scrambled Blocks

```python
# Block A
def forward_request(request, backend_host, backend_port):

# Block B
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Block C
    sock.settimeout(10)

# Block D
    sock.connect((backend_host, backend_port))

# Block E
    sock.sendall(request)

# Block F
    response = b''
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk

# Block G
    sock.close()

# Block H
    return response

# Block I (DISTRACTOR)
    sock.bind(('0.0.0.0', 0))

# Block J (DISTRACTOR)
    sock.listen(1)

# Block K
    import socket
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block K - import
import socket

# Block A - function definition
def forward_request(request, backend_host, backend_port):

# Block B - create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Block C - set timeout before connect
    sock.settimeout(10)

# Block D - connect to backend
    sock.connect((backend_host, backend_port))

# Block E - send request
    sock.sendall(request)

# Block F - receive full response
    response = b''
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk

# Block G - cleanup
    sock.close()

# Block H - return result
    return response
```

**Distractors:**
- **Block I** (`bind`) — Clients don't need to bind; OS assigns ephemeral port
- **Block J** (`listen`) — That's for servers! Clients connect, not listen

**Key insight:** The recv loop is necessary because:
- `recv()` may not return all data at once
- We keep reading until empty bytes (connection closed)
- TCP is a stream; we must reassemble the full response
</details>

---

## Problem P6: Add Proxy Headers

### Task

Add `X-Forwarded-For` header to an HTTP request:
1. Split request into lines
2. Find where headers end (blank line)
3. Insert new header before blank line
4. Rejoin lines

### Scrambled Blocks

```python
# Block A
def add_xff_header(request_str, client_ip):

# Block B
    lines = request_str.split('\r\n')

# Block C
    for i, line in enumerate(lines):
        if line == '':
            insert_pos = i
            break

# Block D
    new_header = f"X-Forwarded-For: {client_ip}"

# Block E
    lines.insert(insert_pos, new_header)

# Block F
    return '\r\n'.join(lines)

# Block G (DISTRACTOR)
    lines.append(new_header)

# Block H (DISTRACTOR)
    lines[0] = new_header

# Block I
    insert_pos = 1  # default after request line
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block A - function definition
def add_xff_header(request_str, client_ip):

# Block B - split into lines
    lines = request_str.split('\r\n')

# Block I - default insert position
    insert_pos = 1  # default after request line

# Block C - find blank line (end of headers)
    for i, line in enumerate(lines):
        if line == '':
            insert_pos = i
            break

# Block D - create new header
    new_header = f"X-Forwarded-For: {client_ip}"

# Block E - insert before blank line
    lines.insert(insert_pos, new_header)

# Block F - rejoin
    return '\r\n'.join(lines)
```

**Distractors:**
- **Block G** (`append`) — Would add AFTER body, not in headers
- **Block H** (`lines[0]`) — Would replace request line!

**Why insert, not append?**
```
Before:
GET / HTTP/1.1\r\n
Host: example.com\r\n
\r\n                    <-- blank line (end of headers)
<body>

After insert at blank line position:
GET / HTTP/1.1\r\n
Host: example.com\r\n
X-Forwarded-For: 192.168.1.1\r\n  <-- inserted
\r\n                               <-- blank line pushed down
<body>
```
</details>

---

## Summary: Key Patterns

| Problem | Key Pattern | Common Mistake |
|---------|-------------|----------------|
| P1: Server Setup | Create → Options → Bind → Listen → Accept | Using `connect` on server |
| P2: HTTP Response | Body first (for length), then headers, then combine | Wrong line endings |
| P3: Round-Robin | Modulo for wraparound | Unbounded index increment |
| P4: Safe Path | Normalise BEFORE join | Simple string check |
| P5: Forward Request | Loop recv until empty | Single recv call |
| P6: Proxy Headers | Insert before blank line | Append after body |

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
