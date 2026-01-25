# Common Misconceptions — Week 14

> NETWORKING class — ASE, CSIE | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

This document addresses common student misconceptions about networking concepts. Each entry includes the misconception, why it is incorrect and the correct understanding.

I've noticed many students initially treat containers like VMs because that's how virtualisation is typically introduced. The misconceptions below are collected from my experience teaching this course over several years.

---

## Misconception 1: IP Addresses and MAC Addresses Serve the Same Purpose

### The Misconception

"IP addresses and MAC addresses both identify devices on a network, so they are interchangeable."

### Why It Is Wrong

IP addresses and MAC addresses operate at different layers and serve different purposes:

- **MAC addresses (Layer 2):** Fixed hardware identifiers for local network communication
- **IP addresses (Layer 3):** Logical addresses for routing between networks

### Correct Understanding

MAC addresses identify the physical network interface and work within a single network segment. IP addresses provide logical addressing that enables routing across multiple networks. A packet needs both: MAC for the next hop, IP for the final destination.

---

## Misconception 2: TCP and UDP Are Just Different Speeds

### The Misconception

"UDP is faster than TCP, so use UDP when you need speed and TCP when you need reliability."

### Why It Is Wrong

The difference is not primarily about speed but about guarantees:

- **TCP:** Connection-oriented, reliable, ordered delivery
- **UDP:** Connectionless, best-effort delivery

### Correct Understanding

TCP provides reliability through acknowledgements, retransmissions and ordering. This adds overhead but guarantees delivery. UDP sends packets without confirmation, making it suitable for real-time applications where occasional packet loss is acceptable (video streaming, DNS queries).

---

## Misconception 3: The Three-Way Handshake Happens Every Request

### The Misconception

"Every HTTP request requires a new TCP three-way handshake."

### Why It Is Wrong

HTTP/1.1 introduced persistent connections (keep-alive), and HTTP/2 uses multiplexing. A single TCP connection can carry multiple HTTP requests.

### Correct Understanding

The three-way handshake establishes a TCP connection once. Multiple HTTP requests can then use that connection. Connection reuse reduces latency significantly. Only when the connection is closed (or times out) is a new handshake needed.

---

## Misconception 4: Wireshark Shows All Network Traffic

### The Misconception

"Wireshark captures everything happening on the network."

### Why It Is Wrong

Wireshark only captures traffic visible to the network interface:

- On switched networks, you see only your traffic (unless mirroring is configured)
- Encrypted traffic (HTTPS) shows as TLS, not readable content
- Some protocols may not be fully dissected

### Correct Understanding

Wireshark captures what the network interface sees. On modern switched networks, this means traffic to/from your machine or broadcast/multicast traffic. To see other traffic, you need port mirroring, a hub or ARP spoofing (which has security implications).

---

## Misconception 5: Docker Port Mapping Direction

### The Misconception

"In `8080:80`, the first number is the container port and the second is the host port."

### Why It Is Wrong

Docker port mapping format is `HOST:CONTAINER`, not `CONTAINER:HOST`.

### Correct Understanding

The format `-p HOST:CONTAINER` means:
- `8080:80` → Host port 8080 forwards to container port 80
- Access via `localhost:8080`, which reaches the container's port 80

Think of it as "from:to" from the perspective of incoming traffic.

---

## Misconception 6: All Docker Containers Share the Same Network

### The Misconception

"All Docker containers can communicate with each other by default."

### Why It Is Wrong

Containers on different networks cannot communicate directly. Docker provides network isolation.

### Correct Understanding

Containers can only communicate if they are on the same Docker network. The default bridge network provides limited connectivity. Custom networks offer DNS-based service discovery. Network segmentation is a key security feature of Docker.

---

## Misconception 7: Container Running = Service Working

### The Misconception

"If `docker ps` shows the container running, the service must be working correctly."

### Why It Is Wrong

A container can be running while the application inside has crashed, is unresponsive or is misconfigured.

### Correct Understanding

`docker ps` only confirms the container process is running. Verify service health by:
1. Checking logs: `docker logs container_name`
2. Testing the endpoint: `curl http://localhost:port/health`
3. Using Docker health checks in your compose file

---

## Misconception 8: Round-Robin Means Random

### The Misconception

"Round-robin load balancing distributes requests randomly across backends."

### Why It Is Wrong

Round-robin is deterministic and sequential, not random.

### Correct Understanding

Round-robin follows a strict rotation:
- Request 1 → Backend A
- Request 2 → Backend B
- Request 3 → Backend A
- Request 4 → Backend B
- ...

This pattern is predictable and repeatable, unlike random distribution which would show statistical variation.

---

## Misconception 9: Load Balancers Instantly Detect Failures

### The Misconception

"When a backend server fails, the load balancer immediately stops sending traffic to it."

### Why It Is Wrong

Health checks run at intervals (typically 5-30 seconds). There is a detection delay.

### Correct Understanding

Load balancers detect failures through periodic health checks. During the interval between checks, requests may still be routed to the failed backend. This is why you might see 502 errors temporarily after a backend fails. Shorter health check intervals improve detection speed but increase overhead.

---

## Misconception 10: "Connection Refused" Always Means Firewall

### The Misconception

"If I get 'Connection refused', the firewall must be blocking traffic."

### Why It Is Wrong

"Connection refused" specifically means the target host received the connection request but no service is listening on that port.

### Correct Understanding

Different error types indicate different problems:
- **Connection refused:** Port is not listening (service not running)
- **Connection timed out:** Traffic not reaching destination (firewall, routing)
- **No route to host:** Network path does not exist

"Connection refused" means the TCP RST packet came back, so the network path works fine.

---

## Misconception 11: HTTPS Traffic Cannot Be Analysed

### The Misconception

"HTTPS encrypts everything, so Wireshark is useless for debugging HTTPS traffic."

### Why It Is Wrong

While payload is encrypted, metadata is still visible, and there are techniques for decryption.

### Correct Understanding

Even with HTTPS, you can see:
- TCP handshake (connection establishment)
- TLS handshake (certificate exchange, cipher negotiation)
- Packet sizes and timing
- Server Name Indication (SNI) in TLS 1.2

With the server's private key or pre-master secret, full decryption is possible for debugging.

---

## Misconception 12: localhost and 127.0.0.1 Are Always Identical

### The Misconception

"localhost and 127.0.0.1 are exactly the same thing."

### Why It Is Wrong

`localhost` is a hostname that must be resolved. It may resolve to IPv6 `::1` or IPv4 `127.0.0.1`.

### Correct Understanding

- `127.0.0.1` is explicitly IPv4 loopback
- `::1` is explicitly IPv6 loopback
- `localhost` depends on `/etc/hosts` and system configuration

If a service listens only on IPv4 (`127.0.0.1`) but `localhost` resolves to IPv6, connections may fail. Be explicit when debugging.

---

*Document version: 2.0 | Week 14: Integrated Recap | January 2025*
*NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim*
