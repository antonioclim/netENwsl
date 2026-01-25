# Week 10 Theory Summary
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> HTTP/HTTPS, REST Architecture and Network Services

---

## Application Layer Overview

The application layer sits at the top of the TCP/IP protocol stack, providing network services directly to end-user applications. This week examines key application-layer protocols that underpin modern internet communication.

### 🏠 Concrete Analogy: Postal Service Levels

Think of the network stack like a postal service:
- **Application Layer** = The letter content and format (what you write)
- **Transport Layer** = The envelope type (registered mail vs postcard)
- **Network Layer** = The postal routing system (sorting centres)
- **Link Layer** = The actual mail trucks and routes

---

## HTTP/HTTPS

### HTTP Fundamentals

HTTP (Hypertext Transfer Protocol) operates as a request-response protocol using TCP as its transport layer.

#### 🏠 Concrete Analogy: Restaurant Orders

HTTP is like ordering at a restaurant:
- **Request** = Your order (what you want)
- **Response** = The dish delivered (what you get)
- **Stateless** = The waiter doesn't remember your previous visits
- **Methods** = Different types of requests (order, cancel, modify)

Key characteristics:
- **Statelessness**: Each request-response pair is independent
- **Text-based**: Headers and much content are human-readable
- **Methods**: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
- **Status codes**: 1xx (informational), 2xx (success), 3xx (redirection), 4xx (client error), 5xx (server error)

> ⚠️ **Common Misconception:** "HTTP methods are interchangeable." Reality: Each method has specific semantics. GET is safe and idempotent; POST is neither. Using POST for everything violates REST principles.

### HTTPS and TLS

HTTPS wraps HTTP within TLS (Transport Layer Security), providing:

1. **Authentication**: Server identity verified through X.509 certificates
2. **Confidentiality**: Symmetric encryption protects data
3. **Integrity**: MACs (Message Authentication Codes) detect tampering

#### 🏠 Concrete Analogy: Sealed Envelope with ID Check

