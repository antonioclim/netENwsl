# Troubleshooting Guide — Week 12
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Common issues and solutions for the SMTP and RPC laboratory.

---

## Docker Issues

### Docker Service Not Running (WSL)

**Symptoms:**
- `docker: command not found`
- `Cannot connect to the Docker daemon`
- `Error response from daemon: dial unix /var/run/docker.sock: connect: no such file or directory`

**Solution:**
```bash
# Start Docker service in WSL
sudo service docker start

# Verify with:
docker info
```

💭 **PREDICTION:** What should you see in `docker ps` after starting Docker?

---

### Port Already in Use

**Symptoms:**
- `Bind for 0.0.0.0:1025 failed: port is already allocated`
- `Error starting userland proxy: listen tcp4 0.0.0.0:6200: bind: address already in use`

**Diagnosis:**
```powershell
# Windows - find process using port
netstat -ano | findstr :1025

# WSL/Linux
sudo lsof -i :1025
sudo ss -tuln | grep 1025
```

**Solutions:**

1. **Stop conflicting service:**
   ```bash
   # If another Docker container
   docker stop <container_id>
   
   # If system service (Linux)
   sudo systemctl stop postfix  # For SMTP port 25/1025
   ```

2. **Use alternative ports:**
   Edit `docker/docker-compose.yml` and change port mappings:
   ```yaml
   ports:
     - "2025:1025"  # Changed from 1025
   ```

3. **Kill process directly (Windows):**
   ```powershell
   # Find PID from netstat output, then:
   taskkill /PID <pid> /F
   ```

---

### Container Won't Start

**Symptoms:**
- Container exits immediately after starting
- `Exited (1)` or similar status in `docker ps -a`

**Diagnosis:**
```bash
# View container logs
docker logs week12_lab

# View detailed container state
docker inspect week12_lab
```

**Common Causes:**

1. **Missing dependencies:**
   ```bash
   # Rebuild the image
   docker compose build --no-cache
   ```

2. **Volume permission issues:**
   ```bash
   # Fix permissions on volume directories
   sudo chown -R 1000:1000 docker/volumes/
   ```

3. **Syntax error in scripts:**
   Check the logs for Python traceback errors.

---

### Docker Network Issues

**Symptoms:**
- Containers cannot communicate
- `Network week12_net not found`

**Solution:**
```bash
# Remove and recreate network
docker network rm week12_net
docker network create week12_net

# Or restart compose
docker compose down
docker compose up -d
```

---

## SMTP Issues

### Cannot Connect to SMTP Server

**Symptoms:**
- `Connection refused` when using netcat or telnet
- Timeout when connecting to port 1025

**Diagnosis:**
```bash
# Check if port is listening
docker exec week12_lab netstat -tuln | grep 1025

# Check if server process is running
docker exec week12_lab ps aux | grep smtp
```

**Solutions:**

1. **Server not started:**
   ```bash
   # Start SMTP server manually inside container
   docker exec week12_lab python /app/src/email/smtp_server.py &
   ```

2. **Firewall blocking connection:**
   - Windows Firewall may block connections
   - Try accessing from inside the container first

3. **Wrong host/port:**
   - Check you're connecting to `localhost:1025` not `localhost:25`

---

### SMTP 503 Bad Sequence Error

**Symptoms:**
- Server responds `503 Bad sequence of commands`

**Cause:** SMTP commands sent out of order.

**Correct Sequence:**
```
HELO/EHLO  →  MAIL FROM  →  RCPT TO  →  DATA  →  message  →  .  →  QUIT
```

**Common Mistakes:**
- Sending `MAIL FROM` before `HELO`
- Sending `DATA` before `RCPT TO`
- Forgetting the single `.` on its own line to end the message

See `docs/misconceptions.md` for detailed explanation of SMTP state machine.

---

### SMTP Messages Not Saving

**Symptoms:**
- Transaction completes but no `.eml` files appear

**Diagnosis:**
```bash
# Check spool directory
docker exec week12_lab ls -la /var/spool/mail/

# Check volume mapping
docker inspect week12_lab | grep -A 10 "Mounts"
```

