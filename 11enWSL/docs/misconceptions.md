# ❌ Common Misconceptions — Week 11
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Common misunderstandings about load balancing, DNS, FTP and SSH protocols.

In previous lab sessions, students consistently confused passive and active health checks. The 502 error on first failure catches everyone off guard.

---

## 1. Load Balancing Misconceptions

### 🚫 1.1: "Round-robin distributes requests perfectly evenly"

**WRONG:** "Each backend will always receive exactly 3 requests from 9 total."

**CORRECT:** Real-world factors affect distribution:
- Connection timing and concurrency
- Backend failures mid-rotation
- Keep-alive connections

**Verification:**
```bash
for i in {1..12}; do curl -s http://localhost:8080/ | grep "Backend"; done | sort | uniq -c
```

---

### 🚫 1.2: "IP hash guarantees session persistence across restarts"

**WRONG:** "My session will always go to the same backend."

**CORRECT:** IP hash provides affinity only while backend pool is stable:
- Adding/removing backends changes hash distribution
- Load balancer restart may reset state

---

### 🚫 1.3: "Nginx detects backend failure instantly"

**WRONG:** "Nginx immediately stops sending traffic to crashed backends."

**CORRECT:** Nginx uses **passive health checks** by default:
- First request to dead backend fails with 502
- After `max_fails` (default 1), backend marked unhealthy
- Recovery after `fail_timeout` (default 10s)

This particular issue tends to appear when students expect "instant" failover like cloud load balancers provide.

---

### 🚫 1.4: "502 Bad Gateway means Nginx is broken"

**WRONG:** "502 errors mean Nginx crashed."

**CORRECT:** 502 indicates Nginx works but cannot reach backend:

| Code | Meaning |
|------|---------|
| 502 | Backend unreachable |
| 503 | All backends down |
| 504 | Backend too slow |

---

## 2. DNS Misconceptions

### 🚫 2.1: "DNS TTL is always respected"

**WRONG:** "TTL=60 means all caches refresh in 60 seconds."

**CORRECT:** TTL is a suggestion:
- ISP resolvers may enforce minimum TTL (e.g., 5 min)
- Browser caches often ignore TTL
- OS caches have own policies

From experience, this catches students during any "instant DNS update" exercise.

---

### 🚫 2.2: "DNS always uses UDP port 53"

**CORRECT:** DNS uses both UDP and TCP:

| Protocol | When Used |
|----------|-----------|
| UDP:53 | Standard queries |
| TCP:53 | Large responses, zone transfers |
| TCP:853 | DNS over TLS |

---

### 🚫 2.3: "NXDOMAIN means DNS is broken"

**CORRECT:** NXDOMAIN is a valid response meaning domain does not exist.

---

## 3. FTP Misconceptions

### 🚫 3.1: "Passive mode eliminates all firewall issues"

**CORRECT:** Passive mode helps but:
- Server must open ephemeral ports
- Firewall must allow inbound to those ports

### 🚫 3.2: "FTP uses a single connection"

**CORRECT:** FTP uses dual-connection architecture:
- Control (port 21) - persistent
- Data (port 20 or ephemeral) - transient per transfer

---

## 4. SSH Misconceptions

### 🚫 4.1: "SSH tunnel encrypts traffic to destination"

**WRONG:** "Everything is encrypted end-to-end."

**CORRECT:** SSH encrypts only the tunnel segment:

```
[Browser] ─PLAIN─► [localhost] ═══ENCRYPTED═══► [jumphost] ─PLAIN─► [website]
```

---

## 5. Nginx-Specific Misconceptions

### 🚫 5.1: "proxy_pass trailing slash doesn't matter"

```nginx
# WITHOUT slash - URI appended
location /api/ { proxy_pass http://backend; }
# /api/users → /api/users

# WITH slash - prefix replaced
location /api/ { proxy_pass http://backend/; }
# /api/users → /users
```

### 🚫 5.2: "weight=3 means 30% of traffic"

**CORRECT:** Weight is relative:
```nginx
upstream backend {
    server web1:80 weight=3;  # 3/6 = 50%
    server web2:80 weight=2;  # 2/6 = 33%
    server web3:80 weight=1;  # 1/6 = 17%
}
```

---

## Quick Reference: Error Diagnosis

| Symptom | Misconception | Reality |
|---------|--------------|---------|
| 502 errors | "Nginx broken" | Backend unreachable |
| Uneven distribution | "Round-robin broken" | Connection timing |
| Session lost | "IP hash broken" | Backend pool changed |
| DNS not updating | "DNS broken" | TTL caching |

---

*NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim*
