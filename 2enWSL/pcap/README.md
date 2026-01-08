# Packet Capture Storage

> NETWORKING class - ASE, Informatics | by Revolvix

This directory stores packet captures (`.pcap` files) generated during laboratory exercises.

## Naming Convention

```
week2_<exercise>_<description>_<timestamp>.pcap
```

**Examples:**
- `week2_tcp_handshake_20250106_143022.pcap`
- `week2_udp_protocol_20250106_144515.pcap`
- `week2_concurrent_clients_20250106_150030.pcap`

## Recommended Captures

### Exercise 1: TCP Server
```powershell
python scripts/capture_traffic.py --filter "tcp port 9090" --output pcap/week2_tcp_server.pcap
```

### Exercise 2: UDP Protocol
```powershell
python scripts/capture_traffic.py --filter "udp port 9091" --output pcap/week2_udp_protocol.pcap
```

## Opening Captures in Wireshark

1. Launch Wireshark on Windows
2. File → Open → Navigate to this directory
3. Select the `.pcap` file

## Useful Wireshark Filters

| Filter | Description |
|--------|-------------|
| `tcp.port == 9090` | TCP server traffic |
| `udp.port == 9091` | UDP server traffic |
| `tcp.flags.syn == 1` | TCP SYN packets (connection initiation) |
| `tcp.flags.fin == 1` | TCP FIN packets (connection termination) |
| `tcp.analysis.retransmission` | Retransmitted packets |

## Cleanup

Packet captures can be large. Remove old captures with:

```powershell
python scripts/cleanup.py --full
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
