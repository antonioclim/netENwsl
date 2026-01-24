# 👥 Pair Programming Guide — Week 4

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

## Physical Layer, Data Link Layer & Custom Protocols

---

## Roles

| Role | Responsibilities | Focus |
|------|-----------------|-------|
| **Driver** | Types code, controls keyboard and mouse | Implementation details, syntax |
| **Navigator** | Reviews, suggests, checks documentation | Big picture, design, correctness |

**SWAP roles every 10-15 minutes!** Set a timer.

---

## Why Pair Programming?

For protocol implementation, pair programming helps because:

- **Four eyes catch endianness bugs** — Navigator can verify byte order whilst Driver types
- **Real-time code review** — Catch off-by-one errors in buffer handling
- **Knowledge sharing** — One partner may know `struct`, the other knows sockets
- **Reduced debugging time** — Errors caught during typing, not during testing

---

## Session Structure

### Phase 1: Setup (5 min)

- [ ] Both partners have WSL terminal open
- [ ] Docker running: `docker ps` shows week4_demo
- [ ] Both can access http://localhost:9000 (Portainer)
- [ ] Decide who drives first (suggestion: less experienced with topic)
- [ ] Open exercise file and read objectives TOGETHER

### Phase 2: Implementation (40-50 min)

Follow the exercise structure. Swap roles at marked points.

**Driver responsibilities:**
- Type code as discussed
- Verbalise what you're typing: "I'm packing the header with big-endian..."
- Ask Navigator before making design decisions

**Navigator responsibilities:**
- Keep documentation open (Python docs, RFC, cheatsheet)
- Watch for common errors (endianness, off-by-one, missing null checks)
- Think ahead: "After this function, we'll need to..."
- DON'T grab the keyboard!

### Phase 3: Review (10 min)

- [ ] Both partners can explain every line
- [ ] Test with provided test cases
- [ ] Test edge cases together (empty payload, max length, corrupted CRC)
- [ ] Discuss: "What would break if...?"

---

## This Week's Pair Exercises

### Exercise P1: TEXT Protocol Parser

**Objective:** Implement length-prefix framing for TEXT protocol

**Estimated time:** 25 min

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  DRIVER TASK                                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  Implement recv_exact() and recv_framed_message()                          │
│  File: src/exercises/ex_4_01_tcp_proto.py                                  │
│                                                                             │
│  Focus on:                                                                  │
│  - Handling partial reads (while loop until n bytes received)              │
│  - Converting length bytes to integer (big-endian)                         │
│  - Error handling for closed connections                                   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  NAVIGATOR TASK                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  - Keep docs/commands_cheatsheet.md open                                   │
│  - Verify Driver uses 'big' endianness for int.from_bytes()               │
│  - Check: Does recv_exact handle n=0? (edge case)                         │
│  - Watch for: ConnectionError vs empty bytes (different meanings)          │
│  - Prepare test cases: empty message, 1-byte message, 65535-byte message  │
└─────────────────────────────────────────────────────────────────────────────┘
```

**🔄 SWAP after:** recv_exact() is working (test with: send 10 bytes, recv_exact(10))

---

### Exercise P2: BINARY Protocol Header

**Objective:** Build and parse the 14-byte binary header with CRC32

**Estimated time:** 30 min

```
Header structure:
┌────────┬─────────┬──────┬────────────┬─────┬───────┐
│ Magic  │ Version │ Type │ PayloadLen │ Seq │ CRC32 │
│ 2B     │ 1B      │ 1B   │ 2B         │ 4B  │ 4B    │
└────────┴─────────┴──────┴────────────┴─────┴───────┘
```

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  DRIVER TASK                                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  Implement pack_header() and unpack_header()                               │
│  File: src/exercises/ex_4_02_udp_sensor.py (or create new)                 │
│                                                                             │
│  Focus on:                                                                  │
│  - struct.pack format string: '>2sBBHII' (discuss with Navigator)         │
│  - CRC32 calculation BEFORE adding CRC field                               │
│  - Named tuple or dataclass for unpacked header                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  NAVIGATOR TASK                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  - Verify format string:                                                   │
│    > = big-endian, 2s = 2-char string, B = unsigned byte,                 │
│    H = unsigned short (2B), I = unsigned int (4B)                         │
│  - Calculate: 2+1+1+2+4+4 = 14 bytes (verify header size)                 │
│  - CRC scope: Calculate over header (without CRC) + payload               │
│  - Test values: Magic=b'NP', Version=1, Type=1, Len=0, Seq=1              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**🔄 SWAP after:** pack_header() produces 14 bytes

---

### Exercise P3: CRC32 Verification

**Objective:** Implement CRC calculation and validation

**Estimated time:** 20 min

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  DRIVER TASK                                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  Implement calculate_crc() and verify_crc()                                │
│                                                                             │
│  Focus on:                                                                  │
│  - Use zlib.crc32() for calculation                                        │
│  - CRC input = header_without_crc + payload                                │
│  - Handle the & 0xFFFFFFFF for unsigned result                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  NAVIGATOR TASK                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  - Verify: CRC is calculated BEFORE being added to header                  │
│  - Test corruption: Flip one bit in payload, verify CRC fails              │
│  - Edge case: Empty payload (CRC of header only)                           │
│  - Read: docs/misconceptions.md #5 and #6 (CRC misconceptions)            │
└─────────────────────────────────────────────────────────────────────────────┘
```

