# Parsons Problems — Week 1

> Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Parsons problems are code arrangement exercises with **distractors** (incorrect blocks).

## P1: Ping Latency Measurement (LO1)

**Task:** Arrange blocks to ping a host 4 times and extract average RTT.

### Correct Blocks
```python
# A
import subprocess
# B
result = subprocess.run(["ping", "-c", "4", "8.8.8.8"], capture_output=True, text=True)
# C
output = result.stdout
# D
for line in output.split("\n"):
    if "avg" in line:
        print(f"Average RTT: {line}")
```

### Distractors
```python
# E (wrong flag - Windows syntax)
result = subprocess.run(["ping", "-n", "4", "8.8.8.8"], capture_output=True, text=True)
# F (missing capture)
result = subprocess.run(["ping", "-c", "4", "8.8.8.8"])
```

**Order:** A → B → C → D | Exclude: E, F

---

## P2: TCP Server Setup (LO2)

**Task:** Create a TCP server listening on port 9090.

### Correct Blocks
```python
# A
import socket
# B
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# C
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# D
server_socket.bind(("0.0.0.0", 9090))
# E
server_socket.listen(1)
# F
client_socket, address = server_socket.accept()
```

### Distractors
```python
# G (UDP socket)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# H (connect instead of bind)
server_socket.connect(("0.0.0.0", 9090))
```

**Order:** A → B → C → D → E → F | Exclude: G, H

---

## P3: CSV Data Parsing (LO3)

**Task:** Parse CSV file and extract unique IPs.

### Correct Blocks
```python
# A
import csv
# B
ip_addresses = []
# C
with open("connections.csv", "r") as file:
# D
    reader = csv.DictReader(file)
# E
    for row in reader:
# F
        ip = row["source_ip"]
        if ip not in ip_addresses:
            ip_addresses.append(ip)
```

### Distractors
```python
# G (wrong module)
import json
# H (string split - fails with quoted commas)
    for line in file:
        ip = line.split(",")[0]
```

**Order:** A → B → C → D → E → F | Exclude: G, H

---

## P4: TCP Client Connection (LO2)

**Task:** Connect to server, send message, receive response.

### Correct Blocks
```python
# A
import socket
# B
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# C
client_socket.connect(("127.0.0.1", 9090))
# D
client_socket.sendall("Hello".encode("utf-8"))
# E
response = client_socket.recv(4096)
# F
client_socket.close()
```

### Distractors
```python
# G (send before connect)
client_socket.sendall("Hello".encode("utf-8"))
client_socket.connect(("127.0.0.1", 9090))
# H (no encode)
client_socket.sendall("Hello")
```

**Order:** A → B → C → D → E → F | Exclude: G, H

---

## P5: Docker Lab Startup (LO6)

**Task:** Start lab environment correctly.

### Correct Blocks
```bash
# A
sudo service docker start
# B  
cd /mnt/d/NETWORKING/WEEK1/01enWSL
# C
docker compose -f docker/docker-compose.yml up -d
# D
docker ps
```

### Distractors
```bash
# E (wrong directory)
cd /mnt/c/Users/NETWORKING/
# F (missing -d flag)
docker compose -f docker/docker-compose.yml up
```

**Order:** A → B → C → D | Exclude: E, F

---

## Summary

| Problem | LO | Correct | Distractors | Difficulty |
|---------|----|---------:|:-----------:|------------|
| P1 | LO1 | 4 | 2 | Basic |
| P2 | LO2 | 6 | 2 | Intermediate |
| P3 | LO3 | 6 | 2 | Intermediate |
| P4 | LO2 | 6 | 2 | Intermediate |
| P5 | LO6 | 4 | 2 | Basic |

---
*NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim*
