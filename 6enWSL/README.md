# Week 6: NAT/PAT, Network Support Protocols & Software-Defined Networking

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
> 
> by Revolvix

## Overview

This laboratory session integrates two complementary domains of modern network architecture: address translation mechanisms that sustain IPv4's extended lifecycle, and the paradigm shift towards software-defined networking (SDN) that decouples control logic from forwarding hardware.

The first component examines Network Address Translation (NAT) and its port-multiplexed variant (PAT/NAPT), protocols that have become indispensable infrastructure for private-to-public address mapping. Students will configure iptables-based MASQUERADE rules on a Linux router, observe the bidirectional translation process, and analyse how ephemeral port allocation enables multiple internal hosts to share a single public address.

The second component introduces SDN architecture through OpenFlow 1.3, demonstrating the fundamental separation between control plane (centralised decision-making) and data plane (distributed packet forwarding). Using OS-Ken as the controller framework and Open vSwitch as the programmable switch, students will implement and observe flow-based policies that selectively permit or block traffic based on source, destination, and protocol criteria.

## Learning Objectives

By the end of this laboratory session, you will be able to:

1. **Recall** the purpose and classification of NAT variants (static, dynamic, PAT) and the role of auxiliary protocols (ARP, DHCP, ICMP, NDP)
2. **Explain** how PAT translation tables maintain bidirectional session state and why this mechanism creates challenges for inbound connections
3. **Implement** NAT/MASQUERADE rules using iptables on a multi-homed Linux router within a simulated topology
4. **Demonstrate** SDN flow installation by observing controller-switch communication and inspecting flow tables with ovs-ofctl
5. **Analyse** the behavioural differences between permitted and blocked traffic in an SDN topology, correlating packet outcomes with installed flow rules
6. **Compare** traditional distributed routing with centralised SDN control, articulating trade-offs in scalability, flexibility, and failure domains
7. **Design** custom OpenFlow policies that implement per-host, per-protocol access control within a software-defined network

## Prerequisites

### Knowledge Requirements

- Understanding of IPv4 addressing, subnetting, and CIDR notation (Weeks 4-5)
- Familiarity with TCP/UDP socket programming concepts (Weeks 2-3)
- Basic Linux command-line proficiency (file navigation, process management)
- Conceptual understanding of the OSI and TCP/IP models

### Software Requirements

- Windows 10/11 with WSL2 enabled (Ubuntu 22.04 or later)
- Docker Desktop with WSL2 backend integration
- Wireshark (native Windows application)
- Python 3.11 or later
- Git (optional, for version control)

### Hardware Requirements

- Minimum 8GB RAM (16GB recommended for parallel container execution)
- 10GB free disk space
- Network connectivity (for initial package installation)

## Quick Start

### First-Time Setup (Run Once)

```powershell
# Open PowerShell as Administrator
cd WEEK6_WSLkit

# Verify prerequisites are installed
python setup/verify_environment.py

# If any checks fail, run the installer helper
python setup/install_prerequisites.py

# Configure Docker for privileged operations
python setup/configure_docker.py
```

### Starting the Laboratory

```powershell
# Start all services (Docker containers, network setup)
python scripts/start_lab.py

# Verify services are running
python scripts/start_lab.py --status

# For rebuilding containers after changes
python scripts/start_lab.py --rebuild
```

### Accessing Services

| Service | URL/Port | Purpose |
|---------|----------|---------|
| Portainer | https://localhost:9443 | Container management dashboard |
| SDN Controller | localhost:6633 | OpenFlow controller endpoint |
| NAT Router (rnat) | 203.0.113.1 | Public-facing NAT gateway |
| NAT Observer | Port 5000 | PAT translation demonstration |
| TCP Echo | Port 9090 | SDN connectivity testing |
| UDP Echo | Port 9091 | Protocol-specific policy testing |

## Network Topology

### Week 6 IP Plan

| Resource | Address | Purpose |
|----------|---------|---------|
| SDN Subnet | 10.0.6.0/24 | SDN topology internal network |
| h1 | 10.0.6.11 | SDN host (full access to h2) |
| h2 | 10.0.6.12 | SDN host (server) |
| h3 | 10.0.6.13 | SDN host (restricted access) |
| Private Subnet | 192.168.1.0/24 | NAT topology internal network |
| NAT Private | 192.168.1.1 | Router interface (private side) |
| NAT Public | 203.0.113.1 | Router interface (public side, TEST-NET-3) |
| h3 (NAT) | 203.0.113.2 | Public server in NAT topology |

### Port Plan

