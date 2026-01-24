# 📋 Commands Cheatsheet — Week 10
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Quick reference for HTTP, DNS, SSH and FTP commands

---

## curl — HTTP Client

### Basic Requests

```bash
# GET request
curl http://localhost:8000/
curl -X GET http://localhost:8000/api/resources

# POST with JSON body
curl -X POST http://localhost:8000/api/resources \
  -H "Content-Type: application/json" \
  -d '{"name": "example", "value": 42}'

# PUT (update)
curl -X PUT http://localhost:8000/api/resources/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "updated", "value": 100}'

# DELETE
curl -X DELETE http://localhost:8000/api/resources/1

# PATCH (partial update)
curl -X PATCH http://localhost:8000/api/resources/1 \
  -H "Content-Type: application/json" \
  -d '{"value": 200}'
```

### HTTPS and Certificates

```bash
# HTTPS with self-signed cert (skip verification)
curl -k https://127.0.0.1:8443/

# Show certificate info
curl -vk https://127.0.0.1:8443/ 2>&1 | grep -A 10 "Server certificate"

# Use specific CA bundle
curl --cacert /path/to/ca.crt https://example.com/
```

### Useful Options

```bash
# Verbose output (see headers)
curl -v http://localhost:8000/

# Show only headers
curl -I http://localhost:8000/

# Follow redirects
curl -L http://example.com/

# Save output to file
curl -o output.html http://localhost:8000/

# Include response headers in output
curl -i http://localhost:8000/

# Send custom header
curl -H "Authorization: Bearer token123" http://localhost:8000/

# Timeout (seconds)
curl --connect-timeout 5 --max-time 10 http://localhost:8000/

# Silent mode (no progress)
curl -s http://localhost:8000/

# Pretty print JSON (pipe to jq)
curl -s http://localhost:8000/api/resources | jq .
```

---

## dig — DNS Lookup

### Basic Queries

```bash
# Query default DNS server
dig example.com

# Query specific server
dig @8.8.8.8 example.com

# Query lab DNS server (port 5353)
dig @127.0.0.1 -p 5353 web.lab.local

# Short output (IP only)
dig @127.0.0.1 -p 5353 web.lab.local +short
```

### Record Types

```bash
# A record (IPv4)
dig example.com A

# AAAA record (IPv6)
dig example.com AAAA

# MX record (mail servers)
dig example.com MX

# NS record (name servers)
dig example.com NS

# TXT record
dig example.com TXT

# ANY (all records) - often blocked
dig example.com ANY

# SOA (Start of Authority)
dig example.com SOA
```

### Advanced Options

```bash
# Force TCP (instead of UDP)
dig @8.8.8.8 example.com +tcp

# Trace resolution path
dig example.com +trace

# Reverse lookup (IP to name)
dig -x 8.8.8.8

# Show query time
dig example.com +stats

# No comments (cleaner output)
dig example.com +nocomments

# Minimal output
dig example.com +short +noall +answer
```

### Lab DNS Server Queries

```bash
# Pre-configured domains in lab
dig @127.0.0.1 -p 5353 myservice.lab.local    # → 10.10.10.10
dig @127.0.0.1 -p 5353 api.lab.local          # → 10.10.10.20
dig @127.0.0.1 -p 5353 web.lab.local          # → 172.20.0.10
dig @127.0.0.1 -p 5353 ssh.lab.local          # → 172.20.0.22
dig @127.0.0.1 -p 5353 ftp.lab.local          # → 172.20.0.21
```

---

## ssh — Secure Shell

### Basic Connection

```bash
# Connect to server
ssh user@hostname

# Connect with specific port
ssh -p 2222 labuser@localhost

# Connect to lab SSH server
ssh -p 2222 labuser@localhost
# Password: labpass
```

### Key-Based Authentication

```bash
# Generate key pair
ssh-keygen -t ed25519 -C "your_email@example.com"
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Copy public key to server
ssh-copy-id user@hostname
ssh-copy-id -p 2222 user@hostname

# Use specific key file
ssh -i ~/.ssh/my_key user@hostname
```

### Port Forwarding

```bash
# Local forwarding (access remote:80 via localhost:8080)
ssh -L 8080:localhost:80 user@remote

# Remote forwarding (expose local:3000 on remote:8080)
ssh -R 8080:localhost:3000 user@remote

# Dynamic SOCKS proxy
ssh -D 1080 user@remote
```

### Useful Options

