# Commands Cheatsheet

> Week 5 - NETWORKING class - ASE, Informatics
>
> by Revolvix

## Laboratory Management

### Starting the Lab
```powershell
# Start all containers
python scripts/start_lab.py

# Start with forced rebuild
python scripts/start_lab.py --rebuild

# Check status only
python scripts/start_lab.py --status
```

### Stopping the Lab
```powershell
# Stop containers (preserve data)
python scripts/stop_lab.py

# Full cleanup (remove all data)
python scripts/cleanup.py --full
```

## Exercise Commands

### CIDR Analysis
```powershell
# Basic analysis
docker exec week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py analyze 192.168.10.14/26

# With verbose output (binary representation)
docker exec week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py analyze 192.168.10.14/26 --verbose

# JSON output
docker exec week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py analyze 192.168.10.14/26 --json

# Binary conversion
docker exec week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py binary 192.168.1.1
```

### FLSM Subnetting
```powershell
# Split into 4 equal subnets
docker exec week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py flsm 192.168.100.0/24 4

# Split into 8 equal subnets
docker exec week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py flsm 10.0.0.0/24 8

# JSON output
docker exec week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py flsm 10.0.0.0/24 4 --json
```

### VLSM Allocation
```powershell
# Allocate for multiple host requirements
docker exec week5_python python /app/src/exercises/ex_5_02_vlsm_ipv6.py vlsm 172.16.0.0/24 60 20 10 2

# Complex scenario
docker exec week5_python python /app/src/exercises/ex_5_02_vlsm_ipv6.py vlsm 10.10.0.0/22 200 100 50 25 10 2 2 2
```

### IPv6 Operations
```powershell
# Compress IPv6 address
docker exec week5_python python /app/src/exercises/ex_5_02_vlsm_ipv6.py ipv6 2001:0db8:0000:0000:0000:0000:0000:0001

# Expand IPv6 address
docker exec week5_python python /app/src/exercises/ex_5_02_vlsm_ipv6.py ipv6-expand 2001:db8::1

# Generate subnets
docker exec week5_python python /app/src/exercises/ex_5_02_vlsm_ipv6.py ipv6-subnets 2001:db8:10::/48 64 10

# Show address types
docker exec week5_python python /app/src/exercises/ex_5_02_vlsm_ipv6.py ipv6-types
```

## Docker Commands

### Container Management
```powershell
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Shell into Python container
docker exec -it week5_python bash

# View container logs
docker logs week5_python
docker logs week5_udp-server

# Follow logs in real-time
docker logs -f week5_python
```

### Network Inspection
```powershell
# List Docker networks
docker network ls

# Inspect lab network
docker network inspect week5_labnet

# Show container IP addresses
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' week5_python
```

## Networking Commands (Inside Containers)

### IP Configuration
```bash
# Show all interfaces
ip addr

# Show specific interface
ip addr show eth0

# Show routing table
ip route

# Show ARP cache
ip neigh
```

### Connectivity Testing
```bash
# Ping another container
ping -c 3 10.5.0.20

# Ping with specific interface
ping -I eth0 10.5.0.20

# Traceroute
traceroute 10.5.0.1
```

### Packet Capture
```bash
# Capture all traffic
tcpdump -i eth0

# Capture and save to file
tcpdump -i eth0 -w /app/pcap/capture.pcap

# Capture specific protocol
tcpdump -i eth0 icmp
tcpdump -i eth0 udp port 9999

# Capture with ASCII output
tcpdump -i eth0 -A

# Read saved capture
tcpdump -r /app/pcap/capture.pcap
```

### UDP Testing
```bash
# Listen on UDP port
nc -ul 9999

# Send UDP message
echo "test" | nc -u 10.5.0.20 9999
```

## Wireshark Filters

### Protocol Filters
```
# ICMP traffic
icmp

# UDP traffic
udp

# TCP traffic
tcp

# IPv6 traffic
ipv6
```

### Address Filters
```
# Traffic to/from specific IP
ip.addr == 10.5.0.10

# Traffic to/from subnet
ip.addr == 10.5.0.0/24

# Source address
ip.src == 10.5.0.10

# Destination address
ip.dst == 10.5.0.20
```

### Port Filters
```
# UDP port 9999
udp.port == 9999

# TCP port 80
tcp.port == 80

# Either source or destination port
port == 9999
```

### Combined Filters
```
# ICMP from specific host
icmp and ip.src == 10.5.0.10

# UDP to port 9999 from container
udp.port == 9999 and ip.src == 10.5.0.30

# Exclude ICMP
not icmp
```

## Quick Reference

### Subnet Sizes
| Prefix | Hosts | Addresses | Mask |
|--------|-------|-----------|------|
| /24 | 254 | 256 | 255.255.255.0 |
| /25 | 126 | 128 | 255.255.255.128 |
| /26 | 62 | 64 | 255.255.255.192 |
| /27 | 30 | 32 | 255.255.255.224 |
| /28 | 14 | 16 | 255.255.255.240 |
| /29 | 6 | 8 | 255.255.255.248 |
| /30 | 2 | 4 | 255.255.255.252 |

### Private Address Ranges
| Class | Range | CIDR |
|-------|-------|------|
| A | 10.0.0.0 - 10.255.255.255 | 10.0.0.0/8 |
| B | 172.16.0.0 - 172.31.255.255 | 172.16.0.0/12 |
| C | 192.168.0.0 - 192.168.255.255 | 192.168.0.0/16 |

### Power of 2 Quick Reference
| 2^n | Value |
|-----|-------|
| 2^2 | 4 |
| 2^3 | 8 |
| 2^4 | 16 |
| 2^5 | 32 |
| 2^6 | 64 |
| 2^7 | 128 |
| 2^8 | 256 |
