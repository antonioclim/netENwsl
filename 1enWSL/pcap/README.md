# Packet Capture Storage

> NETWORKING class - ASE, Informatics | by Revolvix

This directory stores packet capture files generated during laboratory exercises.

## Contents

- **Exercise captures** - Traffic recorded during hands-on exercises
- **Demo captures** - Pre-recorded demonstrations
- **Analysis files** - Exported data for programmatic processing

## File Naming Convention

Use descriptive names following this pattern:

```
week<N>_<exercise>_<description>.pcap
```

Examples:
- `week1_ex3_tcp_handshake.pcap`
- `week1_demo_ping_latency.pcap`
- `week1_analysis_http_requests.pcap`

## Generating Captures

### From Container

```bash
# Using the capture script
python scripts/capture_traffic.py --output pcap/my_capture.pcap

# Direct tcpdump
docker exec week1_lab tcpdump -i eth0 -w /work/pcap/capture.pcap
```

### From Windows (Wireshark)

1. Open Wireshark
2. Select appropriate interface
3. Start capture
4. Save to this directory

## Analysing Captures

### Wireshark (GUI)

Double-click any `.pcap` file to open in Wireshark.

### tshark (CLI)

```bash
# Summary
tshark -r capture.pcap -q -z conv,tcp

# Export to CSV
tshark -r capture.pcap -T fields -e frame.number -e ip.src -e ip.dst > data.csv
```

### Python

```python
import dpkt

with open('capture.pcap', 'rb') as f:
    pcap = dpkt.pcap.Reader(f)
    for timestamp, buf in pcap:
        # Process packets
        pass
```

## Storage Notes

- PCAP files can grow large; archive or delete after analysis
- This directory is excluded from version control (via .gitignore)
- Clean before next week: `python scripts/cleanup.py --full`

---

*NETWORKING class - ASE, Informatics | by Revolvix*
