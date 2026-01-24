# ❌ Common Misconceptions — Week 10
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> HTTP/HTTPS, REST Architecture and Network Services

This document lists common misunderstandings about application layer protocols and how to correct them.

---

## HTTP/HTTPS Misconceptions

### 🚫 Misconception 1: "HTTPS encrypts the entire URL including the domain name"

**WRONG:** "When I use HTTPS, nobody can see which website I'm visiting."

**CORRECT:** HTTPS encrypts the URL path, query parameters, headers and body, but the domain name is visible through SNI (Server Name Indication) during the TLS handshake. The destination IP address is also visible.

| Aspect | Encrypted? | Visible to attacker? |
|--------|------------|---------------------|
| Domain name (via SNI) | No | Yes |
| URL path (`/accounts/123`) | Yes | No |
| Query parameters (`?id=5`) | Yes | No |
| HTTP headers | Yes | No |
| Request/response body | Yes | No |
| Destination IP address | N/A | Yes |

**Practical verification:**
```bash
# Capture TLS handshake in Wireshark
# Filter: ssl.handshake.extensions_server_name
# You'll see the domain in plaintext
```

**Why this matters:** Privacy-conscious users should know that their ISP or network admin can see which domains they visit, even with HTTPS.

---

### 🚫 Misconception 2: "HTTPS means the website is trustworthy and safe"

**WRONG:** "The padlock icon means this website won't steal my data."

**CORRECT:** HTTPS only provides encryption in transit and server authentication. It does NOT guarantee:
- The website operator is honest
- The website won't store your data insecurely
- The content is safe or accurate
- The website isn't a phishing site

**Key distinction:**
- HTTPS = "Your connection to this server is encrypted"
- HTTPS ≠ "This server is trustworthy"

**Real-world example:** Phishing sites routinely use HTTPS with valid certificates from Let's Encrypt.

---

### 🚫 Misconception 3: "HTTP/2 requires HTTPS"

**WRONG:** "HTTP/2 only works over TLS; you can't use HTTP/2 with plain HTTP."

**CORRECT:** The HTTP/2 specification (RFC 7540) supports both encrypted (h2) and unencrypted (h2c) modes. However, all major browsers only implement h2 over TLS. This is a browser policy decision, not a protocol requirement.

| Implementation | HTTP/2 over TLS | HTTP/2 cleartext |
|----------------|-----------------|------------------|
| Chrome, Firefox, Safari | ✅ Yes | ❌ No |
| curl, wget | ✅ Yes | ✅ Yes |
| nginx, Apache | ✅ Yes | ✅ Yes |

**Practical implication:** If you need HTTP/2 for browser clients, you must use HTTPS. Server-to-server communication can use h2c.

---

## REST Architecture Misconceptions

### 🚫 Misconception 4: "REST is a protocol"

**WRONG:** "We communicate using the REST protocol."

**CORRECT:** REST (Representational State Transfer) is an **architectural style**, not a protocol. It defines constraints for building distributed systems:

1. Client-Server separation
2. Statelessness
3. Cacheability
4. Uniform interface
5. Layered system
6. (Optional) Code on demand

REST typically uses HTTP as its transfer protocol, but REST itself is not a protocol — it's a set of design principles.

**Better phrasing:** "We have a RESTful API" or "Our API follows REST principles"

---

### 🚫 Misconception 5: "Any JSON API is RESTful"

**WRONG:** "Our API returns JSON, so it's a REST API."

**CORRECT:** Returning JSON has nothing to do with REST compliance. An API is RESTful based on how it uses:
- Resource-oriented URIs (`/users/123` not `/getUser?id=123`)
- HTTP verbs semantically (GET reads, POST creates, PUT updates, DELETE removes)
- Proper status codes (201 Created, 404 Not Found, etc.)
- (Level 3) Hypermedia links in responses

**Richardson Maturity Model:**
| Level | Characteristics | Example |
|-------|-----------------|---------|
| 0 | Single endpoint, RPC-style | `POST /api {"action": "getUser", "id": 123}` |
| 1 | Resource URIs | `POST /users/123/get` |
| 2 | HTTP verbs + status codes | `GET /users/123` → 200 OK |
| 3 | HATEOAS links | Response includes `"_links": {"self": "/users/123"}` |

---

### 🚫 Misconception 6: "PUT and POST are interchangeable"

**WRONG:** "I use POST for all create and update operations."

**CORRECT:** PUT and POST have different semantics:

| Verb | Idempotent? | Typical use | URI pattern |
|------|-------------|-------------|-------------|
| POST | No | Create new resource | `POST /users` |
| PUT | Yes | Replace/create at specific URI | `PUT /users/123` |
| PATCH | No | Partial update | `PATCH /users/123` |

**Idempotent** means calling the operation multiple times has the same effect as calling it once.

```bash
# POST creates a new user each time
curl -X POST /users -d '{"name": "Alice"}'  # Creates user 1
curl -X POST /users -d '{"name": "Alice"}'  # Creates user 2

# PUT at specific ID is idempotent
curl -X PUT /users/1 -d '{"name": "Alice"}'  # Creates/updates user 1
curl -X PUT /users/1 -d '{"name": "Alice"}'  # Same result
```

