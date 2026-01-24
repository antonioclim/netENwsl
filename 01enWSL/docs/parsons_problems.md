# 🧩 Parsons Problems — Week 1
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Reorder the scrambled code blocks to create a working solution.
> This exercise builds your understanding of code structure without the cognitive load of syntax.

---

## Problem P1: TCP Port Checker

### Task

Create a function that checks if a TCP port is open on a given host. The function should:
1. Create a TCP socket
2. Set a timeout
3. Attempt connection
4. Return True if open, False otherwise
5. Always close the socket

### Scrambled Blocks

```python
# Block A
    return result == 0

# Block B
def is_port_open(host: str, port: int) -> bool:

# Block C
    sock.settimeout(2)

# Block D
    result = sock.connect_ex((host, port))

# Block E
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Block F
    sock.close()

# Block G (DISTRACTOR - not needed)
    sock.bind(('0.0.0.0', 0))

# Block H (DISTRACTOR - not needed)
    sock.listen(1)
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block B
def is_port_open(host: str, port: int) -> bool:

# Block E
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Block C
    sock.settimeout(2)

# Block D
    result = sock.connect_ex((host, port))

# Block F
    sock.close()

# Block A
    return result == 0
```

**Distractors explained:**
- Block G (`bind`) is for servers binding to a local port, not clients connecting
- Block H (`listen`) is for servers waiting for connections, not clients

**Key insight:** `connect_ex()` returns 0 on success, error code otherwise. Always close sockets to free resources.

</details>

---

## Problem P2: Ping Output Parser

### Task

Create a function that extracts the average RTT from ping output. The function should:
1. Define the regex pattern for RTT statistics
2. Search the output for the pattern
3. Extract and return the average value
4. Handle the case when no match is found

### Scrambled Blocks

```python
# Block A
    return None

# Block B
def extract_avg_rtt(ping_output: str) -> float | None:

# Block C
    match = re.search(pattern, ping_output)

# Block D
    if match:
        return float(match.group(1))

# Block E
    pattern = r"rtt min/avg/max/mdev = [^/]+/([^/]+)/"

# Block F (DISTRACTOR - wrong pattern)
    pattern = r"time=(\d+\.?\d*) ms"

# Block G (DISTRACTOR - wrong return)
    return match.group(0)
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block B
def extract_avg_rtt(ping_output: str) -> float | None:

# Block E
    pattern = r"rtt min/avg/max/mdev = [^/]+/([^/]+)/"

# Block C
    match = re.search(pattern, ping_output)

# Block D
    if match:
        return float(match.group(1))

# Block A
    return None
```

**Distractors explained:**
- Block F extracts individual ping times, not the summary average
- Block G returns `group(0)` (entire match) instead of `group(1)` (captured value)

**Key insight:** The summary line format is `rtt min/avg/max/mdev = X/Y/Z/W ms` where Y is the average.

</details>

---

## Problem P3: Docker Container Status Check

### Task

Create a function that checks if a Docker container is running. The function should:
1. Build the docker inspect command
2. Run the command and capture output
3. Check the return code
4. Parse and return the running state

### Scrambled Blocks

```python
# Block A
    return stdout.strip().lower() == "true"

# Block B
def is_container_running(name: str) -> bool:

# Block C
    result = subprocess.run(cmd, capture_output=True, text=True)

# Block D
    if result.returncode != 0:
        return False

# Block E
    cmd = ["docker", "inspect", "--format", "{{.State.Running}}", name]

# Block F
    stdout = result.stdout

# Block G (DISTRACTOR - wrong command)
    cmd = ["docker", "ps", "--filter", f"name={name}"]

# Block H (DISTRACTOR - wrong check)
    if "running" in stdout.lower():
        return True
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block B
def is_container_running(name: str) -> bool:

# Block E
    cmd = ["docker", "inspect", "--format", "{{.State.Running}}", name]

# Block C
    result = subprocess.run(cmd, capture_output=True, text=True)

# Block D
    if result.returncode != 0:
        return False

# Block F
    stdout = result.stdout

# Block A
    return stdout.strip().lower() == "true"
```

**Distractors explained:**
- Block G uses `docker ps` which lists containers but requires parsing tabular output
- Block H checks for substring "running" which is fragile and incorrect

**Key insight:** `docker inspect --format` extracts specific fields directly, avoiding parsing complexity.

</details>

---

## Problem P4: Network Interface Extractor

### Task

Create a function that extracts all IPv4 addresses from `ip addr` output. The function should:
1. Define the regex pattern for IPv4 addresses
2. Find all matches in the output
3. Return a list of IP addresses (without subnet mask)

### Scrambled Blocks

```python
# Block A
    return [match.group(1) for match in matches]

# Block B
def get_ipv4_addresses(ip_output: str) -> list[str]:

# Block C
    matches = re.finditer(pattern, ip_output)

# Block D
    pattern = r"inet (\d+\.\d+\.\d+\.\d+)"

# Block E (DISTRACTOR - includes subnet)
    pattern = r"inet (\d+\.\d+\.\d+\.\d+/\d+)"

# Block F (DISTRACTOR - wrong method)
    matches = re.match(pattern, ip_output)
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block B
def get_ipv4_addresses(ip_output: str) -> list[str]:

# Block D
    pattern = r"inet (\d+\.\d+\.\d+\.\d+)"

# Block C
    matches = re.finditer(pattern, ip_output)

# Block A
    return [match.group(1) for match in matches]
```

**Distractors explained:**
- Block E includes the subnet mask (`/24`), which the task says to exclude
- Block F uses `re.match()` which only matches at string start, not `re.finditer()` for all occurrences

**Key insight:** `re.finditer()` returns an iterator of all matches, allowing extraction of multiple IPs.

</details>

---

## Self-Assessment

After completing these problems, you should be able to:

- [ ] Structure socket operations in the correct order
- [ ] Build regex patterns for network output parsing
- [ ] Use subprocess correctly for Docker commands
- [ ] Distinguish between `re.match()`, `re.search()`, and `re.finditer()`

**Scoring:**
- 4/4 correct without hints: Excellent — ready for implementation exercises
- 2-3/4 correct: Good — review the concepts you missed
- 0-1/4 correct: Need more practice — re-read the code tracing exercises first

---

*NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim*
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
