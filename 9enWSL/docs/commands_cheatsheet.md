# Commands Cheatsheet: Week 9

> Quick reference for Session Layer (L5) and Presentation Layer (L6)
> NETWORKING class - ASE, Informatics | by Revolvix

---

## Laboratory Management

### Starting and Stopping

```powershell
# Start laboratory environment
python scripts/start_lab.py

# Check service status
python scripts/start_lab.py --status

# Stop all containers (preserves data)
python scripts/stop_lab.py

# Full cleanup (before next week)
python scripts/cleanup.py --full

# Preview cleanup actions
python scripts/cleanup.py --dry-run
```

### Running Demonstrations

```powershell
# List available demos
python scripts/run_demo.py --list

# Run specific demo
python scripts/run_demo.py --demo endianness
python scripts/run_demo.py --demo ftp_session
python scripts/run_demo.py --demo multi_client
python scripts/run_demo.py --demo binary_protocol

# Run all demos
python scripts/run_demo.py --all
```

---

## Docker Commands

### Container Management

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# View container logs
docker logs s9_ftp-server
docker logs -f s9_ftp-server    # Follow logs

# Execute command in container
docker exec -it s9_ftp-server /bin/bash

# Inspect container
docker inspect s9_ftp-server
```

### Compose Operations

```bash
# Navigate to docker directory
cd docker/

# Start services
docker compose up -d

# Stop services
docker compose down

# Rebuild and start
docker compose up -d --build

# View service logs
docker compose logs

# Scale a service
docker compose up -d --scale client=3
```

### Network Inspection

```bash
# List networks
docker network ls

# Inspect week9 network
docker network inspect week9_ftp_network

# List containers on network
docker network inspect week9_ftp_network --format '{{range .Containers}}{{.Name}} {{end}}'
```

---

## FTP Commands

### Using the Built-in Demo Client

```python
# Connect to FTP server
python src/exercises/ftp_demo_client.py

# Interactive commands within client:
# USER test
# PASS 12345
# PWD
# LIST
# PASV
# RETR filename.txt
# QUIT
```

### Using Standard FTP Client

```bash
# Connect via ftp command
ftp localhost 2121

# Common FTP commands:
# user test            - Login as user
# pass 12345           - Enter password
# pwd                  - Print working directory
# ls                   - List files
# cd dirname           - Change directory
# get filename         - Download file
# put filename         - Upload file
# binary               - Set binary mode
# ascii                - Set ASCII mode
# passive              - Toggle passive mode
# quit                 - Disconnect
```

### Using Python ftplib

```python
from ftplib import FTP

ftp = FTP()
ftp.connect('localhost', 2121)
ftp.login('test', '12345')

# List directory
ftp.retrlines('LIST')

# Download file
with open('local.txt', 'wb') as f:
    ftp.retrbinary('RETR remote.txt', f.write)

# Upload file
with open('local.txt', 'rb') as f:
    ftp.storbinary('STOR remote.txt', f)

ftp.quit()
```

---

## Python struct Module

### Format Characters

```python
import struct

# Byte order specifiers
# >  Big-endian (network byte order)
# <  Little-endian
# !  Network (= big-endian)
# =  Native

# Type specifiers
# B  unsigned char      (1 byte)
# H  unsigned short     (2 bytes)
# I  unsigned int       (4 bytes)
# Q  unsigned long long (8 bytes)
# s  char[] (bytes)     (n bytes)
# f  float              (4 bytes)
# d  double             (8 bytes)
```

### Packing Examples

```python
import struct

# Pack single integer as big-endian
data = struct.pack(">I", 0x12345678)
# Result: b'\x12\x34\x56\x78'

# Pack multiple values
header = struct.pack(">4sIIB", b"FTPC", 1024, 0xDEADBEEF, 1)

# Unpack data
magic, length, checksum, flags = struct.unpack(">4sIIB", header)

# Calculate packed size
size = struct.calcsize(">4sIIB")  # Returns 13
```

---

## CRC-32 Checksum

```python
import zlib

# Calculate CRC-32
data = b"Hello, World!"
checksum = zlib.crc32(data) & 0xFFFFFFFF
print(f"CRC-32: 0x{checksum:08X}")

# Verify checksum
received_crc = 0xEC4AC3D0
calculated_crc = zlib.crc32(data) & 0xFFFFFFFF
is_valid = received_crc == calculated_crc
```

---

## Network Utilities

### Port Checking

```python
import socket

def check_port(host, port, timeout=2):
    """Check if a port is open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            return True
    except:
        return False

# Usage
if check_port('localhost', 2121):
    print("FTP server is running")
```

### DNS Lookup

```python
import socket

# Get IP from hostname
ip = socket.gethostbyname('localhost')

# Get hostname from IP
hostname = socket.gethostbyaddr('127.0.0.1')[0]

# Get all addresses for hostname
addrs = socket.getaddrinfo('localhost', 2121)
```

---

## Packet Capture

### Using tcpdump (in container)

```bash
# Capture FTP control traffic
docker exec s9_ftp-server tcpdump -i eth0 port 2121 -w /tmp/capture.pcap

# Capture all traffic on network
docker exec s9_ftp-server tcpdump -i eth0 -w /tmp/all_traffic.pcap

# Display traffic in real-time
docker exec s9_ftp-server tcpdump -i eth0 port 2121 -A
```

### Using Wireshark

```
# Useful display filters for FTP:
ftp                           # All FTP control traffic
ftp-data                      # All FTP data traffic
ftp.request.command           # FTP commands only
ftp.response.code             # FTP responses only
tcp.port == 2121              # Traffic on control port
tcp.port >= 60000             # Passive data connections
```

### Saving Captures

```powershell
# Using the capture helper script
python scripts/capture_traffic.py --interface eth0 --output pcap/week9_capture.pcap

# Copy capture from container
docker cp s9_ftp-server:/tmp/capture.pcap ./pcap/
```

---

## Testing Commands

### Running Tests

```powershell
# Quick smoke test
python tests/smoke_test.py

# Environment validation
python tests/test_environment.py

# Exercise verification
python tests/test_exercises.py

# Specific test
python -m pytest tests/test_exercises.py::test_endianness_conversion -v
```

### Verification Helpers

```powershell
# Verify environment
python setup/verify_environment.py

# Check Docker configuration
python setup/configure_docker.py --check
```

---

## Troubleshooting Commands

### Docker Issues

```bash
# Restart Docker Desktop (PowerShell)
Restart-Service docker

# Clean up Docker resources
docker system prune -a

# Check Docker logs
docker logs s9_ftp-server 2>&1 | tail -50

# Reset Docker network
docker network rm week9_ftp_network
```

### Network Issues

```bash
# Check listening ports
netstat -an | findstr 2121

# Test connectivity
curl -v ftp://localhost:2121/

# Check firewall (PowerShell Admin)
Get-NetFirewallRule | Where-Object {$_.LocalPort -eq 2121}
```

---

## Quick Reference: FTP Response Codes

| Code | Meaning                      |
|------|------------------------------|
| 125  | Data connection open         |
| 150  | Opening data connection      |
| 200  | Command OK                   |
| 220  | Service ready                |
| 221  | Closing connection           |
| 226  | Transfer complete            |
| 227  | Entering passive mode        |
| 230  | User logged in               |
| 331  | Username OK, need password   |
| 425  | Can't open data connection   |
| 426  | Connection closed            |
| 450  | File unavailable             |
| 500  | Syntax error                 |
| 530  | Not logged in                |

---

*NETWORKING class - ASE, Informatics | by Revolvix*
