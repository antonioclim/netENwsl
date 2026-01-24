# 📖 Glossary — Week 7: Packet Interception, Filtering and Defensive Port Probing
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Capture Tools

| Term | Definition | Example |
|------|------------|---------|
| **tcpdump** | Command-line packet analyser for Unix/Linux. Captures packets matching BPF filters. | `sudo tcpdump -i eth0 port 9090 -w capture.pcap` |
| **Wireshark** | GUI packet analyser with protocol dissection. Reads pcap files and live captures. | Open `.pcap` file, apply display filter |
| **tshark** | Command-line version of Wireshark. Useful for scripted analysis. | `tshark -r capture.pcap -Y "tcp.port==9090"` |
| **pcap** | Packet capture file format. Standard extension: `.pcap` or `.pcapng`. | `capture.pcap` |
| **BPF** | Berkeley Packet Filter. Syntax for capture filters in tcpdump/Wireshark. | `tcp port 9090 and host 10.0.7.100` |
| **Display filter** | Wireshark filter applied after capture. Different syntax from BPF. | `tcp.port == 9090 && ip.addr == 10.0.7.100` |
| **Promiscuous mode** | Capture mode that receives all packets on the network segment, not just those addressed to the interface. | Enable in Wireshark capture options |

---

## Filtering Actions

| Term | Definition | Example |
|------|------------|---------|
| **DROP** | Firewall action that silently discards packets. Sender receives no response. | `iptables -j DROP` |
| **REJECT** | Firewall action that discards packets and sends refusal notification (RST or ICMP). | `iptables -j REJECT` |
| **ACCEPT** | Firewall action that allows packets to pass through. | `iptables -j ACCEPT` |
| **LOG** | Firewall action that logs packet information (can be combined with other actions). | `iptables -j LOG --log-prefix "BLOCKED: "` |
| **iptables** | Linux firewall administration tool. Manages packet filtering rules in the kernel. | `sudo iptables -L -n -v` |
| **Chain** | Ordered list of firewall rules. Standard chains: INPUT, OUTPUT, FORWARD. | `iptables -A INPUT ...` adds to INPUT chain |
| **Rule** | Single firewall policy: match criteria + action. Evaluated in order until match. | `-p tcp --dport 9090 -j DROP` |

---

## Port States

| Term | Definition | Network Evidence |
|------|------------|------------------|
| **Open** | A service is actively listening on the port and will accept connections. | TCP: SYN-ACK response; UDP: application response |
| **Closed** | No service is listening, but the host is reachable and responsive. | TCP: RST response; UDP: ICMP port unreachable |
| **Filtered** | Cannot determine port state; packets are being blocked (likely by firewall). | No response (timeout) or ICMP admin prohibited |
| **Port probe** | Technique to determine port state by sending test packets and analysing responses. | `port_probe.py --ports 22,80,443` |

---

## TCP Concepts

| Term | Definition | Example |
|------|------------|---------|
| **Three-way handshake** | TCP connection establishment: SYN → SYN-ACK → ACK. Required before data transfer. | Visible as 3 packets in Wireshark |
| **SYN** | TCP flag indicating connection initiation request. First packet of handshake. | `tcp.flags.syn == 1 && tcp.flags.ack == 0` |
| **SYN-ACK** | TCP flags indicating handshake acceptance. Second packet of handshake. | `tcp.flags.syn == 1 && tcp.flags.ack == 1` |
| **ACK** | TCP flag acknowledging received data. Third packet of handshake and ongoing. | `tcp.flags.ack == 1` |
| **RST** | TCP Reset flag. Indicates abrupt connection termination or refusal. | `tcp.flags.reset == 1` |
| **FIN** | TCP Finish flag. Indicates graceful connection close. | `tcp.flags.fin == 1` |
| **Timeout** | Client gives up waiting for response after specified duration. | `--timeout 5` (5 seconds) |

---

## UDP Concepts

| Term | Definition | Example |
|------|------------|---------|
| **Connectionless** | UDP requires no handshake. Packets are sent independently without delivery confirmation. | `sendto()` returns immediately |
| **Datagram** | Single UDP packet. Self-contained unit of data with header and payload. | One `sendto()` = one datagram |
| **Fire-and-forget** | UDP sending pattern. Sender cannot know if packet arrived without application-layer confirmation. | UDP sender "succeeds" even if dropped |
| **ICMP port unreachable** | Error message sent when UDP packet arrives at a closed port. | ICMP Type 3, Code 3 |

---

## ICMP Messages

| Type | Code | Name | Meaning |
|------|------|------|---------|
| 3 | 0 | Net Unreachable | Destination network cannot be reached |
| 3 | 1 | Host Unreachable | Destination host cannot be reached |
| 3 | 3 | Port Unreachable | Destination port has no listening service |
| 3 | 9 | Admin Prohibited | Firewall policy blocks the traffic |
| 3 | 10 | Admin Prohibited | Firewall policy blocks the traffic (host) |
| 3 | 13 | Admin Prohibited | Communication administratively filtered |

