# Commands Cheatsheet

> NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

A quick reference for essential commands used in Week 3 laboratory exercises.

---

## Docker Commands

### Container Management

```powershell
# Start laboratory environment
python scripts/start_lab.py

# Check running containers
docker ps

# Check all containers (including stopped)
docker ps -a

# View container logs
docker logs week3_server
docker logs week3_router --follow    # Live log stream
docker logs --tail 50 week3_client   # Last 50 lines

# Execute command inside container
docker exec -it week3_client bash
docker exec week3_server python3 /app/src/apps/echo_server.py

# Restart specific container
docker restart week3_server

# Stop laboratory environment
python scripts/stop_lab.py
```

### Docker Compose Operations

```powershell
# From the docker/ directory
cd docker

# Start services
docker compose up -d

# Rebuild and start
docker compose up -d --build

# Stop services (preserve volumes)
docker compose down

# Stop and remove volumes
docker compose down -v

# View service status
docker compose ps

# Scale services
docker compose up -d --scale client=3
```

### Network Inspection

```powershell
# List Docker networks
docker network ls

# Inspect network details
docker network inspect week3_network

# View container IP addresses
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' week3_server
```

### Resource Management

```powershell
# View resource usage
docker stats

# Clean unused resources
docker system prune

# Remove all stopped containers
docker container prune

# Remove unused networks
docker network prune

# Full cleanup (caution!)
docker system prune -a --volumes
```

---

## Packet Capture Commands

### tcpdump (Inside Containers)

```bash
# Basic capture on interface
tcpdump -i eth0

# Capture with verbose output
tcpdump -i eth0 -v

# Save to file
tcpdump -i eth0 -w /tmp/capture.pcap

# Read from file
tcpdump -r /tmp/capture.pcap

# Capture specific port
tcpdump -i eth0 port 8080

# Capture UDP only
tcpdump -i eth0 udp

# Capture TCP only
tcpdump -i eth0 tcp

# Capture broadcast traffic
tcpdump -i eth0 broadcast
tcpdump -i eth0 'dst host 255.255.255.255'

# Capture multicast traffic
tcpdump -i eth0 multicast
tcpdump -i eth0 'dst net 224.0.0.0/4'

# Capture specific host
tcpdump -i eth0 host 172.20.0.10

# Capture between two hosts
tcpdump -i eth0 'host 172.20.0.10 and host 172.20.0.100'

# Show packet contents in hex and ASCII
tcpdump -i eth0 -X port 8080

# Capture N packets then stop
tcpdump -i eth0 -c 10 port 5007

# Non-promiscuous mode
tcpdump -i eth0 -p
```

### Capture Script Usage

```powershell
# Start capture on server container
python scripts/capture_traffic.py --container week3_server --output pcap/server.pcap

# Capture with filter
python scripts/capture_traffic.py --container week3_client --filter "port 5007" --output pcap/broadcast.pcap

# Capture with duration limit
python scripts/capture_traffic.py --container week3_router --duration 30 --output pcap/tunnel.pcap
```

---

## Wireshark Filters

### Display Filters (Applied After Capture)

**Protocol Filters:**
```
tcp
udp
icmp
igmp
arp
```

**Address Filters:**
```
ip.addr == 172.20.0.10           # Source or destination
ip.src == 172.20.0.100           # Source only
ip.dst == 172.20.0.254           # Destination only
eth.addr == aa:bb:cc:dd:ee:ff    # MAC address
```

**Port Filters:**
```
tcp.port == 8080                  # TCP source or dest port
tcp.srcport == 9090               # TCP source port
tcp.dstport == 8080               # TCP destination port
udp.port == 5007                  # UDP port
```

**Broadcast/Multicast Filters:**
```
eth.dst == ff:ff:ff:ff:ff:ff      # Ethernet broadcast
ip.dst == 255.255.255.255         # IP limited broadcast
ip.dst >= 224.0.0.0 and ip.dst <= 239.255.255.255   # Multicast range
ip.dst == 239.1.1.1               # Specific multicast group
```

