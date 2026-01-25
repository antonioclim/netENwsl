# Week 13: IoT and Security — Theory Summary

**Computer Networks** — ASE, CSIE | ing. dr. Antonio Clim

---

## 1. IoT Fundamentals

The Internet of Things (IoT) represents a paradigm shift in networked computing whereby physical devices—sensors, actuators, embedded systems—communicate autonomously over IP networks. Unlike traditional client-server architectures, IoT deployments exhibit several distinctive characteristics.

**Constrained Resources**: IoT devices typically operate with limited computational power (8-32 bit MCUs), memory (KB to low MB), and energy budgets (battery or energy harvesting). These constraints fundamentally shape protocol selection and security implementation strategies.

**Heterogeneous Connectivity**: Devices may connect via diverse physical layers including IEEE 802.15.4 (Zigbee), Bluetooth Low Energy (BLE), LoRaWAN for long-range low-power communication, or traditional Wi-Fi/Ethernet. Protocol translation and gateway architectures become essential.

**Scale and Distribution**: Industrial IoT deployments may encompass thousands of devices across geographically dispersed locations, necessitating hierarchical management and edge computing architectures.

---

## 2. MQTT Protocol Architecture

Message Queuing Telemetry Transport (MQTT) has emerged as the dominant application-layer protocol for IoT communications, designed explicitly for constrained environments and unreliable networks.

### 2.1 Publish-Subscribe Model

MQTT employs a topic-based publish-subscribe pattern mediated by a central broker (e.g., Mosquitto, EMQX):

- **Publishers** transmit messages to hierarchical topics (e.g., `building/floor1/temperature`)
- **Subscribers** register interest in topics using exact matches or wildcards (`+` for single level, `#` for multi-level)
- **Broker** maintains topic subscriptions and routes messages accordingly

This decoupling enables asynchronous, many-to-many communication without direct client addressing.

### 2.2 Quality of Service Levels

MQTT defines three QoS levels with distinct delivery guarantees:

| QoS | Name | Guarantee | Overhead |
|-----|------|-----------|----------|
| 0 | At most once | Fire and forget | Minimal |
| 1 | At least once | Acknowledged delivery | Moderate |
| 2 | Exactly once | Four-step handshake | Highest |

QoS selection involves trade-offs between reliability, latency, and bandwidth consumption. Sensor telemetry often tolerates QoS 0, whilst critical commands may require QoS 2.

### 2.3 Transport Security

MQTT operates over TCP (port 1883) or TLS (port 8883). Transport-layer encryption protects message confidentiality but does not address:

- Broker-level access to plaintext messages
- Authentication granularity beyond connection establishment
- Topic-level authorisation policies

---

## 3. OWASP IoT Top 10

The Open Web Application Security Project (OWASP) maintains an IoT-specific vulnerability taxonomy identifying prevalent weaknesses in device ecosystems.

### 3.1 Critical Vulnerabilities

**I1 — Weak, Guessable, or Hardcoded Passwords**: Devices shipping with default credentials (e.g., admin/admin) or lacking password complexity requirements remain trivially exploitable at scale.

**I2 — Insecure Network Services**: Unnecessary services (Telnet, FTP, debugging interfaces) exposed on device interfaces expand the attack surface.

**I3 — Insecure Ecosystem Interfaces**: Web interfaces, APIs, and cloud backends associated with IoT devices frequently exhibit injection vulnerabilities, broken authentication, or inadequate transport security.

### 3.2 Defence Strategies

Effective IoT security requires defence-in-depth across the device lifecycle:

1. **Secure Boot**: Cryptographic verification of firmware integrity during initialisation
2. **Network Segmentation**: Isolating IoT traffic from corporate networks via VLANs or dedicated infrastructure
3. **Certificate-based Authentication**: X.509 certificates for device identity rather than pre-shared keys
4. **Firmware Updates**: Signed, encrypted OTA update mechanisms with rollback capability

---

## 4. Practical Laboratory Exercises

This week's laboratory exercises provide hands-on experience with:

- **Ex 13.01**: MQTT traffic capture and analysis using tcpdump/Wireshark
- **Ex 13.02**: Mosquitto broker configuration with ACL-based topic authorisation
- **Ex 13.03**: TLS certificate generation and MQTT-over-TLS implementation
- **Ex 13.04**: Automated vulnerability scanning against OWASP IoT criteria

---

## 5. Learning Objectives Mapping

| LO | Description | Exercises |
|----|-------------|-----------|
| LO1 | Explain MQTT architecture and QoS semantics | Ex 13.01 |
| LO2 | Analyse network traffic to identify protocol weaknesses | Ex 13.01, 13.02 |
| LO3 | Configure broker security controls | Ex 13.02, 13.03 |
| LO4 | Implement transport-layer encryption | Ex 13.03 |
| LO5 | Identify OWASP IoT vulnerabilities | Ex 13.04 |
| LO6 | Design defence-in-depth strategies | Ex 13.04 |
| LO7 | Evaluate IoT deployment security posture | Quiz |

---

## Summary

IoT security represents a distinct subdomain requiring specialised knowledge of constrained device characteristics, lightweight protocols, and ecosystem-wide threat models. Key principles include:

- MQTT's publish-subscribe architecture provides efficient IoT messaging but requires explicit security configuration
- QoS levels trade reliability against overhead—selection depends on application criticality
- OWASP IoT Top 10 provides a systematic framework for vulnerability identification
- Defence-in-depth strategies must address device, network, and cloud components collectively

Mastery of these concepts enables security-conscious IoT deployment in industrial, healthcare, and smart infrastructure domains.

---

## References

1. OWASP. (2024). *IoT Top 10*. https://owasp.org/www-project-internet-of-things/
2. MQTT.org. (2023). *MQTT Version 5.0 Specification*.
3. Mosquitto. (2024). *Eclipse Mosquitto Documentation*.

---

*Document version: 2.0 | Language: en-GB | Last updated: January 2026*
