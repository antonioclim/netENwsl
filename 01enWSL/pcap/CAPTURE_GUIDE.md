# PCAP Capture Guide

> Manual instructions for capturing network traffic during laboratory exercises.
> Computer Networks - Week 1 | ASE Bucharest | by ing. dr. Antonio Clim

---

## Overview

This guide provides step-by-step instructions for capturing network traffic that demonstrates the protocols covered in Week 1.

### Available Demo Files

| File | Protocol | Packets | Learning Objective |
|------|----------|---------|-------------------|
| `demo_icmp_ping.pcap` | ICMP | 8 | LO1: Latency measurement |
| `demo_tcp_handshake.pcap` | TCP | 10 | LO2: TCP socket communication |
| `demo_dns_query.pcap` | DNS | 2 | LO4, LO7: Traffic capture |
| `demo_http_get.pcap` | HTTP | 4 | LO4: Protocol analysis |

---

## Method 1: Synthetic Generation (Recommended)

Use the provided Python script to generate reproducible PCAP files:

```bash
# Install scapy (if not already installed)
pip install scapy --break-system-packages

# Generate all demo files
cd pcap/
python generate_demo_pcaps.py --all

# Verify generation
ls -la *.pcap
```

**Advantages:**
- Reproducible results
- Works without running containers
- CI/CD friendly
- Controlled packet content

---

## Method 2: Live Capture with tcpdump

### Prerequisites

1. Lab container running:
   ```bash
   docker compose -f docker/docker-compose.yml up -d
   ```

2. Terminal access to container:
   ```bash
   docker exec -it week1_lab bash
   ```

### Capture ICMP Ping

**In Container Terminal 1 (capture):**
```bash
tcpdump -i lo -w /work/pcap/live_icmp_ping.pcap icmp &
```

**In Container Terminal 2 (generate traffic):**
```bash
ping -c 4 127.0.0.1
```

**Stop capture:**
```bash
pkill tcpdump
```

**Expected result:** 8 packets (4 request + 4 reply)

### Capture TCP Handshake

**In Container Terminal 1 (capture):**
```bash
tcpdump -i lo -w /work/pcap/live_tcp_handshake.pcap port 9090 &
```

**In Container Terminal 2 (server):**
```bash
nc -l -p 9090
```

**In Container Terminal 3 (client):**
```bash
echo "Hello, Server!" | nc localhost 9090
```

**Stop capture:**
```bash
pkill tcpdump
```

**Expected packets:**
1. SYN (client -> server)
2. SYN-ACK (server -> client)
3. ACK (client -> server)
4. PSH-ACK with "Hello, Server!" data
5. ACK (data acknowledgement)
6. FIN-ACK (connection close)
7. ACK (final acknowledgement)

### Capture DNS Query

**Note:** This requires network access from the container.

**In Container:**
```bash
# Start capture
tcpdump -i eth0 -w /work/pcap/live_dns_query.pcap port 53 &

# Generate DNS traffic
nslookup example.com

# Stop capture
pkill tcpdump
```

---

## Method 3: Wireshark Capture (Windows)

### Step 1: Start Wireshark

1. Open Wireshark from Windows Start Menu
2. Select interface: **vEthernet (WSL)**

### Step 2: Configure Capture Filter

Before starting capture, set a capture filter:

| Protocol | Capture Filter |
|----------|----------------|
| ICMP only | `icmp` |
| TCP port 9090 | `tcp port 9090` |
| DNS only | `udp port 53` |
| HTTP only | `tcp port 80` |

### Step 3: Generate Traffic

Run the appropriate commands in WSL:

```bash
# For ICMP
docker exec week1_lab ping -c 4 172.20.1.1

# For TCP
docker exec week1_lab python3 /work/src/exercises/ex_1_02_tcp_server_client.py --no-predict
```

### Step 4: Save Capture

1. Click the red square (Stop capture)
2. File -> Save As
3. Navigate to: `D:\NETWORKING\WEEK1\pcap\`
4. Filename: `wireshark_<protocol>_<date>.pcap`
5. Format: Wireshark/pcapng

---

## Verifying Captures

### Check Packet Count

```bash
# Using tcpdump
tcpdump -r demo_icmp_ping.pcap | wc -l

# Using tshark (if available)
tshark -r demo_icmp_ping.pcap | wc -l
```

### View Packet Summary

```bash
tcpdump -r demo_tcp_handshake.pcap -n
```

### Expected Output for TCP Handshake

```
IP 172.20.1.10.54321 > 172.20.1.1.9090: Flags [S], seq 1000
IP 172.20.1.1.9090 > 172.20.1.10.54321: Flags [S.], seq 2000, ack 1001
IP 172.20.1.10.54321 > 172.20.1.1.9090: Flags [.], ack 2001
IP 172.20.1.10.54321 > 172.20.1.1.9090: Flags [P.], seq 1001:1016, ack 2001
...
```

### Using Python to Verify

```python
#!/usr/bin/env python3
"""Quick PCAP verification script."""
import dpkt


def verify_pcap(filename):
    with open(filename, "rb") as f:
        try:
            pcap = dpkt.pcap.Reader(f)
        except ValueError:
            pcap = dpkt.pcapng.Reader(f)

        packets = list(pcap)
        print(f"{filename}: {len(packets)} packets")
        return len(packets)


# Verify all demo files
for name in [
    "demo_icmp_ping.pcap",
    "demo_tcp_handshake.pcap",
    "demo_dns_query.pcap",
    "demo_http_get.pcap",
]:
    try:
        verify_pcap(name)
    except FileNotFoundError:
        print(f"{name}: NOT FOUND")
```

---

## Naming Convention

Use this naming pattern for captured files:

```
<source>_<protocol>_<scenario>.pcap
```

**Examples:**
- `live_icmp_ping.pcap` — Live capture of ICMP ping
- `demo_tcp_handshake.pcap` — Synthetic TCP handshake
- `wireshark_dns_query_20260124.pcap` — Wireshark capture with date

---

## Troubleshooting

### "Permission denied" when capturing

```bash
# Run tcpdump with sudo
sudo tcpdump -i eth0 -w capture.pcap
```

### "No packets captured"

1. Verify correct interface: `ip addr show`
2. Check traffic is being generated during capture
3. Verify capture filter syntax

### "PCAP file is empty"

1. Ensure traffic was generated AFTER starting capture
2. Check the interface matches traffic path
3. Verify filter is not too restrictive

### Cannot open PCAP in Wireshark

1. Check file was not corrupted (partial write)
2. Try opening with: `wireshark -r filename.pcap`
3. Verify file format with: `file filename.pcap`

---

## Integration with Exercises

### LO1: Latency Measurement

Use `demo_icmp_ping.pcap` to:
- Measure time between request and reply
- Compare with `ping` RTT output

### LO2: TCP Communication

Use `demo_tcp_handshake.pcap` to:
- Identify SYN, SYN-ACK, ACK packets
- Track sequence numbers
- Understand connection states

### LO4: PCAP Analysis

Use any demo file with `ex_1_04_pcap_stats.py`:
```bash
python src/exercises/ex_1_04_pcap_stats.py --file pcap/demo_tcp_handshake.pcap
```

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
