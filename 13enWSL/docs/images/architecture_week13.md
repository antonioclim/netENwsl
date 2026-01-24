# 🏗️ Architecture Diagrams — Week 13

> Visual representations of the laboratory environment and protocol flows.

---

## 1. Laboratory Network Architecture

```mermaid
graph TB
    subgraph Windows["Windows 11 Host"]
        Browser["🌐 Browser"]
        Wireshark["🦈 Wireshark"]
        PS["PowerShell"]
    end
    
    subgraph WSL2["WSL2 Ubuntu 22.04"]
        subgraph Docker["Docker Engine"]
            subgraph Network["week13net (10.0.13.0/24)"]
                Mosquitto["🦟 Mosquitto<br/>10.0.13.100<br/>:1883 (plain)<br/>:8883 (TLS)"]
                DVWA["🎯 DVWA<br/>10.0.13.11<br/>:80 (HTTP)"]
                VSFTPD["📁 vsftpd<br/>10.0.13.12<br/>:21 (FTP)<br/>:6200 (stub)"]
            end
        end
        Portainer["🐳 Portainer<br/>:9000"]
        Scripts["📜 Python Scripts"]
    end
    
    Browser -->|":9000"| Portainer
    Browser -->|":8080"| DVWA
    Wireshark -.->|"capture"| Network
    PS -->|"wsl"| Scripts
    Scripts -->|"docker"| Docker
```

---

## 2. MQTT Publish/Subscribe Flow

```mermaid
sequenceDiagram
    participant P as Publisher<br/>(Sensor)
    participant B as Broker<br/>(Mosquitto)
    participant S as Subscriber<br/>(Dashboard)
    
    Note over P,S: Connection Phase
    P->>B: CONNECT
    B->>P: CONNACK (rc=0)
    S->>B: CONNECT
    B->>S: CONNACK (rc=0)
    
    Note over P,S: Subscription Phase
    S->>B: SUBSCRIBE "sensors/#" QoS=1
    B->>S: SUBACK (granted QoS=1)
    
    Note over P,S: Publish Phase
    P->>B: PUBLISH "sensors/temp" QoS=0
    B->>S: PUBLISH "sensors/temp" QoS=0
    
    P->>B: PUBLISH "sensors/temp" QoS=1
    B->>P: PUBACK
    B->>S: PUBLISH "sensors/temp" QoS=1
    S->>B: PUBACK
```

---

## 3. Plaintext vs TLS Traffic Comparison

```mermaid
graph LR
    subgraph Plaintext["Port 1883 (Plaintext)"]
        direction TB
        P1["Client"] -->|"CONNECT<br/>topic: sensors/temp<br/>payload: 23.5"| B1["Broker"]
        B1 -->|"CONNACK<br/>PUBLISH visible"| P1
        style P1 fill:#ffcccc
        style B1 fill:#ffcccc
    end
    
    subgraph TLS["Port 8883 (TLS)"]
        direction TB
        P2["Client"] -->|"🔒 Encrypted<br/>Application Data"| B2["Broker"]
        B2 -->|"🔒 Encrypted<br/>Application Data"| P2
        style P2 fill:#ccffcc
        style B2 fill:#ccffcc
    end
    
    subgraph Observer["Network Observer Sees"]
        O1["Plaintext: topics, payloads, credentials"]
        O2["TLS: IPs, ports, sizes, timing only"]
    end
```

---

## 4. Port Scanner State Machine

```mermaid
stateDiagram-v2
    [*] --> CreateSocket
    CreateSocket --> SetTimeout
    SetTimeout --> ConnectEx
    
    ConnectEx --> Open: return 0
    ConnectEx --> Closed: return non-zero<br/>(ECONNREFUSED)
    ConnectEx --> Filtered: timeout<br/>(no response)
    
    Open --> [*]: Service listening
    Closed --> [*]: No service (RST)
    Filtered --> [*]: Firewall DROP
```

---

## 5. TLS Handshake Sequence

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server (Broker)
    
    Note over C,S: Handshake Phase
    C->>S: ClientHello<br/>(supported ciphers, random)
    S->>C: ServerHello<br/>(chosen cipher, random)
    S->>C: Certificate<br/>(server's public key)
    S->>C: ServerHelloDone
    
    Note over C: Verify certificate<br/>against CA
    
    C->>S: ClientKeyExchange<br/>(pre-master secret)
    C->>S: ChangeCipherSpec
    C->>S: Finished (encrypted)
    
    S->>C: ChangeCipherSpec
    S->>C: Finished (encrypted)
    
    Note over C,S: Encrypted Application Data
    C->>S: 🔒 MQTT CONNECT
    S->>C: 🔒 MQTT CONNACK
```

---

## 6. Vulnerability Assessment Pipeline

```mermaid
flowchart TB
    subgraph Phase1["Phase 1: Discovery"]
        A1[Port Scan] --> A2[Identify Open Ports]
        A2 --> A3[List: 1883, 2121, 8080]
    end
    
    subgraph Phase2["Phase 2: Enumeration"]
        B1[Banner Grabbing] --> B2[Service Detection]
        B2 --> B3[Version Identification]
    end
    
    subgraph Phase3["Phase 3: Analysis"]
        C1[CVE Lookup] --> C2[Risk Assessment]
        C2 --> C3[Generate Report]
    end
    
    Phase1 --> Phase2
    Phase2 --> Phase3
    
    style A1 fill:#e1f5fe
    style B1 fill:#fff3e0
    style C1 fill:#ffebee
```

---

## 7. QoS Level Comparison

```mermaid
graph TB
    subgraph QoS0["QoS 0: At Most Once"]
        Q0P[Publisher] -->|"PUBLISH"| Q0B[Broker]
        Q0B -->|"PUBLISH"| Q0S[Subscriber]
    end
    
    subgraph QoS1["QoS 1: At Least Once"]
        Q1P[Publisher] -->|"PUBLISH"| Q1B[Broker]
        Q1B -->|"PUBACK"| Q1P
        Q1B -->|"PUBLISH"| Q1S[Subscriber]
        Q1S -->|"PUBACK"| Q1B
    end
    
    subgraph QoS2["QoS 2: Exactly Once"]
        Q2P[Publisher] -->|"PUBLISH"| Q2B[Broker]
        Q2B -->|"PUBREC"| Q2P
        Q2P -->|"PUBREL"| Q2B
        Q2B -->|"PUBCOMP"| Q2P
    end
```

---

## How to Use These Diagrams

1. **In presentations:** Copy Mermaid code to [Mermaid Live Editor](https://mermaid.live/) and export as image
2. **In GitHub:** Mermaid renders automatically in `.md` files
3. **In VS Code:** Install "Markdown Preview Mermaid Support" extension
4. **For print:** Export as SVG for best quality

---

*Computer Networks — Week 13: IoT and Security*
*ASE Bucharest, CSIE | by ing. dr. Antonio Clim*
