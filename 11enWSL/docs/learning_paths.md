# 🛤️ Learning Paths — Week 11
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> **Purpose:** Differentiated learning paths based on prior experience  
> **Goal:** Optimise learning time whilst ensuring mastery of Learning Objectives

---

## 🎯 Quick Self-Assessment

Answer these questions to determine your path:

| # | Question | Yes | No |
|---|----------|-----|-----|
| 1 | Have you used Docker Compose before? | → | → |
| 2 | Can you explain what a reverse proxy does? | → | → |
| 3 | Have you configured Nginx (or similar) before? | → | → |
| 4 | Do you know TCP/UDP port numbers for common protocols? | → | → |
| 5 | Have you captured network traffic with Wireshark? | → | → |

**Scoring:**
- **0-1 Yes:** Path A (Beginner)
- **2-3 Yes:** Path B (Intermediate)  
- **4-5 Yes:** Path C (Advanced)

---

## 🌱 Path A: Beginner Track

**For:** First-time Docker users, new to networking concepts  
**Time:** 3-3.5 hours  
**Focus:** Foundations, step-by-step guidance

### Phase 1: Theory Foundation (45 min)

```
📖 Reading Order:
1. docs/concept_analogies.md (30 min)
   - Focus on: Restaurant analogy for load balancing
   - Focus on: Post office analogy for DNS
   
2. docs/theory_summary.md §1-3 (15 min)
   - Skim: FTP, DNS, SSH basics
   - Note: Port numbers (21, 53, 22)
```

**Checkpoint A1:** Can you explain what port 53 is used for?

### Phase 2: Environment Setup (20 min)

```bash
# Step-by-step with verification
cd /mnt/d/NETWORKING/WEEK11/11enWSL

# 1. Verify environment
make verify
# ✓ Should show all green checks

# 2. Install dependencies
make install
# ✓ Should complete without errors

# 3. Start Docker
make docker-up
# ✓ Should show 4 containers running

# 4. Verify services
make status
```

**Checkpoint A2:** Run `curl http://localhost:8080/` — what do you see?

### Phase 3: Core Exercises (90 min)

```
Exercise Sequence:
├── Exercise 1: Backend Server (20 min)
│   └── Goal: Understand HTTP request-response
│   
├── Exercise 2: Round-Robin (30 min)  
│   └── Goal: See load balancing in action
│   
├── Checkpoint Break (10 min)
│   └── Complete C1, C2 in docs/formative_assessment.md
│   
└── Exercise 5: Nginx Docker (30 min)
    └── Goal: See production-style load balancer
```

### Phase 4: Assessment (25 min)

```bash
# Run basic-level quiz only
make quiz-basic

# Target: 80%+ correct
```

**If score < 70%:** Re-read `docs/misconceptions.md` §1 (Load Balancing)

### Phase 5: Homework (Optional)

- Complete **HW 11.01** (basic version)
- Skip advanced requirements marked with ⭐

---

## 🌿 Path B: Intermediate Track

**For:** Familiar with Docker, some networking knowledge  
**Time:** 2.5 hours  
**Focus:** Deeper understanding, algorithm comparison

### Phase 1: Targeted Review (20 min)

```
📖 Focus Reading:
1. docs/theory_summary.md §4-5 (Load Balancing, Nginx)
2. docs/misconceptions.md §1 (Common LB mistakes)
```

### Phase 2: Quick Setup (10 min)

```bash
make setup  # Combined install + verify
make lab    # Start full environment
```

### Phase 3: Full Exercise Sequence (80 min)

```
Exercise Sequence:
├── Exercise 1: Backend (10 min) — Quick verification
│   
├── Exercise 2: Round-Robin (20 min)
│   └── Prediction: What distribution for 9 requests to 3 backends?
│   
├── Exercise 3: IP Hash (15 min)
│   └── Prediction: Same client IP → same backend?
│   
├── Exercise 4: Failover (15 min)
│   └── Stop backend_2, observe behaviour
│   
└── Exercise 5: Nginx Docker (20 min)
    └── Modify weights, observe distribution
```

### Phase 4: Code Understanding (20 min)

```
📝 Complete Code Tracing:
- docs/code_tracing.md T1 (Round-Robin)
- docs/code_tracing.md T3 (Health Check)
```

### Phase 5: Full Assessment (20 min)

```bash
make quiz  # All questions

# Target: 85%+ correct
```

### Phase 6: Homework

- Complete **HW 11.01** (full version)
- Attempt ⭐ advanced requirements

---

## 🌳 Path C: Advanced Track

**For:** Experienced with Docker, networking, ready for challenges  
**Time:** 2 hours  
**Focus:** Implementation details, performance analysis

