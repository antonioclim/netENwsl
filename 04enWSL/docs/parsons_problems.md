# 🧩 Parsons Problems — Week 4

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

## Physical Layer, Data Link Layer & Custom Protocols

Reorder the code blocks to create working solutions. Some problems include distractor blocks that should NOT be used.

---

## Problem P1: Build Binary Header

### Task

Create a function that builds a 14-byte binary header with the following structure:

```
┌────────┬─────────┬──────┬────────────┬─────┬───────┐
│ Magic  │ Version │ Type │ PayloadLen │ Seq │ CRC32 │
│ 2B     │ 1B      │ 1B   │ 2B         │ 4B  │ 4B    │
└────────┴─────────┴──────┴────────────┴─────┴───────┘
```

The CRC32 should be calculated over the header (without CRC field) plus the payload.

### Scrambled Blocks

```python
# Block A
    return header_with_crc

# Block B
def build_header(msg_type: int, payload: bytes, seq: int) -> bytes:

# Block C
    crc = zlib.crc32(header_no_crc + payload) & 0xFFFFFFFF

# Block D
    header_no_crc = struct.pack('>2sBBHI', MAGIC, VERSION, msg_type, len(payload), seq)

# Block E
    header_with_crc = struct.pack('>2sBBHII', MAGIC, VERSION, msg_type, len(payload), seq, crc)

# Block F (DISTRACTOR - not needed)
    header_with_crc = header_no_crc + struct.pack('>I', crc)

# Block G
import struct
import zlib

MAGIC = b'NP'
VERSION = 1

# Block H (DISTRACTOR - wrong byte order)
    header_no_crc = struct.pack('<2sBBHI', MAGIC, VERSION, msg_type, len(payload), seq)
```

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block G - Imports and constants first
import struct
import zlib

MAGIC = b'NP'
VERSION = 1

# Block B - Function definition
def build_header(msg_type: int, payload: bytes, seq: int) -> bytes:

# Block D - Build header without CRC (big-endian!)
    header_no_crc = struct.pack('>2sBBHI', MAGIC, VERSION, msg_type, len(payload), seq)

# Block C - Calculate CRC over header + payload
    crc = zlib.crc32(header_no_crc + payload) & 0xFFFFFFFF

# Block E - Build complete header with CRC
    header_with_crc = struct.pack('>2sBBHII', MAGIC, VERSION, msg_type, len(payload), seq, crc)

# Block A - Return result
    return header_with_crc
```

**Distractor explanations:**
- **Block F** is wrong because it would make the header 10 + 4 = 14 bytes but with inconsistent packing
- **Block H** uses little-endian (`<`) instead of network byte order (`>`)

**Key insight:** CRC is calculated BEFORE being added to the header. The complete header is then packed in one call with the calculated CRC value.

</details>

---

## Problem P2: Receive Exact Bytes

### Task

Create a function that receives exactly `n` bytes from a socket, handling partial reads correctly.

### Scrambled Blocks

```python
# Block A
def recv_exact(sock: socket.socket, n: int) -> bytes:

# Block B
    return data

# Block C
    while len(data) < n:

# Block D
        chunk = sock.recv(n - len(data))

# Block E
    data = b''

# Block F
        if not chunk:
            raise ConnectionError("Connection closed")

# Block G
        data += chunk

# Block H (DISTRACTOR - wrong approach)
    data = sock.recv(n)
    return data

# Block I (DISTRACTOR - infinite loop risk)
    while True:
        chunk = sock.recv(n)
        data += chunk
        if len(data) >= n:
            break
```

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block A - Function definition
def recv_exact(sock: socket.socket, n: int) -> bytes:

# Block E - Initialise empty buffer
    data = b''

# Block C - Loop until we have n bytes
    while len(data) < n:

# Block D - Receive up to remaining bytes needed
        chunk = sock.recv(n - len(data))

# Block F - Check for connection close
        if not chunk:
            raise ConnectionError("Connection closed")

# Block G - Append received chunk
        data += chunk

# Block B - Return complete data
    return data
```

**Distractor explanations:**
- **Block H** assumes `recv(n)` always returns exactly n bytes — WRONG! It may return fewer.
- **Block I** always requests `n` bytes instead of `n - len(data)` and doesn't handle connection close properly.

