# ❌ Common Misconceptions — Week 12
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> **Topic:** Email Protocols and Remote Procedure Call  
> This document lists common misunderstandings and how to correct them.

---

## Email Protocols

### 🚫 Misconception 1: "SMTP sends and receives email"

**WRONG:** "I configure SMTP in my email client and it handles all my email."

**CORRECT:** SMTP is exclusively a *push* protocol for sending email. It transfers messages from sender to recipient's mail server. To *retrieve* email from a server, you need a different protocol:

| Protocol | Direction | Purpose |
|----------|-----------|---------|
| SMTP | Push (send) | Client → Server, Server → Server |
| POP3 | Pull (receive) | Server → Client (download and delete) |
| IMAP | Pull (receive) | Server → Client (synchronise, keep on server) |

**Why this matters:** When configuring an email client, you set up TWO servers:
- Outgoing (SMTP): `smtp.example.com:587`
- Incoming (IMAP/POP3): `imap.example.com:993`

**Practical verification:**
```bash
# SMTP only accepts messages for delivery
nc localhost 1025
EHLO test
MAIL FROM:<sender@test.com>
# Notice: no command to "retrieve" messages exists in SMTP
```

---

### 🚫 Misconception 2: "EHLO and HELO are identical"

**WRONG:** "I can use HELO or EHLO interchangeably — they both just say hello."

**CORRECT:** HELO is the original SMTP greeting (RFC 821). EHLO is the Extended SMTP greeting (RFC 5321) that enables modern features:

| Command | Response | Features enabled |
|---------|----------|------------------|
| HELO | Single 250 line | Basic SMTP only |
| EHLO | Multi-line 250 | SIZE, 8BITMIME, STARTTLS, PIPELINING, AUTH |

**Why this matters:** Modern email requires EHLO for:
- TLS encryption (STARTTLS extension)
- Authentication (AUTH extension)
- Large attachments (SIZE extension)

**Practical verification:**
```bash
nc localhost 1025
HELO client
# Response: 250 Hello client

nc localhost 1025
EHLO client
# Response: 250-Hello client
#           250-SIZE 1048576
#           250-8BITMIME
#           250 PIPELINING
```

---

### 🚫 Misconception 3: "Port 25 is always used for SMTP"

**WRONG:** "SMTP uses port 25. If I can't connect on port 25, SMTP isn't running."

**CORRECT:** SMTP uses multiple ports for different purposes:

| Port | Name | Purpose | Encryption |
|------|------|---------|------------|
| 25 | SMTP | Server-to-server relay | STARTTLS optional |
| 587 | Submission | Client-to-server (authenticated) | STARTTLS required |
| 465 | SMTPS | Client-to-server (legacy) | Implicit TLS |

**Why this matters:** Most ISPs block port 25 to prevent spam. Email clients should use port 587 for sending. Our lab uses port 1025 (unprivileged) for educational purposes.

**Practical verification:**
```bash
# Our lab server on port 1025
nc localhost 1025

# Production servers typically:
# - Block port 25 from residential IPs
# - Require authentication on port 587
# - Use TLS on ports 587 and 465
```

---

### 🚫 Misconception 4: "The DATA command returns 250 OK"

**WRONG:** "All successful SMTP commands return 250."

**CORRECT:** SMTP uses different response code classes:

| Code | Meaning | Example |
|------|---------|---------|
| 2xx | Success | 250 OK, 221 Bye |
| 3xx | Intermediate | **354 Start mail input** |
| 4xx | Temporary failure | 421 Service unavailable |
| 5xx | Permanent failure | 550 Mailbox not found |

The DATA command returns **354** (not 250) because it's transitioning to a different state — the server is now waiting for message content, not another command.

In previous years, roughly half of students confused the 354 response code with 250 during the first manual SMTP exercise. The state transition is the key — DATA switches the server into content-receiving mode, which is fundamentally different from command acknowledgement.

**Why this matters:** Parsing SMTP responses requires handling different code classes. A client that only checks for "250" will fail when DATA returns 354.

