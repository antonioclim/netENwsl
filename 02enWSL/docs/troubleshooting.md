# Troubleshooting Guide — Week 2

> NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim

---

## 🌳 Quick Diagnostic Decision Tree

Start here when something goes wrong:

```
                         ┌─────────────────────────────┐
                         │   What's the symptom?       │
                         └─────────────┬───────────────┘
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        │                              │                              │
        ▼                              ▼                              ▼
┌───────────────────┐    ┌───────────────────┐    ┌───────────────────┐
│ "Connection       │    │ "Address already  │    │ No packets in     │
│  refused"         │    │  in use"          │    │ Wireshark         │
└─────────┬─────────┘    └─────────┬─────────┘    └─────────┬─────────┘
          │                        │                        │
          ▼                        ▼                        ▼
   Is server running?       Kill old process       Correct interface?
   ┌────┴────┐              ss -tlnp | grep       vEthernet (WSL)?
   NO       YES              [port]                      │
   │         │                   │                       │
   ▼         ▼                   ▼                       ▼
Start     Wrong port?      kill <PID> or          Generate traffic
server    Check both       wait 60 seconds        DURING capture
          sides


        ┌──────────────────────────────┼──────────────────────────────┐
        │                              │                              │
        ▼                              ▼                              ▼
┌───────────────────┐    ┌───────────────────┐    ┌───────────────────┐
│ "Cannot connect   │    │ ModuleNotFound    │    │ Docker daemon     │
│  to Docker"       │    │ Error             │    │ not running       │
└─────────┬─────────┘    └─────────┬─────────┘    └─────────┬─────────┘
          │                        │                        │
          ▼                        ▼                        ▼
   sudo service           pip install -r           sudo service
   docker start           requirements.txt         docker start
```

---

## 🚦 Issue Severity Guide

| Severity | Meaning | Action |
|----------|---------|--------|
| 🔴 **Blocker** | Cannot continue lab | Fix immediately |
| 🟡 **Major** | Significant functionality broken | Fix before next exercise |
| 🟢 **Minor** | Inconvenience, workaround exists | Fix when convenient |

---

## ⏱️ When to Ask for Help

**Try these steps first (5 minutes max):**

1. Read the error message completely
2. Check the relevant section in this guide
3. Run `python setup/verify_environment.py`
4. Search the error message online

**Ask for help when:**

- [ ] You've spent more than 10 minutes on the same issue
- [ ] The error message doesn't appear in this guide
- [ ] Your environment verification shows failures you can't fix
- [ ] You suspect a bug in the lab materials

**How to ask effectively:**

```
1. What were you trying to do?
2. What command did you run? (exact command)
3. What was the error? (copy full error message)
4. What have you already tried?
```

---

## 💭 Prediction-Based Debugging

Before examining specific issues, use this systematic approach:

### The "Expected vs Actual" Framework

When something goes wrong, ask yourself:

| Question | Example |
|----------|---------|
| **What did I expect?** | "Server should print 'Connection from...'" |
| **What actually happened?** | "Nothing printed, client got 'Connection refused'" |
| **What's the gap?** | "Server isn't listening on the port" |

### Common Expectation Mismatches

| Expected | Actual | Root cause |
|----------|--------|------------|
| TCP handshake in Wireshark | No packets at all | Wrong capture interface |
| Server accepts connection | "Connection refused" | Server not running or wrong port |
| UDP response received | Timeout | Server down, firewall, or wrong address |
| Multiple clients handled | Only one at a time | Using iterative instead of threaded mode |

### Quick Self-Check Questions

Before asking for help, verify:

1. **Is the server actually running?** Check with `ss -tlnp | grep 9090`
2. **Am I using the right port?** Double-check both server and client
3. **Is Docker running?** Verify with `docker ps`
4. **Am I in the right directory?** Check with `pwd`

---

## Quick Diagnostics

Before examining specific issues, run the environment verification:

```bash
python setup/verify_environment.py
```

This will identify most common configuration problems.

---

## Docker Issues

### Issue: Docker daemon not running

| Severity | 🔴 **Blocker** |
|----------|----------------|

**Symptoms:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

**Solution:**

**For WSL2 (our environment):**
```bash
sudo service docker start
docker ps  # Verify it's running
```

**For Docker Desktop:**
1. Open Docker Desktop application
2. Wait for the Docker icon in the system tray to show "running"
3. Verify with `docker info`

**WSL2 Note:** If using Docker Desktop with WSL2 backend, ensure WSL Integration is enabled:
Settings → Resources → WSL Integration → Enable for your distribution

---

### Issue: Container fails to start

| Severity | 🟡 **Major** |
|----------|--------------|

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

### Issue: Port already in use (Docker)

