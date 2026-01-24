# 📁 PCAP Sample Files — Week 6: NAT/PAT & SDN

> Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

## Overview

This directory contains network captures (PCAP files) for analysis exercises.
Samples are generated during lab execution — they contain YOUR unique traffic.

---

## Pre-generated Samples

After running the laboratory exercises, you should have these captures:

| File | Description | LO Coverage | How to Generate |
|------|-------------|-------------|-----------------|
| `week06_nat_handshake.pcap` | TCP 3-way handshake through NAT | LO2, LO3 | Exercise 1, Step 7 |
| `week06_nat_conntrack.pcap` | Full NAT session with conntrack | LO2 | `make capture-nat` |
| `week06_sdn_flow_install.pcap` | OpenFlow FLOW_MOD messages | LO4 | Exercise 2, Step 5 |
| `week06_sdn_packet_in.pcap` | Packet-In to controller | LO4, LO5 | `make capture-sdn` |
| `week06_arp_resolution.pcap` | ARP request/reply in NAT topo | LO1 | Homework 6.2 |

---

## Capture Commands

### NAT Topology Captures

```bash
# In the Mininet CLI, start capture on public interface:
rnat tcpdump -i rnat-eth1 -w /tmp/nat_capture.pcap -c 50 &

# Generate traffic:
h1 ping -c 5 203.0.113.2
h1 python3 src/apps/nat_observer.py client --host 203.0.113.2 --port 5000

# Stop capture:
rnat pkill tcpdump

# Copy capture out:
# (from host) docker cp mininet:/tmp/nat_capture.pcap ./pcap/
```

### SDN Topology Captures

```bash
# Capture OpenFlow messages on controller interface:
tcpdump -i lo -n port 6633 -w /tmp/openflow.pcap -c 100 &

# Generate traffic that triggers flow installation:
h1 ping -c 3 10.0.6.12  # Permitted
h1 ping -c 3 10.0.6.13  # Blocked (generates packet-in)

# Stop capture:
pkill tcpdump
```

---

## Naming Convention

```
week{NN}_lo{X}_{protocol}_{scenario}.pcap
```

**Examples:**
- `week06_lo2_tcp_nat_session.pcap` — TCP session through NAT for LO2
- `week06_lo4_openflow_flowmod.pcap` — OpenFlow flow installation for LO4
- `week06_lo5_icmp_blocked.pcap` — Blocked ICMP for SDN policy analysis

---

## Wireshark Display Filters

See `week06_example_filters.txt` for ready-to-use filters.

### Quick Reference

| Analysis Goal | Wireshark Filter |
|---------------|------------------|
| NAT traffic only | `ip.addr == 203.0.113.0/24` |
| Private network | `ip.addr == 192.168.1.0/24` |
| Conntrack-relevant | `tcp.flags.syn == 1 or tcp.flags.fin == 1` |
| OpenFlow messages | `openflow_v4` |
| ICMP only | `icmp` |
| ARP only | `arp` |

---

## Verification Tasks

After capturing, verify your PCAPs contain expected data:

### NAT Capture Checklist

- [ ] Contains packets with source 192.168.1.x (internal)
- [ ] Contains packets with source 203.0.113.1 (translated)
- [ ] Same conversation appears with different source IPs (before/after NAT)
- [ ] TCP handshake visible (SYN, SYN-ACK, ACK)

### SDN Capture Checklist

- [ ] Contains OpenFlow PACKET_IN messages (type=10)
- [ ] Contains OpenFlow FLOW_MOD messages (type=14)
- [ ] Shows controller IP (127.0.0.1:6633)
- [ ] Match fields visible in flow rules

---

## Submission Requirements

When submitting PCAPs for grading:

1. **Include your session token** in the filename:
   ```
   week06_nat_capture_W6-ABC123-20260124.pcap
   ```

2. **Verify integrity** before submission:
   ```bash
   capinfos your_capture.pcap
   ```

3. **Minimum packet count**: 20 packets per capture

4. **Privacy check**: Ensure no sensitive data (passwords, etc.)

---

## Troubleshooting

### "Permission denied" when capturing

```bash
# Run tcpdump with sudo inside Mininet node:
sudo h1 tcpdump -i h1-eth0 -w /tmp/capture.pcap
```

### "No packets captured"

1. Verify correct interface name: `ip link show`
2. Check filter is not too restrictive
3. Ensure traffic is being generated during capture

### PCAP file is empty

1. Wait for traffic before stopping capture
2. Use `-c N` to capture N packets then auto-stop
3. Check tcpdump process is still running: `ps aux | grep tcpdump`

---

## Further Reading

- Wireshark User Guide: https://www.wireshark.org/docs/
- tcpdump manual: `man tcpdump`
- OpenFlow dissector: Built into Wireshark 2.0+

---

*Week 6 PCAP Documentation — Computer Networks*
*Contact: Issues: Open an issue in GitHub*
