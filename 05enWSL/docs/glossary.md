# 📖 Glossary — Week 5: IP Addressing, Subnetting, VLSM
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Core IPv4 Terms

| Term | Definition | Example |
|------|------------|---------|
| **IP Address** | 32-bit logical identifier for a network interface | `192.168.1.100` |
| **Octet** | One of four 8-bit segments in an IPv4 address | `192` in `192.168.1.1` |
| **Dotted-decimal notation** | Standard format: four decimal octets separated by dots | `10.0.0.1` |
| **Binary representation** | IP address shown as 32 bits | `11000000.10101000.00000001.00000001` |

---

## CIDR and Masking Terms

| Term | Definition | Example |
|------|------------|---------|
| **CIDR** | Classless Inter-Domain Routing; notation using /prefix | `192.168.0.0/24` |
| **Prefix length** | Number of bits in the network portion | `/24` means 24 network bits |
| **Subnet mask** | 32-bit mask with 1s for network bits, 0s for host bits | `255.255.255.0` for /24 |
| **Wildcard mask** | Inverse of subnet mask; used in ACLs | `0.0.0.255` for /24 |
| **Network portion** | Bits identifying the network | First 24 bits in /24 |
| **Host portion** | Bits identifying the host within the network | Last 8 bits in /24 |

---

## Address Types

| Term | Definition | Example |
|------|------------|---------|
| **Network address** | First address in subnet; all host bits = 0 | `192.168.1.0` in /24 |
| **Broadcast address** | Last address in subnet; all host bits = 1 | `192.168.1.255` in /24 |
| **Host address** | Any address between network and broadcast | `192.168.1.1` to `.254` |
| **Gateway address** | Router interface address; typically first host | `192.168.1.1` |
| **Usable host range** | Addresses assignable to devices | `.1` to `.254` in /24 |

---

## Private and Special Addresses

| Term | Definition | Range |
|------|------------|-------|
| **Private address** | Non-routable addresses for internal use (RFC 1918) | `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` |
| **Public address** | Globally routable Internet addresses | All others (assigned by RIRs) |
| **Loopback address** | Address for local host testing | `127.0.0.0/8` (typically `127.0.0.1`) |
| **APIPA** | Automatic Private IP Addressing; self-assigned when DHCP fails | `169.254.0.0/16` |

---

## Subnetting Terms

| Term | Definition | Example |
|------|------------|---------|
| **Subnetting** | Dividing a network into smaller segments | Split /24 into four /26 networks |
| **FLSM** | Fixed Length Subnet Mask; all subnets same size | Four /26 subnets from /24 |
| **VLSM** | Variable Length Subnet Mask; subnets of different sizes | /25, /26, /28 from same block |
| **Supernetting** | Combining multiple networks into one larger block | Four /24 networks → one /22 |
| **Block size** | Number of addresses in a subnet | 64 addresses for /26 |
| **Subnet boundary** | Starting address of a subnet (must align to block size) | /26 starts at .0, .64, .128, .192 |

---

## IPv6 Terms

| Term | Definition | Example |
|------|------------|---------|
| **IPv6 address** | 128-bit identifier in hexadecimal colon notation | `2001:db8::1` |
| **Hextet** | One 16-bit group (4 hex digits) in IPv6 | `db8` in `2001:db8::1` |
| **Full form** | All 8 groups with leading zeros | `2001:0db8:0000:0000:0000:0000:0000:0001` |
| **Compressed form** | Shortened notation removing zeros | `2001:db8::1` |
| **:: notation** | Represents one or more consecutive all-zero groups | `::1` = `0:0:0:0:0:0:0:1` |

---

## IPv6 Address Types

| Term | Definition | Prefix |
|------|------------|--------|
| **Global unicast** | Routable Internet addresses | `2000::/3` |
| **Link-local** | Single-segment addresses; auto-configured | `fe80::/10` |
| **Unique local** | Private addresses (like RFC 1918) | `fc00::/7` |
| **Multicast** | One-to-many communication | `ff00::/8` |
| **Loopback** | Local host (equivalent to 127.0.0.1) | `::1` |
| **Unspecified** | No address assigned yet | `::` |

---

## IPv6 Subnetting Terms

