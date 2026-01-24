# PCAP Examples — Week 10
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Reference packet captures for laboratory exercises

---

## Overview

This directory contains pre-generated packet captures demonstrating key networking concepts covered in Week 10. Use these as reference material when analysing your own captures.

---

## Available Captures

| File | Protocol | Description | Key Observations |
|------|----------|-------------|------------------|
| `dns_query_udp.pcap` | DNS/UDP | Standard A record query | Transaction ID, flags, question section |
| `dns_query_tcp.pcap` | DNS/TCP | DNS over TCP (large response) | 2-byte length prefix, same format |
| `tls_handshake_v13.pcap` | TLS 1.3 | Complete TLS handshake | ClientHello, ServerHello, encrypted extensions |
| `http_cleartext.pcap` | HTTP | Unencrypted web request | Headers and body visible |
| `https_encrypted.pcap` | HTTPS | Same request over TLS | Only SNI visible, body encrypted |
| `ftp_passive_transfer.pcap` | FTP | File download (passive mode) | Control (21) + data (high port) channels |
| `ssh_key_exchange.pcap` | SSH | SSH connection establishment | Key exchange algorithms, encrypted session |

---

## How to Use

### Opening in Wireshark

```bash
# Open specific capture
wireshark pcap/examples/dns_query_udp.pcap

# Or from command line with filter
tshark -r pcap/examples/dns_query_udp.pcap -Y "dns"
```

### Useful Wireshark Display Filters

| Protocol | Filter | Purpose |
|----------|--------|---------|
| DNS | `dns` | All DNS traffic |
| DNS queries only | `dns.flags.response == 0` | Only queries, not responses |
| TLS handshake | `tls.handshake` | TLS handshake messages |
| SNI extraction | `tls.handshake.extensions_server_name` | Server Name Indication |
| HTTP | `http` | HTTP requests and responses |
| FTP commands | `ftp.request.command` | FTP control channel commands |
| SSH | `ssh` | SSH protocol messages |

### Comparing HTTP vs HTTPS

1. Open `http_cleartext.pcap` — observe readable content
2. Open `https_encrypted.pcap` — same request, encrypted
3. Note: In HTTPS, only the destination IP and domain (via SNI) are visible

---

## Creating Your Own Captures

### DNS Capture

```bash
# Start capture
tcpdump -i any port 5353 -w artifacts/my_dns_capture.pcap &

# Generate traffic
dig @127.0.0.1 -p 5353 web.lab.local

# Stop capture
killall tcpdump
```

### HTTPS Capture

```bash
# Start capture on HTTPS port
tcpdump -i any port 8443 -w artifacts/my_https_capture.pcap &

# Generate traffic
curl -k https://127.0.0.1:8443/api/resources

# Stop capture
killall tcpdump
```

### FTP Capture

```bash
# Capture FTP control and data channels
tcpdump -i any 'port 2121 or portrange 30000-30009' -w artifacts/my_ftp_capture.pcap &

# Generate traffic
ftp -p localhost 2121
# Login and transfer a file

# Stop capture
killall tcpdump
```

---

## Analysis Exercises

### Exercise 1: DNS Query Analysis

1. Open `dns_query_udp.pcap` in Wireshark
2. Identify the following fields:
   - Transaction ID
   - Query flags (recursion desired, etc.)
   - Question section (QNAME, QTYPE)
   - Answer section (if present)

### Exercise 2: TLS Handshake Analysis

1. Open `tls_handshake_v13.pcap` in Wireshark
2. Follow the TLS stream
3. Identify:
   - Supported cipher suites in ClientHello
   - Selected cipher suite in ServerHello
   - Server Name Indication (SNI)
   - Certificate chain

### Exercise 3: FTP Dual-Channel Analysis

1. Open `ftp_passive_transfer.pcap` in Wireshark
2. Filter by `ftp` to see control channel
3. Identify the PASV response with data port
4. Filter by the data port to see file transfer
5. Note: Credentials are visible in plaintext!

---

## Learning Objectives Mapping

| PCAP | Learning Objective | Concepts Demonstrated |
|------|-------------------|----------------------|
| `dns_*.pcap` | LO3 | DNS message structure, UDP vs TCP |
| `tls_*.pcap` | LO1 | TLS certificates, handshake, SNI |
| `http*.pcap` | LO5 | Security comparison, encryption |
| `ftp_*.pcap` | LO4 | Protocol implementation, dual channels |
| `ssh_*.pcap` | LO4, LO5 | Secure protocols, key exchange |

---

## Student Captures Directory

Place your own captures in `pcap/student_captures/` for comparison with the reference files.

```
pcap/
├── examples/           # Reference captures (this directory)
│   └── *.pcap
└── student_captures/   # Your captures go here
    └── .gitkeep
```

---

## Troubleshooting

### "No packets captured"

- Ensure you start the capture BEFORE generating traffic
- Check you are using the correct network interface
- For Docker traffic in WSL, use the appropriate bridge interface

### "Permission denied"

- Run tcpdump with sudo: `sudo tcpdump ...`
- Or add your user to the wireshark group

### Captures are empty

- Verify the service is running: `docker ps`
- Check the port number matches your filter
- Try capturing on `any` interface: `tcpdump -i any ...`

---

*Computer Networks — Week 10 | ASE, CSIE Bucharest*
*Laboratory materials by ing. dr. Antonio Clim*
