# Glossary — Week 3: Broadcast, Multicast and TCP Tunnelling

> Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Core Communication Terms

| Term | Definition | Example |
|------|------------|---------|
| **Unicast** | One-to-one communication; a single sender transmits to a single receiver | `sendto(data, ("172.20.0.10", 8080))` |
| **Broadcast** | One-to-all communication; a single sender transmits to all hosts in a Layer 2 domain | `sendto(data, ("255.255.255.255", 5007))` |
| **Multicast** | One-to-many communication; a single sender transmits to a group of interested receivers | `sendto(data, ("239.1.1.1", 5008))` |
| **Anycast** | One-to-nearest; multiple hosts share an address, packets go to the closest one | Used by DNS root servers, CDNs |

---

## Broadcast-Specific Terms

| Term | Definition | Example |
|------|------------|---------|
| **Limited Broadcast** | Address 255.255.255.255; never forwarded by routers | `sendto(data, ("255.255.255.255", port))` |
| **Directed Broadcast** | Subnet-specific broadcast (e.g., 172.20.0.255 for /24); may be forwarded | `sendto(data, ("172.20.0.255", port))` |
| **Broadcast Domain** | The set of hosts that receive the same broadcast traffic; typically bounded by routers/VLANs | All containers on `week3_network` |
| **SO_BROADCAST** | Socket option that permits sending to broadcast addresses | `sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)` |

---

## Multicast-Specific Terms

| Term | Definition | Example |
|------|------------|---------|
| **Multicast Group** | A logical group identified by a Class D IP address (224.0.0.0–239.255.255.255) | `239.1.1.1` |
| **IGMP** | Internet Group Management Protocol; used by hosts to report multicast group membership to routers | IGMPv2 Membership Report |
| **Group Join** | The act of subscribing to a multicast group via IGMP | `IP_ADD_MEMBERSHIP` socket option |
| **Group Leave** | The act of unsubscribing from a multicast group | `IP_DROP_MEMBERSHIP` socket option |
| **Multicast TTL** | Time To Live for multicast packets; controls hop distance | `IP_MULTICAST_TTL` (1 = link-local) |
| **Multicast Loopback** | Whether a sender receives its own multicast messages | `IP_MULTICAST_LOOP` (0 or 1) |
| **Administratively Scoped** | Multicast range 239.0.0.0/8 reserved for private/local use | Similar to 10.x.x.x for unicast |

### IGMP Message Types

| Type | Purpose |
|------|---------|
| **Membership Query** | Router asks "Who wants this group?" |
| **Membership Report** | Host says "I want group X" |
| **Leave Group** | Host says "I no longer want group X" (IGMPv2+) |

---

## TCP Tunnel Terms

| Term | Definition | Example |
|------|------------|---------|
| **TCP Tunnel** | A relay that accepts TCP connections and forwards traffic to another destination | Router listening on 9090, forwarding to server:8080 |
| **Port Forwarding** | Redirecting traffic from one port to another (same or different host) | `localhost:9090 → server:8080` |
| **Proxy** | An intermediary that handles requests on behalf of clients | The tunnel acts as a proxy |
| **Relay** | A component that receives data and retransmits it | Tunnel relays bytes bidirectionally |
| **Bidirectional Forwarding** | Data flows in both directions through the tunnel | Client↔Router and Router↔Server |

---

## Socket Options Reference

### SOL_SOCKET Level

| Option | Purpose | Values |
|--------|---------|--------|
| `SO_BROADCAST` | Permit broadcast sends | 0 (off), 1 (on) |
| `SO_REUSEADDR` | Allow reuse of local address immediately after close | 0 (off), 1 (on) |
| `SO_REUSEPORT` | Allow multiple sockets to bind to the same port | 0 (off), 1 (on) |
| `SO_RCVBUF` | Receive buffer size in bytes | Integer |
| `SO_SNDBUF` | Send buffer size in bytes | Integer |

### IPPROTO_IP Level (Multicast)

