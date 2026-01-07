# Expected Outputs

> NETWORKING class - ASE, Informatics | by Revolvix
>
> Week 14: Integrated Recap and Project Evaluation

This document describes the expected outputs and observations for each component of the Week 14 laboratory environment.

---

## Environment Verification

### verify_environment.py

**Command:**
```powershell
python setup/verify_environment.py
```

**Expected Output:**
```
==================================================
Environment Verification for Week 14 Laboratory
NETWORKING class - ASE, Informatics
==================================================

Python Environment:
  [PASS] Python 3.11.x

Required Packages:
  [PASS] Python package: requests
  [PASS] Python package: pyyaml
  [PASS] Python package: docker

Docker Environment:
  [PASS] Docker installed
  [PASS] Docker Compose installed
  [PASS] Docker daemon running

WSL2 Environment:
  [PASS] WSL2 available

Network Tools:
  [PASS] Wireshark available
  [PASS] tshark available

Port Availability:
  [PASS] Port 8080 (Load Balancer) available
  [PASS] Port 8001 (Backend App 1) available
  [PASS] Port 8002 (Backend App 2) available
  [PASS] Port 9000 (TCP Echo Server) available

==================================================
Results: 12 passed, 0 failed, 0 warnings
Environment is ready!
```

**Exit Code:** 0 (success)

---

## Laboratory Startup

### start_lab.py

**Command:**
```powershell
python scripts/start_lab.py
```

**Expected Output:**
```
============================================================
Starting Week 14 Laboratory Environment
============================================================

[INFO] Checking Docker status...
[INFO] Docker daemon is running

[INFO] Building Docker images...
[+] Building 15.2s (12/12) FINISHED

[INFO] Starting containers...
[+] Running 6/6
 ✔ Network week14_backend_net    Created
 ✔ Network week14_frontend_net   Created
 ✔ Container week14_app1         Started
 ✔ Container week14_app2         Started
 ✔ Container week14_echo         Started
 ✔ Container week14_lb           Started
 ✔ Container week14_client       Started

[INFO] Waiting for services to initialise...

[INFO] Health checks:
  [PASS] app1 - healthy
  [PASS] app2 - healthy
  [PASS] lb - healthy
  [PASS] echo - ready
  [PASS] client - running

============================================================
Laboratory environment is ready!

Access points:
  Load Balancer:  http://localhost:8080
  Backend App 1:  http://localhost:8001
  Backend App 2:  http://localhost:8002
  Echo Server:    tcp://localhost:9000
============================================================
```

**Exit Code:** 0 (success)

---

## Service Responses

### Load Balancer (port 8080)

**Command:**
```bash
curl http://localhost:8080/
```

**Expected Output (alternates between):**
```
Hello from app1!
```
or
```
Hello from app2!
```

**Headers:**
```
HTTP/1.1 200 OK
Content-Type: text/plain
X-Backend: app1
X-Forwarded-For: 172.21.0.x
```

### Load Balancer Status

**Command:**
```bash
curl http://localhost:8080/status
```

**Expected Output:**
```json
{
  "status": "healthy",
  "backends": [
    {"host": "app1", "port": 8001, "healthy": true},
    {"host": "app2", "port": 8001, "healthy": true}
  ],
  "algorithm": "round-robin",
  "requests_served": 42
}
```

### Backend App Info

**Command:**
```bash
curl http://localhost:8001/info
```

**Expected Output:**
```json
{
  "service": "backend",
  "hostname": "app1",
  "port": 8001,
  "uptime_seconds": 123.45,
  "requests_handled": 15
}
```

### Backend Health Check

**Command:**
```bash
curl http://localhost:8001/health
```

**Expected Output:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-07T12:00:00Z"
}
```

### TCP Echo Server

**Command:**
```bash
echo "Hello World" | nc localhost 9000
```

**Expected Output:**
```
ECHO: Hello World
```

---

## Exercise Outputs

### Exercise 1: Environment Verification

**Command:**
```powershell
python tests/test_exercises.py --exercise 1
```

**Expected Output:**
```
Exercise 1: Environment Verification
=====================================
  [PASS] Load balancer accessible
  [PASS] Backend app1 accessible
  [PASS] Backend app2 accessible
  [PASS] LB status endpoint returns valid JSON

Results: 4/4 tests passed
```

### Exercise 2: Load Balancer Behaviour

**Command:**
```powershell
python tests/test_exercises.py --exercise 2
```

**Expected Output:**
```
Exercise 2: Load Balancer Behaviour Analysis
=============================================
  [INFO] Sending 10 HTTP requests to load balancer...
  [PASS] Both backends received requests
  [PASS] Distribution: app1=5, app2=5
  [PASS] Round-robin pattern detected

