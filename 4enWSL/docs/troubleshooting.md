# Troubleshooting Guide

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by Revolvix

This guide addresses common issues encountered during Week 4 laboratory exercises and provides systematic resolution procedures.

---

## Diagnostic Approach

Before attempting specific fixes, gather diagnostic information:

```powershell
# Run environment verification
python setup/verify_environment.py

# Check Docker status
docker info
docker ps -a

# Check port availability
python -c "import socket; s=socket.socket(); s.settimeout(1); print('Open' if s.connect_ex(('localhost',5400))==0 else 'Closed'); s.close()"
```

---

## Docker Issues

### Docker Desktop Not Running

**Symptoms:**
- `Cannot connect to the Docker daemon`
- `docker: command not found` in WSL

**Diagnosis:**
```powershell
docker info
```

**Solution:**
1. Start Docker Desktop from Windows Start menu
2. Wait for the whale icon in system tray to stop animating
3. Verify with `docker info`

**If Docker Desktop won't start:**
```powershell
# Restart Docker service
net stop com.docker.service
net start com.docker.service
```

---

### WSL2 Integration Disabled

**Symptoms:**
- Docker commands fail in WSL terminal
- `The command 'docker' could not be found`

**Solution:**
1. Open Docker Desktop → Settings
2. Navigate to Resources → WSL Integration
3. Enable integration for your WSL distribution
4. Click "Apply & Restart"
5. Restart WSL: `wsl --shutdown` then open new terminal

---

### Container Fails to Start

**Symptoms:**
- `Container exited with code 1`
- `Cannot start service`

**Diagnosis:**
```bash
docker compose logs week4-lab
docker inspect week4-lab --format='{{.State.ExitCode}}'
```

**Common Causes and Fixes:**

**Port conflict:**
```bash
# Check what's using the port
netstat -ano | findstr :5400
lsof -i :5400

# Stop conflicting process or change port in docker-compose.yml
```

**Permission issues:**
```bash
# Reset volume permissions
docker compose down -v
docker compose up -d
```

**Corrupt image:**
```bash
docker compose build --no-cache
docker compose up -d
```

---

### Network Connectivity Between Containers

**Symptoms:**
- Containers can't communicate
- `Connection refused` between services

**Diagnosis:**
```bash
# Check network exists
docker network ls | grep week4

# Check containers are on same network
docker network inspect week4_network
```

**Solution:**
```bash
# Recreate network
docker compose down
docker network rm week4_network
docker compose up -d
```

---

### Volume Mount Failures

**Symptoms:**
- `Error response from daemon: invalid mount config`
- Files not visible in container

**WSL Path Issues:**
```bash
# Windows paths must be mounted via WSL
# Correct: /home/user/project
# Incorrect: C:\Users\user\project

# Check current directory
pwd

# Ensure running from WSL, not PowerShell
```

**Permission denied:**
```bash
# Make files readable
chmod -R 755 src/
chmod -R 755 docker/

# Check user mapping in docker-compose.yml
```

---

## Port Connectivity Issues

### Port Not Responding

**Symptoms:**
- `Connection refused` when connecting to localhost:5400
- Service appears running but unreachable

**Diagnosis:**
```bash
# Check service is listening inside container
docker exec week4-lab ss -tlnp

# Check port mapping
docker port week4-lab

# Test from inside container
docker exec week4-lab nc -zv localhost 5400
```

**Causes:**

**Service binding to 127.0.0.1 only:**
- Service must bind to 0.0.0.0 to be accessible from host
- Check server code: `bind(('0.0.0.0', 5400))`

**Windows Firewall blocking:**
```powershell
# Add firewall rule (run as Administrator)
New-NetFirewallRule -DisplayName "Week4 Lab" -Direction Inbound -LocalPort 5400-5402 -Protocol TCP -Action Allow
```

---

### Port Already in Use

