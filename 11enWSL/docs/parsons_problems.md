# 🧩 Parsons Problems — Week 11
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Reorder the scrambled code blocks to create a working solution. This builds understanding of code structure without the cognitive load of syntax.

---

## Problem P1: Build a DNS Query Packet

**LO Reference:** LO1, LO2  
**Difficulty:** Intermediate

### Task

Arrange the code blocks to create a function that builds a valid DNS query packet for an A record lookup. The function should:
1. Generate a random transaction ID
2. Set appropriate flags (recursion desired)
3. Encode the domain name
4. Add the question section

### Scrambled Blocks

```python
# Block A
    return header + question

# Block B
def build_dns_query(domain: str) -> bytes:

# Block C
    question = encode_domain_name(domain)
    question += struct.pack(">HH", 1, 1)  # QTYPE=A, QCLASS=IN

# Block D
    flags = 0x0100  # RD (Recursion Desired) flag
    header = struct.pack(">HHHHHH", trans_id, flags, 1, 0, 0, 0)

# Block E
    trans_id = random.randint(0, 0xFFFF)

# Block F (DISTRACTOR — not needed)
    socket.setdefaulttimeout(5.0)

# Block G (DISTRACTOR — not needed)
    response = socket.recv(4096)
```

### Hints

- Function definition must come first
- You need a transaction ID before building the header
- The header must be built before the question section
- The return statement must be last
- Two blocks are distractors (not needed for this function)

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block B — Function definition
def build_dns_query(domain: str) -> bytes:

# Block E — Generate transaction ID
    trans_id = random.randint(0, 0xFFFF)

# Block D — Build header
    flags = 0x0100  # RD (Recursion Desired) flag
    header = struct.pack(">HHHHHH", trans_id, flags, 1, 0, 0, 0)

# Block C — Build question section
    question = encode_domain_name(domain)
    question += struct.pack(">HH", 1, 1)  # QTYPE=A, QCLASS=IN

# Block A — Return complete packet
    return header + question
```

**Distractors explained:**
- Block F (`socket.setdefaulttimeout`) — This configures socket behaviour, not packet building
- Block G (`socket.recv`) — This receives data, but our function only builds the query

**Key insight:** DNS packet structure is Header (12 bytes) + Question section. The header contains the transaction ID, flags and section counts.

</details>

---

## Problem P2: Implement Weighted Round-Robin Selection

**LO Reference:** LO3  
**Difficulty:** Intermediate

### Task

Arrange the code blocks to implement a weighted round-robin backend selector. The function should:
1. Build an expanded list where each backend appears `weight` times
2. Select the next backend from this list
3. Update the index for the next call
4. Handle wraparound when reaching the end

### Scrambled Blocks

```python
# Block A
        return None

# Block B
class WeightedRoundRobin:

# Block C
    def select(self) -> str:
        if not self._expanded:

# Block D
    def __init__(self, backends: dict):
        """backends = {"web1": 3, "web2": 2, "web3": 1}"""
        self._expanded = []
        for name, weight in backends.items():
            self._expanded.extend([name] * weight)
        self._index = 0

# Block E
        backend = self._expanded[self._index]
        self._index = (self._index + 1) % len(self._expanded)
        return backend

# Block F (DISTRACTOR)
        self._expanded.sort()

# Block G (DISTRACTOR)
        return random.choice(self._expanded)
```

### Hints

- Class definition must come first
- `__init__` builds the expanded list on object creation
- `select` method returns one backend and advances the index
- Handle the empty list case before accessing elements
- Two blocks are distractors

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block B — Class definition
class WeightedRoundRobin:

# Block D — Constructor builds expanded list
    def __init__(self, backends: dict):
        """backends = {"web1": 3, "web2": 2, "web3": 1}"""
        self._expanded = []
        for name, weight in backends.items():
            self._expanded.extend([name] * weight)
        self._index = 0

# Block C — Select method signature and empty check
    def select(self) -> str:
        if not self._expanded:

# Block A — Return None for empty list
            return None

# Block E — Main selection logic
        backend = self._expanded[self._index]
        self._index = (self._index + 1) % len(self._expanded)
        return backend
```

