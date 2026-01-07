# Expected Outputs - Week 13 Laboratory

> NETWORKING class - ASE, Informatics | by Revolvix

This document describes expected outputs for verification purposes.

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

### Sample JSON Output
```json
{
  "scan_report": {
    "generated_at": "2025-01-01T12:00:00",
    "tool": "S13 Port Scanner",
    "hosts": [
      {
        "target": "127.0.0.1",
        "statistics": {
          "total_scanned": 100,
          "open": 5,
          "closed": 95,
          "filtered": 0
        },
        "open_ports": [
          {"port": 1883, "service": "MQTT"},
          {"port": 8080, "service": "HTTP-Alt"}
        ]
      }
    ]
  }
}
```

## Exercise 2: MQTT Client

### Plaintext Publish Output
```
========================================================================
Week 13 - MQTT publish
========================================================================
Broker: 127.0.0.1:1883
TLS: False
Auth: none
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

### TLS Publish Output
```
========================================================================
Week 13 - MQTT publish
========================================================================
Broker: 127.0.0.1:8883
TLS: True
CA file: docker/configs/certs/ca.crt
TLS insecure: False
Auth: none
Topic: iot/sensors/temperature
QoS: 0
Count: 3
...
```

## Exercise 3: Packet Sniffer

### Expected Capture Output
```
========================================================================
Week 13 - Packet sniffer (educational)
========================================================================
Interface: any
Timeout: 20s
Count: 0
BPF: tcp port 1883 or tcp port 8883

[12:00:01] TCP 127.0.0.1:54321 -> 127.0.0.1:1883 (MQTT) len=66
[12:00:01] TCP 127.0.0.1:1883 -> 127.0.0.1:54321 (MQTT) len=54 | text:...
```

## Exercise 4: Vulnerability Checker

### HTTP (DVWA) Output
```
========================================================================
Week 13 - Vulnerability checker (defensive)
========================================================================
Target:  127.0.0.1
Service: http
Port:    8080
Reachable: True
Banner/status: HTTP/1.1 200 OK

HTTP headers:
  Server: Apache/2.4.38 (Debian)
  Content-Type: text/html; charset=UTF-8

Findings:
  - [informational] HTTP Server header observed
    Evidence: Server: Apache/2.4.38 (Debian)
  - [informational] DVWA detected (intentionally vulnerable lab target)
    Evidence: Page contains 'Damn Vulnerable Web Application'
```

### FTP Output
```
========================================================================
Week 13 - Vulnerability checker (defensive)
========================================================================
Target:  127.0.0.1
Service: ftp
Port:    2121
Reachable: True
Banner/status: 220 Week13-FTP (vsftpd 2.3.4 simulation)

Findings:
  - [informational] FTP banner observed
    Evidence: 220 Week13-FTP (vsftpd 2.3.4 simulation)
  - [high] vsftpd 2.3.4 detected
    Evidence: This version is associated with CVE-2011-2523 in some distributions.
```

## Smoke Test Output

```
============================================================
Week 13 Smoke Test
NETWORKING class - ASE, Informatics
============================================================

[TEST] Python version...
  [PASS] Python 3.11+
[TEST] Docker availability...
  [PASS] Docker available
[TEST] Project structure...
  [PASS] Structure complete
[TEST] Service connectivity...
  [PASS] MQTT on port 1883
  [PASS] DVWA on port 8080
  [PASS] FTP on port 2121
[TEST] Port scanner syntax...
  [PASS] Port scanner syntax valid

============================================================
Results: 5 passed, 0 failed, 0 skipped
Smoke test PASSED
```
