# 🎯 Concept Analogies — Week 10: Application Layer Protocols
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Understanding through everyday analogies before technical details.
> Based on the Concrete-Pictorial-Abstract (CPA) method from Singapore Mathematics.

---

## How to Use This Document

Each concept follows the **CPA progression**:

1. **🏠 Concrete** — A real-world analogy you already understand
2. **🖼️ Pictorial** — A visual representation bridging analogy and reality
3. **💻 Abstract** — The technical implementation
4. **⚠️ Limitations** — Where the analogy breaks down

> 💡 **Teaching tip:** Always introduce the concrete analogy *before* showing any code or commands.

---

## 1. HTTPS/TLS: The Sealed Envelope with ID Check

### 🏠 Real-World Analogy

Imagine sending a letter to your bank:

| Analogy Component | Network Equivalent |
|-------------------|-------------------|
| **Writing the letter** | Your HTTP request (GET /accounts) |
| **Sealing the envelope** | TLS encryption |
| **Bank's official letterhead** | Server's TLS certificate |
| **Wax seal** | Message integrity (MAC) |
| **Address on envelope** | Domain name (visible via SNI!) |
| **Postal worker sees address** | ISP/network sees destination |
| **Only bank can open** | Only server has private key |

**Key insight:** The postal worker (network) can see *where* the letter goes, but not *what's inside*. Similarly, HTTPS hides content but not destination.

### 🖼️ Visual Representation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          HTTPS CONNECTION                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  VISIBLE TO ATTACKERS              │  HIDDEN FROM ATTACKERS                 │
│  ════════════════════              │  ══════════════════════                │
│                                    │                                        │
│  • Destination IP: 93.184.216.34   │  • URL path: /accounts/12345          │
│  • Domain (SNI): bank.example.com  │  • Query params: ?balance=true        │
│  • Port: 443                       │  • HTTP headers: Cookie, Auth         │
│  • Time of connection              │  • Request/response body              │
│  • Size of encrypted data          │  • HTTP method: GET, POST, etc.       │
│                                    │                                        │
│  ┌──────────────────────┐          │  ┌──────────────────────────────────┐ │
│  │ ✉️ To: bank.example  │          │  │ 🔒 Dear Bank,                    │ │
│  │    (readable)        │          │  │    Please show my balance...     │ │
│  └──────────────────────┘          │  │    (encrypted - unreadable)      │ │
│                                    │  └──────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 💻 Technical Reality

```python
# The TLS handshake (simplified)
# 1. Client sends SNI (plaintext): "I want to talk to bank.example.com"
# 2. Server sends certificate (plaintext): "Here's proof I'm bank.example.com"
# 3. Key exchange happens (Diffie-Hellman or similar)
# 4. Symmetric key derived → all further traffic encrypted

import ssl
import socket

context = ssl.create_default_context()
sock = socket.create_connection(("bank.example.com", 443))
secure_sock = context.wrap_socket(sock, server_hostname="bank.example.com")
#                                       ^^^^^^^^^^^^^^^^
#                                       This is SNI - sent in plaintext!
```

### ⚠️ Where the Analogy Breaks Down

| Analogy Says | Reality Is |
|--------------|------------|
| One letter = one transaction | TLS connection carries multiple HTTP requests |
| Envelope sealing is instant | TLS handshake takes time (RTT latency) |
| Bank verifies your identity | Basic HTTPS only verifies *server*, not client |
| Postal worker is neutral | Network could be actively hostile (MITM) |

---

## 2. REST Maturity Levels: Restaurant Service Quality

### 🏠 Real-World Analogy

Think of REST maturity levels as restaurant service quality:

| Level | Restaurant Equivalent | API Equivalent |
|-------|----------------------|----------------|
| **Level 0** | Fast food counter: "I want a Big Mac meal" (one request type) | `POST /api {"action": "getUser", "id": 123}` |
| **Level 1** | Counter with sections: "I want something from the burger section" | `POST /api/users/123 {"action": "get"}` |
| **Level 2** | Proper restaurant: "Menu please" (GET), "I'll order" (POST), "Cancel that" (DELETE) | `GET /api/users/123`, `DELETE /api/users/123` |
| **Level 3** | Waiter suggests: "For dessert, may I recommend..." (hypermedia) | Response includes links to related resources |