**Wireshark filter:** `icmp.type == 3`

---

## Commands Reference

### tcpdump

| Command | Purpose |
|---------|---------|
| `sudo tcpdump -i any` | Capture on all interfaces |
| `sudo tcpdump -i eth0 -w file.pcap` | Save capture to file |
| `sudo tcpdump -r file.pcap` | Read saved capture |
| `sudo tcpdump port 9090` | Filter by port |
| `sudo tcpdump host 10.0.7.100` | Filter by host |
| `sudo tcpdump -n` | Don't resolve hostnames |
| `sudo tcpdump -c 100` | Capture only 100 packets |
| `sudo tcpdump -X` | Show packet contents in hex and ASCII |

### tshark

| Command | Purpose |
|---------|---------|
| `tshark -i eth0` | Live capture |
| `tshark -r file.pcap` | Read pcap file |
| `tshark -r file.pcap -Y "tcp.port==9090"` | Apply display filter |
| `tshark -r file.pcap -q -z conv,tcp` | Show TCP conversations |
| `tshark -r file.pcap -T fields -e ip.src -e ip.dst` | Extract specific fields |

### iptables

| Command | Purpose |
|---------|---------|
| `sudo iptables -L -n -v` | List all rules with details |
| `sudo iptables -A INPUT -p tcp --dport 9090 -j DROP` | Add DROP rule for TCP port 9090 |
| `sudo iptables -A INPUT -p tcp --dport 9090 -j REJECT` | Add REJECT rule |
| `sudo iptables -D INPUT -p tcp --dport 9090 -j DROP` | Delete specific rule |
| `sudo iptables -F INPUT` | Flush (delete) all INPUT rules |
| `sudo iptables-save` | Output rules in restorable format |
| `sudo iptables-restore < rules.txt` | Restore saved rules |

---

## Wireshark Display Filters

| Filter | Purpose |
|--------|---------|
| `tcp.port == 9090` | TCP traffic on port 9090 |
| `udp.port == 9091` | UDP traffic on port 9091 |
| `tcp.flags.syn == 1 && tcp.flags.ack == 0` | TCP SYN packets (connection attempts) |
| `tcp.flags.reset == 1` | TCP RST packets |
| `icmp.type == 3` | ICMP destination unreachable |
| `ip.addr == 10.0.7.100` | Traffic to/from specific IP |
| `ip.src == 10.0.7.11 && ip.dst == 10.0.7.100` | Traffic between specific hosts |
| `tcp.analysis.retransmission` | TCP retransmissions |
| `frame.time_relative > 1` | Packets after 1 second |

---

## Acronyms

| Acronym | Full Form | Context |
|---------|-----------|---------|
| BPF | Berkeley Packet Filter | Capture filter syntax |
| RST | Reset | TCP flag for connection abort |
| SYN | Synchronise | TCP flag for connection start |
| ACK | Acknowledge | TCP flag for receipt confirmation |
| FIN | Finish | TCP flag for connection close |
| ICMP | Internet Control Message Protocol | Network error/diagnostic messages |
| TTL | Time To Live | IP header field, packet hop limit |
| pcap | Packet Capture | File format for saved packets |
| WSL | Windows Subsystem for Linux | Linux environment on Windows |

---

## Relationships Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PACKET CAPTURE & FILTERING                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   CAPTURE LAYER                        FILTERING LAYER                      │
│   ─────────────                        ───────────────                      │
│   ┌─────────┐                          ┌─────────┐                         │
│   │ tcpdump │──┐                   ┌───│iptables │                         │
│   └─────────┘  │    ┌─────────┐    │   └─────────┘                         │
│                ├───▶│  pcap   │    │        │                              │
│   ┌─────────┐  │    │  file   │    │   ┌────┴────┐                         │
│   │ tshark  │──┘    └─────────┘    │   │         │                         │
│   └─────────┘           │          │ ACCEPT   DROP   REJECT                │
│        │                ▼          │   │       │       │                   │
│        │         ┌───────────┐     │   │       │       │                   │
│        └────────▶│ Wireshark │     │   ▼       ▼       ▼                   │
│                  └───────────┘     │ Pass   Silent   RST/ICMP              │
│                                    │        discard  response              │
│                                    │                                       │
│   PROTOCOLS                        │   PORT STATES                         │
│   ─────────                        │   ───────────                         │
│   TCP: SYN→SYN-ACK→ACK→Data→FIN   │   Open: service listening             │
│   UDP: Data (no handshake)         │   Closed: RST/ICMP response           │
│   ICMP: Error messages             │   Filtered: no response               │
│                                    │                                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

*Computer Networks — Week 7: Packet Interception, Filtering and Defensive Port Probing*  
*ASE Bucharest, CSIE | by ing. dr. Antonio Clim*
