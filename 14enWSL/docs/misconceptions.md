# ❌ Common Misconceptions — Week 14

> NETWORKING class — ASE, CSIE | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

This document lists common misunderstandings students have about networking concepts covered in this course. Each misconception includes the wrong belief, the correct understanding and a practical way to verify.

---

## TCP/IP and OSI Layers

### 🚫 Misconception 1: "IP and MAC addresses do the same thing"

**WRONG:** "Both IP and MAC are just addresses, so they work the same way."

**CORRECT:** IP addresses and MAC addresses serve fundamentally different purposes at different layers.

| Aspect | IP Address (Layer 3) | MAC Address (Layer 2) |
|--------|---------------------|----------------------|
| Scope | Global, routable across networks | Local, within a single network segment |
| Assignment | Configured (static or DHCP) | Burned into hardware (or virtualised) |
| Format | 32 bits (IPv4) or 128 bits (IPv6) | 48 bits |
| Example | 192.168.1.100 | 02:42:ac:14:00:02 |
| Changes | Can change when moving networks | Stays with the device |

**Why this matters:** Routers use IP addresses to forward packets between networks. Switches use MAC addresses to forward frames within a network.

**Practical verification:**

```bash
# See both addresses for a container
docker exec client ip addr show eth0

# See the ARP cache (IP → MAC mappings)
docker exec client ip neigh show
```

---

### 🚫 Misconception 2: "TCP guarantees instant delivery"

**WRONG:** "Since TCP is reliable, my data arrives immediately."

**CORRECT:** TCP guarantees *eventual, ordered* delivery, not instant delivery. TCP provides:

- **Reliability:** Lost packets are retransmitted
- **Order:** Packets are reassembled in sequence
- **Flow control:** Sender adjusts speed to receiver capacity
- **Congestion control:** Sender adjusts speed to network capacity

TCP does NOT guarantee:

- Instant delivery
- Consistent latency
- Maximum delivery time

**Practical verification:**

```bash
# Observe TCP retransmissions under packet loss
# In Wireshark, filter: tcp.analysis.retransmission
```

---

### 🚫 Misconception 3: "The TCP handshake uses only two packets"

**WRONG:** "Client sends SYN, server sends ACK, done."

**CORRECT:** TCP connection establishment requires exactly three packets (three-way handshake):

```
Client                 Server
  |                      |
  |-- SYN (seq=x) ------>|     Packet 1
  |                      |
  |<-- SYN-ACK ---------|     Packet 2
  |    (seq=y, ack=x+1)  |
  |                      |
  |-- ACK (ack=y+1) ---->|     Packet 3
  |                      |
  [Connection established]
```

**Why three packets?** Both sides need to propose their initial sequence number and acknowledge the other side's sequence number.

**Practical verification:**

```bash
# Capture a TCP connection in Wireshark
# Filter: tcp.flags.syn == 1
# You'll see: SYN, SYN-ACK, then data
```

---

## Docker and Containers

### 🚫 Misconception 4: "Containers are virtual machines"

**WRONG:** "Docker containers are like lightweight VMs."

**CORRECT:** Containers and VMs are fundamentally different:

| Aspect | Container | Virtual Machine |
|--------|-----------|-----------------|
| Kernel | Shares host kernel | Has own kernel |
| Boot time | Milliseconds | Minutes |
| Size | Megabytes | Gigabytes |
| Isolation | Process-level (namespaces) | Hardware-level (hypervisor) |
| Overhead | Minimal | Significant |

**Practical verification:**

```bash
# Show that containers share the host kernel
docker exec client uname -r
# Compare with WSL kernel
uname -r
# They're the same!
```

---

### 🚫 Misconception 5: "Port 80 inside equals port 80 outside"

**WRONG:** "If my container runs on port 80, I access it at port 80."

**CORRECT:** Port mapping explicitly translates between host and container ports. The syntax `-p HOST:CONTAINER` or `ports: "8080:80"` means:

- **Host port 8080** (what you type in browser)
- **Container port 80** (what the service listens on)

**Memory aid:** "Left is outside (host), right is inside (container)"

**Practical verification:**

```bash
# Show what port the container THINKS it's listening on
docker exec lb netstat -tlnp | grep nginx
# Shows: 0.0.0.0:80 (container port)

# But we access it from:
curl http://localhost:8080
# Host port 8080 is mapped to container port 80
```

---

### 🚫 Misconception 6: "All containers can talk to each other"

**WRONG:** "If two containers are running, they can communicate."

**CORRECT:** Docker networks provide isolation. Containers can only communicate if:

1. They are on the same Docker network, OR
2. A container is connected to multiple networks and routes between them, OR
3. Ports are published to the host

