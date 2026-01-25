# 🗳️ Peer Instruction Questions — Week 9
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Session Layer (L5) and Presentation Layer (L6)

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

## Question 1: Endianness and Network Byte Order

> 💭 **PREDICTION:** Before looking at the options, write down what byte sequence you expect for the integer 0x12345678 in network byte order.

### Scenario

You are implementing a binary protocol and need to send the 32-bit integer `0x12345678` over the network. You use Python's `struct` module:

```python
import struct
data = struct.pack("!I", 0x12345678)
print(" ".join(f"{b:02x}" for b in data))
```

### Question

What will be printed?

### Options

- **A)** `78 56 34 12` — Little-endian stores LSB first
- **B)** `12 34 56 78` — Network byte order is big-endian (MSB first)
- **C)** `12 78 34 56` — Bytes are interleaved for error detection
- **D)** `21 43 65 87` — Each byte is reversed individually

### Correct Answer

**B** — Network byte order (`!` or `>` in struct) is big-endian, which stores the Most Significant Byte (MSB) first. The value 0x12345678 becomes bytes `12 34 56 78` in memory order.

### Targeted Misconception

Many students confuse big-endian with little-endian, or assume their x86 machine's native order (little-endian) is the network standard. The "!" format character explicitly means "network byte order" which is always big-endian regardless of the host architecture.

### Instructor Notes

- **Target accuracy:** 40-60% on first vote
- **Key concept:** Network protocols use big-endian for portability
- **After discussion:** Show both `>I` and `<I` outputs side by side
- **Common error:** Students selecting A because x86 uses little-endian
- **Timing:** Present (1 min) → Vote (1 min) → Discuss (3 min) → Revote (30 sec) → Explain (2 min)

---

## Question 2: FTP Connection Architecture

> 💭 **PREDICTION:** How many TCP connections does FTP use to download one file?

### Scenario

A client connects to an FTP server and downloads a single file (`RETR document.pdf`). The Wireshark capture shows the following sequence:

```
1. TCP SYN to port 21 → Connection established
2. "220 Welcome to FTP server"
3. "USER test" → "331 Password required"
4. "PASS 12345" → "230 Login successful"
5. "PASV" → "227 Entering Passive Mode (192,168,1,5,234,100)"
6. TCP SYN to port 60004 → Connection established
7. "RETR document.pdf" → "150 Opening data connection"
8. [File data transferred on second connection]
9. "226 Transfer complete"
10. "QUIT" → "221 Goodbye"
```

### Question

How many separate TCP connections were used in this FTP session?

### Options

- **A)** 1 — FTP multiplexes commands and data on a single connection
- **B)** 2 — One control connection (port 21) and one data connection (port 60004)
- **C)** 3 — One for authentication, one for commands, one for data
- **D)** 4 — Separate connections for USER, PASS, PASV and RETR

### Correct Answer

**B** — FTP uses exactly two connections: a persistent **control connection** on port 21 for commands and responses and a temporary **data connection** on a dynamic port (60004 in this case) for file transfers. The data connection is established per-transfer and closed after each file.

### Targeted Misconception

Students often assume FTP works like HTTP with a single connection, or conversely, that each command creates a new connection. The dual-channel architecture is a defining characteristic of FTP that enables features like transfer resumption and out-of-band control.

### Instructor Notes

- **Target accuracy:** 50-70% on first vote
- **Key concept:** FTP's control/data channel separation
- **After discussion:** Draw the two-channel diagram on whiteboard
- **Follow-up:** Ask "What happens to the data connection after the file transfers?"
- **Timing:** Standard 7-minute cycle
- **From running this exercise:** Expect heated debate on whether passive mode counts as "additional connections". Let them argue — the confusion is productive and leads to deeper understanding of the protocol architecture.


---

## Question 3: Session vs Transport Connection

> 💭 **PREDICTION:** If a TCP connection drops and reconnects, what happens to your FTP login status?

### Scenario

You are logged into an FTP server and actively browsing directories:

```
230 Login successful
ftp> pwd
257 "/home/test" is current directory
ftp> cd documents
250 Directory changed to /home/test/documents
```

At this moment, your network cable is accidentally unplugged for 30 seconds, then reconnected. The TCP connection times out and is re-established.

### Question

After the TCP reconnection, what is your session state on the FTP server?

### Options

- **A)** Fully preserved — TCP handles reconnection transparently
- **B)** Lost — You must re-authenticate (USER/PASS) and navigate back to /home/test/documents
- **C)** Partially preserved — Authentication is kept but current directory resets to /
- **D)** Cached — The server remembers your session for 5 minutes by default

### Correct Answer

**B** — The FTP session is tied to the TCP connection. When the TCP connection drops, all session state (authentication, current directory, transfer mode) is lost. A new TCP connection starts fresh with no authentication. This illustrates the distinction between Transport Layer connections (TCP) and Session Layer state (FTP login).

### Targeted Misconception

Students confuse TCP connection state with application session state. TCP provides reliable byte-stream delivery but has no concept of "user" or "login". Session state is maintained by the application protocol (FTP) and must be re-established after any connection interruption.

### Instructor Notes

