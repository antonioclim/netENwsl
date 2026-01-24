# 📚 Further Reading — Week 9

> Session Layer (L5) and Presentation Layer (L6)
> NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

This document provides additional resources for deeper exploration of the
concepts covered in Week 9.

---

## 📖 Primary References

### RFC Documents (Internet Standards)

| RFC | Title | Relevance |
|-----|-------|-----------|
| [RFC 959](https://tools.ietf.org/html/rfc959) | File Transfer Protocol | FTP specification, session management |
| [RFC 2228](https://tools.ietf.org/html/rfc2228) | FTP Security Extensions | AUTH, PROT commands |
| [RFC 2389](https://tools.ietf.org/html/rfc2389) | Feature Negotiation for FTP | FEAT, OPTS commands |
| [RFC 3659](https://tools.ietf.org/html/rfc3659) | Extensions to FTP | MDTM, SIZE, REST commands |
| [RFC 4217](https://tools.ietf.org/html/rfc4217) | FTP over TLS | Secure FTP sessions |

### Core Textbooks

| Title | Author(s) | Chapters | Notes |
|-------|-----------|----------|-------|
| *Computer Networks* (5th ed.) | Tanenbaum & Wetherall | Ch. 7: Application Layer | FTP protocol details |
| *TCP/IP Illustrated, Vol. 1* | Stevens | Ch. 27: FTP | Implementation-level view |
| *Unix Network Programming* | Stevens et al. | Ch. 6: I/O Multiplexing | Socket programming patterns |
| *Computer Networking: A Top-Down Approach* | Kurose & Ross | Ch. 2: Application Layer | Conceptual foundation |

---

## 🏫 Resources Available at ASE Library

### Physical Books (Central Library, Floor 3)

| Title | Author | Call Number | Copies |
|-------|--------|-------------|--------|
| Computer Networks | Tanenbaum, A. | 004.7/T15 | 3 |
| TCP/IP Illustrated Vol. 1 | Stevens, W.R. | 004.738/S84 | 2 |
| Unix Network Programming | Stevens, W.R. | 004.43/S84 | 1 |
| Data Communications | Stallings, W. | 004.6/S78 | 2 |
| Network Security Essentials | Stallings, W. | 004.056/S78 | 1 |

### Electronic Resources (Access with ASE Credentials)

| Resource | URL | Access |
|----------|-----|--------|
| IEEE Xplore | ieeexplore.ieee.org | Via ASE proxy |
| ACM Digital Library | dl.acm.org | Via ASE proxy |
| Springer Link | link.springer.com | Institutional subscription |
| O'Reilly Online | learning.oreilly.com | Check library portal |
| Safari Books | safaribooksonline.com | Check library portal |

**Access from home:** Use VPN or proxy settings from the library portal.

---

## 🎬 Video Resources

### Conceptual Understanding

| Topic | Platform | Duration | Notes |
|-------|----------|----------|-------|
| OSI Model Explained | YouTube | ~15 min | Search "OSI 7 layers explained" |
| FTP Protocol Deep Dive | YouTube | ~20 min | Search "FTP protocol wireshark" |
| Binary Data and Endianness | YouTube | ~10 min | Search "endianness explained" |
| Socket Programming | YouTube | ~30 min | Search "Python socket tutorial" |

### Practical Tutorials

| Topic | Platform | Notes |
|-------|----------|-------|
| Wireshark FTP Analysis | YouTube | Search "wireshark FTP capture" |
| Docker Networking | YouTube | Search "docker networking basics" |
| Python struct Module | YouTube | Search "python struct pack unpack" |

---

## 🔧 Technical Documentation

### Python Libraries

| Library | Documentation | Purpose |
|---------|---------------|---------|
| `struct` | [docs.python.org/3/library/struct.html](https://docs.python.org/3/library/struct.html) | Binary packing/unpacking |
| `socket` | [docs.python.org/3/library/socket.html](https://docs.python.org/3/library/socket.html) | Network programming |
| `ftplib` | [docs.python.org/3/library/ftplib.html](https://docs.python.org/3/library/ftplib.html) | FTP client |
| `pyftpdlib` | [pyftpdlib.readthedocs.io](https://pyftpdlib.readthedocs.io/) | FTP server |
| `zlib` | [docs.python.org/3/library/zlib.html](https://docs.python.org/3/library/zlib.html) | CRC-32 checksums |

### Tools

| Tool | Documentation | Purpose |
|------|---------------|---------|
| Wireshark | [wireshark.org/docs](https://www.wireshark.org/docs/) | Packet analysis |
| Docker | [docs.docker.com](https://docs.docker.com/) | Containerisation |
| Docker Compose | [docs.docker.com/compose](https://docs.docker.com/compose/) | Multi-container apps |

---

## 📝 Academic Papers

### Session Layer Concepts

1. **Day, J.D. & Zimmermann, H.** (1983). "The OSI Reference Model."
   *Proceedings of the IEEE*, 71(12), 1334-1340.
   - Historical context of OSI model layers

2. **Saltzer, J.H., Reed, D.P. & Clark, D.D.** (1984). "End-to-End Arguments in System Design."
   *ACM Transactions on Computer Systems*, 2(4), 277-288.
   - Foundational paper on protocol layering

### Binary Protocol Design

1. **Mogul, J. et al.** (1997). "HTTP/1.1 Protocol."
   *RFC 2616*
   - Text vs binary protocol design decisions

2. **Google** (2008). "Protocol Buffers."
   - Modern binary serialisation approach

### Network Security

1. **Rescorla, E.** (2018). "The Transport Layer Security (TLS) Protocol Version 1.3."
   *RFC 8446*
   - Session security in modern protocols

---

## 🌐 Online Courses

### Free Resources

| Course | Platform | Level |
|--------|----------|-------|
| Computer Networking | Coursera (Stanford) | Intermediate |
| Introduction to Computer Networks | edX (Microsoft) | Beginner |
| Networking Fundamentals | Cisco Networking Academy | Beginner |
| Practical Networking | YouTube (various) | All levels |

### Certification Paths

| Certification | Organisation | Relevance |
|---------------|--------------|-----------|
| CCNA | Cisco | Network fundamentals |
| CompTIA Network+ | CompTIA | Vendor-neutral networking |
| AWS Certified Solutions Architect | Amazon | Cloud networking |

---

## 💡 Practice Resources

### Online Labs

| Platform | URL | Type |
|----------|-----|------|
| Cisco Packet Tracer | netacad.com | Network simulation |
| GNS3 | gns3.com | Network emulation |
| Katacoda (Docker) | katacoda.com | Interactive tutorials |
| OverTheWire | overthewire.org | Security challenges |

### Capture Files for Analysis

| Source | URL | Content |
|--------|-----|---------|
| Wireshark Sample Captures | wiki.wireshark.org/SampleCaptures | Various protocols |
| PacketLife.net | packetlife.net/captures | Network scenarios |
| Netresec | netresec.com | Security-focused |

---

## 🔗 Related Laboratory Topics

| Week | Topic | Connection to Week 9 |
|------|-------|---------------------|
| 7 | Transport Layer (TCP) | Foundation for sessions |
| 8 | Transport Layer (UDP) | Connectionless comparison |
| 10 | Application Layer (HTTP) | Higher-level protocols |
| 11 | Application Layer (DNS) | Name resolution |
| 12 | Security Protocols | Session encryption |

---

## 📋 Recommended Reading Order

For Week 9 specifically:

1. **Before lab:** Read RFC 959 Sections 1-3 (FTP overview)
2. **During lab:** Reference `struct` module documentation
3. **After lab:** Read Tanenbaum Chapter 7 on Application Layer
4. **For homework:** Review Wireshark FTP analysis tutorials

---

## 🆘 Getting Help

- **Technical Issues:** Open an issue on GitHub
- **Course Questions:** Post on Moodle forum
- **Office Hours:** Check course schedule on Moodle

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Week 9: Session Layer and Presentation Layer*
