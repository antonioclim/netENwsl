# Week 5: Network Layer – IP Addressing, Subnetting, VLSM

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by Revolvix

## Overview

The network layer represents the cornerstone of internetworking, providing the fundamental mechanisms that enable communication across heterogeneous networks. This laboratory session delves into the intricacies of IPv4 and IPv6 addressing, examining how logical addresses are assigned, calculated and organised to create scalable network infrastructures.

Students will explore the mathematical foundations of subnetting through both Fixed Length Subnet Mask (FLSM) and Variable Length Subnet Mask (VLSM) techniques. The practical component employs Docker-based environments and Python tooling to simulate addressing scenarios, calculate network parameters and validate configuration correctness.

By mastering these concepts, students establish the prerequisite knowledge for understanding routing protocols, network address translation and the broader architecture of the global Internet.

## Learning Objectives

By the end of this laboratory session, you will be able to:

1. **Identify** the role and functions of the network layer within the OSI and TCP/IP reference models
2. **Explain** the structural differences between IPv4 and IPv6 header formats and addressing schemes
3. **Calculate** network addresses, broadcast addresses and usable host ranges from CIDR notation
4. **Apply** FLSM subnetting to partition networks into equal-sized segments
5. **Design** VLSM allocation schemes that optimise address space utilisation for heterogeneous requirements
6. **Evaluate** the efficiency and correctness of addressing schemes through programmatic validation

## Prerequisites

### Knowledge Requirements
- Understanding of OSI model layers and their functions
- Familiarity with binary number systems and bitwise operations
- Basic Python programming skills (functions, CLI arguments)
- Previous experience with Docker containers

### Software Requirements
- Windows 10/11 with WSL2 enabled
- Docker Desktop (WSL2 backend)
- Wireshark (native Windows)
- Python 3.11 or later
- Git

### Hardware Requirements
- Minimum 8GB RAM (16GB recommended)
- 10GB free disk space
- Network connectivity

## Quick Start

### First-Time Setup (Run Once)

```powershell
# Open PowerShell as Administrator
cd WEEK5_WSLkit

# Verify prerequisites
python setup/verify_environment.py

# If any issues, run the installer helper
python setup/install_prerequisites.py
```

### Starting the Laboratory

```powershell
# Start all services
python scripts/start_lab.py

# Verify everything is running
python scripts/start_lab.py --status
```

### Accessing Services

| Service | URL/Port | Credentials |
|---------|----------|-------------|
| Portainer | https://localhost:9443 | Set on first access |
| Python Container | Interactive shell | N/A |
| UDP Echo Server | localhost:9999/udp | N/A |

## Laboratory Exercises

### Exercise 1: CIDR Analysis and Binary Representation

**Objective:** Analyse IPv4 addresses with CIDR notation, calculating all network parameters and understanding binary representations.

**Duration:** 25 minutes

**Steps:**

1. Open a PowerShell terminal and navigate to the kit directory
2. Start the Docker environment:
   ```powershell
   python scripts/start_lab.py
   ```
3. Execute the CIDR analysis tool:
   ```powershell
   docker exec -it week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py analyze 192.168.10.14/26 --verbose
   ```
4. Observe the output, noting the network address, broadcast address and host range
5. Experiment with different prefix lengths:
   ```powershell
   docker exec -it week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py analyze 10.0.0.100/24
   docker exec -it week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py analyze 172.16.50.1/28
   ```
6. Examine the binary conversion:
   ```powershell
   docker exec -it week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py binary 192.168.10.14
   ```

**Verification:**
```powershell
python tests/test_exercises.py --exercise 1
```

### Exercise 2: FLSM Subnetting

**Objective:** Partition a network into equal-sized subnets using Fixed Length Subnet Mask technique.

**Duration:** 20 minutes

**Steps:**

1. Understand the scenario: Your organisation has been allocated 192.168.100.0/24 and requires 4 equal subnets
2. Calculate manually how many bits must be borrowed from the host portion
3. Verify your calculation using the FLSM tool:
   ```powershell
   docker exec -it week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py flsm 192.168.100.0/24 4
   ```
4. Observe the subnet boundaries, broadcast addresses and usable host counts
5. Try different scenarios:
   ```powershell
   docker exec -it week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py flsm 10.0.0.0/24 8
   docker exec -it week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py flsm 172.16.0.0/16 16
   ```

**Verification:**
```powershell
python tests/test_exercises.py --exercise 2
```

### Exercise 3: VLSM Allocation

**Objective:** Design an efficient addressing scheme using Variable Length Subnet Mask for heterogeneous requirements.

**Duration:** 30 minutes

**Steps:**

1. Consider the scenario: A company needs networks for 60 employees, 20 contractors, 10 servers and 2 point-to-point links
2. Available address space: 172.16.0.0/24
3. Understand why VLSM is more efficient than FLSM for this scenario
4. Execute the VLSM allocation:
   ```powershell
   docker exec -it week5_python python /app/src/exercises/ex_5_02_vlsm_ipv6.py vlsm 172.16.0.0/24 60 20 10 2
   ```
5. Analyse the efficiency percentages for each subnet
6. Try a more complex scenario:
   ```powershell
   docker exec -it week5_python python /app/src/exercises/ex_5_02_vlsm_ipv6.py vlsm 10.10.0.0/22 200 100 50 25 10 2 2 2
   ```

**Verification:**
```powershell
python tests/test_exercises.py --exercise 3
```