**Practical verification:**

```bash
# Client cannot ping backend directly
docker exec client ping -c 1 172.20.0.2
# Result: Network unreachable

# Client can reach LB (same network)
docker exec client ping -c 1 172.21.0.10
# Result: Success
```

---

### 🚫 Misconception 7: "Stopping a container deletes everything"

**WRONG:** "When I stop a container, all data inside is lost."

**CORRECT:** Stopping ≠ removing. Container states:

| Action | Container | Data in container filesystem | Data in volumes |
|--------|-----------|------------------------------|-----------------|
| Stop | Preserved | Preserved | Preserved |
| Start | Resumes | Still there | Still there |
| Remove | Deleted | Deleted | **Preserved** |

**Practical verification:**

```bash
# Create a file in container
docker exec client touch /tmp/testfile

# Stop container
docker stop client

# Start container
docker start client

# File is still there!
docker exec client ls /tmp/testfile
```

---

## Load Balancing

### 🚫 Misconception 8: "Round-robin is random"

**WRONG:** "Round-robin randomly picks a backend for each request."

**CORRECT:** Round-robin is deterministic and sequential. With N backends, requests go to backends in order: 1, 2, 3, ..., N, 1, 2, 3, ..., N, repeatedly.

**Practical verification:**

```bash
# Send 6 requests, observe alternating pattern
for i in 1 2 3 4 5 6; do
    curl -s http://localhost:8080/ | grep -o "app[12]"
done
# Output: app1 app2 app1 app2 app1 app2
```

---

### 🚫 Misconception 9: "Load balancer makes everything faster"

**WRONG:** "Adding a load balancer automatically improves performance."

**CORRECT:** A load balancer adds a network hop and processing overhead. It improves performance only when:

1. Backend servers are the bottleneck
2. Requests can be distributed (stateless or with session handling)
3. The load balancer itself is not the bottleneck

**Practical verification:**

```bash
# Measure latency with and without load balancer
# Direct to backend:
time curl -s http://localhost:8001/ > /dev/null

# Through load balancer:
time curl -s http://localhost:8080/ > /dev/null
# LB adds a few milliseconds
```

---

## HTTP and Web

### 🚫 Misconception 10: "HTTPS means the server is trustworthy"

**WRONG:** "If a website has HTTPS (🔒), it's safe and legitimate."

**CORRECT:** HTTPS provides:

- ✅ **Encryption** — traffic cannot be read in transit
- ✅ **Integrity** — traffic cannot be modified in transit
- ✅ **Authentication** — server has a valid certificate

HTTPS does NOT provide:

- ❌ Server content is truthful
- ❌ Server is not malicious
- ❌ Server won't steal your data

---

### 🚫 Misconception 11: "HTTP status 200 means everything worked"

**WRONG:** "If I get a 200 OK, the request was successful and correct."

**CORRECT:** HTTP 200 means the server processed the request and returned a response. It does NOT mean:

- The response contains what you expected
- The application logic succeeded
- No errors occurred in the backend

Many APIs return 200 with an error in the body:

```json
{
    "status": "error",
    "message": "User not found"
}
```

---

## Wireshark and Packet Analysis

### 🚫 Misconception 12: "Wireshark captures all network traffic"

**WRONG:** "When I run Wireshark, I see everything on the network."

**CORRECT:** Wireshark only captures traffic on interfaces it can access:

| Interface | What you see |
|-----------|-------------|
| Your Ethernet/Wi-Fi | Only traffic to/from your machine |
| vEthernet (WSL) | WSL2/Docker traffic |
| Loopback | localhost traffic only |

**For Docker traffic:** You must select the correct interface (usually `vEthernet (WSL)`) or run tcpdump inside the container.

---

## Summary Table

| # | Misconception | Reality |
|---|---------------|---------|
| 1 | IP = MAC | Different layers, different purposes |
| 2 | TCP = instant | TCP = eventual, ordered delivery |
| 3 | Handshake = 2 packets | Handshake = 3 packets |
| 4 | Container = VM | Containers share kernel |
| 5 | Port 80 = port 80 | Port mapping translates |
| 6 | All containers talk | Networks isolate |
| 7 | Stop = delete | Stop preserves, remove deletes |
| 8 | Round-robin = random | Round-robin = sequential |
| 9 | LB = faster | LB adds overhead, helps with scaling |
| 10 | HTTPS = safe | HTTPS = encrypted, not trustworthy |
| 11 | 200 = success | 200 = server responded |
| 12 | Wireshark sees all | Only selected interface |

---

*Document version: 2.0 | Week 14: Integrated Recap | January 2025*
