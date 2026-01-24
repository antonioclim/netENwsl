# 🔍 Code Tracing Exercises — Week 5
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> IP Addressing, Subnetting and VLSM

Trace through the code mentally before running it. Write down your predictions, then verify.

---

## Exercise T1: Calculating Prefix for Host Requirements

### Code

```python
import math

def prefix_for_hosts(hosts_needed: int) -> int:
    """Calculate minimum prefix for a number of hosts."""
    total_needed = hosts_needed + 2          # Line 1
    host_bits = math.ceil(math.log2(total_needed))  # Line 2
    host_bits = max(host_bits, 2)            # Line 3
    prefix = 32 - host_bits                  # Line 4
    return prefix                            # Line 5

# Test cases
result_a = prefix_for_hosts(50)
result_b = prefix_for_hosts(2)
result_c = prefix_for_hosts(100)
```

### Questions

1. **Line-by-line for hosts_needed=50:** What is `total_needed` after Line 1?
2. **After Line 2:** What is `host_bits` when total_needed=52?
3. **Final result:** What does `result_a` contain?
4. **Edge case:** Why does Line 3 use `max(host_bits, 2)`?

### Trace Table

Fill in before checking the solution:

| Variable | hosts=50 | hosts=2 | hosts=100 |
|----------|----------|---------|-----------|
| total_needed (L1) | ? | ? | ? |
| host_bits (L2) | ? | ? | ? |
| host_bits (L3) | ? | ? | ? |
| prefix (L4) | ? | ? | ? |

### Solution

<details>
<summary>Click to reveal</summary>

| Variable | hosts=50 | hosts=2 | hosts=100 |
|----------|----------|---------|-----------|
| total_needed (L1) | 52 | 4 | 102 |
| host_bits (L2) | 6 (ceil(5.7)) | 2 (ceil(2.0)) | 7 (ceil(6.67)) |
| host_bits (L3) | 6 | 2 | 7 |
| prefix (L4) | 26 | 30 | 25 |

**Results:**
- `result_a = 26` (provides 62 usable hosts for 50 required)
- `result_b = 30` (provides 2 usable hosts for 2 required)
- `result_c = 25` (provides 126 usable hosts for 100 required)

**Why max(host_bits, 2)?**
- Ensures minimum /30 prefix (2 host bits)
- A /31 or /32 would have special behaviour
- Protects against edge cases like hosts_needed=1

</details>

---

## Exercise T2: FLSM Subnet Generation

### Code

```python
import ipaddress

def flsm_split(base: str, num_subnets: int):
    net = ipaddress.ip_network(base, strict=True)  # Line 1
    bits_needed = num_subnets.bit_length() - 1     # Line 2
    new_prefix = net.prefixlen + bits_needed       # Line 3
    return list(net.subnets(prefixlen_diff=bits_needed))  # Line 4

# Test
subnets = flsm_split("192.168.0.0/24", 4)
for i, s in enumerate(subnets):
    print(f"Subnet {i}: {s}")
```

### Questions

1. **Line 2:** What is `bits_needed` when num_subnets=4?
2. **Line 3:** What is the new prefix length?
3. **Output:** List all four subnet addresses.
4. **Block size:** How many addresses in each resulting subnet?

### Trace Table

| Step | Value |
|------|-------|
| Original prefix | ? |
| num_subnets.bit_length() | ? |
| bits_needed | ? |
| new_prefix | ? |
| Block size per subnet | ? |

### Solution

<details>
<summary>Click to reveal</summary>

| Step | Value |
|------|-------|
| Original prefix | 24 |
| num_subnets.bit_length() | 3 (binary 100 has 3 bits) |
| bits_needed | 2 (3 - 1) |
| new_prefix | 26 (24 + 2) |
| Block size per subnet | 64 (2^(32-26)) |

**Output:**
```
Subnet 0: 192.168.0.0/26
Subnet 1: 192.168.0.64/26
Subnet 2: 192.168.0.128/26
Subnet 3: 192.168.0.192/26
```

**Why bit_length() - 1?**
- 4 in binary = 100 (3 bits)
- We need 2 bits to represent 4 values (00, 01, 10, 11)
- Formula: bits_needed = ceil(log2(n)) = bit_length() - 1 for powers of 2

