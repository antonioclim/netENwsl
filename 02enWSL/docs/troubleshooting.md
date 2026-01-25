# 🔧 Troubleshooting Guide — Week 2: Socket Programming

> NETWORKING class — ASE, CSIE Bucharest  
> Computer Networks Laboratory | by ing. dr. Antonio Clim

This guide helps you diagnose and fix common issues in socket programming labs.

**Rule of thumb:** 80% of issues are one of: server not running, wrong port, or wrong bind address. Check these first.

---

## 🚦 Quick Diagnostic Flowchart

```
START: "My code doesn't work"
           │
           ▼
┌─────────────────────────────┐
│ Is the server running?      │
│ Check: ps aux | grep python │
└─────────────────────────────┘
           │
     NO ◄──┴──► YES
     │           │
     ▼           ▼
┌─────────┐  ┌─────────────────────────┐
│ Start   │  │ Is server listening?    │
│ server  │  │ Check: ss -tlnp | grep  │
└─────────┘  │        <port>           │
             └─────────────────────────┘
                       │
                 NO ◄──┴──► YES
                 │           │
                 ▼           ▼
          ┌──────────┐  ┌─────────────────────────┐
          │ Check    │  │ Is bind address correct?│
          │ for      │  │ 0.0.0.0 = all interfaces│
          │ errors   │  │ 127.0.0.1 = local only  │
          └──────────┘  └─────────────────────────┘
                              │
                        NO ◄──┴──► YES
                        │           │
                        ▼           ▼
                 ┌──────────┐  ┌─────────────────┐
                 │ Fix bind │  │ Check firewall  │
                 │ address  │  │ and port number │
                 └──────────┘  └─────────────────┘
```

---

## Issue Categories

| Category | Symptoms | Likely Cause |
|----------|----------|--------------|
| **Connection** | Refused, timeout | Server not running, wrong address |
| **Binding** | Address in use | Previous instance, TIME_WAIT |
| **Data** | Wrong/missing data | Protocol mismatch, boundaries |
| **Docker** | Container unreachable | Network, bind address |
| **Wireshark** | No packets | Wrong interface, filter |

---

## Connection Issues

### ❌ "Connection refused"

**Symptoms:**
```
ConnectionRefusedError: [Errno 111] Connection refused
```

**Diagnostic steps:**

1. **Is the server running?**
   ```bash
   ps aux | grep python
   # Should show your server process
   ```

2. **Is server listening on the port?**
   ```bash
   ss -tlnp | grep 9090
   # Should show: LISTEN ... *:9090
   ```

3. **Are you connecting to the right address?**
   ```bash
   # If server binds to 127.0.0.1, client must connect to 127.0.0.1
   # If server binds to 0.0.0.0, client can connect to any interface
   ```

**Solutions:**

| Cause | Fix |
|-------|-----|
| Server not running | Start the server first |
| Wrong port | Check port numbers match |
| Server on different interface | Use correct IP or 0.0.0.0 |

**From experience:** 90% of "Connection refused" errors are because the server isn't running or the client is connecting to the wrong port. Double-check both before looking elsewhere.

---

### ❌ "Connection timed out"

**Symptoms:**
```
socket.timeout: timed out
# or: Connection timed out after 30 seconds
```

**Diagnostic steps:**

1. **Is the destination reachable?**
   ```bash
   ping <target_ip>
   ```

2. **Is a firewall blocking?**
   ```bash
   # Windows Firewall may block WSL traffic
   # Try disabling temporarily for testing
   ```

3. **Is the server responding?**
   ```bash
   # Check server logs for incoming connection attempts
   ```

**Solutions:**

| Cause | Fix |
|-------|-----|
| Network unreachable | Check network configuration |
| Firewall blocking | Add firewall exception |
| Server overloaded | Restart server, check logs |

---

## Binding Issues

### ❌ "Address already in use"

**Symptoms:**
```
OSError: [Errno 98] Address already in use
```

**Diagnostic steps:**

1. **What's using the port?**
   ```bash
   lsof -i :9090
   # or
   ss -tlnp | grep 9090
   ```

2. **Is it a previous instance?**
   ```bash
   ps aux | grep python
   # Kill any orphaned processes
   ```

3. **Is socket in TIME_WAIT?**
   ```bash
   ss -tn | grep 9090
   # Check for TIME_WAIT state
   ```

**Solutions:**

```python
# ALWAYS use SO_REUSEADDR in server code
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("0.0.0.0", 9090))
```

| Cause | Fix |
|-------|-----|
| Previous process | `kill <pid>` |
| TIME_WAIT state | Use SO_REUSEADDR |
| System service | Choose different port |

**Instructor note:** Students often forget to stop the server before restarting. Teach them to use Ctrl+C properly and check with `ps aux`.

---

### ❌ Cannot bind to specific IP

**Symptoms:**
```
OSError: [Errno 99] Cannot assign requested address
```

**Cause:** Trying to bind to an IP address not assigned to this machine.

**Solution:**
```python
# Bind to all interfaces
sock.bind(("0.0.0.0", 9090))

# OR bind to specific existing interface
# First check: ip addr show
sock.bind(("192.168.1.100", 9090))  # Must be YOUR IP
```

---

## Data Issues

### ❌ Receiving merged messages (TCP)

**Symptoms:**
```python
# Sent: "Hello" then "World"
# Received: "HelloWorld" (merged!)
```

**Cause:** TCP is a byte stream; it does not preserve message boundaries.

**Solutions:**