| Option | Purpose | Values |
|--------|---------|--------|
| `IP_ADD_MEMBERSHIP` | Join a multicast group | `struct ip_mreq` |
| `IP_DROP_MEMBERSHIP` | Leave a multicast group | `struct ip_mreq` |
| `IP_MULTICAST_IF` | Set outgoing interface for multicast | Interface IP address |
| `IP_MULTICAST_TTL` | Set TTL for outgoing multicast | 1–255 (1 = link-local) |
| `IP_MULTICAST_LOOP` | Receive own multicast messages | 0 (off), 1 (on) |

---

## Address Ranges

### Multicast Address Ranges (IPv4)

| Range | Name | Scope |
|-------|------|-------|
| 224.0.0.0/24 | Link-Local | Same subnet only; TTL=1 |
| 224.0.1.0–224.0.1.255 | Internetwork Control | Global |
| 224.0.2.0–224.0.255.255 | AD-HOC | Various protocols |
| 232.0.0.0/8 | Source-Specific Multicast (SSM) | Requires source specification |
| 233.0.0.0/8 | GLOP | Autonomous System based |
| 239.0.0.0/8 | Administratively Scoped | Private/organisation use |

### Well-Known Multicast Addresses

| Address | Protocol |
|---------|----------|
| 224.0.0.1 | All hosts on segment |
| 224.0.0.2 | All multicast routers |
| 224.0.0.5 | OSPF routers |
| 224.0.0.6 | OSPF designated routers |
| 224.0.0.9 | RIPv2 routers |
| 224.0.0.251 | mDNS |

---

## Commands Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `ip maddr show` | List multicast group memberships | `ip maddr show dev eth0` |
| `netstat -g` | Show multicast group memberships (older) | `netstat -gn` |
| `tcpdump igmp` | Capture IGMP messages | `tcpdump -i eth0 igmp` |
| `tcpdump udp port X` | Capture UDP on specific port | `tcpdump -i eth0 udp port 5007` |
| `ss -tn` | Show TCP connections | `ss -tn state established` |
| `ss -un` | Show UDP sockets | `ss -uln` |

---

## Python Socket Snippets

### Enable Broadcast
```python
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
```

### Join Multicast Group
```python
import struct
mreq = socket.inet_aton(group_ip) + struct.pack('=I', socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
```

### Set Multicast TTL
```python
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 4)
```

### Leave Multicast Group
```python
sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
```

---

## Acronyms

| Acronym | Full Form | Context |
|---------|-----------|---------|
| IGMP | Internet Group Management Protocol | Multicast group membership |
| TTL | Time To Live | Hop count limit |
| MTU | Maximum Transmission Unit | Largest packet size |
| CIDR | Classless Inter-Domain Routing | IP addressing notation |
| L2 | Layer 2 (Data Link) | Ethernet frames, MAC addresses |
| L3 | Layer 3 (Network) | IP packets, IP addresses |
| SSM | Source-Specific Multicast | Multicast variant |
| NIC | Network Interface Card | Hardware network adapter |

---

## Relationships Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    COMMUNICATION PARADIGMS                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   UNICAST                BROADCAST              MULTICAST           │
│   ────────               ─────────              ─────────           │
│   1 sender               1 sender               1 sender            │
│   1 receiver             ALL receivers          GROUP members       │
│                          (L2 domain)            (IGMP joined)       │
│                                                                     │
│   No special             SO_BROADCAST           IP_ADD_MEMBERSHIP   │
│   options                required               required            │
│                                                                     │
│   TCP or UDP             UDP only               UDP (typically)     │
│                          (no TCP broadcast)                         │
│                                                                     │
│   Crosses routers        NEVER crosses          Crosses routers     │
│                          routers                (with config)       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                       TCP TUNNEL PATTERN                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   [Client] ──TCP #1──► [Tunnel] ──TCP #2──► [Server]                │
│                           │                                         │
│                     Terminates #1                                   │
│                     Creates #2                                      │
│                     Relays data                                     │
│                                                                     │
│   Connection count: 2 (not 1!)                                      │
│   Server sees: Tunnel's IP (not Client's)                           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

*Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim*
