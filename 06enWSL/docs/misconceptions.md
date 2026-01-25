# ❌ Common Misconceptions — Week 6

## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> This document lists common misunderstandings about NAT, SDN and how to correct them. I recommend reviewing this before the lab session — it will save debugging time.

---

## NAT and PAT Misconceptions

### 🚫 Misconception 1: "NAT provides security"

**WRONG:** "Our network is secure because we use NAT — attackers cannot reach our internal hosts."

**CORRECT:** NAT provides *obscurity*, not *security*. Whilst NAT does block unsolicited inbound connections (because there is no conntrack entry to map them), it does not:
- Inspect packet contents for malware
- Block attacks initiated from inside the network
- Prevent phishing or social engineering
- Encrypt traffic
- Detect intrusions

| Aspect | NAT | Firewall |
|--------|-----|----------|
| Blocks unsolicited inbound | ✓ | ✓ |
| Inspects packet contents | ✗ | ✓ |
| Blocks outbound malware | ✗ | ✓ |
| Logs security events | ✗ | ✓ |
| Application-layer filtering | ✗ | ✓ |

**Why this matters:** Organisations relying solely on NAT for security are vulnerable to insider threats, malware that phones home and attacks via legitimate-looking outbound connections.

This confusion comes up every semester. I find it helps to ask: "If an employee clicks a malicious link, does NAT stop the malware from calling home?" The answer is no.

---

### 🚫 Misconception 2: "NAT preserves the original source port"

**WRONG:** "If my application uses port 12345, the server will see port 12345."

**CORRECT:** The NAT router selects a source port from its available pool. It *may* reuse your original port if available, but there is no guarantee.

**Practical verification:**
```bash
# From two different internal hosts, connect using the same local port
h1 python3 -c "import socket; s=socket.socket(); s.bind(('',12345)); s.connect(('203.0.113.2',5000))"
h2 python3 -c "import socket; s=socket.socket(); s.bind(('',12345)); s.connect(('203.0.113.2',5000))"

# On the server, you will see DIFFERENT source ports for each connection
# Both h1 and h2 used port 12345 internally, but the NAT assigned different external ports
```

**Why this matters:** Applications that assume port preservation (some P2P protocols, certain VoIP implementations) may fail behind NAT. This usually breaks things in subtle ways that are hard to debug.

---

### 🚫 Misconception 3: "Private IP addresses are visible to external hosts"

**WRONG:** "The server at 8.8.8.8 can see that the request came from 192.168.1.10."

**CORRECT:** Private addresses (RFC 1918) are *never* visible outside the NAT boundary. The external server only sees the NAT router's public IP address.

| What internal host sends | What external server sees |
|--------------------------|---------------------------|
| Src: 192.168.1.10:45678 | Src: 203.0.113.1:50001 |
| Dst: 8.8.8.8:443 | Dst: 8.8.8.8:443 |

**Why this matters:** This is actually a privacy benefit of NAT — external servers cannot directly identify individual internal hosts.

---

### 🚫 Misconception 4: "Conntrack entries are permanent"

**WRONG:** "Once a NAT mapping is created, it stays forever."

**CORRECT:** Conntrack entries have timeouts. TCP established connections typically timeout after 5 days of inactivity; UDP after 30 seconds to 2 minutes.

**Practical verification:**
```bash
# Check conntrack timeout values
sysctl net.netfilter.nf_conntrack_tcp_timeout_established
sysctl net.netfilter.nf_conntrack_udp_timeout

# Watch entries expire
watch -n 1 'conntrack -L | wc -l'
```

**Why this matters:** Long-running connections need keepalive packets to prevent NAT timeout. VoIP and gaming applications often suffer from this.

---

## SDN Misconceptions

### 🚫 Misconception 5: "The SDN controller forwards packets"

**WRONG:** "Every packet goes through the controller."

**CORRECT:** The controller only *installs rules*. The switches (data plane) do the actual forwarding at line rate. The controller is only contacted for:
- First packet of a new flow (table-miss)
- Packets explicitly sent to controller
- Statistics queries

```
┌─────────────────────────────────────────────────────────────┐
│                     CONTROL PLANE                            │
│   ┌───────────────────────────────────────────────────────┐ │
│   │  Controller (OS-Ken)                                  │ │
│   │  - Computes paths                                     │ │
│   │  - Installs flow rules                                │ │
│   │  - Handles table-miss events                          │ │
│   └───────────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────────┘
                         │ OpenFlow (rules only)
┌────────────────────────▼────────────────────────────────────┐
│                      DATA PLANE                              │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│   │  Switch s1  │──│  Switch s2  │──│  Switch s3  │        │
│   │  (forwards  │  │  (forwards  │  │  (forwards  │        │
│   │   packets)  │  │   packets)  │  │   packets)  │        │
│   └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
                    Packets flow here (line rate)
```

**Why this matters:** If the controller forwarded every packet, SDN would be very slow and the controller would be a bottleneck. This misconception about SDN controllers comes up every semester. I find it helps to compare with a GPS navigator — it tells you where to go but does not drive the car.

---

### 🚫 Misconception 6: "Higher priority number means lower importance"

**WRONG:** "Priority 1 is the most important rule because it is checked first."

**CORRECT:** In OpenFlow, **higher priority number = higher importance**. Priority 100 beats priority 10.

| Priority | Meaning |
|----------|---------|
| 65535 | Maximum priority (checked first) |
| 100 | Higher priority |
| 10 | Lower priority |
| 0 | Lowest priority (table-miss) |

**Practical verification:**
```bash
# Install two conflicting rules
ovs-ofctl -O OpenFlow13 add-flow s1 "priority=10,ip,actions=drop"
ovs-ofctl -O OpenFlow13 add-flow s1 "priority=100,ip,actions=output:1"

# Packet will be forwarded (priority 100 wins), not dropped
```

**Why this matters:** Getting priorities wrong causes traffic to be dropped or allowed unexpectedly.

---

### 🚫 Misconception 7: "Flow rules persist across controller restarts"

**WRONG:** "I installed the flow rules yesterday, so they should still be there."

**CORRECT:** By default, flow rules are stored in the switch's memory (volatile). When the controller restarts or the connection drops, the rules may be lost unless:
- Rules have `hard_timeout=0` (no expiry)
- Rules are proactively reinstalled by the controller on reconnection
- The switch is configured for persistent storage

**Why this matters:** SDN applications need to handle controller restarts gracefully by re-pushing rules.

---

### 🚫 Misconception 8: "OpenFlow is the only SDN protocol"

**WRONG:** "SDN means OpenFlow."

**CORRECT:** OpenFlow is the most common southbound interface, but SDN is an architecture pattern. Other protocols and approaches exist:
- P4 (programmable data planes)
- NETCONF/YANG (configuration)
- gRPC (modern controller APIs)
- Proprietary APIs (Cisco ACI, VMware NSX)

**Why this matters:** Understanding SDN as an architecture (separation of control and data planes) rather than a specific protocol helps when evaluating different technologies.

---

## Quick Self-Check

Before the lab, verify you understand:

- [ ] NAT provides obscurity, not security
- [ ] Source ports are not guaranteed to be preserved
- [ ] Private IPs are never visible to external servers
- [ ] Conntrack entries expire
- [ ] SDN controller installs rules; switches forward packets
- [ ] Higher priority number = checked first
- [ ] Flow rules can expire or be lost

If any of these feels confusing, review the corresponding section above before starting the exercises.

---

*Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim*
*Issues: Open an issue in GitHub*
