# 🧩 Parsons Problems — Week 12
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> **Topic:** Email Protocols and Remote Procedure Call  
> Reorder the code blocks to create a working solution.

---

## Problem P1: SMTP Client Dialogue

### Task

Arrange the code blocks to create a function that sends an email via SMTP. The function should connect, send the envelope and message, then disconnect properly.

### Scrambled Blocks

```python
# Block A
    sock.sendall(b"QUIT\r\n")
    sock.recv(1024)
    sock.close()

# Block B
def send_email(host, port, sender, recipient, subject, body):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

# Block C
    # Send message body and terminator
    message = f"Subject: {subject}\r\n\r\n{body}\r\n.\r\n"
    sock.sendall(message.encode())
    sock.recv(1024)  # 250 OK

# Block D
    # Receive greeting
    sock.recv(1024)  # 220 greeting

# Block E
    # Send envelope
    sock.sendall(f"MAIL FROM:<{sender}>\r\n".encode())
    sock.recv(1024)  # 250 OK
    sock.sendall(f"RCPT TO:<{recipient}>\r\n".encode())
    sock.recv(1024)  # 250 OK

# Block F
    # Start data transfer
    sock.sendall(b"DATA\r\n")
    sock.recv(1024)  # 354 Start mail input

# Block G
    # Send EHLO
    sock.sendall(b"EHLO client.local\r\n")
    sock.recv(1024)  # 250 OK

# Block H (DISTRACTOR - not needed)
    # Send HELO instead of EHLO
    sock.sendall(b"HELO client\r\n")
    sock.recv(1024)
```

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block B — Function definition and connection
def send_email(host, port, sender, recipient, subject, body):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

# Block D — Receive greeting
    # Receive greeting
    sock.recv(1024)  # 220 greeting

# Block G — Send EHLO
    # Send EHLO
    sock.sendall(b"EHLO client.local\r\n")
    sock.recv(1024)  # 250 OK

# Block E — Send envelope
    # Send envelope
    sock.sendall(f"MAIL FROM:<{sender}>\r\n".encode())
    sock.recv(1024)  # 250 OK
    sock.sendall(f"RCPT TO:<{recipient}>\r\n".encode())
    sock.recv(1024)  # 250 OK

# Block F — Start DATA
    # Start data transfer
    sock.sendall(b"DATA\r\n")
    sock.recv(1024)  # 354 Start mail input

# Block C — Send message body
    # Send message body and terminator
    message = f"Subject: {subject}\r\n\r\n{body}\r\n.\r\n"
    sock.sendall(message.encode())
    sock.recv(1024)  # 250 OK

# Block A — QUIT and close
    sock.sendall(b"QUIT\r\n")
    sock.recv(1024)
    sock.close()
```

**Note:** Block H is a distractor — EHLO (Block G) is preferred over HELO as it enables SMTP extensions.

**SMTP Sequence:** Connect → Greeting → EHLO → MAIL FROM → RCPT TO → DATA → Message → QUIT

</details>

---

## Problem P2: JSON-RPC Request Builder

### Task

Arrange the code blocks to create a function that builds and sends a JSON-RPC request, handling both success and error responses.

### Scrambled Blocks

```python
# Block A
    if "error" in response:
        raise Exception(f"RPC Error: {response['error']['message']}")
    return response.get("result")

# Block B
def call_rpc(url, method, params):
    request_id = random.randint(1, 10000)

# Block C
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

# Block D
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": request_id
    }

# Block E
    response = response.json()

# Block F
    headers = {"Content-Type": "application/json"}

# Block G (DISTRACTOR - not needed)
    # Add authentication header
    headers["Authorization"] = "Bearer token123"

# Block H (DISTRACTOR - not needed)
    payload["version"] = "1.0"  # Wrong field name
```

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block B — Function definition
def call_rpc(url, method, params):
    request_id = random.randint(1, 10000)

# Block D — Build payload
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": request_id
    }

# Block F — Set headers
    headers = {"Content-Type": "application/json"}

# Block C — Send request
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

# Block E — Parse JSON response
    response = response.json()

# Block A — Handle result or error
    if "error" in response:
        raise Exception(f"RPC Error: {response['error']['message']}")
    return response.get("result")
```

**Distractors:**
- Block G: Authentication is not part of JSON-RPC spec (transport concern)
- Block H: `"version"` is wrong — JSON-RPC uses `"jsonrpc": "2.0"`

</details>

---

## Problem P3: gRPC Service Definition

### Task

Arrange the blocks to create a valid Protocol Buffer definition for a calculator service with Add, Subtract, Multiply and Divide methods.

### Scrambled Blocks

```protobuf
// Block A
service Calculator {
    rpc Add(CalcRequest) returns (CalcResponse);
    rpc Subtract(CalcRequest) returns (CalcResponse);
    rpc Multiply(CalcRequest) returns (CalcResponse);
    rpc Divide(CalcRequest) returns (CalcResponse);
}

// Block B
message CalcResponse {
    double result = 1;
    string error = 2;
}

// Block C
syntax = "proto3";

// Block D
message CalcRequest {
    double a = 1;
    double b = 2;
}

// Block E
package calculator;

// Block F (DISTRACTOR - not needed)
option java_package = "com.example.calculator";

// Block G (DISTRACTOR - wrong syntax)
message CalcRequest {
    required double a = 1;  // 'required' is proto2, not proto3
    required double b = 2;
}
```

