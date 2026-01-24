# ❌ Common Misconceptions — Week 1: Network Fundamentals
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> This document lists common misunderstandings and how to correct them.
> Use these to test your own understanding!

---

## Network Measurement

### 🚫 Misconception 1: "Ping measures bandwidth"

**WRONG:** "I pinged the server and got 12ms, so my connection speed is 12ms."

**CORRECT:** Ping measures **latency** (round-trip time), not **bandwidth** (data throughput).

| Metric | What it measures | Units | Analogy |
|--------|-----------------|-------|---------|
| Latency | Time for packet to travel | milliseconds (ms) | Length of a pipe |
| Bandwidth | Data volume per second | Mbps, Gbps | Width of a pipe |

**Practical verification:**
```bash
# This measures LATENCY (RTT)
ping -c 4 8.8.8.8

# This measures BANDWIDTH (requires iperf3 server)
# iperf3 -c speedtest.server.com
```

**Why this matters:** A satellite link can have high bandwidth (100 Mbps) but terrible latency (600ms). A local connection might have low bandwidth (10 Mbps) but excellent latency (1ms). Different applications care about different metrics — video calls hate latency; file downloads hate low bandwidth.

---

### 🚫 Misconception 2: "Traceroute shows the only path to a destination"

**WRONG:** "Traceroute showed 12 hops, so packets always take exactly this route."

**CORRECT:** Traceroute shows **one possible path at one moment in time**. Routing can change dynamically.

| Reality | Explanation |
|---------|-------------|
| Routes change | Load balancing, failures, policy changes |
| Asymmetric paths | Return path may differ from forward path |
| Hidden hops | Some routers don't respond to traceroute |
| Multiple paths | ECMP (Equal-Cost Multi-Path) exists |

**Practical verification:**
```bash
# Run multiple times and compare
traceroute google.com
sleep 60
traceroute google.com
# Paths may differ!
```

---

## Loopback and Localhost

### 🚫 Misconception 3: "localhost and 127.0.0.1 are different things"

**WRONG:** "I should use 127.0.0.1 because it's more direct than localhost."

**CORRECT:** `localhost` is a hostname that resolves to `127.0.0.1`. They refer to the **same loopback interface**.

**Practical verification:**
```bash
# Check hostname resolution
cat /etc/hosts | grep localhost
# Output: 127.0.0.1 localhost

# Both work identically
ping -c 1 localhost
ping -c 1 127.0.0.1

# DNS lookup
getent hosts localhost
```

**The only difference:** Using the IP directly skips DNS/hosts lookup (microseconds faster, rarely matters).

---

### 🚫 Misconception 4: "Loopback traffic goes through the network card"

**WRONG:** "When I ping localhost, packets go out my Ethernet port and back."

**CORRECT:** Loopback traffic **never leaves the machine**. The `lo` interface is entirely virtual.

```
┌─────────────────────────────────────────────────────────────┐
│                     Your Computer                           │
│                                                             │
│   ┌─────────┐      ┌─────────────────┐      ┌─────────┐   │
│   │ Process │ ───► │ Loopback (lo)   │ ───► │ Process │   │
│   │   A     │ ◄─── │ 127.0.0.0/8     │ ◄─── │   B     │   │
│   └─────────┘      └─────────────────┘      └─────────┘   │
│                           │                                 │
│                    Never leaves!                            │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐  │
│   │              Physical NIC (eth0)                     │  │
│   │              ─────────────────────                   │  │
│   │                      │                               │  │
│   └──────────────────────│───────────────────────────────┘  │
└──────────────────────────│──────────────────────────────────┘
                           │
                    To network ───►
```

**Practical verification:**
```bash
# Start capture on physical interface
tcpdump -i eth0 icmp &

# Ping localhost
ping -c 1 localhost

# No packets captured! Because loopback doesn't use eth0
```

---

## TCP/UDP

### 🚫 Misconception 5: "TCP guarantees instant delivery"

**WRONG:** "TCP is reliable, so my data arrives immediately."

**CORRECT:** TCP guarantees **eventual, ordered delivery**, not instant delivery.

| TCP Guarantees | TCP Does NOT Guarantee |
|----------------|----------------------|
| Data arrives eventually (or error reported) | Specific delivery time |
| Data arrives in order | Low latency |
| Data is not corrupted | Fast delivery |
| Duplicates are eliminated | Real-time behaviour |

**Why this matters:** TCP will retransmit lost packets, which adds delay. For real-time applications (VoIP, gaming), this delay is worse than losing a packet. That's why they use UDP.

**Practical verification:**
```bash
# Simulate packet loss and watch TCP retransmit
# (requires tc tool and root)
sudo tc qdisc add dev lo root netem loss 10%
# Now TCP connections will show retransmissions in Wireshark
```

---

### 🚫 Misconception 6: "UDP is unreliable, therefore useless"

**WRONG:** "Why would anyone use UDP? It loses packets!"

**CORRECT:** UDP is used when **speed matters more than guaranteed delivery**.

| Use Case | Why UDP? |
|----------|----------|
| DNS queries | One small request, one small response — faster to retry than maintain connection |
| Video streaming | Missing one frame is fine; waiting for retransmit causes stutter |
| Online gaming | Old position data is useless; want newest data ASAP |
| VoIP | Rather have a small glitch than a delayed conversation |

