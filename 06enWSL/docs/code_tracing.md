# 🔍 Code Tracing Exercises — Week 6

## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Trace through the scenarios mentally before running them. This builds understanding of how NAT and SDN actually work.

---

## Exercise T1: NAT Translation Trace

### Scenario

Host h1 (192.168.1.10) sends a TCP SYN packet to a web server at 8.8.8.8:443. The NAT router (rnat) has public IP 203.0.113.1.

### Initial State

```
Conntrack table: (empty)

h1 local socket: 192.168.1.10:45678 → 8.8.8.8:443
```

### Questions

💭 **Your prediction:** Before looking at the solution, write down your answers:

1. **Outbound packet:** What are the source and destination addresses in the packet as it leaves h1?

2. **After NAT translation:** What are the source and destination addresses in the packet as it leaves rnat towards the internet?

3. **Conntrack entry:** What 5-tuple does the NAT router store in the conntrack table?

4. **Return packet arrives:** A SYN-ACK arrives at rnat from 8.8.8.8:443. What destination address does it have?

5. **After reverse translation:** What destination address does the packet have when it reaches h1?

### Trace Table

Complete this table:

| Step | Packet Location | Src IP:Port | Dst IP:Port |
|------|-----------------|-------------|-------------|
| 1 | Leaving h1 | ? | ? |
| 2 | Leaving rnat (public side) | ? | ? |
| 3 | Arriving at rnat (return) | ? | ? |
| 4 | Arriving at h1 | ? | ? |

### Solution

<details>
<summary>Click to reveal</summary>

| Step | Packet Location | Src IP:Port | Dst IP:Port |
|------|-----------------|-------------|-------------|
| 1 | Leaving h1 | 192.168.1.10:45678 | 8.8.8.8:443 |
| 2 | Leaving rnat (public side) | 203.0.113.1:50001 | 8.8.8.8:443 |
| 3 | Arriving at rnat (return) | 8.8.8.8:443 | 203.0.113.1:50001 |
| 4 | Arriving at h1 | 8.8.8.8:443 | 192.168.1.10:45678 |

**Conntrack entry:**
```
tcp  ESTABLISHED  src=192.168.1.10 dst=8.8.8.8 sport=45678 dport=443
                  src=8.8.8.8 dst=203.0.113.1 sport=443 dport=50001
```

**Explanation:** 
- Step 1→2: SNAT rewrites source from private to public
- Step 3→4: Reverse translation using conntrack entry
- The server (8.8.8.8) never sees the private address 192.168.1.10

</details>

---

## Exercise T2: SDN Flow Matching Trace

### Scenario

An SDN switch (s1) has these flow rules installed:

```
priority=0,   actions=CONTROLLER                           # table-miss
priority=10,  ip, nw_dst=10.0.6.13, actions=drop           # block all to h3
priority=100, icmp, nw_src=10.0.6.11, nw_dst=10.0.6.12, actions=output:2  # h1→h2 ICMP
priority=100, icmp, nw_src=10.0.6.12, nw_dst=10.0.6.11, actions=output:1  # h2→h1 ICMP
priority=200, tcp, nw_dst=10.0.6.12, tp_dst=80, actions=output:2          # HTTP to h2
```

### Packets to Trace

For each packet, determine which rule matches and what happens:

| Packet | Src IP | Dst IP | Protocol | Dst Port |
|--------|--------|--------|----------|----------|
| A | 10.0.6.11 | 10.0.6.12 | ICMP | - |
| B | 10.0.6.11 | 10.0.6.13 | ICMP | - |
| C | 10.0.6.11 | 10.0.6.13 | TCP | 80 |
| D | 10.0.6.11 | 10.0.6.12 | TCP | 80 |
| E | 10.0.6.11 | 10.0.6.12 | TCP | 22 |
| F | 10.0.6.14 | 10.0.6.12 | ICMP | - |

### Questions

💭 **Your prediction:** For each packet, write down:
1. Which rules does it potentially match?
2. Which rule actually applies (highest priority)?
3. What action is taken?

### Solution

<details>
<summary>Click to reveal</summary>

| Packet | Matching Rules | Winning Rule | Action |
|--------|----------------|--------------|--------|
| A | priority=100 (h1→h2 ICMP) | priority=100 | output:2 (forwarded to h2) |
| B | priority=10 (block h3) | priority=10 | drop |
| C | priority=10 (block h3) | priority=10 | drop |
| D | priority=200 (HTTP to h2) | priority=200 | output:2 (forwarded to h2) |
| E | priority=0 (table-miss) | priority=0 | CONTROLLER |
| F | priority=0 (table-miss) | priority=0 | CONTROLLER |

**Explanations:**

- **Packet A:** Matches the specific h1→h2 ICMP rule at priority=100
- **Packet B:** Although it's ICMP from h1, destination is h3 which matches the block rule. No higher-priority rule permits ICMP to h3.
- **Packet C:** TCP to h3 — blocked by priority=10 rule. Note: HTTP rule only applies to h2, not h3.
- **Packet D:** Matches HTTP rule (priority=200) which is higher than any other matching rule
- **Packet E:** SSH to h2 — no specific rule exists, falls to table-miss
- **Packet F:** Unknown source (h4?) — no matching rule, goes to controller

**Key insight:** Priority matters! Packet B is blocked even though h1→h2 ICMP is allowed, because destination is h3, not h2.

</details>

