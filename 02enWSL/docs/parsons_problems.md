# 🧩 Parsons Problems — Week 2: Sockets and Transport Protocols

> NETWORKING class — ASE, CSIE Bucharest  
> Computer Networks Laboratory | by ing. dr. Antonio Clim

Reorder the scrambled code blocks to create working solutions. Some blocks are **distractors** — they don't belong in the solution!

---

## Problem P1: TCP Server Setup

### Task

Create a TCP server that listens on port 9090 and accepts one connection.

### Scrambled Blocks

```python
# Block A
sock.listen(5)

# Block B
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Block C
conn, addr = sock.accept()

# Block D (DISTRACTOR)
sock.connect(("0.0.0.0", 9090))

# Block E
sock.bind(("0.0.0.0", 9090))

# Block F
import socket

# Block G (DISTRACTOR)
sock.sendto(b"Hello", addr)

# Block H
print(f"Connection from {addr}")
```

### Hints

- How many blocks are distractors?
- What's the correct order: bind → listen → accept, or listen → bind → accept?
- Which block initiates a connection vs accepts one?

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block F
import socket

# Block B
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Block E
sock.bind(("0.0.0.0", 9090))

# Block A
sock.listen(5)

# Block C
conn, addr = sock.accept()

# Block H
print(f"Connection from {addr}")
```

**Distractors explained:**
- **Block D** (`connect`) — Used by clients, not servers
- **Block G** (`sendto`) — UDP method, not TCP

**Order rationale:**
1. Import the module
2. Create socket (SOCK_STREAM = TCP)
3. Bind to local address
4. Listen (marks socket as passive)
5. Accept (blocks until client connects)
6. Use the connection

</details>

---

## Problem P2: UDP Client Send-Receive

### Task

Create a UDP client that sends "ping" to a server and receives a response.

### Scrambled Blocks

```python
# Block A
response, server = sock.recvfrom(1024)

# Block B
sock.sendto(b"ping", ("127.0.0.1", 9091))

# Block C (DISTRACTOR)
sock.connect(("127.0.0.1", 9091))

# Block D
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Block E (DISTRACTOR)
conn, addr = sock.accept()

# Block F
print(f"Received: {response}")

# Block G
import socket

# Block H (DISTRACTOR)
sock.listen(5)
```

### Hints

- UDP uses which socket type constant?
- Does UDP require connect() before sending?
- Which method receives UDP datagrams?

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block G
import socket

# Block D
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Block B
sock.sendto(b"ping", ("127.0.0.1", 9091))

# Block A
response, server = sock.recvfrom(1024)

# Block F
print(f"Received: {response}")
```

**Distractors explained:**
- **Block C** (`connect`) — Not required for UDP (though optional)
- **Block E** (`accept`) — TCP server method, not UDP
- **Block H** (`listen`) — TCP server method, not UDP

**Key insight:** UDP is connectionless — just create socket, send, receive!

</details>

---

## Problem P3: Threaded Client Handler

### Task

Create a function that spawns a new thread to handle a TCP client connection.

### Scrambled Blocks

```python
# Block A
t.start()

# Block B
def handle_client(conn, addr):
    data = conn.recv(1024)
    conn.send(data.upper())
    conn.close()

# Block C (DISTRACTOR)
t.join()  # Wait for thread to finish

# Block D
t = threading.Thread(target=handle_client, args=(conn, addr))

# Block E
import threading

# Block F
conn, addr = sock.accept()

# Block G (DISTRACTOR)
t = threading.Thread(target=handle_client(conn, addr))

# Block H (DISTRACTOR)
handle_client(conn, addr)
```

### Hints

- What's the difference between `target=func` and `target=func()`?
- Should the main thread wait for the handler to finish?
- How do you pass arguments to the thread's target function?

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block E
import threading

# Block B
def handle_client(conn, addr):
    data = conn.recv(1024)
    conn.send(data.upper())
    conn.close()

