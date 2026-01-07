# Week 12: Homework Assignments

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by Revolvix

## Overview

These assignments extend the laboratory exercises on SMTP email protocols and Remote Procedure Call (RPC) mechanisms. Complete them independently to reinforce your understanding of application-layer protocols and distributed computing paradigms.

---

## Assignment 1: SMTP Client with MIME Attachments

**Difficulty:** Intermediate  
**Estimated Time:** 2–3 hours  
**Due:** Before the next laboratory session

### Objective

Implement a Python SMTP client capable of sending emails with MIME multipart attachments (text and binary files).

### Requirements

1. Create a module `smtp_mime_client.py` that:
   - Connects to an SMTP server using raw socket communication
   - Implements proper SMTP dialogue (HELO/EHLO, MAIL FROM, RCPT TO, DATA, QUIT)
   - Constructs MIME multipart messages with:
     - Plain text body
     - HTML alternative body
     - At least one binary attachment (image or PDF)
   - Handles Base64 encoding for binary content
   - Supports multiple recipients (To, Cc, Bcc)

2. The client must work with the laboratory SMTP server (port 1025)

3. Include proper error handling for:
   - Connection failures
   - SMTP error responses (4xx, 5xx codes)
   - Invalid email addresses
   - Missing or unreadable attachments

### Deliverables

- `homework/exercises/smtp_mime_client.py` — Main client implementation
- `homework/exercises/test_smtp_mime.py` — Unit tests demonstrating functionality
- Sample output showing a successful multipart email transaction
- Packet capture (`.pcap`) of the SMTP session

### Evaluation Criteria

| Criterion | Weight |
|-----------|--------|
| Correct SMTP protocol implementation | 30% |
| Proper MIME structure and encoding | 25% |
| Error handling and robustness | 20% |
| Code quality and documentation | 15% |
| Test coverage | 10% |

### Hints

- Study RFC 5321 (SMTP) and RFC 2045-2049 (MIME)
- Use Python's `base64` module for encoding
- The MIME boundary must be unique and not appear in content
- Content-Transfer-Encoding: base64 for binary data

---

## Assignment 2: Custom JSON-RPC Method Implementation

**Difficulty:** Intermediate  
**Estimated Time:** 2–3 hours  
**Due:** Before the next laboratory session

### Objective

Extend the JSON-RPC server with a new method `string_stats` and implement comprehensive client testing.

### Requirements

1. Add a new method `string_stats` to the JSON-RPC server that:
   - Accepts a string parameter
   - Returns a JSON object containing:
     - `length`: Total character count
     - `words`: Word count
     - `sentences`: Sentence count (based on `.!?`)
     - `char_frequency`: Dictionary of character frequencies
     - `most_common`: The three most frequent characters
     - `palindrome`: Boolean indicating if the string is a palindrome (ignoring spaces/punctuation)

2. Implement a client script that:
   - Tests the new method with various inputs
   - Demonstrates batch requests combining `string_stats` with other methods
   - Handles all JSON-RPC error conditions

3. Add XML-RPC equivalent for comparison:
   - Implement the same `string_stats` method in the XML-RPC server
   - Compare request/response sizes between JSON-RPC and XML-RPC

### Deliverables

- `homework/exercises/jsonrpc_string_stats.py` — Server extension
- `homework/exercises/xmlrpc_string_stats.py` — XML-RPC equivalent
- `homework/exercises/test_string_stats.py` — Client test suite
- `homework/exercises/protocol_comparison.md` — Analysis document comparing:
  - Request payload sizes
  - Response payload sizes
  - Parsing complexity
  - Type safety considerations

### Evaluation Criteria

| Criterion | Weight |
|-----------|--------|
| Correct method implementation | 30% |
| JSON-RPC 2.0 compliance | 20% |
| XML-RPC implementation | 15% |
| Protocol comparison analysis | 20% |
| Code quality and tests | 15% |

### Hints

- Follow JSON-RPC 2.0 specification exactly (id, jsonrpc, method, params)
- Use `collections.Counter` for character frequency
- Consider edge cases: empty strings, Unicode characters, very long inputs

