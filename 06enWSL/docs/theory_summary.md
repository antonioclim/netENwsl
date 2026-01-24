# Week 6: Theoretical Concepts Summary

> NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

---

## Network Address Translation (NAT)

### The IPv4 Exhaustion Problem

The Internet's explosive growth in the 1990s revealed a fundamental limitation: the 32-bit IPv4 address space (approximately 4.3 billion addresses) could not accommodate the projected number of devices. While IPv6 was developed as the long-term solution, NAT emerged as a practical interim measure that remains ubiquitous today.

**Historical context:** IANA (Internet Assigned Numbers Authority) exhausted the free pool of IPv4 addresses in 2011, yet IPv4 continues to dominate due to NAT's effectiveness and slow IPv6 adoption.

### NAT Variants

**Static NAT** establishes a permanent one-to-one mapping between an internal and external address. This is used when internal servers need consistent external accessibility (e.g., web servers behind a firewall).

```
Internal: 192.168.1.10 ←→ External: 203.0.113.10 (permanent)
```

**Dynamic NAT** maintains a pool of external addresses and assigns them to internal hosts as needed. When a host initiates a connection, an available external address is allocated and released when the connection terminates.

```
Internal: 192.168.1.10 ←→ External: 203.0.113.{10-20} (from pool)
```

**PAT (Port Address Translation)**, also known as NAT Overload or NAPT, allows multiple internal hosts to share a single external IP address by multiplexing through port numbers. This is the most common form of NAT in home routers and enterprise environments.

```
Internal: 192.168.1.10:45678 ←→ External: 203.0.113.1:50001
Internal: 192.168.1.20:45679 ←→ External: 203.0.113.1:50002
(Both share the same external IP!)
```

### PAT Operation

When an internal host (192.168.1.10:45678) connects to an external server (8.8.8.8:443):

1. The router receives the outbound packet
2. It records the original source address/port in its translation table
3. It rewrites the source to its public IP with a unique port (203.0.113.1:50001)
4. When the response arrives at 203.0.113.1:50001, the router consults the table
5. It rewrites the destination back to 192.168.1.10:45678 and forwards internally

💡 **Key Insight:** The conntrack table entry is what allows return traffic to find its way back. Without this state, inbound packets would have no mapping.

### Conntrack Entry Structure

A typical conntrack entry contains two tuples:

```
tcp ESTABLISHED src=192.168.1.10 dst=8.8.8.8 sport=45678 dport=443
                src=8.8.8.8 dst=203.0.113.1 sport=443 dport=50001
```

- **First tuple:** Original direction (internal → external)
- **Second tuple:** Reply direction (external → internal, post-NAT)

### NAT Limitations

⚠️ **Common Misconception:** "NAT provides security." NAT provides *obscurity*, not security. An attacker who can predict or probe port mappings can still reach internal hosts.

- **Breaks end-to-end connectivity**: External hosts cannot initiate connections to internal hosts without port forwarding
- **Protocol complications**: Protocols embedding IP addresses in payloads (FTP, SIP) require Application Layer Gateways (ALGs)
- **State dependency**: The NAT device must maintain session state, creating a single point of failure
- **Performance overhead**: Translation processing adds latency
- **IPv6 incompatibility**: NAT is fundamentally an IPv4 workaround; IPv6 restores end-to-end addressing

---

## Supporting Protocols

### ARP (Address Resolution Protocol)

ARP resolves IPv4 addresses to MAC addresses within a local network segment. When a host needs to send a frame but only knows the destination IP, it broadcasts an ARP request. The host with the matching IP responds with its MAC address.

**ARP Cache States (Linux):**
| State | Description |
|-------|-------------|
| REACHABLE | Recently confirmed reachable |
| STALE | Needs reconfirmation before use |
| DELAY | Waiting before sending probe |
| PROBE | Actively sending probes |
| FAILED | Resolution failed |
| PERMANENT | Statically configured |

Key concepts:
- **ARP Cache**: Hosts maintain a cache of recent resolutions to minimise broadcast traffic
- **Proxy ARP**: A router can answer ARP requests on behalf of hosts in different subnets
- **Gratuitous ARP**: A host announces its own IP-MAC binding, useful for failover scenarios

⚠️ **Security concern:** ARP has no authentication mechanism, making it vulnerable to spoofing attacks.

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

| Type | Code | Name | Use |
|------|------|------|-----|
| 0 | 0 | Echo Reply | Ping response |
| 3 | 0-15 | Destination Unreachable | Routing failures |
| 8 | 0 | Echo Request | Ping |
| 11 | 0 | Time Exceeded | TTL expired (traceroute) |
| 5 | 0-3 | Redirect | Better route available |

### NDP (Neighbour Discovery Protocol)

IPv6's replacement for ARP, providing:
- **Router Discovery**: Hosts locate default gateways
- **Prefix Discovery**: Hosts learn available subnets
- **Neighbour Discovery**: Resolves IPv6 to link-layer addresses
- **SLAAC**: Stateless Address Autoconfiguration (no DHCP needed)
- **Duplicate Address Detection**: Prevents IP conflicts

