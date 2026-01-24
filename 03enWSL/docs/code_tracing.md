# Code Tracing Exercises — Week 3

> Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Trace through the code mentally before running it. Write down your predictions, then verify.

---

## Exercise T1: UDP Broadcast Socket Setup

### Code

```python
import socket

# Line 1
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Line 2
print(f"Broadcast allowed: {sock.getsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST)}")

# Line 3
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Line 4
print(f"Broadcast allowed: {sock.getsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST)}")

# Line 5
sock.sendto(b"Hello", ("255.255.255.255", 5007))

# Line 6
print("Message sent successfully")

# Line 7
sock.close()
```

### Questions

1. **Line 2 output:** What value will be printed for `Broadcast allowed`?
2. **Line 4 output:** What value will be printed after `setsockopt`?
3. **Line 5 behaviour:** Will this line succeed or raise an exception?
4. **State tracking:** Complete the table:

| After line | Socket type | SO_BROADCAST | Can send to 255.255.255.255? |
|------------|-------------|--------------|------------------------------|
| 1 | ? | ? | ? |
| 3 | ? | ? | ? |
| 7 | ? | ? | ? |

### Solution

<details>
<summary>Click to reveal</summary>

| After line | Socket type | SO_BROADCAST | Can send to 255.255.255.255? |
|------------|-------------|--------------|------------------------------|
| 1 | UDP (DGRAM) | 0 (disabled) | No |
| 3 | UDP (DGRAM) | 1 (enabled) | Yes |
| 7 | Closed | N/A | No (socket closed) |

**Output:**
```
Broadcast allowed: 0
Broadcast allowed: 1
Message sent successfully
```

**Explanation:** 
- By default, `SO_BROADCAST` is 0 (disabled)
- After `setsockopt`, it becomes 1 (enabled)
- Line 5 succeeds because broadcast is now permitted
- If Line 3 were removed, Line 5 would raise `OSError: [Errno 101] Network is unreachable`

</details>

---

## Exercise T2: Multicast Group Join Sequence

### Code

```python
import socket
import struct

# Line 1
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Line 2
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Line 3
sock.bind(('', 5008))

# Line 4
group_ip = "239.1.1.1"
mreq = socket.inet_aton(group_ip) + struct.pack('=I', socket.INADDR_ANY)

# Line 5
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Line 6
print(f"Joined multicast group {group_ip}")

# Line 7
sock.settimeout(5.0)

# Line 8
try:
    data, addr = sock.recvfrom(1024)
    print(f"Received: {data} from {addr}")
except socket.timeout:
    print("No data received within timeout")

# Line 9
sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
```

### Questions

1. **Line 4:** What is the size (in bytes) of `mreq`?
2. **Line 5:** What network protocol message is triggered by this line?
3. **Line 7-8:** If no multicast sender is active, what happens?
4. **Line 9:** What network protocol message is triggered?
5. **Order dependency:** What happens if Line 5 is moved before Line 3?

### Solution

<details>
<summary>Click to reveal</summary>

1. **Size of mreq:** 8 bytes (4 bytes for group IP + 4 bytes for interface IP/INADDR_ANY)

2. **Line 5 triggers:** IGMP Membership Report (v2: type 0x16, or v3: type 0x22)

3. **Timeout behaviour:** After 5 seconds of no data, `socket.timeout` is raised and "No data received within timeout" is printed

4. **Line 9 triggers:** IGMP Leave Group message (type 0x17 in IGMPv2)

5. **Order dependency:** It would still work! The multicast join does not require the socket to be bound first. However, binding first is conventional because:
   - It ensures the port is available
   - Some systems require binding before receiving

**State tracking:**

| After line | Bound? | In group 239.1.1.1? | Timeout set? |
|------------|--------|---------------------|--------------|
| 1 | No | No | None |
| 3 | Yes (:5008) | No | None |
| 5 | Yes | Yes | None |
| 7 | Yes | Yes | 5.0s |
| 9 | Yes | No (left) | 5.0s |

</details>

---

## Exercise T3: TCP Tunnel Data Flow

### Code (Simplified tunnel relay function)

```python
import socket
import threading

def relay(src, dst, name):
    """Relay data from src socket to dst socket."""
    count = 0
    while True:
        # Line A
        data = src.recv(4096)
        
        # Line B
        if not data:
            print(f"{name}: Source closed connection")
            break
        
        # Line C
        count += len(data)
        print(f"{name}: Relaying {len(data)} bytes")
        
        # Line D
        dst.sendall(data)
    
    # Line E
    print(f"{name}: Total relayed: {count} bytes")
    dst.shutdown(socket.SHUT_WR)

# Main tunnel code
client_sock, addr = tunnel_listen.accept()  # Line 1
server_sock = socket.create_connection(("server", 8080))  # Line 2

t1 = threading.Thread(target=relay, args=(client_sock, server_sock, "C→S"))  # Line 3
t2 = threading.Thread(target=relay, args=(server_sock, client_sock, "S→C"))  # Line 4

t1.start()  # Line 5
t2.start()  # Line 6
```

