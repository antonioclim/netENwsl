# 🔍 Code Tracing Exercises — Week 13
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Trace through the code mentally before running it. This builds your ability to predict programme behaviour — a critical debugging skill.

---

## Exercise T1: Port Scanner Logic

### 💭 Prediction
Before tracing, predict: How many ports will be reported as "open"?

### Code
```python
import socket

def scan_port(host: str, port: int, timeout: float = 0.5) -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    
    try:
        error_code = sock.connect_ex((host, port))
        if error_code == 0:
            return "open"
        else:
            return "closed"
    except socket.timeout:
        return "filtered"
    finally:
        sock.close()

# Test execution
results = {}
ports_to_scan = [22, 80, 1883, 8080, 9999]
host = "localhost"

for port in ports_to_scan:
    results[port] = scan_port(host, port)

open_count = sum(1 for state in results.values() if state == "open")
print(f"Open ports: {open_count}")
```

### Context
Assume the following services are running:
- SSH on port 22
- Mosquitto MQTT on port 1883
- DVWA on port 8080
- Nothing on ports 80 and 9999

### Questions

1. **Line by line:** What is the value of `error_code` when scanning port 1883?

2. **State tracking:** Complete the table after the for loop completes:

| Port | `results[port]` |
|------|-----------------|
| 22 | ? |
| 80 | ? |
| 1883 | ? |
| 8080 | ? |
| 9999 | ? |

3. **Output prediction:** What will be printed?

### Solution
<details>
<summary>Click to reveal</summary>

1. **error_code for port 1883:** `0` (connection successful)

2. **State tracking:**

| Port | `results[port]` |
|------|-----------------|
| 22 | "open" |
| 80 | "closed" |
| 1883 | "open" |
| 8080 | "open" |
| 9999 | "closed" |

3. **Output:** `Open ports: 3`

**Explanation:**
- Port 22 (SSH): Service listening → `connect_ex()` returns 0 → "open"
- Port 80: No service → `connect_ex()` returns non-zero (111 = ECONNREFUSED) → "closed"
- Port 1883 (MQTT): Service listening → `connect_ex()` returns 0 → "open"
- Port 8080 (DVWA): Service listening → `connect_ex()` returns 0 → "open"
- Port 9999: No service → "closed"

Note: If a firewall drops packets, port 80/9999 would be "filtered" instead of "closed".
</details>

---

## Exercise T2: MQTT Client Flow

### 💭 Prediction
Before tracing, predict: How many times will `on_message` be called?

### Code
```python
import paho.mqtt.client as mqtt
import time

message_count = 0
connected = False

def on_connect(client, userdata, flags, rc):
    global connected
    print(f"Connected: rc={rc}")
    connected = True
    if rc == 0:
        client.subscribe("sensors/#", qos=1)

def on_message(client, userdata, msg):
    global message_count
    message_count += 1
    print(f"Message {message_count}: {msg.topic}")

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Subscribed: mid={mid}, qos={granted_qos}")

# Setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

# Connect and run
client.connect("localhost", 1883)
client.loop_start()

# Wait for connection
time.sleep(1)

# Simulate external publishes (assume these happen):
# - "sensors/temp" with payload "22.5"
# - "sensors/humidity" with payload "65"
# - "weather/temp" with payload "18.0"

time.sleep(2)
client.disconnect()
client.loop_stop()

print(f"Total messages: {message_count}")
```

### Context
Assume the broker receives these publishes during the 2-second wait:
1. Topic: `sensors/temp`, Payload: `"22.5"`
2. Topic: `sensors/humidity`, Payload: `"65"`
3. Topic: `weather/temp`, Payload: `"18.0"`

### Questions

1. **Callback order:** In what order will the callbacks execute?

2. **Message filtering:** Which of the three published messages will trigger `on_message`?

3. **Final state:** What values will these variables have at the end?

| Variable | Final Value |
|----------|-------------|
| `connected` | ? |
| `message_count` | ? |

4. **Output prediction:** Write the complete console output.

### Solution
<details>
<summary>Click to reveal</summary>

1. **Callback order:**
   - `on_connect` (when connection established)
   - `on_subscribe` (when subscription confirmed)
   - `on_message` (for each matching message)

2. **Message filtering:**
   - `sensors/temp` → ✅ Matches `sensors/#`
   - `sensors/humidity` → ✅ Matches `sensors/#`
   - `weather/temp` → ❌ Does NOT match `sensors/#`

3. **Final state:**

| Variable | Final Value |
|----------|-------------|
| `connected` | `True` |
| `message_count` | `2` |

4. **Console output:**
```
Connected: rc=0
Subscribed: mid=1, qos=(1,)
Message 1: sensors/temp
Message 2: sensors/humidity
Total messages: 2
```

