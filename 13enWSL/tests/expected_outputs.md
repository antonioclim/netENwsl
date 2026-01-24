# Expected Outputs - Week 13 Laboratory

> NETWORKING class - ASE, Informatics | by Revolvix

This document describes expected outputs for verification purposes.

---

## Exercise 1: Port Scanner

### Expected Open Ports
When scanning `127.0.0.1` with the laboratory running:

| Port | Service | State |
|------|---------|-------|
| 1883 | MQTT Plain | OPEN |
| 2121 | FTP | OPEN |
| 6200 | Backdoor Stub | OPEN |
| 8080 | HTTP (DVWA) | OPEN |
| 8883 | MQTT TLS | OPEN |

### Sample Console Output
```
============================================================
  Week 13 - TCP Port Scanner
  WARNING: For controlled laboratory environment only!
============================================================

[*] Scanning 127.0.0.1 - 7 ports
    Timeout: 0.5s | Workers: 100
    [OPEN]  1883/tcp  MQTT
    [OPEN]  2121/tcp  FTP-Alt         | 220 Week13-FTP
    [OPEN]  6200/tcp  unknown
    [OPEN]  8080/tcp  HTTP-Alt
    [OPEN]  8883/tcp  MQTT-TLS

[+] Results for 127.0.0.1:
    Open: 5 | Closed: 2 | Filtered: 0
    Duration: 0.52s

[✓] Results exported: artifacts/scan_results.json
```

### Sample JSON Output
```json
{
  "scan_report": {
    "generated_at": "2025-01-07T14:30:00.123456",
    "tool": "Week 13 Port Scanner",
    "hosts": [
      {
        "target": "127.0.0.1",
        "scan_time": "2025-01-07T14:30:00.123456",
        "statistics": {
          "total_scanned": 7,
          "open": 5,
          "closed": 2,
          "filtered": 0
        },
        "open_ports": [
          {"port": 1883, "service": "MQTT", "banner": null, "response_ms": 2.34},
          {"port": 2121, "service": "FTP-Alt", "banner": "220 Week13-FTP (vsftpd 2.3.4 simulation)", "response_ms": 5.67},
          {"port": 6200, "service": "unknown", "banner": null, "response_ms": 3.21},
          {"port": 8080, "service": "HTTP-Alt", "banner": "HTTP/1.1 302 Found", "response_ms": 12.45},
          {"port": 8883, "service": "MQTT-TLS", "banner": null, "response_ms": 4.56}
        ],
        "duration_seconds": 0.52
      }
    ]
  }
}
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `All ports filtered` | Docker not running | `sudo service docker start` |
| `Connection refused on all ports` | Containers not started | `python3 scripts/start_lab.py` |
| `Timeout on port 8883` | TLS handshake incomplete | Normal for banner grab; port is still open |

---

## Exercise 2: MQTT Client

### Plaintext Publish Output
```
========================================================================
Week 13 - MQTT Publish
========================================================================
Broker: 127.0.0.1:1883
TLS: False
Auth: none (anonymous)
Topic: iot/sensors/temperature
QoS: 0
Count: 3
Message:
{
  "sensor": "temp",
  "value": 24.3
}

[PUBLISH] sent 1/3 mid=1
[PUBLISH] ack mid=1
[PUBLISH] sent 2/3 mid=2
[PUBLISH] ack mid=2
[PUBLISH] sent 3/3 mid=3
[PUBLISH] ack mid=3
```

### Plaintext Subscribe Output
```
========================================================================
Week 13 - MQTT Subscribe
========================================================================
Broker: 127.0.0.1:1883
TLS: False
Auth: none (anonymous)
Topic filter: iot/sensors/#
QoS: 1
Timeout: 20s

[SUBSCRIBED] mid=1 granted_qos=(1,)
[INFO] Waiting for messages (20s timeout)...
[MESSAGE] topic=iot/sensors/temperature qos=0 retained=False
{
  "sensor": "temp",
  "value": 24.3
}
----------------------------------------
[MESSAGE] topic=iot/sensors/temperature qos=0 retained=False
{
  "sensor": "temp",
  "value": 24.3
}
----------------------------------------
[INFO] Received 2 message(s).
```

### TLS Publish Output
```
========================================================================
Week 13 - MQTT Publish
========================================================================
Broker: 127.0.0.1:8883
TLS: True
CA file: docker/configs/certs/ca.crt
TLS insecure: False
Auth: none (anonymous)
Topic: iot/sensors/temperature
QoS: 1
Count: 1
Message:
{
  "sensor": "temp_secure",
  "value": 25.0
}

