# Troubleshooting Guide: Week 7

> NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

---

## Docker Issues

### Docker Desktop Not Running

**Symptom:** Commands fail with "Cannot connect to the Docker daemon"

This is the single most common issue I see in lab sessions. After a Windows update, Docker often needs a manual restart even if WSL appears to be running normally.

**Solution:**
1. Open Docker Desktop application
2. Wait for the whale icon to show "running" status
3. Verify with: `docker info`

### Containers Fail to Start

**Symptom:** `docker compose up` exits with errors

**Diagnosis:**
```bash
# Check logs for specific service
docker compose logs tcp_server

# Check if ports are in use
netstat -tuln | grep -E '9090|9091|8888'

# On Windows PowerShell
Get-NetTCPConnection -LocalPort 9090
```

**Common causes:**
- Port already in use by another application
- Insufficient memory allocated to Docker
- Previous containers not cleaned up

**Solution:**
```bash
# Full cleanup
python scripts/cleanup.py --full

# Then restart
python scripts/start_lab.py
```

### Network Creation Fails

**Symptom:** "network week7net already exists"

**Solution:**
```bash
docker network rm week7net
python scripts/start_lab.py
```

---

## Capture Issues

### Wireshark Cannot See Traffic

**Symptom:** Wireshark shows no packets when containers are active

In previous lab sessions, roughly half the students initially captured on the wrong interface. If you see zero packets, that's almost certainly the problem — switch to vEthernet (WSL) on Windows or the Docker bridge interface on Linux.

**Cause:** Docker uses internal bridge networks not visible to host interfaces

**Solution options:**

1. **Capture on Docker network bridge:**
   ```bash
   # Find bridge interface
   docker network inspect week7net | grep "com.docker.network.bridge.name"
   # Capture on that interface
   sudo tcpdump -i br-xxxxx -w capture.pcap
   ```

2. **Capture inside container:**
   ```bash
   docker exec -it week7_tcp_server tcpdump -w /tmp/capture.pcap
   docker cp week7_tcp_server:/tmp/capture.pcap ./pcap/
   ```

3. **Use script helper:**
   ```bash
   python scripts/capture_traffic.py --interface docker0
   ```

### Permission Denied on Capture

**Symptom:** tcpdump or tshark fails with permission error

**Solution (Linux/WSL):**
```bash
# Add user to wireshark group
sudo usermod -aG wireshark $USER

# Or run with sudo
sudo tcpdump -i eth0
```

### Empty Capture File

**Symptom:** capture.pcap has zero packets

**Diagnosis:**
- Verify capture started before traffic was generated
- Check interface name is correct
- Confirm filter syntax is valid

Nine times out of ten, the interface selection is wrong. Always check that first.

**Common mistakes:**
```bash
# Wrong: filter might be too restrictive
tcpdump -i eth0 'tcp port 9090 and host 10.0.7.100'

# Right: start broad, then narrow
tcpdump -i eth0 port 9090
```

---

## TCP Connection Issues

### Connection Refused

**Symptom:** TCP client gets "Connection refused"

**Meaning:** Port is closed (no service listening) or REJECT rule matched

**Diagnosis:**
```bash
# Check if server is running
docker ps | grep tcp_server

# Check if port is listening inside container
docker exec week7_tcp_server netstat -tuln
```

### Connection Timeout

**Symptom:** TCP client hangs, eventually times out

**Meaning:** DROP rule matched or network unreachable

When debugging connection problems, I recommend using REJECT during development. The immediate feedback saves considerable time compared to waiting for timeouts.

**Diagnosis:**
```bash
# Check firewall rules
sudo iptables -L -n

# Check routing
ip route

# Try ICMP
ping -c 1 10.0.7.100
```

### Connection Resets

**Symptom:** Connection established then immediately reset

**Possible causes:**
- Server crashed after accepting connection
- REJECT rule applied mid-connection
- Application error

**Diagnosis:**
```bash
# Capture and look for RST
tcpdump -i eth0 'tcp[tcpflags] & tcp-rst != 0'
```