- **Target accuracy:** 35-55% on first vote (commonly missed)
- **Key concept:** Session Layer adds state that Transport Layer doesn't provide
- **Demonstration:** Actually disconnect and show re-authentication requirement
- **Discussion prompt:** "How could FTP be designed to support session resumption?"
- **Timing:** Allow extra discussion time (3-4 min)

---

## Question 4: CRC-32 Purpose and Limitations

> 💭 **PREDICTION:** Can CRC-32 detect if someone maliciously modified a file during transfer?

### Scenario

You implement a file transfer protocol with CRC-32 verification:

```python
import zlib

def send_file(sock, data):
    crc = zlib.crc32(data) & 0xFFFFFFFF
    header = struct.pack("!II", len(data), crc)
    sock.sendall(header + data)

def recv_file(sock):
    length, expected_crc = struct.unpack("!II", recv_all(sock, 8))
    data = recv_all(sock, length)
    actual_crc = zlib.crc32(data) & 0xFFFFFFFF
    if actual_crc != expected_crc:
        raise ValueError("Data corrupted!")
    return data
```

An attacker intercepts the transmission and wants to modify the file contents without detection.

### Question

Can the attacker modify both the file and the CRC-32 value to avoid detection?

### Options

- **A)** No — CRC-32 is cryptographically secure and cannot be forged
- **B)** Yes — CRC-32 only detects accidental errors; an attacker can recalculate it for modified data
- **C)** No — The polynomial used in CRC-32 prevents intentional modifications
- **D)** Yes, but only for files smaller than 4GB due to the 32-bit limit

### Correct Answer

**B** — CRC-32 is designed to detect **accidental transmission errors** (bit flips, noise), not malicious modifications. An attacker who can modify the data can trivially recalculate the CRC-32 for the modified content. For protection against tampering, cryptographic hashes (SHA-256) or message authentication codes (HMAC) are required.

### Targeted Misconception

Students often conflate "integrity check" with "security". CRC-32 provides data integrity against random errors but offers zero protection against intentional modification. This is a Presentation Layer function (error detection) distinct from security services.

### Instructor Notes

- **Target accuracy:** 45-65% on first vote
- **Key concept:** CRC vs cryptographic hash distinction
- **After discussion:** Show how easy it is to recalculate CRC for modified data
- **Security tie-in:** Mention HMAC and digital signatures for actual tamper detection
- **Timing:** Standard 7-minute cycle

---

## Question 5: FTP Passive vs Active Mode

> 💭 **PREDICTION:** In passive mode, who initiates the data connection — client or server?

### Scenario

A client behind a NAT firewall connects to an FTP server. The firewall blocks incoming connections but allows outgoing ones.

```
Client (192.168.1.100)  ←→  NAT Firewall  ←→  Internet  ←→  FTP Server (203.0.113.50)
     [Private IP]           [Blocks inbound]                    [Public IP]
```

The client issues a `PASV` command and receives:

```
227 Entering Passive Mode (203,0,113,50,234,100)
```

### Question

What happens next to establish the data connection?

### Options

- **A)** Server connects to client on port 60004 — "Passive" means the server waits passively for commands
- **B)** Client connects to server on port 60004 (234×256+100) — Client initiates data connection in passive mode
- **C)** Both open ports and meet in the middle using TCP simultaneous open
- **D)** The NAT firewall creates a tunnel automatically based on the PASV response

### Correct Answer

**B** — In **passive mode**, the server opens a listening port (60004 = 234×256+100) and the **client initiates** the data connection to that port. This works through NAT because the client makes an outbound connection. In contrast, **active mode** has the server connect to the client, which fails through most NAT/firewalls.

### Targeted Misconception

The name "passive mode" confuses students — it refers to the server's role (passively waiting for connection), not the client's. Students often think "passive" means the client does nothing. The key insight is: passive mode = client-initiated data connection = NAT-friendly.

### Instructor Notes

- **Target accuracy:** 40-60% on first vote
- **Key concept:** Data connection direction determines NAT compatibility
- **Demonstration:** Show both modes in Wireshark, highlight connection initiator
- **Calculation exercise:** Have students decode (h1,h2,h3,h4,p1,p2) format
- **Real-world relevance:** "This is why web browsers don't use FTP active mode"
- **Timing:** Standard 7-minute cycle

---

## Summary: Key Concepts Tested

| Question | Layer | Concept | Common Misconception |
|----------|-------|---------|---------------------|
| Q1 | L6 | Endianness | x86 little-endian ≠ network order |
| Q2 | L5 | FTP architecture | Single connection assumption |
| Q3 | L5 | Session vs connection | TCP handles sessions |
| Q4 | L6 | CRC-32 limitations | CRC = security |
| Q5 | L5 | Active vs passive FTP | "Passive" = client passive |

---

## Instructor Preparation Checklist

- [ ] Wireshark capture of FTP session ready for Q2 and Q5
- [ ] Python REPL open for live endianness demo (Q1)
- [ ] Whiteboard diagram of FTP dual-channel architecture
- [ ] Example of CRC recalculation for tampered data (Q4)
- [ ] NAT diagram showing connection direction (Q5)

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Week 9: Session Layer and Presentation Layer*
