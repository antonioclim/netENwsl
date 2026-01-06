# Week 3: Introduction to Network Programming

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
> 
> by Revolvix

## Overview

This laboratory introduces the fundamental concepts and practical techniques of network programming using Python sockets. The session focuses on three essential communication paradigms that form the backbone of distributed systems: UDP broadcast, UDP multicast, and TCP tunnelling.

UDP broadcast represents the simplest form of one-to-many communication, where a single transmission reaches all hosts within a Layer 2 broadcast domain. While straightforward to implement, broadcast communication is inherently limited to local network segments and generates traffic that all hosts must process, making it suitable primarily for service discovery and local announcements.

UDP multicast provides a more sophisticated approach to group communication, allowing selective delivery to hosts that have explicitly joined a multicast group. This mechanism reduces network overhead compared to broadcast while enabling efficient one-to-many delivery across routed networks when IGMP (Internet Group Management Protocol) is properly configured.

TCP tunnelling (port forwarding) demonstrates how to create a relay point that bridges connections between network segments. This technique is foundational for understanding proxy servers, NAT traversal, and the construction of overlay networks. The tunnel accepts incoming TCP connections and establishes corresponding outbound connections to a target server, forwarding data bidirectionally.

## Learning Objectives

By the end of this laboratory session, you will be able to:

1. **Recall** the fundamental differences between unicast, broadcast, and multicast addressing at the IP layer, and identify the socket options required for each communication mode
2. **Explain** why broadcast is constrained to Layer 2 domains while multicast can traverse routers when IGMP is enabled, and describe the role of TTL in multicast propagation
3. **Implement** functional UDP broadcast and multicast senders and receivers using Python's socket library, correctly configuring SO_BROADCAST and multicast group membership
4. **Construct** a TCP tunnel that accepts connections on one port and forwards traffic bidirectionally to a target server, using threading for full-duplex communication
5. **Analyse** captured network traffic using tcpdump and Wireshark, identifying UDP datagrams, IGMP membership reports, and TCP three-way handshakes
6. **Evaluate** the appropriateness of broadcast, multicast, and unicast for different application scenarios, considering factors such as network topology, scalability, and reliability requirements

## Prerequisites

### Knowledge Requirements

Before beginning this laboratory, you should be familiar with:
- OSI and TCP/IP reference models (covered in Week 2)
- Fundamental differences between TCP and UDP transport protocols
- Basic Python programming including functions, classes, and exception handling
- Command-line navigation in Linux environments
- IP addressing and subnetting concepts

### Software Requirements

The following software must be installed and configured:
- Windows 10/11 with WSL2 enabled (Ubuntu 22.04 recommended)
- Docker Desktop for Windows (WSL2 backend)
- Wireshark for Windows (native application)
- Python 3.11 or later
- Git for version control

### Hardware Requirements

Minimum specifications for comfortable operation:
- 8GB RAM (16GB recommended for concurrent containers)
- 10GB free disk space for Docker images and captures
- Dual-core processor (quad-core recommended)
- Stable network connectivity for package installation

## Quick Start

### First-Time Setup (Run Once)

Open PowerShell as Administrator and execute:

```powershell
# Navigate to the kit directory
cd WEEK3_WSLkit

# Verify all prerequisites are installed
python setup/verify_environment.py

# If any checks fail, run the installer helper
python setup/install_prerequisites.py

# Configure Docker for optimal performance
python setup/configure_docker.py
```

### Starting the Laboratory

```powershell
# Start all Docker containers
python scripts/start_lab.py

# Verify services are running correctly
python scripts/start_lab.py --status

# View container logs (optional)
docker compose -f docker/docker-compose.yml logs -f
```

### Accessing Services

| Service | Address | Purpose |
|---------|---------|---------|
| Portainer | https://localhost:9443 | Container management interface |
| Echo Server | localhost:8080 | TCP echo service on server container |
| TCP Tunnel | localhost:9090 | Forwards to server:8080 via router |
| Client Shell | docker exec -it week3_client bash | Interactive testing environment |

## Laboratory Exercises

### Exercise 1: UDP Broadcast Communication

**Objective:** Implement and observe UDP broadcast transmission within a Layer 2 domain, understanding the SO_BROADCAST socket option and the behaviour of limited broadcast addresses.

**Duration:** 30 minutes

**Theory:** UDP broadcast sends datagrams to all hosts on a network segment. The address 255.255.255.255 represents a "limited broadcast" that never crosses routers, while directed broadcasts (e.g., 172.20.0.255) target specific subnets. The operating system kernel requires explicit permission via the SO_BROADCAST socket option before allowing broadcast transmissions.

