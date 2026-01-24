# 🗳️ Peer Instruction Questions — Week 5
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> IP Addressing, Subnetting and VLSM

---

## Peer Instruction Protocol (5 steps)

Each question follows **5 mandatory steps**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 1 (1 min)  │  Read the question and think individually               │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 2 (30 sec) │  Vote your answer (A/B/C/D) — no discussion!            │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 3 (2 min)  │  Discuss with your neighbour — convince them!           │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 4 (30 sec) │  Re-vote — you may change your answer                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 5 (2 min)  │  Instructor explains the correct answer                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Question 1: Usable Hosts in a /26 Network

> 💭 **PREDICTION:** Before looking at the options, calculate mentally: how many usable host addresses exist in a /26 network?

### Scenario

A network administrator receives the address block `192.168.10.0/26` for a new department.

### Question

How many devices can be assigned IP addresses from this block?

### Options

- **A)** 64 devices — *[Misconception: counting total addresses, forgetting network and broadcast]*
- **B)** 62 devices — **[CORRECT]**
- **C)** 63 devices — *[Misconception: subtracting only broadcast OR only network address]*
- **D)** 26 devices — *[Misconception: confusing prefix length with host count]*

### Correct Answer

**B) 62 devices**

**Explanation:** A /26 prefix means 26 bits for network, leaving 6 bits for hosts. Total addresses = 2^6 = 64. However, two addresses are reserved: the network address (all host bits = 0) and the broadcast address (all host bits = 1). Therefore: 64 - 2 = 62 usable host addresses.

### Targeted Misconception

Students often forget to subtract the network and broadcast addresses, or they confuse the prefix number with the number of hosts.

### Instructor Notes

- **Target accuracy:** 50-70% on first vote
- **Key concept:** Usable hosts = 2^(32-prefix) - 2
- **After discussion:** Show binary representation of network (all zeros) and broadcast (all ones)
- **Visual aid:** Draw the 64 addresses with first and last marked as reserved
- **Timing:** Present (1 min) → Vote (30 sec) → Discuss (2 min) → Revote (30 sec) → Explain (2 min)

---

## Question 2: Identifying the Network Address

> 💭 **PREDICTION:** Given an IP with prefix, how do you find which address represents the network itself?

### Scenario

A technician runs the following command:

```bash
$ python ex_5_01_cidr_flsm.py analyse 172.16.45.67/20
```

### Question

What is the network address for this interface?

### Options

- **A)** 172.16.45.0 — *[Misconception: assuming /24 boundary, zeroing only last octet]*
- **B)** 172.16.32.0 — **[CORRECT]**
- **C)** 172.16.0.0 — *[Misconception: assuming /16 boundary]*
- **D)** 172.16.45.64 — *[Misconception: rounding to nearest power of 2]*

### Correct Answer

**B) 172.16.32.0**

**Explanation:** With /20, the network portion uses 20 bits (first two octets + first 4 bits of third octet). In binary:
- 172.16.45.67 = 172.16.00101101.01000011
- Mask /20 means keeping first 20 bits: 172.16.00100000.00000000
- Result: 172.16.32.0

The third octet (45 = 00101101) becomes 32 (00100000) when the last 4 bits are zeroed.

### Targeted Misconception

Students assume subnet boundaries always fall on octet boundaries (/8, /16, /24). They forget that /20 splits within the third octet.

### Instructor Notes

- **Target accuracy:** 30-50% on first vote (harder question)
- **Key concept:** Network address = IP AND subnet mask (bitwise)
- **After discussion:** Work through binary conversion step by step
- **Common error:** Point out that 45 does NOT simply become 0 or 45
- **Timing:** Present (1 min) → Vote (30 sec) → Discuss (3 min) → Revote (30 sec) → Explain (3 min)

---

## Question 3: VLSM Allocation Order

> 💭 **PREDICTION:** When doing VLSM, why does the order of requirements matter?

### Scenario

You need to allocate subnets from `10.0.0.0/24` for these requirements:
- Department A: 50 hosts
- Department B: 10 hosts  
- Department C: 100 hosts
- Department D: 5 hosts

### Question

In what order should VLSM allocate these subnets?

### Options

- **A)** A, B, C, D (as listed) — *[Misconception: process in given order]*
- **B)** D, B, A, C (smallest first) — *[Misconception: smallest first saves space]*
- **C)** C, A, B, D (largest first) — **[CORRECT]**
- **D)** Order does not matter — *[Misconception: any order works]*

### Correct Answer

**C) C, A, B, D (largest first)**

**Explanation:** VLSM allocates largest requirements first because larger subnets need alignment to larger block boundaries. If we allocate small subnets first, we might fragment the address space and leave no contiguous block large enough for bigger subnets.

Example with largest-first:
- C (100 hosts) → needs /25 (128 addresses) → 10.0.0.0/25
- A (50 hosts) → needs /26 (64 addresses) → 10.0.0.128/26
- B (10 hosts) → needs /28 (16 addresses) → 10.0.0.192/28
- D (5 hosts) → needs /29 (8 addresses) → 10.0.0.208/29

