# Troubleshooting Guide — Week 8

> NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

---

## Before You Debug: Predict

Before examining fixes, ask yourself:

1. **What did I expect to happen?**
2. **What actually happened?**
3. **What changed since it last worked?**

> 💭 **Debugging mindset:** The error message tells you WHAT went wrong. Your job is to figure out WHY.

---

## Docker Issues

### Docker Daemon Not Running

**Symptoms:**
- `Cannot connect to the Docker daemon`
- `docker: command not found`
- Containers fail to start

> 💭 **Predict:** What command starts Docker in WSL? What's the password?

**Solutions:**

```bash
# Start Docker service in WSL
sudo service docker start
# Password: stud

# Verify Docker is running
docker info

# If still failing, check status
sudo service docker status
```

### WSL2 Backend Issues

**Symptoms:**
- Docker commands hang
- `WSL2 is not installed` error

**Solutions:**

```powershell
# In PowerShell (Administrator)
wsl --status
wsl --update
wsl --set-default-version 2

# Restart WSL
wsl --shutdown
```

### Port Already in Use

**Symptoms:**
- `Bind for 0.0.0.0:8080 failed: port is already allocated`

> 💭 **Predict:** What command shows which process is using a port?

**Solutions:**

```bash
# Find process using port (WSL/Linux)
sudo lsof -i :8080
# Or
sudo ss -tlnp | grep 8080

# Kill process by PID
kill -9 <pid>

# Or change port in docker-compose.yml
# "8080:80" → "8081:80"
```

### Container Startup Failures

**Symptoms:**
- Containers exit immediately
- Health checks fail

> 💭 **Predict:** Where would you look first — logs or configuration?

**Diagnostics:**
```bash
# Check container logs (FIRST STEP)
docker logs week8-nginx-proxy
docker logs week8-backend-1

# Check container state
docker inspect week8-nginx-proxy --format='{{.State.Status}}'

# View container events
docker events --filter container=week8-nginx-proxy
```

**Common Fixes:**

1. **Configuration errors**: Check nginx.conf syntax
   ```bash
   docker exec week8-nginx-proxy nginx -t
   ```

2. **Missing files**: Ensure www/ directory exists
   ```bash
   ls -la www/
   ```

3. **Network issues**: Recreate network
   ```bash
   docker network rm week8-laboratory-network
   docker compose up -d
   ```

---

## Network Connectivity Issues

### Cannot Reach localhost:8080

> 💭 **Predict:** List three reasons why localhost:8080 might not respond.

**Diagnostics:**
```bash
# Is nginx listening inside container?
docker exec week8-nginx-proxy netstat -tlnp

# What port is mapped?
docker port week8-nginx-proxy

# Can container reach itself?
docker exec week8-nginx-proxy curl localhost:80
```

**Solutions:**

1. Verify port mapping in docker-compose.yml
2. Check Windows Firewall settings
3. Try 127.0.0.1 instead of localhost

### Backends Not Responding

**Symptoms:**
- nginx returns 502 Bad Gateway
- Requests timeout

**Diagnostics:**
```bash
# Check backend health
curl http://localhost:8080/nginx-health

# Test backend directly from nginx container
docker exec week8-nginx-proxy curl http://backend1:8080/health

# Check backend logs
docker logs week8-backend-1
```

> 💭 **Think:** Why test from nginx container, not from host?

**Solutions:**

1. Verify backends are running: `docker ps`
2. Check upstream configuration in nginx
3. Restart backend containers:
   ```bash
   docker restart week8-backend-1 week8-backend-2 week8-backend-3
   ```

### DNS Resolution Issues

**Symptoms:**
- `Could not resolve host: backend1`

**Solutions:**

Docker Compose creates DNS for service names automatically. If failing:

```bash
# Recreate containers with fresh network
docker compose down
docker compose up -d

# Verify DNS from nginx container
docker exec week8-nginx-proxy nslookup backend1
```

---

## HTTP/Proxy Issues

### 502 Bad Gateway

