# 📖 Glossary — Week 12: Email Protocols and RPC
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Email Protocol Terms

| Term | Definition | Example |
|------|------------|---------|
| **SMTP** | Simple Mail Transfer Protocol — a push protocol for sending email between servers and from clients to servers | `nc smtp.example.com 25` |
| **MTA** | Mail Transfer Agent — software that transfers email between servers (e.g., Postfix, Sendmail) | Postfix receiving mail on port 25 |
| **MUA** | Mail User Agent — email client software used by end users (e.g., Thunderbird, Outlook) | Thunderbird composing a message |
| **MDA** | Mail Delivery Agent — software that delivers email to the recipient's mailbox | Dovecot storing mail in Maildir |
| **Envelope** | The SMTP routing information (MAIL FROM, RCPT TO) separate from message headers | `MAIL FROM:<alice@a.com>` |
| **EHLO** | Extended HELO — SMTP greeting that enables extensions like TLS and authentication | `EHLO client.local` → 250-SIZE... |
| **HELO** | Original SMTP greeting from RFC 821, without extension support | `HELO client` → 250 OK |
| **STARTTLS** | SMTP extension to upgrade a plain connection to TLS encryption | `STARTTLS` → 220 Ready to start TLS |
| **POP3** | Post Office Protocol v3 — pull protocol for downloading email (port 110/995) | `USER alice` / `PASS secret` |
| **IMAP** | Internet Message Access Protocol — pull protocol with server-side mailbox management (port 143/993) | `SELECT INBOX` / `FETCH 1 BODY[]` |
| **Spool** | Directory where incoming mail is temporarily stored before delivery | `/var/spool/mail/` |
| **Relay** | Forwarding email through an intermediate server to its destination | Open relay (dangerous), authenticated relay |
| **Submission** | SMTP service for authenticated clients to submit outgoing mail (port 587) | Email client → smtp.gmail.com:587 |

---

## RPC Terms

| Term | Definition | Example |
|------|------------|---------|
| **RPC** | Remote Procedure Call — invoking a function on a remote server as if it were local | `calculator.add(10, 32)` over network |
| **Stub** | Generated code that handles marshalling/unmarshalling for RPC calls | Client stub serialises parameters |
| **Marshalling** | Converting in-memory data structures to a transmittable format | Python dict → JSON string |
| **Unmarshalling** | Converting received data back to in-memory structures | JSON string → Python dict |
| **Serialisation** | Encoding data for storage or transmission (synonym for marshalling) | `json.dumps({"a": 10})` |
| **Deserialisation** | Decoding received data (synonym for unmarshalling) | `json.loads('{"a": 10}')` |
| **JSON-RPC** | RPC protocol using JSON for serialisation, transport agnostic | `{"jsonrpc":"2.0","method":"add"...}` |
| **XML-RPC** | RPC protocol using XML for serialisation over HTTP | `<methodCall><methodName>add</methodName>...` |
| **gRPC** | Google's RPC framework using Protocol Buffers and HTTP/2 | `stub.Add(CalcRequest(a=10, b=32))` |
| **Protocol Buffers** | Google's binary serialisation format with schema definition (.proto files) | `message Request { double a = 1; }` |
| **IDL** | Interface Definition Language — formal specification of RPC interfaces | `.proto` file for gRPC |
| **Service** | Collection of RPC methods exposed by a server | `service Calculator { rpc Add(...) }` |

---

## JSON-RPC Specific

| Term | Definition | Example |
|------|------------|---------|
| **Request ID** | Client-generated identifier to match responses with requests | `"id": 42` |
| **Notification** | JSON-RPC request without an `id` field — no response expected | `{"jsonrpc":"2.0","method":"log","params":["msg"]}` |
| **Batch Request** | Array of JSON-RPC requests processed together | `[{...}, {...}, {...}]` |
| **Error Object** | Structured error response with code and message | `{"code": -32601, "message": "Method not found"}` |
| **Named Parameters** | Passing parameters as a JSON object with keys | `"params": {"a": 10, "b": 32}` |
| **Positional Parameters** | Passing parameters as a JSON array by position | `"params": [10, 32]` |

---

## gRPC Specific

| Term | Definition | Example |
|------|------------|---------|
| **Protobuf** | Short for Protocol Buffers | See Protocol Buffers |
| **Channel** | Connection to a gRPC server | `grpc.insecure_channel('localhost:6251')` |
| **Unary RPC** | Single request, single response | `Add(Request) returns (Response)` |
| **Server Streaming** | Single request, stream of responses | `ListItems(Query) returns (stream Item)` |
| **Client Streaming** | Stream of requests, single response | `UploadFile(stream Chunk) returns (Status)` |
| **Bidirectional Streaming** | Stream of requests and responses | `Chat(stream Msg) returns (stream Msg)` |
| **Wire Type** | Protobuf encoding type (varint, fixed64, length-delimited, etc.) | Field with wire type 0 = varint |
| **Field Tag** | Numeric identifier for a protobuf field | `double a = 1;` — tag is 1 |

