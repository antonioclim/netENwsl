# 🔍 Code Tracing Exercises — Week 12
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> **Topic:** Email Protocols and Remote Procedure Call  
> Trace through the code mentally before running it.

---

## Exercise T1: SMTP State Machine

### Context

The following code simulates an SMTP client sending a message. Trace through to predict the server responses.

### Code

```python
import socket

def send_email():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 1025))
    
    # Line 1: Receive greeting
    greeting = sock.recv(1024).decode()
    print(f"S: {greeting}")
    
    # Line 2: Send EHLO
    sock.sendall(b"EHLO tracer.local\r\n")
    ehlo_resp = sock.recv(1024).decode()
    print(f"S: {ehlo_resp}")
    
    # Line 3: Send MAIL FROM
    sock.sendall(b"MAIL FROM:<trace@test.com>\r\n")
    mail_resp = sock.recv(1024).decode()
    print(f"S: {mail_resp}")
    
    # Line 4: Send RCPT TO
    sock.sendall(b"RCPT TO:<dest@test.com>\r\n")
    rcpt_resp = sock.recv(1024).decode()
    print(f"S: {rcpt_resp}")
    
    # Line 5: Send DATA
    sock.sendall(b"DATA\r\n")
    data_resp = sock.recv(1024).decode()
    print(f"S: {data_resp}")
    
    # Line 6: Send message body + terminator
    sock.sendall(b"Subject: Trace Test\r\n\r\nBody here.\r\n.\r\n")
    final_resp = sock.recv(1024).decode()
    print(f"S: {final_resp}")
    
    # Line 7: QUIT
    sock.sendall(b"QUIT\r\n")
    quit_resp = sock.recv(1024).decode()
    print(f"S: {quit_resp}")
    
    sock.close()

send_email()
```

### Questions

1. **Response codes:** Fill in the expected response code for each line:

| After line | Command sent | Expected response code |
|------------|--------------|------------------------|
| 1 | (connect) | ? |
| 2 | EHLO | ? |
| 3 | MAIL FROM | ? |
| 4 | RCPT TO | ? |
| 5 | DATA | ? |
| 6 | (message + dot) | ? |
| 7 | QUIT | ? |

2. **State transition:** At which line does the server transition from "command mode" to "data mode"?

3. **Termination:** What sequence terminates the message body?

### Solution

<details>
<summary>Click to reveal</summary>

| After line | Command sent | Expected response code |
|------------|--------------|------------------------|
| 1 | (connect) | **220** (Service ready) |
| 2 | EHLO | **250** (multi-line, OK) |
| 3 | MAIL FROM | **250** (OK) |
| 4 | RCPT TO | **250** (OK) |
| 5 | DATA | **354** (Start mail input) |
| 6 | (message + dot) | **250** (Message accepted) |
| 7 | QUIT | **221** (Bye) |

**State transition:** Line 5 — after DATA returns 354, the server enters "data mode" and interprets all input as message content until it sees `<CRLF>.<CRLF>`.

**Termination sequence:** `\r\n.\r\n` (CRLF, dot, CRLF) — a single dot on its own line.

</details>

---

## Exercise T2: JSON-RPC Request Processing

### Context

Trace through this JSON-RPC server dispatcher to predict the response.

### Code