**Symptoms:**
- `Bind: address already in use`
- `Port is already allocated`

**Solution:**
```bash
# Find process using port
# On Windows PowerShell:
netstat -ano | findstr :5400

# On WSL/Linux:
lsof -i :5400
fuser 5400/tcp

# Kill process
# Windows:
taskkill /PID <pid> /F

# Linux:
kill -9 <pid>
fuser -k 5400/tcp

# Or change port in docker-compose.yml
```

---

## Protocol Communication Issues

### TEXT Protocol Not Responding

**Symptoms:**
- Connection establishes but no response
- Timeout on commands

**Diagnosis:**
```bash
# Check server is running
docker exec week4-lab ps aux | grep text_proto

# Test with verbose netcat
nc -v localhost 5400

# Check server logs
docker compose logs week4-lab | grep -i text
```

**Common Causes:**

**Missing newline:**
```bash
# TEXT protocol requires newline after commands
echo -e "PING\n" | nc localhost 5400

# Or use -q flag
echo "PING" | nc -q 1 localhost 5400
```

**Wrong command syntax:**
```
# Correct
SET key1 value1

# Incorrect (extra spaces, wrong case)
set  key1  value1
```

---

### BINARY Protocol Errors

**Symptoms:**
- Server closes connection immediately
- Invalid response data

**Diagnosis:**
```bash
# Capture and examine traffic
tcpdump -i lo port 5401 -XX

# Use provided client for testing
python src/apps/binary_proto_client.py
```

**Common Causes:**

**Incorrect header format:**
```python
# Header must be exactly 14 bytes
# Magic: NP (2 bytes)
# Version: 1 byte
# Type: 1 byte
# Payload length: 4 bytes (big-endian)
# Sequence: 4 bytes (big-endian)
# CRC32: 4 bytes (big-endian)
```

**CRC mismatch:**
```python
import zlib

# CRC must be calculated over header (without CRC field) + payload
data = header_without_crc + payload
crc = zlib.crc32(data) & 0xFFFFFFFF
```

---

### UDP Sensor Protocol Issues

**Symptoms:**
- No response from server
- Malformed data received

**Diagnosis:**
```bash
# UDP is connectionless - no "connection refused"
# Use tcpdump to verify packets sent/received
tcpdump -i lo udp port 5402 -XX
```

**Common Causes:**

**Wrong datagram size:**
```python
# Datagram must be exactly 23 bytes
# Version: 1 byte
# Sensor ID: 4 bytes
# Temperature: 4 bytes (float, big-endian)
# Location: 10 bytes (fixed, padded)
# CRC32: 4 bytes (big-endian)
```

**Firewall blocking UDP:**
```powershell
# Add UDP rule
New-NetFirewallRule -DisplayName "Week4 UDP" -Direction Inbound -LocalPort 5402 -Protocol UDP -Action Allow
```

---

## Packet Capture Issues

### tcpdump Permission Denied

**Symptoms:**
- `Permission denied` when running tcpdump
- `You don't have permission to capture`

**Solution:**
```bash
# Run with sudo
sudo tcpdump -i eth0

# Or add capability to user
sudo setcap cap_net_raw,cap_net_admin+eip /usr/sbin/tcpdump
```

---

### No Traffic Captured

**Symptoms:**
- tcpdump runs but shows no packets
- Wireshark display empty

**Diagnosis:**
```bash
# List available interfaces
tcpdump -D
ip link show

# Try capturing on 'any' interface
sudo tcpdump -i any port 5400
```

**Causes:**

**Wrong interface:**
```bash
# Docker traffic typically on:
# - docker0 (bridge network)
# - br-xxxxx (custom networks)
# - lo (if using localhost)

# Find correct interface
docker network inspect week4_network | grep -i gateway
```

**Traffic on loopback:**
```bash
# localhost traffic uses loopback
sudo tcpdump -i lo port 5400
```

---

### Wireshark Can't See Docker Traffic

