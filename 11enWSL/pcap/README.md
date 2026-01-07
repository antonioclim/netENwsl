# Packet Captures Directory

> NETWORKING class - ASE, Informatics | by Revolvix

This directory stores packet captures (`.pcap` files) generated during laboratory exercises.

## Capturing Traffic

### Using the Capture Script

```powershell
# Capture HTTP traffic on port 8080 for 60 seconds
python scripts/capture_traffic.py --interface eth0 --filter "tcp port 8080" --duration 60

# Capture all traffic with no time limit (Ctrl+C to stop)
python scripts/capture_traffic.py --interface any --output pcap/week11_full.pcap
```

### Using Wireshark Directly

1. Open Wireshark
2. Select the appropriate interface:
   - On Windows: `Ethernet` or `Wi-Fi`
   - For Docker traffic: `\\.\pipe\docker_engine` or the Docker bridge interface
3. Apply capture filter: `tcp port 8080`
4. Start capture
5. Perform exercises
6. Stop and save as `week11_<exercise>.pcap`

### Using tshark (Command Line)

```bash
# Basic capture
tshark -i eth0 -w pcap/week11_capture.pcap

# With display filter
tshark -i eth0 -f "tcp port 8080" -w pcap/week11_lb.pcap

# With duration limit
tshark -i eth0 -a duration:60 -w pcap/week11_60s.pcap
```

## Analysing Captures

### Wireshark GUI

1. Open Wireshark
2. File → Open → Select `.pcap` file
3. Apply display filters (see below)

### tshark (Command Line)

```bash
# Show HTTP traffic
tshark -r pcap/week11_capture.pcap -Y http

# Show DNS queries
tshark -r pcap/week11_capture.pcap -Y dns

# Show TCP conversations
tshark -r pcap/week11_capture.pcap -q -z conv,tcp

# Export to text
tshark -r pcap/week11_capture.pcap -V > pcap/analysis.txt
```

## Recommended Display Filters for Week 11

### Load Balancer Traffic

```
# All HTTP traffic through load balancer
tcp.port == 8080 && http

# HTTP requests only
http.request

# HTTP responses only
http.response

# Requests to specific backend
tcp.dstport == 8081

# Track specific client
ip.src == 172.28.0.1
```

### DNS Traffic

```
# All DNS
dns

# DNS queries only
dns.flags.response == 0

# DNS responses only
dns.flags.response == 1

# Queries for specific domain
dns.qry.name contains "google"

# A record queries
dns.qry.type == 1
```

### SSH Traffic

```
# All SSH
tcp.port == 22

# SSH key exchange
ssh.protocol

# Encrypted traffic (after handshake)
tcp.port == 22 && tcp.len > 0
```

### FTP Traffic

```
# FTP control channel
ftp

# FTP data channel
ftp-data

# FTP commands
ftp.request.command

# FTP responses
ftp.response.code
```

## File Naming Convention

Use the following naming pattern for captures:

```
week11_<exercise>_<timestamp>.pcap
```

Examples:
- `week11_loadbalancer_20250106_1430.pcap`
- `week11_dns_queries_20250106_1445.pcap`
- `week11_failover_test_20250106_1500.pcap`

## Storage Notes

- Packet captures can grow large quickly
- The `scripts/cleanup.py --full` command removes all `.pcap` files
- Consider using capture filters to limit file size
- Default maximum capture size: 100MB

---

*NETWORKING class - ASE, Informatics | by Revolvix*
