# Week 10 Theory Summary

> NETWORKING class - ASE, Informatics | by Revolvix

## Application Layer Overview

The application layer sits at the top of the TCP/IP protocol stack, providing network services directly to end-user applications. This week examines key application-layer protocols that form the backbone of internet communication.

## HTTP/HTTPS

### HTTP Fundamentals

HTTP (Hypertext Transfer Protocol) operates as a request-response protocol using TCP as its transport layer. Key characteristics include:

- **Statelessness**: Each request-response pair is independent
- **Text-based**: Headers and much content are human-readable
- **Methods**: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
- **Status codes**: 1xx (informational), 2xx (success), 3xx (redirection), 4xx (client error), 5xx (server error)

### HTTPS and TLS

HTTPS wraps HTTP within TLS (Transport Layer Security), providing:

1. **Authentication**: Server identity verified through X.509 certificates
2. **Confidentiality**: Symmetric encryption protects data
3. **Integrity**: MACs (Message Authentication Codes) detect tampering

The TLS handshake:
1. Client Hello (supported cipher suites)
2. Server Hello (chosen cipher suite + certificate)
3. Key exchange (asymmetric → symmetric key derivation)
4. Encrypted application data begins

### HTTP/2 and HTTP/3

- HTTP/2: Binary framing, multiplexing, header compression, server push
- HTTP/3: QUIC-based (UDP), reduced connection establishment latency

## REST Architecture

### Principles

REST (Representational State Transfer) is an architectural style with these constraints:

1. **Client-Server**: Separation of concerns
2. **Stateless**: No session state on server
3. **Cacheable**: Responses indicate cacheability
4. **Uniform Interface**: Consistent resource addressing
5. **Layered System**: Intermediaries are transparent

### Richardson Maturity Model

- **Level 0**: HTTP as transport tunnel for RPC
- **Level 1**: Resources with distinct URIs
- **Level 2**: HTTP verbs used semantically
- **Level 3**: HATEOAS (Hypermedia as Engine of Application State)

### REST vs SOAP

| Aspect | REST | SOAP |
|--------|------|------|
| Protocol | HTTP (typically) | HTTP, SMTP, etc. |
| Format | JSON, XML, etc. | XML only |
| State | Stateless | Can be stateful |
| Complexity | Simpler | More complex |
| Standards | Loose | WS-* specifications |

## DNS (Domain Name System)

### Purpose

Translates human-readable domain names to IP addresses.

### Message Format

- Header: ID, flags (QR, opcode, RCODE), counts
- Question section: Query name, type, class
- Answer section: Resource records (name, type, class, TTL, data)

### Record Types

- **A**: IPv4 address
- **AAAA**: IPv6 address
- **CNAME**: Canonical name (alias)
- **MX**: Mail exchanger
- **NS**: Name server
- **TXT**: Arbitrary text

### Transport

- Typically UDP port 53 (queries < 512 bytes)
- TCP port 53 for zone transfers and large responses
- DNS over HTTPS (DoH) and DNS over TLS (DoT) for privacy

## SSH (Secure Shell)

### Purpose

Secure remote access and command execution.

### Protocol Layers

1. **Transport Layer**: Server authentication, encryption, integrity
2. **User Authentication Layer**: Password, public key, etc.
3. **Connection Layer**: Multiplexed channels (shell, X11, port forwarding)

### Key Exchange

SSH uses Diffie-Hellman or ECDH for key agreement, then symmetric encryption (AES, ChaCha20) for data.

## FTP (File Transfer Protocol)

### Architecture

FTP uses separate connections:
- **Control connection**: Port 21, commands and responses
- **Data connection**: Varies, actual file transfers

### Active vs Passive Mode

- **Active**: Server connects to client (port 20 → client port)
- **Passive**: Client connects to server (client → server high port)

Passive mode preferred with NAT/firewalls.

### Commands

- USER, PASS: Authentication
- LIST, NLST: Directory listing
- RETR, STOR: Download, upload
- CWD, PWD: Change/print directory
- TYPE: Transfer mode (ASCII, Binary)

## Key Takeaways

1. HTTP is the foundation of web communication; HTTPS adds essential security
2. REST provides architectural guidelines for scalable APIs
3. DNS is critical infrastructure, primarily using UDP
4. SSH provides secure remote access through encryption
5. FTP demonstrates multi-channel protocol design

---

*NETWORKING class - ASE, Informatics | by Revolvix*