**🔄 SWAP after:** calculate_crc() matches expected test value

---

## Communication Phrases

### Navigator to Driver

| Situation | Say this |
|-----------|----------|
| Spot potential bug | "Hold on—should that be `>` or `<` for endianness?" |
| Need clarification | "Can you walk me through what this line does?" |
| Suggest improvement | "What if we extracted that into a helper function?" |
| Found in docs | "The documentation says recv() returns empty bytes on close..." |
| Thinking ahead | "After this, we'll need to handle the error case..." |

### Driver to Navigator

| Situation | Say this |
|-----------|----------|
| Before typing | "I'm going to use struct.pack with format '>H'..." |
| Need help | "I'm not sure about the CRC calculation order—can you check?" |
| Design question | "Should we return None or raise an exception here?" |
| Ready to test | "Let's run the test client and see what happens." |

---

## Troubleshooting Together

When stuck, follow this sequence:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  1. Driver: Explain your current understanding out loud                    │
│     "I think the problem is... because..."                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  2. Navigator: Ask clarifying questions                                    │
│     "What value did you expect here? What did you get?"                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  3. Both: Re-read the error message carefully                             │
│     Often the answer is right there!                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│  4. Navigator: Search documentation                                        │
│     docs/troubleshooting.md, Python docs, cheatsheet                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  5. Both: Add debug prints                                                 │
│     print(f"header_bytes = {header_bytes.hex()}")                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  6. If stuck > 5 min: Ask instructor                                      │
│     State: "We expected X, got Y, tried Z"                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Common Pair Programming Pitfalls

### ❌ Don't Do This

| Pitfall | Why it's bad |
|---------|--------------|
| Navigator grabs keyboard | Driver loses focus, roles blur |
| "Just let me do it" | No knowledge transfer |
| Silent Driver | Navigator can't follow or help |
| Navigator on phone | Partner feels unsupported |
| Skipping the swap | One person learns, one watches |

### ✅ Do This Instead

| Good Practice | Why it works |
|---------------|--------------|
| Verbalise while typing | Navigator stays engaged |
| Ask before deciding | Catches errors early |
| Swap on time | Both learn both perspectives |
| Celebrate small wins | "recv_exact works! Nice!" |
| Review together at end | Solidifies understanding |

---

## Role Swap Schedule

| Time | Activity | Who Drives |
|------|----------|------------|
| 0:00 | Setup, read exercise | — |
| 0:05 | Exercise P1 start | Partner A |
| 0:15 | **SWAP** | Partner B |
| 0:25 | Exercise P1 complete, P2 start | Partner B |
| 0:35 | **SWAP** | Partner A |
| 0:45 | Exercise P2 complete, P3 start | Partner A |
| 0:55 | **SWAP** | Partner B |
| 1:05 | Exercise P3 complete | Partner B |
| 1:10 | Review together | Both |

---

## After the Session

Each partner should be able to:

- [ ] Explain why TCP needs application-level framing
- [ ] Write a recv_exact() function from memory
- [ ] Describe the binary header structure (fields and sizes)
- [ ] Calculate CRC32 with zlib and explain what it detects
- [ ] Convert between big-endian and little-endian mentally

**Individual follow-up:** Complete homework exercises alone to verify understanding.

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Week 4: Physical Layer, Data Link Layer & Custom Protocols*