```python
def dispatch(request: dict) -> dict:
    # Step 1: Validate JSON-RPC version
    if request.get("jsonrpc") != "2.0":
        return {"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": None}
    
    # Step 2: Extract method and params
    method = request.get("method")
    params = request.get("params", [])
    req_id = request.get("id")
    
    # Step 3: Check if notification (no id)
    is_notification = "id" not in request
    
    # Step 4: Dispatch to method
    if method == "add":
        if isinstance(params, list) and len(params) >= 2:
            result = params[0] + params[1]
        elif isinstance(params, dict):
            result = params.get("a", 0) + params.get("b", 0)
        else:
            return {"jsonrpc": "2.0", "error": {"code": -32602, "message": "Invalid params"}, "id": req_id}
    elif method == "divide":
        a, b = params[0], params[1]
        if b == 0:
            return {"jsonrpc": "2.0", "error": {"code": -32000, "message": "Division by zero"}, "id": req_id}
        result = a / b
    else:
        return {"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": req_id}
    
    # Step 5: Return result (unless notification)
    if is_notification:
        return None
    return {"jsonrpc": "2.0", "result": result, "id": req_id}


# Test cases
req1 = {"jsonrpc": "2.0", "method": "add", "params": [10, 32], "id": 1}
req2 = {"jsonrpc": "2.0", "method": "add", "params": {"a": 5, "b": 3}, "id": 2}
req3 = {"jsonrpc": "2.0", "method": "divide", "params": [10, 0], "id": 3}
req4 = {"jsonrpc": "2.0", "method": "add", "params": [1, 2]}  # No id
req5 = {"jsonrpc": "2.0", "method": "power", "params": [2, 8], "id": 5}
```

### Questions

1. **Trace each request:** What does `dispatch()` return for each test case?

| Request | Expected return value |
|---------|----------------------|
| req1 | ? |
| req2 | ? |
| req3 | ? |
| req4 | ? |
| req5 | ? |

2. **Notification handling:** Why does req4 return `None`?

3. **Error codes:** What is the significance of `-32601` vs `-32000`?

### Solution

<details>
<summary>Click to reveal</summary>

| Request | Expected return value |
|---------|----------------------|
| req1 | `{"jsonrpc": "2.0", "result": 42, "id": 1}` |
| req2 | `{"jsonrpc": "2.0", "result": 8, "id": 2}` |
| req3 | `{"jsonrpc": "2.0", "error": {"code": -32000, "message": "Division by zero"}, "id": 3}` |
| req4 | `None` |
| req5 | `{"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": 5}` |

**Notification handling:** req4 has no `id` field, making it a notification. Per JSON-RPC spec, notifications do not receive responses — the server processes them silently.

**Error codes:**
- `-32601` is a standard JSON-RPC error (Method not found)
- `-32000` is a server-defined error (application-specific, here: division by zero)

Standard error codes (-32700 to -32603) are reserved by the specification.

</details>

---

## Exercise T3: Protocol Buffer Field Encoding

### Context

Understand how Protocol Buffers encode data by tracing through the wire format.

### Schema

```protobuf
message CalcRequest {
    double a = 1;  // field tag 1, wire type 1 (64-bit)
    double b = 2;  // field tag 2, wire type 1 (64-bit)
}
```

### Encoding Rules

| Wire Type | Meaning | Used for |
|-----------|---------|----------|
| 0 | Varint | int32, int64, bool |
| 1 | 64-bit | double, fixed64 |
| 2 | Length-delimited | string, bytes, embedded messages |
| 5 | 32-bit | float, fixed32 |

**Field key formula:** `(field_number << 3) | wire_type`

### Code

```python
import struct

def encode_double(value):
    """Encode a double as 8 bytes (little-endian IEEE 754)."""
    return struct.pack('<d', value)

def encode_field_key(field_number, wire_type):
    """Encode field key as varint."""
    key = (field_number << 3) | wire_type
    return bytes([key])

def encode_calc_request(a, b):
    """Encode CalcRequest message."""
    result = bytearray()
    
    # Field 1: double a
    result.extend(encode_field_key(1, 1))  # key = (1 << 3) | 1 = 9
    result.extend(encode_double(a))
    
    # Field 2: double b
    result.extend(encode_field_key(2, 1))  # key = (2 << 3) | 1 = 17
    result.extend(encode_double(b))
    
    return bytes(result)

# Test
encoded = encode_calc_request(10.0, 32.0)
print(f"Encoded length: {len(encoded)} bytes")
print(f"Hex: {encoded.hex()}")
```

### Questions

1. **Field keys:** Calculate the field key bytes:
   - Field 1 (double): key = ?
   - Field 2 (double): key = ?

