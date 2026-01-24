# 📖 Glossary — Week 10: Application Layer Protocols
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## HTTP/HTTPS Terms

| Term | Definition | Example |
|------|------------|---------|
| **HTTP** | Hypertext Transfer Protocol — stateless request-response protocol for web communication | `GET /index.html HTTP/1.1` |
| **HTTPS** | HTTP over TLS — encrypted HTTP using Transport Layer Security | `https://example.com` |
| **TLS** | Transport Layer Security — cryptographic protocol providing encryption, authentication and integrity | TLS 1.3 handshake |
| **SSL** | Secure Sockets Layer — deprecated predecessor to TLS (avoid using) | SSL 3.0 (obsolete) |
| **SNI** | Server Name Indication — TLS extension that sends hostname in plaintext during handshake | Visible in Wireshark |
| **Certificate** | X.509 digital certificate binding a public key to an identity | `server.crt` |
| **CA** | Certificate Authority — trusted entity that issues certificates | Let's Encrypt, DigiCert |
| **Self-signed certificate** | Certificate signed by its own private key, not a CA | Used in development |
| **Cipher suite** | Set of algorithms for key exchange, encryption and MAC | `TLS_AES_256_GCM_SHA384` |

### HTTP Methods

| Method | Purpose | Idempotent? | Safe? |
|--------|---------|-------------|-------|
| **GET** | Retrieve resource | Yes | Yes |
| **POST** | Create resource or submit data | No | No |
| **PUT** | Replace resource entirely | Yes | No |
| **PATCH** | Partial resource update | No | No |
| **DELETE** | Remove resource | Yes | No |
| **HEAD** | GET without body (metadata only) | Yes | Yes |
| **OPTIONS** | Query supported methods | Yes | Yes |

### HTTP Status Codes

| Code | Category | Meaning | Example |
|------|----------|---------|---------|
| **200** | Success | OK | Successful GET |
| **201** | Success | Created | Successful POST |
| **204** | Success | No Content | Successful DELETE |
| **301** | Redirect | Moved Permanently | URL changed |
| **304** | Redirect | Not Modified | Cache still valid |
| **400** | Client Error | Bad Request | Malformed JSON |
| **401** | Client Error | Unauthorised | Missing credentials |
| **403** | Client Error | Forbidden | Insufficient permissions |
| **404** | Client Error | Not Found | Resource doesn't exist |
| **500** | Server Error | Internal Server Error | Server crashed |
| **503** | Server Error | Service Unavailable | Server overloaded |

---

## REST Terms

| Term | Definition | Example |
|------|------------|---------|
| **REST** | Representational State Transfer — architectural style for distributed systems | RESTful API design |
| **Resource** | Any named information (document, image, service) addressable by URI | `/users/123` |
| **URI** | Uniform Resource Identifier — unique address for a resource | `/api/v1/products/42` |
| **Endpoint** | Specific URI where API operations are available | `POST /api/users` |
| **CRUD** | Create, Read, Update, Delete — basic data operations | Maps to POST, GET, PUT, DELETE |
| **Stateless** | Server stores no client context between requests | Each request is independent |
| **HATEOAS** | Hypermedia as the Engine of Application State — responses include navigation links | `"_links": {"self": "/users/1"}` |
| **Idempotent** | Multiple identical requests have same effect as one request | GET, PUT, DELETE |

### Richardson Maturity Model

| Level | Name | Characteristics |
|-------|------|-----------------|
| **Level 0** | The Swamp of POX | Single URI, single HTTP method, RPC-style |
| **Level 1** | Resources | Multiple URIs for different resources |
| **Level 2** | HTTP Verbs | Proper use of GET, POST, PUT, DELETE |
| **Level 3** | Hypermedia Controls | HATEOAS links in responses |

---

## DNS Terms

| Term | Definition | Example |
|------|------------|---------|
| **DNS** | Domain Name System — hierarchical naming system translating names to IPs | `google.com → 142.250.x.x` |
| **Resolver** | DNS client that queries DNS servers | Your computer's DNS client |
| **Authoritative server** | DNS server with definitive records for a domain | `ns1.google.com` |
| **Recursive resolver** | Server that queries other servers on behalf of clients | 8.8.8.8, 1.1.1.1 |
| **Zone** | Administrative domain in DNS namespace | `example.com` zone |
| **TTL** | Time To Live — how long a record can be cached (seconds) | `TTL: 300` (5 minutes) |
| **FQDN** | Fully Qualified Domain Name — complete domain with root | `www.example.com.` |

### DNS Record Types

| Type | Purpose | Example |
|------|---------|---------|
| **A** | IPv4 address | `example.com. A 93.184.216.34` |
| **AAAA** | IPv6 address | `example.com. AAAA 2606:2800:...` |
| **CNAME** | Canonical name (alias) | `www.example.com. CNAME example.com.` |
| **MX** | Mail exchanger | `example.com. MX 10 mail.example.com.` |
| **NS** | Name server | `example.com. NS ns1.example.com.` |
| **TXT** | Arbitrary text (SPF, DKIM, etc.) | `example.com. TXT "v=spf1..."` |
| **PTR** | Reverse DNS (IP to name) | `34.216.184.93.in-addr.arpa. PTR example.com.` |
| **SOA** | Start of Authority (zone metadata) | Serial, refresh, retry, expire |