### 🖼️ Visual Representation

```
═══════════════════════════════════════════════════════════════════════════════
                     RICHARDSON MATURITY MODEL
═══════════════════════════════════════════════════════════════════════════════

Level 0: THE SWAMP OF POX (Plain Old XML/JSON)
┌─────────────────────────────────────────────────────────────────────────────┐
│  Client: POST /api                                                          │
│          {"action": "getUserById", "userId": 123}                           │
│                                                                              │
│  → One endpoint, actions in body, HTTP is just a tunnel                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
Level 1: RESOURCES (URIs identify things)
┌─────────────────────────────────────────────────────────────────────────────┐
│  Client: POST /api/users/123/getDetails                                     │
│          {}                                                                  │
│                                                                              │
│  → Resources in URL, but actions still in URL path                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
Level 2: HTTP VERBS (proper semantics)
┌─────────────────────────────────────────────────────────────────────────────┐
│  Client: GET /api/users/123                                                 │
│                                                                              │
│  → Verb indicates action, URL is just the resource                          │
│  → GET = read, POST = create, PUT = update, DELETE = remove                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
Level 3: HYPERMEDIA (HATEOAS)
┌─────────────────────────────────────────────────────────────────────────────┐
│  Response: {                                                                │
│    "id": 123,                                                               │
│    "name": "Alice",                                                         │
│    "_links": {                                                              │
│      "self": "/api/users/123",                                              │
│      "orders": "/api/users/123/orders",    ← Server tells you what's next  │
│      "delete": "/api/users/123"                                             │
│    }                                                                        │
│  }                                                                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 💻 Technical Reality

```python
# Level 0: RPC-style
requests.post("/api/service", json={"method": "getUser", "params": {"id": 123}})

# Level 1: Resources, but wrong verbs
requests.post("/api/users/123/fetch")

# Level 2: Proper REST
requests.get("/api/users/123")
requests.put("/api/users/123", json={"name": "Alice Updated"})
requests.delete("/api/users/123")

# Level 3: HATEOAS - follow links from responses
user = requests.get("/api/users/123").json()
orders_url = user["_links"]["orders"]  # Don't hardcode URLs!
orders = requests.get(orders_url).json()
```

### ⚠️ Where the Analogy Breaks Down

| Analogy Says | Reality Is |
|--------------|------------|
| Higher level = better | Level 2 is often sufficient; Level 3 adds complexity |
| Levels are strict | Many APIs mix levels (pragmatic approach) |
| Waiter always knows best | HATEOAS requires careful API design |

---

## 3. DNS: The Phone Directory of the Internet

### 🏠 Real-World Analogy

DNS is like a phone directory system:

| Analogy Component | DNS Equivalent |
|-------------------|----------------|
| **Phone book** | DNS zone file |
| **Name → Number lookup** | Domain → IP resolution |
| **Directory assistance operator** | DNS resolver |
| **Your personal contacts app** | DNS cache |
| **"The number has changed"** | TTL (Time To Live) expiry |
| **Business with multiple lines** | Multiple A records (load balancing) |
| **Call forwarding** | CNAME record |

**Key insight:** You don't memorise phone numbers; you look them up. Similarly, you don't memorise IP addresses; DNS looks them up.

### 🖼️ Visual Representation

```
═══════════════════════════════════════════════════════════════════════════════
                         DNS RESOLUTION PROCESS
═══════════════════════════════════════════════════════════════════════════════