| Term | Definition | Example |
|------|------------|---------|
| **Global routing prefix** | Network portion assigned by ISP | First 48 bits typically |
| **Subnet ID** | Organisation's internal subnet identifier | Bits 49-64 typically |
| **Interface ID** | Host identifier (last 64 bits) | Generated from MAC or random |
| **SLAAC** | Stateless Address Autoconfiguration | Host generates own address |
| **/64 subnet** | Standard LAN subnet size | 2^64 possible addresses |
| **/48 allocation** | Typical organisation assignment | 65,536 possible /64 subnets |

---

## Calculation Terms

| Term | Definition | Formula |
|------|------------|---------|
| **Total addresses** | All addresses in a subnet | 2^(32 - prefix) |
| **Usable hosts** | Addresses assignable to devices | 2^(32 - prefix) - 2 |
| **Bits to borrow** | Extra bits needed for subnetting | ceil(log₂(subnets needed)) |
| **Host bits** | Bits remaining for host addressing | 32 - prefix |
| **Efficiency** | Percentage of addresses actually used | (required / usable) × 100 |

---

## Commands Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `analyse` | Examine CIDR address details | `python ex_5_01_cidr_flsm.py analyse 10.0.0.1/24` |
| `flsm` | Split network into equal subnets | `python ex_5_01_cidr_flsm.py flsm 10.0.0.0/24 4` |
| `vlsm` | Allocate variable-sized subnets | `python ex_5_02_vlsm_ipv6.py vlsm 10.0.0.0/24 50 20 10` |
| `binary` | Show binary representation | `python ex_5_01_cidr_flsm.py binary 192.168.1.1` |
| `ipv6` | Compress IPv6 address | `python ex_5_02_vlsm_ipv6.py ipv6 2001:db8::1` |
| `ipv6-expand` | Expand IPv6 to full form | `python ex_5_02_vlsm_ipv6.py ipv6-expand 2001:db8::1` |
| `ipv6-subnets` | Generate IPv6 subnets | `python ex_5_02_vlsm_ipv6.py ipv6-subnets 2001:db8::/48 64 10` |

---

## Acronyms

| Acronym | Full Form | Context |
|---------|-----------|---------|
| CIDR | Classless Inter-Domain Routing | Modern addressing notation |
| FLSM | Fixed Length Subnet Mask | Equal-sized subnetting |
| VLSM | Variable Length Subnet Mask | Variable-sized subnetting |
| NAT | Network Address Translation | IPv4 address conservation |
| SLAAC | Stateless Address Autoconfiguration | IPv6 auto-addressing |
| EUI-64 | Extended Unique Identifier 64-bit | IPv6 interface ID from MAC |
| RIR | Regional Internet Registry | IP address allocation bodies |
| RFC | Request for Comments | Internet standards documents |

---

## Relationships Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        IPv4 Address                             │
│                     192.168.100.50/26                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────────┐  ┌─────────────────────────────┐  │
│   │    Network Portion      │  │      Host Portion           │  │
│   │    (26 bits)            │  │      (6 bits)               │  │
│   │    192.168.100.0        │  │      .50                    │  │
│   └─────────────────────────┘  └─────────────────────────────┘  │
│              │                              │                   │
│              ▼                              ▼                   │
│   ┌─────────────────────────┐  ┌─────────────────────────────┐  │
│   │   Subnet Mask           │  │   Wildcard Mask             │  │
│   │   255.255.255.192       │  │   0.0.0.63                  │  │
│   └─────────────────────────┘  └─────────────────────────────┘  │
│                                                                 │
│   Derived Addresses:                                            │
│   • Network:    192.168.100.0    (all host bits = 0)           │
│   • Broadcast:  192.168.100.63   (all host bits = 1)           │
│   • First host: 192.168.100.1                                   │
│   • Last host:  192.168.100.62                                  │
│   • Usable:     62 hosts (2^6 - 2)                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Conversion Table

| Prefix | Mask | Hosts | Block Size |
|--------|------|-------|------------|
| /24 | 255.255.255.0 | 254 | 256 |
| /25 | 255.255.255.128 | 126 | 128 |
| /26 | 255.255.255.192 | 62 | 64 |
| /27 | 255.255.255.224 | 30 | 32 |
| /28 | 255.255.255.240 | 14 | 16 |
| /29 | 255.255.255.248 | 6 | 8 |
| /30 | 255.255.255.252 | 2 | 4 |
| /31 | 255.255.255.254 | 2* | 2 |
| /32 | 255.255.255.255 | 1 | 1 |

*RFC 3021 point-to-point

---

*Week 5: IP Addressing, Subnetting, VLSM — Glossary*
*Computer Networks Laboratory — ASE, CSIE Bucharest*
