# Expected Outputs — Week 10
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Reference outputs for verifying exercise solutions

---

## Exercise 1: HTTPS REST API

### Certificate Generation

```bash
$ python3 src/exercises/ex_10_01_https.py generate-cert
[OK] Certificate generated: output/tls/server.crt
[OK] Key generated: output/tls/server.key
```

### Server Startup

```bash
$ python3 src/exercises/ex_10_01_https.py serve
[INFO] HTTPS server ready
[INFO] URL: https://127.0.0.1:8443/
[INFO] Certificate: output/tls/server.crt
[INFO] Press Ctrl+C to stop
```

### API Responses

💭 **PREDICTION:** What status code should POST return when creating a resource?

```bash
# GET /api/resources (empty)
$ curl -k https://127.0.0.1:8443/api/resources
{"resources": []}

# POST /api/resources (create)
$ curl -k -X POST https://127.0.0.1:8443/api/resources \
  -H "Content-Type: application/json" \
  -d '{"name": "test", "value": 42}'
{"id": 1, "name": "test", "value": 42}
# Expected status: 201 Created

# GET /api/resources/1
$ curl -k https://127.0.0.1:8443/api/resources/1
{"id": 1, "name": "test", "value": 42}

# PUT /api/resources/1
$ curl -k -X PUT https://127.0.0.1:8443/api/resources/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "updated", "value": 100}'
{"id": 1, "name": "updated", "value": 100}

# DELETE /api/resources/1
$ curl -k -X DELETE https://127.0.0.1:8443/api/resources/1
# Expected status: 204 No Content (empty body)
```

---

## Exercise 2: REST Maturity Levels

### Level 0 (RPC-style)

```bash
$ curl -X POST http://127.0.0.1:5000/level0/service \
  -H "Content-Type: application/json" \
  -d '{"action": "list_users"}'
{"status": "ok", "users": [{"id": 1, "name": "Alice Smith", "email": "alice@example.com"}, {"id": 2, "name": "Bob Jones", "email": "bob@example.com"}]}
```

### Level 2 (HTTP Verbs)

💭 **PREDICTION:** How does this differ from Level 0?

```bash
$ curl http://127.0.0.1:5000/level2/users
{"users": [{"id": 1, "name": "Alice Smith", "email": "alice@example.com"}, {"id": 2, "name": "Bob Jones", "email": "bob@example.com"}]}
```

### Level 3 (HATEOAS)

```bash
$ curl http://127.0.0.1:5000/level3/users/1
{
  "id": 1,
  "name": "Alice Smith",
  "email": "alice@example.com",
  "_links": {
    "self": {"href": "/level3/users/1", "method": "GET"},
    "update": {"href": "/level3/users/1", "method": "PUT"},
    "delete": {"href": "/level3/users/1", "method": "DELETE"},
    "collection": {"href": "/level3/users", "method": "GET"}
  }
}
```

---

## Exercise 3: DNS Queries

### Basic Query

💭 **PREDICTION:** What IP will web.lab.local resolve to?

```bash
$ dig @127.0.0.1 -p 5353 web.lab.local +short
172.20.0.10
```

### Full Response

```bash
$ dig @127.0.0.1 -p 5353 web.lab.local

; <<>> DiG 9.x.x <<>> @127.0.0.1 -p 5353 web.lab.local
;; QUESTION SECTION:
;web.lab.local.                 IN      A

;; ANSWER SECTION:
web.lab.local.          300     IN      A       172.20.0.10

;; Query time: X msec
;; SERVER: 127.0.0.1#5353(127.0.0.1)
```

### Non-existent Domain

💭 **PREDICTION:** What status code indicates a non-existent domain?

```bash
$ dig @127.0.0.1 -p 5353 nonexistent.lab.local

;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, ...
```

---

## Exercise 4: SSH and FTP

### SSH Commands

```bash
$ ssh -p 2222 labuser@localhost
# Password: labpass

$ hostname
ssh-server

$ whoami
labuser

$ uname -a
Linux ssh-server ...
```

### FTP Session

💭 **PREDICTION:** How many connections does FTP establish?

```bash
$ ftp -p localhost 2121
Connected to localhost.
220 FTP Server ready
Name: labftp
331 Password required
Password: labftp
230 User logged in
ftp> pwd
257 "/" is current directory
ftp> ls
227 Entering Passive Mode (...)
150 Opening data connection
...
226 Transfer complete
ftp> quit
221 Goodbye
```

---

## Smoke Test Output

```bash
$ python3 tests/smoke_test.py
============================================================
Week 10 Smoke Tests
============================================================
  [✓ PASS] Web Server (HTTP) (localhost:8000) — Connected
  [✓ PASS] DNS Server (localhost:5353) — Received 34 bytes
  [✓ PASS] SSH Server (localhost:2222) — Connected
  [✓ PASS] FTP Server (localhost:2121) — Connected

------------------------------------------------------------
Additional Tests:
------------------------------------------------------------
  [✓ PASS] HTTP GET / — HTTP 200
  [✓ PASS] DNS web.lab.local — Resolved to 172.20.0.10

============================================================
Results: 6 passed, 0 failed
============================================================

[OK] All services are running!
```

---

*Computer Networks — Week 10 | ASE, CSIE Bucharest*
*Expected outputs by ing. dr. Antonio Clim*
