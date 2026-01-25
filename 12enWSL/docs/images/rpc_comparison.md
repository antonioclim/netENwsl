# RPC Protocol Comparison Diagram

This diagram compares JSON-RPC, XML-RPC and gRPC protocols.

## Protocol Architecture Comparison

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         RPC PROTOCOL COMPARISON                                  │
├──────────────────┬──────────────────┬──────────────────┬────────────────────────┤
│                  │    JSON-RPC 2.0  │     XML-RPC      │        gRPC            │
├──────────────────┼──────────────────┼──────────────────┼────────────────────────┤
│ Encoding         │    Text (JSON)   │    Text (XML)    │   Binary (protobuf)    │
├──────────────────┼──────────────────┼──────────────────┼────────────────────────┤
│ Transport        │    HTTP/1.1      │    HTTP/1.1      │      HTTP/2            │
├──────────────────┼──────────────────┼──────────────────┼────────────────────────┤
│ Schema           │    Optional      │    None          │   Required (.proto)    │
├──────────────────┼──────────────────┼──────────────────┼────────────────────────┤
│ Type Safety      │    Runtime       │    Runtime       │     Compile-time       │
├──────────────────┼──────────────────┼──────────────────┼────────────────────────┤
│ Human Readable   │       ✓          │       ✓          │         ✗              │
├──────────────────┼──────────────────┼──────────────────┼────────────────────────┤
│ Streaming        │       ✗          │       ✗          │         ✓              │
├──────────────────┼──────────────────┼──────────────────┼────────────────────────┤
│ Batch Requests   │       ✓          │       ✗          │         ✓              │
└──────────────────┴──────────────────┴──────────────────┴────────────────────────┘
```

## Payload Size Comparison

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│              PAYLOAD SIZE: add(10, 32)                                          │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  JSON-RPC (~55 bytes):                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐          │
│  │ {"jsonrpc":"2.0","method":"add","params":[10,32],"id":1}          │          │
│  └───────────────────────────────────────────────────────────────────┘          │
│                                                                                 │
│  XML-RPC (~250 bytes):                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐          │
│  │ <?xml version="1.0"?>                                             │          │
│  │ <methodCall>                                                       │          │
│  │   <methodName>add</methodName>                                     │          │
│  │   <params>                                                         │          │
│  │     <param><value><int>10</int></value></param>                   │          │
│  │     <param><value><int>32</int></value></param>                   │          │
│  │   </params>                                                        │          │
│  │ </methodCall>                                                      │          │
│  └───────────────────────────────────────────────────────────────────┘          │
│                                                                                 │
│  gRPC/Protobuf (~18 bytes):                                                     │
│  ┌───────────────────────────────────────────────────────────────────┐          │
│  │ 09 00 00 00 00 00 00 24 40 11 00 00 00 00 00 00 40 40            │          │
│  │ (field 1: 10.0)        (field 2: 32.0)                            │          │
│  └───────────────────────────────────────────────────────────────────┘          │
│                                                                                 │
│  Size ratio:  JSON-RPC ≈ 3x protobuf, XML-RPC ≈ 14x protobuf                    │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## When to Use Which Protocol

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          PROTOCOL SELECTION GUIDE                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   Use JSON-RPC when:                                                            │
│   ├── Building web APIs with browser clients                                    │
│   ├── Debugging is a priority (human-readable)                                  │
│   ├── Schema flexibility is needed                                              │
│   └── Working with JavaScript/TypeScript                                        │
│                                                                                 │
│   Use XML-RPC when:                                                             │
│   ├── Integrating with legacy systems (WordPress, Bugzilla)                     │
│   ├── Enterprise systems requiring SOAP-like structure                          │
│   └── Existing XML-RPC infrastructure                                           │
│                                                                                 │
│   Use gRPC when:                                                                │
│   ├── Building microservices (service-to-service)                               │
│   ├── Performance is critical                                                   │
│   ├── Streaming data is required                                                │
│   ├── Strong typing and schema evolution are needed                             │
│   └── Polyglot environments (multiple languages)                                │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

*See `docs/misconceptions.md` for common errors with RPC protocols.*
