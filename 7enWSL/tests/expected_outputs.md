# Expected Outputs for Week 7 Exercises

> NETWORKING class - ASE, Informatics | by Revolvix

This document describes the expected outputs and observable behaviours for each exercise in Week 7.

## Exercise 1: Baseline Connectivity and Capture

### Expected Terminal Output

```
[2026-01-XX HH:MM:SS] INFO: Starting baseline connectivity test
[2026-01-XX HH:MM:SS] INFO: Testing TCP connection to 10.0.7.100:9090
[2026-01-XX HH:MM:SS] INFO: TCP connection successful
[2026-01-XX HH:MM:SS] INFO: Echo test: sent 'hello', received 'hello'
[2026-01-XX HH:MM:SS] INFO: Testing UDP to 10.0.7.200:9091
[2026-01-XX HH:MM:SS] INFO: UDP datagram sent successfully
[2026-01-XX HH:MM:SS] INFO: All baseline tests passed
```

### Expected Wireshark Observations

With filter `tcp.port == 9090`:
1. TCP SYN packet (client → server)
2. TCP SYN-ACK packet (server → client)
3. TCP ACK packet (client → server)
4. TCP PSH-ACK with data (echo message)
5. TCP response with echoed data
6. TCP FIN sequence for connection close

With filter `udp.port == 9091`:
1. UDP datagram (sender → receiver)
2. UDP response (if receiver is configured to respond)

## Exercise 2: TCP Filtering with REJECT

### Expected Terminal Output

```
[2026-01-XX HH:MM:SS] INFO: Applying firewall profile: block_tcp_9090
[2026-01-XX HH:MM:SS] INFO: Testing TCP connection to 10.0.7.100:9090
[2026-01-XX HH:MM:SS] WARN: Connection refused (errno 111)
[2026-01-XX HH:MM:SS] INFO: TCP correctly blocked with REJECT
```

### Expected Wireshark Observations

With filter `tcp.port == 9090`:
1. TCP SYN packet (client → server)
2. TCP RST packet (immediate response) **← Key indicator of REJECT**
3. No retransmissions (connection fails immediately)

Alternative with ICMP:
1. TCP SYN packet
2. ICMP Destination Unreachable (Type 3, Code 3: Port Unreachable)

### Distinguishing REJECT from Service Down

| Indicator | REJECT | Service Down |
|-----------|--------|--------------|
| Response time | Immediate (<10ms) | Immediate |
| Response type | RST or ICMP | RST from kernel |
| Pattern | Consistent | May vary |

## Exercise 3: UDP Filtering with DROP

### Expected Terminal Output

```
[2026-01-XX HH:MM:SS] INFO: Applying firewall profile: block_udp_9091
[2026-01-XX HH:MM:SS] INFO: Sending UDP datagram to 10.0.7.200:9091
[2026-01-XX HH:MM:SS] INFO: Datagram sent (no acknowledgment expected)
[2026-01-XX HH:MM:SS] INFO: Waiting 5 seconds for any response...
[2026-01-XX HH:MM:SS] WARN: No response received (timeout)
[2026-01-XX HH:MM:SS] INFO: Behaviour consistent with DROP rule
```

### Expected Wireshark Observations

With filter `udp.port == 9091`:
1. UDP datagram (sender → receiver)
2. **No response packets** **← Key indicator of DROP**
3. No ICMP unreachable messages

### Distinguishing DROP from Network Issues

| Indicator | DROP | Packet Loss | Service Down |
|-----------|------|-------------|--------------|
| ICMP response | None | None | Possible |
| Consistency | 100% silent | Intermittent | Consistent |
| TCP alternative | Still works | Also affected | Also fails |

## Exercise 4: Application-Layer Proxy Filter

### Expected Terminal Output

