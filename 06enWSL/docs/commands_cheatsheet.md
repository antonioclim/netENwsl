# Week 6: Commands Cheatsheet

> NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

## Laboratory Management

### Starting the Environment

```powershell
# Start all services
python scripts/start_lab.py

# Start with SDN controller
python scripts/start_lab.py --controller

# Start with Portainer
python scripts/start_lab.py --portainer

# Check status
python scripts/start_lab.py --status
```

### Stopping and Cleanup

```powershell
# Graceful stop (preserves data)
python scripts/stop_lab.py

# Full cleanup (removes everything)
python scripts/cleanup.py --full

# Dry run (show what would be removed)
python scripts/cleanup.py --full --dry-run
```

### Running Demos

```powershell
# List available demos
python scripts/run_demo.py --list

# Run NAT demo
python scripts/run_demo.py --demo nat

# Run SDN demo
python scripts/run_demo.py --demo sdn
```

## Mininet Commands

### Basic Operations

```bash
# Start Mininet CLI
sudo mn

# Start with specific topology
sudo python3 src/exercises/ex_6_01_nat_topology.py --cli
sudo python3 src/exercises/ex_6_02_sdn_topology.py --cli

# Clean up Mininet
sudo mn -c
```

### Within Mininet CLI

```bash
# List nodes
nodes

# List network interfaces
net

# Test connectivity
pingall

# Run command on host
h1 ifconfig
h1 ping 10.0.6.12

# Open terminal on host
xterm h1

# Dump host information
dump
```

## NAT/iptables Commands

### Viewing NAT Configuration

```bash
# Show NAT rules
iptables -t nat -L -n -v

# Show conntrack table
conntrack -L
cat /proc/net/nf_conntrack

# Show IP forwarding status
sysctl net.ipv4.ip_forward
```

**Expected output for NAT rules:**
```
Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination
MASQUERADE  all  --  192.168.1.0/24      anywhere
```

### Configuring NAT

```bash
# Enable IP forwarding
sysctl -w net.ipv4.ip_forward=1

# Add MASQUERADE rule
iptables -t nat -A POSTROUTING -o eth1 -s 192.168.1.0/24 -j MASQUERADE

# Allow forwarding
iptables -A FORWARD -i eth0 -o eth1 -j ACCEPT
iptables -A FORWARD -i eth1 -o eth0 -m state --state ESTABLISHED,RELATED -j ACCEPT

# Flush NAT rules
iptables -t nat -F
```

## Open vSwitch Commands

### Basic Operations

```bash
# Show OVS configuration
ovs-vsctl show

# List bridges
ovs-vsctl list-br

# List ports on bridge
ovs-vsctl list-ports s1

# Delete bridge
ovs-vsctl del-br s1
```

### Flow Table Management (OpenFlow 1.3)

```bash
# Dump all flows
ovs-ofctl -O OpenFlow13 dump-flows s1

# Dump flows sorted by packets
ovs-ofctl -O OpenFlow13 dump-flows s1 --rsort=n_packets

# Add a flow rule
ovs-ofctl -O OpenFlow13 add-flow s1 "priority=100,icmp,nw_src=10.0.6.11,actions=drop"

# Delete specific flow
ovs-ofctl -O OpenFlow13 del-flows s1 "priority=100,icmp,nw_src=10.0.6.11"

# Delete all flows
ovs-ofctl -O OpenFlow13 del-flows s1

# Show switch description
ovs-ofctl -O OpenFlow13 dump-desc s1
```

**Expected output for dump-flows:**
```
cookie=0x0, duration=120.5s, table=0, n_packets=42, n_bytes=3528,
    priority=100,icmp,nw_src=10.0.6.11,nw_dst=10.0.6.12 actions=output:2
```

### Flow Rule Syntax

```bash
# Match fields
priority=N              # Rule priority (higher = checked first)
in_port=N               # Input port number
eth_type=0x0800         # IPv4
eth_type=0x0806         # ARP
ip_proto=1              # ICMP
ip_proto=6              # TCP
ip_proto=17             # UDP
nw_src=IP               # Source IP
nw_dst=IP               # Destination IP
tp_src=PORT             # Source port (TCP/UDP)
tp_dst=PORT             # Destination port (TCP/UDP)

# Actions
actions=output:N        # Output to port N
actions=drop            # Drop packet
actions=NORMAL          # Use normal L2 learning
actions=CONTROLLER      # Send to controller
actions=flood           # Flood to all ports
```

## Packet Capture

### tcpdump

```bash
# Capture ICMP traffic
tcpdump -i eth0 icmp

# Capture with detail
tcpdump -i eth0 -n -v icmp

# Save to file
tcpdump -i eth0 -w capture.pcap

# Filter by host
tcpdump -i eth0 host 10.0.6.11

# Filter by port
tcpdump -i eth0 port 9090
```

### tshark

```bash
# Capture and display
tshark -i eth0

# Filter by protocol
tshark -i eth0 -f "icmp"

# Display specific fields
tshark -i eth0 -T fields -e ip.src -e ip.dst

# Read pcap file
tshark -r capture.pcap

# OpenFlow traffic
tshark -i lo -f "port 6633"
```

## Docker Commands

### Container Management

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# Enter container shell
docker exec -it week6_lab bash

# View container logs
docker logs week6_lab

# Stop container
docker stop week6_lab

# Remove container
docker rm week6_lab
```

### Docker Compose

```bash
# Build images
docker compose build

# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f

# Execute command in service
docker compose exec week6-lab bash
```

## Network Diagnostics

### Connectivity Testing

```bash
# Basic ping
ping -c 3 10.0.6.12

# Ping with specific interface
ping -I eth0 10.0.6.12

# Traceroute
traceroute -n 10.0.6.12

# Check listening ports
ss -ltn

# Check network connections
ss -tn
```

### Interface Configuration

```bash
# Show all interfaces
ip addr show

# Show routing table
ip route show

# Add static route
ip route add 10.0.6.0/24 via 192.168.1.1

# Show ARP cache
ip neigh show
```

## Week 6 Applications

### TCP Echo

```bash
# Server
python3 src/apps/tcp_echo.py server --bind 0.0.0.0 --port 9090

# Client
python3 src/apps/tcp_echo.py client --dst 10.0.6.12 --port 9090 --message "Hello"
```

### UDP Echo

```bash
# Server
python3 src/apps/udp_echo.py server --bind 0.0.0.0 --port 9091

# Client
python3 src/apps/udp_echo.py client --dst 10.0.6.12 --port 9091 --message "Hello"
```

### NAT Observer

```bash
# Server (on public host)
python3 src/apps/nat_observer.py server --bind 203.0.113.2 --port 5000

# Client (from private host)
python3 src/apps/nat_observer.py client --host 203.0.113.2 --port 5000 --msg "Test"
```

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