**Expanded list for {"web1": 3, "web2": 2, "web3": 1}:**
```python
["web1", "web1", "web1", "web2", "web2", "web3"]
```

**Selection sequence:** web1 → web1 → web1 → web2 → web2 → web3 → web1 → ...

**Distractors explained:**
- Block F (`sort`) — Sorting would group backends together, changing the distribution pattern
- Block G (`random.choice`) — This would give random selection, not round-robin

</details>

---

## Problem P3: Parse HTTP Response Status

**LO Reference:** LO3, LO4  
**Difficulty:** Basic

### Task

Arrange the code blocks to create a function that extracts the status code from an HTTP response. The function should:
1. Find the end of the status line
2. Split the status line into components
3. Extract and return the numeric status code
4. Handle malformed responses gracefully

### Scrambled Blocks

```python
# Block A
def parse_status_code(response: bytes) -> int:

# Block B
    try:
        parts = status_line.split()
        return int(parts[1])
    except (IndexError, ValueError):
        return 0

# Block C
    first_line_end = response.find(b"\r\n")
    if first_line_end == -1:
        return 0

# Block D
    status_line = response[:first_line_end].decode("ascii", errors="replace")

# Block E (DISTRACTOR)
    headers = response.split(b"\r\n\r\n")[0]

# Block F (DISTRACTOR)
    return response.status_code
```

### Hints

- Function definition comes first
- Find the line ending before extracting the line
- Decode bytes to string before splitting
- The status code is the second word (index 1) in the status line
- Handle errors to avoid crashes on malformed input

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block A — Function definition
def parse_status_code(response: bytes) -> int:

# Block C — Find end of first line
    first_line_end = response.find(b"\r\n")
    if first_line_end == -1:
        return 0

# Block D — Extract and decode status line
    status_line = response[:first_line_end].decode("ascii", errors="replace")

# Block B — Parse and return status code
    try:
        parts = status_line.split()
        return int(parts[1])
    except (IndexError, ValueError):
        return 0
```

**Example:**
```
Input: b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html>..."
Status line: "HTTP/1.1 200 OK"
Parts: ["HTTP/1.1", "200", "OK"]
Result: 200
```

**Distractors explained:**
- Block E — This splits headers from body, but we only need the first line
- Block F — This assumes a response object with `.status_code` attribute (like requests library), but we are parsing raw bytes

</details>

---

## Problem P4: Check Port Availability

**LO Reference:** LO1, LO5  
**Difficulty:** Basic

### Task

Arrange the code blocks to create a function that checks if a TCP port is available (not in use). The function should:
1. Create a socket
2. Try to connect to the port
3. Return True if connection succeeds (port is in use)
4. Return False if connection fails (port is available)
5. Always close the socket

### Scrambled Blocks

```python
# Block A
def is_port_in_use(host: str, port: int, timeout: float = 1.0) -> bool:

# Block B
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

# Block C
    try:
        result = sock.connect_ex((host, port))
        return result == 0
    finally:
        sock.close()

# Block D (DISTRACTOR)
    sock.bind((host, port))
    return False

# Block E (DISTRACTOR)
    sock.listen(1)
    return True
```

### Hints

- Function definition first
- Create and configure socket before using it
- `connect_ex` returns 0 on success, error code on failure
- Use `finally` to ensure socket is always closed
- Two blocks are for server-side operations (not what we need)

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block A — Function definition
def is_port_in_use(host: str, port: int, timeout: float = 1.0) -> bool:

# Block B — Create and configure socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

# Block C — Try connection and cleanup
    try:
        result = sock.connect_ex((host, port))
        return result == 0
    finally:
        sock.close()
```

**Key insight:** `connect_ex` is like `connect` but returns an error code instead of raising an exception. Return code 0 means success (something is listening on that port).

