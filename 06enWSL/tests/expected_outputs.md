# ✅ Expected Outputs — Week 6: NAT/PAT & SDN

> Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

This document provides **concrete, verifiable** expected outputs for each exercise. Use these to confirm your implementation is correct.

---

## Environment Verification

### Command: `python setup/verify_environment.py`

**Expected Output (all checks pass):**
```
═══════════════════════════════════════════════════════════════════
  Week 6 Environment Verification
═══════════════════════════════════════════════════════════════════

Checking Python version...
  ✓ Python 3.11.x detected

Checking required packages...
  ✓ docker (6.x.x)
  ✓ requests (2.x.x)
  ✓ pyyaml (6.x)

Checking Docker...
  ✓ Docker Desktop running
  ✓ Docker version 24.x.x

Checking WSL2...
  ✓ WSL2 environment detected

═══════════════════════════════════════════════════════════════════
  All checks passed! Environment ready for Week 6 laboratory.
═══════════════════════════════════════════════════════════════════
```

---

## Exercise 1: NAT/PAT Configuration

### Command: `sudo python3 src/exercises/ex_6_01_nat_topology.py --test`

**Expected Output:**
```
*** NAT configuration complete
*** h1/h2 (192.168.1.0/24) → NAT → 203.0.113.1 → h3

*** TEST 1: Ping h1 → h3 (through NAT)
    Result: OK

*** TEST 2: Ping h2 → h3 (through NAT)
    Result: OK

*** TEST 3: Verify NAT table
    MASQUERADE present: OK

*** NAT table (rnat):
Chain PREROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain POSTROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination
    4   336 MASQUERADE  all  --  *      rnat-eth1  192.168.1.0/24       0.0.0.0/0

*** Conntrack table (showing NAT translations):
tcp      6 431999 ESTABLISHED src=192.168.1.10 dst=203.0.113.2 sport=XXXXX dport=ICMP...

*** ALL TESTS PASSED ***
```

**Key Verification Points:**
- MASQUERADE rule present in POSTROUTING chain
- Source `192.168.1.0/24`, interface `rnat-eth1`
- Conntrack entries show internal IP (192.168.1.x) mapped to external

---

### NAT Observer Output

**Server (h3):** `h3 python3 src/apps/nat_observer.py server --bind 203.0.113.2 --port 5000`

```
═══════════════════════════════════════════════════════════════════
  NAT Observer Server
  Listening on 203.0.113.2:5000
═══════════════════════════════════════════════════════════════════

[2026-01-24 10:15:32] Connection from 203.0.113.1:50001
  Message: "Hello from h1"
  Observed source: 203.0.113.1:50001 (NAT public IP)

[2026-01-24 10:15:45] Connection from 203.0.113.1:50002
  Message: "Hello from h2"
  Observed source: 203.0.113.1:50002 (NAT public IP)
```

**Key Verification Points:**
- Both h1 and h2 appear as `203.0.113.1` (NAT public IP)
- Different source ports (50001, 50002) distinguish the connections

---

## Exercise 2: SDN Topology

### Command: `sudo python3 src/exercises/ex_6_02_sdn_topology.py --test --install-flows`

**Expected Output:**
```
*** SDN topology started
*** Installing static OpenFlow rules...

*** TEST 1: h1 → h2 connectivity (should PASS)
    Result: PASS (0% packet loss)

*** TEST 2: h2 → h1 connectivity (should PASS)
    Result: PASS (0% packet loss)

*** TEST 3: h1 → h3 connectivity (should FAIL - blocked by policy)
    Result: PASS (100% packet loss as expected)

*** TEST 4: h2 → h3 connectivity (should PASS)
    Result: PASS (0% packet loss)

*** Flow table (s1):
 cookie=0x0, duration=XXs, table=0, n_packets=0, n_bytes=0, priority=0 actions=CONTROLLER:65535
 cookie=0x0, duration=XXs, table=0, n_packets=4, n_bytes=392, priority=100,icmp,nw_src=10.0.6.11,nw_dst=10.0.6.12 actions=output:2
 cookie=0x0, duration=XXs, table=0, n_packets=4, n_bytes=392, priority=100,icmp,nw_src=10.0.6.12,nw_dst=10.0.6.11 actions=output:1
 cookie=0x0, duration=XXs, table=0, n_packets=2, n_bytes=196, priority=50,ip,nw_dst=10.0.6.13 actions=drop

*** ALL TESTS PASSED ***
```

**Key Verification Points:**
- Flow rules installed with correct priorities
- h1↔h2: `actions=output:X` (forwarded)
- h1→h3: `actions=drop` (blocked)
- priority=100 > priority=50 (permit rules beat block rules)

---

## Smoke Test

### Command: `python tests/smoke_test.py`

**Expected Output:**
```
════════════════════════════════════════════════════════════════════
  WEEK 6 SMOKE TEST
════════════════════════════════════════════════════════════════════

Checking required files...
  Found: 17/17
  ✓ All required files present

Checking Python syntax...
  Valid: 20
  ✓ All Python files have valid syntax

════════════════════════════════════════════════════════════════════
  SMOKE TEST PASSED
════════════════════════════════════════════════════════════════════
```

