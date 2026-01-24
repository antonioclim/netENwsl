#!/usr/bin/env python3
"""
Week 10 - Homework Assignment 3: DNS Configuration
===================================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

This template provides the structure for your custom DNS configuration.
You need to add your own DNS records and document the resolution process.

Usage:
    python3 hw_10_03_dns_tool.py serve     # Start your custom DNS server
    python3 hw_10_03_dns_tool.py test      # Test your DNS records
    python3 hw_10_03_dns_tool.py trace     # Document resolution process

TODO (Student):
1. Add your custom A record for student.lab.local
2. Add CNAME record for www.student.lab.local
3. Add TXT record with your name
4. Document the resolution process
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import socket
import struct
import sys
import threading
from typing import Dict, List, Tuple

try:
    import dns.message
    import dns.query
    import dns.rdatatype
    import dns.resolver
except ImportError:
    print("[ERROR] dnspython required: pip install dnspython")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# DNS_RECORDS_CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
"""
TODO (Student): Configure your custom DNS records below.

The RECORDS dictionary maps domain names to their DNS records.
Each record is a tuple of (record_type, value, ttl).

Record types:
- "A": IPv4 address (e.g., "192.168.1.100")
- "CNAME": Canonical name (e.g., "student.lab.local")
- "TXT": Text record (e.g., "Your Name Here")

Example:
    "myhost.lab.local": [("A", "10.20.30.40", 300)],
    "alias.lab.local": [("CNAME", "myhost.lab.local", 300)],
    "myhost.lab.local": [("TXT", "Student: John Doe", 300)],
"""

# Base records from the lab (do not modify these)
BASE_RECORDS: Dict[str, List[Tuple[str, str, int]]] = {
    "myservice.lab.local": [("A", "10.10.10.10", 300)],
    "api.lab.local": [("A", "10.10.10.20", 300)],
    "web.lab.local": [("A", "172.20.0.10", 300)],
    "ssh.lab.local": [("A", "172.20.0.22", 300)],
    "ftp.lab.local": [("A", "172.20.0.21", 300)],
}

# TODO (Student): Add your custom records here
CUSTOM_RECORDS: Dict[str, List[Tuple[str, str, int]]] = {
    # Example (replace with your records):
    # "student.lab.local": [("A", "10.10.10.100", 300)],
    # "www.student.lab.local": [("CNAME", "student.lab.local", 300)],
    # "student.lab.local": [("TXT", "Student: [Your Name Here]", 300)],
    
    # 💭 PREDICTION: What IP will www.student.lab.local resolve to?
    # Answer: It will resolve to the IP of student.lab.local because CNAME is an alias
}

# Merge base and custom records
RECORDS = {**BASE_RECORDS, **CUSTOM_RECORDS}


# ═══════════════════════════════════════════════════════════════════════════════
# DNS_SERVER
# ═══════════════════════════════════════════════════════════════════════════════
DNS_PORT = 15353  # Use non-privileged port for testing


def build_dns_response(query: bytes, records: Dict) -> bytes:
    """
    Build a DNS response for the given query.
    
    This is a simplified DNS server for educational purposes.
    It handles A, CNAME and TXT records.
    
    TODO (Student): Study this function to understand DNS message structure
    """
    try:
        msg = dns.message.from_wire(query)
    except Exception:
        return b""
    
    response = dns.message.make_response(msg)
    
    for question in msg.question:
        qname = str(question.name).rstrip(".")
        qtype = question.rdtype
        
        if qname.lower() in records:
            for rtype, rdata, ttl in records[qname.lower()]:
                if rtype == "A" and qtype in (dns.rdatatype.A, dns.rdatatype.ANY):
                    rrset = response.find_rrset(
                        response.answer, question.name, 
                        dns.rdataclass.IN, dns.rdatatype.A, create=True
                    )
                    rrset.add(dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.A, rdata), ttl)
                    
                elif rtype == "CNAME" and qtype in (dns.rdatatype.CNAME, dns.rdatatype.ANY, dns.rdatatype.A):
                    rrset = response.find_rrset(
                        response.answer, question.name,
                        dns.rdataclass.IN, dns.rdatatype.CNAME, create=True
                    )
                    rrset.add(dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.CNAME, rdata + "."), ttl)
                    
                elif rtype == "TXT" and qtype in (dns.rdatatype.TXT, dns.rdatatype.ANY):
                    rrset = response.find_rrset(
                        response.answer, question.name,
                        dns.rdataclass.IN, dns.rdatatype.TXT, create=True
                    )
                    rrset.add(dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.TXT, f'"{rdata}"'), ttl)
        else:
            # NXDOMAIN - domain not found
            response.set_rcode(dns.rcode.NXDOMAIN)
    
    return response.to_wire()


def run_dns_server(port: int = DNS_PORT) -> None:
    """
    Run a simple UDP DNS server.
    
    💭 PREDICTION: Why does this DNS server use UDP?
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", port))
    
    print(f"[INFO] DNS server running on 127.0.0.1:{port}")
    print("[INFO] Press Ctrl+C to stop")
    print(f"\n[INFO] Test with: dig @127.0.0.1 -p {port} student.lab.local")
    
    try:
        while True:
            data, addr = sock.recvfrom(512)
            response = build_dns_response(data, RECORDS)
            if response:
                sock.sendto(response, addr)
    except KeyboardInterrupt:
        pass
    finally:
        sock.close()
        print("\n[INFO] DNS server stopped")


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_RECORDS
# ═══════════════════════════════════════════════════════════════════════════════
def test_dns_records(server: str = "127.0.0.1", port: int = DNS_PORT) -> None:
    """
    Test all configured DNS records.
    
    TODO (Student): Add tests for your custom records
    """
    print(f"\n[TEST] Testing DNS records against {server}:{port}\n")
    
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [server]
    resolver.port = port
    
    # Test base records
    test_domains = [
        ("web.lab.local", "A"),
        ("ssh.lab.local", "A"),
    ]
    
    # TODO (Student): Add your custom domains to test
    # test_domains.append(("student.lab.local", "A"))
    # test_domains.append(("www.student.lab.local", "CNAME"))
    # test_domains.append(("student.lab.local", "TXT"))
    
    for domain, rtype in test_domains:
        try:
            answers = resolver.resolve(domain, rtype)
            print(f"[OK]   {domain} ({rtype}): {[str(r) for r in answers]}")
        except dns.resolver.NXDOMAIN:
            print(f"[FAIL] {domain} ({rtype}): NXDOMAIN")
        except dns.resolver.NoAnswer:
            print(f"[FAIL] {domain} ({rtype}): No answer")
        except Exception as e:
            print(f"[FAIL] {domain} ({rtype}): {e}")
    
    print("\n[INFO] Test complete")


