# Commands Cheatsheet

> Week 13: IoT and Security in Computer Networks  
> NETWORKING class - ASE, Informatics | by Revolvix

---

## Laboratory Management

### Starting the Environment
```powershell
# Full startup with service verification
python scripts/start_lab.py

# Check status only
python scripts/start_lab.py --status

# Rebuild containers before starting
python scripts/start_lab.py --rebuild
```

### Stopping the Environment
```powershell
# Graceful shutdown (preserves data)
python scripts/stop_lab.py

# Full cleanup (removes volumes)
python scripts/cleanup.py --full

# See what would be removed without removing
python scripts/cleanup.py --dry-run
```

---

## Docker Commands

### Container Management
```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# View container logs
docker logs week13_mosquitto
docker logs week13_dvwa
docker logs week13_vsftpd

# Follow logs in real-time
docker logs -f week13_mosquitto

# Execute command in container
docker exec -it week13_mosquitto sh
docker exec -it week13_dvwa bash

# Inspect container details
docker inspect week13_mosquitto
```

### Network Inspection
```bash
# List Docker networks
docker network ls

# Inspect week13 network
docker network inspect week13net

# View network connectivity
docker exec week13_mosquitto ping -c 2 10.0.13.11
```

### Resource Cleanup
```bash
# Remove week13 containers
docker rm -f $(docker ps -aq -f "name=week13")

# Remove week13 network
docker network rm week13net

# System-wide cleanup (use with caution)
docker system prune -a
```

---

## MQTT Commands

> 💭 **Before running:** What do you expect to see when subscribing to `#`? How will TLS traffic look different in Wireshark?

### Mosquitto Client Tools
```bash
# Subscribe to all topics
mosquitto_sub -h localhost -p 1883 -t "#" -v

# Subscribe with TLS
mosquitto_sub -h localhost -p 8883 --cafile docker/configs/certs/ca.crt -t "#" -v

# Publish a message
mosquitto_pub -h localhost -p 1883 -t "iot/sensor/temperature" -m "23.5"

# Publish with TLS
mosquitto_pub -h localhost -p 8883 --cafile docker/configs/certs/ca.crt -t "iot/sensor/temperature" -m "23.5"
```

### Python MQTT Client
```bash
# Subscribe mode
python src/exercises/ex_13_02_mqtt_client.py --mode subscribe --topic "iot/#"

# Publish mode
python src/exercises/ex_13_02_mqtt_client.py --mode publish --topic "iot/sensor/temp" --message "25.3"

# Using TLS
python src/exercises/ex_13_02_mqtt_client.py --mode subscribe --topic "#" --tls --cafile docker/configs/certs/ca.crt --port 8883
```

---

## Port Scanning

### Nmap (if installed)
```bash
# TCP connect scan
nmap -sT -p 1883,8883,8080,2121,6200 localhost

# Service version detection
nmap -sV -p 1883,8883,8080,2121 localhost

# Full scan with scripts
nmap -sT -sV -sC -p- localhost
```

### Python Port Scanner
```bash
# Scan localhost
python src/exercises/ex_13_01_port_scanner.py --target localhost --ports 1-10000

# Scan specific ports
python src/exercises/ex_13_01_port_scanner.py --target localhost --ports 1883,8883,8080,2121,6200

# Scan with banner grabbing
python src/exercises/ex_13_01_port_scanner.py --target localhost --ports 1883,8883,8080,2121 --banner

# Export results to JSON
python src/exercises/ex_13_01_port_scanner.py --target localhost --ports 1883,8883,8080,2121 -o artifacts/scan_results.json
```

### Netcat Port Checking
```bash
# Test single port
nc -zv localhost 1883

# Test with timeout
nc -zv -w 2 localhost 8080

# Banner grab
echo "" | nc -v localhost 2121
```

---

## Packet Capture

### tcpdump
```bash
# Capture MQTT traffic
tcpdump -i any port 1883 -w pcap/mqtt_traffic.pcap

# Capture with verbose output
tcpdump -i any port 1883 -v

# Capture specific host
tcpdump -i any host 10.0.13.100 -w pcap/mosquitto.pcap

# Read pcap file
tcpdump -r pcap/mqtt_traffic.pcap
```

### Capture Script
```powershell
# Default capture (all lab ports)
python scripts/capture_traffic.py --output pcap/week13_capture.pcap

# Custom duration
python scripts/capture_traffic.py --output pcap/capture.pcap --duration 60

# Custom filter
python scripts/capture_traffic.py --output pcap/mqtt_only.pcap --filter "tcp port 1883"
```

---

## Wireshark Filters

### MQTT Traffic
```
mqtt
tcp.port == 1883
mqtt.msgtype == 3  # PUBLISH messages
mqtt.topic contains "sensor"
```

### TLS Traffic
```
tls
tcp.port == 8883
tls.handshake.type == 1  # Client Hello
tls.handshake.type == 2  # Server Hello
```

### HTTP/DVWA Traffic
```
http
tcp.port == 8080
http.request.method == "POST"
http.request.uri contains "login"
```

### FTP Traffic
```
ftp
tcp.port == 2121
ftp.request.command == "USER"
ftp.response.code == 230  # Login successful
```

### Combined Lab Filter
```
tcp.port in {1883, 8883, 8080, 2121, 6200}
```

---

## Vulnerability Testing

### DVWA
```bash
# Access DVWA
curl http://localhost:8080

# Test SQL injection (example)
curl "http://localhost:8080/vulnerabilities/sqli/?id=1' OR '1'='1&Submit=Submit"

# Check security level
curl -c cookies.txt -b cookies.txt http://localhost:8080/security.php
```

### FTP Backdoor Detection
```bash
# Check vsftpd version
echo "USER anonymous" | nc localhost 2121

# Check backdoor port (should respond but not execute commands)
nc -v localhost 6200
```

### Python Vulnerability Checker
```bash
# Full vulnerability scan
python src/exercises/ex_13_04_vuln_checker.py --target localhost

# Check specific service
python src/exercises/ex_13_04_vuln_checker.py --target localhost --service dvwa
python src/exercises/ex_13_04_vuln_checker.py --target localhost --service mqtt
python src/exercises/ex_13_04_vuln_checker.py --target localhost --service ftp
```

---

## Testing

### Smoke Test
```powershell
python tests/smoke_test.py
```

### Full Test Suite
```powershell
# Environment tests
python -m pytest tests/test_environment.py -v

# Exercise tests
python tests/test_exercises.py

# Single exercise test
python tests/test_exercises.py --exercise 1
```

---

## Environment Variables

### Port Configuration (.env file)
```bash
MQTT_PLAIN_PORT=1883
MQTT_TLS_PORT=8883
DVWA_HOST_PORT=8080
VSFTPD_HOST_PORT=2121
VSFTPD_BACKDOOR_HOST_PORT=6200
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
