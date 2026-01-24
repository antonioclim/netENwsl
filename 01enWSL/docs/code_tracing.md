# 🔍 Code Tracing Exercises — Week 1
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Trace through the code mentally before running it.
> This builds your ability to predict programme behaviour — key for debugging!

---

## Exercise T1: Socket Connection States

### Code

```python
import socket

def check_port(host: str, port: int) -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((host, port))
    sock.close()
    
    if result == 0:
        return "OPEN"
    else:
        return "CLOSED"

# Main execution
status = check_port("127.0.0.1", 9090)
print(f"Port 9090 is {status}")
```

### Questions

1. **Line by line:** What type of socket is created on line 4?
2. **Return value:** If no server is listening on port 9090, what will `connect_ex()` return?
3. **Output prediction:** Assuming no server is running on port 9090, what will be printed?

### State Tracking

Complete the table (assume no server on port 9090):

| After line | `sock` state | `result` | `status` |
|------------|--------------|----------|----------|
| 4 | ? | undefined | undefined |
| 5 | ? | undefined | undefined |
| 6 | ? | ? | undefined |
| 7 | ? | ? | undefined |
| 10 | N/A | N/A | ? |

### Solution

<details>
<summary>Click to reveal</summary>

| After line | `sock` state | `result` | `status` |
|------------|--------------|----------|----------|
| 4 | Created (unconnected) | undefined | undefined |
| 5 | Timeout set to 2s | undefined | undefined |
| 6 | Connection failed | 111 (ECONNREFUSED) | undefined |
| 7 | Closed | 111 | undefined |
| 10 | N/A | N/A | "CLOSED" |

**Output:**
```
Port 9090 is CLOSED
```

**Explanation:** 
- `socket.AF_INET` = IPv4
- `socket.SOCK_STREAM` = TCP
- `connect_ex()` returns 0 on success, error code otherwise
- Error 111 is `ECONNREFUSED` — no server listening

</details>

---

## Exercise T2: Ping Result Parsing

### Code

```python
import re

def parse_ping_output(output: str) -> dict:
    result = {"transmitted": 0, "received": 0, "loss": 100.0}
    
    # Pattern: "4 packets transmitted, 3 received"
    match = re.search(r"(\d+) packets transmitted, (\d+) received", output)
    
    if match:
        result["transmitted"] = int(match.group(1))
        result["received"] = int(match.group(2))
        if result["transmitted"] > 0:
            result["loss"] = 100 * (1 - result["received"] / result["transmitted"])
    
    return result

# Test input
ping_output = """
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=12.3 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=117 time=11.8 ms

--- 8.8.8.8 ping statistics ---
4 packets transmitted, 2 received, 50% packet loss, time 3004ms
"""

stats = parse_ping_output(ping_output)
print(f"Sent: {stats['transmitted']}, Got: {stats['received']}, Loss: {stats['loss']}%")
```

### Questions

1. **Regex analysis:** What does `(\d+)` capture in the pattern?
2. **Match groups:** What are `match.group(1)` and `match.group(2)`?
3. **Calculation:** Walk through the loss calculation step by step.
4. **Output prediction:** What will be printed?

### State Tracking

| After line | `result["transmitted"]` | `result["received"]` | `result["loss"]` |
|------------|------------------------|---------------------|-----------------|
| 4 | ? | ? | ? |
| 10 | ? | ? | ? |
| 11 | ? | ? | ? |
| 13 | ? | ? | ? |

### Solution

<details>
<summary>Click to reveal</summary>

| After line | `result["transmitted"]` | `result["received"]` | `result["loss"]` |
|------------|------------------------|---------------------|-----------------|
| 4 | 0 | 0 | 100.0 |
| 10 | 4 | 0 | 100.0 |
| 11 | 4 | 2 | 100.0 |
| 13 | 4 | 2 | 50.0 |

**Calculation breakdown:**
```
loss = 100 * (1 - received / transmitted)
loss = 100 * (1 - 2 / 4)
loss = 100 * (1 - 0.5)
loss = 100 * 0.5
loss = 50.0
```

**Output:**
```
Sent: 4, Got: 2, Loss: 50.0%
```

**Key insights:**
- `\d+` matches one or more digits
- Parentheses `()` create capture groups
- `group(1)` = first captured value, `group(2)` = second
- Integer division is avoided by using float result (Python 3)

</details>

---

## Exercise T3: TCP Server Threading

### Code

