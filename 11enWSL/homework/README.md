# Week 11 Homework Assignments

> NETWORKING class - ASE, Informatics | by Revolvix

## Overview

These homework assignments extend the laboratory exercises and reinforce understanding of application layer protocols and load balancing concepts.

**Submission Deadline:** Check your course schedule on the university platform.

**Submission Format:** ZIP archive containing:
- Completed Python scripts
- Screenshots of working demonstrations
- Brief report (PDF, max 2 pages) documenting your approach

---

## Assignment 1: Extended Load Balancer with Health Checks

**File:** `exercises/hw_11_01.py`

**Objective:** Enhance the Python load balancer with active health checking capabilities.

### Requirements

1. **Active Health Checks** (40 points)
   - Implement periodic HTTP health checks to each backend (every 5 seconds)
   - Mark backends as "unhealthy" after 3 consecutive failures
   - Mark backends as "healthy" after 2 consecutive successes
   - Use a background thread for health checking

2. **Weighted Round Robin** (30 points)
   - Extend the load balancer to support weighted distribution
   - Accept weights via command line: `--backends localhost:8081:3,localhost:8082:2,localhost:8083:1`
   - Weight of 3 means the backend receives 3x more requests than weight 1

3. **Statistics Endpoint** (20 points)
   - Add a `/stats` endpoint on the load balancer
   - Return JSON with:
     - Total requests processed
     - Requests per backend
     - Current backend health status
     - Active connections per backend

4. **Graceful Degradation** (10 points)
   - If all backends are unhealthy, return HTTP 503 Service Unavailable
   - Log warning when available backend count drops below threshold

### Testing Criteria

```powershell
# Start backends (some will be stopped during testing)
python src/exercises/ex_11_01_backend.py --id 1 --port 8081
python src/exercises/ex_11_01_backend.py --id 2 --port 8082
python src/exercises/ex_11_01_backend.py --id 3 --port 8083

# Start your enhanced load balancer
python homework/exercises/hw_11_01.py --backends localhost:8081:3,localhost:8082:2,localhost:8083:1 --listen 0.0.0.0:8080

# Test weighted distribution (expect ~50% to backend 1, ~33% to backend 2, ~17% to backend 3)
for /L %i in (1,1,100) do @curl -s http://localhost:8080/ >> results.txt

# Stop backend 2
# Wait 20 seconds for health checks to detect failure

# Check stats endpoint
curl http://localhost:8080/stats
```

### Hints

- Use `threading.Thread(daemon=True)` for the health check thread
- Consider using a `dataclass` for backend state with fields: host, port, weight, healthy, consecutive_fails, consecutive_successes
- The weighted round-robin can be implemented by creating a list where each backend appears `weight` times

---

## Assignment 2: DNS Caching Resolver

**File:** `exercises/hw_11_02.py`

**Objective:** Implement a local DNS caching resolver that reduces external queries.

### Requirements

1. **UDP DNS Server** (30 points)
   - Listen on UDP port 5353 (non-privileged port)
   - Accept standard DNS queries
   - Parse DNS query packets to extract domain name and query type

2. **Cache Implementation** (30 points)
   - Store DNS responses with their TTL values
   - Automatically expire entries when TTL reaches zero
   - Use a dictionary with structure: `{(domain, type): (response, expiry_time)}`
   - Report cache hits and misses to console

3. **Upstream Resolution** (25 points)
   - Forward cache misses to upstream DNS server (default: 8.8.8.8)
   - Parse response and extract TTL
   - Store in cache before returning to client

4. **Statistics and Management** (15 points)
   - Track and report:
     - Total queries received
     - Cache hit ratio
     - Upstream queries made
   - Implement cache flush via SIGUSR1 signal (or keyboard command on Windows)

### Packet Format Reference

```
DNS Query Format:
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                      ID                       |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                    QDCOUNT                    |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                    ANCOUNT                    |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                    NSCOUNT                    |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                    ARCOUNT                    |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

QR = 0 for query, 1 for response
QDCOUNT = number of questions
ANCOUNT = number of answers
```

### Testing Criteria

```powershell
# Start your DNS caching resolver
python homework/exercises/hw_11_02.py --listen 127.0.0.1:5353 --upstream 8.8.8.8

# First query (cache miss - should forward to upstream)
nslookup google.com 127.0.0.1 -port=5353

# Second query (cache hit - should be instant)
nslookup google.com 127.0.0.1 -port=5353

# Different domain (cache miss)
nslookup github.com 127.0.0.1 -port=5353

# Check resolver reports cache statistics to console
```

### Hints

- Use `struct.pack()` and `struct.unpack()` for binary DNS packet handling
- The `dnspython` library can help parse/create DNS packets, but try implementing parsing manually first for deeper understanding
- TTL is a 32-bit unsigned integer in network byte order
- Consider using `time.time()` plus TTL to calculate expiry timestamps

---

## Grading Rubric

| Criterion | Points | Description |
|-----------|--------|-------------|
| Functionality | 60 | Code works as specified |
| Code Quality | 20 | Clean, documented, follows PEP 8 |
| Error Handling | 10 | Graceful handling of edge cases |
| Report | 10 | Clear explanation of implementation |

### Code Quality Guidelines

- Include docstrings for all functions and classes
- Use type hints where appropriate
- Handle exceptions gracefully (don't let the program crash)
- Log meaningful messages at appropriate levels (INFO, WARNING, ERROR)
- Follow the existing code style in the starter kit

---

## Bonus Challenges (Optional, +10 points each)

### Bonus 1: Connection Pooling

Extend the load balancer to maintain persistent connections to backends instead of creating new connections for each request.

### Bonus 2: DNS over HTTPS (DoH)

Extend the DNS resolver to support upstream queries via HTTPS (RFC 8484) as an alternative to plain UDP.

### Bonus 3: Circuit Breaker Pattern

Implement the circuit breaker pattern in the load balancer:
- **Closed:** Normal operation
- **Open:** After N failures, stop sending requests for T seconds
- **Half-Open:** Allow one test request, return to Closed if successful

---

## Resources

- **Load Balancing Algorithms:** See `docs/theory_summary.md`
- **DNS Protocol:** RFC 1035, `src/exercises/ex_11_03_dns_client.py`
- **Socket Programming:** Python `socket` documentation

---

*NETWORKING class - ASE, Informatics | by Revolvix*
