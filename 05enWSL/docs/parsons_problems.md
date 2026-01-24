# Parsons Problems — Week 5

> Computer Networks Laboratory — ASE-CSIE Bucharest
>
> IP Addressing, Subnetting and VLSM

Parsons problems are code/command block reordering exercises with **distractors** (incorrect options).

---

## Problems Overview

| Problem | Topic | LO | Difficulty | Distractors |
|---------|-------|----|-----------:|------------:|
| P1 | Usable hosts calculation | LO3 | Basic | 3 |
| P2 | VLSM allocation steps | LO5 | Intermediate | 3 |
| P3 | IPv6 compression | LO2 | Intermediate | 3 |
| P4 | Network address | LO3 | Basic | 3 |
| P5 | Lab environment setup | LO1 | Basic | 3 |

**Machine-readable version:** `formative/parsons/problems.json`

---

## P1: Calculate Usable Hosts from CIDR

**LO:** LO3 | **Difficulty:** Basic

Arrange blocks to create a function calculating usable hosts. Distractors include wrong subtraction order and forgetting to subtract 2.

```python
# Correct solution:
def usable_hosts(prefix: int) -> int:
    host_bits = 32 - prefix
    total_addresses = 2 ** host_bits
    return total_addresses - 2
```

---

## P2: VLSM Allocation Algorithm

**LO:** LO5 | **Difficulty:** Intermediate

VLSM requires largest-first sorting to prevent fragmentation.

---

## P3: IPv6 Address Compression

**LO:** LO2 | **Difficulty:** Intermediate

IPv6 compression follows RFC 5952: remove leading zeros, find longest consecutive zero run, replace with :: (only once).

---

## P4: Network Address Calculation

**LO:** LO3 | **Difficulty:** Basic

Use ipaddress module to parse interface and extract network_address.

---

## P5: Start Week 5 Lab Environment

**LO:** LO1 | **Difficulty:** Basic

Navigate → Start Docker → Verify → Start Lab → Check containers.

---

*Week 5: IP Addressing, Subnetting and VLSM — Parsons Problems*
*Computer Networks Laboratory — ASE-CSIE Bucharest*
