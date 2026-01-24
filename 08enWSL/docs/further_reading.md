# Further Reading — Week 8: Transport Layer & HTTP

> NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

---

## Priority Reading

These resources are most relevant to this week's exercises:

### Essential RFCs

| RFC | Title | Why Read It |
|-----|-------|-------------|
| [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110) | HTTP Semantics | Definitive HTTP reference |
| [RFC 9112](https://www.rfc-editor.org/rfc/rfc9112) | HTTP/1.1 | Message syntax and routing |
| [RFC 793](https://www.rfc-editor.org/rfc/rfc793) | TCP Specification | Understanding TCP internals |
| [RFC 768](https://www.rfc-editor.org/rfc/rfc768) | UDP Specification | Short read, complete protocol |

### Textbook Chapters

**Kurose & Ross — Computer Networking: A Top-Down Approach (8th ed.)**
- Chapter 3: Transport Layer (pp. 185-268)
  - 3.1: Transport-layer services
  - 3.3: Connectionless transport: UDP
  - 3.4: Principles of reliable data transfer
  - 3.5: Connection-oriented transport: TCP
  - 3.7: TCP congestion control

**Tanenbaum & Wetherall — Computer Networks (5th ed.)**
- Chapter 6: The Transport Layer (pp. 532-618)

---

## HTTP Detailed Examination

### HTTP/1.1

- [MDN HTTP Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP) — Practical HTTP reference
- [High Performance Browser Networking](https://hpbn.co/http1x/) — HTTP/1.x optimisation

### HTTP/2 and HTTP/3

- [RFC 9113](https://www.rfc-editor.org/rfc/rfc9113) — HTTP/2 specification
- [RFC 9114](https://www.rfc-editor.org/rfc/rfc9114) — HTTP/3 specification
- [HTTP/2 Explained](https://daniel.haxx.se/http2/) — Free book by curl author
- [HTTP/3 Explained](https://http3-explained.haxx.se/) — Free book on QUIC/HTTP/3

---

## Reverse Proxy and Load Balancing

### nginx

- [nginx Documentation](https://nginx.org/en/docs/) — Official documentation
- [nginx Beginner's Guide](https://nginx.org/en/docs/beginners_guide.html) — Quick start
- [nginx Load Balancing](https://nginx.org/en/docs/http/load_balancing.html) — Upstream configuration
- [nginx Reverse Proxy](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/) — Proxy configuration

### Load Balancing Concepts

- [HAProxy Documentation](https://www.haproxy.org/download/2.8/doc/configuration.txt) — Alternative load balancer
- [Introduction to Load Balancing](https://www.nginx.com/resources/glossary/load-balancing/) — Conceptual overview

---

## TCP/IP Internals

### Protocol Analysis

- [TCP/IP Illustrated, Vol. 1](https://www.amazon.com/TCP-Illustrated-Protocols-Addison-Wesley-Professional/dp/0321336313) — Stevens' classic
- [Wireshark User's Guide](https://www.wireshark.org/docs/wsug_html_chunked/) — Packet analysis

### Socket Programming

- [Beej's Guide to Network Programming](https://beej.us/guide/bgnet/) — Classic C sockets tutorial
- [Python Socket Programming](https://docs.python.org/3/library/socket.html) — Official Python docs
- [Real Python: Socket Programming](https://realpython.com/python-sockets/) — Python tutorial

---

## Security

### TLS/HTTPS

- [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446) — TLS 1.3 specification
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/) — Free certificates
- [SSL Labs](https://www.ssllabs.com/ssltest/) — TLS configuration testing

### Web Security

- [OWASP Top Ten](https://owasp.org/www-project-top-ten/) — Common vulnerabilities
- [OWASP Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal) — Directory traversal attacks

---

## Tools Documentation

### Docker

- [Docker Documentation](https://docs.docker.com/) — Official docs
- [Docker Compose](https://docs.docker.com/compose/) — Multi-container orchestration
- [Docker Networking](https://docs.docker.com/network/) — Network configuration

### curl

- [curl Manual](https://curl.se/docs/manual.html) — Complete reference
- [Everything curl](https://everything.curl.dev/) — Free book

### Wireshark

- [Wireshark User's Guide](https://www.wireshark.org/docs/wsug_html_chunked/)
- [Display Filter Reference](https://www.wireshark.org/docs/dfref/)

---

## Academic Papers

### Load Balancing

- Cardellini, V., Colajanni, M., & Yu, P. S. (1999). Dynamic load balancing on web-server systems. *IEEE Internet Computing*, 3(3), 28-39.

### HTTP Performance

- Fielding, R. T., & Reschke, J. (2014). Hypertext Transfer Protocol (HTTP/1.1): Message Syntax and Routing. RFC 7230.

### TCP Congestion Control

- Jacobson, V. (1988). Congestion avoidance and control. *ACM SIGCOMM Computer Communication Review*, 18(4), 314-329.

---

## Video Resources

### YouTube Channels

- [Computerphile](https://www.youtube.com/user/Computerphile) — Networking concepts explained
- [Ben Eater](https://www.youtube.com/c/BenEater) — Low-level networking

### Specific Videos

- [TCP Handshake Explained](https://www.youtube.com/watch?v=HCHFX5O1IaQ)
- [How HTTPS Works](https://www.youtube.com/watch?v=T4Df5_cojAs)

---

## Interactive Learning

### Practice Platforms

- [Katacoda](https://www.katacoda.com/) — Interactive Docker/Linux scenarios
- [OverTheWire: Bandit](https://overthewire.org/wargames/bandit/) — Linux command line practice
- [Hack The Box](https://www.hackthebox.eu/) — Security challenges

### Online Courses

- [Coursera: Computer Networking](https://www.coursera.org/learn/computer-networking) — Stanford course
- [MIT OpenCourseWare 6.829](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-829-computer-networks-fall-2002/) — Graduate networking

---

## Reading Order Suggestion

For Week 8 specifically:

1. **Start with:** Kurose & Ross Chapter 3.1-3.5 (TCP fundamentals)
2. **Then read:** nginx Load Balancing documentation
3. **For exercises:** Beej's Guide (socket programming sections)
4. **For security:** OWASP Path Traversal article
5. **Optional detailed examination:** RFC 9110 (HTTP Semantics)

---

## Related Course Documents

- [docs/theory_summary.md](theory_summary.md) — Week 8 theoretical concepts
- [docs/glossary.md](glossary.md) — Term definitions
- [docs/misconceptions.md](misconceptions.md) — Common mistakes to avoid

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
