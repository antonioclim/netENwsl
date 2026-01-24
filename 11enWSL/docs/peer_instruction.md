# 🗳️ Peer Instruction Questions — Week 11
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Peer Instruction Protocol (5 Steps)

Each question follows **5 mandatory steps**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 1 (1 min)  │  Read the question and think individually               │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 2 (30 sec) │  Vote your answer (A/B/C/D) — no discussion!            │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 3 (2 min)  │  Discuss with your neighbour — convince them!           │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 4 (30 sec) │  Re-vote — you may change your answer                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 5 (2 min)  │  Instructor explains the correct answer                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Question 1: Load Balancer Failure Detection

> 💭 **PREDICTION:** Before reading, predict: How quickly does Nginx detect a backend failure by default?

### Scenario

You have configured Nginx with three backends using the default settings:

```nginx
upstream backend_pool {
    server web1:80;
    server web2:80;
    server web3:80;
}
```

Backend `web2` crashes unexpectedly. A client sends a request that Nginx routes to `web2`.

### Question

What happens to this specific request?

### Options

- **A)** Nginx instantly detects the failure and routes to `web1` or `web3` — the client sees no error
- **B)** The client receives a 502 Bad Gateway error for this request, but subsequent requests avoid `web2`
- **C)** Nginx waits 10 seconds for `web2` to respond, then returns 504 Gateway Timeout
- **D)** All requests fail until an administrator manually removes `web2` from the configuration

### Correct Answer

**B** — The client receives a 502 Bad Gateway error for this request, but subsequent requests avoid `web2`

### Explanation

Nginx uses **passive health checks** by default. This means:

1. Nginx does not proactively test backends
2. It only discovers failures when a real request fails
3. The first request to a dead backend returns 502 to the client
4. After `max_fails` failures (default: 1), Nginx marks the backend as unhealthy
5. The backend remains marked down for `fail_timeout` seconds (default: 10)

This is why option A is wrong — there is no "instant detection" without active health checks.

### Targeted Misconception

**"Nginx detects backend failure instantly"** — Students often assume load balancers have constant awareness of backend health. In reality, passive health checks mean the first failure is always visible to a client.

### Instructor Notes

- **Target accuracy:** 40-60% on first vote
- **Key concept:** Passive vs active health checking
- **After discussion:** Show `proxy_next_upstream` for retry behaviour
- **Demo:** Stop a backend during live testing to show the 502 error
- **Timing:** Present (1 min) → Vote (1 min) → Discuss (3 min) → Revote (30 sec) → Explain (2 min)

---

## Question 2: DNS Caching Behaviour

> 💭 **PREDICTION:** If you change a DNS record with TTL=60, how quickly will all clients see the change?

### Scenario

You manage the DNS for `app.example.com` with this record:

```
app.example.com.  60  IN  A  192.168.1.100
```

You change the IP to `192.168.1.200` and confirm the authoritative server returns the new IP. A user in another country reports they still see the old IP after 5 minutes.

### Question

What is the most likely explanation?

### Options

- **A)** The DNS change failed — the authoritative server must be returning the old record
- **B)** The user's ISP resolver is caching beyond the TTL or has a minimum TTL policy
- **C)** DNS propagation always takes 24-48 hours regardless of TTL settings
- **D)** The user needs to manually flush their DNS cache using `ipconfig /flushdns`

### Correct Answer

**B** — The user's ISP resolver is caching beyond the TTL or has a minimum TTL policy

### Explanation

DNS TTL is a **recommendation**, not a requirement:

| Component | Caching Behaviour |
|-----------|------------------|
| Authoritative server | Definitive, returns current record |
| ISP recursive resolver | May enforce minimum TTL (e.g., 5 min) |
| Browser DNS cache | Often ignores TTL entirely |
| OS DNS cache | May have separate TTL policies |

Many ISP resolvers enforce a minimum cache time (often 300 seconds) regardless of the record's TTL to reduce query load.

### Targeted Misconception

