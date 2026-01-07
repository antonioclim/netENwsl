# Troubleshooting Guide

> NETWORKING class - ASE, Informatics | by Revolvix

This guide covers common issues encountered during the Week 14 laboratory.

## Docker Issues

### Issue: "Cannot connect to the Docker daemon"

**Symptoms:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

**Solutions:**

1. Ensure Docker Desktop is running (check system tray icon)
2. Restart Docker Desktop
3. On WSL2, check Docker integration:
   - Open Docker Desktop Settings
   - Go to Resources > WSL Integration
   - Ensure your WSL distribution is enabled

### Issue: "Port already in use"

**Symptoms:**
```
Error response from daemon: driver failed programming external connectivity
bind for 0.0.0.0:8080 failed: port is already allocated
```

**Solutions:**

1. Find the process using the port:
   ```powershell
   netstat -ano | findstr "8080"
   ```

2. Stop the conflicting process:
   ```powershell
   taskkill /PID <process_id> /F
   ```

3. Or use different ports in docker-compose.yml

### Issue: Containers exit immediately

**Symptoms:**
```
Container week14_app1 exited with code 1
```

**Solutions:**

1. Check container logs:
   ```bash
   docker logs week14_app1
   ```

2. Common causes:
   - Python syntax error in application
   - Missing dependencies
   - Invalid command arguments

3. Try running interactively:
   ```bash
   docker compose run --rm app1 bash
   ```

### Issue: "Network not found"

**Symptoms:**
```
network week14_backend_net declared as external, but could not be found
```

**Solutions:**

1. Run full cleanup and restart:
   ```powershell
   python scripts/cleanup.py --full
   python scripts/start_lab.py
   ```

2. Or create networks manually:
   ```bash
   docker network create week14_backend_net
   docker network create week14_frontend_net
   ```

## WSL2 Issues

### Issue: WSL2 not available

**Symptoms:**
```
WSL2 is required but not available
```

**Solutions:**

1. Install WSL2:
   ```powershell
   wsl --install
   ```

2. Restart Windows after installation

3. Set WSL2 as default:
   ```powershell
   wsl --set-default-version 2
   ```

### Issue: Slow file system performance

**Symptoms:**
- Very slow Docker operations
- Build takes extremely long

**Solutions:**

1. Store project files inside WSL filesystem:
   ```bash
   cd ~
   git clone <repository>
   ```

2. NOT in `/mnt/c/` or other Windows paths

## Network Connectivity Issues

### Issue: Cannot reach containers from Windows

**Symptoms:**
```
curl: (7) Failed to connect to localhost port 8080
```

**Solutions:**

1. Verify containers are running:
   ```bash
   docker ps
   ```

2. Check port mappings:
   ```bash
   docker compose ps
   ```

3. Try using the container IP directly:
   ```bash
   docker inspect week14_lb | grep IPAddress
   curl http://<container_ip>:8080/
   ```

### Issue: Containers cannot reach each other

**Symptoms:**
```
curl: (7) Failed to connect to app1 port 8001: Connection refused
```

**Solutions:**

1. Verify network connectivity:
   ```bash
   docker compose exec client ping app1
   ```

2. Check service is listening:
   ```bash
   docker compose exec app1 ss -tlnp
   ```

3. Verify correct port in compose file

### Issue: Health checks failing

**Symptoms:**
```
Container week14_app1 is unhealthy
```

**Solutions:**

1. Check what the health check command does:
   ```bash
   docker inspect week14_app1 | grep -A 10 Healthcheck
   ```

2. Run health check manually:
   ```bash
   docker compose exec app1 curl -f http://localhost:8001/health
   ```

3. Check application logs for errors

## Packet Capture Issues

### Issue: Wireshark cannot see Docker traffic

**Symptoms:**
- No packets captured on Windows interfaces
- Cannot see inter-container traffic

**Solutions:**

1. Capture inside a container:
   ```bash
   docker compose exec client tcpdump -i eth0 -w /app/pcap/capture.pcap
   ```

2. Use Docker network interface in Wireshark

3. For WSL2, capture on `\Device\NPF_Loopback`

### Issue: tshark not found

**Symptoms:**
```
'tshark' is not recognized as a command
```

**Solutions:**

1. Add Wireshark to PATH:
   ```powershell
   $env:PATH += ";C:\Program Files\Wireshark"
   ```

2. Or reinstall Wireshark with "Install TShark" option

## Application Issues

### Issue: Load balancer shows only one backend

**Symptoms:**
- All requests go to same backend
- One backend shows 0 requests

**Solutions:**

1. Verify both backends are running:
   ```bash
   docker compose ps app1 app2
   ```

2. Check backend health:
   ```bash
   curl http://localhost:8001/health
   curl http://localhost:8002/health
   ```

3. Check LB status:
   ```bash
   curl http://localhost:8080/lb-status
   ```

### Issue: TCP echo server not responding

**Symptoms:**
```
Connection refused to localhost:9000
```

**Solutions:**

1. Verify echo container is running:
   ```bash
   docker compose ps echo
   ```

2. Check logs:
   ```bash
   docker compose logs echo
   ```

3. Test from within Docker network:
   ```bash
   docker compose exec client nc -v echo 9000
   ```

## Python Issues

### Issue: Module not found

**Symptoms:**
```
ModuleNotFoundError: No module named 'requests'
```

**Solutions:**

1. Install dependencies:
   ```powershell
   pip install -r setup/requirements.txt
   ```

2. Check Python version:
   ```powershell
   python --version
   ```

3. Use specific Python version:
   ```powershell
   py -3.11 scripts/start_lab.py
   ```

## Performance Issues

### Issue: Slow container startup

**Solutions:**

1. Pre-build images:
   ```bash
   docker compose build
   ```

2. Use local image cache (avoid --no-cache unless needed)

3. Increase Docker resource limits in Docker Desktop settings

### Issue: High CPU usage

**Solutions:**

1. Check resource-intensive containers:
   ```bash
   docker stats
   ```

2. Limit container resources in compose file:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '0.50'
         memory: 512M
   ```

## Getting Help

If you encounter an issue not covered here:

1. Check Docker logs:
   ```bash
   docker compose logs -f
   ```

2. Run environment verification:
   ```powershell
   python setup/verify_environment.py --verbose
   ```

3. Run tests to identify specific failures:
   ```powershell
   python tests/test_environment.py
   ```

4. Consult the course forum or instructor

---

*NETWORKING class - ASE, Informatics | by Revolvix*
