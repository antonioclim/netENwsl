# 📊 Formative Assessment Guide — Week 7
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> This document consolidates all self-assessment resources for Week 7.
> Use these tools to verify your understanding before the graded assessment.

---

## Quick Assessment Tools

| Tool | Command | Purpose | Time |
|------|---------|---------|------|
| Quiz | `python3 formative/run_quiz.py` | 15 MCQ covering all LOs | 15 min |
| Parsons | `python3 formative/parsons_runner.py` | Code reordering exercises | 20 min |
| Smoke Tests | `python3 tests/smoke_test.py` | Verify environment setup | 2 min |
| Exercise Tests | `python3 tests/test_exercises.py --all` | Validate lab completion | 5 min |

---

## Self-Assessment Checkpoints

### Before Starting the Lab

Complete these checks to ensure you're ready:

- [ ] Docker is running (`docker info` shows no errors)
- [ ] Portainer accessible at http://localhost:9000
- [ ] Wireshark installed and can capture on vEthernet (WSL)
- [ ] Python 3.11+ available (`python3 --version`)
- [ ] Week 7 folder accessible from WSL

**Verification command:**
```bash
python3 setup/verify_environment.py
```

---

### After Exercise 1: Baseline Traffic Capture

**Checkpoint Questions:**

1. ❓ How many TCP packets are in a complete handshake? 
   <details><summary>Answer</summary>3 packets: SYN, SYN-ACK, ACK</details>

2. ❓ What Wireshark filter shows only TCP SYN packets?
   <details><summary>Answer</summary>`tcp.flags.syn == 1 && tcp.flags.ack == 0`</details>

3. ❓ Why do UDP packets have no handshake in your capture?
   <details><summary>Answer</summary>UDP is connectionless - datagrams sent without establishing connection</details>

**Self-Check:**
```bash
python3 tests/test_exercises.py --exercise 1
```

**Expected:** All tests pass (TCP connectivity ✓, TCP echo ✓, UDP send ✓)

---

### After Exercise 2: TCP Filtering with REJECT

**Checkpoint Questions:**

1. ❓ What packet type does REJECT send back to the client?
   <details><summary>Answer</summary>TCP RST or ICMP Destination Unreachable</details>

2. ❓ How does the client experience differ from DROP?
   <details><summary>Answer</summary>REJECT: immediate "Connection refused". DROP: timeout after waiting.</details>

3. ❓ Does the REJECT rule affect UDP traffic?
   <details><summary>Answer</summary>No - the rule is protocol-specific (TCP only)</details>

**Self-Check:**
```bash
python3 tests/test_exercises.py --exercise 2
```

**Expected:** TCP blocked ✓, UDP still works ✓

---

### After Exercise 3: UDP Filtering with DROP

**Checkpoint Questions:**

1. ❓ Why does `udp_sender.py` report success even when packets are dropped?
   <details><summary>Answer</summary>UDP provides no delivery confirmation - sendto() succeeds when handed to network stack</details>

2. ❓ How can you verify UDP packets were actually dropped?
   <details><summary>Answer</summary>Check receiver (no data) or capture at firewall (packets not forwarded)</details>

3. ❓ Which is easier to debug: DROP or REJECT?
   <details><summary>Answer</summary>REJECT - provides immediate feedback about the block</details>

**Self-Check:**
```bash
python3 tests/test_exercises.py --exercise 3
```

---

### After Exercise 4: Application-Layer Packet Filter

**Checkpoint Questions:**

1. ❓ What layer does the packet_filter.py proxy operate at?
   <details><summary>Answer</summary>Application layer (Layer 7) - it reads and forwards TCP streams</details>

2. ❓ How does application-layer filtering differ from iptables?
   <details><summary>Answer</summary>App-layer can inspect content/payloads; iptables only sees headers</details>

3. ❓ What happens to connections from non-allowed IPs?
   <details><summary>Answer</summary>Connection refused by the proxy (or simply not forwarded)</details>

**Self-Check:**
```bash
python3 tests/test_exercises.py --exercise 4
```

---

### After Exercise 5: Defensive Port Probing

**Checkpoint Questions:**

1. ❓ What are the three possible port states from a probe?
   <details><summary>Answer</summary>Open (service listening), Closed (RST received), Filtered (timeout/no response)</details>

2. ❓ Why might all ports show as "filtered"?
   <details><summary>Answer</summary>Default DROP policy, network unreachable, or wrong target IP</details>

3. ❓ How does probe timeout affect scan speed?
   <details><summary>Answer</summary>Longer timeout = slower scan (waiting for each filtered port)</details>

**Self-Check:**
```bash
python3 tests/test_exercises.py --exercise 5
```

---

## Comprehensive Self-Assessment Quiz

Run the interactive quiz to test all learning objectives:

