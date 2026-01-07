# Homework — Week 8

> NETWORKING class - ASE, Informatics | by Revolvix

## Overview

These assignments extend the laboratory exercises and should be completed independently before the next session. They reinforce concepts of HTTP server implementation, reverse proxy operation, and load balancing mechanisms.

## Submission Guidelines

- Complete the Python files in `exercises/`
- Test your implementations thoroughly
- Document any assumptions in code comments
- Submit via the course platform before the deadline

## Assignment 1: HTTPS Server with TLS

**File:** `exercises/hw_8_01_https_server.py`

**Objective:** Extend the basic HTTP server to support HTTPS connections using TLS.

**Requirements:**

1. Generate a self-signed certificate (instructions provided in file)
2. Implement TLS wrapping for the server socket
3. Handle both HTTP (port 8080) and HTTPS (port 8443) connections
4. Implement proper certificate verification logging

**Learning Outcomes:**

- Understand TLS handshake process
- Apply socket wrapping with ssl module
- Configure certificate-based security

**Estimated Time:** 90-120 minutes

**Grading Criteria:**

| Criterion | Points |
|-----------|--------|
| TLS socket implementation | 30 |
| Certificate generation | 20 |
| Dual-port support | 20 |
| Error handling | 15 |
| Code quality | 15 |
| **Total** | **100** |

## Assignment 2: Weighted Load Balancer

**File:** `exercises/hw_8_02_weighted_balancer.py`

**Objective:** Implement a weighted round-robin load balancer that distributes requests according to backend capacity.

**Requirements:**

1. Accept backend configuration with weights (e.g., `{"backend1": 5, "backend2": 3, "backend3": 1}`)
2. Distribute requests proportionally to weights
3. Implement health checking with automatic failover
4. Log distribution statistics

**Learning Outcomes:**

- Implement weighted distribution algorithms
- Apply health monitoring patterns
- Design resilient proxy systems

**Estimated Time:** 120-150 minutes

**Grading Criteria:**

| Criterion | Points |
|-----------|--------|
| Weighted algorithm correctness | 35 |
| Health checking | 25 |
| Failover mechanism | 20 |
| Statistics logging | 10 |
| Code quality | 10 |
| **Total** | **100** |

## Testing Your Solutions

### Assignment 1 Testing

```bash
# Generate certificate
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Start your HTTPS server
python homework/exercises/hw_8_01_https_server.py

# Test HTTP
curl http://localhost:8080/

# Test HTTPS (ignore certificate validation for self-signed)
curl -k https://localhost:8443/

# Verify TLS version
openssl s_client -connect localhost:8443 -tls1_3
```

### Assignment 2 Testing

```bash
# Start three backend servers (in separate terminals)
python -m http.server 8001 --directory www/
python -m http.server 8002 --directory www/
python -m http.server 8003 --directory www/

# Start your load balancer
python homework/exercises/hw_8_02_weighted_balancer.py

# Test distribution (should follow 5:3:1 ratio)
for i in {1..18}; do curl -s http://localhost:8000/ ; done

# Test failover (stop one backend, verify redirection)
```

## Resources

- Python `ssl` module documentation: https://docs.python.org/3/library/ssl.html
- OpenSSL certificate generation: https://www.openssl.org/docs/
- Load balancing algorithms: `docs/further_reading.md`

## Academic Integrity

- You may discuss concepts with classmates
- Code must be your own work
- Cite any external resources used
- Plagiarism will result in zero marks

---

*NETWORKING class - ASE, Informatics | by Revolvix*
