# Peer Instruction Questions — Week 3

> Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Peer Instruction Protocol (5 steps)

Each question follows **5 mandatory steps**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 1 (1 min)  │  Read the question and think individually               │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 2 (30 sec) │  Vote your answer (A/B/C/D) — no discussion!            │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 3 (2 min)  │  Discuss with your neighbour — convince them!           │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 4 (30 sec) │  Re-vote — you may change your answer                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 5 (2 min)  │  Instructor explains the correct answer                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Question 1: Broadcast Address Scope

> 💭 **PREDICTION:** Before reading the scenario, think: Can a broadcast message sent to 255.255.255.255 reach a computer on a different subnet?

### Scenario

A student runs this code on container `week3_client` (172.20.0.100/24):

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.sendto(b"Hello!", ("255.255.255.255", 5007))
```

The network has two subnets: 172.20.0.0/24 and 172.21.0.0/24, connected by a router.

### Question

Which hosts will receive this broadcast message?

### Options

- **A)** All hosts on both subnets (172.20.0.0/24 and 172.21.0.0/24)
- **B)** Only hosts on 172.20.0.0/24 (same subnet as sender)
- **C)** Only the router connecting the two subnets
- **D)** No hosts — 255.255.255.255 is invalid for sending

### Correct Answer

**B** — Only hosts on 172.20.0.0/24 receive the message.

### Targeted Misconception

**"Broadcast reaches the entire internet/network"** — Students often assume broadcast works like multicast or that routers forward broadcast traffic. The address 255.255.255.255 is a "limited broadcast" that is never forwarded by routers; it stays within the Layer 2 broadcast domain.

### Instructor Notes

- **Target accuracy:** 40-50% on first vote
- **Key concept:** Limited broadcast vs directed broadcast; L2 domain boundaries
- **After discussion:** Show `tcpdump` output on both subnets — packets only appear on 172.20.0.0/24
- **Follow-up:** Ask what address would reach 172.21.0.0/24 (answer: 172.21.0.255, if router allows directed broadcast)

---

## Question 2: SO_BROADCAST Requirement

> 💭 **PREDICTION:** What happens if you forget to set SO_BROADCAST before sending to a broadcast address?

### Scenario

A student writes this UDP sender:

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Note: SO_BROADCAST is NOT set
sock.sendto(b"Test", ("255.255.255.255", 5007))
```

### Question

What happens when this code runs?

### Options

- **A)** The message is sent successfully — SO_BROADCAST is optional
- **B)** The message is sent but arrives corrupted
- **C)** An OSError/PermissionError exception is raised
- **D)** The message is silently dropped by the kernel

### Correct Answer

**C** — An OSError (or PermissionError on some systems) is raised.

### Targeted Misconception

**"SO_BROADCAST is just a performance hint"** — Students think socket options are optional optimisations. The kernel deliberately blocks broadcast sends without explicit permission as a safety mechanism to prevent accidental network flooding.

### Instructor Notes

- **Target accuracy:** 50-60% on first vote
- **Key concept:** Socket options as mandatory permissions, not hints
- **After discussion:** Run both versions live — show the exact error message
- **Common error:** `OSError: [Errno 101] Network is unreachable` or `PermissionError`

---

## Question 3: Multicast Group Membership

> 💭 **PREDICTION:** If two containers are on the same network, will they both receive multicast traffic automatically?

### Scenario

Three containers exist on network 172.20.0.0/24:
- `server` sends to multicast group 239.1.1.1:5008
- `client` runs a receiver but does NOT call `IP_ADD_MEMBERSHIP`
- `receiver` runs a receiver and DOES call `IP_ADD_MEMBERSHIP` for 239.1.1.1

```python
# On 'client' — missing the join!
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 5008))
data = sock.recvfrom(1024)  # Waiting...

# On 'receiver' — proper join
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mreq = socket.inet_aton('239.1.1.1') + struct.pack('=I', socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
sock.bind(('', 5008))
data = sock.recvfrom(1024)  # Waiting...
```

### Question

When `server` sends a multicast message to 239.1.1.1:5008, which containers receive it?

### Options

