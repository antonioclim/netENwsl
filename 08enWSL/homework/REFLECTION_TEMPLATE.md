# Reflection Questions — Week 8: Transport Layer & HTTP

> Computer Networks — ASE, CSIE

---

## IMPORTANT: This Document is MANDATORY for Full Credit

These reflection questions verify YOUR understanding beyond code.
They are designed to detect AI-generated or copied submissions.

**Your answers MUST reference:**
- YOUR unique port from `artifacts/student_context.json`
- YOUR unique weights from `artifacts/student_context.json`
- YOUR PCAP files with specific packet numbers and timestamps
- YOUR implementation decisions with line numbers

**Grading:** 40 points (added to your code grade)

---

## Before You Start

1. **Generate your context** (if not done already):
   ```bash
   make init ID=your_student_id
   ```

2. **Open your context file** and note your unique values:
   ```bash
   cat artifacts/student_context.json
   ```

3. **Have your PCAP files ready** in Wireshark for reference

---

## Section A: Your Unique Implementation (15 points)

### Question A1: Port Binding (5 points)

Your HTTP server runs on port **[WRITE YOUR UNIQUE PORT HERE]** from your context.

**Answer these questions:**

1. What error would you see if another process was already using this port?
   
   ```
   YOUR ANSWER:
   [Write the exact error message you would expect]
   ```

2. How did you handle this error in your code? (cite line numbers from ex_8_01_http_server.py)
   
   ```
   YOUR ANSWER:
   Line(s): ___
   My approach: [Explain in 2-3 sentences]
   ```

3. What socket option prevents "Address already in use" after restart?
   
   ```
   YOUR ANSWER:
   Option name: ___
   Why it helps: [1 sentence]
   ```

---

### Question A2: Load Balancer Weights (5 points)

Your load balancer uses these weights from your context:
- backend1: **[WRITE YOUR WEIGHT]**
- backend2: **[WRITE YOUR WEIGHT]**  
- backend3: **[WRITE YOUR WEIGHT]**

**Calculate and verify:**

1. For 18 requests how many should go to each backend?
   
   ```
   YOUR CALCULATION:
   Total weight = ___ + ___ + ___ = ___
   
   backend1: 18 × (___ / ___) = ___ requests
   backend2: 18 × (___ / ___) = ___ requests
   backend3: 18 × (___ / ___) = ___ requests
   ```

2. Look at your `{student_id}_loadbalance.pcap` file. List the actual distribution:
   
   ```
   YOUR PCAP EVIDENCE:
   backend1 received packets: #___, #___, #___, ... (list frame numbers)
   backend2 received packets: #___, #___, #___, ...
   backend3 received packets: #___, #___, #___, ...
   
   Actual count: backend1=___, backend2=___, backend3=___
   ```

3. Does your PCAP match your calculation? Explain any discrepancy:
   
   ```
   YOUR ANSWER:
   [If they match: explain why weighted round-robin produces this pattern]
   [If they differ: explain what caused the difference]
   ```

---

### Question A3: Secret Header (5 points)

Your server must return the header: **[WRITE YOUR SECRET HEADER VALUE]**

1. In which function did you add this header? (cite line number)
   
   ```
   YOUR ANSWER:
   Function: ___
   Line: ___
   ```

2. Open your `{student_id}_http.pcap` in Wireshark. Find an HTTP response containing your header.
   
   ```
   YOUR PCAP EVIDENCE:
   Frame number: #___
   Full header line as shown in Wireshark: ___
   ```

3. Why might a reverse proxy add custom headers to responses?
   
   ```
   YOUR ANSWER (2-3 sentences):
   ```

---

## Section B: Debugging Scenarios (15 points)

### Question B1: The Mysterious 502 (5 points)

You start your load balancer but nginx returns `502 Bad Gateway`.
The logs show:

```
connect() failed (111: Connection refused) while connecting to upstream
```

**Answer:**

1. What does error code 111 mean at the Linux kernel level?
   
   ```
   YOUR ANSWER:
   Error 111 means: ___
   ```

2. List THREE possible causes for this error in the context of Week 8:
   
   ```
   YOUR ANSWER:
   a) ___
   b) ___
   c) ___
   ```

3. What is the FIRST diagnostic command you would run? Why?
   
   ```
   YOUR ANSWER:
   Command: ___
   Because: ___
   ```

