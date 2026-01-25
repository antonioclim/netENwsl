# Common Misconceptions — Week 8: Transport Layer & HTTP

> Computer Networks — ASE, CSIE

This document catalogues common misconceptions students have about transport
layer protocols and HTTP. Each entry includes the misconception, the correct
understanding and a visual aid where helpful.

**Usage:** When you encounter an error or unexpected behaviour check if one
of these misconceptions might be the cause.

> 💡 **From past labs:** These misconceptions come directly from debugging sessions
> with students over the past five years. The port number confusion (#1) and the
> third ACK myth (#3) appear most frequently — expect to see them in your code too.

---

## Table of Contents

1. [Port Size and Range](#port-size)
2. [Demultiplexing](#demultiplexing)
3. [Third ACK is Optional](#third-ack-optional)
4. [HEAD Returns HEAD Metadata](#head-returns-head-metadata)
5. [Reverse vs Forward Proxy](#reverse-vs-forward-proxy)
6. [Round-Robin Equals Equal Load](#round-robin-equal-load)
7. [403 vs 404 for Security](#403-vs-404)
8. [One Request Per Connection](#http-one-request-per-connection)

---

<a name="port-size"></a>
## 1. Port Size and Range

### 🚫 Misconception
> "Port numbers go up to 65536"

### ✅ Correct Understanding

Port numbers are 16-bit unsigned integers ranging from **0 to 65535**.

```
16 bits = 2^16 = 65,536 possible values
But counting starts from 0, so: 0 to 65,535

┌─────────────────────────────────────────────────────────────┐
│                    PORT NUMBER RANGES                        │
├─────────────────────────────────────────────────────────────┤
│  0-1023      │  Well-known ports (HTTP=80, HTTPS=443)       │
│  1024-49151  │  Registered ports (MySQL=3306, Redis=6379)   │
│  49152-65535 │  Dynamic/ephemeral ports (client sockets)    │
└─────────────────────────────────────────────────────────────┘
```

### Why It Matters

If you try to bind to port 65536 you will get an error:
```python
# This fails!
socket.bind(('0.0.0.0', 65536))  # ValueError: port must be 0-65535
```

---

<a name="demultiplexing"></a>
## 2. Demultiplexing

### 🚫 Misconception
> "The kernel knows which process owns a socket because the PID is in the packet header"

### ✅ Correct Understanding

There is NO process ID in TCP/UDP headers. The kernel maintains an internal
table mapping **port numbers to sockets**.

```
┌─────────────────────────────────────────────────────────────┐
│                 KERNEL SOCKET TABLE                          │
├──────────────┬────────────┬─────────────────────────────────┤
│   Protocol   │    Port    │         Socket/Process          │
├──────────────┼────────────┼─────────────────────────────────┤
│     TCP      │     80     │  nginx (PID 1234)               │
│     TCP      │    443     │  nginx (PID 1234)               │
│     TCP      │   3306     │  mysqld (PID 5678)              │
│     UDP      │     53     │  dnsmasq (PID 9012)             │
│     TCP      │   8080     │  YOUR_SERVER (PID ???)          │
└──────────────┴────────────┴─────────────────────────────────┘

When packet arrives with dst_port=80:
  1. Kernel looks up port 80 in table
  2. Finds nginx's socket
  3. Delivers data to nginx's recv() buffer
```

### Why It Matters

This is why "Address already in use" occurs — two processes cannot bind the
same port because the kernel table only has one entry per port.

---

<a name="third-ack-optional"></a>
## 3. Third ACK is Optional

### 🚫 Misconception
> "The third ACK in TCP handshake is optional — the connection works with just SYN and SYN-ACK"

### ✅ Correct Understanding

The third ACK is **REQUIRED**. Without it the server remains in SYN_RCVD state
and will eventually time out.

```
    CLIENT                              SERVER
       │                                   │
  ┌────┴────┐                         ┌────┴────┐
  │ CLOSED  │                         │ LISTEN  │
  └────┬────┘                         └────┬────┘
       │                                   │
       │──────── SYN (seq=100) ──────────▶│
       │                                   │
  ┌────┴────┐                         ┌────┴────┐
  │SYN-SENT │                         │SYN-RCVD │
  └────┬────┘                         └────┬────┘
       │                                   │
       │◀─── SYN-ACK (seq=300,ack=101) ───│
       │                                   │


WITHOUT THIRD ACK (BROKEN):
       │                                   │
  ┌────┴────┐                         ┌────┴────┐
  │ ESTABL  │ ← Client thinks OK      │SYN-RCVD │ ← Server WAITING!
  └────┬────┘                         └────┬────┘
       │                                   │
       │──────── DATA ─────────────────X   │ ← Server DROPS data!
       │                                   │   (connection not established)


WITH THIRD ACK (CORRECT):
       │                                   │
       │──────── ACK (ack=301) ──────────▶│ ← NOW both confirmed!
       │                                   │
  ┌────┴────┐                         ┌────┴────┐
  │ ESTABL  │                         │ ESTABL  │
  └─────────┘                         └─────────┘
```

### Why Three Packets?

The handshake proves **bidirectional communication**:
1. SYN: Client can send
2. SYN-ACK: Server can send AND receive
3. ACK: Client can receive

Two packets would only prove one direction works.

---

<a name="head-returns-head-metadata"></a>
## 4. HEAD Returns HEAD Metadata

### 🚫 Misconception
> "HTTP HEAD method returns metadata about the HEAD request itself"

### ✅ Correct Understanding

HEAD returns **exactly the same headers** that a GET request would return
but **without the response body**.

```
GET /large-file.zip HTTP/1.1        HEAD /large-file.zip HTTP/1.1
Host: example.com                   Host: example.com

         │                                   │
         ▼                                   ▼

HTTP/1.1 200 OK                     HTTP/1.1 200 OK
Content-Type: application/zip       Content-Type: application/zip
Content-Length: 52428800            Content-Length: 52428800
Last-Modified: Mon, 01 Jan 2024     Last-Modified: Mon, 01 Jan 2024

[50 MB of binary data]              [NO BODY - saves 50 MB!]
```

### Why It Matters

HEAD is useful for:
- Checking if a resource exists without downloading it
- Getting file size before download
- Checking Last-Modified for caching
- Validating links without fetching content

---

<a name="reverse-vs-forward-proxy"></a>
## 5. Reverse vs Forward Proxy

### 🚫 Misconception
> "Reverse proxy and forward proxy are the same thing"

### ✅ Correct Understanding

They serve **opposite purposes**:

```
┌─────────────────────────────────────────────────────────────┐
│                    FORWARD PROXY                             │
│  Client knows about proxy; proxy hides client from server   │
└─────────────────────────────────────────────────────────────┘

  ┌────────┐       ┌───────────┐       ┌────────────────┐
  │ Client │──────▶│  Forward  │──────▶│ Internet/      │
  │ (you)  │       │  Proxy    │       │ Servers        │
  └────────┘       └───────────┘       └────────────────┘
     │                   │                     │
     │ "Use proxy        │ "Request from      │ "I see the
     │  server:8080"     │  proxy IP"         │  proxy not
     │                   │                    │  the client"


┌─────────────────────────────────────────────────────────────┐
│                    REVERSE PROXY                             │
│  Client unaware of backend; proxy hides servers from client │
└─────────────────────────────────────────────────────────────┘

  ┌────────┐       ┌───────────┐       ┌────────────────┐
  │ Client │──────▶│  Reverse  │──────▶│ Backend        │
  │ (user) │       │  Proxy    │       │ Servers        │
  └────────┘       └───────────┘       └────────────────┘
     │                   │                     │
     │ "I'm talking      │ "Route to          │ "I only see
     │  to website.com"  │  backend 2"        │  the proxy"
```

### Key Differences

| Aspect | Forward Proxy | Reverse Proxy |
|--------|---------------|---------------|
| Client awareness | Client configures proxy | Client unaware |
| Protects | Client identity | Server identity |
| Use case | Corporate networks | Load balancing |

---

<a name="round-robin-equal-load"></a>
## 6. Round-Robin Equals Equal Load

### 🚫 Misconception
> "If I distribute requests equally using round-robin then all servers have equal load"

### ✅ Correct Understanding

Equal **request count** ≠ equal **load**. Some requests take longer than others.

```
Time ────────────────────────────────────────────────────▶

Backend 1: ████████████████████████████████████████████████ (overloaded!)
           [heavy query 5s][heavy query 4s][query 3s][q 2s]

Backend 2: ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ (idle 80%)
           [0.1s][0.1s][0.1s][0.1s]

Backend 3: ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ (idle 60%)
           [0.5s][0.5s][0.5s][0.5s]

All three received 4 requests but Backend 1 is overwhelmed!
```

### Better Approaches

1. **Weighted round-robin** — give more requests to faster servers
2. **Least connections** — send to server with fewest active requests
3. **Weighted least connections** — combination of both

---

<a name="403-vs-404"></a>
## 7. 403 vs 404 for Security

### 🚫 Misconception
> "Always return 403 Forbidden for directory traversal attacks to tell attackers they cannot access that file"

### ✅ Correct Understanding

Returning 403 **confirms the file exists** which helps attackers. Consider 404.

```
Attacker tries: GET /../../../etc/shadow HTTP/1.1

Response 403 Forbidden:
┌─────────────────────────────────────────────────────────────┐
│ "Aha! The file EXISTS but I cannot read it yet.            │
│  Let me try other techniques..."                           │
└─────────────────────────────────────────────────────────────┘

Response 404 Not Found:
┌─────────────────────────────────────────────────────────────┐
│ "Hmm, maybe the file does not exist, or maybe access        │
│  is denied. I cannot tell. Dead end."                      │
└─────────────────────────────────────────────────────────────┘
```

### Trade-offs

| Response | Reveals | User Experience |
|----------|---------|-----------------|
| 403 | File exists, permission denied | Clear to legitimate users |
| 404 | Nothing (could exist or not) | Confusing for legitimate users |

### What Do Major Servers Do?

- **nginx:** Returns 403 by default, configurable
- **Apache:** Returns 403 by default
- **OWASP recommendation:** Return consistent responses to prevent enumeration

---

<a name="http-one-request-per-connection"></a>
## 8. One Request Per Connection

### 🚫 Misconception
> "Each HTTP request requires a new TCP connection"

### ✅ Correct Understanding

HTTP/1.1 uses **persistent connections** by default. Multiple requests share
one TCP connection.

```
HTTP/1.0 (old behaviour):
┌───────────────────────────────────────────────────────────┐
│ Request 1 │ [SYN][SYN-ACK][ACK][GET][200][FIN][ACK]      │
│ Request 2 │ [SYN][SYN-ACK][ACK][GET][200][FIN][ACK]      │
│ Request 3 │ [SYN][SYN-ACK][ACK][GET][200][FIN][ACK]      │
└───────────────────────────────────────────────────────────┘
             ▲                        ▲
             │                        │
     3 handshakes              3 teardowns = SLOW!


HTTP/1.1 (default — persistent):
┌───────────────────────────────────────────────────────────┐
│ All 3     │ [SYN][SYN-ACK][ACK]                          │
│ Requests  │ [GET][200][GET][200][GET][200]               │
│           │ [FIN][ACK]                                   │
└───────────────────────────────────────────────────────────┘
             ▲                        ▲
             │                        │
     1 handshake               1 teardown = FAST!
```

### HTTP/2 Goes Further

HTTP/2 adds **multiplexing** — multiple requests/responses in parallel on
one connection:

```
HTTP/1.1: Request 1 ────▶ Response 1 ────▶ Request 2 ────▶ Response 2
          (must wait)

HTTP/2:   Request 1 ────────────────▶ Response 1
          Request 2 ────────────────▶ Response 2
          Request 3 ────────────────▶ Response 3
          (all interleaved on one connection)
```

---

## Quick Reference Table

| Misconception | Reality | Quiz Reference |
|--------------|---------|----------------|
| Ports go to 65536 | 0-65535 (16-bit) | q01 |
| PID in packet header | Kernel table lookup | q02 |
| Third ACK optional | Required for ESTABLISHED | q05, q06 |
| HEAD returns metadata | Same headers as GET, no body | q09 |
| Reverse = Forward proxy | Opposite purposes | q12 |
| Round-robin = equal load | Equal requests ≠ equal load | q14 |
| 403 for traversal | 404 reveals less | q19 |
| One request per TCP | HTTP/1.1 keeps connection open | q18 |

---

## See Also

- `docs/theory_summary.md` — Detailed protocol explanations
- `docs/peer_instruction.md` — Discussion questions about these topics
- `formative/quiz.yaml` — Self-assessment with misconception links

---

*Computer Networks — ASE, CSIE*

*"The first step to learning is unlearning what you think you know."*