> 💭 **Predict:** What does 502 mean? (Hint: it's about the PROXY, not the client)

**Causes:**
- Backend servers not running
- Incorrect upstream configuration
- Network connectivity issues between proxy and backends

**Diagnostics:**
```bash
# Check all backends from proxy
for i in 1 2 3; do
    echo "Backend $i:"
    docker exec week8-nginx-proxy curl -s http://backend$i:8080/health || echo "FAILED"
done
```

### 504 Gateway Timeout

**Causes:**
- Backend processing too slowly
- Connection timeout too short

**Solution:**
Add timeout settings to nginx configuration:
```nginx
proxy_connect_timeout 60s;
proxy_send_timeout 60s;
proxy_read_timeout 60s;
```

### Load Balancing Not Working

**Symptoms:**
- All requests go to same backend
- Weighted distribution incorrect

> 💭 **Predict:** Why might all requests go to one backend even with round-robin configured?

**Diagnostics:**
```bash
# Test distribution
for i in {1..12}; do
    curl -s http://localhost:8080/ | grep -o 'Backend [0-9]'
done | sort | uniq -c
```

**Solutions:**

1. Check upstream configuration syntax
2. Verify all backends are healthy
3. Clear browser cache (for testing)
4. Use incognito mode or curl for testing

### Headers Not Forwarded

**Symptoms:**
- Client IP shows as nginx IP
- Missing X-Forwarded headers

**Solution:**
Ensure proxy headers are set in nginx:
```nginx
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
```

---

## Python Script Issues

### ModuleNotFoundError

**Symptoms:**
- `No module named 'docker'`
- Import errors

**Solutions:**
```bash
# Install missing packages
pip install docker requests pyyaml pytest --break-system-packages

# Or use requirements.txt
pip install -r setup/requirements.txt --break-system-packages
```

### Permission Denied

**Symptoms:**
- Cannot create files
- Socket access denied

**Solutions:**

```bash
# Check Docker socket permissions
ls -la /var/run/docker.sock

# Fix permissions
sudo chmod 666 /var/run/docker.sock

# Or add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### Script Not Found

**Symptoms:**
- `python: can't open file`

**Solutions:**
```bash
# Run from correct directory
cd /mnt/d/NETWORKING/WEEK8/8enWSL
python3 scripts/start_lab.py

# Or use absolute path
python3 /mnt/d/NETWORKING/WEEK8/8enWSL/scripts/start_lab.py
```

---

## Wireshark Issues

### No Packets Captured

> 💭 **Predict:** What are three reasons Wireshark might show no packets?

**Causes:**
- Wrong interface selected
- Capture not started
- Traffic on different interface

**Solutions:**

1. For Docker traffic, capture on `vEthernet (WSL)` or `Loopback`
2. Or use tcpdump inside container:
   ```bash
   docker exec week8-nginx-proxy tcpdump -i any port 80 -w /tmp/capture.pcap
   docker cp week8-nginx-proxy:/tmp/capture.pcap pcap/
   ```

### Wireshark Permission Errors

**Windows Solution:**
Run Wireshark as Administrator

**WSL Solution:**
```bash
# Add user to wireshark group
sudo usermod -aG wireshark $USER
# Log out and back in
```

---

## Performance Issues

### Slow Container Startup

**Causes:**
- Image not cached
- Slow disk I/O

**Solutions:**
```bash
# Pre-pull images
docker pull nginx:alpine
docker pull python:3.11-slim
```

### High Memory Usage

**Solutions:**
Add to docker-compose.yml under each service:
```yaml
deploy:
  resources:
    limits:
      memory: 256M
```

---

## Quick Diagnostic Checklist

When something doesn't work, check in this order:

```
□ Is Docker running?           → sudo service docker start
□ Are containers running?      → docker ps
□ Are there error logs?        → docker logs <container>
□ Is the port mapped?          → docker port <container>
□ Can container reach backend? → docker exec nginx curl backend:8080
□ Is configuration valid?      → docker exec nginx nginx -t
□ Is there a firewall issue?   → Check Windows Firewall
```

---

## Recovery Commands

### Complete Reset

```bash
# Stop and remove everything
python3 scripts/cleanup.py --full --prune

# Remove all week8 resources manually
docker rm -f $(docker ps -aq --filter "name=week8")
docker network rm week8-laboratory-network
docker volume rm $(docker volume ls -q --filter "name=week8")

# Start fresh
python3 scripts/start_lab.py --rebuild
```

### Quick Restart

```bash
# Restart all services
docker compose -f docker/docker-compose.yml restart

# Or stop and start
python3 scripts/stop_lab.py
python3 scripts/start_lab.py
```

---

## Getting Help

If issues persist:

1. Check container logs: `docker logs <container>`
2. Verify configuration file syntax
3. Review [docs/misconceptions.md](misconceptions.md) for common errors
4. Check expected outputs in `tests/expected_outputs.md`
5. Ask the instructor (bring your error messages!)

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
