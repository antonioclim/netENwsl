# 👥 Pair Programming Guide — Week 12
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> **Topic:** Email Protocols and Remote Procedure Call  
> **Session duration:** 75-100 minutes  
> **Pair exercises:** 3 structured activities

---

## Roles and Responsibilities

| Role | Responsibilities | Tools |
|------|-----------------|-------|
| **Driver** | Types commands, writes code, controls terminal | Terminal, VS Code |
| **Navigator** | Reviews output, checks documentation, suggests next steps | RFC docs, cheatsheet, browser |

**⚠️ SWAP roles every 10-15 minutes or at designated swap points!**

---

## Session Structure

### Phase 1: Setup (5 min)
- [ ] Both partners have WSL terminal open
- [ ] Lab environment running (`make start` completed)
- [ ] Portainer accessible at http://localhost:9000
- [ ] Decide who drives first (suggestion: alphabetical by surname)

### Phase 2: Paired Exercises (60-70 min)
- Complete exercises P1, P2 and P3 below
- Follow swap points strictly
- Navigator must stay engaged — no phones!

### Phase 3: Review and Reflect (10 min)
- [ ] Both partners can explain each protocol's key characteristics
- [ ] Discuss: "Which RPC style would you choose for a mobile app backend?"
- [ ] Complete the reflection questions together

---

## Exercise P1: SMTP Dialogue Exploration

**Objective:** UNDERSTAND the SMTP command-response protocol through manual interaction

**Estimated time:** 20 minutes

### Setup

💭 **PREDICTION (both partners):** Before starting, predict:
- What greeting will the server send when you connect?
- What response code indicates "ready for message body"?

### Driver Task (10 min)

1. Open terminal and connect to SMTP server:
   ```bash
   nc localhost 1025
   ```

2. Type these commands **exactly**, pressing Enter after each:
   ```
   EHLO student.local
   MAIL FROM:<driver@ase.ro>
   RCPT TO:<navigator@ase.ro>
   DATA
   Subject: Pair Programming Test
   
   This message was sent during pair programming.
   The driver typed it whilst the navigator verified.
   .
   QUIT
   ```

3. **DO NOT** proceed until Navigator confirms each response code.

### Navigator Task

- Keep `docs/commands_cheatsheet.md` open
- After each command, verify the response code:
  - 220 = greeting (on connect)
  - 250 = command OK
  - 354 = ready for data
  - 221 = closing
- Call out any unexpected responses immediately
- Note the session transcript for later review

### 🔄 SWAP POINT: After QUIT response received

### New Driver Task (10 min)

1. Verify the message was stored:
   ```bash
   ls -la docker/volumes/spool/
   cat docker/volumes/spool/*.eml | tail -20
   ```

2. Use the LIST command (non-standard, teaching only):
   ```bash
   nc localhost 1025
   EHLO checker.local
   LIST
   QUIT
   ```

### New Navigator Task

- Verify the `.eml` file contains correct headers (From, To, Subject)
- Check that LIST shows the stored message count
- Document any discrepancies

### Deliverable

Both partners sign off on:
- [ ] Successful SMTP dialogue completed
- [ ] Message stored in spool directory
- [ ] Both partners can explain each SMTP command's purpose

---

## Exercise P2: JSON-RPC Client Development

**Objective:** APPLY JSON-RPC protocol by building and testing client requests

**Estimated time:** 25 minutes

### Setup

💭 **PREDICTION (both partners):** Before starting, predict:
- What HTTP method does JSON-RPC use?
- What happens if you omit the `id` field from a request?

### Driver Task (12 min)

1. Test basic arithmetic using curl:
   ```bash
   # Addition
   curl -X POST http://localhost:6200 \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc": "2.0", "method": "add", "params": [10, 32], "id": 1}'
   ```

2. Test with named parameters:
   ```bash
   curl -X POST http://localhost:6200 \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc": "2.0", "method": "subtract", "params": {"a": 100, "b": 58}, "id": 2}'
   ```

3. Test error handling (division by zero):
   ```bash
   curl -X POST http://localhost:6200 \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc": "2.0", "method": "divide", "params": [42, 0], "id": 3}'
   ```

4. Test method not found:
   ```bash
   curl -X POST http://localhost:6200 \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc": "2.0", "method": "power", "params": [2, 8], "id": 4}'
   ```

### Navigator Task

- Verify each response matches expected format
- Check that `result` appears for success, `error` for failures
- Note the error codes: `-32601` (method not found), `-32000` (server error)
- Keep `docs/theory_summary.md` section on JSON-RPC open

### 🔄 SWAP POINT: After error handling tests

### New Driver Task (13 min)

1. Test batch requests:
   ```bash
   curl -X POST http://localhost:6200 \
     -H "Content-Type: application/json" \
     -d '[
       {"jsonrpc": "2.0", "method": "add", "params": [1, 2], "id": 1},
       {"jsonrpc": "2.0", "method": "multiply", "params": [3, 4], "id": 2},
       {"jsonrpc": "2.0", "method": "divide", "params": [10, 0], "id": 3}
     ]'
   ```

2. Test notification (no id = no response):
   ```bash
   curl -X POST http://localhost:6200 \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc": "2.0", "method": "add", "params": [1, 1]}'
   # Note: Server returns HTTP 204 No Content
   ```

3. Run the Python client:
   ```bash
   cd /mnt/d/NETWORKING/WEEK12/12enWSL
   python3 src/apps/rpc/jsonrpc/jsonrpc_client.py
   ```

