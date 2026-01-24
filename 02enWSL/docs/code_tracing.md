# 🔍 Code Tracing Exercises — Week 2: Sockets and Transport Protocols

> NETWORKING class — ASE, CSIE Bucharest  
> Computer Networks Laboratory | by ing. dr. Antonio Clim

Trace through the code mentally before running it. This builds your mental model of how sockets work.

---

## Exercise T1: TCP Client Connection Sequence

### Code

```python
import socket

def tcp_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"1. Socket created, fd={sock.fileno()}")
    
    sock.settimeout(5.0)
    print("2. Timeout set")
    
    sock.connect(("127.0.0.1", 9090))
    print("3. Connected")
    
    sock.send(b"Hello")
    print("4. Data sent")
    
    data = sock.recv(1024)
    print(f"5. Received: {data}")
    
    sock.close()
    print("6. Closed")

tcp_client()
```

### Questions

1. **Line by line:** After line 4, what is the state of the TCP connection?
2. **Output prediction:** If the server responds with `b"OK: HELLO"`, what prints at step 5?
3. **Network trace:** What TCP packets are exchanged between steps 2 and 3?
4. **Error scenario:** What happens at line 7 if no server is running?

### State Tracking Table

Complete this table (assuming server is running and responds with `b"OK: HELLO"`):

| After line | `sock` state | TCP connection state | Network activity |
|------------|--------------|----------------------|------------------|
| 4 | ? | ? | ? |
| 7 | ? | ? | ? |
| 10 | ? | ? | ? |
| 13 | ? | ? | ? |
| 16 | ? | ? | ? |

### Solution

<details>
<summary>Click to reveal</summary>

| After line | `sock` state | TCP connection state | Network activity |
|------------|--------------|----------------------|------------------|
| 4 | Created, unconnected | CLOSED | None |
| 7 | Timeout configured | CLOSED | None |
| 10 | Connected | ESTABLISHED | SYN → SYN-ACK → ACK |
| 13 | Data sent | ESTABLISHED | DATA → ACK |
| 16 | Data received | ESTABLISHED | (already received) |
| 19 | Closed | TIME_WAIT | FIN → ACK → FIN → ACK |

**Output:**
```
1. Socket created, fd=3
2. Timeout set
3. Connected
4. Data sent
5. Received: b'OK: HELLO'
6. Closed
```

**Error scenario:** If no server is running, line 7 raises `ConnectionRefusedError` because the SYN packet receives RST in response.

</details>

---

## Exercise T2: UDP Server Receive Loop

### Code

```python
import socket

def udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 9091))
    print("Server ready")
    
    count = 0
    while count < 3:
        data, addr = sock.recvfrom(1024)
        count += 1
        print(f"#{count}: {data} from {addr[0]}:{addr[1]}")
        sock.sendto(b"ACK", addr)
    
    sock.close()
    print(f"Done after {count} messages")

udp_server()
```

### Questions

1. **Blocking behaviour:** What happens at line 10 if no client sends data?
2. **Address tracking:** If client A (port 50001) and client B (port 50002) both send "Hi", what do we know about `addr` each time?
3. **Loop termination:** How many datagrams does this server process before exiting?
4. **No connect needed:** Why is there no `accept()` or `connect()` call?

### State Tracking Table

Assume these events occur:
- t=0: Server starts
- t=1: Client 192.168.1.10:50001 sends `b"First"`
- t=2: Client 192.168.1.20:50002 sends `b"Second"`
- t=3: Client 192.168.1.10:50001 sends `b"Third"`

| After event | `count` | `data` | `addr` | Output |
|-------------|---------|--------|--------|--------|
| Server starts | ? | ? | ? | ? |
| First message | ? | ? | ? | ? |
| Second message | ? | ? | ? | ? |
| Third message | ? | ? | ? | ? |

### Solution

<details>
<summary>Click to reveal</summary>

| After event | `count` | `data` | `addr` | Output |
|-------------|---------|--------|--------|--------|
| Server starts | 0 | N/A | N/A | "Server ready" |
| First message | 1 | b"First" | ("192.168.1.10", 50001) | "#1: b'First' from 192.168.1.10:50001" |
| Second message | 2 | b"Second" | ("192.168.1.20", 50002) | "#2: b'Second' from 192.168.1.20:50002" |
| Third message | 3 | b"Third" | ("192.168.1.10", 50001) | "#3: b'Third' from 192.168.1.10:50001" |

**Final output:**
```
Server ready
#1: b'First' from 192.168.1.10:50001
#2: b'Second' from 192.168.1.20:50002
#3: b'Third' from 192.168.1.10:50001
Done after 3 messages
```

**Answers:**
1. The server blocks indefinitely at `recvfrom()` waiting for data
2. `addr` contains the sender's IP and ephemeral port — different for each client
3. Exactly 3 datagrams (while count < 3)
4. UDP is connectionless — no connection to establish or accept

</details>

---

