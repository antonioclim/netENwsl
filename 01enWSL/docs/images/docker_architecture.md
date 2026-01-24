# Docker Lab Architecture

```mermaid
flowchart TB
    subgraph WIN["Windows Host"]
        WS["Wireshark"]
        BR["Browser :9000"]
    end
    subgraph WSL["WSL2 Ubuntu"]
        subgraph DOCKER["Docker Engine"]
            LAB["week1_lab<br/>172.20.1.x"]
            PORT["portainer<br/>:9000"]
        end
    end
    WIN ---|vEthernet WSL| WSL
    WS -.->|captures| LAB
    BR -->|HTTP| PORT
```

## Components

### Windows Layer
- Wireshark: Capture on vEthernet (WSL)
- Browser: Portainer at localhost:9000

### Docker Containers

| Container | Purpose | Port |
|-----------|---------|------|
| week1_lab | Lab exercises | 9090-9092 |
| portainer | Docker UI | 9000 (RESERVED) |

## Network

```yaml
Network: week1_network
Subnet: 172.20.1.0/24
Gateway: 172.20.1.1
```

## Traffic Flow

1. Exercise runs in week1_lab
2. Traffic through Docker bridge
3. Wireshark captures on vEthernet (WSL)
