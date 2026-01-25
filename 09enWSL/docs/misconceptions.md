# ❌ Common Misconceptions — Week 9
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Session Layer (L5) and Presentation Layer (L6)

This document lists common misunderstandings and how to correct them. Use these during exercises to avoid typical pitfalls.

---

## Session Layer (L5) Misconceptions

### 🚫 Misconception 1: "A TCP connection IS a session"

**WRONG:** "Once I have a TCP connection, I have a session with the server."

**CORRECT:** A TCP connection provides reliable byte-stream delivery between two endpoints. A **session** is an application-level concept that includes authentication state, user context and persistent settings. Sessions can span multiple TCP connections (HTTP cookies) or be lost when a single TCP connection drops (FTP).

| Aspect | TCP Connection (L4) | Session (L5) |
|--------|---------------------|--------------|
| Identity | IP:port ↔ IP:port | User ↔ Service |
| State | Sequence numbers, window size | Authentication, preferences, CWD |
| Lifetime | Until FIN or timeout | Until logout or expiry |
| Survives reconnect? | No | Depends on application design |

**Practical verification:**

```bash
# Connect to FTP, login, then kill the terminal
ftp localhost 2121
# USER test / PASS 12345
# pwd → shows /home/test

# Kill terminal (Ctrl+C or close window)
# Reconnect - you must login again!
ftp localhost 2121
# pwd → error "not logged in"
```

**Why this matters:** Understanding this distinction helps you design protocols that handle network interruptions gracefully.

---

### 🚫 Misconception 2: "FTP uses one connection like HTTP"

**WRONG:** "FTP sends commands and receives files on the same connection, just like HTTP."

**CORRECT:** FTP uses TWO separate TCP connections:

1. **Control connection** (port 21) — persistent, carries text commands (USER, PASS, LIST, RETR)
2. **Data connection** (port 20 or dynamic) — temporary, carries file contents and directory listings

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          FTP Dual-Channel Architecture                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Client                                              Server                 │
│   ┌──────────┐                                       ┌──────────┐           │
│   │          │ ══════ Control Channel (21) ════════► │          │           │
│   │          │         USER, PASS, LIST, RETR        │          │           │
│   │          │ ◄═══════════════════════════════════  │          │           │
│   │          │         220, 230, 150, 226            │          │           │
│   │          │                                       │          │           │
│   │          │ ═══════ Data Channel (dyn) ═════════► │          │           │
│   │          │         File contents                 │          │           │
│   └──────────┘                                       └──────────┘           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Practical verification:**

```bash
# In Wireshark, filter: tcp.port == 2121 || tcp.port >= 60000
# Connect and download a file
# Count distinct TCP streams — you will see TWO
```

**Why this matters:** Firewalls must allow both connections. NAT traversal requires passive mode.

---

### 🚫 Misconception 3: "Active and Passive FTP modes are interchangeable"

**WRONG:** "I can use either active or passive mode — they do the same thing."

**CORRECT:** The modes differ in WHO initiates the data connection:

| Mode | Data connection initiator | NAT-friendly? | Firewall-friendly? |
|------|---------------------------|---------------|-------------------|
| **Active** | Server → Client (port 20 → client port) | ❌ No | ❌ No |
| **Passive** | Client → Server (client → server dynamic port) | ✅ Yes | ✅ Yes |

**Active mode fails through NAT because:**
1. Client says "connect to me on port 5000"
2. Server tries to connect to client's private IP (192.168.x.x)
3. NAT blocks incoming connection → Transfer fails

**Passive mode works because:**
1. Server says "I'm listening on port 60005"
2. Client initiates outbound connection to server
3. NAT allows outbound connections → Transfer succeeds

**Practical verification:**

```python
# Test both modes
from ftplib import FTP

ftp = FTP()
ftp.connect('localhost', 2121)
ftp.login('test', '12345')

ftp.set_pasv(True)   # Passive mode - works through NAT
ftp.retrlines('LIST')

ftp.set_pasv(False)  # Active mode - may fail through NAT
ftp.retrlines('LIST')  # Error if behind NAT
```