| Port | Protocol | Usage |
|------|----------|-------|
| 9090 | TCP | Echo server/client application |
| 9091 | UDP | Echo server/client application |
| 6633 | TCP | OpenFlow controller (legacy) |
| 6653 | TCP | OpenFlow controller (standard) |
| 5000 | TCP | NAT observer application |
| 5600-5699 | - | Week 6 custom port range |

## Laboratory Exercises

### Exercise 1: NAT/PAT Configuration and Observation

**Objective:** Configure MASQUERADE NAT on a Linux router and observe port address translation in action.

**Duration:** 40 minutes

**Background:** When private hosts (RFC 1918 addresses) communicate with public servers, NAT rewrites source addresses to the router's public IP. PAT extends this by also translating source ports, enabling multiple internal hosts to share a single public address.

**Steps:**

1. Start the NAT topology:
   ```powershell
   python scripts/run_demo.py --demo nat
   ```

2. In the Mininet CLI, verify interface configuration:
   ```bash
   rnat ifconfig
   rnat iptables -t nat -L -n -v
   ```

3. Start the NAT observer on the public server (h3):
   ```bash
   h3 python3 seminar/python/apps/nat_observer.py server --bind 203.0.113.2 --port 5000
   ```

4. From private hosts, initiate connections:
   ```bash
   h1 python3 seminar/python/apps/nat_observer.py client --host 203.0.113.2 --port 5000 --msg "Hello from h1"
   h2 python3 seminar/python/apps/nat_observer.py client --host 203.0.113.2 --port 5000 --msg "Hello from h2"
   ```

5. Observe the server output - note that both connections appear to originate from 203.0.113.1 (the NAT public IP) with different source ports.

6. Verify NAT translations:
   ```bash
   rnat conntrack -L 2>/dev/null || rnat cat /proc/net/nf_conntrack
   ```

**Expected Observations:**
- Private addresses (192.168.1.x) are never visible on the public side
- Each connection from different internal hosts uses a unique translated port
- The NAT table maintains bidirectional state for return traffic

**Verification:**
```powershell
python tests/test_exercises.py --exercise 1
```

### Exercise 2: SDN Topology and Flow Observation

**Objective:** Deploy an SDN topology with an OpenFlow controller and observe flow-based packet forwarding.

**Duration:** 35 minutes

**Background:** SDN separates the control plane (where forwarding decisions are made) from the data plane (where packets are actually forwarded). The controller installs flow rules in switches that define match-action pairs.

**Steps:**

1. Start the SDN topology with flow rules:
   ```powershell
   python scripts/run_demo.py --demo sdn
   ```

2. Examine the initial flow table:
   ```bash
   sh ovs-ofctl -O OpenFlow13 dump-flows s1
   ```

3. Test permitted connectivity (h1 ↔ h2):
   ```bash
   h1 ping -c 3 10.0.6.12
   h2 ping -c 3 10.0.6.11
   ```

4. Test blocked connectivity (h1 → h3):
   ```bash
   h1 ping -c 3 10.0.6.13
   ```

5. Observe the flow table again - note new entries for matched traffic:
   ```bash
   sh ovs-ofctl -O OpenFlow13 dump-flows s1
   ```

6. Analyse flow statistics:
   ```bash
   sh ovs-ofctl -O OpenFlow13 dump-flows s1 --rsort=n_packets
   ```

**Expected Observations:**
- h1 ↔ h2 traffic succeeds (flow rules permit)
- h1 → h3 ICMP traffic is dropped (specific drop rule)
- Flow entries show packet and byte counters increasing

**Verification:**
```powershell
python tests/test_exercises.py --exercise 2
```

### Exercise 3: SDN Policy Modification

**Objective:** Understand how SDN policies affect traffic by modifying flow rules dynamically.

**Duration:** 25 minutes

**Steps:**

1. With the SDN topology running, add a rule to permit ICMP from h1 to h3:
   ```bash
   sh ovs-ofctl -O OpenFlow13 add-flow s1 "priority=300,icmp,nw_src=10.0.6.11,nw_dst=10.0.6.13,actions=output:3"
   ```

2. Test connectivity again:
   ```bash
   h1 ping -c 3 10.0.6.13
   ```

3. Remove the rule and verify blocking resumes:
   ```bash
   sh ovs-ofctl -O OpenFlow13 del-flows s1 "priority=300,icmp,nw_src=10.0.6.11,nw_dst=10.0.6.13"
   h1 ping -c 3 10.0.6.13
   ```

