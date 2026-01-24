# 🔍 Code Tracing Exercises — Week 7
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Trace through the code mentally before running it. Write your predictions, then verify.

---

## Exercise T1: TCP Client Connection

### Code

```python
import socket

def connect_and_send(host: str, port: int, message: str) -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Line 1
    sock.settimeout(5.0)                                       # Line 2
    sock.connect((host, port))                                 # Line 3
    sock.sendall(message.encode("utf-8"))                      # Line 4
    response = sock.recv(4096)                                 # Line 5
    sock.close()                                               # Line 6
    return response.decode("utf-8")                            # Line 7

# Assume server on localhost:9090 echoes back messages
result = connect_and_send("localhost", 9090, "HELLO")
print(f"Got: {result}")
```

### Questions

1. **After Line 1:** What type of socket is created? What protocol will it use?

2. **After Line 3:** How many packets have been sent at this point? What are they?

3. **After Line 4:** The message "HELLO" is 5 bytes. How many bytes are sent in the TCP segment payload?

4. **Output prediction:** What will be printed if the server echoes the message back?

5. **State tracking:** Complete the table assuming successful execution:

| After Line | Socket State | Packets Sent (cumulative) | Packets Received (cumulative) |
|------------|--------------|---------------------------|-------------------------------|
| 1 | ? | ? | ? |
| 3 | ? | ? | ? |
| 4 | ? | ? | ? |
| 5 | ? | ? | ? |
| 6 | ? | ? | ? |

### Solution

<details>
<summary>Click to reveal</summary>

1. **After Line 1:** TCP socket (SOCK_STREAM) is created. It will use TCP protocol. Socket state: CLOSED (not yet connected).

2. **After Line 3:** Three packets sent (TCP three-way handshake):
   - Client → Server: SYN
   - Server → Client: SYN-ACK
   - Client → Server: ACK
   
   Socket state is now: ESTABLISHED

3. **After Line 4:** 5 bytes in payload ("HELLO"). The TCP segment also includes headers (~20 bytes minimum), but the payload is 5 bytes.

4. **Output:** `Got: HELLO` (server echoes back the same message)

5. **State tracking:**

| After Line | Socket State | Packets Sent (cumulative) | Packets Received (cumulative) |
|------------|--------------|---------------------------|-------------------------------|
| 1 | CLOSED | 0 | 0 |
| 3 | ESTABLISHED | 2 (SYN, ACK) | 1 (SYN-ACK) |
| 4 | ESTABLISHED | 3 (+ data) | 1 |
| 5 | ESTABLISHED | 3 | 2 (+ data + possibly ACK) |
| 6 | CLOSED/TIME_WAIT | 4 (+ FIN) | 3 (+ FIN-ACK) |

**Note:** Actual packet count may vary due to delayed ACKs and piggy-backing.

</details>

---

## Exercise T2: Port Probe Logic

### Code

```python
import socket

def probe_port(host: str, port: int, timeout: float = 2.0) -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Line 1
    sock.settimeout(timeout)                                    # Line 2
    
    try:
        result = sock.connect_ex((host, port))                  # Line 3
        if result == 0:                                         # Line 4
            status = "open"                                     # Line 5
        else:
            status = "closed"                                   # Line 6
    except socket.timeout:                                      # Line 7
        status = "filtered"                                     # Line 8
    finally:
        sock.close()                                            # Line 9
    
    return status                                               # Line 10

# Test scenarios
print(probe_port("localhost", 9090))   # Server running
print(probe_port("localhost", 9999))   # No server, no firewall
print(probe_port("localhost", 8888))   # Firewall DROP rule active
```

### Questions

1. **Line 3:** What is the difference between `connect()` and `connect_ex()`?

2. **Scenario A:** Server running on port 9090. What value does `result` have at Line 4? What is returned?

3. **Scenario B:** No server on port 9999, no firewall. What value does `result` have? What is returned?

4. **Scenario C:** Firewall DROP rule on port 8888. Which line is reached? What is returned?

5. **Trace the execution path** for each scenario (list line numbers executed):

| Scenario | Lines Executed | Return Value |
|----------|---------------|--------------|
| A (server running) | ? | ? |
| B (closed port) | ? | ? |
| C (firewall DROP) | ? | ? |

### Solution

<details>
<summary>Click to reveal</summary>

1. **Line 3:** `connect()` raises an exception on failure. `connect_ex()` returns an error code (0 = success, non-zero = error number) instead of raising an exception. This allows checking the result without try/except.

2. **Scenario A:** `result = 0` (success). Returns `"open"`.

