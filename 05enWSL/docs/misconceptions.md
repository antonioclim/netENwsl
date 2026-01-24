# ❌ Common Misconceptions — Week 5
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> IP Addressing, Subnetting and VLSM

This document lists frequent misunderstandings and their corrections. Review these before exercises to avoid common pitfalls.

---

## CIDR and Prefix Basics

### 🚫 Misconception 1: "A /24 network has 256 usable host addresses"

**WRONG:** "Since 2^8 = 256, a /24 gives me 256 devices."

**CORRECT:** A /24 has 256 total addresses, but only **254 usable** for hosts.

| Address Type | Value | Purpose |
|--------------|-------|---------|
| Network address | x.x.x.0 | Identifies the network itself |
| Usable range | x.x.x.1 – x.x.x.254 | Assignable to hosts |
| Broadcast address | x.x.x.255 | Sends to all hosts |

**Formula:** Usable hosts = 2^(32 - prefix) - 2

**Practical verification:**
```bash
python ex_5_01_cidr_flsm.py analyse 192.168.1.0/24
# Check "Usable Hosts" in output — it shows 254, not 256
```

---

### 🚫 Misconception 2: "The network address can be assigned to a server"

**WRONG:** "192.168.1.0/24 is a valid IP for my web server."

**CORRECT:** The network address (all host bits = 0) identifies the network itself and **cannot be assigned to any device**.

**Why it matters:**
- Routers use the network address to make forwarding decisions
- Assigning it to a host causes routing failures
- Many systems reject this configuration outright

**Practical verification:**
```bash
python ex_5_01_cidr_flsm.py analyse 192.168.1.0/24
# Note: Address Type shows "network", not "host"

python ex_5_01_cidr_flsm.py analyse 192.168.1.1/24
# Note: Address Type shows "host" — this is assignable
```

---

### 🚫 Misconception 3: "Subnet boundaries always fall on .0, .128, .64, etc."

**WRONG:** "The network address always ends in 0 or a nice round number."

**CORRECT:** Subnet boundaries depend on the prefix length. For prefixes not divisible by 8, boundaries fall within octets.

| Prefix | Block Size | Possible Network Starts (last octet) |
|--------|------------|--------------------------------------|
| /24 | 256 | 0 |
| /25 | 128 | 0, 128 |
| /26 | 64 | 0, 64, 128, 192 |
| /27 | 32 | 0, 32, 64, 96, 128, 160, 192, 224 |
| /28 | 16 | 0, 16, 32, 48, 64, 80, 96, 112, 128... |

**Example:** 192.168.1.160/27 is a valid network address.

**Practical verification:**
```bash
python ex_5_01_cidr_flsm.py flsm 192.168.1.0/24 8
# Shows 8 subnets starting at .0, .32, .64, .96, .128, .160, .192, .224
```

---

### 🚫 Misconception 4: "The broadcast address is always .255"

**WRONG:** "To send to everyone on 10.0.0.64/26, I use 10.0.0.255."

**CORRECT:** The broadcast address is the **last address in the subnet**, which depends on the prefix.

| Network | Prefix | Broadcast |
|---------|--------|-----------|
| 10.0.0.0/24 | /24 | 10.0.0.255 ✓ |
| 10.0.0.0/26 | /26 | 10.0.0.63 |
| 10.0.0.64/26 | /26 | 10.0.0.127 |
| 10.0.0.192/27 | /27 | 10.0.0.223 |

**Formula:** Broadcast = Network address + Block size - 1

**Practical verification:**
```bash
python ex_5_01_cidr_flsm.py analyse 10.0.0.64/26
# Broadcast Address: 10.0.0.127 (not .255!)
```

---

## VLSM and Subnetting

### 🚫 Misconception 5: "VLSM wastes more space than FLSM"

**WRONG:** "Variable masks are more complex, so they must be less efficient."

**CORRECT:** VLSM is **more efficient** because it matches subnet sizes to actual requirements.

**Example:** Allocate for 100, 50, 25 and 10 hosts from 192.168.0.0/24

