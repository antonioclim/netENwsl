# 🧩 Parsons Problems — Week 5

> Computer Networks Laboratory — ASE-CSIE Bucharest
>
> IP Addressing, Subnetting and VLSM

Reorder the code blocks to create a working solution. Some blocks are **distractors** — they should not be used.

---

## Problem P1: Calculate Usable Hosts

### Task
Write a function that calculates usable host addresses from a prefix length.

### Scrambled Blocks

```python
# Block A
    return total - 2

# Block B
def usable_hosts(prefix: int) -> int:

# Block C
    host_bits = 32 - prefix

# Block D
    total = 2 ** host_bits

# Block E (DISTRACTOR)
    total = host_bits ** 2

# Block F (DISTRACTOR)
    return total
```

### Correct Order
<details>
<summary>Click to reveal</summary>

```python
# Block B
def usable_hosts(prefix: int) -> int:

# Block C
    host_bits = 32 - prefix

# Block D
    total = 2 ** host_bits

# Block A
    return total - 2
```

**Note:** Block E uses wrong formula (should be 2^bits, not bits^2). Block F forgets to subtract 2 for network/broadcast.
</details>

---

## Problem P2: VLSM Sort Requirements

### Task
Sort VLSM requirements largest-first before allocation.

### Scrambled Blocks

```python
# Block A
    return sorted_reqs

# Block B
def sort_vlsm_requirements(hosts: list) -> list:

# Block C
    sorted_reqs = sorted(indexed, key=lambda x: -x[1])

# Block D
    indexed = list(enumerate(hosts))

# Block E (DISTRACTOR)
    sorted_reqs = sorted(indexed, key=lambda x: x[1])

# Block F (DISTRACTOR)
    indexed = hosts.copy()
```

### Correct Order
<details>
<summary>Click to reveal</summary>

```python
# Block B
def sort_vlsm_requirements(hosts: list) -> list:

# Block D
    indexed = list(enumerate(hosts))

# Block C
    sorted_reqs = sorted(indexed, key=lambda x: -x[1])

# Block A
    return sorted_reqs
```

**Note:** Block E sorts ascending (smallest first) which is wrong. Block F doesn't preserve indices.
</details>

---

## Problem P3: Calculate Network Address

### Task
Calculate the network address from an IP and prefix.

### Scrambled Blocks

```python
# Block A
    return str(ipaddress.IPv4Address(network_int))

# Block B
def get_network_address(ip: str, prefix: int) -> str:

# Block C
    mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF

# Block D
    ip_int = int(ipaddress.IPv4Address(ip))

# Block E
    network_int = ip_int & mask

# Block F (DISTRACTOR)
    network_int = ip_int | mask

# Block G (DISTRACTOR)
    mask = 0xFFFFFFFF >> prefix
```

### Correct Order
<details>
<summary>Click to reveal</summary>

```python
# Block B
def get_network_address(ip: str, prefix: int) -> str:

# Block D
    ip_int = int(ipaddress.IPv4Address(ip))

# Block C
    mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF

# Block E
    network_int = ip_int & mask

# Block A
    return str(ipaddress.IPv4Address(network_int))
```

**Note:** Block F uses OR (would set bits, not clear them). Block G creates wrong mask (shift right instead of left).
</details>

---

## Problem P4: IPv6 Compression Check

### Task
Check if an IPv6 address uses valid :: notation.

### Scrambled Blocks

```python
# Block A
    return address.count('::') <= 1

# Block B
def is_valid_ipv6_compression(address: str) -> bool:

# Block C (DISTRACTOR)
    return '::' in address

# Block D (DISTRACTOR)
    return address.count('::') == 1
```

### Correct Order
<details>
<summary>Click to reveal</summary>

```python
# Block B
def is_valid_ipv6_compression(address: str) -> bool:

# Block A
    return address.count('::') <= 1
```

