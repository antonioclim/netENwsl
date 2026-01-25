# 🗳️ Peer Instruction Questions — Week 4

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

## Physical Layer, Data Link Layer & Custom Protocols

---

## Peer Instruction Protocol (5 steps)

Each question follows **5 mandatory steps**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 1 (1 min)  │  Read the question and think individually               │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 2 (30 sec) │  Vote your answer (A/B/C/D) — no discussion!            │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 3 (2 min)  │  Discuss with your neighbour — convince them!           │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 4 (30 sec) │  Re-vote — you may change your answer                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 5 (2 min)  │  Instructor explains the correct answer                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Question 1: TCP Message Boundaries

> 💭 **PREDICTION:** Before reading the scenario, predict: Does TCP preserve message boundaries between send() calls?

### Scenario

A client sends two messages to a TCP server:

```python
# Client code
sock.send(b"HELLO")
sock.send(b"WORLD")
```

The server receives data with:

```python
# Server code
data = sock.recv(1024)
print(data)
```

### Question

What will the server's `print(data)` statement most likely display?

### Options

- **A)** `b"HELLO"` then `b"WORLD"` in two separate recv() calls — *Misconception: TCP preserves message boundaries*
- **B)** `b"HELLOWORLD"` in a single recv() call — **CORRECT**
- **C)** `b"HELLO WORLD"` with an automatic space separator — *Misconception: TCP adds delimiters*
- **D)** An error because two sends require two receives — *Misconception: send/recv are 1:1 mapped*

### Correct Answer

**B** — TCP is a byte stream protocol. It does not preserve message boundaries. The two `send()` calls may be combined into a single TCP segment, or split differently. The receiver sees a continuous stream of bytes with no indication where one "message" ends and another begins.

### Targeted Misconception

**"TCP preserves message boundaries"** — Students often assume that each `send()` corresponds to exactly one `recv()`. This is false. TCP treats data as an unstructured byte stream. Applications must implement their own framing (length-prefix, delimiter, or fixed-size messages) to identify message boundaries.

### Instructor Notes

- **Target accuracy:** 30-50% on first vote (common misconception)
- **Key concept:** TCP byte stream vs UDP datagrams
- **After discussion:** Show Wireshark capture demonstrating segment coalescence
- **Follow-up:** "How would you fix this?" → introduce length-prefix framing

---

## Question 2: Binary Protocol Endianness

> 💭 **PREDICTION:** What byte sequence represents the number 1000 in big-endian format?

### Scenario

You need to send the integer value `1000` (decimal) as a 2-byte unsigned integer in network byte order (big-endian):

```python
import struct
packed = struct.pack('>H', 1000)
print(packed.hex())
```

### Question

What hexadecimal output will be printed?

### Options

- **A)** `e803` — *Misconception: Using little-endian (x86 native) order*
- **B)** `03e8` — **CORRECT**
- **C)** `1000` — *Misconception: Decimal string, not binary*
- **D)** `00001000` — *Misconception: Binary representation as string*

### Correct Answer

**B** — `1000` decimal = `0x03E8` hexadecimal. In big-endian (network byte order), the most significant byte (`03`) comes first, followed by the least significant byte (`E8`). The format `'>H'` means big-endian (`>`) unsigned short (`H`, 2 bytes).

### Targeted Misconception

**"Little-endian and big-endian are interchangeable"** — Students often forget that x86 processors use little-endian natively, whilst network protocols use big-endian. Option A (`e803`) is what you would get with `'<H'` (little-endian). This mismatch causes protocol bugs when communicating between systems.

### Instructor Notes

- **Target accuracy:** 40-60% on first vote
- **Key concept:** Network byte order is ALWAYS big-endian
- **Live demo:** Show both `struct.pack('>H', 1000)` and `struct.pack('<H', 1000)`
- **Real-world impact:** Explain why mismatched endianness causes values like 1000 to become 59395

---

## Question 3: CRC32 vs Checksum

> 💭 **PREDICTION:** If a single bit flips in transmitted data, will CRC32 always detect it?

### Scenario

A binary protocol uses CRC32 for error detection:

