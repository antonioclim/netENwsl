# 🔍 Code Tracing Exercises — Week 14

> NETWORKING class — ASE, CSIE | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

Trace through each code snippet mentally before running it. Write down your predicted values, then verify.

---

## Exercise T1: TCP Socket Connection

### Code

```python
import socket

def connect_to_server(host: str, port: int) -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    
    result = "unknown"
    try:
        sock.connect((host, port))
        result = "connected"
    except socket.timeout:
        result = "timeout"
    except ConnectionRefusedError:
        result = "refused"
    except OSError as e:
        result = f"error: {e}"
    finally:
        sock.close()
    
    return result

# Trace these calls (assuming lb container is running on 172.21.0.10:80)
status1 = connect_to_server("172.21.0.10", 80)     # Line A
status2 = connect_to_server("172.21.0.10", 9999)  # Line B
status3 = connect_to_server("10.255.255.1", 80)   # Line C
```

### Questions

1. **Line A:** What is the value of `status1`?
2. **Line B:** What is the value of `status2`? (Port 9999 has no service)
3. **Line C:** What is the value of `status3`? (IP is unreachable)

<details>
<summary>Click to reveal solution</summary>

| Call | Exception raised? | `result` value |
|------|-------------------|----------------|
| Line A | No | `"connected"` |
| Line B | `ConnectionRefusedError` | `"refused"` |
| Line C | `socket.timeout` or `OSError` | `"timeout"` or `"error: ..."` |

</details>

---

## Exercise T2: HTTP Response Parsing

### Code

```python
def parse_http_response(raw: str) -> dict:
    lines = raw.split("\r\n")
    
    # Parse status line
    status_line = lines[0]
    parts = status_line.split(" ", 2)
    version = parts[0]
    code = int(parts[1])
    reason = parts[2] if len(parts) > 2 else ""
    
    # Parse headers
    headers = {}
    i = 1
    while i < len(lines) and lines[i] != "":
        key, value = lines[i].split(": ", 1)
        headers[key] = value
        i += 1
    
    # Body is everything after blank line
    body = "\r\n".join(lines[i+1:])
    
    return {"version": version, "code": code, "headers": headers, "body": body}

# Trace with this input
raw_response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nX-Backend: app1\r\n\r\n<h1>Hello</h1>"
result = parse_http_response(raw_response)
```

### Questions

1. What is `result["code"]`?
2. What is `result["headers"]["X-Backend"]`?
3. What is `result["body"]`?

<details>
<summary>Click to reveal solution</summary>

1. `result["code"]` = `200`
2. `result["headers"]["X-Backend"]` = `"app1"`
3. `result["body"]` = `"<h1>Hello</h1>"`

</details>

---

## Exercise T3: Round-Robin Distribution

### Code

```python
class RoundRobinBalancer:
    def __init__(self, backends: list):
        self.backends = backends
        self.index = 0
    
    def get_next(self) -> str:
        if not self.backends:
            return None
        backend = self.backends[self.index]
        self.index = (self.index + 1) % len(self.backends)
        return backend

# Create balancer and make requests
lb = RoundRobinBalancer(["app1", "app2", "app3"])
r1 = lb.get_next()  # Call 1
r2 = lb.get_next()  # Call 2
r3 = lb.get_next()  # Call 3
r4 = lb.get_next()  # Call 4
r5 = lb.get_next()  # Call 5
```

### Questions

1. What is `r1`?
2. What is `r3`?
3. What is `r5`?
4. What is `lb.index` after all 5 calls?

<details>
<summary>Click to reveal solution</summary>

1. `r1` = `"app1"`
2. `r3` = `"app3"`
3. `r5` = `"app2"`
4. `lb.index` = `2`

**Key insight:** The modulo operator `%` wraps the index back to 0 after reaching the end.

</details>

---

## Exercise T4: Container Health Check

### Code

```python
import subprocess

def check_container(name: str) -> dict:
    status = {"name": name, "running": False, "ip": None}
    
    ps_result = subprocess.run(
        ["docker", "ps", "-q", "-f", f"name={name}"],
        capture_output=True, text=True
    )
    
    if ps_result.stdout.strip():
        status["running"] = True
        inspect_result = subprocess.run(
            ["docker", "inspect", "-f", 
             "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}", name],
            capture_output=True, text=True
        )
        status["ip"] = inspect_result.stdout.strip() or None
    
    return status

# Assume: app1 is running with IP 172.20.0.2
# Assume: app99 does not exist
result1 = check_container("app1")
result2 = check_container("app99")
```

### Questions

1. What is `result1["running"]`?
2. What is `result1["ip"]`?
3. What is `result2["running"]`?
4. What is `result2["ip"]`?

<details>
<summary>Click to reveal solution</summary>

1. `result1["running"]` = `True`
2. `result1["ip"]` = `"172.20.0.2"`
3. `result2["running"]` = `False`
4. `result2["ip"]` = `None`

</details>

---

## Exercise T5: Packet Counter

### Code

```python
def analyse_traffic(packets: list) -> dict:
    stats = {"total": 0, "tcp": 0, "udp": 0, "http": 0, "by_port": {}}
    
    for pkt in packets:
        stats["total"] += 1
        proto = pkt.get("protocol", "unknown")
        if proto == "tcp":
            stats["tcp"] += 1
        elif proto == "udp":
            stats["udp"] += 1
        if pkt.get("http"):
            stats["http"] += 1
        port = pkt.get("dst_port")
        if port:
            stats["by_port"][port] = stats["by_port"].get(port, 0) + 1
    
    return stats

packets = [
    {"protocol": "tcp", "dst_port": 80, "http": True},
    {"protocol": "tcp", "dst_port": 80, "http": True},
    {"protocol": "tcp", "dst_port": 443, "http": False},
    {"protocol": "udp", "dst_port": 53},
    {"protocol": "tcp", "dst_port": 80, "http": True},
]
result = analyse_traffic(packets)
```

### Questions

1. What is `result["total"]`?
2. What is `result["tcp"]`?
3. What is `result["http"]`?
4. What is `result["by_port"][80]`?

<details>
<summary>Click to reveal solution</summary>

1. `result["total"]` = `5`
2. `result["tcp"]` = `4`
3. `result["http"]` = `3`
4. `result["by_port"][80]` = `3`

</details>

---

*Document version: 2.0 | Week 14: Integrated Recap | January 2025*