- **A)** Both `client` and `receiver` — they are on the same port
- **B)** Only `receiver` — it joined the multicast group
- **C)** Only `client` — multicast works like broadcast
- **D)** Neither — multicast requires special router configuration

### Correct Answer

**B** — Only `receiver` gets the message because it explicitly joined the group.

### Targeted Misconception

**"Multicast is just broadcast with a different address"** — Students confuse the two. Multicast requires explicit group membership via IGMP; simply binding to a port is not sufficient. This is the key difference that makes multicast more efficient.

### Instructor Notes

- **Target accuracy:** 35-45% on first vote (commonly confused)
- **Key concept:** IGMP membership is mandatory for multicast reception
- **After discussion:** Run `ip maddr show` on both containers — only `receiver` shows the group
- **Demo:** Show IGMP Membership Report in Wireshark when join happens

---

## Question 4: Multicast TTL Meaning

> 💭 **PREDICTION:** What does TTL=1 mean for a multicast packet?

### Scenario

A multicast sender is configured with:

```python
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
sock.sendto(b"Data", ("239.1.1.1", 5008))
```

The network topology:
```
[Container A] ─── [Router 1] ─── [Router 2] ─── [Container B]
   (sender)                                        (receiver)
```

Container B has joined multicast group 239.1.1.1.

### Question

Will Container B receive the multicast message?

### Options

- **A)** Yes — TTL=1 means the packet lives for 1 second
- **B)** Yes — multicast always reaches all group members
- **C)** No — TTL=1 means the packet cannot cross any router
- **D)** No — TTL must be set to the exact hop count (2 in this case)

### Correct Answer

**C** — TTL=1 means the packet stays link-local and cannot traverse any router.

### Targeted Misconception

**"TTL means Time To Live in seconds"** — Students confuse TTL with actual time. In IP, TTL counts router hops, not seconds. Each router decrements TTL by 1; when it reaches 0, the packet is discarded. TTL=1 means "this subnet only."

### Instructor Notes

- **Target accuracy:** 40-55% on first vote
- **Key concept:** TTL = hop count, not time; multicast scope control
- **After discussion:** Show that setting TTL=3 would allow crossing 2 routers
- **Practical note:** In Docker bridge networks, TTL=1 is usually sufficient since containers share a virtual switch

---

## Question 5: TCP Tunnel Connection Count

> 💭 **PREDICTION:** When a client connects through a TCP tunnel to a server, how many TCP connections exist?

### Scenario

The Week 3 lab topology:
```
[Client] ──TCP:9090──► [Router/Tunnel] ──TCP:8080──► [Server]
```

A student runs:
```bash
docker exec week3_client bash -c "echo 'Hello' | nc router 9090"
```

The tunnel on `router` listens on port 9090 and forwards to `server:8080`.

### Question

How many TCP connections are established to deliver this single message?

### Options

- **A)** 1 connection — from client to server (tunnel is transparent)
- **B)** 2 connections — client↔router and router↔server
- **C)** 3 connections — client↔router, router internal, router↔server
- **D)** 0 connections — tunnels use UDP for efficiency

### Correct Answer

**B** — Two separate TCP connections are established.

### Targeted Misconception

**"A tunnel is transparent/invisible"** — Students think the tunnel magically extends the client's connection to the server. In reality, the tunnel terminates the client's TCP connection and creates a new one to the server, acting as an intermediary (proxy pattern).

### Instructor Notes

- **Target accuracy:** 45-55% on first vote
- **Key concept:** TCP tunnels break end-to-end TCP semantics; proxy pattern
- **After discussion:** Show `ss -tn` on router — two ESTABLISHED connections visible
- **Wireshark demo:** Filter `tcp.port == 9090 or tcp.port == 8080` and show two separate TCP handshakes

---

## Summary: Key Misconceptions Targeted

| Question | Misconception | Correct Understanding |
|----------|---------------|----------------------|
| Q1 | Broadcast reaches everywhere | Limited broadcast stays in L2 domain |
| Q2 | SO_BROADCAST is optional | Kernel requires explicit permission |
| Q3 | Multicast = broadcast | Multicast requires IGMP group join |
| Q4 | TTL = time in seconds | TTL = router hop count |
| Q5 | Tunnels are transparent | Tunnels create two separate connections |

---

*Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim*
