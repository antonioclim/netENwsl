# Homework — Week 10: Application Layer Protocols
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> HTTP/HTTPS, REST Architecture and Network Services

---

## 📋 Submission Requirements

- **Deadline:** As announced on the course platform
- **Format:** ZIP archive containing your solutions
- **Naming:** `Week10_Homework_<NumeStudent>.zip`

---

## Academic Integrity — Anti-AI Verification Bundle (mandatory)

Week 10 includes a short interactive verification routine that confirms you
personally interacted with the laboratory environment within a limited time
window. This is designed to support fair assessment and does not attempt to
detect AI text.

Include the following in your submission ZIP:

- `artifacts/challenge_<YourID>_week10.yaml` (generated at the beginning)
- `artifacts/validation_report_<YourID>_week10.json` (generated at the end)
- At least one capture file in `artifacts/` (`*.pcap` or `*.pcapng`) containing
  the required header from the challenge file
- Any additional artefacts produced for the challenges (for example, the FTP
  proof file and your DNS server modification)

Recommended workflow:

1) Generate your personalised challenge (do this first):

   `python -m anti_cheat.challenge_generator --student-id <YourID>`

2) Start the lab environment:

   `python scripts/start_lab.py`

3) Complete the four micro-challenges described in the generated YAML file:

   - DNS TXT record in `docker/dns-server/dns_server.py` under `STATIC_TXT_RECORDS`
   - HTTPS verification endpoint by starting Exercise 1 with:
     `python src/exercises/ex_10_01_tls_rest_crud.py serve --challenge <challenge.yaml>`
     (the HTTPS port is taken from the challenge file)
   - FTP upload to `/uploads/` using the filename and content from the challenge
   - PCAP capture containing the required HTTP header `X-Student-Verify: ...`

4) Run the validator while the lab services and HTTPS server are running:

   `python -m anti_cheat.submission_validator --challenge <challenge.yaml> --report <report.json> --verbose`

---

## 📝 Assignment 1: HTTPS Traffic Analysis (30 points)

### Objective
Analyse the difference between HTTP and HTTPS traffic using Wireshark.

### Tasks

1. **Capture HTTP traffic** (10 points)
   - Start the lab web server
   - Capture traffic while making requests to `http://localhost:8000/`
   - Identify: HTTP methods, headers, response body

2. **Capture HTTPS traffic** (10 points)
   - Generate a self-signed certificate
   - Start the HTTPS server on port 8443 (or on the port specified by your challenge file)
   - Capture traffic while making requests
   - Identify: TLS handshake messages, encrypted application data

3. **Written analysis** (10 points)
   - Compare what is visible in HTTP vs HTTPS captures
   - Explain what SNI reveals and why
   - Describe the TLS handshake sequence observed

### Deliverables
- `wireshark_http.pcapng` — HTTP capture
- `wireshark_https.pcapng` — HTTPS capture
- `analysis.md` — Written analysis (300-500 words)

---

## 📝 Assignment 2: REST API Client (40 points)

### Objective
Implement a command-line REST API client that interacts with all four Richardson Maturity Model levels.

### Tasks

1. **Implement client functions** (20 points)
   Create a Python script `rest_client.py` that includes:
   - `level0_operation(action, **kwargs)` — Call Level 0 endpoint
   - `level2_list()`, `level2_get(id)`, `level2_create(data)`, `level2_update(id, data)`, `level2_delete(id)`
   - Proper error handling for all operations

2. **Comparison table** (10 points)
   - Execute the same operations at each level
   - Document the differences in: request format, response format, status codes
   - Create a markdown table summarising your findings

3. **Critical analysis** (10 points)
   - Which level would you choose for a new API? Why?
   - What are the trade-offs between simplicity and REST compliance?
   - How does HATEOAS benefit API discoverability?

### Deliverables
- `rest_client.py` — Your implementation
- `comparison_table.md` — Operations comparison
- `analysis.md` — Critical analysis (200-400 words)

### Evaluation Rubric

| Criterion | Points | Description |
|-----------|--------|-------------|
| Functionality | 10 | All operations work correctly |
| Error handling | 5 | Graceful handling of errors |
| Code quality | 5 | Clean, readable, documented |
| Comparison accuracy | 10 | Correct observations |
| Analysis depth | 10 | Thoughtful, justified conclusions |

---

## 📝 Assignment 3: DNS Configuration (30 points)

### Objective
Extend the lab DNS server with custom records and analyse DNS resolution.

### Tasks

1. **Add custom DNS records** (15 points)
   Modify the DNS server to include:
   - An A record for `student.lab.local` → your chosen IP
   - A CNAME record aliasing `www.student.lab.local` → `student.lab.local`
   - A TXT record for `student.lab.local` with your name

2. **Document the resolution process** (15 points)
   - Use `dig +trace` (or equivalent) to show DNS resolution path
   - Explain each step of the resolution
   - Capture DNS queries in Wireshark and annotate

### Deliverables
- `dns_config.py` or `zone_file.txt` — Your DNS configuration
- `resolution_trace.md` — Documented resolution process with screenshots
- `dns_capture.pcapng` — Wireshark capture of your queries

---

## ⚖️ Grading Summary

| Assignment | Points |
|------------|--------|
| HTTPS Traffic Analysis | 30 |
| REST API Client | 40 |
| DNS Configuration | 30 |
| **Total** | **100** |

---

## 🎯 Tips for Success

1. **Start early** — Docker issues are common, leave time for debugging
2. **Document as you go** — Take screenshots and notes during experiments
3. **Test thoroughly** — Verify your solutions work before submission
4. **Ask questions** — Use the course forum for clarifications
5. **Review misconceptions** — Check `docs/misconceptions.md` to avoid common errors

---

## 🔗 Useful Resources

- [Wireshark User Guide](https://www.wireshark.org/docs/wsug_html_chunked/)
- [curl Manual](https://curl.se/docs/manual.html)
- [dig Manual](https://linux.die.net/man/1/dig)
- [RFC 7231 — HTTP Semantics](https://datatracker.ietf.org/doc/html/rfc7231)

---

## 🤝 Pair Programming Option

Assignments 2 and 3 may be completed in pairs. If working in pairs:
- Both names must appear in the submission
- Include a brief statement of who contributed what
- Both students submit the same archive

---

*Computer Networks — Week 10 | ASE, CSIE Bucharest*
*Homework by ing. dr. Antonio Clim*
