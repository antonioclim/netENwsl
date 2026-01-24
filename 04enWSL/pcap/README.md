# Packet Captures Directory

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by Revolvix

---

## Purpose

This directory stores packet capture files (.pcap) generated during laboratory exercises. These captures can be analysed using Wireshark or command-line tools like `tshark` and `tcpdump`.

---

## Naming Convention

Please use the following naming convention for your captures:

```
week4_<exercise>_<description>_<timestamp>.pcap
```

**Examples:**
- `week4_ex1_text_proto_20250106_1430.pcap`
- `week4_ex2_binary_crc_test_20250106_1512.pcap`
- `week4_demo_udp_sensor_20250106_1600.pcap`

---

## Capturing Traffic

### Using the Capture Script

```powershell
# Capture all traffic on default interface
python scripts/capture_traffic.py --output pcap/my_capture.pcap

# Capture specific port
python scripts/capture_traffic.py --port 5400 --output pcap/text_proto.pcap

# Capture with duration limit
python scripts/capture_traffic.py --duration 60 --output pcap/timed_capture.pcap
```

### Using Wireshark Directly

1. Open Wireshark
2. Select the appropriate interface:
   - For Docker: `\\.\pipe\docker_engine` or `vEthernet (WSL)`
   - For local traffic: `Loopback` or `Adapter for loopback traffic capture`
3. Start capture
4. Perform laboratory exercises
5. Stop capture and save to this directory

### Using tcpdump (inside WSL or container)

```bash
# Capture all traffic
sudo tcpdump -i any -w pcap/capture.pcap

# Capture specific ports
sudo tcpdump -i any port 5400 or port 5401 or port 5402 -w pcap/protocols.pcap

# Capture with packet count limit
sudo tcpdump -i any -c 1000 -w pcap/sample.pcap
```

---

## Analysis Tips

### Wireshark Filters for Week 4

**TEXT Protocol (TCP port 5400):**
```
tcp.port == 5400
```

**BINARY Protocol (TCP port 5401):**
```
tcp.port == 5401
```

**UDP Sensor Protocol (port 5402):**
```
udp.port == 5402
```

**Follow TCP Stream:**
- Right-click on a TCP packet → Follow → TCP Stream

**Filter by Payload Content:**
```
tcp contains "PING"
tcp contains "SET"
```

### Useful tshark Commands

```bash
# Display summary of capture
tshark -r capture.pcap -q -z io,stat,1

# Show TCP conversations
tshark -r capture.pcap -q -z conv,tcp

# Extract payload data
tshark -r capture.pcap -T fields -e data

# Filter and display specific packets
tshark -r capture.pcap -Y "tcp.port == 5400" -V
```

---

## Storage Guidelines

- **Temporary captures:** Delete after analysis
- **Exercise captures:** Keep until end of semester
- **Reference captures:** Store in personal backup

**Note:** This directory is cleaned during full cleanup operations. Back up important captures before running `python scripts/cleanup.py --full`.

---

## Sample Captures (Reference)

The following reference captures demonstrate expected behaviour:

| File | Description | Exercise |
|------|-------------|----------|
| `sample_text_proto.pcap` | TEXT protocol PING/SET/GET | Exercise 1 |
| `sample_binary_proto.pcap` | BINARY protocol with CRC | Exercise 2 |
| `sample_udp_sensor.pcap` | UDP sensor datagrams | Exercise 3 |
| `sample_crc_error.pcap` | Corrupted packet detection | Exercise 4 |

*Note: Sample captures may be provided separately by your instructor.*

---

*NETWORKING class - ASE, Informatics | by Revolvix*
