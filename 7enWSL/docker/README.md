# Docker Configuration for Week 7

> NETWORKING class - ASE, Informatics | by Revolvix

## Overview

This directory contains the Docker Compose configuration for the Week 7 laboratory environment. The configuration creates an isolated network with TCP and UDP services for packet interception and filtering exercises.

## Services

| Service | Container Name | IP Address | Port |
|---------|---------------|------------|------|
| TCP Echo Server | week7_tcp_server | 10.0.7.100 | 9090 |
| TCP Client | week7_tcp_client | 10.0.7.11 | - |
| UDP Receiver | week7_udp_receiver | 10.0.7.200 | 9091 |
| UDP Sender | week7_udp_sender | 10.0.7.12 | - |
| Packet Filter | week7_packet_filter | 10.0.7.50 | 8888 |

## Network

- Network name: `week7net`
- Subnet: `10.0.7.0/24`
- Gateway: `10.0.7.1`

## Usage

### Start core services
```bash
docker compose up -d tcp_server udp_receiver
```

### Run demonstration (includes clients)
```bash
docker compose --profile demo up
```

### Enable packet filter proxy
```bash
docker compose --profile proxy up -d
```

### View logs
```bash
docker compose logs -f tcp_server
docker compose logs -f udp_receiver
```

### Stop all services
```bash
docker compose down
```

### Full cleanup
```bash
docker compose down -v --remove-orphans
docker network rm week7net 2>/dev/null || true
```

## Profiles

The compose file uses profiles for optional services:

- **default**: tcp_server, udp_receiver (always started)
- **demo**: tcp_client, udp_sender (for demonstrations)
- **proxy**: packet_filter (application-layer filtering)

## Volumes

- `../artifacts`: Shared directory for logs and outputs
- `../src`: Source code mounted read-only

## Health Checks

The TCP server includes a health check that verifies the port is accepting connections. Other services depend on this health check before starting.

## Troubleshooting

### Port already in use
```bash
# Find process using port 9090
netstat -ano | findstr :9090
# Or on Linux/WSL
ss -tlnp | grep 9090
```

### Network already exists
```bash
docker network rm week7net
```

### Containers not starting
```bash
docker compose logs
docker compose ps -a
```
