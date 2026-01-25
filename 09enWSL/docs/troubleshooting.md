# 🔧 Troubleshooting Guide — Week 9

> Session Layer (L5) and Presentation Layer (L6)
> NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

This guide addresses common issues encountered during the Week 9 laboratory
exercises. Issues are organised by category for quick reference.

---

## Table of Contents

1. [Docker Issues](#docker-issues)
2. [WSL2 Issues](#wsl2-issues)
3. [FTP Server Issues](#ftp-server-issues)
4. [Wireshark Issues](#wireshark-issues)
5. [Python/Code Issues](#pythoncode-issues)
6. [Network Issues](#network-issues)
7. [ASE Laboratory Specific Issues](#ase-laboratory-specific-issues)
8. [Complete Reset Procedure](#complete-reset-procedure)

---

## Docker Issues

### Docker Desktop Not Running

**Symptoms:**
- "Cannot connect to the Docker daemon"
- `docker ps` returns connection error

**Solutions:**

```bash
# In WSL Ubuntu terminal
sudo service docker start
# Password: stud

# Verify Docker is running
docker ps
```

If Docker service fails to start:
```bash
# Check status
sudo service docker status

# View logs
sudo journalctl -u docker.service

# Manual start (for debugging)
sudo dockerd
```

### Port Already in Use

**Symptoms:**
- "Bind for 0.0.0.0:2121 failed: port is already allocated"
- Container fails to start

**Solutions:**

```bash
# Find what's using the port
sudo netstat -tlnp | grep 2121
# Or
sudo ss -tlnp | grep 2121

# Kill the process (replace PID)
sudo kill -9 <PID>

# Or change port in docker-compose.yml
# Change "2121:2121" to "2122:2121"
```

### Containers Exit Immediately

**Symptoms:**
- Containers show "Exited" status
- No logs visible

**Solutions:**

```bash
# View container logs
docker logs s9_ftp_server

# Check exit code
docker ps -a --filter name=s9_ftp

# Rebuild containers
docker compose -f docker/docker-compose.yml down
docker compose -f docker/docker-compose.yml build --no-cache
docker compose -f docker/docker-compose.yml up -d
```

### Volume Permission Issues

**Symptoms:**
- "Permission denied" when accessing mounted files
- Files created in container are not accessible

**Solutions:**

```bash
# Fix ownership (in WSL)
sudo chown -R $USER:$USER docker/volumes/

# Or use Docker with correct user
# Add to docker-compose.yml:
#   user: "1000:1000"
```

---

## WSL2 Issues

### WSL2 Not Available

**Symptoms:**
- "WSL 2 requires an update to its kernel component"
- Ubuntu distribution not found

**Solutions:**

```powershell
# In PowerShell (Administrator)
wsl --update
wsl --set-default-version 2

# List distributions
wsl --list --verbose

# Install Ubuntu if missing
wsl --install -d Ubuntu-22.04
```

### WSL2 Network Issues

**Symptoms:**
- Cannot reach internet from WSL
- DNS resolution fails

**Solutions:**

```bash
# In WSL Ubuntu
cat /etc/resolv.conf

# If nameserver is wrong, create override
sudo rm /etc/resolv.conf
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf

# Prevent overwrite
sudo chattr +i /etc/resolv.conf
```

### WSL2 Performance Issues

**Symptoms:**
- Slow file access
- High memory usage

**Solutions:**

Create `%USERPROFILE%\.wslconfig`:
```ini
[wsl2]
memory=4GB
processors=2
localhostForwarding=true
```

Then restart WSL:
```powershell
wsl --shutdown
wsl
```

---

## FTP Server Issues

### Authentication Failures

**Symptoms:**
- "530 Login incorrect"
- Cannot connect with test/12345

**Solutions:**

```bash
# Verify container is running
docker ps | grep ftp

# Check environment variables
docker exec s9_ftp_server env | grep FTP

# Test with correct credentials
# Default: test / 12345

# Manual test
python -c "
from ftplib import FTP
ftp = FTP()
ftp.connect('localhost', 2121)
ftp.login('test', '12345')
print('Success!')
ftp.quit()
"
```

> **Instructor note:** In my experience running this lab, the most common issue is students forgetting that FTP uses TWO separate TCP connections — one for control commands (port 21/2121) and another for data transfer (passive ports 60000-60010). If the control channel works but file transfer fails, always check passive mode configuration first. This catches about 70% of FTP problems.


### Passive Mode Failures

**Symptoms:**
- "425 Cannot open data connection"
- File listing hangs

**Solutions:**

```bash
# Verify passive ports are mapped
docker port s9_ftp_server

# Should show:
# 2121/tcp -> 0.0.0.0:2121
# 60000-60010/tcp -> various ports

# Check firewall (Windows)
# Allow ports 60000-60010 inbound
```

### Data Transfer Corruption

**Symptoms:**
- Downloaded files are corrupted
- Size mismatch

**Solutions:**

```python
# Ensure binary mode for non-text files
ftp.retrbinary('RETR filename.bin', open('local.bin', 'wb').write)

# For text files only
ftp.retrlines('RETR readme.txt', callback)
```

---

## Wireshark Issues

### No Interfaces Found

**Symptoms:**
- Interface list is empty
- "You don't have permission to capture"

**Solutions:**

1. Run Wireshark as Administrator
2. Reinstall Npcap:
   - Download from https://npcap.com/
   - Enable "WinPcap API-compatible Mode"
   - Enable "Install Npcap in WinPcap API-compatible Mode"

### Cannot Capture WSL Traffic

**Symptoms:**
- vEthernet (WSL) not visible
- No packets captured

**Solutions:**

1. Select correct interface: `vEthernet (WSL)`
2. If not visible:
   ```powershell
   # In PowerShell (Administrator)
   Get-NetAdapter | Where-Object {$_.Name -like "*WSL*"}
   ```
3. Ensure WSL is running before starting Wireshark

### FTP Not Decoded

**Symptoms:**
- FTP commands show as raw TCP
- No protocol dissection

**Solutions:**

1. Right-click packet on port 2121
2. Select "Decode As..."
3. Set "Current" to "FTP"
4. Click "Save" then "OK"

---

## Python/Code Issues

### struct.error: Bad Packing

**Symptoms:**
- "struct.error: unpack requires a buffer of X bytes"
- Incorrect data length

**Solutions:**

```python
# Always use recv_exactly pattern
def recv_exactly(sock, n):
    """Receive exactly n bytes from socket."""
    data = b''
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Connection closed")
        data += chunk
    return data

# Then use:
header = recv_exactly(sock, 14)  # For 14-byte header
```

### Endianness Errors

**Symptoms:**
- Integers have wrong values
- Protocol parsing fails

**Solutions:**

```python
# ALWAYS use network byte order for protocols
import struct

# Correct: big-endian (network byte order)
packed = struct.pack(">I", value)  # or "!I"

# Incorrect for network protocols:
packed = struct.pack("<I", value)  # little-endian

# Verification
value = 0x12345678
print(struct.pack(">I", value).hex())  # Should be: 12345678
print(struct.pack("<I", value).hex())  # Would be: 78563412
```

### Import Errors

**Symptoms:**
- "ModuleNotFoundError: No module named 'X'"

**Solutions:**

```bash
# Install dependencies
pip install -r setup/requirements.txt

# Or install specific package
pip install pyftpdlib pyyaml colorama

# Verify installation
pip list | grep -i ftp
```

### CRC Mismatch

**Symptoms:**
- "CRC verification failed"
- Integrity check errors

**Solutions:**

```python
import zlib

# ALWAYS mask to unsigned 32-bit
crc = zlib.crc32(data) & 0xFFFFFFFF

# Common mistake (can give negative values on some Python versions):
# crc = zlib.crc32(data)  # Don't use without mask!
```

---

## Network Issues

### Cannot Connect to Server

**Symptoms:**
- "Connection refused"
- Timeout errors

**Solutions:**

```bash
# Check if port is listening
docker exec s9_ftp_server netstat -tlnp

# Test connectivity
nc -zv localhost 2121

# Check Docker network
docker network inspect week9_ftp_network
```

### DNS Resolution Fails

**Symptoms:**
- "Name or service not known"
- Cannot resolve hostnames

**Solutions:**

```bash
# In WSL
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf

# Or use IP addresses directly
# Instead of: ftp.connect("hostname", 2121)
# Use: ftp.connect("127.0.0.1", 2121)
```

---

## ASE Laboratory Specific Issues

### WiFi Network Restrictions

**Symptoms:**
- Docker pull times out on ASE-Student WiFi
- Cannot download images

**Solutions:**

1. Use wired connection in laboratory (preferred)
2. Or temporarily use mobile hotspot for downloads:
   ```bash
   # Download images
   docker pull python:3.11-slim
   # Then switch back to ASE-Student
   ```

### VPN Interference

**Symptoms:**
- WSL loses network when ASE VPN is active
- Cannot reach localhost

**Solutions:**

1. Disconnect VPN during laboratory work
2. Or configure split tunneling (contact IT support)
3. Use laboratory computers instead of personal laptops

### Limited Disk Space

**Symptoms:**
- "No space left on device"
- Docker build fails

**Solutions:**

```bash
# Clean unused Docker resources
docker system prune -a --volumes

# Check disk usage
df -h
docker system df

# Remove old images
docker image prune -a
```

**Warning:** This removes ALL unused Docker data. Save important containers first.

### Portainer Access Issues

**Symptoms:**
- Cannot access http://localhost:9000
- Portainer container not running

**Solutions:**

```bash
# Check Portainer status
docker ps | grep portainer

# If not running, start it
docker start portainer

# If doesn't exist, contact laboratory instructor
# Portainer should be pre-installed on laboratory machines
```

---

## Complete Reset Procedure

If all else fails, perform a complete reset:

### Step 1: Stop Everything

```bash
# Stop laboratory containers
cd /mnt/d/NETWORKING/WEEK9/09enWSL
docker compose -f docker/docker-compose.yml down --volumes

# Verify only Portainer remains
docker ps
```

### Step 2: Clean Docker

```bash
# Remove Week 9 resources (keeps Portainer!)
docker container prune -f
docker image prune -a -f
docker network prune -f
docker volume prune -f
```

### Step 3: Verify Environment

```bash
# Check Docker
docker ps  # Should show only Portainer

# Check WSL
wsl --status

# Check Python
python3 --version  # Should be 3.10+
```

### Step 4: Rebuild

```bash
# Navigate to project
cd /mnt/d/NETWORKING/WEEK9/09enWSL

# Install dependencies
pip install -r setup/requirements.txt

# Start fresh
make setup
make start
```

### Step 5: Verify

```bash
# Run smoke tests
make smoke

# Check containers
docker ps

# Test FTP connection
python -c "
from ftplib import FTP
ftp = FTP()
ftp.connect('localhost', 2121)
ftp.login('test', '12345')
print(ftp.pwd())
ftp.quit()
print('All working!')
"
```

---

## Getting Help

If you cannot resolve an issue using this guide:

1. **Check existing issues:** https://github.com/antonioclim/netENwsl/issues
2. **Open a new issue:** Include error messages, steps to reproduce, and environment details
3. **Ask on course forum:** Moodle ASE → Computer Networks 2025-2026
4. **Office hours:** Check course schedule on Moodle

When reporting issues, include:
- Operating system and version
- Docker version (`docker --version`)
- Python version (`python3 --version`)
- Complete error message
- Steps to reproduce

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Week 9: Session Layer and Presentation Layer*
