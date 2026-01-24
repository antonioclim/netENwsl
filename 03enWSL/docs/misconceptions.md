# Common Misconceptions — Week 3

> Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

This document lists common misunderstandings about UDP broadcast, multicast and TCP tunnelling, along with corrections and practical verifications.

---

## Broadcast Misconceptions

### 🚫 Misconception 1: "Broadcast reaches the entire network/internet"

**WRONG:** "If I send to 255.255.255.255, all computers everywhere will receive my message."

**CORRECT:** The limited broadcast address (255.255.255.255) is **never forwarded by routers**. It stays within the local Layer 2 broadcast domain (typically a single subnet or VLAN).

| Aspect | Wrong assumption | Reality |
|--------|------------------|---------|
| Scope | Entire network | Single L2 domain only |
| Router behaviour | Forwards broadcast | Drops/blocks broadcast |
| Internet reach | Can reach any IP | Cannot leave local segment |

**Why this matters:** Accidentally broadcasting sensitive data is less catastrophic than you might fear — but relying on broadcast for cross-subnet communication will silently fail.

**Practical verification:**
```bash
# On week3_client (172.20.0.100)
docker exec week3_client tcpdump -i eth0 udp port 5007 &

# Send broadcast
docker exec week3_client python3 -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.sendto(b'test', ('255.255.255.255', 5007))
"

# The packet is visible locally but would NOT appear on a different subnet
```

---

### 🚫 Misconception 2: "SO_BROADCAST is optional or just a performance hint"

**WRONG:** "I can send to broadcast addresses without setting any socket options — options are just optimisations."

**CORRECT:** The kernel **requires** `SO_BROADCAST` to be set before allowing sends to broadcast addresses. This is a deliberate safety mechanism, not a hint.

| Aspect | Wrong assumption | Reality |
|--------|------------------|---------|
| Without SO_BROADCAST | Works but slower | Raises exception |
| Purpose | Performance tuning | Explicit permission |
| Error type | Warning only | Hard error (OSError) |

**Practical verification:**
```bash
# This will FAIL with PermissionError or OSError
docker exec week3_client python3 -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# NOT setting SO_BROADCAST
s.sendto(b'test', ('255.255.255.255', 5007))
"
# Error: [Errno 101] Network is unreachable (or similar)
```

---

### 🚫 Misconception 3: "Directed broadcast (e.g., 172.20.0.255) always works"

**WRONG:** "I can use subnet.255 to broadcast to any subnet, even remote ones."

**CORRECT:** Most modern routers **disable directed broadcast forwarding by default** (since the Smurf attack in the 1990s). Directed broadcasts to remote subnets are typically blocked.

**Practical verification:**
```bash
# Check your router/firewall configuration
# On most systems, directed broadcast forwarding is OFF:
sysctl net.ipv4.icmp_echo_ignore_broadcasts
# Returns: 1 (ignore broadcasts)
```

---

## Multicast Misconceptions

### 🚫 Misconception 4: "Multicast is just broadcast with a different address range"

**WRONG:** "Multicast and broadcast work the same way — just use 239.x.x.x instead of 255.255.255.255."

**CORRECT:** Multicast requires **explicit group membership** via IGMP. Hosts must actively join a multicast group to receive traffic; simply binding to a port is insufficient.

| Aspect | Broadcast | Multicast |
|--------|-----------|-----------|
| Receiver action needed | Just bind to port | Must join group (IGMP) |
| Who receives | All hosts in L2 domain | Only group members |
| Efficiency | All NICs process frame | Only member NICs process |
| Router traversal | Never | Yes, with multicast routing |

**Practical verification:**
```bash
# Container WITHOUT proper multicast join will NOT receive messages
docker exec week3_receiver python3 -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 5008))
s.settimeout(3)
try:
    data = s.recvfrom(1024)
    print('Received:', data)
except socket.timeout:
    print('Timeout - no multicast received (as expected without JOIN)')
"
```

---

### 🚫 Misconception 5: "TTL means Time To Live in seconds"

