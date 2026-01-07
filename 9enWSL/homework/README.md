# Homework: Week 9

> Session Layer (L5) and Presentation Layer (L6) - Take-Home Exercises
> NETWORKING class - ASE, Informatics | by Revolvix

---

## Overview

These homework assignments extend the concepts covered in the Week 9 laboratory session. Complete them individually and submit according to your instructor's guidelines.

**Topics Covered:**
- Binary protocol design and implementation
- Data serialisation with Python's `struct` module
- Session management patterns
- FTP protocol extensions

---

## Assignment 1: Multi-Format Protocol (hw_9_01.py)

### Objective

Design and implement a binary protocol that supports multiple data formats within the same message stream.

### Requirements

1. Create a protocol supporting three message types:
   - **TEXT** (0x01): UTF-8 encoded strings
   - **INTEGER** (0x02): 32-bit signed integers (network byte order)
   - **BLOB** (0x03): Raw binary data

2. Each message must include:
   - Magic bytes: `MFMT` (4 bytes)
   - Protocol version: 1 (1 byte)
   - Message type: 1 byte
   - Payload length: 4 bytes (big-endian)
   - CRC-32 checksum: 4 bytes
   - Payload: variable length

3. Implement:
   - `encode_message(msg_type: int, payload: bytes) -> bytes`
   - `decode_message(data: bytes) -> tuple[int, bytes]`
   - `verify_checksum(data: bytes) -> bool`

### Evaluation Criteria

| Criterion | Points |
|-----------|--------|
| Correct header structure | 20 |
| Proper endianness handling | 20 |
| CRC-32 implementation | 20 |
| Type handling for all formats | 20 |
| Error handling and edge cases | 10 |
| Code quality and documentation | 10 |
| **Total** | **100** |

### Hints

- Use `struct.pack()` with format `">4sBBI"` for the fixed header
- Consider what happens with empty payloads
- Test with binary data containing null bytes

---

## Assignment 2: Session State Machine (hw_9_02.py)

### Objective

Implement a finite state machine for managing FTP-like sessions with authentication and command processing.

### Requirements

1. Define states:
   - **DISCONNECTED**: Initial state
   - **CONNECTED**: TCP connection established
   - **AUTHENTICATING**: Username provided, awaiting password
   - **AUTHENTICATED**: Successfully logged in
   - **TRANSFERRING**: Data transfer in progress
   - **ERROR**: Recoverable error state

2. Define transitions:
   ```
   DISCONNECTED --connect--> CONNECTED
   CONNECTED --user--> AUTHENTICATING
   AUTHENTICATING --pass(valid)--> AUTHENTICATED
   AUTHENTICATING --pass(invalid)--> ERROR
   AUTHENTICATED --transfer--> TRANSFERRING
   TRANSFERRING --complete--> AUTHENTICATED
   TRANSFERRING --abort--> AUTHENTICATED
   * --disconnect--> DISCONNECTED
   ERROR --reset--> CONNECTED
   ```

3. Implement:
   - `Session` class with state management
   - `transition(event: str, **kwargs) -> bool`
   - `get_available_commands() -> list[str]`
   - State change logging with timestamps
   - Timeout handling for inactive sessions

### Evaluation Criteria

| Criterion | Points |
|-----------|--------|
| Correct state machine implementation | 25 |
| All transitions working | 20 |
| Invalid transition handling | 15 |
| Timeout mechanism | 15 |
| State history logging | 10 |
| Thread safety (bonus) | 10 |
| Code quality and documentation | 5 |
| **Total** | **100** |

### Hints

- Use an `Enum` for states
- Consider using a transition table (dictionary)
- Think about what happens with rapid state changes

---

## Submission Guidelines

### Format

1. Submit individual Python files:
   - `hw_9_01_<student_id>.py`
   - `hw_9_02_<student_id>.py`

2. Include at the top of each file:
   ```python
   """
   Homework Assignment: Week 9
   Student: <Your Name>
   ID: <Student ID>
   Date: <Submission Date>
   """
   ```

3. Include unit tests demonstrating functionality

### Testing Your Work

```powershell
# Run your implementation
python homework/exercises/hw_9_01.py

# Verify with provided test cases
python -c "from homework.exercises.hw_9_01 import *; test_all()"
```

### Deadline

Check your course schedule or Moodle for the submission deadline.

---

## Academic Integrity

- Work must be your own
- You may discuss concepts but not share code
- Cite any external resources used
- Plagiarism detection tools will be used

---

## Resources

- Laboratory materials: `src/exercises/`
- Theory summary: `docs/theory_summary.md`
- Python struct documentation: https://docs.python.org/3/library/struct.html
- RFC 959 (FTP): https://tools.ietf.org/html/rfc959

---

*NETWORKING class - ASE, Informatics | by Revolvix*
