# 🧩 Parsons Problems — Week 7
## Computer Networks — ASE, CSIE | Computer Networks Laboratory

> Parsons problems require arranging code blocks in the correct order.
> This technique helps develop understanding of procedural logic without
> the cognitive load of writing syntax from scratch.

---

## How to Use These Problems

1. Read the problem description carefully
2. Identify the blocks that belong in the solution (some are distractors!)
3. Arrange the correct blocks in the proper order
4. Check your solution against the explanation
5. Run the code to verify (where applicable)

**Interactive Mode:** `python3 formative/parsons_runner.py`

---

## Problem P1: TCP Port Probe Implementation

**Learning Objective:** LO1 (Identify TCP/UDP packet fields)  
**Difficulty:** Intermediate  
**Estimated Time:** 5 minutes

### Description

Arrange the code blocks to implement a function that probes a TCP port
and returns its state (open, closed or filtered).

### Available Blocks

```python
# Block A
def probe_tcp_port(host: str, port: int, timeout: float = 2.0) -> str:

# Block B
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Block C
    sock.settimeout(timeout)

# Block D
    try:

# Block E
        result = sock.connect_ex((host, port))

# Block F
        if result == 0:
            return "open"

# Block G
        else:
            return "closed"

# Block H
    except socket.timeout:
        return "filtered"

# Block I
    finally:
        sock.close()
```

### Distractor Blocks (Do NOT include)

```python
# Distractor X - Wrong socket type for TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Distractor Y - Missing error handling
        sock.connect((host, port))
        return "open"

# Distractor Z - Incorrect return value
        return "timeout"
```

### Correct Order

`A → B → C → D → E → F → G → H → I`

### Explanation

1. Function definition with type hints (A)
2. Create TCP socket - SOCK_STREAM for TCP (B)
3. Set timeout before connection attempt (C)
4. Try block for exception handling (D)
5. Non-blocking connect returns error code (E)
6. Result 0 means successful connection (F)
7. Non-zero result means connection refused (G)
8. Timeout exception indicates filtered port (H)
9. Always close socket in finally block (I)

**Why Distractors Are Wrong:**
- X: SOCK_DGRAM is for UDP, not TCP
- Y: connect() raises exception, connect_ex() returns error code
- Z: "timeout" is not a standard port state

---

## Problem P2: Parse iptables Output

**Learning Objective:** LO3 (Implement filtering rules)  
**Difficulty:** Intermediate  
**Estimated Time:** 5 minutes

### Description

Arrange the code blocks to parse iptables output and extract rule information.

### Available Blocks

```python
# Block A
def parse_iptables_rules(output: str) -> list[dict]:

# Block B
    rules = []

# Block C
    lines = output.strip().split('\n')

# Block D
    for line in lines[2:]:  # Skip header lines

# Block E
        if not line.strip():
            continue

# Block F
        parts = line.split()

# Block G
        if len(parts) >= 4:

# Block H
            rule = {
                'target': parts[0],
                'protocol': parts[1],
                'source': parts[3],
                'destination': parts[4] if len(parts) > 4 else 'anywhere'
            }

# Block I
            rules.append(rule)

# Block J
    return rules
```

### Distractor Blocks (Do NOT include)

```python
# Distractor X - Wrong indexing
    for line in lines:  # Includes headers

# Distractor Y - Missing validation
        rule = {'target': parts[0]}
        rules.append(rule)

# Distractor Z - Incorrect return
    return output
```

### Correct Order

`A → B → C → D → E → F → G → H → I → J`

### Explanation

1. Function signature with return type (A)
2. Initialise empty results list (B)
3. Split output into lines (C)
4. Skip first two header lines with [2:] slice (D)
5. Skip empty lines (E)
6. Split line into whitespace-separated parts (F)
7. Validate sufficient parts exist (G)
8. Create rule dictionary with extracted fields (H)
9. Add rule to results (I)
10. Return collected rules (J)

**Why Distractors Are Wrong:**
- X: Would include "Chain INPUT" and column headers
- Y: Missing fields and validation
- Z: Returns raw string instead of parsed data

