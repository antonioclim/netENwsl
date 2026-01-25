# ❌ Common Misconceptions — Week 7
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> This document lists common misunderstandings about packet capture and filtering, with corrections and verification methods.

---

## Filtering Actions

### 🚫 Misconception 1: "DROP and REJECT have the same effect"

**WRONG:** "Both DROP and REJECT block traffic, so they're interchangeable."

**CORRECT:** DROP and REJECT have fundamentally different behaviours that affect debugging and security.

| Aspect | DROP | REJECT |
|--------|------|--------|
| Packet fate | Silently discarded | Discarded with notification |
| Client experience | Timeout (waits for response) | Immediate error (connection refused) |
| Network evidence | No packets from firewall | RST or ICMP packet sent |
| Debugging | Harder (looks like packet loss) | Easier (explicit refusal) |
| Security | Stealthier (hides firewall) | Reveals firewall presence |

When debugging connection problems, I recommend using REJECT during development. The immediate feedback saves considerable time compared to waiting for timeouts. Switch to DROP only when you need stealth in production.

**Practical verification:**

```bash
# Apply DROP rule
sudo iptables -A INPUT -p tcp --dport 9090 -j DROP

# Test — client will hang until timeout
python3 src/apps/tcp_client.py --host localhost --port 9090 --timeout 5
# Output: [waits 5 seconds] Connection timed out

# Apply REJECT rule instead
sudo iptables -D INPUT -p tcp --dport 9090 -j DROP
sudo iptables -A INPUT -p tcp --dport 9090 -j REJECT

# Test — client fails immediately  
python3 src/apps/tcp_client.py --host localhost --port 9090 --timeout 5
# Output: [instant] Connection refused
```

---

### 🚫 Misconception 2: "A filtered port is the same as a closed port"

**WRONG:** "If I can't connect to a port, it's closed."

**CORRECT:** There are three distinct port states with different network evidence.

| State | Meaning | Network Evidence |
|-------|---------|------------------|
| **Open** | Service listening, accepts connections | TCP: completes handshake; UDP: may respond |
| **Closed** | No service listening, but host reachable | TCP: RST packet; UDP: ICMP port unreachable |
| **Filtered** | Cannot determine state (firewall blocking) | No response at all (DROP) or ICMP admin prohibited |

**Why this matters:** A closed port confirms the host is alive. A filtered port reveals nothing — it could be a firewall, packet loss or non-existent host.

**Practical verification:**

```bash
# Probe a closed port (no service, no firewall)
python3 src/apps/port_probe.py --host localhost --ports 9999 --timeout 2
# Result: closed (RST received)

# Probe a filtered port (firewall DROP)
sudo iptables -A INPUT -p tcp --dport 9999 -j DROP
python3 src/apps/port_probe.py --host localhost --ports 9999 --timeout 2
# Result: filtered (no response)
```

---

## Packet Capture

### 🚫 Misconception 3: "tcpdump captures all traffic automatically"

**WRONG:** "Running `tcpdump` will show me everything happening on the network."

**CORRECT:** tcpdump only captures traffic visible to the selected interface and filters determine what is recorded.

| Factor | Impact |
|--------|--------|
| Interface selection | `-i eth0` only sees eth0 traffic |
| Promiscuous mode | Required to see traffic not destined for this host |
| Capture filters | BPF filters limit what is captured |
| Permissions | Root/sudo required for raw packet access |
| Container isolation | Traffic inside container network may need capture inside container |

**Practical verification:**

```bash
# Wrong: captures nothing useful if interface is wrong
tcpdump -i eth0  # Won't see Docker bridge traffic

# Correct: capture on Docker bridge or use 'any'
sudo tcpdump -i any port 9090

# Or capture inside the container
docker exec week7_tcp_server tcpdump -i eth0
```

---

### 🚫 Misconception 4: "Wireshark on Windows sees all Docker traffic"

**WRONG:** "I can open Wireshark on Windows and see my Docker containers communicating."

**CORRECT:** Docker containers in WSL2 use a virtual network. You must capture on the correct interface.

| Interface | What it captures |
|-----------|------------------|
| Wi-Fi / Ethernet | Physical network traffic (external) |
| Loopback Adapter | Windows localhost only (127.0.0.1) |
| **vEthernet (WSL)** | WSL2 virtual network (Docker traffic) ✓ |

This trips up students every semester. The moment you select Wi-Fi instead of vEthernet (WSL), your capture will show nothing useful.

**Why this matters:** Selecting the wrong interface shows zero packets, leading students to think the lab is broken.

**Practical verification:**

```
1. Open Wireshark on Windows
2. Select "vEthernet (WSL)" interface
3. Start capture
4. In WSL, run: python3 src/apps/tcp_client.py --host localhost --port 9090
5. Observe TCP packets in Wireshark
```

**Alternative if vEthernet fails:**

