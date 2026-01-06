# Commands Cheatsheet

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by Revolvix

Quick reference for commonly used commands in Week 4 laboratory exercises.

---

## Docker Commands

### Container Management

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Start containers defined in docker-compose.yml
docker compose up -d

# Stop containers
docker compose down

# View container logs
docker compose logs -f week4-lab

# Execute command in running container
docker exec -it week4-lab bash

# View container resource usage
docker stats
```

### Network Management

```bash
# List Docker networks
docker network ls

# Inspect network configuration
docker network inspect week4_network

# View container IP addresses
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' week4-lab
```

### Image Management

```bash
# Build image from Dockerfile
docker compose build

# Force rebuild without cache
docker compose build --no-cache

# List images
docker images

# Remove unused images
docker image prune
```

### Volume Management

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect week4_artifacts

# Remove unused volumes
docker volume prune
```

---

## tcpdump Commands

### Basic Capture

```bash
# Capture on interface eth0
sudo tcpdump -i eth0

# Capture with packet contents (hex and ASCII)
sudo tcpdump -i eth0 -XX

# Capture first N packets
sudo tcpdump -i eth0 -c 100

# Capture to file
sudo tcpdump -i eth0 -w capture.pcap

# Read from file
tcpdump -r capture.pcap
```

### Filtering

```bash
# Capture specific port
sudo tcpdump -i eth0 port 5400

# Capture TCP only
sudo tcpdump -i eth0 tcp

# Capture UDP only
sudo tcpdump -i eth0 udp

# Capture specific host
sudo tcpdump -i eth0 host 172.28.0.2

# Capture source/destination
sudo tcpdump -i eth0 src host 172.28.0.2
sudo tcpdump -i eth0 dst port 5401

# Combine filters
sudo tcpdump -i eth0 'tcp and port 5400'
sudo tcpdump -i eth0 'host 172.28.0.2 and (port 5400 or port 5401)'
```

### Output Options

```bash
# Don't resolve hostnames
sudo tcpdump -i eth0 -n

# Don't resolve ports to service names
sudo tcpdump -i eth0 -nn

# Verbose output
sudo tcpdump -i eth0 -v
sudo tcpdump -i eth0 -vv
sudo tcpdump -i eth0 -vvv

# Print absolute sequence numbers
sudo tcpdump -i eth0 -S

# Print in ASCII
sudo tcpdump -i eth0 -A

# Timestamp options
sudo tcpdump -i eth0 -tttt  # Human readable
```

### Protocol-Specific Examples

```bash
# TEXT protocol (TCP:5400)
sudo tcpdump -i eth0 -nn -A 'tcp port 5400'

# BINARY protocol (TCP:5401)
sudo tcpdump -i eth0 -nn -XX 'tcp port 5401'

# UDP sensor (UDP:5402)
sudo tcpdump -i eth0 -nn -XX 'udp port 5402'
```

---

## tshark Commands

### Basic Capture

```bash
# Capture on interface
tshark -i eth0

# Capture to file
tshark -i eth0 -w capture.pcap

# Read from file
tshark -r capture.pcap

# Capture N packets
tshark -i eth0 -c 100
```

### Filtering

```bash
# Capture filter (BPF syntax)
tshark -i eth0 -f 'port 5400'

# Display filter (Wireshark syntax)
tshark -i eth0 -Y 'tcp.port == 5400'

# Combined
tshark -i eth0 -f 'port 5400' -Y 'tcp.flags.syn == 1'
```

### Output Formatting

```bash
# Specific fields
tshark -r capture.pcap -T fields -e frame.number -e ip.src -e ip.dst

# JSON output
tshark -r capture.pcap -T json

# Summary statistics
tshark -r capture.pcap -q -z io,stat,1

# Conversation statistics
tshark -r capture.pcap -q -z conv,tcp
```

### Protocol-Specific

```bash
# Follow TCP stream
tshark -r capture.pcap -z follow,tcp,ascii,0

# Decode as specific protocol
tshark -r capture.pcap -d tcp.port==5400,http
```

---

## Netcat Commands

### TCP Client

```bash
# Connect to TCP server
nc localhost 5400

# Connect with timeout
nc -w 5 localhost 5400

# Send data and exit
echo "PING" | nc localhost 5400

# Interactive mode with timing
nc -q 1 localhost 5400
```

### TCP Server

```bash
# Listen on TCP port
nc -l 5400

# Keep listening after client disconnects
nc -lk 5400

# Listen with verbose output
nc -lv 5400
```

### UDP

```bash
# Send UDP datagram
echo "data" | nc -u localhost 5402

# Listen for UDP
nc -lu 5402

# UDP with source port
nc -u -p 12345 localhost 5402
```

### Testing Protocols