**Steps:**

1. Access the client container:
```bash
docker exec -it week3_client bash
```

2. In a separate terminal, start a broadcast receiver:
```bash
docker exec -it week3_client python3 python/examples/ex01_udp_broadcast.py recv --port 5007 --count 5
```

3. In another terminal, start a second receiver on the receiver container:
```bash
docker exec -it week3_receiver python3 python/examples/ex01_udp_broadcast.py recv --port 5007 --count 5
```

4. Send broadcast datagrams from the client:
```bash
docker exec -it week3_client python3 python/examples/ex01_udp_broadcast.py send --dst 255.255.255.255 --port 5007 --count 5 --interval 1
```

5. Observe that both receivers display the same messages

**Verification:**
```powershell
python tests/test_exercises.py --exercise 1
```

**Expected Observations:**
- Both receivers display incoming datagrams with identical content
- The source port varies (ephemeral port selection)
- The destination address in the receiver output shows the sender's IP

### Exercise 2: UDP Multicast Communication

**Objective:** Configure multicast group membership using IGMP and observe selective delivery to subscribed receivers only.

**Duration:** 35 minutes

**Theory:** Multicast addresses in the range 224.0.0.0 to 239.255.255.255 identify groups rather than individual hosts. A host joins a multicast group by sending an IGMP Membership Report, instructing network equipment to forward group traffic to its interface. The IP_ADD_MEMBERSHIP socket option triggers this process.

**Steps:**

1. Start a multicast receiver on the client container:
```bash
docker exec -it week3_client python3 python/examples/ex02_udp_multicast.py recv --group 239.1.1.1 --port 5008 --count 5
```

2. Start a second receiver on the receiver container:
```bash
docker exec -it week3_receiver python3 python/examples/ex02_udp_multicast.py recv --group 239.1.1.1 --port 5008 --count 5
```

3. Send multicast datagrams from the server:
```bash
docker exec -it week3_server python3 python/examples/ex02_udp_multicast.py send --group 239.1.1.1 --port 5008 --count 5 --ttl 4
```

4. Capture IGMP traffic to observe group membership:
```bash
docker exec -it week3_client tcpdump -i eth0 igmp -c 5
```

**Verification:**
```powershell
python tests/test_exercises.py --exercise 2
```

**Expected Observations:**
- IGMP Membership Report messages when receivers join the group
- Only containers that joined the group receive the multicast datagrams
- TTL value determines how many router hops the multicast can traverse

### Exercise 3: TCP Tunnel (Port Forwarding)

**Objective:** Construct and analyse a TCP tunnel that relays connections between endpoints, understanding bidirectional forwarding and the proxy pattern.

**Duration:** 40 minutes

**Theory:** A TCP tunnel acts as an intermediary, accepting connections on one socket and establishing corresponding connections to a target server. Data flows bidirectionally between the client and server through the tunnel. This pattern forms the basis for reverse proxies, SSH tunnelling, and NAT traversal solutions.

**Steps:**

1. Verify the echo server is running:
```bash
docker exec -it week3_client bash -c "echo 'DIRECT TEST' | nc server 8080"
```

2. Test the tunnel by connecting through the router:
```bash
docker exec -it week3_client bash -c "echo 'TUNNEL TEST' | nc router 9090"
```

3. Start a packet capture on the router to observe both connections:
```bash
docker exec -it week3_router tcpdump -i eth0 -w /tmp/tunnel.pcap tcp port 8080 or tcp port 9090 &
```

4. Send multiple messages through the tunnel:
```bash
docker exec -it week3_client bash -c "for i in 1 2 3 4 5; do echo 'Message $i' | nc router 9090 -w 1; done"
```

5. Retrieve and analyse the capture:
```bash
docker cp week3_router:/tmp/tunnel.pcap ./pcap/tunnel_exercise.pcap
```

**Verification:**
```powershell
python tests/test_exercises.py --exercise 3
```

**Expected Observations:**
- Two separate TCP connections visible in the capture: client→router and router→server
- The tunnel logs show bidirectional data transfer for each client connection
- Echo responses return through the same path

### Exercise 4: Protocol Analysis with Wireshark

**Objective:** Capture and interpret network traffic to identify protocol headers, sequence numbers, and connection states.

**Duration:** 25 minutes

**Steps:**

1. Start Wireshark on Windows and select the Docker network interface

2. Apply the capture filter:
```
host 172.20.0.10 or host 172.20.0.100
```