**Key insight:** The application can implement its own reliability on top of UDP if needed (e.g., QUIC protocol).

---

## Docker and Containers

### 🚫 Misconception 7: "Container localhost = Host localhost"

**WRONG:** "I can access my host's Portainer at localhost:9000 from inside a container."

**CORRECT:** Containers have **isolated network namespaces**. Their localhost is different from the host's localhost.

```
┌─────────────────────────────────────────────────────────────┐
│                         HOST                                 │
│  localhost:9000 ──► Portainer                               │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                    CONTAINER                            │ │
│  │  localhost:9000 ──► Nothing (container's own loopback) │ │
│  │                                                         │ │
│  │  To reach host: use host IP or special DNS names       │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Practical verification:**
```bash
# From WSL host - works
curl http://localhost:9000

# From inside container - fails
docker exec week1_lab curl http://localhost:9000
# Connection refused!

# Check different IPs
ip addr show  # on host
docker exec week1_lab ip addr show  # in container
# Different!
```

---

### 🚫 Misconception 8: "docker ps shows all containers"

**WRONG:** "I ran `docker ps` and my container isn't there, so it doesn't exist."

**CORRECT:** `docker ps` shows only **running** containers. Use `docker ps -a` for all containers.

| Command | Shows |
|---------|-------|
| `docker ps` | Running containers only |
| `docker ps -a` | All containers (running + stopped + exited) |
| `docker images` | Downloaded images (not containers) |

**Practical verification:**
```bash
# Create and stop a container
docker run --name test_container alpine echo "hello"

# Not visible!
docker ps

# Visible with -a
docker ps -a | grep test_container

# Clean up
docker rm test_container
```

---

## Commands and Tools

### 🚫 Misconception 9: "ss and netstat are identical"

**WRONG:** "I'll just use netstat; it's the same as ss."

**CORRECT:** `ss` is the modern replacement for `netstat`. It's faster and has better features.

| Aspect | netstat | ss |
|--------|---------|-----|
| Speed | Slower (reads /proc) | Faster (uses netlink) |
| Status | Legacy, deprecated | Current, maintained |
| Information | Less detailed | More detailed |
| Availability | Being removed from distros | Standard |

**Recommended:** Use `ss` for new work. Know `netstat` for legacy systems.

```bash
# Modern way
ss -tlnp

# Legacy way (may not be installed)
netstat -tlnp
```

---

### 🚫 Misconception 10: "Wireshark captures all network traffic"

**WRONG:** "I started Wireshark but I don't see the container traffic."

**CORRECT:** Wireshark captures traffic only on **interfaces it can access**.

| To capture... | Use interface... |
|---------------|-----------------|
| WSL/Docker traffic | vEthernet (WSL) |
| Host loopback | Loopback Adapter |
| Physical network | Ethernet/Wi-Fi |
| Inside container | tcpdump in container |

**Practical verification:**
```bash
# List available interfaces in Wireshark
# Or use tshark
tshark -D

# For Docker traffic, often need to capture inside container
docker exec week1_lab tcpdump -i any -w /work/pcap/capture.pcap
```

---

## Socket States

### 🚫 Misconception 11: "LISTEN means the server is communicating"

**WRONG:** "The socket is in LISTEN state, so it's transferring data."

**CORRECT:** LISTEN means the server is **waiting for connections**, not communicating.

```
Socket Lifecycle:
                                    
CLOSED ──► LISTEN ──► (client connects) ──► ESTABLISHED ──► ...
              │                                    │
              │                                    │
         Waiting for                          Actually
         connections                          communicating
```

**Practical verification:**
```bash
# Start server (enters LISTEN)
nc -l -p 9099 &

# Check state
ss -tln | grep 9099
# Shows: LISTEN

# Connect client
nc localhost 9099 &

# Check state again
ss -tn | grep 9099
# Shows: ESTAB (ESTABLISHED)
```

---

## Summary Table

| # | Misconception | Reality |
|---|--------------|---------|
| 1 | Ping measures bandwidth | Ping measures latency (RTT) |
| 2 | Traceroute shows the only path | Routes are dynamic and can change |
| 3 | localhost ≠ 127.0.0.1 | They're the same (hostname → IP) |
| 4 | Loopback uses network card | Loopback is purely virtual |
| 5 | TCP = instant delivery | TCP = eventual ordered delivery |
| 6 | UDP is useless | UDP is essential for real-time apps |
| 7 | Container localhost = host | Containers have isolated networking |
| 8 | docker ps shows all | docker ps shows only running |
| 9 | ss = netstat | ss is modern, faster replacement |
| 10 | Wireshark sees everything | Only captures accessible interfaces |
| 11 | LISTEN = communicating | LISTEN = waiting for connections |

---

## Test Yourself

For each statement, decide: **True or False?**

1. A 1ms ping time means I have 1Gbps bandwidth.
2. The loopback address 127.0.0.5 would also work for local testing.
3. TCP retransmits lost packets automatically.
4. I can use `docker ps -a` to see stopped containers.
5. From inside a container, `curl localhost:9000` reaches the host's port 9000.

<details>
<summary>Answers</summary>

1. **False** — Ping measures latency, not bandwidth
2. **True** — The entire 127.0.0.0/8 range is loopback
3. **True** — That's TCP's reliability mechanism
4. **True** — The `-a` flag shows all containers
5. **False** — Container's localhost is isolated from host

</details>

---

*NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim*
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
