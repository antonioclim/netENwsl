# Expected Outputs for Week 11 Laboratory

> NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

This document describes the expected outputs for each exercise to help verify correct operation.

## Exercise 1: HTTP Backend Servers

### Starting Backends

```powershell
python src/exercises/ex_11_01_backend.py --id 1 --port 8081 -v
```

**Expected Output:**
```
[Backend 1] Listening on 0.0.0.0:8081
[Backend 1] Press Ctrl+C to stop
```

### Testing Backend

```powershell
curl http://localhost:8081/
```

**Expected Output:**
```
Backend 1 | Host: YOUR-PC | Time: 2025-01-06T14:30:00 | Request #1
```

---

## Exercise 2: Python Load Balancer (Round Robin)

### Starting Load Balancer

```powershell
python src/exercises/ex_11_02_loadbalancer.py --backends localhost:8081,localhost:8082,localhost:8083 --listen 0.0.0.0:8080 --algo rr
```

**Expected Output:**
```
[LB] listen 0.0.0.0:8080 | algo=rr | backends=[('localhost', 8081), ('localhost', 8082), ('localhost', 8083)]
[LB] passive_failures=1 fail_timeout=10.0s sock_timeout=2.5s
```

### Testing Round Robin

```powershell
for /L %i in (1,1,6) do @curl -s http://localhost:8080/
```

**Expected Output:**
```
Backend 1 | Host: ... | Time: ... | Request #1
Backend 2 | Host: ... | Time: ... | Request #1
Backend 3 | Host: ... | Time: ... | Request #1
Backend 1 | Host: ... | Time: ... | Request #2
Backend 2 | Host: ... | Time: ... | Request #2
Backend 3 | Host: ... | Time: ... | Request #2
```

---

## Exercise 3: IP Hash (Sticky Sessions)

### Testing IP Hash

With load balancer running with `--algo ip_hash`:

```powershell
for /L %i in (1,1,5) do @curl -s http://localhost:8080/
```

**Expected Output:**
```
Backend 2 | Host: ... | Request #1
Backend 2 | Host: ... | Request #2
Backend 2 | Host: ... | Request #3
Backend 2 | Host: ... | Request #4
Backend 2 | Host: ... | Request #5
```

All requests go to the **same backend** due to IP hash.

---

## Exercise 4: Failover Simulation

### After Stopping Backend 2

```powershell
docker stop s11_backend_2
for /L %i in (1,1,4) do @curl -s http://localhost:8080/
```

**Expected Output:**
```
Backend 1 | Host: ... | Request #3
Backend 3 | Host: ... | Request #3
Backend 1 | Host: ... | Request #4
Backend 3 | Host: ... | Request #4
```

Traffic is **redistributed** to remaining healthy backends.

---

## Exercise 5: Nginx Docker Load Balancer

### Starting Nginx Stack

```powershell
docker compose -f docker/docker-compose.yml up -d
```

**Expected Output:**
```
[+] Running 4/4
 ✔ Network s11_network  Created
 ✔ Container s11_backend_1  Started
 ✔ Container s11_backend_2  Started
 ✔ Container s11_backend_3  Started
 ✔ Container s11_nginx_lb   Started
```

### Testing Nginx Distribution

```powershell
for /L %i in (1,1,6) do @curl -s http://localhost:8080/
```

**Expected Output:**
```
web1
web2
web3
web1
web2
web3
```

### Health Check

```powershell
curl http://localhost:8080/health
```

**Expected Output:**
```
OK
```

### Nginx Status

```powershell
curl http://localhost:8080/nginx_status
```

**Expected Output:**
```
Active connections: 1
server accepts handled requests
 15 15 15
Reading: 0 Writing: 1 Waiting: 0
```

---

## Exercise 6: DNS Client

### A Record Query

```powershell
python src/exercises/ex_11_03_dns_client.py google.com A --verbose
```

**Expected Output:**
```
[DNS Query] google.com A
[Sending to] 8.8.8.8:53
[Packet Hex]
00 01 01 00 00 01 00 00 00 00 00 00 06 67 6f 6f
67 6c 65 03 63 6f 6d 00 00 01 00 01

[Response]
Name: google.com
Type: A
TTL: 300
Address: 142.250.185.78
```

---

## Exercise 7: Benchmarking

### Python Load Balancer Benchmark

```powershell
python src/exercises/ex_11_02_loadbalancer.py loadgen --url http://localhost:8080/ --n 200 --c 10
```

**Expected Output:**
```
[loadgen] url=http://localhost:8080/
[loadgen] n=200 c=10 duration=0.453s rps=441.50
[loadgen] status_counts={200: 200}
[loadgen] latency_s: p50=0.0215 p90=0.0312 p95=0.0356 p99=0.0421
```

**Expected Metrics:**
- Python LB: ~400-1000 requests/second
- Nginx: ~5000-20000 requests/second

---

## Artefacts Produced

### After Running Demos

The `artifacts/` directory should contain:

- `demo_YYYYMMDD_HHMMSS.log` - Demo execution log

### After Running Captures

The `pcap/` directory should contain:

- `week11_YYYYMMDD_HHMMSS.pcap` - Packet capture file

### Analysing Captures

```powershell
tshark -r pcap/week11_*.pcap -Y http
```

**Expected Output:**
```
1   0.000000 127.0.0.1 → 127.0.0.1 HTTP GET / HTTP/1.1
2   0.001234 127.0.0.1 → 127.0.0.1 HTTP HTTP/1.1 200 OK
...
```

---

## Troubleshooting Guide

### No Response from Load Balancer

1. Check if containers are running: `docker ps`
2. Check port binding: `netstat -ano | findstr :8080`
3. View logs: `docker compose logs`

### Uneven Distribution

1. Verify algorithm setting in nginx.conf
2. Check if a backend is down: `docker ps`
3. Review access logs: `docker compose logs nginx`

### Connection Refused

1. Ensure Docker is running
2. Check firewall settings
3. Verify port mappings in docker-compose.yml

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
