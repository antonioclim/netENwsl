# 📝 Formative Assessment — Week 11
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Self-assessment questions to verify your understanding before, during and after the laboratory.

---

## How to Use This Document

1. **Before Lab:** Answer Pre-Lab questions (5 min)
2. **During Lab:** Complete Checkpoint questions after each exercise
3. **After Lab:** Verify with Post-Lab synthesis questions
4. **Scoring:** Use the rubric at the end for self-evaluation

💡 **Tip:** Run `python formative/run_quiz.py` for an interactive version!

---

## Pre-Lab Assessment (5 questions)

Answer these BEFORE starting the exercises.

### PL-1: Port Numbers
Match each protocol with its default port(s):

| Protocol | Your Answer | Correct |
|----------|-------------|---------|
| FTP Control | ___ | 21 |
| FTP Data (active) | ___ | 20 |
| DNS | ___ | 53 |
| SSH | ___ | 22 |

### PL-2: Load Balancing Prediction
You have 3 backends and send 9 requests using round-robin. How many requests will each backend receive?
- Your prediction: ___
- Expected: 3-3-3

### PL-3: Session Affinity
If you use IP hash and send 5 requests from the same client IP, how many different backends will receive requests?
- Your prediction: ___
- Expected: 1 (all go to same backend)

### PL-4: Failure Detection
With default Nginx settings, if a backend crashes, will the FIRST request to that backend succeed or fail?
- [ ] Succeed [ ] Fail
- Expected: Fail (passive health checks)

### PL-5: DNS Caching
If a DNS record has TTL=60 seconds, will ALL resolvers refresh after exactly 60 seconds?
- [ ] Yes [ ] No
- Expected: No (resolvers may enforce minimum TTL)

---

## Exercise Checkpoints

### Checkpoint 1: Backend Servers (After Exercise 1)

Run this command and observe:
```bash
curl http://localhost:8081/
```

**Self-check:**
- [ ] Response contains "Backend 1"
- [ ] Response includes timestamp
- [ ] Response shows request counter

### Checkpoint 2: Round-Robin (After Exercise 2)

Run 6 requests:
```bash
for i in {1..6}; do curl -s http://localhost:8080/ | grep Backend; done
```

**Expected pattern:** 1 → 2 → 3 → 1 → 2 → 3

### Checkpoint 3: IP Hash (After Exercise 3)

With IP hash enabled, run 5 requests:
```bash
for i in {1..5}; do curl -s http://localhost:8080/ | grep Backend; done
```

**Expected:** All 5 requests go to the SAME backend

### Checkpoint 4: Failover (After Exercise 4)

Stop Backend 2:
```bash
docker stop s11_backend_2
curl http://localhost:8080/
```

First request may return 502 if routed to dead backend.

### Checkpoint 5: Nginx Docker (After Exercise 5)

Check Nginx health:
```bash
curl http://localhost:8080/health
```
**Expected:** HTTP 200 OK

### Checkpoint 6: DNS Client (After Exercise 6)

Query an A record:
```bash
python3 src/exercises/ex_11_03_dns_client.py google.com A
```

### Checkpoint 7: Benchmarking (After Exercise 7)

```bash
python3 src/exercises/ex_11_02_loadbalancer.py loadgen --url http://localhost:8080/ --n 100 --c 5
```

---

## Post-Lab Synthesis

### S-1: Algorithm Comparison

| Algorithm | Best Use Case |
|-----------|---------------|
| Round-robin | Homogeneous backends, stateless requests |
| Least connections | Variable request processing times |
| IP hash | Session affinity required |

### S-2: Failure Modes

| Problem | Status Code |
|---------|-------------|
| Backend unreachable | 502 |
| All backends down | 503 |
| Backend too slow | 504 |

### S-3: SSH Tunnel Security

```
Browser → localhost:8080 → SSH Tunnel → jumphost → website:80
         [A]              [B]          [C]
```
Only segment [B] is encrypted.

---

## Self-Scoring Rubric

| Total (17) | Level | Recommendation |
|------------|-------|----------------|
| 15-17 | Excellent | Ready for homework |
| 12-14 | Good | Review weak areas |
| 9-11 | Satisfactory | Re-read theory |
| <9 | Needs work | Seek help |

---

## Reflection Prompts

After completing the lab:

1. What surprised you most about load balancer behaviour?
2. Which misconception did you hold before starting?
3. How does DNS caching affect your understanding of "instant" updates?

---

*NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim*
