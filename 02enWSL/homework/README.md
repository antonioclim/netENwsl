# Homework Assignments — Week 2

> NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim

## Overview

These homework assignments extend the concepts covered in the laboratory session. Complete them before the next class to reinforce your understanding of socket programming and the TCP/IP architectural model.

| Assignment | Topic | Estimated Time | Difficulty |
|------------|-------|----------------|------------|
| HW 2.01 | Multi-Protocol Calculator | 2-3 hours | ★★☆ Moderate |
| HW 2.02 | Protocol Analyser | 3-4 hours | ★★★ Challenging |

**Deadline:** Before Week 3 laboratory session

---

## Assignment 1: Multi-Protocol Calculator Server

**File:** `exercises/hw_2_01_implement_calculator_server.py`

**⏱️ Estimated time:** 2-3 hours

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

5. Log all requests with timestamp, client address, protocol (TCP/UDP) and result.

### Grading Rubric

| Criterion | Points | Details |
|-----------|--------|---------|
| TCP server implementation | 20 | Correct socket setup, bind, listen, accept |
| UDP server implementation | 20 | Correct datagram handling with recvfrom/sendto |
| Concurrent handling (TCP) | 15 | Threading works correctly, no race conditions |
| Protocol parsing | 15 | All operations parsed correctly |
| Error handling | 15 | All error cases handled gracefully |
| Logging | 10 | Timestamp, address, protocol, result logged |
| Code quality and documentation | 5 | Type hints, docstrings, clean code |
| **Total** | **100** | |

### Grade Boundaries

| Grade | Points | Criteria |
|-------|--------|----------|
| A (Excellent) | 90-100 | All requirements met, clean code, bonus features |
| B (Good) | 75-89 | All core requirements, minor issues |
| C (Satisfactory) | 60-74 | Basic functionality works |
| D (Passing) | 50-59 | Partial implementation |
| F (Fail) | <50 | Major functionality missing |

### Hints

- Use `threading.Thread` for TCP client handling
- Use `select` or separate threads for simultaneous TCP/UDP
- Consider using a dictionary for operation dispatch:
  ```python
  operations = {
      "add": lambda a, b: a + b,
      "sub": lambda a, b: a - b,
      # ...
  }
  ```

---

## Assignment 2: Protocol Analyser

**File:** `exercises/hw_2_02_analyse_pcap_traffic.py`

**⏱️ Estimated time:** 3-4 hours

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

### Grading Rubric

| Criterion | Points | Details |
|-----------|--------|---------|
| PCAP parsing | 25 | File read correctly, packets extracted |
| TCP analysis accuracy | 25 | Handshakes, data, durations correct |
| UDP analysis accuracy | 20 | Flows, counts, sizes correct |
| Output formatting | 15 | Clear, readable, matches spec |
| Edge case handling | 10 | Incomplete connections, empty files |
| Code quality | 5 | Type hints, docstrings, structure |
| **Total** | **100** | |

### Hints

- Install scapy: `pip install scapy`
- Use `rdpcap()` to read PCAP files
- Track TCP state machine per connection
- Sample PCAP files available in `/pcap` directory

---

## Submission with anti‑AI evidence

For assessed submissions, you must include machine‑checkable evidence that you ran the lab. You may use AI tools for explanations and debugging but the submitted artefacts must be produced by real execution.

### Required artefacts

When asked for anti‑AI evidence, include:
- `artifacts/anti_ai/challenge_<YOUR_ID>.yaml`
- `artifacts/anti_ai/proof_<YOUR_ID>/tcp_client.txt`
- `artifacts/anti_ai/proof_<YOUR_ID>/udp_client.txt`
- `artifacts/anti_ai/proof_<YOUR_ID>/tcp_server.txt`
- `artifacts/anti_ai/proof_<YOUR_ID>/udp_server.txt`
- `artifacts/anti_ai/proof_<YOUR_ID>/proof_summary.json`
- `artifacts/anti_ai/evidence_<YOUR_ID>.json`

### Commands

From inside `02enWSL/`:

```bash
make anti-ai STUDENT_ID=YOUR_ID
```

To validate locally:

```bash
make anti-ai-validate-practice STUDENT_ID=YOUR_ID
```

The instructor can require signed challenges by setting `ANTI_AI_MASTER_KEY` for generation and validation.

## Submission Checklist

Before submitting, verify:

### Code Quality
- [ ] Python 3.11+ compatible
- [ ] All functions have type hints
- [ ] All functions and classes have docstrings
- [ ] Code follows PEP 8 style guide
- [ ] No hardcoded paths (use relative paths)

### Functionality
- [ ] Assignment 1: TCP server accepts connections
- [ ] Assignment 1: UDP server responds to datagrams
- [ ] Assignment 1: All five operations work correctly
- [ ] Assignment 1: Error cases handled
- [ ] Assignment 2: PCAP file loads without errors
- [ ] Assignment 2: TCP statistics are accurate
- [ ] Assignment 2: UDP statistics are accurate

### Testing
- [ ] Included at least 3 test cases per assignment
- [ ] Documented expected inputs and outputs
- [ ] Tested with sample PCAP files in `/pcap` directory

### Documentation
- [ ] Brief explanation of approach in module docstring
- [ ] Instructions for running code
- [ ] Any dependencies listed

---

## Testing Your Solutions

### Assignment 1

```bash
# Terminal 1: Start your server
python homework/exercises/hw_2_01_implement_calculator_server.py server

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
python homework/exercises/hw_2_02_analyse_pcap_traffic.py pcap/test.pcap
```

---

## Resources

- Python socket documentation: https://docs.python.org/3/library/socket.html
- Scapy documentation: https://scapy.readthedocs.io/
- Week 2 laboratory exercises for reference
- `docs/misconceptions.md` — common errors to avoid

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
