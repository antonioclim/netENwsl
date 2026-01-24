# Further Reading

> NETWORKING class - ASE, Informatics | by Revolvix
>
> Week 14: Integrated Recap and Project Evaluation

A curated collection of resources for deeper exploration of computer networking concepts covered throughout the course.

---

## Core Textbooks

### Primary References

**Kurose, J. F. & Ross, K. W. (2021)**
*Computer Networking: A Top-Down Approach* (8th Edition)
Pearson Education.
- Complete coverage of networking fundamentals
- Top-down approach starting from application layer
- Excellent for understanding protocol interactions
- [Companion website](https://gaia.cs.umass.edu/kurose_ross/index.php)

**Tanenbaum, A. S. & Wetherall, D. J. (2021)**
*Computer Networks* (6th Edition)
Pearson.
- Classic reference covering all layers in depth
- Strong focus on protocol design principles
- Historical context and evolution of networking

**Stevens, W. R. (1994)**
*TCP/IP Illustrated, Volume 1: The Protocols* (2nd Edition, 2011)
Addison-Wesley.
- Definitive guide to TCP/IP implementation
- Packet-level analysis with real examples
- Essential for understanding protocol behaviour

### Python Network Programming

**Rhodes, B. & Goerzen, J. (2014)**
*Foundations of Python Network Programming* (3rd Edition)
Apress.
- Python-focused network programming
- Socket programming fundamentals
- HTTP, email and application protocols

**Goerzen, J. & Bower, T. (2004)**
*Foundations of Python Network Programming*
Apress.
- Earlier edition with complementary examples
- Historical perspective on Python networking

---

## Topic-Specific Resources

### TCP/IP and Internet Protocols

**RFCs (Request for Comments)**

Essential protocol specifications:

| RFC | Title | Relevance |
|-----|-------|-----------|
| [RFC 791](https://datatracker.ietf.org/doc/html/rfc791) | Internet Protocol | IPv4 specification |
| [RFC 793](https://datatracker.ietf.org/doc/html/rfc793) | Transmission Control Protocol | TCP specification |
| [RFC 768](https://datatracker.ietf.org/doc/html/rfc768) | User Datagram Protocol | UDP specification |
| [RFC 2616](https://datatracker.ietf.org/doc/html/rfc2616) | HTTP/1.1 | HTTP protocol (superseded by RFC 7230-7235) |
| [RFC 7230](https://datatracker.ietf.org/doc/html/rfc7230) | HTTP/1.1 Message Syntax | Current HTTP/1.1 spec |
| [RFC 8446](https://datatracker.ietf.org/doc/html/rfc8446) | TLS 1.3 | Transport Layer Security |
| [RFC 1035](https://datatracker.ietf.org/doc/html/rfc1035) | DNS Implementation | Domain Name System |

### Socket Programming

**Beej's Guide to Network Programming**
https://beej.us/guide/bgnet/
- Free online guide to socket programming in C
- Excellent explanations of system calls
- Platform-specific considerations

**Python socket Documentation**
https://docs.python.org/3/library/socket.html
- Official Python socket module documentation
- Low-level networking interface

**Python asyncio Documentation**
https://docs.python.org/3/library/asyncio.html
- Asynchronous I/O for high-performance networking
- Modern approach to concurrent network applications

### Load Balancing and Proxies

**NGINX Documentation**
https://nginx.org/en/docs/
- Industry-standard reverse proxy
- Configuration examples
- Load balancing strategies

**HAProxy Documentation**
https://www.haproxy.org/download/2.8/doc/
- High-availability load balancer
- Advanced routing and health checks

**Martin Kleppmann (2017)**
*Designing Data-Intensive Applications*
O'Reilly Media.
- Chapter on distributed systems
- Load balancing patterns
- Consistency and availability trade-offs

### Packet Analysis

**Sanders, C. (2017)**
*Practical Packet Analysis* (3rd Edition)
No Starch Press.
- Wireshark-focused analysis techniques
- Real-world troubleshooting scenarios
- Protocol decoding

**Wireshark User's Guide**
https://www.wireshark.org/docs/wsug_html_chunked/
- Official documentation
- Filter syntax reference
- Advanced features

**Chappell, L. (2012)**
*Wireshark Network Analysis* (2nd Edition)
Protocol Analysis Institute.
- Thorough Wireshark usage
- Network forensics techniques

### Docker and Containerisation

**Docker Documentation**
https://docs.docker.com/
- Official Docker reference
- Networking in Docker
- Docker Compose specification

**Nickoloff, J. & Kuenzli, S. (2019)**
*Docker in Action* (2nd Edition)
Manning Publications.
- Container fundamentals
- Networking between containers
- Multi-container applications

### Security and Penetration Testing

**Erickson, J. (2008)**
*Hacking: The Art of Exploitation* (2nd Edition)
No Starch Press.
- Low-level understanding of vulnerabilities
- Network attack vectors
- Defensive programming

**OWASP Testing Guide**
https://owasp.org/www-project-web-security-testing-guide/
- Web application security testing
- Vulnerability categories
- Testing methodologies

---

## Online Courses and Tutorials

### Free Courses

**Stanford CS144: Introduction to Computer Networking**
https://cs144.github.io/
- University-level networking course
- Hands-on lab assignments
- Video lectures available

**Georgia Tech CS 6250: Computer Networks**
https://www.udacity.com/course/computer-networking--ud436
- Graduate-level course on Udacity
- Software-defined networking focus

**MIT OCW 6.829: Computer Networks**
https://ocw.mit.edu/courses/6-829-computer-networks-fall-2002/
- Classic course materials
- Research-oriented approach

### Interactive Learning

**Cisco Networking Academy**
https://www.netacad.com/
- Industry certification preparation
- Packet Tracer simulator
- CCNA curriculum

**GNS3 Academy**
https://academy.gns3.com/
- Network simulation
- Real device emulation
- Advanced topology design

---

## Tools and Software

### Network Analysis

| Tool | Purpose | URL |
|------|---------|-----|
| Wireshark | Packet analysis | https://www.wireshark.org/ |
| tcpdump | Command-line capture | https://www.tcpdump.org/ |
| nmap | Network scanning | https://nmap.org/ |
| Netcat | TCP/UDP Swiss army knife | Pre-installed on most systems |
| iperf3 | Bandwidth testing | https://iperf.fr/ |
| mtr | Network diagnostics | https://www.bitwizard.nl/mtr/ |

### Network Simulation

| Tool | Purpose | URL |
|------|---------|-----|
| Mininet | SDN simulation | http://mininet.org/ |
| GNS3 | Network emulation | https://www.gns3.com/ |
| Packet Tracer | Cisco simulation | https://www.netacad.com/courses/packet-tracer |
| EVE-NG | Network emulation | https://www.eve-ng.net/ |

### Development and Testing

| Tool | Purpose | URL |
|------|---------|-----|
| Postman | API testing | https://www.postman.com/ |
| curl | HTTP client | https://curl.se/ |
| httpie | HTTP client | https://httpie.io/ |
| Insomnia | API development | https://insomnia.rest/ |

---

## Academic Journals and Conferences

### Conferences

- **ACM SIGCOMM** - Premier networking conference
  https://www.sigcomm.org/

- **IEEE INFOCOM** - IEEE Conference on Computer Communications
  https://infocom.info/

- **USENIX NSDI** - Networked Systems Design and Implementation
  https://www.usenix.org/conferences/byname/nsdi

- **IMC** - Internet Measurement Conference
  https://www.sigcomm.org/events/imc-internet-measurement-conference

### Journals

- **IEEE/ACM Transactions on Networking**
- **ACM SIGCOMM Computer Communication Review**
- **IEEE Communications Magazine**
- **Computer Networks (Elsevier)**

---

## Blogs and News

### Technical Blogs

**Cloudflare Blog**
https://blog.cloudflare.com/
- In-depth guides on networking topics
- Internet infrastructure insights
- Security analysis

**Julia Evans' Blog**
https://jvns.ca/
- Accessible explanations of networking concepts
- Zines on TCP, DNS and more
- Systems programming

**High Scalability**
http://highscalability.com/
- Architecture case studies
- Distributed systems patterns
- Real-world scaling stories

**The Morning Paper**
https://blog.acolyer.org/
- Academic paper summaries
- Distributed systems focus
- Networking research

### News and Updates

**APNIC Blog**
https://blog.apnic.net/
- Internet number resources
- Regional networking news

**RIPE Labs**
https://labs.ripe.net/
- European networking research
- Internet measurement

**The Register - Networks**
https://www.theregister.com/networks/
- Industry news
- Technology analysis

---

## Video Resources

### YouTube Channels

**Computerphile**
https://www.youtube.com/user/Computerphile
- University of Nottingham
- Networking fundamentals explained

**Ben Eater**
https://www.youtube.com/c/BenEater
- Low-level networking hardware
- Building networks from scratch

**Network Chuck**
https://www.youtube.com/c/NetworkChuck
- Practical networking tutorials
- Certification preparation

**David Bombal**
https://www.youtube.com/c/DavidBombal
- Network automation
- Python for networking

### Conference Talks

**SIGCOMM Videos**
https://www.youtube.com/c/acmsigcomm
- Research presentations
- Modern networking

**Strange Loop**
https://www.youtube.com/c/StrangeLoopConf
- Systems programming talks
- Networking in-depth guides

---

## Community Resources

### Forums and Q&A

- **Stack Overflow** - [networking] tag
  https://stackoverflow.com/questions/tagged/networking

- **Server Fault** - Professional system administration
  https://serverfault.com/

- **Reddit r/networking**
  https://www.reddit.com/r/networking/

- **Reddit r/netsec**
  https://www.reddit.com/r/netsec/

### Discord and Slack

- **Python Discord** - #networking channel
  https://discord.gg/python

- **Docker Community**
  https://www.docker.com/community

---

## Recommended Learning Path

### Foundation (Weeks 1-4)
1. Kurose & Ross chapters 1-3
2. Beej's Guide to Network Programming
3. Python socket documentation

### Intermediate (Weeks 5-9)
1. TCP/IP Illustrated, selected chapters
2. RFCs for protocols being studied
3. Wireshark documentation

### Advanced (Weeks 10-14)
1. Practical Packet Analysis
2. Docker networking documentation
3. Conference papers from SIGCOMM/NSDI

### Continuous Learning
1. Subscribe to Cloudflare blog
2. Follow APNIC/RIPE updates
3. Practice with GNS3/Mininet simulations

---

## Local Resources (ASE Library)

The ASE Bucharest library provides access to:

- IEEE Xplore Digital Library
- ACM Digital Library
- Springer Link
- ScienceDirect

Check the library portal for current subscriptions and remote access options.

---

*NETWORKING class - ASE, Informatics | by Revolvix*
