# Expected Outputs — Week 8 Laboratory

> NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

This document shows expected outputs for exercises and commands,
with explanations of what each part means.

---

## Exercise 1: HTTP Server

### Successful GET Request

**Command:**
```bash
curl -v http://localhost:8081/index.html
```

**Expected Output:**
```
*   Trying 127.0.0.1:8081...
* Connected to localhost (127.0.0.1) port 8081 (#0)
> GET /index.html HTTP/1.1
> Host: localhost:8081
> User-Agent: curl/7.68.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Date: Fri, 24 Jan 2025 10:30:00 GMT
< Server: MyHTTPServer/1.0
< Content-Type: text/html; charset=utf-8
< Content-Length: 1234
< 
<!DOCTYPE html>
<html>
...
```

**Why this output?**
- `> GET /index.html HTTP/1.1` — Your request (sent to server)
- `< HTTP/1.1 200 OK` — Server response status (file found)
- `< Content-Type: text/html` — MIME type matches .html extension
- `< Content-Length: 1234` — Server tells client how many bytes to expect
- Body follows the blank line after headers

---

### HEAD Request (No Body)

**Command:**
```bash
curl -I http://localhost:8081/index.html
```

**Expected Output:**
```
HTTP/1.1 200 OK
Date: Fri, 24 Jan 2025 10:30:00 GMT
Server: MyHTTPServer/1.0
Content-Type: text/html; charset=utf-8
Content-Length: 1234
```

**Why this output?**
- Same headers as GET request
- Content-Length is still 1234 (size of body that WOULD be returned)
- NO body content — HEAD never sends body
- Useful for checking if file changed without downloading

---

### 404 Not Found

**Command:**
```bash
curl -v http://localhost:8081/nonexistent.html
```

**Expected Output:**
```
< HTTP/1.1 404 Not Found
< Content-Type: text/plain
< Content-Length: 9
< 
Not Found
```

**Why this output?**
- `404 Not Found` — File doesn't exist in document root
- Simple error message in body
- Content-Type is text/plain for error messages

---

### 403 Forbidden (Directory Traversal Blocked)

**Command:**
```bash
curl -v http://localhost:8081/../../../etc/passwd
```

**Expected Output:**
```
< HTTP/1.1 403 Forbidden
< Content-Type: text/plain
< Content-Length: 9
< 
Forbidden
```

**Why this output?**
- `403 Forbidden` — Access denied (not "404 Not Found")
- Server recognised the path as a security violation
- The `..` sequences would escape the document root
- Proper security: reject with 403, don't reveal if file exists

---

## Exercise 2: Reverse Proxy

### Round-Robin Distribution Test

**Command:**
```bash
for i in {1..9}; do
    curl -s http://localhost:8888/ | grep -o 'Backend [A-C]'
done
```

**Expected Output:**
```
Backend A
Backend B
Backend C
Backend A
Backend B
Backend C
Backend A
Backend B
Backend C
```

**Why this output?**
- Requests cycle through backends: A → B → C → A → B → C...
- Each backend receives exactly 3 of 9 requests
- This demonstrates round-robin load balancing
- If you see the same backend repeatedly, check your modulo logic

---

### X-Forwarded-For Header

**Command (from proxy logs or backend logs):**
```bash
curl http://localhost:8888/
# Then check backend server output
```

**Expected Backend Log:**
```
[2025-01-24T10:30:00] 172.28.8.10 -> GET / HTTP/1.1
Headers: {'host': 'backend', 'x-forwarded-for': '192.168.1.100', 'x-real-ip': '192.168.1.100'}
```

**Why this output?**
- `172.28.8.10` — Connection from nginx (proxy IP)
- `x-forwarded-for: 192.168.1.100` — Original client IP added by proxy
- Without this header, backend would only see proxy IP
- Multiple proxies create chain: `client, proxy1, proxy2`

---

### 502 Bad Gateway

**Command (when backends are down):**
```bash
curl -v http://localhost:8888/
```

**Expected Output:**
```
< HTTP/1.1 502 Bad Gateway
< Content-Type: text/plain
< 
Backend error
```

**Why this output?**
- `502 Bad Gateway` — Proxy received invalid response from backend
- Usually means backend is down or unreachable
- Check: Are backend servers running?
- Check: Is the upstream configuration correct?

---

## Docker Commands

### docker ps (All Running)

**Command:**
```bash
docker ps
```

