# 🔍 Code Tracing Exercises — Week 9
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Trace through the code mentally before running it.

These exercises develop your ability to predict binary encoding behaviour — a critical skill for debugging network protocols.

---

## How to Use These Exercises

1. **Read** the code carefully
2. **Predict** the output WITHOUT running the code
3. **Fill in** the tracking tables
4. **Check** your answers using the hidden solutions
5. **Run** the code to verify

---

## Exercise T1: Endianness Byte Tracing

### Code

```python
import struct

value = 0xCAFEBABE

# Pack in different byte orders
be_bytes = struct.pack(">I", value)
le_bytes = struct.pack("<I", value)
native_bytes = struct.pack("=I", value)

# Print each byte
print("Big-endian:    ", end="")
for b in be_bytes:
    print(f"0x{b:02X} ", end="")
print()

print("Little-endian: ", end="")
for b in le_bytes:
    print(f"0x{b:02X} ", end="")
print()

# Unpack with WRONG byte order
wrong_value = struct.unpack("<I", be_bytes)[0]
print(f"\nBE bytes unpacked as LE: 0x{wrong_value:08X}")
```

### Questions

1. **Byte values:** What are the 4 bytes for big-endian packing?
2. **Byte values:** What are the 4 bytes for little-endian packing?
3. **Wrong unpack:** What value results from unpacking BE data with LE format?

### Prediction Table

| Variable | Your Prediction |
|----------|-----------------|
| `be_bytes[0]` | |
| `be_bytes[1]` | |
| `be_bytes[2]` | |
| `be_bytes[3]` | |
| `le_bytes[0]` | |
| `le_bytes[1]` | |
| `le_bytes[2]` | |
| `le_bytes[3]` | |
| `wrong_value` | |

### Solution

<details>
<summary>Click to reveal</summary>

**Value breakdown:** 0xCAFEBABE = bytes CA, FE, BA, BE

| Variable | Value | Explanation |
|----------|-------|-------------|
| `be_bytes[0]` | 0xCA | MSB first (big-endian) |
| `be_bytes[1]` | 0xFE | |
| `be_bytes[2]` | 0xBA | |
| `be_bytes[3]` | 0xBE | LSB last |
| `le_bytes[0]` | 0xBE | LSB first (little-endian) |
| `le_bytes[1]` | 0xBA | |
| `le_bytes[2]` | 0xFE | |
| `le_bytes[3]` | 0xCA | MSB last |
| `wrong_value` | 0xBEBAFECA | Bytes read in reverse order! |

**Output:**
```
Big-endian:    0xCA 0xFE 0xBA 0xBE 
Little-endian: 0xBE 0xBA 0xFE 0xCA 

BE bytes unpacked as LE: 0xBEBAFECA
```

**Key insight:** Using the wrong byte order gives a completely different number. This is a common source of bugs in network protocols!

</details>

---

## Exercise T2: Protocol Header Packing

### Code

```python
import struct
import zlib

# Header format: magic(2s) + version(B) + flags(B) + length(I) + crc(I)
HEADER_FORMAT = ">2sBBII"

payload = b"Hello"
magic = b"S9"
version = 1
flags = 0x03  # bits 0 and 1 set

# Calculate values
length = len(payload)
crc = zlib.crc32(payload) & 0xFFFFFFFF

# Pack header
header = struct.pack(HEADER_FORMAT, magic, version, flags, length, crc)

# Print header info
print(f"Header size: {len(header)} bytes")
print(f"Payload size: {length} bytes")
print(f"Total message: {len(header) + length} bytes")

# Print header bytes
print("\nHeader bytes:")
for i, b in enumerate(header):
    print(f"  byte[{i:2d}] = 0x{b:02X} ({b:3d})")

# Unpack and verify
m, v, f, l, c = struct.unpack(HEADER_FORMAT, header)
print(f"\nUnpacked: magic={m}, version={v}, flags=0x{f:02X}, length={l}, crc=0x{c:08X}")
```

### Questions

