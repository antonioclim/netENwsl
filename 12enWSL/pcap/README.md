# Packet Capture Directory

> NETWORKING class - ASE, Informatics | by Revolvix

## Purpose

This directory stores packet captures (`.pcap`, `.pcapng`) generated during laboratory exercises and demonstrations.

## Suggested Naming Convention

```
week12_<protocol>_<description>_<timestamp>.pcap
```

**Examples:**
- `week12_smtp_dialogue_20240115_1430.pcap`
- `week12_jsonrpc_batch_20240115_1445.pcap`
- `week12_grpc_calculator_20240115_1500.pcap`
- `week12_all_protocols_benchmark_20240115_1515.pcap`

## Capturing Traffic

### Using the Helper Script

```powershell
# Capture all Week 12 traffic for 60 seconds
python scripts/capture_traffic.py --duration 60 --output pcap/week12_session.pcap

# Capture specific protocol
python scripts/capture_traffic.py --filter "port 1025" --output pcap/smtp_only.pcap
python scripts/capture_traffic.py --filter "port 6200 or port 6201" --output pcap/rpc_http.pcap
python scripts/capture_traffic.py --filter "port 6251" --output pcap/grpc_only.pcap
```

### Using Wireshark Directly

1. Open Wireshark on Windows
2. Select the appropriate interface:
   - For Docker traffic: `\Device\NPF_Loopback` or `Adapter for loopback traffic capture`
   - For WSL2: May require `vEthernet (WSL)` adapter
3. Apply capture filter: `port 1025 or port 6200 or port 6201 or port 6251`
4. Save captures to this directory

### Using tcpdump (Inside Container)

```bash
# Enter the lab container
docker exec -it week12_lab bash

# Capture SMTP traffic
tcpdump -i any -w /app/pcap/smtp_capture.pcap port 1025

# Capture all RPC traffic
tcpdump -i any -w /app/pcap/rpc_capture.pcap port 6200 or port 6201 or port 6251
```

## Useful Wireshark Display Filters

### SMTP Analysis
```
smtp                           # All SMTP traffic
smtp.req.command == "MAIL"     # MAIL FROM commands
smtp.response.code == 250      # Successful responses
tcp.port == 1025               # Week 12 SMTP port
```

### JSON-RPC/XML-RPC Analysis (HTTP-based)
```
http.request.method == "POST"  # All POST requests
tcp.port == 6200               # JSON-RPC server
tcp.port == 6201               # XML-RPC server
http contains "jsonrpc"        # JSON-RPC requests
http contains "methodCall"     # XML-RPC requests
```

### gRPC Analysis (HTTP/2)
```
http2                          # All HTTP/2 traffic
tcp.port == 6251               # gRPC server
http2.header.name == ":path"   # gRPC method paths
```

### General Analysis
```
tcp.analysis.retransmission    # Retransmitted packets
tcp.analysis.duplicate_ack     # Duplicate ACKs
tcp.flags.syn == 1             # Connection establishments
```

## File Management

- Captures are **not** version-controlled (listed in `.gitignore`)
- Clean up old captures before submitting homework
- Large captures can be compressed: `gzip week12_capture.pcap`

## Analysis Tips

1. **Follow TCP Stream:** Right-click a packet → Follow → TCP Stream
2. **Protocol Statistics:** Statistics → Protocol Hierarchy
3. **IO Graphs:** Statistics → I/O Graphs (compare protocols)
4. **Expert Info:** Analyze → Expert Information (find issues)

---

*NETWORKING class - ASE, Informatics | by Revolvix*