### Scenario

A client sends "Hello" (5 bytes) through the tunnel and the server echoes it back.

### Questions

1. **Line 1-2:** How many TCP connections exist after both lines execute?
2. **Threading:** Why are two threads needed (t1 and t2)?
3. **Data flow:** Trace the path of "Hello" through the relay functions.
4. **Line B:** Why check `if not data`? What does empty data mean?
5. **Line D:** Why use `sendall()` instead of `send()`?

### Solution

<details>
<summary>Click to reveal</summary>

1. **Connections after Line 2:** 2 TCP connections
   - Connection 1: Client ↔ Tunnel (from `accept()`)
   - Connection 2: Tunnel ↔ Server (from `create_connection()`)

2. **Why two threads:** TCP is bidirectional. Data can flow:
   - Client → Server (t1 handles this)
   - Server → Client (t2 handles this)
   
   Both directions must work simultaneously. A single thread would block on `recv()` and could not handle the other direction.

3. **Data flow trace for "Hello":**
   ```
   Client sends "Hello" → client_sock receives in t1
   t1: Line A reads "Hello" (5 bytes)
   t1: Line C prints "C→S: Relaying 5 bytes"
   t1: Line D sends "Hello" to server_sock → Server receives
   
   Server echoes "Hello" → server_sock receives in t2
   t2: Line A reads "Hello" (5 bytes)
   t2: Line C prints "S→C: Relaying 5 bytes"
   t2: Line D sends "Hello" to client_sock → Client receives
   ```

4. **Empty data check:** In TCP, `recv()` returning empty bytes (`b''`) indicates:
   - The remote side has closed its send direction (sent FIN)
   - No more data will arrive on this socket
   - This is the graceful close signal

5. **sendall() vs send():**
   - `send()` may send fewer bytes than requested (returns actual count)
   - `sendall()` guarantees all bytes are sent (loops internally)
   - For relay correctness, we must forward ALL received data

**Connection state timeline:**

| Event | Connection 1 (C↔T) | Connection 2 (T↔S) |
|-------|--------------------|--------------------|
| After Line 1 | ESTABLISHED | - |
| After Line 2 | ESTABLISHED | ESTABLISHED |
| Client closes | FIN received | Still open |
| t1 exits | Half-closed | SHUT_WR sent |
| Server closes | Still open | FIN received |
| t2 exits | SHUT_WR sent | Half-closed |

</details>

---

## Exercise T4: Broadcast vs Multicast Reception

### Code

```python
import socket
import struct

def setup_broadcast_receiver(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))
    return sock

def setup_multicast_receiver(group, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))
    mreq = socket.inet_aton(group) + struct.pack('=I', socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    return sock

# Scenario: Two receivers on the same host
bcast_recv = setup_broadcast_receiver(5007)      # Receiver A
mcast_recv = setup_multicast_receiver("239.1.1.1", 5008)  # Receiver B

# Sender sends:
# 1. Broadcast to 255.255.255.255:5007
# 2. Multicast to 239.1.1.1:5008
# 3. Broadcast to 255.255.255.255:5008
# 4. Multicast to 239.1.1.1:5007
```

### Questions

For each sent message, will Receiver A and Receiver B receive it?

| Message | Receiver A (bcast:5007) | Receiver B (mcast:5008) |
|---------|-------------------------|-------------------------|
| 1. Broadcast to :5007 | ? | ? |
| 2. Multicast to :5008 | ? | ? |
| 3. Broadcast to :5008 | ? | ? |
| 4. Multicast to :5007 | ? | ? |

### Solution

<details>
<summary>Click to reveal</summary>

| Message | Receiver A (bcast:5007) | Receiver B (mcast:5008) |
|---------|-------------------------|-------------------------|
| 1. Broadcast to :5007 | ✅ Yes (correct port) | ❌ No (wrong port) |
| 2. Multicast to :5008 | ❌ No (wrong port) | ✅ Yes (joined group + correct port) |
| 3. Broadcast to :5008 | ❌ No (wrong port) | ✅ Yes* (port matches) |
| 4. Multicast to :5007 | ❌ No (not in group) | ❌ No (wrong port) |

**Key insight for message 3:** Receiver B WILL receive the broadcast even though it is set up for multicast! Why?
- Broadcast goes to ALL hosts on port 5008
- Receiver B is bound to port 5008
- The multicast group membership does not filter out broadcast

**Key insight for message 4:** Receiver A will NOT receive multicast to port 5007 because:
- Multicast requires explicit group membership (IP_ADD_MEMBERSHIP)
- Simply binding to a port is not sufficient for multicast

</details>

---

## Self-Assessment Checklist

After completing these exercises, you should be able to:

- [ ] Predict the effect of SO_BROADCAST on send operations
- [ ] Understand IGMP message triggers (join/leave)
- [ ] Trace data through a TCP tunnel with two threads
- [ ] Distinguish broadcast and multicast reception requirements
- [ ] Explain why sendall() is preferred over send() for relays

---

*Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim*