```python
import threading
import time

messages = []
lock = threading.Lock()

def handle_client(client_id: int):
    time.sleep(0.1 * client_id)  # Simulate varying processing time
    with lock:
        messages.append(f"Client {client_id} processed")

# Create and start threads
threads = []
for i in [3, 1, 2]:
    t = threading.Thread(target=handle_client, args=(i,))
    threads.append(t)
    t.start()

# Wait for all threads
for t in threads:
    t.join()

print(messages)
```

### Questions

1. **Thread creation:** How many threads are created?
2. **Sleep times:** What is the sleep duration for each client ID?
3. **Order prediction:** In what order will messages be appended to the list?
4. **Final output:** What will `messages` contain?

### Timing Analysis

| Client ID | Sleep time | Expected completion order |
|-----------|------------|--------------------------|
| 3 | ? | ? |
| 1 | ? | ? |
| 2 | ? | ? |

### Solution

<details>
<summary>Click to reveal</summary>

| Client ID | Sleep time | Expected completion order |
|-----------|------------|--------------------------|
| 3 | 0.3s | 3rd |
| 1 | 0.1s | 1st |
| 2 | 0.2s | 2nd |

**Output:**
```
['Client 1 processed', 'Client 2 processed', 'Client 3 processed']
```

**Explanation:**
- All three threads start nearly simultaneously
- Client 1 sleeps shortest (0.1s), finishes first
- Client 2 sleeps medium (0.2s), finishes second
- Client 3 sleeps longest (0.3s), finishes last
- The lock ensures only one thread modifies `messages` at a time
- Order is determined by completion time, not start order

**Key insight:** Thread start order ≠ completion order. The loop order [3, 1, 2] doesn't determine the output order.

</details>

---

## Exercise T4: Network Byte Order

### Code

```python
import struct

def pack_header(msg_type: int, length: int, seq_num: int) -> bytes:
    # Format: ! = network byte order (big-endian)
    #         B = unsigned char (1 byte)
    #         H = unsigned short (2 bytes)
    #         I = unsigned int (4 bytes)
    return struct.pack("!BHI", msg_type, length, seq_num)

def unpack_header(data: bytes) -> tuple:
    return struct.unpack("!BHI", data)

# Pack a header
header = pack_header(1, 256, 1000)
print(f"Packed bytes: {header.hex()}")
print(f"Length: {len(header)} bytes")

# Unpack it
msg_type, length, seq_num = unpack_header(header)
print(f"Type: {msg_type}, Length: {length}, Seq: {seq_num}")
```

### Questions

1. **Size calculation:** How many bytes will `pack_header` return? (B=1, H=2, I=4)
2. **Byte representation:** What is 256 in big-endian 2-byte hex?
3. **Byte representation:** What is 1000 in big-endian 4-byte hex?
4. **Full output:** Predict all three print statements.

### Byte Analysis

| Value | Size | Big-endian hex |
|-------|------|----------------|
| 1 (msg_type) | 1 byte | ? |
| 256 (length) | 2 bytes | ? |
| 1000 (seq_num) | 4 bytes | ? |

### Solution

<details>
<summary>Click to reveal</summary>

| Value | Size | Big-endian hex |
|-------|------|----------------|
| 1 (msg_type) | 1 byte | `01` |
| 256 (length) | 2 bytes | `0100` |
| 1000 (seq_num) | 4 bytes | `000003e8` |

**Calculations:**
- 256 = 0x0100 (1×256 + 0×1)
- 1000 = 0x000003E8 (3×256 + 14×16 + 8 = 768 + 224 + 8 = 1000)

**Output:**
```
Packed bytes: 010100000003e8
Length: 7 bytes
Type: 1, Length: 256, Seq: 1000
```

**Key insight:** Network byte order (big-endian) puts the most significant byte first. This is the standard for network protocols to ensure machines with different native byte orders can communicate.

</details>

---

## Exercise T5: Connection Timeout Handling

### Code

```python
import socket
import time

def connect_with_retry(host: str, port: int, max_retries: int = 3) -> bool:
    attempt = 0
    
    while attempt < max_retries:
        attempt += 1
        print(f"Attempt {attempt}/{max_retries}...")
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((host, port))
            sock.close()
            return True
        except socket.timeout:
            print(f"  Timeout on attempt {attempt}")
        except ConnectionRefusedError:
            print(f"  Connection refused on attempt {attempt}")
        
        if attempt < max_retries:
            time.sleep(0.5)
    
    return False

# Test against non-existent server
result = connect_with_retry("127.0.0.1", 9999, max_retries=2)
print(f"Connection successful: {result}")
```

### Questions

