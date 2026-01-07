# Expected Outputs

> NETWORKING class - ASE, Informatics | by Revolvix

This document describes the expected output for each laboratory exercise.

## Exercise 1: HTTP Service

### curl http://localhost:8000/

```
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.12.x
Content-type: text/html
Content-Length: ...

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    ...
```

### curl http://localhost:8000/hello.txt

```
HTTP/1.0 200 OK
Content-type: text/plain
Content-Length: ...

Hello from the Week 10 HTTP Server!
...
```

## Exercise 2: DNS Service

### dig @127.0.0.1 -p 5353 myservice.lab.local +short

```
10.10.10.10
```

### dig @127.0.0.1 -p 5353 nonexistent.lab.local

Response should include NXDOMAIN (RCODE 3).

## Exercise 3: SSH Service

### ssh -p 2222 labuser@localhost

```
labuser@localhost's password: [enter: labpass]
Welcome to Alpine!
...
```

### Paramiko selftest

```
[OK] Connected successfully
[CMD] hostname
  <container_id>
[OK] All commands executed successfully
```

## Exercise 4: FTP Service

### FTP client output

```
[OK] Connected successfully
[BANNER] Week 10 FTP server ready.
[DIR] Directory listing:
      drwxr-xr-x   uploads
      drwxr-xr-x   downloads
      -rw-r--r--   welcome.txt
[OK] FTP demo completed successfully
```

## Exercise 5: HTTPS Selftest

```
[OK] HTTPS selftest passed
```

The selftest creates a resource, lists it, updates it, and deletes it.

## Exercise 6: REST Maturity Levels

### Level 0 (RPC)

Request:
```json
POST /level0/service
{"action": "list_users"}
```

Response:
```json
{"users": [{"id": 1, "name": "Alice Example", "email": "alice@example.test"}, ...]}
```

### Level 3 (HATEOAS)

Response includes `_links`:
```json
{
  "users": [...],
  "_links": {
    "self": "/level3/users"
  }
}
```

## Packet Capture Evidence

### DNS Query

```
Frame N: 78 bytes
Ethernet II, Src: ..., Dst: ...
Internet Protocol Version 4, Src: 127.0.0.1, Dst: 127.0.0.1
User Datagram Protocol, Src Port: ..., Dst Port: 5353
Domain Name System (query)
    Transaction ID: ...
    Flags: 0x0100 Standard query
    Questions: 1
    Queries
        myservice.lab.local: type A, class IN
```

### HTTP Request

```
GET /hello.txt HTTP/1.1
Host: localhost:8000
User-Agent: curl/...
Accept: */*
```

### SSH Handshake

Initial packets should show SSH version exchange:
```
SSH-2.0-OpenSSH_...
```

After key exchange, payload is encrypted and not readable.

---

*NETWORKING class - ASE, Informatics | by Revolvix*
