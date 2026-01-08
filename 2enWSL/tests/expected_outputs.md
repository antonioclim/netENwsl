# Expected Outputs — Week 2

> NETWORKING class - ASE, Informatics | by Revolvix

## Exercise 1: TCP Concurrent Server

### Server Start (Threaded Mode)

```
$ python src/exercises/ex_2_01_tcp.py server
2024-XX-XX HH:MM:SS [INFO] Starting TCP server (threaded mode) on 0.0.0.0:9090
2024-XX-XX HH:MM:SS [INFO] Server listening, press Ctrl+C to stop
```

### Server Start (Iterative Mode)

```
$ python src/exercises/ex_2_01_tcp.py server --mode iterative
2024-XX-XX HH:MM:SS [INFO] Starting TCP server (iterative mode) on 0.0.0.0:9090
2024-XX-XX HH:MM:SS [INFO] Server listening, press Ctrl+C to stop
```

### Client Connection

```
$ python src/exercises/ex_2_01_tcp.py client
2024-XX-XX HH:MM:SS [INFO] Connecting to localhost:9090
2024-XX-XX HH:MM:SS [INFO] Connected to server
Enter message (or 'quit' to exit): hello world
Server response: OK: HELLO WORLD
Enter message (or 'quit' to exit): networking class
Server response: OK: NETWORKING CLASS
Enter message (or 'quit' to exit): quit
2024-XX-XX HH:MM:SS [INFO] Disconnected from server
```

### Server Log (Client Connected)

```
2024-XX-XX HH:MM:SS [INFO] Client connected: ('127.0.0.1', 54321)
2024-XX-XX HH:MM:SS [INFO] [127.0.0.1:54321] Received: hello world
2024-XX-XX HH:MM:SS [INFO] [127.0.0.1:54321] Sent: OK: HELLO WORLD
2024-XX-XX HH:MM:SS [INFO] [127.0.0.1:54321] Received: networking class
2024-XX-XX HH:MM:SS [INFO] [127.0.0.1:54321] Sent: OK: NETWORKING CLASS
2024-XX-XX HH:MM:SS [INFO] Client disconnected: ('127.0.0.1', 54321)
```

### Load Test Output

```
$ python src/exercises/ex_2_01_tcp.py load --clients 5
2024-XX-XX HH:MM:SS [INFO] Starting load test with 5 clients
2024-XX-XX HH:MM:SS [INFO] Client 1: Connected
2024-XX-XX HH:MM:SS [INFO] Client 2: Connected
2024-XX-XX HH:MM:SS [INFO] Client 3: Connected
2024-XX-XX HH:MM:SS [INFO] Client 4: Connected
2024-XX-XX HH:MM:SS [INFO] Client 5: Connected
2024-XX-XX HH:MM:SS [INFO] All clients completed
2024-XX-XX HH:MM:SS [INFO] Load test complete: 5 clients, 0 errors
```

---

## Exercise 2: UDP Protocol Server

### Server Start

```
$ python src/exercises/ex_2_02_udp.py server
2024-XX-XX HH:MM:SS [INFO] Starting UDP server on 0.0.0.0:9091
2024-XX-XX HH:MM:SS [INFO] Server ready, press Ctrl+C to stop
```

### Interactive Client

```
$ python src/exercises/ex_2_02_udp.py client
2024-XX-XX HH:MM:SS [INFO] UDP client ready (target: localhost:9091)
Type 'help' for available commands, 'quit' to exit

> help
Available commands:
  ping         - Server responds with PONG
  upper:TEXT   - Convert text to uppercase
  lower:TEXT   - Convert text to lowercase
  reverse:TEXT - Reverse the text
  echo:TEXT    - Echo back the text
  time         - Get server timestamp
  help         - Show this help

> ping
PONG

> upper:hello world
HELLO WORLD

> lower:NETWORKING
networking

> reverse:python
nohtyp

> time
2024-XX-XX HH:MM:SS

> quit
2024-XX-XX HH:MM:SS [INFO] Session stats: 5 sent, 5 received, 0 timeouts
```

### Single Command Mode

```
$ python src/exercises/ex_2_02_udp.py client --command "upper:test"
Response: TEST
```

### Server Log

```
2024-XX-XX HH:MM:SS [INFO] [127.0.0.1:54321] Request: ping
2024-XX-XX HH:MM:SS [INFO] [127.0.0.1:54321] Response: PONG
2024-XX-XX HH:MM:SS [INFO] [127.0.0.1:54321] Request: upper:hello world
2024-XX-XX HH:MM:SS [INFO] [127.0.0.1:54321] Response: HELLO WORLD
2024-XX-XX HH:MM:SS [INFO] [127.0.0.1:54321] Request: time
2024-XX-XX HH:MM:SS [INFO] [127.0.0.1:54321] Response: 2024-XX-XX HH:MM:SS
```

---

## Smoke Test Output

```
$ python tests/smoke_test.py
================================================================
Smoke Test - Week 2: Socket Programming
NETWORKING class - ASE, Informatics
================================================================

[1/4] Checking Python syntax...
  ✓ ex_2_01_tcp.py: OK
  ✓ ex_2_02_udp.py: OK

[2/4] Testing imports...
  ✓ ex_2_01_tcp: OK
  ✓ ex_2_02_udp: OK

[3/4] Testing TCP server...
  Starting server...
  Connecting client...
  Sending test message...
  ✓ TCP echo test: OK

[4/4] Testing UDP server...
  Starting server...
  Sending ping...
  ✓ UDP ping test: OK

================================================================
Results: 4/4 passed
All smoke tests passed!
================================================================
```

