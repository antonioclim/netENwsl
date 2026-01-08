# Expected Outputs - Week 3

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by Revolvix

This document describes the expected outputs for each exercise to help verify correct implementation.

---

## Exercise 1: UDP Broadcast

### Sender Output

```
=== UDP Broadcast Sender ===
Target: 255.255.255.255:5007
Message: Hello, broadcast world!

[10:30:01] Sending broadcast message 1...
[10:30:02] Sent 22 bytes to 255.255.255.255:5007
[10:30:03] Sending broadcast message 2...
[10:30:04] Sent 22 bytes to 255.255.255.255:5007
...
```

### Receiver Output

```
=== UDP Broadcast Receiver ===
Listening on 0.0.0.0:5007

[10:30:02] Received 22 bytes from 172.20.0.100:45678
           Message: Hello, broadcast world!
[10:30:04] Received 22 bytes from 172.20.0.100:45678
           Message: Hello, broadcast world!
...
```

### Wireshark Filter

```
udp.port == 5007
```

### Expected Packet Structure

| Field | Value |
|-------|-------|
| Source IP | 172.20.0.100 (client container) |
| Destination IP | 255.255.255.255 |
| Protocol | UDP |
| Source Port | Ephemeral (>1024) |
| Destination Port | 5007 |
| Payload | ASCII text message |

### Verification Commands

```bash
# From client container
docker exec -it week3_client python3 /app/src/exercises/ex_3_01_udp_broadcast.py --mode sender --count 5

# From receiver container (separate terminal)
docker exec -it week3_receiver python3 /app/src/exercises/ex_3_01_udp_broadcast.py --mode receiver
```

---

## Exercise 2: UDP Multicast

### Sender Output

```
=== UDP Multicast Sender ===
Group: 239.0.0.1:5008
Message: Multicast message

[10:35:01] Joining multicast group 239.0.0.1
[10:35:01] Sending message 1 to group...
[10:35:02] Sent 17 bytes
[10:35:03] Sending message 2 to group...
[10:35:04] Sent 17 bytes
...
```

### Receiver Output

```
=== UDP Multicast Receiver ===
Joining group 239.0.0.1 on port 5008

[10:35:01] Joined multicast group 239.0.0.1
[10:35:02] Received 17 bytes from 172.20.0.100:52341
           Message: Multicast message
[10:35:04] Received 17 bytes from 172.20.0.100:52341
           Message: Multicast message
...
```

### Wireshark Filters

```
# All multicast traffic
ip.dst >= 239.0.0.0 and ip.dst <= 239.255.255.255

# Specific group
ip.dst == 239.0.0.1 and udp.port == 5008

# IGMP membership reports
igmp
```

### Expected IGMP Behaviour

1. **Group Join:** IGMP Membership Report (type 0x16 for IGMPv2)
   - Destination: 239.0.0.1 (same as group)
   - Reports membership to local router

2. **Group Leave:** IGMP Leave Group (type 0x17)
   - Destination: 224.0.0.2 (all routers)

### Expected Packet Structure

| Field | Value |
|-------|-------|
| Source IP | 172.20.0.100 (sender) |
| Destination IP | 239.0.0.1 (multicast group) |
| Protocol | UDP |
| TTL | 1 (default) or configured value |
| Destination Port | 5008 |

### Verification Commands

```bash
# Start multiple receivers
docker exec -it week3_receiver python3 /app/src/exercises/ex_3_02_udp_multicast.py --mode receiver &
docker exec -it week3_client python3 /app/src/exercises/ex_3_02_udp_multicast.py --mode receiver &

# Send multicast messages
docker exec week3_server python3 /app/src/exercises/ex_3_02_udp_multicast.py --mode sender --count 5

# Check IGMP groups in container
docker exec week3_receiver cat /proc/net/igmp
```

---

## Exercise 3: TCP Tunnel

### Tunnel Server Output

```
=== TCP Tunnel ===
Listening on 0.0.0.0:9090
Forwarding to 172.20.0.10:8080

[10:40:01] New connection from 172.20.0.100:54321
[10:40:01] Connected to target 172.20.0.10:8080
[10:40:02] Relaying data...
[10:40:05] Connection closed. Transferred: 1.2 KB in, 1.2 KB out
...
```

### Client Perspective

```bash
# Connect through tunnel
$ nc localhost 9090
Hello through tunnel
Hello through tunnel    # Echo response from server

# Or using Python
$ python3 -c "
import socket
s = socket.socket()
s.connect(('localhost', 9090))
s.send(b'Test message\n')
print(s.recv(1024))
s.close()
"
b'Test message\n'
```

