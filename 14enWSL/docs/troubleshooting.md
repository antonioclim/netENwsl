# Troubleshooting Guide — Week 14

> NETWORKING class — ASE, CSIE | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

This guide helps diagnose and resolve common issues encountered during the Week 14 laboratory session.

From my experience, about 80% of "container not starting" issues come from forgetting to run `sudo service docker start` after a Windows restart.

---

## Quick Diagnostics Checklist

Before diving into specific issues, run through this checklist:

```bash
# 1. Docker daemon running?
sudo service docker status

# 2. Containers running?
docker ps --filter name=week14

# 3. Networks exist?
docker network ls | grep week14

# 4. Ports listening?
ss -tlnp | grep -E '8080|8001|8002|9090'

# 5. Can reach load balancer?
curl -s http://localhost:8080/health
```

---

## Issue 1: Docker Daemon Not Running

### Symptoms
- "Cannot connect to Docker daemon"
- "docker: command not found" (in some cases)
- All docker commands fail

### Diagnosis
```bash
sudo service docker status
# or
systemctl status docker
```

### Solution
```bash
# Start Docker in WSL2
sudo service docker start

# Verify it started
docker info
```

### Prevention
Add to your `.bashrc`:
```bash
# Auto-start Docker if not running
if ! pgrep -x "dockerd" > /dev/null; then
    sudo service docker start
fi
```

---

## Issue 2: Port Already in Use

### Symptoms
- "Bind: address already in use"
- Container exits immediately
- Port mapping fails

### Diagnosis
```bash
# Find what is using the port
sudo ss -tlnp | grep :8080
# or
sudo lsof -i :8080
```

### Solution
```bash
# Option 1: Stop the conflicting process
kill <PID>

# Option 2: Use a different port in docker-compose
# Change "8080:80" to "8081:80"

# Option 3: Stop all week14 containers and restart
docker compose -f docker/docker-compose.yml down
docker compose -f docker/docker-compose.yml up -d
```

---

## Issue 3: Container Starts But Service Not Responding

### Symptoms
- `docker ps` shows container running
- `curl localhost:8080` fails or times out
- No response from service

### Diagnosis
```bash
# Check container logs
docker logs week14_app1

# Check if service is listening inside container
docker exec week14_app1 ss -tlnp

# Check health endpoint
docker exec week14_app1 curl -s localhost:8080/health
```

### Solution
The service inside the container may have crashed. Common causes:

1. **Missing dependencies:** Check logs for import errors
2. **Configuration error:** Verify environment variables
3. **Crash loop:** Container restarts repeatedly

```bash
# Restart the specific container
docker restart week14_app1

# Or rebuild and restart
docker compose -f docker/docker-compose.yml up -d --build app1
```

---

## Issue 4: Containers Cannot Communicate

### Symptoms
- Load balancer returns 502 errors
- "Name or service not known" errors
- Ping between containers fails

### Diagnosis
```bash
# Check containers are on same network
docker network inspect week14_backend_net

# Test DNS resolution inside container
docker exec week14_lb nslookup app1

# Test connectivity
docker exec week14_lb ping -c 2 app1
```

### Solution
```bash
# Ensure containers are on the correct network
docker network connect week14_backend_net week14_app1

# Restart with fresh networks
docker compose -f docker/docker-compose.yml down
docker network prune -f
docker compose -f docker/docker-compose.yml up -d
```

---

## Issue 5: Permission Denied Errors

### Symptoms
- "Permission denied" when running scripts
- Cannot write to mounted volumes
- Docker socket access denied

### Diagnosis
```bash
# Check file permissions
ls -la scripts/start_lab.py

# Check Docker group membership
groups $USER
```

### Solution
```bash
# Make scripts executable
chmod +x scripts/*.py

# Add user to docker group (requires logout/login)
sudo usermod -aG docker $USER
newgrp docker

# Fix volume permissions
sudo chown -R $USER:$USER docker/volumes/
```

---

## Issue 6: WSL2-Specific Issues

