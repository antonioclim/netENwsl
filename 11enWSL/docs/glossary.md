# 📖 Glossary — Week 11: Application Protocols and Load Balancing
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Core Terms

### Load Balancing

| Term | Definition | Example |
|------|------------|---------|
| **Backend** | A server that receives forwarded requests from a load balancer | `server web1:80` in upstream block |
| **Upstream** | Nginx term for a group of backend servers | `upstream backend_pool { ... }` |
| **Health check** | Periodic verification that a backend is operational | HTTP GET to `/health` endpoint |
| **Failover** | Automatic redirection of traffic when a backend fails | Request retried on next healthy server |
| **Sticky session** | Routing all requests from same client to same backend | IP hash, cookie-based affinity |
| **Round-robin** | Distribution algorithm cycling through backends sequentially | 1→2→3→1→2→3... |
| **Least connections** | Algorithm routing to backend with fewest active connections | Best for varying request times |
| **Weighted distribution** | Allocating more traffic to higher-capacity backends | `weight=3` gets 3× more requests |
| **Reverse proxy** | Server that forwards client requests to backend servers | Nginx in front of application servers |
| **Passive health check** | Detecting failures from actual request failures | `max_fails=2 fail_timeout=10s` |
| **Active health check** | Proactively sending test requests to backends | Nginx Plus feature, or custom implementation |

### DNS (Domain Name System)

| Term | Definition | Example |
|------|------------|---------|
| **Resolver** | DNS client that performs queries on behalf of applications | `8.8.8.8`, system stub resolver |
| **Authoritative server** | DNS server with definitive records for a zone | `ns1.google.com` for google.com |
| **Recursive query** | Query where resolver performs complete resolution | Client → Resolver → Root → TLD → Auth |
| **Iterative query** | Query returning referral to another server | Resolver receives "ask ns1.example.com" |
| **TTL (Time To Live)** | Duration a DNS record may be cached | `300` = 5 minutes |
| **RCODE** | Response code indicating query result | `0`=NOERROR, `3`=NXDOMAIN |
| **Zone** | Administrative boundary in DNS namespace | `example.com` zone |
| **QNAME** | Query name - the domain being looked up | `www.google.com` |
| **RR (Resource Record)** | Single DNS record entry | `www IN A 93.184.216.34` |
| **Glue record** | A record in parent zone for child nameserver | Required when NS is within same domain |

### FTP (File Transfer Protocol)

| Term | Definition | Example |
|------|------------|---------|
| **Control connection** | Persistent TCP connection for commands (port 21) | `USER`, `PASS`, `LIST`, `RETR` |
| **Data connection** | Transient connection for file transfers | Port 20 (active) or ephemeral (passive) |
| **Active mode** | Server initiates data connection to client | `PORT 192,168,1,5,4,1` |
| **Passive mode** | Client initiates data connection to server | `PASV` → `227 (h1,h2,h3,h4,p1,p2)` |
| **EPSV** | Extended passive mode for IPv6 compatibility | Returns only port number |
| **Binary mode** | Transfer without character conversion | Required for images, executables |
| **ASCII mode** | Transfer with line ending conversion | For text files between OS types |

### SSH (Secure Shell)

| Term | Definition | Example |
|------|------------|---------|
| **Key exchange** | Process establishing shared secret | Diffie-Hellman, ECDH |
| **Host key** | Server's identity key for authentication | `/etc/ssh/ssh_host_ed25519_key` |
| **Local forwarding** | Tunnel from client port to remote destination | `ssh -L 8080:webserver:80 user@jump` |
| **Remote forwarding** | Tunnel from server port back to client network | `ssh -R 9000:localhost:3000 user@server` |
| **Dynamic forwarding** | SOCKS proxy through SSH tunnel | `ssh -D 1080 user@server` |
| **Agent forwarding** | Forwarding SSH keys through jump hosts | `ssh -A user@jumphost` |
| **Known hosts** | File storing trusted server fingerprints | `~/.ssh/known_hosts` |
| **Multiplexing** | Multiple logical channels over single connection | Shell + SFTP + port forward simultaneously |

### Nginx-Specific

| Term | Definition | Example |
|------|------------|---------|
| **proxy_pass** | Directive forwarding requests to backend | `proxy_pass http://backend_pool;` |
| **upstream block** | Configuration defining backend server group | `upstream backend { server web1; }` |
| **location block** | URL path matching configuration | `location /api/ { ... }` |
| **proxy_set_header** | Pass headers to backend | `proxy_set_header Host $host;` |
| **proxy_next_upstream** | Conditions for trying next backend | `error timeout http_502` |

---

## Commands Reference

### Docker Compose

| Command | Purpose | Example |
|---------|---------|---------|
| `docker compose up -d` | Start services in background | `docker compose -f docker/docker-compose.yml up -d` |
| `docker compose down` | Stop and remove containers | `docker compose down` |
| `docker compose logs` | View service logs | `docker compose logs -f nginx` |
| `docker compose ps` | List running services | `docker compose ps` |
| `docker compose restart` | Restart specific service | `docker compose restart nginx` |

