# Diagrams — Week 12
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

This folder contains architectural diagrams for Week 12 concepts.

---

## Why ASCII Diagrams?

1. **Version control friendly** — Diffs are meaningful
2. **Accessible** — Works in terminals and screen readers
3. **Portable** — No external dependencies
4. **Editable** — Students can modify and learn

---

## Diagram 1: SMTP Protocol Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    SMTP PROTOCOL FLOW                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   CLIENT                                        SERVER           │
│     │                                             │              │
│     │◄────────────── 220 Ready ──────────────────│  Connection  │
│     │                                             │              │
│     │────────────── EHLO client ────────────────►│              │
│     │◄────────────── 250 OK ─────────────────────│  Greeting    │
│     │                                             │              │
│     │────── MAIL FROM:<sender@test.com> ────────►│              │
│     │◄────────────── 250 OK ─────────────────────│  Envelope    │
│     │                                             │              │
│     │────── RCPT TO:<recipient@test.com> ───────►│              │
│     │◄────────────── 250 OK ─────────────────────│              │
│     │                                             │              │
│     │─────────────── DATA ──────────────────────►│              │
│     │◄──────────── 354 Start input ──────────────│  Data Phase  │
│     │                                             │              │
│     │─────────── Subject: Test ─────────────────►│              │
│     │─────────── (message body) ────────────────►│              │
│     │──────────────── . ────────────────────────►│  End         │
│     │◄────────────── 250 OK ─────────────────────│              │
│     │                                             │              │
│     │─────────────── QUIT ──────────────────────►│              │
│     │◄────────────── 221 Bye ────────────────────│  Disconnect  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Key Response Codes:
  220 = Service ready       354 = Start mail input (NOT 250!)
  250 = Command successful  221 = Closing connection
```

---

## Diagram 2: RPC Architecture Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                   RPC ARCHITECTURE LAYERS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   CLIENT SIDE                           SERVER SIDE              │
│   ══════════                            ═══════════              │
│                                                                  │
│   ┌──────────────┐                      ┌──────────────┐        │
│   │ Application  │   result = add(a,b)  │ Application  │        │
│   │    Code      │◄────────────────────►│    Code      │        │
│   └──────┬───────┘                      └──────┬───────┘        │
│          │                                     │                 │
│          ▼                                     ▼                 │
│   ┌──────────────┐                      ┌──────────────┐        │
│   │ Client Stub  │   Serialise/         │ Server Stub  │        │
│   │  (Proxy)     │   Deserialise        │  (Skeleton)  │        │
│   └──────┬───────┘                      └──────┬───────┘        │
│          │                                     │                 │
│          ▼                                     ▼                 │
│   ┌──────────────┐                      ┌──────────────┐        │
│   │  Transport   │══════════════════════│  Transport   │        │
│   │  (HTTP/TCP)  │◄═════════════════════│  (HTTP/TCP)  │        │
│   └──────────────┘   Network Request    └──────────────┘        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Diagram 3: Protocol Comparison

```
┌─────────────────────────────────────────────────────────────────┐
│                  RPC PROTOCOL COMPARISON                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   JSON-RPC 2.0           XML-RPC              gRPC               │
│   ════════════          ════════             ══════              │
│                                                                  │
│   ┌──────────────┐     ┌──────────────┐    ┌──────────────┐     │
│   │    JSON      │     │     XML      │    │   Protobuf   │     │
│   │   (Text)     │     │   (Text)     │    │   (Binary)   │     │
│   │  ~45 bytes   │     │  ~200 bytes  │    │  ~15 bytes   │     │
│   └──────┬───────┘     └──────┬───────┘    └──────┬───────┘     │
│          │                    │                   │              │
│          ▼                    ▼                   ▼              │
│   ┌──────────────┐     ┌──────────────┐    ┌──────────────┐     │
│   │   HTTP/1.1   │     │   HTTP/1.1   │    │   HTTP/2     │     │
│   │  Port 6200   │     │  Port 6201   │    │  Port 6251   │     │
│   └──────────────┘     └──────────────┘    └──────────────┘     │
│                                                                  │
│   Best for:            Best for:           Best for:             │
│   • Public APIs        • Legacy systems    • Microservices       │
│   • Browser clients    • WordPress         • Mobile apps         │
│   • Debugging          • Enterprise        • High performance    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Diagram 4: Week 12 Lab Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                 WEEK 12 LABORATORY ARCHITECTURE                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Windows Host                                                   │
│   ┌─────────────┐   ┌─────────────┐                             │
│   │  Wireshark  │   │  Browser    │                             │
│   │  (Capture)  │   │  Portainer  │                             │
│   └──────┬──────┘   └──────┬──────┘                             │
│          │    vEthernet    │    localhost:9000                   │
│   ═══════╪═════════════════╪════════════════════════════════    │
│                                                                  │
│   WSL2 + Ubuntu 22.04                                            │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │               Docker Network (week12_net)                │   │
│   │                  172.28.12.0/24                          │   │
│   │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────┐ │   │
│   │  │   SMTP    │  │ JSON-RPC  │  │  XML-RPC  │  │ gRPC  │ │   │
│   │  │  :1025    │  │  :6200    │  │  :6201    │  │ :6251 │ │   │
│   │  └───────────┘  └───────────┘  └───────────┘  └───────┘ │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│   Reserved: Port 9000 = Portainer (NEVER use for lab services)  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tools for Creating ASCII Diagrams

| Tool | Platform | URL |
|------|----------|-----|
| ASCIIFlow | Web | https://asciiflow.com |
| Monodraw | macOS | https://monodraw.helftone.com |
| textik | Web | https://textik.com |

---

## See Also

- `docs/theory_summary.md` — Protocol specifications
- `docs/misconceptions.md` — Common errors
- `README.md` — Architecture overview

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