### New Navigator Task

- For batch: verify response is an array with 3 elements
- Confirm the third response contains an error object
- For notification: verify no response body returned
- Compare curl output with Python client output

### Deliverable

Both partners sign off on:
- [ ] Successful single requests (add, subtract, multiply, divide)
- [ ] Error responses correctly formatted
- [ ] Batch request returns array of responses
- [ ] Notification returns no body

---

## Exercise P3: RPC Protocol Comparison

**Objective:** ANALYSE differences between JSON-RPC, XML-RPC and gRPC through benchmarking

**Estimated time:** 20 minutes

### Setup

💭 **PREDICTION (both partners):** Before starting, predict:
- Which protocol will have the smallest payload size?
- Which protocol will have the lowest latency?

### Driver Task (10 min)

1. Test XML-RPC and compare payload:
   ```bash
   # XML-RPC request
   curl -X POST http://localhost:6201 \
     -H "Content-Type: text/xml" \
     -d '<?xml version="1.0"?>
   <methodCall>
     <methodName>add</methodName>
     <params>
       <param><value><double>10</double></value></param>
       <param><value><double>32</double></value></param>
     </params>
   </methodCall>'
   ```

2. Compare request sizes:
   ```bash
   # JSON-RPC payload size
   echo '{"jsonrpc": "2.0", "method": "add", "params": [10, 32], "id": 1}' | wc -c
   
   # XML-RPC payload size (approximate)
   echo '<?xml version="1.0"?><methodCall><methodName>add</methodName><params><param><value><double>10</double></value></param><param><value><double>32</double></value></param></params></methodCall>' | wc -c
   ```

3. Run the benchmark script:
   ```bash
   python3 src/apps/rpc/benchmark_rpc.py --iterations 100
   ```

### Navigator Task

- Record payload sizes for comparison table
- Note latency results from benchmark
- Prepare comparison notes for discussion

### 🔄 SWAP POINT: After benchmark completes

### New Driver Task (10 min)

1. Test gRPC (if grpcio installed):
   ```bash
   # Start gRPC server (if not running)
   python3 src/apps/rpc/grpc/grpc_server.py &
   
   # Run gRPC client
   python3 src/apps/rpc/grpc/grpc_client.py
   ```

2. Capture traffic for analysis (optional):
   ```bash
   # In Wireshark, filter: tcp.port in {6200, 6201, 6251}
   # Compare payload sizes visually
   ```

3. Complete the comparison table together:

| Aspect | JSON-RPC | XML-RPC | gRPC |
|--------|----------|---------|------|
| Request size (bytes) | ___ | ___ | ___ |
| Response size (bytes) | ___ | ___ | ___ |
| Avg latency (ms) | ___ | ___ | ___ |
| Human readable? | Yes | Yes | No |

### New Navigator Task

- Fill in comparison table with actual measurements
- Note any unexpected results
- Prepare explanation for why gRPC is faster despite HTTP/2 overhead

### Deliverable

Both partners sign off on:
- [ ] All three protocols tested successfully
- [ ] Comparison table completed with real data
- [ ] Both partners can explain trade-offs between protocols

---

## Communication Phrases

### Navigator to Driver

| Situation | Phrase |
|-----------|--------|
| Checking understanding | "What do you expect to happen next?" |
| Spotting an error | "Hold on — I think there's a typo in line X" |
| Suggesting improvement | "What if we tried using named parameters?" |
| Needing clarification | "Can you explain why you chose that approach?" |
| Referencing docs | "According to the cheatsheet, the response should be..." |

### Driver to Navigator

| Situation | Phrase |
|-----------|--------|
| Before executing | "I'm about to run this — what should we expect?" |
| When stuck | "I'm not sure what's wrong. Can you check the docs?" |
| Confirming approach | "Does this look right to you?" |
| Requesting verification | "Can you verify the response code?" |
| Explaining reasoning | "I'm doing this because..." |

---

## Troubleshooting Together

When stuck, follow this sequence:

1. **Driver:** Explain what you expected vs what happened
2. **Navigator:** Read the error message aloud, word by word
3. **Both:** Check the troubleshooting guide (`docs/troubleshooting.md`)
4. **Navigator:** Search the commands cheatsheet for correct syntax
5. **If still stuck after 5 min:** Raise hand for instructor help

**Common issues this week:**
- Port not listening → Check `docker ps` for running containers
- Connection refused → Verify server started with `make smtp-server`
- JSON parse error → Check for missing commas or quotes in payload
- gRPC import error → Run `pip install grpcio grpcio-tools --break-system-packages`

---

## Reflection Questions

Complete together after all exercises:

1. **Protocol choice:** If building a public API for web browsers, which RPC style would you choose and why?

2. **Trade-offs:** What are the advantages of gRPC's binary encoding? What are the disadvantages?

3. **SMTP insight:** Why does SMTP use a separate response code (354) for the DATA command instead of 250?

4. **Collaboration:** What did your partner help you understand that you might have missed alone?

---

## Attendance and Completion

Both partners must sign to confirm completion:

| Partner | Name | Signature | Exercises Completed |
|---------|------|-----------|---------------------|
| Driver (initial) | _____________ | _______ | P1 ☐ P2 ☐ P3 ☐ |
| Navigator (initial) | _____________ | _______ | P1 ☐ P2 ☐ P3 ☐ |

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
