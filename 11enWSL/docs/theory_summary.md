# Week 11: Theoretical Foundations

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
> 
> by Revolvix

This document synthesises the key theoretical concepts underlying Week 11's practical exercises on application layer protocols (FTP, DNS, SSH) and load balancing architectures.

---

## 1. File Transfer Protocol (FTP)

### 1.1 Dual-Connection Architecture

FTP employs a distinctive **separation of concerns** through two concurrent TCP connections:

**Control Connection (Port 21)**
Persistent throughout the session, this channel carries commands and responses using a Telnet-like text protocol. Commands follow a verb-argument structure (e.g., `USER username`, `RETR filename`, `LIST`), whilst responses use three-digit status codes analogous to HTTP (2xx success, 4xx client error, 5xx server error).

**Data Connection (Port 20 or ephemeral)**
Transient connections established on-demand for file transfers and directory listings. This architectural decision enables concurrent command processing during lengthy transfers and simplifies protocol state management.

### 1.2 Active vs Passive Mode

The NAT traversal problem necessitated two connection establishment modes:

| Aspect | Active Mode | Passive Mode |
|--------|-------------|--------------|
| **Initiator** | Server connects to client | Client connects to server |
| **Client command** | `PORT h1,h2,h3,h4,p1,p2` | `PASV` |
| **Server response** | Data connection from :20 | `227 (h1,h2,h3,h4,p1,p2)` |
| **NAT compatibility** | Problematic | Preferred |
| **Firewall rules** | Complex (requires ALG) | Simpler (outbound only) |

The **Extended Passive Mode** (`EPSV`) addresses IPv6 compatibility by returning only the port number, assuming the same IP as the control connection.

### 1.3 Security Considerations

Plain FTP transmits credentials in cleartext, rendering it vulnerable to credential interception. Modern deployments favour:
- **FTPS** (FTP Secure): TLS encryption over standard ports
- **SFTP**: SSH File Transfer Protocol (distinct from FTP over SSH)

---

## 2. Domain Name System (DNS)

### 2.1 Hierarchical Namespace Architecture

DNS implements a distributed, hierarchical database structured as an inverted tree:

```
                    . (root)
                    │
        ┌───────────┼───────────┐
       com         org         ro
        │           │           │
    ┌───┴───┐      ...      ┌──┴──┐
  google  amazon          ase  gov
```

Each zone delegates authority to child zones, creating a scalable system with no single point of failure. The **zone** represents an administratively distinct portion of the namespace, potentially spanning multiple domain levels.

### 2.2 Resolution Process

**Recursive Resolution**: The resolver performs complete resolution on behalf of the client, querying iteratively through the hierarchy and caching responses. Preferred for end-user clients.

**Iterative Resolution**: The queried server returns the best answer it possesses, potentially a referral to another server. Used between DNS servers in the hierarchy.

The resolution path for `www.ase.ro`:
1. Query local resolver → cache miss
2. Query root servers → referral to `.ro` TLD servers
3. Query `.ro` servers → referral to `ase.ro` authoritative servers
4. Query `ase.ro` servers → definitive A/AAAA record

### 2.3 Resource Record Types

| Type | Purpose | Example |
|------|---------|---------|
| A | IPv4 address mapping | `www IN A 192.168.1.1` |
| AAAA | IPv6 address mapping | `www IN AAAA 2001:db8::1` |
| MX | Mail exchanger with priority | `@ IN MX 10 mail.example.com.` |
| NS | Nameserver delegation | `@ IN NS ns1.example.com.` |
| CNAME | Canonical name alias | `www IN CNAME server1.example.com.` |
| TXT | Arbitrary text (SPF, DKIM) | `@ IN TXT "v=spf1 include:_spf.google.com ~all"` |
| SOA | Start of Authority metadata | Serial, refresh, retry, expire, minimum TTL |

### 2.4 DNSSEC Trust Chain

DNSSEC provides authentication through cryptographic signatures:
1. **RRSIG**: Signature over a resource record set
2. **DNSKEY**: Zone signing key (ZSK) and key signing key (KSK)
3. **DS**: Delegation signer linking parent zone to child's DNSKEY

The trust chain anchors at the root zone's KSK, distributed via IANA.

---

## 3. Secure Shell (SSH)

### 3.1 Protocol Layering

SSH comprises three interdependent protocols:

**Transport Layer Protocol (RFC 4253)**
Provides server authentication, confidentiality, and integrity over a reliable transport (typically TCP:22). Negotiates key exchange algorithm, encryption cipher, and MAC algorithm. The Diffie-Hellman exchange establishes shared session keys without transmitting secrets.

**User Authentication Protocol (RFC 4252)**
Authenticates the client to the server using:
- **publickey**: Asymmetric cryptography (RSA, Ed25519)
- **password**: Encrypted password transmission
- **hostbased**: Trust delegation from client host
- **keyboard-interactive**: Challenge-response for MFA

