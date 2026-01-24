# 🧩 Parsons Problems — Week 14

> NETWORKING class — ASE, CSIE | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

Reorder the scrambled code blocks to create a working solution. Some problems include distractor blocks that should not be used.

---

## Problem P1: TCP Port Checker

### Task

Create a function that checks if a TCP port is open. The function should create a socket, set timeout, attempt to connect, return True/False and always close the socket.

### Scrambled Blocks

```python
# Block A
    return True

# Block B
def check_port(host: str, port: int, timeout: int = 3) -> bool:

# Block C
    sock.settimeout(timeout)

# Block D
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Block E
    try:
        sock.connect((host, port))

# Block F
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False

# Block G
    finally:
        sock.close()

# Block H (DISTRACTOR)
    sock.bind(('', 0))
```

<details>
<summary>Click to reveal correct order</summary>

**B → D → C → E → A → F → G**

Block H is a distractor — `bind()` is for servers, not clients.

</details>

---

## Problem P2: HTTP GET Request

### Task

Create a function that sends an HTTP GET request and returns the response body.

### Scrambled Blocks

```python
# Block A
def http_get(host: str, port: int, path: str) -> str:

# Block B
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

# Block C
    sock.connect((host, port))

# Block D
    sock.sendall(request.encode())

# Block E
    response = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk

# Block F
    sock.close()

# Block G
    body = response.decode().split("\r\n\r\n", 1)[1]
    return body

# Block H
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Block I (DISTRACTOR)
    response = sock.recv(4096)  # Only receives once
```

<details>
<summary>Click to reveal correct order</summary>

**A → H → C → B → D → E → F → G**

Block I is a distractor — single recv may miss data if response > 4096 bytes.

</details>

---

## Problem P3: Container Status Checker

### Task

Create a function that checks if a Docker container is running using subprocess.

### Scrambled Blocks

```python
# Block A
def is_container_running(name: str) -> bool:

# Block B
    cmd = ["docker", "ps", "-q", "-f", f"name={name}"]

# Block C
    result = subprocess.run(cmd, capture_output=True, text=True)

# Block D
    return bool(result.stdout.strip())

# Block E (DISTRACTOR)
    return result.returncode == 0  # Always 0 even if no match
```

<details>
<summary>Click to reveal correct order</summary>

**A → B → C → D**

Block E is a distractor — `docker ps` returns 0 even when no containers match.

</details>

---

## Problem P4: Round-Robin Backend Selector

### Task

Create a class that selects backends in round-robin order with wrap-around.

### Scrambled Blocks

```python
# Block A
class RoundRobinSelector:

# Block B
    def __init__(self, backends: list):
        self.backends = backends
        self.index = 0

# Block C
    def next(self) -> str:

# Block D
        if not self.backends:
            return None

# Block E
        backend = self.backends[self.index]

# Block F
        self.index = (self.index + 1) % len(self.backends)

# Block G
        return backend

# Block H (DISTRACTOR)
        self.index = self.index + 1  # No modulo
```

<details>
<summary>Click to reveal correct order</summary>

**A → B → C → D → E → F → G**

Block H is a distractor — no modulo means IndexError after last element.

</details>

---

## Problem P5: Parse Docker Network Output

### Task

Create a function that parses `docker network inspect` JSON to extract container IPs.

### Scrambled Blocks

```python
# Block A
def get_network_containers(network_name: str) -> dict:

# Block B
    cmd = ["docker", "network", "inspect", network_name]

# Block C
    result = subprocess.run(cmd, capture_output=True, text=True)

# Block D
    if result.returncode != 0:
        return {}

# Block E
    data = json.loads(result.stdout)

# Block F
    containers = data[0].get("Containers", {})

# Block G
    ip_map = {}
    for container_id, info in containers.items():
        name = info.get("Name", container_id)
        ip = info.get("IPv4Address", "").split("/")[0]
        ip_map[name] = ip

# Block H
    return ip_map

# Block I (DISTRACTOR)
    containers = data["Containers"]  # data is a list, not dict
```

<details>
<summary>Click to reveal correct order</summary>

**A → B → C → D → E → F → G → H**

Block I is a distractor — `docker network inspect` returns a JSON array, so we need `data[0]`.

</details>

---

*Document version: 2.0 | Week 14: Integrated Recap | January 2025*
