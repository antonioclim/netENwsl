# Theoretical Summary - Week 13: IoT and Security

> NETWORKING class - ASE, Informatics | by Revolvix

## 1. Internet of Things (IoT) Fundamentals

### 1.1 IoT Architecture Layers
The IoT environment comprises multiple interconnected layers:

- **Perception Layer**: Physical sensors and actuators collecting environmental data (temperature, humidity, motion, etc.)
- **Network Layer**: Communication infrastructure connecting devices to processing centres
- **Processing Layer**: Data aggregation, storage and analysis platforms
- **Application Layer**: User-facing services and business logic

### 1.2 Communication Protocols
IoT deployments utilise various protocols optimised for constrained environments:

| Protocol | Transport | QoS | Use Case |
|----------|-----------|-----|----------|
| MQTT | TCP | 0,1,2 | Telemetry, sensors |
| CoAP | UDP | Confirmable | Resource-constrained |
| HTTP/REST | TCP | None | Web integration |
| AMQP | TCP | 0,1,2 | Enterprise messaging |

## 2. MQTT Protocol

> 💭 **Before reading:** How do you think messages get from a sensor to a dashboard in IoT systems? What role might a central server play?

### 2.1 Architecture
MQTT (Message Queuing Telemetry Transport) implements a publish/subscribe pattern:

```
[Publisher] ---> [Broker] ---> [Subscriber]
                    |
             Topic Routing
```

**Components:**
- **Broker**: Central message router (e.g., Mosquitto, HiveMQ)
- **Publisher**: Sends messages to topics
- **Subscriber**: Receives messages from subscribed topics
- **Topic**: Hierarchical namespace for message routing

### 2.2 Topic Structure
Topics use forward-slash hierarchy:
```
building/floor1/room101/temperature
sensors/outdoor/weather/humidity
```

**Wildcards:**
- `+` Single level: `sensors/+/temperature` matches `sensors/A/temperature`
- `#` Multi-level: `sensors/#` matches all under `sensors/`

### 2.3 Quality of Service (QoS)

| Level | Name | Guarantee | Overhead |
|-------|------|-----------|----------|
| 0 | At most once | Fire and forget | Lowest |
| 1 | At least once | Acknowledged | Medium |
| 2 | Exactly once | Four-way handshake | Highest |

#### QoS Level Packet Flows (ASCII Diagrams)

**QoS 0 — Fire and Forget:**
```
Publisher                    Broker                    Subscriber
    |                           |                           |
    |-------- PUBLISH --------->|                           |
    |                           |-------- PUBLISH --------->|
    |                           |                           |
    (No acknowledgement - message may be lost)
```

**QoS 1 — At Least Once:**
```
Publisher                    Broker                    Subscriber
    |                           |                           |
    |-------- PUBLISH --------->|                           |
    |<-------- PUBACK ----------|                           |
    |                           |-------- PUBLISH --------->|
    |                           |<-------- PUBACK ----------|
    |                           |                           |
    (Guaranteed delivery, may duplicate)
```

**QoS 2 — Exactly Once:**
```
Publisher                    Broker
    |                           |
    |-------- PUBLISH --------->|
    |<-------- PUBREC ----------|  (Publish Received)
    |-------- PUBREL ---------->|  (Publish Release)
    |<-------- PUBCOMP ---------|  (Publish Complete)
    |                           |
    (Guaranteed exactly once - highest overhead)
```

## 3. Transport Layer Security (TLS)

> 💭 **Before reading:** If you encrypt network traffic with TLS, what information do you think an eavesdropper can still observe? What gets hidden?

### 3.1 Security Properties
TLS provides three fundamental security guarantees:

1. **Confidentiality**: Encrypts payload content
2. **Integrity**: Detects message tampering via MACs
3. **Authentication**: Verifies server (optionally client) identity

### 3.2 TLS Handshake Sequence
```
Client                              Server
  |-------- ClientHello ------------>|
  |<------- ServerHello -------------|
  |<------- Certificate -------------|
  |<------- ServerHelloDone ---------|
  |-------- ClientKeyExchange ------>|
  |-------- ChangeCipherSpec ------->|
  |-------- Finished --------------->|
  |<------- ChangeCipherSpec --------|
  |<------- Finished ----------------|
  |<======= Encrypted Data =========>|
```

### 3.3 Metadata Leakage
Even with TLS, certain information remains observable:

**Visible:**
- Source and destination IP addresses
- Port numbers
- Connection timing
- Approximate message sizes
- Traffic patterns and frequencies

**Hidden:**
- Application payload content
- Topic names (for MQTT)
- Authentication credentials

## 4. Network Reconnaissance

> 💭 **Before reading:** When a port scanner reports a port as "filtered", what do you think that means? Is it the same as "closed"?

### 4.1 Port Scanning Techniques