```bash
# Full quiz (15 questions, ~15 minutes)
python3 formative/run_quiz.py

# Quick quiz (5 random questions)
python3 formative/run_quiz.py --random --limit 5

# Focus on specific LOs
python3 formative/run_quiz.py --lo LO1 LO2

# Review mode (see answers immediately)
python3 formative/run_quiz.py --review
```

### Scoring Interpretation

| Score | Grade | Interpretation |
|-------|-------|----------------|
| 90-100% | A | Excellent - ready for assessment |
| 80-89% | B | Good - minor review needed |
| 70-79% | C | Satisfactory - review weak areas |
| 60-69% | D | Needs work - redo exercises |
| <60% | F | Insufficient - restart from theory |

---

## Code Comprehension: Parsons Problems

Test your understanding of code structure without syntax burden:

```bash
# Run all Parsons problems
python3 formative/parsons_runner.py

# Run specific problem
python3 formative/parsons_runner.py --problem P1

# With hints about distractors
python3 formative/parsons_runner.py --hint
```

### Problem Mapping to LOs

| Problem | Title | LO | Difficulty |
|---------|-------|-----|------------|
| P1 | TCP Port Probe | LO1 | Intermediate |
| P2 | Parse iptables Output | LO3 | Intermediate |
| P3 | UDP Send with Error Handling | LO2 | Intermediate |
| P4 | Apply Firewall Profile | LO3 | Advanced |
| P5 | Capture Traffic Summary | LO4 | Intermediate |

---

## Code Tracing Exercises

Work through these manually (pen and paper recommended):

1. **docs/code_tracing.md#exercise-t1** - TCP Client Connection
   - Trace socket states through connection lifecycle
   - Predict packet counts at each step

2. **docs/code_tracing.md#exercise-t2** - Port Probe Logic
   - Understand connect_ex() vs connect()
   - Map return values to port states

3. **docs/code_tracing.md#exercise-t3** - Firewall Rule Processing
   - Trace first-match-wins logic
   - Understand rule order importance

---

## Peer Instruction Questions

Use with a study partner (5-step protocol):

1. **Read** question individually (1 min)
2. **Vote** your answer (30 sec)
3. **Discuss** with partner (2 min)
4. **Re-vote** (30 sec)
5. **Check** solution and explanation

Questions available in: `docs/peer_instruction.md`

| Question | Topic | Target Accuracy |
|----------|-------|-----------------|
| Q1 | DROP vs REJECT | 40-50% |
| Q2 | Port States | 35-45% |
| Q3 | Capture Interface | 50-60% |
| Q4 | TCP Handshake | 60-70% |
| Q5 | UDP Blocking | 45-55% |

---

## Common Misconceptions Checklist

Review these before the exam - `docs/misconceptions.md`:

- [ ] I understand DROP ≠ REJECT (different client experience)
- [ ] I know Closed ≠ Filtered (different network evidence)
- [ ] I know tcpdump only sees selected interface traffic
- [ ] I know Wireshark needs vEthernet (WSL) for Docker traffic
- [ ] I understand UDP sender can't detect dropped packets
- [ ] I know TCP RST can come from server, firewall, or app
- [ ] I know iptables rules don't persist across reboots

---

## Readiness Checklist

Before the graded assessment, ensure:

### Technical Skills
- [ ] Can start/stop lab environment with scripts
- [ ] Can capture traffic with tcpdump or Wireshark
- [ ] Can apply and verify iptables rules
- [ ] Can interpret Wireshark captures for connection issues
- [ ] Can distinguish DROP vs REJECT in captures

### Conceptual Understanding
- [ ] TCP three-way handshake purpose and packets
- [ ] UDP connectionless nature implications
- [ ] Port states (open/closed/filtered) and their evidence
- [ ] Firewall rule ordering importance
- [ ] Application-layer vs network-layer filtering

### Assessment Preparation
- [ ] Completed all 5 lab exercises
- [ ] Passed quiz with ≥70%
- [ ] Solved at least 3/5 Parsons problems
- [ ] Reviewed all misconceptions
- [ ] Practiced code tracing exercises

---

## Additional Resources

| Resource | Path | Purpose |
|----------|------|---------|
| Theory Summary | `docs/theory_summary.md` | Conceptual foundations |
| Concept Analogies | `docs/concept_analogies.md` | Real-world metaphors |
| Commands Cheatsheet | `docs/commands_cheatsheet.md` | Quick reference |
| Troubleshooting | `docs/troubleshooting.md` | Problem solving |
| Glossary | `docs/glossary.md` | Term definitions |

---

*Computer Networks — Week 7: Packet Interception, Filtering and Defensive Port Probing*  
*ASE Bucharest, CSIE | by ing. dr. Antonio Clim*
