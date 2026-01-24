# Week 11: Commands Cheatsheet

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
> 
> by Revolvix

Quick reference for commands used during the Week 11 laboratory session.

---

## Docker Compose Operations

```powershell
# Start all services in background
docker compose -f docker/docker-compose.yml up -d

# View running containers
docker compose -f docker/docker-compose.yml ps

# View logs (follow mode)
docker compose -f docker/docker-compose.yml logs -f

# View specific service logs
docker compose -f docker/docker-compose.yml logs nginx

# Stop all services (preserve volumes)
docker compose -f docker/docker-compose.yml down

# Stop and remove volumes
docker compose -f docker/docker-compose.yml down -v

# Rebuild images
docker compose -f docker/docker-compose.yml build --no-cache

# Restart specific service
docker compose -f docker/docker-compose.yml restart nginx
```

---

## Container Management

```powershell
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop specific container
docker stop s11_backend_2

# Start stopped container
docker start s11_backend_2

# Execute command in container
docker exec -it s11_nginx_lb /bin/sh

# View container logs
docker logs s11_nginx_lb

# Inspect container details
docker inspect s11_nginx_lb

# View container resource usage
docker stats
```

---

## Network Inspection

```powershell
# List Docker networks
docker network ls

# Inspect network details
docker network inspect s11_network

# View connected containers
docker network inspect s11_network --format '{{range .Containers}}{{.Name}} {{.IPv4Address}}{{"\n"}}{{end}}'
```

---

## Load Balancer Testing

```powershell
# Single request
curl http://localhost:8080/

# Request with headers displayed
curl -i http://localhost:8080/

# Multiple requests (PowerShell)
1..10 | ForEach-Object { curl -s http://localhost:8080/ }

# Multiple requests (CMD)
for /L %i in (1,1,10) do @curl -s http://localhost:8080/

# Health check
curl http://localhost:8080/health

# Nginx status
curl http://localhost:8080/nginx_status

# Request with custom header
curl -H "X-Custom: value" http://localhost:8080/

# POST request
curl -X POST -d "data=test" http://localhost:8080/

# Timed request
curl -w "Time: %{time_total}s\n" -o /dev/null -s http://localhost:8080/
```

---

## Python Exercise Commands

### Backend Servers

```powershell
# Start single backend
python src/exercises/ex_11_01_backend.py --id 1 --port 8081

# Start with verbose logging
python src/exercises/ex_11_01_backend.py --id 1 --port 8081 -v

# Start with artificial delay (latency simulation)
python src/exercises/ex_11_01_backend.py --id 1 --port 8081 --delay 0.1

# Start all three backends (separate terminals)
python src/exercises/ex_11_01_backend.py --id 1 --port 8081
python src/exercises/ex_11_01_backend.py --id 2 --port 8082
python src/exercises/ex_11_01_backend.py --id 3 --port 8083
```

### Load Balancer

```powershell
# Round-robin (default)
python src/exercises/ex_11_02_loadbalancer.py --backends localhost:8081,localhost:8082,localhost:8083 --listen 0.0.0.0:8080

# Least connections
python src/exercises/ex_11_02_loadbalancer.py --backends localhost:8081,localhost:8082,localhost:8083 --listen 0.0.0.0:8080 --algo least_conn

# IP hash (sticky sessions)
python src/exercises/ex_11_02_loadbalancer.py --backends localhost:8081,localhost:8082,localhost:8083 --listen 0.0.0.0:8080 --algo ip_hash

# With verbose logging
python src/exercises/ex_11_02_loadbalancer.py --backends localhost:8081,localhost:8082,localhost:8083 -v
```

### Load Generator

```powershell
# Basic load test
python src/exercises/ex_11_02_loadbalancer.py loadgen --url http://localhost:8080/ --n 100

# Concurrent load test
python src/exercises/ex_11_02_loadbalancer.py loadgen --url http://localhost:8080/ --n 500 --c 20

# Benchmark Nginx
python src/exercises/ex_11_02_loadbalancer.py loadgen --url http://localhost:8080/ --n 1000 --c 50
```

### DNS Client

```powershell
# A record query
python src/exercises/ex_11_03_dns_client.py google.com A

# MX records
python src/exercises/ex_11_03_dns_client.py google.com MX

# NS records
python src/exercises/ex_11_03_dns_client.py google.com NS

# TXT records
python src/exercises/ex_11_03_dns_client.py google.com TXT

# Verbose output
python src/exercises/ex_11_03_dns_client.py google.com A --verbose

# Custom DNS server
python src/exercises/ex_11_03_dns_client.py google.com A --server 1.1.1.1
```

---

## Starter Kit Scripts

```powershell
# Verify environment
python setup/verify_environment.py

# Start laboratory
python scripts/start_lab.py

# Check status
python scripts/start_lab.py --status

# Run demonstrations
python scripts/run_demo.py

# Run specific demo
python scripts/run_demo.py --demo load_balancing
python scripts/run_demo.py --demo failover
python scripts/run_demo.py --demo benchmark

# Stop laboratory
python scripts/stop_lab.py

# Cleanup (preserve data)
python scripts/cleanup.py

# Full cleanup (remove volumes)
python scripts/cleanup.py --full
```

---

## Packet Capture

```powershell
# Start capture (30 seconds)
python scripts/capture_traffic.py --duration 30

# Capture specific port
python scripts/capture_traffic.py --filter "tcp port 8080"

# Capture to specific file
python scripts/capture_traffic.py --output pcap/my_capture.pcap

# Using tshark directly
tshark -i eth0 -w pcap/capture.pcap -a duration:60

# Read capture file
tshark -r pcap/capture.pcap

# Filter HTTP traffic
tshark -r pcap/capture.pcap -Y http

# Display HTTP requests
tshark -r pcap/capture.pcap -Y "http.request.method"
```

---

## Wireshark Filters

```
# HTTP traffic
http

# HTTP requests only
http.request

# HTTP responses only
http.response

# HTTP to specific port
http and tcp.port == 8080

# TCP SYN packets (connections)
tcp.flags.syn == 1 and tcp.flags.ack == 0

# DNS queries
dns.flags.response == 0

# DNS responses
dns.flags.response == 1

# FTP commands
ftp.request.command

# SSH traffic
ssh
```

---

## Port and Process Management

```powershell
# Check port usage (PowerShell)
Get-NetTCPConnection -LocalPort 8080

# Check port usage (CMD)
netstat -ano | findstr :8080

# Find process by port (PowerShell)
Get-Process -Id (Get-NetTCPConnection -LocalPort 8080).OwningProcess

# Kill process by port (PowerShell)
Stop-Process -Id (Get-NetTCPConnection -LocalPort 8080).OwningProcess -Force

# Kill Python processes (PowerShell)
Get-Process python* | Stop-Process -Force
```

---

## Environment Verification

```powershell
# Python version
python --version

# Docker version
docker --version

# Docker Compose version
docker compose version

# WSL status
wsl --status

# Docker info
docker info

# Check running containers
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

---

## Troubleshooting Commands

```powershell
# Check Docker daemon
docker info

# Check Docker Desktop service
Get-Service *docker*

# Restart Docker Desktop (PowerShell Admin)
Restart-Service docker

# Clear Docker cache
docker system prune -f

# Remove all stopped containers
docker container prune -f

# Remove unused networks
docker network prune -f

# View Docker logs
docker compose logs --tail=50

# Check container health
docker inspect --format='{{.State.Health.Status}}' s11_nginx_lb
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
