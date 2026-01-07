# Theoretical Summary - Week 13: IoT and Security

> NETWORKING class - ASE, Informatics | by Revolvix

## 1. Internet of Things (IoT) Fundamentals

### 1.1 IoT Architecture Layers
The IoT ecosystem comprises multiple interconnected layers:

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

## 3. Transport Layer Security (TLS)

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
3. Insecure ecosystem interfaces
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
