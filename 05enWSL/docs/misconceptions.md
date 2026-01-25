# Common Misconceptions — Week 5

> Computer Networks Laboratory — ASE-CSIE Bucharest
>
> IP Addressing, Subnetting and VLSM

This document addresses the mistakes I see most often when marking coursework. In previous cohorts, roughly 60% of students made at least one of these errors in their first subnet design attempt.

---


> 📊 **Related diagram:** See `docs/images/osi_network_layer.svg` for visual reference.

## Misconception 0: "Routers work at Layer 2 because they forward frames"
{#misconception-0}

**WRONG:** "Routers receive frames and send frames, so they must be Layer 2 devices."

**CORRECT:** Routers operate at **Layer 3 (Network Layer)** because they make forwarding decisions based on **IP addresses**, not MAC addresses. Yes, routers must decapsulate frames to read the IP header, but the routing decision itself uses Layer 3 information.

| Device | Layer | Decision Basis |
|--------|-------|----------------|
| Switch | Layer 2 | MAC addresses |
| Router | Layer 3 | IP addresses |

**Why this matters:** If you configure a switch expecting it to route between subnets, nothing will work. Routing requires Layer 3 intelligence.

**Verify:**
```bash
# Routers have IP addresses on interfaces, switches typically don't
ip addr show
```

---

## Misconception 1: "A /24 network has 256 usable host addresses"
{#misconception-1}

**WRONG:** "Since 2^8 = 256, a /24 gives me 256 devices."

**CORRECT:** A /24 has 256 total addresses, but only **254 usable** for hosts.

**Formula:** Usable hosts = 2^(32 - prefix) - 2

The two reserved addresses are:
- **Network address** (all host bits = 0): identifies the network itself
- **Broadcast address** (all host bits = 1): reaches all hosts on the network

**Binary view for 192.168.1.0/24:**
```
Network:   11000000.10101000.00000001.00000000  (192.168.1.0)
Broadcast: 11000000.10101000.00000001.11111111  (192.168.1.255)
```

**Verify:**
```bash
python3 -c "print(f'Total: {2**8}, Usable: {2**8 - 2}')"
# Output: Total: 256, Usable: 254
```

---

## Misconception 2: "The network address can be assigned to a server"
{#misconception-2}

**WRONG:** "I'll assign 192.168.1.0 to my web server."

**CORRECT:** The network address (all host bits = 0) is **RESERVED** and cannot be assigned to any device. Operating systems will reject this configuration.

**Why it fails:** The network address identifies the network itself in routing tables. Assigning it to a host creates ambiguity — is this packet destined for the entire network or one specific host?

**Verify:**
```bash
# This should fail
sudo ip addr add 192.168.1.0/24 dev eth0
# Error: Invalid prefix for a host address
```

---

## Misconception 3: "Subnet boundaries always fall on octet boundaries"
{#misconception-3}

**WRONG:** "172.16.45.67/20 has network address 172.16.45.0"

**CORRECT:** Subnet boundaries are determined by the prefix length, not octet positions.

**Binary calculation for 172.16.45.67/20:**
```
IP:        10101100.00010000.00101101.01000011  (172.16.45.67)
Mask /20:  11111111.11111111.11110000.00000000
                                ↑
                         Boundary within 3rd octet!

Network:   10101100.00010000.00100000.00000000  (172.16.32.0)
```

The third octet (45 = 00101101) becomes 32 (00100000) when the last 4 bits are zeroed.

**Verify:**
```bash
python3 src/exercises/ex_5_01_cidr_flsm.py analyse 172.16.45.67/20
# Network: 172.16.32.0/20
```

---

## Misconception 4: "Broadcast address is always x.x.x.255"
{#misconception-4}

**WRONG:** "The broadcast for 192.168.1.64/26 is 192.168.1.255"

**CORRECT:** Broadcast address = Network address + Block size - 1

For /26: Block size = 2^6 = 64

| Network | Block | Broadcast |
|---------|-------|-----------|
| 192.168.1.0/24 | 256 | 192.168.1.255 |
| 192.168.1.64/26 | 64 | 192.168.1.127 |
| 192.168.1.64/27 | 32 | 192.168.1.95 |

**Binary for 192.168.1.64/26:**
```
Network:   11000000.10101000.00000001.01000000  (192.168.1.64)
Broadcast: 11000000.10101000.00000001.01111111  (192.168.1.127)
                                      ↑↑↑↑↑↑
                                 Host bits all 1s
```

**Verify:**
```bash
python3 -c "print(64 + 64 - 1)"
# Output: 127
```

---

## Misconception 5: "FLSM and VLSM produce the same number of usable addresses"
{#misconception-5}

**WRONG:** "It doesn't matter which method I use — same addresses either way."

**CORRECT:** VLSM typically provides **higher efficiency** because it matches allocation to actual needs.

**Example:** Allocate for departments needing 100, 50, 20 and 2 hosts from 10.0.0.0/24

| Method | Allocation | Wasted |
|--------|-----------|--------|
| FLSM (/26 each) | 4 × 62 = 248 | 248 - 172 = 76 (31%) |
| VLSM | /25 + /26 + /27 + /30 = 126+62+30+2 = 220 | 220 - 172 = 48 (22%) |

---

## Misconception 6: "VLSM can allocate subnets in any order"
{#misconception-6}

**WRONG:** "I'll allocate small subnets first, then big ones."

**CORRECT:** VLSM **MUST** allocate largest subnets first to prevent fragmentation and ensure proper block alignment.

**Why largest first:** Larger blocks need alignment to power-of-2 boundaries. A /25 block must start at .0 or .128. If you allocate small blocks first, you may fragment the space and leave no valid starting point for larger blocks.

**Correct order for 100, 50, 20, 2 hosts:**
1. 100 hosts → /25 (needs 128 addresses)
2. 50 hosts → /26 (needs 64 addresses)
3. 20 hosts → /27 (needs 32 addresses)
4. 2 hosts → /30 (needs 4 addresses)

---

## Misconception 7: "Point-to-point links need a /30 subnet"
{#misconception-7}

**WRONG:** "/30 is the only option for router-to-router links."

**CORRECT:** While /30 is traditional (2 usable addresses), /31 is now supported per **RFC 3021** for point-to-point links.

| Prefix | Usable | Use case |
|--------|--------|----------|
| /30 | 2 | Traditional P2P |
| /31 | 2 | Modern P2P (no broadcast) |

**Why /31 works:** Point-to-point links don't need broadcast (there's no "all hosts" — just two endpoints), so both addresses can be assigned.

---

## Misconception 8: "Multiple :: can appear in an IPv6 address"
{#misconception-8}

**WRONG:** "2001:db8::85a3::7334 is valid — each :: replaces some zeros."

**CORRECT:** The :: notation can appear **only ONCE** per address (RFC 5952).

**Why only once:** If :: appeared twice, the parser cannot determine how many zero groups each represents. Example: does `a::b::c` expand to 2 zeros + 4 zeros, or 3 zeros + 3 zeros, or...?

**Valid compressions of 2001:0db8:0000:0000:0000:85a3:0000:7334:**
- `2001:db8::85a3:0:7334` (:: for middle three zero groups)
- `2001:db8:0:0:0:85a3::7334` (:: for last zero group)

**Invalid:** `2001:db8::85a3::7334`

---

## Misconception 9: "IPv6 eliminates the need for NAT"
{#misconception-9}

**WRONG:** "With IPv6, NAT completely disappears."

**CORRECT:** IPv6 makes NAT **unnecessary** for address conservation, but NAT66 exists for policy reasons (security policies, network migration, etc.).

The vast IPv6 address space (2^128) means every device can have a globally routable address. However, some organisations still prefer NAT for consistent addressing or to hide internal structure.

---

## Misconception 10: "Link-local addresses (fe80::) can be routed"
{#misconception-10}

**WRONG:** "I can reach fe80::1 on the other side of the router."

**CORRECT:** Link-local addresses are **NEVER routed** beyond the local network segment. They're valid only within a single broadcast domain.

**Use cases for link-local:**
- Router discovery
- Neighbour discovery
- DHCPv6 communication
- Automatic address configuration before getting a global address

---

## Summary Table

| # | Misconception | Reality |
|---|---------------|---------|
| 0 | Routers are L2 | Routers use L3 (IP) for decisions |
| 1 | /24 = 256 hosts | /24 = 254 usable hosts |
| 2 | Network addr assignable | Network addr is reserved |
| 3 | Boundaries on octets | Boundaries on prefix length |
| 4 | Broadcast = .255 | Broadcast = network + block - 1 |
| 5 | FLSM = VLSM efficiency | VLSM is more efficient |
| 6 | VLSM any order | VLSM largest first |
| 7 | P2P needs /30 | /31 works per RFC 3021 |
| 8 | Multiple :: in IPv6 | Only one :: allowed |
| 9 | IPv6 = no NAT | NAT66 exists for policy |
| 10 | fe80:: routable | Link-local never routed |

---

*Week 5: IP Addressing, Subnetting and VLSM — Misconceptions Guide*
*Computer Networks Laboratory — ASE-CSIE Bucharest*