### Phase 1: Direct to Practice (5 min)

```bash
make lab  # Start immediately
```

### Phase 2: Advanced Exercises (60 min)

```
Exercise Sequence (reverse order):
├── Exercise 7: Benchmarking (20 min)
│   └── Compare Python LB vs Nginx performance
│   
├── Exercise 6: DNS Client (25 min)
│   └── Implement manual DNS query construction
│   
└── Exercise 5: Nginx Advanced (15 min)
    └── Configure weighted balancing, health checks
```

### Phase 3: Deep Dive (30 min)

```
📝 Code Tracing (challenging):
- docs/code_tracing.md T4 (IP Hash algorithm)
- docs/code_tracing.md T5 (HTTP Response building)

🔧 Hands-on Challenges:
1. Modify ex_11_02_loadbalancer.py to add weighted round-robin
2. Configure Nginx for least_conn algorithm
3. Capture and analyse DNS query structure in Wireshark
```

### Phase 4: Challenge Quiz (15 min)

```bash
make quiz-advanced  # Advanced questions only

# Target: 90%+ correct
```

### Phase 5: Extended Homework

- Complete **HW 11.01** with all ⭐ requirements
- Attempt **HW 11.02** (advanced)
- **Bonus Challenge:** Implement consistent hashing algorithm

---

## 📊 Learning Objectives Coverage by Path

| LO | Description | Path A | Path B | Path C |
|----|-------------|--------|--------|--------|
| LO1 | Protocol Architecture | ✅ Full | ✅ Full | ⚡ Quick |
| LO2 | Protocol Differences | ✅ Full | ✅ Full | ⚡ Quick |
| LO3 | Implement Load Balancer | 🔹 Basic | ✅ Full | ✅ Extended |
| LO4 | Nginx Configuration | 🔹 Basic | ✅ Full | ✅ Extended |
| LO5 | Traffic Analysis | 🔹 Demo | ✅ Full | ✅ Extended |
| LO6 | Container Architecture | ✅ Full | ✅ Full | ⚡ Quick |
| LO7 | Performance Evaluation | ❌ Skip | 🔹 Basic | ✅ Full |

**Legend:** ✅ Full coverage | 🔹 Partial | ⚡ Quick review | ❌ Optional

---

## 🔄 Path Transitions

### Upgrading Paths

```
Path A → Path B:
  After completing Path A with 80%+ quiz score,
  continue with Path B Phases 3-5

Path B → Path C:
  After completing Path B with 90%+ quiz score,
  continue with Path C Phases 2-5
```

### Struggling? Downgrade

```
Path C struggling → Path B:
  If quiz score < 70%, complete Path B theory review first

Path B struggling → Path A:
  If concepts unclear, start with Path A theory foundation
```

---

## ⏱️ Time Comparison

| Activity | Path A | Path B | Path C |
|----------|--------|--------|--------|
| Theory | 45 min | 20 min | 0 min |
| Setup | 20 min | 10 min | 5 min |
| Exercises | 90 min | 80 min | 60 min |
| Assessment | 25 min | 20 min | 15 min |
| Code Tracing | 0 min | 20 min | 30 min |
| **Total** | **3h** | **2.5h** | **2h** |

---

## 🎓 Success Criteria

### Path A Success
- [ ] Quiz basic: ≥ 80%
- [ ] Can explain round-robin in own words
- [ ] Successfully ran all Docker containers
- [ ] Completed HW 11.01 basic requirements

### Path B Success
- [ ] Quiz full: ≥ 85%
- [ ] Can explain IP hash vs round-robin tradeoffs
- [ ] Modified Nginx weights and verified distribution
- [ ] Completed HW 11.01 full requirements

### Path C Success
- [ ] Quiz advanced: ≥ 90%
- [ ] Can implement custom LB algorithm modification
- [ ] Performance comparison documented
- [ ] Completed HW 11.02 or bonus challenge

---

## 💡 Tips for Each Path

### Path A Tips
- Use `docs/commands_cheatsheet.md` frequently
- Do not skip `docs/troubleshooting.md` if stuck
- Ask questions early — do not struggle alone

### Path B Tips
- Focus on understanding "why" not just "how"
- Compare your predictions with actual results
- Review misconceptions even if quiz score is high

### Path C Tips
- Challenge assumptions — try breaking things
- Benchmark everything quantitatively
- Share interesting findings with classmates

---

## Support

Issues: Open an issue in GitHub

---

*NETWORKING class - ASE, CSIE | Computer Networks Laboratory*  
*Week 11: Application Protocols — FTP, DNS, SSH and Load Balancing*
