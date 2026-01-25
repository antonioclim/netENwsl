# 🔧 Troubleshooting Guide — Week 10
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> HTTP/HTTPS, REST Architecture and Network Services

---

## Quick Diagnostic Commands

```bash
# Check if Docker is running
docker ps

# Check all Week 10 containers
docker ps --filter "name=week10"

# View container logs
docker logs week10_web
docker logs week10_dns
docker logs week10_ssh
docker logs week10_ftp

# Check port availability
netstat -tlnp | grep -E "(8000|5353|2222|2121)"
ss -tlnp | grep -E "(8000|5353|2222|2121)"

# Test connectivity
curl http://localhost:8000/
dig @127.0.0.1 -p 5353 web.lab.local +short
nc -zv localhost 2222
nc -zv localhost 2121
```

---

## HTTP/HTTPS Issues

### Problem: "Connection refused" on port 8000

**Symptoms:**
```
curl: (7) Failed to connect to localhost port 8000: Connection refused
```

**Diagnosis:**
```bash
# Check if web container is running
docker ps | grep week10_web

# Check container logs
docker logs week10_web
```

**Solutions:**

1. **Container not running:**
   ```bash
   cd /mnt/d/NETWORKING/WEEK10/10enWSL
   docker compose -f docker/docker-compose.yml up -d web
   ```

2. **Port already in use:**
   ```bash
   # Find what's using port 8000
   sudo lsof -i :8000
   # Kill the process or use different port
   ```

3. **Docker not running:**
   ```bash
   sudo service docker start
   ```

> 💡 **From experience:** In previous years, students often forgot to start Docker after rebooting WSL. If you see "Cannot connect to Docker daemon", run `sudo service docker start` first.

---

### Problem: Certificate errors with HTTPS

**Symptoms:**
```
curl: (60) SSL certificate problem: self-signed certificate
```

**Solutions:**

1. **For testing (skip verification):**
   ```bash
   curl -k https://127.0.0.1:8443/
   ```

2. **Use the generated certificate:**
   ```bash
   curl --cacert output/tls/server.crt https://127.0.0.1:8443/
   ```

3. **Regenerate certificate:**
   ```bash
   rm -f output/tls/server.crt output/tls/server.key
   python3 src/exercises/ex_10_01_tls_rest_crud.py generate-cert
   ```

---

### Problem: SSL verification fails in Python requests

**Symptoms:**
```python
requests.exceptions.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED]
```

**Solutions:**

1. **Disable verification for local testing:**
   ```python
   import requests
   import urllib3
   urllib3.disable_warnings()
   
   response = requests.get("https://127.0.0.1:8443/", verify=False)
   ```

2. **Point to the certificate:**
   ```python
   response = requests.get(
       "https://127.0.0.1:8443/",
       verify="output/tls/server.crt"
   )
   ```

> ⚠️ **This usually breaks when:** students copy the certificate path but the current working directory is different. Always use absolute paths or Path objects for reliability.

---

### Problem: "400 Bad Request" or "Invalid JSON"

**Symptoms:**
```json
{"error": "Invalid JSON: ..."}
```

**Solutions:**

1. **Check Content-Type header:**
   ```bash
   curl -X POST http://localhost:8000/api/resources \
     -H "Content-Type: application/json" \
     -d '{"name": "test", "value": 1}'
   ```

2. **Validate JSON syntax:**
   ```bash
   echo '{"name": "test", "value": 1}' | jq .
   ```

3. **Common JSON mistakes:**
   - Single quotes instead of double quotes
   - Trailing commas
   - Missing quotes around keys

---

## DNS Issues

### Problem: DNS queries timeout

**Symptoms:**
```
;; connection timed out; no servers could be reached
```

**Diagnosis:**
```bash
# Check if DNS container is running
docker ps | grep week10_dns

# Check container logs
docker logs week10_dns

# Test UDP connectivity
nc -u -zv 127.0.0.1 5353
```

**Solutions:**

1. **Container not running:**
   ```bash
   docker compose -f docker/docker-compose.yml up -d dns-server
   ```

2. **Wrong port or server:**
   ```bash
   # Correct syntax
   dig @127.0.0.1 -p 5353 web.lab.local
   
   # NOT this (wrong port syntax)
   dig @127.0.0.1:5353 web.lab.local
   ```

3. **Firewall blocking UDP:**
   ```bash
   # Check Windows Firewall for UDP 5353
   # Or test from inside Docker network:
   docker exec week10_debug dig @dns-server -p 5353 web.lab.local
   ```

