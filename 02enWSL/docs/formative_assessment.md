# 📝 Formative Assessment — Week 2: Architectural Models and Socket Programming

> NETWORKING class — ASE, CSIE Bucharest  
> Computer Networks Laboratory | by ing. dr. Antonio Clim

---

## 🎯 Purpose

This document provides **self-assessment tools** integrated into your learning workflow. Use these checkpoints to:

1. **Identify gaps** before starting exercises
2. **Monitor progress** during the lab session
3. **Consolidate learning** after completion
4. **Prepare for summative assessment** (exam/project)

---

## ⏱️ When to Use This Document

| Phase | Section | Time | Purpose |
|-------|---------|------|---------|
| Before lab | Pre-Lab Knowledge Check | 5 min | Identify what to review |
| During lab | Exercise Checkpoints | 2 min each | Verify understanding |
| After lab | Post-Lab Reflection | 10 min | Consolidate learning |
| Before exam | Mastery Checklist | 15 min | Identify revision needs |

---

## 📋 Pre-Lab Knowledge Check (5 minutes)

**Instructions:** Complete this BEFORE starting the laboratory. Be honest — this helps you focus your learning.

### Self-Assessment Grid

| # | Concept | I know this well | I think I know | I need to learn |
|---|---------|------------------|----------------|-----------------|
| 1 | How many layers does the OSI model have? | □ | □ | □ |
| 2 | What is the difference between TCP and UDP? | □ | □ | □ |
| 3 | What does `SOCK_STREAM` mean in Python? | □ | □ | □ |
| 4 | What is a three-way handshake? | □ | □ | □ |
| 5 | What does `bind()` do vs `connect()`? | □ | □ | □ |
| 6 | Why do we use `SO_REUSEADDR`? | □ | □ | □ |
| 7 | What happens if I bind to `127.0.0.1` vs `0.0.0.0`? | □ | □ | □ |

### Interpretation Guide

| "I know this well" count | Recommended action |
|--------------------------|-------------------|
| 0-2 | Read `docs/theory_summary.md` thoroughly before exercises |
| 3-4 | Skim theory, focus on weak areas |
| 5-6 | Start exercises directly, refer to theory as needed |
| 7 | You are well prepared — aim for deeper understanding |

### Quick Answers (check after self-assessment)

<details>
<summary>Click to reveal answers</summary>

1. **7 layers** (Physical, Data Link, Network, Transport, Session, Presentation, Application)
2. **TCP**: connection-oriented, reliable, ordered. **UDP**: connectionless, best-effort, no ordering
3. **SOCK_STREAM** = TCP socket (reliable byte stream)
4. **Three-way handshake**: SYN → SYN-ACK → ACK (establishes TCP connection)
5. **bind()**: assigns local address to socket. **connect()**: initiates connection to remote address
6. **SO_REUSEADDR**: allows rebinding to a port in TIME_WAIT state
7. **127.0.0.1**: accepts only local connections. **0.0.0.0**: accepts from all interfaces

</details>

---

## 🔬 During-Lab Checkpoints

### After Exercise 1: TCP Concurrent Server

**Time check:** You should reach this point within 45 minutes of starting.

#### Comprehension Checkpoint

| # | Verification | ✓ |
|---|--------------|---|
| 1 | I ran the TCP server in threaded mode | □ |
| 2 | I connected with a client and saw the response | □ |
| 3 | I observed the three-way handshake in Wireshark | □ |
| 4 | I understand why `SO_REUSEADDR` prevents "Address in use" errors | □ |
| 5 | I can explain why threaded mode handles concurrent clients faster | □ |

#### Prediction Verification

Before running the load test, I predicted:
- Iterative server with 10 clients, 100ms each: _____ ms total
- Threaded server with 10 clients, 100ms each: _____ ms total

After running:
- Iterative actual: _____ ms
- Threaded actual: _____ ms
- My prediction was: □ Correct □ Close □ Wrong

**If wrong, why?** _________________________________________________

#### Wireshark Observation Checklist

| Packet type | Found? | Count |
|-------------|--------|-------|
| SYN (client → server) | □ | ___ |
| SYN-ACK (server → client) | □ | ___ |
| ACK (completing handshake) | □ | ___ |
| PSH-ACK (data packets) | □ | ___ |
| FIN (connection close) | □ | ___ |

---

### After Exercise 2: UDP Server

**Time check:** You should reach this point within 30 minutes after Exercise 1.

#### Comprehension Checkpoint

| # | Verification | ✓ |
|---|--------------|---|
| 1 | I ran the UDP server and sent ping/upper/reverse commands | □ |
| 2 | I observed UDP packets in Wireshark (no handshake!) | □ |
| 3 | I understand that UDP `sendto()` succeeds even if nobody listens | □ |
| 4 | I can explain when to choose UDP over TCP | □ |
| 5 | I understand that `recvfrom()` returns both data AND sender address | □ |

#### Compare TCP vs UDP

Fill in from your observations:

| Aspect | TCP (Exercise 1) | UDP (Exercise 2) |
|--------|------------------|------------------|
| Packets before first data | ___ | ___ |
| Header overhead | ___ bytes | ___ bytes |
| Error if server not running | _______________ | _______________ |
| Response to client | Guaranteed | ____________ |

---

### After Exercise 3: Traffic Capture and Analysis

