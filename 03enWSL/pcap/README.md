# PCAP Reference Captures — Week 3

> NETWORKING class - ASE, CSIE | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

---

## Overview

This directory contains reference packet captures (PCAP files) for Week 3 laboratory exercises. These captures serve as:

1. **Reference outputs** — What students should see when exercises work correctly
2. **Teaching aids** — Pre-captured traffic for classroom demonstrations
3. **Verification tools** — Compare against student captures for assessment

---

## Available Captures

### 1. week3_broadcast_demo.pcap

**Contents:** UDP broadcast traffic demonstration

| Field | Value |
|-------|-------|
| Packets | ~10 |
| Duration | 5 seconds |
| Protocol | UDP |
| Source | 172.20.0.100 (client) |
| Destination | 255.255.255.255:5007 |

**Wireshark display filter:**
```
udp.port == 5007 && eth.dst == ff:ff:ff:ff:ff:ff
```

**Key observations:**
- Destination MAC is broadcast (ff:ff:ff:ff:ff:ff)
- Destination IP is limited broadcast (255.255.255.255)
- All hosts on the subnet receive these packets

---

### 2. week3_multicast_igmp.pcap

**Contents:** IGMP group join and multicast traffic

| Field | Value |
|-------|-------|
| Packets | ~15-20 |
| Duration | 10 seconds |
| Protocols | IGMP, UDP |
| Multicast group | 239.1.1.1 |
| Port | 5008 |

**Wireshark display filter:**
```
igmp || (udp.port == 5008 && ip.dst == 239.1.1.1)
```

**Key observations:**
- IGMP Membership Report when joining group
- Multicast destination MAC starts with 01:00:5e
- TTL value affects propagation scope

**IGMP message types to identify:**
- Type 0x16: Membership Report (IGMPv2)
- Type 0x17: Leave Group
- Type 0x11: Membership Query

---

### 3. week3_tcp_tunnel_flow.pcap

**Contents:** Complete TCP tunnel connection flow

| Field | Value |
|-------|-------|
| Packets | ~20-30 |
| Duration | 5 seconds |
| Protocol | TCP |
| Client | 172.20.0.100:random |
| Tunnel | 172.20.0.254:9090 |
| Server | 172.20.0.10:8080 |

**Wireshark display filter:**
```
tcp.port == 9090 || tcp.port == 8080
```

**Key observations:**
- Two separate 3-way handshakes (client↔tunnel, tunnel↔server)
- Different source ports on each connection
- Server sees tunnel's IP, not original client's IP

**TCP flags to identify:**
- SYN: Connection initiation
- SYN-ACK: Connection acceptance
- ACK: Acknowledgement
- FIN: Connection termination

---

## How to Generate Your Own Captures

### Using tcpdump (in container)

```bash
# Broadcast capture
docker exec week3_client tcpdump -i eth0 -w /app/pcap/my_broadcast.pcap \
    'udp port 5007' -c 20

# Multicast/IGMP capture
docker exec week3_client tcpdump -i eth0 -w /app/pcap/my_multicast.pcap \
    'igmp or (udp port 5008)' -c 30

# TCP tunnel capture
docker exec week3_router tcpdump -i eth0 -w /app/pcap/my_tunnel.pcap \
    'tcp port 9090 or tcp port 8080' -c 50
```

### Using scripts

```bash
# Use the capture_traffic.py script
python scripts/capture_traffic.py --interface eth0 --duration 30 \
    --filter "udp port 5007" --output pcap/my_capture.pcap
```

---

## Opening in Wireshark

### From WSL

```bash
# Copy to Windows-accessible location
cp pcap/week3_broadcast_demo.pcap /mnt/c/Users/YourName/Desktop/

# Or use Wireshark directly if installed
wireshark pcap/week3_broadcast_demo.pcap &
```

### Display Filter Quick Reference

| Purpose | Filter |
|---------|--------|
| All broadcast | `eth.dst == ff:ff:ff:ff:ff:ff` |
| UDP broadcast on port 5007 | `udp.port == 5007` |
| Multicast traffic | `ip.dst >= 224.0.0.0 && ip.dst <= 239.255.255.255` |
| IGMP only | `igmp` |
| TCP handshakes | `tcp.flags.syn == 1` |
| Tunnel traffic | `tcp.port == 9090` |
| HTTP traffic | `tcp.port == 8080` |

---

## Verification Checklist

When comparing your captures to reference files, verify:

### Broadcast (ex_3_01)
- [ ] Destination IP is 255.255.255.255 or subnet broadcast
- [ ] Destination MAC is ff:ff:ff:ff:ff:ff
- [ ] SO_BROADCAST was set (no "Permission denied" errors)

### Multicast (ex_3_02)
- [ ] IGMP Membership Report present
- [ ] Destination IP is 239.x.x.x range
- [ ] Destination MAC starts with 01:00:5e
- [ ] TTL matches configured value

### TCP Tunnel (ex_3_03)
- [ ] Two complete 3-way handshakes visible
- [ ] Source IP changes between client→tunnel and tunnel→server
- [ ] Data is relayed in both directions

---

## Troubleshooting

### No packets captured

1. Check interface name: `ip link show`
2. Verify containers are running: `docker ps`
3. Check filter syntax: start with no filter, then add constraints

### Cannot open PCAP file

1. Verify file exists: `ls -la pcap/`
2. Check file size (should be > 0 bytes)
3. Try `tcpdump -r filename.pcap` to validate

### Wireshark shows "malformed packets"

1. Capture may have been truncated
2. Try capturing with `-s 0` for full packets
3. Check network interface MTU settings

---

## Note on File Availability

Reference PCAP files may need to be generated locally due to environment-specific network configurations. Use the commands above or run the laboratory exercises to create captures.

To generate reference captures automatically:

```bash
make docker-up
# Wait for containers to start
python scripts/capture_traffic.py --generate-references
```

---

*NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim*
*Week 3: Network Programming — Broadcast, Multicast and TCP Tunnelling*
