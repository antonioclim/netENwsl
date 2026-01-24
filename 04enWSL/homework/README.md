# Week 4: Homework Assignments

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

---

## 👥 Pair Programming Guidelines

These assignments can be completed individually or in pairs. If working in pairs:

1. **Both names** must appear in the file header
2. **Both partners** must be able to explain any part of the code
3. Follow Driver/Navigator roles (swap every 15-20 minutes)
4. Submit ONE solution per pair with both names

---

## Overview

These homework assignments extend the laboratory exercises and test your understanding of custom protocol design, binary data handling and network programming concepts.

**Submission Deadline:** As specified by your instructor  
**Submission Format:** Python source files (.py) with accompanying documentation

---

## 📋 Assessment Rubric

| Criterion | Points | Description |
|-----------|--------|-------------|
| **Functionality** | 40 | Code works correctly for all specified requirements |
| **Code Quality** | 20 | Clean code, proper naming, docstrings, type hints |
| **Error Handling** | 15 | Reliable handling of edge cases and errors |
| **Documentation** | 15 | Clear comments, protocol specification, README |
| **Testing** | 10 | Provided tests demonstrate functionality |

---

## Assignment 1: Enhanced Binary Protocol

**File:** `exercises/hw_4_01.py`

### Objective

Extend the BINARY protocol implementation to support additional message types and features.

### Requirements

1. **New Message Types**
   - Implement `MSG_BATCH` (type 0x10): Send multiple key-value pairs in one message
   - Implement `MSG_SUBSCRIBE` (type 0x11): Subscribe to key change notifications
   - Implement `MSG_NOTIFY` (type 0x12): Server notification of key changes

2. **Protocol Extensions**
   - Add a `flags` field to the header (1 byte after version)
   - Implement compression flag (bit 0): payload compressed with zlib
   - Implement encryption flag (bit 1): payload encrypted (simple XOR for demonstration)

3. **Enhanced Error Handling**
   - Return appropriate error codes for invalid operations
   - Implement timeout handling for subscriptions
   - Add retry logic for failed operations

### Deliverables

- Modified server implementation supporting new message types
- Client implementation demonstrating all features
- Protocol specification document (markdown) describing your extensions
- Test script verifying all functionality

### Grading Criteria

| Criterion | Points |
|-----------|--------|
| Correct message type implementation | 30 |
| Flags field implementation | 20 |
| Error handling | 20 |
| Code quality and documentation | 15 |
| Test coverage | 15 |
| **Total** | **100** |

---

## Assignment 2: Reliable UDP Protocol

**File:** `exercises/hw_4_02.py`

### Objective

Design and implement a reliable data transfer protocol over UDP, implementing core concepts from the transport layer.

### Requirements

1. **Reliability Mechanisms**
   - Implement sequence numbers for ordering
   - Add acknowledgment messages
   - Implement timeout-based retransmission
   - Handle duplicate detection

2. **Flow Control**
   - Implement a simple sliding window (window size: 4)
   - Track outstanding (unacknowledged) packets
   - Implement window-based sending

3. **Congestion Awareness**
   - Implement adaptive timeout calculation (simple EWMA)
   - Add basic congestion detection (3 duplicate ACKs)

4. **File Transfer Application**
   - Transfer a file reliably over your protocol
   - Verify integrity using SHA-256 checksum
   - Report transfer statistics (throughput, retransmissions)

### Protocol Specification

Design your own header format including:
- Sequence number (4 bytes)
- Acknowledgment number (4 bytes)
- Flags (1 byte): SYN, ACK, FIN, DATA
- Window size (2 bytes)
- Checksum (4 bytes)
- Payload length (2 bytes)

### Deliverables

- Sender implementation (`reliable_sender.py`)
- Receiver implementation (`reliable_receiver.py`)
- Protocol specification document
- Performance analysis comparing with raw UDP
- Test with artificial packet loss (10%, 20%, 30%)

### Testing with Packet Loss

```python
# Simulate packet loss for testing
import random

LOSS_RATE = 0.1  # 10% packet loss

def maybe_drop_packet(data: bytes) -> bytes | None:
    """Simulate packet loss."""
    if random.random() < LOSS_RATE:
        return None  # Packet "lost"
    return data
```

### Grading Criteria

| Criterion | Points |
|-----------|--------|
| Reliability (no data loss) | 25 |
| Ordering (correct sequence) | 20 |
| Flow control implementation | 20 |
| File transfer functionality | 15 |
| Performance analysis | 10 |
| Documentation and code quality | 10 |
| **Total** | **100** |

---

## Submission Guidelines

### Code Requirements

1. **Header Comment**
   ```python
   """
   Week 4 Homework Assignment <N>
   Student: <Your Name>
   Group: <Your Group>
   Date: <Submission Date>
   
   Description: <Brief description of your implementation>
   """
   ```

2. **Code Style**
   - Follow PEP 8 guidelines
   - Include docstrings for all functions
   - Use meaningful variable names
   - Add inline comments for complex logic

3. **Testing**
   - Include unit tests for key functions
   - Provide instructions for running tests
   - Document expected output

### Documentation Requirements

Each assignment must include:
- Protocol specification (if designing new protocol)
- Implementation notes explaining design decisions
- Known limitations or issues
- Instructions for running and testing

### Submission Package Structure

```
hw_4_<student_name>/
├── README.md           # Overview and running instructions
├── hw_4_01/
│   ├── enhanced_server.py
│   ├── enhanced_client.py
│   ├── PROTOCOL.md
│   └── test_hw_01.py
└── hw_4_02/
    ├── reliable_sender.py
    ├── reliable_receiver.py
    ├── PROTOCOL.md
    ├── test_hw_02.py
    └── performance_analysis.md
```

---

## Hints and Tips

### Assignment 1 Hints

1. **Batch Messages**
   - Consider using a count field followed by repeated key-value structures
   - Handle partial failures (some keys succeed, some fail)

2. **Subscription Pattern**
   - Keep a list of subscribed clients per key
   - Consider using a separate notification thread

3. **Compression**
   ```python
   import zlib
   
   compressed = zlib.compress(data)
   decompressed = zlib.decompress(compressed)
   ```

### Assignment 2 Hints

1. **Sequence Numbers**
   - Use 32-bit unsigned integers
   - Handle wraparound correctly

2. **Timeout Calculation**
   ```python
   # Exponential Weighted Moving Average
   ALPHA = 0.125
   estimated_rtt = (1 - ALPHA) * estimated_rtt + ALPHA * sample_rtt
   timeout = estimated_rtt * 2
   ```

3. **Sliding Window**
   - Track `base` (oldest unacked) and `next_seq` (next to send)
   - Window: [base, base + window_size)

4. **Testing with Loss**
   - Start with 0% loss to verify basic functionality
   - Gradually increase loss rate
   - Log all retransmissions for analysis

---

## Academic Integrity

- This is individual work unless specified otherwise
- You may discuss concepts with classmates but must write your own code
- Cite any external resources used
- Plagiarism detection will be applied to submissions

---

## Questions and Support

- Post questions on the course forum
- Attend office hours for clarification
- Review laboratory exercises for reference implementations

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