---

## DNS Misconceptions

### 🚫 Misconception 7: "DNS only uses UDP"

**WRONG:** "DNS is a UDP-based protocol on port 53."

**CORRECT:** DNS uses **both** UDP and TCP on port 53:

| Scenario | Transport | Reason |
|----------|-----------|--------|
| Standard queries (<512 bytes response) | UDP | Efficiency |
| Large responses (DNSSEC, many records) | TCP | Reliability |
| Zone transfers (AXFR/IXFR) | TCP | Reliability, size |
| When UDP response is truncated (TC bit) | Retry with TCP | Completeness |

**Practical verification:**
```bash
# Force TCP for DNS query
dig @8.8.8.8 google.com +tcp

# Compare with UDP (default)
dig @8.8.8.8 google.com +notcp
```

---

### 🚫 Misconception 8: "DNS caching improves privacy"

**WRONG:** "Using a local DNS cache protects my privacy."

**CORRECT:** DNS caching reduces the number of queries but does NOT improve privacy:
- Your queries still go to the upstream resolver initially
- Cached results reveal your browsing patterns if examined
- DNS queries are typically unencrypted (unless using DoH/DoT)

**What actually improves DNS privacy:**
- DNS over HTTPS (DoH)
- DNS over TLS (DoT)
- Using a privacy-focused resolver (Cloudflare 1.1.1.1, Quad9)

---

## SSH Misconceptions

### 🚫 Misconception 9: "SSH and SSL/TLS are the same thing"

**WRONG:** "SSH uses SSL for encryption."

**CORRECT:** SSH and SSL/TLS are **completely separate** protocols:

| Aspect | SSH | SSL/TLS |
|--------|-----|---------|
| Purpose | Remote shell, file transfer | General transport encryption |
| Port | 22 | 443 (HTTPS), varies |
| Authentication | Password, public key, etc. | Certificates |
| Protocol design | Integrated auth + encryption | Layered (handshake then data) |
| Key exchange | DH/ECDH built-in | Multiple methods |

They share cryptographic concepts but are different protocols with different designs.

---

### 🚫 Misconception 10: "SSH key authentication is less secure than passwords"

**WRONG:** "I prefer passwords because I can remember them."

**CORRECT:** SSH key authentication is significantly MORE secure:

| Aspect | Password | SSH Key |
|--------|----------|---------|
| Brute-force resistance | Low (dictionary attacks) | Extremely high (2048+ bits) |
| Phishing vulnerability | Yes | No (key never leaves client) |
| Network exposure | Transmitted to server | Only public key sent |
| Reuse risk | Often reused | Unique per key pair |

**Best practice:** Disable password authentication entirely once SSH keys are configured.

---

## FTP Misconceptions

### 🚫 Misconception 11: "FTP uses a single connection like HTTP"

**WRONG:** "FTP opens one connection to the server for everything."

**CORRECT:** FTP uses a **dual-channel architecture**:

```
┌─────────────────────────────────────────────────────────────────┐
│ Control Channel (port 21)                                       │
│ - Persistent connection                                         │
│ - Commands: USER, PASS, LIST, RETR, STOR, QUIT                 │
│ - Responses: 220, 230, 150, 226, 550, etc.                     │
├─────────────────────────────────────────────────────────────────┤
│ Data Channel (port 20 or high port)                            │
│ - Created per transfer                                          │
│ - Actual file data or directory listings                       │
│ - Closed after each transfer                                    │
└─────────────────────────────────────────────────────────────────┘
```

This separation allows monitoring transfer progress via the control channel.

---

### 🚫 Misconception 12: "Active and passive FTP modes are equivalent"

**WRONG:** "Active and passive mode are just different names for the same thing."

**CORRECT:** They have fundamentally different connection directions:

| Aspect | Active Mode | Passive Mode |
|--------|-------------|--------------|
| Data connection initiator | Server → Client | Client → Server |
| Client firewall issues | Yes (inbound blocked) | No |
| Server firewall issues | No | Yes (high ports needed) |
| NAT compatibility | Poor | Good |
| Modern preference | Rarely used | Standard |

**Why passive mode dominates:** Most clients are behind NAT/firewalls that block inbound connections, making active mode impractical.

```bash
# Using passive mode with ftp command
ftp -p server.example.com

# Explicit passive mode command
ftp> passive
Passive mode: on
```

---

## Quick Reference Card

| Topic | Wrong Assumption | Reality |
|-------|------------------|---------|
| HTTPS | Encrypts domain name | Domain visible via SNI |
| HTTPS | Guarantees site safety | Only encrypts connection |
| HTTP/2 | Requires HTTPS | Browsers enforce it, not spec |
| REST | Is a protocol | Is an architectural style |
| REST | JSON = RESTful | Verbs and resources matter |
| DNS | UDP only | TCP for large responses |
| SSH vs TLS | Same protocol | Completely different |
| FTP | Single connection | Control + data channels |

---

*Computer Networks — Week 10 | ASE, CSIE Bucharest*
*Common misconceptions compiled by ing. dr. Antonio Clim*
