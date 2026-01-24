# 📖 Glossary — Week 6: NAT/PAT & SDN

## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## NAT and Address Translation Terms

| Term | Definition | Example |
|------|------------|---------|
| **NAT** | Network Address Translation — rewrites IP addresses in packet headers as they pass through a router | Private 192.168.1.10 → Public 203.0.113.1 |
| **PAT** | Port Address Translation — extends NAT by also translating port numbers, enabling many-to-one mapping | Also called NAPT, NAT Overload |
| **SNAT** | Source NAT — rewrites the source address of outbound packets | Used for internet access from private networks |
| **DNAT** | Destination NAT — rewrites the destination address of inbound packets | Used for port forwarding to internal servers |
| **MASQUERADE** | Dynamic SNAT that automatically uses the outbound interface's IP | `iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE` |
| **Conntrack** | Connection tracking — kernel subsystem that tracks NAT state | Stores 5-tuple mappings for bidirectional translation |
| **ALG** | Application Layer Gateway — NAT helper for protocols that embed IPs in payload | FTP, SIP, H.323 require ALGs |
| **Port forwarding** | Static DNAT rule mapping external port to internal host:port | External:8080 → Internal:192.168.1.10:80 |
| **Hairpin NAT** | NAT that allows internal hosts to reach internal servers via public IP | Also called NAT loopback or NAT reflection |
| **RFC 1918** | Standard defining private IPv4 address ranges | 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 |
| **TEST-NET-3** | Documentation address range from RFC 5737 | 203.0.113.0/24 — used in examples |

---

## SDN Architecture Terms

| Term | Definition | Example |
|------|------------|---------|
| **SDN** | Software-Defined Networking — architecture separating control and data planes | Controller + programmable switches |
| **Control plane** | Network intelligence layer that makes forwarding decisions | Runs on controller server |
| **Data plane** | Packet forwarding layer that moves traffic | Runs on switches at line rate |
| **Southbound interface** | Protocol between controller and switches | OpenFlow is the main example |
| **Northbound interface** | API between controller and applications | REST APIs, Python libraries |
| **Flow** | A sequence of packets sharing common header fields | All packets from 10.0.6.11 to 10.0.6.12 on port 80 |
| **Flow table** | Switch data structure storing match-action rules | Each entry: match + actions + counters |
| **Flow entry** | Single rule in a flow table | priority=100, match=icmp, action=output:3 |

---

## OpenFlow Protocol Terms

| Term | Definition | Example |
|------|------------|---------|
| **OpenFlow** | Protocol for controller-switch communication | Version 1.3 is common standard |
| **Packet-in** | Message from switch to controller for unmatched packets | Triggers when no flow matches |
| **Flow-mod** | Message from controller to switch to install/modify rules | Adds new flow entry |
| **Packet-out** | Message from controller telling switch to send a specific packet | Used with packet-in responses |
| **Table-miss** | Event when packet matches no flow entries | Default: send to controller |
| **Priority** | Flow rule importance — higher number = checked first | Priority 300 beats priority 30 |
| **Match fields** | Criteria for flow matching | `nw_src`, `nw_dst`, `tp_dst`, `ip_proto` |
| **Actions** | What to do with matched packets | `output:3`, `drop`, `CONTROLLER` |
| **Idle timeout** | Delete flow after N seconds of no matches | `idle_timeout=60` |
| **Hard timeout** | Delete flow after N seconds regardless | `hard_timeout=300` |

---

## Commands Reference

### NAT Commands (iptables)

| Command | Purpose | Example |
|---------|---------|---------|
| `iptables -t nat -L` | List NAT rules | `iptables -t nat -L -n -v` |
| `iptables -t nat -A POSTROUTING` | Add SNAT rule | `-o eth1 -j MASQUERADE` |
| `iptables -t nat -A PREROUTING` | Add DNAT rule | `-p tcp --dport 80 -j DNAT --to 192.168.1.10` |
| `iptables -t nat -F` | Flush all NAT rules | Removes all entries |
| `conntrack -L` | List active connections | Shows 5-tuple mappings |
| `conntrack -D` | Delete connection entries | `-s 192.168.1.10` |

### SDN Commands (ovs-ofctl)