| Method | 100 hosts | 50 hosts | 25 hosts | 10 hosts | Wasted |
|--------|-----------|----------|----------|----------|--------|
| FLSM /25 | 126 (26 wasted) | 126 (76 wasted) | — | — | Only 2 subnets fit! |
| VLSM | /25 (126) | /26 (62) | /27 (30) | /28 (14) | Minimal waste |

**Practical verification:**
```bash
# VLSM allocation
python ex_5_02_vlsm_ipv6.py vlsm 192.168.0.0/24 100 50 25 10
# Check efficiency percentages — much higher than FLSM would achieve
```

---

### 🚫 Misconception 6: "VLSM allocation order does not matter"

**WRONG:** "I can allocate subnets in any order I want."

**CORRECT:** Allocate **largest requirements first** to avoid fragmentation and alignment problems.

**Why largest first?**
- Larger subnets need alignment to larger power-of-2 boundaries
- A /25 must start at addresses divisible by 128
- A /26 must start at addresses divisible by 64
- Allocating small subnets first may leave fragmented space

**Bad example (smallest first):**
```
10.0.0.0/30   (4 addresses)   → 10.0.0.0 - 10.0.0.3
10.0.0.4/30   (4 addresses)   → 10.0.0.4 - 10.0.0.7
Now need /25 (128 addresses) → Must start at 10.0.0.128, wasting .8 to .127!
```

**Practical verification:**
```bash
python ex_5_02_vlsm_ipv6.py vlsm 10.0.0.0/24 60 20 10 2
# Notice requirements are internally sorted largest-first
```

---

### 🚫 Misconception 7: "A /31 network has zero usable hosts"

**WRONG:** "2^1 - 2 = 0, so /31 is useless."

**CORRECT:** RFC 3021 defines /31 for **point-to-point links** where no broadcast is needed.

| Prefix | Total | Traditional Use | RFC 3021 Use |
|--------|-------|-----------------|--------------|
| /30 | 4 | 2 usable hosts | 2 usable hosts |
| /31 | 2 | 0 usable (old view) | 2 usable (point-to-point) |
| /32 | 1 | Host route | Host route |

**When to use /31:**
- Router-to-router links
- Any point-to-point connection where broadcast is unnecessary

**Practical verification:**
```bash
python ex_5_01_cidr_flsm.py analyse 10.0.0.0/31
# Shows 2 usable hosts (RFC 3021 compliant)
```

---

## IPv6 Addressing

### 🚫 Misconception 8: "The :: can appear multiple times in an IPv6 address"

**WRONG:** "2001:db8::1::2 compresses zeros in two places."

**CORRECT:** The `::` can appear **only once** per address; otherwise, expansion is ambiguous.

**Why?**
- `::` means "fill with as many zero groups as needed"
- If `::` appears twice, the parser cannot determine how many zeros each represents

**Valid compressions of 2001:0db8:0000:0000:0085:0000:0000:7334:**
- `2001:db8::85:0:0:7334` (:: replaces groups 3-4)
- `2001:db8:0:0:85::7334` (:: replaces groups 6-7)

**Invalid:**
- `2001:db8::85::7334` ❌

**Practical verification:**
```bash
python ex_5_02_vlsm_ipv6.py ipv6-expand 2001:db8::1
# Works — single ::

# Invalid addresses will raise errors
```

---

### 🚫 Misconception 9: "IPv6 addresses need NAT like IPv4"

**WRONG:** "We need IPv6 NAT for security and address conservation."

**CORRECT:** IPv6's vast address space (2^128) eliminates the need for NAT. Security comes from firewalls, not address hiding.

| Aspect | IPv4 + NAT | IPv6 |
|--------|------------|------|
| Address space | 4.3 billion (exhausted) | 340 undecillion |
| NAT required? | Yes, for conservation | No |
| Security | NAT provides obscurity (not security) | Firewall provides security |
| End-to-end | Broken by NAT | Preserved |