**Solution:**
Verify the volume is correctly mounted in `docker-compose.yml`:
```yaml
volumes:
  - ./volumes/spool:/var/spool/mail
```

---

## JSON-RPC Issues

### Parse Error (-32700)

**Symptoms:**
- Error response: `{"jsonrpc": "2.0", "error": {"code": -32700, "message": "Parse error"}, "id": null}`

**Cause:** Malformed JSON in request.

**Common Mistakes:**
```json
// Wrong - trailing comma
{"jsonrpc": "2.0", "method": "add", "params": [1, 2,], "id": 1}

// Wrong - single quotes
{'jsonrpc': '2.0', 'method': 'add', 'params': [1, 2], 'id': 1}

// Correct
{"jsonrpc": "2.0", "method": "add", "params": [1, 2], "id": 1}
```

---

### Invalid Request (-32600)

**Symptoms:**
- Error response with code -32600

**Cause:** Missing required fields or wrong types.

**Required Fields:**
- `jsonrpc`: Must be exactly `"2.0"` (string)
- `method`: Must be a string
- `id`: Required for requests expecting a response

---

### Method Not Found (-32601)

**Symptoms:**
- Error response with code -32601

💭 **PREDICTION:** What HTTP status code accompanies this error? (Hint: check `docs/misconceptions.md`)

**Diagnosis:**
```bash
# Check available methods
curl -X POST http://localhost:6200 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"get_server_info","id":1}'
```

**Solution:** Use one of the available methods: `add`, `subtract`, `multiply`, `divide`, `echo`, `sort_list`, `get_time`, `get_server_info`, `get_stats`

---

### Connection Refused to Port 6200

**Diagnosis:**
```bash
# Check if server is running
docker exec week12_lab ps aux | grep jsonrpc

# Check port binding
docker exec week12_lab netstat -tuln | grep 6200
```

**Solution:**
```bash
# Start server manually
docker exec week12_lab python /app/src/rpc/jsonrpc/jsonrpc_server.py &
```

---

## XML-RPC Issues

### Fault Response

**Symptoms:**
```xml
<fault>
  <value>
    <struct>
      <member><n>faultCode</n><value><int>1</int></value></member>
      <member><n>faultString</n><value><string>...</string></value></member>
    </struct>
  </value>
</fault>
```

**Common Causes:**
1. Method name typo
2. Wrong parameter types
3. Server-side exception

**Diagnosis:**
```python
import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:6201")

# List available methods
print(proxy.system.listMethods())

# Check method signature
print(proxy.system.methodSignature("add"))
```

---

### XML Parsing Errors

**Symptoms:**
- `xml.parsers.expat.ExpatError`
- Malformed XML response

**Cause:** Usually malformed request XML.

**Correct Format:**
```xml
<?xml version="1.0"?>
<methodCall>
  <methodName>add</methodName>
  <params>
    <param><value><int>5</int></value></param>
    <param><value><int>3</int></value></param>
  </params>
</methodCall>
```

---

## gRPC Issues

### Import Error: No module named 'grpc'

**Symptoms:**
```
ModuleNotFoundError: No module named 'grpc'
```

**Solution:**
```bash
pip install grpcio grpcio-tools --break-system-packages
```

---

### Import Error: No module named 'calculator_pb2'

**Symptoms:**
```
ModuleNotFoundError: No module named 'calculator_pb2'
```

**Cause:** Protocol Buffer stubs not generated.

**Solution:**
```bash
cd src/apps/rpc/grpc/

python -m grpc_tools.protoc \
  -I. \
  --python_out=. \
  --grpc_python_out=. \
  calculator.proto
```

---

### gRPC Connection Failed

**Symptoms:**
- `grpc._channel._InactiveRpcError`
- `failed to connect to all addresses`

**Diagnosis:**
```bash
# Check if server is running
docker exec week12_lab ps aux | grep grpc

# Check port
docker exec week12_lab netstat -tuln | grep 6251
```

**Solution:**
```bash
# Start gRPC server
docker exec week12_lab python /app/src/rpc/grpc/grpc_server.py &
```

---