2. **Total size:** What is the total encoded size of `CalcRequest(a=10.0, b=32.0)`?

3. **Comparison:** How does this compare to the JSON equivalent `{"a": 10.0, "b": 32.0}`?

### Solution

<details>
<summary>Click to reveal</summary>

**Field keys:**
- Field 1: `(1 << 3) | 1 = 8 | 1 = 9` → byte `0x09`
- Field 2: `(2 << 3) | 1 = 16 | 1 = 17` → byte `0x11`

**Total size:** 18 bytes
- Field 1 key: 1 byte (0x09)
- Field 1 value: 8 bytes (IEEE 754 double for 10.0)
- Field 2 key: 1 byte (0x11)
- Field 2 value: 8 bytes (IEEE 754 double for 32.0)

**Comparison:**
- Protobuf: 18 bytes (binary, not human-readable)
- JSON: `{"a": 10.0, "b": 32.0}` = 22 bytes (text, human-readable)
- JSON with spaces: `{"a": 10.0, "b": 32.0}` = ~25 bytes

Protobuf saves ~20-30% for this simple message, but savings increase dramatically for larger messages with repeated fields and nested structures.

**Hex output:** `09 00 00 00 00 00 00 24 40 11 00 00 00 00 00 00 40 40`
- `09` = field 1 key
- `00...24 40` = 10.0 as IEEE 754 double (little-endian)
- `11` = field 2 key
- `00...40 40` = 32.0 as IEEE 754 double (little-endian)

</details>

---

## Exercise T4: SMTP Error Handling

### Context

Trace through this SMTP session with intentional errors.

### Session

```
C: (connects to port 1025)
S: 220 Week12 SMTP server ready
C: MAIL FROM:<alice@example.com>
S: ???
C: EHLO client.local
S: 250-Hello client.local
S: 250 PIPELINING
C: MAIL FROM:<alice@example.com>
S: ???
C: DATA
S: ???
C: RCPT TO:<bob@example.com>
S: ???
C: DATA
S: ???
```

### Questions

1. **First MAIL FROM:** What response does the server send? Why?

2. **Second MAIL FROM:** What response now?

3. **First DATA:** What response? Why?

4. **RCPT TO after failed DATA:** What response?

5. **Second DATA:** What response now?

### Solution

<details>
<summary>Click to reveal</summary>

```
C: (connects)
S: 220 Week12 SMTP server ready

C: MAIL FROM:<alice@example.com>
S: 503 Bad sequence of commands
   (Must send EHLO/HELO first!)

C: EHLO client.local
S: 250-Hello client.local
S: 250 PIPELINING

C: MAIL FROM:<alice@example.com>
S: 250 OK
   (Now valid — EHLO was sent)

C: DATA
S: 503 Bad sequence of commands
   (Must have at least one RCPT TO first!)

C: RCPT TO:<bob@example.com>
S: 250 OK

C: DATA
S: 354 End data with <CR><LF>.<CR><LF>
   (Now valid — have MAIL FROM and RCPT TO)
```

**Key insight:** SMTP is a state machine. Commands must be sent in the correct sequence:
1. Connection → greeting (220)
2. EHLO/HELO → capabilities (250)
3. MAIL FROM → sender accepted (250)
4. RCPT TO (one or more) → recipient accepted (250)
5. DATA → ready for content (354)
6. Content + dot → message accepted (250)
7. QUIT → goodbye (221)

</details>

---

## Tips for Code Tracing

1. **Draw the state:** For protocols, draw a state diagram and track current state
2. **Track variables:** Use a table to track variable values at each step
3. **Predict first:** Write your prediction before checking the answer
4. **Understand errors:** Error conditions reveal protocol requirements
5. **Compare formats:** Trace the same data through different serialisation formats

---

## See Also

- `parsons_problems.md` — Reorder code exercises
- `misconceptions.md` — Common errors explained
- `theory_summary.md` — Protocol specifications

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