---

## Formative Quiz

### Command: `python formative/run_quiz.py --limit 3`

**Expected Output (example interaction):**
```
═══════════════════════════════════════════════════════════════════
  FORMATIVE QUIZ — Week 6: NAT/PAT & SDN
  Computer Networks — ASE, CSIE
═══════════════════════════════════════════════════════════════════

  Topic:         NAT/PAT, Network Support Protocols & Software-Defined Networking
  Questions:     3
  Time estimate: 3-4 minutes
  Passing score: 70%

Press Enter to start the quiz...

──────────────────────────────────────────────────────────────────
Question 1/3  [LO1] [BASIC] [Remember]
──────────────────────────────────────────────────────────────────

Which NAT variant allows multiple internal hosts to share a single public IP address by also translating port numbers?

   a) Static NAT
   b) Dynamic NAT
   c) PAT (Port Address Translation)
   d) Proxy ARP

Your answer: c

✅ CORRECT!

📖 PAT (also called NAPT or NAT Overload) multiplexes connections through unique port numbers, enabling many-to-one address mapping.

[... more questions ...]

═══════════════════════════════════════════════════════════════════
  QUIZ RESULTS
═══════════════════════════════════════════════════════════════════

  Score:    2/3 (66.7%)
  Status:   ❌ NEEDS REVIEW
  Time:     45 seconds

  Performance by Learning Objective:
    LO1: ██████████ 1/1 (100%)
    LO2: █████░░░░░ 1/2 (50%)

═══════════════════════════════════════════════════════════════════
```

---

## ovs-ofctl Commands

### List all flows: `ovs-ofctl -O OpenFlow13 dump-flows s1`

**Expected Output:**
```
 cookie=0x0, duration=123.456s, table=0, n_packets=0, n_bytes=0, priority=0 actions=CONTROLLER:65535
 cookie=0x0, duration=123.456s, table=0, n_packets=8, n_bytes=784, priority=100,icmp,nw_src=10.0.6.11,nw_dst=10.0.6.12 actions=output:2
 cookie=0x0, duration=123.456s, table=0, n_packets=8, n_bytes=784, priority=100,icmp,nw_src=10.0.6.12,nw_dst=10.0.6.11 actions=output:1
 cookie=0x0, duration=123.456s, table=0, n_packets=4, n_bytes=392, priority=100,icmp,nw_src=10.0.6.12,nw_dst=10.0.6.13 actions=output:3
 cookie=0x0, duration=123.456s, table=0, n_packets=2, n_bytes=196, priority=50,ip,nw_dst=10.0.6.13 actions=drop
 cookie=0x0, duration=123.456s, table=0, n_packets=12, n_bytes=504, priority=100,arp actions=NORMAL
```

**Column meanings:**
- `duration`: Time since flow was installed
- `n_packets`: Number of packets matched
- `n_bytes`: Total bytes matched
- `priority`: Higher number = higher importance
- `actions`: What happens to matched packets

---

## iptables Commands

### List NAT rules: `iptables -t nat -L -n -v`

**Expected Output:**
```
Chain PREROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain POSTROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination
   12  1008 MASQUERADE  all  --  *      rnat-eth1  192.168.1.0/24       0.0.0.0/0
```

---

## conntrack Commands

### List connections: `conntrack -L`

**Expected Output:**
```
tcp      6 431999 ESTABLISHED src=192.168.1.10 dst=203.0.113.2 sport=45678 dport=5000 src=203.0.113.2 dst=203.0.113.1 sport=5000 dport=50001 [ASSURED] mark=0 use=1
tcp      6 431998 ESTABLISHED src=192.168.1.20 dst=203.0.113.2 sport=45679 dport=5000 src=203.0.113.2 dst=203.0.113.1 sport=5000 dport=50002 [ASSURED] mark=0 use=1
icmp     1 29 src=192.168.1.10 dst=203.0.113.2 type=8 code=0 id=1234 src=203.0.113.2 dst=203.0.113.1 type=0 code=0 id=1234 mark=0 use=1
```

**Entry format:**
```
<protocol> <proto_num> <timeout> <state> 
  src=<internal_ip> dst=<dest_ip> sport=<internal_port> dport=<dest_port>
  src=<dest_ip> dst=<NAT_public_ip> sport=<dest_port> dport=<translated_port>
```

---

## Error Scenarios (Expected Failures)

### Missing Docker
```
ERROR: Docker is not running or not installed.
Please start Docker Desktop and ensure WSL2 integration is enabled.
```

### Missing Mininet (in non-container environment)
```
ModuleNotFoundError: No module named 'mininet'
Solution: Run inside the Docker container or install Mininet manually.
```

### Permission denied
```
ERROR: This script requires root privileges.
Run with: sudo python3 ...
```

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