**Key insight:** `recv()` may return fewer bytes than requested. The loop must continue until exactly n bytes are accumulated and connection close (empty bytes) must be detected.

</details>

---

## Problem P3: Parse Length-Prefixed Message

### Task

Create a function that receives and parses a length-prefixed message where the length is a 2-byte big-endian unsigned integer.

### Scrambled Blocks

```python
# Block A
def recv_framed_message(sock: socket.socket) -> bytes:

# Block B
    length = int.from_bytes(length_bytes, 'big')

# Block C
    return payload

# Block D
    length_bytes = recv_exact(sock, 2)

# Block E
    payload = recv_exact(sock, length)

# Block F (DISTRACTOR - wrong endianness)
    length = int.from_bytes(length_bytes, 'little')

# Block G (DISTRACTOR - wrong approach)
    length = struct.unpack('<H', length_bytes)[0]

# Block H (DISTRACTOR - doesn't use recv_exact)
    length_bytes = sock.recv(2)
```

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block A - Function definition
def recv_framed_message(sock: socket.socket) -> bytes:

# Block D - Receive exactly 2 bytes for length
    length_bytes = recv_exact(sock, 2)

# Block B - Convert to integer (big-endian = network order)
    length = int.from_bytes(length_bytes, 'big')

# Block E - Receive exactly 'length' bytes of payload
    payload = recv_exact(sock, length)

# Block C - Return the payload
    return payload
```

**Distractor explanations:**
- **Block F** uses little-endian, but network protocols use big-endian
- **Block G** also uses little-endian (`<H`)
- **Block H** uses raw `recv(2)` which might return only 1 byte!

**Key insight:** Always use `recv_exact()` (or equivalent) for protocol data. Network byte order is big-endian.

</details>

---

## Problem P4: Verify CRC32

### Task

Create a function that verifies the CRC32 of a received message. The CRC is the last 4 bytes of the message and covers all preceding bytes.

### Scrambled Blocks

```python
# Block A
def verify_crc(message: bytes) -> bool:

# Block B
    return calculated_crc == received_crc

# Block C
    received_crc = struct.unpack('>I', message[-4:])[0]

# Block D
    data_without_crc = message[:-4]

# Block E
    calculated_crc = zlib.crc32(data_without_crc) & 0xFFFFFFFF

# Block F (DISTRACTOR - wrong slice)
    received_crc = struct.unpack('>I', message[:4])[0]

# Block G (DISTRACTOR - CRC at wrong position)
    data_without_crc = message[4:]

# Block H
import struct
import zlib
```

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block H - Imports
import struct
import zlib

# Block A - Function definition
def verify_crc(message: bytes) -> bool:

# Block D - Separate data from CRC (CRC is last 4 bytes)
    data_without_crc = message[:-4]

# Block C - Extract received CRC (last 4 bytes, big-endian)
    received_crc = struct.unpack('>I', message[-4:])[0]

# Block E - Calculate expected CRC
    calculated_crc = zlib.crc32(data_without_crc) & 0xFFFFFFFF

# Block B - Compare and return
    return calculated_crc == received_crc
```

**Distractor explanations:**
- **Block F** reads CRC from the beginning instead of the end
- **Block G** excludes the wrong bytes from CRC calculation

**Key insight:** CRC position must match between sender and receiver. The `& 0xFFFFFFFF` ensures unsigned 32-bit result.

</details>

---

## Problem P5: UDP Sensor Packet Builder

### Task

Build a UDP sensor packet with the following structure:

```
┌─────────┬──────────┬──────────────┬──────────────┬───────────┬───────┐
│ Version │ SensorID │ Temperature  │ Humidity     │ Timestamp │ CRC16 │
│ 1B      │ 4B       │ 4B (float)   │ 4B (float)   │ 8B        │ 2B    │
└─────────┴──────────┴──────────────┴──────────────┴───────────┴───────┘
```

### Scrambled Blocks