**Connection Protocol (RFC 4254)**
Multiplexes the encrypted tunnel into logical channels, each with flow control via window size adjustments. Channel types include:
- Session (shell, exec, subsystem)
- Direct TCP/IP forwarding
- Forwarded TCP/IP
- X11 forwarding

### 3.2 Port Forwarding Architectures

**Local Forwarding** (`-L [bind_address:]port:host:hostport`):
Creates a listening socket on the SSH client; connections are forwarded through the encrypted tunnel to the remote network.

```
[Local Client] ─────► [SSH Client :8080] ═══SSH Tunnel═══► [SSH Server] ─────► [Remote:80]
```

**Remote Forwarding** (`-R [bind_address:]port:host:hostport`):
Creates a listening socket on the SSH server; connections are forwarded back through the tunnel to the client's network.

**Dynamic Forwarding** (`-D [bind_address:]port`):
Creates a SOCKS proxy on the client, enabling application-level proxying through the tunnel.

---

## 4. Load Balancing Theory

### 4.1 Distribution Algorithms

**Round-Robin**
Sequential distribution across backends in cyclic order. Assumes homogeneous server capacity. Simple implementation with O(1) selection complexity.

```python
next_server = servers[counter % len(servers)]
counter += 1
```

**Weighted Round-Robin**
Extends round-robin with capacity weights. Server with weight 3 receives thrice the requests of weight 1. Commonly implemented via expanded server list:

```
weights = {A: 3, B: 2, C: 1}
expanded = [A, A, A, B, B, C]  # Round-robin through expanded list
```

**Least Connections**
Routes to the server with fewest active connections. Optimal when requests have heterogeneous processing times. Requires connection tracking overhead.

**IP Hash**
Deterministic routing based on client IP hash. Provides session affinity ("sticky sessions") without shared state. Hash function:

```python
backend_index = hash(client_ip) % len(backends)
```

**Consistent Hashing**
Distributes servers and requests on a virtual ring. Minimises redistribution when servers join/leave. Employed in distributed caches (Memcached, Redis Cluster).

### 4.2 Health Checking Strategies

**Active Health Checks**
Periodic probes to backend health endpoints. Configurable parameters:
- Interval: Time between probes (e.g., 5s)
- Timeout: Maximum probe response time (e.g., 2s)
- Threshold: Failures before marking unhealthy (e.g., 2)
- Recovery: Successes before marking healthy (e.g., 3)

**Passive Health Checks**
Inference from production traffic. Connection failures or HTTP 5xx responses increment failure counters. Lower overhead but delayed detection.

### 4.3 Layer 4 vs Layer 7 Load Balancing

| Characteristic | L4 (Transport) | L7 (Application) |
|----------------|----------------|------------------|
| **Decision basis** | IP, port, TCP flags | HTTP headers, cookies, URI |
| **Session awareness** | Limited (IP hash) | Full (cookies, headers) |
| **SSL termination** | Pass-through or terminate | Typically terminates |
| **Content modification** | None | Possible (rewriting, injection) |
| **Performance** | Higher throughput | More flexible routing |
| **Examples** | HAProxy TCP, LVS | Nginx, HAProxy HTTP, Envoy |

---

## 5. Nginx Reverse Proxy Architecture

### 5.1 Upstream Configuration

Nginx defines backend pools through the `upstream` directive:

```nginx
upstream backend_pool {
    least_conn;  # Algorithm selection
    
    server web1:80 weight=3;
    server web2:80;
    server web3:80 backup;  # Failover only
    
    keepalive 32;  # Connection pooling
}
```

### 5.2 Proxy Header Propagation

Essential headers for backend transparency:

| Header | Purpose | Configuration |
|--------|---------|---------------|
| Host | Original Host header | `proxy_set_header Host $host;` |
| X-Real-IP | Client IP address | `proxy_set_header X-Real-IP $remote_addr;` |
| X-Forwarded-For | Proxy chain | `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;` |
| X-Forwarded-Proto | Original protocol | `proxy_set_header X-Forwarded-Proto $scheme;` |

### 5.3 Failover Semantics

```nginx
proxy_next_upstream error timeout http_500 http_502 http_503 http_504;
proxy_next_upstream_timeout 10s;
proxy_next_upstream_tries 3;
```

Nginx automatically retries on specified conditions, providing resilience against transient backend failures.

---

## References

1. Kurose, J. F., & Ross, K. W. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.

2. Rhodes, B., & Goetzen, J. (2014). *Foundations of Python Network Programming* (3rd ed.). Apress.

3. Postel, J., & Reynolds, J. (1985). *File Transfer Protocol (FTP)* (RFC 959). IETF.

4. Mockapetris, P. (1987). *Domain Names - Concepts and Facilities* (RFC 1034). IETF.

5. Ylonen, T., & Lonvick, C. (2006). *The Secure Shell (SSH) Protocol Architecture* (RFC 4251). IETF.

6. Nginx, Inc. (2024). *Nginx HTTP Load Balancing*. https://nginx.org/en/docs/http/load_balancing.html

---

*NETWORKING class - ASE, Informatics | by Revolvix*