---

## Problem P3: UDP Send with Error Handling

**Learning Objective:** LO2 (Explain app vs network-layer failures)  
**Difficulty:** Basic  
**Estimated Time:** 3 minutes

### Description

Arrange the blocks to send a UDP datagram with proper error handling
that acknowledges UDP's fire-and-forget nature.

### Available Blocks

```python
# Block A
def send_udp_message(host: str, port: int, message: str) -> tuple[bool, str]:

# Block B
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Block C
    try:

# Block D
        sock.sendto(message.encode('utf-8'), (host, port))

# Block E
        # Note: Success only means packet was sent, not delivered
        return (True, "Datagram sent (delivery not confirmed)")

# Block F
    except OSError as e:
        return (False, f"Send failed: {e}")

# Block G
    finally:
        sock.close()
```

### Distractor Blocks (Do NOT include)

```python
# Distractor X - Wrong assumption about UDP
        return (True, "Message delivered successfully")

# Distractor Y - Unnecessary for UDP
        sock.connect((host, port))
        sock.send(message.encode('utf-8'))

# Distractor Z - TCP socket type
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

### Correct Order

`A → B → C → D → E → F → G`

### Explanation

1. Function with return type indicating success and message (A)
2. Create UDP socket - SOCK_DGRAM (B)
3. Try block for error handling (C)
4. sendto() for connectionless UDP (D)
5. Return acknowledges no delivery confirmation (E)
6. Catch OS-level errors (F)
7. Clean up socket (G)

**Why Distractors Are Wrong:**
- X: UDP cannot confirm delivery
- Y: connect() not needed for UDP (and misleading)
- Z: SOCK_STREAM is TCP, not UDP

---

## Problem P4: Apply Firewall Profile from JSON

**Learning Objective:** LO5 (Design custom firewall profiles)  
**Difficulty:** Advanced  
**Estimated Time:** 7 minutes

### Description

Arrange the blocks to load a firewall profile from JSON and apply
the rules using iptables commands.

### Available Blocks

```python
# Block A
def apply_firewall_profile(profile_path: str, profile_name: str) -> bool:

# Block B
    with open(profile_path, 'r') as f:
        profiles = json.load(f)

# Block C
    if profile_name not in profiles:
        print(f"Profile '{profile_name}' not found")
        return False

# Block D
    profile = profiles[profile_name]

# Block E
    # Clear existing rules in chain
    subprocess.run(['iptables', '-F', 'FORWARD'], check=True)

# Block F
    # Set default policy
    policy = profile.get('forward_policy', 'ACCEPT')
    subprocess.run(['iptables', '-P', 'FORWARD', policy], check=True)

# Block G
    # Apply rules in order (first match wins)
    for rule in profile.get('rules', []):

# Block H
        cmd = ['iptables', '-A', rule.get('chain', 'FORWARD')]
        if 'proto' in rule:
            cmd.extend(['-p', rule['proto']])
        if 'dport' in rule:
            cmd.extend(['--dport', str(rule['dport'])])
        cmd.extend(['-j', rule.get('action', 'ACCEPT')])

# Block I
        subprocess.run(cmd, check=True)

# Block J
    return True
```

### Distractor Blocks (Do NOT include)

```python
# Distractor X - Wrong chain clear
    subprocess.run(['iptables', '-F'], check=True)  # Clears ALL chains

# Distractor Y - Missing policy setting
    # Jump straight to rules without setting policy

# Distractor Z - Wrong rule order
    for rule in reversed(profile.get('rules', [])):  # Wrong order!

# Distractor W - Insecure command construction
        cmd = f"iptables -A FORWARD {rule}"  # Shell injection risk
        os.system(cmd)
