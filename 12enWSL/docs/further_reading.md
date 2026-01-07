# Further Reading — Week 12

> NETWORKING class - ASE, Informatics | by Revolvix

Additional resources for deepening your understanding of email protocols and RPC architectures.

---

## SMTP and Email Protocols

### RFC Specifications

| RFC | Title | Description |
|-----|-------|-------------|
| [RFC 5321](https://datatracker.ietf.org/doc/html/rfc5321) | Simple Mail Transfer Protocol | Core SMTP specification (obsoletes RFC 2821) |
| [RFC 5322](https://datatracker.ietf.org/doc/html/rfc5322) | Internet Message Format | Email message structure and headers |
| [RFC 2045](https://datatracker.ietf.org/doc/html/rfc2045) | MIME Part One | Multipurpose Internet Mail Extensions basics |
| [RFC 2046](https://datatracker.ietf.org/doc/html/rfc2046) | MIME Part Two | Media types and multipart messages |
| [RFC 8314](https://datatracker.ietf.org/doc/html/rfc8314) | Email TLS | Cleartext considered obsolete |
| [RFC 6409](https://datatracker.ietf.org/doc/html/rfc6409) | Message Submission | Port 587 and authenticated relay |

### Related Protocols

| RFC | Title | Description |
|-----|-------|-------------|
| [RFC 1939](https://datatracker.ietf.org/doc/html/rfc1939) | POP3 | Post Office Protocol version 3 |
| [RFC 9051](https://datatracker.ietf.org/doc/html/rfc9051) | IMAP | Internet Message Access Protocol |
| [RFC 7489](https://datatracker.ietf.org/doc/html/rfc7489) | DMARC | Domain-based Message Authentication |
| [RFC 7208](https://datatracker.ietf.org/doc/html/rfc7208) | SPF | Sender Policy Framework |
| [RFC 6376](https://datatracker.ietf.org/doc/html/rfc6376) | DKIM | DomainKeys Identified Mail |

### Tutorials and Articles

- [How Email Works](https://computer.howstuffworks.com/e-mail-messaging/email.htm) — HowStuffWorks overview
- [SMTP Protocol Explained](https://mailtrap.io/blog/smtp/) — Mailtrap comprehensive guide
- [Building an Email Server](https://www.digitalocean.com/community/tutorials/how-to-configure-postfix-as-a-send-only-smtp-server-on-ubuntu-20-04) — DigitalOcean Postfix tutorial
- [Email Security Best Practices](https://www.cloudflare.com/learning/email-security/email-security-best-practices/) — Cloudflare guide

### Python Libraries

- [smtplib](https://docs.python.org/3/library/smtplib.html) — Python standard library SMTP client
- [email](https://docs.python.org/3/library/email.html) — Python email message handling
- [aiosmtpd](https://aiosmtpd.readthedocs.io/) — Async SMTP server framework
- [Python-emails](https://github.com/lavr/python-emails) — Modern email handling

---

## JSON-RPC

### Specifications

| Document | Description |
|----------|-------------|
| [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification) | Official specification |
| [JSON-RPC 1.0](https://www.jsonrpc.org/specification_v1) | Legacy version (for comparison) |
| [JSON Schema](https://json-schema.org/) | Validating JSON structures |

### Implementation Guides

- [JSON-RPC 2.0 Tutorial](https://www.tutorialspoint.com/json-rpc/index.htm) — TutorialsPoint introduction
- [Building a JSON-RPC Server](https://realpython.com/python-json-api/) — Real Python guide
- [JSON-RPC vs REST](https://nordicapis.com/json-rpc-vs-rest-whats-the-difference/) — Nordic APIs comparison

### Python Libraries

- [jsonrpclib-pelix](https://pypi.org/project/jsonrpclib-pelix/) — Full JSON-RPC 2.0 implementation
- [json-rpc](https://pypi.org/project/json-rpc/) — Framework-agnostic library
- [aiohttp-json-rpc](https://pypi.org/project/aiohttp-json-rpc/) — Async JSON-RPC

### Error Codes Reference

| Code | Message | Meaning |
|------|---------|---------|
| -32700 | Parse error | Invalid JSON |
| -32600 | Invalid Request | Not a valid request object |
| -32601 | Method not found | Method does not exist |
| -32602 | Invalid params | Invalid method parameters |
| -32603 | Internal error | Internal JSON-RPC error |
| -32000 to -32099 | Server error | Implementation-defined errors |

---

## XML-RPC

### Specifications

| Document | Description |
|----------|-------------|
| [XML-RPC Specification](http://xmlrpc.com/spec.md) | Original Dave Winer specification |
| [XML-RPC Wikipedia](https://en.wikipedia.org/wiki/XML-RPC) | Historical context and overview |

### Data Types

| Type | XML Element | Example |
|------|-------------|---------|
| Integer | `<int>` or `<i4>` | `<int>42</int>` |
| Boolean | `<boolean>` | `<boolean>1</boolean>` |
| String | `<string>` | `<string>hello</string>` |
| Double | `<double>` | `<double>3.14</double>` |
| DateTime | `<dateTime.iso8601>` | `<dateTime.iso8601>20240115T09:30:00</dateTime.iso8601>` |
| Base64 | `<base64>` | `<base64>SGVsbG8=</base64>` |
| Array | `<array>` | Contains `<data>` with `<value>` elements |
| Struct | `<struct>` | Contains `<member>` elements |

### Python Libraries

- [xmlrpc](https://docs.python.org/3/library/xmlrpc.html) — Python standard library
- [xmlrpc.client](https://docs.python.org/3/library/xmlrpc.client.html) — Client implementation
- [xmlrpc.server](https://docs.python.org/3/library/xmlrpc.server.html) — Server implementation

### Tutorials

- [Python XML-RPC Tutorial](https://pymotw.com/3/xmlrpc.client/) — PyMOTW comprehensive guide
- [SimpleXMLRPCServer Guide](https://pymotw.com/3/xmlrpc.server/) — Server implementation

---

## gRPC and Protocol Buffers

### Official Documentation

- [gRPC Documentation](https://grpc.io/docs/) — Official guides and tutorials
- [Protocol Buffers Documentation](https://protobuf.dev/) — Protobuf official site
- [gRPC Python Quickstart](https://grpc.io/docs/languages/python/quickstart/) — Getting started guide
- [Protocol Buffers Language Guide](https://protobuf.dev/programming-guides/proto3/) — Proto3 syntax

### Specifications

| Document | Description |
|----------|-------------|
| [gRPC Core Concepts](https://grpc.io/docs/what-is-grpc/core-concepts/) | Architecture overview |
| [HTTP/2 Specification](https://httpwg.org/specs/rfc9113.html) | Transport layer (RFC 9113) |
| [Protocol Buffers Wire Format](https://protobuf.dev/programming-guides/encoding/) | Binary encoding details |

### Tutorials and Courses

- [gRPC Python Tutorial](https://grpc.io/docs/languages/python/basics/) — Official basics tutorial
- [Introduction to gRPC](https://www.youtube.com/watch?v=RoXT_Rkg8LA) — Tech Talk video introduction
- [gRPC vs REST Performance](https://blog.dreamfactory.com/grpc-vs-rest-how-does-grpc-compare-with-traditional-rest-apis/) — DreamFactory comparison

### Python Libraries

- [grpcio](https://pypi.org/project/grpcio/) — gRPC Python package
- [grpcio-tools](https://pypi.org/project/grpcio-tools/) — Protobuf compiler for Python
- [grpcio-reflection](https://pypi.org/project/grpcio-reflection/) — Server reflection support
- [grpcio-health-checking](https://pypi.org/project/grpcio-health-checking/) — Health check protocol

### Tools

- [grpcurl](https://github.com/fullstorydev/grpcurl) — Command-line gRPC client
- [BloomRPC](https://github.com/bloomrpc/bloomrpc) — GUI client for gRPC
- [Postman gRPC](https://learning.postman.com/docs/sending-requests/grpc/grpc-request-interface/) — Postman gRPC support
- [Evans](https://github.com/ktr0731/evans) — Expressive gRPC client

---

## RPC Architecture Comparison

### Academic Papers

- Birrell, A. D., & Nelson, B. J. (1984). *Implementing remote procedure calls*. ACM Transactions on Computer Systems, 2(1), 39-59.
- Srinivasan, R. (1995). *RPC: Remote Procedure Call Protocol Specification Version 2*. RFC 1831.

### Protocol Comparison

| Aspect | JSON-RPC | XML-RPC | gRPC |
|--------|----------|---------|------|
| Encoding | JSON (text) | XML (text) | Protocol Buffers (binary) |
| Transport | HTTP, WebSocket | HTTP | HTTP/2 |
| Type Safety | Runtime | Runtime | Compile-time |
| Streaming | No | No | Yes (bidirectional) |
| Browser Support | Excellent | Good | Limited |
| Schema | Optional | None | Required (.proto) |
| Payload Size | Medium | Large | Small |

### When to Use Each

| Protocol | Best For |
|----------|----------|
| JSON-RPC | Web applications, JavaScript clients, simple APIs |
| XML-RPC | Legacy systems, enterprise integration, SOAP migration |
| gRPC | Microservices, real-time systems, mobile backends |
| REST | Public APIs, hypermedia, resource-oriented design |

---

## General Networking Resources

### Textbooks

- Kurose, J. F., & Ross, K. W. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.
- Tanenbaum, A. S., & Wetherall, D. J. (2021). *Computer Networks* (6th ed.). Pearson.
- Stevens, W. R. (1993). *TCP/IP Illustrated, Volume 1: The Protocols* (2nd ed.). Addison-Wesley.
- Rhodes, B., & Goerzen, J. (2014). *Foundations of Python Network Programming* (3rd ed.). Apress.

### Online Courses

- [Computer Networking](https://www.coursera.org/learn/computer-networking) — Google Career Certificate on Coursera
- [Networking Fundamentals](https://www.udemy.com/course/networking-fundamentals/) — Udemy comprehensive course
- [MIT 6.829: Computer Networks](https://ocw.mit.edu/courses/6-829-computer-networks-fall-2002/) — MIT OpenCourseWare

### Tools Documentation

- [Wireshark User's Guide](https://www.wireshark.org/docs/wsug_html_chunked/) — Official documentation
- [tcpdump Manual](https://www.tcpdump.org/manpages/tcpdump.1.html) — Command reference
- [Docker Documentation](https://docs.docker.com/) — Container platform docs
- [Python asyncio](https://docs.python.org/3/library/asyncio.html) — Async I/O documentation

---

## Video Resources

### YouTube Channels

- [Computerphile](https://www.youtube.com/user/Computerphile) — Computer science concepts
- [Hussein Nasser](https://www.youtube.com/c/HusseinNasser-software-engineering) — Backend engineering
- [TechWorld with Nana](https://www.youtube.com/c/TechWorldwithNana) — DevOps and Docker

### Specific Videos

- [How SMTP Works](https://www.youtube.com/watch?v=PJo5yOtu6o8) — Email protocol explanation
- [gRPC Introduction](https://www.youtube.com/watch?v=gnchfOojMk4) — Golang UK Conference
- [Protocol Buffers Explained](https://www.youtube.com/watch?v=46O73On0gyI) — Tech Primers

---

## Practice Resources

### Online Labs

- [Katacoda](https://www.katacoda.com/) — Interactive learning scenarios (archived)
- [Play with Docker](https://labs.play-with-docker.com/) — Free Docker playground
- [Exercism](https://exercism.org/) — Programming exercises with mentorship

### Challenge Platforms

- [HackerRank](https://www.hackerrank.com/) — Coding challenges
- [LeetCode](https://leetcode.com/) — Algorithm practice
- [PicoCTF](https://picoctf.org/) — Security and networking challenges

---

## Community Resources

### Forums and Q&A

- [Stack Overflow - SMTP Tag](https://stackoverflow.com/questions/tagged/smtp)
- [Stack Overflow - gRPC Tag](https://stackoverflow.com/questions/tagged/grpc)
- [Reddit r/networking](https://www.reddit.com/r/networking/)
- [Reddit r/learnprogramming](https://www.reddit.com/r/learnprogramming/)

### Discord and Slack

- [Python Discord](https://discord.gg/python) — Python community
- [gRPC Slack](https://grpc.slack.com/) — Official gRPC community

---

*NETWORKING class - ASE, Informatics | by Revolvix*
