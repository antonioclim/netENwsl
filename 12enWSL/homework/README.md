# 📝 Homework — Week 12: Email Protocols and Remote Procedure Calls

> Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

## Overview

This week's homework covers SMTP client implementation and RPC protocol comparison, bridging application-layer protocols with practical performance analysis.

## Assignments

| File | Topic | Difficulty | Est. Time |
|------|-------|------------|-----------|
| `hw_12_01_smtp_client.py` | SMTP Client Implementation | ⭐⭐ Intermediate | 60-75 min |
| `hw_12_02_rpc_comparison.py` | RPC Protocol Comparison and Benchmarking | ⭐⭐⭐ Advanced | 75-90 min |

## Assignment Details

### hw_12_01_smtp_client.py

Implement a basic SMTP client following RFC 5321.

**Learning Objectives:**
- Understand SMTP command-response protocol
- Implement EHLO, MAIL FROM, RCPT TO, DATA sequence
- Handle SMTP response codes correctly
- Format email messages with proper headers

**Key Skills:**
- Socket programming
- Protocol implementation
- Error handling

**SMTP Commands Covered:**
- `EHLO` — Client identification
- `MAIL FROM` — Sender specification
- `RCPT TO` — Recipient specification
- `DATA` — Message content transfer
- `QUIT` — Session termination

### hw_12_02_rpc_comparison.py

Compare XML-RPC, JSON-RPC, and gRPC protocols through analysis and benchmarking.

**Learning Objectives:**
- Understand trade-offs between RPC protocols
- Analyse payload size differences
- Measure and compare performance characteristics
- Select appropriate protocols for different use cases

**Key Skills:**
- Protocol analysis
- Performance benchmarking
- Technology selection criteria

**Protocols Compared:**
| Protocol | Encoding | Transport | Best For |
|----------|----------|-----------|----------|
| XML-RPC | XML | HTTP | Legacy integration |
| JSON-RPC | JSON | HTTP | Web APIs, debugging |
| gRPC | Protocol Buffers | HTTP/2 | Microservices |

## Prerequisites

Before starting, ensure you have completed:
- Week 12 lab exercises
- Understanding of application-layer protocols
- Basic socket programming knowledge

For SMTP exercise:
- Lab SMTP server should be running (port 2525)

## Submission Guidelines

1. Complete all `TODO` sections
2. Successfully send a test email (SMTP exercise)
3. Run benchmarks and analyse results (RPC exercise)
4. Document your findings and conclusions

## Grading Rubric

| Criterion | Points |
|-----------|--------|
| Correct protocol implementation | 40% |
| Successful message/call completion | 25% |
| Analysis quality and insights | 20% |
| Code quality and documentation | 15% |

## Tips

### SMTP Exercise
- Test with the lab's local SMTP server first
- Pay attention to CRLF line endings
- Remember to escape lines starting with "." in DATA
- Response codes 2xx = success, 3xx = continue, 4xx/5xx = error

### RPC Exercise
- Focus on understanding WHY protocols differ in performance
- Payload size directly impacts network bandwidth usage
- Consider both latency and throughput in your analysis
- Real-world choice depends on constraints (legacy systems, debugging needs, performance requirements)

---

*Week 12 Homework — Computer Networks*
