# 🔍 Code Tracing Exercises — Week 4

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

## Physical Layer, Data Link Layer & Custom Protocols

Trace through the code mentally before running it. Write down your predictions, then verify.

---

## Exercise T1: struct.pack Byte Order

### Code

```python
import struct

# Pack the value 1000 in different byte orders
value = 1000

big_endian = struct.pack('>H', value)
little_endian = struct.pack('<H', value)

print(f"Big-endian:    {big_endian.hex()}")
print(f"Little-endian: {little_endian.hex()}")

# What if we unpack with wrong endianness?
wrong = struct.unpack('>H', little_endian)[0]
print(f"Wrong unpack:  {wrong}")
```

### Questions

1. **Hex conversion:** What is 1000 in hexadecimal?
2. **Big-endian output:** What bytes will `big_endian.hex()` print?
3. **Little-endian output:** What bytes will `little_endian.hex()` print?
4. **Wrong unpack:** What decimal value will `wrong` contain?

### Trace Table

| Step | Variable | Value |
|------|----------|-------|
| value | int | 1000 |
| 1000 in hex | — | ? |
| big_endian | bytes | ? |
| little_endian | bytes | ? |
| wrong | int | ? |

### Solution

<details>
<summary>Click to reveal</summary>

| Step | Variable | Value |
|------|----------|-------|
| value | int | 1000 |
| 1000 in hex | — | 0x03E8 |
| big_endian | bytes | b'\x03\xe8' → "03e8" |
| little_endian | bytes | b'\xe8\x03' → "e803" |
| wrong | int | 59395 |

**Output:**
```
Big-endian:    03e8
Little-endian: e803
Wrong unpack:  59395
```

**Explanation:** 
- 1000 decimal = 0x03E8 hex
- Big-endian: MSB first → 03 E8
- Little-endian: LSB first → E8 03
- Reading E8 03 as big-endian: 0xE803 = 59395

</details>

---

## Exercise T2: CRC32 Calculation

### Code

```python
import zlib

data = b"Hello"
crc = zlib.crc32(data)

print(f"Data: {data}")
print(f"CRC:  {crc}")
print(f"Hex:  {crc:#010x}")

# Append more data
data2 = b"Hello, World!"
crc2 = zlib.crc32(data2)

# Incremental calculation (same result)
crc_incremental = zlib.crc32(b", World!", crc)

print(f"\nFull CRC:        {crc2:#010x}")
print(f"Incremental CRC: {crc_incremental:#010x}")
print(f"Match: {crc2 == crc_incremental}")
```

### Questions

1. **CRC type:** What Python type does `zlib.crc32()` return?
2. **CRC range:** What is the range of possible CRC32 values?
3. **Incremental:** Will `crc2` and `crc_incremental` be equal?
4. **Prediction:** If we change "Hello" to "hello", will CRC change?

### Trace Table

| Variable | Type | Approximate Value |
|----------|------|-------------------|
| data | bytes | b"Hello" |
| crc | ? | ? |
| crc2 | int | ? |
| crc_incremental | int | ? |
| Match | bool | ? |

### Solution

<details>
<summary>Click to reveal</summary>

| Variable | Type | Value |
|----------|------|-------|
| data | bytes | b"Hello" |
| crc | int | 4157704578 |
| crc (hex) | — | 0xf7d18982 |
| crc2 | int | 3964322768 |
| crc_incremental | int | 3964322768 |
| Match | bool | True |

**Output:**
```
Data: b'Hello'
CRC:  4157704578
Hex:  0xf7d18982

Full CRC:        0xec4ac3d0
Incremental CRC: 0xec4ac3d0
Match: True
```

**Explanation:**
- `zlib.crc32()` returns an unsigned 32-bit integer (0 to 4294967295)
- The second parameter allows incremental calculation
- Changing any bit in input changes the CRC completely

</details>

---

## Exercise T3: Length-Prefix Framing

### Code