**TCP Connect Scan:**
- Completes full three-way handshake
- Easily detected, but reliable
- Used in this laboratory

**Port States:**
| State | Indication | Cause |
|-------|------------|-------|
| Open | Service accepting connections | Application listening |
| Closed | No service | RST response |
| Filtered | No response | Firewall drop |

### 4.2 Service Fingerprinting
Techniques to identify running services:

1. **Banner Grabbing**: Reading service welcome messages
2. **Protocol Probing**: Sending protocol-specific requests
3. **Version Detection**: Analysing response patterns

### 4.3 Ethical Considerations
Network scanning is only legal when:
- You own the target system
- You have explicit written authorisation
- Operating within a controlled laboratory environment

## 5. Common IoT Vulnerabilities

### 5.1 OWASP IoT Top 10 (2018)
1. Weak, guessable or hardcoded passwords
2. Insecure network services
3. Insecure environment interfaces
4. Lack of secure update mechanism
5. Use of insecure or outdated components
6. Insufficient privacy protection
7. Insecure data transfer and storage
8. Lack of device management
9. Insecure default settings
10. Lack of physical hardening

### 5.2 MQTT-Specific Risks
- Anonymous access enabled
- Unencrypted communications
- Wildcard subscriptions allowing eavesdropping
- Retained messages exposing historical data
- Lack of access control lists

## 6. Defensive Measures

### 6.1 Network Segmentation
Isolate IoT devices from critical infrastructure:
```
[Internet] --- [Firewall] --- [IoT VLAN]
                    |
              [Corporate VLAN]
```

### 6.2 Encryption Requirements
- Enforce TLS 1.2 or higher
- Disable plaintext listeners in production
- Implement certificate pinning where feasible

### 6.3 Authentication and Authorisation
- Require username/password authentication
- Implement topic-level ACLs
- Use client certificates for sensitive deployments

### 6.4 Monitoring and Detection
- Log all connection attempts
- Alert on anomalous traffic patterns
- Implement intrusion detection systems

## 7. Key Terminology

| Term | Definition |
|------|------------|
| CVE | Common Vulnerabilities and Exposures - standardised vulnerability identifiers |
| Broker | Central MQTT message routing server |
| QoS | Quality of Service - delivery guarantee level |
| Banner | Service identification string sent on connection |
| ACL | Access Control List - permission definitions |
| TLS | Transport Layer Security - encryption protocol |
| MITM | Man-in-the-Middle - interception attack |
| Wildcard | Pattern matching character in topics |

---

## 🎯 Key Takeaways

After completing Week 13, you should be able to:

### Conceptual Understanding
1. **MQTT is publish/subscribe**: Publishers and subscribers are decoupled through a broker
2. **QoS is per-hop**: The effective QoS is the minimum of publisher and subscriber QoS
3. **TLS encrypts content, not metadata**: IP addresses, timing and sizes remain visible
4. **Filtered ≠ Closed**: Filtered means no response (firewall DROP), closed means active refusal (RST)
5. **Authentication before encryption**: Default credentials are a bigger risk than unencrypted traffic

### Practical Skills
1. Scan networks to identify open services (ethically, with permission)
2. Use MQTT clients for IoT communication (both plaintext and TLS)
3. Capture and analyse network traffic to distinguish protocols
4. Assess vulnerabilities and understand their implications

### Security Mindset
1. Defence in depth — multiple layers of protection
2. Assume breach — monitor and detect anomalies
3. Least privilege — only expose what is necessary
4. Regular updates — patch known vulnerabilities promptly

---

## Quick Reference Card

```
┌────────────────────────────────────────────────────────────────────────┐
│  WEEK 13 QUICK REFERENCE                                               │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  MQTT PORTS:           1883 (plaintext), 8883 (TLS)                   │
│  MQTT WILDCARDS:       + = one level, # = all remaining levels        │
│  MQTT QoS:             0 = fire-forget, 1 = ack'd, 2 = exactly-once   │
│                                                                        │
│  PORT STATES:          OPEN (service), CLOSED (RST), FILTERED (drop)  │
│                                                                        │
│  TLS HIDES:            payload, topics, credentials                   │
│  TLS SHOWS:            IPs, ports, timing, sizes                      │
│                                                                        │
│  OWASP #1:             Weak/default passwords (not encryption!)       │
│                                                                        │
│  LAB SERVICES:                                                        │
│    - Mosquitto MQTT:   10.0.13.100 (:1883, :8883)                    │
│    - DVWA:             10.0.13.11  (:8080)                            │
│    - vsftpd:           10.0.13.12  (:2121, :6200)                     │
│    - Portainer:        localhost:9000 (global)                        │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

> 📖 **Further study:** Review common misconceptions about these topics in `docs/misconceptions.md` and test your understanding with the peer instruction questions in `docs/peer_instruction.md`.
