# Packet Capture Directory

> NETWORKING class - ASE, Informatics | by Revolvix

This directory stores packet capture files generated during laboratory exercises.

## Naming Convention

Use the following naming pattern for captures:

```
week7_<exercise>_<description>.pcap
```

Examples:
- `week7_ex1_baseline.pcap` - Baseline capture from Exercise 1
- `week7_ex2_tcp_reject.pcap` - TCP rejection capture
- `week7_ex3_udp_drop.pcap` - UDP drop capture
- `week7_demo_full.pcap` - Full demonstration capture

## Capture Commands

### Using the capture script:

```bash
python scripts/capture_traffic.py --interface eth0 --output pcap/week7_capture.pcap --duration 60
```

### Using tcpdump directly:

```bash
# Capture all traffic on port 9090
tcpdump -i eth0 port 9090 -w pcap/tcp_traffic.pcap

# Capture with packet details
tcpdump -i eth0 -vvv port 9090 -w pcap/detailed.pcap
```

### Using tshark:

```bash
# Capture with display filter
tshark -i eth0 -f "port 9090 or port 9091" -w pcap/combined.pcap
```

## Analysis Tips

When opening captures in Wireshark:

1. **For TCP analysis:**
   - Filter: `tcp.port == 9090`
   - Look for SYN, SYN-ACK, RST packets
   - Check for retransmissions

2. **For UDP analysis:**
   - Filter: `udp.port == 9091`
   - Note absence of response (DROP vs REJECT)

3. **For filtering analysis:**
   - Compare timestamps before and after filter application
   - Look for ICMP destination unreachable messages

## Cleaning Up

Capture files can grow large. To clean:

```bash
# Remove all captures
rm pcap/*.pcap

# Or use cleanup script
python scripts/cleanup.py --full
```

## Submission

For homework assignments, include your captures in the submission:
- `hw_scenario_1.pcap` - TCP REJECT scenario
- `hw_scenario_2.pcap` - UDP DROP scenario
- `hw_scenario_3.pcap` - Application-layer filtering

---

*NETWORKING class - ASE, Informatics | by Revolvix*
