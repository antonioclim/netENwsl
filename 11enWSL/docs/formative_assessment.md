# 📝 Formative Assessment — Week 11
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Self-assessment questions to verify your understanding before, during, and after the laboratory.

---

## How to Use This Document

1. **Before Lab:** Answer the Pre-Lab questions (5 min)
2. **During Lab:** Complete Checkpoint questions after each exercise
3. **After Lab:** Verify with Post-Lab synthesis questions
4. **Scoring:** Use the rubric at the end for self-evaluation

💡 **Tip:** Run `python formative/run_quiz.py` for an interactive version!

---

## Pre-Lab Assessment (5 questions)

Answer these BEFORE starting the exercises. Write your predictions.

### PL-1: Port Numbers
**Question:** Match each protocol with its default port(s):

| Protocol | Your Answer | Correct |
|----------|-------------|---------|
| FTP Control | ___ | 21 |
| FTP Data (active) | ___ | 20 |
| DNS | ___ | 53 |
| SSH | ___ | 22 |
| HTTP | ___ | 80 |

### PL-2: Load Balancing Prediction
**Question:** You have 3 backends and send 9 requests using round-robin. How many requests will each backend receive?

- Your prediction: ___
- Expected: 3-3-3 (equal distribution)

### PL-3: Session Affinity
**Question:** If you use IP hash and send 5 requests from the same client IP, how many different backends will receive requests?

- Your prediction: ___
- Expected: 1 (all go to same backend)

### PL-4: Failure Detection
**Question:** With default Nginx settings, if a backend crashes, will the FIRST request to that backend succeed or fail?

- Your prediction: [ ] Succeed [ ] Fail
- Expected: Fail (passive health checks)

### PL-5: DNS Caching
**Question:** If a DNS record has TTL=60 seconds, will ALL resolvers refresh after exactly 60 seconds?

- Your prediction: [ ] Yes [ ] No
- Expected: No (resolvers may enforce minimum TTL)

---

## Exercise Checkpoints

### Checkpoint 1: Backend Servers (After Exercise 1)

**C1-1:** Run this command and observe the output:
```bash
curl http://localhost:8081/
```

**Expected format:** `Backend 1 | Host: ... | Time: ... | Request #1`

**Self-check:**
- [ ] Response contains "Backend 1"
- [ ] Response includes timestamp
- [ ] Response shows request counter

**C1-2:** What HTTP header identifies the backend?
- Answer: `X-Backend-ID`

---

### Checkpoint 2: Round-Robin (After Exercise 2)

**C2-1:** Run 6 requests and record which backend handles each:
```bash
for i in {1..6}; do curl -s http://localhost:8080/ | grep Backend; done
```

**Your observations:**

| Request # | Backend |
|-----------|---------|
| 1 | ___ |
| 2 | ___ |
| 3 | ___ |
| 4 | ___ |
| 5 | ___ |
| 6 | ___ |

**Expected pattern:** 1 → 2 → 3 → 1 → 2 → 3

**Self-check:**
- [ ] Pattern repeats cyclically
- [ ] Each backend received exactly 2 requests

---

### Checkpoint 3: IP Hash (After Exercise 3)

**C3-1:** With IP hash enabled, run 5 requests:
```bash
for i in {1..5}; do curl -s http://localhost:8080/ | grep Backend; done
```

**Your observations:**

| Request # | Backend |
|-----------|---------|
| 1-5 | All: ___ |

**Expected:** All 5 requests go to the SAME backend

**C3-2:** Why do all requests go to the same backend?
- Answer: IP hash produces deterministic result for same client IP

---

### Checkpoint 4: Failover (After Exercise 4)

**C4-1:** Stop Backend 2 and send a request:
```bash
docker stop s11_backend_2
curl http://localhost:8080/
```

**Your observation:**
- First request result: [ ] Success (200) [ ] Failure (502)

**Expected:** First request MAY return 502 if routed to dead backend

**C4-2:** Send 6 more requests. Which backends respond?
- Backends seen: ___
- Expected: Only Backend 1 and Backend 3

---

### Checkpoint 5: Nginx Docker (After Exercise 5)

**C5-1:** Check Nginx health endpoint:
```bash
curl http://localhost:8080/health
```

**Expected:** HTTP 200 OK

**C5-2:** Check Nginx status:
```bash
curl http://localhost:8080/nginx_status
```

