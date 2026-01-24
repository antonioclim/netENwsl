# Project 14: Network Security — IDS/IPS Simulation

> **Course:** Computer Networks | **Institution:** ASE Bucharest - CSIE | **Project type:** Main

**Common guides:** [Pair Programming](../docs/common/pair_programming_guide.md) | [Code Quality](../docs/common/code_quality_standards.md) | [Git Workflow](../docs/common/git_workflow_detailed.md)

### 📅 Stage Calendar
| Stage | Week | Deliverables | Score |
|-------|------|--------------|-------|
| **E1** - Design | Week 5 | Specifications + Diagrams | 20% |
| **E2** - Prototype | Week 9 | Partial implementation | 25% |
| **E3** - Final | Week 13 | Complete version | 35% |
| **E4** - Presentation | Week 14 | Live demo | 20% |

**Repository:** `https://github.com/[username]/retele-proiect-14`

---

## 📚 Project Description

Simulate a network environment with IDS (Intrusion Detection) and IPS (Intrusion Prevention) capabilities. Deploy Snort/Suricata in Docker, create custom rules and demonstrate detection and blocking of simulated attacks.

### 🎯 Learning Objectives
- **Configure** IDS/IPS systems
- **Write** custom detection rules
- **Simulate** common network attacks
- **Analyse** alerts and responses

---

## 🎯 Concept Analogies

### IDS vs IPS = Security Camera vs Security Guard
🏠 **Analogy:** 
- **IDS** = Security camera — records and alerts but doesn't stop intruders
- **IPS** = Security guard — sees threat and actively blocks it

💻 **Technical:** IDS monitors (passive), IPS blocks (inline).

### Signatures = Wanted Posters
🏠 **Analogy:** Police have "wanted" posters with specific faces. IDS has signatures with specific packet patterns.

---

## 🗳️ Peer Instruction Questions

### Question 1: Inline vs Passive
**Question:** For IPS to block traffic, where must it be placed?
- A) Anywhere on the network
- B) Inline (traffic passes through it) ✓
- C) On the firewall
- D) On each host

### Question 2: False Positive Impact
**Question:** In IPS, what happens with a false positive?
- A) Alert is logged
- B) Legitimate traffic is blocked ✓
- C) Nothing
- D) System crashes

---

## ❌ Common Misconceptions

### 🚫 "IDS/IPS catches all attacks"
**CORRECT:** Only known signatures or detectable anomalies are caught. Zero-days may slip through.

### 🚫 "More rules = better security"
**CORRECT:** More rules = more processing = potential performance impact and more false positives.

---

## 📖 Glossary
| Term | Definition |
|------|------------|
| **IDS** | Intrusion Detection System |
| **IPS** | Intrusion Prevention System |
| **Signature** | Pattern matching known attacks |
| **Anomaly** | Deviation from baseline |
| **Alert** | Notification of detected event |
| **Snort/Suricata** | Open-source IDS/IPS tools |

---

## 🔨 Implementation Example

```bash
# Snort rule example
# ═══════════════════════════════════════════════════════════════════════════════
# CUSTOM_RULES
# ═══════════════════════════════════════════════════════════════════════════════

# Detect ICMP flood
alert icmp any any -> $HOME_NET any (msg:"ICMP Flood Detected"; \
    threshold:type both, track by_src, count 100, seconds 10; \
    sid:1000001; rev:1;)

# 💭 PREDICTION: What does "count 100, seconds 10" mean?
# Answer: Alert if 100+ ICMP packets from same source in 10 seconds

# Detect SSH brute force
alert tcp any any -> $HOME_NET 22 (msg:"SSH Brute Force Attempt"; \
    flow:to_server,established; \
    threshold:type both, track by_src, count 5, seconds 60; \
    sid:1000002; rev:1;)

# Detect SQL injection attempt
alert http any any -> $HOME_NET any (msg:"SQL Injection Attempt"; \
    content:"SELECT"; nocase; \
    content:"FROM"; nocase; distance:0; \
    content:"WHERE"; nocase; distance:0; \
    sid:1000003; rev:1;)
```

---

## 📚 Laboratory References

Consult these resources from **netENwsl** (https://github.com/antonioclim/netENwsl):

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 13 | `13enWSL/` | Network security, IDS concepts |
| 7 | `07enWSL/` | Packet analysis with Wireshark/Scapy |

---

*Last update: January 2026 — Computer Networks, ASE Bucharest*
