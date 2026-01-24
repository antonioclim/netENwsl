# 🧩 Parsons Problems — Week 3

> Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Reorder the code blocks to create a working solution. Some problems include distractor blocks that should not be used.

---

## Problem P1: UDP Broadcast Sender

### Task

Create a function that sends a UDP broadcast message to all hosts on the local network segment.

### Scrambled Blocks

```python
# Block A
    sock.sendto(message.encode(), (broadcast_addr, port))

# Block B
def send_broadcast(message: str, port: int, broadcast_addr: str = "255.255.255.255") -> bool:

# Block C
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Block D
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Block E
    return True

# Block F
    sock.close()

# Block G (DISTRACTOR - not needed)
    sock.bind(('', 0))

# Block H (DISTRACTOR - not needed)
    sock.connect((broadcast_addr, port))
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block B - Function definition
def send_broadcast(message: str, port: int, broadcast_addr: str = "255.255.255.255") -> bool:

# Block D - Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Block C - Enable broadcast permission
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Block A - Send the message
    sock.sendto(message.encode(), (broadcast_addr, port))

# Block F - Clean up
    sock.close()

# Block E - Return success
    return True
```

**Distractors explained:**
- **Block G (bind):** Not needed for sending — bind is for receivers or when you need a specific source port
- **Block H (connect):** UDP broadcast uses `sendto()`, not `connect()` + `send()`. Also, `connect()` would set a default destination, but broadcast requires explicit addressing

**Key insight:** `SO_BROADCAST` must be set BEFORE calling `sendto()` with a broadcast address, or the kernel will reject the operation.

</details>

---

## Problem P2: Multicast Group Join

### Task

Create a function that sets up a UDP socket to receive multicast traffic from a specific group.

### Scrambled Blocks

```python
# Block A
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Block B
def join_multicast_group(group_ip: str, port: int) -> socket.socket:

# Block C
    sock.bind(('', port))

# Block D
    mreq = socket.inet_aton(group_ip) + struct.pack('=I', socket.INADDR_ANY)

# Block E
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Block F
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Block G
    return sock

# Block H (DISTRACTOR - not needed)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Block I (DISTRACTOR - wrong order)
    sock.connect((group_ip, port))
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block B - Function definition
def join_multicast_group(group_ip: str, port: int) -> socket.socket:

# Block E - Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Block F - Allow address reuse (important for multiple receivers)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Block C - Bind to port
    sock.bind(('', port))

# Block D - Build membership request structure
    mreq = socket.inet_aton(group_ip) + struct.pack('=I', socket.INADDR_ANY)

# Block A - Join the multicast group
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Block G - Return configured socket
    return sock
```

**Distractors explained:**
- **Block H (SO_BROADCAST):** Multicast and broadcast are different mechanisms — SO_BROADCAST is not used for multicast
- **Block I (connect):** Multicast receivers should not `connect()` — they need to receive from any sender in the group

**Key insight:** The `mreq` structure is 8 bytes: 4 bytes for the group IP address and 4 bytes for the local interface (INADDR_ANY = all interfaces).

</details>

---

## Problem P3: TCP Tunnel Connection Setup

### Task

Create the connection setup portion of a TCP tunnel that listens for incoming connections and forwards them to a target server.

### Scrambled Blocks

```python
# Block A
    client_sock, client_addr = listen_sock.accept()

# Block B
def setup_tunnel_connection(listen_port: int, target_host: str, target_port: int):

# Block C
    listen_sock.listen(5)

# Block D
    target_sock = socket.create_connection((target_host, target_port))

# Block E
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Block F
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Block G
    listen_sock.bind(('', listen_port))

# Block H
    return client_sock, target_sock

# Block I (DISTRACTOR - wrong protocol)
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Block J (DISTRACTOR - wrong order)
    listen_sock.accept()
    listen_sock.bind(('', listen_port))
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block B - Function definition
def setup_tunnel_connection(listen_port: int, target_host: str, target_port: int):

# Block E - Create TCP listening socket
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Block F - Allow address reuse
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Block G - Bind to listen port
    listen_sock.bind(('', listen_port))

# Block C - Start listening for connections
    listen_sock.listen(5)

# Block A - Accept incoming client connection
    client_sock, client_addr = listen_sock.accept()

# Block D - Connect to target server
    target_sock = socket.create_connection((target_host, target_port))

# Block H - Return both sockets for relay
    return client_sock, target_sock
```

**Distractors explained:**
- **Block I (SOCK_DGRAM):** TCP tunnel requires TCP sockets (SOCK_STREAM), not UDP
- **Block J (wrong order):** You cannot `accept()` before `bind()` and `listen()` — the sequence is always: socket → bind → listen → accept

**Key insight:** The tunnel creates TWO connections: one from the client to the tunnel (via accept) and one from the tunnel to the server (via create_connection).

</details>

---

## Problem P4: Bidirectional Data Relay

### Task

Create a function that relays data bidirectionally between two sockets using threads.

### Scrambled Blocks

```python
# Block A
def relay(src: socket.socket, dst: socket.socket, name: str) -> None:

# Block B
    while True:

# Block C
        data = src.recv(4096)

# Block D
        if not data:
            break

# Block E
        dst.sendall(data)

# Block F
def start_bidirectional_relay(sock_a: socket.socket, sock_b: socket.socket) -> None:

# Block G
    t1 = threading.Thread(target=relay, args=(sock_a, sock_b, "A→B"))

# Block H
    t2 = threading.Thread(target=relay, args=(sock_b, sock_a, "B→A"))

# Block I
    t1.start()
    t2.start()

# Block J (DISTRACTOR - wrong function)
        dst.send(data)

# Block K (DISTRACTOR - unnecessary)
        time.sleep(0.001)
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block A - Relay function definition
def relay(src: socket.socket, dst: socket.socket, name: str) -> None:

# Block B - Main loop
    while True:

# Block C - Receive data
        data = src.recv(4096)

# Block D - Check for connection close
        if not data:
            break

# Block E - Forward all data
        dst.sendall(data)

# Block F - Bidirectional relay setup function
def start_bidirectional_relay(sock_a: socket.socket, sock_b: socket.socket) -> None:

# Block G - Create thread for A→B direction
    t1 = threading.Thread(target=relay, args=(sock_a, sock_b, "A→B"))

# Block H - Create thread for B→A direction
    t2 = threading.Thread(target=relay, args=(sock_b, sock_a, "B→A"))

# Block I - Start both threads
    t1.start()
    t2.start()
```

**Distractors explained:**
- **Block J (send vs sendall):** `send()` may not send all data in one call — `sendall()` guarantees complete transmission
- **Block K (sleep):** Unnecessary delay that reduces throughput — `recv()` already blocks when no data is available

**Key insight:** Two threads are essential because `recv()` is a blocking call. Without separate threads, data could only flow in one direction at a time.

</details>

---

## Self-Assessment

After completing these problems, you should be able to:

- [ ] Correctly sequence socket setup operations (socket → bind → listen → accept)
- [ ] Distinguish between broadcast and multicast socket options
- [ ] Understand why TCP tunnels require two separate connections
- [ ] Explain the role of threads in bidirectional data relay
- [ ] Choose `sendall()` over `send()` for reliable forwarding

---

*Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim*
