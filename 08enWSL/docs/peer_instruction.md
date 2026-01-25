# 🗳️ Peer Instruction Questions — Week 8
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> 💡 **Teaching heuristic:** If vote distribution is >80% correct on first vote,
> the question is too easy — skip the discussion phase. If <20% correct, provide
> a hint before the peer discussion. The sweet spot is 40-60% where discussion
> produces the most learning.

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

## Question 1: TCP Three-Way Handshake

> 💭 **PREDICTION:** Before reading the scenario, predict: How many packets are needed to establish a TCP connection?

### Scenario

A client wants to connect to a web server. You capture the following packets in Wireshark:

```
Packet 1: Client → Server  [SYN] Seq=1000
Packet 2: Server → Client  [SYN, ACK] Seq=5000, Ack=1001
Packet 3: Client → Server  [ACK] Seq=1001, Ack=5001
```

### Question

Why does TCP require exactly THREE packets for connection establishment, not two or four?

### Options

- **A)** Two packets would be sufficient — the third ACK is just for confirmation and can be skipped
  - *[Misconception: Confusing TCP with simpler protocols]*

- **B)** Three packets ensure both sides confirm they can send AND receive, synchronising sequence numbers in both directions
  - *[CORRECT]*

- **C)** The third packet carries the first data payload, so it serves a dual purpose
  - *[Misconception: Confusing handshake with data transfer]*

- **D)** Four packets would be needed for full reliability, but TCP sacrifices reliability for speed
  - *[Misconception: Misunderstanding TCP reliability guarantees]*

### Correct Answer

**B** — The three-way handshake ensures both parties confirm bidirectional communication:
1. SYN: Client proves it can send
2. SYN-ACK: Server proves it can send AND receive
3. ACK: Client proves it can receive

Two packets would only confirm one direction. Four packets would add no additional confirmation.

### Targeted Misconception

Students often think the third ACK is optional or redundant. Without it, the server cannot confirm the client received its SYN-ACK, leaving the connection half-established.

### Instructor Notes

- **Target accuracy:** ~50% on first vote
- **Key concept:** Bidirectional confirmation
- **After discussion:** Show Wireshark capture of real handshake, highlight sequence numbers
- **Demo:** `curl -v http://localhost:8080` while capturing with filter `tcp.flags.syn == 1`

---

## Question 2: HTTP Status Codes and Directory Traversal

> 💭 **PREDICTION:** What happens when a web server receives a request for `/../../../etc/passwd`?

### Scenario

You implement an HTTP server that serves files from `/var/www/html`. A client sends:

```http
GET /../../../etc/passwd HTTP/1.1
Host: localhost
```

Your server uses `os.path.normpath()` and checks if the resolved path starts with the document root.

### Question

What HTTP status code should your server return?

### Options

- **A)** 404 Not Found — the file doesn't exist in the web directory
  - *[Misconception: Treating security issues as missing files]*

- **B)** 403 Forbidden — access to the file is denied due to security restrictions
  - *[CORRECT]*

- **C)** 400 Bad Request — the URL is malformed
  - *[Misconception: Path traversal is syntactically valid]*

- **D)** 500 Internal Server Error — the server cannot process the request
  - *[Misconception: Security checks are not server errors]*

### Correct Answer

**B** — 403 Forbidden is correct because:
- The request is syntactically valid (not 400)
- The file may exist but access is DENIED (not 404)
- The server processed correctly and made a security decision (not 500)

403 tells the client: "I understood your request, but I refuse to fulfill it."

### Targeted Misconception

Students often return 404 for security violations, thinking "if they can't access it, it doesn't exist for them." This is security through obscurity and leaks information (404 vs 403 tells attackers which paths exist).

### Instructor Notes

- **Target accuracy:** ~40% on first vote
- **Key concept:** Semantic meaning of HTTP status codes
- **After discussion:** Show both approaches, discuss security implications
- **Demo:** Test with `curl -v http://localhost:8081/../../etc/passwd`

---

## Question 3: Reverse Proxy vs Forward Proxy

> 💭 **PREDICTION:** Which component does the client connect to when using a reverse proxy?

### Scenario

Your company deploys the following architecture:

```
┌──────────┐     ┌─────────────────┐     ┌──────────────┐
│  Client  │────▶│  nginx (proxy)  │────▶│  Backend 1   │
│ Browser  │     │  172.28.8.10    │────▶│  Backend 2   │
└──────────┘     └─────────────────┘────▶│  Backend 3   │
                                         └──────────────┘
```

### Question

In this reverse proxy setup, what does the client browser know about?

### Options

- **A)** The client knows about all three backends and nginx, choosing which to connect to
  - *[Misconception: Confusing reverse proxy with DNS round-robin]*

- **B)** The client only knows about nginx; the backends are hidden from the client
  - *[CORRECT]*

- **C)** The client connects directly to backends; nginx only monitors traffic
  - *[Misconception: Confusing reverse proxy with network monitor]*