[PUBLISH] sent 1/1 mid=1
[PUBLISH] ack mid=1
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Connection refused` | Broker not running | Start lab containers |
| `SSL: CERTIFICATE_VERIFY_FAILED` | Wrong CA file | Use `docker/configs/certs/ca.crt` |
| `TLS is enabled but --cafile was not provided` | Missing argument | Add `--cafile` flag |
| `Connection timed out (no CONNACK)` | Firewall blocking | Check Docker network |

---

## Exercise 3: Packet Sniffer

### Expected Capture Output
```
========================================================================
Week 13 - Packet Sniffer (educational)
========================================================================
Interface: any
Timeout: 30s
Count: 0 (unlimited)
BPF filter: tcp port 1883 or tcp port 8883

[INFO] Starting capture... (Ctrl+C to stop)

[14:35:01.123] TCP 127.0.0.1:54321 → 127.0.0.1:1883 len=66
  Protocol: MQTT | Flags: PSH,ACK
  
[14:35:01.125] TCP 127.0.0.1:1883 → 127.0.0.1:54321 len=54
  Protocol: MQTT | Flags: PSH,ACK
  Payload preview: \x20\x02\x00\x00 (CONNACK)

[14:35:01.234] TCP 127.0.0.1:54321 → 127.0.0.1:1883 len=78
  Protocol: MQTT | Flags: PSH,ACK
  Payload preview: \x30\x1c\x00\x16iot/sensors/temperature

[14:35:05.456] TCP 127.0.0.1:54322 → 127.0.0.1:8883 len=517
  Protocol: TLS | Flags: PSH,ACK
  TLS Record: Handshake (ClientHello)

[14:35:05.478] TCP 127.0.0.1:8883 → 127.0.0.1:54322 len=1452
  Protocol: TLS | Flags: PSH,ACK
  TLS Record: Handshake (ServerHello, Certificate)

[INFO] Capture complete: 5 packets captured
[INFO] Saved to: pcap/mqtt_capture.pcap
```

### Wireshark Filter Examples

| Filter | Purpose | Expected Packets |
|--------|---------|------------------|
| `tcp.port == 1883` | MQTT plaintext | CONNECT, CONNACK, PUBLISH, PUBACK |
| `tcp.port == 8883` | MQTT over TLS | TLS handshake + Application Data |
| `mqtt` | MQTT protocol decode | Only works on port 1883 |
| `tls.handshake` | TLS negotiation | ClientHello, ServerHello, etc. |

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `No packets captured` | Wrong interface | Use `vEthernet (WSL)` in Wireshark |
| `Permission denied` | Need root | Run with `sudo` or as Administrator |
| `Interface 'any' not found` | Windows limitation | Specify exact interface |

---

## Exercise 4: Vulnerability Checker

### HTTP (DVWA) Output
```
========================================================================
Week 13 - Vulnerability Checker (defensive assessment)
========================================================================
Target:    127.0.0.1
Service:   http
Port:      8080

[*] Connecting to target...
[+] Connection successful

[*] Gathering service information...
Reachable: True
Banner/status: HTTP/1.1 302 Found

HTTP Headers:
  Server: Apache/2.4.38 (Debian)
  X-Powered-By: PHP/7.3.14
  Location: login.php
  Content-Type: text/html; charset=UTF-8

[*] Analysing findings...

Findings:
  [INFO] HTTP Server header observed
         Evidence: Server: Apache/2.4.38 (Debian)
         Risk: Information disclosure (version revealed)

  [INFO] PHP version disclosed
         Evidence: X-Powered-By: PHP/7.3.14
         Risk: Information disclosure

  [HIGH] DVWA detected (intentionally vulnerable application)
         Evidence: Redirect to login.php, known DVWA pattern
         Note: This is a lab target - expected behaviour

Summary:
  Total findings: 3
  High: 1 | Medium: 0 | Low: 0 | Info: 2

[✓] Report saved: artifacts/vuln_dvwa.json
```

### FTP Output
```
========================================================================
Week 13 - Vulnerability Checker (defensive assessment)
========================================================================
Target:    127.0.0.1
Service:   ftp
Port:      2121

[*] Connecting to target...
[+] Connection successful

[*] Gathering service information...
Reachable: True
Banner/status: 220 Week13-FTP (vsftpd 2.3.4 simulation)

[*] Analysing findings...

