# Week 11: Troubleshooting Guide

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
> 
> by Revolvix

This document addresses common issues encountered during the Week 11 laboratory session on load balancing and application protocols.

---

## Table of Contents

1. [Docker and Container Issues](#1-docker-and-container-issues)
2. [Load Balancer Problems](#2-load-balancer-problems)
3. [Port and Network Conflicts](#3-port-and-network-conflicts)
4. [Python Script Issues](#4-python-script-issues)
5. [WSL2 Specific Issues](#5-wsl2-specific-issues)
6. [Packet Capture Problems](#6-packet-capture-problems)

---

## 1. Docker and Container Issues

### 1.1 Docker Desktop Not Running

**Symptoms:**
```
error during connect: This error may indicate that the docker daemon is not running
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

**Solution:**
1. Launch Docker Desktop from the Start Menu
2. Wait for the whale icon to stabilise (green)
3. Verify with `docker info`

If Docker Desktop fails to start:
```powershell
# Restart Docker service (Admin PowerShell)
Restart-Service docker

# Check service status
Get-Service docker
```

### 1.2 Containers Fail to Start

**Symptoms:**
```
Error response from daemon: Conflict. The container name "/s11_nginx_lb" is already in use
```

**Solution:**
```powershell
# Remove existing containers
docker rm -f s11_nginx_lb s11_backend_1 s11_backend_2 s11_backend_3

# Or use cleanup script
python scripts/cleanup.py
```

### 1.3 Image Build Failures

**Symptoms:**
```
ERROR: failed to solve: failed to compute cache key: failed to calculate checksum
```

**Solution:**
```powershell
# Clear Docker build cache
docker builder prune -f

# Rebuild without cache
docker compose -f docker/docker-compose.yml build --no-cache
```

### 1.4 Volume Permission Errors

**Symptoms:**
```
Error: EACCES: permission denied
nginx: [emerg] open() "/etc/nginx/nginx.conf" failed (13: Permission denied)
```

**Solution:**
```powershell
# Reset permissions (WSL terminal)
wsl chmod 644 docker/configs/nginx.conf

# Or recreate volumes
docker compose -f docker/docker-compose.yml down -v
docker compose -f docker/docker-compose.yml up -d
```

---

## 2. Load Balancer Problems

### 2.1 Uneven Traffic Distribution

**Symptoms:**
One backend receives significantly more requests than others.

**Diagnosis:**
```powershell
# Send 10 requests and observe distribution
1..10 | ForEach-Object { curl -s http://localhost:8080/ }
```

**Possible Causes:**
1. **IP hash enabled**: All requests from same IP go to same backend
2. **Weight misconfiguration**: Check `weight` in nginx.conf
3. **Backend unhealthy**: Check container status

**Solution:**
```powershell
# Check nginx.conf for algorithm
cat docker/configs/nginx.conf | Select-String -Pattern "least_conn|ip_hash"

# Ensure round-robin (remove ip_hash and least_conn)
# Restart nginx
docker compose -f docker/docker-compose.yml restart nginx
```

### 2.2 All Requests Fail (502 Bad Gateway)

**Symptoms:**
```html
<html><body><h1>502 Bad Gateway</h1></body></html>
```

**Diagnosis:**
```powershell
# Check if backends are running
docker compose -f docker/docker-compose.yml ps

# Check backend logs
docker compose -f docker/docker-compose.yml logs web1 web2 web3
```

**Solution:**
```powershell
# Restart all services
docker compose -f docker/docker-compose.yml restart

# Or recreate containers
docker compose -f docker/docker-compose.yml up -d --force-recreate
```

### 2.3 Failover Not Working

**Symptoms:**
Stopping a backend causes all requests to fail instead of redirecting.

**Solution:**
Verify `proxy_next_upstream` in nginx.conf:
```nginx
proxy_next_upstream error timeout http_500 http_502 http_503 http_504;
proxy_next_upstream_timeout 10s;
proxy_next_upstream_tries 3;
```

Check upstream configuration:
```nginx
upstream backend_pool {
    server web1:80 max_fails=2 fail_timeout=10s;
    server web2:80 max_fails=2 fail_timeout=10s;
    server web3:80 max_fails=2 fail_timeout=10s;
}
```

---

## 3. Port and Network Conflicts

### 3.1 Port Already in Use

**Symptoms:**
```
Error starting userland proxy: listen tcp4 0.0.0.0:8080: bind: address already in use
```

**Diagnosis:**
```powershell
# Find process using port
Get-NetTCPConnection -LocalPort 8080 | Select-Object OwningProcess
Get-Process -Id <PID>

# Or in CMD
netstat -ano | findstr :8080
```

**Solution:**
```powershell
# Terminate conflicting process
Stop-Process -Id <PID> -Force

# Or stop Python backends
Get-Process python* | Stop-Process -Force
```

### 3.2 Network Already Exists

**Symptoms:**
```
Error response from daemon: network with name s11_network already exists
```

**Solution:**
```powershell
# Remove network
docker network rm s11_network

# Or disconnect all containers first
docker network disconnect s11_network $(docker ps -q)
docker network rm s11_network
```

### 3.3 DNS Resolution Inside Containers

**Symptoms:**
Containers cannot resolve each other by name.

**Solution:**
Ensure all services are on the same network in docker-compose.yml:
```yaml
services:
  nginx:
    networks:
      - s11_network
  web1:
    networks:
      - s11_network

networks:
  s11_network:
    driver: bridge
```

---

## 4. Python Script Issues

### 4.1 Module Not Found

**Symptoms:**
```
ModuleNotFoundError: No module named 'dnspython'
ModuleNotFoundError: No module named 'paramiko'
```

**Solution:**
```powershell
# Install required packages
pip install dnspython paramiko pyftpdlib requests pyyaml --break-system-packages

# Or use requirements
pip install -r setup/requirements.txt --break-system-packages
```

### 4.2 Connection Refused to Backends

**Symptoms:**
```
ConnectionRefusedError: [Errno 111] Connection refused
```

**Diagnosis:**
```powershell
# Check if backend is running
curl http://localhost:8081/

# Check if port is listening
netstat -ano | findstr :8081
```

**Solution:**
Start the backend servers:
```powershell
# In separate terminals
python src/exercises/ex_11_01_backend.py --id 1 --port 8081
python src/exercises/ex_11_01_backend.py --id 2 --port 8082
python src/exercises/ex_11_01_backend.py --id 3 --port 8083
```

### 4.3 Load Balancer Script Crashes

**Symptoms:**
```
OSError: [Errno 98] Address already in use
BrokenPipeError: [Errno 32] Broken pipe
```

**Solution:**
```powershell
# Kill existing Python processes
Get-Process python* | Stop-Process -Force

# Wait for port release
Start-Sleep -Seconds 5

# Restart load balancer
python src/exercises/ex_11_02_loadbalancer.py ...
```

### 4.4 DNS Query Timeout

**Symptoms:**
```
dns.exception.Timeout: The DNS operation timed out
```

**Solution:**
1. Check internet connectivity
2. Try alternative DNS server:
```powershell
python src/exercises/ex_11_03_dns_client.py google.com A --server 1.1.1.1
```

---

## 5. WSL2 Specific Issues

### 5.1 WSL2 Not Installed

**Symptoms:**
```
WSL 2 is not installed. Please install it via: wsl --install
```

**Solution:**
```powershell
# Install WSL2 (Admin PowerShell)
wsl --install

# Restart computer
Restart-Computer
```

### 5.2 Network Issues Between Windows and WSL2

**Symptoms:**
Windows cannot access services running in WSL2.

**Solution:**
```powershell
# Get WSL2 IP
wsl hostname -I

# Use WSL2 IP instead of localhost
curl http://<WSL2_IP>:8080/
```

### 5.3 Docker Integration Disabled

**Symptoms:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

**Solution:**
1. Open Docker Desktop Settings
2. Navigate to Resources > WSL Integration
3. Enable integration for your WSL2 distribution
4. Apply & Restart

---

## 6. Packet Capture Problems

### 6.1 tshark Not Found

**Symptoms:**
```
'tshark' is not recognized as an internal or external command
```

**Solution:**
Add Wireshark to PATH:
```powershell
# Add to current session
$env:PATH += ";C:\Program Files\Wireshark"

# Or use full path
& "C:\Program Files\Wireshark\tshark.exe" -i eth0 -w capture.pcap
```

### 6.2 No Interfaces Available

**Symptoms:**
```
tshark: There are no interfaces on which a capture can be done
```

**Solution:**
Run as Administrator:
```powershell
# Elevate PowerShell
Start-Process powershell -Verb RunAs

# Then run capture
python scripts/capture_traffic.py
```

### 6.3 Capture Permission Denied

**Symptoms:**
```
Capturing on 'eth0' requires running with root privileges
```

**Solution (WSL):**
```bash
# Use sudo in WSL
sudo tcpdump -i eth0 -w capture.pcap

# Or add user to wireshark group
sudo usermod -aG wireshark $USER
```

---

## Quick Recovery Procedure

If the laboratory environment becomes unstable, perform a full reset:

```powershell
# 1. Stop all Python processes
Get-Process python* | Stop-Process -Force

# 2. Full cleanup
python scripts/cleanup.py --full --prune

# 3. Verify Docker is running
docker info

# 4. Restart laboratory
python scripts/start_lab.py --rebuild

# 5. Verify services
python scripts/start_lab.py --status
```

---

## Contact and Support

For issues not covered in this guide:

1. Check Docker logs: `docker compose logs`
2. Verify environment: `python setup/verify_environment.py`
3. Consult the course forum or contact the laboratory assistant

---

*NETWORKING class - ASE, Informatics | by Revolvix*
