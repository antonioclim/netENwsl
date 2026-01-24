# 🧩 Parsons Problems — Week 5
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> IP Addressing, Subnetting and VLSM

Reorder the code blocks to create working solutions. Some problems include distractor blocks that should not be used.

---

## Problem P1: Calculate Usable Hosts

### Task

Create a function that calculates the number of usable host addresses given a CIDR prefix length.

### Scrambled Blocks

```python
# Block A
    return usable

# Block B
def usable_hosts(prefix: int) -> int:

# Block C
    host_bits = 32 - prefix

# Block D
    usable = (2 ** host_bits) - 2

# Block E
    total = 2 ** host_bits

# Block F (DISTRACTOR)
    usable = total / 2
```

### Hints

- The function signature comes first
- Calculate host bits from prefix
- Total addresses = 2^host_bits
- Usable = total - 2 (network and broadcast)

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block B
def usable_hosts(prefix: int) -> int:

# Block C
    host_bits = 32 - prefix

# Block E
    total = 2 ** host_bits

# Block D
    usable = (2 ** host_bits) - 2

# Block A
    return usable
```

**Complete function:**
```python
def usable_hosts(prefix: int) -> int:
    host_bits = 32 - prefix
    total = 2 ** host_bits
    usable = (2 ** host_bits) - 2
    return usable
```

**Note:** Block E is optional since Block D recalculates, but including it shows the logic clearly. Block F is wrong because dividing by 2 is not how we calculate usable hosts.

</details>

---

## Problem P2: Validate Network Address

### Task

Create a function that checks if a given IP address is the network address for its subnet (i.e., all host bits are zero).

### Scrambled Blocks

```python
# Block A
import ipaddress

# Block B
def is_network_address(cidr: str) -> bool:

# Block C
    interface = ipaddress.IPv4Interface(cidr)

# Block D
    return interface.ip == interface.network.network_address

# Block E
    network = interface.network

# Block F (DISTRACTOR)
    return str(interface.ip).endswith('.0')

# Block G (DISTRACTOR)
    return interface.ip == interface.network.broadcast_address
```

### Hints

- Import statement comes first
- Create an interface object from the CIDR string
- Compare the IP to the network's network_address
- Ending in .0 is NOT a reliable check (think about /26, /27, etc.)

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block A
import ipaddress

# Block B
def is_network_address(cidr: str) -> bool:

# Block C
    interface = ipaddress.IPv4Interface(cidr)

# Block D
    return interface.ip == interface.network.network_address
```

**Complete function:**
```python
import ipaddress

def is_network_address(cidr: str) -> bool:
    interface = ipaddress.IPv4Interface(cidr)
    return interface.ip == interface.network.network_address
```

**Why distractors are wrong:**
- Block F: `.endswith('.0')` fails for subnets like /26 where network addresses can be .64, .128, .192
- Block G: Checks for broadcast address, not network address
- Block E: Not needed; we can access network_address directly

**Test:**
```python
is_network_address("192.168.1.0/24")   # True
is_network_address("192.168.1.1/24")   # False
is_network_address("192.168.1.64/26")  # True (network address of this /26)
```

</details>

---

## Problem P3: VLSM Prefix Calculator

### Task

Create a function that determines the minimum prefix length needed to accommodate a given number of hosts.

### Scrambled Blocks

```python
# Block A
import math

# Block B
def prefix_for_hosts(hosts_needed: int) -> int:

# Block C
    total_needed = hosts_needed + 2

# Block D
    host_bits = math.ceil(math.log2(total_needed))

# Block E
    prefix = 32 - host_bits

# Block F
    return prefix

# Block G (DISTRACTOR)
    host_bits = hosts_needed.bit_length()

# Block H (DISTRACTOR)
    prefix = host_bits
```

### Hints

- Need to account for network and broadcast addresses (+2)
- Use ceiling of log2 to find minimum bits needed
- Prefix = 32 minus host bits
- bit_length() alone does not account for +2

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block A
import math

# Block B
def prefix_for_hosts(hosts_needed: int) -> int:

# Block C
    total_needed = hosts_needed + 2

# Block D
    host_bits = math.ceil(math.log2(total_needed))

# Block E
    prefix = 32 - host_bits

# Block F
    return prefix
```

**Complete function:**
```python
import math

def prefix_for_hosts(hosts_needed: int) -> int:
    total_needed = hosts_needed + 2
    host_bits = math.ceil(math.log2(total_needed))
    prefix = 32 - host_bits
    return prefix