```python
# Block A
def build_sensor_packet(sensor_id: int, temp: float, humidity: float) -> bytes:

# Block B
    timestamp = int(time.time())

# Block C
    packet_no_crc = struct.pack('>BIffQ', VERSION, sensor_id, temp, humidity, timestamp)

# Block D
    crc16 = zlib.crc32(packet_no_crc) & 0xFFFF

# Block E
    return packet_no_crc + struct.pack('>H', crc16)

# Block F
import struct
import zlib
import time

VERSION = 1

# Block G (DISTRACTOR - wrong format)
    packet_no_crc = struct.pack('>BIddQ', VERSION, sensor_id, temp, humidity, timestamp)

# Block H (DISTRACTOR - little-endian)
    packet_no_crc = struct.pack('<BIffQ', VERSION, sensor_id, temp, humidity, timestamp)
```

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block F - Imports and constants
import struct
import zlib
import time

VERSION = 1

# Block A - Function definition
def build_sensor_packet(sensor_id: int, temp: float, humidity: float) -> bytes:

# Block B - Get current timestamp
    timestamp = int(time.time())

# Block C - Pack data (f = float, Q = unsigned long long)
    packet_no_crc = struct.pack('>BIffQ', VERSION, sensor_id, temp, humidity, timestamp)

# Block D - Calculate CRC16 (mask to 16 bits)
    crc16 = zlib.crc32(packet_no_crc) & 0xFFFF

# Block E - Append CRC and return
    return packet_no_crc + struct.pack('>H', crc16)
```

**Distractor explanations:**
- **Block G** uses `d` (8-byte double) instead of `f` (4-byte float)
- **Block H** uses little-endian

**Key insight:** 
- `f` = 4-byte float, `d` = 8-byte double
- `Q` = 8-byte unsigned integer (for timestamp)
- CRC16 uses `& 0xFFFF` to mask to 16 bits

</details>

---

## Challenge Problem: Complete Protocol Handler

### Task

Create a complete message handler that:
1. Receives a framed message
2. Validates the CRC
3. Processes the command
4. Sends a framed response

This is a larger problem — arrange ALL blocks correctly.

### Scrambled Blocks (12 blocks, 2 distractors)

```python
# Block A
def handle_message(sock: socket.socket) -> None:

# Block B
    frame = recv_framed_message(sock)

# Block C
    if not verify_crc(frame):
        send_error(sock, "CRC mismatch")
        return

# Block D
    header = frame[:14]
    payload = frame[14:-4]

# Block E
    msg_type = header[3]

# Block F
    if msg_type == TYPE_ECHO:
        response_payload = payload
    elif msg_type == TYPE_UPPER:
        response_payload = payload.upper()
    else:
        send_error(sock, "Unknown type")
        return

# Block G
    response = build_response(msg_type + 1, response_payload, get_seq(header))

# Block H
    send_framed_message(sock, response)

# Block I (DISTRACTOR - processes before validation)
    msg_type = header[3]
    if msg_type == TYPE_ECHO:
        response_payload = payload

# Block J (DISTRACTOR - sends unframed)
    sock.send(response)
```

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block A
def handle_message(sock: socket.socket) -> None:

# Block B - Receive the complete framed message
    frame = recv_framed_message(sock)

# Block C - Validate CRC FIRST (security!)
    if not verify_crc(frame):
        send_error(sock, "CRC mismatch")
        return

# Block D - Parse frame components
    header = frame[:14]
    payload = frame[14:-4]

# Block E - Extract message type
    msg_type = header[3]

# Block F - Process based on type
    if msg_type == TYPE_ECHO:
        response_payload = payload
    elif msg_type == TYPE_UPPER:
        response_payload = payload.upper()
    else:
        send_error(sock, "Unknown type")
        return

# Block G - Build response
    response = build_response(msg_type + 1, response_payload, get_seq(header))

# Block H - Send framed response
    send_framed_message(sock, response)
```

**Distractor explanations:**
- **Block I** processes the message before validating CRC — security risk!
- **Block J** sends response without framing

**Key insight:** Always validate integrity (CRC) BEFORE processing. Response type is typically request type + 1.

</details>

---

## Self-Assessment Checklist

After completing these problems, verify you understand:

- [ ] Order of operations for building binary packets
- [ ] Why `recv_exact()` uses a loop
- [ ] Difference between big-endian and little-endian format characters
- [ ] Where CRC is calculated vs where it's placed in the packet
- [ ] Why validation must happen before processing

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Week 4: Physical Layer, Data Link Layer & Custom Protocols*
