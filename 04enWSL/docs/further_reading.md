# Further Reading

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

This document provides additional resources for students wishing to deepen their understanding of the Physical Layer, Data Link Layer and custom protocol development.

---

## Core Textbooks

### Primary Reference
- **Kurose, J.F. & Ross, K.W.** (2017). *Computer Networking: A Top-Down Approach* (7th Edition). Pearson.
  - Chapter 5: The Link Layer and LANs
  - Chapter 6: The Physical Layer (available in some editions)

### Network Programming
- **Rhodes, B. & Goetzen, J.** (2014). *Foundations of Python Network Programming* (3rd Edition). Apress.
  - Chapter 2: UDP
  - Chapter 3: TCP
  - Chapter 5: Network Data and Network Errors

### Protocol Design
- **Fall, K.R. & Stevens, W.R.** (2011). *TCP/IP Illustrated, Volume 1: The Protocols* (2nd Edition). Addison-Wesley.
  - Chapter 1: Introduction
  - Chapter 10: User Datagram Protocol (UDP)
  - Chapter 12-20: TCP Fundamentals

---

## RFC Documents

### Fundamental Protocols
| RFC | Title | Relevance |
|-----|-------|-----------|
| RFC 768 | User Datagram Protocol | UDP specification |
| RFC 793 | Transmission Control Protocol | TCP specification |
| RFC 1122 | Requirements for Internet Hosts | Host requirements |
| RFC 3439 | Some Internet Architectural Guidelines | Protocol design principles |

### Error Detection and Framing
| RFC | Title | Relevance |
|-----|-------|-----------|
| RFC 1071 | Computing the Internet Checksum | Checksum algorithms |
| RFC 3309 | Stream Control Transmission Protocol Checksum Change | CRC32 discussion |

### Access RFCs Online
- IETF RFC Repository: https://www.rfc-editor.org/
- RFC Search: https://www.rfc-editor.org/search/rfc_search.php

---

## Academic Papers

### Protocol Design and Analysis
1. **Clark, D.D.** (1988). "The Design Philosophy of the DARPA Internet Protocols." *ACM SIGCOMM Computer Communication Review*, 18(4), 106-114.
   - Foundational paper on Internet protocol design decisions

2. **Saltzer, J.H., Reed, D.P., & Clark, D.D.** (1984). "End-to-End Arguments in System Design." *ACM Transactions on Computer Systems*, 2(4), 277-288.
   - Essential reading on where to place functionality in networked systems

3. **Postel, J.** (1981). "Internet Protocol." RFC 791.
   - Original IP specification, demonstrating protocol documentation standards

### Binary Protocol Design
1. **Mogul, J., & Deering, S.** (1990). "Path MTU Discovery." RFC 1191.
   - Considerations for message size in protocol design

2. **Braden, R. (Ed.)** (1989). "Requirements for Internet Hosts -- Communication Layers." RFC 1122.
   - Protocol implementation guidelines

---

## Online Resources

### Python Network Programming
- **Python Socket Documentation**: https://docs.python.org/3/library/socket.html
- **Python struct Module**: https://docs.python.org/3/library/struct.html
- **Python Real-World Examples**: https://realpython.com/python-sockets/

### Protocol Analysis
- **Wireshark User's Guide**: https://www.wireshark.org/docs/wsug_html_chunked/
- **Wireshark Display Filter Reference**: https://wiki.wireshark.org/DisplayFilters
- **tcpdump Tutorial**: https://danielmiessler.com/study/tcpdump/

### Binary Data Handling
- **Python Binary Data Tutorial**: https://pymotw.com/3/struct/
- **Endianness Explained**: https://betterexplained.com/articles/understanding-big-and-little-endian-byte-order/

---

## Video Resources

### Protocol Fundamentals
- **Computer Networks (Neso Academy)** - YouTube playlist covering OSI layers
- **Ben Eater's Networking Series** - Hardware-level networking explanations
- **Computerphile** - Various videos on protocols and networking concepts

### Wireshark Training
- **Chris Greer's Wireshark Tutorials** - Practical packet analysis
- **Wireshark University** - Official training materials

---

## Practical Exercises Beyond the Lab

### Protocol Implementation Challenges
1. **Implement a Simple ARQ Protocol**
   - Stop-and-wait ARQ over UDP
   - Add sequence numbers and acknowledgments
   - Implement timeout and retransmission

2. **Create a Custom File Transfer Protocol**
   - Design header format for file metadata
   - Implement chunked transfer with checksums
   - Add resume capability

3. **Build a Protocol Analyser**
   - Parse captured packets programmatically
   - Decode custom protocol headers
   - Generate statistics and visualisations

### Network Simulation
- **GNS3**: https://www.gns3.com/ - Network simulation platform
- **Mininet**: http://mininet.org/ - SDN network emulator
- **Packet Tracer**: https://www.netacad.com/courses/packet-tracer - Cisco simulation tool

---

## Error Detection in Detail

### CRC Algorithms
- **CRC RevEng**: https://reveng.sourceforge.io/ - CRC algorithm catalogue
- **CRC Calculator**: https://crccalc.com/ - Online CRC computation
- **Ross Williams' CRC Tutorial**: "A Painless Guide to CRC Error Detection Algorithms"

### Checksum Implementations
```python
# Example: Internet Checksum (RFC 1071)
def internet_checksum(data: bytes) -> int:
    """Calculate Internet checksum as per RFC 1071."""
    if len(data) % 2:
        data += b'\x00'
    
    total = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i + 1]
        total += word
        total = (total & 0xFFFF) + (total >> 16)
    
    return ~total & 0xFFFF
```

---

## Industry Standards and Best Practices

### Protocol Documentation
- **Protocol Buffers**: https://developers.google.com/protocol-buffers - Google's data serialisation
- **MessagePack**: https://msgpack.org/ - Efficient binary serialisation
- **CBOR**: https://cbor.io/ - Concise Binary Object Representation

### Network Security
- **OWASP**: https://owasp.org/ - Security best practices
- **SANS Reading Room**: https://www.sans.org/reading-room/ - Security research papers

---

## Romanian Language Resources

### University Materials
- ASE Course Materials: Available through the university portal
- Romanian Computer Networks Community: Various forums and discussion groups

### Technical Translations
- IEEE Romanian Section publications
- Romanian IT magazines with networking coverage

---

## Suggested Learning Path

### Week 4 Follow-Up Study Plan

**Day 1-2: Theory Reinforcement**
- Re-read Kurose & Ross Chapter 5 sections on framing and error detection
- Review CRC mathematics and implementation

**Day 3-4: Practical Exploration**
- Capture and analyse real-world protocol traffic
- Identify framing mechanisms in common protocols

**Day 5-6: Extension Projects**
- Implement one of the practical exercises above
- Document your protocol design decisions

**Day 7: Reflection**
- Compare your implementation with standard protocols
- Identify potential improvements and trade-offs

---

## Questions for Further Exploration

1. Why do some protocols use text-based formats (HTTP, SMTP) whilst others use binary (DNS, most IoT)?

2. How do modern protocols balance efficiency with extensibility?

3. What are the trade-offs between checksum, CRC and hash-based integrity verification?

4. How does the choice of framing mechanism affect protocol robustness?

5. In what scenarios would you choose UDP over TCP despite lacking reliability guarantees?

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
