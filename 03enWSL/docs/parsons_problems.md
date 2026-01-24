# Parsons Problems — Week 3

> NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim

## Instructions

Arrange scrambled code blocks into correct order. Watch for **DISTRACTOR** blocks!

---

## Problem 1: UDP Broadcast Sender ⭐⭐

**LO3** — Arrange blocks to create UDP broadcast sender.

### Blocks (scrambled)
```python
# A
message = "Hello!".encode('utf-8')

# B
sock.sendto(message, (BROADCAST_ADDR, PORT))

# C
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# D
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# E — DISTRACTOR
sock.connect((BROADCAST_ADDR, PORT))

# F
import socket
BROADCAST_ADDR = '255.255.255.255'
PORT = 5007

# G — DISTRACTOR
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```

<details><summary>Solution</summary>
**Order: F → C → D → A → B**

Distractors wrong: E (UDP uses sendto, not connect), G (SO_REUSEADDR for receivers)
</details>

---

## Problem 2: UDP Multicast Receiver ⭐⭐

**LO3** — Arrange blocks for multicast receiver joining 239.1.1.1.

### Blocks
```python
# A
data, addr = sock.recvfrom(1024)

# B
import socket, struct
MCAST_GROUP = '239.1.1.1'
PORT = 5008

# C
sock.bind(('', PORT))

# D
mreq = struct.pack('4sL', socket.inet_aton(MCAST_GROUP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# E
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# F — DISTRACTOR
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# G — DISTRACTOR
sock.bind((MCAST_GROUP, PORT))
```

<details><summary>Solution</summary>
**Order: B → E → C → D → A**

Distractors wrong: F (multicast doesn't use SO_BROADCAST), G (bind to '', not group)
</details>

---

## Problem 3: Multicast Sender with TTL ⭐⭐

**LO2, LO3** — Create multicast sender with TTL=32.

### Blocks
```python
# A
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)

# B
import socket
MCAST_GROUP = '239.1.1.1'
PORT = 5008
TTL = 32

# C
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# D
sock.sendto(b"Hello multicast", (MCAST_GROUP, PORT))

# E — DISTRACTOR
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# F — DISTRACTOR
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
```

<details><summary>Solution</summary>
**Order: B → C → A → D**

Distractors wrong: E (not needed for multicast), F (TTL=1 is link-local only)
</details>

---

## Problem 4: TCP Tunnel Handler ⭐⭐⭐

**LO4** — Arrange bidirectional tunnel handler.

### Blocks
```python
# A
def handle_connection(client_sock, target_host, target_port):

# B
    target_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_sock.connect((target_host, target_port))

# C
    t1 = threading.Thread(target=relay, args=(client_sock, target_sock))
    t2 = threading.Thread(target=relay, args=(target_sock, client_sock))

# D
    t1.start(); t2.start()
    t1.join(); t2.join()

# E
    client_sock.close(); target_sock.close()

# F — DISTRACTOR
    target_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# G — DISTRACTOR
    data = client_sock.recv(4096)
    target_sock.send(data)
```

<details><summary>Solution</summary>
**Order: A → B → C → D → E**

Distractors wrong: F (tunnel uses TCP not UDP), G (single-threaded blocks bidirectional)
</details>

---

## Problem 5: Relay Function ⭐⭐⭐

**LO4** — Create relay function for tunnel.

### Blocks
```python
# A
def relay(source, destination):

# B
    try:
        while True:
            data = source.recv(4096)

# C
            if not data:
                break

# D
            destination.sendall(data)

# E
    except (socket.error, BrokenPipeError):
        pass

# F
    finally:
        source.close(); destination.close()

# G — DISTRACTOR
            destination.send(data)

# H — DISTRACTOR
            if len(data) < 4096:
                break

# I — DISTRACTOR
    data = source.recv(4096)
```

<details><summary>Solution</summary>
**Order: A → B → C → D → E → F**

Distractors wrong:
- G: send() may not send all bytes (use sendall)
- H: short read doesn't mean end
- I: outside loop = reads once only
</details>

---

## Summary

| Problem | LO | Difficulty | Key Concept |
|---------|-----|------------|-------------|
| P1 | LO3 | ⭐⭐ | SO_BROADCAST |
| P2 | LO3 | ⭐⭐ | IP_ADD_MEMBERSHIP |
| P3 | LO2,3 | ⭐⭐ | TTL scope |
| P4 | LO4 | ⭐⭐⭐ | Threading for bidirectional |
| P5 | LO4 | ⭐⭐⭐ | sendall() vs send() |

---
*Week 3: Network Programming — Broadcast, Multicast and TCP Tunnelling*
