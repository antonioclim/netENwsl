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


## Problem P6: UDP Sensor Datagram Builder

### Task

Create a function to build a 23-byte UDP sensor datagram with the structure:

```
┌─────────┬───────────┬─────────────┬──────────┬───────┐
│ Version │ Sensor ID │ Temperature │ Location │ CRC32 │
│ 1B      │ 4B        │ 4B (float)  │ 10B      │ 4B    │
└─────────┴───────────┴─────────────┴──────────┴───────┘
```

### Scrambled Blocks

```python
# Block A
def build_sensor_datagram(sensor_id: int, temp: float, location: str) -> bytes:

# Block B
    location_bytes = location.encode('utf-8').ljust(10)[:10]

# Block C
    payload = struct.pack('>BIf10s', VERSION, sensor_id, temp, location_bytes)

# Block D
    crc = zlib.crc32(payload) & 0xFFFFFFFF

# Block E
    return payload + struct.pack('>I', crc)

# Block F (DISTRACTOR - wrong byte order)
    payload = struct.pack('<BIf10s', VERSION, sensor_id, temp, location_bytes)

# Block G (DISTRACTOR - CRC before payload)
    return struct.pack('>I', crc) + payload

# Block H (DISTRACTOR - location not padded)
    location_bytes = location.encode('utf-8')
```

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block A
def build_sensor_datagram(sensor_id: int, temp: float, location: str) -> bytes:

# Block B
    location_bytes = location.encode('utf-8').ljust(10)[:10]

# Block C
    payload = struct.pack('>BIf10s', VERSION, sensor_id, temp, location_bytes)

# Block D
    crc = zlib.crc32(payload) & 0xFFFFFFFF

# Block E
    return payload + struct.pack('>I', crc)
```

**Distractor explanations:**
- **Block F** uses little-endian (`<`) instead of network byte order (`>`)
- **Block G** places CRC at the start instead of end
- **Block H** doesn't pad/truncate location to exactly 10 bytes

**Key insight:** Network protocols use big-endian (network byte order). Fixed-size fields must be padded/truncated.

</details>

---

## Problem P7: TCP Connection State Machine

### Task

Reorder the blocks to implement a basic TCP-like connection establishment (simplified 3-way handshake simulation).

### Scrambled Blocks

```python
# Block A
def establish_connection(sock: socket.socket, server_addr: tuple) -> bool:

# Block B
    sock.settimeout(5.0)

# Block C
    syn_packet = build_packet(SYN, seq=1000, ack=0)
    sock.sendto(syn_packet, server_addr)

# Block D
    response, addr = sock.recvfrom(1024)
    if not is_syn_ack(response):
        return False

# Block E
    server_seq = get_sequence(response)
    ack_packet = build_packet(ACK, seq=1001, ack=server_seq + 1)
    sock.sendto(ack_packet, server_addr)

# Block F
    return True

# Block G (DISTRACTOR - wrong order)
    ack_packet = build_packet(ACK, seq=1001, ack=server_seq)

# Block H (DISTRACTOR - missing timeout)
    response = sock.recv(1024)
```

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block A
def establish_connection(sock: socket.socket, server_addr: tuple) -> bool:

# Block B
    sock.settimeout(5.0)

# Block C
    syn_packet = build_packet(SYN, seq=1000, ack=0)
    sock.sendto(syn_packet, server_addr)

# Block D
    response, addr = sock.recvfrom(1024)
    if not is_syn_ack(response):
        return False

# Block E
    server_seq = get_sequence(response)
    ack_packet = build_packet(ACK, seq=1001, ack=server_seq + 1)
    sock.sendto(ack_packet, server_addr)

# Block F
    return True
```

**Distractor explanations:**
- **Block G** doesn't add 1 to server sequence for ACK (ACK must be seq+1)
- **Block H** uses `recv()` without capturing sender address (needed for UDP)

**Key insight:** In TCP handshake, the ACK number is always the received sequence number + 1.

</details>

---

## Problem P8: Sliding Window Sender

### Task

Implement a simplified sliding window protocol sender that manages outstanding frames.

### Scrambled Blocks

