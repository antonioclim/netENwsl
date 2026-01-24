# Packet Captures — Week 4

> NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

This directory contains packet capture files for protocol analysis exercises.

---

## Pre-captured Samples

| File | LO | Description | Filter |
|------|-----|-------------|--------|
| `week04_lo3_text_proto.pcap` | LO3 | TEXT protocol session: PING, SET, GET, COUNT, QUIT | `tcp.port == 5400` |
| `week04_lo4_binary_proto.pcap` | LO4 | BINARY protocol with valid and corrupted CRC packets | `tcp.port == 5401` |
| `week04_lo5_udp_sensor.pcap` | LO5 | UDP sensor datagrams from multiple sensors | `udp.port == 5402` |

---

## Creating Your Own Captures

### Using tcpdump (Recommended)

```bash
# Capture TEXT protocol traffic
sudo tcpdump -i lo -w pcap/my_text_capture.pcap port 5400

# Capture BINARY protocol traffic
sudo tcpdump -i lo -w pcap/my_binary_capture.pcap port 5401

# Capture UDP sensor traffic
sudo tcpdump -i lo -w pcap/my_udp_capture.pcap port 5402
```

### Using the Capture Script

```bash
# Start lab environment first
python scripts/start_lab.py

# In a separate terminal, start capture
python scripts/capture_traffic.py --port 5400 --output pcap/my_capture.pcap

# Run client commands to generate traffic
python src/apps/text_proto_client.py -c "PING" -c "SET key1 value1"

# Stop capture with Ctrl+C
```

### Using Wireshark

1. Open Wireshark (from Windows)
2. Select the **Loopback** or **\\Device\\NPF_Loopback** interface
3. Apply filter: `tcp.port == 5400` or `tcp.port == 5401`
4. Start capture
5. Run client commands
6. Stop capture and save as `.pcap`

---

## Analysis Tips

### TEXT Protocol (Port 5400)

Look for the length prefix at the start of each message:
```
Frame: 31 31 20 53 45 54 20 6e 61 6d 65
       ^^ ^^  = "11" (length prefix in ASCII)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^ = " SET name" (payload)
```

### BINARY Protocol (Port 5401)

Identify the 14-byte header structure:
```
4e 50  01  01  00 05  00 00 00 2a  xx xx xx xx  [payload]
^^^^^ ^^  ^^  ^^^^^  ^^^^^^^^^^   ^^^^^^^^^^^
Magic V   T   Len    Seq          CRC32
```

### UDP Sensor (Port 5402)

Each datagram is exactly 23 bytes:
```
01  00 00 03 e9  41 b0 00 00  54 65 73 74 4c 61 62 20 20 20  xx xx xx xx
^^  ^^^^^^^^^^^  ^^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^^
V   Sensor ID    Temperature  Location (10 bytes padded)    CRC32
```

---

## Useful Wireshark Filters

```
# Show only TEXT protocol
tcp.port == 5400

# Show only BINARY protocol
tcp.port == 5401

# Show only UDP sensor
udp.port == 5402

# Show packets with specific content
frame contains "SET"

# Show only TCP retransmissions
tcp.analysis.retransmission

# Show TCP connection establishment
tcp.flags.syn == 1
```

---

## Exercise: Protocol Overhead Analysis

1. Capture TEXT and BINARY protocol sessions with the same commands
2. Compare total bytes transmitted for equivalent operations
3. Calculate overhead ratio: `(TEXT bytes - BINARY bytes) / TEXT bytes × 100`
4. Document your findings in the Exercise 4 report

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
