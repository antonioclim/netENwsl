# 🧩 Parsons Problems — Week 9

> Session Layer (L5) and Presentation Layer (L6)
> NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Parsons Problems present code blocks in scrambled order. Your task is to arrange
them correctly whilst avoiding distractor blocks (incorrect code that should not
be included).

**How to use:**
1. Read the problem description carefully
2. Identify the correct blocks (some are distractors!)
3. Arrange the correct blocks in proper order
4. Verify your solution matches the expected output

---

## P1: Pack a Network Message (LO2, LO3)

**Objective:** Arrange the code blocks to pack a message with a header containing
magic bytes, message type, length and CRC-32 checksum in network byte order.

**Expected output:** A bytes object with 14-byte header + payload

### Scrambled Blocks

```python
# Block A
import struct
import zlib

# Block B
def pack_message(payload: bytes, msg_type: int = 1) -> bytes:

# Block C
    magic = b"S9PK"

# Block D
    length = len(payload)

# Block E
    crc = zlib.crc32(payload) & 0xFFFFFFFF

# Block F
    header = struct.pack(">4sBxII", magic, msg_type, length, crc)

# Block G (DISTRACTOR - wrong byte order)
    header = struct.pack("<4sBxII", magic, msg_type, length, crc)

# Block H (DISTRACTOR - missing CRC mask)
    crc = zlib.crc32(payload)

# Block I
    return header + payload
```

### Solution Order

<details>
<summary>Click to reveal solution</summary>

**Correct order:** A → B → C → D → E → F → I

**Distractors to avoid:**
- Block G: Uses little-endian (`<`) instead of network byte order (`>`)
- Block H: Missing `& 0xFFFFFFFF` mask for unsigned CRC

**Complete solution:**
```python
import struct
import zlib

def pack_message(payload: bytes, msg_type: int = 1) -> bytes:
    magic = b"S9PK"
    length = len(payload)
    crc = zlib.crc32(payload) & 0xFFFFFFFF
    header = struct.pack(">4sBxII", magic, msg_type, length, crc)
    return header + payload
```
</details>

---

## P2: FTP Session Setup (LO1, LO4)

**Objective:** Arrange the code blocks to establish an FTP session with proper
authentication sequence.

**Expected output:** Successfully authenticated FTP connection

### Scrambled Blocks

```python
# Block A
from ftplib import FTP

# Block B
def connect_ftp(host: str, port: int, user: str, password: str) -> FTP:

# Block C
    ftp = FTP()

# Block D
    ftp.connect(host, port)

# Block E
    ftp.login(user, password)

# Block F (DISTRACTOR - wrong order)
    ftp.login(user, password)
    ftp.connect(host, port)

# Block G
    return ftp
```

### Solution Order

<details>
<summary>Click to reveal solution</summary>

**Correct order:** A → B → C → D → E → G

**Distractors to avoid:**
- Block F: Attempts login before connect (will fail)

**Key insight:** FTP requires connection before authentication. The session
layer (authentication) builds on the transport layer (TCP connection).

**Complete solution:**
```python
from ftplib import FTP

def connect_ftp(host: str, port: int, user: str, password: str) -> FTP:
    ftp = FTP()
    ftp.connect(host, port)
    ftp.login(user, password)
    return ftp
```
</details>

---

## P3: Checkpoint State Machine (LO6)

**Objective:** Arrange the code blocks to implement a session state machine with
checkpoint and recovery capabilities.

**Expected output:** A state machine that tracks session states and supports checkpointing

### Scrambled Blocks

```python
# Block A
from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional

# Block B
class SessionState(Enum):
    DISCONNECTED = auto()
    CONNECTED = auto()
    AUTHENTICATED = auto()
    TRANSFERRING = auto()

# Block C
@dataclass
class Checkpoint:
    state: SessionState
    bytes_transferred: int
    timestamp: float

# Block D
class Session:
    def __init__(self):
        self.state = SessionState.DISCONNECTED
        self.checkpoint: Optional[Checkpoint] = None

# Block E
    def save_checkpoint(self, bytes_transferred: int) -> None:
        import time
        self.checkpoint = Checkpoint(
            state=self.state,
            bytes_transferred=bytes_transferred,
            timestamp=time.time()
        )

# Block F
    def restore_checkpoint(self) -> int:
        if self.checkpoint is None:
            return 0
        self.state = self.checkpoint.state
        return self.checkpoint.bytes_transferred

# Block G (DISTRACTOR - no state restoration)
    def restore_checkpoint(self) -> int:
        if self.checkpoint is None:
            return 0
        return self.checkpoint.bytes_transferred

# Block H (DISTRACTOR - missing timestamp)
@dataclass
class Checkpoint:
    state: SessionState
    bytes_transferred: int

# Block I (DISTRACTOR - wrong initial state)
class Session:
    def __init__(self):
        self.state = SessionState.AUTHENTICATED
        self.checkpoint: Optional[Checkpoint] = None
```

### Solution Order

<details>
<summary>Click to reveal solution</summary>

**Correct order:** A → B → C → D → E → F

**Distractors to avoid:**
- Block G: Does not restore state, only returns bytes (incomplete recovery)
- Block H: Missing timestamp field (cannot verify checkpoint age)
- Block I: Wrong initial state (should start DISCONNECTED)

**Key insight:** Checkpoint recovery must restore BOTH the session state AND
the transfer position. Timestamps enable checkpoint validity verification.

