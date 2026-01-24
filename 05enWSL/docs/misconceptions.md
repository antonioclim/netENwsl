# Common Misconceptions — Week 5

> Computer Networks Laboratory — ASE-CSIE Bucharest
>
> IP Addressing, Subnetting and VLSM

---

## Misconception 0: "Routers work at Layer 2 because they forward frames"
{#misconception-0}

**WRONG:** "Routers receive frames and send frames, so they must be Layer 2 devices."

**CORRECT:** Routers operate at **Layer 3 (Network Layer)** because they make forwarding decisions based on **IP addresses**, not MAC addresses.

| Device | Layer | Decision Basis |
|--------|-------|----------------|
| Switch | Layer 2 | MAC addresses |
| Router | Layer 3 | IP addresses |

---

## Misconception 1: "A /24 network has 256 usable host addresses"
{#misconception-1}

**WRONG:** "Since 2^8 = 256, a /24 gives me 256 devices."

**CORRECT:** A /24 has 256 total addresses, but only **254 usable** for hosts.

**Formula:** Usable hosts = 2^(32 - prefix) - 2

---

## Misconception 2: "The network address can be assigned to a server"
{#misconception-2}

**CORRECT:** The network address (all host bits = 0) is **RESERVED** and cannot be assigned to any device.

---

## Misconception 3: "Subnet boundaries always fall on octet boundaries"
{#misconception-3}

**CORRECT:** Subnet boundaries are determined by the prefix length, not octet positions.

Example: 172.16.45.67/20 → Network address is **172.16.32.0**, NOT 172.16.45.0

---

## Misconception 4: "Broadcast address is always x.x.x.255"
{#misconception-4}

**CORRECT:** Broadcast address = Network address + Block size - 1

| Network | Broadcast |
|---------|-----------|
| 192.168.1.0/24 | 192.168.1.255 |
| 192.168.1.64/26 | 192.168.1.127 |

---

## Misconception 5: "FLSM and VLSM produce the same number of usable addresses"
{#misconception-5}

**CORRECT:** VLSM typically provides **higher efficiency** because it matches allocation to actual needs.

---

## Misconception 6: "VLSM can allocate subnets in any order"
{#misconception-6}

**CORRECT:** VLSM **MUST** allocate largest subnets first to prevent fragmentation.

---

## Misconception 7: "Point-to-point links need a /30 subnet"
{#misconception-7}

**CORRECT:** While /30 is traditional, /31 is now supported per RFC 3021.

---

## Misconception 8: "Multiple :: can appear in an IPv6 address"
{#misconception-8}

**CORRECT:** The :: notation can appear **only ONCE** per address (RFC 5952).

---

## Misconception 9: "IPv6 eliminates the need for NAT"
{#misconception-9}

**CORRECT:** IPv6 makes NAT **unnecessary** for address conservation, but NAT66 exists for policy reasons.

---

## Misconception 10: "Link-local addresses (fe80::) can be routed"
{#misconception-10}

**CORRECT:** Link-local addresses are **NEVER routed** beyond the local network segment.

---

*Week 5: IP Addressing, Subnetting and VLSM — Misconceptions Guide*
*Computer Networks Laboratory — ASE-CSIE Bucharest*
