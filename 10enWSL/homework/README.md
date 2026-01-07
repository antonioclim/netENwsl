# Week 10: Homework Assignments

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by Revolvix

## Overview

These homework exercises extend the laboratory work on HTTP/HTTPS, REST API design, and network services. Complete these assignments to reinforce your understanding of application layer protocols.

## Assignment 1: Extended REST API Service

**Objective:** Design and implement a RESTful API that achieves Richardson Maturity Level 3 (HATEOAS).

**Requirements:**
1. Create a resource management API (e.g., library books, inventory items, student records)
2. Implement all CRUD operations with proper HTTP methods
3. Include hypermedia links in all responses
4. Document your API endpoints

**Deliverables:**
- `hw_10_01_rest_api.py` - Flask application implementing your API
- `hw_10_01_client.py` - Client script demonstrating all operations
- Brief documentation (comments or separate markdown)

**Evaluation Criteria:**
- Correct use of HTTP methods (GET, POST, PUT, DELETE)
- Proper status codes (200, 201, 204, 400, 404)
- HATEOAS implementation with `_links` in responses
- Clean, well-documented code

## Assignment 2: Multi-Protocol Network Analyser

**Objective:** Create a Python tool that tests connectivity across multiple application layer protocols.

**Requirements:**
1. Test HTTP/HTTPS endpoints (with certificate validation handling)
2. Perform DNS lookups (both standard and custom DNS servers)
3. Establish SSH connections and execute commands
4. Connect to FTP servers and list directories

**Deliverables:**
- `hw_10_02_analyser.py` - Multi-protocol testing tool
- Sample output showing tests against the laboratory services

**Evaluation Criteria:**
- Handles connection failures gracefully
- Provides clear output for each protocol test
- Uses appropriate libraries (requests, dns.resolver, paramiko, ftplib)
- Configurable via command-line arguments

## Assignment 3: TLS Certificate Inspector (Bonus)

**Objective:** Build a tool that inspects and reports on TLS certificates.

**Requirements:**
1. Connect to HTTPS servers and retrieve certificate information
2. Display: issuer, subject, validity period, key algorithm
3. Check for common issues (expired, self-signed, weak algorithms)
4. Support multiple target URLs

**Deliverables:**
- `hw_10_03_tls_inspector.py` - Certificate inspection tool

## Submission Guidelines

1. Place completed exercises in the `exercises/` directory
2. Test your code against the laboratory Docker services
3. Include any additional dependencies in a `requirements.txt` file
4. Submit via the course portal before the deadline

## Hints and Resources

- Use `ssl` and `socket` modules for TLS inspection
- Refer to `src/exercises/ex_10_01_https.py` for HTTPS server patterns
- The laboratory `debug` container includes useful tools for testing
- Richardson Maturity Model: https://martinfowler.com/articles/richardsonMaturityModel.html

## Grading Rubric

| Criterion | Points |
|-----------|--------|
| Functionality | 40% |
| Code quality and documentation | 25% |
| Error handling | 20% |
| Bonus assignment | 15% |

---

*NETWORKING class - ASE, Informatics | by Revolvix*