You type: www.example.com
                │
                ▼
        ┌───────────────┐
        │ Your Computer │  "Do I know this number?"
        │   (Cache)     │  
        └───────┬───────┘
         miss   │
                ▼
        ┌───────────────┐
        │ Home Router   │  "Is it in my cache?"
        │   (Cache)     │
        └───────┬───────┘
         miss   │
                ▼
        ┌───────────────┐
        │ ISP Resolver  │  "Let me ask around..."
        │  (Recursive)  │
        └───────┬───────┘
                │
    ┌───────────┼───────────┐
    ▼           ▼           ▼
┌───────┐  ┌─────────┐  ┌─────────────┐
│ Root  │→│  .com   │→│ example.com │
│ (.)   │  │  TLD   │  │Authoritative│
└───────┘  └─────────┘  └─────────────┘
                              │
                              ▼
                        93.184.216.34
                              │
                              ▼
                    ┌───────────────────┐
                    │ Cached for 3600s  │
                    │ (TTL = 1 hour)    │
                    └───────────────────┘
```

### 💻 Technical Reality

```bash
# Query the lab DNS server
dig @127.0.0.1 -p 5353 web.lab.local

# See the full resolution path
dig +trace example.com

# Force TCP (for large responses)
dig +tcp example.com

# Query specific record types
dig MX example.com     # Mail servers
dig TXT example.com    # Text records (SPF, DKIM, etc.)
dig AAAA example.com   # IPv6 address
```

```python
import dns.resolver

# Simple lookup
answers = dns.resolver.resolve('web.lab.local', 'A')
for rdata in answers:
    print(f"IP: {rdata.address}")
```

### ⚠️ Where the Analogy Breaks Down

| Analogy Says | Reality Is |
|--------------|------------|
| One name = one number | One domain can have multiple IPs (load balancing) |
| Phone book is authoritative | DNS has hierarchy (root → TLD → domain) |
| Lookup is instant | DNS resolution adds latency (why caching matters) |
| Directory is trusted | DNS can be spoofed (DNSSEC adds security) |

---

## 4. SSH: The Secure Private Tunnel

### 🏠 Real-World Analogy

SSH is like a secure, private tunnel to a building:

| Analogy Component | SSH Equivalent |
|-------------------|----------------|
| **Building entrance** | SSH server (port 22) |
| **Security guard checks ID** | Host key verification |
| **You show your badge** | Client authentication (key/password) |
| **Private office inside** | Shell session |
| **Soundproof walls** | Encryption |
| **Tunnel to another building** | SSH port forwarding |

**Key insight:** SSH creates a secure "tunnel" where everything you do is private, even on an untrusted network.

### 🖼️ Visual Representation

```
═══════════════════════════════════════════════════════════════════════════════
                           SSH CONNECTION
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────┐                              ┌─────────────────┐
│   Your Laptop   │                              │   SSH Server    │
│                 │                              │                 │
│  ┌───────────┐  │    ═══════════════════════   │  ┌───────────┐  │
│  │  Terminal │  │    ║ Encrypted Tunnel  ║   │  │   Shell   │  │
│  │           │──┼────║   (AES-256-GCM)   ║───┼──│           │  │
│  │  $ ssh    │  │    ║                   ║   │  │  bash/zsh │  │
│  └───────────┘  │    ═══════════════════════   │  └───────────┘  │
│                 │                              │                 │
│  🔑 Private Key │                              │ 🔑 Host Key     │
│  (proves you)   │                              │ (proves server) │
└─────────────────┘                              └─────────────────┘

                    ┌─────────────────────────┐
                    │   What ISP/WiFi sees:   │
                    │   • Encrypted blob      │
                    │   • Destination IP      │
                    │   • Port 22             │
                    │   • NOT your commands   │
                    │   • NOT file contents   │
                    └─────────────────────────┘
```

### 💻 Technical Reality

```bash
# Basic SSH connection
ssh labuser@localhost -p 2222

# SSH with key authentication (more secure)
ssh -i ~/.ssh/lab_key labuser@localhost -p 2222

# Port forwarding: access remote service locally
ssh -L 8080:localhost:80 user@server
#     ^^^^              ^^
#     local port        remote port
```

```python
# Using Paramiko library
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("localhost", port=2222, username="labuser", password="labpass")

