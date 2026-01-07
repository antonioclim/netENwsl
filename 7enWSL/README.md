# Week 7: Packet Interception, Filtering and Defensive Port Probing

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
> 
> by Revolvix

## Overview

This laboratory session explores the practical foundations of network traffic observation and policy enforcement at the packet level. The week builds upon your understanding of TCP/IP fundamentals and socket programming, introducing the critical skill of capturing and analysing real network traffic as forensic evidence. You will learn to distinguish between application-layer behaviour and network-layer phenomena, a distinction that proves essential when debugging distributed systems in production environments.

The seminar component focuses on packet filtering and defensive port probing techniques. Filtering rules transform abstract security policies into concrete, enforceable decisions at the network boundary. Rather than treating firewalls as opaque infrastructure, you will construct and verify filtering rules programmatically, understanding exactly why a connection succeeds or fails. This approach prepares you for container networking, reverse proxies and incident response scenarios covered in subsequent weeks.

All exercises operate within an isolated laboratory network created by Docker containers or Mininet topologies. The kit emphasises reproducibility: every observation you make should be backed by packet captures and logs that another engineer could verify independently.

## Learning Objectives

By the end of this laboratory session, you will be able to:

1. **Identify** TCP and UDP packet fields in captured traffic using tcpdump and Wireshark filters
2. **Explain** the difference between application-layer failures and network-layer filtering effects using concrete packet evidence
3. **Implement** IP-based allow and block filtering rules using iptables profiles and verify their effect with repeatable tests
4. **Analyse** packet captures to determine root causes of connection timeouts, resets and drops
5. **Design** custom firewall profiles that enforce specific traffic policies whilst maintaining baseline connectivity
6. **Evaluate** the trade-offs between DROP and REJECT filtering actions for debugging and security purposes

## Prerequisites

### Knowledge Requirements

- TCP three-way handshake mechanics (SYN, SYN-ACK, ACK)
- UDP connectionless transmission model
- IPv4 addressing and basic subnetting (covered in Week 5)
- Socket programming fundamentals from Weeks 2-4
- Basic command-line proficiency

### Software Requirements

- Windows 10/11 with WSL2 enabled
- Docker Desktop (WSL2 backend)
- Wireshark (native Windows installation)
- Python 3.11 or later
- Git (recommended)

### Hardware Requirements

- Minimum 8GB RAM (16GB recommended)
- 10GB free disk space
- Network connectivity for initial setup

## Quick Start

### First-Time Setup (Run Once)

