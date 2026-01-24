# Packet Capture Storage

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by Revolvix

This directory stores packet capture files (`.pcap`) generated during laboratory exercises.

---

## Directory Purpose

Store Wireshark/tcpdump captures for:
- Exercise verification and debugging
- Protocol analysis assignments
- Homework submissions requiring traffic samples
- Reference captures for comparison

---

## Naming Convention

Use descriptive names following this pattern:

```
week3_<exercise>_<description>_<timestamp>.pcap
```

**Examples:**
- `week3_ex01_broadcast_20240215_1030.pcap`
- `week3_ex02_multicast_join_20240215_1045.pcap`
- `week3_ex03_tunnel_session_20240215_1100.pcap`
- `week3_analysis_full_session_20240215.pcap`

---

## Creating Captures

### Method 1: Capture Script (Recommended)

```powershell
# From project root
python scripts/capture_traffic.py --container server --duration 30 --output pcap/my_capture.pcap
```

### Method 2: tcpdump in Container

```bash
# Start capture
docker exec week3_server tcpdump -i eth0 -w /tmp/capture.pcap

# Stop with Ctrl+C, then copy out
docker cp week3_server:/tmp/capture.pcap ./pcap/
```

### Method 3: Wireshark on Windows

1. Open Wireshark as Administrator
2. Select WSL/Docker interface
3. Apply capture filter if needed
4. File → Save As → `pcap/filename.pcap`

---

## Recommended Capture Filters

Apply these filters during capture to reduce file size:

### Exercise 1: Broadcast

```
udp port 5007
```

### Exercise 2: Multicast

```
udp port 5008 or igmp
```

### Exercise 3: Tunnel

```
tcp port 8080 or tcp port 9090
```

### Full Session

```
host 172.20.0.10 or host 172.20.0.100 or host 172.20.0.101 or host 172.20.0.254
```

---

## File Size Guidelines

- **Exercise captures:** 100KB - 1MB typical
- **Full session:** 1MB - 10MB typical
- **Maximum recommended:** 50MB

Large captures may be truncated or sampled for analysis.

---

## Cleaning Up

Capture files are cleaned automatically by:

```powershell
python scripts/cleanup.py --full
```

Or manually:

```powershell
# Remove all captures
Remove-Item pcap/*.pcap

# Keep .gitkeep
```

---

## Submitting Captures

For homework requiring packet captures:

1. Name file according to homework instructions
2. Verify file opens correctly in Wireshark
3. Include relevant display filters in submission
4. Note any interesting observations

---

## Troubleshooting Captures

### Empty Capture File

- Check you're capturing on the correct interface
- Verify containers are running and generating traffic
- Try capturing without filters first

### Missing Packets

- Increase capture buffer: `-B 10` in tcpdump
- Disable promiscuous mode if not needed
- Check for packet drops in tcpdump output

### Permission Denied

- Run Wireshark as Administrator on Windows
- Check Docker socket permissions on WSL

---

*NETWORKING class - ASE, Informatics | by Revolvix*
