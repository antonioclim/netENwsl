# 🔍 Code Tracing Exercises — Week 10
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Trace through the code mentally before running it.

---

## Exercise T1: HTTP Request Routing

### Code

```python
def route_request(method: str, path: str) -> tuple[str, int]:
    """Route an HTTP request to the appropriate handler."""
    
    if path == "/":
        return "Welcome page", 200
    
    if path.startswith("/api/users"):
        if path == "/api/users":
            if method == "GET":
                return "List all users", 200
            elif method == "POST":
                return "Create user", 201
            else:
                return "Method not allowed", 405
        
        # Extract user ID from path like /api/users/123
        parts = path.split("/")
        if len(parts) == 4 and parts[3].isdigit():
            user_id = int(parts[3])
            if method == "GET":
                return f"Get user {user_id}", 200
            elif method == "PUT":
                return f"Update user {user_id}", 200
            elif method == "DELETE":
                return f"Delete user {user_id}", 204
    
    return "Not found", 404


# Test cases
requests = [
    ("GET", "/"),
    ("GET", "/api/users"),
    ("POST", "/api/users"),
    ("GET", "/api/users/42"),
    ("DELETE", "/api/users/7"),
    ("GET", "/api/users/abc"),
    ("PATCH", "/api/users"),
    ("GET", "/unknown"),
]

for method, path in requests:
    response, status = route_request(method, path)
    print(f"{method} {path} -> {status}: {response}")
```

### Questions

1. **Line by line:** After processing `("GET", "/api/users/42")`, what values does the function return?

2. **Output prediction:** What will be printed for `("GET", "/api/users/abc")`?

3. **State tracking:** Complete the table for each request:

| Request | path.split("/") | len(parts) | parts[3].isdigit() | Response | Status |
|---------|-----------------|------------|-------------------|----------|--------|
| GET / | ? | ? | N/A | ? | ? |
| GET /api/users | ? | ? | N/A | ? | ? |
| GET /api/users/42 | ? | ? | ? | ? | ? |
| GET /api/users/abc | ? | ? | ? | ? | ? |

### Solution

<details>
<summary>Click to reveal</summary>

| Request | path.split("/") | len(parts) | parts[3].isdigit() | Response | Status |
|---------|-----------------|------------|-------------------|----------|--------|
| GET / | ['', ''] | 2 | N/A | "Welcome page" | 200 |
| GET /api/users | ['', 'api', 'users'] | 3 | N/A | "List all users" | 200 |
| GET /api/users/42 | ['', 'api', 'users', '42'] | 4 | True | "Get user 42" | 200 |
| GET /api/users/abc | ['', 'api', 'users', 'abc'] | 4 | False | "Not found" | 404 |

**Full output:**
```
GET / -> 200: Welcome page
GET /api/users -> 200: List all users
POST /api/users -> 201: Create user
GET /api/users/42 -> 200: Get user 42
DELETE /api/users/7 -> 204: Delete user 7
GET /api/users/abc -> 404: Not found
PATCH /api/users -> 405: Method not allowed
GET /unknown -> 404: Not found
```

**Key insight:** The routing logic uses string operations to parse the path. Non-numeric IDs fall through to 404 because `isdigit()` returns False.
</details>

---

## Exercise T2: DNS Response Building

### Code

```python
RECORDS = {
    "web.lab.local": "172.20.0.10",
    "api.lab.local": "172.20.0.20",
    "db.lab.local": "172.20.0.30",
}

def resolve_dns(query_name: str) -> dict:
    """Simulate DNS resolution."""
    
    result = {
        "query": query_name,
        "status": "NXDOMAIN",
        "answer": None,
        "ttl": 0,
    }
    
    # Remove trailing dot if present
    name = query_name.rstrip(".")
    
    # Check exact match
    if name in RECORDS:
        result["status"] = "NOERROR"
        result["answer"] = RECORDS[name]
        result["ttl"] = 300
        return result
    
    # Check wildcard (*.lab.local)
    parts = name.split(".")
    if len(parts) >= 3:
        wildcard = "*." + ".".join(parts[1:])
        if wildcard in RECORDS:
            result["status"] = "NOERROR"
            result["answer"] = RECORDS[wildcard]
            result["ttl"] = 60
            return result
    
    return result


# Test queries
queries = [
    "web.lab.local",
    "web.lab.local.",
    "api.lab.local",
    "unknown.lab.local",
    "test.example.com",
]

for q in queries:
    r = resolve_dns(q)
    print(f"Query: {q}")
    print(f"  Status: {r['status']}, Answer: {r['answer']}, TTL: {r['ttl']}")
```

### Questions

1. **Line by line:** What is the value of `name` after `"web.lab.local.".rstrip(".")`?

2. **Output prediction:** What will be the status and answer for `"unknown.lab.local"`?

3. **Logic tracing:** Why does `"web.lab.local."` (with trailing dot) still resolve correctly?

### Solution

<details>
<summary>Click to reveal</summary>

1. `name = "web.lab.local"` (trailing dot removed)

2. Status: `"NXDOMAIN"`, Answer: `None`

3. The trailing dot is removed by `rstrip(".")` before the lookup, so both `"web.lab.local"` and `"web.lab.local."` become the same key.

