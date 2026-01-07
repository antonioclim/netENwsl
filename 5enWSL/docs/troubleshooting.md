# Troubleshooting Guide

> Week 5 - NETWORKING class - ASE, Informatics
>
> by Revolvix

## Docker Issues

### Docker Desktop Not Running

**Symptoms:**
- `docker info` returns an error
- Scripts fail with "Cannot connect to Docker daemon"

**Solutions:**
1. Start Docker Desktop from the Start menu (Windows) or Applications (macOS)
2. Wait 30-60 seconds for Docker to fully initialise
3. Verify with `docker info`

### WSL2 Backend Not Enabled (Windows)

**Symptoms:**
- Docker runs but containers are slow
- Network connectivity issues between containers

**Solutions:**
1. Open Docker Desktop settings
2. Go to General tab
3. Enable "Use the WSL 2 based engine"
4. Apply and restart Docker

### Port Already in Use

**Symptoms:**
- Container fails to start
- Error: "bind: address already in use"

**Solutions:**
```powershell
# Find process using the port
netstat -ano | findstr :9999

# Kill the process (Windows)
taskkill /PID <process_id> /F

# Or change the port in docker-compose.yml
```

### Container Creation Fails

**Symptoms:**
- `docker compose up` fails
- Image build errors

**Solutions:**
```powershell
# Rebuild without cache
python scripts/start_lab.py --rebuild

# Or manually
docker compose build --no-cache
docker compose up -d
```

## Network Connectivity Issues

### Containers Cannot Communicate

**Symptoms:**
- Ping between containers fails
- Applications cannot connect

**Solutions:**
1. Verify containers are on the same network:
   ```powershell
   docker network inspect week5_labnet
   ```

2. Check container IP addresses:
   ```powershell
   docker exec week5_python ip addr
   ```

3. Verify firewall isn't blocking:
   ```powershell
   # Windows Firewall may block Docker traffic
   # Try temporarily disabling or adding rules
   ```

### DNS Resolution Fails

**Symptoms:**
- Cannot resolve hostnames
- `ping google.com` fails from container

**Solutions:**
1. Check DNS configuration:
   ```bash
   docker exec week5_python cat /etc/resolv.conf
   ```

2. Try using IP addresses directly
3. Verify host machine has internet connectivity

### Cannot Access Container from Host

**Symptoms:**
- `localhost:9999` doesn't respond
- Port mapping appears correct

**Solutions:**
1. Verify port mapping:
   ```powershell
   docker ps
   # Check PORTS column
   ```

2. Test from inside container first:
   ```bash
   docker exec week5_python curl localhost:9999
   ```

3. Check if service is listening:
   ```bash
   docker exec week5_udp-server netstat -ulnp
   ```

## Python/Exercise Issues

### Module Import Errors

**Symptoms:**
- `ModuleNotFoundError: No module named 'src'`
- Import failures in exercises

**Solutions:**
1. Ensure you're running from the correct directory:
   ```powershell
   cd WEEK5_WSLkit
   ```

2. Run exercises through Docker:
   ```powershell
   docker exec week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py --help
   ```

3. Check PYTHONPATH:
   ```bash
   docker exec week5_python echo $PYTHONPATH
   # Should include /app
   ```

### Exercise Output Missing Colours

**Symptoms:**
- Output shows escape codes like `[32m`
- Formatting appears broken

**Solutions:**
1. Use a terminal that supports ANSI colours
2. Run with `--json` flag for clean output
3. On Windows, use Windows Terminal instead of CMD

### Invalid IP Address Errors

**Symptoms:**
- `ValueError: invalid IP address`
- Exercises reject valid-looking addresses

**Solutions:**
1. Verify address format:
   - Include prefix for CIDR: `192.168.1.1/24`
   - Use network address for FLSM: `192.168.1.0/24`

2. Check for typos and extra spaces

3. Ensure IPv4 octets are 0-255

## Packet Capture Issues

### tcpdump Permission Denied

**Symptoms:**
- `tcpdump: permission denied`
- Cannot capture traffic

**Solutions:**
1. Container should have NET_ADMIN capability (included in compose file)
2. If running directly, add capability:
   ```powershell
   docker run --cap-add=NET_ADMIN ...
   ```

### No Packets Captured

**Symptoms:**
- tcpdump runs but shows no output
- Capture file is empty

**Solutions:**
1. Verify interface name:
   ```bash
   docker exec week5_python ip link
   # Use correct interface (usually eth0)
   ```

2. Generate traffic while capturing:
   ```bash
   # In one terminal
   docker exec week5_python tcpdump -i eth0

   # In another terminal
   docker exec week5_python ping 10.5.0.20
   ```

3. Check filter is not too restrictive

### Wireshark Cannot Read Capture

**Symptoms:**
- Wireshark shows no packets
- File appears corrupted

**Solutions:**
1. Ensure capture completed properly (Ctrl+C to stop tcpdump)
2. Copy file from container correctly:
   ```powershell
   docker cp week5_python:/app/pcap/capture.pcap ./capture.pcap
   ```

3. Try capinfos to verify file:
   ```powershell
   capinfos capture.pcap
   ```

## Performance Issues

### Containers Start Slowly

**Symptoms:**
- `docker compose up` takes several minutes
- Timeouts during startup

**Solutions:**
1. Increase Docker Desktop resources:
   - Settings → Resources → Advanced
   - Increase memory to 4GB+
   - Increase CPUs to 2+

2. Use pre-built images when possible:
   ```powershell
   python scripts/start_lab.py
   # (without --rebuild unless necessary)
   ```

### High CPU Usage

**Symptoms:**
- System becomes slow
- Docker Desktop using excessive CPU

**Solutions:**
1. Stop unused containers:
   ```powershell
   python scripts/stop_lab.py
   ```

2. Limit container resources in docker-compose.yml:
   ```yaml
   services:
     python:
       deploy:
         resources:
           limits:
             cpus: '1.0'
             memory: 512M
   ```

## Getting Help

### Diagnostic Information

Collect this information when reporting issues:

```powershell
# Docker version
docker version

# Docker info
docker info

# Container status
docker ps -a

# Container logs
docker logs week5_python

# Network info
docker network ls
docker network inspect week5_labnet
```

### Clean Reset

If all else fails, perform a complete reset:

```powershell
# Stop everything
python scripts/stop_lab.py

# Full cleanup
python scripts/cleanup.py --full --prune

# Rebuild from scratch
python scripts/start_lab.py --rebuild
```