---

## Assignment 3: Protocol Analysis Report

**Difficulty:** Advanced  
**Estimated Time:** 3–4 hours  
**Due:** Before the next laboratory session

### Objective

Conduct a comprehensive protocol analysis using Wireshark, comparing SMTP, JSON-RPC, XML-RPC, and gRPC communications.

### Requirements

1. Capture network traffic for each protocol performing equivalent operations:
   - SMTP: Send an email with subject "Protocol Analysis Test"
   - JSON-RPC: Call `add(10, 20)` and `get_server_info()`
   - XML-RPC: Call equivalent methods
   - gRPC: Call `Add(10, 20)` and `GetStats()`

2. For each protocol, document:
   - Connection establishment (TCP handshake analysis)
   - Request structure and encoding
   - Response structure and encoding
   - Total bytes transmitted (headers + payload)
   - Number of round trips required
   - Latency measurements

3. Create comparison tables and visualisations:
   - Overhead comparison (protocol bytes vs payload bytes)
   - Latency comparison chart
   - Complexity assessment matrix

4. Write analytical conclusions addressing:
   - When to choose each protocol
   - Trade-offs between human readability and efficiency
   - Impact of Protocol Buffers on gRPC performance
   - Security considerations for each approach

### Deliverables

- `homework/exercises/captures/` — Directory containing:
  - `smtp_analysis.pcapng`
  - `jsonrpc_analysis.pcapng`
  - `xmlrpc_analysis.pcapng`
  - `grpc_analysis.pcapng`
- `homework/exercises/protocol_analysis_report.md` — Full analysis report (minimum 1500 words)
- `homework/exercises/comparison_charts.png` — Visualisation of findings

### Evaluation Criteria

| Criterion | Weight |
|-----------|--------|
| Capture completeness and accuracy | 20% |
| Protocol analysis depth | 25% |
| Comparative analysis quality | 25% |
| Conclusions and recommendations | 20% |
| Presentation and formatting | 10% |

### Hints

- Use Wireshark's "Follow TCP Stream" for readable output
- Export statistics using Wireshark's IO graphs
- gRPC uses HTTP/2 — enable HTTP/2 dissector in Wireshark
- Consider using `tshark -z` for automated statistics

---

## Submission Guidelines

1. **Format:** Submit all files in a ZIP archive named `WEEK12_HW_<StudentID>.zip`

2. **Structure:**
   ```
   WEEK12_HW_<StudentID>/
   ├── assignment1/
   │   ├── smtp_mime_client.py
   │   ├── test_smtp_mime.py
   │   └── smtp_session.pcap
   ├── assignment2/
   │   ├── jsonrpc_string_stats.py
   │   ├── xmlrpc_string_stats.py
   │   ├── test_string_stats.py
   │   └── protocol_comparison.md
   └── assignment3/
       ├── captures/
       ├── protocol_analysis_report.md
       └── comparison_charts.png
   ```

3. **Code Requirements:**
   - All Python files must include docstrings
   - Follow PEP 8 style guidelines
   - Include type hints for function signatures
   - No external dependencies beyond standard library and course packages

4. **Documentation:**
   - Write in British English
   - Include your student ID in file headers
   - Cite any external resources used

---

## Academic Integrity

These assignments must be completed individually. You may:
- Discuss concepts with classmates
- Reference course materials and documentation
- Use the laboratory starter kit as a foundation

You may **not**:
- Share code with other students
- Submit work that is not your own
- Use AI-generated code without explicit permission

Violations will result in a zero grade and potential disciplinary action.

---

## Resources

- [RFC 5321 - SMTP](https://tools.ietf.org/html/rfc5321)
- [RFC 2045-2049 - MIME](https://tools.ietf.org/html/rfc2045)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
- [XML-RPC Specification](http://xmlrpc.com/spec.md)
- [gRPC Documentation](https://grpc.io/docs/)
- [Wireshark User Guide](https://www.wireshark.org/docs/wsug_html/)

---

*NETWORKING class - ASE, Informatics | by Revolvix*