```

### Correct Order

`A → B → C → D → E → F → G → H → I → J`

### Explanation

1. Function signature (A)
2. Load JSON file (B)
3. Validate profile exists (C)
4. Extract profile data (D)
5. Clear FORWARD chain specifically (E)
6. Set default policy from profile (F)
7. Iterate rules in order (G)
8. Build command list safely (H)
9. Execute each rule (I)
10. Return success (J)

**Why Distractors Are Wrong:**
- X: `-F` without chain clears ALL chains including INPUT
- Y: Missing policy could leave chain in unexpected state
- Z: Rules must be applied in order (first match wins)
- W: Shell injection vulnerability and deprecated os.system

---

## Problem P5: Analyse PCAP with tshark

**Learning Objective:** LO4 (Analyse packet captures)  
**Difficulty:** Intermediate  
**Estimated Time:** 5 minutes

### Description

Arrange the blocks to analyse a PCAP file and extract TCP connection statistics.

### Available Blocks

```python
# Block A
def analyse_tcp_connections(pcap_path: str) -> dict:

# Block B
    cmd = [
        'tshark', '-r', pcap_path,
        '-q', '-z', 'conv,tcp'
    ]

# Block C
    result = subprocess.run(cmd, capture_output=True, text=True)

# Block D
    if result.returncode != 0:
        return {'error': result.stderr}

# Block E
    stats = {
        'total_connections': 0,
        'total_bytes': 0,
        'connections': []
    }

# Block F
    for line in result.stdout.split('\n'):

# Block G
        if '<->' in line:  # Connection line format

# Block H
            parts = line.split()
            if len(parts) >= 10:
                stats['connections'].append({
                    'endpoints': f"{parts[0]} <-> {parts[2]}",
                    'frames': int(parts[4]) + int(parts[7]),
                    'bytes': int(parts[5]) + int(parts[8])
                })
                stats['total_connections'] += 1
                stats['total_bytes'] += int(parts[5]) + int(parts[8])

# Block I
    return stats
```

### Distractor Blocks (Do NOT include)

```python
# Distractor X - Missing quiet flag
    cmd = ['tshark', '-r', pcap_path, '-z', 'conv,tcp']  # Verbose output

# Distractor Y - Wrong parsing
        stats['connections'].append(line)  # Raw line, not parsed

# Distractor Z - Ignoring errors
    result = subprocess.run(cmd, capture_output=True, text=True)
    # No error checking
    for line in result.stdout.split('\n'):
```

### Correct Order

`A → B → C → D → E → F → G → H → I`

### Explanation

1. Function with return type (A)
2. Build tshark command with conversation stats (B)
3. Run command capturing output (C)
4. Check for errors (D)
5. Initialise statistics dictionary (E)
6. Iterate through output lines (F)
7. Identify connection lines by marker (G)
8. Parse and accumulate statistics (H)
9. Return results (I)

**Why Distractors Are Wrong:**
- X: Without `-q`, output includes packet details making parsing harder
- Y: Storing raw lines loses structured data
- Z: Ignoring errors could lead to parsing garbage

---

## Answer Key Summary

| Problem | LO | Correct Order | Distractors |
|---------|-----|---------------|-------------|
| P1 | LO1 | A→B→C→D→E→F→G→H→I | X, Y, Z |
| P2 | LO3 | A→B→C→D→E→F→G→H→I→J | X, Y, Z |
| P3 | LO2 | A→B→C→D→E→F→G | X, Y, Z |
| P4 | LO5 | A→B→C→D→E→F→G→H→I→J | X, Y, Z, W |
| P5 | LO4 | A→B→C→D→E→F→G→H→I | X, Y, Z |

---

## Self-Assessment Rubric

| Score | Interpretation |
|-------|----------------|
| 5/5 correct | Excellent understanding of networking code patterns |
| 4/5 correct | Good understanding, review the missed concept |
| 3/5 correct | Adequate, additional practice recommended |
| <3/5 correct | Review theory and code tracing exercises first |

---

## Interactive Runner

Run Parsons problems interactively:

```bash
# All problems
python3 formative/parsons_runner.py

# With hints enabled
python3 formative/parsons_runner.py --hints

# Specific problem
python3 formative/parsons_runner.py --problem P1
```

---

*Computer Networks — Week 7: Packet Interception, Filtering and Defensive Port Probing*  
*ASE Bucharest, CSIE | Computer Networks Laboratory*
