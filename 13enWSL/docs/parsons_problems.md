# 🧩 Parsons Problems — Week 13
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Reorder the code blocks to create a working solution. Some blocks may be distractors (not needed).

---

## Problem P1: MQTT Publish with QoS

### Task
Create a function that publishes a message to an MQTT broker with QoS 1 and waits for acknowledgement.

### Scrambled Blocks

```python
# Block A
    client.loop_stop()
    return True

# Block B
def publish_with_ack(broker: str, port: int, topic: str, message: str) -> bool:

# Block C
    client.on_publish = on_publish

# Block D
    ack_received = False

# Block E
    def on_publish(client, userdata, mid):
        nonlocal ack_received
        ack_received = True

# Block F
    client = mqtt.Client()

# Block G
    client.connect(broker, port)
    client.loop_start()

# Block H
    client.publish(topic, message, qos=1)

# Block I (DISTRACTOR)
    client.subscribe(topic)

# Block J
    import time
    timeout = time.time() + 5
    while not ack_received and time.time() < timeout:
        time.sleep(0.1)

# Block K (DISTRACTOR)
    client.disconnect()
    return ack_received
```

### Hints
- The function needs to track whether an acknowledgement was received
- QoS 1 requires the `on_publish` callback to confirm delivery
- We need to wait for the acknowledgement before returning
- One block subscribes to a topic — is that needed for publishing?

### Correct Order
<details>
<summary>Click to reveal solution</summary>

```python
# Block B
def publish_with_ack(broker: str, port: int, topic: str, message: str) -> bool:

# Block D
    ack_received = False

# Block E
    def on_publish(client, userdata, mid):
        nonlocal ack_received
        ack_received = True

# Block F
    client = mqtt.Client()

# Block C
    client.on_publish = on_publish

# Block G
    client.connect(broker, port)
    client.loop_start()

# Block H
    client.publish(topic, message, qos=1)

# Block J
    import time
    timeout = time.time() + 5
    while not ack_received and time.time() < timeout:
        time.sleep(0.1)

# Block A
    client.loop_stop()
    return True
```

**Distractors:**
- Block I (`client.subscribe(topic)`) — subscribing is not needed for publishing
- Block K — contains duplicate `return` statement; Block A handles cleanup correctly

**Key insight:** The `on_publish` callback is essential for QoS 1 to know when the broker acknowledged the message.
</details>

---

## Problem P2: TCP Port Scanner Function

### Task
Create a function that scans a single port and returns its state (open, closed, or filtered).

### Scrambled Blocks

```python
# Block A
    except socket.timeout:
        return "filtered"

# Block B
def scan_port(host: str, port: int, timeout: float = 0.5) -> str:

# Block C
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Block D
        return "open"

# Block E
    sock.settimeout(timeout)

# Block F
    try:

# Block G
        result = sock.connect_ex((host, port))

# Block H
    finally:
        sock.close()

# Block I
        if result == 0:

# Block J
        else:
            return "closed"

# Block K (DISTRACTOR)
    sock.bind(('', 0))

# Block L (DISTRACTOR)
        sock.send(b"HELLO")
```

### Hints
- Socket must be created before setting timeout
- `connect_ex()` returns 0 for successful connection
- The socket must always be closed (use `finally`)
- Port scanning doesn't require binding to a local port
- We're checking if port is open, not sending data

### Correct Order
<details>
<summary>Click to reveal solution</summary>

```python
# Block B
def scan_port(host: str, port: int, timeout: float = 0.5) -> str:

# Block C
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Block E
    sock.settimeout(timeout)

# Block F
    try:

# Block G
        result = sock.connect_ex((host, port))

# Block I
        if result == 0:

# Block D
            return "open"

# Block J
        else:
            return "closed"

# Block A
    except socket.timeout:
        return "filtered"

# Block H
    finally:
        sock.close()
```

**Distractors:**
- Block K (`sock.bind(('', 0))`) — binding is for servers, not clients
- Block L (`sock.send(b"HELLO")`) — port scanning only checks if connection succeeds

**Key insight:** `connect_ex()` returns an error code instead of raising an exception, making it ideal for scanning.
</details>

---

## Problem P3: TLS Context Configuration

### Task
Create a function that configures an SSL context for connecting to an MQTT broker with TLS.

### Scrambled Blocks

```python
# Block A
    return context

# Block B
def create_tls_context(ca_file: str, verify: bool = True) -> ssl.SSLContext:

# Block C
    context = ssl.create_default_context()

# Block D
    context.load_verify_locations(ca_file)

# Block E
    if not verify:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

# Block F (DISTRACTOR)
    context.set_ciphers('HIGH:!aNULL:!MD5')

# Block G
    import ssl

# Block H (DISTRACTOR)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)

# Block I (DISTRACTOR)
    context.load_cert_chain('client.crt', 'client.key')
```

### Hints
- Import statement comes first
- `create_default_context()` is preferred over manual `SSLContext()`
- CA file must be loaded for server verification
- Disabling verification should be conditional
- Client certificates are optional and not needed here

### Correct Order
<details>
<summary>Click to reveal solution</summary>

