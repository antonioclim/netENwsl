# 📦 Packet Captures — Week 6: NAT/PAT & SDN

> Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

## Overview

This folder stores network packet captures (.pcap files) generated during laboratory exercises. These captures are essential for:
- Verifying NAT translation behaviour
- Observing OpenFlow controller-switch communication
- Debugging connectivity issues
- Post-lab analysis with Wireshark

---

## Naming Convention

Use the following naming pattern for consistency:

```
week06_{topology}_{protocol}_{scenario}_{timestamp}.pcap
```

**Examples:**
- `week06_nat_icmp_ping_through_nat_20260124.pcap`
- `week06_sdn_openflow_flow_installation_20260124.pcap`
- `week06_nat_tcp_http_request_20260124.pcap`

---

## Capture Generation

### Method 1: Using tcpdump in Mininet CLI

```bash
# Capture NAT traffic on router's public interface
rnat tcpdump -i rnat-eth1 -w /home/student/week6/pcap/nat_public.pcap -c 100

# Capture all traffic on switch port
s1 tcpdump -i s1-eth1 -w /home/student/week6/pcap/sdn_h1.pcap -c 100

# Capture ARP traffic specifically
h1 tcpdump -i h1-eth0 -w /home/student/week6/pcap/arp_only.pcap arp
```

### Method 2: Using Wireshark (Native Windows)

1. Open Wireshark on Windows host
2. Select the correct interface:
   - For Docker: `vEthernet (WSL)` or similar
   - For direct WSL: Use the WSL IP range filter
3. Apply display filter for relevant traffic
4. Save capture to shared folder

### Method 3: Using scripts/run_demo.py

```bash
# Capture automatically during demo
python scripts/run_demo.py --demo nat --capture

# Captures are saved to pcap/ directory
```

---

## Recommended Captures for Week 6

### NAT/PAT Exercises

| Capture Name | Interface | Filter | Purpose |
|--------------|-----------|--------|---------|
| `nat_outbound.pcap` | rnat-eth1 | `ip` | Observe translated source IPs |
| `nat_inbound.pcap` | rnat-eth0 | `ip` | Compare with original IPs |
| `nat_conntrack.pcap` | rnat-eth1 | `tcp or udp` | Correlate with conntrack table |

**What to look for:**
- Source IP changes from 192.168.1.x → 203.0.113.1
- Source port may change (PAT)
- Return traffic has destination 203.0.113.1:port

### SDN Exercises

| Capture Name | Interface | Filter | Purpose |
|--------------|-----------|--------|---------|
| `sdn_openflow.pcap` | lo (controller) | `tcp port 6633` | Controller-switch messages |
| `sdn_permitted.pcap` | s1-eth2 | `icmp` | Successful ping (h1→h2) |
| `sdn_blocked.pcap` | s1-eth3 | `icmp` | Blocked ping (h1→h3) |

**What to look for:**
- OpenFlow packet-in messages (0x0a)
- OpenFlow flow-mod messages (0x0e)
- ICMP packets present/absent based on policy

---

## Analysis Guide

### Wireshark Display Filters

```
# NAT analysis
ip.src == 192.168.1.0/24          # Traffic from private network
ip.src == 203.0.113.1             # Traffic from NAT public IP
tcp.port == 5000                   # NAT observer traffic

# SDN/OpenFlow analysis
openflow_v4                        # All OpenFlow 1.3 messages
openflow_v4.type == 10            # Packet-in only
openflow_v4.type == 14            # Flow-mod only

# ARP analysis
arp                               # All ARP traffic
arp.opcode == 1                   # ARP requests only
arp.opcode == 2                   # ARP replies only

# ICMP analysis
icmp                              # All ICMP
icmp.type == 8                    # Echo request (ping)
icmp.type == 0                    # Echo reply
```

### Wireshark Columns for NAT Analysis

Add these columns for easier analysis:
1. Source IP
2. Destination IP
3. Source Port
4. Destination Port
5. Info

**Tip:** Right-click column header → Column Preferences → Add columns

---

## Expected Observations

### NAT Translation Example

**Before NAT (captured on rnat-eth0):**
```
Source: 192.168.1.10:45678
Destination: 203.0.113.2:5000
```

**After NAT (captured on rnat-eth1):**
```
Source: 203.0.113.1:50001    ← IP and port changed!
Destination: 203.0.113.2:5000
```

### SDN Flow Installation Example

**Packet-in (switch → controller):**
```
OpenFlow 1.3, Type: OFPT_PACKET_IN (10)
Buffer ID: 0x00000001
Total Length: 98
Reason: OFPR_NO_MATCH (0)
Table ID: 0
Data: [Ethernet frame that triggered packet-in]
```

**Flow-mod (controller → switch):**
```
OpenFlow 1.3, Type: OFPT_FLOW_MOD (14)
Cookie: 0x0000000000000000
Command: OFPFC_ADD (0)
Priority: 100
Match: nw_src=10.0.6.11, nw_dst=10.0.6.12
Instructions: Apply-Actions: Output:2
```

---

## Troubleshooting Capture Issues

### No packets captured
1. Verify interface name: `ip link show`
2. Check traffic is actually flowing: `ping` from another terminal
3. Ensure tcpdump has permissions: run with `sudo`

### Capture file too large
- Limit packet count: `tcpdump -c 1000`
- Limit by time: `timeout 60 tcpdump ...`
- Filter specific traffic: add BPF filter

### Cannot open in Wireshark
- Check file permissions
- Ensure file transfer didn't corrupt (use binary mode)
- Verify Wireshark version supports pcap format

---

## File Management

```bash
# Clean old captures (keep last 7 days)
find pcap/ -name "*.pcap" -mtime +7 -delete

# Compress captures for storage
gzip pcap/*.pcap

# List captures by size
ls -lhS pcap/*.pcap
```

---

## Integration with Lab Scripts

The lab scripts can automatically generate captures:

```python
# In scripts/run_demo.py
python scripts/run_demo.py --demo nat --capture --capture-dir pcap/
```

Captures are timestamped and saved to this directory.

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