> 💡 **Teaching note:** DNS resolution works in terminal but not in container? Check if you are using the container's DNS server name (`dns-server`) vs the host's loopback (`127.0.0.1`).

---

### Problem: "NXDOMAIN" or "Name not found"

**Symptoms:**
```
;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN
```

**Solutions:**

1. **Check exact domain spelling:**
   ```bash
   # Correct domains for lab:
   dig @127.0.0.1 -p 5353 web.lab.local
   dig @127.0.0.1 -p 5353 myservice.lab.local
   dig @127.0.0.1 -p 5353 api.lab.local
   ```

2. **List available domains:**
   ```bash
   # Check dns_server.py for configured records
   docker exec week10_dns cat /app/dns_server.py | grep -A5 "RECORDS"
   ```

---

## SSH Issues

### Problem: "Connection refused" on port 2222

**Symptoms:**
```
ssh: connect to host localhost port 2222: Connection refused
```

**Diagnosis:**
```bash
docker ps | grep week10_ssh
docker logs week10_ssh
```

**Solutions:**

1. **Container not running:**
   ```bash
   docker compose -f docker/docker-compose.yml up -d ssh-server
   ```

2. **SSH service not started inside container:**
   ```bash
   docker exec week10_ssh service ssh status
   docker exec week10_ssh service ssh start
   ```

---

### Problem: "Permission denied" or wrong password

**Symptoms:**
```
labuser@localhost: Permission denied (publickey,password).
```

**Solutions:**

1. **Correct credentials:**
   ```bash
   # Lab SSH server credentials:
   # User: labuser
   # Password: labpass
   ssh -p 2222 labuser@localhost
   ```

2. **Host key changed:**
   ```bash
   # Remove old host key
   ssh-keygen -R "[localhost]:2222"
   # Then reconnect
   ssh -p 2222 labuser@localhost
   ```

3. **Force password authentication:**
   ```bash
   ssh -p 2222 -o PreferredAuthentications=password labuser@localhost
   ```

---

### Problem: "Host key verification failed"

**Symptoms:**
```
WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!
```

**Solution:**
```bash
# Remove the old key
ssh-keygen -R "[localhost]:2222"

# Or for lab environment only (insecure!):
ssh -p 2222 -o StrictHostKeyChecking=no labuser@localhost
```

---

## FTP Issues

### Problem: "Connection refused" on port 2121

**Diagnosis:**
```bash
docker ps | grep week10_ftp
docker logs week10_ftp
```

**Solutions:**

1. **Container not running:**
   ```bash
   docker compose -f docker/docker-compose.yml up -d ftp-server
   ```

2. **Service not started:**
   ```bash
   docker exec week10_ftp ps aux | grep ftp
   ```

---

### Problem: Passive mode data connection fails

**Symptoms:**
```
ftp> ls
227 Entering Passive Mode (...)
ftp: Can't connect to `...': Connection timed out
```

**Solutions:**

1. **Check passive port range is mapped:**
   ```bash
   docker ps --format "{{.Ports}}" | grep week10_ftp
   # Should show: 30000-30009->30000-30009/tcp
   ```

2. **Check Windows Firewall:**
   - Allow inbound TCP 30000-30009

3. **Use active mode (if possible):**
   ```bash
   ftp localhost 2121
   ftp> passive
   Passive mode: off
   ftp> ls
   ```

> 💡 **This often confuses students:** FTP passive mode requires additional ports beyond 2121. If the data channel times out, check that ports 30000-30009 are mapped in docker-compose.yml.

---

### Problem: "530 Login incorrect"

**Solution:**
```bash
# Correct FTP credentials:
# User: labftp
# Password: labftp

ftp -p localhost 2121
# Enter: labftp
# Password: labftp
```

---

## Docker Issues

### Problem: "Cannot connect to Docker daemon"

**Solutions:**

1. **Start Docker service:**
   ```bash
   sudo service docker start
   ```

2. **Add user to docker group:**
   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```

---

### Problem: Container starts but immediately exits

**Diagnosis:**
```bash
docker ps -a | grep week10
docker logs week10_<container_name>
```

**Common causes:**
- Missing dependencies in Dockerfile
- Syntax error in startup script
- Port already in use

---

### Problem: Container starts but port not accessible

**Symptoms:**
- Container shows as "Up" in `docker ps`
- But `curl localhost:PORT` times out or refuses connection

