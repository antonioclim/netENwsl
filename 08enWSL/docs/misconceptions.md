# ❌ Common Misconceptions — Week 8
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> This document lists common misunderstandings and how to correct them.
> Review these BEFORE starting the exercises to avoid common pitfalls.

---

## TCP/Transport Layer Misconceptions

### 🚫 Misconception 1: "TCP guarantees instant delivery"

**WRONG:** "If I send data with TCP, it arrives immediately."

**CORRECT:** TCP guarantees **eventual, ordered delivery** — not instant delivery. Data may be:
- Buffered before sending (Nagle's algorithm)
- Delayed by network congestion
- Retransmitted if packets are lost

| Aspect | Wrong assumption | Reality |
|--------|------------------|---------|
| Timing | Instant arrival | Eventual arrival (may take seconds) |
| Ordering | First-sent = first-arrived | Network may reorder; TCP fixes this |
| Retransmission | Automatic and invisible | May cause noticeable delays |

**Practical verification:**
```bash
# Send data and observe timing with tcpdump
# Notice retransmission delays on lossy networks
tcpdump -i lo port 8080 -n
```

---

### 🚫 Misconception 2: "UDP is unreliable therefore useless"

**WRONG:** "UDP is just broken TCP. Nobody should use it."

**CORRECT:** UDP is **intentionally simple** for specific use cases where TCP's guarantees would hurt performance:

| Use Case | Why UDP is better |
|----------|-------------------|
| Video streaming | Dropped frames are acceptable; latency is not |
| Online gaming | Old position data is useless; need current state |
| DNS queries | Single request-response; handshake overhead wasteful |
| VoIP | Late audio is worse than dropped audio |

**Why this matters:** Understanding when to choose UDP vs TCP is a key networking skill.

---

### 🚫 Misconception 3: "The third ACK in TCP handshake is optional"

**WRONG:** "SYN and SYN-ACK are enough to establish a connection."

**CORRECT:** The third ACK is **essential** because:
- It confirms the client received the server's SYN-ACK
- Without it, the server cannot confirm bidirectional communication
- The server's SYN-ACK could have been lost

```
Client                  Server
   │                       │
   │──── SYN ─────────────▶│  Client: "Can you hear me?"
   │                       │
   │◀──── SYN-ACK ─────────│  Server: "Yes, can you hear me?"
   │                       │
   │──── ACK ─────────────▶│  Client: "Yes!" ← WITHOUT THIS, SERVER DOESN'T KNOW!
   │                       │
```

---

## HTTP Misconceptions

### 🚫 Misconception 4: "HTTP/1.1 sends one request per connection"

**WRONG:** "Each HTTP request needs a new TCP connection."

**CORRECT:** HTTP/1.1 uses **persistent connections** (keep-alive) by default:
- Multiple requests can use the same TCP connection
- Connection stays open between requests
- Saves TCP handshake overhead (3 × RTT per connection)

| HTTP Version | Default Behaviour |
|--------------|-------------------|
| HTTP/1.0 | Close after each request |
| HTTP/1.1 | Keep-alive (persistent) |
| HTTP/2 | Multiplexed streams on single connection |

**Practical verification:**
```bash
# Watch Wireshark — multiple HTTP exchanges on same TCP stream
curl -v http://localhost:8080/
# Note "Connection: keep-alive" in response
```

---

### 🚫 Misconception 5: "HEAD returns the headers OF the HEAD method"

**WRONG:** "HEAD returns metadata about what HEAD would return."

**CORRECT:** HEAD returns **the exact same headers that GET would return**, but with no body:
- Same Content-Type
- Same Content-Length (length of body that WOULD be sent)
- Same Last-Modified
- Same everything, minus the actual body

**Why it exists:** Check if a resource has changed without downloading it (caching, validation).

**Practical verification:**
```bash
# Compare GET and HEAD responses
curl -I http://localhost:8080/index.html  # HEAD
curl -i http://localhost:8080/index.html  # GET with headers
# Note: Content-Length is the same in both!
```

---

### 🚫 Misconception 6: "403 and 404 mean the same thing for security"

**WRONG:** "Return 404 for forbidden paths to hide that they exist."

**CORRECT:** 403 and 404 have **different security implications**:

| Status | Meaning | Reveals |
|--------|---------|---------|
| 403 Forbidden | "It exists but you can't access it" | Path exists |
| 404 Not Found | "It doesn't exist" | Path doesn't exist |

**Security consideration:** Some argue 404 is "more secure" because it doesn't reveal path existence. However:
- Consistent 404 for everything makes debugging hard
- Attackers can often distinguish 403/404 by timing
- Proper authentication/authorisation is better than obscurity

**Best practice:** Use 403 for authorisation failures, 404 for genuinely missing resources.

---

## Reverse Proxy Misconceptions

### 🚫 Misconception 7: "Reverse proxy and forward proxy are the same"

**WRONG:** "A proxy is a proxy — they all work the same way."

**CORRECT:** They serve **opposite purposes**:

| Aspect | Forward Proxy | Reverse Proxy |
|--------|---------------|---------------|
| Configured by | Client | Server |
| Hides | Client identity | Server identity |
| Client knows? | Yes (explicit config) | No (transparent) |
| Use case | Privacy, filtering | Load balancing, security |

```
Forward Proxy:  Client → [Proxy] → Internet
                Client configures proxy

Reverse Proxy:  Internet → [Proxy] → Backend Servers
                Server deploys proxy, client unaware
```

---

### 🚫 Misconception 8: "Round-robin means equal load"

**WRONG:** "Round-robin distributes load perfectly evenly."

**CORRECT:** Round-robin distributes **requests evenly**, not **load evenly**:

| Scenario | Round-robin result | Actual load |
|----------|-------------------|-------------|
| All requests take 10ms | Equal | Equal |
| Request 1 takes 1s, rest take 10ms | Equal requests | Backend 1 overloaded |
| Backend 3 is slower | Equal requests | Backend 3 falls behind |

**Better alternatives:**
- **Least connections:** Route to server with fewest active connections
- **Weighted round-robin:** Account for server capacity differences
- **Adaptive:** Monitor response times, adjust routing

---

### 🚫 Misconception 9: "X-Forwarded-For contains only one IP"

**WRONG:** "X-Forwarded-For: 192.168.1.100 — always a single IP."

**CORRECT:** X-Forwarded-For can contain **a chain of IPs** when multiple proxies are involved:

```
X-Forwarded-For: client, proxy1, proxy2
X-Forwarded-For: 192.168.1.100, 10.0.0.50, 172.16.0.10
```

**Reading order:** Leftmost = original client, rightmost = most recent proxy.

**Security warning:** Clients can spoof X-Forwarded-For! Only trust the rightmost IP that YOUR proxy added.

---

## Port and Socket Misconceptions

### 🚫 Misconception 10: "Port 80 inside container = port 80 outside"

**WRONG:** "If nginx listens on port 80, I access it on port 80."

**CORRECT:** Docker **port mapping** translates between host and container ports:

```yaml
# docker-compose.yml
ports:
  - "8080:80"  # host:container
```

| Container perspective | Host perspective |
|----------------------|------------------|
| nginx listens on 80 | Access via 8080 |
| Backend listens on 8080 | May not be exposed at all |

**Practical verification:**
```bash
# Inside container
docker exec nginx netstat -tlnp  # Shows port 80

# From host
curl http://localhost:8080  # Uses mapped port
curl http://localhost:80    # FAILS (not mapped)
```

---

### 🚫 Misconception 11: "localhost inside container = host localhost"

**WRONG:** "curl http://localhost:8080 from container reaches host."

**CORRECT:** Each container has its **own network namespace**:

| Context | `localhost` refers to |
|---------|----------------------|
| Host machine | Host's loopback (127.0.0.1) |
| Inside container | Container's loopback |
| Container → Host | Need `host.docker.internal` or host IP |

**Practical verification:**
```bash
# From host
curl http://localhost:8080  # Works (reaches nginx)

# From inside container
docker exec nginx curl http://localhost:8080  # FAILS (no service in container on 8080)
docker exec nginx curl http://backend1:8080   # Works (container DNS)
```

---

## Keep-Alive and Connection Misconceptions

### 🚫 Misconception 12: "Keep-alive means connection never closes"

**WRONG:** "With Connection: keep-alive, the TCP connection stays open forever."

**CORRECT:** Keep-alive connections have **timeouts and limits**:

| Parameter | Typical value | Effect |
|-----------|---------------|--------|
| keepalive_timeout | 65 seconds | Close after N seconds idle |
| keepalive_requests | 100 | Close after N requests |
| Client timeout | Browser-dependent | Client may close first |

**nginx default:**
```nginx
keepalive_timeout 65;
keepalive_requests 100;
```

**Practical verification:**
```bash
# Open connection, wait, try again
curl -v http://localhost:8080/
sleep 70
curl -v http://localhost:8080/
# Second request establishes NEW connection (timeout exceeded)
```

---

## Summary Table

| # | Misconception | Reality |
|---|--------------|---------|
| 1 | TCP = instant delivery | TCP = eventual, ordered delivery |
| 2 | UDP is useless | UDP is ideal for real-time applications |
| 3 | Third ACK is optional | Third ACK confirms bidirectional communication |
| 4 | HTTP/1.1 = one request per connection | HTTP/1.1 = persistent connections by default |
| 5 | HEAD returns HEAD metadata | HEAD returns GET headers without body |
| 6 | 403 = 404 for security | 403 and 404 have different meanings |
| 7 | Forward proxy = reverse proxy | They hide different endpoints |
| 8 | Round-robin = equal load | Round-robin = equal requests |
| 9 | X-Forwarded-For = one IP | X-Forwarded-For = chain of IPs |
| 10 | Container port = host port | Port mapping translates ports |
| 11 | Container localhost = host | Each container has own localhost |
| 12 | Keep-alive = forever | Keep-alive has timeouts and limits |

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
