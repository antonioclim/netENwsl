# Troubleshooting Guide: Week 9

> Common issues and solutions for Session Layer (L5) and Presentation Layer (L6) Laboratory
> NETWORKING class - ASE, Informatics | by Revolvix

---

## Quick Diagnostics

Before examining specific issues, run these diagnostic commands:

```powershell
# 1. Verify environment
python setup/verify_environment.py

# 2. Check Docker status
docker info

# 3. Check running containers
docker ps

# 4. Run smoke tests
python tests/smoke_test.py
```

---

## Docker Issues

### Docker Desktop Not Running

**Symptoms:**
- "Cannot connect to the Docker daemon"
- "docker: command not found"
- "Error response from daemon: dial unix /var/run/docker.sock"

**Solutions:**

1. **Start Docker Desktop:**
   - Open Docker Desktop from Start Menu
   - Wait for "Docker Desktop is running" status

2. **Enable WSL2 Backend:**
   ```
   Docker Desktop > Settings > General > Use WSL 2 based engine
   ```

3. **Restart Docker service (PowerShell Admin):**
   ```powershell
   Restart-Service docker
   ```

4. **Verify installation:**
   ```powershell
   docker --version
   docker compose version
   ```

---

### Port 2121 Already in Use

**Symptoms:**
- "Bind for 0.0.0.0:2121 failed: port is already allocated"
- FTP server container fails to start

**Solutions:**

1. **Find process using port:**
   ```powershell
   netstat -ano | findstr :2121
   ```

2. **Stop conflicting process:**
   ```powershell
   # Find PID from above, then:
   taskkill /PID <pid> /F
   ```

3. **Check for existing containers:**
   ```bash
   docker ps -a | grep ftp
   docker rm -f $(docker ps -a -q --filter name=ftp)
   ```

4. **Use alternative port (modify docker-compose.yml):**
   ```yaml
   ports:
     - "2122:21"  # Changed from 2121
   ```

---

### Containers Start but Exit Immediately

**Symptoms:**
- `docker ps` shows containers as "Exited"
- Services become unavailable shortly after start

**Solutions:**

1. **Check container logs:**
   ```bash
   docker logs s9_ftp-server
   docker logs s9_client1
   ```

2. **Run container interactively:**
   ```bash
   docker compose run --rm ftp-server /bin/bash
   ```

3. **Check for missing dependencies:**
   ```bash
   docker compose build --no-cache
   ```

4. **Verify volume permissions:**
   ```bash
   docker volume ls
   docker volume inspect week9_wslkit_server-files
   ```

---

### Network Connectivity Issues

**Symptoms:**
- Containers cannot communicate with each other
- "Connection refused" from client to server

**Solutions:**

1. **Verify network exists:**
   ```bash
   docker network ls | grep week9
   ```

2. **Recreate network:**
   ```bash
   docker network rm week9_ftp_network
   docker compose up -d
   ```

3. **Check container IPs:**
   ```bash
   docker network inspect week9_ftp_network
   ```

4. **Test connectivity from inside container:**
   ```bash
   docker exec -it s9_client1 ping ftp-server
   docker exec -it s9_client1 nc -zv ftp-server 21
   ```

---

## FTP Issues

### Authentication Failures

**Symptoms:**
- "530 Login authentication failed"
- "530 Permission denied"

**Solutions:**

1. **Verify credentials:**
   - Default username: `test`
   - Default password: `12345`

2. **Check user configuration in server:**
   ```bash
   docker exec s9_ftp-server cat /etc/ftpusers
   ```

3. **Try anonymous login:**
   ```python
   ftp.login('anonymous', 'guest@example.com')
   ```

---

### Passive Mode Failures

**Symptoms:**
- "425 Can't open data connection"
- "227 Entering Passive Mode" followed by timeout
- File listing works but file transfer fails

**Solutions:**

1. **Verify passive port range is exposed:**
   ```yaml
   # docker-compose.yml
   ports:
     - "2121:21"
     - "60000-60010:60000-60010"
   ```

2. **Check firewall rules (PowerShell Admin):**
   ```powershell
   New-NetFirewallRule -DisplayName "FTP Passive" -Direction Inbound -Protocol TCP -LocalPort 60000-60010 -Action Allow
   ```

3. **Force active mode (if passive fails):**
   ```python
   ftp.set_pasv(False)
   ```

---

### Data Transfer Corruption

**Symptoms:**
- Downloaded files are corrupted
- Binary files (images, archives) appear damaged
- Text files have wrong line endings

**Solutions:**

1. **Use binary mode for non-text files:**
   ```python
   ftp.voidcmd('TYPE I')  # Binary mode
   # or
   ftp.retrbinary('RETR file.zip', f.write)
   ```

2. **Use ASCII mode for text files:**
   ```python
   ftp.voidcmd('TYPE A')  # ASCII mode
   # or
   ftp.retrlines('RETR file.txt', callback)
   ```