```bash
# Execute command and exit
ssh user@host "ls -la /tmp"

# Verbose (debugging)
ssh -v user@host
ssh -vvv user@host  # More verbose

# Disable host key checking (insecure, for lab only!)
ssh -o StrictHostKeyChecking=no user@host

# Keep connection alive
ssh -o ServerAliveInterval=60 user@host

# Run in background
ssh -fN -L 8080:localhost:80 user@host
```

### SSH Config File (~/.ssh/config)

```
Host lab-ssh
    HostName localhost
    Port 2222
    User labuser

Host myserver
    HostName server.example.com
    User admin
    IdentityFile ~/.ssh/server_key
```

Then connect with: `ssh lab-ssh`

---

## ftp — File Transfer

### Basic Connection

```bash
# Connect to FTP server
ftp hostname
ftp -p hostname          # Passive mode (recommended)
ftp hostname port        # Custom port

# Connect to lab FTP server
ftp -p 127.0.0.1 2121
# User: labftp, Password: labftp
```

### FTP Commands (inside ftp session)

```bash
# Navigation
pwd                      # Print working directory
ls                       # List files
cd directory             # Change directory
lcd local_dir            # Change local directory

# Transfer modes
binary                   # Binary mode (for executables, images)
ascii                    # ASCII mode (for text files)

# Download
get filename             # Download single file
mget *.txt               # Download multiple files

# Upload
put filename             # Upload single file
mput *.txt               # Upload multiple files

# Directory operations
mkdir dirname            # Create directory
rmdir dirname            # Remove directory

# File operations
delete filename          # Delete file
rename old new           # Rename file

# Connection
passive                  # Toggle passive mode
quit                     # Close connection
bye                      # Same as quit
```

### lftp — Advanced FTP Client

```bash
# Connect
lftp ftp://labftp:labftp@localhost:2121

# Mirror directory (download)
lftp -e "mirror /remote/dir /local/dir; quit" ftp://user:pass@host

# Mirror directory (upload)
lftp -e "mirror -R /local/dir /remote/dir; quit" ftp://user:pass@host
```

---

## openssl — TLS/Crypto Toolkit

### Certificate Operations

```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout server.key -out server.crt -days 365 \
  -subj "/CN=localhost"

# View certificate details
openssl x509 -in server.crt -text -noout

# Verify certificate chain
openssl verify -CAfile ca.crt server.crt
```

### TLS Connection Testing

```bash
# Connect to HTTPS server
openssl s_client -connect example.com:443

# With SNI (required for virtual hosting)
openssl s_client -connect example.com:443 -servername example.com

# Show certificate chain
openssl s_client -connect example.com:443 -showcerts

# Test specific TLS version
openssl s_client -connect example.com:443 -tls1_2
openssl s_client -connect example.com:443 -tls1_3
```

### Certificate Inspection

```bash
# Check certificate expiry
openssl s_client -connect example.com:443 2>/dev/null | \
  openssl x509 -noout -dates

# Get certificate fingerprint
openssl x509 -in cert.crt -noout -fingerprint -sha256
```

---

## netcat (nc) — Network Utility

```bash
# Test if port is open
nc -zv localhost 8000

# Simple TCP client
nc localhost 8000

# Listen on port (server)
nc -l 8000

# UDP mode
nc -u localhost 5353
```

---

## Docker Commands (for this lab)

```bash
# Start lab
cd /mnt/d/NETWORKING/WEEK10/10enWSL
docker compose -f docker/docker-compose.yml up -d

# Stop lab
docker compose -f docker/docker-compose.yml down

# View logs
docker logs week10_web
docker logs week10_dns
docker logs week10_ssh
docker logs week10_ftp

# Enter debug container
docker exec -it week10_debug bash

# Check container status
docker ps --filter "name=week10"
```

---

## Quick Reference Card

| Task | Command |
|------|---------|
| HTTP GET | `curl http://localhost:8000/` |
| HTTP POST JSON | `curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' URL` |
| HTTPS (self-signed) | `curl -k https://localhost:8443/` |
| DNS query | `dig @127.0.0.1 -p 5353 domain +short` |
| DNS with TCP | `dig @server domain +tcp` |
| SSH connect | `ssh -p 2222 user@localhost` |
| FTP connect | `ftp -p localhost 2121` |
| Test port | `nc -zv localhost 8000` |
| TLS test | `openssl s_client -connect host:443` |

---

*Computer Networks — Week 10 | ASE, CSIE Bucharest*
*Commands cheatsheet by ing. dr. Antonio Clim*