HTTPS is like sending a letter where:
- The **envelope is sealed** (encryption — nobody can read the contents)
- The recipient **shows ID** (authentication — you know who you're talking to)
- The seal **shows if tampered** (integrity — you know if someone modified it)

The TLS handshake:
1. Client Hello (supported cipher suites)
2. Server Hello (chosen cipher suite + certificate)
3. Key exchange (asymmetric → symmetric key derivation)
4. Encrypted application data begins

> 💡 **From teaching experience:** Students often struggle to understand why the domain name is visible even with HTTPS. The key insight is that TLS negotiation happens *before* encryption is established — and the server needs to know which certificate to present.

> ⚠️ **Common Misconception:** "HTTPS encrypts everything." Reality: The domain name is visible via SNI (Server Name Indication). The URL path is encrypted, but the destination domain is not.

> ⚠️ **Common Misconception:** "HTTPS means the site is safe." Reality: HTTPS only encrypts the connection. A phishing site can have valid HTTPS.

### HTTP/2 and HTTP/3

- **HTTP/2**: Binary framing, multiplexing, header compression, server push
- **HTTP/3**: QUIC-based (UDP), reduced connection establishment latency

> ⚠️ **Common Misconception:** "HTTP/2 requires HTTPS." Reality: The spec allows cleartext HTTP/2, but browsers only implement it over TLS.

---

## REST Architecture

### Principles

REST (Representational State Transfer) is an **architectural style** (not a protocol) with these constraints:

1. **Client-Server**: Separation of concerns
2. **Stateless**: No session state on server
3. **Cacheable**: Responses indicate cacheability
4. **Uniform Interface**: Consistent resource addressing
5. **Layered System**: Intermediaries are transparent

#### 🏠 Concrete Analogy: Library System

REST is like a well-organised library:
- **Resources** = Books (each has a unique call number/URI)
- **Representations** = The book content (JSON, XML, HTML)
- **Uniform Interface** = Standard operations (borrow, return, renew)
- **Stateless** = The librarian doesn't remember your previous visits

> ⚠️ **Common Misconception:** "REST is a protocol." Reality: REST is a set of architectural constraints. It typically uses HTTP, but REST itself is not a protocol.

> ⚠️ **Common Misconception:** "Any JSON API is RESTful." Reality: REST is about resource-oriented URIs and proper HTTP verb usage, not data format.

### Richardson Maturity Model

| Level | Name | Characteristics |
|-------|------|-----------------|
| **Level 0** | The Swamp of POX | HTTP as transport tunnel for RPC |
| **Level 1** | Resources | Resources with distinct URIs |
| **Level 2** | HTTP Verbs | HTTP verbs used semantically |
| **Level 3** | Hypermedia | HATEOAS (Hypermedia as Engine of Application State) |

> 💡 **In previous years, students often confused Level 1 and Level 2.** The key difference: Level 1 has resource URIs but may still use verbs in the URL (`/users/123/delete`). Level 2 uses HTTP verbs semantically (`DELETE /users/123`).

#### Level Comparison Example

| Operation | Level 0 | Level 1 | Level 2 | Level 3 |
|-----------|---------|---------|---------|---------|
| List users | `POST /api {"action": "list"}` | `GET /users/list` | `GET /users` | `GET /users` + links |
| Get user | `POST /api {"action": "get", "id": 1}` | `GET /users/1/get` | `GET /users/1` | `GET /users/1` + links |
| Create user | `POST /api {"action": "create", ...}` | `POST /users/create` | `POST /users` | `POST /users` + links |

---

## DNS (Domain Name System)

### Purpose

Translates human-readable domain names to IP addresses.

#### 🏠 Concrete Analogy: Phone Directory

DNS is like a phone book:
- **Domain name** = Person's name ("John Smith")
- **IP address** = Phone number (192.168.1.1)
- **DNS server** = The phone book itself
- **Caching** = Writing frequently-used numbers on a sticky note

### Message Format

- **Header**: ID, flags (QR, opcode, RCODE), counts
- **Question section**: Query name, type, class
- **Answer section**: Resource records (name, type, class, TTL, data)

### Record Types

| Type | Purpose | Example |
|------|---------|---------|
| **A** | IPv4 address | `example.com → 93.184.216.34` |
| **AAAA** | IPv6 address | `example.com → 2606:2800:...` |
| **CNAME** | Canonical name (alias) | `www → example.com` |
| **MX** | Mail exchanger | `mail.example.com` |
| **NS** | Name server | `ns1.example.com` |
| **TXT** | Arbitrary text | SPF, DKIM records |

### Transport

- Typically UDP port 53 (queries < 512 bytes)
- TCP port 53 for zone transfers and large responses
- DNS over HTTPS (DoH) and DNS over TLS (DoT) for privacy

> 💡 **This usually trips students up during packet captures:** If you see DNS over TCP, it's not an error — it means the response was too large for UDP, or it's a zone transfer.

> ⚠️ **Common Misconception:** "DNS only uses UDP." Reality: DNS uses TCP for large responses (when UDP response is truncated) and for zone transfers.

---

## SSH (Secure Shell)

### Purpose

Secure remote access and command execution.

#### 🏠 Concrete Analogy: Secure Phone Line

SSH is like a secure phone call:
- **Encryption** = Scrambled voice that only you and the recipient understand
- **Authentication** = Verifying who's on the other end
- **Port forwarding** = Conference calling through the secure line

### Protocol Layers

1. **Transport Layer**: Server authentication, encryption, integrity
2. **User Authentication Layer**: Password, public key, etc.
3. **Connection Layer**: Multiplexed channels (shell, X11, port forwarding)

### Key Exchange

SSH uses Diffie-Hellman or ECDH for key agreement, then symmetric encryption (AES, ChaCha20) for data.

> ⚠️ **Common Misconception:** "SSH and SSL/TLS are the same." Reality: They are completely different protocols that happen to use similar cryptographic concepts.

> ⚠️ **Common Misconception:** "Password authentication is as secure as key authentication." Reality: SSH keys (2048+ bits) are far more resistant to brute-force attacks than passwords.

---

## FTP (File Transfer Protocol)

### Architecture

FTP uses **separate connections**:
- **Control connection**: Port 21, commands and responses
- **Data connection**: Varies, actual file transfers

#### 🏠 Concrete Analogy: Phone Order with Delivery

FTP is like ordering by phone:
- **Control channel** = The phone call (you discuss what to order)
- **Data channel** = The delivery truck (the actual goods arrive separately)
- **Two connections** = You stay on the phone while the truck delivers

### Active vs Passive Mode

| Aspect | Active Mode | Passive Mode |
|--------|-------------|--------------|
| **Data connection initiator** | Server → Client | Client → Server |
| **Client behind NAT** | Problems | Works fine |
| **Modern preference** | Rarely used | Standard |

> 💡 **If this feels confusing at first,** focus on who initiates the data connection. In active mode, the server calls back to the client (which fails if the client is behind NAT). In passive mode, the client calls the server (which almost always works).

> ⚠️ **Common Misconception:** "FTP uses a single connection like HTTP." Reality: FTP uses separate control and data channels, which is why firewall configuration can be tricky.

Passive mode is preferred because most clients are behind NAT/firewalls that block inbound connections.

### Commands

| Command | Purpose |
|---------|---------|
| USER, PASS | Authentication |
| LIST, NLST | Directory listing |
| RETR, STOR | Download, upload |
| CWD, PWD | Change/print directory |
| TYPE | Transfer mode (ASCII, Binary) |
| PASV | Enter passive mode |

---

## Key Takeaways

1. **HTTP** underpins web communication; **HTTPS** adds essential security through TLS
2. **REST** provides architectural guidelines for building APIs (not a protocol)
3. **DNS** is critical infrastructure, using primarily UDP but also TCP
4. **SSH** provides secure remote access through encryption and authentication
5. **FTP** demonstrates multi-channel protocol design (control + data)

---

## Quick Reference: Protocol Summary

| Protocol | Port(s) | Transport | Purpose |
|----------|---------|-----------|---------|
| HTTP | 80 | TCP | Web content |
| HTTPS | 443 | TCP + TLS | Secure web content |
| DNS | 53 | UDP/TCP | Name resolution |
| SSH | 22 | TCP | Secure remote access |
| FTP | 21, 20+ | TCP | File transfer |

---

## See Also

- [Concept Analogies](concept_analogies.md) — Extended everyday analogies
- [Misconceptions](misconceptions.md) — Common errors and how to avoid them
- [Peer Instruction Questions](peer_instruction.md) — Test your understanding

---

*Computer Networks — Week 10 | ASE, CSIE Bucharest*
*Theory summary by ing. dr. Antonio Clim*