3. **Verify checksum after transfer:**
   ```python
   import hashlib
   local_hash = hashlib.md5(open('local.txt', 'rb').read()).hexdigest()
   ```

---

## Python Issues

### struct.error: unpack requires a buffer

**Symptoms:**
- "struct.error: unpack requires a buffer of X bytes"
- Unpacking fails with size mismatch

**Solutions:**

1. **Verify buffer size:**
   ```python
   expected = struct.calcsize(format_string)
   actual = len(buffer)
   if actual < expected:
       raise ValueError(f"Buffer too small: {actual} < {expected}")
   ```

2. **Handle partial reads:**
   ```python
   def recv_exactly(sock, n):
       data = b''
       while len(data) < n:
           chunk = sock.recv(n - len(data))
           if not chunk:
               raise ConnectionError("Connection closed")
           data += chunk
       return data
   ```

---

### Endianness Conversion Errors

**Symptoms:**
- Numbers appear incorrect after network transfer
- Values are byte-swapped

**Solutions:**

1. **Always use network byte order:**
   ```python
   # Sending
   data = struct.pack(">I", value)  # Big-endian
   
   # Receiving
   value = struct.unpack(">I", data)[0]
   ```

2. **Convert between host and network order:**
   ```python
   import socket
   
   # Host to network
   net_value = socket.htonl(host_value)
   
   # Network to host
   host_value = socket.ntohl(net_value)
   ```

---

### Import Errors

**Symptoms:**
- "ModuleNotFoundError: No module named 'X'"
- "ImportError: cannot import name 'Y'"

**Solutions:**

1. **Install missing packages:**
   ```powershell
   pip install -r setup/requirements.txt
   ```

2. **Verify Python version:**
   ```powershell
   python --version  # Should be 3.8+
   ```

3. **Check PYTHONPATH:**
   ```powershell
   $env:PYTHONPATH = "$PWD"
   python -c "import src.exercises.ex_9_01_endianness"
   ```

---

## Wireshark Issues

### Cannot Capture Docker Traffic

**Symptoms:**
- No packets visible in Wireshark
- Cannot see traffic between containers

**Solutions:**

1. **Capture from correct interface:**
   - Use "\\.\pipe\docker_engine" on Windows
   - Or capture inside container with tcpdump

2. **Capture inside container:**
   ```bash
   docker exec s9_ftp-server tcpdump -i eth0 -w /tmp/capture.pcap
   docker cp s9_ftp-server:/tmp/capture.pcap ./pcap/
   ```

3. **Use host network mode (for debugging only):**
   ```yaml
   network_mode: host
   ```

---

### Missing FTP Protocol Dissection

**Symptoms:**
- FTP traffic shows as generic TCP
- Commands not decoded

**Solutions:**

1. **Decode as FTP:**
   - Right-click packet > Decode As > FTP

2. **Check Wireshark preferences:**
   - Edit > Preferences > Protocols > FTP
   - Verify TCP port is set correctly

3. **Update Wireshark:**
   - Download latest version from wireshark.org

---

## WSL2 Issues

### WSL2 Not Available

**Symptoms:**
- "WSL 2 requires an update to its kernel component"
- "Please enable the Virtual Machine Platform"

**Solutions:**

1. **Enable required Windows features (PowerShell Admin):**
   ```powershell
   dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
   dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
   ```

2. **Install WSL2 kernel update:**
   - Download from: https://aka.ms/wsl2kernel

3. **Set WSL2 as default:**
   ```powershell
   wsl --set-default-version 2
   ```

4. **Restart computer after changes**

---

### WSL2 Performance Issues

**Symptoms:**
- Slow file access
- High memory usage

**Solutions:**

1. **Create .wslconfig (in %USERPROFILE%):**
   ```ini
   [wsl2]
   memory=4GB
   processors=2
   localhostForwarding=true
   ```

2. **Store files in Linux filesystem:**
   - Use `/home/user/` instead of `/mnt/c/`

3. **Restart WSL:**
   ```powershell
   wsl --shutdown
   ```

---

## Environment Reset

If all else fails, perform a complete reset:

```powershell
# 1. Stop everything
python scripts/stop_lab.py

# 2. Full cleanup
python scripts/cleanup.py --full --prune

# 3. Verify environment
python setup/verify_environment.py

# 4. Reinstall prerequisites
python setup/install_prerequisites.py

# 5. Fresh start
python scripts/start_lab.py --rebuild
```

---

## Getting Help

### Collect Diagnostic Information

```powershell
# Generate diagnostic report
python setup/verify_environment.py > diagnostic.txt
docker info >> diagnostic.txt
docker ps -a >> diagnostic.txt
docker logs s9_ftp-server >> diagnostic.txt 2>&1
```

### Resources

- **Course Materials:** docs/theory_summary.md
- **Command Reference:** docs/commands_cheatsheet.md
- **Docker Documentation:** https://docs.docker.com
- **Wireshark Documentation:** https://www.wireshark.org/docs/

---

*NETWORKING class - ASE, Informatics | by Revolvix*