4. Experiment with protocol-specific rules (TCP vs UDP):
   ```bash
   # Start TCP server on h3
   h3 python3 seminar/python/apps/tcp_echo.py server --bind 10.0.6.13 --port 9090 &
   
   # Try TCP connection from h1 (should be blocked by default)
   h1 python3 seminar/python/apps/tcp_echo.py client --dst 10.0.6.13 --port 9090 --message "Test"
   
   # Add TCP permit rule
   sh ovs-ofctl -O OpenFlow13 add-flow s1 "priority=300,tcp,nw_dst=10.0.6.13,actions=output:3"
   
   # Retry TCP connection
   h1 python3 seminar/python/apps/tcp_echo.py client --dst 10.0.6.13 --port 9090 --message "Test"
   ```

**Verification:**
```powershell
python tests/test_exercises.py --exercise 3
```

## Demonstrations

### Demo 1: NAT Translation Visualisation

Automated demonstration showing PAT in action with multiple simultaneous connections.

```powershell
python scripts/run_demo.py --demo nat-visual
```

**What to observe:**
- Real-time NAT table updates as connections are established
- Port allocation patterns for concurrent connections
- Connection state transitions (ESTABLISHED, TIME_WAIT)

### Demo 2: SDN Flow Installation

Demonstrates the controller-switch interaction during flow installation.

```powershell
python scripts/run_demo.py --demo sdn-flows
```

**What to observe:**
- Packet-in events sent to controller for unknown traffic
- Flow-mod messages installing new rules
- Subsequent packets matching installed flows (no controller involvement)

## Packet Capture and Analysis

### Capturing Traffic

```powershell
# Start capture for NAT topology
python scripts/capture_traffic.py --topology nat --output pcap/nat_capture.pcap

# Start capture for SDN topology
python scripts/capture_traffic.py --topology sdn --output pcap/sdn_capture.pcap
```

### Recommended Wireshark Filters

```
# NAT/PAT analysis
ip.addr == 203.0.113.1 && icmp
tcp.port == 5000

# SDN/OpenFlow analysis
openflow_v4
of13.type == 10  # Packet-in
of13.type == 14  # Flow-mod

# ARP traffic
arp

# ICMP traffic
icmp || icmpv6
```

### Opening Captures in Wireshark

The captured files are stored in the `pcap/` directory and can be opened directly in Wireshark on Windows.

## Shutdown and Cleanup

### End of Session

```powershell
# Stop all containers gracefully (preserves data)
python scripts/stop_lab.py

# Verify shutdown
docker ps
```

### Full Cleanup (Before Next Week)

```powershell
# Remove all containers, networks, and volumes for this week
python scripts/cleanup.py --full

# Verify cleanup
docker system df

# Optional: prune unused Docker resources
python scripts/cleanup.py --full --prune
```

## Homework Assignments

See the `homework/` directory for take-home exercises.

### Assignment 1: Extended NAT Analysis

Document the NAT translation process for the following scenario:
- Three internal hosts simultaneously connecting to the same external server
- Each host makes two connections (HTTP and HTTPS)
- Capture and analyse the NAT table state

**Deliverable:** `homework/exercises/hw_6_01_nat_analysis.md`

### Assignment 2: Custom SDN Policy Implementation

Design and implement an SDN policy that:
- Permits HTTP (port 80) and HTTPS (port 443) from all hosts to h3
- Blocks all ICMP to h3 except from h2
- Permits SSH (port 22) only from h1 to h2

**Deliverable:** `homework/exercises/hw_6_02_sdn_policy.py`

## Troubleshooting

### Common Issues

#### Issue: Mininet cleanup errors ("File exists")
**Solution:** Run cleanup with force flag:
```powershell
python scripts/cleanup.py --force
# Or manually in WSL:
sudo mn -c
```

#### Issue: OVS switch not connecting to controller
**Solution:** Verify controller is running and port is accessible:
```bash
ss -ltn | grep 6633
ovs-vsctl show
```

#### Issue: Docker containers fail to start in privileged mode
**Solution:** Ensure Docker Desktop is configured for WSL2 integration:
1. Open Docker Desktop Settings
2. Navigate to Resources > WSL Integration
3. Enable integration with your Ubuntu distribution

#### Issue: NAT not translating packets
**Solution:** Verify IP forwarding is enabled:
```bash
sysctl net.ipv4.ip_forward
# Should be 1; if not:
sudo sysctl -w net.ipv4.ip_forward=1
```

#### Issue: SDN topology pings are slow or timeout
**Solution:** Check if flow rules are installed:
```bash
ovs-ofctl -O OpenFlow13 dump-flows s1
```
If empty or only table-miss rule exists, the controller may not be functioning correctly.

See `docs/troubleshooting.md` for additional solutions.

## Theoretical Background

### NAT and PAT