**Explanation:**
- The `#` wildcard matches all levels under `sensors/`, so both `sensors/temp` and `sensors/humidity` match
- `weather/temp` does not start with `sensors/`, so it's not delivered
- The third message is published but never received by this client
</details>

---

## Exercise T3: TLS Handshake State Machine

### 💭 Prediction
Before tracing, predict: Will the connection succeed or fail?

### Code
```python
import ssl
import socket

def connect_with_tls(host: str, port: int, ca_file: str) -> dict:
    state = {
        "socket_created": False,
        "context_created": False,
        "wrapped": False,
        "connected": False,
        "verified": False,
        "error": None
    }
    
    try:
        # Step 1: Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        state["socket_created"] = True
        sock.settimeout(5)
        
        # Step 2: Create SSL context
        context = ssl.create_default_context()
        state["context_created"] = True
        
        # Step 3: Load CA certificate
        context.load_verify_locations(ca_file)
        
        # Step 4: Wrap socket
        secure_sock = context.wrap_socket(sock, server_hostname=host)
        state["wrapped"] = True
        
        # Step 5: Connect
        secure_sock.connect((host, port))
        state["connected"] = True
        
        # Step 6: Verify certificate
        cert = secure_sock.getpeercert()
        if cert:
            state["verified"] = True
            
    except FileNotFoundError as e:
        state["error"] = f"CA file not found: {e}"
    except ssl.SSLCertVerificationError as e:
        state["error"] = f"Certificate verification failed: {e}"
    except socket.timeout:
        state["error"] = "Connection timeout"
    except ConnectionRefusedError:
        state["error"] = "Connection refused"
    except Exception as e:
        state["error"] = f"Unexpected: {e}"
    
    return state

# Test scenarios
result = connect_with_tls("localhost", 8883, "docker/configs/certs/ca.crt")
```

### Scenarios
Trace the code for each scenario:

**Scenario A:** CA file exists, server running, certificate valid
**Scenario B:** CA file does not exist
**Scenario C:** CA file exists, but server not running
**Scenario D:** CA file exists, server running, but certificate is self-signed with different CA

### Questions

For each scenario, complete the state dictionary:

**Scenario A (all correct):**
| Key | Value |
|-----|-------|
| socket_created | ? |
| context_created | ? |
| wrapped | ? |
| connected | ? |
| verified | ? |
| error | ? |

**Scenario B (missing CA file):**
| Key | Value |
|-----|-------|
| socket_created | ? |
| context_created | ? |
| wrapped | ? |
| connected | ? |
| verified | ? |
| error | ? |

### Solution
<details>
<summary>Click to reveal</summary>

**Scenario A (all correct):**
| Key | Value |
|-----|-------|
| socket_created | `True` |
| context_created | `True` |
| wrapped | `True` |
| connected | `True` |
| verified | `True` |
| error | `None` |

**Scenario B (missing CA file):**
| Key | Value |
|-----|-------|
| socket_created | `True` |
| context_created | `True` |
| wrapped | `False` |
| connected | `False` |
| verified | `False` |
| error | `"CA file not found: ..."` |

Exception occurs at `context.load_verify_locations(ca_file)` which raises `FileNotFoundError`.

**Scenario C (server not running):**
| Key | Value |
|-----|-------|
| socket_created | `True` |
| context_created | `True` |
| wrapped | `True` |
| connected | `False` |
| verified | `False` |
| error | `"Connection refused"` |

**Scenario D (wrong CA):**
| Key | Value |
|-----|-------|
| socket_created | `True` |
| context_created | `True` |
| wrapped | `True` |
| connected | `False` |
| verified | `False` |
| error | `"Certificate verification failed: ..."` |

The SSL handshake fails during `connect()` because the server's certificate is not signed by the loaded CA.
</details>

---

## Exercise T4: Packet Sniffer Protocol Detection

### 💭 Prediction
Before tracing, predict: What protocol will be detected for each packet?

