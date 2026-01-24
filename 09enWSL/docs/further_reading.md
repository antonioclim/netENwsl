# Further Reading: Week 9

> Extended resources for Session Layer (L5) and Presentation Layer (L6)
> NETWORKING class - ASE, Informatics | by Revolvix

---

## Core Textbooks

### Network Fundamentals

1. **Kurose, J.F. & Ross, K.W. (2021)** *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.
   - Chapter 2: Application Layer (FTP coverage)
   - Chapter 3: Transport Layer (TCP fundamentals)
   - Excellent companion website with Wireshark labs

2. **Tanenbaum, A.S. & Wetherall, D.J. (2021)** *Computer Networks* (6th ed.). Pearson.
   - Chapter 7: Application Layer
   - Complete OSI model coverage
   - Strong theoretical foundation

3. **Stevens, W.R. (1994)** *TCP/IP Illustrated, Volume 1: The Protocols*. Addison-Wesley.
   - Classic reference for protocol internals
   - Detailed examination into FTP mechanics
   - Essential for understanding byte-level operations

### Python Network Programming

4. **Rhodes, B. & Goerzen, J. (2014)** *Foundations of Python Network Programming* (3rd ed.). Apress.
   - Chapter 17: FTP
   - Chapter 5: Network Data and Network Errors
   - Practical code examples throughout

5. **Goerzen, J. (2004)** *Foundations of Python Network Programming*. Apress.
   - Older but foundational
   - Excellent struct module coverage

---

## RFC Documents (Standards)

### FTP Protocol

- **RFC 959** - File Transfer Protocol (FTP)
  - https://tools.ietf.org/html/rfc959
  - The definitive FTP specification
  - Essential reading for protocol implementation

- **RFC 2228** - FTP Security Extensions
  - https://tools.ietf.org/html/rfc2228
  - Authentication and encryption extensions

- **RFC 2428** - FTP Extensions for IPv6 and NATs
  - https://tools.ietf.org/html/rfc2428
  - EPSV and EPRT commands

- **RFC 4217** - Securing FTP with TLS
  - https://tools.ietf.org/html/rfc4217
  - FTPS implementation guide

### Data Representation

- **RFC 4506** - XDR: External Data Representation Standard
  - https://tools.ietf.org/html/rfc4506
  - Foundation for network data encoding

- **RFC 1832** - XDR: External Data Representation Standard
  - https://tools.ietf.org/html/rfc1832
  - Earlier version, still useful

---

## Online Resources

### Tutorials and Guides

1. **Python struct Module Documentation**
   - https://docs.python.org/3/library/struct.html
   - Official reference with format string tables

2. **Python ftplib Documentation**
   - https://docs.python.org/3/library/ftplib.html
   - Standard library FTP client

3. **Wireshark FTP Analysis**
   - https://wiki.wireshark.org/FTP
   - Protocol dissection and capture filters

4. **Docker Networking Guide**
   - https://docs.docker.com/network/
   - Container networking fundamentals

### Interactive Learning

5. **Computer Networking Course (Stanford)**
   - https://www.coursera.org/learn/computer-networking
   - Free online course covering OSI layers

6. **The TCP/IP Guide**
   - http://www.tcpipguide.com/
   - Thorough free online reference
   - Excellent diagrams and explanations

---

## Academic Papers

### Session Management

1. **Clark, D.D. (1988)** "The Design Philosophy of the DARPA Internet Protocols"
   - *ACM SIGCOMM Computer Communication Review*, 18(4), 106-114.
   - Foundational paper on protocol design

2. **Saltzer, J.H., Reed, D.P., & Clark, D.D. (1984)** "End-to-End Arguments in System Design"
   - *ACM Transactions on Computer Systems*, 2(4), 277-288.
   - Explains why session management is application-layer

### Data Encoding

