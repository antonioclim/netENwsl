# Troubleshooting Guide - Week 3

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

## Table of Contents

1. [Socket and Broadcast Issues](#socket-and-broadcast-issues)
2. [Multicast Problems](#multicast-problems)
3. [TCP Tunnel Errors](#tcp-tunnel-errors)
4. [Docker and Container Issues](#docker-and-container-issues)
5. [Wireshark Capture Problems](#wireshark-capture-problems)
6. [Network Connectivity](#network-connectivity)

---

## Socket and Broadcast Issues

### Issue: `OSError: [Errno 10013] Permission denied` on Windows

**Symptoms:** Cannot bind to broadcast address or low ports.

**Cause:** Windows requires elevated privileges for certain socket operations.

**Solution:**
```powershell
# Run PowerShell as Administrator
# Or use ports above 1024
```

### Issue: `OSError: [Errno 10048] Address already in use`

**Symptoms:** Cannot start server, port is occupied.

**Cause:** Previous instance still running or another application using the port.

**Solution:**
```bash
# Inside container, find process using port
ss -tlnp | grep :5007

# Kill the process
kill -9 <PID>

# Or restart the container
docker restart week3_receiver
```

### Issue: `socket.error: [Errno 101] Network is unreachable` for broadcast

**Symptoms:** Broadcast packets not being sent.

**Cause:** SO_BROADCAST socket option not set, or network interface misconfigured.

**Solution:**
```python
# Ensure SO_BROADCAST is enabled BEFORE sending
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Verify with
print(sock.getsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST))  # Should print 1
```

### Issue: Broadcast messages not received by other containers

**Symptoms:** Sender reports success, but receivers show nothing.

**Cause:** Docker networks may filter broadcast by default, or receiver not bound correctly.

**Solution:**
```bash
# Verify receiver is listening
docker exec week3_receiver ss -ulnp | grep 5007

# Check network configuration
docker network inspect week3_network

# Ensure receiver binds to 0.0.0.0, not a specific IP
# In Python: sock.bind(('0.0.0.0', 5007))  # Correct
#            sock.bind(('172.20.0.101', 5007))  # May miss broadcasts
```

---

## Multicast Problems

### Issue: Multicast messages not received

**Symptoms:** Sender transmits but receivers see nothing.

**Cause:** IGMP group join failed, or multicast routing not enabled.

**Solution:**
```python
# Verify group membership is properly configured
import struct

# Join multicast group correctly
mreq = struct.pack('4s4s', 
                   socket.inet_aton('239.0.0.1'),  # Multicast group
                   socket.inet_aton('0.0.0.0'))    # Interface (all)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
```

```bash
# Inside container, check multicast group membership
cat /proc/net/igmp
# or
ip maddr show
```

### Issue: `OSError: [Errno 19] No such device` for multicast

**Symptoms:** Cannot join multicast group.

**Cause:** Network interface not supporting multicast or wrong interface specified.

**Solution:**
```bash
# Verify multicast is enabled on interface
ip link show eth0 | grep MULTICAST

# If not shown, enable it (requires privileges)
ip link set eth0 multicast on
```

### Issue: Multicast TTL too low

**Symptoms:** Multicast works locally but not across network segments.

**Cause:** Default TTL of 1 limits multicast to local subnet.

**Solution:**
```python
# Set multicast TTL (Time To Live)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
```

### Issue: Receiving own multicast messages

**Symptoms:** Sender receives its own transmitted messages.

**Cause:** Multicast loopback is enabled by default.

**Solution:**
```python
# Disable multicast loopback if not desired
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)
```

---

## TCP Tunnel Errors

### Issue: `ConnectionRefusedError: [Errno 111] Connection refused`

**Symptoms:** Tunnel cannot connect to target server.

**Cause:** Target server not running, wrong port, or firewall blocking.

**Solution:**
```bash
# Verify server is running
docker exec week3_server ss -tlnp | grep 8080

# Test connectivity from tunnel container
docker exec week3_router nc -zv 172.20.0.10 8080

# Check server logs
docker logs week3_server
```

### Issue: Tunnel data corruption or incomplete transfer

**Symptoms:** Data received differs from data sent.

**Cause:** Buffer handling issues or connection closed prematurely.

**Solution:**
```python
# Use proper buffer handling
def relay_data(source, destination):
    """Relay data between sockets with proper buffer handling."""
    while True:
        try:
            data = source.recv(4096)
            if not data:
                break  # Connection closed gracefully
            destination.sendall(data)  # sendall ensures complete transmission
        except socket.error as e:
            break
```

### Issue: Tunnel hangs with bidirectional traffic

**Symptoms:** Data flows one direction but blocks when both sides send.

**Cause:** Single-threaded relay blocking on recv().

**Solution:**
```python
# Use threading for bidirectional relay
import threading

def create_tunnel(client_sock, server_sock):
    # Thread 1: client -> server
    t1 = threading.Thread(target=relay_data, args=(client_sock, server_sock))
    # Thread 2: server -> client  
    t2 = threading.Thread(target=relay_data, args=(server_sock, client_sock))
    
    t1.start()
    t2.start()
    t1.join()
    t2.join()
```

### Issue: `BrokenPipeError` during tunnel operation

**Symptoms:** Tunnel crashes when one side disconnects.

**Cause:** Attempting to write to closed socket.

**Solution:**
```python
import signal
signal.signal(signal.SIGPIPE, signal.SIG_IGN)  # Ignore SIGPIPE

# And handle exception
try:
    destination.sendall(data)
except BrokenPipeError:
    logger.info("Remote end closed connection")
    break
```

---

## Docker and Container Issues

### Issue: Containers fail to start with network errors

**Symptoms:** `docker compose up` fails with network creation errors.

**Cause:** Conflicting network from previous session or Docker network exhaustion.

**Solution:**
```bash
# Remove existing week3 network
docker network rm week3_network

# Prune unused networks
docker network prune -f

# Restart Docker Desktop if issues persist
```

### Issue: Container cannot resolve hostnames

**Symptoms:** `ping server` fails with "Name or service not known".

**Cause:** Docker DNS not configured or container not on same network.

**Solution:**
```bash
# Verify containers on same network
docker network inspect week3_network | grep -A5 "Containers"

# Use explicit IP addresses as fallback
ping 172.20.0.10  # Instead of 'server'
```

### Issue: `exec format error` when running Python scripts

**Symptoms:** Container starts but scripts fail immediately.

**Cause:** Wrong shebang or DOS line endings in scripts.

**Solution:**
```bash
# Convert line endings inside container
apt-get install dos2unix
dos2unix /app/*.py

# Or fix shebang
head -1 script.py  # Should show: #!/usr/bin/env python3
```

### Issue: Changes to source code not reflected in container

**Symptoms:** Modified Python files show old behaviour.

**Cause:** Volume mounts not configured, or Docker caching old image.

**Solution:**
```bash
# Rebuild without cache
docker compose build --no-cache

# Or for development, use volume mounts in docker-compose.yml:
# volumes:
#   - ./src:/app/src:ro
```

---

## Wireshark Capture Problems

### Issue: Cannot see Docker container traffic in Wireshark

**Symptoms:** Wireshark shows no packets from containers.

**Cause:** Capturing on wrong interface.

**Solution:**
```powershell
# On Windows, capture on WSL interface:
# 1. Open Wireshark as Administrator
# 2. Select interface named similar to:
#    - "Ethernet (WSL)"  
#    - "vEthernet (WSL)"
#    - Interface with 172.x.x.x range

# Or use tcpdump inside container and export pcap:
python scripts/capture_traffic.py --container server --duration 30
```

### Issue: Wireshark filter shows no results

**Symptoms:** Applied filter returns empty results despite traffic.

**Cause:** Incorrect filter syntax or filtering wrong field.

**Solution:**
```
# Common filter corrections:

# WRONG: port 5007
# RIGHT: udp.port == 5007

# WRONG: ip.addr = 172.20.0.10
# RIGHT: ip.addr == 172.20.0.10

# For broadcast:
eth.dst == ff:ff:ff:ff:ff:ff

# For multicast (239.x.x.x range):
ip.dst >= 239.0.0.0 and ip.dst <= 239.255.255.255
```

### Issue: Capture file too large or missing packets

**Symptoms:** pcap file grows very large or misses expected packets.

**Cause:** Capturing all traffic or buffer overflow.

**Solution:**
```bash
# Use capture filter (at capture time, not display filter)
tcpdump -i eth0 -w capture.pcap 'udp port 5007 or tcp port 8080'

# Limit capture size
tcpdump -i eth0 -w capture.pcap -c 1000  # Stop after 1000 packets
```

---

## Network Connectivity

### Issue: Cannot reach containers from Windows host

**Symptoms:** `curl localhost:8080` times out.

**Cause:** Port not published or Docker Desktop network mode issue.

**Solution:**
```yaml
# Verify port mapping in docker-compose.yml:
ports:
  - "8080:8080"  # hostPort:containerPort

# Check if port is listening
netstat -an | findstr :8080
```

### Issue: Containers cannot reach external internet

**Symptoms:** `apt-get update` fails inside container.

**Cause:** Docker DNS issues or corporate proxy not configured.

**Solution:**
```bash
# Test DNS resolution
docker exec week3_client nslookup google.com

# If DNS fails, add to docker-compose.yml:
dns:
  - 8.8.8.8
  - 8.8.4.4
```

### Issue: Intermittent packet loss between containers

**Symptoms:** Some messages lost randomly.

**Cause:** UDP has no guaranteed delivery; buffer overflow under load.

**Solution:**
```python
# Increase socket receive buffer
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)

# For testing, add sequence numbers to detect loss
message = f"{sequence_number}:{payload}"
```

---

## Quick Diagnostic Commands

```bash
# Container status
docker ps -a --filter "name=week3"

# Container logs
docker logs --tail 50 week3_server

# Network inspection
docker network inspect week3_network

# Port bindings
docker port week3_server

# Execute command in container
docker exec -it week3_client bash

# Check listening ports in container
docker exec week3_server ss -tulnp

# Test connectivity
docker exec week3_client ping -c 3 172.20.0.10

# Packet capture in container
docker exec week3_server tcpdump -i eth0 -c 10
```

---

## Getting Further Help

If issues persist after trying these solutions:

1. Collect diagnostic information:
   ```bash
   docker version > diagnostics.txt
   docker compose version >> diagnostics.txt
   docker ps -a >> diagnostics.txt
   docker logs week3_server >> diagnostics.txt 2>&1
   ```

2. Review the exercise source code for correct implementation patterns

3. Compare your output with expected results in `tests/expected_outputs.md`

4. Consult the course instructor during laboratory hours

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