**Symptoms:**
- Wireshark on Windows can't capture container traffic
- Only sees host traffic

**Solution:**

**Option 1: Use Npcap loopback adapter**
1. Install Npcap with loopback adapter option
2. In Wireshark, select "Adapter for loopback traffic capture"

**Option 2: Capture inside container**
```bash
# Run tcpdump in container
docker exec week4-lab tcpdump -i eth0 -w /tmp/capture.pcap

# Copy file out
docker cp week4-lab:/tmp/capture.pcap ./pcap/

# Open in Wireshark
```

**Option 3: Use tshark in WSL**
```bash
# Install tshark
sudo apt install tshark

# Capture
sudo tshark -i docker0 -w capture.pcap
```

---

## Python Issues

### Module Not Found

**Symptoms:**
- `ModuleNotFoundError: No module named 'xxx'`

**Solution:**
```bash
# Install missing module
pip install <module_name> --break-system-packages

# Or use requirements.txt
pip install -r setup/requirements.txt --break-system-packages
```

---

### Socket Connection Refused

**Symptoms:**
- `ConnectionRefusedError: [Errno 111] Connection refused`

**Diagnosis:**
```python
import socket

# Check if port is open
def check_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

print(check_port('localhost', 5400))
```

**Common Causes:**
1. Server not running
2. Server bound to different address (127.0.0.1 vs 0.0.0.0)
3. Firewall blocking connection
4. Wrong port number

---

### struct.error: unpack requires a buffer

**Symptoms:**
- `struct.error: unpack requires a buffer of N bytes`
- Incomplete data received

**Solution:**
```python
# Ensure you receive exact number of bytes needed
def recv_exact(sock, n):
    """Receive exactly n bytes from socket."""
    data = b''
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Connection closed")
        data += chunk
    return data

# Use instead of sock.recv(n)
header = recv_exact(sock, 14)
```

---

## WSL-Specific Issues

### Time Synchronisation

**Symptoms:**
- WSL clock differs from Windows
- File timestamps incorrect
- TLS certificate errors

**Solution:**
```bash
# Sync WSL clock
sudo hwclock -s

# Or restart WSL
wsl --shutdown
# Then reopen terminal
```

---

### File Permission Issues

**Symptoms:**
- `Permission denied` on scripts
- Can't execute Python files

**Solution:**
```bash
# Make scripts executable
chmod +x scripts/*.py
chmod +x setup/*.py

# Fix line endings (CRLF to LF)
sed -i 's/\r$//' scripts/*.py
```

---

### Slow File Access

**Symptoms:**
- Operations on Windows filesystem from WSL very slow
- `/mnt/c/` paths slow

**Solution:**
- Work in native WSL filesystem (`/home/user/`)
- Copy project to WSL filesystem:
```bash
cp -r /mnt/c/Users/user/WEEK4_WSLkit ~/
cd ~/WEEK4_WSLkit
```

---

## Quick Fixes Summary

| Issue | Quick Fix |
|-------|-----------|
| Docker not starting | Restart Docker Desktop |
| Port in use | `fuser -k 5400/tcp` |
| Container won't start | `docker compose down -v && docker compose up -d` |
| No network | `docker network rm week4_network && docker compose up -d` |
| Permission denied | `chmod +x script.py` |
| Module not found | `pip install module --break-system-packages` |
| Clock sync | `sudo hwclock -s` |
| WSL slow | Work in `/home/user/` not `/mnt/c/` |

---

## Getting Help

If issues persist:

1. Run diagnostic script:
   ```bash
   python setup/verify_environment.py > diagnostic.txt
   docker compose logs > docker-logs.txt
   ```

2. Check Docker events:
   ```bash
   docker events --since 10m
   ```

3. Review Portainer logs at https://localhost:9443

4. Consult course materials or laboratory assistant

---

*NETWORKING class - ASE, Informatics | by Revolvix*
