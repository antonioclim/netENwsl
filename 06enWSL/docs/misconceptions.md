# ❌ Common Misconceptions — Week 6

## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> This document lists common misunderstandings about NAT, SDN and how to correct them.

---

## NAT and PAT Misconceptions

### 🚫 Misconception 1: "NAT provides security"

**WRONG:** "Our network is secure because we use NAT — attackers can't reach our internal hosts."

**CORRECT:** NAT provides *obscurity*, not *security*. While NAT does block unsolicited inbound connections (because there's no conntrack entry to map them), it does not:
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

---

### 🚫 Misconception 2: "NAT preserves the original source port"

**WRONG:** "If my application uses port 12345, the server will see port 12345."

**CORRECT:** The NAT router selects a source port from its available pool. It *may* reuse your original port if it's available, but there's no guarantee.

**Practical verification:**
```bash
# From two different internal hosts, connect using the same local port
h1 python3 -c "import socket; s=socket.socket(); s.bind(('',12345)); s.connect(('203.0.113.2',5000))"
h2 python3 -c "import socket; s=socket.socket(); s.bind(('',12345)); s.connect(('203.0.113.2',5000))"

# On the server, you'll see DIFFERENT source ports for each connection
# Both h1 and h2 used port 12345 internally, but the NAT assigned different external ports
```

**Why this matters:** Applications that assume port preservation (e.g., some P2P protocols) may fail behind NAT.

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
Packet flow (first packet):
  Host → Switch → [table-miss] → Controller → [flow-mod] → Switch → Host

Packet flow (subsequent packets):
  Host → Switch → [flow match] → Host
  (Controller not involved!)
```

**Why this matters:** If the controller forwarded every packet, SDN would be extremely slow and the controller would be a bottleneck.

---

### 🚫 Misconception 6: "Higher priority number = lower importance"

**WRONG:** "Priority 1 is the most important rule, like Unix nice values."

**CORRECT:** In OpenFlow, **higher priority number = higher importance**. A rule with priority=300 takes precedence over priority=30.

| Priority | Matches first? |
|----------|----------------|
| 300 | ✓ Yes |
| 100 | Second |
| 30 | Third |
| 0 | Last (table-miss) |

**Practical verification:**
```bash
# Add two conflicting rules
ovs-ofctl -O OpenFlow13 add-flow s1 "priority=10,ip,nw_dst=10.0.6.13,actions=drop"
ovs-ofctl -O OpenFlow13 add-flow s1 "priority=100,icmp,nw_dst=10.0.6.13,actions=output:3"

# ICMP to h3 will be FORWARDED (priority 100 > priority 10)
h1 ping -c 1 10.0.6.13  # Works!
```

**Why this matters:** Misunderstanding priority leads to security policies that don't work as intended.

---

### 🚫 Misconception 7: "Flow rules are permanent"

**WRONG:** "Once I install a flow, it stays until I delete it."

**CORRECT:** Flow rules can have timeouts:
- **idle_timeout:** Delete after N seconds of no matching packets
- **hard_timeout:** Delete after N seconds regardless of traffic

```bash
# This rule will expire after 60 seconds of inactivity
ovs-ofctl -O OpenFlow13 add-flow s1 "idle_timeout=60,priority=100,icmp,actions=output:1"

# This rule will expire after 300 seconds no matter what
ovs-ofctl -O OpenFlow13 add-flow s1 "hard_timeout=300,priority=100,tcp,actions=output:2"
```

**Why this matters:** Security policies should use appropriate timeouts. Stale rules can create vulnerabilities or consume switch memory.

---

### 🚫 Misconception 8: "ovs-ofctl dump-flows shows real-time traffic"

**WRONG:** "The packet counter updates instantly as traffic flows."

**CORRECT:** Flow statistics are cached and may have a slight delay. The counters show *cumulative* totals, not real-time rates.

**Practical verification:**
```bash
# Check flows before and after traffic
ovs-ofctl -O OpenFlow13 dump-flows s1  # Note n_packets value
h1 ping -c 10 10.0.6.12
ovs-ofctl -O OpenFlow13 dump-flows s1  # n_packets increased by ~10
```

**Why this matters:** For real-time traffic analysis, use packet capture tools (tcpdump, Wireshark), not flow statistics.

---

## Quick Reference Table

| Misconception | Reality |
|---------------|---------|
| NAT = security | NAT = obscurity only |
| Source port preserved | Port may change |
| Private IPs visible externally | Only public NAT IP visible |
| Conntrack entries permanent | Entries timeout |
| Controller forwards packets | Controller installs rules only |
| Low priority = important | High priority number = important |
| Flow rules permanent | Rules can timeout |
| dump-flows = real-time | Statistics are cached/cumulative |

---

## Self-Check Questions

Before the lab, answer these questions (check your answers against this document):

1. If I configure NAT, do I still need a firewall?
2. What happens to a NAT connection after 30 minutes of inactivity?
3. In OpenFlow, which rule matches first: priority=50 or priority=5?
4. Does every packet in an SDN network go through the controller?
5. Can a server at Google see my private IP address (192.168.x.x)?

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
