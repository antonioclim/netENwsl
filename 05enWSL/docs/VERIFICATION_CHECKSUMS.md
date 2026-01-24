# 🔐 Verification Checksums — Week 5
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Independent Verification of All Technical Claims

This document provides verification commands and expected outputs for all calculations and technical claims in the Week 5 materials. Every formula and example can be independently verified using standard tools.

---

## Purpose

**AI Risk Mitigation**: All technical content in this kit can be verified through:
1. **RFC Standards** — Authoritative source documents
2. **Python stdlib** — Using only `ipaddress` module (no external dependencies)
3. **Mathematical proofs** — Derivable from first principles

---

## Core Formulas with Verification

### Formula 1: Usable Hosts

**Claim**: Usable hosts = 2^(32 - prefix) - 2

**Source**: RFC 791 Section 3.2; RFC 950 (Subnetting)

**Verification**:
```bash
# Test with /26
python3 -c "print(f'/26 usable hosts: {2**(32-26) - 2}')"
# Expected output: /26 usable hosts: 62

# Test with /24
python3 -c "print(f'/24 usable hosts: {2**(32-24) - 2}')"
# Expected output: /24 usable hosts: 254

# Test with /28
python3 -c "print(f'/28 usable hosts: {2**(32-28) - 2}')"
# Expected output: /28 usable hosts: 14
```

**Cross-verification with ipaddress module**:
```bash
python3 -c "
import ipaddress
net = ipaddress.ip_network('192.168.1.0/26')
print(f'Total: {net.num_addresses}, Usable: {net.num_addresses - 2}')
"
# Expected: Total: 64, Usable: 62
```

---

### Formula 2: Broadcast Address

**Claim**: Broadcast = Network address + 2^(32 - prefix) - 1

**Source**: RFC 791 Section 3.2; RFC 922 (Broadcasting)

**Verification**:
```bash
# Test: 192.168.1.64/26
python3 -c "
import ipaddress
net = ipaddress.ip_network('192.168.1.64/26', strict=True)
print(f'Network: {net.network_address}')
print(f'Broadcast: {net.broadcast_address}')
print(f'Manual calc: {int(net.network_address) + 2**(32-26) - 1}')
"
# Expected:
# Network: 192.168.1.64
# Broadcast: 192.168.1.127
# Manual calc: 3232235903 (which is 192.168.1.127)
```

**Additional verification**:
```bash
# Convert to verify: 64 + 64 - 1 = 127
python3 -c "print(f'64 + 64 - 1 = {64 + 64 - 1}')"
# Expected: 64 + 64 - 1 = 127
```

---

### Formula 3: FLSM New Prefix

**Claim**: New prefix = Original prefix + ceil(log₂(num_subnets))

**Source**: RFC 950 (Subnetting); RFC 1878 (VLSM)

**Verification**:
```bash
# Split /24 into 8 subnets
python3 -c "
import math
original = 24
num_subnets = 8
bits_needed = math.ceil(math.log2(num_subnets))
new_prefix = original + bits_needed
print(f'Bits needed for {num_subnets} subnets: {bits_needed}')
print(f'New prefix: /{new_prefix}')
"
# Expected:
# Bits needed for 8 subnets: 3
# New prefix: /27
```

**Cross-verification with ipaddress**:
```bash
python3 -c "
import ipaddress
net = ipaddress.ip_network('192.168.0.0/24')
subnets = list(net.subnets(prefixlen_diff=3))
print(f'Number of subnets: {len(subnets)}')
print(f'First subnet: {subnets[0]}')
print(f'New prefix: /{subnets[0].prefixlen}')
"
# Expected:
# Number of subnets: 8
# First subnet: 192.168.0.0/27
# New prefix: /27
```

---

### Formula 4: Prefix for Host Requirements

**Claim**: Prefix = 32 - ceil(log₂(hosts_needed + 2))

**Source**: RFC 1878 (VLSM)

**Verification**:
```bash
# For 60 hosts
python3 -c "
import math
hosts = 60
total_needed = hosts + 2  # network + broadcast
bits = math.ceil(math.log2(total_needed))
prefix = 32 - bits
print(f'Hosts needed: {hosts}')
print(f'Total addresses needed: {total_needed}')
print(f'Host bits required: {bits}')
print(f'Prefix: /{prefix}')
print(f'Actual usable: {2**bits - 2}')
"
# Expected:
# Hosts needed: 60
# Total addresses needed: 62
# Host bits required: 6
# Prefix: /26
# Actual usable: 62
```

---

### Formula 5: Network Address Calculation

**Claim**: Network Address = IP AND Subnet Mask

**Source**: RFC 791 Section 3.1