```python
def frame_message(payload: bytes) -> bytes:
    """Create a length-prefixed frame."""
    length = len(payload)
    length_bytes = length.to_bytes(2, 'big')
    return length_bytes + payload

def parse_frame(frame: bytes) -> tuple:
    """Parse a length-prefixed frame."""
    length = int.from_bytes(frame[:2], 'big')
    payload = frame[2:2+length]
    return length, payload

# Test
message = b"SET key value"
frame = frame_message(message)

print(f"Original:  {message}")
print(f"Frame hex: {frame.hex()}")
print(f"Frame len: {len(frame)}")

parsed_len, parsed_payload = parse_frame(frame)
print(f"Parsed:    {parsed_len}, {parsed_payload}")
```

### Questions

1. **Message length:** How many bytes is "SET key value"?
2. **Length bytes:** What hex bytes represent this length in big-endian?
3. **Total frame:** How many bytes is the complete frame?
4. **Frame hex:** What will `frame.hex()` output? (first 4 characters + ...)

### Trace Table

| Step | Value |
|------|-------|
| message length | ? bytes |
| length in hex (big-endian) | ? |
| frame total length | ? bytes |
| frame[:4].hex() | ? |
| parsed_len | ? |

### Solution

<details>
<summary>Click to reveal</summary>

| Step | Value |
|------|-------|
| message length | 13 bytes |
| length in hex (big-endian) | 000d |
| frame total length | 15 bytes (2 + 13) |
| frame[:4].hex() | 000d5345 |
| parsed_len | 13 |

**Output:**
```
Original:  b'SET key value'
Frame hex: 000d534554206b65792076616c7565
Frame len: 15
Parsed:    13, b'SET key value'
```

**Breakdown:**
- `00 0d` = length 13 in big-endian
- `53 45 54 20` = "SET " in ASCII
- `6b 65 79 20` = "key "
- `76 61 6c 75 65` = "value"

</details>

---

## Exercise T4: Binary Header Construction

### Code

```python
import struct
import zlib

MAGIC = b'NP'
VERSION = 1

def build_header(msg_type: int, payload: bytes, seq: int) -> bytes:
    """Build 14-byte binary header with CRC32."""
    payload_len = len(payload)
    
    # Pack header without CRC (10 bytes)
    header_no_crc = struct.pack('>2sBBHI',
                                 MAGIC, VERSION, msg_type, payload_len, seq)
    
    # Calculate CRC over header + payload
    crc = zlib.crc32(header_no_crc + payload) & 0xFFFFFFFF
    
    # Pack complete header with CRC (14 bytes)
    header = struct.pack('>2sBBHII',
                         MAGIC, VERSION, msg_type, payload_len, seq, crc)
    
    return header

# Build header for ECHO request (type=1) with payload "Hi"
header = build_header(msg_type=1, payload=b"Hi", seq=42)

print(f"Header length: {len(header)}")
print(f"Header hex:    {header.hex()}")

# Parse it back
magic, ver, typ, plen, seq, crc = struct.unpack('>2sBBHII', header)
print(f"\nParsed:")
print(f"  Magic:   {magic}")
print(f"  Version: {ver}")
print(f"  Type:    {typ}")
print(f"  Length:  {plen}")
print(f"  Seq:     {seq}")
print(f"  CRC:     {crc:#010x}")
```

### Questions

1. **Header size:** Verify that 2+1+1+2+4+4 = 14 bytes
2. **Magic bytes:** What hex values represent 'NP'?
3. **Payload length:** What is `plen` for payload b"Hi"?
4. **Seq bytes:** How is 42 represented in 4 bytes big-endian?

### Trace Table

| Field | Size | Hex Value |
|-------|------|-----------|
| Magic | 2B | ? |
| Version | 1B | ? |
| Type | 1B | ? |
| PayloadLen | 2B | ? |
| Seq | 4B | ? |
| CRC | 4B | (calculated) |

### Solution

<details>
<summary>Click to reveal</summary>

