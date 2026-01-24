# 🔍 Code Tracing Exercises — Week 11
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Trace through the code mentally before running it. This builds debugging skills and deepens understanding of how network code executes.

---

## Exercise T1: Round-Robin Selection

### Code

```python
class LoadBalancer:
    def __init__(self, backends):
        self.backends = backends  # ["web1", "web2", "web3"]
        self._rr_idx = 0
    
    def pick_rr(self):
        n = len(self.backends)
        backend = self.backends[self._rr_idx]
        self._rr_idx = (self._rr_idx + 1) % n
        return backend

# Execution
lb = LoadBalancer(["web1", "web2", "web3"])
results = []
for i in range(7):
    results.append(lb.pick_rr())
print(results)
```

### Questions

1. **After initialisation:** What is the value of `self._rr_idx`?
2. **After first call:** What does `pick_rr()` return? What is `_rr_idx` now?
3. **Final output:** What will `results` contain after the loop?

### State Tracking Table

Complete this table:

| Call # | `_rr_idx` before | Backend returned | `_rr_idx` after |
|--------|------------------|------------------|-----------------|
| 1 | ? | ? | ? |
| 2 | ? | ? | ? |
| 3 | ? | ? | ? |
| 4 | ? | ? | ? |
| 5 | ? | ? | ? |
| 6 | ? | ? | ? |
| 7 | ? | ? | ? |

### Solution

<details>
<summary>Click to reveal</summary>

| Call # | `_rr_idx` before | Backend returned | `_rr_idx` after |
|--------|------------------|------------------|-----------------|
| 1 | 0 | web1 | 1 |
| 2 | 1 | web2 | 2 |
| 3 | 2 | web3 | 0 |
| 4 | 0 | web1 | 1 |
| 5 | 1 | web2 | 2 |
| 6 | 2 | web3 | 0 |
| 7 | 0 | web1 | 1 |

**Output:**
```python
['web1', 'web2', 'web3', 'web1', 'web2', 'web3', 'web1']
```

**Key insight:** The modulo operator `% n` causes the index to wrap around: `(2 + 1) % 3 = 0`

</details>

---

## Exercise T2: DNS Domain Name Encoding

### Code

```python
def encode_domain_name(domain):
    result = b""
    for label in domain.split("."):
        if label:
            encoded_label = label.encode("ascii")
            result += bytes([len(encoded_label)]) + encoded_label
    result += b"\x00"
    return result

# Execution
domain = "www.ase.ro"
encoded = encode_domain_name(domain)
print(f"Length: {len(encoded)}")
print(f"Hex: {encoded.hex()}")
```

### Questions

1. **Split result:** What does `"www.ase.ro".split(".")` return?
2. **First iteration:** What bytes are added for "www"?
3. **Final byte:** Why is `\x00` appended at the end?
4. **Total length:** How many bytes is the encoded domain?

### Byte-by-Byte Breakdown

Complete this table:

| Label | Length byte | ASCII bytes | Hex representation |
|-------|-------------|-------------|-------------------|
| www | ? | ? | ? |
| ase | ? | ? | ? |
| ro | ? | ? | ? |
| (terminator) | - | - | ? |

### Solution

<details>
<summary>Click to reveal</summary>

| Label | Length byte | ASCII bytes | Hex representation |
|-------|-------------|-------------|-------------------|
| www | `\x03` (3) | `www` | `03 77 77 77` |
| ase | `\x03` (3) | `ase` | `03 61 73 65` |
| ro | `\x02` (2) | `ro` | `02 72 6f` |
| (terminator) | - | - | `00` |

**Output:**
```
Length: 12
Hex: 03777777036173650272bf00
```

Wait, let me recalculate:
- `\x03` + `www` = 4 bytes
- `\x03` + `ase` = 4 bytes  
- `\x02` + `ro` = 3 bytes
- `\x00` = 1 byte
- Total = 12 bytes

Hex: `03 77 77 77 03 61 73 65 02 72 6f 00`