**Verification**:
```bash
# Calculate network for 172.16.45.67/20
python3 -c "
import ipaddress
interface = ipaddress.ip_interface('172.16.45.67/20')
print(f'IP: {interface.ip}')
print(f'Network: {interface.network.network_address}')
print(f'Mask: {interface.netmask}')

# Binary verification
ip_int = int(interface.ip)
mask_int = int(interface.netmask)
network_int = ip_int & mask_int
print(f'IP AND Mask = {ipaddress.ip_address(network_int)}')
"
# Expected:
# IP: 172.16.45.67
# Network: 172.16.32.0
# Mask: 255.255.240.0
# IP AND Mask = 172.16.32.0
```

---

## RFC Reference Verification

All RFC numbers cited in this kit are real and can be verified at:

| RFC | Title | URL |
|-----|-------|-----|
| RFC 791 | Internet Protocol | https://www.rfc-editor.org/rfc/rfc791 |
| RFC 950 | Internet Standard Subnetting | https://www.rfc-editor.org/rfc/rfc950 |
| RFC 1878 | Variable Length Subnet Table | https://www.rfc-editor.org/rfc/rfc1878 |
| RFC 1918 | Private Address Allocation | https://www.rfc-editor.org/rfc/rfc1918 |
| RFC 3021 | 31-Bit Prefixes | https://www.rfc-editor.org/rfc/rfc3021 |
| RFC 4291 | IPv6 Addressing Architecture | https://www.rfc-editor.org/rfc/rfc4291 |
| RFC 5952 | IPv6 Text Representation | https://www.rfc-editor.org/rfc/rfc5952 |
| RFC 8200 | IPv6 Specification | https://www.rfc-editor.org/rfc/rfc8200 |

---

## Exercise Output Verification

### Exercise 5.01: CIDR Analysis

**Input**: `192.168.10.14/26`

**Expected JSON Output** (verify with `--json` flag):
```json
{
  "input": "192.168.10.14/26",
  "address": "192.168.10.14",
  "address_type": "host",
  "network": "192.168.10.0",
  "prefix": 26,
  "netmask": "255.255.255.192",
  "wildcard": "0.0.0.63",
  "broadcast": "192.168.10.63",
  "total_addresses": 64,
  "usable_hosts": 62,
  "first_host": "192.168.10.1",
  "last_host": "192.168.10.62",
  "is_private": true
}
```

**Verification command**:
```bash
python3 src/exercises/ex_5_01_cidr_flsm.py analyse 192.168.10.14/26 --json
```

---

### Exercise 5.01: FLSM Split

**Input**: `192.168.100.0/24` split into 4 subnets

**Expected Output**:
```
Subnet 0: 192.168.100.0/26   (Network: .0, Broadcast: .63)
Subnet 1: 192.168.100.64/26  (Network: .64, Broadcast: .127)
Subnet 2: 192.168.100.128/26 (Network: .128, Broadcast: .191)
Subnet 3: 192.168.100.192/26 (Network: .192, Broadcast: .255)
```

**Verification command**:
```bash
python3 src/exercises/ex_5_01_cidr_flsm.py flsm 192.168.100.0/24 4
```

---

## Quick Verification Script

Run this script to verify all core calculations:

```bash
#!/bin/bash
# verify_all.sh — Verify all Week 5 calculations

echo "═══ Week 5 Calculation Verification ═══"
echo ""

echo "1. Usable hosts for /26:"
python3 -c "print(f'   Expected: 62, Actual: {2**(32-26) - 2}')"

echo "2. Broadcast for 192.168.1.64/26:"
python3 -c "print(f'   Expected: 127, Actual: {64 + 64 - 1}')"

echo "3. New prefix when splitting /24 into 8:"
python3 -c "import math; print(f'   Expected: 27, Actual: {24 + math.ceil(math.log2(8))}')"

echo "4. Prefix needed for 60 hosts:"
python3 -c "import math; print(f'   Expected: 26, Actual: {32 - math.ceil(math.log2(62))}')"

echo "5. Network address for 172.16.45.67/20:"
python3 -c "import ipaddress; print(f'   Expected: 172.16.32.0, Actual: {ipaddress.ip_interface(\"172.16.45.67/20\").network.network_address}')"

echo ""
echo "═══ All verifications complete ═══"
```

---

## Automated Verification

The test suite automatically verifies all calculations:

```bash
# Run full verification
make test

# Run specific formula tests
python3 -m pytest tests/test_exercises.py -v -k "test_analyze"
python3 -m pytest tests/test_exercises.py -v -k "test_flsm"
python3 -m pytest tests/test_exercises.py -v -k "test_vlsm"
```

---

## Note on AI-Generated Content

This educational kit was developed with AI assistance. To ensure accuracy:

1. **All formulas** are derived from RFC standards (not AI interpretation)
2. **All examples** include verification commands using Python stdlib
3. **All outputs** can be independently reproduced
4. **No external APIs** are required for verification

If you find any discrepancy, please:
1. Run the verification command
2. Check the RFC source
3. Report via issue on the GitHub repository

---

*Week 5: IP Addressing, Subnetting, VLSM — Verification Checksums*
*Computer Networks Laboratory — ASE, CSIE Bucharest*