**WRONG:** "Setting TTL=60 means the packet lives for 60 seconds before expiring."

**CORRECT:** In IP, TTL counts **router hops**, not seconds. Each router decrements TTL by 1. When TTL reaches 0, the packet is discarded. For multicast, TTL controls the **scope** (how far the packet can travel).

| TTL Value | Actual meaning | Scope |
|-----------|----------------|-------|
| 1 | Link-local only | Same subnet, no routers |
| 2 | Can cross 1 router | Adjacent subnets |
| 32 | Can cross 31 routers | Site-wide |
| 255 | Maximum hops | Unrestricted |

**Practical verification:**
```bash
# Send multicast with TTL=1 — will NOT cross routers
docker exec week3_server python3 -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
print('TTL set to 1 - packet stays link-local')
"
```

---

### 🚫 Misconception 6: "Multicast groups are created automatically"

**WRONG:** "When I send to 239.1.1.1, that multicast group is automatically created."

**CORRECT:** Multicast group addresses are **predefined ranges** (224.0.0.0–239.255.255.255). You do not create groups — you join existing address spaces. The group "exists" when at least one host has joined it.

| Range | Usage | Notes |
|-------|-------|-------|
| 224.0.0.0/24 | Link-local, well-known | Reserved (OSPF, VRRP, etc.) |
| 224.0.1.0–224.0.1.255 | Internetwork control | Globally scoped |
| 232.0.0.0/8 | Source-Specific Multicast | SSM range |
| 239.0.0.0/8 | Administratively scoped | Private use (like 10.x.x.x) |

**Practical verification:**
```bash
# View multicast group memberships on an interface
docker exec week3_client ip maddr show dev eth0
# After joining 239.1.1.1, you will see it listed
```

---

## TCP Tunnel Misconceptions

### 🚫 Misconception 7: "A TCP tunnel is transparent — it extends my connection to the server"

**WRONG:** "When I connect through a tunnel, I have a direct TCP connection to the server."

**CORRECT:** A TCP tunnel **terminates** your connection and creates a **new, separate connection** to the target server. The tunnel acts as an intermediary (proxy), not a transparent pipe.

| Aspect | Wrong assumption | Reality |
|--------|------------------|---------|
| Connections | 1 (client→server) | 2 (client→tunnel, tunnel→server) |
| TCP state | End-to-end | Two separate state machines |
| Acknowledgements | Direct from server | From tunnel only |
| Latency | Same as direct | Added processing delay |

**Why this matters:**
- TCP reliability is NOT end-to-end through a tunnel
- The server sees the tunnel's IP, not yours
- If the tunnel crashes, both connections are lost

**Practical verification:**
```bash
# Check connections on the router (tunnel host)
docker exec week3_router ss -tn
# You will see TWO ESTABLISHED connections for each tunnel session

# One connection: client ↔ router:9090
# Another connection: router ↔ server:8080
```

---

### 🚫 Misconception 8: "UDP tunnels have the same behaviour as TCP tunnels"

**WRONG:** "Tunnels work the same way regardless of protocol."

**CORRECT:** UDP tunnels are fundamentally different because UDP is connectionless. A UDP tunnel:
- Does not have "connections" to terminate
- Cannot guarantee delivery or ordering
- May have different latency characteristics
- Is often used for different purposes (VPNs, game servers)

---

## Quick Reference: Testing Your Understanding

| Misconception | Test yourself |
|---------------|---------------|
| Broadcast scope | Can you explain why 255.255.255.255 does not reach the internet? |
| SO_BROADCAST | What error do you get without it? |
| Multicast vs broadcast | What is IGMP and why is it needed? |
| TTL meaning | What does TTL=1 prevent? |
| Tunnel connections | How many TCP handshakes for one tunnel session? |

---

## Further Reading

- [docs/theory_summary.md](theory_summary.md) — Theoretical foundations
- [docs/peer_instruction.md](peer_instruction.md) — Test your knowledge with MCQs
- [docs/troubleshooting.md](troubleshooting.md) — When things go wrong

---

*Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim*