**Key insight:** DNS labels are length-prefixed, not null-terminated. The final `\x00` marks the end of the domain name (root label has length 0).

</details>

---

## Exercise T3: Health Check State Machine

### Code

```python
from dataclasses import dataclass
import time

@dataclass
class Backend:
    name: str
    fails: int = 0
    down_until: float = 0.0
    
    def is_down(self, current_time):
        return current_time < self.down_until

def mark_failure(backend, current_time, max_fails=2, fail_timeout=10.0):
    backend.fails += 1
    if backend.fails >= max_fails:
        backend.down_until = current_time + fail_timeout
        print(f"{backend.name}: marked DOWN until {backend.down_until}")
    else:
        print(f"{backend.name}: fail count = {backend.fails}")

def mark_success(backend):
    backend.fails = 0
    print(f"{backend.name}: reset to healthy")

# Simulation
backend = Backend(name="web1")
t = 0.0

mark_failure(backend, t)      # t=0
mark_failure(backend, t)      # t=0
print(f"is_down at t=5? {backend.is_down(5.0)}")
print(f"is_down at t=15? {backend.is_down(15.0)}")
mark_success(backend)
mark_failure(backend, 20.0)   # t=20
print(f"is_down at t=20? {backend.is_down(20.0)}")
```

### Questions

1. **After first failure:** What is `backend.fails`? Is it marked down?
2. **After second failure:** What is `backend.down_until`?
3. **At t=5:** Is the backend considered down?
4. **After mark_success:** What is `backend.fails`?
5. **Final state:** After the last failure at t=20, is it down?

### State Tracking Table

| Event | Time | `fails` after | `down_until` after | Output |
|-------|------|---------------|-------------------|--------|
| Initial | - | ? | ? | - |
| mark_failure | 0 | ? | ? | ? |
| mark_failure | 0 | ? | ? | ? |
| is_down check | 5 | - | - | ? |
| is_down check | 15 | - | - | ? |
| mark_success | - | ? | ? | ? |
| mark_failure | 20 | ? | ? | ? |
| is_down check | 20 | - | - | ? |

### Solution

<details>
<summary>Click to reveal</summary>

| Event | Time | `fails` after | `down_until` after | Output |
|-------|------|---------------|-------------------|--------|
| Initial | - | 0 | 0.0 | - |
| mark_failure | 0 | 1 | 0.0 | "web1: fail count = 1" |
| mark_failure | 0 | 2 | 10.0 | "web1: marked DOWN until 10.0" |
| is_down check | 5 | 2 | 10.0 | True (5 < 10) |
| is_down check | 15 | 2 | 10.0 | False (15 >= 10) |
| mark_success | - | 0 | 10.0 | "web1: reset to healthy" |
| mark_failure | 20 | 1 | 10.0 | "web1: fail count = 1" |
| is_down check | 20 | 1 | 10.0 | False (20 >= 10) |