| Field | Size | Hex Value |
|-------|------|-----------|
| Magic | 2B | 4e50 ('NP') |
| Version | 1B | 01 |
| Type | 1B | 01 |
| PayloadLen | 2B | 0002 |
| Seq | 4B | 0000002a (42) |
| CRC | 4B | (varies) |

**Output:**
```
Header length: 14
Header hex:    4e50010100020000002a[8 hex digits for CRC]

Parsed:
  Magic:   b'NP'
  Version: 1
  Type:    1
  Length:  2
  Seq:     42
  CRC:     0x[calculated]
```

**Byte breakdown:**
- `4e 50` = 'N' 'P' in ASCII
- `01` = version 1
- `01` = type 1 (ECHO)
- `00 02` = payload length 2
- `00 00 00 2a` = sequence 42 in big-endian
- `[4 bytes]` = CRC32

</details>

---

## Exercise T5: TCP Receive Loop

### Code

```python
def recv_exact(sock, n: int) -> bytes:
    """Receive exactly n bytes from socket."""
    data = b''
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Connection closed")
        data += chunk
        print(f"  Received chunk: {len(chunk)} bytes, total: {len(data)}/{n}")
    return data

# Simulate fragmented receives
class FakeSocket:
    def __init__(self, data: bytes, chunk_sizes: list):
        self.data = data
        self.chunk_sizes = chunk_sizes
        self.pos = 0
        self.chunk_idx = 0
    
    def recv(self, max_bytes: int) -> bytes:
        if self.pos >= len(self.data):
            return b''
        chunk_size = min(self.chunk_sizes[self.chunk_idx], 
                         max_bytes, 
                         len(self.data) - self.pos)
        result = self.data[self.pos:self.pos + chunk_size]
        self.pos += chunk_size
        self.chunk_idx = (self.chunk_idx + 1) % len(self.chunk_sizes)
        return result

# Test: 10 bytes arriving in chunks of 3, 3, 4
fake = FakeSocket(b"HELLOWORLD", [3, 3, 4])
result = recv_exact(fake, 10)
print(f"\nFinal result: {result}")
```

### Questions

1. **Loop iterations:** How many times will the while loop execute?
2. **First chunk:** What will the first chunk contain?
3. **Second chunk:** After first chunk, how many bytes still needed?
4. **Final result:** What is the complete received data?

### Trace Table

| Iteration | chunk | len(data) | n - len(data) |
|-----------|-------|-----------|---------------|
| 1 | ? | ? | ? |
| 2 | ? | ? | ? |
| 3 | ? | ? | ? |

### Solution

<details>
<summary>Click to reveal</summary>

| Iteration | chunk | len(data) | n - len(data) |
|-----------|-------|-----------|---------------|
| 1 | b'HEL' (3) | 3 | 7 |
| 2 | b'LOW' (3) | 6 | 4 |
| 3 | b'ORLD' (4) | 10 | 0 (exit) |

**Output:**
```
  Received chunk: 3 bytes, total: 3/10
  Received chunk: 3 bytes, total: 6/10
  Received chunk: 4 bytes, total: 10/10

Final result: b'HELLOWORLD'
```

**Explanation:**
- Loop continues while `len(data) < n`
- Each recv gets up to `n - len(data)` bytes
- Socket returns chunks of 3, 3, 4 bytes
- After 3 iterations, we have all 10 bytes

</details>

---

## Self-Assessment

After completing these exercises, you should be able to:

- [ ] Convert decimal to hexadecimal manually
- [ ] Predict struct.pack output for any format string
- [ ] Calculate frame sizes including headers
- [ ] Trace through a receive loop with partial data
- [ ] Understand CRC32 calculation scope

**Challenge:** Create your own trace exercise for a classmate involving:
- A 16-byte header with different field types
- Incremental CRC calculation
- Parsing a fragmented message

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Week 4: Physical Layer, Data Link Layer & Custom Protocols*