stdin, stdout, stderr = client.exec_command("uname -a")
print(stdout.read().decode())
```

### ⚠️ Where the Analogy Breaks Down

| Analogy Says | Reality Is |
|--------------|------------|
| One tunnel at a time | SSH can multiplex many channels |
| Guard checks once | Authentication can be multi-factor |
| Physical tunnel is fixed | SSH can do dynamic port forwarding (SOCKS proxy) |
| Only you use the tunnel | SSH supports multiple simultaneous sessions |

---

## 5. FTP: The Dual-Lane Highway

### 🏠 Real-World Analogy

FTP is like a highway with two lanes — one for talking, one for cargo:

| Analogy Component | FTP Equivalent |
|-------------------|----------------|
| **Control lane (walkie-talkie)** | Control channel (port 21) |
| **Cargo lane (trucks)** | Data channel (port 20 or high port) |
| **Dispatcher giving directions** | FTP commands (LIST, RETR, STOR) |
| **Trucks carrying goods** | Actual file data |
| **"Pull into bay 5"** | Passive mode port assignment |

**Key insight:** FTP uses *two* TCP connections because it was designed when bandwidth was precious — you want to send commands quickly while large files transfer slowly.

### 🖼️ Visual Representation

```
═══════════════════════════════════════════════════════════════════════════════
                    FTP DUAL-CHANNEL ARCHITECTURE
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────┐                              ┌─────────────────┐
│   FTP Client    │                              │   FTP Server    │
│                 │                              │                 │
│  ┌───────────┐  │  ═══════════════════════════ │  ┌───────────┐  │
│  │  Control  │──┼──║ TCP Port 21 (commands) ║──┼──│  Control  │  │
│  │  Channel  │  │  ║  USER labftp           ║  │  │  Channel  │  │
│  │           │  │  ║  PASS ****             ║  │  │           │  │
│  │           │  │  ║  PASV                  ║  │  │           │  │
│  │           │  │  ║  RETR file.txt         ║  │  │           │  │
│  └───────────┘  │  ═══════════════════════════ │  └───────────┘  │
│                 │                              │                 │
│  ┌───────────┐  │  ═══════════════════════════ │  ┌───────────┐  │
│  │   Data    │──┼──║ TCP Port 30000 (data)  ║──┼──│   Data    │  │
│  │  Channel  │  │  ║  [file bytes...]       ║  │  │  Channel  │  │
│  │           │  │  ║  [file bytes...]       ║  │  │           │  │
│  └───────────┘  │  ═══════════════════════════ │  └───────────┘  │
└─────────────────┘                              └─────────────────┘

PASSIVE MODE (227 response):
  Server: "227 Entering Passive Mode (192,168,1,100,117,48)"
  
  Port calculation: 117 × 256 + 48 = 30000
                    ^^^       ^^
                    high byte  low byte
```

### 💻 Technical Reality

```python
from ftplib import FTP
from io import BytesIO

# Connect and authenticate
ftp = FTP()
ftp.connect("localhost", 2121)
ftp.login("labftp", "labftp")

# List directory (uses data channel)
ftp.retrlines("LIST")

# Download file (uses data channel)
buffer = BytesIO()
ftp.retrbinary("RETR hello.txt", buffer.write)
print(buffer.getvalue().decode())

ftp.quit()
```

### ⚠️ Where the Analogy Breaks Down

| Analogy Says | Reality Is |
|--------------|------------|
| Two lanes always exist | Data channel is created per transfer, then closed |
| Highways are one-way | FTP data channel can upload or download |
| Lanes are symmetric | Passive vs Active mode changes who initiates data connection |
| Only cargo moves on truck lane | Some FTP variants embed data in control (FTP over TLS) |

---

## 6. Certificate Chain: The Notary Chain of Trust

### 🏠 Real-World Analogy

TLS certificate verification is like verifying a document through a chain of notaries:

| Analogy Component | Certificate Equivalent |
|-------------------|------------------------|
| **Your local notary** | End-entity certificate (website's cert) |
| **Regional notary office** | Intermediate CA certificate |
| **National notary authority** | Root CA certificate |
| **Government ID** | Pre-installed root certificates in browser/OS |
| **"I verify this notary"** | CA signature on certificate |

**Key insight:** You don't need to personally know every website. You trust a few Root CAs, who vouch for Intermediate CAs, who vouch for websites.

### 🖼️ Visual Representation

```
═══════════════════════════════════════════════════════════════════════════════
                      CERTIFICATE CHAIN OF TRUST
