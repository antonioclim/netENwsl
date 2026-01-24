# Commands Cheatsheet — Week 8

> NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

---

## Docker Commands

### Container Management

```bash
# Start laboratory environment
python3 scripts/start_lab.py
# Expected: "Laboratory environment is ready!"

# Check running containers
docker ps
# Expected: 4 containers (nginx + 3 backends)

# View container logs
docker logs week8-nginx-proxy
docker logs week8-backend-1 --follow

# Stop all containers
python3 scripts/stop_lab.py

# Full cleanup
python3 scripts/cleanup.py --full
```

### Docker Compose

```bash
# Start services (from kit directory)
docker compose -f docker/docker-compose.yml up -d
# Expected: Creating week8-nginx-proxy ... done

# Stop services
docker compose -f docker/docker-compose.yml down

# Rebuild images
docker compose -f docker/docker-compose.yml build --no-cache

# View service logs
docker compose -f docker/docker-compose.yml logs -f nginx
docker compose -f docker/docker-compose.yml logs -f backend1 backend2 backend3
```

### Docker Networking

```bash
# List networks
docker network ls
# Expected: week8-laboratory-network in list

# Inspect network
docker network inspect week8-laboratory-network
# Expected: Shows subnet 172.28.8.0/24

# View container IP addresses
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' week8-nginx-proxy
# Expected: 172.28.8.10
```

---

## HTTP Testing Commands

### curl Basics

```bash
# Simple GET request
curl http://localhost:8080/
# Expected: HTML response from backend

# GET with headers displayed
curl -i http://localhost:8080/
# Expected: HTTP/1.1 200 OK + headers + body

# Verbose output (shows TCP handshake info)
curl -v http://localhost:8080/
# Expected: > GET / HTTP/1.1, < HTTP/1.1 200 OK

# HEAD request only
curl -I http://localhost:8080/
# Expected: Headers only, no body

# POST request with data
curl -X POST -d "key=value" http://localhost:8080/api/data
# Expected: Depends on server implementation

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
# Expected: Backend 1, Backend 2, Backend 3, Backend 1, ... (repeating)

# Count distribution
for i in {1..12}; do
    curl -s http://localhost:8080/ | grep -o 'Backend [0-9]'
done | sort | uniq -c
# Expected: 4 Backend 1, 4 Backend 2, 4 Backend 3

# Check backend headers
curl -i http://localhost:8080/ | grep -i backend
# Expected: X-Backend-ID or similar header
```

### nginx Status

```bash
# Health check
curl http://localhost:8080/nginx-health
# Expected: "healthy" or 200 OK

# nginx version
docker exec week8-nginx-proxy nginx -v
# Expected: nginx version: nginx/x.x.x
```

---

## Packet Capture Commands

### tcpdump

```bash
# Capture HTTP traffic
sudo tcpdump -i any port 8080 -w pcap/http_capture.pcap
# Then generate traffic with curl
# Stop with Ctrl+C

# Capture with ASCII display
sudo tcpdump -i any port 8080 -A
# Expected: Shows HTTP headers in plain text

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

# Successful responses
http.response.code == 200

# Error responses
http.response.code >= 400

# Specific backend
ip.addr == 172.28.8.21

# Follow TCP stream
tcp.stream eq 0

# Backend identification headers
http.response.header matches "X-Backend"
```

---

## Python HTTP Tools

### Simple HTTP Server

```bash
# Start Python HTTP server (port 8000)
python3 -m http.server 8000
# Expected: Serving HTTP on 0.0.0.0 port 8000

# Specific directory
python3 -m http.server 8000 --directory www/

# Bind to specific address
python3 -m http.server 8000 --bind 127.0.0.1
```

### Python Requests (Interactive)

```python
import requests

# GET request
response = requests.get('http://localhost:8080/')
print(response.status_code)  # Expected: 200
print(response.headers)       # Expected: dict with headers

# POST request
response = requests.post('http://localhost:8080/api/data',
                         json={'key': 'value'})

# Session with cookies
session = requests.Session()
session.get('http://localhost:8080/')
```

---

## Network Diagnostics

### Port Checking

```bash
# Check if port is open (nc)
nc -zv localhost 8080
# Expected: Connection to localhost 8080 port [tcp/*] succeeded!

# netstat (shows listening ports)
sudo netstat -tlnp | grep 8080
# Expected: tcp 0 0 0.0.0.0:8080 ... LISTEN

# ss (modern netstat)
ss -tlnp | grep 8080
# Expected: LISTEN 0 ... *:8080
```

### DNS and Connectivity

```bash
# Test DNS resolution
nslookup localhost
# Expected: Address: 127.0.0.1

# Ping test
ping -c 3 localhost
# Expected: 3 packets transmitted, 3 received

# Test from container
docker exec week8-nginx-proxy ping -c 3 backend1
# Expected: 3 packets transmitted, 3 received
```

---

## File Operations

### Log Analysis

```bash
# Follow nginx access log
docker exec week8-nginx-proxy tail -f /var/log/nginx/access.log

# Search for specific patterns
docker logs week8-nginx-proxy 2>&1 | grep "Backend"

# Count requests per backend
docker logs week8-nginx-proxy 2>&1 | grep -o 'Backend [0-9]' | sort | uniq -c
```

### Configuration Testing

```bash
# Test nginx configuration
docker exec week8-nginx-proxy nginx -t
# Expected: nginx: configuration file /etc/nginx/nginx.conf test is successful

# Reload nginx configuration
docker exec week8-nginx-proxy nginx -s reload
```

---

## Quick Reference Table

| Task | Command | Expected Output |
|------|---------|-----------------|
| Start lab | `python3 scripts/start_lab.py` | "Laboratory environment is ready!" |
| Stop lab | `python3 scripts/stop_lab.py` | Containers stopped |
| Check status | `docker ps` | 4 running containers |
| Test HTTP | `curl -i http://localhost:8080/` | HTTP/1.1 200 OK |
| View logs | `docker logs week8-nginx-proxy` | Access logs |
| Capture traffic | `python3 scripts/capture_traffic.py` | PCAP file created |
| Run demo | `python3 scripts/run_demo.py --demo load-balance` | Demo output |
| Cleanup | `python3 scripts/cleanup.py --full` | Resources removed |
| Test backend 1 | `curl http://localhost:8080/` | Response with Backend ID |
| Check nginx config | `docker exec week8-nginx-proxy nginx -t` | "test is successful" |

---

## Common Mistakes

| What You Typed | Problem | Correct Command |
|----------------|---------|-----------------|
| `curl localhost:8080` | Missing protocol | `curl http://localhost:8080/` |
| `docker logs nginx` | Wrong container name | `docker logs week8-nginx-proxy` |
| `sudo docker ...` | Unnecessary sudo in WSL | `docker ...` |
| `docker-compose` | Old command | `docker compose` (v2) |
| `curl -d data` | Missing -X POST | `curl -X POST -d data` |

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
