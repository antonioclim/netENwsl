# Week 6: Theoretical Concepts Summary

> NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

## Network Address Translation (NAT)

### The IPv4 Exhaustion Problem

The Internet's explosive growth in the 1990s revealed a fundamental limitation: the 32-bit IPv4 address space (approximately 4.3 billion addresses) could not accommodate the projected number of devices. While IPv6 was developed as the long-term solution, NAT emerged as a practical interim measure that remains ubiquitous today.

### NAT Variants

**Static NAT** establishes a permanent one-to-one mapping between an internal and external address. This is used when internal servers need consistent external accessibility (e.g., web servers behind a firewall).

**Dynamic NAT** maintains a pool of external addresses and assigns them to internal hosts as needed. When a host initiates a connection, an available external address is allocated and released when the connection terminates.

**PAT (Port Address Translation)**, also known as NAT Overload or NAPT, allows multiple internal hosts to share a single external IP address by multiplexing through port numbers. This is the most common form of NAT in home routers and enterprise environments.

### PAT Operation

When an internal host (192.168.1.10:45678) connects to an external server (8.8.8.8:443):

1. The router receives the outbound packet
2. It records the original source address/port in its translation table
3. It rewrites the source to its public IP with a unique port (203.0.113.1:50001)
4. When the response arrives at 203.0.113.1:50001, the router consults the table
5. It rewrites the destination back to 192.168.1.10:45678 and forwards internally

💡 **Key Insight:** The conntrack table entry is what allows return traffic to find its way back. Without this state, inbound packets would have no mapping.

### NAT Limitations

⚠️ **Common Misconception:** "NAT provides security." NAT provides *obscurity*, not security. An attacker who can predict or probe port mappings can still reach internal hosts.

- **Breaks end-to-end connectivity**: External hosts cannot initiate connections to internal hosts without port forwarding
- **Protocol complications**: Protocols embedding IP addresses in payloads (FTP, SIP) require Application Layer Gateways (ALGs)
- **State dependency**: The NAT device must maintain session state, creating a single point of failure
- **Performance overhead**: Translation processing adds latency

## Supporting Protocols

### ARP (Address Resolution Protocol)

ARP resolves IPv4 addresses to MAC addresses within a local network segment. When a host needs to send a frame but only knows the destination IP, it broadcasts an ARP request. The host with the matching IP responds with its MAC address.

Key concepts:
- **ARP Cache**: Hosts maintain a cache of recent resolutions to minimise broadcast traffic
- **Proxy ARP**: A router can answer ARP requests on behalf of hosts in different subnets
- **Gratuitous ARP**: A host announces its own IP-MAC binding, useful for failover scenarios

### DHCP (Dynamic Host Configuration Protocol)

DHCP automates IP configuration for hosts joining a network. The DORA process:

1. **Discover**: Client broadcasts seeking DHCP servers
2. **Offer**: Servers respond with configuration offers
3. **Request**: Client requests a specific offer
4. **Acknowledge**: Server confirms and commits the lease

DHCP provides: IP address, subnet mask, default gateway, DNS servers and lease duration.

💡 **Key Insight:** DHCP leases are temporary. The client must renew before expiry or lose its address.

### ICMP (Internet Control Message Protocol)

ICMP enables network diagnostics and error reporting. Key message types:

- **Echo Request/Reply (Type 8/0)**: Used by ping
- **Destination Unreachable (Type 3)**: Indicates routing failures
- **Time Exceeded (Type 11)**: TTL expired, used by traceroute
- **Redirect (Type 5)**: Suggests a better route

### NDP (Neighbour Discovery Protocol)

IPv6's replacement for ARP, providing:
- **Router Discovery**: Hosts locate default gateways
- **Prefix Discovery**: Hosts learn available subnets
- **Neighbour Discovery**: Resolves IPv6 to link-layer addresses
- **SLAAC**: Stateless Address Autoconfiguration

## Software-Defined Networking (SDN)

### Architecture

SDN fundamentally separates network control from data forwarding:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CONTROL PLANE                                      │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                     SDN Controller (OS-Ken)                            │  │
│  │  • Maintains global network view                                       │  │
│  │  • Computes forwarding decisions                                       │  │
│  │  • Implements routing algorithms and policies                          │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │ Southbound Interface (OpenFlow)
┌──────────────────────────────────▼──────────────────────────────────────────┐
│                            DATA PLANE                                        │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                    Switches / Routers                                  │  │
│  │  • Execute controller-provided rules                                   │  │
│  │  • Forward packets at line rate                                        │  │
│  │  • Report statistics to controller                                     │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Control Plane**: Centralised intelligence that makes forwarding decisions
- Runs on commodity servers
- Maintains global network view
- Implements routing algorithms and policies

**Data Plane**: Distributed forwarding that moves packets
- Runs on switches/routers
- Executes controller-provided rules
- Operates at line rate

**Southbound Interface**: Protocol between controller and switches (typically OpenFlow)

**Northbound Interface**: API for applications to programme network behaviour

⚠️ **Common Misconception:** "The SDN controller forwards packets." The controller only *installs rules*. The switches do the actual forwarding based on those rules.

### OpenFlow Protocol

OpenFlow defines how controllers communicate with switches. Key concepts:

**Flow Table**: Each switch maintains one or more flow tables containing rules

**Flow Entry**: Match criteria paired with actions
- **Match Fields**: Source/destination IP, ports, protocols, VLANs, etc.
- **Actions**: Output to port, drop, modify headers, send to controller
- **Priority**: Higher priority rules match first (opposite of what some expect!)
- **Counters**: Packet/byte statistics

**Table-Miss**: Packets not matching any rule trigger the default action (typically send to controller)

⚠️ **Common Misconception:** "Higher priority number = lower importance." In OpenFlow, **higher priority number = higher importance**. A rule with priority 300 takes precedence over priority 30.

### SDN Benefits

- **Centralised control**: Single point of configuration and visibility
- **Programmability**: Network behaviour defined in software
- **Vendor independence**: Standard southbound interfaces
- **Rapid innovation**: New features without hardware upgrades
- **Fine-grained control**: Per-flow policies

### SDN Challenges

- **Scalability**: Controller must handle all network events
- **Consistency**: Ensuring uniform policy across distributed switches
- **Latency**: First packets of flows incur controller round-trip
- **Security**: Controller becomes a critical attack target

## Glossary Quick Reference

See `docs/glossary.md` for complete definitions of:
- NAT, PAT, SNAT, DNAT, MASQUERADE
- Conntrack, ALG, port forwarding
- Control plane, data plane, flow table
- OpenFlow, packet-in, flow-mod

## References

1. Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
2. RFC 1918 – Address Allocation for Private Internets
3. RFC 3022 – Traditional IP Network Address Translator
4. RFC 4861 – Neighbour Discovery for IP version 6
5. RFC 2131 – Dynamic Host Configuration Protocol
6. Open Networking Foundation (2015). *OpenFlow Switch Specification* Version 1.3.5

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