### Wireshark Analysis

**Filter for tunnel traffic:**
```
tcp.port == 9090 or tcp.port == 8080
```

**Expected TCP Flow:**

1. **Client → Tunnel (port 9090)**
   - SYN, SYN-ACK, ACK (3-way handshake)
   - PSH/ACK with data
   
2. **Tunnel → Server (port 8080)**
   - Separate TCP connection
   - Data relayed from client
   
3. **Server → Tunnel**
   - Echo response

4. **Tunnel → Client**
   - Relayed response

### Expected Behaviour

| Scenario | Expected Result |
|----------|-----------------|
| Single message | Echoed back through tunnel |
| Multiple messages | Each echoed in sequence |
| Large payload (>MTU) | Correctly reassembled |
| Client disconnect | Both connections closed |
| Server unavailable | Error message to client |

### Verification Commands

```bash
# Test basic tunnel functionality
echo "Test" | nc localhost 9090

# Test from client container through tunnel
docker exec week3_client bash -c 'echo "Hello" | nc 172.20.0.254 9090'

# Measure throughput
docker exec week3_client bash -c 'dd if=/dev/zero bs=1M count=10 | nc 172.20.0.254 9090 > /dev/null'
```

---

## Exercise 4: Wireshark Analysis

### Capture Commands

```bash
# Start capture on server
python scripts/capture_traffic.py --container server --duration 30 --output pcap/week3_server.pcap

# Or directly with tcpdump
docker exec week3_server tcpdump -i eth0 -w /tmp/capture.pcap -c 100
docker cp week3_server:/tmp/capture.pcap ./pcap/
```

### Analysis Tasks

**Task 1: Identify Broadcast Traffic**
```
Filter: eth.dst == ff:ff:ff:ff:ff:ff
Expected: UDP packets to 255.255.255.255
```

**Task 2: Find Multicast Groups**
```
Filter: igmp
Expected: Membership reports for 239.0.0.1
```

**Task 3: Trace TCP Tunnel Path**
```
Filter: tcp.stream eq 0
Follow TCP Stream to see both legs
```

**Task 4: Calculate Statistics**
```
Statistics → Protocol Hierarchy
Statistics → Conversations → TCP/UDP
Statistics → I/O Graphs
```

### Expected Statistics (Sample Session)

| Metric | Expected Range |
|--------|----------------|
| Total packets | 100-500 |
| UDP broadcast | 20-50 packets |
| UDP multicast | 20-50 packets |
| TCP (tunnel) | 50-200 packets |
| IGMP | 2-10 packets |

---

## Common Issues and Expected Errors

### Broadcast Permission Error

**Error:**
```
OSError: [Errno 10013] An attempt was made to access a socket in a way forbidden by its access permissions
```

**Cause:** Windows requires elevated privileges for broadcast.

**Solution:** Run as Administrator or use Docker containers.

### Multicast Not Received

**Symptom:** Sender shows success, receiver shows nothing.

**Verification:**
```bash
# Check if group is joined
docker exec week3_receiver cat /proc/net/igmp | grep 239
```

**Expected output when joined:**
```
2    eth0            : 1      V3
                             EF000001
```

### Tunnel Connection Refused

**Error:**
```
ConnectionRefusedError: [Errno 111] Connection refused
```

**Verification:**
```bash
# Check server is running
docker exec week3_server ss -tlnp | grep 8080
```

**Expected:**
```
LISTEN 0      128          0.0.0.0:8080       0.0.0.0:*    users:(("python3",pid=1,fd=3))
```

---

## Test Verification Summary

Run the automated tests to verify all exercises:

```bash
# Full test suite
python tests/test_exercises.py

# Individual exercise
python tests/test_exercises.py --exercise 1

# Smoke test (quick)
python tests/smoke_test.py
```

### Expected Test Output

```
===============================================
Week 3 Exercise Tests
===============================================

Exercise 1: UDP Broadcast
  [PASS] Broadcast socket creation
  [PASS] Broadcast send/receive
  [PASS] Multiple receivers

Exercise 2: UDP Multicast
  [PASS] Multicast group join
  [PASS] Multicast send/receive
  [PASS] Multiple group members

Exercise 3: TCP Tunnel
  [PASS] Tunnel accepts connections
  [PASS] Data relayed correctly
  [PASS] Bidirectional communication
  [PASS] Connection cleanup

Exercise 4: Wireshark Analysis
  [PASS] Capture file created
  [PASS] Expected packets present

===============================================
Results: 11 passed, 0 failed
===============================================
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
