# Week 7: Theoretical Foundations
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> This document provides the conceptual foundations for packet capture and filtering.
> Read this before starting the laboratory exercises.

---

## Table of Contents

1. [Packet Capture as Evidence](#packet-capture-as-evidence)
2. [Filtering Semantics: DROP vs REJECT](#filtering-semantics-drop-vs-reject)
3. [Port States and Their Meaning](#port-states-and-their-meaning)
4. [TCP Three-Way Handshake](#tcp-three-way-handshake)
5. [UDP Connectionless Nature](#udp-connectionless-nature)
6. [Reproducibility in Network Experiments](#reproducibility-in-network-experiments)
7. [References and RFCs](#references-and-rfcs)

---

## Packet Capture as Evidence

Traffic capture provides the **ground truth** for network behaviour. Unlike log files or application-level traces, packet captures record precisely what traverses the wire. This evidentiary quality makes captures indispensable for debugging, security analysis, and compliance auditing.

### Capture Semantics

A packet capture records the exact byte sequence seen at the capture point. This includes headers from multiple layers (Ethernet, IP, TCP/UDP) and payloads. The capture timestamp reflects when the packet arrived at the interface, **not** when it was sent or when the application processed it.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CAPTURE POINT PLACEMENT                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Application                                                           │
│       │                                                                 │
│       ▼                                                                 │
│   Socket Layer (send/recv)                                              │
│       │                                                                 │
│       ▼                                                                 │
│   TCP/UDP Processing                                                    │
│       │                                                                 │
│       ▼                                                                 │
│   IP Layer ◀──────── CAPTURE POINT (tcpdump) ──────▶ What we SEE       │
│       │                                                                 │
│       ▼                                                                 │
│   Network Interface                                                     │
│       │                                                                 │
│       ▼                                                                 │
│   Physical Wire                                                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Critical distinction:** Captures show **what happened**, not what *should have happened*. A misconfigured firewall, a misbehaving application, or a network fault all leave traces in captures that differ from expected behaviour.

### Capture Limitations

| Factor | Impact | Mitigation |
|--------|--------|------------|
| Interface selection | Only sees traffic on selected interface | Use `-i any` or capture at multiple points |
| Promiscuous mode | Without it, only sees traffic to/from this host | Enable promiscuous mode |
| Filter timing | BPF filters apply at capture time | Capture broad, filter in analysis |
| Performance | High traffic can cause drops | Limit capture size/duration |
| Encryption | TLS/SSL payload is opaque | Capture before encryption or use key logs |

---

## Filtering Semantics: DROP vs REJECT

Network filtering controls which packets pass through a checkpoint. Two primary actions exist when a packet matches a blocking rule:

### DROP (Silent Discard)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              DROP ACTION                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Client                      Firewall                      Server      │
│     │                            │                            │         │
│     │  ─────── SYN ──────▶      │                            │         │
│     │                       ┌────┴────┐                      │         │
│     │                       │  DROP   │                      │         │
│     │                       │ (silent)│                      │         │
│     │                       └─────────┘                      │         │
│     │                                                        │         │
│     │  [waiting...]          ❌ No packet                    │         │
│     │                                                        │         │
│     │  [still waiting...]                                    │         │
│     │                                                        │         │
│     │  [TIMEOUT!]                                            │         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Characteristics:**
- No ICMP response generated
- TCP connections experience timeout rather than immediate failure
- Stealthy but delays error detection for legitimate traffic
- Sender cannot distinguish DROP from packet loss

### REJECT (Active Refusal)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                             REJECT ACTION                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Client                      Firewall                      Server      │
│     │                            │                            │         │
│     │  ─────── SYN ──────▶      │                            │         │
│     │                       ┌────┴────┐                      │         │
│     │                       │ REJECT  │                      │         │
│     │                       └────┬────┘                      │         │
│     │                            │                            │         │
│     │  ◀─── RST or ICMP ────    │                            │         │
│     │                            │                            │         │
│     │  [Connection refused!]     │                            │         │
│     │  (immediate feedback)      │                            │         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Characteristics:**
- ICMP "port unreachable" for UDP (Type 3, Code 3)
- TCP RST for TCP connections
- Faster error detection for legitimate traffic
- Reveals the presence of a firewall to potential attackers

### Choosing Between DROP and REJECT

| Scenario | Recommended | Rationale |
|----------|-------------|-----------|
| External-facing services | **DROP** | Minimise reconnaissance information |
| Internal network segments | **REJECT** | Faster debugging for legitimate issues |
| Rate-limited abuse detection | **DROP** | Avoid amplification attacks |
| Debugging firewall rules | **REJECT** | Immediate feedback on rule matching |
| Honeypot/deception | **DROP** | Mimic non-existent hosts |
| Development environment | **REJECT** | Rapid feedback during testing |

### Comparison Summary

| Aspect | DROP | REJECT |
|--------|------|--------|
| Response sent | None | RST or ICMP |
| Client experience | Timeout (slow failure) | Immediate error |
| Network evidence | No packets from firewall | Response packet visible |
| Debugging difficulty | High | Low |
| Security posture | Stealthier | Reveals firewall presence |
| Resource usage | Minimal | Generates response packet |

---

## Port States and Their Meaning

When probing a port, three distinct states may be observed:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          PORT STATE DIAGRAM                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                          ┌──────────────┐                               │
│                          │   PROBE      │                               │
│                          │   (SYN)      │                               │
│                          └──────┬───────┘                               │
│                                 │                                       │
│              ┌──────────────────┼──────────────────┐                    │
│              ▼                  ▼                  ▼                    │
│       ┌────────────┐     ┌────────────┐     ┌────────────┐             │
│       │   OPEN     │     │   CLOSED   │     │  FILTERED  │             │
│       └─────┬──────┘     └─────┬──────┘     └─────┬──────┘             │
│             │                  │                  │                     │
│             ▼                  ▼                  ▼                     │
│       ┌──────────┐       ┌──────────┐       ┌──────────┐               │
│       │ SYN-ACK  │       │   RST    │       │ (nothing)│               │
│       │ received │       │ received │       │  timeout │               │
│       └──────────┘       └──────────┘       └──────────┘               │
│             │                  │                  │                     │
│             ▼                  ▼                  ▼                     │
│       "Service          "No service,       "Cannot                      │
│        listening"        host reachable"   determine"                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Detailed State Descriptions

**1. OPEN**
- A service is listening and responding
- TCP: Completes handshake (SYN → SYN-ACK → ACK)
- UDP: May respond depending on application protocol
- Evidence: Successful connection or application response

**2. CLOSED**
- No service is listening, but the host is reachable
- TCP: Responds with RST packet
- UDP: Responds with ICMP port unreachable (Type 3, Code 3)
- Evidence: Confirms host is alive and responding

**3. FILTERED**
- The port's state cannot be determined because a firewall blocks probes
- No response received (DROP rule)
- Or ICMP administratively prohibited (Type 3, Code 13)
- Evidence: Could be firewall, packet loss, or non-existent host

---

## TCP Three-Way Handshake

Understanding the handshake is essential for interpreting captures:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TCP THREE-WAY HANDSHAKE                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   CLIENT                                               SERVER           │
│   (state)                                              (state)          │
│                                                                         │
│   CLOSED                                               LISTEN           │
│      │                                                    │             │
│      │  ─────────── SYN (seq=x) ────────────────▶        │             │
│      │                                                    │             │
│   SYN-SENT                                             SYN-RCVD         │
│      │                                                    │             │
│      │  ◀──────── SYN-ACK (seq=y, ack=x+1) ──────        │             │
│      │                                                    │             │
│      │  ─────────── ACK (seq=x+1, ack=y+1) ─────▶        │             │
│      │                                                    │             │
│   ESTABLISHED                                          ESTABLISHED      │
│      │                                                    │             │
│      │  ◀════════════ DATA TRANSFER ═══════════▶        │             │
│      │                                                    │             │
└─────────────────────────────────────────────────────────────────────────┘
```

### Handshake Packet Details

| Packet | Flags | Sequence | Acknowledgement | Purpose |
|--------|-------|----------|-----------------|---------|
| 1 | SYN | x (ISN) | - | Client requests connection |
| 2 | SYN,ACK | y (ISN) | x+1 | Server accepts, sends its ISN |
| 3 | ACK | x+1 | y+1 | Client confirms, connection ready |

### Blocked Connection Manifestations

| Evidence | Likely Cause |
|----------|--------------|
| SYN sent, no response | DROP rule or packet loss |
| SYN sent, RST received | Closed port or REJECT rule |
| SYN sent, ICMP unreachable | Firewall REJECT |
| Multiple SYN, all timeout | DROP rule (retransmits visible) |

---

## UDP Connectionless Nature

UDP has no handshake. A datagram is sent; the sender has no confirmation of delivery.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        UDP COMMUNICATION                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   SENDER                                               RECEIVER         │
│      │                                                    │             │
│      │  ─────────── UDP Datagram ────────────────▶       │             │
│      │           (fire and forget)                       │             │
│      │                                                    │             │
│      │  sendto() returns SUCCESS                          │             │
│      │  (regardless of delivery!)                         │             │
│      │                                                    │             │
│      │                              ┌─────────────────────┤             │
│      │                              │ Received? Maybe.    │             │
│      │                              │ Dropped? Maybe.     │             │
│      │                              │ Sender doesn't know.│             │
│      │                              └─────────────────────┘             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### UDP Filtering Challenges

| Scenario | What Sender Sees | Actual Cause |
|----------|------------------|--------------|
| sendto() returns 0 | Success | Packet sent to network |
| No response from receiver | Could be anything | Receiver not listening, DROP, packet loss |
| ICMP port unreachable | Error | REJECT rule or closed port |

**Key insight:** UDP sender **cannot distinguish** between:
- Successful delivery with no application response
- Firewall DROP
- Network packet loss
- Receiver not listening

---

## Reproducibility in Network Experiments

Network experiments must be **reproducible** to be valuable. This requires:

### Requirements for Reproducibility

1. **Controlled environment**
   - Isolated network namespace (Docker network)
   - No interference from external traffic
   - Documented network topology

2. **Documented initial state**
   - Which services are running
   - Which filtering rules are applied
   - Expected topology diagram

3. **Timestamped evidence**
   - Captures include accurate timestamps
   - Logs correlate with capture times
   - Use NTP-synced clocks when possible

4. **Explicit variables**
   - Document each change (new rule, different port)
   - One variable change per experiment
   - Clear before/after comparison

### Week 7 Reproducibility Checklist

- [ ] Lab environment started fresh (`scripts/cleanup.py --full` first)
- [ ] Baseline capture taken before applying rules
- [ ] Each filtering profile documented in JSON
- [ ] Capture files named with exercise number
- [ ] Timestamps noted in lab report

---

## References and RFCs

### Core RFCs

| RFC | Title | Relevance |
|-----|-------|-----------|
| RFC 793 | Transmission Control Protocol | TCP fundamentals, state machine |
| RFC 768 | User Datagram Protocol | UDP specification |
| RFC 792 | Internet Control Message Protocol | ICMP error messages |
| RFC 1122 | Requirements for Internet Hosts | Host behaviour requirements |

### Textbooks

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
  - Chapter 3: Transport Layer
  - Chapter 4: Network Layer
  
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
  - Chapters on TCP and UDP sockets
  
- Bejtlich, R. (2013). *The Practice of Network Security Monitoring*. No Starch Press.
  - Packet capture methodology
  - Evidence-based analysis

### Manual Pages

- `iptables(8)` — Linux Netfilter administration
- `tcpdump(1)` — Network packet analyser
- `tshark(1)` — Wireshark command-line tool
- `netstat(8)` — Network statistics
- `ss(8)` — Socket statistics

### Online Resources

- [Wireshark User's Guide](https://www.wireshark.org/docs/wsug_html_chunked/)
- [tcpdump Tutorial](https://danielmiessler.com/study/tcpdump/)
- [iptables Tutorial](https://www.frozentux.net/iptables-tutorial/iptables-tutorial.html)

---

*Computer Networks — Week 7: Packet Interception, Filtering and Defensive Port Probing*  
*ASE Bucharest, CSIE | by ing. dr. Antonio Clim*