---

### 🚫 Misconception 4: "Closing the control channel immediately stops data transfer"

**WRONG:** "If I close the FTP control connection during a file download, the transfer stops immediately."

**CORRECT:** The data channel is a separate TCP connection. Closing the control channel does NOT immediately terminate an in-progress data transfer. The data connection has its own TCP state and will continue until:

- The file transfer completes normally
- The data connection times out
- The server explicitly closes the data socket

However, you lose the ability to:
- Receive transfer completion confirmation (226)
- Abort the transfer gracefully (ABOR command)
- Request additional files

**Why this matters:** Proper cleanup requires closing connections in the correct order.

---

## Presentation Layer (L6) Misconceptions

### 🚫 Misconception 5: "My computer uses big-endian like the network"

**WRONG:** "x86 processors use big-endian byte order, so I don't need to convert."

**CORRECT:** Intel/AMD x86 and x86-64 processors use **little-endian** byte order. Network protocols use **big-endian** (network byte order). You MUST convert when sending multi-byte integers over the network.

| Architecture | Byte order | 0x12345678 in memory |
|--------------|------------|---------------------|
| x86, x86-64, ARM (default) | Little-endian | `78 56 34 12` |
| Network protocols, SPARC, PowerPC | Big-endian | `12 34 56 78` |

**Practical verification:**

```python
import struct
import sys

value = 0x12345678

# Native byte order (your machine)
native = struct.pack("=I", value)
print(f"Native ({sys.byteorder}): {native.hex()}")

# Network byte order (always big-endian)
network = struct.pack("!I", value)
print(f"Network: {network.hex()}")

# Little-endian explicit
little = struct.pack("<I", value)
print(f"Little: {little.hex()}")

# Big-endian explicit
big = struct.pack(">I", value)
print(f"Big: {big.hex()}")
```

**Output on x86:**
```
Native (little): 78563412
Network: 12345678
Little: 78563412
Big: 12345678
```

---

> In previous years, roughly 60% of students initially selected little-endian when asked about network byte order on the first quiz attempt. After the hands-on struct exercises, this drops to under 10% on the re-test. The key insight that sticks: "network = big, Intel = little".


### 🚫 Misconception 6: "CRC-32 provides security against tampering"

**WRONG:** "I use CRC-32 to verify data integrity, so attackers can't modify my files undetected."

**CORRECT:** CRC-32 detects **accidental errors** (transmission noise, bit flips) but provides **zero security** against intentional modification. An attacker who can modify the data can trivially recalculate the correct CRC-32 for the modified content.

| Feature | CRC-32 | SHA-256 | HMAC-SHA256 |
|---------|--------|---------|-------------|
| Detects accidental errors | ✅ Yes | ✅ Yes | ✅ Yes |
| Detects intentional tampering | ❌ No | ✅ Yes | ✅ Yes |
| Requires shared secret | ❌ No | ❌ No | ✅ Yes |
| Speed | Very fast | Fast | Fast |
| Output size | 32 bits | 256 bits | 256 bits |

**Practical verification:**

```python
import zlib
import hashlib

original = b"Transfer $100 to Alice"
modified = b"Transfer $999 to Alice"

# Attacker can easily recalculate CRC
crc_original = zlib.crc32(original) & 0xFFFFFFFF
crc_modified = zlib.crc32(modified) & 0xFFFFFFFF

print(f"Original: {original} → CRC: 0x{crc_original:08X}")
print(f"Modified: {modified} → CRC: 0x{crc_modified:08X}")
print("Attacker just sends modified data with new CRC — undetectable!")

# SHA-256 doesn't help either without authentication
sha_original = hashlib.sha256(original).hexdigest()
sha_modified = hashlib.sha256(modified).hexdigest()
print(f"\nSHA-256 also recalculable by attacker")

# Only HMAC with secret key provides tamper detection
import hmac
secret = b"shared_secret_key"
hmac_original = hmac.new(secret, original, hashlib.sha256).hexdigest()
print(f"\nHMAC requires secret key attacker doesn't have")
```