**Note:** Block C only checks presence (doesn't catch multiple ::). Block D requires exactly one :: (but valid addresses may have zero ::).
</details>

---

## Problem P5: Lab Startup Sequence

### Task
Order the steps to start the Week 5 Docker lab environment.

### Scrambled Blocks

```
# Block A
Check containers are running

# Block B
Go to kit directory

# Block C
Start Docker service

# Block D
Run docker-compose up

# Block E
Verify environment prerequisites

# Block F (DISTRACTOR)
Install Docker Desktop
```

### Correct Order
<details>
<summary>Click to reveal</summary>

```
Block B: Go to kit directory
Block C: Start Docker service  
Block E: Verify environment prerequisites
Block D: Run docker-compose up
Block A: Check containers are running
```

**Note:** Block F is only needed once during initial setup, not every lab start.
</details>

---

## Problem P6: Prefix for Hosts Calculation

### Task
Calculate minimum prefix length for a required number of hosts.

### Scrambled Blocks

```python
# Block A
    return 32 - host_bits

# Block B
def prefix_for_hosts(needed: int) -> int:

# Block C
    import math

# Block D
    total_needed = needed + 2

# Block E
    host_bits = math.ceil(math.log2(total_needed))

# Block F (DISTRACTOR)
    host_bits = math.floor(math.log2(needed))

# Block G (DISTRACTOR)
    total_needed = needed
```

### Correct Order
<details>
<summary>Click to reveal</summary>

```python
# Block C
    import math

# Block B
def prefix_for_hosts(needed: int) -> int:

# Block D
    total_needed = needed + 2

# Block E
    host_bits = math.ceil(math.log2(total_needed))

# Block A
    return 32 - host_bits
```

**Note:** Block F uses floor (would give insufficient space) and doesn't add 2. Block G forgets network/broadcast addresses.
</details>

---

## Problem P7: Broadcast Address Calculation

### Task
Calculate broadcast address from network address and prefix.

### Scrambled Blocks

```python
# Block A
    return str(ipaddress.IPv4Address(broadcast_int))

# Block B
def get_broadcast(network: str, prefix: int) -> str:

# Block C
    block_size = 2 ** (32 - prefix)

# Block D
    network_int = int(ipaddress.IPv4Address(network))

# Block E
    broadcast_int = network_int + block_size - 1

# Block F (DISTRACTOR)
    broadcast_int = network_int + block_size

# Block G (DISTRACTOR)
    block_size = 32 - prefix
```

### Correct Order
<details>
<summary>Click to reveal</summary>

```python
# Block B
def get_broadcast(network: str, prefix: int) -> str:

# Block D
    network_int = int(ipaddress.IPv4Address(network))

# Block C
    block_size = 2 ** (32 - prefix)

# Block E
    broadcast_int = network_int + block_size - 1

# Block A
    return str(ipaddress.IPv4Address(broadcast_int))
```

**Note:** Block F doesn't subtract 1 (would overflow into next subnet). Block G confuses block size with host bits.
</details>

---

## Problem P8: FLSM Subnet Validation

### Task
Validate that subnet count is a power of 2 for FLSM.

### Scrambled Blocks

```python
# Block A
    return is_power_of_2

# Block B
def validate_flsm_count(n: int) -> bool:

# Block C
    if n <= 0:
        return False

# Block D
    is_power_of_2 = (n & (n - 1)) == 0

# Block E (DISTRACTOR)
    is_power_of_2 = n % 2 == 0

# Block F (DISTRACTOR)
    if n < 0:
        return False
```

### Correct Order
<details>
<summary>Click to reveal</summary>

```python
# Block B
def validate_flsm_count(n: int) -> bool:

# Block C
    if n <= 0:
        return False

# Block D
    is_power_of_2 = (n & (n - 1)) == 0

# Block A
    return is_power_of_2
```

**Note:** Block E only checks if even (6 is even but not power of 2). Block F allows n=0 which is invalid.
</details>

---

## Difficulty Summary

| Problem | Topic | Difficulty |
|---------|-------|------------|
| P1 | Usable hosts | Basic |
| P2 | VLSM sorting | Intermediate |
| P3 | Network address | Intermediate |
| P4 | IPv6 validation | Basic |
| P5 | Lab startup | Basic |
| P6 | Prefix calculation | Intermediate |
| P7 | Broadcast address | Intermediate |
| P8 | FLSM validation | Advanced |

---

*Week 5: IP Addressing, Subnetting and VLSM — Parsons Problems*
*Computer Networks Laboratory — ASE-CSIE Bucharest*
