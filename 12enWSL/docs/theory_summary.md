# Week 12 Theory Summary: Email Protocols and RPC

> NETWORKING class - ASE, Informatics | by Revolvix

## 1. Email Protocols

### 1.1 SMTP (Simple Mail Transfer Protocol)

SMTP is a **push protocol** used for sending email between mail servers and from clients to servers. It operates at the **Application Layer** (Layer 7) of the OSI model.

**Key Characteristics:**
- Text-based protocol over TCP (port 25, 587 for submission, 465 for SMTPS)
- Stateful connection with command-response dialogue
- Commands are 4-letter ASCII words followed by parameters
- Response codes: 2xx success, 3xx intermediate, 4xx temporary failure, 5xx permanent failure

**SMTP Commands:**
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

**Mail Transaction Phases:**
1. **Connection**: TCP handshake + 220 greeting
2. **Envelope**: MAIL FROM + RCPT TO define routing
3. **Data**: Headers + blank line + body + terminating dot
4. **Commitment**: Server accepts responsibility for delivery

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

### 2.1 The RPC Paradigm

RPC abstracts network communication, allowing remote function calls with local call syntax.

**Architecture:**
```
Client                              Server
┌─────────┐                        ┌─────────┐
│  App    │ ──call()──▶ │ Stub │ ──serialise──▶ │Network│
│         │ ◀─return─── │      │ ◀─deserialise── │       │
└─────────┘                        └─────────┘
```

**Components:**
- **Client Stub**: Marshalls parameters, sends request, unmarshalls response
- **Server Stub**: Unmarshalls request, invokes method, marshalls response
- **Transport**: TCP, HTTP, HTTP/2
- **Serialisation**: JSON, XML, Protocol Buffers

### 2.2 JSON-RPC 2.0

**Specification:** https://www.jsonrpc.org/specification

**Request Format:**
```json
{
    "jsonrpc": "2.0",
    "method": "method_name",
    "params": [arg1, arg2] or {"key": "value"},
    "id": 1
}
```

**Response Format:**
```json
{"jsonrpc": "2.0", "result": value, "id": 1}
```

**Error Response:**
```json
{"jsonrpc": "2.0", "error": {"code": -32601, "message": "..."}, "id": 1}
```

**Standard Error Codes:**
| Code | Meaning |
|------|---------|
| -32700 | Parse error |
| -32600 | Invalid request |
| -32601 | Method not found |
| -32602 | Invalid params |
| -32603 | Internal error |
| -32000 to -32099 | Server errors |

**Features:**
- Batch requests (array of requests)
- Notifications (no `id` → no response)
- Transport agnostic

### 2.3 XML-RPC

XML-RPC is the predecessor to JSON-RPC, using XML for serialisation.

**Request Format:**
```xml
<methodCall>
    <methodName>add</methodName>
    <params>
        <param><value><int>10</int></value></param>
        <param><value><int>32</int></value></param>
    </params>
</methodCall>
```

**Data Types:**
- `<int>`, `<i4>`: Integers
- `<double>`: Floats
- `<string>`: Strings
- `<boolean>`: 0 or 1
- `<array>`: Arrays
- `<struct>`: Key-value objects
- `<base64>`: Binary data
- `<dateTime.iso8601>`: Timestamps

**Introspection Methods:**
- `system.listMethods`
- `system.methodSignature`
- `system.methodHelp`

### 2.4 gRPC with Protocol Buffers

gRPC is a high-performance RPC framework developed by Google.

**Characteristics:**
- Binary serialisation with Protocol Buffers
- HTTP/2 transport (multiplexing, header compression)
- Strong typing with `.proto` definitions
- Code generation for multiple languages
- Streaming support (unary, server, client, bidirectional)

**Protocol Buffer Definition:**
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

**gRPC Status Codes:**
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
| Transport | Any (HTTP) | HTTP | HTTP/2 |
| Streaming | No | No | Yes |
| Code generation | Optional | No | Required |
| Browser support | Direct | Via library | Via grpc-web |

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

## 5. References

1. Postel, J. (1982). RFC 821: Simple Mail Transfer Protocol
2. Klensin, J. (2008). RFC 5321: Simple Mail Transfer Protocol
3. JSON-RPC 2.0 Specification. https://www.jsonrpc.org/specification
4. gRPC Documentation. https://grpc.io/docs/
5. Protocol Buffers Documentation. https://protobuf.dev/

---

*NETWORKING class - ASE, Informatics | by Revolvix*
