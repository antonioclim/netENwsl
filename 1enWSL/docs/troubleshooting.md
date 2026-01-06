# Troubleshooting Guide

> NETWORKING class - ASE, Informatics | by Revolvix

Common issues and solutions for Week 1 laboratory exercises.

---

## Docker Issues

### Docker Desktop Not Starting

**Symptoms:**
- Docker Desktop stuck on "Starting..."
- "Cannot connect to Docker daemon" error

**Solutions:**

1. **Restart Docker Desktop**
   ```powershell
   # Close Docker Desktop completely
   # Right-click tray icon > Quit Docker Desktop
   # Wait 30 seconds, then restart
   ```

2. **Reset Docker Desktop**
   ```powershell
   # Settings > Troubleshoot > Reset to factory defaults
   # Warning: This removes all containers and images
   ```

3. **Check WSL2 Integration**
   ```powershell
   wsl --status
   wsl --update
   ```

4. **Reinstall WSL2 Kernel**
   ```powershell
   wsl --update --web-download
   ```

### "Cannot connect to Docker daemon"

**Symptoms:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

**Solutions:**

1. **Start Docker Desktop** - Ensure it's running in the system tray

2. **Check Docker service (WSL)**
   ```bash
   sudo service docker status
   sudo service docker start
   ```

3. **Verify Docker socket**
   ```bash
   ls -la /var/run/docker.sock
   ```

### Container Build Failures

**Symptoms:**
- `docker compose build` fails
- "no space left on device" error

**Solutions:**

1. **Clean up Docker resources**
   ```powershell
   docker system prune -a
   docker volume prune
   ```

2. **Increase Docker disk allocation**
   - Docker Desktop > Settings > Resources > Disk image size

3. **Check available disk space**
   ```powershell
   Get-PSDrive C
   ```

---

## Network Issues

### "Address already in use"

**Symptoms:**
```
OSError: [Errno 98] Address already in use
bind: Address already in use
```

**Solutions:**

1. **Find process using the port**
   ```bash
   ss -tlnp | grep PORT
   # or
   netstat -tlnp | grep PORT
   ```

2. **Kill the process**
   ```bash
   kill PID
   # or force
   kill -9 PID
   ```

3. **Wait for TIME_WAIT to expire**
   - TCP connections stay in TIME_WAIT for ~60 seconds
   - Wait and retry, or use a different port

4. **Use SO_REUSEADDR in code**
   ```python
   sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   ```

### "Connection refused"

**Symptoms:**
```
Connection refused
nc: connect to localhost port 9090 (tcp) failed: Connection refused
```

**Solutions:**

1. **Verify server is running**
   ```bash
   ss -tlnp | grep 9090
   ```

2. **Check correct port number**

3. **Verify firewall settings**
   ```powershell
   # Windows Firewall
   Get-NetFirewallRule | Where-Object {$_.Enabled -eq 'True'}
   ```

4. **Check if server is bound to correct interface**
   - `0.0.0.0` = all interfaces
   - `127.0.0.1` = localhost only

### Ping Fails

**Symptoms:**
```
ping: sendmsg: Operation not permitted
```

**Solutions:**

1. **Run with sudo (if required)**
   ```bash
   sudo ping -c 4 HOST
   ```

2. **Check container capabilities**
   - Ensure `NET_RAW` capability is enabled in docker-compose.yml

3. **Verify network connectivity**
   ```bash
   ip route
   ip addr
   ```

### DNS Resolution Fails

**Symptoms:**
```
ping: google.com: Temporary failure in name resolution
```

**Solutions:**

1. **Check DNS configuration**
   ```bash
   cat /etc/resolv.conf
   ```

2. **Test with IP address**
   ```bash
   ping 8.8.8.8  # If this works, DNS is the issue
   ```

3. **Manually set DNS**
   ```bash
   echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
   ```

---

## Python Issues