### Correct Order

<details>
<summary>Click to reveal</summary>

```protobuf
// Block C — Syntax declaration (must be first)
syntax = "proto3";

// Block E — Package declaration
package calculator;

// Block D — Request message
message CalcRequest {
    double a = 1;
    double b = 2;
}

// Block B — Response message
message CalcResponse {
    double result = 1;
    string error = 2;
}

// Block A — Service definition
service Calculator {
    rpc Add(CalcRequest) returns (CalcResponse);
    rpc Subtract(CalcRequest) returns (CalcResponse);
    rpc Multiply(CalcRequest) returns (CalcResponse);
    rpc Divide(CalcRequest) returns (CalcResponse);
}
```

**Distractors:**
- Block F: Java-specific option, not needed for basic definition
- Block G: `required` keyword is proto2 syntax; proto3 has no required/optional

**Key rules:**
1. `syntax` must be the first non-comment line
2. Messages must be defined before the service that uses them
3. Field tags (1, 2) are wire format identifiers, not defaults

</details>

---

## Problem P4: SMTP Response Parser

### Task

Arrange the code blocks to create a function that parses SMTP responses, handling both single-line and multi-line responses.

### Scrambled Blocks

```python
# Block A
def parse_smtp_response(sock):
    lines = []
    
# Block B
    while True:
        line = sock.recv(1024).decode().strip()
        lines.append(line)

# Block C
        # Check if this is the last line (no hyphen after code)
        if len(line) >= 4 and line[3] != '-':
            break

# Block D
    # Extract code from first line
    code = int(lines[0][:3])
    
# Block E
    # Combine all message text
    message = '\n'.join(line[4:] for line in lines)
    return code, message

# Block F (DISTRACTOR - incomplete)
    return lines[0][:3]  # Only returns code as string, loses message

# Block G (DISTRACTOR - wrong logic)
        if line.endswith('\n'):  # Wrong check for multi-line
            break
```

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block A — Function definition and initialise list
def parse_smtp_response(sock):
    lines = []
    
# Block B — Receive loop
    while True:
        line = sock.recv(1024).decode().strip()
        lines.append(line)

# Block C — Check for continuation (hyphen means more lines)
        # Check if this is the last line (no hyphen after code)
        if len(line) >= 4 and line[3] != '-':
            break

# Block D — Extract numeric code
    # Extract code from first line
    code = int(lines[0][:3])
    
# Block E — Combine messages
    # Combine all message text
    message = '\n'.join(line[4:] for line in lines)
    return code, message
```

**Distractors:**
- Block F: Returns only code string, loses the message content
- Block G: Checking for `\n` is wrong; multi-line is indicated by hyphen after code

**SMTP Multi-line Response Format:**
```
250-First line of response
250-Second line continues
250 Last line (space instead of hyphen)
```

</details>

---

## Problem P5: RPC Benchmark Function

### Task

Arrange the code blocks to create a function that benchmarks RPC call latency.

### Scrambled Blocks

```python
# Block A
def benchmark_rpc(url, method, params, iterations=100):
    latencies = []

# Block B
    for _ in range(iterations):
        start = time.perf_counter()

# Block C
        # Make the RPC call
        response = requests.post(url, json={
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        })

# Block D
        end = time.perf_counter()
        latencies.append((end - start) * 1000)  # Convert to ms

# Block E
    return {
        "min": min(latencies),
        "max": max(latencies),
        "avg": sum(latencies) / len(latencies),
        "iterations": iterations
    }

# Block F (DISTRACTOR - wrong timing)
        latencies.append(response.elapsed.total_seconds())
        # Wrong: measures server time, not round-trip

# Block G (DISTRACTOR - missing conversion)
        latencies.append(end - start)  # Seconds, not milliseconds
```

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block A — Function definition
def benchmark_rpc(url, method, params, iterations=100):
    latencies = []

# Block B — Start iteration and timing
    for _ in range(iterations):
        start = time.perf_counter()

# Block C — Make the RPC call
        # Make the RPC call
        response = requests.post(url, json={
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        })

# Block D — End timing and record
        end = time.perf_counter()
        latencies.append((end - start) * 1000)  # Convert to ms

# Block E — Return statistics
    return {
        "min": min(latencies),
        "max": max(latencies),
        "avg": sum(latencies) / len(latencies),
        "iterations": iterations
    }
```

**Distractors:**
- Block F: `response.elapsed` only measures server processing time, not network round-trip
- Block G: Missing millisecond conversion makes results hard to interpret

**Key insight:** Use `time.perf_counter()` for high-resolution timing and measure the complete round-trip including network latency.

</details>

---

## Tips for Parsons Problems

1. **Identify the entry point:** Look for function definitions or required first statements (like `syntax` in protobuf)
2. **Follow data flow:** Variables must be defined before use
3. **Look for control flow:** Loops need setup before the body, cleanup after
4. **Spot distractors:** Wrong syntax, incomplete logic, or unnecessary code
5. **Check language conventions:** Proto3 vs proto2, Python 3 vs 2, etc.

---

## See Also

- `code_tracing.md` — Trace execution exercises
- `misconceptions.md` — Common errors explained
- `pair_programming_guide.md` — Collaborative exercises

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