---

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
- **Timeouts**: idle_timeout, hard_timeout for automatic expiry

**Table-Miss**: Packets not matching any rule trigger the default action (typically send to controller)

⚠️ **Common Misconception:** "Higher priority number = lower importance." In OpenFlow, **higher priority number = higher importance**. A rule with priority 300 takes precedence over priority 30.

---

## Traditional vs SDN: Detailed Comparison (LO6)

This section directly addresses **Learning Objective 6**: Compare traditional distributed routing with centralised SDN control, articulating trade-offs in scalability, flexibility and failure domains.

### Architectural Comparison

| Aspect | Traditional Networking | Software-Defined Networking |
|--------|----------------------|----------------------------|
| **Control Location** | Distributed (each device) | Centralised (controller) |
| **Configuration** | Per-device CLI/GUI | Programmatic API |
| **Network View** | Local (neighbours only) | Global (entire network) |
| **Protocol** | Proprietary or standard | OpenFlow (standardised) |
| **Intelligence** | In hardware (ASIC) | In software (commodity servers) |

### Scalability Trade-offs

**Traditional Networking:**
- ✅ Scales naturally — each device handles its own decisions
- ✅ No single bottleneck for forwarding decisions
- ❌ Configuration complexity grows linearly with devices
- ❌ Difficult to maintain consistent policies across devices

**SDN:**
- ✅ Single point of configuration for entire network
- ✅ Consistent policies automatically propagated
- ❌ Controller can become bottleneck for large networks
- ❌ First packet of new flows incurs controller latency
- ⚡ **Mitigation:** Controller clustering, reactive vs proactive flow installation

### Flexibility Trade-offs

**Traditional Networking:**
- ❌ Limited to vendor-provided features
- ❌ New protocols require hardware upgrades
- ❌ Multi-vendor environments difficult to manage
- ✅ Mature, well-understood behaviour

**SDN:**
- ✅ Network behaviour defined in software — change without hardware
- ✅ Custom forwarding logic, traffic engineering, security policies
- ✅ Vendor-agnostic data plane (any OpenFlow switch)
- ❌ Controller software complexity
- ❌ Debugging distributed systems is challenging

### Failure Domain Trade-offs

**Traditional Networking:**
- ✅ Distributed failure domains — one device failure affects only local traffic
- ✅ Routing protocols (OSPF, BGP) converge around failures
- ❌ Convergence can be slow (seconds to minutes)
- ❌ Inconsistent state during convergence

**SDN:**
- ❌ Controller is single point of failure (SPOF)
- ❌ If controller fails, new flows cannot be installed
- ✅ Existing flows continue to work (data plane independent)
- ⚡ **Mitigation:** Controller redundancy, graceful degradation
- ✅ Faster policy updates (milliseconds)

### When to Use Each Approach

| Use Case | Recommendation | Reasoning |
|----------|---------------|-----------|
| Small office network | Traditional | Simplicity, no controller overhead |
| Enterprise campus | Hybrid | Mix of traditional routing + SDN for policy |
| Data centre | SDN | Traffic engineering, multi-tenancy, automation |
| Service provider backbone | Traditional + SDN overlay | Proven stability + programmability |
| Research/education | SDN | Flexibility for experimentation |

### SDN Deployment Models

1. **Greenfield SDN**: Entire network built with SDN from start
2. **Hybrid SDN**: SDN controller manages subset of traffic/devices
3. **SDN Overlay**: SDN controls virtual networks on traditional underlay

---

## SDN Benefits

- **Centralised control**: Single point of configuration and visibility
- **Programmability**: Network behaviour defined in software
- **Vendor independence**: Standard southbound interfaces
- **Rapid innovation**: New features without hardware upgrades
- **Fine-grained control**: Per-flow policies
- **Automation**: API-driven network management

## SDN Challenges

- **Scalability**: Controller must handle all network events
- **Consistency**: Ensuring uniform policy across distributed switches
- **Latency**: First packets of flows incur controller round-trip
- **Security**: Controller becomes a critical attack target
- **Debugging**: Distributed systems are inherently harder to troubleshoot
- **Migration**: Moving from traditional to SDN requires careful planning

---

## Glossary Quick Reference

See `docs/glossary.md` for complete definitions of:
- NAT, PAT, SNAT, DNAT, MASQUERADE
- Conntrack, ALG, port forwarding
- Control plane, data plane, flow table
- OpenFlow, packet-in, flow-mod

---

## References

1. Kurose, J. & Ross, K. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.
2. RFC 1918 – Address Allocation for Private Internets
3. RFC 3022 – Traditional IP Network Address Translator
4. RFC 4861 – Neighbour Discovery for IP version 6
5. RFC 2131 – Dynamic Host Configuration Protocol
6. Open Networking Foundation (2015). *OpenFlow Switch Specification* Version 1.3.5
7. Kreutz, D. et al. (2015). "Software-Defined Networking: A Comprehensive Survey." *Proceedings of the IEEE*, 103(1), 14-76.

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
