# 🧩 Parsons Problems — Week 13

> Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## What are Parsons Problems?

Parsons Problems are code-ordering exercises where you arrange scrambled code blocks into the correct sequence. They help develop:

- **Code reading skills** — Understanding code structure
- **Logical thinking** — Identifying dependencies between statements
- **Debugging intuition** — Spotting incorrect orderings

**⚠️ Warning:** Some blocks below are **distractors** — they should NOT be included in the solution!

---

## Problem 1: MQTT Publish with QoS

**Learning Objective:** LO1, LO4  
**Difficulty:** ⭐⭐☆☆☆ (Intermediate)  
**Distractors:** 2 blocks

### Task

Arrange the blocks to create a function that publishes an MQTT message with QoS 1 and waits for acknowledgement.

### Scrambled Blocks

```python
# Block A
def mqtt_publish_qos1(broker, topic, message):

# Block B
    client = mqtt.Client()

# Block C
    client.connect(broker, 1883, 60)

# Block D
    result = client.publish(topic, message, qos=1)

# Block E
    result.wait_for_publish()

# Block F
    client.disconnect()

# Block G
    return result.is_published()

# Block H (DISTRACTOR)
    client.subscribe(topic)

# Block I (DISTRACTOR)
    result = client.publish(topic, message, qos=0)
```

<details>
<summary>💡 Hint</summary>

QoS 1 requires waiting for PUBACK. The `wait_for_publish()` method blocks until acknowledgement is received.

</details>

<details>
<summary>✅ Solution</summary>

**Correct order: A → B → C → D → E → F → G**

```python
def mqtt_publish_qos1(broker, topic, message):
    client = mqtt.Client()
    client.connect(broker, 1883, 60)
    result = client.publish(topic, message, qos=1)
    result.wait_for_publish()
    client.disconnect()
    return result.is_published()
```

**Why distractors are wrong:**
- Block H: `subscribe()` is for receiving messages, not publishing
- Block I: Uses QoS 0 (fire-and-forget), not QoS 1

</details>

---

## Problem 2: TCP Port Scanner Function

**Learning Objective:** LO3  
**Difficulty:** ⭐⭐⭐☆☆ (Intermediate)  
**Distractors:** 2 blocks

### Task

Arrange the blocks to create a function that scans a single TCP port and returns its state.

### Scrambled Blocks

```python
# Block A
def scan_port(host, port, timeout=0.5):

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
        else:
            return "closed"

# Block G
    except socket.timeout:
        return "filtered"

# Block H
    finally:
        sock.close()

# Block I (DISTRACTOR)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Block J (DISTRACTOR)
        if result == 1:
            return "open"
```

<details>
<summary>💡 Hint</summary>

- `connect_ex()` returns 0 for success (open port)
- `SOCK_STREAM` is for TCP (connection-oriented)
- `finally` ensures socket cleanup even on exceptions

</details>

<details>
<summary>✅ Solution</summary>

**Correct order: A → B → C → D → E → F → G → H**

```python
def scan_port(host, port, timeout=0.5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((host, port))
        if result == 0:
            return "open"
        else:
            return "closed"
    except socket.timeout:
        return "filtered"
    finally:
        sock.close()
```

**Why distractors are wrong:**
- Block I: `SOCK_DGRAM` is UDP, not TCP
- Block J: `connect_ex()` returns 0 for success, not 1

</details>

---

## Problem 3: TLS Context Configuration

**Learning Objective:** LO2  
**Difficulty:** ⭐⭐⭐☆☆ (Intermediate)  
**Distractors:** 1 block

### Task

Arrange the blocks to create a secure TLS context for MQTT connection.

### Scrambled Blocks

```python
# Block A
def create_tls_context(ca_cert_path):

# Block B
    context = ssl.create_default_context()

# Block C
    context.check_hostname = True

# Block D
    context.verify_mode = ssl.CERT_REQUIRED

# Block E
    context.load_verify_locations(ca_cert_path)

# Block F
    return context

# Block G (DISTRACTOR)
    context.verify_mode = ssl.CERT_NONE
```

<details>
<summary>💡 Hint</summary>

For secure connections:
- `CERT_REQUIRED` ensures server certificate is validated
- `check_hostname = True` verifies the server's identity
- CA certificate must be loaded to verify the server

</details>

<details>
<summary>✅ Solution</summary>

**Correct order: A → B → C → D → E → F**

```python
def create_tls_context(ca_cert_path):
    context = ssl.create_default_context()
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(ca_cert_path)
    return context
```

**Why distractor is wrong:**
- Block G: `CERT_NONE` disables certificate verification, making the connection insecure (vulnerable to MITM attacks)

</details>

---

## Problem 4: Packet Capture Filter

**Learning Objective:** LO5  
**Difficulty:** ⭐⭐☆☆☆ (Easy)  
**Distractors:** 2 blocks

### Task

Arrange the blocks to capture MQTT packets and save to a PCAP file.

