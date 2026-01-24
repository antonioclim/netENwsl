# PCAP Capture Directory — Week 2

> NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim

## Purpose

This directory stores network packet captures (PCAP files) generated during laboratory exercises. These captures are essential for:

- Verifying TCP three-way handshake
- Analysing UDP datagram exchange
- Understanding protocol encapsulation
- Debugging network issues

## Naming Convention

Use the following format for captured files:

```
week02_<exercise>_<protocol>_<scenario>.pcap
```

**Examples:**

| Filename | Description |
|----------|-------------|
| `week02_ex1_tcp_handshake.pcap` | TCP three-way handshake capture |
| `week02_ex1_tcp_echo.pcap` | TCP echo server conversation |
| `week02_ex2_udp_ping.pcap` | UDP ping-pong exchange |
| `week02_ex3_combined.pcap` | Mixed TCP and UDP traffic |

## Capture Procedures

### Method 1: Wireshark (Windows)

1. Open Wireshark
2. Select interface: **vEthernet (WSL)** for WSL traffic
3. Apply capture filter: `port 9090 or port 9091`
4. Start capture
5. Run exercise
6. Stop capture
7. Save as: `pcap/week02_<description>.pcap`

### Method 2: tcpdump (Linux/WSL)

```bash
# Capture TCP traffic on port 9090
sudo tcpdump -i eth0 port 9090 -w pcap/week02_ex1_tcp.pcap

# Capture UDP traffic on port 9091
sudo tcpdump -i eth0 udp port 9091 -w pcap/week02_ex2_udp.pcap

# Capture both with verbose output
sudo tcpdump -i eth0 'port 9090 or port 9091' -v -w pcap/week02_combined.pcap
```

### Method 3: Python Script

```bash
# Using the provided capture script
python scripts/capture_traffic.py \
    --interface eth0 \
    --port 9090 \
    --output pcap/week02_ex1_tcp.pcap \
    --duration 30
```

## Expected Captures for Week 2

| Exercise | Expected Traffic | Key Observations |
|----------|------------------|------------------|
| Exercise 1 (TCP) | SYN → SYN-ACK → ACK → DATA → FIN | Three-way handshake, PSH flags |
| Exercise 2 (UDP) | Request → Response datagrams | No handshake, immediate data |
| Exercise 3 | Mixed TCP and UDP | Compare packet sizes and flags |

## Analysis Tips

### TCP Handshake Verification

In Wireshark, filter for the handshake:
```
tcp.flags.syn == 1
```

You should see:
1. Client → Server: SYN (Seq=0)
2. Server → Client: SYN-ACK (Seq=0, Ack=1)
3. Client → Server: ACK (Seq=1, Ack=1)

### Following a Conversation

1. Right-click any packet in the conversation
2. Select **Follow → TCP Stream** (or UDP Stream)
3. View the complete application-layer exchange

### Useful Display Filters

| Filter | Purpose |
|--------|---------|
| `tcp.port == 9090` | TCP server traffic |
| `udp.port == 9091` | UDP server traffic |
| `tcp.flags.syn == 1 && tcp.flags.ack == 0` | Initial SYN only |
| `tcp.flags.fin == 1` | Connection termination |
| `ip.addr == 10.0.2.10` | Container traffic |
| `tcp.analysis.retransmission` | Retransmitted packets |

## Sample Captures (Reference)

The following reference captures demonstrate expected behaviour:

### Sample 1: TCP Echo (Not included — generate yourself)

**How to generate:**
```bash
# Terminal 1: Start server
python src/exercises/ex_2_01_tcp.py server --port 9090

# Terminal 2: Start Wireshark/tcpdump

# Terminal 3: Run client
python src/exercises/ex_2_01_tcp.py client --host 127.0.0.1 --port 9090 -m "Hello World"
```

**Expected packet sequence:**
```
1. [SYN]       Client → Server   Seq=0
2. [SYN,ACK]   Server → Client   Seq=0, Ack=1
3. [ACK]       Client → Server   Seq=1, Ack=1
4. [PSH,ACK]   Client → Server   "Hello World" (11 bytes)
5. [ACK]       Server → Client   Ack=12
6. [PSH,ACK]   Server → Client   "OK: HELLO WORLD" (15 bytes)
7. [ACK]       Client → Server   Ack=16
8. [FIN,ACK]   Client → Server   Connection close
9. [FIN,ACK]   Server → Client   Connection close
10.[ACK]       Client → Server   Final ack
```

### Sample 2: UDP Ping (Not included — generate yourself)

**How to generate:**
```bash
# Terminal 1: Start server
python src/exercises/ex_2_02_udp.py server --port 9091

# Terminal 2: Start Wireshark/tcpdump

# Terminal 3: Run client
python src/exercises/ex_2_02_udp.py client --host 127.0.0.1 --port 9091 -o ping
```

**Expected packet sequence:**
```
1. [UDP] Client → Server   "ping" (4 bytes)
2. [UDP] Server → Client   "PONG" (4 bytes)
```

Note: No handshake, no connection state, no acknowledgements at transport layer.

## Troubleshooting

### No packets captured

1. Verify correct interface (vEthernet WSL for Docker)
2. Ensure capture started BEFORE generating traffic
3. Check display filter is not too restrictive

### Permission denied

```bash
# tcpdump requires root
sudo tcpdump -i eth0 port 9090 -w pcap/capture.pcap
```

### Cannot find interface

```bash
# List available interfaces
ip link show          # Linux
tcpdump -D            # List tcpdump interfaces
```

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