**Time check:** You should complete this within 25 minutes.

#### Comprehension Checkpoint

| # | Verification | ✓ |
|---|--------------|---|
| 1 | I captured traffic with Wireshark on the correct interface | □ |
| 2 | I applied display filters to isolate TCP/UDP traffic | □ |
| 3 | I used "Follow TCP Stream" to see conversation | □ |
| 4 | I saved a PCAP file for later analysis | □ |
| 5 | I can identify the encapsulation layers in a packet | □ |

#### Encapsulation Identification

In a captured TCP packet, identify the layers:

```
Layer 1 (Physical): ________________________________
Layer 2 (Data Link): _______________________________ (hint: MAC addresses)
Layer 3 (Network): _________________________________ (hint: IP addresses)
Layer 4 (Transport): _______________________________ (hint: port numbers)
Layer 7 (Application): _____________________________ (hint: your message)
```

---

## 🪞 Post-Lab Reflection (10 minutes)

**Instructions:** Complete this immediately after the lab while the experience is fresh.

### Learning Reflection

**1. My biggest "Aha!" moment today was:**

_________________________________________________________________

_________________________________________________________________

**2. The concept I found most challenging was:**

_________________________________________________________________

_________________________________________________________________

**3. Something I would explain differently to a friend:**

_________________________________________________________________

_________________________________________________________________

**4. A real-world application I now understand better:**

_________________________________________________________________

_________________________________________________________________

### Misconception Check

Did you fall into any of these common traps? (Check all that apply)

- [ ] I thought TCP preserves message boundaries (it does not — byte stream!)
- [ ] I thought UDP cannot receive replies (it can — same socket)
- [ ] I thought `127.0.0.1` and `0.0.0.0` are the same for bind (they are not)
- [ ] I thought each `send()` triggers a new handshake (only `connect()` does)
- [ ] I thought threading always makes servers faster (not for 1 client)
- [ ] I thought `close()` immediately frees the port (TIME_WAIT exists)

**If you checked any, review:** `docs/misconceptions.md`

### Connection to Future Topics

How does Week 2 content connect to later weeks?

| This week's concept | Future application |
|--------------------|-------------------|
| TCP three-way handshake | Week 10: TLS handshake builds on this |
| UDP connectionless | Week 7: DNS uses UDP for queries |
| Socket options | Week 11: Load balancing socket options |
| Threading | Week 8: HTTP server concurrency |

---

## ✅ Mastery Checklist (Before Week 3)

Use this checklist to verify readiness for the next lab.

### Foundational Skills (Required for Week 3)

| Skill | Confident? | Verified? |
|-------|------------|-----------|
| I can write a TCP echo server from memory | □ | □ |
| I can write a UDP echo server from memory | □ | □ |
| I can use Wireshark to capture and filter traffic | □ | □ |
| I can explain TCP vs UDP to a non-technical person | □ | □ |
| I can debug "Address already in use" errors | □ | □ |

### Intermediate Skills (Expected)

| Skill | Confident? | Verified? |
|-------|------------|-----------|
| I can implement concurrent TCP handling with threading | □ | □ |
| I can explain why TCP does not preserve message boundaries | □ | □ |
| I can design a simple text-based protocol | □ | □ |
| I can use `ss` to inspect socket states | □ | □ |

### Advanced Skills (Stretch Goals)

| Skill | Confident? | Verified? |
|-------|------------|-----------|
| I can benchmark iterative vs threaded server performance | □ | □ |
| I can implement proper timeout handling | □ | □ |
| I can explain when thread pools are better than per-connection threads | □ | □ |

### Verification Methods

- **"Confident"**: You believe you can do this
- **"Verified"**: You have actually done it successfully (not just read about it)

**Goal:** All "Required" skills should be both Confident ✓ and Verified ✓

---

## 📊 Self-Scoring Guide

After completing the lab, score yourself:

| Category | Max Points | Your Score |
|----------|------------|------------|
| Pre-lab assessment completed honestly | 10 | ___ |
| Exercise 1 checkpoints (5 items × 2) | 10 | ___ |
| Exercise 2 checkpoints (5 items × 2) | 10 | ___ |
| Exercise 3 checkpoints (5 items × 2) | 10 | ___ |
| Wireshark observations filled | 10 | ___ |
| Post-lab reflection completed | 20 | ___ |
| Mastery checklist reviewed | 10 | ___ |
| Quiz score (`make quiz`) | 20 | ___ |
| **Total** | **100** | **___** |

### Interpretation

| Score | Status | Next Steps |
|-------|--------|------------|
| 90-100 | Excellent | Ready for Week 3, consider helping peers |
| 75-89 | Good | Review weak areas, redo quiz |
| 60-74 | Satisfactory | Revisit exercises, read misconceptions |
| <60 | Needs work | Schedule office hours, redo lab |

---

## 🔗 Related Resources

| Resource | Purpose | Location |
|----------|---------|----------|
| Theory summary | Quick reference | `docs/theory_summary.md` |
| Misconceptions | Common errors | `docs/misconceptions.md` |
| Interactive quiz | Test knowledge | `make quiz` |
| Peer instruction | Discussion prompts | `docs/peer_instruction.md` |
| Code tracing | Predict output | `docs/code_tracing.md` |
| Visual diagrams | Concept visualisation | `docs/images/` |

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
