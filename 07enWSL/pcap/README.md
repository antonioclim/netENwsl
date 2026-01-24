# 📦 Packet Capture Directory — Week 7
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> This directory stores packet capture files generated during laboratory exercises.

---

## Directory Structure

```
pcap/
├── README.md           # This file
├── samples/            # Pre-generated reference captures
│   ├── README.md       # Sample descriptions and generation instructions
│   └── *.pcap          # Reference capture files
└── *.pcap              # Your captured files (gitignored)
```

---

## Naming Convention

**All PCAP files MUST follow this naming pattern:**

```
week{NN}_lo{X}_{protocol}_{scenario}.pcap
```

| Component | Format | Example | Description |
|-----------|--------|---------|-------------|
| `week` | `NN` | `07` | Week number (zero-padded) |
| `lo` | `X` | `1`, `2`, `3` | Learning Objective number |
| `protocol` | text | `tcp`, `udp`, `mixed` | Primary protocol captured |
| `scenario` | snake_case | `baseline`, `blocked_reject` | Descriptive name |

### Valid Examples

| Filename | LO | Description |
|----------|-----|-------------|
| `week07_lo1_tcp_handshake.pcap` | LO1 | TCP three-way handshake |
| `week07_lo1_udp_baseline.pcap` | LO1 | Baseline UDP traffic |
| `week07_lo2_tcp_blocked_reject.pcap` | LO2 | TCP blocked with REJECT |
| `week07_lo2_tcp_blocked_drop.pcap` | LO2 | TCP blocked with DROP |
| `week07_lo3_udp_dropped.pcap` | LO3 | UDP packets dropped |
| `week07_lo4_timeout_analysis.pcap` | LO4 | Connection timeout |
| `week07_lo6_drop_vs_reject.pcap` | LO6 | Comparison capture |

### Invalid Examples

| Filename | Problem |
|----------|---------|
| `capture.pcap` | Missing week, LO, protocol |
| `tcp_test.pcap` | Missing week and LO |
| `week7_tcp.pcap` | Missing LO, week not zero-padded |
| `Week07_LO1_TCP.pcap` | Wrong case (use lowercase) |

---

## Creating Captures

### Using Lab Script

```bash
# Basic capture (60 seconds, all traffic)
python3 scripts/capture_traffic.py \
    --output pcap/week07_lo1_tcp_handshake.pcap \
    --duration 60

# Filtered capture (TCP only)
python3 scripts/capture_traffic.py \
    --output pcap/week07_lo2_tcp_blocked_reject.pcap \
    --filter "tcp port 9090" \
    --duration 30
```

### Using tcpdump Directly

```bash
# Capture to file
sudo tcpdump -i any -w pcap/week07_lo1_tcp_handshake.pcap \
    -c 100 port 9090 or port 9091

# Capture with timestamp precision
sudo tcpdump -i any -w pcap/week07_lo4_timeout_analysis.pcap \
    --time-stamp-precision=micro port 9090
```

### Using Makefile Shortcuts

```bash
make capture          # General capture
make capture-tcp      # TCP only
make capture-udp      # UDP only
```

---

## Analysing Captures

### Open in Wireshark (Windows)

1. Navigate to `\\wsl$\Ubuntu\path\to\week7\pcap\`
2. Double-click the `.pcap` file
3. Apply display filters as needed

### Quick Analysis with tshark

```bash
# Packet summary
tshark -r pcap/week07_lo1_tcp_handshake.pcap

# Protocol hierarchy
tshark -r pcap/week07_lo1_tcp_handshake.pcap -q -z io,phs

# TCP conversations
tshark -r pcap/week07_lo1_tcp_handshake.pcap -q -z conv,tcp

# Extract specific fields
tshark -r pcap/week07_lo2_tcp_blocked_reject.pcap \
    -T fields -e frame.number -e ip.src -e ip.dst -e tcp.flags
```

### Verify Capture Contents

```bash
# Check packet count
capinfos pcap/week07_lo1_tcp_handshake.pcap

# First 10 packets summary
tshark -r pcap/week07_lo1_tcp_handshake.pcap -c 10
```

---

## Suggested Wireshark Filters

| Purpose | Filter |
|---------|--------|
| TCP handshake | `tcp.flags.syn == 1` |
| SYN only (no SYN-ACK) | `tcp.flags.syn == 1 && tcp.flags.ack == 0` |
| TCP RST packets | `tcp.flags.reset == 1` |
| Failed connections | `tcp.analysis.retransmission` |
| Specific port | `tcp.port == 9090` |
| ICMP errors | `icmp.type == 3` |
| UDP traffic | `udp.port == 9091` |

---

## Reference Samples

Pre-generated samples are available in `pcap/samples/`:

| File | Purpose | LO |
|------|---------|-----|
| `week07_lo1_tcp_handshake.pcap` | Complete TCP lifecycle | LO1 |
| `week07_lo1_udp_baseline.pcap` | UDP datagram exchange | LO1 |
| `week07_lo2_tcp_blocked_reject.pcap` | REJECT action evidence | LO2 |
| `week07_lo2_tcp_blocked_drop.pcap` | DROP action evidence | LO2 |
| `week07_lo6_drop_vs_reject.pcap` | Side-by-side comparison | LO6 |

See `pcap/samples/README.md` for detailed descriptions and regeneration instructions.

---

## Git Configuration

The `.gitignore` excludes student-generated captures:

```gitignore
# Exclude student captures
pcap/*.pcap

# Keep samples
!pcap/samples/*.pcap
```

This ensures your captures don't accidentally get committed while preserving reference samples.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Permission denied | Run tcpdump with `sudo` |
| No packets captured | Check interface (`-i any` or `-i eth0`) |
| File too large | Use `-c` to limit packet count |
| Can't open in Wireshark | Check file path, ensure `.pcap` extension |
| Wrong traffic captured | Verify BPF filter syntax |

---

*Computer Networks — Week 7: Packet Interception, Filtering and Defensive Port Probing*  
*ASE Bucharest, CSIE | by ing. dr. Antonio Clim*
