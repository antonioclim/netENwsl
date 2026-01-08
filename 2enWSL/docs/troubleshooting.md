# Troubleshooting Guide — Week 2

> NETWORKING class - ASE, Informatics | by Revolvix

## Quick Diagnostics

Before diving into specific issues, run the environment verification:

```powershell
python setup/verify_environment.py
```

This will identify most common configuration problems.

---

## Docker Issues

### Issue: Docker daemon not running

**Symptoms:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

**Solution:**
1. Open Docker Desktop application
2. Wait for the Docker icon in the system tray to show "running"
3. Verify with `docker info`

**WSL2 Note:** If using WSL2 backend, ensure Docker Desktop has WSL Integration enabled:
Settings → Resources → WSL Integration → Enable for your distribution

---

### Issue: Container fails to start

**Symptoms:**
```
Error response from daemon: Conflict. The container name is already in use
```

**Solution:**
```bash
# Remove the conflicting container
docker rm -f week2_lab

# Restart
python scripts/start_lab.py
```

---

### Issue: Port already in use

**Symptoms:**
```
bind: address already in use
Error starting userland proxy: listen tcp4 0.0.0.0:9090: bind: address already in use
```

**Solution:**

**Windows (PowerShell):**
```powershell
# Find process using port
netstat -ano | findstr :9090

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**Linux/WSL:**
```bash
# Find process using port
sudo lsof -i :9090

# Kill process
sudo kill -9 <PID>
```

---

### Issue: Cannot access container from Windows

**Symptoms:** Services running inside container but not accessible from localhost.

**Solution:**
1. Ensure port mapping in docker-compose.yml:
   ```yaml
   ports:
     - "9090:9090"
   ```

2. Check Windows Firewall isn't blocking the port

3. Verify container is on correct network:
   ```bash
   docker network inspect week2_network
   ```

---

## Python Issues

### Issue: ModuleNotFoundError

**Symptoms:**
```
ModuleNotFoundError: No module named 'docker'
```

**Solution:**
```bash
pip install -r setup/requirements.txt
```

Or for specific packages:
```bash
pip install docker pyyaml requests
```

---

### Issue: Python version too old

**Symptoms:**
```
SyntaxError: invalid syntax (on type hints or f-strings)
```

**Solution:**
Install Python 3.11 or later from python.org. Verify:
```bash
python --version
```

---

### Issue: Socket bind error in exercise scripts

**Symptoms:**
```
OSError: [Errno 98] Address already in use
```

**Solution:**
1. A previous server is still running. Kill it:
   ```bash
   # Find Python processes
   ps aux | grep python
   
   # Kill the process
   kill <PID>
   ```

2. Wait for socket timeout (typically 60 seconds) or use SO_REUSEADDR:
   ```python
   sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   ```

---

## Network Issues

### Issue: Cannot capture traffic with Wireshark

**Symptoms:** No packets visible in Wireshark when running exercises.

**Solution:**

**For localhost traffic:**
- Windows: Capture on "Adapter for loopback traffic capture" or "Npcap Loopback Adapter"
- Linux: Capture on `lo` interface

**For Docker traffic:**
- Capture on `docker0` bridge interface
- Or use `\\.\pipe\docker_engine` on Windows

**Alternative:** Use tcpdump inside container:
```bash
docker exec -it week2_lab tcpdump -i eth0 -w /app/pcap/capture.pcap
```

---

### Issue: TCP connection refused

**Symptoms:**
```
ConnectionRefusedError: [Errno 111] Connection refused
```

**Causes and Solutions:**

1. **Server not running:**
   - Start the server first: `python src/exercises/ex_2_01_tcp.py server`

2. **Wrong port:**
   - Verify port number matches between server and client

3. **Firewall blocking:**
   - Temporarily disable firewall for testing
   - Add exception for Python executable

---

### Issue: UDP packets not received

**Symptoms:** Client sends messages but server shows nothing.

**Causes and Solutions:**

1. **Firewall dropping UDP:**
   - UDP is often blocked more aggressively than TCP
   - Add explicit firewall rule for UDP port

2. **Wrong bind address:**
   - Server bound to `127.0.0.1` won't receive from Docker network
   - Use `0.0.0.0` to bind to all interfaces

3. **Buffer size too small:**
   ```python
   # Increase receive buffer
   data, addr = sock.recvfrom(4096)  # Not 1024
   ```

---

## WSL2 Issues

### Issue: WSL2 not available

**Symptoms:**
```
WSL 2 requires an update to its kernel component
```

**Solution:**
1. Download WSL2 kernel update from Microsoft
2. Install and restart
3. Set WSL2 as default: `wsl --set-default-version 2`

---

### Issue: Networking between Windows and WSL2

**Symptoms:** Cannot access WSL2 services from Windows or vice versa.

**Solution:**

1. **Access WSL2 from Windows:**
   ```powershell
   # Get WSL2 IP
   wsl hostname -I
   
   # Connect to that IP instead of localhost
   ```

2. **Access Windows from WSL2:**
   ```bash
   # Windows host is accessible via
   cat /etc/resolv.conf  # nameserver is Windows IP
   ```

3. **Use localhost forwarding (newer WSL2):**
   - Ensure `localhostforwarding=true` in `.wslconfig`

---

## Exercise-Specific Issues

### TCP Exercise (ex_2_01_tcp.py)

**Issue:** Iterative server seems frozen

**Cause:** In iterative mode, server handles one client at a time.

**Solution:** This is expected behaviour. Use threaded mode for concurrent handling:
```bash
python src/exercises/ex_2_01_tcp.py server --mode threaded
```

---

### UDP Exercise (ex_2_02_udp.py)

**Issue:** Timeout errors in interactive mode

**Symptoms:**
```
socket.timeout: timed out
```

**Solution:**
1. Ensure server is running
2. Check correct port (default: 9091)
3. Increase timeout if network is slow:
   ```python
   sock.settimeout(5.0)  # 5 seconds
   ```

---

## Performance Issues

### Issue: Slow container startup

**Solution:**
1. Allocate more resources to Docker Desktop:
   Settings → Resources → CPUs: 2+, Memory: 4GB+

2. Ensure WSL2 backend is enabled (faster than Hyper-V)

3. Prune unused Docker resources:
   ```bash
   docker system prune -a
   ```

---

### Issue: High memory usage

**Solution:**
1. Limit WSL2 memory in `%UserProfile%\.wslconfig`:
   ```ini
   [wsl2]
   memory=4GB
   ```

2. Stop unused containers:
   ```bash
   python scripts/stop_lab.py
   ```

---

## Getting Further Help

1. **Check logs:**
   ```bash
   docker logs week2_lab
   ```

2. **Run smoke test:**
   ```bash
   python tests/smoke_test.py
   ```

3. **Verify environment:**
   ```bash
   python setup/verify_environment.py
   ```

4. **Consult documentation:**
   - Docker: https://docs.docker.com
   - Python socket: https://docs.python.org/3/library/socket.html
   - Wireshark: https://www.wireshark.org/docs/

---

*NETWORKING class - ASE, Informatics | by Revolvix*