**Full output:**
```
Query: web.lab.local
  Status: NOERROR, Answer: 172.20.0.10, TTL: 300
Query: web.lab.local.
  Status: NOERROR, Answer: 172.20.0.10, TTL: 300
Query: api.lab.local
  Status: NOERROR, Answer: 172.20.0.20, TTL: 300
Query: unknown.lab.local
  Status: NXDOMAIN, Answer: None, TTL: 0
Query: test.example.com
  Status: NXDOMAIN, Answer: None, TTL: 0
```
</details>

---

## Exercise T3: TLS State Machine

### Code

```python
class TLSConnection:
    """Simplified TLS connection state machine."""
    
    STATES = ["INIT", "CLIENT_HELLO", "SERVER_HELLO", 
              "KEY_EXCHANGE", "ENCRYPTED", "CLOSED"]
    
    def __init__(self):
        self.state = "INIT"
        self.cipher_suite = None
        self.session_key = None
    
    def client_hello(self, supported_ciphers: list[str]) -> str:
        if self.state != "INIT":
            return f"Error: Invalid state {self.state}"
        
        self.state = "CLIENT_HELLO"
        return f"ClientHello sent with {len(supported_ciphers)} cipher suites"
    
    def server_hello(self, chosen_cipher: str) -> str:
        if self.state != "CLIENT_HELLO":
            return f"Error: Invalid state {self.state}"
        
        self.cipher_suite = chosen_cipher
        self.state = "SERVER_HELLO"
        return f"ServerHello received, cipher: {chosen_cipher}"
    
    def key_exchange(self) -> str:
        if self.state != "SERVER_HELLO":
            return f"Error: Invalid state {self.state}"
        
        self.session_key = "shared_secret_12345"
        self.state = "KEY_EXCHANGE"
        return "Key exchange complete"
    
    def finish_handshake(self) -> str:
        if self.state != "KEY_EXCHANGE":
            return f"Error: Invalid state {self.state}"
        
        self.state = "ENCRYPTED"
        return "Handshake complete, connection encrypted"
    
    def close(self) -> str:
        self.state = "CLOSED"
        self.session_key = None
        return "Connection closed"


# Simulate handshake
conn = TLSConnection()
print(f"Initial state: {conn.state}")

steps = [
    lambda c: c.client_hello(["AES_256_GCM", "CHACHA20"]),
    lambda c: c.server_hello("AES_256_GCM"),
    lambda c: c.key_exchange(),
    lambda c: c.finish_handshake(),
    lambda c: c.close(),
]

for i, step in enumerate(steps, 1):
    result = step(conn)
    print(f"Step {i}: {result}")
    print(f"  State: {conn.state}, Cipher: {conn.cipher_suite}, Key: {conn.session_key}")
```

### Questions

1. **State tracking:** Complete the state transitions:

| Step | Method called | State before | State after |
|------|---------------|--------------|-------------|
| 1 | client_hello | ? | ? |
| 2 | server_hello | ? | ? |
| 3 | key_exchange | ? | ? |
| 4 | finish_handshake | ? | ? |
| 5 | close | ? | ? |

2. **Error condition:** What would happen if we called `server_hello()` immediately after `__init__`?

3. **Object state:** After step 4 completes, what are the values of `cipher_suite` and `session_key`?

### Solution

<details>
<summary>Click to reveal</summary>

| Step | Method called | State before | State after |
|------|---------------|--------------|-------------|
| 1 | client_hello | INIT | CLIENT_HELLO |
| 2 | server_hello | CLIENT_HELLO | SERVER_HELLO |
| 3 | key_exchange | SERVER_HELLO | KEY_EXCHANGE |
| 4 | finish_handshake | KEY_EXCHANGE | ENCRYPTED |
| 5 | close | ENCRYPTED | CLOSED |

2. It would return `"Error: Invalid state INIT"` because `server_hello()` expects state to be `CLIENT_HELLO`.

3. After step 4:
   - `cipher_suite = "AES_256_GCM"`
   - `session_key = "shared_secret_12345"`

**Full output:**
```
Initial state: INIT
Step 1: ClientHello sent with 2 cipher suites
  State: CLIENT_HELLO, Cipher: None, Key: None
Step 2: ServerHello received, cipher: AES_256_GCM
  State: SERVER_HELLO, Cipher: AES_256_GCM, Key: None
Step 3: Key exchange complete
  State: KEY_EXCHANGE, Cipher: AES_256_GCM, Key: shared_secret_12345
Step 4: Handshake complete, connection encrypted
  State: ENCRYPTED, Cipher: AES_256_GCM, Key: shared_secret_12345
Step 5: Connection closed
  State: CLOSED, Cipher: AES_256_GCM, Key: None
```

**Key insight:** TLS handshake follows a strict state machine. Attempting operations out of order fails. This prevents protocol violations.
</details>

---

## Tips for Code Tracing

1. **Track state explicitly** — write down variable values after each line
2. **Follow control flow** — trace which branch of if/else executes
3. **Watch for mutations** — note when objects are modified
4. **Check boundary cases** — empty strings, None values, edge cases
5. **Predict before running** — form a hypothesis, then verify

---

*Computer Networks — Week 10 | ASE, CSIE Bucharest*
*Code tracing exercises by ing. dr. Antonio Clim*
