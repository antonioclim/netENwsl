# 🗳️ Peer Instruction Questions — Week 12
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> **Topic:** Email Protocols and Remote Procedure Call  
> **Duration:** ~25 minutes (5 questions × 5 min each)

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

## Question 1: SMTP Response Codes

> 💭 **PREDICTION:** Before answering, recall what happens when you type `DATA` in an SMTP session.

### Scenario

You connect to an SMTP server using netcat and send these commands:

```
EHLO client.local
MAIL FROM:<alice@example.com>
RCPT TO:<bob@example.com>
DATA
```

### Question

What response code does the server send after the `DATA` command?

### Options

- **A)** `250 OK` — Success, ready for message content
- **B)** `354 Start mail input` — Intermediate response, waiting for message body
- **C)** `220 Service ready` — Greeting response
- **D)** `550 Requested action not taken` — Permanent failure

### Correct Answer

**B** — `354 Start mail input; end with <CRLF>.<CRLF>`

### Targeted Misconception

Students often confuse `250` (command success) with `354` (intermediate state). The DATA command triggers a state transition where the server expects message content, not another command. The `354` code signals "I'm ready to receive the message body" rather than "command completed successfully".

### Instructor Notes

- **Target accuracy:** ~50-60% on first vote
- **Key concept:** SMTP is a stateful protocol with distinct phases (envelope vs data)
- **After discussion:** Show the RFC 5321 state diagram
- **Visual aid:** Run `nc localhost 1025` and demonstrate live

---

## Question 2: JSON-RPC vs REST

> 💭 **PREDICTION:** Think about what makes JSON-RPC different from a typical REST API.

### Scenario

You need to call a remote `calculator.add(10, 32)` method. Here are two approaches:

**Approach A (REST-style):**
```http
POST /calculator/add HTTP/1.1
Content-Type: application/json

{"a": 10, "b": 32}
```

**Approach B (JSON-RPC):**
```http
POST / HTTP/1.1
Content-Type: application/json

{"jsonrpc": "2.0", "method": "add", "params": [10, 32], "id": 1}
```

### Question

Which statement correctly describes a key difference between these approaches?

### Options

- **A)** REST uses HTTP verbs for semantics; JSON-RPC uses a single endpoint with method names in the payload
- **B)** JSON-RPC is faster because it uses binary encoding
- **C)** REST requires XML; JSON-RPC requires JSON
- **D)** JSON-RPC only works over WebSockets, not HTTP

### Correct Answer

**A** — REST uses HTTP verbs (GET, POST, PUT, DELETE) and URLs to express operations, whilst JSON-RPC routes all requests to a single endpoint and specifies the method name in the JSON payload.

### Targeted Misconception

Students often think JSON-RPC must be faster or use special encoding. Both approaches use JSON over HTTP — the difference is architectural: REST is resource-oriented (URLs represent resources, verbs represent actions), whilst RPC is procedure-oriented (URLs are endpoints, methods are in the payload).

### Instructor Notes

- **Target accuracy:** ~40-50% on first vote
- **Key concept:** Architectural style vs protocol
- **After discussion:** Show Wireshark captures comparing payload structures
- **Follow-up:** Ask "Which is better for a public API? Why?"

---

## Question 3: gRPC Serialisation

> 💭 **PREDICTION:** Consider what Protocol Buffers actually are before answering.

### Scenario

You have a gRPC service defined as:

```protobuf
message CalcRequest {
    double a = 1;
    double b = 2;
}

service Calculator {
    rpc Add(CalcRequest) returns (CalcResponse);
}
```

A client calls `Add(a=10.0, b=32.0)`.

### Question

How is this request transmitted over the network?

### Options

- **A)** As JSON: `{"a": 10.0, "b": 32.0}`
- **B)** As XML: `<CalcRequest><a>10.0</a><b>32.0</b></CalcRequest>`
- **C)** As compact binary data encoded according to the .proto schema
- **D)** As plain text: `a=10.0&b=32.0`

### Correct Answer

**C** — Protocol Buffers encode data as compact binary using field numbers (1, 2) and wire types. The resulting payload is much smaller than JSON or XML equivalents.

