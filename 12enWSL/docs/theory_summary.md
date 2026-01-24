# Week 12 Theory Summary: Email Protocols and RPC
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## 1. Email Protocols

### 1.1 SMTP (Simple Mail Transfer Protocol)

SMTP is a **push protocol** used for sending email between mail servers and from clients to servers. It operates at the **Application Layer** (Layer 7) of the OSI model.

#### Real-World Analogy (CPA: Concrete)

Think of SMTP like a postal service:
- You write a letter (compose email)
- You put it in an envelope with addresses (MAIL FROM, RCPT TO)
- You hand it to the post office (SMTP server)
- The post office delivers it to the recipient's post office (destination MTA)
- The recipient must collect it themselves (using POP3/IMAP)

**Key insight:** The postal service only *delivers* — it doesn't let you *retrieve* letters from someone else's mailbox. That's why SMTP only sends; retrieval needs a different protocol.

#### Key Characteristics

- Text-based protocol over TCP (port 25, 587 for submission, 465 for SMTPS)
- Stateful connection with command-response dialogue
- Commands are 4-letter ASCII words followed by parameters
- Response codes: 2xx success, 3xx intermediate, 4xx temporary failure, 5xx permanent failure

#### SMTP Commands

| Command | Purpose |
|---------|---------|
| HELO/EHLO | Identify client to server |
| MAIL FROM | Specify sender address |
| RCPT TO | Specify recipient address |
| DATA | Begin message transfer |
| QUIT | End session |
| RSET | Reset transaction |
| VRFY | Verify address (often disabled) |
| NOOP | No operation (keep-alive) |

#### Mail Transaction Phases

1. **Connection**: TCP handshake + 220 greeting
2. **Envelope**: MAIL FROM + RCPT TO define routing
3. **Data**: Headers + blank line + body + terminating dot
4. **Commitment**: Server accepts responsibility for delivery

#### Common Misconception

❌ "SMTP handles all email operations"

✅ SMTP only **sends** email. Retrieval requires POP3 or IMAP. See `docs/misconceptions.md` for details.

### 1.2 POP3 (Post Office Protocol v3)

POP3 is a **pull protocol** for retrieving email from a mail server (port 110, 995 for SSL).

**Characteristics:**
- Simple download-and-delete model
- State-based: AUTHORIZATION → TRANSACTION → UPDATE
- Limited server-side management
- Suitable for single-device access

### 1.3 IMAP (Internet Message Access Protocol)

IMAP provides more sophisticated mailbox management (port 143, 993 for SSL).

**Characteristics:**
- Server-side message storage and organisation
- Multiple folder support
- Partial message retrieval
- Flag management (read, deleted, etc.)
- Suitable for multi-device access

---

## 2. Remote Procedure Call (RPC)

### 2.1 The RPC Abstraction

RPC abstracts network communication, allowing remote function calls with local call syntax.

#### Real-World Analogy (CPA: Concrete)

Think of RPC like ordering food by phone:
- You call the restaurant (establish connection)
- You say "I want a pizza with pepperoni" (method call with parameters)
- Someone in the kitchen makes it (server processes request)
- They tell you "Ready in 20 minutes" (return value)
- You didn't need to know *how* they made it — just what you wanted

The phone call is the "transport", your order is "serialised" into words and the kitchen "deserialises" your words into actions.

#### Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  CLIENT                                              SERVER                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [Application]                                      [Application]           │
│       │                                                  ▲                  │
│       ▼ call(a, b)                              return   │                  │
│  [Client Stub]                                   [Server Stub]              │
│       │                                                  ▲                  │
│       ▼ serialise                           deserialise │                  │
│  [Transport]  ──────── Network (bytes) ────────▶ [Transport]               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### Components

- **Client Stub**: Marshalls parameters, sends request, unmarshalls response
- **Server Stub**: Unmarshalls request, invokes method, marshalls response
- **Transport**: TCP, HTTP, HTTP/2
- **Serialisation**: JSON, XML, Protocol Buffers

### 2.2 JSON-RPC 2.0

**Specification:** https://www.jsonrpc.org/specification

#### Request Format

```json
{
    "jsonrpc": "2.0",
    "method": "method_name",
    "params": [arg1, arg2],
    "id": 1
}
```

Alternative with named parameters:
```json
{
    "jsonrpc": "2.0",
    "method": "add",
    "params": {"a": 10, "b": 32},
    "id": 1
}
```

#### Response Format

```json
{"jsonrpc": "2.0", "result": 42, "id": 1}
```

#### Error Response

```json
{"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": 1}
```

#### Standard Error Codes

| Code | Meaning |
|------|---------|
| -32700 | Parse error |
| -32600 | Invalid request |
| -32601 | Method not found |
| -32602 | Invalid params |
| -32603 | Internal error |
| -32000 to -32099 | Server errors |

#### Features

