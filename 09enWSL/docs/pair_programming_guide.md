# 👥 Pair Programming Guide — Week 9
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Session Layer (L5) and Presentation Layer (L6)

---

## Why Pair Programming?

Pair programming accelerates learning through:

- **Immediate feedback** — catch errors as they happen
- **Knowledge transfer** — learn from your partner's approach
- **Reduced frustration** — two minds solving problems together
- **Better code quality** — continuous review during development

---

## Roles and Responsibilities

| Role | Responsibilities | Focus |
|------|-----------------|-------|
| **Driver** | Types code, controls keyboard and mouse | Tactical — writing correct syntax |
| **Navigator** | Reviews code, suggests improvements, checks documentation | Strategic — overall approach and design |

### Role Guidelines

**Driver should:**
- Think aloud while typing
- Ask questions when unsure
- Focus on the current line/block of code
- Be open to Navigator's suggestions

**Navigator should:**
- Watch for typos and syntax errors
- Keep track of the bigger picture
- Look up documentation when needed
- Suggest improvements without grabbing the keyboard

**SWAP roles every 10-15 minutes!** Set a timer.

---

## Session Structure for Week 9

### Phase 1: Setup (5 min)
- [ ] Both partners can access the lab environment
- [ ] Docker containers are running (`python3 scripts/start_lab.py --status`)
- [ ] Wireshark is ready (select vEthernet WSL interface)
- [ ] Decide who drives first
- [ ] Review exercise objectives together

### Phase 2: Implementation (50-60 min)
- Follow the pair exercises below
- Swap roles at designated swap points
- Navigator: actively review, don't just watch

### Phase 3: Review (10 min)
- [ ] Both partners can explain every function
- [ ] Test edge cases together
- [ ] Discuss: "What would happen if...?"
- [ ] Document any issues encountered

---

## Pair Exercises for Week 9

### Pair Exercise P1: Binary Protocol Header

**Objective:** Implement and verify a binary message framing protocol

**Estimated time:** 25 minutes

**Starting point:** `src/exercises/ex_9_01_demonstrate_endianness.py`

#### Driver 1 Tasks (12 min)

1. Open the exercise file and review the header structure
2. Implement a function to visualise byte differences:

```python
def visualise_bytes(data: bytes, label: str) -> None:
    """
    Display bytes in hex with visual grouping.
    
    💭 PREDICTION: How many bytes will a 4-byte integer show?
    """
    print(f"{label}:")
    print("  Hex:    ", " ".join(f"{b:02x}" for b in data))
    print("  Decimal:", " ".join(f"{b:3d}" for b in data))
```

3. Test with big-endian and little-endian packing of 0xDEADBEEF

**Navigator 1 Tasks:**
- Verify the format string is correct (`>I` vs `<I`)
- Check that the output matches expected byte order
- Look up `struct.calcsize()` if needed

**💭 PREDICTION before running:** What bytes will `struct.pack(">I", 0xDEADBEEF)` produce?

---

#### ⏱️ SWAP ROLES

---

#### Driver 2 Tasks (12 min)

1. Implement CRC-32 verification with deliberate corruption:

```python
def test_corruption_detection() -> None:
    """
    Demonstrate CRC-32 detecting single-bit errors.
    
    💭 PREDICTION: Will flipping bit 0 and bit 31 both be detected?
    """
    original = b"Session Layer manages dialogue control"
    crc_original = zlib.crc32(original) & 0xFFFFFFFF
    
    # Corrupt one byte
    corrupted = bytearray(original)
    corrupted[10] ^= 0x01  # Flip one bit
    corrupted = bytes(corrupted)
    
    crc_corrupted = zlib.crc32(corrupted) & 0xFFFFFFFF
    
    print(f"Original CRC:  0x{crc_original:08X}")
    print(f"Corrupted CRC: 0x{crc_corrupted:08X}")
    print(f"Match: {crc_original == crc_corrupted}")
```

2. Run the test and verify CRC detects the corruption

**Navigator 2 Tasks:**
- Verify the bit flip is actually happening (print before/after)
- Suggest testing with different corruption positions
- Check: does CRC-32 tell us WHERE the error is?

**💭 PREDICTION:** Will two different corruptions ever produce the same CRC?

---

### Pair Exercise P2: FTP Session Lifecycle

**Objective:** Observe and analyse FTP authentication and data transfer

**Estimated time:** 30 minutes

**Prerequisites:** Docker containers running, Wireshark capturing

#### Driver 1 Tasks (15 min)

1. Start Wireshark capture on vEthernet (WSL) interface
2. Apply filter: `tcp.port == 2121 || tcp.port >= 60000`
3. Connect to FTP server using the demo client:

```bash
cd src/exercises
python3 ex_9_03_ftp_client_demo.py --host localhost --port 2121 \
    --user test --password 12345 --local-dir ./downloads list
```

4. In Wireshark, identify:
   - TCP three-way handshake (SYN, SYN-ACK, ACK)
   - FTP banner (220 response)
   - USER/PASS authentication sequence
   - LIST command and response