3. Execute the broadcast, multicast, and tunnel demos sequentially:
```powershell
python scripts/run_demo.py --demo all
```

4. In Wireshark, apply display filters to isolate traffic types:
```
# UDP broadcast
udp.port == 5007

# UDP multicast
ip.dst == 239.1.1.1

# TCP tunnel connections
tcp.port == 9090 or tcp.port == 8080
```

5. For TCP connections, right-click and select "Follow TCP Stream" to view the conversation

**Expected Observations:**
- UDP datagrams lack sequence numbers or acknowledgements
- TCP shows SYN, SYN-ACK, ACK handshake before data transfer
- Multicast destination addresses begin with 239.x.x.x
- Broadcast frames have destination 255.255.255.255 or subnet broadcast

## Demonstrations

### Demo 1: Broadcast Propagation

Automated demonstration showing broadcast within the Docker network segment.

```powershell
python scripts/run_demo.py --demo broadcast
```

**What to observe:**
- All containers on the network receive the broadcast
- The router does not forward broadcast to other segments
- SO_BROADCAST permission error if the option is not set

### Demo 2: Multicast Group Dynamics

Demonstrates multicast group join/leave and selective delivery.

```powershell
python scripts/run_demo.py --demo multicast
```

**What to observe:**
- IGMP messages when receivers join/leave the group
- Only subscribed receivers display the multicast data
- TTL expiration prevents multicast from reaching distant segments

### Demo 3: TCP Tunnel Relay

Shows complete tunnel operation with logging.

```powershell
python scripts/run_demo.py --demo tunnel
```

**What to observe:**
- Connection acceptance on the tunnel listen port
- Establishment of outbound connection to target
- Bidirectional data flow logged by the tunnel
- Clean connection teardown in both directions

## Packet Capture and Analysis

### Capturing Traffic

Using the helper script:
```powershell
python scripts/capture_traffic.py --interface eth0 --output pcap/week3_capture.pcap --duration 60
```

Using tcpdump directly in containers:
```bash
docker exec -it week3_client tcpdump -i eth0 -w /app/capture.pcap -c 100
```

### Suggested Wireshark Filters

```
# All UDP traffic on demo ports
udp.port >= 5000 and udp.port <= 5100

# Broadcast traffic only
eth.dst == ff:ff:ff:ff:ff:ff

# Multicast group 239.1.1.1
ip.dst == 239.1.1.1

# IGMP protocol messages
igmp

# TCP tunnel traffic
tcp.port == 9090 or tcp.port == 8080

# TCP SYN packets (connection attempts)
tcp.flags.syn == 1 and tcp.flags.ack == 0

# Retransmissions (useful for debugging)
tcp.analysis.retransmission
```

## Shutdown and Cleanup

### End of Session

Graceful shutdown preserving data:
```powershell
# Stop all containers
python scripts/stop_lab.py

# Verify shutdown
docker ps

# View logs before stopping (optional)
docker compose -f docker/docker-compose.yml logs --tail=50
```

### Full Cleanup (Before Next Week)

Complete removal for fresh start:
```powershell
# Remove containers, networks, and volumes
python scripts/cleanup.py --full

# Verify cleanup
docker system df

# Prune unused Docker resources (optional)
python scripts/cleanup.py --full --prune
```

## Homework Assignments

See the `homework/` directory for detailed instructions.

### Assignment 1: Enhanced Broadcast Receiver

Extend the broadcast receiver to log statistics including packet count, bytes received, and source distribution. Implement a timeout mechanism that terminates reception after a configurable period of inactivity.

### Assignment 2: Multicast Chat Application

Design a simple chat application where multiple clients join a multicast group and exchange messages. Each client should display messages from others with sender identification. Consider how to handle the "loopback" problem where a sender receives its own messages.

### Assignment 3: TCP Tunnel with Logging

Modify the TCP tunnel to write a detailed log file containing timestamps, connection IDs, direction, and byte counts. Add support for multiple concurrent tunnels to different targets.

## Troubleshooting

### Common Issues

#### Issue: "Permission denied" when sending broadcast
**Solution:** Ensure SO_BROADCAST is set on the socket before calling sendto(). On some systems, elevated privileges may be required. Verify with:
```python
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
```

#### Issue: Multicast not received by other containers
**Solution:** Check that all receivers have joined the same multicast group and that the interface binding is correct. Verify IGMP is not blocked by firewall rules. Increase TTL if crossing network segments:
```bash
docker exec -it week3_client sysctl net.ipv4.icmp_echo_ignore_broadcasts
```