```bash
# Test TEXT protocol
echo "PING" | nc localhost 5400

# Test with newline (required for some protocols)
echo -e "SET key1 value1\n" | nc localhost 5400

# Binary data
printf '\x4e\x50\x01\x01' | nc localhost 5401

# Hex dump response
nc localhost 5400 | xxd
```

---

## Python Protocol Testing

### TCP Client (One-Shot)

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 5400))
sock.send(b'PING\n')
response = sock.recv(1024)
print(response.decode())
sock.close()
```

### TCP Client (Length-Prefix)

```python
import socket
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 5401))

# Send with length prefix
message = b'Hello'
header = struct.pack('>H', len(message))
sock.send(header + message)

# Receive with length prefix
header = sock.recv(2)
length = struct.unpack('>H', header)[0]
data = sock.recv(length)
sock.close()
```

### UDP Client

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b'sensor_data', ('localhost', 5402))
response, addr = sock.recvfrom(1024)
print(f"Received from {addr}: {response}")
sock.close()
```

### CRC-32 Calculation

```python
import zlib

data = b'Hello, World!'
crc = zlib.crc32(data) & 0xFFFFFFFF
print(f"CRC-32: {crc:#010x}")

# Verify
received_data = b'Hello, World!'
received_crc = 0xec4ac3d0
calculated = zlib.crc32(received_data) & 0xFFFFFFFF
valid = (calculated == received_crc)
```

---

## Wireshark Display Filters

### TCP Filters

```
# Specific port
tcp.port == 5400

# Source port
tcp.srcport == 5400

# Destination port
tcp.dstport == 5400

# Port range
tcp.port >= 5400 && tcp.port <= 5402

# TCP flags
tcp.flags.syn == 1
tcp.flags.ack == 1
tcp.flags.fin == 1
tcp.flags.reset == 1

# Connection establishment
tcp.flags.syn == 1 && tcp.flags.ack == 0

# TCP stream
tcp.stream == 0

# Retransmissions
tcp.analysis.retransmission
```

### UDP Filters

```
# Specific port
udp.port == 5402

# UDP length
udp.length > 20

# Checksum errors
udp.checksum.status == "Bad"
```

### IP Filters

```
# Source IP
ip.src == 172.28.0.2

# Destination IP
ip.dst == 172.28.0.1

# IP range
ip.addr == 172.28.0.0/16
```

### Content Filters

```
# Contains string (case-sensitive)
frame contains "PING"

# TCP payload contains
tcp.payload contains "SET"

# Regular expression
tcp.payload matches ".*key[0-9].*"
```

### Combined Filters

```
# TEXT protocol commands
tcp.port == 5400 && tcp.payload contains "SET"

# BINARY protocol with errors
tcp.port == 5401 && tcp.analysis.retransmission

# UDP sensor traffic
udp.port == 5402 && udp.length == 31
```

---

## Shell Utilities

### Hex Tools

```bash
# Hex dump of file
xxd file.bin

# Hex to binary
echo "4e50" | xxd -r -p > output.bin

# Binary to hex
xxd -p file.bin

# od (octal dump)
od -A x -t x1z -v file.bin
```

### Network Utilities

```bash
# Check open ports
ss -tlnp
netstat -tlnp

# Check port connectivity
timeout 1 bash -c 'cat < /dev/null > /dev/tcp/localhost/5400' && echo "Open"

# DNS lookup
nslookup hostname
dig hostname

# IP configuration
ip addr show
ip route show
```

### Process Management

```bash
# Find process using port
lsof -i :5400
fuser 5400/tcp

# Kill process on port
fuser -k 5400/tcp
```

---

## Protocol-Specific Commands

### TEXT Protocol Testing

```bash
# Interactive session
nc localhost 5400

# Commands (type in nc session):
PING
SET key1 value1
GET key1
COUNT
KEYS
DEL key1
QUIT
```

### BINARY Protocol Testing

```bash
# Requires proper header construction
# Use Python or provided client instead
python src/apps/binary_proto_client.py
```

### UDP Sensor Testing

```bash
# Send malformed packet (for error testing)
echo "invalid" | nc -u localhost 5402

# Use provided client
python src/apps/udp_sensor_client.py --sensor-id 1 --temp 23.5 --location "Lab-A"
```

---

## Quick Debugging Sequence

```bash
# 1. Check containers running
docker ps

# 2. Check port listening
ss -tlnp | grep 5400

# 3. Test connectivity
nc -zv localhost 5400

# 4. Start capture
sudo tcpdump -i any port 5400 -w debug.pcap &

# 5. Run test
echo "PING" | nc localhost 5400

# 6. Stop capture
fg   # then Ctrl+C

# 7. Analyse
tcpdump -r debug.pcap -XX
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
