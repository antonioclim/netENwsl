# Expected Outputs — Week 4

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

Reference outputs for exercises and tests to help verify correct implementation.

---

## Exercise 1: TEXT Protocol

### Successful PING

```
$ python src/apps/text_proto_client.py -c "PING"
Connecting to localhost:5400...
Connected.
Sending: PING
Response: OK pong
```

### SET/GET Sequence

```
$ python src/apps/text_proto_client.py -c "SET name Alice" -c "GET name"
Sending: SET name Alice
Response: OK stored name
Sending: GET name
Response: OK name Alice
```

### Full Command Sequence

```
$ python src/apps/text_proto_client.py -c "PING" -c "SET key1 value1" \
    -c "SET key2 value2" -c "GET key1" -c "COUNT" -c "KEYS"
Sending: PING
Response: OK pong
Sending: SET key1 value1
Response: OK stored key1
Sending: SET key2 value2
Response: OK stored key2
Sending: GET key1
Response: OK key1 value1
Sending: COUNT
Response: OK 2 keys
Sending: KEYS
Response: OK key1 key2
```

### Error Cases

```
$ python src/apps/text_proto_client.py -c "GET nonexistent"
Sending: GET nonexistent
Response: ERROR key not found

$ python src/apps/text_proto_client.py -c "INVALID"
Sending: INVALID
Response: ERROR unknown command
```

---

## Exercise 2: BINARY Protocol

### Header Hex Dump (ECHO request)

```
Header (14 bytes): 4e 50 01 01 00 05 00 00 00 2a XX XX XX XX
                   ^^^^^ ^^ ^^ ^^^^^ ^^^^^^^^^^^ ^^^^^^^^^^^
                   Magic V  T  Len   Seq=42      CRC32
                   
Legend:
  4e 50 = 'NP' (magic bytes)
  01    = Version 1
  01    = Type 1 (ECHO_REQ)
  00 05 = Payload length 5 (big-endian)
  00 00 00 2a = Sequence number 42
  XX XX XX XX = CRC32 checksum
```

### BINARY Client Session

```
$ python src/apps/binary_proto_client.py
Connected to localhost:5401
Binary Protocol Client (type 'help' for commands)

> echo hello
Sending ECHO_REQ (seq=1): hello
Response ECHO_RESP: hello

> put mykey myvalue
Sending PUT_REQ (seq=2): mykey=myvalue
Response PUT_RESP: OK

> get mykey
Sending GET_REQ (seq=3): mykey
Response GET_RESP: myvalue

> count
Sending COUNT_REQ (seq=4)
Response COUNT_RESP: 1

> quit
Closing connection...
```

### CRC Verification Failure

```
$ python src/apps/binary_proto_client.py --corrupt
Connected to localhost:5401

> echo test
Sending ECHO_REQ with corrupted CRC...
Response ERROR: CRC verification failed
```

---

## Exercise 3: UDP Sensor Protocol

### Sensor Client Output

```
$ python src/apps/udp_sensor_client.py --sensor-id 1001 --location "Lab01"
Sending sensor datagram...
  Version: 1
  Sensor ID: 1001
  Temperature: 22.50°C
  Location: Lab01
  CRC32: 0xA1B2C3D4
Datagram sent (23 bytes)
```

### Server Aggregation Output

```
$ python src/apps/udp_sensor_server.py
UDP Sensor Server listening on 0.0.0.0:5402

[2026-01-24 10:15:01] Received datagram from 127.0.0.1:54321
  Sensor ID: 1001
  Temperature: 22.50°C
  Location: Lab01
  CRC32: VALID

[2026-01-24 10:15:02] Received datagram from 127.0.0.1:54322
  Sensor ID: 1002
  Temperature: 23.10°C
  Location: Lab02
  CRC32: VALID

Statistics:
  Total datagrams: 2
  Valid CRC: 2
  Invalid CRC: 0
  Average temperature: 22.80°C
```

---

## Smoke Test Output