**Distractors explained:**
- Block D (`bind`) — This is for creating a server, not checking if a port is in use
- Block E (`listen`) — This is also server-side; we are acting as a client to test connectivity

</details>

---

## Problem P5: Implement Passive Health Check

**LO Reference:** LO3, LO7  
**Difficulty:** Advanced

### Task

Arrange the code blocks to create a passive health check function. The function should:
1. Track failed request counts per backend
2. Mark backend as unhealthy after max_fails failures
3. Recover backend after fail_timeout seconds
4. Return whether a backend is healthy

### Scrambled Blocks

```python
# Block A
def is_healthy(self, backend: str) -> bool:

# Block B
class PassiveHealthCheck:
    def __init__(self, max_fails: int = 2, fail_timeout: float = 10.0):
        self.max_fails = max_fails
        self.fail_timeout = fail_timeout
        self._failures = {}  # backend -> (count, last_fail_time)

# Block C
    # Check if backend has recovered (timeout expired)
    if time.time() - last_fail_time > self.fail_timeout:
        self._failures[backend] = (0, 0)
        return True

# Block D
    count, last_fail_time = self._failures.get(backend, (0, 0))
    if count < self.max_fails:
        return True

# Block E
    return False

# Block F (DISTRACTOR)
    requests.get(f"http://{backend}/health", timeout=1)
    return True

# Block G (DISTRACTOR)
    self._failures[backend] = count + 1
```

### Hints

- Class definition and `__init__` come first
- The `is_healthy` method checks backend status
- Check failure count before checking recovery
- Recovery check compares current time with last failure
- Two blocks are for different functionality (active health checks, recording failures)

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block B — Class definition and constructor
class PassiveHealthCheck:
    def __init__(self, max_fails: int = 2, fail_timeout: float = 10.0):
        self.max_fails = max_fails
        self.fail_timeout = fail_timeout
        self._failures = {}  # backend -> (count, last_fail_time)

# Block A — Method signature
def is_healthy(self, backend: str) -> bool:

# Block D — Get failure info and check count
    count, last_fail_time = self._failures.get(backend, (0, 0))
    if count < self.max_fails:
        return True

# Block C — Check for recovery after timeout
    # Check if backend has recovered (timeout expired)
    if time.time() - last_fail_time > self.fail_timeout:
        self._failures[backend] = (0, 0)
        return True

# Block E — Backend still unhealthy
    return False
```

**Logic flow:**
1. Get failure count and last failure time
2. If count < max_fails → healthy
3. If count >= max_fails but timeout expired → reset and mark healthy
4. Otherwise → unhealthy

**Distractors explained:**
- Block F (`requests.get`) — This is an active health check (probing the backend), not passive
- Block G (`count + 1`) — This records a failure but does not check health status

</details>

---

## LO Traceability Matrix for Parsons Problems

| Problem | LOs Covered | Difficulty | Core Concept |
|---------|-------------|------------|--------------|
| P1 | LO1, LO2 | Intermediate | DNS packet structure |
| P2 | LO3 | Intermediate | Weighted round-robin algorithm |
| P3 | LO3, LO4 | Basic | HTTP response parsing |
| P4 | LO1, LO5 | Basic | Socket programming |
| P5 | LO3, LO7 | Advanced | Health check implementation |

---

## Tips for Parsons Problems

1. **Find the boundaries:** Look for function definitions, class definitions and return statements — these anchor the structure
2. **Identify dependencies:** If block X uses a variable defined in block Y, Y must come before X
3. **Spot distractors:** Blocks that use different patterns or solve a different problem are likely distractors
4. **Check indentation:** In Python, indentation determines scope — make sure methods are inside classes
5. **Trace execution:** After ordering, mentally execute the code to verify it makes sense

---

## Additional Challenge

Try creating your own Parsons problem for a peer! Good candidates:
- Backend health check implementation
- DNS response parsing
- Load balancer failover logic

---

*NETWORKING class - ASE, CSIE | Computer Networks Laboratory*  
*Week 11: Application Protocols — FTP, DNS, SSH and Load Balancing*