---

## HTTP/Transport Terms

| Term | Definition | Example |
|------|------------|---------|
| **HTTP/2** | Modern HTTP protocol with multiplexing, used by gRPC | Single connection, multiple streams |
| **Multiplexing** | Multiple requests/responses over a single connection simultaneously | gRPC streams over HTTP/2 |
| **Content-Type** | HTTP header specifying the format of the request/response body | `application/json`, `text/xml` |
| **TLS** | Transport Layer Security — encryption for network connections | HTTPS, SMTPS, IMAPS |

---

## Response Codes

### SMTP Response Codes

| Code | Class | Meaning |
|------|-------|---------|
| 220 | 2xx | Service ready (greeting) |
| 221 | 2xx | Service closing (goodbye) |
| 250 | 2xx | Requested action OK |
| 354 | 3xx | Start mail input (DATA accepted) |
| 421 | 4xx | Service unavailable (temporary) |
| 450 | 4xx | Mailbox unavailable (temporary) |
| 500 | 5xx | Syntax error, command unrecognised |
| 550 | 5xx | Mailbox unavailable (permanent) |
| 554 | 5xx | Transaction failed |

### JSON-RPC Error Codes

| Code | Meaning |
|------|---------|
| -32700 | Parse error (invalid JSON) |
| -32600 | Invalid request (missing required fields) |
| -32601 | Method not found |
| -32602 | Invalid params |
| -32603 | Internal error |
| -32000 to -32099 | Server-defined errors |

### gRPC Status Codes

| Code | Name | Meaning |
|------|------|---------|
| 0 | OK | Success |
| 1 | CANCELLED | Operation cancelled by client |
| 2 | UNKNOWN | Unknown error |
| 3 | INVALID_ARGUMENT | Invalid input parameters |
| 5 | NOT_FOUND | Resource not found |
| 13 | INTERNAL | Internal server error |
| 14 | UNAVAILABLE | Service unavailable |

---

## Acronyms

| Acronym | Full Form | Context |
|---------|-----------|---------|
| SMTP | Simple Mail Transfer Protocol | Email sending |
| POP3 | Post Office Protocol version 3 | Email retrieval |
| IMAP | Internet Message Access Protocol | Email retrieval with sync |
| MTA | Mail Transfer Agent | Server software |
| MUA | Mail User Agent | Client software |
| MDA | Mail Delivery Agent | Local delivery |
| RPC | Remote Procedure Call | Distributed computing |
| gRPC | gRPC Remote Procedure Call | Google's RPC framework |
| IDL | Interface Definition Language | Service definition |
| TLS | Transport Layer Security | Encryption |
| HTTP | Hypertext Transfer Protocol | Web transport |

---

## Relationships Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           EMAIL FLOW                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [MUA]  ──SMTP──▶  [MTA]  ──SMTP──▶  [MTA]  ──▶  [MDA]  ──▶  [Mailbox]   │
│  (Client)         (Sender's          (Recipient's)    (Delivery)           │
│                    Server)            Server)                               │
│                                                                             │
│   [MUA]  ◀──IMAP/POP3──  [Mailbox]                                         │
│  (Client)                (Retrieval)                                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           RPC ARCHITECTURE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [Client App]                              [Server App]                    │
│        │                                          │                         │
│        ▼                                          ▼                         │
│   [Client Stub]  ──── Serialise ────▶  [Server Stub]                       │
│        │              (Marshal)               │                             │
│        ▼                                      ▼                             │
│   [Transport]   ════ Network ════▶    [Transport]                          │
│   (HTTP/TCP)         (bytes)          (HTTP/TCP)                           │
│                                               │                             │
│   [Client Stub]  ◀─── Deserialise ────  [Server Stub]                      │
│        │              (Unmarshal)             │                             │
│        ▼                                      ▼                             │
│   [Client App]                          [Server App]                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        SERIALISATION FORMATS                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   JSON-RPC:     {"method": "add", "params": [10, 32]}     (text, ~50 bytes)│
│                                                                             │
│   XML-RPC:      <methodCall><methodName>add</methodName>  (text, ~200 bytes)│
│                   <params>...</params></methodCall>                         │
│                                                                             │
│   Protocol      [binary: field tags + values]             (binary, ~20 bytes)│
│   Buffers:      0x09 0x00 0x00 0x00 0x00 0x00 0x24 0x40...                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## See Also

- `theory_summary.md` — Detailed protocol explanations
- `misconceptions.md` — Common errors and corrections
- `commands_cheatsheet.md` — Quick reference for commands

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