```
$ python tests/smoke_test.py

============================================================
Week 4 Laboratory Smoke Test
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim
============================================================

Python Environment:
  ✓ Python 3.10.12
  ✓ Required modules available

CRC32 Functionality:
  ✓ CRC32 calculation
  ✓ Change detection

Binary Packing:
  ✓ Pack to bytes (10 bytes)
  ✓ Unpack from bytes

Length-Prefix Framing:
  ✓ Frame creation
  ✓ Frame parsing

Docker (optional):
  ✓ Docker service running
  ✓ Containers available

============================================================
Result: 8/8 tests passed
============================================================
```

---

## Unit Test Output

```
$ python tests/test_unit_functions.py

============================================================
Week 4 Unit Tests — Protocol Functions
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim
============================================================

test_crc32_consistency ... ok
test_crc32_detects_byte_swap ... ok
test_crc32_detects_single_bit_change ... ok
test_big_endian_1000 ... ok
test_little_endian_1000 ... ok
test_wrong_endian_interpretation ... ok
test_header_size_with_crc ... ok
test_header_roundtrip ... ok
test_frame_hello ... ok
test_frame_unicode ... ok
...

----------------------------------------------------------------------
Ran 35 tests in 0.042s

OK
```

---

## Exercise Test Output

```
$ python tests/test_exercises.py --all

============================================================
Week 4 Exercise Tests
============================================================

TestTextProtocol:
  test_ping_response ... ok
  test_set_get_roundtrip ... ok
  test_count_keys ... ok

TestBinaryProtocol:
  test_echo_request ... ok
  test_header_construction ... ok
  test_crc_validation ... ok

TestUDPProtocol:
  test_datagram_size ... ok
  test_location_padding ... ok
  test_crc_verification ... ok

TestCRC32:
  test_consistency ... ok
  test_change_detection ... ok

----------------------------------------------------------------------
Ran 11 tests in 0.156s

OK
```

---

## Formative Quiz Output

```
$ python formative/run_quiz.py --limit 3 --random

════════════════════════════════════════════════════════════
  📝 QUIZ: Physical Layer, Data Link Layer & Custom Protocols
  Questions: 3 | Passing: 70%
════════════════════════════════════════════════════════════

────────────────────────────────────────────────────────────
Question 1/3 [APPLY] [LO4] [intermediate]
────────────────────────────────────────────────────────────

Ce returnează struct.pack('>H', 1000).hex()?

Your answer: 03e8

✅ Correct!
📖 1000 decimal = 0x03E8. Format '>H' înseamnă big-endian unsigned short.

Press Enter to continue...

...

════════════════════════════════════════════════════════════
  📊 RESULTS SUMMARY
════════════════════════════════════════════════════════════

  Score: 3/3 (100.0%)
  Status: ✅ PASSED

  By Learning Objective:
    ✅ LO4: 2/2 (100%)
    ✅ LO2: 1/1 (100%)

  By Bloom Level:
    Apply: 2/2 (100%)
    Understand: 1/1 (100%)

════════════════════════════════════════════════════════════
```

---

## Wireshark Filter Examples

### TEXT Protocol Traffic

```
Filter: tcp.port == 5400
Display: [TCP] [PSH,ACK] Len=15

Frame data (hex):
  0000  31 31 20 53 45 54 20 6e 61 6d 65 20 41 6c 69    11 SET name Ali
  0010  63 65                                            ce

Interpretation:
  "11 SET name Alice" = length-prefixed TEXT protocol message
```

### BINARY Protocol Header

```
Filter: tcp.port == 5401
Display: [TCP] [PSH,ACK] Len=19

Frame data (hex):
  0000  4e 50 01 01 00 05 00 00 00 01 ab cd ef 12 68    NP.........h
  0010  65 6c 6c 6f                                      ello

Interpretation:
  4e 50       = Magic 'NP'
  01          = Version 1
  01          = Type ECHO_REQ
  00 05       = Payload length 5
  00 00 00 01 = Sequence 1
  ab cd ef 12 = CRC32
  68 65 6c 6c 6f = "hello"
```

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
