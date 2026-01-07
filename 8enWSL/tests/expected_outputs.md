# Expected Outputs — Week 8

> NETWORKING class - ASE, Informatics | by Revolvix

## Docker Environment Startup

### Expected Output: `python scripts/start_lab.py`

```
============================================================
Starting Week 8 Laboratory Environment
============================================================
[INFO] Checking Docker availability...
[INFO] Docker daemon is running
[INFO] Building images...
[INFO] Starting containers...
[INFO] Waiting for services to initialise...
[INFO] Checking nginx health...
[INFO] Checking backend1 health...
[INFO] Checking backend2 health...
[INFO] Checking backend3 health...
============================================================
Laboratory environment is ready!

Access points:
  Portainer:    https://localhost:9443
  HTTP Proxy:   http://localhost:8080
  HTTPS Proxy:  https://localhost:8443

Quick test:
  curl http://localhost:8080/
============================================================
```

### Expected Container Status: `docker ps`

```
CONTAINER ID   IMAGE                    PORTS                                      NAMES
abc123...      nginx:alpine             0.0.0.0:8080->80/tcp, 0.0.0.0:8443->443/tcp week8-nginx-1
def456...      week8-backend            8080/tcp                                    week8-backend1-1
ghi789...      week8-backend            8080/tcp                                    week8-backend2-1
jkl012...      week8-backend            8080/tcp                                    week8-backend3-1
mno345...      portainer/portainer-ce   0.0.0.0:9443->9443/tcp                      week8-portainer-1
```

## HTTP Responses

### Expected: `curl -i http://localhost:8080/`

```http
HTTP/1.1 200 OK
Server: nginx/1.25.x
Date: <current date>
Content-Type: text/html
Content-Length: <varies>
Connection: keep-alive
X-Backend-ID: 1
X-Backend-Name: Alpha
X-Served-By: backend1

<!DOCTYPE html>
<html>
<head>
    <title>Week 8 Laboratory</title>
</head>
<body>
    <h1>Welcome to Week 8 Laboratory</h1>
    <p>Served by Backend 1 (Alpha)</p>
    ...
</body>
</html>
```

### Expected: Round-Robin Distribution (6 requests)

```bash
$ for i in {1..6}; do curl -s http://localhost:8080/ | grep -o 'Backend [0-9]'; done
Backend 1
Backend 2
Backend 3
Backend 1
Backend 2
Backend 3
```

### Expected: Health Endpoint

```bash
$ curl http://localhost:8080/nginx-health
OK
```

### Expected: `/api/info` Endpoint

```json
{
    "backend_id": 1,
    "backend_name": "Alpha",
    "hostname": "backend1",
    "timestamp": "2026-01-07T12:00:00.000000",
    "request_count": 5
}
```

## Load Balancing Algorithms

### Round-Robin (Default)

```bash
$ for i in {1..9}; do curl -s localhost:8080/ | grep Backend; done
Backend 1
Backend 2
Backend 3
Backend 1
Backend 2
Backend 3
Backend 1
Backend 2
Backend 3
```

Distribution: Equal (33% each)

### Weighted Distribution

```bash
$ for i in {1..20}; do curl -s localhost:8080/weighted/ | grep Backend; done
# Expected approximate distribution:
# Backend 1: ~55% (weight 5)
# Backend 2: ~33% (weight 3)
# Backend 3: ~11% (weight 1)
```

### Least Connections

```bash
$ curl localhost:8080/least-conn/
# Routes to backend with fewest active connections
```

### IP Hash (Sticky Sessions)

```bash
$ for i in {1..5}; do curl -s localhost:8080/sticky/ | grep Backend; done
Backend 2
Backend 2
Backend 2
Backend 2
Backend 2
# Same backend for same client IP
```

## Packet Capture

### Expected TCP Handshake (Wireshark)

| No. | Time | Source | Destination | Protocol | Info |
|-----|------|--------|-------------|----------|------|
| 1 | 0.000 | 127.0.0.1 | 127.0.0.1 | TCP | 52345 → 8080 [SYN] |
| 2 | 0.001 | 127.0.0.1 | 127.0.0.1 | TCP | 8080 → 52345 [SYN, ACK] |
| 3 | 0.001 | 127.0.0.1 | 127.0.0.1 | TCP | 52345 → 8080 [ACK] |
| 4 | 0.002 | 127.0.0.1 | 127.0.0.1 | HTTP | GET / HTTP/1.1 |
| 5 | 0.005 | 127.0.0.1 | 127.0.0.1 | HTTP | HTTP/1.1 200 OK |

### Expected Wireshark Filters

```
# HTTP traffic only
http

# TCP handshake (SYN packets)
tcp.flags.syn == 1 && tcp.flags.ack == 0

# Specific port
tcp.port == 8080

# HTTP requests
http.request.method == "GET"

# HTTP responses
http.response.code == 200
```

## Exercise Outputs

### Exercise 1: HTTP Server

When implemented correctly, running the basic HTTP server:

```bash
$ python src/exercises/ex_8_01_http_server.py
[INFO] Starting HTTP server on 127.0.0.1:8888
[INFO] Server ready, waiting for connections...
```

Test request:
```bash
$ curl -i http://localhost:8888/hello.txt
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 13
Connection: close

Hello, World!
```

### Exercise 2: Reverse Proxy

When implemented correctly:

```bash
$ python src/exercises/ex_8_02_reverse_proxy.py
[INFO] Starting reverse proxy on port 8000
[INFO] Backends: ['127.0.0.1:8001', '127.0.0.1:8002', '127.0.0.1:8003']
[INFO] Load balancing: round-robin
```

Request flow:
```
Client → Proxy (8000) → Backend (8001/8002/8003) → Response
```

## Demo Outputs

### Demo: docker-nginx

```bash
$ python scripts/run_demo.py --demo docker-nginx

============================================================
Demo: Docker nginx Reverse Proxy
============================================================

Testing round-robin load balancing...

Request 1: Backend 1 (Alpha)
Request 2: Backend 2 (Beta)
Request 3: Backend 3 (Gamma)
Request 4: Backend 1 (Alpha)
...

Distribution:
  Backend 1 (Alpha): 4 requests
  Backend 2 (Beta):  4 requests
  Backend 3 (Gamma): 4 requests

✓ Round-robin is working correctly!
============================================================
```

### Demo: load-balance

```bash
$ python scripts/run_demo.py --demo load-balance

============================================================
Demo: Load Balancing Algorithms Comparison
============================================================

1. Round-Robin (default):
   1→2→3→1→2→3→1→2→3→1→2→3
   Distribution: {1: 4, 2: 4, 3: 4}

2. Weighted (5:3:1):
   1→1→1→2→1→2→1→3→2→1→1→2
   Distribution: {1: 7, 2: 4, 3: 1}

3. Least Connections:
   (varies based on current connections)

4. IP Hash:
   2→2→2→2→2→2→2→2→2→2→2→2
   (consistent for same client IP)
============================================================
```

## Cleanup Output

### Expected: `python scripts/cleanup.py --full`

```
============================================================
Cleaning up Week 8 Laboratory Environment
============================================================
[INFO] Stopping containers...
[INFO] Removing containers...
[INFO] Removing networks...
[INFO] Removing volumes...
[INFO] Cleaning artifacts directory...
[INFO] Cleaning pcap directory...
============================================================
Cleanup complete!
System is ready for the next laboratory session.
============================================================
```

### Verification: `docker ps -a | grep week8`

```
(no output - all week8 containers removed)
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
