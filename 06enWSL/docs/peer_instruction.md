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

I recommend writing students' first-vote percentages on the board before discussion — it makes the shift visible after re-voting and students find it motivating.

---

## Question 1: NAT vs PAT (LO1, LO2)

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

**B** — PAT (Port Address Translation) assigns unique source ports to each connection. Even though both connections share the same public IP (203.0.113.1), h1's traffic might use port 50001 whilst h2's uses port 50002. The conntrack table maps these back to the original internal addresses.

### Targeted Misconception

Many students confuse static NAT (one-to-one mapping) with PAT (many-to-one). They may think NAT requires multiple public IPs, not realising port numbers provide the multiplexing.

### Instructor Notes

- **Target accuracy:** ~55% on first vote
- **Key concept:** Port multiplexing enables address sharing
- **After discussion:** Show conntrack table with two entries sharing same public IP
- **Historical note:** In previous years, roughly 60% chose option A on first vote. After peer discussion, this typically drops to under 15%.

---

## Question 2: Source Port Preservation (LO2)

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

Students often assume the source port passes through unchanged. This confusion surfaces frequently when debugging NAT traversal issues or understanding why port prediction attacks work.

### Instructor Notes

- **Target accuracy:** ~35% on first vote
- **Key concept:** NAT port selection is implementation-dependent
- **After discussion:** Show two connections from same internal port getting different external ports
- **Tip:** This usually breaks applications that assume port preservation. P2P protocols learned this the hard way.

---

## Question 3: SDN Flow Priority (LO5)

> 💭 **PREDICTION:** In OpenFlow, does a higher priority number mean more or less important?

### Scenario

An SDN switch has two flow rules installed:
- Rule A: priority=10, match=ip, action=drop
- Rule B: priority=100, match=ip, action=output:2

### Question

A packet arrives that matches both rules. Which rule is applied?

### Options

- **A)** Rule A — it was installed first
- **B)** Rule B — higher priority number wins — **CORRECT**
- **C)** Both rules are applied in sequence
- **D)** The packet is sent to the controller due to conflict

### Correct Answer

**B** — In OpenFlow, higher priority numbers indicate higher importance. Rule B (priority=100) takes precedence over Rule A (priority=10). The packet is forwarded to port 2.

### Targeted Misconception

Students often assume "priority 1" means "first priority" (most important). OpenFlow uses the opposite convention: higher numbers = higher priority. This trips up nearly everyone the first time.

### Instructor Notes

- **Target accuracy:** ~30% on first vote
- **Key concept:** OpenFlow priority semantics
- **After discussion:** Compare with CSS specificity or iptables rule ordering
- **From experience:** If students struggle here, ask them about the priority=0 table-miss rule. Why zero? That usually clicks.

---

## Question 4: SDN Controller Role (LO4, LO6)

> 💭 **PREDICTION:** Does every packet go through the SDN controller?

### Scenario

An SDN controller has installed flow rules on switch S1. Host h1 sends 1000 packets to host h2, all matching the same installed flow rule.

### Question

How many packets does the controller process?

### Options

- **A)** 1000 — the controller processes every packet
- **B)** 1 — only the first packet (table-miss) goes to the controller
- **C)** 0 — if a matching rule exists, no packets go to the controller — **CORRECT**
- **D)** 500 — the controller samples half the packets

### Correct Answer

**C** — Once a flow rule is installed, matching packets are forwarded directly by the switch hardware at line rate. The controller is only involved during table-miss events (when no rule matches). This is what makes SDN scalable.

### Targeted Misconception

Students often believe the controller is always in the forwarding path, making SDN seem inherently slower than traditional networking. In reality, the data plane operates independently once flows are installed. I find it helps to compare with a GPS navigator — it tells you where to go but does not drive the car.

### Instructor Notes

- **Target accuracy:** ~50% on first vote
- **Key concept:** Data plane independence, reactive vs proactive flow installation
- **After discussion:** Show Wireshark capture with packet-in only for first packet

---

## Question 5: NAT and Security (LO1)

> 💭 **PREDICTION:** Does NAT provide security? Write down your reasoning.

### Scenario

A company uses NAT to connect 500 internal hosts to the internet through a single public IP address. The security team claims "NAT is our firewall."

### Question

Is NAT an adequate replacement for a firewall?

### Options

- **A)** Yes — NAT hides internal IPs and blocks all inbound attacks
- **B)** Partially — NAT blocks unsolicited inbound traffic but is not a true firewall — **CORRECT**
- **C)** No — NAT has no security benefits whatsoever
- **D)** Yes — NAT encrypts all outbound traffic

### Correct Answer

**B** — NAT provides *obscurity*, not *security*. It does block unsolicited inbound connections (since there is no conntrack entry to map them), which offers some protection. However, NAT does not inspect packet contents, block malware, prevent phishing, or stop attacks initiated from inside. A proper firewall with stateful inspection is still necessary.

### Targeted Misconception

Many believe NAT is a security feature. Whilst it incidentally blocks some attacks, relying on NAT for security is dangerous. In my experience teaching this module, the NAT-as-security misconception causes the most debugging frustration when students later encounter real network security issues.

### Instructor Notes

- **Target accuracy:** ~60% on first vote
- **Key concept:** Obscurity ≠ security; defence in depth required
- **After discussion:** List what NAT blocks vs. what a firewall blocks

---

## Question 6: NAT Implementation (LO3)

> 💭 **PREDICTION:** Which iptables chain handles outbound NAT translation?

### Scenario

You are configuring NAT on a Linux router. The private network is 192.168.1.0/24 connected to eth0, and the public interface is eth1 with a dynamic IP.

### Question