### Targeted Misconception

Many students assume gRPC "is just RPC with JSON" or that Protocol Buffers are simply "compressed JSON". Protocol Buffers are a completely different serialisation format: schema-defined, binary-encoded and not human-readable. The `.proto` file defines the schema; the actual wire format uses varint encoding and field tags.

### Instructor Notes

- **Target accuracy:** ~55-65% on first vote
- **Key concept:** Binary vs text serialisation trade-offs
- **After discussion:** Show hex dump of actual gRPC payload vs JSON equivalent
- **Demo:** Compare payload sizes using the benchmark script

---

## Question 4: SMTP Mail Flow

> 💭 **PREDICTION:** Think about which protocols your email client uses when you click "Send".

### Scenario

Alice uses Thunderbird to send an email to Bob, who uses Gmail's web interface.

### Question

Which protocols are involved in delivering Alice's email to Bob's inbox?

### Options

- **A)** SMTP only — from Alice's client to Bob's inbox
- **B)** SMTP to send, then POP3 or IMAP for Bob to retrieve
- **C)** HTTP only — modern email is all web-based
- **D)** FTP to transfer the email file between servers

### Correct Answer

**B** — SMTP is a *push* protocol used for sending: Alice's client → her mail server → Bob's mail server. Bob then uses a *pull* protocol (POP3 or IMAP, or HTTP via Gmail's web interface) to retrieve the message from his server.

### Targeted Misconception

Students frequently believe "SMTP handles email" without distinguishing send vs receive. SMTP is exclusively for transmission (Mail Transfer Agent to MTA). Retrieval requires a different protocol. Even Gmail's web interface ultimately uses IMAP internally or proprietary protocols — the HTTP is for the web UI, not the email transfer itself.

### Instructor Notes

- **Target accuracy:** ~45-55% on first vote
- **Key concept:** Push vs pull protocols; MTA vs MUA
- **After discussion:** Draw the complete email flow diagram
- **Real-world:** Explain why you configure "outgoing server" (SMTP) separately from "incoming server" (IMAP/POP3)

---

## Question 5: RPC Error Handling

> 💭 **PREDICTION:** What happens when you call a method that doesn't exist on a JSON-RPC server?

### Scenario

You send this request to a JSON-RPC server:

```json
{"jsonrpc": "2.0", "method": "nonexistent", "params": [], "id": 42}
```

### Question

What does the server respond with?

### Options

- **A)** HTTP 404 Not Found with no body
- **B)** HTTP 200 OK with a JSON-RPC error object containing code `-32601`
- **C)** HTTP 500 Internal Server Error
- **D)** The connection is closed with no response

### Correct Answer

**B** — JSON-RPC returns errors as structured JSON objects within an HTTP 200 response:
```json
{"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": 42}
```

### Targeted Misconception

Students often expect RPC errors to map to HTTP status codes. JSON-RPC deliberately separates transport-level success (HTTP 200 = "I received and processed your request") from application-level errors (the error object). This allows batch requests where some calls succeed and others fail, all in one HTTP 200 response.

### Instructor Notes

- **Target accuracy:** ~35-45% on first vote (this is tricky!)
- **Key concept:** Transport vs application layer error handling
- **After discussion:** Show the standard JSON-RPC error codes table
- **Comparison:** Contrast with REST, where HTTP 404 might mean "resource not found"

---

## Summary of Question Topics

| # | Topic | Key Misconception Targeted |
|---|-------|---------------------------|
| 1 | SMTP Response Codes | 250 vs 354 (success vs intermediate) |
| 2 | JSON-RPC vs REST | Architectural differences |
| 3 | gRPC/Protocol Buffers | "gRPC is JSON-RPC with binary" |
| 4 | Email Protocol Flow | "SMTP does everything" |
| 5 | RPC Error Handling | HTTP status vs RPC errors |

---

## Additional Resources

- See `misconceptions.md` for detailed explanations of common errors
- See `glossary.md` for terminology definitions
- See `theory_summary.md` for protocol specifications

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