```

**Why distractors are wrong:**
- Block G: `hosts_needed.bit_length()` does not add 2 for network/broadcast
- Block H: `prefix = host_bits` is backwards; prefix = 32 - host_bits

**Test:**
```python
prefix_for_hosts(50)   # Returns 26 (62 usable hosts)
prefix_for_hosts(100)  # Returns 25 (126 usable hosts)
prefix_for_hosts(2)    # Returns 30 (2 usable hosts)
```

</details>

---

## Problem P4: IPv6 Address Expansion

### Task

Create a function that expands a compressed IPv6 address to its full form with all zeros shown.

### Scrambled Blocks

```python
# Block A
import ipaddress

# Block B
def expand_ipv6(address: str) -> str:

# Block C
    addr = ipaddress.IPv6Address(address)

# Block D
    return addr.exploded

# Block E (DISTRACTOR)
    return str(addr)

# Block F (DISTRACTOR)
    groups = address.split(':')
    return ':'.join(g.zfill(4) for g in groups)
```

### Hints

- The ipaddress module does the heavy lifting
- IPv6Address has an `exploded` property
- str(addr) gives compressed form, not expanded
- Manual splitting does not handle :: correctly

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block A
import ipaddress

# Block B
def expand_ipv6(address: str) -> str:

# Block C
    addr = ipaddress.IPv6Address(address)

# Block D
    return addr.exploded
```

**Complete function:**
```python
import ipaddress

def expand_ipv6(address: str) -> str:
    addr = ipaddress.IPv6Address(address)
    return addr.exploded
```

**Why distractors are wrong:**
- Block E: `str(addr)` returns the compressed form, not expanded
- Block F: Manual splitting fails when `::` is present because it represents multiple zero groups

**Test:**
```python
expand_ipv6("2001:db8::1")
# Returns: "2001:0db8:0000:0000:0000:0000:0000:0001"

expand_ipv6("::1")
# Returns: "0000:0000:0000:0000:0000:0000:0000:0001"
```

</details>

---

## Challenge Problem P5: Subnet Iterator

### Task

Create a generator function that yields all usable host addresses in a given subnet.

### Scrambled Blocks

```python
# Block A
import ipaddress

# Block B
def usable_hosts_generator(cidr: str):

# Block C
    network = ipaddress.ip_network(cidr, strict=False)

# Block D
    for host in network.hosts():

# Block E
        yield host

# Block F (DISTRACTOR)
    for host in network:

# Block G (DISTRACTOR)
        yield str(host)

# Block H (DISTRACTOR)
    return list(network.hosts())
```

### Hints

- Use `network.hosts()` method which excludes network and broadcast
- `yield` makes this a generator
- Iterating `network` directly includes network and broadcast addresses
- `return list(...)` would return a list, not yield items one by one

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block A
import ipaddress

# Block B
def usable_hosts_generator(cidr: str):

# Block C
    network = ipaddress.ip_network(cidr, strict=False)

# Block D
    for host in network.hosts():

# Block E
        yield host
```

**Complete function:**
```python
import ipaddress

def usable_hosts_generator(cidr: str):
    network = ipaddress.ip_network(cidr, strict=False)
    for host in network.hosts():
        yield host
```

**Why distractors are wrong:**
- Block F: `for host in network` includes network and broadcast addresses
- Block G: Converting to string is unnecessary; yield the address object
- Block H: `return list(...)` returns everything at once, not a generator

**Test:**
```python
for ip in usable_hosts_generator("192.168.1.0/30"):
    print(ip)
# Output:
# 192.168.1.1
# 192.168.1.2
```

**Note:** `strict=False` allows passing addresses like "192.168.1.5/24" which would otherwise raise an error.

</details>

---

## Self-Assessment Checklist

After completing all problems:

- [ ] I can write functions with correct Python syntax
- [ ] I understand the difference between total and usable addresses
- [ ] I know how to use the ipaddress module
- [ ] I can identify why certain approaches are wrong
- [ ] I understand generators vs regular functions

---

## Bonus: Create Your Own

Try creating a Parsons problem for one of these tasks:

1. A function that checks if an IP is in a given subnet
2. A function that calculates the broadcast address from network address and prefix
3. A function that validates IPv6 address format

Share with your pair programming partner and test each other!

---

*Week 5: IP Addressing, Subnetting, VLSM — Parsons Problems*
*Computer Networks Laboratory — ASE, CSIE Bucharest*
