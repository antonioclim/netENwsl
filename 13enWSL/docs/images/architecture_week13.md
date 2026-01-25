# Week 13: Architecture Diagrams

**Computer Networks** — ASE, CSIE | ing. dr. Antonio Clim

This document contains Mermaid diagram definitions for Week 13 IoT and Security materials.

---

## 1. MQTT Publish-Subscribe Architecture

```mermaid
flowchart TB
    subgraph Publishers
        P1[Temperature Sensor]
        P2[Humidity Sensor]
        P3[Motion Detector]
    end
    
    subgraph Broker
        B[Mosquitto Broker<br/>Port 1883/8883]
    end
    
    subgraph Subscribers
        S1[Dashboard App]
        S2[Alert Service]
        S3[Data Logger]
    end
    
    P1 -->|PUBLISH sensors/temp| B
    P2 -->|PUBLISH sensors/humidity| B
    P3 -->|PUBLISH sensors/motion| B
    
    B -->|SUBSCRIBE sensors/#| S1
    B -->|SUBSCRIBE sensors/motion| S2
    B -->|SUBSCRIBE sensors/+| S3
```

---

## 2. MQTT QoS Handshakes

```mermaid
sequenceDiagram
    participant C as Client
    participant B as Broker
    
    Note over C,B: QoS 0 - At Most Once
    C->>B: PUBLISH (QoS 0)
    
    Note over C,B: QoS 1 - At Least Once
    C->>B: PUBLISH (QoS 1)
    B->>C: PUBACK
    
    Note over C,B: QoS 2 - Exactly Once
    C->>B: PUBLISH (QoS 2)
    B->>C: PUBREC
    C->>B: PUBREL
    B->>C: PUBCOMP
```

---

## 3. Laboratory Environment Topology

```mermaid
flowchart LR
    subgraph Host["Host Machine (WSL2)"]
        subgraph Docker["Docker Network: iot_lab_net"]
            M[Mosquitto<br/>1883, 8883]
            D[DVWA<br/>8080]
            V[vsftpd<br/>2121]
        end
        P[Portainer<br/>9000]
    end
    
    U[Student Workstation] -->|localhost:1883| M
    U -->|localhost:8080| D
    U -->|localhost:9000| P
    U -->|localhost:2121| V
```

---

## 4. TLS Certificate Chain

```mermaid
flowchart TB
    CA[Certificate Authority<br/>ca.crt]
    
    subgraph Server
        SC[Server Certificate<br/>server.crt]
        SK[Server Key<br/>server.key]
    end
    
    subgraph Client
        CC[Client Certificate<br/>client.crt]
        CK[Client Key<br/>client.key]
    end
    
    CA -->|Signs| SC
    CA -->|Signs| CC
    SC --- SK
    CC --- CK
```

---

## 5. OWASP IoT Vulnerability Categories

```mermaid
pie showData
    title OWASP IoT Top 10 Distribution
    "I1 Weak Passwords" : 20
    "I2 Insecure Services" : 15
    "I3 Insecure Interfaces" : 18
    "I4 Lack of Update" : 12
    "I5 Insecure Components" : 10
    "I6 Privacy Concerns" : 8
    "I7 Insecure Transfer" : 7
    "I8 Device Management" : 5
    "I9 Insecure Defaults" : 3
    "I10 Physical Security" : 2
```

---

## 6. Defence-in-Depth Layers

```mermaid
flowchart TB
    subgraph Physical["Physical Layer"]
        P1[Tamper Detection]
        P2[Secure Enclosure]
    end
    
    subgraph Network["Network Layer"]
        N1[VLAN Segmentation]
        N2[Firewall Rules]
        N3[IDS/IPS]
    end
    
    subgraph Transport["Transport Layer"]
        T1[TLS 1.3]
        T2[Certificate Pinning]
    end
    
    subgraph Application["Application Layer"]
        A1[Authentication]
        A2[Authorisation]
        A3[Input Validation]
    end
    
    Physical --> Network --> Transport --> Application
```

---

## 7. Exercise Workflow

```mermaid
flowchart LR
    subgraph "Ex 13.01"
        E1[Capture MQTT Traffic]
    end
    
    subgraph "Ex 13.02"
        E2[Configure ACLs]
    end
    
    subgraph "Ex 13.03"
        E3[Implement TLS]
    end
    
    subgraph "Ex 13.04"
        E4[Run Vuln Scanner]
    end
    
    E1 --> E2 --> E3 --> E4
    
    E1 -.->|Identifies weaknesses| E2
    E2 -.->|Requires encryption| E3
    E3 -.->|Validates security| E4
```

---

## Usage

These diagrams can be rendered using:

1. **GitHub**: Automatically renders in Markdown files
2. **VS Code**: Install Mermaid Preview extension
3. **Mermaid Live Editor**: https://mermaid.live/
4. **pandoc**: With mermaid-filter for PDF export

### Export to PNG

```bash
# Using mmdc (Mermaid CLI)
npm install -g @mermaid-js/mermaid-cli
mmdc -i architecture_week13.md -o diagram.png -t default
```

---

*Document version: 2.0 | Language: en-GB | Last updated: January 2026*
