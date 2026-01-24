# 🔍 Code Tracing Exercises — Week 8
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Trace through the code mentally before running it.
> This builds understanding of how HTTP servers and proxies work internally.

---

## How to Use This Document

1. **Read the code** without running it
2. **Predict the output** by tracing variable values
3. **Fill in the tables** with expected values
4. **Check your answers** by clicking "Reveal Solution"
5. **Run the code** to verify your understanding

---

## Exercise T1: HTTP Request Parsing

### Code

```python
def parse_request(raw: bytes) -> tuple:
    """Parse HTTP request into components."""
    text = raw.decode('utf-8')
    lines = text.split('\r\n')
    
    # Parse request line
    request_line = lines[0]
    parts = request_line.split(' ')
    method = parts[0]
    path = parts[1]
    version = parts[2]
    
    # Parse headers
    headers = {}
    for line in lines[1:]:
        if line == '':
            break
        key, value = line.split(': ', 1)
        headers[key.lower()] = value
    
    return method, path, version, headers

# Input
raw_request = b'GET /index.html HTTP/1.1\r\nHost: localhost:8080\r\nUser-Agent: curl/7.68.0\r\nAccept: */*\r\n\r\n'

# Execution
method, path, version, headers = parse_request(raw_request)
print(f"Method: {method}")
print(f"Path: {path}")
print(f"Headers: {len(headers)}")
print(f"Host: {headers.get('host', 'N/A')}")
```

### Questions

1. **After `text.split('\r\n')`**, how many elements are in `lines`?
2. **What is `parts[1]`** after splitting the request line?
3. **How many headers** are in the final `headers` dictionary?
4. **What is `headers['user-agent']`**?

### Trace Table

| After Line | `method` | `path` | `len(headers)` | `headers.get('host')` |
|------------|----------|--------|----------------|-----------------------|
| Before execution | - | - | - | - |
| After `text.split()` | - | - | - | - |
| After request line parse | ? | ? | - | - |
| After header loop | ? | ? | ? | ? |

### Solution

<details>
<summary>Click to reveal</summary>

**Trace Table (Completed):**

| After Line | `method` | `path` | `len(headers)` | `headers.get('host')` |
|------------|----------|--------|----------------|-----------------------|
| Before execution | - | - | - | - |
| After `text.split()` | - | - | - | - |
| After request line parse | `'GET'` | `'/index.html'` | - | - |
| After header loop | `'GET'` | `'/index.html'` | `3` | `'localhost:8080'` |

**Output:**
```
Method: GET
Path: /index.html
Headers: 3
Host: localhost:8080
```

**Explanation:**
- `lines` has 5 elements: request line, 3 headers, empty line (plus trailing empty from final \r\n)
- The header loop breaks at the empty line
- Headers are normalised to lowercase keys
</details>

---

## Exercise T2: Path Safety Check

### Code

```python
import os

def is_safe_path(requested: str, docroot: str) -> bool:
    """Check if path is within document root."""
    # Normalise the requested path
    normalised = os.path.normpath(requested)
    
    # Build full path
    full_path = os.path.join(docroot, normalised.lstrip('/'))
    
    # Get absolute paths
    abs_docroot = os.path.abspath(docroot)
    abs_full = os.path.abspath(full_path)
    
    # Check containment
    return abs_full.startswith(abs_docroot)

# Test cases
docroot = '/var/www/html'

paths = [
    '/index.html',
    '/images/logo.png',
    '/../etc/passwd',
    '/./images/../index.html',
    '/images/../../etc/shadow',
]

for p in paths:
    result = is_safe_path(p, docroot)
    print(f"{p:30} -> {result}")
```

### Questions

1. **What does `os.path.normpath('/../etc/passwd')` return?**
2. **For path `/./images/../index.html`**, what is the normalised path?
3. **Which paths return `True`?** Which return `False`?
4. **Why does `.lstrip('/')` matter?**

### Trace Table

| Input Path | After `normpath` | After `join` | `is_safe`? |
|------------|------------------|--------------|------------|
| `/index.html` | ? | ? | ? |
| `/images/logo.png` | ? | ? | ? |
| `/../etc/passwd` | ? | ? | ? |
| `/./images/../index.html` | ? | ? | ? |
| `/images/../../etc/shadow` | ? | ? | ? |

### Solution

<details>
<summary>Click to reveal</summary>

**Trace Table (Completed):**