</details>

---

## Exercise T3: VLSM Block Alignment

### Code

```python
import ipaddress

def align_to_boundary(current_addr: int, block_size: int) -> int:
    """Align address to next block boundary."""
    if current_addr % block_size == 0:        # Line 1
        return current_addr                    # Line 2
    else:
        return ((current_addr // block_size) + 1) * block_size  # Line 3

# Test: Starting from address 10 (as integer), align to blocks of various sizes
addr = 10
print(f"Start: {addr}")
print(f"Align to 8:  {align_to_boundary(addr, 8)}")
print(f"Align to 16: {align_to_boundary(addr, 16)}")
print(f"Align to 32: {align_to_boundary(addr, 32)}")
print(f"Align to 64: {align_to_boundary(addr, 64)}")
```

### Questions

1. **For block_size=8:** Is 10 divisible by 8? What's the result?
2. **For block_size=16:** What calculation happens in Line 3?
3. **For block_size=64:** What is the aligned address?
4. **Why alignment matters:** What would happen without alignment?

### Trace Table

| Block Size | 10 % block_size | Line 3 calculation | Result |
|------------|-----------------|-------------------|--------|
| 8 | ? | ? | ? |
| 16 | ? | ? | ? |
| 32 | ? | ? | ? |
| 64 | ? | ? | ? |

### Solution

<details>
<summary>Click to reveal</summary>