Results: 3/3 tests passed
```

### Exercise 3: TCP Echo Testing

**Command:**
```powershell
python tests/test_exercises.py --exercise 3
```

**Expected Output:**
```
Exercise 3: TCP Echo Service Testing
=====================================
  [INFO] Testing echo with 4 messages...
  [PASS] "Hello" echoed correctly
  [PASS] "NetworkTest123" echoed correctly  
  [PASS] Empty string handled
  [PASS] Long message (50 chars) echoed correctly

Results: 4/4 tests passed
```

### Exercise 4: Packet Capture Analysis

**Command:**
```powershell
python tests/test_exercises.py --exercise 4
```

**Expected Output:**
```
Exercise 4: Packet Capture Analysis
====================================
  [INFO] Checking pcap/ directory...
  [PASS] PCAP files found
  [INFO] Files: demo.pcap, http_capture.pcap

Results: 1/1 tests passed
```

---

## Demonstration Outputs

### Full Demo

**Command:**
```powershell
python scripts/run_demo.py --demo full
```

**Expected Output:**
```
============================================================
Week 14 - Full System Demonstration
============================================================

[Phase 1] Health Check
-----------------------
  Checking service health...
  app1: healthy
  app2: healthy
  lb: healthy
  echo: ready

[Phase 2] HTTP Load Balancing
-----------------------------
  Sending 20 HTTP requests...
  
  Request  1: app1 (23ms)
  Request  2: app2 (18ms)
  Request  3: app1 (15ms)
  ...
  Request 20: app2 (16ms)
  
  Distribution:
    app1: 10 requests (50%)
    app2: 10 requests (50%)
  
  Latency:
    Min: 14ms
    Max: 28ms
    Avg: 18ms

[Phase 3] TCP Echo Testing
--------------------------
  Testing echo server...
  
  Test 1: "Hello" -> "ECHO: Hello" [OK]
  Test 2: "12345" -> "ECHO: 12345" [OK]
  Test 3: "Network" -> "ECHO: Network" [OK]

[Phase 4] Report Generation
---------------------------
  Writing demo_report.json...
  Writing http_requests.json...
  Writing validation.txt...

============================================================
Demo completed successfully!
Artifacts saved to: artifacts/
============================================================
```

**Generated Files:**

`artifacts/demo_report.json`:
```json
{
  "timestamp": "2026-01-07T12:30:00Z",
  "duration_seconds": 15.2,
  "http_tests": {
    "total_requests": 20,
    "successful": 20,
    "failed": 0,
    "distribution": {
      "app1": 10,
      "app2": 10
    },
    "latency": {
      "min_ms": 14,
      "max_ms": 28,
      "avg_ms": 18
    }
  },
  "echo_tests": {
    "total": 3,
    "passed": 3,
    "failed": 0
  },
  "health_status": {
    "app1": "healthy",
    "app2": "healthy",
    "lb": "healthy",
    "echo": "ready"
  }
}
```

### Failover Demo

**Command:**
```powershell
python scripts/run_demo.py --demo failover
```

**Expected Output:**
```
============================================================
Week 14 - Failover Demonstration
============================================================

[Step 1] Initial State
-----------------------
  All backends healthy
  Distribution: app1=50%, app2=50%

[Step 2] Stopping app1
-----------------------
  docker stop week14_app1
  Waiting for health check to detect failure...
  
  LB status:
    app1: unhealthy (connection refused)
    app2: healthy

[Step 3] Testing After Failure
-------------------------------
  Sending 10 requests...
  All requests routed to app2
  
  Distribution:
    app1: 0 requests (0%)
    app2: 10 requests (100%)

[Step 4] Restoring app1
------------------------
  docker start week14_app1
  Waiting for health check...
  
  LB status:
    app1: healthy
    app2: healthy

[Step 5] Testing After Recovery
--------------------------------
  Sending 10 requests...
  Both backends responding
  
  Distribution:
    app1: 5 requests (50%)
    app2: 5 requests (50%)

============================================================
Failover demonstration complete
============================================================
```

---

## Smoke Test Output

**Command:**
```powershell
python tests/smoke_test.py
```

**Expected Output (all passing):**
```
Week 14 Laboratory - Smoke Test
NETWORKING class - ASE, Informatics | by Revolvix

