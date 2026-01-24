# 🧩 Parsons Problems — Week 7: Packet Capture and Filtering

## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Reorder the code blocks to create a working solution.  
> Each problem includes one or more **distractor blocks** that should NOT be used.

---

## How to Use These Problems

Parsons problems develop code comprehension without the cognitive load of syntax recall. For each problem:

1. **Read** the task description carefully
2. **Identify** which blocks are distractors (not needed)
3. **Arrange** the remaining blocks in the correct order
4. **Verify** by tracing through the logic mentally
5. **Check** your answer against the solution

**Pair Programming Adaptation:**
- Navigator reads the task aloud
- Driver arranges blocks on paper/whiteboard
- Discuss disagreements before revealing solution

---

## Problem P1: TCP Port Probe with Timeout

### Task

Create a function that probes a TCP port and returns one of three states: `"open"`, `"closed"`, or `"filtered"`. The function should:
- Create a TCP socket
- Set a timeout of 2 seconds
- Attempt to connect
- Return the appropriate state based on the result

### Scrambled Blocks

```python
# Block A
    return "open"

# Block B
def probe_port(host: str, port: int) -> str:

# Block C
    sock.settimeout(2)

# Block D
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Block E
    result = sock.connect_ex((host, port))

# Block F
    if result == 0:

# Block G
    sock.close()
    return "closed"

# Block H (DISTRACTOR)
    sock.bind(('', 0))

# Block I
    except socket.timeout:
        return "filtered"

# Block J
    try:

# Block K (DISTRACTOR)
    sock.listen(1)
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block B
def probe_port(host: str, port: int) -> str:

# Block J
    try:

# Block D
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Block C
    sock.settimeout(2)

# Block E
    result = sock.connect_ex((host, port))

# Block F
    if result == 0:

# Block A
        return "open"

# Block G
    sock.close()
    return "closed"

# Block I
    except socket.timeout:
        return "filtered"
```

**Distractors explained:**
- **Block H** (`sock.bind`) — Used for servers, not clients. Binding is unnecessary for outgoing connections.
- **Block K** (`sock.listen`) — Used for servers to accept connections. Probing is a client operation.

**Key insight:** The distinction between `"closed"` and `"filtered"` depends on whether we receive a response (RST for closed) or timeout (no response for filtered).

</details>

---

## Problem P2: Parse iptables Rule Output

### Task

Create a function that parses a single line of `iptables -L -n` output and extracts the action, protocol and destination port. The function should return a dictionary with keys `"action"`, `"protocol"` and `"dport"`.

Example input: `"DROP       tcp  --  0.0.0.0/0  0.0.0.0/0  tcp dpt:9090"`

### Scrambled Blocks

```python
# Block A
    return {
        "action": parts[0],
        "protocol": parts[1],
        "dport": dport
    }

# Block B
def parse_iptables_line(line: str) -> dict:

# Block C
    parts = line.split()

# Block D
    if "dpt:" in line:
        dport_part = [p for p in parts if p.startswith("dpt:")]
        dport = int(dport_part[0].split(":")[1]) if dport_part else None

# Block E (DISTRACTOR)
    subprocess.run(["iptables", "-L", "-n"])

# Block F
    else:
        dport = None

# Block G (DISTRACTOR)
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW)
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block B
def parse_iptables_line(line: str) -> dict:

# Block C
    parts = line.split()

# Block D
    if "dpt:" in line:
        dport_part = [p for p in parts if p.startswith("dpt:")]
        dport = int(dport_part[0].split(":")[1]) if dport_part else None

# Block F
    else:
        dport = None

# Block A
    return {
        "action": parts[0],
        "protocol": parts[1],
        "dport": dport
    }
```

**Distractors explained:**
- **Block E** (`subprocess.run`) — This function parses existing output; it doesn't run iptables.
- **Block G** (`socket.AF_INET, socket.SOCK_RAW`) — Raw sockets are for packet crafting, not parsing text output.

**Key insight:** Parsing iptables output requires understanding the column structure. The action is always first, protocol second and `dpt:` indicates the destination port.

</details>

---

## Problem P3: UDP Send with Error Handling

### Task

Create a function that sends a UDP message and waits for a response with timeout handling. The function should:
- Create a UDP socket
- Set a 3-second timeout
- Send the message
- Try to receive a response
- Return `(True, response)` on success or `(False, "timeout")` on timeout

### Scrambled Blocks

```python
# Block A
    except socket.timeout:
        return (False, "timeout")

# Block B
def udp_send_recv(host: str, port: int, message: bytes) -> tuple:

# Block C
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Block D
    sock.settimeout(3)

# Block E
    try:

# Block F
        sock.sendto(message, (host, port))

# Block G
        response, addr = sock.recvfrom(1024)
        return (True, response)

# Block H (DISTRACTOR)
        sock.connect((host, port))

# Block I
    finally:
        sock.close()

# Block J (DISTRACTOR)
        sock.accept()
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block B
def udp_send_recv(host: str, port: int, message: bytes) -> tuple:

# Block C
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Block D
    sock.settimeout(3)

# Block E
    try:

# Block F
        sock.sendto(message, (host, port))

# Block G
        response, addr = sock.recvfrom(1024)
        return (True, response)

# Block A
    except socket.timeout:
        return (False, "timeout")

# Block I
    finally:
        sock.close()
```

