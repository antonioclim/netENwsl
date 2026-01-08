# Further Reading - Week 3

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by Revolvix

## Core Concepts Covered

This week's laboratory explored fundamental network programming concepts: UDP broadcast and multicast communication, and TCP tunnelling. The resources below provide deeper theoretical foundations and advanced applications.

---

## RFC Documents

### Broadcasting

**RFC 919 - Broadcasting Internet Datagrams** (1984)
- Defines the concept of IP broadcast addressing
- Establishes the limited broadcast address (255.255.255.255)
- URL: https://datatracker.ietf.org/doc/html/rfc919

**RFC 922 - Broadcasting Internet Datagrams in the Presence of Subnets** (1984)
- Extends broadcast semantics to subnetted environments
- Introduces directed broadcast addresses
- URL: https://datatracker.ietf.org/doc/html/rfc922

### Multicasting

**RFC 1112 - Host Extensions for IP Multicasting** (1989)
- Foundational document for IP multicast
- Defines IGMP version 1
- Specifies multicast address range (224.0.0.0 - 239.255.255.255)
- URL: https://datatracker.ietf.org/doc/html/rfc1112

**RFC 2236 - Internet Group Management Protocol, Version 2** (1997)
- Improves leave latency over IGMPv1
- Introduces Group-Specific Query
- URL: https://datatracker.ietf.org/doc/html/rfc2236

**RFC 3376 - Internet Group Management Protocol, Version 3** (2002)
- Adds source filtering capability
- Enables Source-Specific Multicast (SSM)
- URL: https://datatracker.ietf.org/doc/html/rfc3376

**RFC 5771 - IANA Guidelines for IPv4 Multicast Address Assignments** (2010)
- Defines multicast address allocation policies
- Explains administratively scoped addresses (239.x.x.x)
- URL: https://datatracker.ietf.org/doc/html/rfc5771

### Socket Programming

**RFC 793 - Transmission Control Protocol** (1981)
- Definitive TCP specification
- Essential for understanding TCP tunnel behaviour
- URL: https://datatracker.ietf.org/doc/html/rfc793

**RFC 768 - User Datagram Protocol** (1980)
- Brief but complete UDP specification
- Foundation for broadcast/multicast transport
- URL: https://datatracker.ietf.org/doc/html/rfc768

---

## Textbooks

### Primary References

**Kurose, J.F. & Ross, K.W. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.**
- Chapter 2: Application Layer (socket programming basics)
- Chapter 3: Transport Layer (UDP, TCP mechanics)
- Chapter 4: Network Layer (IP addressing, multicast)

**Stevens, W.R., Fenner, B. & Rudoff, A.M. (2004). *UNIX Network Programming, Volume 1: The Sockets Networking API* (3rd ed.). Addison-Wesley.**
- Chapter 20: Broadcasting
- Chapter 21: Multicasting
- Definitive reference for socket programming

**Rhodes, B. & Goerzen, J. (2014). *Foundations of Python Network Programming* (3rd ed.). Apress.**
- Chapter 2: UDP
- Chapter 3: TCP
- Practical Python implementations

### Secondary References

**Tanenbaum, A.S. & Wetherall, D.J. (2011). *Computer Networks* (5th ed.). Pearson.**
- Chapter 5: Network Layer
- Theoretical foundations of addressing

**Comer, D.E. (2015). *Internetworking with TCP/IP, Volume 1: Principles, Protocols, and Architecture* (6th ed.). Pearson.**
- Chapter 15: IP Multicast
- Chapter 17: TCP

---

## Online Resources

### Python Documentation

**Socket Module Documentation**
- Official Python socket programming reference
- URL: https://docs.python.org/3/library/socket.html

**Socket Programming HOWTO**
- Practical guide to Python sockets
- URL: https://docs.python.org/3/howto/sockets.html

### Tutorials and Guides

**Beej's Guide to Network Programming**
- Classic C networking tutorial (concepts apply to Python)
- URL: https://beej.us/guide/bgnet/

**Real Python - Socket Programming in Python**
- Modern Python-focused tutorial
- URL: https://realpython.com/python-sockets/

