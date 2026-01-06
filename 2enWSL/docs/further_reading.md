# Further Reading — Week 2

> NETWORKING class - ASE, Informatics | by Revolvix

## Core Textbooks

### Computer Networking: A Top-Down Approach
**Authors:** James F. Kurose and Keith W. Ross  
**Edition:** 8th Edition (2021)  
**Publisher:** Pearson

The definitive textbook for understanding computer networks from the application layer downward. Chapters 2 and 3 are particularly relevant for this week's topics.

**Key Chapters:**
- Chapter 1: Computer Networks and the Internet
- Chapter 2: Application Layer
- Chapter 3: Transport Layer (TCP and UDP)

---

### UNIX Network Programming, Volume 1
**Authors:** W. Richard Stevens, Bill Fenner, Andrew M. Rudoff  
**Edition:** 3rd Edition (2004)  
**Publisher:** Addison-Wesley

The authoritative reference for socket programming. Though focused on UNIX/C, the concepts translate directly to Python.

**Key Chapters:**
- Chapter 2: The Transport Layer: TCP, UDP, and SCTP
- Chapter 4: Elementary TCP Sockets
- Chapter 8: Elementary UDP Sockets

---

### Foundations of Python Network Programming
**Authors:** Brandon Rhodes and John Goerzen  
**Edition:** 3rd Edition (2014)  
**Publisher:** Apress

Practical Python networking with modern practices.

**Key Chapters:**
- Chapter 2: UDP
- Chapter 3: TCP
- Chapter 7: Server Architecture

---

## RFCs (Request for Comments)

The authoritative specifications for Internet protocols.

### RFC 793 — Transmission Control Protocol
https://tools.ietf.org/html/rfc793

The original TCP specification defining connection establishment, data transfer, and connection termination.

**Key Sections:**
- Section 3.2: Terminology
- Section 3.4: Sequence Numbers
- Section 3.5: Connection Establishment

---

### RFC 768 — User Datagram Protocol
https://tools.ietf.org/html/rfc768

The UDP specification — notably concise at just three pages.

---

### RFC 1122 — Requirements for Internet Hosts
https://tools.ietf.org/html/rfc1122

Clarifications and requirements for TCP/IP implementations.

---

## Online Resources

### Python Documentation

**socket — Low-level networking interface**  
https://docs.python.org/3/library/socket.html

**socketserver — A framework for network servers**  
https://docs.python.org/3/library/socketserver.html

**selectors — High-level I/O multiplexing**  
https://docs.python.org/3/library/selectors.html

---

### Docker Networking

**Docker Network Documentation**  
https://docs.docker.com/network/

**Container Networking Model**  
https://docs.docker.com/engine/extend/plugins_network/

---

### Wireshark Resources

**Wireshark User's Guide**  
https://www.wireshark.org/docs/wsug_html_chunked/

**Display Filter Reference**  
https://www.wireshark.org/docs/dfref/

**Sample Captures**  
https://wiki.wireshark.org/SampleCaptures

---

## Video Tutorials

### Computerphile
https://www.youtube.com/user/Computerphile

Excellent short-form explanations of networking concepts:
- "TCP Meltdown" — Understanding TCP behaviour
- "UDP and TCP" — Protocol comparison
- "How ARP Works" — Address resolution

---

### Ben Eater
https://www.youtube.com/c/BenEater

Deep technical explanations:
- "Networking tutorial" series — Building networks from first principles

---

## Interactive Learning

### Beej's Guide to Network Programming
https://beej.us/guide/bgnet/

A classic, freely available guide to socket programming in C. The concepts apply directly to Python.

---

### Computer Networking: Principles, Protocols and Practice
https://www.computer-networking.info/

Open-source networking textbook with interactive exercises.

---

## Research Papers

### The Design Philosophy of the DARPA Internet Protocols
**Author:** David D. Clark  
**Publication:** SIGCOMM '88

Essential reading for understanding why TCP/IP was designed the way it was.

---

### Congestion Avoidance and Control
**Author:** Van Jacobson  
**Publication:** SIGCOMM '88

The paper that saved the Internet from congestion collapse.

---

## Tools Documentation

### tcpdump
https://www.tcpdump.org/manpages/tcpdump.1.html

The canonical packet capture tool for command-line analysis.

---

### netcat (nc)
https://nc110.sourceforge.io/

The "Swiss Army knife" of networking — useful for quick TCP/UDP testing.

---

### tshark
https://www.wireshark.org/docs/man-pages/tshark.html

Command-line version of Wireshark for scriptable analysis.

---

## Suggested Learning Path

### Beginner
1. Kurose & Ross, Chapters 1–3
2. Python socket module documentation
3. Beej's Guide (skim for concepts)

### Intermediate
1. UNIX Network Programming, Chapters 2, 4, 8
2. RFC 793 (TCP specification)
3. Wireshark User's Guide

### Advanced
1. Stevens, TCP/IP Illustrated, Volume 1
2. Research papers on TCP congestion control
3. RFC 1122 and related clarifications

---

## Practice Platforms

### Hack The Box
https://www.hackthebox.com/

Network security challenges that require understanding protocols.

---

### TryHackMe
https://tryhackme.com/

Guided rooms for network analysis and packet capture.

---

### PicoCTF
https://picoctf.org/

CTF challenges including networking fundamentals.

---

## Academic Journals

For those pursuing research:

- **IEEE/ACM Transactions on Networking**
- **ACM SIGCOMM Conference Proceedings**
- **IEEE INFOCOM Conference Proceedings**

---

*NETWORKING class - ASE, Informatics | by Revolvix*