### curl (HTTP Testing)

| Command | Purpose | Example |
|---------|---------|---------|
| `curl -s` | Silent mode (no progress) | `curl -s http://localhost:8080/` |
| `curl -i` | Include response headers | `curl -i http://localhost:8080/` |
| `curl -v` | Verbose (show request/response) | `curl -v http://localhost:8080/` |
| `curl -H` | Add custom header | `curl -H "X-Test: value" http://...` |
| `curl -w` | Custom output format | `curl -w "Time: %{time_total}s\n" -o /dev/null -s URL` |

### dig (DNS Testing)

| Command | Purpose | Example |
|---------|---------|---------|
| `dig A` | Query A record | `dig google.com A` |
| `dig MX` | Query mail exchangers | `dig google.com MX` |
| `dig NS` | Query nameservers | `dig example.com NS` |
| `dig +short` | Concise output | `dig google.com A +short` |
| `dig +tcp` | Force TCP query | `dig google.com A +tcp` |
| `dig @server` | Query specific server | `dig @1.1.1.1 google.com A` |
| `dig +trace` | Show resolution path | `dig google.com A +trace` |

### Nginx

| Command | Purpose | Example |
|---------|---------|---------|
| `nginx -t` | Test configuration syntax | `docker exec s11_nginx_lb nginx -t` |
| `nginx -s reload` | Reload configuration | `docker exec s11_nginx_lb nginx -s reload` |
| `nginx -V` | Show compile options | `nginx -V` |

---

## Acronyms

| Acronym | Full Form | Context |
|---------|-----------|---------|
| **DNS** | Domain Name System | Translates domain names to IP addresses |
| **FTP** | File Transfer Protocol | Legacy file transfer (ports 20, 21) |
| **FTPS** | FTP Secure | FTP with TLS encryption |
| **SFTP** | SSH File Transfer Protocol | File transfer over SSH (port 22) |
| **SSH** | Secure Shell | Encrypted remote access protocol |
| **TLS** | Transport Layer Security | Encryption for TCP connections |
| **TTL** | Time To Live | Cache duration for DNS records |
| **ALG** | Application Layer Gateway | Firewall feature for protocol inspection |
| **NAT** | Network Address Translation | Private-to-public IP mapping |
| **SOCKS** | Socket Secure | Proxy protocol for any TCP traffic |
| **RCODE** | Response Code | DNS query result status |
| **QTYPE** | Query Type | DNS record type being requested |
| **EPSV** | Extended Passive | IPv6-compatible FTP passive mode |
| **LB** | Load Balancer | Traffic distribution component |
| **HA** | High Availability | System designed to minimise downtime |
| **RR** | Resource Record | Single DNS database entry |
| **SOA** | Start of Authority | DNS zone metadata record |
| **MX** | Mail Exchanger | DNS record for email servers |
| **NS** | Name Server | DNS record delegating a zone |
| **CNAME** | Canonical Name | DNS alias record |

---

## Relationships Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        APPLICATION LAYER PROTOCOLS                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   DNS (UDP/TCP:53)          FTP (TCP:21,20)           SSH (TCP:22)         │
│   ┌─────────────┐           ┌─────────────┐           ┌─────────────┐      │
│   │  Resolver   │           │   Control   │           │  Transport  │      │
│   │      ↓      │           │      ↓      │           │      ↓      │      │
│   │ Authoritative│          │    Data     │           │    Auth     │      │
│   │      ↓      │           │             │           │      ↓      │      │
│   │   Caching   │           └─────────────┘           │  Connection │      │
│   └─────────────┘                                     └─────────────┘      │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                           LOAD BALANCING                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                            ┌───────────┐                                    │
│                            │  Client   │                                    │
│                            └─────┬─────┘                                    │
│                                  │                                          │
│                                  ▼                                          │
│                     ┌────────────────────────┐                              │
│                     │     Load Balancer      │                              │
│                     │  ┌──────────────────┐  │                              │
│                     │  │ Algorithm:       │  │                              │
│                     │  │ • Round-robin    │  │                              │
│                     │  │ • Least-conn     │  │                              │
│                     │  │ • IP hash        │  │                              │
│                     │  └──────────────────┘  │                              │
│                     └───────────┬────────────┘                              │
│                    ┌────────────┼────────────┐                              │
│                    ▼            ▼            ▼                              │
│              ┌─────────┐  ┌─────────┐  ┌─────────┐                          │
│              │Backend 1│  │Backend 2│  │Backend 3│                          │
│              │ (healthy)│ │ (healthy)│ │  (down) │                          │
│              └─────────┘  └─────────┘  └─────────┘                          │
│                                                                             │
│   Health States: healthy ←→ unhealthy (based on max_fails/fail_timeout)    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## See Also

- `docs/misconceptions.md` — Common misunderstandings about these concepts
- `docs/theory_summary.md` — Detailed theoretical background
- `docs/peer_instruction.md` — Quiz questions testing these concepts

---

*NETWORKING class - ASE, Informatics | Computer Networks Laboratory*
*Week 11: Application Protocols — FTP, DNS, SSH and Load Balancing*