**Navigator 1 Tasks:**
- Note the TCP port numbers for each connection
- Track the FTP response codes (220, 331, 230, etc.)
- Document: How many packets for authentication?

**💭 PREDICTION:** What response code indicates successful login?

---

#### ⏱️ SWAP ROLES

---

#### Driver 2 Tasks (15 min)

1. Perform a file download in passive mode:

```bash
python3 ex_9_03_ftp_client_demo.py --host localhost --port 2121 \
    --user test --password 12345 get hello.txt
```

2. In Wireshark, find:
   - PASV command and response
   - Second TCP connection establishment (data channel)
   - File content transfer
   - Data connection closure

3. Right-click on a data packet → Follow → TCP Stream

**Navigator 2 Tasks:**
- Calculate the passive port from the PASV response: (p1 × 256) + p2
- Verify the data connection uses a different port than control
- Question: "What would happen if we used active mode through NAT?"

**💭 PREDICTION:** How many TCP connections total for one file download?

---

### Pair Exercise P3: Pseudo-FTP Implementation

**Objective:** Build a simplified FTP-like protocol with binary framing

**Estimated time:** 35 minutes

**Starting point:** `src/exercises/ex_9_02_implement_pseudo_ftp.py`

#### Driver 1 Tasks (17 min)

1. Review the Session class implementation
2. Add session state logging:

```python
def log_session_state(session: Session) -> None:
    """Display current session state for debugging."""
    print(f"─── Session State ───")
    print(f"  Authenticated: {session.is_authenticated()}")
    print(f"  Username: {session.username or '(none)'}")
    print(f"  CWD: /{session.cwd}")
    print(f"  Root: {session.root_dir}")
    print(f"─────────────────────")
```

3. Insert logging calls after login and directory changes

4. Start the server in one terminal:

```bash
python3 ex_9_02_implement_pseudo_ftp.py server --port 3333 --root ./server-files
```

**Navigator 1 Tasks:**
- Verify the Session class correctly tracks state
- Check: What happens to session state on QUIT?
- Look for security issues (path traversal protection)

**💭 PREDICTION:** What prevents a client from accessing `../../etc/passwd`?

---

#### ⏱️ SWAP ROLES

---

#### Driver 2 Tasks (18 min)

1. In a second terminal, connect as client:

```bash
python3 ex_9_02_implement_pseudo_ftp.py client --port 3333 --interactive
```

2. Test the session lifecycle:

```
ftp> AUTH wrong_user wrong_pass
ftp> AUTH test 12345
ftp> PWD
ftp> CWD ..
ftp> LIST
ftp> QUIT
```

3. Observe the binary framing in Wireshark (filter: `tcp.port == 3333`)

4. Add compression test:

```python
# In client, test with gzip flag
client.passive_put("large_file.txt", use_gzip=True)
```

**Navigator 2 Tasks:**
- Track the session state changes through each command
- Verify CWD ".." doesn't escape the sandbox
- Compare wire size with and without gzip compression

**💭 PREDICTION:** How much smaller will a text file be with gzip?

---

## Communication Phrases

### Navigator → Driver

| Situation | Phrase |
|-----------|--------|
| Spotted error | "I think there's a typo on line X..." |
| Suggest approach | "What if we tried...?" |
| Need clarification | "Could you explain what this part does?" |
| Documentation needed | "Let me look that up while you continue..." |
| Time to swap | "Want to swap? I have some ideas to try." |

### Driver → Navigator

| Situation | Phrase |
|-----------|--------|
| Thinking aloud | "I'm going to try... because..." |
| Need help | "I'm stuck on how to... any ideas?" |
| Verify approach | "Does this approach make sense?" |
| Ready to swap | "Good stopping point — your turn?" |

---

## Troubleshooting Together

When stuck, follow this sequence:

1. **Driver:** Explain your current understanding out loud
2. **Navigator:** Ask clarifying questions (not solutions yet)
3. **Both:** Re-read the error message word by word
4. **Navigator:** Search documentation or examples
5. **Together:** Form a hypothesis and test it
6. **If stuck >5 minutes:** Ask the instructor

### Common Week 9 Issues

| Symptom | Driver checks | Navigator checks |
|---------|---------------|------------------|
| Wrong byte order | Format string (`>` vs `<`) | Expected vs actual hex dump |
| CRC mismatch | Data modification order | CRC calculation scope |
| FTP auth fails | Credentials spelling | Server logs for error details |
| Passive port wrong | PASV parsing formula | Wireshark port numbers |
| Session lost | Connection state | Server-side session object |

---

## End of Session Checklist

- [ ] Both partners can explain the binary header structure
- [ ] Both partners understand FTP dual-channel architecture
- [ ] Both partners can trace a session lifecycle
- [ ] Code is committed (if using git)
- [ ] Wireshark captures saved to `pcap/` folder
- [ ] Any unresolved questions noted for instructor

---

## Reflection Questions

After completing the pair exercises, discuss:

1. What was the most surprising thing you learned?
2. Where did having a partner help most?
3. What would you do differently next time?
4. Which concept needs more practice?

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Week 9: Session Layer and Presentation Layer*
