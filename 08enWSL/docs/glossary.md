# 📖 Glossary — Week 8: Transport Layer & HTTP
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Transport Layer Terms

| Term | Definition | Example |
|------|------------|---------|
| **TCP** | Transmission Control Protocol — connection-oriented, reliable, ordered delivery | `socket.SOCK_STREAM` |
| **UDP** | User Datagram Protocol — connectionless, best-effort delivery | `socket.SOCK_DGRAM` |
| **Port** | 16-bit number identifying a process on a host (0-65535) | Port 80 (HTTP), 443 (HTTPS) |
| **Socket** | Endpoint for communication — combination of IP address and port | `192.168.1.10:8080` |
| **Segment** | TCP's unit of data transfer (TCP header + payload) | Maximum segment size (MSS) |
| **Datagram** | UDP's unit of data transfer (UDP header + payload) | DNS query datagram |
| **Three-way handshake** | TCP connection establishment: SYN → SYN-ACK → ACK | Wireshark filter: `tcp.flags.syn` |
| **Sequence number** | 32-bit counter tracking bytes sent in TCP | Initial: random, then increments |
| **Acknowledgment number** | Next expected byte number from sender | `Ack = Seq + data_length` |
| **Window size** | Receiver's buffer space available (flow control) | `Window: 65535` |
| **MSS** | Maximum Segment Size — largest payload TCP will send | Typically 1460 bytes (Ethernet) |
| **RTT** | Round-Trip Time — time for packet to reach destination and return | Measured in milliseconds |
| **Retransmission** | Re-sending lost or unacknowledged segments | Triggered by timeout or duplicate ACKs |
| **Flow control** | Preventing sender from overwhelming receiver | Via TCP window size |
| **Congestion control** | Preventing sender from overwhelming network | Slow start, AIMD |

---

## HTTP Terms

| Term | Definition | Example |
|------|------------|---------|
| **HTTP** | HyperText Transfer Protocol — application-layer protocol for web | HTTP/1.1, HTTP/2, HTTP/3 |
| **Request** | Client-to-server message requesting a resource | `GET /index.html HTTP/1.1` |
| **Response** | Server-to-client message with status and content | `HTTP/1.1 200 OK` |
| **Method** | HTTP verb indicating desired action | GET, POST, HEAD, PUT, DELETE |
| **Status code** | 3-digit number indicating response status | 200 (OK), 404 (Not Found) |
| **Header** | Metadata in key: value format | `Content-Type: text/html` |
| **Body** | Actual content of request or response | HTML, JSON, binary data |
| **CRLF** | Carriage Return + Line Feed (line ending in HTTP) | `\r\n` |
| **Keep-alive** | Reusing TCP connection for multiple requests | `Connection: keep-alive` |
| **Content-Type** | MIME type of the body content | `application/json` |
| **Content-Length** | Size of body in bytes | `Content-Length: 1234` |
| **Host** | Target hostname (required in HTTP/1.1) | `Host: example.com` |
| **User-Agent** | Client software identification | `User-Agent: curl/7.68.0` |

---

## HTTP Status Code Categories

| Range | Category | Examples |
|-------|----------|----------|
| **1xx** | Informational | 100 Continue, 101 Switching Protocols |
| **2xx** | Success | 200 OK, 201 Created, 204 No Content |
| **3xx** | Redirection | 301 Moved Permanently, 302 Found, 304 Not Modified |
| **4xx** | Client Error | 400 Bad Request, 403 Forbidden, 404 Not Found |
| **5xx** | Server Error | 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable |

---

## Proxy Terms

| Term | Definition | Example |
|------|------------|---------|
| **Proxy** | Intermediary server between client and destination | Forward proxy, reverse proxy |
| **Forward proxy** | Proxy configured by client to access internet | Corporate firewall proxy |
| **Reverse proxy** | Proxy deployed by server, transparent to clients | nginx in front of backends |
| **Load balancer** | Distributes requests across multiple servers | nginx, HAProxy |
| **Upstream** | Backend server(s) behind a reverse proxy | `upstream backend_pool {...}` |
| **Round-robin** | Cycling through backends sequentially | A → B → C → A → B → C |
| **Weighted round-robin** | Round-robin with proportional distribution | 5:3:1 weight ratio |
| **Least connections** | Route to server with fewest active connections | Dynamic load awareness |
| **Health check** | Periodic verification that backend is responsive | `HEAD /health` every 30s |
| **Sticky session** | Routing same client to same backend | Via cookie or IP hash |

---

## Proxy Headers

| Header | Direction | Purpose |
|--------|-----------|---------|
| **X-Forwarded-For** | Client → Proxy → Backend | Original client IP address |
| **X-Forwarded-Proto** | Client → Proxy → Backend | Original protocol (http/https) |
| **X-Forwarded-Host** | Client → Proxy → Backend | Original Host header |
| **X-Real-IP** | Proxy → Backend | Single client IP (nginx specific) |
| **Via** | Both | Proxies the request passed through |

---

## nginx Terms