**Distractors explained:**
- **Block H** (`sock.connect`) — UDP is connectionless; `sendto()` already specifies the destination. While `connect()` can be used with UDP, it's not required here.
- **Block J** (`sock.accept`) — Only TCP servers use `accept()`. UDP has no connection to accept.

**Key insight:** UDP's "fire and forget" nature means we cannot distinguish between a dropped packet and a slow server until the timeout expires.

</details>

---

## Problem P4: Apply Firewall Profile from JSON

### Task

Create a function that reads a firewall profile from JSON and applies each rule using iptables. The function should:
- Load the JSON file
- Iterate through the rules
- Build and execute the iptables command for each rule
- Return the number of rules applied

### Scrambled Blocks

```python
# Block A
    return count

# Block B
def apply_profile(profile_path: str) -> int:

# Block C
    with open(profile_path) as f:
        profile = json.load(f)

# Block D
    count = 0
    for rule in profile["rules"]:

# Block E
        cmd = [
            "iptables", "-A", "INPUT",
            "-p", rule["protocol"],
            "--dport", str(rule["port"]),
            "-j", rule["action"]
        ]

# Block F
        subprocess.run(cmd, check=True)
        count += 1

# Block G (DISTRACTOR)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Block H (DISTRACTOR)
    profile = yaml.safe_load(f)
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block B
def apply_profile(profile_path: str) -> int:

# Block C
    with open(profile_path) as f:
        profile = json.load(f)

# Block D
    count = 0
    for rule in profile["rules"]:

# Block E
        cmd = [
            "iptables", "-A", "INPUT",
            "-p", rule["protocol"],
            "--dport", str(rule["port"]),
            "-j", rule["action"]
        ]

# Block F
        subprocess.run(cmd, check=True)
        count += 1

# Block A
    return count
```

**Distractors explained:**
- **Block G** (`setsockopt`) — Socket options are for network programming, not firewall management.
- **Block H** (`yaml.safe_load`) — The task specifies JSON format, not YAML.

**Key insight:** The iptables command structure is: `iptables -A <chain> -p <protocol> --dport <port> -j <action>`. The `-A` flag appends to the chain.

</details>

---

## Problem P5: Capture Traffic Summary

### Task

Create a function that analyses a pcap file using tshark and returns a summary dictionary with packet counts by protocol. The function should:
- Run tshark with appropriate filters
- Parse the output to count TCP, UDP and ICMP packets
- Return a dictionary with the counts

### Scrambled Blocks

```python
# Block A
    return summary

# Block B
def analyse_pcap(pcap_path: str) -> dict:

# Block C
    summary = {"tcp": 0, "udp": 0, "icmp": 0}

# Block D
    result = subprocess.run(
        ["tshark", "-r", pcap_path, "-T", "fields", "-e", "ip.proto"],
        capture_output=True,
        text=True
    )

# Block E
    for line in result.stdout.strip().split("\n"):
        proto = line.strip()
        if proto == "6":
            summary["tcp"] += 1
        elif proto == "17":
            summary["udp"] += 1
        elif proto == "1":
            summary["icmp"] += 1

# Block F (DISTRACTOR)
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)

# Block G (DISTRACTOR)
    wireshark.open(pcap_path)
```

### Correct Order

<details>
<summary>Click to reveal solution</summary>

```python
# Block B
def analyse_pcap(pcap_path: str) -> dict:

# Block C
    summary = {"tcp": 0, "udp": 0, "icmp": 0}

# Block D
    result = subprocess.run(
        ["tshark", "-r", pcap_path, "-T", "fields", "-e", "ip.proto"],
        capture_output=True,
        text=True
    )

# Block E
    for line in result.stdout.strip().split("\n"):
        proto = line.strip()
        if proto == "6":
            summary["tcp"] += 1
        elif proto == "17":
            summary["udp"] += 1
        elif proto == "1":
            summary["icmp"] += 1

# Block A
    return summary
```

**Distractors explained:**
- **Block F** (`AF_PACKET, SOCK_RAW`) — Raw packet capture requires root privileges and is for live capture, not pcap analysis.
- **Block G** (`wireshark.open`) — There is no Python `wireshark` module. Use `tshark` (command-line) or `pyshark` (library).

**Key insight:** IP protocol numbers are: TCP = 6, UDP = 17, ICMP = 1. The `-T fields -e ip.proto` options extract just the protocol field from each packet.

</details>

---

## Self-Assessment Checklist

After completing these problems, you should be able to:

- [ ] Distinguish between client and server socket operations
- [ ] Understand the difference between TCP (connection-oriented) and UDP (connectionless)
- [ ] Parse structured text output from network tools
- [ ] Construct iptables commands programmatically
- [ ] Use tshark for automated pcap analysis
- [ ] Identify common distractors (wrong operations for the context)

---

## Additional Challenge

Try creating your own Parsons problem for one of these scenarios:
1. A function that checks if a firewall rule exists
2. A function that extracts source/destination IPs from a pcap
3. A function that tests both TCP and UDP connectivity to a host

Share with your pair programming partner and compare solutions.

---

*NETWORKING class - ASE, Informatics | by Revolvix*  
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