## Exercise T3: Threaded Server Accept Pattern

### Code

```python
import socket
import threading

def handle_client(conn, addr, client_id):
    print(f"[{client_id}] Handler started for {addr}")
    data = conn.recv(1024)
    print(f"[{client_id}] Received: {data}")
    conn.send(b"OK")
    conn.close()
    print(f"[{client_id}] Handler finished")

def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", 9090))
    sock.listen(5)
    print("Server listening")
    
    client_id = 0
    while client_id < 2:
        conn, addr = sock.accept()
        client_id += 1
        print(f"[Main] Accepted #{client_id}")
        t = threading.Thread(target=handle_client, args=(conn, addr, client_id))
        t.start()
        print(f"[Main] Thread started for #{client_id}")
    
    print("[Main] Done accepting")
    sock.close()

server()
```

### Questions

1. **Concurrency:** If two clients connect at t=0, can their handlers run simultaneously?
2. **Socket ownership:** After `accept()`, who owns the `conn` socket — main thread or handler thread?
3. **Output ordering:** Is the output order deterministic or could it vary between runs?
4. **Race condition:** What happens if main thread closes `sock` while a handler is still running?

### Execution Trace

Assume:
- t=0: Client A connects, sends `b"AAA"` immediately
- t=0: Client B connects, sends `b"BBB"` immediately
- Handlers take 100ms to process

Mark the **possible** output orderings:

| Output sequence | Possible? | Why? |
|-----------------|-----------|------|
| All [Main] first, then all handlers | ? | ? |
| [Main] and handlers interleaved | ? | ? |
| [1] finished before [2] started | ? | ? |
| [2] finished before [1] finished | ? | ? |

### Solution

<details>
<summary>Click to reveal</summary>

| Output sequence | Possible? | Why? |
|-----------------|-----------|------|
| All [Main] first, then all handlers | Yes | Main loop could complete before handlers run |
| [Main] and handlers interleaved | Yes | Threads run concurrently; OS schedules |
| [1] finished before [2] started | Yes | If thread 1 runs to completion first |
| [2] finished before [1] finished | Yes | Threads are independent; scheduling varies |

**One possible output:**
```
Server listening
[Main] Accepted #1
[Main] Thread started for #1
[Main] Accepted #2
[1] Handler started for ('127.0.0.1', 50001)
[Main] Thread started for #2
[2] Handler started for ('127.0.0.1', 50002)
[Main] Done accepting
[1] Received: b'AAA'
[2] Received: b'BBB'
[1] Handler finished
[2] Handler finished
```

**Answers:**
1. Yes — that's the point of threading; handlers run in parallel
2. The handler thread; main passes `conn` as argument and doesn't use it again
3. Non-deterministic — thread scheduling is up to the OS
4. No problem — `sock` is the listening socket; `conn` sockets are independent

</details>

---

## Exercise T4: Socket Options Effect

### Code

```python
import socket
import time

def test_reuse():
    # First server
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.bind(("0.0.0.0", 9999))
    s1.listen(1)
    print("Server 1 listening")
    s1.close()
    print("Server 1 closed")
    
    # Immediate rebind attempt
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s2.bind(("0.0.0.0", 9999))
        print("Server 2 bound successfully")
    except OSError as e:
        print(f"Server 2 bind failed: {e}")
    
    # With SO_REUSEADDR
    s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s3.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s3.bind(("0.0.0.0", 9999))
        print("Server 3 bound successfully")
    except OSError as e:
        print(f"Server 3 bind failed: {e}")

test_reuse()
```

### Questions

1. **Without SO_REUSEADDR:** Why might s2.bind() fail?
2. **TIME_WAIT state:** How long does a socket typically stay in TIME_WAIT?
3. **With SO_REUSEADDR:** Why does s3.bind() succeed?
4. **Production impact:** Why is SO_REUSEADDR important for server development?

### Solution

<details>
<summary>Click to reveal</summary>

**Likely output:**
```
Server 1 listening
Server 1 closed
Server 2 bind failed: [Errno 98] Address already in use
Server 3 bound successfully
```

**Answers:**
1. After close(), the socket enters TIME_WAIT state (typically 60 seconds) to handle delayed packets. The OS prevents rebinding during this period.
2. 2×MSL (Maximum Segment Lifetime), typically 60 seconds on Linux.
3. SO_REUSEADDR tells the OS "I know there's a TIME_WAIT socket; let me bind anyway."
4. During development, you frequently restart servers. Without SO_REUSEADDR, you'd wait 60 seconds between restarts or change ports.

</details>

---

## Self-Assessment Checklist

After completing these exercises, verify you can:

- [ ] Trace TCP connection establishment (SYN-SYN/ACK-ACK)
- [ ] Identify when blocking calls will wait
- [ ] Predict thread interleaving possibilities
- [ ] Explain why SO_REUSEADDR is necessary
- [ ] Distinguish socket states (CLOSED, ESTABLISHED, TIME_WAIT)

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
