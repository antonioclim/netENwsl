# 📚 Further Reading — Week 5: IP Addressing, Subnetting, VLSM
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## RFC Documents (Primary Sources)

| RFC | Title | Relevance |
|-----|-------|-----------|
| [RFC 791](https://tools.ietf.org/html/rfc791) | Internet Protocol (IPv4) | Core IPv4 specification |
| [RFC 8200](https://tools.ietf.org/html/rfc8200) | Internet Protocol, Version 6 | IPv6 specification |
| [RFC 1918](https://tools.ietf.org/html/rfc1918) | Address Allocation for Private Internets | Private IPv4 ranges |
| [RFC 4291](https://tools.ietf.org/html/rfc4291) | IPv6 Addressing Architecture | IPv6 address types |
| [RFC 3021](https://tools.ietf.org/html/rfc3021) | /31 Networks for Point-to-Point | Using /31 for P2P links |
| [RFC 4632](https://tools.ietf.org/html/rfc4632) | CIDR: Internet Address Assignment | CIDR and supernetting |
| [RFC 1878](https://tools.ietf.org/html/rfc1878) | Variable Length Subnet Table for IPv4 | VLSM reference tables |

---

## Textbooks

### Primary References

**Kurose, J. F., & Ross, K. W. (2021).** *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.
- Chapter 4: The Network Layer: Data Plane
- Sections on IP addressing and subnetting

**Tanenbaum, A. S., & Wetherall, D. J. (2021).** *Computer Networks* (6th ed.). Pearson.
- Chapter 5: The Network Layer
- Detailed IPv4 and IPv6 coverage

### Supplementary References

**Stevens, W. R. (1994).** *TCP/IP Illustrated, Volume 1: The Protocols* (2nd ed.). Addison-Wesley.
- Classic reference for protocol details

**Comer, D. E. (2014).** *Internetworking with TCP/IP Volume 1* (6th ed.). Pearson.
- Thorough treatment of IP addressing

---

## Online Resources

### Interactive Tutorials

| Resource | URL | Description |
|----------|-----|-------------|
| Subnet Practice | https://subnettingpractice.com | Interactive subnet quizzes |
| IP Calculator | https://jodies.de/ipcalc | Visual subnet calculator |
| IPv6 Test | https://test-ipv6.com | Check IPv6 connectivity |
| Wireshark Wiki | https://wiki.wireshark.org | Packet analysis guides |

### Documentation

| Resource | URL | Description |
|----------|-----|-------------|
| Cisco Learning | https://learningnetwork.cisco.com | Networking fundamentals |
| Docker Networking | https://docs.docker.com/network/ | Container networking |
| NetworkLessons | https://networklessons.com | Visual protocol explanations |
| Practical Networking | https://www.practicalnetworking.net | Subnetting guides |

---

## Video Resources

### Subnetting

- **Professor Messer** — *Subnetting* (free series on YouTube)
  - Clear visual explanations of subnetting mathematics

- **Sunny Classroom** — *Subnetting is Simple* (YouTube)
  - Step-by-step VLSM walkthrough

### IPv6

- **Cisco Networking Academy** — IPv6 Fundamentals
  - Addresses, compression, configuration

- **Keith Barker** — *IPv6 Addressing* (CBT Nuggets)
  - Practical IPv6 deployment

---

## Practice Tools

### Subnet Calculators

| Tool | Platform | Features |
|------|----------|----------|
| `ipcalc` | Linux/WSL | Command-line calculator |
| SolarWinds Subnet Calculator | Web | Visual VLSM planning |
| GestioIP | Web | Enterprise IP management |

### Installation in WSL

```bash
# Install ipcalc
sudo apt install ipcalc

# Usage example
ipcalc 192.168.10.0/26
```

### Python Libraries

```python
# ipaddress (standard library)
import ipaddress
net = ipaddress.ip_network('192.168.1.0/24')
print(list(net.subnets(prefixlen_diff=2)))

# netaddr (extended features)
# pip install netaddr
from netaddr import IPNetwork
net = IPNetwork('192.168.1.0/24')
print(net.cidr, net.broadcast, net.netmask)
```

---

## Related Weeks in This Course

| Week | Topic | Connection to Week 5 |
|------|-------|---------------------|
| Week 1 | Network Fundamentals | Basic `ping`, `traceroute` use IP addresses |
| Week 6 | NAT, ARP, DHCP | NAT translates addresses; DHCP assigns them |
| Week 7 | Packet Capture | Wireshark filters by IP address/subnet |
| Week 10 | DNS | Domain names resolve to IP addresses |

---

## Exam Preparation

### Key Concepts to Master

1. **CIDR notation** — Converting between prefix and mask
2. **Subnet boundaries** — Finding network and broadcast addresses
3. **FLSM vs VLSM** — When to use each approach
4. **IPv6 compression** — Rules for :: and leading zeros
5. **Address types** — Private, public, link-local, multicast

### Practice Problems

Try calculating without tools first, then verify:

1. What is the broadcast address of 172.16.45.67/20?
2. Split 10.0.0.0/24 into 8 equal subnets — what is the new prefix?
3. Allocate subnets for 100, 50, 20 and 2 hosts from 192.168.0.0/24
4. Compress: 2001:0db8:0000:0000:0000:ff00:0042:8329
5. What type of address is fe80::1?

---

## Academic Integrity Note

When using online calculators or tools:
- Use them to **verify** your manual calculations
- Understand **why** the answer is correct
- Be prepared to solve problems **without** tools in examinations

---

*Week 5: IP Addressing, Subnetting, VLSM — Further Reading*
*Computer Networks Laboratory — ASE, CSIE Bucharest*
