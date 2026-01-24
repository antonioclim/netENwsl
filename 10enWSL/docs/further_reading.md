# 📚 Further Reading — Week 10
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> HTTP/HTTPS, REST Architecture and Network Services

---

## RFC Specifications (Primary Sources)

### HTTP

| RFC | Title | Notes |
|-----|-------|-------|
| [RFC 7230](https://datatracker.ietf.org/doc/html/rfc7230) | HTTP/1.1: Message Syntax and Routing | Core HTTP/1.1 spec |
| [RFC 7231](https://datatracker.ietf.org/doc/html/rfc7231) | HTTP/1.1: Semantics and Content | Methods, status codes |
| [RFC 7232](https://datatracker.ietf.org/doc/html/rfc7232) | HTTP/1.1: Conditional Requests | Caching validation |
| [RFC 7233](https://datatracker.ietf.org/doc/html/rfc7233) | HTTP/1.1: Range Requests | Partial content |
| [RFC 7234](https://datatracker.ietf.org/doc/html/rfc7234) | HTTP/1.1: Caching | Cache headers |
| [RFC 7235](https://datatracker.ietf.org/doc/html/rfc7235) | HTTP/1.1: Authentication | Auth framework |
| [RFC 7540](https://datatracker.ietf.org/doc/html/rfc7540) | HTTP/2 | Binary framing, multiplexing |
| [RFC 9110](https://datatracker.ietf.org/doc/html/rfc9110) | HTTP Semantics | Updated HTTP semantics (2022) |
| [RFC 9114](https://datatracker.ietf.org/doc/html/rfc9114) | HTTP/3 | QUIC-based HTTP |

### TLS/Security

| RFC | Title | Notes |
|-----|-------|-------|
| [RFC 8446](https://datatracker.ietf.org/doc/html/rfc8446) | TLS 1.3 | Current TLS standard |
| [RFC 5246](https://datatracker.ietf.org/doc/html/rfc5246) | TLS 1.2 | Still widely used |
| [RFC 6066](https://datatracker.ietf.org/doc/html/rfc6066) | TLS Extensions | SNI and others |
| [RFC 5280](https://datatracker.ietf.org/doc/html/rfc5280) | X.509 PKI | Certificate format |

### DNS

| RFC | Title | Notes |
|-----|-------|-------|
| [RFC 1034](https://datatracker.ietf.org/doc/html/rfc1034) | Domain Names - Concepts | DNS architecture |
| [RFC 1035](https://datatracker.ietf.org/doc/html/rfc1035) | Domain Names - Implementation | DNS protocol details |
| [RFC 8484](https://datatracker.ietf.org/doc/html/rfc8484) | DNS over HTTPS (DoH) | Encrypted DNS |
| [RFC 7858](https://datatracker.ietf.org/doc/html/rfc7858) | DNS over TLS (DoT) | Encrypted DNS |

### SSH

| RFC | Title | Notes |
|-----|-------|-------|
| [RFC 4251](https://datatracker.ietf.org/doc/html/rfc4251) | SSH Protocol Architecture | Overview |
| [RFC 4252](https://datatracker.ietf.org/doc/html/rfc4252) | SSH Authentication Protocol | Auth methods |
| [RFC 4253](https://datatracker.ietf.org/doc/html/rfc4253) | SSH Transport Layer Protocol | Encryption, integrity |
| [RFC 4254](https://datatracker.ietf.org/doc/html/rfc4254) | SSH Connection Protocol | Channels, forwarding |

### FTP

| RFC | Title | Notes |
|-----|-------|-------|
| [RFC 959](https://datatracker.ietf.org/doc/html/rfc959) | FTP Specification | Core FTP protocol |
| [RFC 2228](https://datatracker.ietf.org/doc/html/rfc2228) | FTP Security Extensions | AUTH, security |
| [RFC 4217](https://datatracker.ietf.org/doc/html/rfc4217) | FTP over TLS | FTPS |

---

## Textbooks

### Networking Fundamentals

- **Kurose, J. & Ross, K.** (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.
  - Chapter 2: Application Layer (HTTP, DNS, FTP)
  - Chapter 8: Security (TLS, certificates)

- **Tanenbaum, A. & Wetherall, D.** (2021). *Computer Networks* (6th ed.). Pearson.
  - Application layer protocols overview
  - Security protocols

### Python Network Programming

- **Rhodes, B. & Goetzen, J.** (2014). *Foundations of Python Network Programming* (3rd ed.). Apress.
  - HTTP clients and servers
  - TLS/SSL in Python
  - Available online: [Link](https://github.com/brandon-rhodes/fopnp)

### REST API Design

- **Richardson, L. & Ruby, S.** (2007). *RESTful Web Services*. O'Reilly.
  - REST principles and design patterns
  - Richardson Maturity Model origin

- **Masse, M.** (2011). *REST API Design Rulebook*. O'Reilly.
  - Practical API design guidelines

---

## Academic Papers

### REST Architecture

- **Fielding, R. T.** (2000). *Architectural Styles and the Design of Network-based Software Architectures*. Doctoral dissertation, University of California, Irvine.
  - Original REST definition (Chapter 5)
  - [Available online](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm)

### Security

- **Rescorla, E.** (2018). *The Transport Layer Security (TLS) Protocol Version 1.3*. RFC 8446.
  - Complete TLS 1.3 specification with rationale

---

## Online Resources

### HTTP/HTTPS

| Resource | URL | Description |
|----------|-----|-------------|
| MDN HTTP Guide | [developer.mozilla.org/HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP) | Excellent HTTP reference |
| HTTP Status Codes | [httpstatuses.com](https://httpstatuses.com/) | Status code reference |
| Let's Encrypt | [letsencrypt.org](https://letsencrypt.org/) | Free TLS certificates |
| SSL Labs | [ssllabs.com](https://www.ssllabs.com/ssltest/) | TLS configuration testing |

### REST API

| Resource | URL | Description |
|----------|-----|-------------|
| REST API Tutorial | [restfulapi.net](https://restfulapi.net/) | REST design principles |
| JSON API Spec | [jsonapi.org](https://jsonapi.org/) | JSON API standard |
| OpenAPI | [openapis.org](https://www.openapis.org/) | API documentation standard |
| Postman Learning | [learning.postman.com](https://learning.postman.com/) | API testing tutorials |

### DNS

| Resource | URL | Description |
|----------|-----|-------------|
| DNS Explained | [howdns.works](https://howdns.works/) | Visual DNS explanation |
| DNSViz | [dnsviz.net](https://dnsviz.net/) | DNS visualisation tool |
| ICANN | [icann.org](https://www.icann.org/) | DNS governance |

### SSH

| Resource | URL | Description |
|----------|-----|-------------|
| SSH.com Academy | [ssh.com/academy](https://www.ssh.com/academy/ssh) | SSH tutorials |
| OpenSSH Manual | [openssh.com/manual.html](https://www.openssh.com/manual.html) | Official documentation |

---

## Tools Documentation

| Tool | Documentation |
|------|---------------|
| curl | [curl.se/docs/manpage.html](https://curl.se/docs/manpage.html) |
| dig | [bind9.readthedocs.io](https://bind9.readthedocs.io/en/latest/manpages.html#dig-dns-lookup-utility) |
| OpenSSL | [openssl.org/docs](https://www.openssl.org/docs/) |
| Wireshark | [wireshark.org/docs](https://www.wireshark.org/docs/) |
| Paramiko (Python SSH) | [paramiko.org](https://www.paramiko.org/) |
| Requests (Python HTTP) | [requests.readthedocs.io](https://requests.readthedocs.io/) |
| Flask | [flask.palletsprojects.com](https://flask.palletsprojects.com/) |

---

## Video Courses

- **Coursera: Computer Networks** - University of Washington
  - Application layer protocols module

- **YouTube: Computerphile**
  - DNS Explained
  - How HTTPS Works
  - TLS Handshake Explained

- **YouTube: LiveOverflow**
  - Practical security concepts
  - Network protocol analysis

---

## Practice Platforms

| Platform | URL | Focus |
|----------|-----|-------|
| TryHackMe | [tryhackme.com](https://tryhackme.com/) | Network security labs |
| HackTheBox | [hackthebox.com](https://www.hackthebox.com/) | Security challenges |
| PortSwigger Academy | [portswigger.net/web-security](https://portswigger.net/web-security) | Web security |

---

## Recommended Reading Order

### For beginners:
1. MDN HTTP Guide (online)
2. Kurose & Ross, Chapter 2
3. REST API Tutorial (online)
4. howdns.works (visual DNS)

### For deeper understanding:
1. RFC 7231 (HTTP Semantics)
2. Fielding's dissertation, Chapter 5 (REST)
3. RFC 8446 (TLS 1.3)
4. Rhodes & Goetzen book (Python networking)

### For security focus:
1. SSL Labs documentation
2. RFC 8446 (TLS 1.3)
3. PortSwigger Web Security Academy

---

*Computer Networks — Week 10 | ASE, CSIE Bucharest*
*Further reading compiled by ing. dr. Antonio Clim*