---

## UDP Issues

### UDP Messages Not Received

**Symptom:** Sender shows success but receiver shows nothing

This trips up students every semester. Remember: UDP success at the sender only means "handed to the network stack", not "delivered to receiver".

**Diagnosis steps:**

1. **Verify receiver started first:**
   ```bash
   # Start receiver
   docker compose up udp_receiver
   # Then send
   python src/apps/udp_sender.py
   ```

2. **Check IP and port:**
   ```bash
   docker inspect week7_udp_receiver | grep IPAddress
   ```

3. **Check firewall:**
   ```bash
   sudo iptables -L -n | grep 9091
   ```

4. **Capture to verify packets:**
   ```bash
   tcpdump -i docker0 udp port 9091
   ```

---

## Firewall Rule Issues

### Rules Don't Take Effect

**Symptom:** Connections succeed despite block rules

**Diagnosis:**
```bash
# Verify rules are in correct chain
sudo iptables -L INPUT -n --line-numbers

# Check rule order (first match wins)
sudo iptables -L -n -v

# Check packet counters (are packets hitting the rule?)
sudo iptables -L -n -v | grep 9090
```

**Common mistakes:**
- Rule in wrong chain (OUTPUT vs INPUT vs FORWARD)
- Rule order wrong (ACCEPT rule before DROP)
- Wrong interface specified

### REJECT Not Showing ICMP

**Symptom:** Used REJECT but no ICMP response visible

**Possible causes:**
- ICMP filtered by another rule
- ICMP rate-limited
- Capture filter excludes ICMP

**Solution:**
```bash
# Capture all traffic, not just TCP
tcpdump -i eth0 -w all.pcap

# Then filter in Wireshark
# Display filter: icmp.type == 3
```

---

## Port Probe Issues

### All Ports Show Filtered

**Symptom:** Port probe returns "filtered" for all ports

**Causes:**
- Network connectivity issue
- Default DROP policy
- Wrong target IP

**Diagnosis:**
```bash
# Verify target is reachable
ping -c 1 10.0.7.100

# Check routing
traceroute 10.0.7.100

# Try direct connection
nc -zv 10.0.7.100 9090
```

### Probe Takes Too Long

**Symptom:** Scanning is extremely slow

**Cause:** DROP rules cause timeout waiting for responses

**Solution:**
```bash
# Reduce timeout
python src/apps/port_probe.py --timeout 1

# Or scan fewer ports
python src/apps/port_probe.py --ports 9090,9091
```

---

## WSL-Specific Issues

### Cannot Access Docker from WSL

**Symptom:** docker commands fail in WSL

This usually breaks when Docker Desktop has been updated but WSL integration wasn't re-enabled automatically.

**Solution:**
1. Ensure Docker Desktop has "Use WSL 2 based engine" enabled
2. In Docker Settings > Resources > WSL Integration, enable your distro
3. Restart WSL: `wsl --shutdown` then reopen

### Wireshark Cannot Capture

**Symptom:** Wireshark on Windows cannot see WSL traffic

**Solution:**
Capture inside WSL using tcpdump, then open the pcap file in Windows Wireshark:
```bash
# In WSL
sudo tcpdump -i eth0 -w /mnt/c/Users/YourName/capture.pcap
# Then open in Windows Wireshark
```

---

## General Debugging Strategy

If you're stuck, work through this sequence systematically:

1. **Isolate the problem:** Is it network, firewall, application or configuration?

2. **Start simple:** Can you ping? Can you connect without firewall?

3. **Capture everything:** Broad capture first, filter later

4. **Check both ends:** Verify both client and server perspectives

5. **Compare expected vs actual:** What packets should you see vs what do you see?

6. **Read error messages:** They usually tell you exactly what's wrong

If this feels overwhelming at first, focus on steps 2 and 3. Most problems become obvious once you have a packet capture to examine.

---

*NETWORKING class — ASE, Informatics | by ing. dr. Antonio Clim*
