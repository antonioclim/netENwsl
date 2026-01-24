# 📦 PCAP Sample Files — Week 7
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> This directory contains reference packet capture files demonstrating key concepts.
> Use these as reference when analysing your own captures.

---

## Naming Convention

All PCAP files follow this naming pattern:

```
week{NN}_lo{X}_{protocol}_{scenario}.pcap

Where:
  NN = Week number (07)
  X  = Learning Objective number (1-6)
  protocol = tcp, udp, icmp, mixed
  scenario = descriptive name (snake_case)
```

### Examples

| Filename | LO | Description |
|----------|-----|-------------|
| `week07_lo1_tcp_handshake.pcap` | LO1 | Complete TCP three-way handshake |
| `week07_lo1_udp_baseline.pcap` | LO1 | UDP datagram exchange |
| `week07_lo2_tcp_blocked_reject.pcap` | LO2 | TCP blocked with REJECT (RST visible) |
| `week07_lo2_tcp_blocked_drop.pcap` | LO2 | TCP blocked with DROP (timeout) |
| `week07_lo3_udp_dropped.pcap` | LO3 | UDP packets dropped by firewall |
| `week07_lo4_timeout_analysis.pcap` | LO4 | Connection timeout investigation |
| `week07_lo6_drop_vs_reject.pcap` | LO6 | Side-by-side DROP vs REJECT |

---

## Sample Descriptions

### week07_lo1_tcp_handshake.pcap

**Purpose:** Demonstrate complete TCP connection lifecycle

**Contents:**
- TCP three-way handshake (SYN, SYN-ACK, ACK)
- Data exchange (echo request/response)
- Connection teardown (FIN, FIN-ACK)

**Key Packets:**
| Frame | Flags | Description |
|-------|-------|-------------|
| 1 | SYN | Client initiates connection |
| 2 | SYN,ACK | Server acknowledges and responds |
| 3 | ACK | Client completes handshake |
| 4 | PSH,ACK | Client sends "hello" |
| 5 | PSH,ACK | Server echoes "hello" |
| 6-9 | FIN sequence | Connection teardown |

**Wireshark Filter:** `tcp.port == 9090`

**How Generated:**
```bash
# Start capture
python3 scripts/capture_traffic.py --output pcap/samples/week07_lo1_tcp_handshake.pcap --duration 30

# Generate traffic
python3 src/apps/tcp_client.py --host localhost --port 9090 --message "hello"
```

---

### week07_lo1_udp_baseline.pcap

**Purpose:** Demonstrate UDP connectionless communication

**Contents:**
- Single UDP datagram (no handshake)
- Optional response from receiver

**Key Packets:**
| Frame | Protocol | Description |
|-------|----------|-------------|
| 1 | UDP | Client sends datagram |
| 2 | UDP | Server response (if echoing) |

**Wireshark Filter:** `udp.port == 9091`

**How Generated:**
```bash
python3 scripts/capture_traffic.py --output pcap/samples/week07_lo1_udp_baseline.pcap --duration 10

python3 src/apps/udp_sender.py --host localhost --port 9091 --message "test"
```

---

### week07_lo2_tcp_blocked_reject.pcap

**Purpose:** Show network evidence of REJECT action

**Contents:**
- TCP SYN attempt
- ICMP Destination Unreachable OR TCP RST

**Key Packets:**
| Frame | Type | Description |
|-------|------|-------------|
| 1 | TCP SYN | Client attempts connection |
| 2 | TCP RST | Firewall rejects (or ICMP type 3) |

**Wireshark Filter:** `tcp.port == 9090 or icmp.type == 3`

**How Generated:**
```bash
# Apply REJECT rule
python3 src/apps/firewallctl.py --profile block_tcp_9090_reject

# Capture
python3 scripts/capture_traffic.py --output pcap/samples/week07_lo2_tcp_blocked_reject.pcap --duration 15

# Attempt connection
python3 src/apps/tcp_client.py --host localhost --port 9090 --timeout 5
```

