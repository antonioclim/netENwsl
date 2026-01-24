# TCP/IP Layer Model

```mermaid
flowchart TB
    subgraph APP["Application Layer"]
        HTTP["HTTP"] & DNS["DNS"] & FTP["FTP"]
    end
    subgraph TRANS["Transport Layer"]
        TCP["TCP"] & UDP["UDP"]
    end
    subgraph NET["Network Layer"]
        IP["IP"] & ICMP["ICMP"]
    end
    subgraph LINK["Data Link Layer"]
        ETH["Ethernet"]
    end
    APP --> TRANS --> NET --> LINK
```

## Layer Functions

| Layer | Protocols | Function |
|-------|-----------|----------|
| Application | HTTP, DNS, FTP | User services |
| Transport | TCP, UDP | End-to-end delivery |
| Network | IP, ICMP | Addressing, routing |
| Data Link | Ethernet | Local delivery |

## LO Coverage
- LO1: ICMP (ping)
- LO2: TCP (sockets)
- LO4: All layers (PCAP)