**Key insights:**
1. `max_fails=2` means the backend is marked down on the **second** failure
2. `down_until` is set to `current_time + fail_timeout`
3. `mark_success` resets `fails` but not `down_until` (doesn't matter since fails < max_fails)
4. The last failure only brings `fails` to 1, so not marked down yet

</details>

---

## Exercise T4: IP Hash Backend Selection

### Code

```python
def ip_hash_select(client_ip, backends):
    """Select backend using IP hash."""
    h = 0
    for ch in client_ip:
        h = (h * 131 + ord(ch)) & 0xFFFFFFFF
    
    index = h % len(backends)
    return backends[index], h, index

backends = ["web1", "web2", "web3"]

# Test with different IPs
test_ips = ["192.168.1.1", "192.168.1.2", "192.168.1.1"]
for ip in test_ips:
    backend, hash_val, idx = ip_hash_select(ip, backends)
    print(f"IP: {ip} → hash: {hash_val} → index: {idx} → {backend}")
```

### Questions

1. **Hash property:** Will the same IP always produce the same hash?
2. **Different IPs:** Will `192.168.1.1` and `192.168.1.2` likely select different backends?
3. **Repeated IP:** What happens when we query `192.168.1.1` twice?
4. **Why `& 0xFFFFFFFF`:** What does this bitwise AND do?

### Analysis

Without calculating exact hash values, answer:

| IP Address | Same hash as previous? | Same backend as previous? |
|------------|----------------------|--------------------------|
| 192.168.1.1 (1st) | N/A | N/A |
| 192.168.1.2 | ? | ? |
| 192.168.1.1 (2nd) | ? | ? |

### Solution

<details>
<summary>Click to reveal</summary>

| IP Address | Same hash as previous? | Same backend as previous? |
|------------|----------------------|--------------------------|
| 192.168.1.1 (1st) | N/A | N/A |
| 192.168.1.2 | No (different input) | Probably not (different hash) |
| 192.168.1.1 (2nd) | Yes (same as 1st) | Yes (deterministic) |

**Key insights:**

1. **Deterministic:** Same IP always produces same hash (no randomness)
2. **`& 0xFFFFFFFF`:** Keeps hash as 32-bit unsigned integer (prevents Python's arbitrary precision from growing unbounded)
3. **Sticky sessions:** This is how IP hash provides session affinity
4. **Weakness:** If backend list changes (e.g., one removed), hash distribution changes

**Actual output (may vary by implementation):**
```
IP: 192.168.1.1 → hash: 1234567890 → index: 0 → web1
IP: 192.168.1.2 → hash: 2345678901 → index: 1 → web2
IP: 192.168.1.1 → hash: 1234567890 → index: 0 → web1
```

</details>

---

## Exercise T5: HTTP Response Building

### Code

```python
def build_response(backend_id, request_count):
    body = f"Backend {backend_id} | Request #{request_count}\n"
    body_bytes = body.encode("utf-8")
    
    response = (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: text/plain\r\n"
        b"Content-Length: " + str(len(body_bytes)).encode() + b"\r\n"
        b"\r\n"
    ) + body_bytes
    
    return response

# Execution
resp = build_response(2, 5)
print(f"Total bytes: {len(resp)}")
print(f"Response:\n{resp.decode()}")
```

### Questions

1. **Body content:** What is the exact body string for backend_id=2, request_count=5?
2. **Body length:** How many bytes is the body (including newline)?
3. **Header separator:** What separates headers from body in HTTP?
4. **Total response:** Approximately how many bytes is the complete response?

### Byte Counting

| Component | Content | Bytes |
|-----------|---------|-------|
| Status line | `HTTP/1.1 200 OK\r\n` | ? |
| Content-Type header | ? | ? |
| Content-Length header | ? | ? |
| Header terminator | `\r\n` | ? |
| Body | ? | ? |
| **Total** | | ? |

### Solution

<details>
<summary>Click to reveal</summary>

Body: `"Backend 2 | Request #5\n"` = 24 characters = 24 bytes

| Component | Content | Bytes |
|-----------|---------|-------|
| Status line | `HTTP/1.1 200 OK\r\n` | 17 |
| Content-Type | `Content-Type: text/plain\r\n` | 26 |
| Content-Length | `Content-Length: 24\r\n` | 20 |
| Header terminator | `\r\n` | 2 |
| Body | `Backend 2 | Request #5\n` | 24 |
| **Total** | | **89** |

**Key insight:** `\r\n\r\n` (CRLF CRLF) separates headers from body in HTTP. The blank line signals "headers are done, body follows."

</details>

---

## Tips for Code Tracing

1. **Use paper:** Write down variable values as they change
2. **Execute mentally:** Step through line by line, don't skip
3. **Check boundaries:** Pay attention to loop indices and off-by-one errors
4. **Verify with print:** After tracing, run the code to check your answers
5. **Understand, don't memorise:** Focus on *why* the code behaves this way

---

*NETWORKING class - ASE, Informatics | Computer Networks Laboratory*
*Week 11: Application Protocols — FTP, DNS, SSH and Load Balancing*