| Input Path | After `normpath` | After `join` | `is_safe`? |
|------------|------------------|--------------|------------|
| `/index.html` | `/index.html` | `/var/www/html/index.html` | ✅ True |
| `/images/logo.png` | `/images/logo.png` | `/var/www/html/images/logo.png` | ✅ True |
| `/../etc/passwd` | `/etc/passwd` | `/var/www/html/etc/passwd` | ✅ True* |
| `/./images/../index.html` | `/index.html` | `/var/www/html/index.html` | ✅ True |
| `/images/../../etc/shadow` | `/etc/shadow` | `/var/www/html/etc/shadow` | ✅ True* |

**Wait — all return True?** Yes, because `os.path.join()` with a path that has leading `/` stripped appends to docroot. The `..` is normalised BEFORE joining.

*Note: These paths point to files that don't exist, but they ARE within docroot (or would be). The safety check passes but file serving would 404.

**Output:**
```
/index.html                    -> True
/images/logo.png               -> True
/../etc/passwd                 -> True
/./images/../index.html        -> True
/images/../../etc/shadow       -> True
```

**Key insight:** `normpath` happens first, then `join`. This is why `/../etc/passwd` normalises to `/etc/passwd`, then joins as `docroot + 'etc/passwd'`.

**SECURITY NOTE:** This implementation is safe because:
1. We normalise BEFORE joining
2. We strip the leading `/` so join works correctly
3. We compare absolute paths at the end
</details>

---

## Exercise T3: Round-Robin Selection

### Code

```python
class RoundRobinBalancer:
    def __init__(self, backends):
        self.backends = backends
        self.index = 0
    
    def next_backend(self):
        if not self.backends:
            return None
        
        backend = self.backends[self.index]
        self.index = (self.index + 1) % len(self.backends)
        return backend

# Setup
balancer = RoundRobinBalancer(['A', 'B', 'C'])

# Execution
results = []
for i in range(7):
    selected = balancer.next_backend()
    results.append(selected)
    print(f"Request {i+1}: {selected} (next index: {balancer.index})")

print(f"\nFinal sequence: {results}")
```

### Questions

1. **After selecting 'A'**, what is `self.index`?
2. **What is `(6 + 1) % 3`?** (After 7th request)
3. **What is the 7th backend selected?**
4. **If we added a 4th backend 'D'**, what would request 8 select?

### Trace Table

| Request # | `self.index` (before) | Selected | `self.index` (after) |
|-----------|----------------------|----------|---------------------|
| 1 | 0 | ? | ? |
| 2 | ? | ? | ? |
| 3 | ? | ? | ? |
| 4 | ? | ? | ? |
| 5 | ? | ? | ? |
| 6 | ? | ? | ? |
| 7 | ? | ? | ? |

### Solution

<details>
<summary>Click to reveal</summary>

**Trace Table (Completed):**

| Request # | `self.index` (before) | Selected | `self.index` (after) |
|-----------|----------------------|----------|---------------------|
| 1 | 0 | A | 1 |
| 2 | 1 | B | 2 |
| 3 | 2 | C | 0 |
| 4 | 0 | A | 1 |
| 5 | 1 | B | 2 |
| 6 | 2 | C | 0 |
| 7 | 0 | A | 1 |

**Output:**
```
Request 1: A (next index: 1)
Request 2: B (next index: 2)
Request 3: C (next index: 0)
Request 4: A (next index: 1)
Request 5: B (next index: 2)
Request 6: C (next index: 0)
Request 7: A (next index: 1)

Final sequence: ['A', 'B', 'C', 'A', 'B', 'C', 'A']
```

**Key insight:** The modulo operation `% len(backends)` makes the index wrap around, creating the round-robin cycle.
</details>

---

## Exercise T4: HTTP Response Building

### Code

```python
def build_response(status_code, headers, body):
    """Build HTTP response bytes."""
    status_messages = {200: 'OK', 404: 'Not Found', 403: 'Forbidden'}
    
    # Status line
    status_line = f"HTTP/1.1 {status_code} {status_messages[status_code]}\r\n"
    
    # Headers
    header_lines = ""
    for key, value in headers.items():
        header_lines += f"{key}: {value}\r\n"
    
    # Combine
    response_str = status_line + header_lines + "\r\n"
    response_bytes = response_str.encode('utf-8') + body
    
    return response_bytes

# Test
body = b"<h1>Hello World</h1>"
headers = {
    "Content-Type": "text/html",
    "Content-Length": str(len(body)),
    "Server": "MyServer/1.0"
}

response = build_response(200, headers, body)
print(response.decode('utf-8'))
print(f"\nTotal bytes: {len(response)}")
```