1. **Size calculation:** What is `struct.calcsize(">2sBBII")`?
2. **Byte positions:** Which bytes contain the magic value?
3. **Byte positions:** Which bytes contain the length field?
4. **CRC value:** What is `zlib.crc32(b"Hello") & 0xFFFFFFFF`?

### Prediction Table

Complete the header byte values:

| Byte Index | Field | Your Prediction |
|------------|-------|-----------------|
| 0 | magic[0] | |
| 1 | magic[1] | |
| 2 | version | |
| 3 | flags | |
| 4 | length[0] (MSB) | |
| 5 | length[1] | |
| 6 | length[2] | |
| 7 | length[3] (LSB) | |
| 8-11 | crc32 | (calculate or look up) |

### Solution

<details>
<summary>Click to reveal</summary>

**Header size:** 2 + 1 + 1 + 4 + 4 = **12 bytes**

**CRC-32 of "Hello":** 0xF7D18982

| Byte Index | Field | Value | Explanation |
|------------|-------|-------|-------------|
| 0 | magic[0] | 0x53 | 'S' = 83 = 0x53 |
| 1 | magic[1] | 0x39 | '9' = 57 = 0x39 |
| 2 | version | 0x01 | version = 1 |
| 3 | flags | 0x03 | flags = 3 |
| 4 | length[0] | 0x00 | 5 in big-endian: 00 00 00 05 |
| 5 | length[1] | 0x00 | |
| 6 | length[2] | 0x00 | |
| 7 | length[3] | 0x05 | LSB = 5 |
| 8 | crc[0] | 0xF7 | 0xF7D18982 in big-endian |
| 9 | crc[1] | 0xD1 | |
| 10 | crc[2] | 0x89 | |
| 11 | crc[3] | 0x82 | |

**Output:**
```
Header size: 12 bytes
Payload size: 5 bytes
Total message: 17 bytes

Header bytes:
  byte[ 0] = 0x53 ( 83)
  byte[ 1] = 0x39 ( 57)
  byte[ 2] = 0x01 (  1)
  byte[ 3] = 0x03 (  3)
  byte[ 4] = 0x00 (  0)
  byte[ 5] = 0x00 (  0)
  byte[ 6] = 0x00 (  0)
  byte[ 7] = 0x05 (  5)
  byte[ 8] = 0xF7 (247)
  byte[ 9] = 0xD1 (209)
  byte[10] = 0x89 (137)
  byte[11] = 0x82 (130)

Unpacked: magic=b'S9', version=1, flags=0x03, length=5, crc=0xF7D18982
```

</details>

---

## Exercise T3: FTP PASV Response Parsing

### Code

```python
def parse_pasv_response(response: str) -> tuple:
    """Parse FTP PASV response to extract IP and port."""
    
    # Step 1: Find parentheses
    start = response.index("(")
    end = response.index(")")
    
    # Step 2: Extract and split
    inner = response[start + 1:end]
    parts = inner.split(",")
    
    # Step 3: Build IP address
    ip = f"{parts[0]}.{parts[1]}.{parts[2]}.{parts[3]}"
    
    # Step 4: Calculate port
    p1 = int(parts[4])
    p2 = int(parts[5])
    port = p1 * 256 + p2
    
    return ip, port

# Test cases
responses = [
    "227 Entering Passive Mode (192,168,1,5,234,100)",
    "227 Entering Passive Mode (10,0,0,1,0,21)",
    "227 Entering Passive Mode (172,29,9,10,195,88)",
]

for resp in responses:
    ip, port = parse_pasv_response(resp)
    print(f"Response: {resp}")
    print(f"  → IP: {ip}, Port: {port}")
    print()
```

### Questions

For each response, calculate the port number:

1. `(192,168,1,5,234,100)` → Port = ?
2. `(10,0,0,1,0,21)` → Port = ?
3. `(172,29,9,10,195,88)` → Port = ?

### Prediction Table

| Response | p1 | p2 | Calculation | Port |
|----------|----|----|-------------|------|
| Response 1 | 234 | 100 | 234 × 256 + 100 = | |
| Response 2 | 0 | 21 | 0 × 256 + 21 = | |
| Response 3 | 195 | 88 | 195 × 256 + 88 = | |

