# Commands Cheatsheet — Week 12

> NETWORKING class - ASE, Informatics | by Revolvix

Quick reference for SMTP and RPC laboratory commands.

---

## Docker Management

### Container Lifecycle

```powershell
# Start laboratory environment
python scripts/start_lab.py

# Check service status
python scripts/start_lab.py --status

# Rebuild containers from scratch
python scripts/start_lab.py --rebuild

# Stop all containers (preserves data)
python scripts/stop_lab.py

# Full cleanup (removes volumes)
python scripts/cleanup.py --full
```

### Container Inspection

```bash
# List running containers
docker ps

# View container logs
docker logs week12_lab
docker logs week12_lab --follow

# Execute shell inside container
docker exec -it week12_lab /bin/bash

# Check network configuration
docker network ls
docker network inspect week12_net

# View resource usage
docker stats
```

### Docker Compose Commands

```bash
# Navigate to docker directory
cd docker/

# Build images
docker compose build

# Start in detached mode
docker compose up -d

# View service logs
docker compose logs -f

# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v
```

---

## SMTP Commands

### Manual SMTP Session with Netcat

```bash
# Connect to SMTP server
nc localhost 1025

# Or using telnet
telnet localhost 1025
```

### SMTP Dialogue Sequence

```
HELO client.example.com
MAIL FROM:<sender@example.com>
RCPT TO:<recipient@example.com>
DATA
Subject: Test Message

This is the message body.
.
LIST
QUIT
```

### SMTP Response Codes

| Code | Meaning |
|------|---------|
| 220 | Service ready |
| 250 | OK, command completed |
| 354 | Start mail input |
| 421 | Service not available |
| 450 | Mailbox unavailable |
| 500 | Syntax error |
| 501 | Syntax error in parameters |
| 503 | Bad sequence of commands |

### Python SMTP Client

```python
import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg['From'] = 'sender@example.com'
msg['To'] = 'recipient@example.com'
msg['Subject'] = 'Test'
msg.set_content('Hello, World!')

with smtplib.SMTP('localhost', 1025) as server:
    server.send_message(msg)
```

---

## JSON-RPC 2.0 Commands

### Using curl

```bash
# Single method call
curl -X POST http://localhost:6200 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"add","params":[5,3],"id":1}'

# Method with named parameters
curl -X POST http://localhost:6200 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"echo","params":{"message":"Hello"},"id":2}'

# Batch request
curl -X POST http://localhost:6200 \
  -H "Content-Type: application/json" \
  -d '[
    {"jsonrpc":"2.0","method":"add","params":[1,2],"id":1},
    {"jsonrpc":"2.0","method":"multiply","params":[3,4],"id":2},
    {"jsonrpc":"2.0","method":"get_time","id":3}
  ]'

# Notification (no id = no response)
curl -X POST http://localhost:6200 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"echo","params":{"message":"Silent"}}'
```

### Available JSON-RPC Methods

| Method | Parameters | Description |
|--------|------------|-------------|
| `add` | `[a, b]` | Returns a + b |
| `subtract` | `[a, b]` | Returns a - b |
| `multiply` | `[a, b]` | Returns a × b |
| `divide` | `[a, b]` | Returns a ÷ b |
| `echo` | `{message: str}` | Returns the message |
| `sort_list` | `{items: list}` | Returns sorted list |
| `get_time` | None | Returns server time |
| `get_server_info` | None | Returns server details |
| `get_stats` | None | Returns call statistics |

### Python JSON-RPC Client

```python
import requests
import json

def jsonrpc_call(method, params=None, id=1):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": id
    }
    if params:
        payload["params"] = params
    
    response = requests.post(
        "http://localhost:6200",
        json=payload
    )
    return response.json()

# Usage
result = jsonrpc_call("add", [10, 5])
print(result["result"])  # 15
```

---

## XML-RPC Commands

### Using curl

```bash
# Add method call
curl -X POST http://localhost:6201 \
  -H "Content-Type: text/xml" \
  -d '<?xml version="1.0"?>
<methodCall>
  <methodName>add</methodName>
  <params>
    <param><value><int>5</int></value></param>
    <param><value><int>3</int></value></param>
  </params>
</methodCall>'

# List available methods (introspection)
curl -X POST http://localhost:6201 \
  -H "Content-Type: text/xml" \
  -d '<?xml version="1.0"?>
<methodCall>
  <methodName>system.listMethods</methodName>
</methodCall>'

# Get method signature
curl -X POST http://localhost:6201 \
  -H "Content-Type: text/xml" \
  -d '<?xml version="1.0"?>
<methodCall>
  <methodName>system.methodSignature</methodName>
  <params>
    <param><value><string>add</string></value></param>
  </params>
</methodCall>'
```

### Python XML-RPC Client

```python
import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:6201")

# Call methods
result = proxy.add(5, 3)
print(f"5 + 3 = {result}")

# Introspection
methods = proxy.system.listMethods()
print(f"Available methods: {methods}")

help_text = proxy.system.methodHelp("add")
print(f"Help for add: {help_text}")
```

---

## gRPC Commands

### Using grpcurl (if installed)

```bash
# List services
grpcurl -plaintext localhost:6251 list

# Describe service
grpcurl -plaintext localhost:6251 describe Calculator

# Call Add method
grpcurl -plaintext -d '{"a": 5, "b": 3}' \
  localhost:6251 Calculator/Add

# Call Echo method
grpcurl -plaintext -d '{"message": "Hello"}' \
  localhost:6251 Calculator/Echo

# Call Sha256Hash
grpcurl -plaintext -d '{"data": "test"}' \
  localhost:6251 Calculator/Sha256Hash
```

### Python gRPC Client

