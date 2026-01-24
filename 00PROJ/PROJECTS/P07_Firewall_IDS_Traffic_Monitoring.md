# Project 07: Software Firewall with Traffic Monitoring

> **Course:** Computer Networks | **Institution:** ASE Bucharest - CSIE | **Project type:** Main

**Common guides:** [Pair Programming](../docs/common/pair_programming_guide.md) | [Code Quality](../docs/common/code_quality_standards.md) | [Git Workflow](../docs/common/git_workflow_detailed.md)

### 📅 Stage Calendar
| Stage | Week | Deliverables | Score |
|-------|------|--------------|-------|
| **E1** - Design | Week 5 | Specifications + Diagrams | 20% |
| **E2** - Prototype | Week 9 | Partial implementation | 25% |
| **E3** - Final | Week 13 | Complete version | 35% |
| **E4** - Presentation | Week 14 | Live demo | 20% |

**Repository:** `https://github.com/[username]/retele-proiect-07`

---

## 📚 Project Description

Implement a software firewall that filters traffic based on configurable rules (IP, port, protocol) with logging and monitoring capabilities. Combine with basic intrusion detection for suspicious patterns.

### 🎯 Learning Objectives
- **Implement** packet filtering rules
- **Design** rule configuration system
- **Log** and analyse filtered traffic
- **Integrate** basic anomaly detection

---

## 🎯 Concept Analogies

### Firewall Rules = Building Security Policies
🏠 **Analogy:** A building has rules: "Employees can enter floors 1-5, visitors only lobby, deliveries through back door." Each person (packet) is checked against rules in order.

💻 **Technical:** Rules checked top-to-bottom, first match wins.

---

## 🗳️ Peer Instruction Questions

### Question 1: Rule Order
**Scenario:** 
```
Rule 1: ALLOW from 10.0.0.0/8
Rule 2: DENY from 10.0.0.5
```
**Question:** Is 10.0.0.5 allowed?
- A) Yes, Rule 1 matches first ✓
- B) No, Rule 2 is more specific
- C) Depends on protocol
- D) Error: conflicting rules

**Explanation:** First-match wins. Rule order matters!

### Question 2: Stateful vs Stateless
**Question:** Which requires tracking connection state?
- A) Blocking all incoming traffic
- B) Allowing replies to outgoing connections ✓
- C) Blocking specific IP addresses
- D) Allowing specific ports

---

## ❌ Common Misconceptions

### 🚫 "Default deny is always best"
**CORRECT:** Default deny is more secure but requires explicitly allowing legitimate traffic. Default allow is easier but less secure.

### 🚫 "Firewall logs everything automatically"
**CORRECT:** Logging must be explicitly configured and can impact performance.

---

## 📖 Glossary
| Term | Definition |
|------|------------|
| **Stateless** | Each packet judged independently |
| **Stateful** | Tracks connections, allows replies |
| **Default Policy** | Action when no rule matches |
| **Rule Chain** | Ordered list of filtering rules |

---

## 🔨 Implementation Example

```python
# ═══════════════════════════════════════════════════════════════════════════════
# FIREWALL_RULES
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class FirewallRule:
    """Single firewall rule."""
    action: str  # 'allow' or 'deny'
    src_ip: str = '*'
    dst_ip: str = '*'
    protocol: str = '*'
    dst_port: int = None
    
    def matches(self, packet: dict) -> bool:
        """Check if packet matches this rule."""
        # 💭 PREDICTION: What if src_ip='*' and packet has no IP?
        if self.src_ip != '*' and packet.get('src_ip') != self.src_ip:
            return False
        if self.dst_port and packet.get('dst_port') != self.dst_port:
            return False
        return True
```

---

## 📚 Laboratory References

Consult these resources from **netENwsl** (https://github.com/antonioclim/netENwsl):

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 7 | `07enWSL/` | Packet filtering, Scapy, defensive probing |
| 13 | `13enWSL/` | Network security, IDS concepts |

---

*Last update: January 2026 — Computer Networks, ASE Bucharest*