---

### week07_lo2_tcp_blocked_drop.pcap

**Purpose:** Show network evidence of DROP action (silence)

**Contents:**
- Multiple TCP SYN attempts (retransmissions)
- NO responses (contrast with REJECT)

**Key Packets:**
| Frame | Type | Description |
|-------|------|-------------|
| 1 | TCP SYN | Initial attempt |
| 2 | TCP SYN | Retransmit (1s later) |
| 3 | TCP SYN | Retransmit (2s later) |
| ... | ... | More retransmits until timeout |

**Wireshark Filter:** `tcp.port == 9090 && tcp.flags.syn == 1`

**How Generated:**
```bash
# Apply DROP rule
python3 src/apps/firewallctl.py --profile block_tcp_9090_drop

# Capture (longer duration for retransmits)
python3 scripts/capture_traffic.py --output pcap/samples/week07_lo2_tcp_blocked_drop.pcap --duration 30

# Attempt connection
python3 src/apps/tcp_client.py --host localhost --port 9090 --timeout 10
```

---

### week07_lo6_drop_vs_reject.pcap

**Purpose:** Side-by-side comparison for LO6 evaluation

**Contents:**
- First half: DROP scenario (retransmits, no response)
- Second half: REJECT scenario (single SYN, immediate RST)

**Wireshark Filter:** `tcp.port == 9090`

**Analysis Questions:**
1. At what timestamp does the DROP sequence end?
2. How many retransmit packets in DROP vs REJECT?
3. What is the total time difference?

---

## Generating Your Own Samples

### Basic Capture Command

```bash
python3 scripts/capture_traffic.py \
    --interface any \
    --output pcap/my_capture.pcap \
    --duration 60 \
    --filter "port 9090 or port 9091"
```

### Using tcpdump Directly

```bash
sudo tcpdump -i any \
    -w pcap/my_capture.pcap \
    -c 100 \
    port 9090 or port 9091
```

### Inside Docker Container

```bash
# Start capture inside container
docker exec -it week7_tcp_server tcpdump -i eth0 -w /tmp/capture.pcap -c 50

# Copy out
docker cp week7_tcp_server:/tmp/capture.pcap pcap/container_capture.pcap
```

---

## Analysing Samples

### Open in Wireshark

```bash
# From Windows (if pcap in WSL)
# Navigate to \\wsl$\Ubuntu\path\to\pcap in Explorer
# Double-click to open in Wireshark
```

### Quick Analysis with tshark

```bash
# Packet count by protocol
tshark -r pcap/samples/week07_lo1_tcp_handshake.pcap -q -z io,phs

# TCP conversation summary
tshark -r pcap/samples/week07_lo1_tcp_handshake.pcap -q -z conv,tcp

# Extract specific fields
tshark -r pcap/samples/week07_lo2_tcp_blocked_reject.pcap \
    -T fields -e frame.number -e ip.src -e ip.dst -e tcp.flags
```

---

## File Integrity

Verify sample files haven't been corrupted:

| File | MD5 Checksum | Size |
|------|--------------|------|
| week07_lo1_tcp_handshake.pcap | *generate after creation* | ~2KB |
| week07_lo1_udp_baseline.pcap | *generate after creation* | ~1KB |
| week07_lo2_tcp_blocked_reject.pcap | *generate after creation* | ~1KB |
| week07_lo2_tcp_blocked_drop.pcap | *generate after creation* | ~3KB |
| week07_lo6_drop_vs_reject.pcap | *generate after creation* | ~4KB |

**Generate checksums:**
```bash
md5sum pcap/samples/*.pcap
```

---

*Computer Networks — Week 7: Packet Interception, Filtering and Defensive Port Probing*  
*ASE Bucharest, CSIE | by ing. dr. Antonio Clim*