### Symptoms
- Network unreachable from Windows browser
- localhost not resolving
- Slow file system performance

### Diagnosis
```bash
# Check WSL2 IP address
ip addr show eth0

# Verify WSL2 networking mode
cat /etc/resolv.conf
```

### Solution

**Cannot access from Windows browser:**
```bash
# Find WSL2 IP
hostname -I

# Access via WSL2 IP instead of localhost
# http://172.x.x.x:8080 instead of http://localhost:8080
```

**Slow file system:**
Store project files in WSL2 filesystem (`/home/`), not Windows (`/mnt/c/`).

---

## Issue 7: Wireshark Cannot Capture Traffic

### Symptoms
- No packets captured
- "Permission denied" on interface
- Cannot see Docker traffic

### Diagnosis
```bash
# List available interfaces
ip link show

# Check tcpdump permissions
which tcpdump
ls -la $(which tcpdump)
```

### Solution
```bash
# Install tcpdump if missing
sudo apt install tcpdump

# Run Wireshark with sudo (not recommended for regular use)
sudo wireshark

# Or add capabilities
sudo setcap cap_net_raw,cap_net_admin+eip $(which dumpcap)
```

**For Docker traffic:**
Capture on the Docker bridge interface (`docker0` or `br-*`), not `eth0`.

---

## Issue 8: Quiz Script Errors

### Symptoms
- "ModuleNotFoundError: No module named 'yaml'"
- Quiz fails to load
- Encoding errors

### Diagnosis
```bash
# Check Python version
python3 --version

# Check if pyyaml is installed
python3 -c "import yaml; print(yaml.__version__)"
```

### Solution
```bash
# Install dependencies
pip install -r setup/requirements.txt

# Or install yaml specifically
pip install pyyaml

# Fix encoding issues (set UTF-8)
export PYTHONIOENCODING=utf-8
```

---

## Issue 9: Load Balancer 502 Bad Gateway

### Symptoms
- Intermittent 502 errors
- Some requests succeed, others fail
- Error rate around 50%

### Diagnosis
```bash
# Check all backends are running
docker ps --filter name=week14_app

# Test each backend directly
curl -s http://localhost:8001/health
curl -s http://localhost:8002/health

# Check load balancer logs
docker logs week14_lb --tail 20
```

### Solution
If one backend is down, the round-robin LB will still route to it until health check fails:

```bash
# Restart the failed backend
docker restart week14_app1

# Wait for health check (usually 5-10 seconds)
sleep 10

# Verify both backends healthy
curl -s http://localhost:8080/health
```

---

## Issue 10: "Connection Refused" vs "Connection Timed Out"

### Understanding the Difference

| Error | Meaning | Likely Cause |
|-------|---------|--------------|
| Connection refused | Host reachable, port not listening | Service not running |
| Connection timed out | No response received | Firewall, wrong IP, host down |
| No route to host | Network path unavailable | Routing issue, network down |

### Diagnosis Approach
```bash
# Step 1: Is the host reachable?
ping -c 2 <target>

# Step 2: Is the port open?
nc -zv <target> <port>

# Step 3: Is the service responding?
curl -v http://<target>:<port>/
```

---

## Emergency Recovery

If everything is broken, start fresh:

```bash
# Nuclear option: remove everything week14-related
docker compose -f docker/docker-compose.yml down --volumes --remove-orphans
docker system prune -f
docker network prune -f

# Rebuild from scratch
docker compose -f docker/docker-compose.yml build --no-cache
docker compose -f docker/docker-compose.yml up -d

# Verify
make smoke
```

---

## Getting Help

If you cannot resolve an issue:

1. Check the error message carefully — it often contains the solution
2. Search the error message online
3. Review the relevant section in `docs/theory_summary.md`
4. Open an issue on GitHub with:
   - Error message (full output)
   - Steps to reproduce
   - Your environment (`uname -a`, `docker --version`)

---

*Document version: 2.0 | Week 14: Integrated Recap | January 2025*
*NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim*
