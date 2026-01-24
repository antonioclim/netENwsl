# Commands Cheatsheet

> NETWORKING class — ASE, CSIE | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim
>
> Week 14: Integrated Recap and Project Evaluation

A quick reference guide for commands used throughout the Computer Networks course, with emphasis on Week 14's integrated laboratory.

💭 **SELF-CHECK:** Before looking up a command, try to recall it from memory. Use this cheatsheet to verify your answer.

---

## Table of Contents

1. [Laboratory Management](#laboratory-management)
2. [Docker Commands](#docker-commands)
3. [Network Analysis](#network-analysis)
4. [HTTP Testing](#http-testing)
5. [TCP/Socket Testing](#tcpsocket-testing)
6. [Python Utilities](#python-utilities)
7. [Troubleshooting Commands](#troubleshooting-commands)

---

## Laboratory Management

### Starting the Lab

```powershell
# Verify prerequisites
python setup/verify_environment.py

# Start all services
python scripts/start_lab.py

# Start with rebuild (fresh images)
python scripts/start_lab.py --rebuild

# Check status only
python scripts/start_lab.py --status
```

### Stopping the Lab

```powershell
# Graceful shutdown (preserves data)
python scripts/stop_lab.py

# Full cleanup (removes everything)
python scripts/cleanup.py --full

# Cleanup with system prune
python scripts/cleanup.py --full --prune
```

### Running Tests

```powershell
# Quick smoke test
python tests/smoke_test.py

# All exercises
python tests/test_exercises.py --all

# Specific exercise
python tests/test_exercises.py --exercise 2

# Environment tests
python tests/test_environment.py
```

### Demonstrations

```powershell
# Full system demo
python scripts/run_demo.py --demo full

# Failover demonstration
python scripts/run_demo.py --demo failover

# Traffic generation
python scripts/run_demo.py --demo traffic
```

---

## Docker Commands

### Container Management

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Start container
docker start <container_name>

# Stop container
docker stop <container_name>

# Restart container
docker restart <container_name>

# Remove container
docker rm <container_name>

# Force remove running container
docker rm -f <container_name>
```

### Container Inspection

```bash
# View container logs
docker logs <container_name>

# Follow logs in real-time
docker logs -f <container_name>

# Show last 50 lines
docker logs --tail 50 <container_name>

# Container details
docker inspect <container_name>

# Container IP address
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_name>

# Container resource usage
docker stats <container_name>
```

### Execute Commands in Containers

```bash
# Interactive shell
docker exec -it <container_name> bash

# Run single command
docker exec <container_name> <command>

# Examples for Week 14:
docker exec week14_client curl http://lb:8080/
docker exec week14_app1 cat /app/backend_server.py
docker exec week14_lb ping -c 3 app1
```

### Docker Compose

```bash
# Start services (detached)
docker compose up -d

# Start services (foreground)
docker compose up

# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v

# Rebuild and start
docker compose up --build -d

# View service logs
docker compose logs

# Follow specific service logs
docker compose logs -f lb

# Scale service (if applicable)
docker compose up -d --scale app=3
```

### Network Management

```bash
# List networks
docker network ls

# Inspect network
docker network inspect <network_name>

# Create network
docker network create <network_name>

# Remove network
docker network rm <network_name>

# Connect container to network
docker network connect <network_name> <container_name>

# Disconnect container from network
docker network disconnect <network_name> <container_name>

# Week 14 networks:
docker network inspect week14_backend_net
docker network inspect week14_frontend_net
```

### Image Management

```bash
# List images
docker images

# Remove image
docker rmi <image_name>

# Build image
docker build -t <tag> .

# Pull image
docker pull <image_name>

# Remove unused images
docker image prune
```

### System Commands

```bash
# Disk usage
docker system df

# Detailed disk usage
docker system df -v

# Clean unused resources
docker system prune

# Clean everything (including volumes)
docker system prune -a --volumes

# Docker info
docker info

# Docker version
docker version
```

---

## Network Analysis

### Wireshark

```powershell
# Start Wireshark (Windows)
& "C:\Program Files\Wireshark\Wireshark.exe"

# Open specific capture file
wireshark pcap/demo.pcap
```

### tshark (Command-line)

```bash
# Capture to file
tshark -i any -w output.pcap

# Capture with duration limit
tshark -i any -a duration:30 -w output.pcap

# Capture with filter
tshark -i any -f "port 8080" -w http.pcap

# Read capture file
tshark -r capture.pcap

# Apply display filter
tshark -r capture.pcap -Y "http"

# Show specific fields
tshark -r capture.pcap -Y "http.request" -T fields -e ip.src -e http.host -e http.request.uri

# Statistics - protocol hierarchy
tshark -r capture.pcap -q -z io,phs

# Statistics - conversations
tshark -r capture.pcap -q -z conv,tcp

# Statistics - endpoints
tshark -r capture.pcap -q -z endpoints,tcp

# Follow TCP stream
tshark -r capture.pcap -q -z follow,tcp,ascii,0
```

### tcpdump

```bash
# Basic capture
tcpdump -i any

# Capture specific port
tcpdump -i any port 8080

# Capture with verbose output
tcpdump -i any -v port 8080

# Write to file
tcpdump -i any -w capture.pcap

# Read from file
tcpdump -r capture.pcap

# Capture HTTP traffic
tcpdump -i any -A port 80

# Capture specific host
tcpdump -i any host 172.20.0.2

# Capture TCP flags
tcpdump -i any 'tcp[tcpflags] & tcp-syn != 0'
```

### Wireshark Display Filters

```
# HTTP traffic
http

# HTTP requests
http.request

# HTTP responses
http.response

# Specific HTTP method
http.request.method == "GET"
http.request.method == "POST"

# HTTP status codes
http.response.code == 200
http.response.code >= 400

# TCP port
tcp.port == 8080

# TCP flags
tcp.flags.syn == 1
tcp.flags.fin == 1
tcp.flags.reset == 1

# IP address
ip.addr == 172.20.0.2
ip.src == 172.20.0.2
ip.dst == 172.20.0.3

# Week 14 specific
tcp.port in {8080, 8001, 8002, 9000}
```

### Wireshark Capture Filters

```
# Port
port 8080

# Host
host 172.20.0.2

# Network
net 172.20.0.0/24

# TCP only
tcp

# Exclude port
not port 22

# Combined
tcp and port 8080 and host 172.20.0.2
```

---

## HTTP Testing

### curl

```bash
# Basic GET request
curl http://localhost:8080/

# Verbose output (headers)
curl -v http://localhost:8080/

# Show only headers
curl -I http://localhost:8080/

# POST request with data
curl -X POST -d "key=value" http://localhost:8080/

# POST with JSON
curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' http://localhost:8080/

# Follow redirects
curl -L http://localhost:8080/

# Custom headers
curl -H "X-Custom: value" http://localhost:8080/

# Save response to file
curl -o response.txt http://localhost:8080/

# Timing information
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8080/

# Multiple requests
for i in {1..10}; do curl -s http://localhost:8080/; done
```

### wget

```bash
# Download file
wget http://localhost:8080/file.txt

# Quiet mode
wget -q http://localhost:8080/

# Output to stdout
wget -qO- http://localhost:8080/

# Save with different name
wget -O output.txt http://localhost:8080/
```

### httpie (if installed)

```bash
# GET request
http localhost:8080/

# POST request
http POST localhost:8080/ key=value

# Headers
http localhost:8080/ X-Custom:value

# Verbose
http -v localhost:8080/
```

---

## TCP/Socket Testing

### netcat (nc)

```bash
# Connect to TCP server
nc localhost 9000

# Send data and receive response
echo "Hello" | nc localhost 9000

# Listen on port
nc -l 9000

# Port scan
nc -zv localhost 8080

# UDP mode
nc -u localhost 9000

# Verbose
nc -v localhost 9000

# Timeout
nc -w 5 localhost 9000
```

### telnet

```bash
# Connect to server
telnet localhost 9000

# HTTP request via telnet
telnet localhost 8080
# Then type:
GET / HTTP/1.1
Host: localhost
# Press Enter twice
```

### Python Socket Testing

```python
# Simple TCP client
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 9000))
s.send(b'Hello\n')
print(s.recv(1024))
s.close()

# Simple TCP server
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 9000))
s.listen(1)
conn, addr = s.accept()
print(f'Connected by {addr}')
data = conn.recv(1024)
conn.sendall(data)
conn.close()
```

---

## Python Utilities

### Running Python Scripts

```powershell
# Run script
python script.py

# Run with arguments
python script.py --arg value

# Run module
python -m module_name

# Interactive mode
python -i script.py

# Check syntax only
python -m py_compile script.py
```

### Package Management

```powershell
# Install package
pip install package_name

# Install from requirements
pip install -r requirements.txt

# List installed
pip list

# Show package info
pip show package_name

# Upgrade package
pip install --upgrade package_name
```

### Week 14 Exercises

```powershell
# Exercise 1: Review Quiz
python src/exercises/ex_14_01.py --mode quiz

# Exercise 2: Verification Harness
python src/exercises/ex_14_02.py

# Exercise 3: Advanced Challenges
python src/exercises/ex_14_03.py
```

---

## Troubleshooting Commands

### Port Checking

```powershell
# Windows - find process on port
netstat -ano | findstr :8080

# Kill process by PID
taskkill /PID <pid> /F

# Linux/WSL - find process on port
lsof -i :8080
netstat -tulpn | grep 8080

# Kill process
kill -9 <pid>
```

### Docker Troubleshooting

```bash
# Check container logs
docker logs week14_lb --tail 100

# Check container health
docker inspect --format='{{.State.Health.Status}}' week14_app1

# Check container processes
docker top week14_app1

# Copy files from container
docker cp week14_app1:/app/file.txt ./file.txt

# Check Docker events
docker events --since 1h

# Check Docker daemon logs (Windows)
# Event Viewer > Application and Services Logs > Docker
```

### Network Troubleshooting

```bash
# Ping from container
docker exec week14_client ping -c 3 app1

# DNS resolution in container
docker exec week14_client nslookup app1

# Check routes in container
docker exec week14_client ip route

# Check network interfaces
docker exec week14_client ip addr

# Test connectivity
docker exec week14_client curl -v http://app1:8001/
```

### WSL Troubleshooting

```powershell
# WSL status
wsl --status

# List distributions
wsl -l -v

# Shutdown WSL
wsl --shutdown

# Restart distribution
wsl -t <distro_name>

# Check WSL version
wsl --version
```

---

## Quick Reference Card

| Action | Command |
|--------|---------|
| Start lab | `python scripts/start_lab.py` |
| Stop lab | `python scripts/stop_lab.py` |
| Full cleanup | `python scripts/cleanup.py --full` |
| Smoke test | `python tests/smoke_test.py` |
| View logs | `docker logs week14_lb -f` |
| Shell into container | `docker exec -it week14_client bash` |
| Test HTTP | `curl http://localhost:8080/` |
| Test TCP echo | `echo "test" \| nc localhost 9000` |
| Capture traffic | `python scripts/capture_traffic.py --duration 30` |
| Network inspect | `docker network inspect week14_backend_net` |

---

*NETWORKING class - ASE, Informatics | by Revolvix*
