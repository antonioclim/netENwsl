# Packet Captures — Week 14: Integration and Review

> **NETWORKING** Laboratory — ASE-CSIE, Bucharest
>
> by ing. dr. Antonio Clim

---

## Directory Purpose

This directory stores packet capture files (`.pcap`) generated during Week 14 laboratory exercises. These captures demonstrate integrated networking concepts across all protocol layers studied throughout the semester.

---

## Expected Capture Files

| Filename | Protocol Stack | Exercise Reference | Typical Size |
|----------|---------------|-------------------|--------------|
| `tcp_echo_traffic.pcap` | TCP/IP | Ex 14.01 | 5-15 KB |
| `http_session.pcap` | HTTP/TCP/IP | Ex 14.02 | 10-30 KB |
| `full_stack_demo.pcap` | Mixed protocols | Ex 14.03 | 20-50 KB |
| `integration_test.pcap` | All layers | Final review | 30-80 KB |

---

## Wireshark Analysis Instructions

### Opening Captures in Wireshark

1. Launch Wireshark from Windows Start Menu
2. Navigate to: File → Open
3. Browse to: `D:\NETWORKING\WEEK14\14enWSL\pcap\`
4. Select the `.pcap` file to analyse

### Recommended Display Filters

```wireshark
# TCP traffic to specific port
tcp.port == 9090

# HTTP requests and responses
http

# All traffic involving the load balancer
ip.addr == 172.20.14.10

# DNS queries only
dns.flags.response == 0

# TCP connection establishment (SYN packets)
tcp.flags.syn == 1 && tcp.flags.ack == 0

# Retransmissions (indicates network issues)
tcp.analysis.retransmission
```

### Protocol Analysis Checklist

- [ ] Identify complete TCP three-way handshake sequences
- [ ] Verify HTTP request/response pairs match expectations
- [ ] Check load balancer traffic distribution patterns
- [ ] Note any retransmissions or connection resets
- [ ] Examine DNS query and response timing

---

## Generating New Captures

### From WSL Terminal

```bash
# Navigate to week directory
cd /mnt/d/NETWORKING/WEEK14/14enWSL

# Start capture with duration limit
python3 scripts/capture_traffic.py --duration 60 --output pcap/my_capture.pcap

# Run exercises while capture is active
python3 src/exercises/ex_14_01_review_drills.py
```

### Capture Best Practices

- Use specific interface filters to reduce noise
- Set appropriate capture duration (30-120 seconds)
- Name files descriptively: `protocol_scenario_date.pcap`

---

## Troubleshooting

**No traffic captured?**
- Verify Docker containers are running: `docker ps`
- Check correct interface selection in capture script
- Ensure exercises generate network traffic

**Capture file too large?**
- Apply capture filters to limit scope
- Reduce capture duration
- Filter specific protocols only

**Cannot open in Wireshark?**
- Verify file was saved completely
- Check file permissions
- Try opening from Wireshark directly

---

*Packet captures provide concrete evidence of network behaviour — analyse them thoroughly.*
