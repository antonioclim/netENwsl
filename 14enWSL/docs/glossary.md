# 📖 Glossary — Week 14: Integrated Recap

> NETWORKING class — ASE, CSIE | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

---

## Core Networking Terms

| Term | Definition | Example |
|------|------------|---------|
| **IP Address** | A numerical label assigned to each device on a network using the Internet Protocol for identification and routing | `172.20.0.2` |
| **MAC Address** | A hardware identifier assigned to network interface controllers, used for communication within a network segment | `02:42:ac:14:00:02` |
| **Subnet** | A logical subdivision of an IP network, defined by a network address and mask | `172.20.0.0/24` (256 addresses) |
| **CIDR** | Classless Inter-Domain Routing — notation that specifies IP address and subnet mask together | `/24` means 24 bits for network, 8 for hosts |
| **Gateway** | A network node that serves as an access point to another network | `172.20.0.1` (Docker bridge) |
| **Port** | A logical endpoint for network communication, identified by a 16-bit number (0-65535) | Port 80 (HTTP), Port 443 (HTTPS) |
| **Socket** | An endpoint for sending/receiving data, defined by IP address + port + protocol | `172.20.0.2:8080/TCP` |
| **Protocol** | A set of rules defining how data is formatted and transmitted | TCP, UDP, HTTP, DNS |

---

## OSI Model Layers

| Layer | Name | Function | PDU | Examples |
|-------|------|----------|-----|----------|
| 7 | **Application** | User interface and application services | Data | HTTP, FTP, DNS, SMTP |
| 6 | **Presentation** | Data formatting, encryption, compression | Data | SSL/TLS, JPEG, ASCII |
| 5 | **Session** | Session establishment, maintenance, termination | Data | NetBIOS, RPC |
| 4 | **Transport** | End-to-end delivery, error recovery | Segment (TCP) / Datagram (UDP) | TCP, UDP |
| 3 | **Network** | Logical addressing, routing | Packet | IP, ICMP, OSPF |
| 2 | **Data Link** | Physical addressing, framing | Frame | Ethernet, ARP |
| 1 | **Physical** | Bit transmission on physical medium | Bits | Cables, signals |

**Memory aid:** "Please Do Not Throw Sausage Pizza Away" (Physical → Application)

---

## TCP/IP Terms

| Term | Definition | Context |
|------|------------|---------|
| **TCP** | Transmission Control Protocol — connection-oriented, reliable transport | Web browsing, file transfer, email |
| **UDP** | User Datagram Protocol — connectionless, unreliable transport | DNS queries, streaming, gaming |
| **Three-way handshake** | TCP connection establishment: SYN → SYN-ACK → ACK | Every TCP connection begins with this |
| **Segment** | TCP protocol data unit containing header and payload | TCP divides data into segments |
| **Packet** | Network layer PDU containing IP header and segment | Routers forward packets |
| **Frame** | Data link layer PDU containing MAC header, packet and trailer | Switches forward frames |
| **ACK** | Acknowledgement — confirms receipt of data | TCP uses ACKs for reliability |
| **SYN** | Synchronise — initiates TCP connection | First packet of handshake |
| **FIN** | Finish — terminates TCP connection | Graceful connection close |
| **RST** | Reset — abruptly terminates connection | Error or rejection |

---

## HTTP Terms

| Term | Definition | Example |
|------|------------|---------|
| **HTTP** | Hypertext Transfer Protocol — application protocol for web | `GET /index.html HTTP/1.1` |
| **HTTPS** | HTTP Secure — HTTP over TLS encryption | Port 443 by default |
| **Request** | Client message asking server for a resource | `GET /api/users` |
| **Response** | Server message returning requested data or status | `200 OK` with body |
| **Method** | HTTP action type | GET, POST, PUT, DELETE |
| **Status code** | Three-digit response indicator | 200=OK, 404=Not Found, 500=Error |
| **Header** | Metadata in request or response | `Content-Type: application/json` |
| **Body** | Content payload of request or response | HTML, JSON, binary data |

### Common HTTP Status Codes