---

## Exercise T3: ARP Handling in SDN Controller

### Scenario

Trace what happens when h1 wants to ping h2 for the first time. The SDN controller uses a learning switch approach.

### Initial State

```
Switch s1 flow table:
  priority=0, actions=CONTROLLER (table-miss only)

Controller MAC table: (empty)
  mac_to_port = {}
```

### Sequence to Trace

1. h1 (10.0.6.11, MAC=00:00:00:00:00:01) wants to ping h2 (10.0.6.12)
2. h1 doesn't know h2's MAC address
3. h1 sends ARP request: "Who has 10.0.6.12?"
4. The ARP packet arrives at switch s1 on port 1

### Questions

💭 **Your prediction:** Answer these before revealing the solution:

1. What happens when the ARP request arrives at s1?
2. What does the controller learn from this packet?
3. What action does the controller tell s1 to take with the ARP request?
4. When h2 responds with ARP reply, what does the controller learn?
5. After the ARP exchange, what's in the controller's MAC table?

### Trace Steps

Complete this execution trace:

```
Step 1: h1 → s1 (port 1)
  Packet: ARP Request, src_mac=00:00:00:00:00:01, dst_mac=ff:ff:ff:ff:ff:ff
  Flow match: ???
  Action: ???

Step 2: Controller receives packet-in
  Learns: ???
  Decides: ???
  Sends: ???

Step 3: s1 → h2, h3 (flood)
  Packet: ???

Step 4: h2 → s1 (port 2)
  Packet: ARP Reply, src_mac=00:00:00:00:00:02, dst_mac=00:00:00:00:00:01
  Flow match: ???
  Action: ???

Step 5: Controller receives packet-in
  Learns: ???
  Decides: ???
  Sends: ???

Step 6: s1 → h1 (port 1)
  Packet: ???
```

### Solution

<details>
<summary>Click to reveal</summary>

```
Step 1: h1 → s1 (port 1)
  Packet: ARP Request, src_mac=00:00:00:00:00:01, dst_mac=ff:ff:ff:ff:ff:ff
  Flow match: table-miss (priority=0)
  Action: Send to CONTROLLER

Step 2: Controller receives packet-in
  Learns: MAC 00:00:00:00:00:01 is on port 1
  mac_to_port = {00:00:00:00:00:01: 1}
  Decides: Destination is broadcast, so flood
  Sends: packet-out with action=FLOOD

Step 3: s1 → h2, h3 (flood)
  Packet: ARP Request forwarded to all ports except port 1

Step 4: h2 → s1 (port 2)
  Packet: ARP Reply, src_mac=00:00:00:00:00:02, dst_mac=00:00:00:00:00:01
  Flow match: table-miss (priority=0)
  Action: Send to CONTROLLER

Step 5: Controller receives packet-in
  Learns: MAC 00:00:00:00:00:02 is on port 2
  mac_to_port = {00:00:00:00:00:01: 1, 00:00:00:00:00:02: 2}
  Decides: Destination MAC 00:00:00:00:00:01 is known → port 1
  Sends: packet-out with action=output:1
         (may also install flow for future packets)

Step 6: s1 → h1 (port 1)
  Packet: ARP Reply delivered to h1
```

**Final MAC table:**
```python
mac_to_port = {
    "00:00:00:00:00:01": 1,  # h1
    "00:00:00:00:00:02": 2,  # h2
}
```

**Key insight:** The controller doesn't install flows for ARP (too transient). It learns MACs and either floods (unknown destination) or unicasts (known destination).

</details>

---

## Exercise T4: PAT with Multiple Connections

### Scenario

Two internal hosts (h1 and h2) both connect to the same external server using the same local port.

### Initial State

```
h1: 192.168.1.10, opens connection from port 12345
h2: 192.168.1.20, opens connection from port 12345
NAT router public IP: 203.0.113.1
External server: 8.8.8.8:443
```

### Questions

💭 **Your prediction:**

1. Can both connections exist simultaneously?
2. What source ports will the server see for each connection?
3. How does the NAT router distinguish return traffic?

### State Table

Track the conntrack entries:

| Internal | External (NAT) | Remote | State |
|----------|----------------|--------|-------|
| ? | ? | ? | ? |
| ? | ? | ? | ? |

### Solution

<details>
<summary>Click to reveal</summary>

| Internal | External (NAT) | Remote | State |
|----------|----------------|--------|-------|
| 192.168.1.10:12345 | 203.0.113.1:50001 | 8.8.8.8:443 | ESTABLISHED |
| 192.168.1.20:12345 | 203.0.113.1:50002 | 8.8.8.8:443 | ESTABLISHED |

**Answers:**

1. **Yes**, both connections can exist simultaneously
2. The server sees **different source ports** (50001 and 50002) even though both hosts used 12345 internally
3. The NAT router uses the **external port** to distinguish return traffic — packets to :50001 go to h1, packets to :50002 go to h2

**Key insight:** PAT doesn't preserve internal port numbers. It assigns unique external ports to distinguish connections.

</details>

---

## Self-Assessment

After completing these exercises, you should be able to:

- [ ] Trace a packet through NAT translation in both directions
- [ ] Predict which SDN flow rule will match a given packet
- [ ] Explain how an SDN controller learns network topology
- [ ] Distinguish between table-miss, flood and unicast forwarding
- [ ] Explain how PAT enables multiple hosts to share one public IP

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