Network Address Translation emerged as a response to IPv4 address exhaustion, enabling organisations to use private address ranges (RFC 1918: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) internally while sharing limited public addresses externally. Port Address Translation extends this by multiplexing connections through port numbers, allowing thousands of internal hosts to share a single public IP.

The translation process involves:
1. **Outbound:** Rewriting source IP (and port in PAT) to the NAT device's public address
2. **State tracking:** Maintaining a translation table mapping internal to external tuples
3. **Inbound:** Reverse translation using the stored state

### Software-Defined Networking

SDN represents a fundamental architectural shift from distributed to centralised network control. Key principles include:
1. **Separation of concerns:** Control logic (controller) distinct from forwarding (switches)
2. **Programmability:** Network behaviour defined through software APIs
3. **Centralised view:** Controller maintains global network state
4. **Flow-based forwarding:** Packets matched against rules and actions applied

OpenFlow provides the southbound interface between controller and switches, defining how flow tables are populated and queried.

## References

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- RFC 1918 – Address Allocation for Private Internets
- RFC 5737 – IPv4 Address Blocks Reserved for Documentation
- RFC 4861 – Neighbor Discovery for IP version 6 (IPv6)
- Open Networking Foundation (2015). *OpenFlow Switch Specification* Version 1.3.5

## Architecture Diagrams

### NAT Topology
```
    ┌─────────────────────────────────────────────────────────────┐
    │                    Private Network                          │
    │                    192.168.1.0/24                           │
    │                                                             │
    │   ┌───────────┐              ┌───────────┐                  │
    │   │    h1     │              │    h2     │                  │
    │   │.10        │              │.20        │                  │
    │   └─────┬─────┘              └─────┬─────┘                  │
    │         │                          │                        │
    │         └──────────┬───────────────┘                        │
    │                    │                                        │
    │              ┌─────┴─────┐                                   │
    │              │    s1     │                                   │
    │              └─────┬─────┘                                   │
    └────────────────────┼────────────────────────────────────────┘
                         │ eth0: 192.168.1.1
                   ┌─────┴─────┐
                   │   rnat    │  ← NAT/MASQUERADE
                   │  (router) │
                   └─────┬─────┘
                         │ eth1: 203.0.113.1
    ┌────────────────────┼────────────────────────────────────────┐
    │                    │                                        │
    │              ┌─────┴─────┐                                   │
    │              │    s2     │                                   │
    │              └─────┬─────┘                                   │
    │                    │                                        │
    │              ┌─────┴─────┐                                   │
    │              │    h3     │                                   │
    │              │.2         │                                   │
    │              └───────────┘                                   │
    │                                                             │
    │                    Public Network                           │
    │                    203.0.113.0/24 (TEST-NET-3)              │
    └─────────────────────────────────────────────────────────────┘
```

### SDN Topology
```
                          ┌─────────────────────────────┐
                          │      SDN Controller         │
                          │       (OS-Ken)              │
                          │                             │
                          │  ┌──────────────────────┐   │
                          │  │  Policy Engine       │   │
                          │  │  • h1↔h2: PERMIT     │   │
                          │  │  • *→h3: DROP        │   │
                          │  │  • UDP→h3: CONFIG    │   │
                          │  └──────────────────────┘   │
                          └─────────────┬───────────────┘
                                        │ OpenFlow 1.3
                                        │ (port 6633)
    ┌───────────────────────────────────┼───────────────────────────────────┐
    │                                   │                                   │
    │                           ┌───────┴───────┐                           │
    │                           │      s1       │                           │
    │                           │   (OVS)       │                           │
    │                           │               │                           │
    │                           │ ┌───────────┐ │                           │
    │                           │ │Flow Table │ │                           │
    │                           │ └───────────┘ │                           │
    │                           └───┬───┬───┬───┘                           │
    │                               │   │   │                               │
    │                    ┌──────────┘   │   └──────────┐                    │
    │                    │              │              │                    │
    │              ┌─────┴─────┐  ┌─────┴─────┐  ┌─────┴─────┐              │
    │              │    h1     │  │    h2     │  │    h3     │              │
    │              │10.0.6.11  │  │10.0.6.12  │  │10.0.6.13  │              │
    │              │           │  │           │  │           │              │
    │              │  [✓ FULL  │  │  [SERVER] │  │[RESTRICTED│              │
    │              │   ACCESS] │  │           │  │   ACCESS] │              │
    │              └───────────┘  └───────────┘  └───────────┘              │
    │                                                                       │
    │                        SDN Network: 10.0.6.0/24                       │
    └───────────────────────────────────────────────────────────────────────┘
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