Running smoke tests...

  [PASS] Docker Running (45ms)
  [PASS] Containers Running (120ms)
  [PASS] Network Configuration (85ms)
  [PASS] Load Balancer Port (12ms)
  [PASS] Backend App 1 Port (8ms)
  [PASS] Backend App 2 Port (9ms)
  [PASS] Echo Server Port (7ms)
  [PASS] HTTP Response (65ms)
  [PASS] Echo Functionality (23ms)
  [PASS] Round-Robin Distribution (180ms)

==================================================
Smoke Test Summary
==================================================

Tests: 10/10 passed
Duration: 554ms

✓ All smoke tests passed!
The laboratory environment is ready.
```

**Exit Code:** 0 (success)

---

## Cleanup Output

### Standard Cleanup

**Command:**
```powershell
python scripts/cleanup.py
```

**Expected Output:**
```
============================================================
Cleaning up Week 14 Laboratory Environment
============================================================

[INFO] Stopping containers...
[+] Running 5/5
 ✔ Container week14_client  Stopped
 ✔ Container week14_lb      Stopped
 ✔ Container week14_app1    Stopped
 ✔ Container week14_app2    Stopped
 ✔ Container week14_echo    Stopped

[INFO] Removing containers...
[+] Running 5/5
 ✔ Container week14_client  Removed
 ✔ Container week14_lb      Removed
 ✔ Container week14_app1    Removed
 ✔ Container week14_app2    Removed
 ✔ Container week14_echo    Removed

[INFO] Removing networks...
[+] Running 2/2
 ✔ Network week14_backend_net   Removed
 ✔ Network week14_frontend_net  Removed

============================================================
Cleanup complete!
============================================================
```

### Full Cleanup

**Command:**
```powershell
python scripts/cleanup.py --full
```

**Expected Output:**
```
============================================================
Cleaning up Week 14 Laboratory Environment
============================================================

[INFO] Stopping and removing containers...
[INFO] Removing networks...
[INFO] Removing volumes...
[INFO] Cleaning artifacts directory...
  Removed: demo_report.json
  Removed: http_requests.json
  Removed: validation.txt

[INFO] Cleaning pcap directory...
  Removed: demo.pcap
  Removed: http_capture.pcap

[INFO] Docker disk usage:
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          5         0         1.2GB     1.2GB (100%)
Containers      0         0         0B        0B
Local Volumes   0         0         0B        0B
Build Cache     15        0         450MB     450MB

============================================================
Cleanup complete!
System is ready for the next laboratory session.
============================================================
```

---

## Packet Capture Output

### Using capture_traffic.py

**Command:**
```powershell
python scripts/capture_traffic.py --duration 30 --output pcap/test.pcap
```

**Expected Output:**
```
============================================================
Starting packet capture
============================================================

[INFO] Using tshark for capture
[INFO] Interface: any
[INFO] Duration: 30 seconds
[INFO] Output: pcap/test.pcap

Capturing... [████████████████████████████████] 30s

[INFO] Capture complete
[INFO] File size: 245 KB
[INFO] Packets captured: 1,234

Analysis suggestions:
  Open in Wireshark:
    wireshark pcap/test.pcap

  Filter HTTP traffic:
    tshark -r pcap/test.pcap -Y "http"

  Show TCP conversations:
    tshark -r pcap/test.pcap -q -z conv,tcp
```

---

## Error Conditions

### Docker Not Running

**Expected Output:**
```
[ERROR] Docker daemon is not running
[INFO] Please start Docker Desktop and try again
```

**Exit Code:** 1

### Port Already in Use

**Expected Output:**
```
[ERROR] Port 8080 is already in use
[INFO] Stop the conflicting service or change the port in docker-compose.yml
[INFO] To find the process: netstat -ano | findstr :8080
```

**Exit Code:** 1

### Container Health Check Failed

**Expected Output:**
```
[WARN] Container week14_app1 failed health check
[INFO] Checking logs...

--- Container logs ---
Traceback (most recent call last):
  File "/app/backend_server.py", line 45
    ...
SyntaxError: invalid syntax
--- End logs ---

[INFO] Fix the error and run: python scripts/start_lab.py --rebuild
```

**Exit Code:** 1

---

## Wireshark Filter Examples

### HTTP Traffic to Load Balancer
```
tcp.port == 8080 && http
```

### Backend Communication
```
tcp.port == 8001 || tcp.port == 8002
```

### TCP Echo Traffic
```
tcp.port == 9000
```

### Full Week 14 Traffic
```
tcp.port in {8080, 8001, 8002, 9000}
```

### HTTP Requests Only
```
http.request.method == "GET"
```

### TCP Handshake
```
tcp.flags.syn == 1
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