```python
import zlib

original_data = b"Hello, Network!"
crc = zlib.crc32(original_data)
print(f"Original CRC: {crc:#010x}")

# Simulate single bit error
corrupted_data = bytes([original_data[0] ^ 0x01]) + original_data[1:]
corrupted_crc = zlib.crc32(corrupted_data)
print(f"Corrupted CRC: {corrupted_crc:#010x}")
```

### Question

What is TRUE about CRC32 error detection?

### Options

- **A)** CRC32 detects AND corrects single-bit errors — *Misconception: CRC detects only, ECC corrects*
- **B)** CRC32 guarantees detection of all possible errors — *Misconception: No error detection is 100%*
- **C)** CRC32 detects all single-bit, double-bit and burst errors up to 32 bits — **CORRECT**
- **D)** CRC32 is identical to a simple checksum but faster — *Misconception: Different mathematical basis*

### Correct Answer

**C** — CRC32 is mathematically guaranteed to detect: all single-bit errors, all double-bit errors, all odd numbers of bit errors and all burst errors of 32 bits or fewer. For longer bursts, detection probability is 99.99999998%. However, CRC detects errors but cannot correct them.

### Targeted Misconception

**"CRC guarantees data integrity"** — CRC detects transmission errors with very high probability, but it does NOT guarantee integrity against malicious modification (use cryptographic hashes for that) and does NOT correct errors (use ECC for that). Also, identical CRCs do not prove data is identical (though collisions are rare).

### Instructor Notes

- **Target accuracy:** 35-55% on first vote
- **Key concept:** Detection vs correction, CRC vs cryptographic hash
- **Demo:** Calculate CRC of original and corrupted data, show they differ
- **Extension:** When would you use SHA-256 instead of CRC32?

---

## Question 4: Length-Prefix Framing

> 💭 **PREDICTION:** How many bytes total are needed to send the message "HELLO" using 2-byte length-prefix framing?

### Scenario

Your TEXT protocol uses length-prefix framing:

```
┌──────────────┬─────────────────────┐
│ Length (2B)  │ Payload (N bytes)   │
└──────────────┴─────────────────────┘
```

You want to send the ASCII message `"SET key value"` (13 characters).

### Question

What is the complete frame that should be transmitted?

### Options

- **A)** `b'\x00\x0dSET key value'` — **CORRECT**
- **B)** `b'13 SET key value'` — *Misconception: Length as ASCII text, not binary*
- **C)** `b'\x0d\x00SET key value'` — *Misconception: Little-endian length field*
- **D)** `b'SET key value\x00\x0d'` — *Misconception: Length at end, not beginning*

### Correct Answer

**A** — The length field is 2 bytes in big-endian format. 13 decimal = `0x000D`. In big-endian, this is `\x00\x0d`. The complete frame is the 2-byte length prefix followed by the 13-byte payload, totalling 15 bytes.

### Targeted Misconception

**"Length prefix should be human-readable"** — Students sometimes encode the length as ASCII digits (like "13") instead of binary. This wastes bytes and complicates parsing. Binary length fields have fixed size (2 or 4 bytes) regardless of the value, making parsing predictable.

### Instructor Notes

- **Target accuracy:** 45-65% on first vote
- **Key concept:** Binary framing efficiency
- **Calculation:** 2 (length) + 13 (payload) = 15 bytes total
- **Comparison:** ASCII "13" = 2 bytes, binary 13 = 2 bytes (same here, but "1000" = 4 bytes ASCII vs 2 bytes binary)

---

## Question 5: Binary vs Text Protocol Overhead

> 💭 **PREDICTION:** Which protocol type has less overhead for transmitting the number 1000000?

### Scenario

You need to transmit a key-value pair where the value is the integer `1000000`.

**Text protocol:**
```
SET counter 1000000\r\n
```

**Binary protocol (simplified):**
```
┌────────┬─────────┬───────────┐
│ Type   │ Key_len │ Key       │ Value (4B int) │
│ 1 byte │ 1 byte  │ 7 bytes   │ 4 bytes        │
└────────┴─────────┴───────────┴────────────────┘
```

### Question

Which statement about protocol overhead is CORRECT?

### Options

- **A)** Text protocols always have more overhead than binary — *Misconception: Depends on data type and size*
- **B)** Binary protocols are always faster to parse — *Misconception: Text parsing can be optimised*
- **C)** For this example, binary uses 13 bytes vs text's 20 bytes — **CORRECT**
- **D)** The overhead difference is negligible for modern networks — *Misconception: Matters at scale*

