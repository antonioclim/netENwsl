# 🗳️ Peer Instruction Questions — Week 11
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Peer Instruction Protocol (5 Steps)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 1 (1 min)  │  Read and think individually                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 2 (30 sec) │  Vote your answer — no discussion!                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 3 (2 min)  │  Discuss with neighbour — convince them!                │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 4 (30 sec) │  Re-vote — you may change your answer                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 5 (2 min)  │  Instructor explains correct answer                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Question 1: Load Balancer Failure Detection

### Scenario

Nginx with three backends using default settings. Backend `web2` crashes. A client sends a request routed to `web2`.

### Question

What happens to this request?

### Options

- **A)** Nginx instantly detects failure and routes to healthy backend
  - *Common wrong reasoning:* "Modern load balancers detect failures immediately"
- **B)** Client receives 502 Bad Gateway, subsequent requests avoid web2 ✓
- **C)** Nginx waits 10 seconds, returns 504 Gateway Timeout
  - *Common wrong reasoning:* Confusing fail_timeout with request timeout
- **D)** All requests fail until admin removes web2
  - *Common wrong reasoning:* Assuming manual intervention required

### Correct Answer: B

Nginx uses passive health checks — failure detection only when real request fails.

### Instructor Notes

- **Target accuracy:** 40-60% on first vote
- **From experience:** Question 1 typically shows 30-40% correct initially, rising to 75%+ after discussion. If higher, add follow-up about active health checks.
- **Demo:** Stop a backend during live testing

---

## Question 2: DNS Caching Behaviour

### Scenario

DNS record `app.example.com` has TTL=60. You change IP and confirm authoritative server returns new IP. User reports old IP after 5 minutes.

### Question

Most likely explanation?

### Options

- **A)** DNS change failed
  - *Common wrong reasoning:* Assuming any discrepancy means failure
- **B)** User's ISP resolver caches beyond TTL ✓
- **C)** DNS propagation always takes 24-48 hours
  - *Common wrong reasoning:* Persistent myth from early internet
- **D)** User needs to flush DNS cache
  - *Common wrong reasoning:* Overestimating client-side control

### Correct Answer: B

TTL is a suggestion, not a guarantee. ISP resolvers may enforce minimum TTL.

### Instructor Notes

- **Target accuracy:** 30-50% on first vote
- This surprises many students

---

## Question 3: FTP Connection Architecture

### Scenario

Client connects to FTP server in passive mode, downloads 10MB file. During transfer, client sends `STAT` command.

### Question

How many simultaneous TCP connections?

### Options

- **A)** One — FTP multiplexes on port 21
  - *Common wrong reasoning:* Assuming FTP works like HTTP
- **B)** Two — control (21) + data ✓
- **C)** Three — control + upload + download
  - *Common wrong reasoning:* Assuming separate channels per direction
- **D)** Depends on file size
  - *Common wrong reasoning:* Confusing with parallel download tools

### Correct Answer: B

FTP dual-connection: persistent control + transient data.

---

## Question 4: IP Hash Session Affinity

### Scenario

IP hash load balancer. User (IP 192.168.1.50) logs in, routed to web2. Session stored in web2 memory. Next day, after deployment restart, same user connects.

### Question

What happens to user's session?

### Options

- **A)** Session works — IP hash always routes to web2
  - *Common wrong reasoning:* Assuming hash is absolute guarantee
- **B)** Session lost — hash may differ after restart ✓
- **C)** Session works — Nginx stores mappings persistently
  - *Common wrong reasoning:* Assuming state persistence
- **D)** Session lost — IP hash only works within single request
  - *Common wrong reasoning:* Underestimating IP hash scope

### Correct Answer: B

IP hash provides affinity, not persistence. Backend pool changes affect distribution.

---

## Question 5: SSH Port Forwarding Security

### Scenario

```bash
ssh -L 8080:internal-web:80 user@jumphost
```

You browse to `http://localhost:8080`.

### Question

Which segments are encrypted?

### Options

- **A)** Entire path end-to-end
  - *Common wrong reasoning:* Assuming SSH protects everything
- **B)** Only localhost:8080 → jumphost (tunnel) ✓
- **C)** Nothing — SSH only redirects
  - *Common wrong reasoning:* Underestimating tunnel capabilities
- **D)** Depends on internal web server HTTPS
  - *Common wrong reasoning:* Partially correct but misses SSH encryption

### Correct Answer: B

SSH encrypts only the tunnel segment. Traffic jumphost → destination is plaintext.

---

## Summary

| Q# | Topic | Wrong Belief | Reality |
|----|-------|--------------|---------|
| 1 | Load Balancing | Instant detection | Passive = first fails |
| 2 | DNS | TTL guaranteed | Resolvers may cache longer |
| 3 | FTP | Single connection | Dual connection |
| 4 | Load Balancing | IP hash = persistent | Affinity ≠ persistence |
| 5 | SSH | End-to-end encryption | Only tunnel encrypted |

---

*NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim*