**Practical verification:**
```bash
nc localhost 1025
EHLO test
MAIL FROM:<a@b.com>
RCPT TO:<c@d.com>
DATA
# Response: 354 End data with <CR><LF>.<CR><LF>
# (NOT 250!)
```

---

## Remote Procedure Call (RPC)

### 🚫 Misconception 5: "gRPC is just JSON-RPC with binary encoding"

**WRONG:** "gRPC is faster JSON-RPC because it compresses the JSON."

**CORRECT:** gRPC uses an entirely different serialisation format called Protocol Buffers (protobuf):

| Aspect | JSON-RPC | gRPC + Protobuf |
|--------|----------|-----------------|
| Format | Text (JSON) | Binary (protobuf) |
| Schema | Optional | Required (.proto files) |
| Type safety | Runtime | Compile-time |
| Code generation | Optional | Required |
| Transport | HTTP/1.1 | HTTP/2 |
| Streaming | No | Yes (4 types) |

**Why this matters:** Protobuf isn't "compressed JSON" — it's a completely different wire format using field numbers and varint encoding. You cannot read protobuf data as text.

**Practical verification:**
```bash
# JSON-RPC payload (human readable)
echo '{"jsonrpc":"2.0","method":"add","params":[10,32],"id":1}' | xxd

# gRPC/protobuf payload (binary, not readable)
# The same data is ~10-20 bytes instead of 56 bytes
```

---

### 🚫 Misconception 6: "JSON-RPC requires HTTP"

**WRONG:** "JSON-RPC is an HTTP-based protocol."

**CORRECT:** JSON-RPC is *transport agnostic*. The specification defines the message format, not the transport:

| Transport | JSON-RPC Support | Use Case |
|-----------|------------------|----------|
| HTTP | Yes (most common) | Web APIs |
| WebSocket | Yes | Real-time apps |
| TCP raw | Yes | Custom protocols |
| Unix socket | Yes | Local IPC |
| Serial/UART | Yes | Embedded systems |

**Why this matters:** You can use JSON-RPC over any bidirectional channel. The `jsonrpc: "2.0"` field identifies the protocol version regardless of transport.

**Practical verification:**
```bash
# JSON-RPC over HTTP (common)
curl -X POST http://localhost:6200 -d '{"jsonrpc":"2.0"...}'

# JSON-RPC over raw TCP would also work:
# echo '{"jsonrpc":"2.0","method":"add","params":[1,2],"id":1}' | nc server 6200
# (Depends on server implementation)
```

---

### 🚫 Misconception 7: "RPC errors return HTTP 4xx/5xx status codes"

**WRONG:** "If my JSON-RPC call fails, the server returns HTTP 500."

**CORRECT:** JSON-RPC separates transport-level and application-level errors:

| Layer | Success indicator | Error indicator |
|-------|-------------------|-----------------|
| Transport (HTTP) | 200 OK | 4xx/5xx (network/server issues) |
| Application (JSON-RPC) | `result` field present | `error` field present |

A method-not-found error returns:
```
HTTP/1.1 200 OK
Content-Type: application/json

{"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": 1}
```

**Why this matters:** Batch requests can have mixed results — some succeed, some fail — all in one HTTP 200 response. HTTP status only indicates transport success.

This trips up students who have REST experience. In REST, HTTP 404 means "resource not found". In JSON-RPC, HTTP 200 with an error object means "method not found". Different paradigms entirely.

**Practical verification:**
```bash
# Request for non-existent method
curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:6200 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"nonexistent","params":[],"id":1}'
# Output: 200 (NOT 404!)

# Check the body for the error
curl -X POST http://localhost:6200 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"nonexistent","params":[],"id":1}'
# Output: {"jsonrpc":"2.0","error":{"code":-32601,...},"id":1}
```

---

### 🚫 Misconception 8: "XML-RPC is obsolete and never used"

**WRONG:** "Nobody uses XML-RPC anymore. It's been replaced by REST and gRPC."

**CORRECT:** XML-RPC is still actively used in specific domains:

