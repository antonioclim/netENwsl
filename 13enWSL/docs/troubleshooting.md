# Troubleshooting Guide

> Week 13: IoT and Security in Computer Networks  
> NETWORKING class - ASE, Informatics | by Revolvix

---

## Docker Issues

### Docker Desktop Not Running

**Symptoms:**
- "Cannot connect to the Docker daemon"
- "docker: command not found" (in WSL)
- Container commands fail silently

**Solutions:**
1. Start Docker Desktop from the Windows Start menu
2. Wait for the Docker icon in the system tray to show "Docker Desktop is running"
3. In WSL, verify with: `docker info`
4. If still failing, restart Docker Desktop

### Permission Denied on Docker Socket

**Symptoms:**
- "permission denied while trying to connect to the Docker daemon socket"

**Solutions:**
```bash
# In WSL, add user to docker group
sudo usermod -aG docker $USER

# Log out and back in, or run
newgrp docker
```

### Port Already in Use

**Symptoms:**
- "Bind for 0.0.0.0:1883 failed: port is already allocated"
- Container fails to start

**Solutions:**
1. Check what's using the port:
   ```powershell
   netstat -ano | findstr :1883
   ```

2. Stop the conflicting process, or

3. Change the port in `.env`:
   ```bash
   MQTT_PLAIN_PORT=11883
   ```

4. Restart with `python scripts/start_lab.py`

### Containers Not Starting

**Symptoms:**
- `docker ps` shows no containers
- Start script reports failures

**Solutions:**
1. Check Docker logs:
   ```bash
   docker logs week13_mosquitto 2>&1
   docker logs week13_dvwa 2>&1
   docker logs week13_vsftpd 2>&1
   ```

2. Rebuild images:
   ```bash
   python scripts/start_lab.py --rebuild
   ```

3. Full cleanup and restart:
   ```bash
   python scripts/cleanup.py --full
   python scripts/start_lab.py
   ```

### Docker Network Issues

**Symptoms:**
- Containers can't communicate with each other
- "network week13net not found"

**Solutions:**
```bash
# Remove and recreate network
docker network rm week13net
docker network create --subnet=10.0.13.0/24 week13net

# Or let docker-compose recreate it
python scripts/cleanup.py --full
python scripts/start_lab.py
```

---

## Certificate Issues

### TLS Connection Refused

**Symptoms:**
- MQTT TLS connection fails
- "SSL: CERTIFICATE_VERIFY_FAILED"
- "unable to get local issuer certificate"

**Solutions:**
1. Regenerate certificates:
   ```bash
   python setup/configure_docker.py
   ```

2. Verify certificates exist:
   ```bash
   ls -la docker/configs/certs/
   # Should show: ca.crt, server.crt, server.key
   ```

3. Check certificate validity:
   ```bash
   openssl x509 -in docker/configs/certs/ca.crt -text -noout | grep "Not After"
   ```

4. Use correct CA file path in client:
   ```bash
   python src/exercises/ex_13_02_mqtt_client.py --tls --cafile docker/configs/certs/ca.crt
   ```

### Certificate Expired

**Symptoms:**
- "certificate has expired"

**Solutions:**
```bash
# Regenerate certificates (valid for 365 days)
python setup/configure_docker.py

# Restart services to load new certificates
python scripts/stop_lab.py
python scripts/start_lab.py
```

---

## MQTT Issues

### Cannot Connect to MQTT Broker

**Symptoms:**
- "Connection refused"
- mosquitto_sub/pub hangs or times out

**Solutions:**
1. Verify container is running:
   ```bash
   docker ps | grep mosquitto
   ```

2. Check Mosquitto logs:
   ```bash
   docker logs week13_mosquitto
   ```

3. Test with netcat:
   ```bash
   nc -zv localhost 1883
   ```

4. Check firewall isn't blocking:
   ```powershell
   # Windows Firewall - allow port
   netsh advfirewall firewall add rule name="MQTT" dir=in action=allow protocol=TCP localport=1883
   ```

### No Messages Received

**Symptoms:**
- Subscriber shows no output
- Publisher appears to work but nothing received

**Solutions:**
1. Use wildcard subscription:
   ```bash
   mosquitto_sub -h localhost -p 1883 -t "#" -v
   ```

2. Verify topic spelling (case-sensitive)

