# Commands Cheatsheet: Week 7

> NETWORKING class - ASE, Informatics | by Revolvix

## tcpdump

### Basic Capture

```bash
# Capture all traffic on interface eth0
sudo tcpdump -i eth0

# Capture and save to file
sudo tcpdump -i eth0 -w capture.pcap

# Capture with verbose output
sudo tcpdump -i eth0 -v

# Capture with packet contents (hex + ASCII)
sudo tcpdump -i eth0 -X

# Capture first 100 packets only
sudo tcpdump -i eth0 -c 100
```

### Protocol Filters

```bash
# TCP only
sudo tcpdump -i eth0 tcp

# UDP only
sudo tcpdump -i eth0 udp

# ICMP only
sudo tcpdump -i eth0 icmp
```

### Port Filters

```bash
# Specific port
sudo tcpdump -i eth0 port 9090

# Source port
sudo tcpdump -i eth0 src port 9090

# Destination port
sudo tcpdump -i eth0 dst port 9090

# Port range
sudo tcpdump -i eth0 portrange 9000-9100
```

### Host Filters

```bash
# Traffic to/from host
sudo tcpdump -i eth0 host 10.0.7.100

# Source host
sudo tcpdump -i eth0 src host 10.0.7.100

# Destination host
sudo tcpdump -i eth0 dst host 10.0.7.100

# Subnet
sudo tcpdump -i eth0 net 10.0.7.0/24
```

### Compound Filters

```bash
# TCP port 9090 from specific host
sudo tcpdump -i eth0 'tcp port 9090 and host 10.0.7.100'

# TCP SYN packets only
sudo tcpdump -i eth0 'tcp[tcpflags] & tcp-syn != 0'

# TCP RST packets only
sudo tcpdump -i eth0 'tcp[tcpflags] & tcp-rst != 0'

# ICMP port unreachable
sudo tcpdump -i eth0 'icmp[icmptype] == 3 and icmp[icmpcode] == 3'
```

## tshark

### Basic Usage

```bash
# Live capture
tshark -i eth0

# Read pcap file
tshark -r capture.pcap

# Summary statistics
tshark -r capture.pcap -q -z io,stat,1
```

### Display Filters

```bash
# TCP traffic
tshark -r capture.pcap -Y "tcp"

# Specific port
tshark -r capture.pcap -Y "tcp.port == 9090"

# TCP flags
tshark -r capture.pcap -Y "tcp.flags.syn == 1"
tshark -r capture.pcap -Y "tcp.flags.reset == 1"

# ICMP unreachable
tshark -r capture.pcap -Y "icmp.type == 3"
```

### Field Extraction

```bash
# Extract specific fields
tshark -r capture.pcap -T fields -e ip.src -e ip.dst -e tcp.port

# Export to CSV
tshark -r capture.pcap -T fields -e frame.time -e ip.src -e tcp.srcport -E header=y -E separator=,
```

## iptables

### Viewing Rules

```bash
# List all rules (numbered)
sudo iptables -L -n --line-numbers

# List INPUT chain
sudo iptables -L INPUT -n -v

# List with packet counters
sudo iptables -L -n -v
```

### Adding Rules

```bash
# Block TCP port 9090 (DROP)
sudo iptables -A INPUT -p tcp --dport 9090 -j DROP

# Block TCP port 9090 (REJECT with RST)
sudo iptables -A INPUT -p tcp --dport 9090 -j REJECT --reject-with tcp-reset

# Block UDP port 9091 (DROP)
sudo iptables -A INPUT -p udp --dport 9091 -j DROP

# Block UDP port 9091 (REJECT with ICMP)
sudo iptables -A INPUT -p udp --dport 9091 -j REJECT

# Block from specific source
sudo iptables -A INPUT -s 10.0.7.10 -p tcp --dport 9090 -j DROP
```

### Removing Rules

```bash
# Delete by line number
sudo iptables -D INPUT 3

# Delete by specification
sudo iptables -D INPUT -p tcp --dport 9090 -j DROP

# Flush all rules
sudo iptables -F
```

### Saving and Restoring

```bash
# Save current rules
sudo iptables-save > rules.v4

# Restore rules
sudo iptables-restore < rules.v4
```

## netcat (nc)

### TCP Server/Client

```bash
# Start TCP listener
nc -l -p 9090

# Connect to TCP server
nc localhost 9090

# Send data and close
echo "test" | nc localhost 9090
```

### UDP Server/Client

```bash
# Start UDP listener
nc -u -l -p 9091

# Send UDP datagram
echo "test" | nc -u localhost 9091
```

### Port Scanning

```bash
# Scan single port
nc -zv localhost 9090

# Scan port range
nc -zv localhost 9000-9100

# UDP scan
nc -zuv localhost 9091
```

## Docker Commands

### Container Management

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f

# Execute command in container
docker exec -it week7_tcp_server bash
```

### Network Inspection

```bash
# List networks
docker network ls

# Inspect network
docker network inspect week7net

# View container IPs
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name
```

## Socket Testing (Python one-liners)

```bash
# Test TCP port
python3 -c "import socket; s=socket.socket(); s.settimeout(3); print('open' if s.connect_ex(('localhost',9090))==0 else 'closed'); s.close()"

# Send UDP datagram
python3 -c "import socket; s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.sendto(b'test',('localhost',9091))"
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