```powershell
# Open PowerShell as Administrator
cd WEEK7_WSLkit

# Verify prerequisites
python setup/verify_environment.py

# If any issues, run the installer helper
python setup/install_prerequisites.py

# Configure Docker for this week's requirements
python setup/configure_docker.py
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
| TCP Echo Server | localhost:9090 | None |
| UDP Echo Receiver | localhost:9091 | None |
| Packet Filter Proxy | localhost:8888 | None (when enabled) |

## Laboratory Exercises

### Exercise 1: Baseline Traffic Capture

**Objective:** Establish baseline TCP and UDP connectivity and capture evidence of successful communication.

**Duration:** 20 minutes

**Steps:**

1. Start the laboratory environment:
   ```powershell
   python scripts/start_lab.py
   ```

2. In a separate terminal, begin traffic capture:
   ```powershell
   python scripts/capture_traffic.py --interface any --output pcap/ex1_baseline.pcap --duration 60
   ```

3. Run the baseline demonstration:
   ```powershell
   python scripts/run_demo.py --demo baseline
   ```

4. Examine the captured traffic using Wireshark:
   - Open `pcap/ex1_baseline.pcap`
   - Apply filter: `tcp.port == 9090`
   - Identify the three-way handshake (SYN, SYN-ACK, ACK)
   - Locate the echo request and response payloads

5. Repeat for UDP traffic:
   - Apply filter: `udp.port == 9091`
   - Note the absence of connection establishment overhead

**Verification:**
```powershell
python tests/test_exercises.py --exercise 1
```

**Expected Observations:**
- TCP stream shows complete handshake before data transfer
- UDP packets appear immediately without setup phase
- Both protocols successfully echo the test message

### Exercise 2: TCP Filtering with REJECT

**Objective:** Apply a filtering rule that blocks TCP connections to port 9090 and observe the client-side failure mode.

**Duration:** 25 minutes

**Steps:**

1. Ensure the baseline is working:
   ```powershell
   python scripts/run_demo.py --demo baseline
   ```

2. Apply the TCP blocking profile:
   ```powershell
   python src/apps/firewallctl.py --profile block_tcp_9090 --dry-run
   python src/apps/firewallctl.py --profile block_tcp_9090
   ```

3. Capture traffic whilst testing the blocked connection:
   ```powershell
   python scripts/capture_traffic.py --output pcap/ex2_tcp_blocked.pcap --duration 30
   ```

4. In another terminal, attempt the TCP connection:
   ```powershell
   python src/apps/tcp_client.py --host localhost --port 9090 --message "blocked_test" --timeout 5
   ```

5. Stop the capture and analyse in Wireshark:
   - Look for ICMP "Destination Unreachable" or TCP RST packets
   - Compare the timing to the baseline capture

6. Verify UDP still works:
   ```powershell
   python scripts/run_demo.py --demo udp_only
   ```

**Verification:**
```powershell
python tests/test_exercises.py --exercise 2
```

**Expected Observations:**
- Client receives immediate feedback (connection refused)
- ICMP or RST packets visible in the capture
- UDP traffic unaffected by the TCP rule

### Exercise 3: UDP Filtering with DROP

**Objective:** Apply a DROP rule to UDP port 9091 and contrast the failure mode with REJECT.

**Duration:** 25 minutes

**Steps:**

1. Restore baseline first:
   ```powershell
   python src/apps/firewallctl.py --profile baseline
   ```

2. Apply the UDP drop profile:
   ```powershell
   python src/apps/firewallctl.py --profile block_udp_9091
   ```

3. Capture and test:
   ```powershell
   python scripts/capture_traffic.py --output pcap/ex3_udp_dropped.pcap --duration 30
   ```

4. Attempt UDP communication:
   ```powershell
   python src/apps/udp_sender.py --host localhost --port 9091 --message "dropped_test" --count 3
   ```

5. Observe the receiver timeout behaviour and capture contents

**Verification:**
```powershell
python tests/test_exercises.py --exercise 3
```

**Key Questions:**
- How does the client behave differently with DROP vs REJECT?
- What packet evidence distinguishes a dropped packet from a lost packet?
- Which approach is better for debugging? For security?

### Exercise 4: Application-Layer Packet Filter

**Objective:** Use the user-space packet filter proxy to implement allow/block lists at the application layer.

**Duration:** 30 minutes

**Steps:**

1. Start the TCP server on port 9090:
   ```powershell
   python src/apps/tcp_server.py --host 0.0.0.0 --port 9090 --log artifacts/tcp_server.log
   ```

2. Start the packet filter proxy:
   ```powershell
   python src/apps/packet_filter.py --listen-port 8888 --upstream-host localhost --upstream-port 9090 --log artifacts/proxy.log
   ```

3. Test connectivity through the proxy:
   ```powershell
   python src/apps/tcp_client.py --host localhost --port 8888 --message "via_proxy"
   ```

4. Add an allow list (blocks all other sources):
   ```powershell
   python src/apps/packet_filter.py --listen-port 8888 --upstream-host localhost --upstream-port 9090 --allow 127.0.0.1 --log artifacts/proxy_filtered.log
   ```

5. Test from different source addresses (if available) and observe the proxy logs

**Verification:**
```powershell
python tests/test_exercises.py --exercise 4
```

### Exercise 5: Defensive Port Probing

**Objective:** Use controlled port probing to verify which services are accessible and which are filtered.

**Duration:** 20 minutes

**Steps:**

1. Configure a mixed filtering profile:
   ```powershell
   python src/apps/firewallctl.py --profile mixed_filtering
   ```

2. Run the port probe:
   ```powershell
   python src/apps/port_probe.py --host localhost --ports 22,80,443,8080,9090,9091 --timeout 1 --log artifacts/probe_results.log
   ```

3. Compare probe results against the applied profile
4. Document which ports appear open, closed, or filtered

**Verification:**
```powershell
python tests/test_exercises.py --exercise 5
```

## Demonstrations

### Demo 1: Complete Traffic Flow

Automated demonstration showing baseline connectivity, TCP filtering and UDP filtering in sequence.

```powershell
python scripts/run_demo.py --demo full
```

**What to observe:**
- Console output indicating success/failure at each stage
- Log files generated in `artifacts/`
- Packet capture showing all traffic types

### Demo 2: REJECT vs DROP Comparison

Side-by-side comparison of client behaviour under different filtering actions.

```powershell
python scripts/run_demo.py --demo reject_vs_drop
```

**What to observe:**
- Timing differences in client failure responses
- Packet evidence of each filtering mode

## Packet Capture and Analysis

### Capturing Traffic

```powershell
# Start capture with automatic duration
python scripts/capture_traffic.py --interface any --output pcap/week7_capture.pcap --duration 120

# Or use Wireshark directly on Windows
# Open Wireshark > Select appropriate interface > Start capture
```

### Suggested Wireshark Filters

```
# TCP traffic to echo server
tcp.port == 9090

# UDP traffic to receiver
udp.port == 9091

