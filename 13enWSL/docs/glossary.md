# 📖 Glossary — Week 13: IoT and Security
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## MQTT Terms

| Term | Definition | Example |
|------|------------|---------|
| **Broker** | Central server that routes MQTT messages between publishers and subscribers | Mosquitto running on `localhost:1883` |
| **Publisher** | Client that sends messages to topics on the broker | Sensor publishing temperature readings |
| **Subscriber** | Client that receives messages from topics it has subscribed to | Dashboard receiving sensor data |
| **Topic** | Hierarchical string used to route messages (uses `/` as separator) | `building/floor1/room101/temperature` |
| **QoS (Quality of Service)** | Delivery guarantee level: 0 (at most once), 1 (at least once), 2 (exactly once) | `client.publish(topic, msg, qos=1)` |
| **Retain** | Flag that makes the broker store the last message on a topic for new subscribers | `client.publish(topic, msg, retain=True)` |
| **Will Message** | Message the broker publishes if a client disconnects unexpectedly | "sensor/status: offline" |
| **Wildcard (+)** | Single-level wildcard matching one topic segment | `sensors/+/temp` matches `sensors/A/temp` |
| **Wildcard (#)** | Multi-level wildcard matching zero or more segments (end only) | `sensors/#` matches all under `sensors/` |
| **CONNACK** | Connection acknowledgement packet from broker to client | Response code 0 = success |
| **PUBLISH** | Packet containing the message payload sent to a topic | Contains topic, QoS, payload |
| **SUBSCRIBE** | Packet requesting to receive messages from topic patterns | Contains topic filter and QoS |

---

## Security Terms

| Term | Definition | Example |
|------|------------|---------|
| **TLS (Transport Layer Security)** | Cryptographic protocol providing encrypted communication | MQTT over TLS on port 8883 |
| **Certificate Authority (CA)** | Trusted entity that issues digital certificates | Self-signed CA for lab environment |
| **X.509 Certificate** | Standard format for public key certificates | `server.crt` file |
| **Handshake** | Initial exchange establishing secure connection parameters | TLS 1.3 handshake (2 round trips) |
| **CVE** | Common Vulnerabilities and Exposures — standardised vulnerability identifier | CVE-2011-2523 (vsftpd backdoor) |
| **Reconnaissance** | Information gathering phase before an attack | Port scanning, banner grabbing |
| **Banner Grabbing** | Technique to identify services by reading their welcome messages | SSH banner reveals version |
| **ACL (Access Control List)** | Rules defining who can access which resources | MQTT topic permissions |
| **Metadata** | Data about data — information that describes communication patterns | IP addresses, timestamps, packet sizes |
| **OWASP** | Open Web Application Security Project — security guidelines organisation | OWASP IoT Top 10 |

---

## Port Scanning Terms

| Term | Definition | Example |
|------|------------|---------|
| **TCP Connect Scan** | Scanning method that completes full three-way handshake | `connect_ex()` returns 0 for open |
| **Open Port** | Port with a service accepting connections | Port 1883 with Mosquitto listening |
| **Closed Port** | Port with no service (RST response) | Port 12345 with nothing listening |
| **Filtered Port** | Port with no response (firewall DROP) | Firewall silently drops packets |
| **Three-Way Handshake** | TCP connection establishment: SYN → SYN-ACK → ACK | Required for TCP connect scan |
| **RST (Reset)** | TCP packet indicating connection refusal | Sent by closed ports |
| **SYN** | TCP synchronisation packet initiating connection | First packet of handshake |
| **Timeout** | Maximum wait time for a response | 0.5 seconds typical for scanning |

---

## IoT Terms

| Term | Definition | Example |
|------|------------|---------|
| **IoT (Internet of Things)** | Network of physical devices with embedded connectivity | Sensors, actuators, smart devices |
| **Sensor** | Device that measures physical properties | Temperature, humidity, motion sensor |
| **Actuator** | Device that performs physical actions | Motor, relay, valve |
| **Telemetry** | Automated collection and transmission of measurements | Sensor data sent via MQTT |
| **Edge Device** | Computing device at the network periphery | Raspberry Pi running local processing |
| **Gateway** | Device bridging IoT devices to broader networks | MQTT-to-HTTP bridge |

---

## Docker/Lab Terms

| Term | Definition | Example |
|------|------------|---------|
| **Container** | Isolated runtime environment for applications | `week13_mosquitto` container |
| **Docker Compose** | Tool for defining multi-container applications | `docker-compose.yml` |
| **Port Mapping** | Exposing container ports on host | `-p 1883:1883` |
| **Volume** | Persistent storage for container data | Certificate storage |
| **Bridge Network** | Docker network type allowing container communication | `week13net` |

---

## Commands Reference

### MQTT Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `mosquitto_sub` | Subscribe to MQTT topics | `mosquitto_sub -h localhost -t "#" -v` |
| `mosquitto_pub` | Publish MQTT messages | `mosquitto_pub -h localhost -t "test" -m "hello"` |
| `--cafile` | Specify CA certificate for TLS | `--cafile docker/configs/certs/ca.crt` |
| `-q` | Set QoS level (0, 1, 2) | `-q 1` |
| `-v` | Verbose output (show topics) | Shows `topic: message` format |

### Scanning Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `nc -zv` | Test port connectivity | `nc -zv localhost 1883` |
| `nmap -sT` | TCP connect scan | `nmap -sT -p 1883 localhost` |
| `nmap -sV` | Service version detection | `nmap -sV -p 1883 localhost` |

### Capture Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `tcpdump` | Capture network packets | `tcpdump -i any port 1883 -w capture.pcap` |
| `tshark` | Command-line Wireshark | `tshark -i any -f "port 1883"` |

### TLS Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `openssl s_client` | Test TLS connection | `openssl s_client -connect localhost:8883` |
| `openssl x509` | Examine certificate | `openssl x509 -in ca.crt -text -noout` |

---

## Acronyms

| Acronym | Full Form | Context |
|---------|-----------|---------|
| MQTT | Message Queuing Telemetry Transport | IoT messaging protocol |
| TLS | Transport Layer Security | Encryption protocol |
| QoS | Quality of Service | Delivery guarantees |
| TCP | Transmission Control Protocol | Reliable transport |
| UDP | User Datagram Protocol | Unreliable transport |
| CA | Certificate Authority | TLS trust hierarchy |
| CVE | Common Vulnerabilities and Exposures | Vulnerability database |
| ACL | Access Control List | Permission rules |
| IoT | Internet of Things | Connected devices |
| OWASP | Open Web Application Security Project | Security standards |
| RST | Reset | TCP connection refusal |
| SYN | Synchronise | TCP handshake initiation |
| DVWA | Damn Vulnerable Web Application | Training platform |
| FTP | File Transfer Protocol | File transfer |
| BPF | Berkeley Packet Filter | Capture filtering |

---

## Relationships Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              IoT ECOSYSTEM                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌──────────┐         ┌──────────┐         ┌──────────┐                   │
│   │  Sensor  │─publish─▶│  Broker  │◀─subscribe─│Dashboard │                │
│   │(Publisher)│         │(Mosquitto)│         │(Subscriber)│                │
│   └──────────┘         └────┬─────┘         └──────────┘                   │
│                              │                                               │
│                     Topics: building/floor1/temp                            │
│                     QoS: 0, 1, or 2                                         │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                           SECURITY LAYERS                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ TLS (Transport Layer Security)                                       │   │
│   │  • Encrypts: payload, topics, credentials                           │   │
│   │  • Exposes: IPs, ports, timing, sizes                               │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ Authentication                                                       │   │
│   │  • Username/password                                                 │   │
│   │  • Client certificates                                               │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ Authorisation (ACLs)                                                 │   │
│   │  • Topic-level permissions                                           │   │
│   │  • Read/write separation                                             │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

*Computer Networks — Week 13: IoT and Security*
*ASE Bucharest, CSIE | by ing. dr. Antonio Clim*