3. **Cohen, D. (1981)** "On Holy Wars and a Plea for Peace"
   - USC/ISI IEN 137
   - Classic paper on byte order debates
   - Origin of "big-endian" and "little-endian" terms

### Protocol Design

4. **Postel, J. (1980)** "DoD Standard Transmission Control Protocol"
   - RFC 761
   - Original TCP specification with design rationale

---

## Tools and Software

### FTP Servers

- **vsftpd** - Very Secure FTP Daemon
  - https://security.appspot.com/vsftpd.html
  - Production-grade, security-focused

- **ProFTPD** - Professional FTP Server
  - http://www.proftpd.org/
  - Highly configurable, modular design

- **pyftpdlib** - Python FTP Server Library
  - https://github.com/giampaolo/pyftpdlib
  - Used in this laboratory
  - Excellent for learning and testing

### Network Analysis

- **Wireshark**
  - https://www.wireshark.org/
  - Essential packet capture tool

- **tcpdump**
  - https://www.tcpdump.org/
  - Command-line packet capture

- **netcat (nc)**
  - Network Swiss army knife
  - Testing connections and protocols

### Development Tools

- **Docker**
  - https://www.docker.com/
  - Container platform for isolated testing

- **Portainer**
  - https://www.portainer.io/
  - Docker management GUI

---

## Video Resources

### University Lectures

1. **MIT OpenCourseWare: Computer Networks**
   - https://ocw.mit.edu/
   - Academic-level network courses

2. **Stanford CS144: Introduction to Computer Networking**
   - https://cs144.github.io/
   - Excellent lecture videos and labs

### YouTube Channels

3. **Computerphile**
   - Network protocol explanations
   - Accessible technical content

4. **Ben Eater**
   - Low-level networking concepts
   - Byte-order explanations

---

## Practice Resources

### Hands-on Labs

1. **SEED Labs**
   - https://seedsecuritylabs.org/
   - Network security labs including FTP

2. **Hack The Box**
   - https://www.hackthebox.eu/
   - FTP-related challenges

3. **OverTheWire: Bandit**
   - https://overthewire.org/wargames/bandit/
   - Command-line and networking practice

### Code Repositories

4. **Python Network Programming Examples**
   - https://github.com/brandon-rhodes/fopnp
   - Code from "Foundations of Python Network Programming"

5. **Wireshark Sample Captures**
   - https://wiki.wireshark.org/SampleCaptures
   - FTP captures for analysis practice

---

## Related Topics for Advanced Study

### Session Layer Extensions

- **WebSockets** - Full-duplex session management for web
- **gRPC** - Modern RPC with streaming sessions
- **MQTT** - Lightweight publish/subscribe sessions (IoT)

### Presentation Layer Alternatives

- **Protocol Buffers** - Google's binary serialisation
- **MessagePack** - Efficient binary format
- **CBOR** - Concise Binary Object Representation (IoT)
- **ASN.1** - Abstract Syntax Notation One (telecom)

### Security Extensions

- **TLS/SSL** - Transport Layer Security
- **SSH** - Secure Shell (SFTP)
- **IPsec** - Network layer security

---

## Course-Related Links

### ASE Resources

- **Faculty Website:** https://csie.ase.ro/
- **Course Materials:** See Moodle/internal platform
- **Laboratory Schedule:** Check departmental announcements

### Contact

For questions related to this laboratory:
- Laboratory instructor
- Course coordinator
- Teaching assistants

---

## Citation Format

When referencing materials in academic work:

```
# Book
Kurose, J.F. & Ross, K.W. (2021). Computer Networking: A Top-Down Approach
(8th ed.). Pearson Education.

# RFC
Postel, J. & Reynolds, J. (1985). File Transfer Protocol (FTP) (RFC 959).
Internet Engineering Task Force. https://tools.ietf.org/html/rfc959

# Online Resource
Python Software Foundation. (2024). struct — Interpret bytes as packed
binary data. https://docs.python.org/3/library/struct.html
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