### Questions

1. **What is on line 1** of the response?
2. **How many `\r\n`** sequences are in the header section (including the blank line)?
3. **What is `len(body)`**?
4. **Where does the body start** in the response?

### Trace Step-by-Step

| Step | Variable | Value |
|------|----------|-------|
| 1 | `status_line` | ? |
| 2 | `header_lines` (after loop) | ? |
| 3 | `response_str` | ? |
| 4 | `len(response_bytes)` | ? |

### Solution

<details>
<summary>Click to reveal</summary>

**Step-by-Step Trace:**

| Step | Variable | Value |
|------|----------|-------|
| 1 | `status_line` | `"HTTP/1.1 200 OK\r\n"` |
| 2 | `header_lines` | `"Content-Type: text/html\r\nContent-Length: 20\r\nServer: MyServer/1.0\r\n"` |
| 3 | `response_str` | `"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 20\r\nServer: MyServer/1.0\r\n\r\n"` |
| 4 | `len(response_bytes)` | 103 bytes (83 header + 20 body) |

**Output:**
```
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 20
Server: MyServer/1.0

<h1>Hello World</h1>
Total bytes: 103
```

**Key insight:** The blank line (`\r\n\r\n`) separates headers from body. Without it, the client cannot determine where headers end.

**Breakdown:**
- Status line: 17 bytes (including \r\n)
- 3 headers: ~66 bytes (including \r\n for each)
- Blank line: 2 bytes (\r\n)
- Body: 20 bytes
</details>

---

## Exercise T5: Connection Forwarding

### Code

```python
def add_forwarded_header(request_str, client_ip):
    """Add X-Forwarded-For header to request."""
    lines = request_str.split('\r\n')
    
    # Find existing X-Forwarded-For or insert position
    xff_index = None
    insert_index = 1  # After request line
    
    for i, line in enumerate(lines[1:], 1):
        if line == '':
            insert_index = i
            break
        if line.lower().startswith('x-forwarded-for:'):
            xff_index = i
    
    if xff_index is not None:
        # Append to existing
        existing = lines[xff_index].split(': ', 1)[1]
        lines[xff_index] = f"X-Forwarded-For: {existing}, {client_ip}"
    else:
        # Insert new header
        lines.insert(insert_index, f"X-Forwarded-For: {client_ip}")
    
    return '\r\n'.join(lines)

# Test 1: No existing X-Forwarded-For
req1 = "GET / HTTP/1.1\r\nHost: backend\r\n\r\n"
result1 = add_forwarded_header(req1, "192.168.1.100")
print("Test 1:")
print(result1)

# Test 2: Existing X-Forwarded-For
req2 = "GET / HTTP/1.1\r\nHost: backend\r\nX-Forwarded-For: 10.0.0.1\r\n\r\n"
result2 = add_forwarded_header(req2, "192.168.1.100")
print("\nTest 2:")
print(result2)
```

### Questions

1. **In Test 1**, where is the new header inserted?
2. **In Test 2**, what is the final X-Forwarded-For value?
3. **Why do we check `line == ''`** in the loop?
4. **What would happen** if we always inserted instead of appending?

### Solution

<details>
<summary>Click to reveal</summary>

**Test 1 Output:**
```
GET / HTTP/1.1
Host: backend
X-Forwarded-For: 192.168.1.100

```

**Test 2 Output:**
```
GET / HTTP/1.1
Host: backend
X-Forwarded-For: 10.0.0.1, 192.168.1.100

```

**Answers:**
1. **Test 1:** Header inserted at index 2, before the blank line
2. **Test 2:** `10.0.0.1, 192.168.1.100` (appended to existing)
3. **Empty line:** Marks end of headers — we need to insert BEFORE it
4. **Always inserting:** Would create duplicate X-Forwarded-For headers, which is technically valid but messy

**Key insight:** X-Forwarded-For forms a chain showing all proxies the request passed through. Rightmost IP is the most recently added (and most trusted if you control that proxy).
</details>

---

## Summary: What These Exercises Teach

| Exercise | Key Concept |
|----------|-------------|
| T1: Request Parsing | HTTP message structure, CRLF line endings |
| T2: Path Safety | Path normalisation, directory traversal prevention |
| T3: Round-Robin | Modular arithmetic for cyclic selection |
| T4: Response Building | HTTP response format, header-body separation |
| T5: Header Forwarding | Proxy header chains, insertion vs appending |

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