# Block F
conn, addr = sock.accept()

# Block D
t = threading.Thread(target=handle_client, args=(conn, addr))

# Block A
t.start()
```

**Distractors explained:**
- **Block C** (`join`) — Would block the main thread, defeating concurrency
- **Block G** — Wrong syntax: `target=handle_client(conn, addr)` CALLS the function immediately!
- **Block H** — Direct call without thread = iterative server, not concurrent

**Critical distinction:**
- `target=handle_client` — Pass the function object (correct!)
- `target=handle_client()` — Call function NOW, pass its return value (wrong!)

</details>

---

## Problem P4: Socket with Timeout and Error Handling

### Task

Create a TCP client that connects with a timeout and handles connection errors.

### Scrambled Blocks

```python
# Block A
except socket.timeout:
    print("Connection timed out")

# Block B
sock.settimeout(5.0)

# Block C
sock.connect(("192.168.1.100", 9090))

# Block D
try:

# Block E (DISTRACTOR)
sock.setblocking(True)

# Block F
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Block G
except ConnectionRefusedError:
    print("Server not running")

# Block H
import socket

# Block I (DISTRACTOR)
sock.settimeout(0)  # Non-blocking
```

### Hints

- Where should `try:` be placed relative to operations that might fail?
- What's the difference between timeout and non-blocking mode?
- Which operations can raise ConnectionRefusedError?

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block H
import socket

# Block F
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Block B
sock.settimeout(5.0)

# Block D
try:

# Block C
    sock.connect(("192.168.1.100", 9090))

# Block A
except socket.timeout:
    print("Connection timed out")

# Block G
except ConnectionRefusedError:
    print("Server not running")
```

**Distractors explained:**
- **Block E** (`setblocking(True)`) — Default behaviour; redundant
- **Block I** (`settimeout(0)`) — Makes socket non-blocking, not timed

**Note:** Indentation matters! Block C must be indented inside the try block.

</details>

---

## Problem P5: Complete UDP Echo Server

### Task

Create a UDP server that echoes back whatever it receives, with logging.

### Scrambled Blocks

```python
# Block A
data, addr = sock.recvfrom(1024)

# Block B
while True:

# Block C
sock.sendto(data, addr)

# Block D
sock.bind(("0.0.0.0", 9091))

# Block E (DISTRACTOR)
sock.listen(5)

# Block F
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Block G
print(f"Echo to {addr}: {data}")

# Block H
import socket

# Block I (DISTRACTOR)
conn, addr = sock.accept()
```

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block H
import socket

# Block F
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Block D
sock.bind(("0.0.0.0", 9091))

# Block B
while True:

# Block A
    data, addr = sock.recvfrom(1024)

# Block G
    print(f"Echo to {addr}: {data}")

# Block C
    sock.sendto(data, addr)
```

**Distractors explained:**
- **Block E** (`listen`) — TCP only; UDP doesn't listen
- **Block I** (`accept`) — TCP only; UDP doesn't accept connections

**UDP server pattern:** bind → loop(recvfrom → process → sendto)

</details>

---

## Difficulty Progression

| Problem | Difficulty | Concepts |
|---------|------------|----------|
| P1 | ⭐ Easy | TCP server basics |
| P2 | ⭐ Easy | UDP client basics |
| P3 | ⭐⭐ Medium | Threading, function references |
| P4 | ⭐⭐ Medium | Error handling, timeouts |
| P5 | ⭐⭐⭐ Hard | Complete server pattern |

---

## Common Mistakes to Avoid

1. **Calling function in Thread target:** `target=func()` vs `target=func`
2. **Using TCP methods for UDP:** `listen()`, `accept()` are TCP-only
3. **Using UDP methods for TCP:** `sendto()`, `recvfrom()` are typically UDP
4. **Wrong order:** Must bind before listen, listen before accept
5. **Forgetting imports:** Always need `import socket` (and `import threading` for threads)

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