```
[2026-01-XX HH:MM:SS] INFO: Testing application-layer filter on port 8888
[2026-01-XX HH:MM:SS] INFO: Test 1: Sending allowed content
[2026-01-XX HH:MM:SS] INFO: Response received: OK (200)
[2026-01-XX HH:MM:SS] INFO: Test 2: Sending blocked keyword 'malware'
[2026-01-XX HH:MM:SS] WARN: Request blocked by content filter
[2026-01-XX HH:MM:SS] INFO: Test 3: Sending blocked keyword 'attack'
[2026-01-XX HH:MM:SS] WARN: Request blocked by content filter
[2026-01-XX HH:MM:SS] INFO: Application filter working as expected
```

### Expected Wireshark Observations

With filter `tcp.port == 8888`:

For allowed requests:
1. TCP three-way handshake (SYN, SYN-ACK, ACK)
2. HTTP request in TCP payload
3. HTTP response in TCP payload
4. TCP close sequence

For blocked requests:
1. TCP three-way handshake **completes successfully**
2. HTTP request in TCP payload (contains blocked keyword)
3. Connection closed by proxy (RST or FIN)
4. No HTTP response body

### Key Distinction from Network-Layer Filtering

| Layer | Connection | Request | Response |
|-------|------------|---------|----------|
| Network (iptables) | Blocked/Reset | N/A | N/A |
| Application (proxy) | Succeeds | Received | May be blocked |

## Exercise 5: Defensive Port Probing

### Expected Terminal Output

```
[2026-01-XX HH:MM:SS] INFO: Starting port probe on 10.0.7.100
[2026-01-XX HH:MM:SS] INFO: Probing ports 9080-9100
[2026-01-XX HH:MM:SS] INFO: Port 9090: OPEN (TCP echo server)
[2026-01-XX HH:MM:SS] INFO: Port 9091: FILTERED (no response)
[2026-01-XX HH:MM:SS] INFO: Port 9092: CLOSED (RST received)
[2026-01-XX HH:MM:SS] INFO: Probe complete. Open: 1, Closed: 19, Filtered: 1
```

### Port State Interpretation

| State | TCP Behaviour | Meaning |
|-------|---------------|---------|
| OPEN | SYN → SYN-ACK | Service listening |
| CLOSED | SYN → RST | No service, no filter |
| FILTERED | SYN → (timeout) | Firewall DROP rule |
| REJECTED | SYN → RST/ICMP | Firewall REJECT rule |

### Expected Wireshark Observations

With filter `tcp.flags.syn == 1`:
- Multiple SYN packets to consecutive ports
- Mix of RST responses (closed ports)
- SYN-ACK responses (open ports)
- No responses for filtered ports

## Demonstration: REJECT vs DROP Comparison

### Expected Output

```
================================================================================
DEMO: REJECT vs DROP Behaviour Comparison
================================================================================

Phase 1: Testing with REJECT rule
---------------------------------
Applying profile: block_tcp_9090 (REJECT)
Attempting TCP connection...
Result: Connection refused immediately
Time elapsed: 0.003 seconds

Phase 2: Testing with DROP rule  
-------------------------------
Applying profile: block_tcp_9090_drop (DROP)
Attempting TCP connection...
Result: Connection timed out
Time elapsed: 5.002 seconds

================================================================================
ANALYSIS
================================================================================
REJECT: Fast failure, reveals firewall presence
DROP:   Slow failure (timeout), silent, appears as network issue

Security trade-off:
- REJECT is user-friendly but reveals firewall configuration
- DROP is stealthier but causes application timeouts
================================================================================
```

## Smoke Test Expected Output

```
============================================================
Week 7 Smoke Test
NETWORKING class - ASE, Informatics
============================================================

[1/5] Checking docker-compose.yml...
  [OK] docker-compose.yml found
[2/5] Checking Docker daemon...
  [OK] Docker daemon running
[3/5] Checking TCP server (localhost:9090)...
  [OK] TCP server is responding
[4/5] Checking source files...
  [OK] All 5 application files found
[5/5] Checking directories...
  [OK] artifacts/ exists
  [OK] pcap/ exists

============================================================
Smoke test completed in 2.3 seconds
============================================================
All checks passed
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