**TCP Analysis Filters:**
```
tcp.flags.syn == 1                # SYN packets (connection start)
tcp.flags.fin == 1                # FIN packets (connection end)
tcp.flags.rst == 1                # RST packets (connection reset)
tcp.analysis.retransmission       # Retransmitted packets
tcp.analysis.duplicate_ack        # Duplicate ACKs
tcp.analysis.zero_window          # Zero window conditions
```

**Combined Filters:**
```
ip.addr == 172.20.0.10 and tcp.port == 8080
udp.port == 5007 and ip.dst == 255.255.255.255
tcp.port == 9090 or tcp.port == 8080
!(arp or icmp)                    # Exclude ARP and ICMP
```

### Capture Filters (Applied During Capture)

```
host 172.20.0.10
net 172.20.0.0/24
port 8080
tcp port 9090
udp port 5007
broadcast
multicast
```

### Following Streams

1. Right-click on a TCP packet
2. Select "Follow" → "TCP Stream"
3. View complete conversation
4. Filter automatically applied: `tcp.stream eq N`

---

## Network Utilities

### netcat (nc)

```bash
# TCP client - connect to server
nc server 8080
nc -v server 8080            # Verbose mode
echo "Hello" | nc server 8080

# TCP server - listen for connections
nc -l -p 8080

# UDP client
nc -u server 5007
echo "Broadcast test" | nc -u -b 255.255.255.255 5007

# UDP listener
nc -u -l -p 5007

# Port scanning
nc -zv server 8080
nc -zv server 8000-8100      # Range scan

# File transfer
# Receiver: nc -l -p 9999 > received_file
# Sender:   nc server 9999 < file_to_send
```

### Testing Connectivity

```bash
# Ping host
ping -c 4 server

# Check port availability
nc -zv server 8080

# TCP connection test
python3 -c "import socket; s=socket.socket(); s.connect(('server', 8080)); print('Connected'); s.close()"

# DNS lookup (if available)
nslookup server
dig server
```

### iperf3 (Network Performance)

```bash
# Server mode
iperf3 -s

# Client mode - TCP test
iperf3 -c server

# UDP test
iperf3 -c server -u

# Bidirectional test
iperf3 -c server -d

# Specify bandwidth
iperf3 -c server -u -b 100M

# Test duration
iperf3 -c server -t 30
```

---

## Python Socket Quick Reference

### UDP Broadcast Sender

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.sendto(b"Hello", ("255.255.255.255", 5007))
sock.close()
```

### UDP Broadcast Receiver

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("", 5007))
data, addr = sock.recvfrom(1024)
print(f"Received: {data} from {addr}")
sock.close()
```

### UDP Multicast Sender

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
sock.sendto(b"Hello Multicast", ("239.1.1.1", 5008))
sock.close()
```

### UDP Multicast Receiver

```python
import socket
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("", 5008))

mreq = struct.pack("4sl", socket.inet_aton("239.1.1.1"), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

data, addr = sock.recvfrom(1024)
print(f"Received: {data} from {addr}")
sock.close()
```

### TCP Echo Client

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("server", 8080))
sock.sendall(b"Hello Server")
response = sock.recv(1024)
print(f"Received: {response}")
sock.close()
```

---

## Laboratory Shortcuts

### Quick Tests

```powershell
# Verify environment
python setup/verify_environment.py

# Test all exercises
python tests/test_exercises.py

# Test specific exercise
python tests/test_exercises.py --exercise 1

# Run smoke test
python tests/smoke_test.py

# Run demonstration
python scripts/run_demo.py --demo broadcast
```

### Common Workflows

```powershell
# Start lab and run demo
python scripts/start_lab.py
python scripts/run_demo.py --demo all

# Capture traffic during exercise
# Terminal 1:
python scripts/capture_traffic.py --container week3_server --output pcap/exercise1.pcap

# Terminal 2:
python tests/test_exercises.py --exercise 1

# Cleanup after lab
python scripts/cleanup.py --full
```

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