# ═══════════════════════════════════════════════════════════════════════════════
# RESOLUTION_TRACE
# ═══════════════════════════════════════════════════════════════════════════════
RESOLUTION_TRACE_TEMPLATE = """# DNS Resolution Process Documentation

## Student: [YOUR NAME HERE]
## Date: [DATE]

---

## 1. Custom DNS Records Added

| Domain | Type | Value | TTL |
|--------|------|-------|-----|
| student.lab.local | A | [YOUR IP] | 300 |
| www.student.lab.local | CNAME | student.lab.local | 300 |
| student.lab.local | TXT | "[YOUR NAME]" | 300 |

---

## 2. Resolution Trace for student.lab.local

### Command Used
```bash
dig @127.0.0.1 -p {port} student.lab.local
```

### Output
```
[PASTE DIG OUTPUT HERE]
```

### Explanation of Each Section

#### HEADER
- Flags: [QR, RD, RA, etc. - explain what they mean]
- QUERY: [number of queries]
- ANSWER: [number of answers]

#### QUESTION SECTION
[What was asked]

#### ANSWER SECTION
[What was returned, explain the record]

---

## 3. Resolution Trace for www.student.lab.local (CNAME)

### Command Used
```bash
dig @127.0.0.1 -p {port} www.student.lab.local
```

### Output
```
[PASTE DIG OUTPUT HERE]
```

### Explanation
[Explain how CNAME resolution works - the alias is resolved first, 
then the target domain is resolved]

---

## 4. Wireshark Capture Analysis

### Screenshot
[Include screenshot of DNS query/response in Wireshark]

### Observations
- Query packet size: [XX bytes]
- Response packet size: [XX bytes]
- Transaction ID match: [yes/no]
- UDP port used: [53 or your custom port]

---

## 5. Conclusions

[Write 100-150 words about what you learned from this exercise.
Include: how DNS resolution works, the role of TTL, CNAME behaviour.]

"""


def generate_trace_template() -> None:
    """Generate the resolution trace template."""
    template = RESOLUTION_TRACE_TEMPLATE.format(port=DNS_PORT)
    output_path = "resolution_trace.md"
    
    with open(output_path, "w") as f:
        f.write(template)
    
    print(f"[INFO] Created template: {output_path}")
    print("[INFO] Fill in the template with your dig outputs and analysis")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    parser = argparse.ArgumentParser(description="DNS Configuration Tool for Week 10 Homework")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    subparsers.add_parser("serve", help="Start the DNS server")
    subparsers.add_parser("test", help="Test DNS records")
    subparsers.add_parser("trace", help="Generate resolution trace template")
    
    args = parser.parse_args()
    
    if args.command == "serve":
        if not CUSTOM_RECORDS:
            print("[WARNING] No custom records defined!")
            print("[INFO] Edit CUSTOM_RECORDS in this file to add your records")
        run_dns_server()
        
    elif args.command == "test":
        test_dns_records()
        
    elif args.command == "trace":
        generate_trace_template()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