3. **Scenario B:** `result = 111` (ECONNREFUSED on Linux). Returns `"closed"`.
   - Note: The exact error code varies by OS (111 on Linux, 10061 on Windows).

4. **Scenario C:** Line 7 is reached (socket.timeout exception). Returns `"filtered"`.
   - The `connect_ex()` call blocks until timeout because DROP sends no response.

5. **Execution paths:**

| Scenario | Lines Executed | Return Value |
|----------|---------------|--------------|
| A (server running) | 1, 2, 3, 4, 5, 9, 10 | "open" |
| B (closed port) | 1, 2, 3, 4, 6, 9, 10 | "closed" |
| C (firewall DROP) | 1, 2, 3, 7, 8, 9, 10 | "filtered" |

**Key insight:** The timeout only triggers for DROP (silent discard). REJECT would return a non-zero error code immediately, so it would be classified as "closed" — this is a limitation of this simple probe.

</details>

---

## Exercise T3: Firewall Rule Processing

### Code

```python
# Simulated iptables rule matching logic
rules = [
    {"protocol": "tcp", "port": 9090, "action": "ACCEPT"},
    {"protocol": "tcp", "port": 9091, "action": "REJECT"},
    {"protocol": "udp", "port": 9091, "action": "DROP"},
    {"protocol": "tcp", "port": None, "action": "DROP"},  # Default: drop all TCP
]

def match_packet(protocol: str, port: int) -> str:
    for i, rule in enumerate(rules):                        # Line 1
        if rule["protocol"] != protocol:                    # Line 2
            continue                                        # Line 3
        if rule["port"] is not None and rule["port"] != port:  # Line 4
            continue                                        # Line 5
        print(f"Matched rule {i}: {rule}")                  # Line 6
        return rule["action"]                               # Line 7
    return "ACCEPT"  # Default policy                       # Line 8

# Test packets
print(match_packet("tcp", 9090))   # Packet A
print(match_packet("tcp", 9091))   # Packet B
print(match_packet("udp", 9091))   # Packet C
print(match_packet("tcp", 8080))   # Packet D
print(match_packet("udp", 5000))   # Packet E
```

### Questions

1. **Packet A (tcp, 9090):** Which rule index matches? What action is taken?

2. **Packet B (tcp, 9091):** Which rule index matches? What action is taken?

3. **Packet C (udp, 9091):** Which rule index matches? What action is taken?

4. **Packet D (tcp, 8080):** Which rule index matches? What action is taken?

5. **Packet E (udp, 5000):** Which rule index matches? What action is taken?

6. **Rule order matters:** If we swapped rules 0 and 3 (put default DROP first), what would happen to Packet A?

### Solution

<details>
<summary>Click to reveal</summary>

1. **Packet A (tcp, 9090):** Rule 0 matches. Action: `ACCEPT`
   - Output: `Matched rule 0: {'protocol': 'tcp', 'port': 9090, 'action': 'ACCEPT'}`

2. **Packet B (tcp, 9091):** Rule 1 matches. Action: `REJECT`
   - Output: `Matched rule 1: {'protocol': 'tcp', 'port': 9091, 'action': 'REJECT'}`

3. **Packet C (udp, 9091):** Rule 2 matches. Action: `DROP`
   - Output: `Matched rule 2: {'protocol': 'udp', 'port': 9091, 'action': 'DROP'}`

4. **Packet D (tcp, 8080):** Rule 3 matches (default TCP rule with `port: None`). Action: `DROP`
   - Output: `Matched rule 3: {'protocol': 'tcp', 'port': None, 'action': 'DROP'}`

5. **Packet E (udp, 5000):** No rule matches (no UDP default rule). Action: `ACCEPT` (Line 8 default policy)
   - Output: No "Matched rule" print, just returns "ACCEPT"

6. **If rules 0 and 3 swapped:** The default DROP rule (`port: None`) would match ALL TCP packets before the specific port rules could be checked. Packet A (tcp, 9090) would be DROPPED instead of ACCEPTED.

**Key insight:** Firewall rules are evaluated in order. More specific rules must come before general/default rules, or they will never match.

</details>

---

## Self-Assessment

After completing these exercises, you should be able to:

- [ ] Trace TCP socket state transitions during connection
- [ ] Predict packet counts for TCP vs UDP operations
- [ ] Understand how `connect_ex()` differs from `connect()`
- [ ] Explain how firewall rule order affects packet matching
- [ ] Distinguish between open, closed and filtered port detection logic

---

*Computer Networks — Week 7: Packet Interception, Filtering and Defensive Port Probing*  
*ASE Bucharest, CSIE | by ing. dr. Antonio Clim*
