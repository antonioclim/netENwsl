# Project 06: SDN with Mininet and OpenFlow Controller

> **Course:** Computer Networks | **Institution:** ASE Bucharest - CSIE | **Project type:** Main

**Common guides:** [Pair Programming](../docs/common/pair_programming_guide.md) | [Code Quality](../docs/common/code_quality_standards.md) | [Git Workflow](../docs/common/git_workflow_detailed.md)

### 📅 Stage Calendar
| Stage | Week | Deliverables | Score |
|-------|------|--------------|-------|
| **E1** - Design | Week 5 | Specifications + Diagrams | 20% |
| **E2** - Prototype | Week 9 | Partial implementation | 25% |
| **E3** - Final | Week 13 | Complete version | 35% |
| **E4** - Presentation | Week 14 | Live demo | 20% |

**Repository:** `https://github.com/[username]/retele-proiect-06`

---

## 📚 Project Description

Build an SDN controller that manages network topology discovery, implements learning switch functionality and provides basic traffic engineering capabilities using OpenFlow.

### 🎯 Learning Objectives
- **Develop** OpenFlow controller applications
- **Implement** topology discovery mechanisms
- **Create** flow installation policies
- **Monitor** network state and statistics

---

## 🎯 Concept Analogies

### Learning Switch = Library Card System
🏠 **Analogy:** A library learns which shelf each book belongs to by tracking returns. After seeing a book returned to shelf A, it knows where to find it next time.

💻 **Technical:** Switch learns MAC-to-port mapping by observing source addresses.

---

## 🗳️ Peer Instruction Questions

### Question 1: Flow Priority
**Question:** Two flow rules match a packet. Which one applies?
- A) First installed
- B) Higher priority value ✓
- C) More specific match
- D) Random selection

**Correct:** B — OpenFlow uses explicit priority field.

### Question 2: Table-Miss
**Question:** What is the default action when no flow matches?
- A) Drop the packet ✓ (in OpenFlow 1.3+)
- B) Flood to all ports
- C) Send to controller
- D) Forward to port 1

**Explanation:** Default is drop. You must install a table-miss rule to send to controller.

---

## ❌ Common Misconceptions

### 🚫 "Learning switch = SDN benefit"
**WRONG:** Learning switch is basic functionality — real SDN value is in programmable policies, centralised control and network-wide optimisation.

### 🚫 "Controller handles every packet"
**CORRECT:** Controller installs rules so switches handle most traffic autonomously.

---

## 📖 Glossary
| Term | Definition |
|------|------------|
| **Learning Switch** | Maps MAC addresses to ports dynamically |
| **Topology Discovery** | Finding network structure via LLDP |
| **Flow Statistics** | Packet/byte counters per flow |

---

## 🔨 Implementation Example

```python
# ═══════════════════════════════════════════════════════════════════════════════
# TOPOLOGY_DISCOVERY
# ═══════════════════════════════════════════════════════════════════════════════
def send_lldp(self, dpid: int, port: int) -> None:
    """Send LLDP packet for topology discovery."""
    # Create LLDP packet with switch ID and port
    lldp = create_lldp_packet(dpid, port)
    
    # 💭 PREDICTION: Where will this packet go?
    # Answer: To connected switch, which sends PacketIn
    self.send_packet_out(dpid, port, lldp)
```

---

## 📚 Laboratory References

Consult these resources from **netENwsl** (https://github.com/antonioclim/netENwsl):

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 6 | `06enWSL/` | SDN architecture, OpenFlow 1.3, OS-Ken |
| 7 | `07enWSL/` | Packet analysis with Wireshark |

---

*Last update: January 2026 — Computer Networks, ASE Bucharest*
