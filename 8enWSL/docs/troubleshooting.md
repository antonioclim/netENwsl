# Troubleshooting Guide — Week 8

> NETWORKING class - ASE, Informatics | by Revolvix

## Docker Issues

### Docker Desktop Not Running

**Symptoms:**
- `Cannot connect to the Docker daemon`
- `docker: command not found`
- Containers fail to start

**Solutions:**

1. Start Docker Desktop from the Windows Start Menu
2. Wait 30-60 seconds for initialisation
3. Verify with: `docker info`

If Docker Desktop fails to start:
```powershell
# Restart Docker Desktop service
net stop com.docker.service
net start com.docker.service
```

### WSL2 Backend Issues

**Symptoms:**
- Docker commands hang
- `WSL2 is not installed` error

**Solutions:**

```powershell
# Check WSL status
wsl --status

# Update WSL
wsl --update

# Set WSL2 as default
wsl --set-default-version 2

# Restart WSL
wsl --shutdown
```

### Port Already in Use

**Symptoms:**
- `Bind for 0.0.0.0:8080 failed: port is already allocated`

**Solutions:**

```bash
# Find process using port (Windows PowerShell)
netstat -ano | findstr :8080

# Kill process by PID
taskkill /PID <pid> /F

# Or use a different port in docker-compose.yml
# Change "8080:80" to "8081:80"
```

### Container Startup Failures

**Symptoms:**
- Containers exit immediately
- Health checks fail

**Diagnostics:**
```bash
# Check container logs
docker logs week8-nginx-1
docker logs week8-backend1-1

# Check container state
docker inspect week8-nginx-1 --format='{{.State.Status}}'

# View all container events
docker events --filter container=week8-nginx-1
```

**Common Fixes:**

1. **Configuration errors**: Check nginx.conf syntax
   ```bash
   docker exec week8-nginx-1 nginx -t
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

## Network Connectivity Issues

### Cannot Reach localhost:8080

**Diagnostics:**
```bash
# Check if nginx is listening
docker exec week8-nginx-1 netstat -tlnp

# Check port mapping
docker port week8-nginx-1

# Test from inside container
docker exec week8-nginx-1 curl localhost:80
```

**Solutions:**

1. Verify port mapping in docker-compose.yml
2. Check Windows Firewall settings
3. Try accessing via 127.0.0.1 instead of localhost

### Backends Not Responding

**Symptoms:**
- nginx returns 502 Bad Gateway
- Requests timeout

**Diagnostics:**
```bash
# Check backend health
curl http://localhost:8080/nginx-health

# Test backend directly
docker exec week8-nginx-1 curl http://backend1:8080/health

# Check backend logs
docker logs week8-backend1-1
```

**Solutions:**

1. Verify backends are running: `docker ps`
2. Check upstream configuration in nginx
3. Restart backend containers:
   ```bash
   docker restart week8-backend1-1 week8-backend2-1 week8-backend3-1
   ```

### DNS Resolution Issues

**Symptoms:**
- `Could not resolve host: backend1`

**Solutions:**

Docker Compose automatically creates DNS for service names. If failing:

```bash
# Recreate containers with fresh network
docker compose down
docker compose up -d

# Verify DNS from nginx container
docker exec week8-nginx-1 nslookup backend1
```

## HTTP/Proxy Issues

### 502 Bad Gateway

**Causes:**
- Backend servers not running
- Incorrect upstream configuration
- Network connectivity issues

**Diagnostics:**
```bash
# Check all backends
for i in 1 2 3; do
    echo "Backend $i:"
    docker exec week8-nginx-1 curl -s http://backend$i:8080/health || echo "FAILED"
done
```

### 504 Gateway Timeout

**Causes:**
- Backend processing too slow
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
3. Clear browser cache (for sticky sessions)
4. Use incognito mode for testing

### Headers Not Forwarded

**Symptoms:**
- Client IP shows as nginx IP
- Missing X-Forwarded headers

**Solution:**
Ensure proxy headers are set:
```nginx
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
```

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
# Run as administrator (Windows)
# Right-click PowerShell > Run as Administrator

# Check Docker socket permissions (Linux/WSL)
sudo chmod 666 /var/run/docker.sock
```

### Script Not Found

**Symptoms:**
- `python: can't open file`

**Solutions:**
```bash
# Run from correct directory
cd WEEK8_WSLkit
python scripts/start_lab.py

# Or use absolute path
python /path/to/WEEK8_WSLkit/scripts/start_lab.py
```

## Wireshark Issues

### No Packets Captured

**Causes:**
- Wrong interface selected
- Capture not started
- Traffic on different interface

**Solutions:**

1. For Docker traffic, capture on `\Device\NPF_Loopback` or `Loopback`
2. Or use tcpdump inside container:
   ```bash
   docker exec week8-nginx-1 tcpdump -i any port 80 -w /tmp/capture.pcap
   docker cp week8-nginx-1:/tmp/capture.pcap pcap/
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

# Use SSD storage for Docker
# Docker Desktop > Settings > Resources > Disk image location
```

### High Memory Usage

**Solutions:**
```bash
# Limit container memory
# Add to docker-compose.yml under each service:
deploy:
  resources:
    limits:
      memory: 256M
```

## Recovery Commands

### Complete Reset

```bash
# Stop and remove everything
python scripts/cleanup.py --full --prune

# Remove all week8 resources manually
docker rm -f $(docker ps -aq --filter "name=week8")
docker network rm week8-laboratory-network
docker volume rm $(docker volume ls -q --filter "name=week8")

# Start fresh
python scripts/start_lab.py --rebuild
```

### Quick Restart

```bash
# Restart all services
docker compose -f docker/docker-compose.yml restart

# Or stop and start
python scripts/stop_lab.py
python scripts/start_lab.py
```

## Getting Help

If issues persist:

1. Check container logs: `docker logs <container>`
2. Verify configuration files syntax
3. Consult documentation in `docs/` directory
4. Review expected outputs in `tests/expected_outputs.md`

---

*NETWORKING class - ASE, Informatics | by Revolvix*