**Diagnosis:**
```bash
# Check what ports the container is actually listening on
docker exec week10_web ss -tlnp

# Check port mapping
docker port week10_web

# Check if the service inside container is running
docker exec week10_web ps aux
```

**Solutions:**

1. **Service not bound to 0.0.0.0:**
   ```bash
   # Bad: only accessible from inside container
   flask run --host=127.0.0.1
   
   # Good: accessible from outside container
   flask run --host=0.0.0.0
   ```

2. **Check Dockerfile EXPOSE matches compose ports:**
   ```yaml
   # docker-compose.yml
   ports:
     - "8000:8000"  # host:container must match
   ```

> 💡 **If this feels confusing:** remember that `127.0.0.1` inside a container is different from `127.0.0.1` on the host. Services must bind to `0.0.0.0` to be reachable.

---

### Problem: "Port already in use"

**Diagnosis:**
```bash
sudo netstat -tlnp | grep <port>
# or
sudo ss -tlnp | grep <port>
```

**Solutions:**

1. **Stop conflicting service:**
   ```bash
   # Find PID using the port
   sudo lsof -i :<port>
   # Kill the process
   kill <PID>
   ```

2. **Stop old containers:**
   ```bash
   docker compose -f docker/docker-compose.yml down
   docker compose -f docker/docker-compose.yml up -d
   ```

---

## Wireshark Issues

### Problem: No packets captured

**Checklist:**
- [ ] Correct interface selected? Use `vEthernet (WSL)` for Docker traffic
- [ ] Capture started BEFORE generating traffic?
- [ ] Display filter not hiding packets? Try clearing the filter
- [ ] Promiscuous mode enabled?

**Solutions:**

1. **Select correct interface:**
   - For Docker containers: `vEthernet (WSL)`
   - For localhost only: `Loopback Adapter`

2. **Clear display filter:**
   - Remove any text from the filter bar
   - Press Enter

3. **Run as Administrator:**
   - Right-click Wireshark → Run as administrator

---

### Problem: "No interfaces found"

**Solutions:**

1. **Reinstall Npcap:**
   - Download from npcap.com
   - Enable "WinPcap API-compatible Mode"
   - Enable "Support raw 802.11 traffic"

2. **Run as Administrator**

---

## Exercise-Specific Issues

### HTTPS Exercise (ex_10_01_tls_rest_crud.py)

**Problem:** OpenSSL not found
```bash
# Install OpenSSL
sudo apt update && sudo apt install openssl
```

**Problem:** requests module not installed
```bash
pip3 install requests --break-system-packages
```

---

### REST Exercise (ex_10_02_richardson_maturity.py)

**Problem:** Flask not installed
```bash
pip3 install flask --break-system-packages
```

**Problem:** Port 5000 already in use
```bash
# Use different port
python3 src/exercises/ex_10_02_richardson_maturity.py serve --port 5001
```

---

### DNS Exercise (ex_10_03_dns_query_analysis.py)

**Problem:** dnslib not installed
```bash
pip3 install dnslib --break-system-packages
```

**Problem:** DNS server not responding
```bash
# Check if the lab DNS container is running
docker ps | grep week10_dns

# Start it if needed
docker compose -f docker/docker-compose.yml up -d dns-server
```

---

## General Debugging Steps

1. **Check container status:**
   ```bash
   docker ps -a --filter "name=week10"
   ```

2. **Check container logs:**
   ```bash
   docker logs <container_name>
   ```

3. **Enter container for debugging:**
   ```bash
   docker exec -it <container_name> bash
   ```

4. **Check network connectivity:**
   ```bash
   docker exec week10_debug ping web
   docker exec week10_debug curl http://web:8000/
   ```

5. **Restart everything:**
   ```bash
   docker compose -f docker/docker-compose.yml down
   docker compose -f docker/docker-compose.yml up -d
   ```

---

## Getting Help

If none of the above solutions work:

1. **Collect diagnostic information:**
   ```bash
   docker ps -a
   docker logs week10_web 2>&1 | tail -50
   docker logs week10_dns 2>&1 | tail -50
   docker network ls
   docker network inspect week10_labnet
   ```

2. **Check the error message carefully** — it often contains the solution

3. **Open an issue in GitHub** with:
   - Exact error message
   - Command you ran
   - Diagnostic output from above

---

*Computer Networks — Week 10 | ASE, CSIE Bucharest*
*Troubleshooting guide by ing. dr. Antonio Clim*