═══════════════════════════════════════════════════════════════════════════════

                    ┌─────────────────────────────────┐
                    │        ROOT CA CERTIFICATE       │
                    │   "DigiCert Global Root CA"      │
                    │   ✅ Pre-installed in your OS    │
                    │   🔐 Self-signed                 │
                    └────────────────┬────────────────┘
                                     │ signs
                                     ▼
                    ┌─────────────────────────────────┐
                    │    INTERMEDIATE CA CERTIFICATE   │
                    │  "DigiCert TLS RSA SHA256 CA"   │
                    │  ✅ Signed by Root CA           │
                    │  🔐 Signs website certificates  │
                    └────────────────┬────────────────┘
                                     │ signs
                                     ▼
                    ┌─────────────────────────────────┐
                    │    END-ENTITY CERTIFICATE       │
                    │     "www.example.com"           │
                    │  ✅ Signed by Intermediate CA   │
                    │  🔐 Website proves identity     │
                    └─────────────────────────────────┘
                                     │
                                     ▼
                    ┌─────────────────────────────────┐
                    │        YOUR BROWSER             │
                    │  1. Receives cert chain         │
                    │  2. Verifies each signature     │
                    │  3. Checks against root store   │
                    │  4. 🔒 Shows padlock if valid   │
                    └─────────────────────────────────┘
```

### 💻 Technical Reality

```python
import ssl
import socket

# Connect and get certificate
context = ssl.create_default_context()
sock = socket.create_connection(("example.com", 443))
secure_sock = context.wrap_socket(sock, server_hostname="example.com")

# Get certificate info
cert = secure_sock.getpeercert()
print(f"Subject: {cert['subject']}")
print(f"Issuer: {cert['issuer']}")
print(f"Valid until: {cert['notAfter']}")
```

```bash
# View certificate chain with OpenSSL
openssl s_client -connect example.com:443 -showcerts

# View certificate details
echo | openssl s_client -connect example.com:443 2>/dev/null | \
  openssl x509 -noout -text
```

### ⚠️ Where the Analogy Breaks Down

| Analogy Says | Reality Is |
|--------------|------------|
| Trust is permanent | Certificates expire (notAfter date) |
| Notary is always honest | CAs have been compromised (DigiNotar incident) |
| One notary chain | Multiple valid chains can exist |
| Paper documents | Digital signatures use public-key cryptography |

---

## Quick Reference: All Analogies

| Concept | Analogy | Key Insight |
|---------|---------|-------------|
| **HTTPS/TLS** | Sealed envelope | Address visible, content private |
| **REST Levels** | Restaurant service | From fast food to fine dining |
| **DNS** | Phone directory | Name → number lookup with caching |
| **SSH** | Secure tunnel | Private passage through hostile territory |
| **FTP** | Dual-lane highway | Separate lanes for control and cargo |
| **Cert Chain** | Notary chain | Trust through verified intermediaries |

---

## Using Analogies in Teaching

### Do ✅

- Introduce the analogy *before* technical details
- Return to the analogy when students struggle
- Ask students to extend the analogy
- Use the analogy in troubleshooting ("Where did the letter get lost?")

### Don't ❌

- Over-rely on one analogy for everything
- Forget to discuss limitations
- Use analogies that are culturally specific
- Assume the analogy is universally understood

---

*Computer Networks — Week 10 | ASE, CSIE Bucharest*
*Concept analogies by ing. dr. Antonio Clim*