```python
# Block A
class SlidingWindowSender:
    def __init__(self, window_size: int = 4):
        self.window_size = window_size
        self.base = 0
        self.next_seq = 0
        self.buffer = {}

# Block B
    def can_send(self) -> bool:
        return self.next_seq < self.base + self.window_size

# Block C
    def send_frame(self, data: bytes, sock: socket.socket, addr: tuple):
        if not self.can_send():
            return False

# Block D
        frame = build_frame(self.next_seq, data)
        self.buffer[self.next_seq] = (frame, time.time())
        sock.sendto(frame, addr)

# Block E
        self.next_seq += 1
        return True

# Block F
    def acknowledge(self, ack_num: int):
        while self.base <= ack_num:
            self.buffer.pop(self.base, None)
            self.base += 1

# Block G (DISTRACTOR - no window check)
    def send_frame(self, data: bytes, sock: socket.socket, addr: tuple):
        frame = build_frame(self.next_seq, data)

# Block H (DISTRACTOR - wrong ACK handling)
    def acknowledge(self, ack_num: int):
        self.buffer.pop(ack_num, None)
```

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block A - Class definition with state
# Block B - Window availability check
# Block C - Send with window check
# Block D - Build and buffer frame
# Block E - Increment sequence
# Block F - Cumulative ACK handling
```

**Distractor explanations:**
- **Block G** sends without checking window—will overflow receiver
- **Block H** only removes single frame—cumulative ACKs acknowledge all frames up to ack_num

**Key insight:** Cumulative acknowledgements mean "I've received everything up to this sequence number."

</details>

---

## Problem P9: Protocol Multiplexer

### Task

Create a server that handles multiple protocol types on the same port by examining the first bytes.

### Scrambled Blocks

```python
# Block A
def handle_connection(sock: socket.socket):
    data = recv_exact(sock, 2)  # Peek at magic bytes

# Block B
    if data == b'NP':
        return handle_binary_protocol(sock, data)

# Block C
    elif data[0:1].isdigit():
        return handle_text_protocol(sock, data)

# Block D
    elif data == b'{"':
        return handle_json_protocol(sock, data)

# Block E
    else:
        sock.send(b'ERROR: Unknown protocol\n')
        return False

# Block F (DISTRACTOR - wrong comparison)
    if data == 'NP':  # Missing b prefix

# Block G (DISTRACTOR - doesn't pass initial bytes)
    elif data[0:1].isdigit():
        return handle_text_protocol(sock)
```

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block A - Receive magic bytes
# Block B - Check binary protocol
# Block C - Check text protocol (starts with digit for length)
# Block D - Check JSON protocol
# Block E - Handle unknown
```

**Distractor explanations:**
- **Block F** compares bytes to string (type mismatch in Python 3)
- **Block G** doesn't pass the already-read bytes to handler (they'd be lost)

**Key insight:** Protocol multiplexing requires passing already-read bytes to handlers.

</details>

---

## Problem P10: Checksum vs CRC Comparison

### Task

Implement functions to compare simple checksum with CRC32 for error detection demonstration.

### Scrambled Blocks

```python
# Block A
def simple_checksum(data: bytes) -> int:
    return sum(data) & 0xFF

# Block B
def crc32_check(data: bytes) -> int:
    return zlib.crc32(data) & 0xFFFFFFFF

# Block C
def demonstrate_weakness():
    original = b'AB'
    swapped = b'BA'

# Block D
    checksum_orig = simple_checksum(original)
    checksum_swap = simple_checksum(swapped)
    print(f"Checksum detects swap: {checksum_orig != checksum_swap}")

# Block E
    crc_orig = crc32_check(original)
    crc_swap = crc32_check(swapped)
    print(f"CRC32 detects swap: {crc_orig != crc_swap}")

# Block F (DISTRACTOR - wrong mask)
def crc32_check(data: bytes) -> int:
    return zlib.crc32(data) & 0xFF

# Block G (DISTRACTOR - wrong return type)
def simple_checksum(data: bytes) -> bytes:
    return bytes([sum(data) & 0xFF])
```

### Correct Order

<details>
<summary>Click to reveal</summary>

```python
# Block A - Simple checksum (8-bit)
# Block B - CRC32 check (32-bit)  
# Block C - Test setup
# Block D - Compare checksums
# Block E - Compare CRCs

# Output:
# Checksum detects swap: False  (A+B = B+A)
# CRC32 detects swap: True      (polynomial division is position-sensitive)
```

**Distractor explanations:**
- **Block F** masks to 8 bits, losing most of CRC32's error detection
- **Block G** returns bytes instead of int, breaking comparison

**Key insight:** Simple checksums use commutative addition (A+B=B+A), so byte swaps go undetected. CRC uses polynomial division which IS position-sensitive.

</details>

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
