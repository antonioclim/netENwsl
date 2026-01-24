# 📦 Example PCAP Files

## Week 13: IoT and Security

---

## Purpose

This directory contains pre-generated packet captures for reference and offline analysis when Docker services are not available.

---

## Files to Generate

| File | Description | Filter | Generation Command |
|------|-------------|--------|-------------------|
| `mqtt_plaintext.pcap` | MQTT pub/sub on port 1883 | `tcp.port == 1883` | See below |
| `mqtt_tls.pcap` | MQTT over TLS on port 8883 | `tcp.port == 8883` | See below |
| `port_scan.pcap` | TCP connect scan example | `tcp.flags.syn == 1` | See below |
| `ftp_session.pcap` | FTP control channel | `tcp.port == 2121` | See below |

---

## How to Generate

### Step 1: Start Laboratory
```bash
cd 13enWSL
make start
# Wait for services to be ready
```

### Step 2: Capture MQTT Plaintext
```bash
# Terminal 1: Start capture
python scripts/capture_traffic.py \
    --filter "port 1883" \
    --output pcap/examples/mqtt_plaintext.pcap \
    --duration 30

# Terminal 2: Generate traffic
python src/exercises/ex_13_02_mqtt_client.py \
    --mode publish \
    --topic sensors/temperature \
    --message "23.5" \
    --count 5
```

### Step 3: Capture MQTT TLS
```bash
# Terminal 1: Start capture
python scripts/capture_traffic.py \
    --filter "port 8883" \
    --output pcap/examples/mqtt_tls.pcap \
    --duration 30

# Terminal 2: Generate traffic
python src/exercises/ex_13_02_mqtt_client.py \
    --mode publish \
    --broker localhost \
    --port 8883 \
    --tls \
    --cafile docker/configs/certs/ca.crt \
    --topic secure/data \
    --message "encrypted" \
    --count 5
```

### Step 4: Capture Port Scan
```bash
# Terminal 1: Start capture
python scripts/capture_traffic.py \
    --filter "host 10.0.13.11" \
    --output pcap/examples/port_scan.pcap \
    --duration 30

# Terminal 2: Perform scan
python src/exercises/ex_13_01_port_scanner.py \
    --target 10.0.13.11 \
    --ports 1-100
```

---

## Analysis in Wireshark

### MQTT Plaintext Analysis
1. Open `mqtt_plaintext.pcap`
2. Filter: `mqtt`
3. Right-click packet → Follow → TCP Stream
4. Observe: Topic names and payloads visible in plaintext

### MQTT TLS Comparison
1. Open `mqtt_tls.pcap`
2. Filter: `tls`
3. Observe: "Application Data" records are encrypted
4. Note: IP addresses, ports, timing still visible

### Port Scan Patterns
1. Open `port_scan.pcap`
2. Filter: `tcp.flags.syn == 1`
3. Observe: Multiple SYN packets to different ports
4. Note patterns: SYN→SYN-ACK→ACK (open) vs SYN→RST (closed)

---

## Educational Notes

### What These Captures Demonstrate

| Capture | Demonstrates |
|---------|--------------|
| `mqtt_plaintext.pcap` | Complete visibility of MQTT traffic without TLS |
| `mqtt_tls.pcap` | What TLS hides vs. what remains visible (metadata) |
| `port_scan.pcap` | TCP handshake patterns for open/closed/filtered ports |

### Key Observations

1. **Plaintext MQTT**: Topic names, payloads, client IDs all visible
2. **TLS MQTT**: Only connection metadata visible; content encrypted
3. **Port Scanning**: Different responses for open (SYN-ACK) vs closed (RST)

---

## File Naming Convention

```
week13_lo{N}_{protocol}_{scenario}.pcap

Examples:
- week13_lo1_mqtt_pubsub.pcap
- week13_lo2_tls_handshake.pcap
- week13_lo3_tcp_scan.pcap
```

---

*Week 13: IoT and Security*
*Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim*
