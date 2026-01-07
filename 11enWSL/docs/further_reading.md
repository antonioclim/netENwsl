# Further Reading: Application Protocols and Load Balancing

> NETWORKING class - ASE, Informatics | by Revolvix

This document provides curated resources for deeper exploration of Week 11 topics.

---

## Foundational Texts

### Computer Networking

- **Kurose, J. & Ross, K. (2021).** *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.
  - Chapter 2: Application Layer – comprehensive coverage of HTTP, FTP, DNS, SMTP
  - Chapter 8: Security in Computer Networks – TLS, SSH fundamentals

- **Tanenbaum, A. & Wetherall, D. (2011).** *Computer Networks* (5th ed.). Prentice Hall.
  - Chapter 7: Application Layer – protocol design principles
  - Excellent historical context on protocol evolution

### Network Programming

- **Rhodes, B. & Goetzen, J. (2014).** *Foundations of Python Network Programming* (3rd ed.). Apress.
  - Chapter 14: FTP – programmatic file transfer
  - Chapter 16: DNS – resolver implementation
  - Chapter 18: SSH – paramiko library usage

- **Stevens, W. R. (2003).** *Unix Network Programming* (3rd ed.). Addison-Wesley.
  - Definitive reference for socket-level programming
  - Chapters on concurrent server design patterns

---

## Protocol Specifications (RFCs)

### File Transfer Protocol (FTP)