**"DNS TTL is always respected by all resolvers"** — Students assume TTL guarantees cache refresh timing. The "24-48 hour propagation" myth (option C) persists from the early days of DNS when TTLs were much longer.

### Instructor Notes

- **Target accuracy:** 30-50% on first vote (this surprises many)
- **Key concept:** TTL is a suggestion, not a guarantee
- **After discussion:** Show `dig +trace` to see actual caching
- **Real-world impact:** DNS-based failover may be slower than expected
- **Timing:** Present (1 min) → Vote (1 min) → Discuss (3 min) → Revote (30 sec) → Explain (2 min)

---

## Question 3: FTP Connection Architecture

> 💭 **PREDICTION:** How many TCP connections does FTP use to transfer a single file?

### Scenario

A client connects to an FTP server in passive mode and downloads a 10MB file. During the transfer, the client also sends the `STAT` command to check transfer progress.

### Question

How many simultaneous TCP connections exist between client and server during this operation?

### Options

- **A)** One connection — FTP multiplexes commands and data on port 21
- **B)** Two connections — one for control (port 21) and one for data transfer
- **C)** Three connections — control, data upload and data download channels
- **D)** It depends on the file size — large files use multiple parallel data connections

### Correct Answer

**B** — Two connections — one for control (port 21) and one for data transfer

### Explanation

FTP uses a **dual-connection architecture**:

```
┌────────────────────────────────────────────────────────────────────┐
│  Control Connection (Port 21) — PERSISTENT                        │
│  • Always open during session                                     │
│  • Carries: USER, PASS, LIST, RETR, STAT commands                │
│  • Text-based protocol (like Telnet)                              │
├────────────────────────────────────────────────────────────────────┤
│  Data Connection (Ephemeral Port) — TRANSIENT                     │
│  • Created for each transfer                                      │
│  • Carries: File content, directory listings                      │
│  • Closed after transfer completes                                │
└────────────────────────────────────────────────────────────────────┘
```

The `STAT` command travels on the control connection while the file transfers on the data connection — this is why FTP can report progress during transfers.

### Targeted Misconception

**"FTP uses a single connection like HTTP"** — Students familiar with HTTP/1.1 assume all protocols work similarly. FTP's dual-connection design predates HTTP and was optimised for long file transfers.

### Instructor Notes

- **Target accuracy:** 50-70% on first vote
- **Key concept:** Separation of control and data channels
- **After discussion:** Explain why this design matters for firewalls (active vs passive mode)
- **Demo:** Use Wireshark to show both connections
- **Timing:** Present (1 min) → Vote (1 min) → Discuss (3 min) → Revote (30 sec) → Explain (2 min)

---

## Question 4: IP Hash Session Affinity

> 💭 **PREDICTION:** If you use IP hash, will the same user always reach the same backend?

### Scenario

Your load balancer uses IP hash for session affinity:

```nginx
upstream backend_pool {
    ip_hash;
    server web1:80;
    server web2:80;
    server web3:80;
}
```

A user with IP `192.168.1.50` logs in and is routed to `web2`. Their session data is stored in `web2`'s memory. The next day, after a deployment that restarted all services, the same user (same IP) tries to access the application.

### Question

What happens to this user's session?

### Options

- **A)** The session works — IP hash always routes `192.168.1.50` to `web2`
- **B)** The session is lost — the hash may produce a different result after backend restart
- **C)** The session works — Nginx stores IP-to-backend mappings persistently
- **D)** The session is lost — IP hash only works within a single HTTP request

### Correct Answer

**B** — The session is lost — the hash may produce a different result after backend restart

### Explanation

IP hash provides **session affinity**, not **session persistence**:

| Factor | Impact |
|--------|--------|
| Same IP, stable backends | Same backend (consistent) |
| Backend added/removed | Hash redistribution occurs |
| Backend restart | Usually consistent, but not guaranteed |
| Load balancer restart | Hash state may reset |

The hash function is deterministic, but if the backend list changes order or a backend was temporarily removed during restart, the hash calculation may route to a different server.

**Proper solution:** Store sessions in shared storage (Redis, database) rather than relying on affinity.