- **D)** The client knows about nginx and one backend that nginx selects permanently
  - *[Misconception: Confusing with sticky sessions]*

### Correct Answer

**B** — In a reverse proxy setup:
- The client sees ONLY the proxy (nginx)
- The client's TCP connection terminates at nginx
- nginx opens SEPARATE connections to backends
- Backends are completely hidden from clients

This is the opposite of a forward proxy where the client knows it's using a proxy.

### Targeted Misconception

Students confuse reverse proxies with DNS load balancing, where clients DO know about multiple servers. In reverse proxy, all backend details are hidden.

### Instructor Notes

- **Target accuracy:** ~55% on first vote
- **Key concept:** Connection termination point
- **After discussion:** Draw the TCP connections explicitly (two separate connections)
- **Demo:** Show `curl -v` output — note it only shows nginx, not backends

---

## Question 4: HTTP Keep-Alive

> 💭 **PREDICTION:** How many TCP connections are needed to fetch a webpage with 5 images?

### Scenario

A browser requests an HTML page that references 5 images:

```http
GET /index.html HTTP/1.1
Host: example.com
Connection: keep-alive
```

The server responds with `Connection: keep-alive` in all responses.

### Question

How many TCP connections will be established to fetch the HTML and all 5 images?

### Options

- **A)** 6 connections — one for each resource (HTML + 5 images)
  - *[Misconception: Ignoring keep-alive entirely]*

- **B)** 1 connection — keep-alive reuses the same connection for all requests
  - *[CORRECT]*

- **C)** 2 connections — one for HTML, one shared for all images
  - *[Misconception: Confusing with HTTP/2 streams]*

- **D)** It depends on the timeout — connections close after 30 seconds of inactivity
  - *[Misconception: Mixing connection reuse with timeout behaviour]*

### Correct Answer

**B** — With HTTP/1.1 keep-alive:
- One TCP connection is established (3-way handshake)
- All 6 requests (HTML + 5 images) use the same connection
- The connection stays open between requests
- This saves 5 × RTT for avoided handshakes

Note: Modern browsers may open multiple parallel connections (6-8) for performance, but each connection can be reused for multiple requests.

### Targeted Misconception

Students often think each HTTP request needs a new TCP connection. HTTP/1.0 worked this way by default; HTTP/1.1 changed the default to keep-alive.

### Instructor Notes

- **Target accuracy:** ~45% on first vote
- **Key concept:** Connection reuse vs new connections
- **After discussion:** Show Wireshark capture with multiple HTTP requests on same TCP stream
- **Demo:** Filter `tcp.stream eq 0` and count HTTP request/response pairs

---

## Question 5: Round-Robin Load Balancing

> 💭 **PREDICTION:** With 3 backends weighted 5:3:1, how many of the first 9 requests go to backend 1?

### Scenario

nginx is configured with weighted round-robin:

```nginx
upstream backend_pool {
    server backend1:8080 weight=5;
    server backend2:8080 weight=3;
    server backend3:8080 weight=1;
}
```

### Question

After 9 requests, approximately how many went to each backend?

### Options

- **A)** backend1: 3, backend2: 3, backend3: 3 — weights are ignored in round-robin
  - *[Misconception: Confusing weighted with simple round-robin]*

- **B)** backend1: 5, backend2: 3, backend3: 1 — distribution matches the weights
  - *[CORRECT]*

- **C)** backend1: 9, backend2: 0, backend3: 0 — highest weight gets all until it fails
  - *[Misconception: Confusing with failover behaviour]*

- **D)** backend1: 5, backend2: 3, backend3: 1, but only after 90+ requests (weights need large samples)
  - *[Misconception: Thinking weights only work statistically over time]*

### Correct Answer

**B** — Weighted round-robin distributes requests proportionally:
- Total weight = 5 + 3 + 1 = 9
- backend1 gets 5/9 of requests (≈ 5 out of 9)
- backend2 gets 3/9 of requests (≈ 3 out of 9)
- backend3 gets 1/9 of requests (≈ 1 out of 9)

The algorithm cycles through, giving more turns to higher-weighted servers.

### Targeted Misconception

Students often think weights only matter statistically over thousands of requests. nginx's smooth weighted round-robin ensures proportional distribution even for small request counts.

### Instructor Notes

- **Target accuracy:** ~50% on first vote
- **Key concept:** Weighted distribution algorithm
- **After discussion:** Show nginx access logs with backend selection
- **Demo:** `for i in {1..9}; do curl -s http://localhost:8080/ | grep Backend; done`

---

## Summary: Key Concepts Tested

| Question | Topic | Primary Misconception Targeted |
|----------|-------|-------------------------------|
| Q1 | TCP Handshake | Third ACK is optional |
| Q2 | HTTP Status Codes | 404 for security violations |
| Q3 | Reverse Proxy | Client knows about backends |
| Q4 | Keep-Alive | Each request needs new connection |
| Q5 | Load Balancing | Weights only matter statistically |

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