| Command | Purpose | Example |
|---------|---------|---------|
| `ovs-ofctl dump-flows` | Show flow table | `ovs-ofctl -O OpenFlow13 dump-flows s1` |
| `ovs-ofctl add-flow` | Install flow rule | `"priority=100,icmp,actions=output:3"` |
| `ovs-ofctl del-flows` | Delete flow rules | `"priority=100,icmp"` |
| `ovs-ofctl dump-ports` | Show port statistics | `ovs-ofctl -O OpenFlow13 dump-ports s1` |
| `ovs-vsctl show` | Show OVS configuration | Bridge and port info |
| `ovs-vsctl list-br` | List bridges | Switch names |

---

## Protocol Numbers

| Protocol | IP Protocol Number | Common Use |
|----------|-------------------|------------|
| ICMP | 1 | Ping, traceroute |
| TCP | 6 | HTTP, SSH, most applications |
| UDP | 17 | DNS, DHCP, streaming |

---

## Port Numbers (This Week)

| Port | Protocol | Service |
|------|----------|---------|
| 22 | TCP | SSH |
| 80 | TCP | HTTP |
| 443 | TCP | HTTPS |
| 5000 | TCP | NAT Observer (lab) |
| 6633 | TCP | OpenFlow (legacy) |
| 6653 | TCP | OpenFlow (standard) |
| 9090 | TCP | TCP Echo (lab) |
| 9091 | UDP | UDP Echo (lab) |

---

## Flow Rule Syntax Quick Reference

```bash
# Basic structure
"priority=N,MATCH_FIELDS,actions=ACTIONS"

# Match fields
ip                    # IPv4 packets (eth_type=0x0800)
icmp                  # ICMP packets (ip_proto=1)
tcp                   # TCP packets (ip_proto=6)
udp                   # UDP packets (ip_proto=17)
arp                   # ARP packets (eth_type=0x0806)
nw_src=10.0.6.11      # Source IP
nw_dst=10.0.6.13      # Destination IP
tp_src=80             # Source port (TCP/UDP)
tp_dst=443            # Destination port (TCP/UDP)
in_port=1             # Input port on switch

# Actions
output:3              # Forward to port 3
drop                  # Drop packet (empty actions)
CONTROLLER            # Send to controller
NORMAL                # Use normal L2 switching
flood                 # Send to all ports except input

# Examples
"priority=100,icmp,nw_src=10.0.6.11,nw_dst=10.0.6.13,actions=output:3"
"priority=200,tcp,tp_dst=80,actions=output:2"
"priority=50,ip,nw_dst=10.0.6.13,actions=drop"
```

---

## Relationships Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              SDN ARCHITECTURE                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    ┌─────────────────┐                                                      │
│    │  Applications   │  ← Northbound API (REST, Python)                     │
│    └────────┬────────┘                                                      │
│             │                                                               │
│    ┌────────▼────────┐                                                      │
│    │   Controller    │  ← Control Plane (OS-Ken, OpenDaylight)              │
│    │                 │     • Installs flow rules                            │
│    │  ┌───────────┐  │     • Receives packet-in                             │
│    │  │  Policy   │  │     • Sends flow-mod                                 │
│    │  │  Engine   │  │                                                      │
│    │  └───────────┘  │                                                      │
│    └────────┬────────┘                                                      │
│             │ OpenFlow (Southbound)                                         │
│    ┌────────▼────────┐                                                      │
│    │     Switch      │  ← Data Plane (OVS, hardware switches)               │
│    │                 │     • Matches packets to flows                       │
│    │  ┌───────────┐  │     • Executes actions                               │
│    │  │Flow Table │  │     • Forwards at line rate                          │
│    │  └───────────┘  │                                                      │
│    └─────────────────┘                                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              NAT TRANSLATION                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Private Network              NAT Router              Public Network       │
│   192.168.1.0/24              203.0.113.1              Internet             │
│                                                                             │
│   ┌──────────┐                ┌──────────┐                                  │
│   │   h1     │  ──outbound──▶ │          │                                  │
│   │ .10:4567 │                │ Conntrack│  ──translated──▶  Server         │
│   └──────────┘                │  Table   │                   8.8.8.8        │
│                               │          │                                  │
│   ┌──────────┐                │ ┌──────┐ │                                  │
│   │   h2     │  ──outbound──▶ │ │Entry1│ │                                  │
│   │ .20:7890 │                │ │Entry2│ │                                  │
│   └──────────┘                │ └──────┘ │                                  │
│                               └──────────┘                                  │
│                                                                             │
│   Original: 192.168.1.10:4567 → 8.8.8.8:443                                │
│   Translated: 203.0.113.1:50001 → 8.8.8.8:443                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
