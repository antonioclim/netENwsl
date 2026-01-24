# 📝 Formative Assessment — Week 1
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Quick checks to verify understanding before, during and after the laboratory session.

---

## Pre-Lab Quick Check (5 minutes)

Answer these questions **before** starting the laboratory exercises. This helps identify gaps to focus on.

### Questions

1. What is the difference between **latency** and **bandwidth**?

2. What command shows your machine's IP addresses in Linux?

3. What does the **LISTEN** socket state mean?

4. In Docker, what is the difference between an **image** and a **container**?

5. What port does Portainer use by default?

### Self-Check Answers

<details>
<summary>Click to reveal answers</summary>

1. **Latency** = time for data to travel (measured in ms); **Bandwidth** = data volume per second (measured in Mbps)

2. `ip addr` or `ip addr show` (legacy: `ifconfig`)

3. Server socket is waiting for incoming connections (not yet communicating)

4. **Image** = read-only template; **Container** = running instance of an image

5. Port **9000** (http://localhost:9000)

**Scoring:**
- 5/5: Ready to proceed
- 3-4/5: Review the theory summary before starting
- 0-2/5: Read docs/theory_summary.md carefully first

</details>

---

## During-Lab Checkpoints

### Checkpoint 1: After Exercise 1 (Network Inspection)

**Quick verification:**
```bash
# Can you answer these from your output?
ip addr show
```

- [ ] I can identify my loopback interface (lo)
- [ ] I can identify my primary network interface (eth0 or similar)
- [ ] I can read an IP address with subnet mask (e.g., 172.20.1.5/24)

### Checkpoint 2: After Exercise 2 (Connectivity)

**Quick verification:**
```bash
ping -c 2 127.0.0.1
```

- [ ] I understand what RTT (round-trip time) means
- [ ] I can explain why loopback ping has very low latency (<1ms)
- [ ] I know the difference between ping success and failure

### Checkpoint 3: After Exercise 3 (TCP/UDP)

**Quick verification:**
```bash
ss -tlnp
```

- [ ] I can identify which ports have listening services
- [ ] I understand the TCP three-way handshake (SYN → SYN-ACK → ACK)
- [ ] I can explain why netcat is useful for testing

### Checkpoint 4: After Exercise 4 (Capture)

**Quick verification:**
- [ ] I captured at least one pcap file
- [ ] I can apply a filter in Wireshark (e.g., `tcp.port == 9090`)
- [ ] I can follow a TCP stream in Wireshark

---

## Exit Ticket (End of Session)

Complete this **before leaving** the laboratory. Hand in or self-assess.

### Part A: Concept Check (1 point each)

1. **True or False:** Ping measures bandwidth.
   - [ ] True
   - [ ] False

2. **True or False:** A Docker container's localhost is the same as the host's localhost.
   - [ ] True
   - [ ] False

3. **Fill in:** The TCP three-way handshake consists of: SYN → _______ → ACK

4. **Match:** Connect each command to its purpose:
   
   | Command | Purpose |
   |---------|---------|
   | `ip addr` | A. Show listening ports |
   | `ss -tlnp` | B. Test connectivity |
   | `ping` | C. Show IP addresses |
   | `docker ps` | D. List containers |

5. **Short answer:** Why might you use UDP instead of TCP?

### Part B: Practical Application (2 points each)

6. Write the command to ping google.com exactly 4 times:
   ```
   _________________________________
   ```

7. Write the command to show all listening TCP ports with process information:
   ```
   _________________________________
   ```

8. You run `docker ps` and see nothing. Your container exists but isn't shown. What command shows all containers including stopped ones?
   ```
   _________________________________
   ```

### Part C: Reflection (3 points)

9. What was the most challenging concept today and why?

10. What would you like to explore further next week?

---

## Exit Ticket Answers

<details>
<summary>Click to reveal answers</summary>

**Part A:**
1. **False** — Ping measures latency (RTT), not bandwidth
2. **False** — Containers have isolated network namespaces
3. **SYN-ACK**
4. `ip addr` → C, `ss -tlnp` → A, `ping` → B, `docker ps` → D
5. When speed matters more than reliability (streaming, gaming, DNS)

**Part B:**
6. `ping -c 4 google.com`
7. `ss -tlnp`
8. `docker ps -a`

**Part C:** Personal reflection — no single correct answer

**Grading:**
- Part A: 5 points (1 each)
- Part B: 6 points (2 each)
- Part C: 3 points (effort-based)
- **Total: 14 points**

</details>

---

## Self-Assessment Rubric

Use this to evaluate your own understanding:

| Level | Description | Action |
|-------|-------------|--------|
| 🟢 **Confident** | Can explain concept to others, apply in new situations | Ready for homework |
| 🟡 **Developing** | Understand with notes, need practice | Review before homework |
| 🔴 **Struggling** | Confused, cannot apply independently | Seek help, re-read theory |

### Week 1 Concepts Self-Rating

| Concept | 🟢 | 🟡 | 🔴 |
|---------|-----|-----|-----|
| Latency vs Bandwidth | [ ] | [ ] | [ ] |
| IP addresses and interfaces | [ ] | [ ] | [ ] |
| Socket states (LISTEN, ESTABLISHED) | [ ] | [ ] | [ ] |
| TCP three-way handshake | [ ] | [ ] | [ ] |
| Docker containers vs images | [ ] | [ ] | [ ] |
| Wireshark capture and filters | [ ] | [ ] | [ ] |
| Basic Linux networking commands | [ ] | [ ] | [ ] |

---

## Common Gaps and Resources

If you marked 🔴 on any concept, here are targeted resources:

| Concept | Resource |
|---------|----------|
| Latency vs Bandwidth | docs/misconceptions.md §1 |
| IP addresses | docs/glossary.md (Core Networking Terms) |
| Socket states | docs/glossary.md (Socket States) |
| TCP handshake | docs/peer_instruction.md Q2 |
| Docker basics | docs/concept_analogies.md (Container: Food Truck) |
| Wireshark | README.md §Wireshark Setup |
| Linux commands | docs/commands_cheatsheet.md |

---

*NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim*
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
