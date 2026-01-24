# 🗳️ Peer Instruction Questions — Week 6

## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Peer Instruction Protocol (5 steps)

Each question follows **5 mandatory steps**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 1 (1 min)  │  Read the question and think individually               │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 2 (30 sec) │  Vote your answer (A/B/C/D) — no discussion!            │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 3 (2 min)  │  Discuss with your neighbour — convince them!           │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 4 (30 sec) │  Re-vote — you may change your answer                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 5 (2 min)  │  Instructor explains the correct answer                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Question 1: NAT vs PAT

> 💭 **PREDICTION:** Before reading, write down what you think is the main difference between NAT and PAT.

### Scenario

A home router has public IP 203.0.113.1. Two internal hosts (192.168.1.10 and 192.168.1.20) both connect to the same web server (8.8.8.8:443) simultaneously.

### Question

How does the router distinguish return packets for each internal host?

### Options

- **A)** It uses different public IP addresses for each internal host
- **B)** It uses different translated source ports for each internal host — **CORRECT**
- **C)** It examines the payload to identify the original sender
- **D)** It cannot — only one host can connect at a time

### Correct Answer

**B** — PAT (Port Address Translation) assigns unique source ports to each connection. Even though both connections share the same public IP (203.0.113.1), h1's traffic might use port 50001 while h2's uses port 50002. The conntrack table maps these back to the original internal addresses.

### Targeted Misconception

Many students confuse static NAT (one-to-one mapping) with PAT (many-to-one). They may think NAT requires multiple public IPs, not realising port numbers provide the multiplexing.

### Instructor Notes

- **Target accuracy:** ~50% on first vote
- **Key concept:** Port multiplexing enables address sharing
- **After discussion:** Show conntrack table with two entries sharing same public IP
- **Timing:** Present (1 min) → Vote (1 min) → Discuss (3 min) → Revote (30 sec) → Explain (2 min)

---

## Question 2: Source Port Preservation

> 💭 **PREDICTION:** When a private host uses source port 12345, what port will the public server see?

### Scenario

Host h1 (192.168.1.10) opens a connection using local port 12345 to a server at 8.8.8.8:80. The NAT router performs MASQUERADE translation.

```
h1 (192.168.1.10:12345) → NAT → Server (8.8.8.8:80)
```

### Question

What source port will the server (8.8.8.8) observe for this connection?

### Options

- **A)** Always 12345 — NAT preserves the original port
- **B)** A port chosen by the NAT router, possibly 12345 if available — **CORRECT**
- **C)** Always a random port in the ephemeral range (49152-65535)
- **D)** The destination port (80) mirrored back

### Correct Answer

**B** — The NAT router selects a source port from its available pool. It *may* use 12345 if that port is free on the public interface, but if another connection is already using it, the router will choose a different port. The original source port is not guaranteed to be preserved.

### Targeted Misconception

Students often assume the source port passes through unchanged. This leads to confusion when debugging NAT issues or understanding why port prediction attacks work.

### Instructor Notes

- **Target accuracy:** ~40% on first vote
- **Key concept:** NAT port selection is implementation-dependent
- **After discussion:** Show two connections from same internal port getting different external ports
- **Timing:** Present (1 min) → Vote (1 min) → Discuss (3 min) → Revote (30 sec) → Explain (2 min)

---

## Question 3: SDN Flow Priority

> 💭 **PREDICTION:** In OpenFlow, does a higher priority number mean more important or less important?

### Scenario

An SDN switch has these flow rules installed:

```
priority=10,  ip, nw_dst=10.0.6.13, actions=drop
priority=100, icmp, nw_src=10.0.6.11, nw_dst=10.0.6.13, actions=output:3
```

### Question

Host h1 (10.0.6.11) sends an ICMP ping to h3 (10.0.6.13). What happens?

### Options

- **A)** The packet is dropped because priority=10 was installed first
- **B)** The packet is dropped because lower priority number means higher importance
- **C)** The packet is forwarded to port 3 because higher priority number takes precedence — **CORRECT**
- **D)** The packet matches both rules and is both dropped and forwarded

