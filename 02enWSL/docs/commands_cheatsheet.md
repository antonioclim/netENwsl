# 📋 Commands Cheatsheet — Week 2: Socket Programming

> NETWORKING class — ASE, CSIE Bucharest  
> Computer Networks Laboratory | by ing. dr. Antonio Clim

Quick reference for commands used in Week 2 exercises.

---

## Lab Environment

### Docker

| Command | Purpose | Example Output |
|---------|---------|----------------|
| `sudo service docker start` | Start Docker daemon | `* Starting Docker: docker` |
| `docker ps` | List running containers | Shows container table |
| `docker ps -a` | List all containers | Includes stopped |
| `docker compose up -d` | Start compose services | `Creating week2_lab...` |
| `docker compose down` | Stop and remove services | `Removing week2_lab...` |
| `docker logs <name>` | View container logs | Log output |
| `docker exec -it <name> bash` | Shell into container | Container prompt |

### WSL Navigation

| Command | Purpose | Example |
|---------|---------|---------|
| `cd /mnt/d/NETWORKING` | Access Windows D: drive | — |
| `explorer.exe .` | Open current dir in Windows | Opens Explorer |
| `code .` | Open in VS Code | Opens VS Code |
| `wsl --shutdown` | Restart WSL (from PowerShell) | — |

---

## Socket Programming

### Exercise Commands

| Command | Purpose |
|---------|---------|
| `python3 src/exercises/ex_2_01_tcp.py server --port 9090` | Start TCP server |
| `python3 src/exercises/ex_2_01_tcp.py client --host 127.0.0.1 --port 9090 -m "Hello"` | TCP client |
| `python3 src/exercises/ex_2_01_tcp.py load --clients 10` | TCP load test |
| `python3 src/exercises/ex_2_02_udp.py server --port 9091` | Start UDP server |
| `python3 src/exercises/ex_2_02_udp.py client --host 127.0.0.1 --port 9091 -i` | Interactive UDP client |

### Server Mode Options

| Option | Meaning |
|--------|---------|
| `--mode threaded` | Handle clients concurrently (default) |
| `--mode iterative` | Handle clients sequentially |
| `--bind 0.0.0.0` | Accept from all interfaces |
| `--bind 127.0.0.1` | Accept from localhost only |
| `--interactive` | Enable prediction prompts |

---

## Network Debugging

### Port and Connection Status

| Command | Purpose | Example Output |
|---------|---------|----------------|
| `ss -tlnp` | List TCP listening sockets | `LISTEN 0 128 0.0.0.0:9090` |
| `ss -ulnp` | List UDP listening sockets | `UNCONN 0 0 0.0.0.0:9091` |
| `ss -tnp` | List established TCP connections | `ESTAB ... 127.0.0.1:9090` |
| `ss -tn state time-wait` | List TIME_WAIT sockets | Sockets in TIME_WAIT |
| `lsof -i :9090` | What's using port 9090? | Process info |
| `netstat -tlnp` | Alternative to ss | Similar output |

### Process Management

| Command | Purpose |
|---------|---------|
| `ps aux \| grep python` | Find Python processes |
| `kill <pid>` | Terminate process gracefully |
| `kill -9 <pid>` | Force terminate process |
| `pkill -f "ex_2_01"` | Kill by command name |
| `jobs` | List background jobs |
| `fg` | Bring job to foreground |
| `Ctrl+C` | Interrupt running process |
| `Ctrl+Z` | Suspend process (use `bg` to resume) |

### Network Testing

| Command | Purpose | Example |
|---------|---------|---------|
| `ping 127.0.0.1` | Test loopback | Shows RTT |
| `ping 10.0.2.10` | Test container IP | Shows RTT |
| `nc -zv 127.0.0.1 9090` | Test TCP port | `Connection succeeded` |
| `nc -u 127.0.0.1 9091` | UDP client (netcat) | Interactive |
| `curl http://localhost:8080` | HTTP request | Response body |
| `telnet 127.0.0.1 9090` | Interactive TCP client | Manual protocol testing |

---

## Wireshark Filters

### Display Filters