### Exercise 4: IPv6 Address Operations

**Objective:** Understand IPv6 address representation, compression rules and subnetting.

**Duration:** 25 minutes

**Steps:**

1. Explore IPv6 address types:
   ```powershell
   docker exec -it week5_python python /app/src/exercises/ex_5_02_vlsm_ipv6.py ipv6-types
   ```
2. Compress an expanded IPv6 address:
   ```powershell
   docker exec -it week5_python python /app/src/exercises/ex_5_02_vlsm_ipv6.py ipv6 2001:0db8:0000:0000:0000:0000:0000:0001
   ```
3. Expand a compressed address:
   ```powershell
   docker exec -it week5_python python /app/src/exercises/ex_5_02_vlsm_ipv6.py ipv6-expand 2001:db8::1
   ```
4. Generate IPv6 /64 subnets from a /48 allocation:
   ```powershell
   docker exec -it week5_python python /app/src/exercises/ex_5_02_vlsm_ipv6.py ipv6-subnets 2001:db8:10::/48 64 10
   ```

**Verification:**
```powershell
python tests/test_exercises.py --exercise 4
```

## Demonstrations

### Demo 1: Complete Addressing Workflow

Automated demonstration showcasing CIDR analysis, FLSM partitioning and VLSM allocation.

```powershell
python scripts/run_demo.py --demo 1
```

**What to observe:**
- How the same /24 network is partitioned differently with FLSM vs VLSM
- Efficiency comparisons between the two approaches
- Binary representation of network boundaries

### Demo 2: UDP Echo with Network Isolation

Demonstrates containerised network communication with explicit IP addressing.

```powershell
python scripts/run_demo.py --demo 2
```

**What to observe:**
- Container IP assignments within the 10.5.0.0/24 subnet
- UDP packet exchange between client and server containers
- Traffic patterns visible in packet captures

## Packet Capture and Analysis

### Capturing Traffic

```powershell
# Start capture in Docker network
python scripts/capture_traffic.py --interface eth0 --output pcap/week5_capture.pcap

# Or capture directly from UDP server container
docker exec week5_udp-server tcpdump -i eth0 -w /app/pcap/udp_traffic.pcap &
```

### Suggested Wireshark Filters

```
# Show only ICMP (ping) traffic
icmp

# Filter by specific subnet
ip.addr == 10.5.0.0/24

# UDP traffic on port 9999
udp.port == 9999

# IPv6 only
ipv6

# ICMPv6 (including Neighbour Discovery)
icmpv6
```

## Shutdown and Cleanup

### End of Session

```powershell
# Stop all containers (preserves data)
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
```

## Homework Assignments

See the `homework/` directory for take-home exercises.

### Assignment 1: Corporate Network Design
Design a VLSM addressing scheme for a medium enterprise with headquarters (500 users), two branch offices (150 and 80 users), DMZ servers (25) and point-to-point WAN links.

### Assignment 2: IPv6 Migration Planning
Given an existing IPv4 /22 network with 12 subnets, propose an equivalent IPv6 addressing plan using a /48 allocation, maintaining logical groupings.

## Troubleshooting

### Common Issues

#### Issue: Docker containers fail to start
**Solution:** Ensure Docker Desktop is running and WSL2 integration is enabled. Run `docker info` to verify.

#### Issue: Python module not found errors
**Solution:** Ensure you're executing commands from the correct directory. The container mounts expect the kit structure.

#### Issue: Cannot access UDP server from host
**Solution:** Check that port 9999/udp is properly mapped. Use `docker ps` to verify port bindings.

#### Issue: Wireshark cannot capture Docker traffic
**Solution:** On Windows, capture on the "Ethernet" or "Wi-Fi" interface. For container-internal traffic, use tcpdump within containers.

See `docs/troubleshooting.md` for more solutions.

## Theoretical Background

The network layer (Layer 3) provides end-to-end logical addressing and routing capabilities. Unlike data link layer addresses which have only local significance, network layer addresses enable communication across diverse physical networks.

**IPv4 Addressing**: 32-bit addresses expressed in dotted-decimal notation (e.g., 192.168.1.1). The address space is divided into network and host portions, with the boundary determined by the subnet mask or CIDR prefix.

**Subnetting**: The practice of dividing a network into smaller segments. FLSM creates equal-sized subnets, whilst VLSM allows variable sizes to match actual requirements, improving address utilisation efficiency.

**IPv6 Addressing**: 128-bit addresses expressed in hexadecimal colon notation. The vastly larger address space eliminates the need for NAT and supports hierarchical allocation. Standard subnet size is /64, providing 64 bits for the interface identifier.

## References

- Kurose, J. & Ross, K. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- RFC 791 – Internet Protocol (IPv4)
- RFC 8200 – Internet Protocol, Version 6 (IPv6)
- RFC 1918 – Address Allocation for Private Internets
- RFC 4291 – IP Version 6 Addressing Architecture

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                    Docker Network: labnet                        │
│                    Subnet: 10.5.0.0/24                          │
│                    Gateway: 10.5.0.1                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   python     │    │  udp-server  │    │  udp-client  │       │
│  │  10.5.0.10   │    │  10.5.0.20   │    │  10.5.0.30   │       │
│  │              │    │  :9999/udp   │    │              │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                             ▲                    │               │
│                             │    UDP Echo        │               │
│                             └────────────────────┘               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