### Correct Answer

**C** — In OpenFlow, **higher priority number = higher importance**. The ICMP packet matches both rules, but the rule with priority=100 takes precedence over priority=10. The packet is forwarded to port 3.

### Targeted Misconception

Many systems use "priority 1 = highest" (like Unix nice values). OpenFlow uses the opposite convention, which catches students off guard.

### Instructor Notes

- **Target accuracy:** ~35% on first vote (this is a common trap!)
- **Key concept:** OpenFlow priority semantics differ from other systems
- **After discussion:** Show flow table sorted by priority, demonstrate matching
- **Timing:** Present (1 min) → Vote (1 min) → Discuss (3 min) → Revote (30 sec) → Explain (2 min)

---

## Question 4: SDN Controller Role

> 💭 **PREDICTION:** Does the SDN controller forward packets, or does it do something else?

### Scenario

In an SDN network, host h1 sends its first packet to h2. The switch has no matching flow rule.

### Question

What is the role of the SDN controller when this packet arrives?

### Options

- **A)** The controller receives the packet, processes it and forwards it to h2
- **B)** The controller installs a flow rule in the switch, then the switch forwards subsequent packets — **CORRECT**
- **C)** The controller buffers the packet until h2 responds
- **D)** The controller drops the packet and logs the attempt

### Correct Answer

**B** — The controller's job is to *decide policy and install rules*, not to forward packets. When a table-miss occurs, the switch sends a packet-in to the controller. The controller analyses the situation, installs appropriate flow rules via flow-mod messages and the switch then forwards the packet (and subsequent matching packets) according to those rules.

### Targeted Misconception

Students often think the controller acts like a central router, forwarding every packet. This would be extremely slow and defeat the purpose of SDN's distributed data plane.

### Instructor Notes

- **Target accuracy:** ~45% on first vote
- **Key concept:** Control plane decides, data plane executes
- **After discussion:** Draw timeline showing packet-in → flow-mod → packet forwarding
- **Timing:** Present (1 min) → Vote (1 min) → Discuss (3 min) → Revote (30 sec) → Explain (2 min)

---

## Question 5: NAT and Security

> 💭 **PREDICTION:** Does NAT make your network more secure? Why or why not?

### Scenario

A company uses NAT to hide 500 internal workstations behind a single public IP address. The IT manager claims "We don't need a firewall because NAT protects us."

### Question

Is the IT manager's claim correct?

### Options

- **A)** Yes — NAT hides internal addresses, making attacks impossible
- **B)** Partially — NAT blocks unsolicited inbound connections but doesn't inspect traffic — **CORRECT**
- **C)** No — NAT has no security benefits whatsoever
- **D)** Yes — NAT encrypts all outbound traffic automatically

### Correct Answer

**B** — NAT provides *obscurity*, not *security*. It does block unsolicited inbound connections (since there's no conntrack entry to map them), which offers some protection. However, NAT does not inspect packet contents, block malware, prevent phishing, or stop attacks initiated from inside. A proper firewall with stateful inspection is still necessary.

### Targeted Misconception

Many believe NAT is a security feature. While it incidentally blocks some attacks, relying on NAT for security is dangerous. It creates a false sense of protection.

### Instructor Notes

- **Target accuracy:** ~55% on first vote
- **Key concept:** Obscurity ≠ security; defence in depth required
- **After discussion:** List what NAT blocks vs. what a firewall blocks
- **Timing:** Present (1 min) → Vote (1 min) → Discuss (3 min) → Revote (30 sec) → Explain (2 min)

---

## Summary Table

| Question | Topic | Target Accuracy | Key Misconception |
|----------|-------|-----------------|-------------------|
| Q1 | NAT vs PAT | ~50% | NAT requires multiple public IPs |
| Q2 | Port preservation | ~40% | Source port always preserved |
| Q3 | SDN priority | ~35% | Lower number = higher priority |
| Q4 | Controller role | ~45% | Controller forwards packets |
| Q5 | NAT security | ~55% | NAT = firewall |

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