---

### 🚫 Misconception 7: "struct.pack preserves message boundaries on TCP"

**WRONG:** "If I send a 12-byte header with struct.pack and then 100 bytes of data, the receiver will get exactly 12 bytes, then exactly 100 bytes."

**CORRECT:** TCP is a **byte stream** protocol with NO message boundaries. A single `send(112)` might be received as:

- `recv(112)` — all at once
- `recv(50)` + `recv(62)` — split
- `recv(8)` + `recv(4)` + `recv(100)` — multiple splits
- `recv(200)` — combined with next message!

**This is why we need FRAMING:**

```python
# WRONG - assumes message boundaries
def recv_message_wrong(sock):
    header = sock.recv(12)      # Might get only 8 bytes!
    length = struct.unpack("!I", header[4:8])[0]
    payload = sock.recv(length)  # Might get partial data!
    return payload

# CORRECT - explicit framing
def recv_exactly(sock, n):
    """Receive exactly n bytes, handling partial reads."""
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Connection closed")
        data += chunk
    return data

def recv_message_correct(sock):
    header = recv_exactly(sock, 12)  # Guaranteed 12 bytes
    length = struct.unpack("!I", header[4:8])[0]
    payload = recv_exactly(sock, length)  # Guaranteed length bytes
    return payload
```

**Why this matters:** Without proper framing, your protocol will randomly fail under network congestion or with large messages.

---

### 🚫 Misconception 8: "The PASV response port number is just one number"

**WRONG:** "The PASV response says port 60004, so I connect to port 60004."

**CORRECT:** The PASV response encodes the port as TWO numbers that must be combined:

```
227 Entering Passive Mode (192,168,1,5,234,100)
                           └─────────┘ └──┬──┘
                           IP address   Port encoding
                                        
Port = (p1 × 256) + p2 = (234 × 256) + 100 = 59908 + 100 = 60004
```

The format is `(h1,h2,h3,h4,p1,p2)` where:
- `h1.h2.h3.h4` = IP address (often server's internal IP)
- Port = `p1 * 256 + p2`

**Practical verification:**

```python
def parse_pasv_response(response: str) -> tuple[str, int]:
    """
    Parse PASV response to extract IP and port.
    
    Example: "227 Entering Passive Mode (192,168,1,5,234,100)"
    Returns: ("192.168.1.5", 60004)
    """
    # Extract the parentheses content
    start = response.index("(") + 1
    end = response.index(")")
    parts = response[start:end].split(",")
    
    # Parse IP and port
    ip = ".".join(parts[:4])
    port = int(parts[4]) * 256 + int(parts[5])
    
    return ip, port

# Test
response = "227 Entering Passive Mode (192,168,1,5,234,100)"
ip, port = parse_pasv_response(response)
print(f"Connect to {ip}:{port}")  # 192.168.1.5:60004
```

---

## Summary: Quick Reference

| # | Misconception | Reality |
|---|---------------|---------|
| 1 | TCP connection = session | Session is application-level state |
| 2 | FTP uses one connection | FTP uses control + data channels |
| 3 | Active/passive are equivalent | Passive works through NAT |
| 4 | Closing control stops transfer | Data channel is independent |
| 5 | x86 is big-endian | x86 is little-endian |
| 6 | CRC-32 prevents tampering | CRC only detects accidents |
| 7 | TCP preserves message boundaries | TCP is a byte stream |
| 8 | PASV port is single number | Port = p1×256 + p2 |

---

## Testing Your Understanding

After reviewing these misconceptions, you should be able to answer:

1. Why does FTP require two connections while HTTP uses one?
2. What happens to your FTP session if the network drops briefly?
3. Why do we use `>` or `!` in struct format strings for network protocols?
4. When would CRC-32 fail to detect data modification?
5. How do you ensure you receive exactly N bytes from a TCP socket?

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Week 9: Session Layer and Presentation Layer*
