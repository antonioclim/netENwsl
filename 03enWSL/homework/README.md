# Homework Assignments - Week 3

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

## Overview

These homework assignments extend the concepts explored during the Week 3 laboratory session. Each assignment builds upon the broadcast, multicast and tunnelling exercises completed in class.


## Anti-AI submission requirements

These homework assignments are assessed with an **anti-AI** validator. You may use AI tools for clarification and debugging, but AI alone must not be sufficient to produce a valid submission.

You must submit **verifiable execution evidence**:

1. A per-student challenge file (`challenge_<student_id>.yaml`)
2. Three PCAP captures that contain your unique **payload token**:
   - UDP broadcast
   - UDP multicast
   - TCP tunnel traffic (including the TCP handshake)
3. A short report file that contains your unique **report token**
4. An evidence file (`evidence.json`) that lists SHA-256 hashes of the artefacts

### Naming conventions (required)

Place all anti-AI artefacts in `artifacts/anti_ai/` using these exact names:

- `artifacts/anti_ai/w03_report_<student_id>.md`
- `artifacts/anti_ai/w03_broadcast_<student_id>.pcap`
- `artifacts/anti_ai/w03_multicast_<student_id>.pcap`
- `artifacts/anti_ai/w03_tunnel_<student_id>.pcap`
- `artifacts/anti_ai/evidence_<student_id>.json`

### Step-by-step workflow

From the `03enWSL/` directory:

1) Start the lab environment

```bash
sudo service docker start
docker compose -f docker/docker-compose.yml up -d
```

2) Generate your challenge

```bash
python3 -m anti_ai.challenge_generator --student-id <student_id>
# Optional: randomise ports (advanced)
# python3 -m anti_ai.challenge_generator --student-id <student_id> --random-ports
```

The command prints your recommended ports and your two tokens:
- `payload_token` must appear inside your PCAP payloads
- `report_token` must appear in your report file

3) Create the report file and include the report token

```bash
mkdir -p artifacts/anti_ai
cat > artifacts/anti_ai/w03_report_<student_id>.md << 'EOF'
Week 3 anti-AI report

Report token: <paste your report_token here>

Brief notes:
- What you ran and what you observed
- Any issues and how you resolved them
EOF
```

4) Produce and capture UDP broadcast traffic (payload token)

Run a receiver and a sender and capture the traffic. Use the recommended broadcast port printed by the challenge generator.

Example commands (inside Docker containers):

```bash
# Receiver (in one terminal)
docker exec -it week3_receiver       python3 /app/src/exercises/ex_3_01_udp_broadcast.py recv       --port <broadcast_port> --count 5 --no-predict
```

```bash
# Capture (in another terminal on the host)
python3 scripts/capture_traffic.py       --container week3_receiver       --filter "udp port <broadcast_port>"       --duration 10       --output artifacts/anti_ai/w03_broadcast_<student_id>.pcap
```

```bash
# Sender (in a third terminal)
docker exec -it week3_client       python3 /app/src/exercises/ex_3_01_udp_broadcast.py send       --dst 255.255.255.255 --port <broadcast_port>       --count 5 --interval 0.2       --message "<payload_token> broadcast"       --no-predict
```

5) Produce and capture UDP multicast traffic (payload token)

```bash
# Receiver
docker exec -it week3_receiver       python3 /app/src/exercises/ex_3_02_udp_multicast.py recv       --group 239.0.0.10 --port <multicast_port> --count 5 --no-predict
```

```bash
# Capture
python3 scripts/capture_traffic.py       --container week3_receiver       --filter "udp port <multicast_port>"       --duration 10       --output artifacts/anti_ai/w03_multicast_<student_id>.pcap
```

```bash
# Sender
docker exec -it week3_client       python3 /app/src/exercises/ex_3_02_udp_multicast.py send       --group 239.0.0.10 --port <multicast_port>       --count 5 --interval 0.2       --message "<payload_token> multicast"       --no-predict
```