---

## SSH Terms

| Term | Definition | Example |
|------|------------|---------|
| **SSH** | Secure Shell — encrypted protocol for remote access | `ssh user@host` |
| **Public key** | Shareable key for encryption/verification | `id_rsa.pub` |
| **Private key** | Secret key for decryption/signing | `id_rsa` (never share!) |
| **Key pair** | Mathematically linked public and private keys | RSA, Ed25519 |
| **Known hosts** | File storing trusted server fingerprints | `~/.ssh/known_hosts` |
| **Agent** | Program holding decrypted private keys in memory | `ssh-agent` |
| **Port forwarding** | Tunnelling traffic through SSH | `-L 8080:localhost:80` |
| **SCP** | Secure Copy — file transfer over SSH | `scp file user@host:/path` |
| **SFTP** | SSH File Transfer Protocol — FTP-like interface over SSH | `sftp user@host` |

---

## FTP Terms

| Term | Definition | Example |
|------|------------|---------|
| **FTP** | File Transfer Protocol — multi-channel file transfer | Port 21 (control) |
| **Control channel** | Persistent connection for commands | USER, PASS, LIST, RETR |
| **Data channel** | Separate connection for file/listing transfer | Port 20 or high port |
| **Active mode** | Server connects to client for data transfer | Client behind NAT = problem |
| **Passive mode** | Client connects to server for data transfer | NAT-friendly, preferred |
| **PASV** | Command to enter passive mode | `227 Entering Passive Mode` |
| **Binary mode** | Transfer files as raw bytes | For executables, images |
| **ASCII mode** | Transfer with line-ending conversion | For text files |
| **Anonymous FTP** | Login without credentials (user: anonymous) | Public file servers |

### FTP Response Codes

| Code | Meaning |
|------|---------|
| **220** | Service ready |
| **230** | User logged in |
| **150** | File status okay, opening data connection |
| **226** | Transfer complete |
| **331** | Username okay, need password |
| **530** | Not logged in |
| **550** | Requested action not taken (file not found, etc.) |

---

## Cryptography Terms (for TLS/SSH)

| Term | Definition | Example |
|------|------------|---------|
| **Symmetric encryption** | Same key encrypts and decrypts | AES, ChaCha20 |
| **Asymmetric encryption** | Different keys for encrypt/decrypt | RSA, ECDSA |
| **Key exchange** | Protocol to establish shared secret | Diffie-Hellman, ECDH |
| **Hash function** | One-way function producing fixed-size digest | SHA-256 |
| **MAC** | Message Authentication Code — integrity verification | HMAC-SHA256 |
| **Digital signature** | Asymmetric authentication of data | RSA signature |
| **Handshake** | Initial negotiation establishing secure parameters | TLS handshake |

---

## Commands Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `curl` | HTTP client | `curl -X GET http://localhost:8000` |
| `dig` | DNS lookup utility | `dig @8.8.8.8 example.com` |
| `nslookup` | DNS query tool | `nslookup example.com` |
| `ssh` | SSH client | `ssh -p 2222 user@localhost` |
| `scp` | Secure copy | `scp file.txt user@host:/path/` |
| `ftp` | FTP client | `ftp -p server.example.com` |
| `openssl` | TLS/crypto toolkit | `openssl s_client -connect host:443` |
| `nc` (netcat) | Network utility | `nc -zv localhost 8080` |

---

## Acronyms

| Acronym | Full form | Context |
|---------|-----------|---------|
| API | Application Programming Interface | REST APIs |
| CA | Certificate Authority | TLS certificates |
| CRUD | Create, Read, Update, Delete | Database/API operations |
| DNS | Domain Name System | Name resolution |
| DoH | DNS over HTTPS | Encrypted DNS |
| DoT | DNS over TLS | Encrypted DNS |
| FQDN | Fully Qualified Domain Name | Complete domain name |
| FTP | File Transfer Protocol | File transfers |
| HATEOAS | Hypermedia as Engine of Application State | REST Level 3 |
| HTTP | Hypertext Transfer Protocol | Web communication |
| HTTPS | HTTP Secure | Encrypted web |
| JSON | JavaScript Object Notation | Data format |
| MAC | Message Authentication Code | Integrity |
| REST | Representational State Transfer | API architecture |
| RPC | Remote Procedure Call | Function-style API |
| SCP | Secure Copy | File transfer over SSH |
| SFTP | SSH File Transfer Protocol | Secure FTP alternative |
| SNI | Server Name Indication | TLS extension |
| SSH | Secure Shell | Remote access |
| SSL | Secure Sockets Layer | Deprecated, use TLS |
| TLS | Transport Layer Security | Encryption protocol |
| TTL | Time To Live | Caching duration |
| URI | Uniform Resource Identifier | Resource address |
| URL | Uniform Resource Locator | Web address |

---

*Computer Networks — Week 10 | ASE, CSIE Bucharest*
*Glossary compiled by ing. dr. Antonio Clim*
