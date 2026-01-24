# 🗳️ Peer Instruction Questions — Week 7
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

## Question 1: REJECT vs DROP Behaviour

> 💭 **PREDICTION:** Before reading the scenario, predict: when a firewall blocks a TCP connection, does the client always know immediately?

### Scenario

You configure an iptables rule on a Linux firewall:

```bash
# Rule A
iptables -A INPUT -p tcp --dport 9090 -j DROP

# Rule B  
iptables -A INPUT -p tcp --dport 9090 -j REJECT
```

A client attempts to connect to port 9090. You observe the client behaviour.

### Question

What is the **primary observable difference** between Rule A and Rule B from the client's perspective?

### Options

- **A)** Rule A sends TCP RST; Rule B sends ICMP unreachable — *Misconception: confuses the two actions*
- **B)** Rule A causes client timeout; Rule B causes immediate connection refused — **CORRECT**
- **C)** Both rules behave identically; the difference is only in firewall logs — *Misconception: assumes filtering actions are equivalent*
- **D)** Rule A blocks the packet; Rule B allows it through but logs it — *Misconception: misunderstands REJECT semantics*

### Correct Answer

**B** — DROP silently discards packets, causing the client to wait until timeout (no response received). REJECT sends an explicit refusal (TCP RST or ICMP), causing immediate "Connection refused" error.

### Targeted Misconception

Students often assume all blocking actions behave the same way. This question reveals whether they understand the timing and feedback implications of DROP vs REJECT.

### Instructor Notes

- **Target accuracy:** 40-50% on first vote
- **Key concept:** Silent discard vs active refusal
- **After discussion:** Demonstrate with `tcpdump` showing RST packets for REJECT, silence for DROP
- **Timing:** Present (1 min) → Vote (1 min) → Discuss (3 min) → Revote (30 sec) → Explain (2 min)

---

## Question 2: Port States in Scanning

> 💭 **PREDICTION:** If you probe a port and receive no response at all, what can you conclude about that port?

### Scenario

You run a port probe against host 10.0.7.100:

```bash
python3 src/apps/port_probe.py --host 10.0.7.100 --ports 22,80,443 --timeout 2
```

Results:
```
Port 22:  open
Port 80:  closed
Port 443: filtered
```

### Question

What network evidence distinguishes a "closed" port from a "filtered" port?

### Options

- **A)** Closed ports respond with SYN-ACK; filtered ports respond with RST — *Misconception: reverses TCP handshake logic*
- **B)** Closed ports respond with RST or ICMP unreachable; filtered ports produce no response — **CORRECT**
- **C)** Closed means no service running; filtered means service running but blocked — *Misconception: conflates service state with network evidence*
- **D)** There is no difference; both indicate the port cannot be reached — *Misconception: ignores diagnostic value*

### Correct Answer

**B** — A closed port has no listening service, but the host is reachable and responds with TCP RST (or ICMP port unreachable for UDP). A filtered port produces no response because a firewall silently drops the probe packets.

### Targeted Misconception

Students confuse the concepts of "no service listening" with "firewall blocking". This question tests whether they can interpret probe results correctly.

### Instructor Notes

- **Target accuracy:** 35-45% on first vote
- **Key concept:** Network evidence interpretation
- **After discussion:** Show Wireshark captures of RST packets (closed) vs no packets (filtered)
- **Follow-up:** Ask "Why might filtered be harder to diagnose than closed?"

---

## Question 3: Capture Interface Selection

> 💭 **PREDICTION:** If you start Wireshark on Windows and select your Wi-Fi interface, will you see Docker container traffic?

### Scenario

You are running the Week 7 lab in WSL2 with Docker containers. You want to capture traffic between containers using Wireshark on Windows.

Available Wireshark interfaces:
- Ethernet
- Wi-Fi
- vEthernet (WSL)
- Loopback Adapter

### Question

Which interface should you select to capture traffic between Docker containers running in WSL2?

### Options

- **A)** Wi-Fi — because all traffic eventually reaches the physical network — *Misconception: assumes Docker traffic routes externally*
- **B)** Loopback Adapter — because containers use localhost — *Misconception: confuses host loopback with container networking*
- **C)** vEthernet (WSL) — because this is the virtual interface connecting Windows to WSL2 — **CORRECT**
- **D)** Ethernet — because Docker uses bridge networking — *Misconception: conflates Docker bridge with physical Ethernet*

### Correct Answer