3. Check QoS settings match between publisher and subscriber

---

## DVWA Issues

### DVWA Shows Blank Page

**Symptoms:**
- http://localhost:8080 loads but shows nothing
- PHP errors in browser

**Solutions:**
1. Wait longer for initialisation (up to 30 seconds)

2. Check container logs:
   ```bash
   docker logs week13_dvwa
   ```

3. Reset DVWA database:
   - Navigate to http://localhost:8080/setup.php
   - Click "Create / Reset Database"

### Cannot Login to DVWA

**Symptoms:**
- Login page loads but credentials don't work

**Solutions:**
- Default credentials: `admin` / `password`
- If changed, reset the database via setup.php

---

## FTP Issues

### Cannot Connect to FTP

**Symptoms:**
- FTP client times out
- "Connection refused" on port 2121

**Solutions:**
1. Verify container is running:
   ```bash
   docker ps | grep vsftpd
   ```

2. Test with netcat:
   ```bash
   nc -v localhost 2121
   ```

3. Check container logs:
   ```bash
   docker logs week13_vsftpd
   ```

### Backdoor Port Not Responding

**Symptoms:**
- Port 6200 not accepting connections

**Solutions:**
This is expected behaviour in some configurations. The backdoor stub may only respond after specific trigger conditions. This is intentional for educational purposes.

---

## Python Issues

### Module Not Found

**Symptoms:**
- "ModuleNotFoundError: No module named 'paho'"
- Import errors for required packages

**Solutions:**
```bash
# Install all requirements
pip install -r setup/requirements.txt

# Or install individually
pip install paho-mqtt scapy requests docker pyyaml
```

### Scapy Permission Errors

**Symptoms:**
- "Operation not permitted" when using scapy
- Packet capture fails

**Solutions:**
```bash
# Run with elevated privileges
sudo python src/exercises/ex_13_03_packet_sniffer.py

# Or use tcpdump instead for capture
python scripts/capture_traffic.py
```

### Python Version Too Old

**Symptoms:**
- Syntax errors on valid code
- "f-string" related errors

**Solutions:**
1. Check Python version:
   ```bash
   python --version
   ```

2. Install Python 3.11+:
   - Windows: Download from python.org
   - WSL: `sudo apt install python3.11`

3. Use correct Python command:
   ```bash
   python3.11 scripts/start_lab.py
   ```

---

## Network Issues

### WSL2 Network Isolation

**Symptoms:**
- Can access services from WSL but not from Windows
- localhost works in WSL but not in browser

**Solutions:**
1. Use Windows localhost (Docker Desktop handles port forwarding)

2. Check WSL2 IP:
   ```bash
   # In WSL
   ip addr show eth0
   ```

3. Access via WSL IP from Windows:
   ```
   http://<WSL_IP>:8080
   ```

### Wireshark Can't See Traffic

**Symptoms:**
- No packets captured
- Wrong interface selected

**Solutions:**
1. Select correct interface:
   - For Docker traffic: "\\.\pipe\docker_engine" or "Npcap Loopback Adapter"
   - For WSL traffic: The adapter labelled "vEthernet (WSL)"

2. Run Wireshark as Administrator

3. Use capture script instead:
   ```bash
   python scripts/capture_traffic.py --output pcap/capture.pcap
   ```

---

## Cleanup Issues

### Resources Not Fully Removed

**Symptoms:**
- Old containers/networks persist
- Disk space not freed

**Solutions:**
```bash
# Full cleanup
python scripts/cleanup.py --full --prune

# Manual cleanup
docker stop $(docker ps -aq -f "name=week13")
docker rm $(docker ps -aq -f "name=week13")
docker network rm week13net
docker volume rm $(docker volume ls -q -f "name=week13")

# System-wide prune (careful!)
docker system prune -a --volumes
```

---

## Getting Help

If issues persist:

1. Run the environment verification:
   ```bash
   python setup/verify_environment.py
   ```

2. Collect diagnostic information:
   ```bash
   docker version
   docker info
   docker ps -a
   docker logs week13_mosquitto 2>&1 > mqtt_logs.txt
   ```

3. Check the course forum or contact the teaching assistant with:
   - Error messages
   - Steps to reproduce
   - Diagnostic output

---

*NETWORKING class - ASE, Informatics | by Revolvix*