```python
# Block G
    import ssl

# Block B
def create_tls_context(ca_file: str, verify: bool = True) -> ssl.SSLContext:

# Block C
    context = ssl.create_default_context()

# Block D
    context.load_verify_locations(ca_file)

# Block E
    if not verify:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

# Block A
    return context
```

**Distractors:**
- Block F (`set_ciphers`) — `create_default_context()` already sets secure ciphers
- Block H (`SSLContext(ssl.PROTOCOL_TLS)`) — manual context creation is less secure than `create_default_context()`
- Block I (`load_cert_chain`) — client certificates are for mutual TLS, not required for basic server authentication

**Key insight:** `create_default_context()` provides secure defaults; only override when necessary.
</details>

---

## Problem P4: Packet Capture Filter

### Task
Create a function that captures packets matching specific ports and saves them to a file.

### Scrambled Blocks

```python
# Block A
    return len(packets)

# Block B
def capture_lab_traffic(interface: str, output_file: str, duration: int = 10) -> int:

# Block C
    from scapy.all import sniff, wrpcap

# Block D
    packets = sniff(
        iface=interface,
        filter=bpf_filter,
        timeout=duration
    )

# Block E
    # Week 13 ports: MQTT (1883, 8883), DVWA (8080), FTP (2121)
    bpf_filter = "tcp port 1883 or tcp port 8883 or tcp port 8080 or tcp port 2121"

# Block F
    wrpcap(output_file, packets)

# Block G (DISTRACTOR)
    packets = sniff(iface=interface, count=100)

# Block H (DISTRACTOR)
    bpf_filter = "ip"
```

### Hints
- Import scapy functions first
- Define the BPF filter before using it
- Use timeout-based capture for predictable duration
- Save packets after capture completes
- "ip" filter is too broad for lab traffic

### Correct Order
<details>
<summary>Click to reveal solution</summary>

```python
# Block C
    from scapy.all import sniff, wrpcap

# Block B
def capture_lab_traffic(interface: str, output_file: str, duration: int = 10) -> int:

# Block E
    # Week 13 ports: MQTT (1883, 8883), DVWA (8080), FTP (2121)
    bpf_filter = "tcp port 1883 or tcp port 8883 or tcp port 8080 or tcp port 2121"

# Block D
    packets = sniff(
        iface=interface,
        filter=bpf_filter,
        timeout=duration
    )

# Block F
    wrpcap(output_file, packets)

# Block A
    return len(packets)
```

**Distractors:**
- Block G (`count=100`) — count-based capture doesn't respect duration
- Block H (`bpf_filter = "ip"`) — captures all IP traffic, not specific to lab

**Key insight:** BPF filters are essential for capturing only relevant traffic; timeout ensures predictable capture duration.
</details>

---

## Problem P5: Vulnerability Check Result

### Task
Create a data class and function to check if anonymous MQTT access is enabled.

### Scrambled Blocks

```python
# Block A
    return VulnResult(
        name="Anonymous MQTT",
        vulnerable=True,
        details="Broker accepts connections without credentials"
    )

# Block B
@dataclass
class VulnResult:
    name: str
    vulnerable: bool
    details: str

# Block C
def check_anonymous_mqtt(host: str, port: int = 1883) -> VulnResult:

# Block D
    from dataclasses import dataclass
    import paho.mqtt.client as mqtt

# Block E
    try:
        client = mqtt.Client()
        client.connect(host, port, keepalive=5)
        client.disconnect()

# Block F
    except Exception:
        return VulnResult(
            name="Anonymous MQTT",
            vulnerable=False,
            details="Connection failed or requires authentication"
        )

# Block G (DISTRACTOR)
    client.username_pw_set("admin", "admin")

# Block H (DISTRACTOR)
        client.subscribe("#")
```

### Correct Order
<details>
<summary>Click to reveal solution</summary>

```python
# Block D
    from dataclasses import dataclass
    import paho.mqtt.client as mqtt

# Block B
@dataclass
class VulnResult:
    name: str
    vulnerable: bool
    details: str

# Block C
def check_anonymous_mqtt(host: str, port: int = 1883) -> VulnResult:

# Block E
    try:
        client = mqtt.Client()
        client.connect(host, port, keepalive=5)
        client.disconnect()

# Block A
    return VulnResult(
        name="Anonymous MQTT",
        vulnerable=True,
        details="Broker accepts connections without credentials"
    )

# Block F
    except Exception:
        return VulnResult(
            name="Anonymous MQTT",
            vulnerable=False,
            details="Connection failed or requires authentication"
        )
```

**Distractors:**
- Block G (`username_pw_set`) — we're testing anonymous access, so no credentials
- Block H (`subscribe("#")`) — connecting without auth is enough to prove vulnerability

**Key insight:** If connection succeeds without credentials, the broker allows anonymous access — a security vulnerability.
</details>

---

## Tips for Solving Parsons Problems

1. **Identify the function signature** — always starts the sequence
2. **Find imports** — usually at the very beginning
3. **Track variable dependencies** — variables must be defined before use
4. **Look for try/except/finally patterns** — `finally` always comes last in try block
5. **Spot distractors** — blocks that add functionality not required by the task
6. **Check return statements** — usually near the end

---

*Computer Networks — Week 13: IoT and Security*
*ASE Bucharest, CSIE | by ing. dr. Antonio Clim*