| System | Uses XML-RPC | Why |
|--------|--------------|-----|
| WordPress | Yes (xmlrpc.php) | Plugin APIs, mobile apps |
| Apache (mod_xmlrpc) | Yes | Server management |
| Bugzilla | Yes | Bug tracking APIs |
| Legacy enterprise | Yes | Existing integrations |
| Supervisord | Yes | Process control |

**Why this matters:** Understanding XML-RPC helps you:
- Integrate with legacy systems
- Debug WordPress security issues (xmlrpc attacks)
- Appreciate the evolution from XML-RPC → JSON-RPC → gRPC

**Practical verification:**
```bash
# XML-RPC introspection (list available methods)
curl -X POST http://localhost:6201 \
  -H "Content-Type: text/xml" \
  -d '<?xml version="1.0"?><methodCall><methodName>system.listMethods</methodName></methodCall>'
```

---

### 🚫 Misconception 9: "Protocol Buffers are just compressed JSON"

**WRONG:** "Protobuf takes JSON and compresses it for transmission."

**CORRECT:** Protocol Buffers are a completely different serialisation format:

| Aspect | JSON | Protocol Buffers |
|--------|------|------------------|
| Format | Text (UTF-8) | Binary |
| Schema | None (implicit) | Required (.proto file) |
| Field identification | String keys | Numeric field tags |
| Encoding | Human readable | Varint + wire types |
| Parsing | Dynamic | Generated code |

A protobuf message `{a: 10.0, b: 32.0}` is encoded as raw bytes using field numbers (1, 2) and IEEE 754 doubles — not as JSON with compression.

**Why this matters:** You cannot "view" protobuf as text. You need the .proto schema to decode it. This is a feature (schema enforcement) not a limitation.

**Practical verification:**
```bash
# View the .proto schema
cat src/apps/rpc/grpc/calculator.proto

# The wire format uses field numbers (1, 2) not names ("a", "b")
# message CalcRequest {
#     double a = 1;  <- field tag 1
#     double b = 2;  <- field tag 2
# }
```

---

### 🚫 Misconception 10: "RPC calls are always synchronous"

**WRONG:** "When I call an RPC method, my programme blocks until it returns."

**CORRECT:** RPC can be synchronous or asynchronous:

| Pattern | Blocking? | Use case |
|---------|-----------|----------|
| Synchronous (request-response) | Yes | Simple calls |
| Asynchronous (callback/promise) | No | Non-blocking I/O |
| JSON-RPC notification | No response | Fire-and-forget |
| gRPC streaming | Continuous | Real-time data |

**Why this matters:** Modern RPC frameworks support async patterns:
- JSON-RPC notifications (omit `id` field)
- gRPC server streaming, client streaming, bidirectional streaming
- Async client libraries (asyncio in Python)

**Practical verification:**
```bash
# JSON-RPC notification (no id = no response expected)
curl -X POST http://localhost:6200 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"add","params":[1,2]}'
# Server returns HTTP 204 No Content (no response body)
```

---

## Quick Reference Table

| # | Misconception | Reality |
|---|---------------|---------|
| 1 | SMTP sends and receives | SMTP sends only; POP3/IMAP receive |
| 2 | EHLO = HELO | EHLO enables extensions (TLS, AUTH) |
| 3 | SMTP always uses port 25 | 587 (submission), 465 (SMTPS), 25 (relay) |
| 4 | DATA returns 250 | DATA returns 354 (intermediate state) |
| 5 | gRPC = binary JSON-RPC | gRPC uses Protocol Buffers (different format) |
| 6 | JSON-RPC requires HTTP | JSON-RPC is transport agnostic |
| 7 | RPC errors = HTTP errors | Application errors return HTTP 200 + error object |
| 8 | XML-RPC is obsolete | Still used (WordPress, legacy systems) |
| 9 | Protobuf = compressed JSON | Protobuf is binary with schema |
| 10 | RPC is always synchronous | Notifications, streaming, async patterns exist |

---

## See Also

- `peer_instruction.md` — MCQ questions targeting these misconceptions
- `glossary.md` — Terminology definitions
- `theory_summary.md` — Protocol specifications

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