### Targeted Misconception

**"IP hash guarantees session persistence across restarts"** — Students confuse session *affinity* (same client tends to go to same backend) with session *persistence* (session data survives failures).

### Instructor Notes

- **Target accuracy:** 30-50% on first vote
- **Key concept:** Affinity vs persistence
- **After discussion:** Introduce Redis/Memcached for session storage
- **Real-world impact:** Lost sessions after deployment = angry users
- **Timing:** Present (1 min) → Vote (1 min) → Discuss (3 min) → Revote (30 sec) → Explain (2 min)

---

## Question 5: SSH Port Forwarding Security

> 💭 **PREDICTION:** Does SSH port forwarding encrypt traffic to the final destination?

### Scenario

You set up local port forwarding to access an internal HTTP server:

```bash
ssh -L 8080:internal-web:80 user@jumphost
```

You then browse to `http://localhost:8080` from your laptop. The data flows:

```
Laptop:browser → localhost:8080 → SSH tunnel → jumphost → internal-web:80
```

### Question

Which segments of this connection are encrypted?

### Options

- **A)** The entire path from browser to `internal-web:80` is encrypted by SSH
- **B)** Only `localhost:8080 → jumphost` (the SSH tunnel) is encrypted; `jumphost → internal-web:80` is plaintext
- **C)** Nothing is encrypted — SSH port forwarding only redirects traffic, it doesn't encrypt
- **D)** The encryption depends on whether the internal web server has HTTPS enabled

### Correct Answer

**B** — Only `localhost:8080 → jumphost` (the SSH tunnel) is encrypted; `jumphost → internal-web:80` is plaintext

### Explanation

SSH encrypts **only the tunnel segment**:

```
[Browser] ─PLAIN─► [localhost:8080] ═══ENCRYPTED═══► [jumphost] ─PLAIN─► [internal-web:80]
          (local)                    (SSH tunnel)               (remote network)
```

| Segment | Encryption |
|---------|------------|
| Browser → SSH client (localhost) | Plaintext (internal to laptop) |
| SSH client → SSH server | **Encrypted** (SSH tunnel) |
| SSH server → destination | **Plaintext** (unless HTTPS) |

This means anyone on the network between `jumphost` and `internal-web` can see the traffic.

### Targeted Misconception

**"SSH port forwarding encrypts traffic to the destination"** — Students assume the entire path is protected. This is dangerous when accessing sensitive services over HTTP through SSH tunnels — the "last mile" is unprotected.

### Instructor Notes

- **Target accuracy:** 40-60% on first vote
- **Key concept:** SSH protects the tunnel, not the destination
- **After discussion:** Emphasise using HTTPS even through SSH tunnels for sensitive data
- **Security implication:** Don't send passwords over HTTP, even through SSH tunnel
- **Timing:** Present (1 min) → Vote (1 min) → Discuss (3 min) → Revote (30 sec) → Explain (2 min)

---

## Summary: Key Misconceptions Addressed

| Q# | Topic | Common Wrong Belief | Reality |
|----|-------|--------------------| --------|
| 1 | Load Balancing | Instant failure detection | Passive checks = first request fails |
| 2 | DNS | TTL guarantees timing | Resolvers may cache longer |
| 3 | FTP | Single connection | Dual connection (control + data) |
| 4 | Load Balancing | IP hash = persistent sessions | Affinity ≠ persistence |
| 5 | SSH | End-to-end encryption | Only tunnel segment encrypted |

---

## Additional Practice Questions

For self-study, consider these scenarios:

1. **Load Balancing:** What happens if you use `least_conn` and all backends have equal connections?
2. **DNS:** Why might `dig @8.8.8.8 example.com` and `dig @1.1.1.1 example.com` return different results?
3. **FTP:** Why does active FTP fail through NAT but passive mode works?
4. **SSH:** What is the security difference between `-L` (local) and `-R` (remote) forwarding?

---

*NETWORKING class - ASE, Informatics | Computer Networks Laboratory*
*Week 11: Application Protocols — FTP, DNS, SSH and Load Balancing*