---

## Test Suite Output

```
$ python tests/test_exercises.py
================================================================
Test Suite - Week 2: Socket Programming
================================================================

test_tcp_server_starts ... OK
test_tcp_client_connects ... OK
test_tcp_uppercase_transform ... OK
test_tcp_concurrent_handling ... OK
test_tcp_iterative_mode ... OK
test_udp_server_starts ... OK
test_udp_ping_response ... OK
test_udp_upper_command ... OK
test_udp_lower_command ... OK
test_udp_reverse_command ... OK
test_udp_time_command ... OK
test_udp_invalid_command ... OK

================================================================
Ran 12 tests in 5.234s

OK
```

---

## Demonstration Output

### Demo 1: TCP vs UDP Comparison

```
$ python scripts/run_demo.py --demo 1
================================================================
Demo 1: TCP vs UDP Protocol Comparison
================================================================

This demonstration shows the fundamental differences between
TCP (connection-oriented) and UDP (connectionless) protocols.

Step 1: Starting servers...
  TCP server on port 9090
  UDP server on port 9091

Step 2: TCP three-way handshake demonstration
  Client initiating connection...
  → SYN sent to server
  ← SYN-ACK received from server
  → ACK sent to server
  ✓ Connection established

  Sending data over TCP...
  → "Hello TCP" sent
  ← "OK: HELLO TCP" received
  ✓ Data exchanged reliably

Step 3: UDP datagram exchange
  No handshake required
  → "ping" sent to server
  ← "PONG" received
  ✓ Datagram exchanged

Step 4: Comparison summary

| Characteristic  | TCP          | UDP          |
|-----------------|--------------|--------------|
| Connection      | Required     | Not required |
| Handshake       | 3-way        | None         |
| Reliability     | Guaranteed   | Best effort  |
| Packet overhead | 20+ bytes    | 8 bytes      |

Press Enter to continue...

Step 5: Cleanup
  Stopping servers...
  ✓ Demo complete

================================================================
Demo 1 completed successfully
================================================================
```

### Demo 2: Concurrent Server Handling

```
$ python scripts/run_demo.py --demo 2
================================================================
Demo 2: Concurrent vs Iterative Server
================================================================

This demonstration compares threaded (concurrent) and iterative
server models under simultaneous client load.

Step 1: Starting threaded server...
  Server ready on port 9090 (threaded mode)

Step 2: Launching 5 simultaneous clients...
  All clients connected within 0.05 seconds
  All clients completed within 0.12 seconds
  ✓ Threaded server handles concurrent connections efficiently

Step 3: Restarting in iterative mode...
  Server ready on port 9090 (iterative mode)

Step 4: Launching 5 simultaneous clients...
  Clients complete sequentially (one at a time)
  Total time: 0.51 seconds
  ⚠ Iterative server creates bottleneck under load

Step 5: Results comparison

| Server Mode  | 5 Clients | Avg Response |
|--------------|-----------|--------------|
| Threaded     | 0.12s     | 0.024s       |
| Iterative    | 0.51s     | 0.102s       |

Observations:
- Threaded server processes all clients in parallel
- Iterative server processes clients sequentially
- Under load, threaded mode provides ~4x better throughput

Step 6: Cleanup
  ✓ Demo complete

================================================================
Demo 2 completed successfully
================================================================
```

---

## Wireshark Observations

### TCP Three-Way Handshake

When filtering with `tcp.port == 9090`, you should observe:

| No. | Time     | Source    | Destination | Protocol | Info                          |
|-----|----------|-----------|-------------|----------|-------------------------------|
| 1   | 0.000000 | 127.0.0.1 | 127.0.0.1   | TCP      | 54321 → 9090 [SYN]           |
| 2   | 0.000042 | 127.0.0.1 | 127.0.0.1   | TCP      | 9090 → 54321 [SYN, ACK]      |
| 3   | 0.000058 | 127.0.0.1 | 127.0.0.1   | TCP      | 54321 → 9090 [ACK]           |
| 4   | 0.001234 | 127.0.0.1 | 127.0.0.1   | TCP      | 54321 → 9090 [PSH, ACK] Len=11 |
| 5   | 0.001456 | 127.0.0.1 | 127.0.0.1   | TCP      | 9090 → 54321 [PSH, ACK] Len=15 |

### UDP Exchange

When filtering with `udp.port == 9091`, you should observe:

| No. | Time     | Source    | Destination | Protocol | Info              |
|-----|----------|-----------|-------------|----------|-------------------|
| 1   | 0.000000 | 127.0.0.1 | 127.0.0.1   | UDP      | 54321 → 9091 Len=4 |
| 2   | 0.000089 | 127.0.0.1 | 127.0.0.1   | UDP      | 9091 → 54321 Len=4 |

Note: UDP shows no connection establishment — datagrams are sent directly.

---

*NETWORKING class - ASE, Informatics | by Revolvix*