### Solution

<details>
<summary>Click to reveal</summary>

| Response | p1 | p2 | Calculation | Port |
|----------|----|----|-------------|------|
| Response 1 | 234 | 100 | 234 × 256 + 100 = 59904 + 100 | **60004** |
| Response 2 | 0 | 21 | 0 × 256 + 21 = 0 + 21 | **21** |
| Response 3 | 195 | 88 | 195 × 256 + 88 = 49920 + 88 | **50008** |

**Output:**
```
Response: 227 Entering Passive Mode (192,168,1,5,234,100)
  → IP: 192.168.1.5, Port: 60004

Response: 227 Entering Passive Mode (10,0,0,1,0,21)
  → IP: 10.0.0.1, Port: 21

Response: 227 Entering Passive Mode (172,29,9,10,195,88)
  → IP: 172.29.9.10, Port: 50008
```

**Key insight:** The port encoding allows ports 0-65535 using two bytes:
- p1 = port // 256 (high byte)
- p2 = port % 256 (low byte)
- port = p1 × 256 + p2

</details>

---

## Bonus Exercise T4: CRC Corruption Detection

### Code

```python
import zlib

def demonstrate_crc_detection():
    original = b"Transfer $100 to Alice"
    
    # Calculate original CRC
    crc_original = zlib.crc32(original) & 0xFFFFFFFF
    
    # Create corrupted versions
    corrupted1 = b"Transfer $100 to Bob"      # Different name
    corrupted2 = b"Transfer $900 to Alice"    # Different amount
    corrupted3 = bytearray(original)
    corrupted3[10] ^= 0x01                    # Single bit flip
    corrupted3 = bytes(corrupted3)
    
    # Calculate CRCs
    crc1 = zlib.crc32(corrupted1) & 0xFFFFFFFF
    crc2 = zlib.crc32(corrupted2) & 0xFFFFFFFF
    crc3 = zlib.crc32(corrupted3) & 0xFFFFFFFF
    
    print(f"Original: '{original.decode()}'")
    print(f"  CRC: 0x{crc_original:08X}")
    print()
    print(f"Corrupted 1: '{corrupted1.decode()}'")
    print(f"  CRC: 0x{crc1:08X}, Match: {crc1 == crc_original}")
    print()
    print(f"Corrupted 2: '{corrupted2.decode()}'")
    print(f"  CRC: 0x{crc2:08X}, Match: {crc2 == crc_original}")
    print()
    print(f"Corrupted 3: (bit flip at position 10)")
    print(f"  CRC: 0x{crc3:08X}, Match: {crc3 == crc_original}")

demonstrate_crc_detection()
```

### Questions

1. Will ANY of the corrupted versions match the original CRC?
2. Does CRC-32 detect single-bit errors?
3. Could an attacker create a message with the SAME CRC as the original?

### Solution

<details>
<summary>Click to reveal</summary>

**Answers:**

1. **No** — All corrupted versions will have different CRCs
2. **Yes** — CRC-32 is specifically designed to detect single-bit errors
3. **Yes** — An attacker can create a message that produces any desired CRC (CRC is not cryptographically secure)

**Output:**
```
Original: 'Transfer $100 to Alice'
  CRC: 0x8B5C4E8A

Corrupted 1: 'Transfer $100 to Bob'
  CRC: 0x4A8E5D21, Match: False

Corrupted 2: 'Transfer $900 to Alice'
  CRC: 0xE3C27B19, Match: False

Corrupted 3: (bit flip at position 10)
  CRC: 0x7F2A1BC4, Match: False
```

**Key insight:** CRC-32 detects accidental errors extremely well but provides ZERO security against intentional tampering. An attacker who controls the data can always recalculate the CRC.

</details>

---

## Self-Assessment

After completing these exercises, you should be able to:

- [ ] Predict byte sequences for big-endian and little-endian packing
- [ ] Calculate struct sizes and identify field positions
- [ ] Parse FTP PASV responses manually
- [ ] Explain why CRC detects errors but not attacks

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Week 9: Session Layer and Presentation Layer*
