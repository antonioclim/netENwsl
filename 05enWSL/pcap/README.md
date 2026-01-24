# Packet Capture Directory — Week 5

> Computer Networks Laboratory — ASE-CSIE Bucharest

This directory stores packet captures (PCAP files) generated during laboratory exercises.

---

## Naming Convention

```
week05_lo{N}_{protocol}_{scenario}.pcap
```

| Example | Description |
|---------|-------------|
| `week05_lo3_icmp_ping_test.pcap` | ICMP ping between containers |
| `week05_lo2_udp_echo_session.pcap` | UDP echo server communication |

---

## How to Capture Traffic

### Method 1: Lab Script (Recommended)

```bash
python3 scripts/capture_traffic.py --duration 60 --output pcap/week05_capture.pcap
make capture
```

### Method 2: Manual tcpdump

```bash
docker exec -it week5_python bash
tcpdump -i eth0 -w /app/pcap/capture.pcap
```

### Method 3: Wireshark on Windows

1. Select interface: **vEthernet (WSL)**
2. Apply filter: `ip.addr == 10.5.0.0/24`

---

## Useful Filters

| tcpdump Filter | Purpose |
|----------------|---------|
| `host 10.5.0.10` | Python container traffic |
| `net 10.5.0.0/24` | All labnet traffic |
| `port 9999` | UDP echo server |
| `icmp` | ICMP packets |

---

## Cleanup

```bash
rm -f pcap/*.pcap
make clean
```

---

*Week 5: IP Addressing, Subnetting and VLSM — Packet Capture Guide*