```bash
# Capture inside WSL and copy out
sudo tcpdump -i any -w /mnt/d/capture.pcap port 9090
# Open /mnt/d/capture.pcap in Windows Wireshark
```

---

### 🚫 Misconception 5: "Packet capture has no performance impact"

**WRONG:** "I can run tcpdump continuously in production without consequences."

**CORRECT:** Packet capture consumes CPU, memory and disk I/O. In high-traffic environments, it can cause packet drops.

| Impact | Description |
|--------|-------------|
| CPU | Kernel copies each packet to userspace |
| Memory | Capture buffer holds packets before writing |
| Disk I/O | Writing pcap files at wire speed is expensive |
| Packet drops | If capture can't keep up, packets are lost |

**Best practices:**

```bash
# Limit capture with filters
sudo tcpdump -i eth0 'port 9090' -w capture.pcap

# Limit packet size (headers only)
sudo tcpdump -i eth0 -s 96 -w headers.pcap

# Limit duration or count
sudo tcpdump -i eth0 -c 1000 -w limited.pcap
sudo timeout 60 tcpdump -i eth0 -w timed.pcap
```

---

## TCP/UDP Behaviour

### 🚫 Misconception 6: "UDP blocking is immediately detectable"

**WRONG:** "If a UDP packet is blocked, my sender will get an error."

**CORRECT:** UDP is connectionless. The sender has no confirmation of delivery and cannot distinguish between dropped and delivered packets.

| Protocol | Delivery confirmation | Blocking detection |
|----------|----------------------|-------------------|
| TCP | Yes (ACK packets) | Timeout or RST/ICMP |
| UDP | No (fire-and-forget) | Cannot detect without application-layer ACK |

**Why this matters:** A UDP sender always "succeeds" at the socket level, even if every packet is dropped. In practice, if you need reliable delivery, you must implement acknowledgements at the application layer or use TCP.

**Practical verification:**

```bash
# Block UDP
sudo iptables -A INPUT -p udp --dport 9091 -j DROP

# Send UDP — reports success!
python3 src/apps/udp_sender.py --host localhost --port 9091 --message "test"
# Output: Datagram sent successfully

# But receiver sees nothing
python3 src/apps/udp_receiver.py --port 9091
# Output: [waiting indefinitely]
```

---

### 🚫 Misconception 7: "TCP RST always means firewall rejection"

**WRONG:** "If I see a TCP RST packet, a firewall blocked my connection."

**CORRECT:** TCP RST can come from multiple sources.

| RST Source | Meaning |
|------------|---------|
| Server (closed port) | No service listening on that port |
| Server (application) | Application explicitly closed connection |
| Firewall (REJECT) | Firewall blocking with active refusal |
| Client | Client aborting connection |
| Middlebox | NAT/proxy timeout or policy |

**How to distinguish:**

```bash
# Check RST source IP in Wireshark
# - If RST comes from destination IP: server or its firewall
# - If RST comes from intermediate IP: middlebox

# Check timing
# - Immediate RST after SYN: closed port or REJECT rule
# - RST after established connection: application close or timeout
```

---

## Firewall Configuration

### 🚫 Misconception 8: "iptables rules persist after reboot"

**WRONG:** "I added an iptables rule, so it will still be there tomorrow."

**CORRECT:** iptables rules are stored in kernel memory and lost on reboot unless explicitly saved.

**Practical verification:**

```bash
# Add rule
sudo iptables -A INPUT -p tcp --dport 9090 -j DROP

# Verify it exists
sudo iptables -L INPUT -n | grep 9090
# Shows the rule

# After reboot (or Docker container restart)
sudo iptables -L INPUT -n | grep 9090
# Rule is gone!
```

**To persist rules:**

```bash
# Save rules
sudo iptables-save > /etc/iptables.rules

# Restore on boot (add to /etc/rc.local or systemd)
sudo iptables-restore < /etc/iptables.rules
```

**In Docker:** Container restarts clear iptables. Use entrypoint scripts or Docker's `--cap-add=NET_ADMIN` with rule application on start.

---

## Summary Table

| # | Misconception | Reality |
|---|---------------|---------|
| 1 | DROP = REJECT | DROP times out; REJECT refuses immediately |
| 2 | Filtered = Closed | Closed sends RST; filtered sends nothing |
| 3 | tcpdump sees all | Only sees selected interface traffic |
| 4 | Wireshark sees Docker | Must use vEthernet (WSL) interface |
| 5 | Capture is free | Capture has CPU/memory/disk cost |
| 6 | UDP block is visible | UDP sender cannot detect drops |
| 7 | RST = firewall | RST can come from server, app or middlebox |
| 8 | iptables persists | Rules lost on reboot unless saved |

---

*Computer Networks — Week 7: Packet Interception, Filtering and Defensive Port Probing*  
*ASE Bucharest, CSIE | by ing. dr. Antonio Clim*
