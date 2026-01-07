# Packet Captures: Week 9

> Storage directory for Wireshark/tcpdump captures
> NETWORKING class - ASE, Informatics | by Revolvix

---

## Purpose

This directory stores packet capture files generated during the laboratory session.

## Naming Convention

Use descriptive names with timestamps:

```
week9_<topic>_<timestamp>.pcap
```

Examples:
- `week9_ftp_session_20260107_1430.pcap`
- `week9_passive_transfer_20260107_1445.pcap`
- `week9_authentication_flow_20260107_1500.pcap`

## Capturing Traffic

### Method 1: Using the helper script

```powershell
python scripts/capture_traffic.py --interface eth0 --output pcap/week9_capture.pcap
```

### Method 2: Using tcpdump inside container

```bash
# Start capture
docker exec s9_ftp-server tcpdump -i eth0 -w /tmp/capture.pcap

# Copy to host
docker cp s9_ftp-server:/tmp/capture.pcap ./pcap/
```

### Method 3: Using Wireshark

1. Open Wireshark
2. Select interface (e.g., `\\.\pipe\docker_engine` on Windows)
3. Apply capture filter: `port 2121 or port 20`
4. Save to this directory

## Analysis Tips

### Useful Wireshark Display Filters

```
# FTP control traffic
ftp

# FTP commands only
ftp.request

# FTP responses only
ftp.response

# Specific FTP commands
ftp.request.command == "USER"
ftp.request.command == "PASS"
ftp.request.command == "RETR"

# FTP data transfers
ftp-data

# Authentication sequence
ftp.response.code == 331 || ftp.response.code == 230 || ftp.response.code == 530
```

### Export Options

- **Follow TCP Stream**: Right-click > Follow > TCP Stream
- **Export Objects**: File > Export Objects > FTP-DATA

## Cleanup

Capture files can be large. Delete old captures before next week:

```powershell
python scripts/cleanup.py --full
```

Or manually:

```powershell
del pcap\*.pcap
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
