# Expected Outputs — Week 12

> NETWORKING class - ASE, Informatics | by Revolvix

This document describes the expected outputs for each laboratory exercise and demonstration.

## Exercise 1: SMTP Protocol

### SMTP Server Greeting
When connecting to the SMTP server, you should see:
```
220 Week12 SMTP server ready
```

### EHLO Response
After sending `EHLO client.test`, expect:
```
250-Hello client.test
250-SIZE 1048576
250-8BITMIME
250-PIPELINING
250 This server is for education only
```

### Complete Mail Transaction
```
C: MAIL FROM:<alice@example.test>
S: 250 OK
C: RCPT TO:<bob@example.test>
S: 250 OK
C: DATA
S: 354 End data with <CR><LF>.<CR><LF>
C: Subject: Test
C: 
C: Message body here.
C: .
S: 250 Message accepted for delivery (stored as 20250107_120000_1234_0001.eml)
```

### Stored Message Format
Messages are stored as `.eml` files:
```
From: alice@example.test
To: bob@example.test
Date: Tue, 07 Jan 2025 12:00:00 +0000
Subject: Week 12 SMTP message

Message body here.
```

## Exercise 2: JSON-RPC

### Successful Request
Request:
```json
{"jsonrpc":"2.0","id":1,"method":"add","params":[10,32]}
```

Response:
```json
{"jsonrpc":"2.0","id":1,"result":42.0}
```

### Error Response (Division by Zero)
Request:
```json
{"jsonrpc":"2.0","id":1,"method":"divide","params":[10,0]}
```

Response:
```json
{"jsonrpc":"2.0","id":1,"error":{"code":-32000,"message":"Division by zero"}}
```

### Method Not Found
Request:
```json
{"jsonrpc":"2.0","id":1,"method":"unknown"}
```

Response:
```json
{"jsonrpc":"2.0","id":1,"error":{"code":-32601,"message":"Method not found","data":"unknown"}}
```

### Batch Request
Request:
```json
[
  {"jsonrpc":"2.0","id":1,"method":"add","params":[1,2]},
  {"jsonrpc":"2.0","id":2,"method":"multiply","params":[3,4]}
]
```

Response:
```json
[
  {"jsonrpc":"2.0","id":1,"result":3.0},
  {"jsonrpc":"2.0","id":2,"result":12.0}
]
```

## Exercise 3: XML-RPC

### Successful Request
The XML-RPC client returns Python values directly:
```python
>>> proxy.add(10, 32)
42.0
```

### Introspection
```python
>>> proxy.system.listMethods()
['add', 'divide', 'echo', 'get_server_info', 'get_stats', ...]
```

## Exercise 4: gRPC

### Successful Calculation
```
Add(10, 32) = CalcResponse(result=42.0, operation='add', timestamp=1704628800)
```

### Division by Zero Error
```
grpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated with:
    status = StatusCode.INVALID_ARGUMENT
    details = "Division by zero"
>
```

## Benchmark Expected Range

Typical results on modern hardware (will vary):

| Protocol | Requests/sec | Latency (ms) |
|----------|-------------|--------------|
| JSON-RPC | 500-2000 | 0.5-2.0 |
| XML-RPC | 300-1500 | 0.7-3.0 |
| gRPC | 800-3000 | 0.3-1.5 |

## Wireshark Capture Expectations

### SMTP Traffic (tcp.port == 1025)
- TCP 3-way handshake visible
- Clear text commands and responses
- DATA phase content readable
- Terminating dot sequence visible

### JSON-RPC Traffic (tcp.port == 6200)
- HTTP POST requests
- Content-Type: application/json
- Readable JSON in payload

### XML-RPC Traffic (tcp.port == 6201)
- HTTP POST requests
- Content-Type: text/xml
- XML methodCall and methodResponse visible

### gRPC Traffic (tcp.port == 6251)
- HTTP/2 frames
- Binary Protocol Buffer payload (not human-readable)
- Multiple streams possible

---

*NETWORKING class - ASE, Informatics | by Revolvix*
