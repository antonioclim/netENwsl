# Packet Capture Storage

> NETWORKING class - ASE, Informatics | by Revolvix

## Purpose

This directory stores packet captures (PCAP files) generated during laboratory exercises and demonstrations.

## Naming Convention

Use the following format for capture files:

```
week6_<exercise>_<timestamp>.pcap
```

Examples:
- `week6_nat_demo_20250107_1430.pcap`
- `week6_sdn_policies_20250107_1445.pcap`
- `week6_pat_translation_20250107_1500.pcap`

## Capturing Traffic

### From within Mininet topology

```bash
# On specific host
mininet> h1 tcpdump -i h1-eth0 -w /pcap/capture.pcap &

# On NAT router public interface
mininet> rnat tcpdump -i rnat-eth1 -w /pcap/nat_public.pcap &
```

### Using the capture script

```powershell
python scripts/capture_traffic.py --interface eth0 --output pcap/week6_capture.pcap
```

### Using Wireshark (Windows)

1. Open Wireshark
2. Select the Docker network interface
3. Start capture
4. Save to this directory when complete

## Analysis Tips

### Useful Wireshark Filters for Week 6

```
# NAT Analysis
ip.addr == 203.0.113.0/24        # Public network traffic
ip.addr == 192.168.1.0/24        # Private network traffic
tcp.port == 5000                  # NAT observer traffic

# SDN Analysis
ip.addr == 10.0.6.0/24           # SDN subnet
openflow_v4                       # OpenFlow messages
tcp.port == 6633 || tcp.port == 6653  # Controller traffic

# Protocol-specific
icmp                              # Ping traffic
tcp.flags.syn == 1               # TCP connection attempts
```

## Cleanup

Before the next laboratory session:

```powershell
python scripts/cleanup.py --full
```

This removes all PCAP files from this directory.

---

*NETWORKING class - ASE, Informatics | by Revolvix*