### Wireshark Resources

**Wireshark User's Guide**
- Complete documentation
- URL: https://www.wireshark.org/docs/wsug_html_chunked/

**Wireshark Display Filter Reference**
- All available filter expressions
- URL: https://www.wireshark.org/docs/dfref/

---

## Academic Papers

### Multicast

**Deering, S.E. (1988). "Multicast Routing in Internetworks and Extended LANs." *ACM SIGCOMM Computer Communication Review*, 18(4), 55-64.**
- Seminal paper on multicast routing
- Introduces concepts still used today

**Holbrook, H.W. & Cheriton, D.R. (1999). "IP Multicast Channels: EXPRESS Support for Large-scale Single-source Applications." *ACM SIGCOMM Computer Communication Review*, 29(4), 65-78.**
- Foundation for Source-Specific Multicast

### Tunnelling

**Kent, S. & Atkinson, R. (1998). "Security Architecture for the Internet Protocol." RFC 2401.**
- IPsec tunnel mode concepts
- URL: https://datatracker.ietf.org/doc/html/rfc2401

---

## Related Concepts for Further Study

### Advanced Broadcasting Patterns

1. **Service Discovery Protocols**
   - mDNS (Multicast DNS) - RFC 6762
   - DNS-SD (DNS Service Discovery) - RFC 6763
   - Used by Bonjour, Avahi

2. **Network Boot Protocols**
   - BOOTP - RFC 951
   - DHCP - RFC 2131
   - PXE boot process

### Advanced Multicast Applications

1. **Streaming Media**
   - RTP/RTCP over multicast - RFC 3550
   - IGMP snooping in switches

2. **Reliable Multicast**
   - PGM (Pragmatic General Multicast) - RFC 3208
   - NORM (NACK-Oriented Reliable Multicast) - RFC 5740

3. **Multicast Routing Protocols**
   - PIM-SM (Protocol Independent Multicast - Sparse Mode)
   - MSDP (Multicast Source Discovery Protocol)

### Tunnelling Technologies

1. **VPN Technologies**
   - OpenVPN (SSL/TLS tunnels)
   - WireGuard (modern VPN protocol)
   - IPsec tunnel mode

2. **Overlay Networks**
   - VXLAN - RFC 7348
   - GRE tunnels - RFC 2784
   - SSH port forwarding

3. **Application-Level Proxies**
   - SOCKS5 - RFC 1928
   - HTTP CONNECT tunnelling

---

## Tools for Experimentation

### Packet Crafting

**Scapy**
- Powerful Python packet manipulation library
- URL: https://scapy.net/

**hping3**
- Command-line packet generator
- Supports crafting custom TCP/UDP/ICMP packets

### Network Simulation

**Mininet**
- Realistic virtual network emulator
- URL: http://mininet.org/

**GNS3**
- Network simulation platform
- URL: https://www.gns3.com/

### Traffic Analysis

**tcpdump**
- Command-line packet analyser
- Man page: https://www.tcpdump.org/manpages/tcpdump.1.html

**tshark**
- Terminal-based Wireshark
- URL: https://www.wireshark.org/docs/man-pages/tshark.html

---

## Video Lectures

**MIT OpenCourseWare - Computer Networks**
- Free university-level networking course
- URL: https://ocw.mit.edu/

**Computerphile**
- Networking fundamentals explained accessibly
- URL: https://www.youtube.com/user/Computerphile

---

## Practical Projects to Extend Learning

1. **Build a LAN Chat Application**
   - Use multicast for group messaging
   - Implement user discovery via broadcast

2. **Create a Simple VPN**
   - Extend the TCP tunnel to encrypt traffic
   - Add authentication mechanisms

3. **Implement Service Discovery**
   - Broadcast service announcements
   - Build a service registry

4. **Develop a File Sharing System**
   - Multicast file availability announcements
   - TCP transfer with resume capability

5. **Network Monitor Dashboard**
   - Capture broadcast/multicast traffic
   - Visualise network activity in real-time

---

*NETWORKING class - ASE, Informatics | by Revolvix*