### Protocol Buffer Version Mismatch

**Symptoms:**
```
TypeError: Descriptors cannot not be created directly
```

**Cause:** Version incompatibility between protobuf and generated code.

**Solution:**
```bash
# Upgrade protobuf
pip install --upgrade protobuf grpcio grpcio-tools --break-system-packages

# Regenerate stubs
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. calculator.proto
```

---

## Python Environment Issues

### Wrong Python Version

**Symptoms:**
- Syntax errors on valid Python 3.11+ code
- `f-string` or `match` statement errors

**Diagnosis:**
```bash
python --version
python3 --version
```

**Solution:**
- Download Python 3.11+ from python.org
- Verify Python 3.11+ is first in PATH

---

### Missing Dependencies

**Symptoms:**
- `ModuleNotFoundError` for various packages

**Solution:**
```bash
cd /mnt/d/NETWORKING/WEEK12/12enWSL
pip install -r setup/requirements.txt --break-system-packages
```

---

### Virtual Environment Issues

If using a virtual environment:

```bash
# Create new venv
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (WSL/Linux)
source venv/bin/activate

# Install dependencies
pip install -r setup/requirements.txt
```

---

## Wireshark Issues

### No Traffic Captured

**Symptoms:**
- Wireshark shows no packets despite active communication

**Solutions:**

1. **Select correct interface:**
   - For WSL Docker traffic: Use `vEthernet (WSL)`
   - For loopback: Use `Npcap Loopback Adapter`

2. **Check capture filter:**
   - Remove any capture filters initially
   - Add specific display filters after capture starts

3. **Use tcpdump inside container:**
   ```bash
   docker exec week12_lab tcpdump -i any port 1025 -w /tmp/capture.pcap
   docker cp week12_lab:/tmp/capture.pcap ./pcap/
   ```

---

### Cannot Capture on Loopback

**Windows Limitation:** Standard WinPcap cannot capture loopback traffic.

**Solutions:**
1. Install Npcap with loopback support during installation
2. Use tcpdump/tshark inside Docker container
3. Access services from a different machine on the network

---

## Test Failures

### Environment Tests Failing

```bash
# Run verification
python setup/verify_environment.py

# Check specific issues
python -c "import docker; print(docker.__version__)"
python -c "import grpc; print(grpc.__version__)"
```

---

### Exercise Tests Failing

**Symptoms:**
- Tests fail with connection errors

**Cause:** Services not running.

**Solution:**
```bash
# Check lab is running
python scripts/start_lab.py --status

# If not running
python scripts/start_lab.py
```

---

### Smoke Test Timeout

**Symptoms:**
- `TimeoutError` during smoke tests

**Cause:** Services slow to start or not responding.

**Solution:**
```bash
# Wait longer and retry
python scripts/start_lab.py
sleep 10
python tests/smoke_test.py
```

---

## Performance Issues

### Slow Container Startup

**Cause:** Docker image not cached or WSL2 resource limits.

**Solutions:**

1. **Pre-pull images:**
   ```bash
   docker pull python:3.12-slim
   docker pull portainer/portainer-ce:latest
   ```

2. **Increase WSL2 resources:**
   Create/edit `%USERPROFILE%\.wslconfig`:
   ```ini
   [wsl2]
   memory=8GB
   processors=4
   ```
   Then restart WSL: `wsl --shutdown`

---

### High Memory Usage

**Diagnosis:**
```bash
docker stats
```

**Solution:**
- Stop unused containers: `docker stop <container>`
- Prune unused resources: `docker system prune`

---

## Getting Further Help

If none of these solutions work:

1. **Check container logs:**
   ```bash
   docker logs week12_lab 2>&1 | tail -100
   ```

2. **Export diagnostic information:**
   ```bash
   docker info > docker_info.txt
   docker logs week12_lab > container_logs.txt 2>&1
   python setup/verify_environment.py > env_check.txt
   ```

3. **Consult course instructor** with the diagnostic files

---

## See Also

- `misconceptions.md` — Common conceptual errors
- `commands_cheatsheet.md` — Quick command reference
- `theory_summary.md` — Protocol specifications

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