1. **Loop iterations:** How many times will the while loop execute?
2. **Exception type:** Which exception will be raised (timeout or refused)?
3. **Sleep count:** How many times will `time.sleep(0.5)` execute?
4. **Full output:** Trace all print statements.

### Execution Trace

| Iteration | `attempt` | Exception | Sleeps after? |
|-----------|----------|-----------|---------------|
| 1 | ? | ? | ? |
| 2 | ? | ? | ? |

### Solution

<details>
<summary>Click to reveal</summary>

| Iteration | `attempt` | Exception | Sleeps after? |
|-----------|----------|-----------|---------------|
| 1 | 1 | ConnectionRefusedError | Yes (attempt < max_retries) |
| 2 | 2 | ConnectionRefusedError | No (attempt == max_retries) |

**Output:**
```
Attempt 1/2...
  Connection refused on attempt 1
Attempt 2/2...
  Connection refused on attempt 2
Connection successful: False
```

**Explanation:**
- No server on port 9999, so connection is refused immediately (not timeout)
- Timeout would occur if a firewall drops packets silently
- Connection refused means the OS actively rejects the connection
- Sleep only happens between retries, not after the last attempt

</details>

---

## Exercise T6: Socket Server Lifecycle

### Code

```python
import socket
import threading
import time

def run_server(host: str, port: int, ready_event: threading.Event):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(1)
    ready_event.set()
    
    conn, addr = server.accept()
    data = conn.recv(1024)
    conn.sendall(b"ACK:" + data)
    conn.close()
    server.close()

# Main
ready = threading.Event()
t = threading.Thread(target=run_server, args=("127.0.0.1", 9999, ready))
t.start()
ready.wait()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9999))
client.sendall(b"Hello")
response = client.recv(1024)
client.close()

t.join()
print(f"Response: {response}")
```

### Questions

1. **Socket states:** What state is the server socket in after `listen()` but before `accept()`?
2. **Blocking calls:** Which line causes the server thread to wait?
3. **Data flow:** Trace the path of "Hello" through the code.
4. **Output prediction:** What will be printed at the end?

### State Timeline

Complete the timeline of socket states:

| Time | Server Socket | Client Socket | Event |
|------|--------------|---------------|-------|
| T1 | ? | doesn't exist | server.bind() |
| T2 | ? | doesn't exist | server.listen() |
| T3 | ? | doesn't exist | ready.wait() returns |
| T4 | LISTEN (blocked) | ? | client.connect() starts |
| T5 | ? | ? | accept() returns |
| T6 | closed | ? | after data exchange |

### Solution

<details>
<summary>Click to reveal</summary>

| Time | Server Socket | Client Socket | Event |
|------|--------------|---------------|-------|
| T1 | BOUND | doesn't exist | server.bind() |
| T2 | LISTEN | doesn't exist | server.listen() |
| T3 | LISTEN | doesn't exist | ready.wait() returns |
| T4 | LISTEN (blocked) | SYN_SENT→ESTABLISHED | client.connect() starts |
| T5 | ESTABLISHED (via conn) | ESTABLISHED | accept() returns |
| T6 | CLOSED | CLOSED | after data exchange |

**Output:**
```
Response: b'ACK:Hello'
```

**Key insights:**
1. After `listen()`, socket is in LISTEN state — waiting, not communicating
2. `accept()` is a blocking call — server waits here for client
3. `accept()` returns a NEW socket (`conn`) for the actual communication
4. The original server socket stays in LISTEN (could accept more connections)
5. `SO_REUSEADDR` allows immediate port reuse after close

**Data flow:**
```
client.sendall(b"Hello")
    │
    ▼
Network (TCP)
    │
    ▼
conn.recv(1024) → data = b"Hello"
    │
    ▼
conn.sendall(b"ACK:" + data) → b"ACK:Hello"
    │
    ▼
Network (TCP)
    │
    ▼
client.recv(1024) → response = b"ACK:Hello"
```

</details>

---

## Self-Assessment

After completing these exercises, you should be able to:

- [ ] Trace socket creation and connection attempts
- [ ] Predict regex match results and group captures
- [ ] Understand thread execution order vs creation order
- [ ] Convert between integers and network byte order
- [ ] Trace exception handling in retry loops
- [ ] Follow socket state transitions through server lifecycle

**Scoring:**
- 6/6 correct without hints: Excellent — ready for advanced exercises
- 4-5/6 correct: Good — review the ones you missed
- 2-3/6 correct: Need more practice — re-read theory and try again
- 0-1/6 correct: Start with the basic concepts first

---

*NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim*
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