| RFC | Title | Description |
|-----|-------|-------------|
| [RFC 959](https://datatracker.ietf.org/doc/html/rfc959) | File Transfer Protocol | Core FTP specification |
| [RFC 1579](https://datatracker.ietf.org/doc/html/rfc1579) | Firewall-Friendly FTP | Passive mode rationale |
| [RFC 2228](https://datatracker.ietf.org/doc/html/rfc2228) | FTP Security Extensions | AUTH, PROT commands |
| [RFC 4217](https://datatracker.ietf.org/doc/html/rfc4217) | Securing FTP with TLS | FTPS implementation |

### Domain Name System (DNS)

| RFC | Title | Description |
|-----|-------|-------------|
| [RFC 1034](https://datatracker.ietf.org/doc/html/rfc1034) | Domain Concepts | DNS architecture overview |
| [RFC 1035](https://datatracker.ietf.org/doc/html/rfc1035) | DNS Implementation | Wire format, message structure |
| [RFC 2181](https://datatracker.ietf.org/doc/html/rfc2181) | Clarifications to DNS | Authoritative answers |
| [RFC 4033-4035](https://datatracker.ietf.org/doc/html/rfc4033) | DNSSEC | Cryptographic DNS validation |
| [RFC 8484](https://datatracker.ietf.org/doc/html/rfc8484) | DNS over HTTPS (DoH) | Privacy-preserving DNS |

### Secure Shell (SSH)

| RFC | Title | Description |
|-----|-------|-------------|
| [RFC 4251](https://datatracker.ietf.org/doc/html/rfc4251) | SSH Protocol Architecture | Layer model, design goals |
| [RFC 4252](https://datatracker.ietf.org/doc/html/rfc4252) | SSH Authentication | Password, public key methods |
| [RFC 4253](https://datatracker.ietf.org/doc/html/rfc4253) | SSH Transport Layer | Key exchange, encryption |
| [RFC 4254](https://datatracker.ietf.org/doc/html/rfc4254) | SSH Connection Protocol | Channels, port forwarding |
| [RFC 4819](https://datatracker.ietf.org/doc/html/rfc4819) | SSH Public Key Subsystem | Key management |

---

## Load Balancing and Reverse Proxies

### Nginx Resources

- **Nginx Official Documentation**: https://nginx.org/en/docs/
  - [HTTP Load Balancing](https://nginx.org/en/docs/http/load_balancing.html) – algorithm configuration
  - [Reverse Proxy](https://nginx.org/en/docs/http/ngx_http_proxy_module.html) – proxy_pass directives
  - [Health Checks](https://nginx.org/en/docs/http/ngx_http_upstream_hc_module.html) – active/passive monitoring

- **Nginx Cookbook** by Derek DeJonghe (O'Reilly, 2022)
  - Practical recipes for load balancing scenarios
  - TLS termination, caching strategies

### Load Balancing Theory

- **Brewer, E. (2012).** *CAP Twelve Years Later: How the "Rules" Have Changed*. IEEE Computer.
  - Foundational understanding of distributed system trade-offs

- **Schroeder, B. & Harchol-Balter, M. (2006).** *Web Servers Under Overload*. Performance Evaluation.
  - Empirical analysis of load balancing algorithms
  - Round-robin vs weighted vs least-connections performance

### HAProxy (Alternative Load Balancer)

- **HAProxy Documentation**: https://www.haproxy.org/documentation/
  - Industry-standard TCP/HTTP load balancer
  - Excellent comparison point against Nginx

---

## Container Orchestration

### Docker Compose

- **Docker Compose Specification**: https://docs.docker.com/compose/compose-file/
  - Service definitions, networking, volumes
  - Health check configuration

- **Docker Networking**: https://docs.docker.com/network/
  - Bridge networks, overlay networks
  - Container DNS resolution

### Kubernetes (Advanced)

For production-scale load balancing:

- **Kubernetes Services**: https://kubernetes.io/docs/concepts/services-networking/service/
  - ClusterIP, NodePort, LoadBalancer types
  - Ingress controllers

---

## Packet Analysis

### Wireshark Resources

- **Sanders, C. (2017).** *Practical Packet Analysis* (3rd ed.). No Starch Press.
  - Protocol dissection techniques
  - Filtering and statistics

- **Wireshark Wiki**: https://wiki.wireshark.org/
  - [Display Filter Reference](https://wiki.wireshark.org/DisplayFilters) – filter syntax
  - [FTP Protocol](https://wiki.wireshark.org/FTP) – dissection details
  - [DNS Protocol](https://wiki.wireshark.org/DNS) – query/response analysis

### Useful Display Filters for Week 11

```
# FTP traffic (control and data)
ftp || ftp-data

# DNS queries and responses
dns

# HTTP through load balancer
http && tcp.port == 8080

# SSH handshake
ssh
```

---

## Online Courses and Tutorials

### Free Resources

- **Computer Networking (Stanford Online)**: https://online.stanford.edu/courses/cs144-introduction-computer-networking
  - Video lectures covering application layer protocols

- **DNS & BIND Course (Pluralsight)**: Comprehensive DNS administration
  - Zone file configuration, DNSSEC deployment

- **Load Balancing with Nginx (DigitalOcean)**: https://www.digitalocean.com/community/tutorials/understanding-nginx-http-proxying-load-balancing-buffering-and-caching
  - Step-by-step load balancer configuration

### Interactive Labs

- **Katacoda/Killercoda**: https://killercoda.com/
  - Browser-based Docker and Kubernetes scenarios
  - Nginx load balancing exercises

- **TryHackMe**: https://tryhackme.com/
  - Network fundamentals rooms
  - Practical DNS and SSH challenges

---

## Academic Papers

### Classic Papers

1. **Mockapetris, P. (1983).** *Domain Names: Concepts and Facilities*. RFC 882.
   - Original DNS design rationale

2. **Ylonen, T. (1996).** *SSH - Secure Login Connections over the Internet*.
   - SSH design motivation and security analysis

3. **Fielding, R. (2000).** *Architectural Styles and the Design of Network-Based Software Architectures*.
   - REST architectural principles (doctoral dissertation)

### Recent Research

- **Zhu, L. et al. (2015).** *Connection-less DNS: Moving Forward with DNS Security and Privacy*.
  - Modern DNS privacy considerations

- **Aitchison, R. (2011).** *Pro DNS and BIND* (2nd ed.). Apress.
  - Advanced DNS administration techniques

---

## Tools and Libraries

### Python Libraries

| Library | Purpose | Documentation |
|---------|---------|---------------|
| `dnspython` | DNS queries and zone manipulation | https://dnspython.readthedocs.io/ |
| `paramiko` | SSH client and server implementation | https://www.paramiko.org/ |
| `pyftpdlib` | FTP server library | https://pyftpdlib.readthedocs.io/ |
| `ftplib` | FTP client (stdlib) | https://docs.python.org/3/library/ftplib.html |

### Command-Line Tools

| Tool | Purpose | Man Page |
|------|---------|----------|
| `dig` | DNS query utility | `man dig` |
| `nslookup` | DNS lookup | `man nslookup` |
| `ssh` | Secure Shell client | `man ssh` |
| `curl` | HTTP client with proxy support | `man curl` |
| `tcpdump` | Packet capture | `man tcpdump` |

---

## Community Resources

### Forums and Q&A

- **Server Fault**: https://serverfault.com/ – system administration questions
- **Stack Overflow**: https://stackoverflow.com/ – programming questions
- **Reddit r/networking**: https://reddit.com/r/networking – professional networking discussion

### Blogs

- **Nginx Blog**: https://www.nginx.com/blog/ – performance tuning articles
- **Cloudflare Blog**: https://blog.cloudflare.com/ – DNS and CDN insights
- **Julia Evans**: https://jvns.ca/ – excellent networking zines and explanations

---

## Suggested Learning Path

### Beginner (1-2 weeks)

1. Read Kurose & Ross Chapter 2 (Application Layer)
2. Complete Nginx tutorial on DigitalOcean
3. Experiment with `dig` and DNS queries
4. Set up FTP server with pyftpdlib

### Intermediate (2-4 weeks)

1. Read relevant RFCs (start with RFC 1035 for DNS)
2. Implement simple load balancer from scratch
3. Configure HTTPS termination with Let's Encrypt
4. Study SSH key exchange in Wireshark

### Advanced (1-2 months)

1. Implement DNS resolver from protocol specification
2. Deploy Kubernetes Ingress controller
3. Study DNSSEC chain of trust
4. Contribute to open-source load balancer project

---

*NETWORKING class - ASE, Informatics | by Revolvix*
