# Project 13: Distributed RPC Application

> **Course:** Computer Networks | **Institution:** ASE Bucharest - CSIE | **Project type:** Main

**Common guides:** [Pair Programming](../docs/common/pair_programming_guide.md) | [Code Quality](../docs/common/code_quality_standards.md) | [Git Workflow](../docs/common/git_workflow_detailed.md)

### 📅 Stage Calendar
| Stage | Week | Deliverables | Score |
|-------|------|--------------|-------|
| **E1** - Design | Week 5 | Specifications + Diagrams | 20% |
| **E2** - Prototype | Week 9 | Partial implementation | 25% |
| **E3** - Final | Week 13 | Complete version | 35% |
| **E4** - Presentation | Week 14 | Live demo | 20% |

**Repository:** `https://github.com/[username]/retele-proiect-13`

---

## 📚 Project Description

Implement a distributed application using Remote Procedure Calls (RPC). Compare different RPC frameworks (gRPC, JSON-RPC, XML-RPC) and demonstrate inter-service communication.

### 🎯 Learning Objectives
- **Implement** RPC client and server
- **Define** service interfaces with Protocol Buffers
- **Handle** serialisation and deserialisation
- **Compare** RPC frameworks performance

---

## 🎯 Concept Analogies

### RPC = Phone Call to Expert
🏠 **Analogy:** You call an expert (remote server) with a question (function call). They do the work and tell you the answer (return value). You don't need to know how they found the answer.

💻 **Technical:** Client calls function, network transports request, server executes, returns result.

### Protocol Buffers = Pre-Agreed Forms
🏠 **Analogy:** Instead of describing everything in free text (JSON), you use standardised forms (protobuf schema) that are faster to fill and process.

---

## 🗳️ Peer Instruction Questions

### Question 1: gRPC vs REST
**Question:** What makes gRPC faster than REST for many use cases?
- A) Better servers
- B) Binary serialisation and HTTP/2 ✓
- C) Simpler API
- D) No network overhead

### Question 2: Streaming
**Question:** gRPC supports streaming. What does server streaming mean?
- A) Client sends multiple messages
- B) Server sends multiple messages ✓
- C) Bidirectional communication
- D) Video streaming

---

## ❌ Common Misconceptions

### 🚫 "RPC is just like REST"
**CORRECT:** RPC is action-oriented (call function), REST is resource-oriented (manipulate resource). Different approaches.

### 🚫 "gRPC requires Protocol Buffers"
**CORRECT:** gRPC can use JSON, but protobuf is default and recommended for performance.

---

## 📖 Glossary
| Term | Definition |
|------|------------|
| **RPC** | Remote Procedure Call |
| **gRPC** | Google's high-performance RPC framework |
| **Protocol Buffers** | Binary serialisation format |
| **Stub** | Client-side proxy for remote calls |
| **Streaming** | Continuous message exchange |

---

## 🔨 Implementation Example

```protobuf
// calculator.proto
syntax = "proto3";

service Calculator {
    // 💭 PREDICTION: What network protocol does this use?
    // Answer: HTTP/2
    
    rpc Add(AddRequest) returns (AddResponse);
    rpc Multiply(MultiplyRequest) returns (MultiplyResponse);
}

message AddRequest {
    int32 a = 1;
    int32 b = 2;
}

message AddResponse {
    int32 result = 1;
}
```

```python
# server.py
# ═══════════════════════════════════════════════════════════════════════════════
# GRPC_SERVER
# ═══════════════════════════════════════════════════════════════════════════════
import grpc
from concurrent import futures
import calculator_pb2
import calculator_pb2_grpc

class CalculatorServicer(calculator_pb2_grpc.CalculatorServicer):
    def Add(self, request, context):
        result = request.a + request.b
        return calculator_pb2.AddResponse(result=result)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(
        CalculatorServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
```

---

## 📚 Laboratory References

Consult these resources from **netENwsl** (https://github.com/antonioclim/netENwsl):

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 12 | `12enWSL/` | RPC (gRPC, JSON-RPC, XML-RPC) |
| 4 | `04enWSL/` | Protocol design with struct |

---

*Last update: January 2026 — Computer Networks, ASE Bucharest*