### Scrambled Blocks

```python
# Block A
from scapy.all import sniff, wrpcap

# Block B
def capture_mqtt_traffic(interface, count, output_file):

# Block C
    bpf_filter = "tcp port 1883"

# Block D
    packets = sniff(iface=interface, filter=bpf_filter, count=count)

# Block E
    wrpcap(output_file, packets)

# Block F
    return len(packets)

# Block G (DISTRACTOR)
    bpf_filter = "udp port 1883"

# Block H (DISTRACTOR)
    packets = sniff(iface=interface, count=count)
```

<details>
<summary>💡 Hint</summary>

- MQTT uses TCP (not UDP)
- BPF filter must be applied to capture only relevant traffic
- `wrpcap()` saves packets to PCAP format

</details>

<details>
<summary>✅ Solution</summary>

**Correct order: A → B → C → D → E → F**

```python
from scapy.all import sniff, wrpcap

def capture_mqtt_traffic(interface, count, output_file):
    bpf_filter = "tcp port 1883"
    packets = sniff(iface=interface, filter=bpf_filter, count=count)
    wrpcap(output_file, packets)
    return len(packets)
```

**Why distractors are wrong:**
- Block G: MQTT uses TCP, not UDP
- Block H: No filter means capturing ALL traffic, not just MQTT

</details>

---

## Problem 5: Vulnerability Check Workflow

**Learning Objective:** LO6  
**Difficulty:** ⭐⭐⭐⭐☆ (Advanced)  
**Distractors:** 1 block

### Task

Arrange the blocks to create a vulnerability assessment function that checks a service and generates a report.

### Scrambled Blocks

```python
# Block A
def assess_service(target, port, service_type):

# Block B
    report = {"target": target, "port": port, "findings": []}

# Block C
    # Step 1: Verify port is open
    if not is_port_open(target, port):
        report["status"] = "unreachable"
        return report

# Block D
    # Step 2: Grab service banner
    banner = grab_banner(target, port)
    report["banner"] = banner

# Block E
    # Step 3: Identify version
    version = parse_version(banner)
    report["version"] = version

# Block F
    # Step 4: Check for known vulnerabilities
    cves = lookup_cves(service_type, version)
    report["findings"].extend(cves)

# Block G
    # Step 5: Calculate risk score
    report["risk_score"] = calculate_risk(report["findings"])
    report["status"] = "complete"

# Block H
    return report

# Block I (DISTRACTOR)
    # Step 1: Check for vulnerabilities first
    cves = lookup_cves(service_type, "unknown")
```

<details>
<summary>💡 Hint</summary>

The correct order follows a logical workflow:
1. Verify target is reachable
2. Gather information (banner, version)
3. Analyse (CVE lookup)
4. Assess (risk score)

You cannot look up vulnerabilities without knowing the version first!

</details>

<details>
<summary>✅ Solution</summary>

**Correct order: A → B → C → D → E → F → G → H**

```python
def assess_service(target, port, service_type):
    report = {"target": target, "port": port, "findings": []}
    
    # Step 1: Verify port is open
    if not is_port_open(target, port):
        report["status"] = "unreachable"
        return report
    
    # Step 2: Grab service banner
    banner = grab_banner(target, port)
    report["banner"] = banner
    
    # Step 3: Identify version
    version = parse_version(banner)
    report["version"] = version
    
    # Step 4: Check for known vulnerabilities
    cves = lookup_cves(service_type, version)
    report["findings"].extend(cves)
    
    # Step 5: Calculate risk score
    report["risk_score"] = calculate_risk(report["findings"])
    report["status"] = "complete"
    
    return report
```

**Why distractor is wrong:**
- Block I: Looking up CVEs with "unknown" version is useless. You must first identify the version through banner grabbing, then look up vulnerabilities for that specific version.

</details>

---

## Scoring Rubric

Use this rubric for self-assessment:

| Score | Criteria |
|-------|----------|
| **5/5** | Correct order, no distractors included, can explain why |
| **4/5** | Correct order, no distractors, minor hesitation |
| **3/5** | Mostly correct, one block misplaced OR one distractor included |
| **2/5** | Several blocks misplaced, logic unclear |
| **1/5** | Significant errors, distractors included |
| **0/5** | Could not complete |

---

## Tips for Solving Parsons Problems

1. **Identify the function signature first** — This is always Block A
2. **Look for dependencies** — Some blocks require others to run first
3. **Watch for try/except/finally** — These must be properly nested
4. **Check return statements** — Usually come last
5. **Spot distractors by logic errors** — Wrong protocols, wrong values, missing prerequisites

---

## Additional Practice

For more practice, try:

1. **Reverse engineering** — Take working code and identify the logical order
2. **Error insertion** — Find the bug in intentionally broken code
3. **Code completion** — Fill in missing blocks from a partial solution

---

*Computer Networks — Week 13: IoT and Security*  
*ASE Bucharest, CSIE | by ing. dr. Antonio Clim*