**Standard practice:**
- Organisations receive /48 (65,536 /64 subnets)
- Each LAN gets a /64 (18 quintillion hosts)
- No translation needed

---

### 🚫 Misconception 10: "Link-local addresses (fe80::) are routable"

**WRONG:** "I can ping fe80::1 from any network."

**CORRECT:** Link-local addresses are valid **only within a single network segment** and are never forwarded by routers.

| Address Type | Prefix | Scope | Routable? |
|--------------|--------|-------|-----------|
| Link-local | fe80::/10 | Single link | No |
| Unique local | fc00::/7 | Organisation | No (private) |
| Global unicast | 2000::/3 | Internet | Yes |

**Use cases for link-local:**
- Neighbour discovery
- Router advertisements
- Communication before global address is assigned

**Practical verification:**
```bash
python ex_5_02_vlsm_ipv6.py ipv6 fe80::1
# Shows: Type = link-local, Scope = link-local
```

---

## Docker Container Networking

### 🚫 Misconception 11: "Docker containers on the same subnet can always communicate"

**WRONG:** "If I assign 10.5.0.10 and 10.5.0.20 to containers, they automatically see each other."

**CORRECT:** Containers must be on the **same Docker network** to communicate. IP addresses alone are insufficient.

| Configuration | Can Communicate? |
|---------------|------------------|
| Same Docker network, same subnet | ✅ Yes |
| Different Docker networks, same subnet range | ❌ No (isolated) |
| Same Docker network, different subnets | ❌ No (no routing) |

**Practical verification:**
```bash
# Check container network
docker inspect week5_python --format "{{.NetworkSettings.Networks}}"

# Both containers must show the same network name (week5_labnet)
```

**Why this matters:**
- Docker creates isolated network namespaces
- Even if IPs appear to be in the same range, different networks are completely isolated
- This is by design for security and multi-tenancy

---

### 🚫 Misconception 12: "The gateway address in Docker compose must be .1"

**WRONG:** "For subnet 10.5.0.0/24, the gateway is always 10.5.0.1."

**CORRECT:** Docker allows **any valid host address** as gateway. The .1 convention is common but not required.

| Subnet | Valid Gateways | Notes |
|--------|----------------|-------|
| 10.5.0.0/24 | 10.5.0.1 – 10.5.0.254 | .1 is conventional |
| 10.5.0.0/28 | 10.5.0.1 – 10.5.0.14 | Smaller range |
| 10.5.0.64/26 | 10.5.0.65 – 10.5.0.126 | .65 would be first host |

**Docker compose example:**
```yaml
networks:
  labnet:
    ipam:
      config:
        - subnet: 10.5.0.0/24
          gateway: 10.5.0.1    # Convention, not requirement
```

**Practical verification:**
```bash
docker network inspect week5_labnet --format "{{range .IPAM.Config}}{{.Gateway}}{{end}}"
# Shows the configured gateway
```

---

## Quick Reference: Formulas

| Calculation | Formula |
|-------------|---------|
| Total addresses | 2^(32 - prefix) for IPv4 |
| Usable hosts | 2^(32 - prefix) - 2 |
| Broadcast address | Network address + block size - 1 |
| Required prefix for N hosts | 32 - ceil(log₂(N + 2)) |
| Block size | 2^(32 - prefix) |
| Number of /64 subnets in /48 | 2^(64-48) = 65,536 |

---

## Self-Check Questions

Before the lab, verify you understand:

1. ☐ Why does a /26 have 62 usable hosts, not 64?
2. ☐ What is the broadcast address of 172.16.100.64/26?
3. ☐ Why must VLSM allocate largest subnets first?
4. ☐ How many times can :: appear in one IPv6 address?
5. ☐ What is the standard subnet size for IPv6 LANs?
6. ☐ Can two Docker containers communicate if they have IPs in the same range but are on different Docker networks?
7. ☐ What address does Docker typically use as the gateway in a custom network?

---

*Week 5: IP Addressing, Subnetting, VLSM — Common Misconceptions*
*Computer Networks Laboratory — ASE, CSIE Bucharest*
