# 🧩 Parsons Problems — Week 12
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> **Topic:** Email Protocols and Remote Procedure Call  
> Reorder the code blocks to create a working solution.  
> **Note:** Some problems include distractor blocks (marked with ❌) that should NOT be used.

---

## Problem P1: SMTP Client Dialogue (LO1)

### Task

Arrange the code blocks to create a function that sends an email via SMTP.

**Difficulty:** ⭐⭐ Intermediate  
**Estimated time:** 5 minutes

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
    message = f"Subject: {subject}\r\n\r\n{body}\r\n.\r\n"
    sock.sendall(message.encode())
    sock.recv(1024)

# Block D
    sock.recv(1024)  # 220 greeting

# Block E
    sock.sendall(f"MAIL FROM:<{sender}>\r\n".encode())
    sock.recv(1024)
    sock.sendall(f"RCPT TO:<{recipient}>\r\n".encode())
    sock.recv(1024)

# Block F
    sock.sendall(b"DATA\r\n")
    sock.recv(1024)  # 354 Start mail input

# Block G
    sock.sendall(b"EHLO client.local\r\n")
    sock.recv(1024)

# Block H (DISTRACTOR ❌)
    sock.sendall(b"HELO client\r\n")
    sock.recv(1024)

# Block I (DISTRACTOR ❌)
    sock.sendall(b"DATA\r\n")
    sock.sendall(f"MAIL FROM:<{sender}>\r\n".encode())
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

**Correct sequence: B → D → G → E → F → C → A**

**Why Block H is wrong:** HELO is legacy; EHLO enables extended features.

**Why Block I is wrong:** DATA must come AFTER MAIL FROM and RCPT TO.

</details>

---

## Problem P2: JSON-RPC Request Construction (LO2)

### Task

Arrange the code blocks to construct and send a valid JSON-RPC 2.0 request.

**Difficulty:** ⭐ Basic  
**Estimated time:** 3 minutes

### Scrambled Blocks

```python
# Block A
def call_jsonrpc(url, method, params):

# Block B
    return response.json()

# Block C
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }

# Block D
    headers = {"Content-Type": "application/json"}

# Block E
    response = requests.post(url, json=payload, headers=headers)

# Block F (DISTRACTOR ❌)
    payload = {
        "jsonrpc": "1.0",
        "method": method,
        "params": params
    }

# Block G (DISTRACTOR ❌)
    payload = {
        "method": method,
        "params": params,
        "id": 1
    }
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

**Correct sequence: A → C → D → E → B**

**Why Block F is wrong:** Version must be "2.0", not "1.0".

**Why Block G is wrong:** Missing required "jsonrpc" field.

</details>

---

## Problem P3: RPC Server Setup (LO3)

### Task

Arrange the code blocks to create a simple JSON-RPC server.

**Difficulty:** ⭐⭐⭐ Advanced  
**Estimated time:** 7 minutes

### Scrambled Blocks

```python
# Block A
if __name__ == "__main__":
    server = HTTPServer(("", 6200), JSONRPCHandler)
    server.serve_forever()

# Block B
class JSONRPCHandler(BaseHTTPRequestHandler):

# Block C
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        request = json.loads(body)

# Block D
        method = request.get("method")
        params = request.get("params", [])
        result = self.dispatch(method, params)

# Block E
        response = {"jsonrpc": "2.0", "result": result, "id": request.get("id")}
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

# Block F
    def dispatch(self, method, params):
        if method == "add":
            return params[0] + params[1]
        raise ValueError(f"Unknown method: {method}")

# Block G
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# Block H (DISTRACTOR ❌)
    def do_GET(self):
        content_length = int(self.headers["Content-Length"])

# Block I (DISTRACTOR ❌)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

**Correct sequence: G → B → C → D → E → F → A**

**Why Block H is wrong:** JSON-RPC uses POST, not GET.

**Why Block I is wrong:** Missing Content-Type header.

</details>

---

## Problem P4: curl JSON-RPC Call (LO4)

### Task

Arrange the command-line arguments to construct a valid curl command.

**Difficulty:** ⭐ Basic  
**Estimated time:** 2 minutes

### Scrambled Blocks

