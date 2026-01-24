# Commands Cheatsheet

> NETWORKING class - ASE, Informatics | by Revolvix

Quick reference for essential networking commands used in Week 1.

> 📖 **See also:** [Glossary](glossary.md) for definitions of technical terms used in these commands.

---

## Interface and Address Management

### Display Interfaces

```bash
# Brief format (recommended)
ip -br addr show
ip -br a

# Detailed format
ip addr show
ip a

# Specific interface
ip addr show eth0
```

### Display Routes

```bash
# Show routing table
ip route show
ip r

# Show default gateway only
ip route | grep default

# Show route to specific destination
ip route get 8.8.8.8
```

### Neighbour Cache (ARP)

```bash
# Show ARP cache
ip neigh show
ip n
```

---

## Connectivity Testing

### Ping (ICMP)

```bash
# Basic ping
ping 8.8.8.8

# Limited count
ping -c 4 8.8.8.8

# Set timeout per packet
ping -W 2 8.8.8.8

# Numeric output (no DNS)
ping -n 8.8.8.8

# Combined
ping -n -c 4 -W 2 192.168.1.1
```

### DNS Resolution

```bash
# Resolve hostname
getent hosts google.com

# Using nslookup
nslookup google.com

# Using dig (more detailed)
dig google.com
dig +short google.com
```

---

## Socket Inspection

### ss Command (Recommended)

```bash
# TCP listening sockets
ss -tlnp

# UDP listening sockets
ss -ulnp

# All sockets (TCP + UDP)
ss -tunap

# Filter by port
ss -tnp | grep 9090

# Filter by state
ss -t state established
```

**ss Flags:**
| Flag | Meaning |
|------|---------|
| `-t` | TCP sockets |
| `-u` | UDP sockets |
| `-l` | Listening only |
| `-n` | Numeric (no DNS) |
| `-p` | Show process |
| `-a` | All sockets |

### netstat (Legacy)

```bash
# Equivalent to ss -tunap
netstat -tunap

# Listening sockets
netstat -tlnp
```

---

## Netcat (nc)

### TCP Server

```bash
# Start TCP server
nc -l -p 9090

# Persistent server (loop)
while true; do nc -l -p 9090; done

# With verbose output
nc -v -l -p 9090
```

### TCP Client

```bash
# Connect to server
nc localhost 9090

# Send single message
echo "hello" | nc localhost 9090

# Send file
nc localhost 9090 < file.txt

# With timeout
nc -w 5 localhost 9090
```

### UDP Communication

```bash
# UDP server
nc -u -l -p 9091

# UDP client
nc -u localhost 9091

# Send UDP message
echo "ping" | nc -u -w 1 localhost 9091
```

### File Transfer

```bash
# Receiver
nc -l -p 9090 > received_file.txt

# Sender
nc localhost 9090 < file_to_send.txt
```

---

## Packet Capture

### tcpdump

```bash
# Capture on interface
sudo tcpdump -i eth0

# Capture on all interfaces
sudo tcpdump -i any

# Filter by port
sudo tcpdump -i any port 9090

# Filter by host
sudo tcpdump -i any host 192.168.1.1

# Save to file
sudo tcpdump -i any -w capture.pcap

# Read from file
sudo tcpdump -r capture.pcap

# Limit packet count
sudo tcpdump -i any -c 100

# No DNS resolution
sudo tcpdump -nn -i any
```

### tshark (CLI Wireshark)

```bash
# Live capture
tshark -i eth0

# Capture with filter
tshark -i lo -f "port 9090"

# Save to file
tshark -i lo -w output.pcap

# Read file
tshark -r capture.pcap

# Display filter
tshark -r capture.pcap -Y "tcp.flags.syn==1"

# Extract fields
tshark -r capture.pcap -T fields \
    -e frame.number \
    -e ip.src \
    -e ip.dst \
    -e tcp.srcport \
    -e tcp.dstport

# Export to CSV
tshark -r capture.pcap -T fields \
    -e frame.number \
    -e frame.time_relative \
    -E header=y \
    -E separator=, > output.csv

# Statistics
tshark -r capture.pcap -q -z conv,tcp
tshark -r capture.pcap -q -z io,stat,1
```

---

## Docker Commands

### Container Management

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# Start container
docker start container_name

# Stop container
docker stop container_name

# Remove container
docker rm container_name

# Execute command in container
docker exec -it container_name bash

# View logs
docker logs container_name
docker logs -f container_name  # follow
```

### Docker Compose

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v

# Rebuild images
docker compose build --no-cache

# View logs
docker compose logs
docker compose logs -f service_name

# Service status
docker compose ps
```

### Network Management

```bash
# List networks
docker network ls

# Inspect network
docker network inspect network_name

# Create network
docker network create --driver bridge my_network
```

---

## Python One-Liners

### Simple TCP Server

```bash
python -c "
import socket
s = socket.socket()
s.bind(('', 9090))
s.listen(1)
print('Listening on :9090')
conn, addr = s.accept()
print(f'Connected: {addr}')
print(conn.recv(1024))
conn.close()
"
```

### Simple TCP Client

```bash
python -c "
import socket
s = socket.socket()
s.connect(('localhost', 9090))
s.send(b'Hello from Python!')
s.close()
"
```

### HTTP Server

```bash
# Python 3 built-in HTTP server
python -m http.server 8080

# Serve specific directory
python -m http.server 8080 --directory /path/to/dir
```

---

## Filter Expressions

### tcpdump/tshark Capture Filters (BPF)

```
port 80                  # HTTP traffic
port 443                 # HTTPS traffic
tcp port 9090           # TCP on specific port
udp port 53             # DNS traffic
host 192.168.1.1        # Specific host
src host 192.168.1.1    # Source IP
dst host 192.168.1.1    # Destination IP
net 192.168.1.0/24      # Network range
tcp                     # TCP only
udp                     # UDP only
icmp                    # ICMP only
not port 22             # Exclude SSH
port 80 or port 443     # Multiple ports
```

### Wireshark Display Filters

```
tcp                     # TCP protocol
udp                     # UDP protocol
ip.addr == 192.168.1.1  # IP address
tcp.port == 80          # TCP port
tcp.flags.syn == 1      # SYN packets
tcp.flags.ack == 1      # ACK packets
http                    # HTTP traffic
dns                     # DNS traffic
frame.len > 1000        # Large packets
tcp.analysis.retransmission  # Retransmissions
```

---

## Quick Reference Table

| Task | Command |
|------|---------|
| Show IP | `ip -br a` |
| Show routes | `ip r` |
| Test connectivity | `ping -c 4 HOST` |
| TCP server | `nc -l -p PORT` |
| TCP client | `nc HOST PORT` |
| UDP server | `nc -u -l -p PORT` |
| Show sockets | `ss -tunap` |
| Capture traffic | `tcpdump -i any port PORT` |
| Analyse PCAP | `tshark -r file.pcap` |
| Container shell | `docker exec -it NAME bash` |

---

*NETWORKING class - ASE, Informatics | by Revolvix*