Which iptables command correctly enables MASQUERADE for outbound traffic from the private network?

### Options

- **A)** `iptables -t nat -A PREROUTING -o eth1 -j MASQUERADE`
- **B)** `iptables -t nat -A POSTROUTING -o eth1 -s 192.168.1.0/24 -j MASQUERADE` — **CORRECT**
- **C)** `iptables -t nat -A INPUT -i eth0 -j MASQUERADE`
- **D)** `iptables -A FORWARD -o eth1 -j MASQUERADE`

### Correct Answer

**B** — MASQUERADE must be in the POSTROUTING chain (applied after the routing decision), on the outbound public interface (`-o eth1`), for traffic originating from the private subnet (`-s 192.168.1.0/24`).

### Targeted Misconception

Students frequently confuse PREROUTING (used for DNAT/port forwarding of inbound traffic) with POSTROUTING (used for SNAT/MASQUERADE of outbound traffic). The chain name indicates WHEN in the packet flow the rule is applied.

### Instructor Notes

- **Target accuracy:** ~40% on first vote
- **Key concept:** Chain selection based on packet flow position
- **After discussion:** Draw the netfilter packet flow diagram showing where each chain applies
- **Common error:** Using -i (input interface) instead of -o (output interface) for POSTROUTING. I see this in about a third of first attempts.

---

## Question 7: SDN Flow Installation (LO4)

> 💭 **PREDICTION:** When does the SDN controller get involved in packet forwarding?

### Scenario

An OpenFlow SDN switch receives a packet from host h1. The switch has been running for 10 minutes and has some flow rules installed by the controller.

### Question

Under what condition does the switch send this packet to the controller?

### Options

- **A)** Always — every packet goes through the controller for approval
- **B)** Never — once flows are installed, the controller is not needed
- **C)** Only when the packet does not match any existing flow rule (table-miss) — **CORRECT**
- **D)** Only for the first packet from each new source MAC address

### Correct Answer

**C** — The switch only contacts the controller when a packet does not match any installed flow rule (table-miss). The table-miss rule typically has lowest priority and action `CONTROLLER`. Once a flow is installed, subsequent matching packets are forwarded directly by the switch without controller involvement.

### Targeted Misconception

Students often believe the controller is always in the forwarding path, making SDN inherently slower. In reality, the controller only handles exceptions; normal traffic is forwarded at line rate by the switch hardware.

### Instructor Notes

- **Target accuracy:** ~48% on first vote
- **Key concept:** Reactive vs proactive flow installation; data plane independence
- **After discussion:** Show packet-in/flow-mod sequence in Wireshark, demonstrate that subsequent packets do not generate packet-in

---

## Question 8: OpenFlow Policy Design (LO7)

> 💭 **PREDICTION:** How do you implement "allow specific, deny general" in OpenFlow?

### Scenario

You need to design an SDN security policy with these requirements:
1. Allow SSH (TCP port 22) to server 10.0.6.12
2. Block ALL other traffic to 10.0.6.12
3. Allow all other traffic in the network

### Question

What priority ordering correctly implements this policy?

### Options

- **A)** SSH allow: priority=100, Block to .12: priority=50, Default allow: priority=10 — **CORRECT**
- **B)** SSH allow: priority=10, Block to .12: priority=50, Default allow: priority=100
- **C)** Block to .12: priority=100, SSH allow: priority=50, Default allow: priority=10
- **D)** All rules at priority=100; order of installation determines matching

### Correct Answer

**A** — The most specific permit rule (SSH to .12) needs the highest priority (100) so it is checked first. The block rule (50) catches everything else destined for .12. The default allow (10) handles all remaining traffic. Higher priority number = higher importance.

### Targeted Misconception

Students often place the block rule at highest priority, forgetting that specific permit rules must be able to override it. The design pattern is: "specific permit > general deny > default policy"

### Instructor Notes

- **Target accuracy:** ~25% on first vote
- **Key concept:** Priority layering for security policies
- **After discussion:** Walk through packet matching for SSH packet, HTTP packet, and packet to different host
- **Teaching tip:** Draw three packets on the board and trace them through the rules. The visual really helps here.

---

## Summary Table

| Question | Topic | LO | Target Accuracy | Key Misconception |
|----------|-------|-----|-----------------|-------------------|
| Q1 | NAT vs PAT | LO1, LO2 | ~55% | NAT requires multiple public IPs |
| Q2 | Port preservation | LO2 | ~35% | Source port always preserved |
| Q3 | SDN priority | LO5 | ~30% | Lower number = higher priority |
| Q4 | Controller role | LO4, LO6 | ~50% | Controller forwards packets |
| Q5 | NAT security | LO1 | ~60% | NAT = firewall |
| Q6 | NAT implementation | LO3 | ~40% | PREROUTING vs POSTROUTING confusion |
| Q7 | Flow installation | LO4 | ~48% | Controller always involved |
| Q8 | Policy design | LO7 | ~25% | Block at highest priority |

---

## Using Peer Instruction Effectively

### Before Class
- Ensure students have completed the pre-lab reading
- Prepare voting mechanism (hands, clickers, or online tool)
- Have diagrams ready for explanation phase

### During Voting
- Enforce silence during individual thinking
- Do not reveal vote distribution until after discussion
- Encourage students to commit to an answer

### During Discussion
- Circulate and listen to student reasoning
- Note common arguments to address in explanation
- Pair students with different answers when possible

### After Re-vote
- Show vote change statistics
- Explain correct answer with emphasis on common mistakes
- Connect to upcoming lab exercises

If this feels like too much structure at first, focus on just Q1, Q4 and Q5 — they generate the best discussions.

---

*Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim*
*Issues: Open an issue in GitHub*
