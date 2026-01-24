# 📊 Architecture Diagrams — Week 7
## Computer Networks — ASE, CSIE | Computer Networks Laboratory

> Visual diagrams illustrating key concepts for packet interception, filtering
> and defensive port probing.

---

## Lab Environment Architecture

```mermaid
graph TB
    subgraph Windows Host
        W[Wireshark]
        P[Portainer :9000]
    end
    
    subgraph WSL2
        subgraph Docker Network 10.0.7.0/24
            TS[TCP Server<br/>10.0.7.100:9090]
            TC[TCP Client<br/>10.0.7.11]
            UR[UDP Receiver<br/>10.0.7.200:9091]
            US[UDP Sender<br/>10.0.7.12]
            FW[Packet Filter<br/>10.0.7.50:8888]
        end
        TD[tcpdump]
    end
    
    W -.->|vEthernet WSL| TD
    P -.->|Docker API| Docker Network
    TC -->|TCP :9090| TS
    US -->|UDP :9091| UR
    TC -.->|via| FW
```

---

## TCP Three-Way Handshake

```mermaid
sequenceDiagram
    participant C as TCP Client<br/>10.0.7.11
    participant S as TCP Server<br/>10.0.7.100:9090
    
    Note over C,S: Connection Establishment
    C->>S: SYN (seq=1000)
    S->>C: SYN-ACK (seq=2000, ack=1001)
    C->>S: ACK (seq=1001, ack=2001)
    
    Note over C,S: Data Transfer
    C->>S: PSH-ACK + "Hello"
    S->>C: ACK
    S->>C: PSH-ACK + "Hello"
    
    Note over C,S: Connection Termination
    C->>S: FIN-ACK
    S->>C: FIN-ACK
    C->>S: ACK
```

---

## DROP vs REJECT Comparison

```mermaid
sequenceDiagram
    participant C as Client
    participant FW as Firewall
    participant S as Server
    
    rect rgb(255, 200, 200)
        Note over C,S: Scenario A: REJECT Action
        C->>FW: SYN (connection attempt)
        FW--xS: ❌ Blocked
        FW->>C: RST (immediate refusal)
        Note over C: Client sees:<br/>"Connection refused"
    end
    
    rect rgb(200, 200, 255)
        Note over C,S: Scenario B: DROP Action
        C->>FW: SYN (attempt 1)
        FW--xS: ❌ Blocked (silent)
        Note over C: No response...
        C->>FW: SYN (attempt 2, t+1s)
        FW--xS: ❌ Blocked (silent)
        C->>FW: SYN (attempt 3, t+3s)
        FW--xS: ❌ Blocked (silent)
        Note over C: Client sees:<br/>"Connection timed out"
    end
```

---

## Port States

```mermaid
stateDiagram-v2
    [*] --> Open: Service listening
    [*] --> Closed: No service
    [*] --> Filtered: Firewall blocking
    
    Open --> Open: Connection accepted
    Closed --> Closed: RST sent to client
    Filtered --> Filtered: No response (DROP)
    
    Open: Port OPEN<br/>Service accepts connections<br/>SYN → SYN-ACK
    Closed: Port CLOSED<br/>No service listening<br/>SYN → RST
    Filtered: Port FILTERED<br/>Firewall blocking probes<br/>SYN → timeout
```

---

## iptables Rule Processing

```mermaid
flowchart TD
    A[Incoming Packet] --> B{Chain: INPUT}
    B --> C{Rule 1 Match?}
    C -->|Yes| D[Action: ACCEPT/DROP/REJECT]
    C -->|No| E{Rule 2 Match?}
    E -->|Yes| F[Action]
    E -->|No| G{Rule N Match?}
    G -->|Yes| H[Action]
    G -->|No| I[Default Policy]
    
    D --> J[Packet Processed]
    F --> J
    H --> J
    I --> J
    
    style D fill:#90EE90
    style F fill:#90EE90
    style H fill:#90EE90
    style I fill:#FFB6C1
```

**Key Concept:** First match wins. Rule order matters!

---

## Firewall Profile Application Flow

```mermaid
flowchart LR
    A[Profile JSON] --> B[firewallctl.py]
    B --> C{Validate<br/>Structure}
    C -->|Invalid| D[Error Message]
    C -->|Valid| E[Clear Chain]
    E --> F[Set Policy]
    F --> G[Apply Rules<br/>In Order]
    G --> H[Verify Rules]
    H --> I[Profile Active]
    
    style D fill:#FFB6C1
    style I fill:#90EE90
```

---

## Packet Capture Analysis Workflow

```mermaid
flowchart TB
    subgraph Capture
        A[Start tcpdump/<br/>Wireshark] --> B[Generate Traffic]
        B --> C[Stop Capture]
        C --> D[Save PCAP]
    end
    
    subgraph Analysis
        D --> E[Open in Wireshark]
        E --> F[Apply Filters]
        F --> G{Identify Pattern}
        G -->|Handshake| H[Check SYN-ACK-ACK]
        G -->|Timeout| I[Check Retransmits]
        G -->|Blocked| J[Check RST/ICMP]
    end
    
    subgraph Diagnosis
        H --> K[Connection OK]
        I --> L[Possible DROP]
        J --> M[Possible REJECT]
    end
```

---

## Learning Path

```mermaid
graph LR
    subgraph Week 7 Topics
        LO1[LO1: Identify<br/>Packet Fields]
        LO2[LO2: Explain<br/>Failures]
        LO3[LO3: Implement<br/>Filtering]
        LO4[LO4: Analyse<br/>Captures]
        LO5[LO5: Design<br/>Profiles]
        LO6[LO6: Evaluate<br/>DROP vs REJECT]
    end
    
    LO1 --> LO2
    LO2 --> LO3
    LO3 --> LO4
    LO4 --> LO5
    LO4 --> LO6
    
    style LO1 fill:#E8F5E9
    style LO2 fill:#E3F2FD
    style LO3 fill:#FFF3E0
    style LO4 fill:#F3E5F5
    style LO5 fill:#FFEBEE
    style LO6 fill:#E0F7FA
```

---

## Viewing These Diagrams

### Option 1: GitHub/GitLab
Mermaid diagrams render automatically in Markdown files on GitHub and GitLab.

### Option 2: VS Code
Install the "Markdown Preview Mermaid Support" extension.

### Option 3: Online
Copy diagram code to [mermaid.live](https://mermaid.live/) for interactive editing.

### Option 4: Export as Images
```bash
# Using mermaid-cli
npm install -g @mermaid-js/mermaid-cli
mmdc -i docs/diagrams.md -o docs/images/diagram.png
```

---

*Computer Networks — Week 7: Packet Interception, Filtering and Defensive Port Probing*  
*ASE Bucharest, CSIE | Computer Networks Laboratory*