### Import Errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'scapy'
```

**Solutions:**

1. **Install missing package**
   ```bash
   pip install scapy --break-system-packages
   ```

2. **Verify correct Python environment**
   ```bash
   which python
   python --version
   ```

3. **Use virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

### Permission Denied (Scripts)

**Symptoms:**
```
bash: ./script.py: Permission denied
```

**Solutions:**

1. **Make script executable**
   ```bash
   chmod +x script.py
   ```

2. **Run with Python explicitly**
   ```bash
   python script.py
   ```

### Socket Permission Denied

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied
```

**Solutions:**

1. **Use port above 1024** (unprivileged ports)

2. **Run with sudo** (for ports below 1024)
   ```bash
   sudo python server.py
   ```

3. **Use capabilities**
   ```bash
   sudo setcap 'cap_net_bind_service=+ep' /usr/bin/python3
   ```

---

## Capture Issues

### tcpdump Permission Denied

**Symptoms:**
```
tcpdump: eth0: You don't have permission to capture on that device
```

**Solutions:**

1. **Run with sudo**
   ```bash
   sudo tcpdump -i eth0
   ```

2. **Add user to wireshark group**
   ```bash
   sudo usermod -aG wireshark $USER
   newgrp wireshark
   ```

### tshark Permission Denied

**Symptoms:**
```
tshark: Couldn't run /usr/bin/dumpcap in child process: Permission denied
```

**Solutions:**

1. **Configure dumpcap permissions**
   ```bash
   sudo dpkg-reconfigure wireshark-common
   # Select "Yes" for non-root users
   sudo usermod -aG wireshark $USER
   ```

2. **Logout and login** or run `newgrp wireshark`

### No Packets Captured

**Symptoms:**
- Capture runs but shows no packets

**Solutions:**

1. **Check correct interface**
   ```bash
   ip link show
   tcpdump -D  # List available interfaces
   ```

2. **Use `-i any` to capture all interfaces**
   ```bash
   tcpdump -i any port 9090
   ```

3. **Verify traffic is being generated** during capture

4. **Check capture filter syntax**
   - Incorrect filter may exclude all packets

### PCAP File Empty or Corrupted

**Symptoms:**
- File size is 0 or very small
- tshark reports "The file isn't a capture file"

**Solutions:**

1. **Let capture run longer** before stopping

2. **Don't interrupt capture abruptly**
   - Use Ctrl+C to stop cleanly
   - Use `-c COUNT` to auto-stop

3. **Verify write permissions**
   ```bash
   touch test.pcap
   ls -la test.pcap
   ```

---

## WSL2 Issues

### WSL2 Not Installed

**Symptoms:**
```
'wsl' is not recognized as an internal or external command
```

**Solutions:**

1. **Install WSL2**
   ```powershell
   # Run as Administrator
   wsl --install
   ```

2. **Enable required Windows features**
   ```powershell
   dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
   dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
   ```

3. **Restart computer**

### WSL2 Network Issues

**Symptoms:**
- Cannot access host from WSL2
- Port forwarding not working

**Solutions:**

1. **Get WSL2 IP address**
   ```bash
   hostname -I
   ```

2. **Use `localhost` from Windows**
   - WSL2 ports should be accessible via localhost

3. **Check Windows Firewall**
   ```powershell
   New-NetFirewallRule -DisplayName "WSL2" -Direction Inbound -Action Allow
   ```

---

## Quick Diagnostic Commands

Run these to gather diagnostic information:

```bash
# System information
uname -a
cat /etc/os-release

# Network configuration
ip addr
ip route
cat /etc/resolv.conf

# Docker status
docker info
docker ps -a
docker network ls

# Port usage
ss -tulnp

# Process information
ps aux | grep python
ps aux | grep nc
```

---

## Getting Help

If you encounter an issue not covered here:

1. **Check the error message carefully** - it often contains the solution hint
2. **Search the documentation** in the `docs/` directory
3. **Run verification tests**
   ```bash
   python tests/test_environment.py
   python tests/smoke_test.py
   ```
4. **Check Docker logs**
   ```bash
   docker compose logs
   ```
5. **Contact the instructor** during laboratory hours

---

*NETWORKING class - ASE, Informatics | by Revolvix*