1. **Length-prefix framing:**
   ```python
   import struct
   
   # Send
   msg = b"Hello"
   sock.send(struct.pack(">I", len(msg)) + msg)
   
   # Receive
   length_data = sock.recv(4)
   length = struct.unpack(">I", length_data)[0]
   msg = sock.recv(length)
   ```

2. **Delimiter-based:**
   ```python
   # Send with newline delimiter
   sock.send(b"Hello\n")
   
   # Receive until delimiter
   buffer = b""
   while b"\n" not in buffer:
       buffer += sock.recv(1024)
   msg, buffer = buffer.split(b"\n", 1)
   ```

---

### ❌ Receiving partial data

**Symptoms:**
```python
# Expected 1000 bytes, received only 536
```

**Cause:** `recv()` returns as soon as ANY data is available, not when all expected data arrives.

**Solution:**
```python
def recv_exactly(sock, n):
    """Receive exactly n bytes."""
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Connection closed")
        data += chunk
    return data
```

---

## Docker Issues

### ❌ Cannot connect from container to host

**Symptoms:**
```bash
# From inside container:
curl http://localhost:9090
# Connection refused
```

**Cause:** `localhost` inside container refers to the container, not the host.

**Solutions:**

1. **Use host.docker.internal (Docker Desktop):**
   ```bash
   curl http://host.docker.internal:9090
   ```

2. **Use host network mode:**
   ```yaml
   # docker-compose.yml
   services:
     myservice:
       network_mode: "host"
   ```

3. **Bind server to 0.0.0.0:**
   ```python
   # Server must bind to 0.0.0.0, not 127.0.0.1
   sock.bind(("0.0.0.0", 9090))
   ```

---

### ❌ Container cannot reach external services

**Symptoms:**
```bash
# Inside container:
ping google.com
# Network unreachable
```

**Diagnostic:**
```bash
# Check Docker network
docker network ls
docker network inspect week2_network
```

**Solutions:**
```bash
# Restart Docker
sudo service docker restart

# Or restart WSL entirely
wsl --shutdown  # From PowerShell
```

---

## Wireshark Issues

### ❌ No packets captured

**Symptoms:** Wireshark shows empty capture while traffic should be occurring.

**Diagnostic checklist:**

1. **Correct interface selected?**
   - For WSL/Docker: **vEthernet (WSL)**
   - For localhost only: **Loopback Adapter**
   - For physical network: **Ethernet/Wi-Fi**

2. **Capture started before traffic?**
   - Start capture FIRST
   - Then run client/server

3. **Display filter too restrictive?**
   - Clear filter to see ALL traffic
   - Then refine

**Common filters:**
```
tcp.port == 9090         # TCP on port 9090
udp.port == 9091         # UDP on port 9091
ip.addr == 10.0.2.10     # Traffic to/from container
tcp.flags.syn == 1       # TCP SYN packets only
```

---

### ❌ Cannot see Docker traffic

**Cause:** Docker traffic on bridge networks may not appear on host interfaces.

**Solutions:**

1. **Use tcpdump inside container:**
   ```bash
   docker exec -it week2_lab tcpdump -i eth0 port 9090
   ```

2. **Use host network mode for debugging:**
   ```yaml
   network_mode: "host"
   ```

3. **Capture on docker0 interface (if available):**
   ```bash
   sudo tcpdump -i docker0 port 9090
   ```

---

## WSL-Specific Issues

### ❌ Docker not starting

**Symptoms:**
```bash
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

**Solution:**
```bash
sudo service docker start
# Enter password: stud

# Verify
docker ps
```

**Autostart tip:** This command must be run after EVERY Windows restart.

---

### ❌ Files not visible between Windows and WSL

**Windows → WSL:**
```
Windows path: D:\NETWORKING\WEEK2
WSL path:     /mnt/d/NETWORKING/WEEK2
```

**WSL → Windows:**
```
WSL path:     /home/stud/project
Windows path: \\wsl$\Ubuntu\home\stud\project
```

---

### ❌ "Permission denied" errors

**Symptoms:**
```bash
bash: ./script.py: Permission denied
```

**Solutions:**
```bash
# Add execute permission
chmod +x script.py

# Or run with Python explicitly
python3 script.py
```

---

## Nuclear Options

When nothing else works:

### Restart WSL
```powershell
# From PowerShell (Windows)
wsl --shutdown
# Then reopen Ubuntu
```

### Full Docker reset
```bash
# Stop all containers
docker stop $(docker ps -q)

# Remove all containers (except Portainer)
docker rm $(docker ps -aq --filter "name!=portainer")

# Restart Docker
sudo service docker restart
```

### Portainer recovery
```bash
# If Portainer is broken
docker stop portainer
docker rm portainer
docker volume rm portainer_data

# Recreate (will need initial setup again)
docker run -d -p 9000:9000 --name portainer \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce
```

---

## Quick Reference Card

| Problem | First Check | Quick Fix |
|---------|-------------|-----------|
| Connection refused | Is server running? | Start server |
| Address in use | What's on port? | Kill process or SO_REUSEADDR |
| Timeout | Is target reachable? | Check IP and firewall |
| Merged messages | Using TCP? | Add message framing |
| Container unreachable | Bind address? | Use 0.0.0.0 |
| No Wireshark packets | Right interface? | Use vEthernet (WSL) |
| Docker not working | Service running? | `sudo service docker start` |

---

## When to Escalate

If you've spent more than 15 minutes on an issue:

1. Document what you've tried
2. Note exact error messages
3. Check [docs/misconceptions.md](misconceptions.md)
4. Ask a classmate (pair debugging works!)
5. Issues: Open an issue in GitHub

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
