# Further Reading — Week 8

> NETWORKING class - ASE, Informatics | by Revolvix

## Transport Layer Fundamentals

### Textbooks

- **Kurose, J. & Ross, K.** (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
  - Chapter 3: Transport Layer
  - Essential reading on TCP, UDP, and reliable data transfer

- **Tanenbaum, A. & Wetherall, D.** (2011). *Computer Networks* (5th ed.). Pearson.
  - Chapter 6: The Transport Layer
  - Detailed coverage of congestion control and flow control

- **Stevens, W. R.** (1993). *TCP/IP Illustrated, Volume 1: The Protocols*. Addison-Wesley.
  - Classic reference for TCP/IP implementation details
  - Chapters 17-24 cover TCP extensively

### RFC Documents (Standards)

| RFC | Title | Relevance |
|-----|-------|-----------|
| RFC 793 | Transmission Control Protocol | TCP specification |
| RFC 768 | User Datagram Protocol | UDP specification |
| RFC 9293 | TCP (updated) | Modern TCP specification (2022) |
| RFC 5681 | TCP Congestion Control | Slow start, congestion avoidance |
| RFC 7323 | TCP Extensions | Window scaling, timestamps |
| RFC 6298 | Computing TCP Retransmission Timer | RTO calculation |

## HTTP and Web Protocols

### HTTP Standards

| RFC | Title | Description |
|-----|-------|-------------|
| RFC 9110 | HTTP Semantics | Core HTTP concepts |
| RFC 9111 | HTTP Caching | Cache mechanisms |
| RFC 9112 | HTTP/1.1 | Message syntax and routing |
| RFC 9113 | HTTP/2 | Binary framing protocol |
| RFC 9114 | HTTP/3 | QUIC-based HTTP |

### TLS and Security

| RFC | Title | Description |
|-----|-------|-------------|
| RFC 8446 | TLS 1.3 | Current TLS standard |
| RFC 5246 | TLS 1.2 | Widely deployed version |
| RFC 6066 | TLS Extensions | SNI and other extensions |

### Recommended Reading

- **Fielding, R.** (2000). *Architectural Styles and the Design of Network-based Software Architectures*. PhD Thesis.
  - Origin of REST architectural style
  - Available: https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm

- **Grigorik, I.** (2013). *High Performance Browser Networking*. O'Reilly.
  - Excellent coverage of HTTP/2, WebSocket, WebRTC
  - Free online: https://hpbn.co/

## Reverse Proxies and Load Balancing

### nginx Documentation

- **nginx Official Documentation**: https://nginx.org/en/docs/
  - Module reference
  - Configuration examples
  - Best practices

- **nginx Admin's Handbook** by Michał Sapka
  - Comprehensive configuration guide
  - Security hardening

### Load Balancing Concepts

- **Bourke, T.** (2001). *Server Load Balancing*. O'Reilly.
  - Foundational concepts
  - Algorithm explanations

- **HAProxy Documentation**: https://docs.haproxy.org/
  - Alternative load balancer
  - Excellent algorithm documentation

### Load Balancing Algorithms

| Algorithm | Use Case | Characteristics |
|-----------|----------|-----------------|
| Round Robin | General purpose | Simple, equal distribution |
| Weighted Round Robin | Heterogeneous servers | Capacity-aware distribution |
| Least Connections | Variable request duration | Dynamic load awareness |
| IP Hash | Session persistence | Client affinity |
| Random | Large-scale systems | Stateless, simple |
| Consistent Hashing | Distributed caches | Minimal redistribution |

## Python Networking

### Books

- **Rhodes, B. & Goetzen, J.** (2014). *Foundations of Python Network Programming* (3rd ed.). Apress.
  - Comprehensive Python networking guide
  - Socket programming, HTTP, protocols

- **Goerzen, J.** (2004). *Foundations of Python Network Programming*. Apress.
  - Earlier edition, still valuable
  - Low-level networking concepts

### Online Resources

- **Python Socket Documentation**: https://docs.python.org/3/library/socket.html
- **Python http.server Module**: https://docs.python.org/3/library/http.server.html
- **Requests Library**: https://requests.readthedocs.io/

## Docker Networking

### Official Documentation

- **Docker Networking Overview**: https://docs.docker.com/network/
- **Docker Compose Networking**: https://docs.docker.com/compose/networking/
- **Bridge Network Driver**: https://docs.docker.com/network/drivers/bridge/

### Recommended Articles

- **Container Networking Demystified**: Docker Blog series
- **Understanding Docker Networking Drivers**: Official tutorials

## Packet Analysis

### Wireshark Resources

- **Wireshark User's Guide**: https://www.wireshark.org/docs/wsug_html_chunked/
- **Wireshark Display Filter Reference**: https://www.wireshark.org/docs/dfref/
- **Sample Captures**: https://wiki.wireshark.org/SampleCaptures

### Books

- **Sanders, C.** (2017). *Practical Packet Analysis* (3rd ed.). No Starch Press.
  - Wireshark fundamentals
  - Real-world analysis scenarios

- **Orebaugh, A. et al.** (2006). *Wireshark & Ethereal Network Protocol Analyzer Toolkit*. Syngress.
  - In-depth protocol analysis
  - Advanced features

## Performance and Optimisation

### TCP Tuning

- **Mathis, M. et al.** (1997). *The Macroscopic Behavior of the TCP Congestion Avoidance Algorithm*. ACM SIGCOMM.
  - Foundational congestion control paper

- **Cardwell, N. et al.** (2017). *BBR: Congestion-Based Congestion Control*. ACM Queue.
  - Modern congestion control algorithm

### Web Performance

- **Souders, S.** (2007). *High Performance Web Sites*. O'Reilly.
  - Frontend optimisation techniques
  - Still relevant principles

- **Web Vitals**: https://web.dev/vitals/
  - Modern performance metrics
  - Google's performance guidelines

## Academic Papers

### Transport Layer

1. Jacobson, V. (1988). *Congestion Avoidance and Control*. ACM SIGCOMM.
2. Clark, D. (1988). *The Design Philosophy of the DARPA Internet Protocols*. ACM SIGCOMM.
3. Allman, M. et al. (1999). *TCP Congestion Control*. RFC 2581.

### HTTP Evolution

1. Berners-Lee, T. et al. (1996). *Hypertext Transfer Protocol – HTTP/1.0*. RFC 1945.
2. Belshe, M. et al. (2015). *Hypertext Transfer Protocol Version 2 (HTTP/2)*. RFC 7540.
3. Bishop, M. (2022). *HTTP/3*. RFC 9114.

### Load Balancing

1. Karger, D. et al. (1997). *Consistent Hashing and Random Trees*. ACM STOC.
2. Eisenbud, D. et al. (2016). *Maglev: A Fast and Reliable Software Network Load Balancer*. USENIX NSDI.

## Online Courses

### Free Resources

- **Stanford CS144: Introduction to Computer Networking**
  - https://cs144.github.io/
  - Excellent transport layer coverage

- **MIT 6.829: Computer Networks**
  - Research-oriented approach
  - Advanced topics

### Interactive Learning

- **Cloudflare Learning Center**: https://www.cloudflare.com/learning/
  - Accessible explanations
  - Modern web concepts

- **Julia Evans' Networking Zines**: https://jvns.ca/
  - Visual, approachable explanations
  - Practical focus

## Tools and Utilities

| Tool | Purpose | Link |
|------|---------|------|
| Wireshark | Packet analysis | https://www.wireshark.org/ |
| tcpdump | Command-line capture | Built into Linux/macOS |
| curl | HTTP client | https://curl.se/ |
| httpie | Modern HTTP client | https://httpie.io/ |
| wrk | HTTP benchmarking | https://github.com/wg/wrk |
| ab | Apache benchmark | Part of Apache HTTPD |
| siege | Load testing | https://github.com/JoeDog/siege |

---

*NETWORKING class - ASE, Informatics | by Revolvix*
