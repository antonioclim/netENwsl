# Further Reading: Week 7

> NETWORKING class - ASE, Informatics | by Revolvix

## Core Textbooks

### Computer Networking: A Top-Down Approach
**Kurose, J. & Ross, K. (2016)**. 7th Edition. Pearson.

- Chapter 3: Transport Layer (TCP/UDP fundamentals)
- Chapter 4: Network Layer (IP, routing, NAT)
- Chapter 8: Security in Computer Networks (firewalls, IDS)

This text provides the theoretical foundation for understanding why packets have specific fields and how filtering decisions are made at each layer.

### TCP/IP Illustrated, Volume 1
**Stevens, W. R., Fall, K. & Stevens, W. (2011)**. 2nd Edition. Addison-Wesley.

- Part 2: Internet Protocols (IP, ICMP)
- Part 3: Transport Protocols (TCP, UDP)

The definitive reference for protocol internals. Essential for understanding exactly what appears in packet captures.

## Network Security References

### The Practice of Network Security Monitoring
**Bejtlich, R. (2013)**. No Starch Press.

Practical guidance on using packet captures for security analysis. Covers tcpdump, Wireshark and correlation techniques.

### Network Security Through Data Analysis
**Collins, M. (2014)**. O'Reilly Media.

Methods for analysing network traffic at scale. Useful for understanding patterns in large captures.

## Tool Documentation

### tcpdump Man Page
```bash
man tcpdump
```
Or online: https://www.tcpdump.org/manpages/tcpdump.1.html

Official documentation for capture filters (BPF syntax) and output formats.

### Wireshark User's Guide
https://www.wireshark.org/docs/wsug_html_chunked/

Complete guide to display filters, protocol dissectors and analysis features.

### tshark Man Page
```bash
man tshark
```
Or online: https://www.wireshark.org/docs/man-pages/tshark.html

Command-line Wireshark for scripted analysis.

### iptables Manual
```bash
man iptables
```
Or online: https://linux.die.net/man/8/iptables

Complete reference for firewall rule syntax and matching options.

### nftables Wiki
https://wiki.nftables.org/

Modern replacement for iptables with cleaner syntax. Increasingly the default in newer Linux distributions.

## RFCs (Protocol Specifications)

### RFC 793 - Transmission Control Protocol
https://datatracker.ietf.org/doc/html/rfc793

The original TCP specification. Essential for understanding flags, state transitions and connection establishment.

### RFC 768 - User Datagram Protocol
https://datatracker.ietf.org/doc/html/rfc768

UDP specification (remarkably brief). Explains the connectionless nature.

### RFC 792 - Internet Control Message Protocol
https://datatracker.ietf.org/doc/html/rfc792

ICMP message types including port unreachable (essential for understanding REJECT behaviour).

### RFC 1918 - Private Address Space
https://datatracker.ietf.org/doc/html/rfc1918

Defines 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 used in laboratory environments.

## Python Network Programming

### Foundations of Python Network Programming
**Rhodes, B. & Goetzen, J. (2014)**. 3rd Edition. Apress.

Practical Python examples for socket programming, including the patterns used in this laboratory.

### Python socket Module Documentation
https://docs.python.org/3/library/socket.html

Official reference for socket creation, binding, connection and data transfer.

## Docker Networking

### Docker Networking Documentation
https://docs.docker.com/network/

Official guide to bridge networks, overlay networks and container connectivity.

### Container Networking Detailed Guide
https://docs.docker.com/network/network-tutorial-standalone/

Hands-on tutorial for understanding Docker network namespaces and bridges.

## Academic Papers

### A Survey of Network Security
**Needham, R. M. (1994)**. "Denial of service". ACM CCS.

Early systematic treatment of network-level attacks and defences.

### Bro: A System for Detecting Network Intruders in Real-Time
**Paxson, V. (1999)**. Computer Networks.

Foundational work on network monitoring that influenced modern packet analysis tools.

## Online Resources

### Wireshark SampleCaptures
https://wiki.wireshark.org/SampleCaptures

Pre-recorded captures demonstrating various protocols and scenarios.

### PacketLife Capture Repository
https://packetlife.net/captures/

Annotated captures for learning protocol analysis.

### SANS Reading Room - Network Security
https://www.sans.org/white-papers/

Research papers on network security topics including firewall configuration and traffic analysis.

## Video Tutorials

### Professor Messer - Network+
https://www.professormesser.com/network-plus/

Free video series covering networking fundamentals at an accessible level.

### Chris Greer - Wireshark Tutorials
https://www.youtube.com/user/chrisgreer

Practical packet analysis demonstrations.

## Practice Environments

### Hack The Box
https://www.hackthebox.eu/

Penetration testing practice labs (requires ethical usage agreement).

### TryHackMe
https://tryhackme.com/

Guided network security exercises in browser-accessible VMs.

### GNS3
https://www.gns3.com/

Network emulation for practising with real router and switch images.

---

*NETWORKING class - ASE, Informatics | by Revolvix*
