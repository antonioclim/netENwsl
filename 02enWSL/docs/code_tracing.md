# 🔍 Code Tracing Exercises — Week 2: Socket Programming

> NETWORKING class — ASE, CSIE Bucharest  
> Computer Networks Laboratory | by ing. dr. Antonio Clim

Code tracing builds deep understanding by forcing you to simulate program execution mentally. Complete these exercises without running the code.

---

## Instructions

For each exercise:
1. Read the code carefully
2. Trace execution step by step
3. Write your predicted output
4. **Only then** run the code to check

---

## Trace T1: TCP Server Socket Creation

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"Type: {sock.type}")
print(f"Family: {sock.family}")

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("127.0.0.1", 9090))
sock.listen(5)

print(f"Listening: {sock.getsockname()}")
```

### Your prediction:
```
Type: _______________
Family: _______________
Listening: _______________
```

<details>
<summary>Click to reveal answer</summary>

```
Type: SocketKind.SOCK_STREAM
Family: AddressFamily.AF_INET
Listening: ('127.0.0.1', 9090)
```

**Key insight:** `sock.type` returns the socket type constant, `getsockname()` returns the bound address.
</details>

---

## Trace T2: TCP vs UDP Packet Count

Consider these two scenarios running simultaneously (with Wireshark capturing):

**Scenario A: TCP**
```python
# Server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("0.0.0.0", 9090))
sock.listen(1)
conn, addr = sock.accept()
data = conn.recv(1024)
conn.send(b"OK")
conn.close()
sock.close()

# Client
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 9090))
sock.send(b"Hello")
sock.recv(1024)
sock.close()
```

**Scenario B: UDP**
```python
# Server
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 9091))
data, addr = sock.recvfrom(1024)
sock.sendto(b"OK", addr)
sock.close()

# Client
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b"Hello", ("127.0.0.1", 9091))
sock.recvfrom(1024)
sock.close()
```

### Your prediction:

| Scenario | Minimum packets in Wireshark |
|----------|------------------------------|
| A (TCP)  | ___ packets                  |
| B (UDP)  | ___ packets                  |

<details>
<summary>Click to reveal answer</summary>

| Scenario | Minimum packets |
|----------|-----------------|
| A (TCP)  | **10 packets** (SYN, SYN-ACK, ACK, DATA, ACK, DATA, ACK, FIN, ACK, FIN-ACK) |
| B (UDP)  | **2 packets** (DATA, DATA) |

**Key insight:** TCP's reliability comes at the cost of overhead. UDP has zero connection setup.
</details>

---

## Trace T3: TCP Three-Way Handshake Sequence

Trace what happens at each step when a client connects:

```python
# Server is already running on 127.0.0.1:9090

# Client code:
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Step 1
sock.settimeout(5.0)                                       # Step 2
sock.connect(("127.0.0.1", 9090))                         # Step 3
```

### Your prediction:

| Step | Client State | Server State | Packets Sent |
|------|--------------|--------------|--------------|
| 1    | ___          | LISTEN       | ___          |
| 2    | ___          | LISTEN       | ___          |
| 3a   | ___          | ___          | ___          |
| 3b   | ___          | ___          | ___          |
| 3c   | ___          | ___          | ___          |

<details>
<summary>Click to reveal answer</summary>

| Step | Client State | Server State | Packets Sent |
|------|--------------|--------------|--------------|
| 1    | CLOSED       | LISTEN       | None         |
| 2    | CLOSED       | LISTEN       | None         |
| 3a   | SYN_SENT     | LISTEN       | Client→Server: SYN |
| 3b   | SYN_SENT     | SYN_RCVD     | Server→Client: SYN-ACK |
| 3c   | ESTABLISHED  | ESTABLISHED  | Client→Server: ACK |

**Key insight:** `connect()` blocks until the three-way handshake completes.
</details>

---

## Trace T4: Message Boundary Problem

```python
import socket
import time

# Server
def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", 9090))
    sock.listen(1)
    conn, _ = sock.accept()
    
    conn.send(b"Hello")
    conn.send(b"World")
    time.sleep(0.1)
    conn.close()

# Client
def client():
    time.sleep(0.05)  # Wait for server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 9090))
    
    data = sock.recv(1024)
    print(f"Received: {data!r}")
    sock.close()
```

### Your prediction:

What will the client print?

- [ ] A: `Received: b'Hello'`
- [ ] B: `Received: b'World'`
- [ ] C: `Received: b'HelloWorld'`
- [ ] D: Could be A, B or C depending on timing

<details>
<summary>Click to reveal answer</summary>

**D: Could be A, B or C depending on timing**

Most likely **C** (`HelloWorld`) because both sends happen quickly before the recv().

**Key insight:** TCP is a byte stream. Two consecutive `send()` calls may be received as one chunk, or split differently. Never assume message boundaries!
</details>

---

## Trace T5: Threaded Server Execution Order

```python
import socket
import threading
import time

results = []

def handle(conn, client_id):
    time.sleep(0.1)  # Simulate work
    results.append(client_id)
    conn.close()

# Server accepts 3 connections, spawns threads
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("127.0.0.1", 9090))
sock.listen(5)

for i in range(3):
    conn, _ = sock.accept()
    t = threading.Thread(target=handle, args=(conn, i))
    t.start()

time.sleep(0.5)
print(f"Results: {results}")
```

If 3 clients connect simultaneously at t=0, what is printed?

### Your prediction:
```
Results: _______________
```

<details>
<summary>Click to reveal answer</summary>

```
Results: [0, 1, 2]
```

Or possibly `[1, 0, 2]`, `[2, 1, 0]`, etc. — **any permutation of [0, 1, 2]**

**Key insight:** Thread execution order is non-deterministic. All three threads run in parallel, each taking ~100ms. They complete at roughly the same time, so the order depends on scheduling.
</details>

---

## Common Tracing Errors

| Error | Why It Happens |
|-------|----------------|
| Assuming TCP message boundaries | TCP is a stream, not messages |
| Forgetting `accept()` creates new socket | `conn` is different from `sock` |
| Thinking `bind()` sends packets | `bind()` is local only |
| Assuming thread order | Threads are non-deterministic |
| Forgetting timeout affects `recv()` | `recv()` blocks by default |

---

## Self-Assessment

After completing all traces:

| Trace | Correct? | Concept Verified |
|-------|----------|------------------|
| T1    | ☐ Yes ☐ No | Socket creation |
| T2    | ☐ Yes ☐ No | TCP vs UDP overhead |
| T3    | ☐ Yes ☐ No | Three-way handshake |
| T4    | ☐ Yes ☐ No | Stream boundaries |
| T5    | ☐ Yes ☐ No | Thread concurrency |

**Goal:** 4/5 or better before proceeding to exercises.

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