Findings:
  [INFO] FTP banner observed
         Evidence: 220 Week13-FTP (vsftpd 2.3.4 simulation)

  [HIGH] vsftpd 2.3.4 version detected
         Evidence: Banner contains "vsftpd 2.3.4"
         CVE: CVE-2011-2523 (backdoor in some distributions)
         Note: This is a simulation for educational purposes

  [MEDIUM] Anonymous FTP may be enabled
           Evidence: Standard FTP port, no auth required for banner
           Recommendation: Verify anonymous access policy

Summary:
  Total findings: 3
  High: 1 | Medium: 1 | Low: 0 | Info: 1

[✓] Report saved: artifacts/vuln_ftp.json
```

### MQTT Output
```
========================================================================
Week 13 - Vulnerability Checker (defensive assessment)
========================================================================
Target:    127.0.0.1
Service:   mqtt
Port:      1883

[*] Connecting to target...
[+] Connection successful (TCP)

[*] Gathering service information...
Reachable: True
MQTT Connection: Accepted (rc=0)

[*] Analysing findings...

Findings:
  [MEDIUM] Anonymous MQTT access permitted
           Evidence: Connection accepted without credentials
           Risk: Unauthorised publish/subscribe possible
           Recommendation: Enable authentication

  [LOW] Plaintext MQTT transport
        Evidence: Port 1883 (non-TLS)
        Risk: Traffic interception possible
        Recommendation: Use port 8883 with TLS in production

Summary:
  Total findings: 2
  High: 0 | Medium: 1 | Low: 1 | Info: 0

[✓] Report saved: artifacts/vuln_mqtt.json
```

### Sample JSON Report
```json
{
  "vulnerability_report": {
    "generated_at": "2025-01-07T14:45:00.000000",
    "target": "127.0.0.1",
    "service": "ftp",
    "port": 2121,
    "findings": [
      {
        "severity": "high",
        "title": "vsftpd 2.3.4 version detected",
        "evidence": "Banner contains 'vsftpd 2.3.4'",
        "cve": "CVE-2011-2523",
        "description": "This version had a backdoor in some distributions",
        "remediation": "Update to latest vsftpd version"
      },
      {
        "severity": "medium",
        "title": "Anonymous FTP may be enabled",
        "evidence": "Standard FTP port, no auth required for banner",
        "remediation": "Disable anonymous access or restrict to read-only"
      }
    ],
    "summary": {
      "high": 1,
      "medium": 1,
      "low": 0,
      "info": 1
    }
  }
}
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Connection refused` | Service not running | Start lab containers |
| `Timeout` | Firewall or slow service | Increase timeout with `--timeout` |
| `JSON decode error` | Corrupted response | Check service health |

---

## Smoke Test Output

```
============================================================
Week 13 Smoke Test
NETWORKING class - ASE, Informatics
============================================================

[TEST] Python version...
  [PASS] Python 3.11.6

[TEST] Required packages...
  [PASS] paho-mqtt installed
  [PASS] scapy installed (optional)

[TEST] Docker availability...
  [PASS] Docker daemon running
  [PASS] Docker Compose available

[TEST] Project structure...
  [PASS] docker/docker-compose.yml exists
  [PASS] src/exercises/ contains 4 exercises
  [PASS] docs/ contains required files

[TEST] Service connectivity...
  [PASS] MQTT broker on port 1883
  [PASS] MQTT TLS on port 8883
  [PASS] DVWA on port 8080
  [PASS] FTP on port 2121
  [PASS] Backdoor stub on port 6200

[TEST] Portainer status...
  [PASS] Portainer running on port 9000

[TEST] Exercise syntax...
  [PASS] ex_13_01_port_scanner.py
  [PASS] ex_13_02_mqtt_client.py
  [PASS] ex_13_03_packet_sniffer.py
  [PASS] ex_13_04_vuln_checker.py

============================================================
Results: 15 passed, 0 failed, 0 skipped
Smoke test PASSED ✓
============================================================
```

---

## Quick Diagnostic Commands

Use these commands to verify the environment:

```bash
# Check Docker is running
docker info > /dev/null 2>&1 && echo "Docker OK" || echo "Docker FAIL"

# Check containers
docker ps --filter "name=week13" --format "{{.Names}}: {{.Status}}"

# Check ports
for port in 1883 2121 6200 8080 8883; do
    nc -zv 127.0.0.1 $port 2>&1 | grep -q succeeded && echo "Port $port: OPEN" || echo "Port $port: CLOSED"
done

# Check Portainer
curl -s -o /dev/null -w "%{http_code}" http://localhost:9000 | grep -q 200 && echo "Portainer OK" || echo "Portainer FAIL"
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