```python
import grpc
import calculator_pb2
import calculator_pb2_grpc

# Create channel and stub
channel = grpc.insecure_channel('localhost:6251')
stub = calculator_pb2_grpc.CalculatorStub(channel)

# Call Add
request = calculator_pb2.AddRequest(a=5, b=3)
response = stub.Add(request)
print(f"5 + 3 = {response.result}")

# Call Echo
request = calculator_pb2.EchoRequest(message="Hello")
response = stub.Echo(request)
print(f"Echo: {response.message}")

# Call GetStats
response = stub.GetStats(calculator_pb2.Empty())
print(f"Total calls: {response.total_calls}")
```

### Protocol Buffer Compilation

```bash
# Generate Python stubs from .proto
python -m grpc_tools.protoc \
  -I. \
  --python_out=. \
  --grpc_python_out=. \
  calculator.proto
```

---

## Packet Capture Commands

### Using tcpdump

```bash
# Capture SMTP traffic
tcpdump -i any port 1025 -w smtp_capture.pcap

# Capture JSON-RPC traffic
tcpdump -i any port 6200 -w jsonrpc_capture.pcap

# Capture all RPC traffic
tcpdump -i any 'port 6200 or port 6201 or port 6251' -w rpc_capture.pcap

# Capture with packet content display
tcpdump -i any port 1025 -A

# Capture specific number of packets
tcpdump -i any port 1025 -c 20 -w smtp_20packets.pcap
```

### Using tshark

```bash
# Capture with display filter
tshark -i any -f "port 1025" -a duration:60 -w smtp.pcap

# Read and analyse capture
tshark -r smtp.pcap -Y "smtp"

# Extract HTTP (JSON-RPC/XML-RPC) payloads
tshark -r rpc.pcap -Y "http" -T fields -e http.request.method -e http.file_data

# Follow TCP stream
tshark -r smtp.pcap -z follow,tcp,ascii,0
```

### Using capture_traffic.py Script

```powershell
# Start capture with automatic filter
python scripts/capture_traffic.py --interface eth0 --duration 60

# Capture specific protocol
python scripts/capture_traffic.py --filter "port 1025" --output pcap/smtp.pcap

# Analyse existing capture
python scripts/capture_traffic.py --analyse pcap/smtp.pcap
```

---

## Wireshark Filters

### SMTP Filters

```
# SMTP protocol
smtp

# SMTP on custom port
tcp.port == 1025

# SMTP commands
tcp.port == 1025 && tcp.flags.push == 1

# Specific SMTP response
tcp.port == 1025 && frame contains "250"
```

### HTTP Filters (JSON-RPC/XML-RPC)

```
# HTTP protocol
http

# JSON-RPC port
tcp.port == 6200

# XML-RPC port
tcp.port == 6201

# HTTP POST requests
http.request.method == "POST"

# JSON content type
http.content_type contains "json"

# XML content type
http.content_type contains "xml"
```

### gRPC Filters

```
# gRPC port
tcp.port == 6251

# HTTP/2 frames
http2

# gRPC protocol
grpc
```

### Combined Filters

```
# All laboratory traffic
tcp.port == 1025 || tcp.port == 6200 || tcp.port == 6201 || tcp.port == 6251

# Exclude ACK-only packets
tcp.port == 1025 && tcp.len > 0
```

---

## Benchmarking Commands

### Using benchmark_rpc.py

```bash
# Run full benchmark
python src/apps/rpc/benchmark_rpc.py

# From inside container
docker exec -it week12_lab python /app/src/rpc/benchmark_rpc.py
```

### Using run_demo.py

```powershell
# Run benchmark demonstration
python scripts/run_demo.py --demo benchmark

# Run all demonstrations
python scripts/run_demo.py --demo all
```

### Manual Performance Testing

```bash
# Simple loop benchmark with curl
time for i in {1..100}; do
  curl -s -X POST http://localhost:6200 \
    -H "Content-Type: application/json" \
    -d '{"jsonrpc":"2.0","method":"add","params":[1,2],"id":'$i'}' > /dev/null
done

# Using ab (Apache Bench)
echo '{"jsonrpc":"2.0","method":"add","params":[1,2],"id":1}' > /tmp/payload.json
ab -n 1000 -c 10 -p /tmp/payload.json -T application/json http://localhost:6200/
```

---

## Testing Commands

### pytest Commands

```powershell
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_exercises.py

# Run specific test
pytest tests/test_exercises.py::test_smtp_transaction

# Run smoke tests only
pytest tests/smoke_test.py

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### Verification Commands

```powershell
# Verify environment
python setup/verify_environment.py

# Quick smoke test
python tests/smoke_test.py

# Test specific service
python -c "from scripts.utils.network_utils import check_port; print(check_port('localhost', 1025))"
```

---

## Utility Commands

### Port Checking

```bash
# Check if port is in use (Windows PowerShell)
netstat -an | findstr :1025

# Check if port is in use (WSL/Linux)
ss -tuln | grep 1025
netstat -tuln | grep 1025

# Using Python
python -c "import socket; s=socket.socket(); print('Open' if s.connect_ex(('localhost',1025))==0 else 'Closed'); s.close()"
```

### Process Management

```bash
# Find process using port (Windows)
netstat -ano | findstr :1025
tasklist /FI "PID eq <PID>"

# Find process using port (Linux)
lsof -i :1025
fuser 1025/tcp
```

### Network Diagnostics

```bash
# Test connectivity
ping localhost

# DNS lookup
nslookup localhost

# Trace route
traceroute localhost

# Netcat port test
nc -zv localhost 1025
nc -zv localhost 6200
nc -zv localhost 6201
nc -zv localhost 6251
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