4. You run `docker exec week8-nginx-proxy curl http://backend1:8080/health` and get "Connection refused". What does this tell you that `curl http://localhost:8080/health` from your host machine would NOT tell you?
   
   ```
   YOUR ANSWER:
   This tells me: ___
   The difference is important because: ___
   ```

---

### Question B2: PCAP Deep Analysis (5 points)

Open YOUR `{student_id}_handshake.pcap` in Wireshark.

**Find and report these EXACT values:**

1. Timestamp of the FIRST SYN packet:
   
   ```
   YOUR ANSWER: ___
   (Format: YYYY-MM-DD HH:MM:SS.microseconds)
   ```

2. TCP sequence number in the SYN-ACK packet:
   
   ```
   YOUR ANSWER: ___
   (This is the server's Initial Sequence Number)
   ```

3. The acknowledgment number in the third packet (ACK):
   
   ```
   YOUR ANSWER: ___
   (This should be SYN-ACK seq + 1)
   ```

4. Time delta between SYN and final ACK (connection establishment time):
   
   ```
   YOUR ANSWER: ___ milliseconds
   ```

---

### Question B3: HTTP Response Analysis (5 points)

Open YOUR `{student_id}_http.pcap` in Wireshark.

Find an HTTP request-response pair and report:

1. HTTP Request details:
   
   ```
   Frame number: #___
   Method: ___
   Path: ___
   Host header value: ___
   ```

2. HTTP Response details:
   
   ```
   Frame number: #___
   Status code: ___
   Content-Length: ___
   Content-Type: ___
   ```

3. Time between request and response:
   
   ```
   Request timestamp: ___
   Response timestamp: ___
   Latency: ___ ms
   ```

---

## Section C: Design Decisions (10 points)

### Question C1: Security Trade-offs (5 points)

In `is_safe_path()` you had to decide what to return for directory traversal attempts.

**Your implementation returns:** (circle one)
- [ ] 403 Forbidden
- [ ] 404 Not Found

**Explain your choice (minimum 100 words):**

Consider:
- What information does each status code reveal to an attacker?
- How do professional web servers (nginx, Apache) handle this?
- What does OWASP recommend?
- Is there a "right" answer?

```
YOUR ANSWER:
[Write here — must be YOUR reasoning not a generic explanation]
```

---

### Question C2: Stateful vs Stateless (5 points)

Your round-robin load balancer maintains state (which backend is "next").

1. Where in your code is this state stored? (cite variable name and line)
   
   ```
   YOUR ANSWER:
   Variable: ___
   Line: ___
   ```

2. What happens to this state if your load balancer process crashes and restarts?
   
   ```
   YOUR ANSWER:
   [2-3 sentences]
   ```

3. In production how would you make this state survive restarts? Name ONE approach.
   
   ```
   YOUR ANSWER:
   Approach: ___
   Brief explanation: ___
   ```

---

## Submission Checklist

Before submitting verify:

```
[ ] My unique port is written in A1: _____
[ ] My weights are written in A2: _____, _____, _____
[ ] My secret header is written in A3: _____
[ ] I cited specific line numbers from MY code
[ ] I cited specific frame numbers from MY PCAP files
[ ] I cited specific timestamps from MY captures
[ ] My explanations are in MY words not generic
[ ] Section C answers are at least 100 words each
```

---

## Grading Rubric

| Criterion | Points | What We Look For |
|-----------|--------|------------------|
| **Specificity** | 10 | References YOUR unique values, YOUR code lines, YOUR PCAP frames |
| **Technical Accuracy** | 10 | Correct understanding of TCP, HTTP and load balancing |
| **Evidence of Testing** | 10 | Real packet numbers, real timestamps and real calculations |
| **Depth of Analysis** | 10 | Goes beyond surface explanations, shows understanding |
| **Total** | **40** | |

---

## Academic Integrity Notice

These reflection questions verify YOUR personal understanding.

**AI-generated answers are detectable through:**
- Lack of YOUR specific port/weight/header values
- Generic frame numbers (real captures have specific numbers like #47, #123)
- Missing or fake timestamps
- Explanations that do not match YOUR code structure
- Perfect grammar with no personal voice

**Consequence:** Submitting AI-generated reflections is treated as plagiarism
and will result in zero marks for the entire homework assignment.

**If you are struggling:** Ask the instructor or TA for help. We want you to
learn and that is hard to do if you outsource your thinking.

---

*Computer Networks — ASE, CSIE*

*"The goal is not to finish the homework. The goal is to understand networks."*