### Correct Answer

**C** — Text: "SET counter 1000000\r\n" = 20 bytes. Binary: 1 (type) + 1 (key_len) + 7 (key) + 4 (value) = 13 bytes. The binary protocol saves 35% bandwidth. For bulk data transfer or high-frequency updates, this difference compounds significantly.

### Targeted Misconception

**"Binary protocols are always better"** — While binary is more compact for numeric data, text protocols offer advantages: human-readable (easier debugging), self-documenting, simpler to implement and work with standard tools (telnet, curl). The choice depends on requirements: high-volume sensor data favours binary; configuration APIs often use text/JSON.

### Instructor Notes

- **Target accuracy:** 50-70% on first vote
- **Key concept:** Trade-offs in protocol design
- **Discussion prompt:** "When would you choose text over binary?"
- **Real examples:** HTTP/1.1 (text) vs HTTP/2 (binary framing)

---


## Question 6: CRC32 Error Detection Limits

> 💭 **PREDICTION:** If two bytes in a message are swapped, will CRC32 detect the error?

### Scenario

A sensor sends a UDP datagram with CRC32 integrity check. During transmission, a network device accidentally swaps two adjacent bytes:

```python
# Original message
original = b'\x01\x00\x00\x2A\x41\x98\x00\x00'  # sensor_id=42, temp=19.0

# Corrupted (bytes at positions 3 and 4 swapped)
corrupted = b'\x01\x00\x00\x41\x2A\x98\x00\x00'  # sensor_id=??, temp=??

original_crc = zlib.crc32(original) & 0xFFFFFFFF
corrupted_crc = zlib.crc32(corrupted) & 0xFFFFFFFF
```

### Question

What will happen when the receiver validates the corrupted message?

### Options

- **A)** CRC will match because byte swaps preserve the sum — *Misconception: CRC uses polynomial division, not simple sums*
- **B)** CRC will detect the error because any change affects the polynomial remainder — **CORRECT**
- **C)** CRC might or might not detect it, depending on which bytes were swapped — *Misconception: CRC32 detects all 2-byte changes*
- **D)** CRC only detects single-bit errors, not byte-level corruption — *Misconception: CRC detects burst errors up to its length*

### Correct Answer

**B** — CRC32 uses polynomial division, not simple addition. Unlike a checksum where swapping bytes might preserve the sum, CRC detects byte transpositions because the position of each byte affects the polynomial remainder differently. CRC32 detects all single-bit errors, all double-bit errors, all odd-number-of-bit errors and all burst errors up to 32 bits.

### Targeted Misconception

**"CRC is just a fancy checksum"** — Students often confuse CRC with simple checksums. A basic checksum (sum of bytes mod 256) would NOT detect byte swaps because addition is commutative. CRC's polynomial division makes it position-sensitive, catching transposition errors that checksums miss.

### Instructor Notes

- **Target accuracy:** 40-60% on first vote (many confuse CRC with checksum)
- **Key concept:** CRC uses polynomial division, not addition
- **Live demo:** Run the Python code above to show different CRC values
- **Follow-up:** Compare `zlib.crc32(b'AB')` vs `zlib.crc32(b'BA')` — different values prove position matters

---

## Summary: Key Misconceptions Targeted

| Question | Primary Misconception |
|----------|----------------------|
| Q1 | TCP preserves message boundaries |
| Q2 | Endianness doesn't matter / is automatic |
| Q3 | CRC guarantees integrity / corrects errors |
| Q4 | Length fields should be human-readable |
| Q5 | Binary protocols are always superior |
| Q6 | CRC is just a checksum / detects only bit flips |

---

## Additional Discussion Questions

For extended sessions, consider these follow-up questions:

1. **Q1 Follow-up:** How would you implement length-prefix framing to solve the boundary problem?
2. **Q2 Follow-up:** What happens if client uses big-endian and server expects little-endian?
3. **Q3 Follow-up:** When would you use SHA-256 instead of CRC32?
4. **Q4 Follow-up:** What are the pros/cons of delimiter-based framing vs length-prefix?
5. **Q5 Follow-up:** Why does HTTP/2 use binary framing when HTTP/1.1 was text-based?

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Week 4: Physical Layer, Data Link Layer & Custom Protocols*
