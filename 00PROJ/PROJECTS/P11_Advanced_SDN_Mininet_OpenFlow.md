# Project 11: Advanced SDN with Mininet and OpenFlow

> **Course:** Computer Networks | **Institution:** ASE Bucharest - CSIE | **Project type:** Main

**Common guides:** [Pair Programming](../docs/common/pair_programming_guide.md) | [Code Quality](../docs/common/code_quality_standards.md) | [Git Workflow](../docs/common/git_workflow_detailed.md)

### 📅 Stage Calendar
| Stage | Week | Deliverables | Score |
|-------|------|--------------|-------|
| **E1** - Design | Week 5 | Specifications + Diagrams | 20% |
| **E2** - Prototype | Week 9 | Partial implementation | 25% |
| **E3** - Final | Week 13 | Complete version | 35% |
| **E4** - Presentation | Week 14 | Live demo | 20% |

**Repository:** `https://github.com/[username]/retele-proiect-11`

---

## 📚 Project Description

Extend basic SDN concepts with advanced features: QoS implementation, traffic engineering, multi-path routing and network slicing using OpenFlow 1.3+ features.

### 🎯 Learning Objectives
- **Implement** QoS policies using OpenFlow meters
- **Design** multi-path routing algorithms
- **Configure** network slicing for traffic isolation
- **Measure** performance impact of SDN policies

---

## 🎯 Concept Analogies

### QoS = Highway Lane Management
🏠 **Analogy:** Highways have express lanes (high priority), regular lanes and truck lanes (low priority). Traffic is directed based on type.

💻 **Technical:** Different queues/meters for different traffic classes.

### Network Slicing = Apartment Building
🏠 **Analogy:** One building (infrastructure) houses multiple tenants (slices) with isolated utilities (bandwidth, routes).

---

## 🗳️ Peer Instruction Questions

### Question 1: OpenFlow Meters
**Question:** What do OpenFlow meters control?
- A) Packet size
- B) Packet rate (bandwidth limiting) ✓
- C) Packet content
- D) Packet priority

### Question 2: Multi-path Routing
**Question:** Why use multiple paths for same destination?
- A) Redundancy only
- B) Load balancing and increased throughput ✓
- C) Security
- D) Simplicity

---

## ❌ Common Misconceptions

### 🚫 "QoS guarantees bandwidth"
**CORRECT:** QoS prioritises and limits, but can't create bandwidth that doesn't exist.

### 🚫 "More paths = better performance"
**CORRECT:** More paths help if properly load-balanced; otherwise may cause reordering issues.

---

## 📖 Glossary
| Term | Definition |
|------|------------|
| **QoS** | Quality of Service — traffic prioritisation |
| **Meter** | OpenFlow bandwidth limiter |
| **ECMP** | Equal-Cost Multi-Path routing |
| **Network Slice** | Isolated virtual network partition |

---

## 🔨 Implementation Example

```python
# ═══════════════════════════════════════════════════════════════════════════════
# QOS_METER
# ═══════════════════════════════════════════════════════════════════════════════
def install_rate_limiter(self, dpid: int, meter_id: int, rate_kbps: int) -> None:
    """
    Install OpenFlow meter for rate limiting.
    
    Args:
        dpid: Switch datapath ID
        meter_id: Meter identifier
        rate_kbps: Rate limit in Kbps
    """
    # 💭 PREDICTION: What happens to excess traffic?
    # Answer: Dropped (or marked, depending on band type)
    
    bands = [
        parser.OFPMeterBandDrop(rate=rate_kbps, burst_size=10)
    ]
    
    mod = parser.OFPMeterMod(
        datapath=dp,
        command=ofproto.OFPMC_ADD,
        meter_id=meter_id,
        bands=bands
    )
    dp.send_msg(mod)
```

---

## 📚 Laboratory References

Consult these resources from **netENwsl** (https://github.com/antonioclim/netENwsl):

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 6 | `06enWSL/` | SDN, OpenFlow, OS-Ken controller |
| 11 | `11enWSL/` | Load balancing concepts |

---

*Last update: January 2026 — Computer Networks, ASE Bucharest*