### Targeted Misconception

Students think that allocating smaller subnets first might "save space" or that order is irrelevant. They do not understand block alignment requirements.

### Instructor Notes

- **Target accuracy:** 40-60% on first vote
- **Key concept:** Larger blocks need alignment to power-of-2 boundaries
- **After discussion:** Show what happens if you try smallest-first (fragmentation)
- **Demonstrate:** Use the VLSM tool to show both orderings
- **Timing:** Present (1 min) → Vote (30 sec) → Discuss (2 min) → Revote (30 sec) → Explain (2 min)

---

## Question 4: IPv6 Address Compression

> 💭 **PREDICTION:** How many times can you use :: in a single IPv6 address?

### Scenario

A student writes the following IPv6 address:

```
2001:0db8::85a3::7334
```

### Question

Is this IPv6 address valid?

### Options

- **A)** Yes, it correctly compresses two separate groups of zeros — *[Misconception: :: can be used multiple times]*
- **B)** No, :: can only appear once per address — **[CORRECT]**
- **C)** Yes, but it should be written as 2001:db8::85a3::7334 — *[Misconception: leading zero removal fixes it]*
- **D)** No, because 85a3 is not a valid hexadecimal group — *[Misconception: misunderstanding hex]*

### Correct Answer

**B) No, :: can only appear once per address**

**Explanation:** The :: notation replaces one or more consecutive groups of all zeros. If :: appeared twice, the parser could not determine how many zero groups each :: represents. For example, `2001:db8::85a3::7334` could expand to multiple different addresses.

Valid compressions of `2001:0db8:0000:0000:0000:85a3:0000:7334`:
- `2001:db8::85a3:0:7334` (using :: for the three middle zero groups)
- `2001:db8:0:0:0:85a3::7334` (using :: for the last zero group)

But never both :: in the same address.

### Targeted Misconception

Students believe :: simply means "zeros here" and can be used wherever zeros appear. They do not realise it creates ambiguity.

### Instructor Notes

- **Target accuracy:** 50-70% on first vote
- **Key concept:** :: is ambiguous if used twice
- **After discussion:** Ask students to expand `a::b::c` — how many zeros in each?
- **Tool demo:** Show `ipv6-expand` with valid and invalid inputs
- **Timing:** Present (1 min) → Vote (30 sec) → Discuss (2 min) → Revote (30 sec) → Explain (2 min)

---

## Question 5: Broadcast Address Calculation

> 💭 **PREDICTION:** The broadcast address is NOT always .255 — when is it different?

### Scenario

Given the network `192.168.1.64/27`, a student needs to find the broadcast address.

### Question

What is the broadcast address for this network?

### Options

- **A)** 192.168.1.255 — *[Misconception: broadcast is always .255]*
- **B)** 192.168.1.95 — **[CORRECT]**
- **C)** 192.168.1.127 — *[Misconception: next power of 2 minus 1]*
- **D)** 192.168.1.64 — *[Misconception: confusing network with broadcast]*

### Correct Answer

**B) 192.168.1.95**

**Explanation:** 
- /27 means 5 host bits (32 - 27 = 5)
- Block size = 2^5 = 32 addresses
- Network starts at .64, so it spans .64 to .64 + 32 - 1 = .95
- Network address: 192.168.1.64 (first)
- Broadcast address: 192.168.1.95 (last)
- Usable range: .65 to .94

The broadcast is the network address + block size - 1, or equivalently, set all host bits to 1.

### Targeted Misconception

Students memorise that broadcast "ends in .255" from /24 examples. They do not generalise the rule: broadcast = all host bits set to 1.

### Instructor Notes

- **Target accuracy:** 40-60% on first vote
- **Key concept:** Broadcast = network address + 2^(32-prefix) - 1
- **After discussion:** Show binary: 64 = 01000000, broadcast = 01011111 = 95
- **Pattern recognition:** For /27, blocks are 0, 32, 64, 96, 128... broadcasts are 31, 63, 95, 127...
- **Timing:** Present (1 min) → Vote (30 sec) → Discuss (2 min) → Revote (30 sec) → Explain (2 min)

---

## Quick Reference: Question Timing

| Question | Topic | Difficulty | First Vote Target |
|----------|-------|------------|-------------------|
| Q1 | Usable hosts /26 | Easy | 50-70% |
| Q2 | Network address /20 | Hard | 30-50% |
| Q3 | VLSM ordering | Medium | 40-60% |
| Q4 | IPv6 compression :: | Medium | 50-70% |
| Q5 | Broadcast address | Medium | 40-60% |

**Total time for all 5 questions:** ~35-40 minutes

---

*Week 5: IP Addressing, Subnetting, VLSM — Peer Instruction Questions*
*Computer Networks Laboratory — ASE, CSIE Bucharest*