```bash
# Block A
curl

# Block B
-X POST

# Block C
http://localhost:6200

# Block D
-H "Content-Type: application/json"

# Block E
-d '{"jsonrpc":"2.0","method":"add","params":[10,32],"id":1}'

# Block F (DISTRACTOR ❌)
-X GET

# Block G (DISTRACTOR ❌)
-H "Content-Type: text/plain"
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

**Correct sequence: A → B → C → D → E**

```bash
curl -X POST http://localhost:6200 -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"add","params":[10,32],"id":1}'
```

</details>

---

## Problem P5: Protocol Comparison Analysis (LO5)

### Task

Arrange the code blocks to create a function that compares response times between JSON-RPC and gRPC.

**Difficulty:** ⭐⭐⭐ Advanced  
**Estimated time:** 8 minutes

### Scrambled Blocks

```python
# Block A
def compare_protocols(iterations=100):
    results = {"jsonrpc": [], "grpc": []}

# Block B
    for _ in range(iterations):
        start = time.perf_counter()
        call_jsonrpc("http://localhost:6200", "add", [10, 32])
        elapsed = time.perf_counter() - start
        results["jsonrpc"].append(elapsed)

# Block C
    channel = grpc.insecure_channel("localhost:6251")
    stub = calculator_pb2_grpc.CalculatorStub(channel)
    for _ in range(iterations):
        start = time.perf_counter()
        stub.Add(calculator_pb2.CalcRequest(a=10, b=32))
        elapsed = time.perf_counter() - start
        results["grpc"].append(elapsed)

# Block D
    for protocol, times in results.items():
        avg = sum(times) / len(times)
        print(f"{protocol}: avg={avg*1000:.2f}ms")

# Block E
    return results

# Block F
import time
import grpc

# Block G (DISTRACTOR ❌)
    for _ in range(iterations):
        call_jsonrpc("http://localhost:6200", "add", [10, 32])
    elapsed = time.perf_counter() - start

# Block H (DISTRACTOR ❌)
    for _ in range(iterations):
        channel = grpc.insecure_channel("localhost:6251")
        stub = calculator_pb2_grpc.CalculatorStub(channel)
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

**Correct sequence: F → A → B → C → D → E**

**Why Block G is wrong:** Timer start is outside the loop.

**Why Block H is wrong:** Channel creation inside loop adds overhead.

</details>

---


## Problem P6: SMTP Response Code Handling (LO1)

### Task

Arrange the code blocks to create a function that checks SMTP response codes.

**Difficulty:** ⭐⭐ Intermediate  
**Estimated time:** 4 minutes

### Scrambled Blocks

```python
# Block A
def check_smtp_response(response_line):
    code = int(response_line[:3])
    message = response_line[4:].strip()

# Block B
    if code >= 500:
        raise SMTPPermanentError(code, message)

# Block C
    if code >= 400:
        raise SMTPTemporaryError(code, message)

# Block D
    if code == 354:
        return "intermediate", message

# Block E
    if code >= 200 and code < 300:
        return "success", message

# Block F
    return "unknown", message

# Block G (DISTRACTOR ❌)
    if code == 250:
        return "intermediate", message

# Block H (DISTRACTOR ❌)
    if code >= 200:
        return "success", message
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

**Correct sequence: A → B → C → D → E → F**

**Why Block G is wrong:** 250 is success, not intermediate. 354 is intermediate.

**Why Block H is wrong:** Does not exclude 3xx, 4xx, 5xx codes.

</details>

---

## Problem P7: XML-RPC Client Call (LO4)

### Task

Arrange the code blocks to create an XML-RPC client function.

**Difficulty:** ⭐ Basic  
**Estimated time:** 3 minutes

### Scrambled Blocks

```python
# Block A
import xmlrpc.client

# Block B
def call_xmlrpc(host, port, method, *args):

# Block C
    url = f"http://{host}:{port}"
    proxy = xmlrpc.client.ServerProxy(url)

# Block D
    func = getattr(proxy, method)
    return func(*args)

# Block E (DISTRACTOR ❌)
    proxy = xmlrpc.client.ServerProxy(url, allow_none=False)
    return proxy.call(method, *args)

# Block F (DISTRACTOR ❌)
    url = f"tcp://{host}:{port}"
    proxy = xmlrpc.client.ServerProxy(url)
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

**Correct sequence: A → B → C → D**

**Why Block E is wrong:** XML-RPC uses attribute access, not a `call()` method.

**Why Block F is wrong:** XML-RPC uses HTTP, not TCP protocol prefix.

</details>

---

## Problem P8: gRPC Service Definition (LO3)

### Task

Arrange the Protocol Buffer definition blocks to create a valid calculator service.

**Difficulty:** ⭐⭐ Intermediate  
**Estimated time:** 4 minutes

### Scrambled Blocks

