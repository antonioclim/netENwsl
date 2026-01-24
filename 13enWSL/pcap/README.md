# Packet Captures Directory

> Week 13: IoT and Security in Computer Networks  
> NETWORKING class - ASE, Informatics | by Revolvix

---

## Purpose

This directory stores packet capture (pcap) files generated during laboratory exercises. These files can be analysed using Wireshark or other packet analysis tools.

---

## Generating Captures

### Using the Capture Script

```powershell
# Default capture (all lab ports)
python scripts/capture_traffic.py --output pcap/lab_capture.pcap

# With duration limit
python scripts/capture_traffic.py --output pcap/capture.pcap --duration 60

# Custom BPF filter
python scripts/capture_traffic.py --output pcap/mqtt_only.pcap --filter "tcp port 1883"
```

### Using tcpdump Directly

```bash
# Capture MQTT traffic
tcpdump -i any port 1883 or port 8883 -w pcap/mqtt_traffic.pcap

# Capture all lab traffic
tcpdump -i any "tcp port 1883 or tcp port 8883 or tcp port 8080 or tcp port 2121 or tcp port 6200" -w pcap/all_traffic.pcap
```

### Using Wireshark

1. Open Wireshark
2. Select appropriate interface (Docker or loopback)
3. Apply capture filter: `tcp port 1883 or tcp port 8080`
4. Save capture to this directory

---

## Suggested Capture Files

| Filename | Description | Exercise |
|----------|-------------|----------|
| `mqtt_plaintext.pcap` | Unencrypted MQTT traffic | Exercise 2 |
| `mqtt_tls.pcap` | TLS-encrypted MQTT traffic | Exercise 2 |
| `port_scan.pcap` | Port scanning activity | Exercise 1 |
| `dvwa_http.pcap` | DVWA web traffic | Exercise 4 |
| `ftp_session.pcap` | FTP connection attempts | Exercise 4 |

---

## Analysis Tips

### Opening in Wireshark

```powershell
# Windows
& "C:\Program Files\Wireshark\Wireshark.exe" pcap\mqtt_plaintext.pcap

# Or right-click the .pcap file and "Open with Wireshark"
```

### Useful Display Filters

```
# MQTT messages
mqtt

# TLS handshakes
tls.handshake

# HTTP requests
http.request

# FTP commands
ftp.request
```

### Command-line Analysis with tshark

```bash
# Count packets by protocol
tshark -r pcap/capture.pcap -q -z io,phs

# Extract MQTT topics
tshark -r pcap/mqtt_plaintext.pcap -Y mqtt -T fields -e mqtt.topic

# Show HTTP requests
tshark -r pcap/dvwa_http.pcap -Y "http.request" -T fields -e http.request.method -e http.request.uri
```

---

## File Naming Convention

Use descriptive names following this pattern:

```
<protocol>_<description>_<timestamp>.pcap
```

Examples:
- `mqtt_sensor_data_20260107.pcap`
- `tls_handshake_analysis_20260107.pcap`
- `full_lab_session_week13.pcap`

---

## Cleanup

Capture files can grow large. Remove old captures before starting new exercises:

```powershell
# Using cleanup script
python scripts/cleanup.py --artifacts-only

# Manual removal
Remove-Item pcap/*.pcap
```

---

## Privacy Notice

Packet captures may contain sensitive information. Do not share capture files publicly without reviewing and sanitising their contents.

---

*NETWORKING class - ASE, Informatics | by Revolvix*