| Code | Meaning | When you see it |
|------|---------|-----------------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created (POST) |
| 301 | Moved Permanently | URL has changed |
| 400 | Bad Request | Malformed request |
| 401 | Unauthorised | Authentication required |
| 403 | Forbidden | No permission |
| 404 | Not Found | Resource does not exist |
| 500 | Internal Server Error | Server-side problem |
| 502 | Bad Gateway | Upstream server error |
| 503 | Service Unavailable | Server overloaded |

---

## Docker Terms

| Term | Definition | Example |
|------|------------|---------|
| **Container** | An isolated runtime instance of an image | `docker run nginx` |
| **Image** | A read-only template for creating containers | `nginx:latest` |
| **Dockerfile** | Script defining how to build an image | `FROM python:3.11` |
| **docker-compose** | Tool for defining multi-container applications | `docker compose up` |
| **Volume** | Persistent storage that survives container removal | `-v mydata:/data` |
| **Network** | Isolated communication channel for containers | `docker network create mynet` |
| **Port mapping** | Forwarding host port to container port | `-p 8080:80` |
| **Bridge network** | Default Docker network mode, NAT-based | Containers get private IPs |

---

## Load Balancing Terms

| Term | Definition | Example |
|------|------------|---------|
| **Load balancer** | Distributes requests across multiple backends | Nginx, HAProxy, cloud LBs |
| **Backend** | Server that handles requests behind a load balancer | `app1`, `app2` containers |
| **Round-robin** | Distributes requests sequentially to each backend | 1→A, 2→B, 3→A, 4→B |
| **Health check** | Periodic test to verify backend availability | `GET /health` every 10s |
| **Upstream** | Backend server group in load balancer config | Nginx `upstream` block |
| **Failover** | Automatic routing to healthy backends when one fails | If A down, send to B |

---

## Wireshark Terms

| Term | Definition | Example |
|------|------------|---------|
| **Capture** | Recording network packets | Start capture on interface |
| **Filter** | Expression to show only matching packets | `tcp.port == 80` |
| **Display filter** | Filter applied to already-captured packets | Filter box in main window |
| **Capture filter** | Filter applied during capture (BPF syntax) | `port 80` |
| **PCAP** | Packet capture file format | `capture.pcap` |
| **Follow stream** | Reconstruct complete TCP/UDP conversation | Right-click → Follow → TCP Stream |

### Essential Wireshark Filters

| Filter | Purpose |
|--------|---------|
| `http` | All HTTP traffic |
| `tcp.port == 8080` | Traffic on specific port |
| `ip.addr == 172.20.0.2` | Traffic to/from specific IP |
| `tcp.flags.syn == 1` | TCP SYN packets (connections) |
| `http.request.method == "GET"` | HTTP GET requests |

---

## Acronyms

| Acronym | Full Form | Notes |
|---------|-----------|-------|
| **ARP** | Address Resolution Protocol | IP → MAC mapping |
| **CIDR** | Classless Inter-Domain Routing | Modern IP notation |
| **DHCP** | Dynamic Host Configuration Protocol | Automatic IP assignment |
| **DNS** | Domain Name System | Name → IP resolution |
| **HTTP** | Hypertext Transfer Protocol | Web communication |
| **HTTPS** | HTTP Secure | Encrypted web |
| **ICMP** | Internet Control Message Protocol | ping, traceroute |
| **IP** | Internet Protocol | Network layer addressing |
| **LB** | Load Balancer | Request distribution |
| **MAC** | Media Access Control | Layer 2 address |
| **NAT** | Network Address Translation | IP address mapping |
| **OSI** | Open Systems Interconnection | Reference model |
| **PDU** | Protocol Data Unit | Data unit at each layer |
| **TCP** | Transmission Control Protocol | Reliable transport |
| **TLS** | Transport Layer Security | Encryption protocol |
| **UDP** | User Datagram Protocol | Unreliable transport |
| **WSL** | Windows Subsystem for Linux | Linux on Windows |

---

*Document version: 2.0 | Week 14: Integrated Recap | January 2025*