6) Produce and capture TCP tunnel traffic (payload token)

The router container already runs a tunnel from `router:9090` to `server:8080` in the default docker-compose setup.

```bash
# Capture on the router side (recommended)
python3 scripts/capture_traffic.py       --container week3_router       --filter "tcp port 9090"       --duration 10       --output artifacts/anti_ai/w03_tunnel_<student_id>.pcap
```

```bash
# Send payload through the tunnel (client -> router:9090 -> server:8080)
docker exec -it week3_client bash -lc 'echo "<payload_token> tunnel" | nc -w 2 router 9090'
```

Ensure the capture includes the **connection setup** (SYN, SYN-ACK and ACK) and the payload bytes.

7) Collect evidence (hashes)

```bash
python3 -m anti_ai.evidence_collector       --challenge artifacts/anti_ai/challenge_<student_id>.yaml       --output artifacts/anti_ai/evidence_<student_id>.json       --base-dir .       --artefact artifacts/anti_ai/w03_report_<student_id>.md       --artefact artifacts/anti_ai/w03_broadcast_<student_id>.pcap       --artefact artifacts/anti_ai/w03_multicast_<student_id>.pcap       --artefact artifacts/anti_ai/w03_tunnel_<student_id>.pcap
```

8) Validate locally before submission

```bash
python3 -m anti_ai.submission_validator       --challenge artifacts/anti_ai/challenge_<student_id>.yaml       --evidence artifacts/anti_ai/evidence_<student_id>.json       --base-dir .       --verbose
```

If the validator fails, fix the issue and re-capture. Do not submit failing evidence.

---
---

## Assignment 1: Enhanced Broadcast Receiver with Statistics

**File:** `exercises/hw_3_01_broadcast_statistics.py`

**Objective:** Extend the basic UDP broadcast receiver to collect and display thorough statistics about received traffic.

**Requirements:**

1. **Packet Statistics**
   - Count total packets received
   - Track unique sender IP addresses
   - Calculate packets per second (moving average)
   - Measure minimum, maximum and average payload sizes

2. **Timing Analysis**
   - Record timestamp of first and last packet
   - Calculate inter-arrival time statistics
   - Detect gaps (>1 second between packets)

3. **Output Format**
   - Display real-time statistics every 5 seconds
   - Generate summary report on programme termination (Ctrl+C)
   - Optionally save statistics to JSON file

**Example Output:**
```
=== Broadcast Receiver Statistics ===
Runtime: 45.2 seconds
Total packets: 127
Unique senders: 3
Packets/second: 2.81 (avg)
Payload size: min=32, max=512, avg=128.4 bytes
Gaps detected: 2

Sender breakdown:
  172.20.0.10: 65 packets (51.2%)
  172.20.0.100: 42 packets (33.1%)
  172.20.0.101: 20 packets (15.7%)
```

**Grading Criteria:**
- Correct statistics calculation: 40%
- Graceful shutdown handling: 20%
- Code quality and documentation: 20%
- Optional JSON export: 20%

---

## Assignment 2: Multicast Chat Application

**File:** `exercises/hw_3_02_multicast_chat.py`

**Objective:** Implement a simple multicast-based chat application where multiple users can join a group and exchange messages.

**Requirements:**

1. **User Interface**
   - Text-based command-line interface
   - Prompt for username on startup
   - Display received messages with sender name and timestamp

2. **Multicast Communication**
   - Use multicast group 239.0.0.10, port 5010
   - Join group on startup, leave on exit
   - Handle both sending and receiving concurrently

3. **Message Protocol**
   - Design a simple message format (JSON recommended)
   - Include: sender name, timestamp, message type, content
   - Support message types: JOIN, MESSAGE, LEAVE

