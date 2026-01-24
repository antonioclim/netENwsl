# ❌ Common Misconceptions — Week 11
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> This document lists common misunderstandings about load balancing, DNS, FTP and SSH protocols, with corrections and practical verification methods.

---

## Table of Contents

1. [Load Balancing Misconceptions](#1-load-balancing-misconceptions)
2. [DNS Misconceptions](#2-dns-misconceptions)
3. [FTP Misconceptions](#3-ftp-misconceptions)
4. [SSH Misconceptions](#4-ssh-misconceptions)
5. [Nginx-Specific Misconceptions](#5-nginx-specific-misconceptions)

---

## 1. Load Balancing Misconceptions

### 🚫 Misconception 1.1: "Round-robin distributes requests perfectly evenly"

**WRONG:** "If I have 3 backends and send 9 requests, each backend will always receive exactly 3 requests."

**CORRECT:** Round-robin distributes requests in sequence, but real-world factors affect actual distribution:
- Connection timing and concurrency can cause uneven distribution
- If a backend fails mid-rotation, the pattern shifts
- Keep-alive connections may send multiple requests to the same backend
- The starting index affects which backend receives the first request

| Factor | Impact on Distribution |
|--------|----------------------|
| Backend failure | Remaining backends receive more traffic |
| Connection pooling | Same backend may handle burst of requests |
| Health check timing | Recently recovered backend may be skipped |

**Practical verification:**
```bash
# Send 12 requests and observe distribution
for i in {1..12}; do curl -s http://localhost:8080/ | grep "Backend"; done | sort | uniq -c
# You may see slight variations like 4-4-4 or 5-4-3
```

---

### 🚫 Misconception 1.2: "IP hash guarantees session persistence across load balancer restarts"

**WRONG:** "My session will always go to the same backend because my IP address never changes."

**CORRECT:** IP hash provides session affinity only while the backend pool remains stable:
- Adding or removing a backend changes the hash distribution
- Load balancer restart resets internal state
- Different load balancer instances may use different hash algorithms
- IPv6 vs IPv4 produces different hash values

**Why this matters:** If you rely on IP hash for session state without proper session storage, users may lose their sessions during deployments or scaling events.

**Practical verification:**
```bash
# Test IP hash consistency
for i in {1..5}; do curl -s http://localhost:8080/; done
# All requests should go to the same backend

# Now stop one backend and test again
docker stop s11_backend_2
for i in {1..5}; do curl -s http://localhost:8080/; done
# Some clients may now route to a different backend
```

---

### 🚫 Misconception 1.3: "Nginx detects backend failure instantly"

**WRONG:** "As soon as a backend crashes, Nginx immediately stops sending traffic to it."

**CORRECT:** Nginx uses **passive health checks** by default, which means:
- Failure detection happens only when a real request fails
- The first request to a dead backend will fail (502 error)
- Multiple failures (`max_fails`) must occur before marking unhealthy
- Recovery requires waiting for `fail_timeout` to expire

| Parameter | Default | Meaning |
|-----------|---------|---------|
| `max_fails` | 1 | Failures before marking down |
| `fail_timeout` | 10s | Time before retry and unhealthy period |

**Practical verification:**
```bash
# Stop a backend
docker stop s11_backend_2

# First request to that backend will fail
curl http://localhost:8080/  # May return 502 if it hit backend_2

# Subsequent requests will avoid the failed backend
for i in {1..6}; do curl -s http://localhost:8080/; done
```

---

### 🚫 Misconception 1.4: "502 Bad Gateway means the load balancer is broken"

**WRONG:** "I see 502 errors, so Nginx must have crashed or be misconfigured."

**CORRECT:** A 502 Bad Gateway indicates the load balancer is working correctly but cannot reach the backend:
- The backend server is down or not responding
- The backend returned an invalid response
- Connection to backend timed out
- Backend closed connection unexpectedly

| Error Code | Meaning | Likely Cause |
|------------|---------|--------------|
| 502 | Bad Gateway | Backend unreachable or invalid response |
| 503 | Service Unavailable | All backends down or overloaded |
| 504 | Gateway Timeout | Backend too slow to respond |

**Practical verification:**
```bash
# Stop all backends
docker stop s11_backend_1 s11_backend_2 s11_backend_3

# Now try to access - you'll get 502/503
curl -i http://localhost:8080/
# HTTP/1.1 502 Bad Gateway (Nginx is fine, backends are not)
```

---

### 🚫 Misconception 1.5: "Load balancer and reverse proxy are the same thing"

**WRONG:** "A reverse proxy is just another name for a load balancer."

**CORRECT:** These are related but distinct concepts:

| Aspect | Reverse Proxy | Load Balancer |
|--------|---------------|---------------|
| Primary purpose | Hide backend identity, add features | Distribute traffic |
| Backend count | Often single backend | Multiple backends |
| Features | Caching, SSL termination, compression | Health checks, algorithms |
| Example use | API gateway, CDN edge | High availability cluster |

A load balancer is typically implemented as a reverse proxy, but a reverse proxy does not necessarily balance load. Nginx can function as both.

---

## 2. DNS Misconceptions

### 🚫 Misconception 2.1: "DNS TTL is always respected by all resolvers"

**WRONG:** "I set TTL to 300 seconds, so all caches will refresh exactly every 5 minutes."

**CORRECT:** TTL is a suggestion, not a guarantee:
- Some resolvers enforce minimum TTL (e.g., 5 minutes regardless of setting)
- Some resolvers cap maximum TTL (e.g., ignore TTL > 1 day)
- Browser DNS caches often ignore TTL entirely
- Operating system caches may have their own policies

**Why this matters:** During DNS-based failover or migration, old records may persist longer than expected.

**Practical verification:**
```bash
# Query with dig and observe TTL countdown
dig google.com A +noall +answer
# Wait 30 seconds and query again - TTL should decrease
sleep 30
dig google.com A +noall +answer
```

---

### 🚫 Misconception 2.2: "DNS always uses port 53 UDP"

**WRONG:** "DNS is a UDP protocol on port 53, always."

**CORRECT:** DNS uses both UDP and TCP on port 53:

| Protocol | When Used |
|----------|-----------|
| UDP:53 | Standard queries (responses < 512 bytes) |
| TCP:53 | Large responses, zone transfers (AXFR) |
| TCP:53 | When UDP response is truncated (TC flag) |
| TCP:853 | DNS over TLS (DoT) |
| TCP:443 | DNS over HTTPS (DoH) |

**Practical verification:**
```bash
# Force TCP query
dig google.com A +tcp

# Query for large record (TXT often exceeds UDP limit)
dig google.com TXT
```

---

### 🚫 Misconception 2.3: "NXDOMAIN means the DNS server is broken"

**WRONG:** "I got NXDOMAIN, so there must be a DNS configuration problem."

**CORRECT:** NXDOMAIN (Non-Existent Domain) is a valid, successful DNS response indicating the domain does not exist:

| RCODE | Name | Meaning |
|-------|------|---------|
| 0 | NOERROR | Query successful, records found |
| 3 | NXDOMAIN | Domain does not exist (valid response) |
| 2 | SERVFAIL | Server failed to process query |
| 5 | REFUSED | Server refused to answer |

**Practical verification:**
```bash
# Query non-existent domain
python3 src/exercises/ex_11_03_dns_client.py --query thisdomaindoesnotexist12345.com --type A
# Status: NXDOMAIN (this is correct behaviour, not an error)
```

---

## 3. FTP Misconceptions

### 🚫 Misconception 3.1: "FTP passive mode eliminates all firewall issues"

**WRONG:** "If I use passive mode, FTP will work through any firewall."

**CORRECT:** Passive mode helps but does not solve all problems:
- Server must open ephemeral ports (often 1024-65535)
- Firewall must allow inbound connections to those ports
- NAT devices may still have issues with dynamic port ranges
- Some firewalls require FTP ALG (Application Layer Gateway)

| Mode | Client Firewall | Server Firewall |
|------|-----------------|-----------------|
| Active | Must allow inbound :20 | Simple outbound |
| Passive | Simple outbound | Must allow inbound ephemeral range |

**Why this matters:** Enterprise firewalls often block the ephemeral port range, making even passive FTP problematic.

---

### 🚫 Misconception 3.2: "FTP uses a single connection"

**WRONG:** "FTP is like HTTP - one connection for everything."

**CORRECT:** FTP uses a dual-connection architecture:

```
┌──────────────────────────────────────────────────────┐
│  Control Connection (Port 21) - PERSISTENT          │
│  • Authentication (USER, PASS)                      │
│  • Commands (LIST, RETR, STOR)                      │
│  • Status responses (codes 1xx-5xx)                 │
├──────────────────────────────────────────────────────┤
│  Data Connection (Port 20 or ephemeral) - TRANSIENT │
│  • File transfers                                   │
│  • Directory listings                               │
│  • Created per transfer, then closed                │
└──────────────────────────────────────────────────────┘
```

This separation allows sending commands during file transfers and simplifies protocol state management.

---

## 4. SSH Misconceptions

### 🚫 Misconception 4.1: "SSH port forwarding encrypts traffic to the destination"

**WRONG:** "If I use SSH tunnel to access a website, everything is encrypted end-to-end."

**CORRECT:** SSH encrypts only the tunnel segment:

```
[Browser] ──PLAIN──► [SSH Client :8080] ═══ENCRYPTED═══► [SSH Server] ──PLAIN──► [Website :80]
          (local)                        (tunnel)                      (remote)
```

- Traffic between SSH server and final destination is unencrypted (unless HTTPS)
- The SSH tunnel protects against local network sniffing
- The destination server sees the SSH server's IP, not yours

**Why this matters:** Using SSH tunnel to access HTTP sites still exposes data on the remote network.

---

### 🚫 Misconception 4.2: "SSH key authentication is always more secure than passwords"

**WRONG:** "I use SSH keys, so my server is completely secure."

**CORRECT:** SSH keys are more secure only when properly managed:

| Risk Factor | Password | SSH Key |
|-------------|----------|---------|
| Brute force | Vulnerable | Immune (2048+ bit) |
| Stolen credentials | One server | All servers with that key |
| Key management | None | Must protect private key |
| Revocation | Change password | Remove from all authorized_keys |

An unprotected private key (no passphrase) on a compromised workstation gives attackers access to all servers.

---

## 5. Nginx-Specific Misconceptions

### 🚫 Misconception 5.1: "proxy_pass URL trailing slash doesn't matter"

**WRONG:** "proxy_pass http://backend and proxy_pass http://backend/ are identical."

**CORRECT:** The trailing slash significantly affects URI handling:

```nginx
# WITHOUT trailing slash - URI is appended
location /api/ {
    proxy_pass http://backend;
}
# Request: /api/users → Backend receives: /api/users

# WITH trailing slash - location prefix is replaced
location /api/ {
    proxy_pass http://backend/;
}
# Request: /api/users → Backend receives: /users
```

**Practical verification:**
```bash
# Check nginx.conf for proxy_pass directives
cat docker/configs/nginx.conf | grep proxy_pass
```

---

### 🚫 Misconception 5.2: "upstream server weight means percentage"

**WRONG:** "Setting weight=3 means this server gets 30% of traffic."

**CORRECT:** Weight is relative to other servers in the pool:

```nginx
upstream backend {
    server web1:80 weight=3;  # 3/(3+2+1) = 50%
    server web2:80 weight=2;  # 2/(3+2+1) = 33%
    server web3:80 weight=1;  # 1/(3+2+1) = 17%
}
```

| Configuration | web1 | web2 | web3 |
|---------------|------|------|------|
| weight=3,2,1 | 50% | 33% | 17% |
| weight=1,1,1 | 33% | 33% | 33% |
| weight=5,5,0 | 50% | 50% | 0% (backup only if weight=0 invalid, use `backup`) |

---

## Quick Reference: Error Diagnosis

| Symptom | Likely Misconception | Reality |
|---------|---------------------|---------|
| 502 errors | "Nginx broken" | Backend unreachable |
| Uneven distribution | "Round-robin broken" | Connection timing, failures |
| Session lost after deploy | "IP hash broken" | Backend pool changed |
| DNS not updating | "DNS broken" | TTL caching behaviour |
| FTP timeout | "Passive mode broken" | Firewall blocking ephemeral ports |

---

*NETWORKING class - ASE, Informatics | Computer Networks Laboratory*
*Week 11: Application Protocols — FTP, DNS, SSH and Load Balancing*