| Term | Definition | Example |
|------|------------|---------|
| **nginx** | High-performance web server and reverse proxy | Pronounced "engine-x" |
| **Directive** | Configuration instruction in nginx.conf | `listen 80;` |
| **Block** | Group of directives in curly braces | `server { ... }` |
| **Location** | URL path matching block | `location /api { ... }` |
| **upstream** | Group of backend servers | `upstream backend { server ...; }` |
| **proxy_pass** | Forward request to backend | `proxy_pass http://backend;` |
| **worker** | nginx process handling connections | `worker_processes auto;` |

---

## Docker Networking Terms

| Term | Definition | Example |
|------|------------|---------|
| **Bridge network** | Default Docker network type — isolated network | `docker network create mynet` |
| **Port mapping** | Exposing container port on host | `-p 8080:80` (host:container) |
| **Container DNS** | Automatic DNS for container names | `ping backend1` from another container |
| **Network namespace** | Isolated network stack per container | Each container has own localhost |
| **docker-compose** | Multi-container orchestration tool | `docker compose up -d` |

---

## Security Terms

| Term | Definition | Example |
|------|------------|---------|
| **Directory traversal** | Attack using `..` to access files outside docroot | `GET /../../../etc/passwd` |
| **Path normalisation** | Resolving `.` and `..` in paths | `/a/b/../c` → `/a/c` |
| **TLS** | Transport Layer Security — encryption for TCP | HTTPS uses TLS |
| **Certificate** | Digital document proving server identity | Self-signed or CA-signed |
| **Rate limiting** | Restricting request frequency per client | 100 requests/minute |
| **Token bucket** | Rate limiting algorithm with burst tolerance | Bucket size = burst capacity |

---

## Commands Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `curl` | HTTP client for testing | `curl -v http://localhost:8080/` |
| `curl -I` | HEAD request only | `curl -I http://localhost:8080/` |
| `curl -X POST` | Specify HTTP method | `curl -X POST -d "data" http://...` |
| `netstat -tlnp` | Show listening TCP ports | `sudo netstat -tlnp \| grep 8080` |
| `ss -tlnp` | Modern netstat alternative | `ss -tlnp \| grep 8080` |
| `tcpdump` | Capture network traffic | `sudo tcpdump -i lo port 8080` |
| `docker ps` | List running containers | `docker ps` |
| `docker logs` | View container output | `docker logs nginx` |
| `docker exec` | Run command in container | `docker exec -it nginx bash` |

---

## Wireshark Filters

| Filter | Purpose |
|--------|---------|
| `http` | All HTTP traffic |
| `tcp.port == 8080` | Traffic on port 8080 |
| `tcp.flags.syn == 1` | TCP SYN packets (connection start) |
| `tcp.flags.fin == 1` | TCP FIN packets (connection end) |
| `http.request` | HTTP requests only |
| `http.response` | HTTP responses only |
| `http.response.code == 200` | Successful responses |
| `http.response.code >= 400` | Error responses |
| `ip.addr == 172.28.8.10` | Traffic to/from specific IP |
| `tcp.stream eq N` | Follow specific TCP connection |

---

## Acronyms

| Acronym | Full form | Context |
|---------|-----------|---------|
| TCP | Transmission Control Protocol | Transport layer |
| UDP | User Datagram Protocol | Transport layer |
| HTTP | HyperText Transfer Protocol | Application layer |
| HTTPS | HTTP Secure (HTTP over TLS) | Encrypted HTTP |
| TLS | Transport Layer Security | Encryption |
| SSL | Secure Sockets Layer (deprecated predecessor of TLS) | Legacy term |
| IP | Internet Protocol | Network layer |
| DNS | Domain Name System | Name resolution |
| URL | Uniform Resource Locator | Web address |
| URI | Uniform Resource Identifier | Resource identifier |
| MIME | Multipurpose Internet Mail Extensions | Content types |
| API | Application Programming Interface | Service interface |
| REST | Representational State Transfer | API architecture |
| CRLF | Carriage Return Line Feed | Line ending |
| RTT | Round-Trip Time | Latency measurement |
| MSS | Maximum Segment Size | TCP parameter |
| ACK | Acknowledgment | TCP flag |
| SYN | Synchronise | TCP flag |
| FIN | Finish | TCP flag |

---

## Relationships Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Protocol Stack                               │
├─────────────────────────────────────────────────────────────────────┤
│  Application    │  HTTP, HTTPS, DNS, FTP                            │
│  Layer          │  ↓ uses                                           │
├─────────────────┼───────────────────────────────────────────────────┤
│  Transport      │  TCP (reliable) │ UDP (fast)                      │
│  Layer          │  ↓ uses                                           │
├─────────────────┼───────────────────────────────────────────────────┤
│  Network        │  IP (addressing, routing)                         │
│  Layer          │  ↓ uses                                           │
├─────────────────┼───────────────────────────────────────────────────┤
│  Link           │  Ethernet, Wi-Fi                                  │
│  Layer          │                                                   │
└─────────────────┴───────────────────────────────────────────────────┘

HTTP → TCP → IP → Ethernet
 │       │     │
 │       │     └── Packet routing between networks
 │       └──────── Reliable, ordered delivery
 └──────────────── Request-response semantics
```

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