**Expected Output:**
```
CONTAINER ID   IMAGE                    STATUS         PORTS                    NAMES
abc123...      nginx:alpine             Up 2 minutes   0.0.0.0:8080->80/tcp    week8-nginx-proxy
def456...      python:3.11-slim         Up 2 minutes   8080/tcp                week8-backend-1
ghi789...      python:3.11-slim         Up 2 minutes   8080/tcp                week8-backend-2
jkl012...      python:3.11-slim         Up 2 minutes   8080/tcp                week8-backend-3
mno345...      portainer/portainer-ce   Up 3 hours     0.0.0.0:9000->9000/tcp  portainer
```

**Why this output?**
- 4 containers for this week + Portainer (global)
- nginx has port mapping `0.0.0.0:8080->80/tcp` — accessible from host
- Backends show `8080/tcp` without mapping — internal only
- All show "Up" status — healthy and running

---

### docker logs (nginx access log)

**Command:**
```bash
docker logs week8-nginx-proxy
```

**Expected Output:**
```
192.168.1.100 - - [24/Jan/2025:10:30:00 +0000] "GET / HTTP/1.1" 200 1234 "-" "curl/7.68.0"
192.168.1.100 - - [24/Jan/2025:10:30:01 +0000] "GET /style.css HTTP/1.1" 200 567 "-" "Mozilla/5.0..."
```

**Why this output?**
- nginx default access log format
- Client IP, timestamp, request, status code, bytes sent
- Useful for debugging: which requests succeeded/failed?

---

## Wireshark Captures

### TCP Three-Way Handshake

**Filter:** `tcp.flags.syn == 1`

**Expected Packets:**
```
1. 192.168.1.100 → 172.28.8.10   TCP   [SYN]     Seq=1000
2. 172.28.8.10  → 192.168.1.100  TCP   [SYN,ACK] Seq=5000, Ack=1001
3. 192.168.1.100 → 172.28.8.10   TCP   [ACK]     Seq=1001, Ack=5001
```

**Why this output?**
- Packet 1: Client initiates with SYN
- Packet 2: Server responds with SYN-ACK
- Packet 3: Client confirms with ACK
- After this, connection is ESTABLISHED and data can flow

---

### HTTP Request-Response

**Filter:** `http`

**Expected Packets:**
```
1. 192.168.1.100 → 172.28.8.10   HTTP   GET /index.html HTTP/1.1
2. 172.28.8.10  → 192.168.1.100  HTTP   HTTP/1.1 200 OK
```

**Why this output?**
- Wireshark reassembles TCP segments into HTTP messages
- Shows complete request and response
- Right-click → Follow → TCP Stream for full conversation

---

## Test Suite

### All Tests Passing

**Command:**
```bash
python3 tests/test_exercises.py
```

**Expected Output:**
```
test_parse_request_basic (__main__.TestExercise1HTTPServer) ... ok
test_parse_request_headers_lowercase (__main__.TestExercise1HTTPServer) ... ok
test_is_safe_path_basic (__main__.TestExercise1HTTPServer) ... ok
test_is_safe_path_traversal_blocked (__main__.TestExercise1HTTPServer) ... ok
test_build_response_format (__main__.TestExercise1HTTPServer) ... ok
test_handle_request_head_no_body (__main__.TestExercise1HTTPServer) ... ok
test_round_robin_balancer_init (__main__.TestExercise2ReverseProxy) ... ok
test_round_robin_balancer_cycling (__main__.TestExercise2ReverseProxy) ... ok
test_round_robin_empty_backends (__main__.TestExercise2ReverseProxy) ... ok
test_add_proxy_headers_xff (__main__.TestExercise2ReverseProxy) ... ok
test_add_proxy_headers_chain (__main__.TestExercise2ReverseProxy) ... ok

----------------------------------------------------------------------
Ran 11 tests in 0.042s

OK
```

**Why this output?**
- Each test function runs independently
- "ok" means assertion passed
- "FAIL" would show what went wrong and why
- "ERROR" indicates exception during test

---

## Common Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| `Connection refused` | Nothing listening on port | Start the server |
| `Address already in use` | Port occupied | Find and kill process using port |
| `Permission denied` | Need sudo or wrong permissions | Check file/socket permissions |
| `Name resolution failed` | DNS issue | Check container network |
| `502 Bad Gateway` | Backend unreachable | Start backends |
| `504 Gateway Timeout` | Backend too slow | Increase timeout |

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