| Severity | 🟡 **Major** |
|----------|--------------|

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

| Severity | 🟡 **Major** |
|----------|--------------|

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

| Severity | 🟢 **Minor** |
|----------|--------------|

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

| Severity | 🔴 **Blocker** |
|----------|----------------|

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

| Severity | 🟡 **Major** |
|----------|--------------|

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

| Severity | 🟡 **Major** |
|----------|--------------|

**Symptoms:** No packets visible in Wireshark when running exercises.

**Solution:**

**For WSL traffic (our environment):**
- Select **vEthernet (WSL)** interface in Wireshark
- Start capture BEFORE generating traffic
- Use filter: `tcp.port == 9090` or `udp.port == 9091`

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

| Severity | 🟡 **Major** |
|----------|--------------|

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

4. **Server bound to wrong address:**
   - If server bound to 127.0.0.1, only localhost can connect
   - Use 0.0.0.0 to accept from all interfaces

---

### Issue: UDP packets not received

| Severity | 🟡 **Major** |
|----------|--------------|

**Symptoms:** Client sends messages but server shows nothing.

**Causes and Solutions:**

1. **Firewall dropping UDP:**
   - UDP is often blocked by default; add firewall exception

2. **Wrong port or address:**
   - Verify both sides use same port
   - Check server is bound to 0.0.0.0, not 127.0.0.1

3. **No error on client side:**
   - UDP sendto() succeeds even if nobody is listening
   - This is expected behaviour — UDP has no delivery confirmation

---

### Issue: Wireshark shows no TCP handshake

| Severity | 🟢 **Minor** |
|----------|--------------|

**Symptoms:** Data packets visible but no SYN/SYN-ACK/ACK.

**Causes:**
1. **Capture started too late:**
   - Start Wireshark BEFORE running client
   
2. **Filter too restrictive:**
   - Remove filters temporarily to see all traffic
   
3. **Connection reused:**
   - If using persistent connections, handshake happened earlier

**Verification:**
```
# Filter for SYN packets specifically
tcp.flags.syn == 1 && tcp.flags.ack == 0
```

---

## WSL-Specific Issues

### Issue: "Cannot find service docker"

| Severity | 🔴 **Blocker** |
|----------|----------------|

**Symptoms:**
```
docker: command not found
```
or
```
Job for docker.service failed
```

**Solution:**
1. Check if Docker is installed:
   ```bash
   which docker
   ```

2. Start Docker manually:
   ```bash
   sudo service docker start
   ```

3. Common fix — ensure iptables is available:
   ```bash
   sudo update-alternatives --set iptables /usr/sbin/iptables-legacy
   sudo service docker start
   ```

---

### Issue: WSL2 networking unreachable

| Severity | 🟡 **Major** |
|----------|--------------|

**Symptoms:** Cannot reach localhost from Windows, or vice versa.

**Solution:**
1. Restart WSL:
   ```powershell
   wsl --shutdown
   wsl
   ```

2. Check WSL IP address:
   ```bash
   ip addr show eth0
   ```

3. From Windows, use that IP instead of localhost

---

### Issue: Performance issues with /mnt/c/ paths

| Severity | 🟢 **Minor** |
|----------|--------------|

**Symptoms:** Scripts run slowly when accessing Windows files.

**Solution:**
- Work in `/home/stud/` instead of `/mnt/c/` or `/mnt/d/`
- Copy files to WSL filesystem for better performance:
  ```bash
  cp -r /mnt/d/NETWORKING/WEEK2 ~/WEEK2
  cd ~/WEEK2/2enWSL
  ```

---

## Getting Further Help

### Self-Help Checklist

Before asking for help, confirm:

- [ ] Docker is running (`docker ps` shows containers)
- [ ] You're in the correct directory (`pwd`)
- [ ] The server is running before the client
- [ ] Port numbers match between server and client
- [ ] Wireshark is capturing on the correct interface

### Diagnostic Commands Reference

```bash
# Check Docker status
docker ps
docker logs week2_lab

# Check network
ss -tlnp | grep 9090    # TCP listeners
ss -ulnp | grep 9091    # UDP listeners
ip addr                  # Network interfaces

# Check processes
ps aux | grep python
lsof -i :9090           # What's using port 9090

# Environment verification
python setup/verify_environment.py

# Run smoke tests
python tests/smoke_test.py
```

### External Resources

| Resource | URL |
|----------|-----|
| Docker documentation | https://docs.docker.com |
| Python socket module | https://docs.python.org/3/library/socket.html |
| Wireshark user guide | https://www.wireshark.org/docs/ |
| WSL documentation | https://docs.microsoft.com/en-us/windows/wsl/ |

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
