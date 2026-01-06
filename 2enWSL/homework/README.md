# Homework Assignments — Week 2

> NETWORKING class - ASE, Informatics | by Revolvix

## Overview

These homework assignments extend the concepts covered in the laboratory session. Complete them before the next class to reinforce your understanding of socket programming and the TCP/IP architectural model.

**Deadline:** Before Week 3 laboratory session

---

## Assignment 1: Multi-Protocol Calculator Server

**File:** `exercises/hw_2_01.py`

### Objective

Implement a calculator server that supports both TCP and UDP clients simultaneously, demonstrating your understanding of both transport protocols and concurrent server design.

### Requirements

1. The server must listen on two ports:
   - TCP on port 9100
   - UDP on port 9101

2. Support the following operations via text protocol:
   ```
   add:5:3      → 8
   sub:10:4     → 6
   mul:6:7      → 42
   div:15:3     → 5.0
   pow:2:8      → 256
   ```

3. Error handling:
   - Invalid operation → `ERROR: Unknown operation`
   - Division by zero → `ERROR: Division by zero`
   - Invalid format → `ERROR: Invalid format`

4. The server must handle multiple TCP clients concurrently using threading.

5. Log all requests with timestamp, client address, protocol (TCP/UDP), and result.

### Evaluation Criteria

| Criterion | Points |
|-----------|--------|
| TCP server implementation | 20 |
| UDP server implementation | 20 |
| Concurrent handling (TCP) | 15 |
| Protocol parsing | 15 |
| Error handling | 15 |
| Logging | 10 |
| Code quality and documentation | 5 |
| **Total** | **100** |

### Hints

- Use `threading.Thread` for TCP client handling
- Use `select` or separate threads for simultaneous TCP/UDP
- Consider using a dictionary for operation dispatch

---

## Assignment 2: Protocol Analyser

**File:** `exercises/hw_2_02.py`

### Objective

Create a tool that analyses captured network traffic and generates statistics about TCP and UDP conversations.

### Requirements

1. Read a PCAP file (you may use the `scapy` library or parse raw bytes)

2. For TCP connections, identify and report:
   - Number of complete three-way handshakes
   - Number of connections with data transfer
   - Total bytes transferred per connection
   - Connection duration (SYN to FIN)

3. For UDP, report:
   - Number of unique source-destination pairs
   - Total datagrams per pair
   - Average datagram size

4. Output format (example):
   ```
   === TCP Analysis ===
   Total connections: 5
   Complete handshakes: 4
   
   Connection 1: 192.168.1.100:54321 → 93.184.216.34:80
     Duration: 1.234s
     Bytes sent: 1024
     Bytes received: 45678
   
   === UDP Analysis ===
   Total unique flows: 3
   
   Flow 1: 192.168.1.100:53421 ↔ 8.8.8.8:53
     Datagrams: 2
     Avg size: 64 bytes
   ```

### Evaluation Criteria

| Criterion | Points |
|-----------|--------|
| PCAP parsing | 25 |
| TCP analysis accuracy | 25 |
| UDP analysis accuracy | 20 |
| Output formatting | 15 |
| Edge case handling | 10 |
| Code quality | 5 |
| **Total** | **100** |

### Hints

- Install scapy: `pip install scapy`
- Use `rdpcap()` to read PCAP files
- Track TCP state machine per connection
- Sample PCAP files available in `/pcap` directory

---

## Submission Guidelines

1. **File naming:** Keep the original filenames (`hw_2_01.py`, `hw_2_02.py`)

2. **Code requirements:**
   - Python 3.11+ compatible
   - Type hints required for function signatures
   - Docstrings for all functions and classes
   - PEP 8 compliant

3. **Testing:**
   - Include at least 3 test cases per assignment
   - Document expected inputs and outputs

4. **Documentation:**
   - Brief explanation of your approach (in docstring or comments)
   - Instructions for running your code

---

## Testing Your Solutions

### Assignment 1

```bash
# Terminal 1: Start your server
python homework/exercises/hw_2_01.py server

# Terminal 2: Test TCP
python -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 9100))
s.send(b'add:5:3')
print(s.recv(1024))
s.close()
"

# Terminal 3: Test UDP
python -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(b'mul:6:7', ('localhost', 9101))
print(s.recv(1024))
"
```

### Assignment 2

```bash
# Generate test traffic first
python src/exercises/ex_2_01_tcp.py server &
python src/exercises/ex_2_01_tcp.py client
python scripts/capture_traffic.py --interface eth0 --output pcap/test.pcap --duration 10

# Then analyse
python homework/exercises/hw_2_02.py pcap/test.pcap
```

---

## Resources

- Python socket documentation: https://docs.python.org/3/library/socket.html
- Scapy documentation: https://scapy.readthedocs.io/
- Week 2 laboratory exercises for reference

---

*NETWORKING class - ASE, Informatics | by Revolvix*