| Filter | Purpose |
|--------|---------|
| `tcp.port == 9090` | TCP traffic on port 9090 |
| `udp.port == 9091` | UDP traffic on port 9091 |
| `tcp.port == 9090 or udp.port == 9091` | Either protocol |
| `ip.addr == 10.0.2.10` | Traffic to/from container |
| `ip.src == 127.0.0.1` | Traffic from localhost |
| `ip.dst == 10.0.2.10` | Traffic to container |

### TCP-Specific Filters

| Filter | Purpose |
|--------|---------|
| `tcp.flags.syn == 1` | SYN packets (connection start) |
| `tcp.flags.fin == 1` | FIN packets (connection end) |
| `tcp.flags.rst == 1` | RST packets (connection reset) |
| `tcp.flags.syn == 1 and tcp.flags.ack == 0` | Initial SYN only |
| `tcp.analysis.retransmission` | Retransmitted packets |
| `tcp.stream eq 0` | First TCP conversation |

### Following Streams

1. Find any packet in the conversation
2. Right-click → **Follow → TCP Stream** (or UDP Stream)
3. View complete conversation

---

## Makefile Targets

| Target | Command | Purpose |
|--------|---------|---------|
| `make help` | — | Show all targets |
| `make install` | `pip install -r requirements.txt` | Install dependencies |
| `make verify` | `python setup/verify_environment.py` | Check setup |
| `make lint` | `ruff check ...` | Code quality |
| `make test` | `pytest tests/` | Run tests |
| `make smoke` | `python tests/smoke_test.py` | Quick sanity check |
| `make quiz` | `python formative/run_quiz.py` | Interactive quiz |
| `make quiz-quick` | `... --limit 5 --random` | 5 random questions |
| `make quiz-export` | `... export_quiz_to_lms.py` | LMS export |
| `make docker-up` | `docker compose up -d` | Start containers |
| `make docker-down` | `docker compose down` | Stop containers |
| `make clean` | Remove `__pycache__`, etc. | Cleanup |
| `make ci` | lint + test | CI pipeline |

---

## Python Socket Quick Reference

### TCP Server Pattern

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("0.0.0.0", 9090))
sock.listen(5)

while True:
    conn, addr = sock.accept()
    data = conn.recv(1024)
    conn.send(b"Response")
    conn.close()
```

### TCP Client Pattern

```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(("127.0.0.1", 9090))
    sock.send(b"Request")
    response = sock.recv(1024)
```

### UDP Server Pattern

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 9091))

while True:
    data, addr = sock.recvfrom(1024)
    sock.sendto(b"Response", addr)
```

### UDP Client Pattern

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b"Request", ("127.0.0.1", 9091))
response, server = sock.recvfrom(1024)
```

---

## Common Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| `Address already in use` | Port occupied | `lsof -i :PORT` then `kill` |
| `Connection refused` | Server not running | Start server first |
| `Connection timed out` | Server unreachable | Check IP and firewall |
| `Name or service not known` | DNS failure | Use IP address instead |
| `Permission denied` | Port < 1024 without root | Use port > 1024 |
| `Network is unreachable` | No route to host | Check network config |

---

## Debugging Workflow

### Step 1: Check Server Status

```bash
# Is server process running?
ps aux | grep python

# Is server listening?
ss -tlnp | grep 9090
```

### Step 2: Check Port Availability

```bash
# What's using the port?
lsof -i :9090

# Kill if needed
kill <pid>
```

### Step 3: Test Connectivity

```bash
# Can we reach the port?
nc -zv 127.0.0.1 9090

# Or use telnet
telnet 127.0.0.1 9090
```

### Step 4: Check Wireshark

1. Select correct interface (vEthernet WSL)
2. Apply filter: `tcp.port == 9090`
3. Generate traffic
4. Look for: SYN → SYN-ACK → ACK (success) or RST (failure)

### Step 5: Check Logs

```bash
# Server output
# Check terminal where server is running

# Docker logs
docker logs week2_lab
```

---

## Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `PYTHONUNBUFFERED=1` | Immediate print output | `export PYTHONUNBUFFERED=1` |
| `DOCKER_HOST` | Docker daemon location | Usually unset for local |

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Interrupt/stop process |
| `Ctrl+D` | End input (EOF) |
| `Ctrl+Z` | Suspend process |
| `Ctrl+L` | Clear terminal |
| `Tab` | Autocomplete |
| `↑` | Previous command |
| `Ctrl+R` | Search command history |

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