# TCP connection attempts (SYN packets)
tcp.flags.syn == 1 && tcp.flags.ack == 0

# Reset packets (indicating rejection)
tcp.flags.reset == 1

# ICMP unreachable messages
icmp.type == 3

# All traffic between specific hosts
ip.addr == 10.0.7.11 && ip.addr == 10.0.7.200
```

### tshark Command-Line Analysis

```bash
# Conversation summary
tshark -r pcap/week7_capture.pcap -q -z conv,tcp

# Field extraction
tshark -r pcap/week7_capture.pcap -Y "tcp.port==9090" -T fields -e frame.time -e ip.src -e ip.dst -e tcp.flags -e tcp.len

# Packet count
tshark -r pcap/week7_capture.pcap -Y "udp.port==9091" | wc -l
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

### Assignment 1: Custom Filtering Profile

Create a new firewall profile that blocks TCP port 9090 only from a specific source IP whilst allowing all other sources. Document your approach and provide packet capture evidence.

**Deliverables:** Modified `firewall_profiles.json`, capture file, short explanation (half page)

### Assignment 2: Failure Analysis Report

Take one filtering scenario (TCP blocked or UDP dropped) and write a structured analysis including: expected behaviour, observed packets (5-10 tshark lines), root cause explanation, and recommendations for automated verification.

**Deliverables:** Markdown report, supporting capture file

## Troubleshooting

### Common Issues

#### Issue: Docker containers fail to start
**Solution:** Ensure Docker Desktop is running and WSL2 integration is enabled. Run `docker info` to verify. If issues persist, restart Docker Desktop.

#### Issue: Wireshark cannot capture Docker traffic
**Solution:** On Windows, capture on the `vEthernet (WSL)` interface or use tcpdump inside WSL2 and copy captures out.

#### Issue: TCP client hangs instead of failing quickly
**Solution:** Verify you are using REJECT (not DROP) in your filtering profile. Use `--timeout` flag on the client.

#### Issue: Permission denied when applying iptables rules
**Solution:** Run inside a privileged container or use `sudo` in WSL2. The Docker-based exercises handle this automatically.

#### Issue: UDP receiver shows nothing
**Solution:** Ensure the receiver starts before the sender. Check destination IP and port match exactly.

See `docs/troubleshooting.md` for additional solutions.

## Theoretical Background

### Packet Capture as Evidence

When distributed systems misbehave, application logs may be incomplete or misleading. Packet captures provide ground truth: they show exactly what crossed the wire, including retransmissions, resets and ICMP errors that applications might not log. This week's exercises establish the habit of capturing evidence before concluding that code is at fault.

### Filtering Semantics

Network filtering transforms security policies into concrete decisions at packet boundaries. The key distinction is between:

- **REJECT:** Send an explicit refusal (TCP RST or ICMP Unreachable), providing fast feedback
- **DROP:** Silently discard the packet, forcing timeouts that can mask the true cause

For debugging, REJECT is preferable. For security (concealing service existence), DROP may be appropriate.

### Reproducibility

A firewall rule should be readable (what does it do), testable (how do we verify it), and reversible (how do we undo it safely). This week's profile-based approach demonstrates declarative policy management suitable for automation.

## References

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- Bejtlich, R. (2013). *The Practice of Network Security Monitoring*. No Starch Press.
- *iptables(8)* - Linux Netfilter administration manual page
- *tcpdump(1)* - Network packet analyser manual page

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        WEEK 7 Laboratory Topology                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────┐                           ┌─────────────────┐        │
│   │   TCP Client    │                           │   TCP Server    │        │
│   │   (src/apps/)   │                           │   Port 9090     │        │
│   └────────┬────────┘                           └────────┬────────┘        │
│            │                                             │                  │
│            │         ┌───────────────────┐              │                  │
│            │         │  Packet Filter    │              │                  │
│            ├────────▶│  Proxy (8888)     │─────────────▶│                  │
│            │         │  (Optional)       │              │                  │
│            │         └───────────────────┘              │                  │
│            │                                             │                  │
│   ┌────────┴────────────────────────────────────────────┴────────┐        │
│   │                     Docker Network (week7net)                 │        │
│   │                         10.0.7.0/24                           │        │
│   └───────────────────────────────────────────────────────────────┘        │
│            │                                             │                  │
│   ┌────────┴────────┐                           ┌────────┴────────┐        │
│   │   UDP Sender    │                           │   UDP Receiver  │        │
│   │   (src/apps/)   │──────────────────────────▶│   Port 9091     │        │
│   └─────────────────┘                           └─────────────────┘        │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                     Filtering Layer                              │      │
│   │   iptables FORWARD chain (applied on router/firewall host)      │      │
│   │   Profiles: baseline | block_tcp_9090 | block_udp_9091          │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