### Code
```python
from typing import Optional

def detect_protocol(src_port: int, dst_port: int, payload: bytes) -> str:
    """
    Detect protocol based on port numbers and payload inspection.
    
    💭 PREDICTION: What will this function return for MQTT over TLS traffic?
    """
    # Known port mappings
    MQTT_PORTS = {1883, 8883}
    HTTP_PORTS = {80, 8080, 443, 8443}
    FTP_PORTS = {20, 21, 2121}
    
    # Check by port first
    all_ports = {src_port, dst_port}
    
    if all_ports & MQTT_PORTS:
        # Check if it looks like MQTT (starts with specific bytes)
        if payload and len(payload) >= 2:
            # MQTT CONNECT starts with 0x10, PUBLISH with 0x30-0x3F
            first_byte = payload[0]
            if first_byte == 0x10 or (0x30 <= first_byte <= 0x3F):
                return "MQTT"
            # TLS starts with 0x16 (handshake) or 0x17 (application data)
            if first_byte in (0x16, 0x17):
                return "MQTT-TLS"
        return "MQTT-like"
    
    if all_ports & HTTP_PORTS:
        if payload:
            try:
                text = payload[:20].decode('ascii', errors='ignore')
                if text.startswith(('GET ', 'POST ', 'HTTP/')):
                    return "HTTP"
                if payload[0] in (0x16, 0x17):
                    return "HTTPS"
            except Exception:
                pass
        return "HTTP-like"
    
    if all_ports & FTP_PORTS:
        if payload:
            try:
                text = payload[:10].decode('ascii', errors='ignore')
                if text.startswith('220 ') or text.startswith('USER '):
                    return "FTP"
            except Exception:
                pass
        return "FTP-like"
    
    return "Unknown"


# Test packets
packets = [
    {"src": 54321, "dst": 1883,  "payload": b"\x10\x0c\x00\x04MQTT"},  # MQTT CONNECT
    {"src": 1883,  "dst": 54321, "payload": b"\x20\x02\x00\x00"},      # MQTT CONNACK
    {"src": 54321, "dst": 8883,  "payload": b"\x16\x03\x03\x00\x05"},  # TLS handshake
    {"src": 8883,  "dst": 54321, "payload": b"\x17\x03\x03\x00\x1a"},  # TLS app data
    {"src": 54321, "dst": 8080,  "payload": b"GET / HTTP/1.1\r\n"},   # HTTP request
    {"src": 54321, "dst": 2121,  "payload": b"USER anonymous\r\n"},   # FTP command
    {"src": 2121,  "dst": 54321, "payload": b"220 Welcome\r\n"},      # FTP banner
    {"src": 54321, "dst": 9999,  "payload": b"\x00\x01\x02\x03"},      # Unknown
]

results = []
for pkt in packets:
    protocol = detect_protocol(pkt["src"], pkt["dst"], pkt["payload"])
    results.append(f"{pkt['src']}→{pkt['dst']}: {protocol}")
    
for r in results:
    print(r)
```

### Questions

1. **State tracking:** Complete the results list:

| Packet | src→dst | Expected Protocol |
|--------|---------|-------------------|
| 1 | 54321→1883 | ? |
| 2 | 1883→54321 | ? |
| 3 | 54321→8883 | ? |
| 4 | 8883→54321 | ? |
| 5 | 54321→8080 | ? |
| 6 | 54321→2121 | ? |
| 7 | 2121→54321 | ? |
| 8 | 54321→9999 | ? |

2. **Edge case:** What would happen if packet 3 had an empty payload?

3. **Code understanding:** Why does the code check `all_ports & MQTT_PORTS` instead of just checking `dst_port`?

### Solution
<details>
<summary>Click to reveal</summary>

1. **Results:**

| Packet | src→dst | Expected Protocol |
|--------|---------|-------------------|
| 1 | 54321→1883 | "MQTT" |
| 2 | 1883→54321 | "MQTT-like" |
| 3 | 54321→8883 | "MQTT-TLS" |
| 4 | 8883→54321 | "MQTT-TLS" |
| 5 | 54321→8080 | "HTTP" |
| 6 | 54321→2121 | "FTP" |
| 7 | 2121→54321 | "FTP" |
| 8 | 54321→9999 | "Unknown" |

**Explanation:**
- Packet 1: Port 1883 matches MQTT_PORTS, first byte 0x10 = CONNECT
- Packet 2: Port 1883 matches, but 0x20 (CONNACK) isn't in the specific check, falls to "MQTT-like"
- Packet 3: Port 8883 matches, first byte 0x16 = TLS handshake
- Packet 4: Port 8883 matches, first byte 0x17 = TLS application data
- Packet 5: Port 8080 matches HTTP_PORTS, payload starts with "GET "
- Packet 6: Port 2121 matches FTP_PORTS, payload starts with "USER "
- Packet 7: Port 2121 matches, payload starts with "220 "
- Packet 8: Port 9999 matches nothing

2. **Edge case:** With empty payload, packet 3 would return "MQTT-like" because the payload length check `len(payload) >= 2` would fail.

3. **Code understanding:** Using `all_ports & MQTT_PORTS` (set intersection) checks both source AND destination ports. This is important because:
   - Request packets have dst=1883
   - Response packets have src=1883
   Both should be classified as MQTT traffic.
</details>

---

## Tracing Tips

1. **Track state changes:** Use a table to record variable values after each line
2. **Follow the flow:** Note which branches (if/else) are taken
3. **Watch for exceptions:** Identify where exceptions might be raised
4. **Verify assumptions:** Don't assume — trace each step
5. **Test your predictions:** Run the code and compare with your trace

---

*Computer Networks — Week 13: IoT and Security*
*ASE Bucharest, CSIE | by ing. dr. Antonio Clim*