**Self-check:**
- [ ] Shows "Active connections"
- [ ] Shows request statistics

---

### Checkpoint 6: DNS Client (After Exercise 6)

**C6-1:** Query an A record:
```bash
python3 src/exercises/ex_11_03_dns_client.py google.com A
```

**Your observation:**
- IP returned: ___
- TTL: ___

**C6-2:** Query MX records:
```bash
python3 src/exercises/ex_11_03_dns_client.py google.com MX
```

**Self-check:**
- [ ] Multiple MX records returned
- [ ] Each has priority value

---

### Checkpoint 7: Benchmarking (After Exercise 7)

**C7-1:** Run a quick benchmark:
```bash
python3 src/exercises/ex_11_02_loadbalancer.py loadgen --url http://localhost:8080/ --n 100 --c 5
```

**Your observations:**

| Metric | Value |
|--------|-------|
| Requests/second | ___ |
| Mean latency | ___ ms |
| 95th percentile | ___ ms |

**Self-check:**
- [ ] All 100 requests completed
- [ ] Latency is reasonable (<100ms for local)

---

## Post-Lab Synthesis (5 questions)

### S-1: Algorithm Comparison
**Question:** When would you choose each algorithm?

| Algorithm | Best Use Case |
|-----------|---------------|
| Round-robin | ___ |
| Least connections | ___ |
| IP hash | ___ |

**Expected answers:**
- Round-robin: Homogeneous backends, stateless requests
- Least connections: Variable request processing times
- IP hash: Session affinity required, no shared session store

---

### S-2: Failure Modes
**Question:** What HTTP status codes indicate these problems?

| Problem | Status Code |
|---------|-------------|
| Backend unreachable | ___ |
| All backends down | ___ |
| Backend too slow | ___ |

**Expected:** 502, 503, 504

---

### S-3: FTP Architecture
**Question:** Draw the FTP connection model:

```
Client                     Server
  │                          │
  │◄────── ___ (port ___) ──►│  Control
  │                          │
  │◄────── ___ (port ___) ──►│  Data
```

**Expected:** Control (21), Data (20 or ephemeral)

---

### S-4: DNS Resolution
**Question:** Order the DNS resolution steps (1-4):

| Step | Order |
|------|-------|
| Query root servers | ___ |
| Query TLD servers (.com) | ___ |
| Query local resolver | ___ |
| Query authoritative server | ___ |

**Expected:** 3 → 1 → 2 → 4

---

### S-5: SSH Tunnel Security
**Question:** In this SSH tunnel, which segments are encrypted?

```
Browser → localhost:8080 → SSH Tunnel → jumphost → website:80
         [A]              [B]          [C]
```

- Encrypted segments: ___
- Expected: Only [B] (the SSH tunnel)

---

## Self-Scoring Rubric

### Pre-Lab (5 points)
| Score | Criteria |
|-------|----------|
| 5 | All 5 predictions correct |
| 4 | 4 predictions correct |
| 3 | 3 predictions correct |
| 2 | 2 predictions correct |
| 1 | 1 prediction correct |
| 0 | No correct predictions |

### Checkpoints (7 points)
| Score | Criteria |
|-------|----------|
| 7 | All checkpoints completed successfully |
| 5-6 | Most checkpoints completed |
| 3-4 | Half completed |
| 1-2 | Few completed |
| 0 | None completed |

### Synthesis (5 points)
| Score | Criteria |
|-------|----------|
| 5 | All synthesis questions correct |
| 4 | 4 questions correct |
| 3 | 3 questions correct |
| 2 | 2 questions correct |
| 1 | 1 question correct |

### Total Score Interpretation

| Total (17) | Level | Recommendation |
|------------|-------|----------------|
| 15-17 | Excellent | Ready for homework |
| 12-14 | Good | Review weak areas |
| 9-11 | Satisfactory | Re-read theory, redo exercises |
| <9 | Needs work | Seek help, restart from beginning |

---

## Quick Reference

For detailed explanations of any concept:
- **Theory:** `docs/theory_summary.md`
- **Misconceptions:** `docs/misconceptions.md`
- **Commands:** `docs/commands_cheatsheet.md`
- **Troubleshooting:** `docs/troubleshooting.md`

---

*NETWORKING class - ASE, Informatics | Computer Networks Laboratory*
*Week 11: Application Protocols — FTP, DNS, SSH and Load Balancing*