**Complete solution:**
```python
from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional

class SessionState(Enum):
    DISCONNECTED = auto()
    CONNECTED = auto()
    AUTHENTICATED = auto()
    TRANSFERRING = auto()

@dataclass
class Checkpoint:
    state: SessionState
    bytes_transferred: int
    timestamp: float

class Session:
    def __init__(self):
        self.state = SessionState.DISCONNECTED
        self.checkpoint: Optional[Checkpoint] = None

    def save_checkpoint(self, bytes_transferred: int) -> None:
        import time
        self.checkpoint = Checkpoint(
            state=self.state,
            bytes_transferred=bytes_transferred,
            timestamp=time.time()
        )

    def restore_checkpoint(self) -> int:
        if self.checkpoint is None:
            return 0
        self.state = self.checkpoint.state
        return self.checkpoint.bytes_transferred
```
</details>

---

## P4: FTP Passive Mode Setup (LO4)

**Objective:** Arrange the code blocks to parse an FTP PASV response and connect
to the data channel.

**Expected output:** Socket connected to the passive data port

### Scrambled Blocks

```python
# Block A
import socket
import re

# Block B
def parse_pasv_response(response: str) -> tuple[str, int]:
    """Parse '227 Entering Passive Mode (h1,h2,h3,h4,p1,p2)'"""

# Block C
    match = re.search(r'\((\d+),(\d+),(\d+),(\d+),(\d+),(\d+)\)', response)

# Block D
    if not match:
        raise ValueError("Invalid PASV response")

# Block E
    parts = [int(x) for x in match.groups()]

# Block F
    host = f"{parts[0]}.{parts[1]}.{parts[2]}.{parts[3]}"

# Block G
    port = (parts[4] * 256) + parts[5]

# Block H (DISTRACTOR - wrong port calculation)
    port = parts[4] + parts[5]

# Block I (DISTRACTOR - wrong port calculation)
    port = (parts[4] << 16) + parts[5]

# Block J
    return host, port
```

### Solution Order

<details>
<summary>Click to reveal solution</summary>

**Correct order:** A → B → C → D → E → F → G → J

**Distractors to avoid:**
- Block H: Simple addition instead of (p1 * 256) + p2
- Block I: Bit shift by 16 instead of 8 (same as * 65536)

**Key insight:** FTP PASV port = (p1 × 256) + p2. For example,
(234, 120) = (234 × 256) + 120 = 59904 + 120 = 60024.

**Complete solution:**
```python
import socket
import re

def parse_pasv_response(response: str) -> tuple[str, int]:
    """Parse '227 Entering Passive Mode (h1,h2,h3,h4,p1,p2)'"""
    match = re.search(r'\((\d+),(\d+),(\d+),(\d+),(\d+),(\d+)\)', response)
    if not match:
        raise ValueError("Invalid PASV response")
    parts = [int(x) for x in match.groups()]
    host = f"{parts[0]}.{parts[1]}.{parts[2]}.{parts[3]}"
    port = (parts[4] * 256) + parts[5]
    return host, port
```
</details>

---

## P5: Wireshark Filter Construction (LO5)

**Objective:** Arrange the filter expressions to create a compound Wireshark
display filter for FTP traffic analysis.

**Expected output:** A filter that shows FTP control and data channel traffic

### Scrambled Blocks

```
# Block A - Base filter for FTP control channel
tcp.port == 2121

# Block B - Filter for passive data channels
tcp.port >= 60000 && tcp.port <= 60010

# Block C - Combine with OR operator
(tcp.port == 2121) || (tcp.port >= 60000 && tcp.port <= 60010)

# Block D - Add FTP command filter
ftp.request.command

# Block E (DISTRACTOR - wrong operator precedence)
tcp.port == 2121 || tcp.port >= 60000 && tcp.port <= 60010

# Block F (DISTRACTOR - wrong comparison)
tcp.port > 60000 && tcp.port < 60010

# Block G - Filter for authentication only
ftp.request.command == "USER" || ftp.request.command == "PASS"

# Block H - Complete filter with authentication
(tcp.port == 2121 && (ftp.request.command == "USER" || ftp.request.command == "PASS")) || (tcp.port >= 60000 && tcp.port <= 60010)
```

### Solution Order

<details>
<summary>Click to reveal solution</summary>

**For basic FTP traffic:** Block C

**For authentication + data:** Block H

**Distractors to avoid:**
- Block E: Missing parentheses causes wrong precedence (AND binds tighter than OR)
- Block F: Uses `>` and `<` instead of `>=` and `<=`, missing ports 60000 and 60010

**Key insight:** Wireshark filters follow C-style operator precedence.
Always use parentheses for compound OR/AND expressions.

**Filter examples:**
```
# All FTP traffic (control + data)
(tcp.port == 2121) || (tcp.port >= 60000 && tcp.port <= 60010)

# Only authentication commands
tcp.port == 2121 && (ftp.request.command == "USER" || ftp.request.command == "PASS")

# Only data transfers
tcp.port >= 60000 && tcp.port <= 60010
```
</details>

---

## Summary Table

| Problem | Learning Objectives | Difficulty | Distractors | Key Concept |
|---------|---------------------|------------|-------------|-------------|
| P1 | LO2, LO3 | Intermediate | 2 | Network byte order, CRC masking |
| P2 | LO1, LO4 | Basic | 1 | Connect before login sequence |
| P3 | LO6 | Advanced | 3 | State + position recovery |
| P4 | LO4 | Intermediate | 2 | PASV port calculation formula |
| P5 | LO5 | Basic | 2 | Filter operator precedence |

---

## Self-Check Questions

After completing each Parsons Problem, ask yourself:

1. **P1:** Why must we use `& 0xFFFFFFFF` on the CRC result?
2. **P2:** What happens if you call `login()` before `connect()`?
3. **P3:** Why is timestamp important in a checkpoint?
4. **P4:** What port does `(234, 120)` decode to?
5. **P5:** Why do we need parentheses in compound Wireshark filters?

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Week 9: Session Layer and Presentation Layer*