**C** — Docker containers in WSL2 communicate through the WSL2 virtual network. The `vEthernet (WSL)` interface on Windows captures this traffic. Physical interfaces (Wi-Fi, Ethernet) only see traffic that leaves the host. Loopback only sees Windows localhost traffic, not WSL2 traffic.

### Targeted Misconception

Students often select the wrong capture interface and wonder why they see no packets. This question addresses the WSL2/Docker networking model.

### Instructor Notes

- **Target accuracy:** 50-60% on first vote
- **Key concept:** Virtual networking in WSL2
- **After discussion:** Demonstrate by starting capture on wrong interface, showing zero packets
- **Alternative:** Use `tcpdump` inside WSL2 if vEthernet capture fails

---

## Question 4: TCP Handshake Evidence

> 💭 **PREDICTION:** How many packets does a successful TCP connection require before any application data can be sent?

### Scenario

You capture traffic while running:

```bash
python3 src/apps/tcp_client.py --host localhost --port 9090 --message "hello"
```

The connection succeeds and echoes back "hello".

### Question

In the packet capture, how many TCP packets are exchanged **before** the "hello" payload appears?

### Options

- **A)** 1 packet (SYN only, server responds with data) — *Misconception: ignores handshake requirement*
- **B)** 2 packets (SYN, SYN-ACK, then data) — *Misconception: forgets client ACK*
- **C)** 3 packets (SYN, SYN-ACK, ACK) — **CORRECT**
- **D)** 4 packets (SYN, SYN-ACK, ACK, ACK) — *Misconception: adds spurious packet*

### Correct Answer

**C** — The TCP three-way handshake requires exactly 3 packets: (1) Client sends SYN, (2) Server responds with SYN-ACK, (3) Client sends ACK. Only after this can application data be transmitted.

### Targeted Misconception

Students may memorise "three-way handshake" without understanding what each packet does. This question verifies they can count and identify handshake packets in a capture.

### Instructor Notes

- **Target accuracy:** 60-70% on first vote (slightly easier)
- **Key concept:** TCP connection establishment
- **After discussion:** Open Wireshark, filter `tcp.flags.syn==1`, count packets
- **Extension:** Ask "What if we see only SYN packets repeating?"

---

## Question 5: UDP Blocking Detection

> 💭 **PREDICTION:** If a UDP packet is dropped by a firewall, what will the sender observe?

### Scenario

You apply a DROP rule for UDP port 9091:

```bash
iptables -A INPUT -p udp --dport 9091 -j DROP
```

Then send a UDP datagram:

```bash
python3 src/apps/udp_sender.py --host localhost --port 9091 --message "test"
```

The sender script reports "Datagram sent successfully".

### Question

Given that the firewall dropped the packet, why does the sender report success?

### Options

- **A)** The firewall is not working correctly — *Misconception: assumes tool failure*
- **B)** UDP is connectionless; the sender cannot know if the receiver got the packet — **CORRECT**
- **C)** The DROP rule only affects incoming traffic from external sources — *Misconception: misunderstands rule scope*
- **D)** Python's socket library automatically retries until delivery succeeds — *Misconception: attributes TCP behaviour to UDP*

### Correct Answer

**B** — UDP provides no delivery confirmation. The `sendto()` call succeeds when the packet is handed to the network stack, not when the receiver acknowledges it. The sender has no way to know the packet was dropped unless the application implements its own acknowledgement protocol.

### Targeted Misconception

Students expect blocking to produce visible errors. This question reveals whether they understand UDP's fire-and-forget nature and why dropped UDP is hard to diagnose.

### Instructor Notes

- **Target accuracy:** 45-55% on first vote
- **Key concept:** UDP connectionless semantics
- **After discussion:** Show that `udp_sender.py` always "succeeds" regardless of receiver state
- **Contrast:** Compare with TCP client behaviour when blocked (timeout or refused)

---

## Summary Table

| Question | Topic | Target Accuracy | Key Misconception |
|----------|-------|-----------------|-------------------|
| Q1 | REJECT vs DROP | 40-50% | Blocking actions are equivalent |
| Q2 | Port states | 35-45% | Closed = filtered |
| Q3 | Capture interface | 50-60% | Physical interface sees Docker traffic |
| Q4 | TCP handshake | 60-70% | Handshake packet count |
| Q5 | UDP blocking | 45-55% | Sender knows if UDP is dropped |

---

*Computer Networks — Week 7: Packet Interception, Filtering and Defensive Port Probing*  
*ASE Bucharest, CSIE | by ing. dr. Antonio Clim*
