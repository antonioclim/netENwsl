# Week 13: IoT and Security — Glossary

**Computer Networks** — ASE, CSIE | ing. dr. Antonio Clim

---

## A

**ACL (Access Control List)**
A security mechanism defining which clients may publish or subscribe to specific MQTT topics. Configured in broker settings (e.g., `mosquitto.acl`).

**At-most-once delivery**
MQTT QoS level 0; messages sent without acknowledgement. Suitable for non-critical telemetry where occasional loss is acceptable.

**At-least-once delivery**
MQTT QoS level 1; requires PUBACK acknowledgement. Guarantees delivery but may produce duplicates under network instability.

**Authentication**
The process of verifying client identity. MQTT supports username/password, X.509 certificates, and token-based methods (e.g., JWT).

**Authorisation**
The process of determining permitted actions for an authenticated entity. In MQTT, typically implemented via topic-based ACLs.

---

## B

**Broker**
Central server in MQTT architecture responsible for receiving published messages and routing them to subscribed clients. Examples: Mosquitto, EMQX, HiveMQ.

**BLE (Bluetooth Low Energy)**
Short-range wireless protocol optimised for low power consumption. Common in wearables and proximity-based IoT applications.

---

## C

**CA (Certificate Authority)**
Trusted entity issuing X.509 certificates for TLS authentication. May be public (Let's Encrypt) or private (organisational PKI).

**Clean Session**
MQTT connection flag determining whether the broker retains session state (subscriptions, queued messages) between connections.

**Client ID**
Unique identifier for MQTT clients. The broker uses this to track session state and enforce connection policies.

**CoAP (Constrained Application Protocol)**
RESTful protocol designed for constrained IoT devices. Uses UDP transport with optional DTLS encryption.

**CVE (Common Vulnerabilities and Exposures)**
Standardised identifiers for publicly disclosed security vulnerabilities. Format: CVE-YYYY-NNNNN.

---

## D

**Defence-in-depth**
Security strategy employing multiple layers of controls so that compromise of one layer does not breach the entire system.

**DTLS (Datagram Transport Layer Security)**
TLS variant for UDP-based protocols. Provides confidentiality and integrity for CoAP and other datagram protocols.

---

## E

**Ecosystem** *(OWASP IoT context)*
The complete environment surrounding IoT devices, including cloud backends, mobile applications, web interfaces, APIs, and update mechanisms. OWASP explicitly addresses ecosystem interface security.

**Edge Computing**
Processing data near its source rather than transmitting to centralised cloud infrastructure. Reduces latency and bandwidth for IoT applications.

**Exactly-once delivery**
MQTT QoS level 2; four-step handshake (PUBLISH, PUBREC, PUBREL, PUBCOMP) guaranteeing single delivery without duplicates.

---

## F

**Firmware**
Software embedded in device flash memory providing low-level hardware control. Security requires integrity verification and secure update mechanisms.

**FTP (File Transfer Protocol)**
Legacy file transfer protocol. Often unnecessarily enabled on IoT devices, representing a security risk per OWASP I2.

---

## G

**Gateway**
Network device translating between protocols (e.g., Zigbee to MQTT) or providing security boundary between IoT and enterprise networks.

---

## H

**Hardcoded Credentials**
Passwords or keys embedded in firmware source code. A critical vulnerability (OWASP I1) as credentials cannot be changed post-deployment.

**HMAC (Hash-based Message Authentication Code)**
Cryptographic construct providing message integrity and authenticity. Used in some IoT authentication schemes.

---

## I

**IoT (Internet of Things)**
Network of physical devices with embedded sensors, actuators, and connectivity enabling autonomous data exchange and remote control.

---

## J

**JTAG (Joint Test Action Group)**
Hardware debugging interface. If accessible on deployed devices, permits firmware extraction and manipulation.

---

## K

**Keep-alive**
MQTT mechanism where clients send periodic PINGREQ messages to maintain connection state. Broker disconnects clients exceeding the keep-alive interval.

---

## L

**Last Will and Testament (LWT)**
MQTT feature allowing clients to register a message the broker publishes upon unexpected disconnection. Useful for device status monitoring.

**LoRaWAN**
Low-power wide-area network protocol for long-range IoT communication. Operates in unlicensed spectrum with typical ranges of 2-15 km.

---

## M

**MCU (Microcontroller Unit)**
Integrated circuit containing processor, memory, and I/O peripherals. Common IoT MCUs include ESP32, STM32, and Nordic nRF series.

**MITM (Man-in-the-Middle)**
Attack where adversary intercepts and potentially modifies communication between parties. TLS mitigates MITM through certificate validation.

**Mosquitto**
Open-source MQTT broker from Eclipse Foundation. Widely used in IoT deployments and laboratory environments.

**MQTT (Message Queuing Telemetry Transport)**
Lightweight publish-subscribe protocol designed for constrained devices and unreliable networks. Operates over TCP (1883) or TLS (8883).

---

## N

**Network Segmentation**
Dividing networks into isolated zones to contain breaches. IoT devices should reside in separate VLANs from corporate systems.

---

## O

**OTA (Over-the-Air)**
Wireless firmware update mechanism. Secure OTA requires signed images, encrypted transport, and rollback capability.

**OWASP (Open Web Application Security Project)**
Non-profit organisation publishing security guidance. The IoT Top 10 enumerates prevalent device vulnerabilities.

---

## P

**Payload**
The application data within an MQTT message, distinct from protocol headers and metadata.

**PKI (Public Key Infrastructure)**
Framework for managing digital certificates and public-key encryption. Enables certificate-based device authentication.

**Port Scanning**
Network reconnaissance technique identifying open services. Tools: nmap, masscan. Reveals attack surface per OWASP I2.

**PUBACK**
MQTT acknowledgement packet for QoS 1 messages, confirming broker receipt.

**Publish**
MQTT operation where a client sends a message to a topic for distribution to subscribers.

---

## Q

**QoS (Quality of Service)**
MQTT delivery guarantee levels: 0 (at-most-once), 1 (at-least-once), 2 (exactly-once).

---

## R

**Retained Message**
MQTT feature where the broker stores the last message on a topic, delivering it immediately to new subscribers.

---

## S

**Secure Boot**
Boot process verifying firmware cryptographic signatures before execution. Prevents execution of tampered code.

**Subscribe**
MQTT operation where a client registers interest in topics matching a filter pattern.

---

## T

**Telemetry**
Data transmitted from remote devices for monitoring. Sensor readings constitute typical IoT telemetry.

**TLS (Transport Layer Security)**
Cryptographic protocol providing confidentiality and integrity for TCP connections. MQTT-over-TLS uses port 8883.

**Topic**
Hierarchical namespace for MQTT message routing (e.g., `sensors/temperature/room1`). Supports wildcard subscriptions.

---

## V

**VLAN (Virtual LAN)**
Layer-2 network segmentation mechanism. Isolates IoT traffic from other network segments.

---

## W

**Wildcard**
MQTT subscription patterns: `+` matches single level, `#` matches multiple levels. Example: `sensors/+/temperature`.

---

## X

**X.509**
ITU-T standard for digital certificates. Used in TLS for server and client authentication.

---

## Z

**Zigbee**
Low-power mesh networking protocol based on IEEE 802.15.4. Common in home automation and industrial sensing.

---

*Document version: 2.0 | Language: en-GB | Last updated: January 2026*