4. **Features**
   - Display notification when users join/leave
   - Ignore own messages (don't echo back)
   - Handle network errors gracefully

**Message Format Example:**
```json
{
  "type": "MESSAGE",
  "sender": "Alice",
  "timestamp": "2024-02-15T10:30:45",
  "content": "Hello everyone!"
}
```

**Example Session:**
```
=== Multicast Chat ===
Enter username: Alice
Joined chat group 239.0.0.10:5010

[10:30:42] Bob joined the chat
[10:30:45] Alice: Hello everyone!
[10:30:48] Bob: Hi Alice!
[10:31:02] Charlie joined the chat
[10:31:15] Charlie: Good morning!
^C
[10:31:20] Alice left the chat
```

**Grading Criteria:**
- Correct multicast implementation: 30%
- Concurrent send/receive handling: 25%
- Message protocol design: 20%
- User experience and error handling: 25%

---

## Assignment 3: TCP Tunnel with Logging and Metrics

**File:** `exercises/hw_3_03_tunnel_logging.py`

**Objective:** Enhance the basic TCP tunnel to provide detailed logging, traffic metrics and optional features.

**Requirements:**

1. **Thorough Logging**
   - Log all connections (source, destination, timestamp)
   - Log data transfer statistics per connection
   - Support multiple log levels (DEBUG, INFO, WARNING, ERROR)
   - Write logs to both console and file

2. **Traffic Metrics**
   - Bytes transferred in each direction
   - Connection duration
   - Average throughput (bytes/second)
   - Peak concurrent connections

3. **Enhanced Features**
   - Maximum connections limit
   - Idle connection timeout
   - Bandwidth throttling (optional)
   - Connection filtering by source IP (optional)

4. **Status Interface**
   - Display current connections on demand (e.g., SIGUSR1)
   - Show cumulative statistics

**Log Format Example:**
```
2024-02-15 10:30:42 INFO  [conn-001] New connection from 172.20.0.100:45678
2024-02-15 10:30:42 INFO  [conn-001] Connected to target 172.20.0.10:8080
2024-02-15 10:30:43 DEBUG [conn-001] Relayed 256 bytes client->server
2024-02-15 10:30:43 DEBUG [conn-001] Relayed 1024 bytes server->client
2024-02-15 10:30:45 INFO  [conn-001] Connection closed. Duration: 3.2s, Tx: 512B, Rx: 2048B
```

**Statistics Output:**
```
=== Tunnel Statistics ===
Uptime: 1h 23m 45s
Total connections: 47
Active connections: 3
Peak concurrent: 8
Total bytes relayed: 15.2 MB (client->server: 5.1 MB, server->client: 10.1 MB)
Average connection duration: 45.3 seconds
Average throughput: 128.5 KB/s
```

**Grading Criteria:**
- Logging implementation: 30%
- Metrics collection: 25%
- Code architecture and quality: 25%
- Optional features: 20%

---

## Submission Guidelines

### Format

1. Submit Python source files only (`.py`)
2. Include your name and student ID in file headers
3. Ensure code runs without modification in the Week 3 Docker environment

### File Header Template

```python
#!/usr/bin/env python3
"""
Homework 3.<N>: <Title>
NETWORKING class - ASE, Informatics

Student: <Your Name>
Student ID: <Your ID>
Date: <Submission Date>

Description:
<Brief description of your implementation>
"""
```

### Testing

Before submission, verify your code works:

```bash
# Start the laboratory environment
python scripts/start_lab.py

# Test your homework in the client container
docker exec -it week3_client python3 /app/homework/exercises/hw_3_0X_name.py
```

### Deadline

Submit via the university e-learning platform by the deadline announced in class.

---

## Evaluation

Each assignment is worth 33.3% of the homework grade. Partial credit is awarded for incomplete implementations that demonstrate understanding of the concepts.

**Bonus Points:**
- Exceptional code quality and documentation
- Creative extensions beyond requirements
- Thorough error handling and edge case coverage

---

## Academic Integrity

- Individual work required
- Cite any external resources used
- Discussion of concepts is encouraged; sharing code is not permitted

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