- Batch requests (array of requests)
- Notifications (no `id` → no response)
- Transport agnostic (works over HTTP, WebSocket, TCP, etc.)

#### Common Misconception

❌ "JSON-RPC errors return HTTP 4xx/5xx"

✅ JSON-RPC returns HTTP 200 even for application errors. The error is in the JSON body. See `docs/misconceptions.md`.

### 2.3 XML-RPC

XML-RPC is the predecessor to JSON-RPC, using XML for serialisation.

#### Request Format

```xml
<methodCall>
    <methodName>add</methodName>
    <params>
        <param><value><int>10</int></value></param>
        <param><value><int>32</int></value></param>
    </params>
</methodCall>
```

#### Data Types

- `<int>`, `<i4>`: Integers
- `<double>`: Floats
- `<string>`: Strings
- `<boolean>`: 0 or 1
- `<array>`: Arrays
- `<struct>`: Key-value objects
- `<base64>`: Binary data
- `<dateTime.iso8601>`: Timestamps

#### Introspection Methods

- `system.listMethods`
- `system.methodSignature`
- `system.methodHelp`

### 2.4 gRPC with Protocol Buffers

gRPC is a high-performance RPC framework developed by Google.

#### Real-World Analogy (CPA: Concrete)

If JSON-RPC is like writing a letter in English (anyone can read it), Protocol Buffers is like using a secret code book:
- Both sender and receiver need the same code book (.proto file)
- Messages are much shorter (binary, not text)
- Only those with the code book can understand the message
- But it's much faster to transmit and decode

#### Characteristics

- Binary serialisation with Protocol Buffers
- HTTP/2 transport (multiplexing, header compression)
- Strong typing with `.proto` definitions
- Code generation for multiple languages
- Streaming support (unary, server, client, bidirectional)

#### Protocol Buffer Definition

```protobuf
syntax = "proto3";

message CalcRequest {
    double a = 1;
    double b = 2;
}

message CalcResponse {
    double result = 1;
}

service Calculator {
    rpc Add(CalcRequest) returns (CalcResponse);
}
```

#### gRPC Status Codes

| Code | Meaning |
|------|---------|
| OK | Success |
| CANCELLED | Operation cancelled |
| INVALID_ARGUMENT | Invalid input |
| NOT_FOUND | Resource not found |
| INTERNAL | Server error |
| UNAVAILABLE | Service unavailable |

---

## 3. Protocol Comparison

| Aspect | JSON-RPC | XML-RPC | gRPC |
|--------|----------|---------|------|
| Serialisation | JSON | XML | Protocol Buffers |
| Payload size | Small | Large | Smallest |
| Human readable | Yes | Yes | No |
| Type safety | Loose | Loose | Strong |
| Transport | Any (typically HTTP) | HTTP | HTTP/2 |
| Streaming | No | No | Yes |
| Code generation | Optional | No | Required |
| Browser support | Direct | Via library | Via grpc-web |

### Payload Size Comparison (add(10, 32))

```
JSON-RPC:  ~56 bytes   {"jsonrpc":"2.0","method":"add","params":[10,32],"id":1}
XML-RPC:   ~195 bytes  <?xml version="1.0"?><methodCall>...</methodCall>
gRPC:      ~18 bytes   [binary protobuf encoding]
```

---

## 4. Practical Considerations

### When to Use Each Protocol

**JSON-RPC:**
- Public APIs (human debugging)
- Browser-first applications
- Simple integrations
- Blockchain APIs (Bitcoin, Ethereum)

**XML-RPC:**
- Legacy system integration
- WordPress plugins
- Systems requiring introspection

**gRPC:**
- Internal microservices
- High-throughput systems
- Mobile backends (bandwidth efficiency)
- Real-time streaming applications

### Security Considerations

- SMTP: Use STARTTLS or SMTPS for encryption
- RPC: Use HTTPS/TLS for transport security
- Authentication: API keys, OAuth, mutual TLS
- Validate all inputs to prevent injection

---

## 5. Summary

1. **SMTP is push-only** — it sends email but cannot retrieve it
2. **RPC abstracts network calls** — making remote functions feel local
3. **JSON-RPC is transport agnostic** — it defines message format, not transport
4. **gRPC uses binary encoding** — not human-readable but very efficient
5. **Protocol choice depends on use case** — there's no universally "best" option

---

## 6. References

1. Postel, J. (1982). RFC 821: Simple Mail Transfer Protocol
2. Klensin, J. (2008). RFC 5321: Simple Mail Transfer Protocol
3. JSON-RPC 2.0 Specification. https://www.jsonrpc.org/specification
4. gRPC Documentation. https://grpc.io/docs/
5. Protocol Buffers Documentation. https://protobuf.dev/

---

## See Also

- `misconceptions.md` — Common errors explained
- `glossary.md` — Technical terminology
- `peer_instruction.md` — MCQ questions for self-assessment

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