#### Issue: TCP tunnel connection refused
**Solution:** Confirm the target server is running and listening on the expected port. Check that the tunnel has network connectivity to the target. Verify with:
```bash
docker exec -it week3_router nc -zv server 8080
```

#### Issue: Docker containers cannot communicate
**Solution:** Ensure all containers are on the same Docker network. Check with:
```bash
docker network inspect week3_network
```

#### Issue: Wireshark cannot see Docker traffic
**Solution:** On Windows, capture on the "vEthernet (WSL)" adapter or use tcpdump inside containers and copy the pcap file out for analysis.

See `docs/troubleshooting.md` for additional solutions.

## Theoretical Background

### UDP Socket Programming

UDP (User Datagram Protocol) provides connectionless, unreliable delivery of datagrams. Key characteristics relevant to this laboratory:

The absence of connection state means each datagram is independent. The sendto() function specifies the destination for each transmission, while recvfrom() returns the source address along with the received data. There is no built-in mechanism for ordering, duplicate detection, or acknowledgement.

Socket options modify behaviour: SO_BROADCAST enables transmission to broadcast addresses, SO_REUSEADDR permits immediate reuse of a local address after socket closure, and IP_ADD_MEMBERSHIP subscribes to a multicast group.

### TCP Connection Forwarding

TCP tunnelling involves maintaining two simultaneous connections and forwarding data between them. The pattern requires:

A listening socket that accepts incoming client connections. For each accepted connection, a new outbound connection to the target server. Two concurrent data flows: client-to-target and target-to-client. Proper shutdown handling when either side closes the connection.

Threading or asynchronous I/O enables full-duplex operation where data can flow in both directions simultaneously.

### Broadcast vs Multicast

Broadcast transmissions reach all hosts on a Layer 2 segment regardless of interest. The address 255.255.255.255 is a "limited broadcast" confined to the local network, while directed broadcasts (subnet.255) are typically blocked by routers.

Multicast delivers only to hosts that have explicitly joined the group via IGMP. This selective delivery reduces wasted bandwidth and processing on uninterested hosts. Multicast can traverse routers when multicast routing protocols (DVMRP, PIM) are configured.

## References

- Kurose, J. F. & Ross, K. W. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson. Chapters 3 and 4.
- Rhodes, B. & Goerzen, J. (2014). *Foundations of Python Network Programming* (3rd ed.). Apress. Chapters 2 and 3.
- Stevens, W. R., Fenner, B. & Rudoff, A. M. (2004). *UNIX Network Programming, Volume 1: The Sockets Networking API* (3rd ed.). Addison-Wesley.
- RFC 1112 - Host Extensions for IP Multicasting
- RFC 2236 - Internet Group Management Protocol, Version 2
- Python Documentation: socket — Low-level networking interface

## Architecture Diagram

```
                         WEEK 3 NETWORK TOPOLOGY
    ╔════════════════════════════════════════════════════════════════╗
    ║                     Docker Network: 172.20.0.0/24              ║
    ╠════════════════════════════════════════════════════════════════╣
    ║                                                                ║
    ║   ┌─────────────┐         ┌─────────────┐                      ║
    ║   │   SERVER    │         │   ROUTER    │                      ║
    ║   │ 172.20.0.10 │◄───────►│172.20.0.254 │                      ║
    ║   │             │         │             │                      ║
    ║   │ Echo :8080  │         │ Tunnel :9090│                      ║
    ║   └─────────────┘         └──────┬──────┘                      ║
    ║                                  │                             ║
    ║                                  │                             ║
    ║   ┌─────────────┐         ┌──────┴──────┐                      ║
    ║   │  RECEIVER   │         │   CLIENT    │                      ║
    ║   │172.20.0.101 │◄───────►│ 172.20.0.100│                      ║
    ║   │             │         │             │                      ║
    ║   │ Bcast :5007 │         │  Interactive│                      ║
    ║   └─────────────┘         └─────────────┘                      ║
    ║                                                                ║
    ╠════════════════════════════════════════════════════════════════╣
    ║  Broadcast: 172.20.0.255 or 255.255.255.255                    ║
    ║  Multicast: 239.1.1.1 (example group)                          ║
    ║  Gateway: 172.20.0.1 (Docker bridge)                           ║
    ╚════════════════════════════════════════════════════════════════╝
    
    Data Flow (TCP Tunnel):
    
    Client ──TCP:9090──► Router (Tunnel) ──TCP:8080──► Server (Echo)
           ◄────────────────────────────◄────────────────────────
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
