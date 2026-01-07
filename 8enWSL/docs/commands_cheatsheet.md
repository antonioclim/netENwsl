# Commands Cheatsheet — Week 8

> NETWORKING class - ASE, Informatics | by Revolvix

## Docker Commands

### Container Management

```bash
# Start laboratory environment
python scripts/start_lab.py

# Check running containers
docker ps

# View container logs
docker logs week8-nginx-1
docker logs week8-backend1-1 --follow

# Stop all containers
python scripts/stop_lab.py

# Full cleanup
python scripts/cleanup.py --full
```

### Docker Compose

```bash
# Start services (from docker/ directory)
docker compose up -d

# Stop services
docker compose down

# Rebuild images
docker compose build --no-cache

# View service logs
docker compose logs -f nginx
docker compose logs -f backend1 backend2 backend3
```

### Docker Networking

```bash
# List networks
docker network ls

# Inspect network
docker network inspect week8-laboratory-network

# View container IP addresses
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' week8-nginx-1
```

## HTTP Testing Commands

### curl Basics

```bash
# Simple GET request
curl http://localhost:8080/

# GET with headers displayed
curl -i http://localhost:8080/

# Verbose output (shows TCP handshake)
curl -v http://localhost:8080/

# HEAD request only
curl -I http://localhost:8080/

# POST request with data
curl -X POST -d "key=value" http://localhost:8080/api/data

# POST with JSON
curl -X POST -H "Content-Type: application/json" \
     -d '{"name":"test"}' http://localhost:8080/api/data
```

### Load Balancer Testing

```bash
# Round-robin distribution test
for i in {1..12}; do
    curl -s http://localhost:8080/ | grep -o 'Backend [0-9]'
done

# Weighted distribution
for i in {1..20}; do
    curl -s http://localhost:8080/weighted/ | grep -o 'Backend [0-9]'
done

# Least connections
curl http://localhost:8080/least-conn/

# Sticky sessions (IP hash)
curl http://localhost:8080/sticky/
```

### nginx Status

```bash
# Health check
curl http://localhost:8080/nginx-health

# Status page (if enabled)
curl http://localhost:8080/nginx-status
```

## Packet Capture Commands

### tcpdump

```bash
# Capture HTTP traffic
sudo tcpdump -i any port 8080 -w pcap/http_capture.pcap

# Capture with display
sudo tcpdump -i any port 8080 -A

# Capture TCP handshake
sudo tcpdump -i any 'tcp[tcpflags] & (tcp-syn|tcp-ack) != 0' -w pcap/handshake.pcap

# Limit capture count
sudo tcpdump -i any port 8080 -c 100 -w pcap/sample.pcap
```

### Wireshark Filters

```
# HTTP traffic only
http

# TCP port 8080
tcp.port == 8080

# HTTP requests
http.request

# HTTP responses
http.response

# TCP handshake (SYN packets)
tcp.flags.syn == 1

# Specific backend
ip.addr == 172.28.8.21

# Follow TCP stream
tcp.stream eq 0
```

## Python HTTP Tools

### Simple HTTP Server

```python
# Start Python HTTP server (port 8000)
python -m http.server 8000

# Specific directory
python -m http.server 8000 --directory www/

# Bind to specific address
python -m http.server 8000 --bind 127.0.0.1
```

### HTTP Requests (Python)

```python
import requests

# GET request
response = requests.get('http://localhost:8080/')
print(response.status_code)
print(response.headers)

# POST request
response = requests.post('http://localhost:8080/api/data',
                         json={'key': 'value'})

# Session with cookies
session = requests.Session()
session.get('http://localhost:8080/')
```

## Network Diagnostics

### Port Checking

```bash
# Check if port is open
nc -zv localhost 8080

# netstat (Windows)
netstat -an | findstr 8080

# ss (Linux/WSL)
ss -tulpn | grep 8080
```

### DNS and Connectivity

```bash
# Test DNS resolution
nslookup localhost

# Ping test
ping -c 3 localhost

# Trace route
traceroute localhost
```

## File Operations

### Log Analysis

```bash
# Follow nginx access log
docker exec week8-nginx-1 tail -f /var/log/nginx/access.log

# Search for specific patterns
docker logs week8-nginx-1 2>&1 | grep "Backend"

# Count requests per backend
docker logs week8-nginx-1 2>&1 | grep -o 'Backend [0-9]' | sort | uniq -c
```

### Configuration Testing

```bash
# Test nginx configuration
docker exec week8-nginx-1 nginx -t

# Reload nginx configuration
docker exec week8-nginx-1 nginx -s reload
```

## Quick Reference

| Task | Command |
|------|---------|
| Start lab | `python scripts/start_lab.py` |
| Stop lab | `python scripts/stop_lab.py` |
| Check status | `docker ps` |
| Test HTTP | `curl -i http://localhost:8080/` |
| View logs | `docker logs week8-nginx-1` |
| Capture traffic | `python scripts/capture_traffic.py` |
| Run demo | `python scripts/run_demo.py --demo load-balance` |
| Cleanup | `python scripts/cleanup.py --full` |

---

*NETWORKING class - ASE, Informatics | by Revolvix*
