# Commands Cheatsheet — Week 2

> NETWORKING class - ASE, CSIE Bucharest | by ing. dr. Antonio Clim

## Laboratory Management

### Starting the Environment

```powershell
# Start all containers
python scripts/start_lab.py

# Check service status
python scripts/start_lab.py --status

# Rebuild images (after Dockerfile changes)
python scripts/start_lab.py --rebuild
```

### Stopping the Environment

```powershell
# Graceful stop (preserves data)
python scripts/stop_lab.py

# Full cleanup (removes volumes)
python scripts/cleanup.py --full

# Dry run (shows what would be removed)
python scripts/cleanup.py --dry-run
```

## Docker Commands

### Container Management

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# View container logs
docker logs week2_lab

# Follow logs in real time
docker logs -f week2_lab

# Execute command inside container
docker exec -it week2_lab bash

# Check container resource usage
docker stats week2_lab
```

### Network Inspection

```bash
# List networks
docker network ls

# Inspect network details
docker network inspect week2_network

# View container IP addresses
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' week2_lab
```

### Cleanup Commands

```bash
# Remove stopped containers
docker container prune

# Remove unused networks
docker network prune

# Remove unused volumes
docker volume prune

# Remove all unused resources
docker system prune -a
```

## Socket Programming Commands

### TCP Server (Exercise 1)

```bash
# Start threaded server (default)
python src/exercises/ex_2_01_tcp.py server

# Start iterative server
python src/exercises/ex_2_01_tcp.py server --mode iterative

# Start on custom port
python src/exercises/ex_2_01_tcp.py server --port 8080

# Start client
python src/exercises/ex_2_01_tcp.py client

# Run load test (10 concurrent clients)
python src/exercises/ex_2_01_tcp.py load --clients 10
```

### UDP Server (Exercise 2)

```bash
# Start UDP server
python src/exercises/ex_2_02_udp.py server

# Interactive client
python src/exercises/ex_2_02_udp.py client

# Single command client
python src/exercises/ex_2_02_udp.py client --command "upper:hello"

# Test protocol commands
ping
upper:hello world
lower:HELLO WORLD
reverse:networking
echo:test message
time
help
```

## Network Debugging

### Using netcat

```bash
# TCP connection test
nc -v localhost 9090

# UDP connection test
nc -vu localhost 9091

# Listen on TCP port
nc -l 9090

# Listen on UDP port
nc -lu 9091
```

### Using tcpdump

```bash
# Capture all traffic on interface
tcpdump -i eth0

# Capture TCP traffic on port 9090
tcpdump -i eth0 tcp port 9090

# Capture UDP traffic on port 9091
tcpdump -i eth0 udp port 9091

# Save to file
tcpdump -i eth0 -w capture.pcap

# Read from file
tcpdump -r capture.pcap

# Verbose output with hex dump
tcpdump -i eth0 -X port 9090
```

### Using tshark

```bash
# Capture with display filter
tshark -i eth0 -Y "tcp.port == 9090"

# Show packet summary
tshark -i eth0 -c 10

# Extract fields
tshark -i eth0 -T fields -e ip.src -e ip.dst -e tcp.port
```

## Wireshark Filters

### Display Filters

```
# TCP traffic on specific port
tcp.port == 9090

# UDP traffic on specific port
udp.port == 9091

# TCP handshake packets
tcp.flags.syn == 1

# TCP data packets
tcp.len > 0

# Localhost traffic
ip.addr == 127.0.0.1

# Container network traffic
ip.addr == 10.0.2.0/24

# TCP retransmissions
tcp.analysis.retransmission

# Packets with specific content
frame contains "hello"
```

### Capture Filters

```
# Specific port
port 9090

# TCP only
tcp

# UDP only
udp

# Host filter
host 10.0.2.2

# Exclude SSH
not port 22
```

## Python Network Utilities

### Socket Creation

```python
import socket

# TCP socket
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# UDP socket
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Enable address reuse
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```

### Quick Port Check

```python
import socket

def is_port_available(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0
```

## Testing Commands

```powershell
# Run smoke test
python tests/smoke_test.py

# Run all tests
python tests/test_exercises.py

# Run specific test
python tests/test_exercises.py --exercise 1

# Run with verbose output
python tests/test_exercises.py -v
```

## Demonstrations

```powershell
# Demo 1: TCP vs UDP comparison
python scripts/run_demo.py --demo 1

# Demo 2: Concurrent server handling
python scripts/run_demo.py --demo 2

# List available demos
python scripts/run_demo.py --list
```

---

*NETWORKING class - ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
