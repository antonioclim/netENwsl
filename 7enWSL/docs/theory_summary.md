# Week 7: Theoretical Foundations

> NETWORKING class - ASE, Informatics | by Revolvix

## Packet Capture as Evidence

Traffic capture provides the ground truth for network behaviour. Unlike log files or application-level traces, packet captures record precisely what traverses the wire. This evidentiary quality makes captures indispensable for debugging, security analysis and compliance auditing.

### Capture Semantics

A packet capture records the exact byte sequence seen at the capture point. This includes headers from multiple layers (Ethernet, IP, TCP/UDP) and payloads. The capture timestamp reflects when the packet arrived at the interface, not when it was sent or when the application processed it.

**Critical distinction:** Captures show what happened, not what should have happened. A misconfigured firewall, a misbehaving application or a network fault all leave traces in captures that differ from the expected behaviour.

## Filtering Semantics: REJECT vs DROP

Network filtering controls which packets pass through a checkpoint. Two primary actions exist when a packet matches a blocking rule:

### DROP (Silent Discard)

The packet is silently discarded. The sender receives no indication that the packet was blocked. From the sender's perspective, the packet simply disappeared into the network.

**Characteristics:**
- No ICMP response generated
- TCP connections experience timeout rather than immediate failure
- Stealthy but delays error detection for legitimate traffic

### REJECT (Active Refusal)

The packet is discarded but the sender receives notification. For TCP, this typically means an RST (reset) segment or ICMP destination unreachable message.

**Characteristics:**
- ICMP "port unreachable" for UDP
- TCP RST for TCP connections
- Faster error detection for legitimate traffic
- Reveals the presence of a firewall

### Choosing Between DROP and REJECT

| Scenario | Recommended Action | Rationale |
|----------|-------------------|-----------|
| External-facing services | DROP | Minimise reconnaissance information |
| Internal network segments | REJECT | Faster debugging for legitimate issues |
| Rate-limited abuse | DROP | Avoid amplification attacks |
| Debugging firewall rules | REJECT | Immediate feedback on rule matching |

## Port States and Their Meaning

When probing a port, three distinct states may be observed:

1. **Open:** A service is listening and responding. TCP handshake completes; UDP may respond depending on the application.

2. **Closed:** No service is listening but the host is reachable. TCP responds with RST; UDP responds with ICMP port unreachable.

3. **Filtered:** The port's state cannot be determined because a firewall blocks probes. No response is received (DROP) or an ICMP administratively prohibited message appears.

## Reproducibility in Network Experiments

Network experiments must be reproducible to be valuable. This requires:

1. **Controlled environment:** Isolated network namespace (Mininet, Docker network) eliminates interference from external traffic.

2. **Documented initial state:** Record which services are running, which rules are applied and what the expected topology looks like.

3. **Timestamped evidence:** Captures should include timestamps and be correlated with logs.

4. **Explicit variables:** Any change (new rule, different port, altered payload) should be documented as a distinct experiment.

## TCP Three-Way Handshake

Understanding the handshake is essential for interpreting captures:

```
Client                    Server
   |                         |
   |  SYN (seq=x)           |
   |------------------------>|
   |                         |
   |  SYN-ACK (seq=y,ack=x+1)|
   |<------------------------|
   |                         |
   |  ACK (seq=x+1,ack=y+1)  |
   |------------------------>|
   |                         |
   |  Connection established |
```

A blocked connection may manifest as:
- SYN sent, no response (DROP)
- SYN sent, RST received (REJECT or closed port)
- SYN sent, ICMP unreachable (firewall REJECT)

## UDP Connectionless Nature

UDP has no handshake. A datagram is sent; the sender has no confirmation of delivery. This creates challenges for filtering verification:

- A blocked UDP port may be indistinguishable from packet loss
- ICMP "port unreachable" indicates either a closed port or a REJECT rule
- Application-layer acknowledgement is required for reliable delivery

## Further Reading

- Kurose & Ross, Chapter 4 (Network Layer)
- Kurose & Ross, Chapter 3 (Transport Layer)
- Bejtlich, R. *The Practice of Network Security Monitoring*
- man iptables, man tcpdump, man tshark

---

*NETWORKING class - ASE, Informatics | by Revolvix*