| Block Size | 10 % block_size | Line 3 calculation | Result |
|------------|-----------------|-------------------|--------|
| 8 | 2 (not 0) | (10//8 + 1) × 8 = 2 × 8 | 16 |
| 16 | 10 (not 0) | (10//16 + 1) × 16 = 1 × 16 | 16 |
| 32 | 10 (not 0) | (10//32 + 1) × 32 = 1 × 32 | 32 |
| 64 | 10 (not 0) | (10//64 + 1) × 64 = 1 × 64 | 64 |

**Output:**
```
Start: 10
Align to 8:  16
Align to 16: 16
Align to 32: 32
Align to 64: 64
```

**Why alignment matters:**
- Network addresses must start at boundaries divisible by block size
- A /26 (64 addresses) must start at .0, .64, .128, or .192
- Without alignment, the subnet would span two logical blocks
- Routers expect proper alignment for efficient routing table entries

</details>

---

## Exercise T4: IPv6 Compression Logic

### Code

```python
def compress_ipv6_simple(groups: list) -> str:
    """Simplified IPv6 compression (educational version)."""
    # Step 1: Remove leading zeros from each group
    shortened = [g.lstrip('0') or '0' for g in groups]  # Line 1
    
    # Step 2: Find longest run of '0' groups
    longest_start = -1
    longest_len = 0
    current_start = -1
    current_len = 0
    
    for i, g in enumerate(shortened):                    # Line 2
        if g == '0':
            if current_start == -1:
                current_start = i
            current_len += 1
        else:
            if current_len > longest_len:
                longest_start = current_start
                longest_len = current_len
            current_start = -1
            current_len = 0
    
    # Check final run
    if current_len > longest_len:                        # Line 3
        longest_start = current_start
        longest_len = current_len
    
    # Step 3: Build result with :: for longest run
    if longest_len > 1:                                  # Line 4
        before = shortened[:longest_start]
        after = shortened[longest_start + longest_len:]
        return ':'.join(before) + '::' + ':'.join(after)
    else:
        return ':'.join(shortened)

# Test
groups = ['2001', '0db8', '0000', '0000', '0000', '0085', '0000', '7334']
result = compress_ipv6_simple(groups)
print(result)
```

### Questions

1. **After Line 1:** What does `shortened` contain?
2. **After Line 2-3:** Where is the longest run of zeros? (start, length)
3. **Line 4:** What are `before` and `after`?
4. **Final result:** What is the compressed address?

### Trace Table

| Step | Value |
|------|-------|
| Original groups | ['2001', '0db8', '0000', '0000', '0000', '0085', '0000', '7334'] |
| shortened (L1) | ? |
| longest_start | ? |
| longest_len | ? |
| before | ? |
| after | ? |
| result | ? |

### Solution

<details>
<summary>Click to reveal</summary>

| Step | Value |
|------|-------|
| Original groups | ['2001', '0db8', '0000', '0000', '0000', '0085', '0000', '7334'] |
| shortened (L1) | ['2001', 'db8', '0', '0', '0', '85', '0', '7334'] |
| longest_start | 2 |
| longest_len | 3 (positions 2, 3, 4) |
| before | ['2001', 'db8'] |
| after | ['85', '0', '7334'] |
| result | `2001:db8::85:0:7334` |

**Note:** The single '0' at position 6 is NOT compressed because:
- Only the longest consecutive run gets ::
- :: can only appear once
- A run of length 1 is not worth compressing with ::

**Full address:** `2001:0db8:0000:0000:0000:0085:0000:7334`
**Compressed:** `2001:db8::85:0:7334`

</details>

---

## Challenge Exercise T5: Complete VLSM Trace

### Code

```python
def vlsm_trace(base: str, requirements: list):
    """Trace VLSM allocation step by step."""
    import ipaddress
    
    net = ipaddress.ip_network(base)
    sorted_reqs = sorted(requirements, reverse=True)  # Line 1
    
    current = int(net.network_address)                 # Line 2
    end = int(net.broadcast_address)
    
    results = []
    for req in sorted_reqs:                            # Line 3
        prefix = 32 - (req + 2 - 1).bit_length()       # Line 4
        block = 2 ** (32 - prefix)
        
        # Align
        if current % block != 0:
            current = ((current // block) + 1) * block
        
        subnet = f"{ipaddress.IPv4Address(current)}/{prefix}"
        results.append((req, prefix, subnet))
        current += block
    
    return results

# Test
allocations = vlsm_trace("10.0.0.0/24", [60, 14, 30, 2])
for req, prefix, subnet in allocations:
    print(f"Need {req:>3} hosts → /{prefix} → {subnet}")
```

### Trace This Yourself

Given requirements [60, 14, 30, 2] for network 10.0.0.0/24:

1. What order are they processed? (Line 1)
2. For 60 hosts, what prefix is calculated? (Line 4)
3. What subnet is allocated first?
4. Where does the cursor move after each allocation?

### Solution

<details>
<summary>Click to reveal</summary>

**Step-by-step trace:**

```
Sorted requirements: [60, 30, 14, 2]
Starting cursor: 10.0.0.0 (integer: 167772160)

Iteration 1: req=60
  prefix = 32 - (62).bit_length() = 32 - 6 = 26
  block = 64
  No alignment needed (0 % 64 == 0)
  Subnet: 10.0.0.0/26
  Cursor moves to: 10.0.0.64

Iteration 2: req=30
  prefix = 32 - (32).bit_length() = 32 - 6 = 26
  block = 64
  No alignment needed (64 % 64 == 0)
  Subnet: 10.0.0.64/26
  Cursor moves to: 10.0.0.128

Iteration 3: req=14
  prefix = 32 - (16).bit_length() = 32 - 5 = 27
  block = 32
  No alignment needed (128 % 32 == 0)
  Subnet: 10.0.0.128/27
  Cursor moves to: 10.0.0.160

Iteration 4: req=2
  prefix = 32 - (4).bit_length() = 32 - 3 = 29
  block = 8
  No alignment needed (160 % 8 == 0)
  Subnet: 10.0.0.160/29
  Cursor moves to: 10.0.0.168
```

**Output:**
```
Need  60 hosts → /26 → 10.0.0.0/26
Need  30 hosts → /26 → 10.0.0.64/26
Need  14 hosts → /27 → 10.0.0.128/27
Need   2 hosts → /29 → 10.0.0.160/29
```

**Space used:** 64 + 64 + 32 + 8 = 168 addresses
**Space remaining:** 256 - 168 = 88 addresses (10.0.0.168 - 10.0.0.255)

</details>

---

## Self-Assessment

After completing all traces:

- [ ] I can calculate prefix from host requirements
- [ ] I understand bit_length() for power-of-2 calculations
- [ ] I can trace FLSM subnet generation
- [ ] I understand block boundary alignment
- [ ] I can apply IPv6 compression rules
- [ ] I can trace complete VLSM allocation

---

*Week 5: IP Addressing, Subnetting, VLSM — Code Tracing Exercises*
*Computer Networks Laboratory — ASE, CSIE Bucharest*
