# Packet Captures — Week 8

> NETWORKING class - ASE, Informatics | by Revolvix

## Purpose

This directory stores packet capture files (.pcap) generated during laboratory exercises.

## Capturing Traffic

### Using the Helper Script

```powershell
python scripts/capture_traffic.py --interface eth0 --output pcap/week8_capture.pcap
```

### Using tcpdump Directly

```bash
# Capture HTTP traffic
sudo tcpdump -i any port 8080 -w pcap/http_traffic.pcap

# Capture with packet limit
sudo tcpdump -i any port 8080 -c 100 -w pcap/sample.pcap
```

### Using Wireshark

1. Open Wireshark
2. Select the appropriate interface (usually `Loopback` for localhost traffic)
3. Apply capture filter: `port 8080`
4. Start capture
5. Generate traffic with curl or browser
6. Save as `.pcap` file in this directory

## Suggested Captures

| Filename | Description |
|----------|-------------|
| `tcp_handshake.pcap` | TCP three-way handshake |
| `http_request.pcap` | Complete HTTP request/response |
| `load_balancing.pcap` | Multiple requests showing distribution |
| `tls_handshake.pcap` | TLS negotiation (HTTPS) |

## Analysing Captures

Open captures in Wireshark:

```powershell
& "C:\Program Files\Wireshark\Wireshark.exe" pcap\http_traffic.pcap
```

## Cleanup

Captures are removed during full cleanup:

```powershell
python scripts/cleanup.py --full
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