```protobuf
// Block A
syntax = "proto3";

// Block B
message CalcRequest {
    double a = 1;
    double b = 2;
}

// Block C
message CalcResponse {
    double result = 1;
}

// Block D
service Calculator {
    rpc Add(CalcRequest) returns (CalcResponse);
    rpc Subtract(CalcRequest) returns (CalcResponse);
}

// Block E (DISTRACTOR ❌)
syntax = "proto2";

// Block F (DISTRACTOR ❌)
service Calculator {
    rpc Add(double a, double b) returns (double);
}
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

**Correct sequence: A → B → C → D**

**Why Block E is wrong:** We use proto3, not proto2.

**Why Block F is wrong:** gRPC methods take message types, not primitives directly.

</details>

---

## Problem P9: JSON-RPC Error Response (LO5)

### Task

Arrange the code blocks to create a proper JSON-RPC error response handler.

**Difficulty:** ⭐⭐ Intermediate  
**Estimated time:** 5 minutes

### Scrambled Blocks

```python
# Block A
def build_error_response(request_id, code, message):

# Block B
    return {
        "jsonrpc": "2.0",
        "error": {
            "code": code,
            "message": message
        },
        "id": request_id
    }

# Block C
ERROR_CODES = {
    "parse_error": -32700,
    "invalid_request": -32600,
    "method_not_found": -32601,
    "invalid_params": -32602,
}

# Block D
def handle_error(request, error_type):
    code = ERROR_CODES.get(error_type, -32000)
    return build_error_response(request.get("id"), code, error_type)

# Block E (DISTRACTOR ❌)
    return {
        "jsonrpc": "2.0",
        "error": message,
        "id": request_id
    }

# Block F (DISTRACTOR ❌)
def handle_error(request, error_type):
    return {"error": error_type, "status": 500}
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

**Correct sequence: C → A → B → D**

**Why Block E is wrong:** Error must be an object with code and message, not a string.

**Why Block F is wrong:** JSON-RPC errors don't use HTTP status in the body.

</details>

---

## Problem P10: SMTP Message Formatting (LO1)

### Task

Arrange the code blocks to format an email message correctly for SMTP DATA phase.

**Difficulty:** ⭐⭐ Intermediate  
**Estimated time:** 4 minutes

### Scrambled Blocks

```python
# Block A
def format_email(sender, recipient, subject, body):
    lines = []

# Block B
    lines.append(f"From: {sender}")
    lines.append(f"To: {recipient}")
    lines.append(f"Subject: {subject}")

# Block C
    lines.append("")  # Blank line separates headers from body

# Block D
    for line in body.split("\n"):
        if line.startswith("."):
            lines.append("." + line)  # Dot-stuffing
        else:
            lines.append(line)

# Block E
    lines.append(".")  # End of message
    return "\r\n".join(lines)

# Block F (DISTRACTOR ❌)
    lines.append("\n")  # Blank line

# Block G (DISTRACTOR ❌)
    return "\n".join(lines)
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

**Correct sequence: A → B → C → D → E**

**Why Block F is wrong:** Should append empty string, not "\n" (join adds separators).

**Why Block G is wrong:** SMTP requires CRLF (\r\n), not just LF (\n).

</details>

---

## Summary Table

| Problem | LO | Difficulty | Blocks | Distractors | Key Concept |
|---------|-----|------------|--------|-------------|-------------|
| P1 | LO1 | ⭐⭐ | 7 | 2 | SMTP command sequence |
| P2 | LO2 | ⭐ | 5 | 2 | JSON-RPC 2.0 structure |
| P3 | LO3 | ⭐⭐⭐ | 7 | 2 | HTTP server implementation |
| P4 | LO4 | ⭐ | 5 | 2 | curl command construction |
| P5 | LO5 | ⭐⭐⭐ | 6 | 2 | Protocol benchmarking |
| P6 | LO1 | ⭐⭐ | 6 | 2 | SMTP response codes |
| P7 | LO4 | ⭐ | 4 | 2 | XML-RPC client |
| P8 | LO3 | ⭐⭐ | 4 | 2 | Protocol Buffers definition |
| P9 | LO5 | ⭐⭐ | 4 | 2 | JSON-RPC error handling |
| P10 | LO1 | ⭐⭐ | 5 | 2 | SMTP message formatting |

**Total: 10 problems with 20 distractor blocks**

---

## See Also

- `docs/code_tracing.md` — Trace execution exercises
- `docs/misconceptions.md` — Common errors
- `formative/quiz.yaml` — Self-assessment quiz

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
