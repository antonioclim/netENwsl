# 👥 Pair Programming Guide — Week 10
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> HTTP/HTTPS, REST Architecture and Network Services

---

## Roles

| Role | Responsibilities | Duration |
|------|-----------------|----------|
| **Driver** | Types code, controls keyboard/mouse, executes commands | 10-15 min |
| **Navigator** | Reviews code, suggests improvements, checks documentation, thinks ahead | 10-15 min |

**SWAP roles every 10-15 minutes!** Set a timer.

---

## Session Structure

### Phase 1: Setup (5 min)
- [ ] Both partners can access the WSL environment
- [ ] Docker is running (`docker ps` works)
- [ ] Lab containers are started (`python3 scripts/start_lab.py`)
- [ ] Decide who drives first
- [ ] Review the exercise objectives together

### Phase 2: Implementation (40-50 min)
- Driver types, Navigator reviews
- Navigator should:
  - Check for typos and syntax errors
  - Suggest improvements or alternatives
  - Look up documentation when stuck
  - Ask "what if..." questions
  - Watch for edge cases

### Phase 3: Review (10 min)
- [ ] Both partners can explain every line of code
- [ ] Test edge cases together
- [ ] Discuss alternative approaches
- [ ] Document any issues encountered

---

## This Week's Pair Exercises

### Exercise P1: HTTPS Server Exploration
**Objective:** Understand TLS certificate generation and HTTPS server setup
**Estimated time:** 25 min

#### ✅ Success Criteria

Before moving on, verify:

| Criterion | Check |
|-----------|-------|
| Certificate file exists in `output/tls/` | ☐ |
| HTTPS server responds on port 8443 | ☐ |
| `curl -k` returns valid JSON response | ☐ |
| POST request creates resource with 201 status | ☐ |
| Both partners can explain why `-k` is needed | ☐ |

**Driver tasks:**
1. Generate a self-signed certificate using the exercise script
2. Start the HTTPS server
3. Make requests using `curl -k` (insecure mode)

**Navigator tasks:**
1. Explain why `-k` flag is needed for self-signed certs
2. Identify the certificate fields (CN, O, OU)
3. Research: What would change for a production certificate?

**Swap point:** After successfully making the first HTTPS request

**Prediction prompts:**
- 💭 "What error will curl show WITHOUT the -k flag?"
- 💭 "What HTTP status code will a POST to /api/resources return?"

```bash
# Commands to try
cd /mnt/d/NETWORKING/WEEK10/10enWSL
python3 src/exercises/ex_10_01_tls_rest_crud.py generate-cert
python3 src/exercises/ex_10_01_tls_rest_crud.py serve &
curl -k https://127.0.0.1:8443/
curl -k -X POST https://127.0.0.1:8443/api/resources \
  -H "Content-Type: application/json" \
  -d '{"name": "test", "value": 42}'
```

#### 🔍 Post-Exercise Reflection (P1)

Discuss with your partner before moving on:
1. What is the difference between a self-signed certificate and a CA-signed one?
2. Why do browsers show a warning for self-signed certificates?
3. In what scenarios would you use self-signed certs in production?

---

### Exercise P2: REST Maturity Level Comparison
**Objective:** Compare API designs across Richardson Maturity Model levels
**Estimated time:** 30 min

#### ✅ Success Criteria

Before moving on, verify:

| Criterion | Check |
|-----------|-------|
| Successfully queried all 4 levels (0, 1, 2, 3) | ☐ |
| Comparison table is completely filled | ☐ |
| Both partners can explain Level 0 vs Level 2 difference | ☐ |
| Both partners can explain what `_links` in Level 3 is for | ☐ |
| Created at least one user via POST at Level 2 | ☐ |

**Driver tasks:**
1. Start the REST levels server
2. Perform the same operation (list users, create user, update user) at each level
3. Document the differences in request format

**Navigator tasks:**
1. Identify which HTTP verbs are used at each level
2. Note the URI patterns at each level
3. Explain why Level 3 includes `_links` in responses

**Swap point:** After completing Level 1 requests, swap for Level 2-3

**Prediction prompts:**
- 💭 "How will creating a user differ between Level 0 and Level 2?"
- 💭 "What extra information will Level 3 responses contain?"

```bash
# Start the server
python3 src/exercises/ex_10_02_richardson_maturity.py serve &

# Level 0 - RPC style
curl -X POST http://127.0.0.1:5000/level0/service \
  -H "Content-Type: application/json" \
  -d '{"action": "list_users"}'

# Level 2 - Proper verbs
curl http://127.0.0.1:5000/level2/users
curl -X POST http://127.0.0.1:5000/level2/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com"}'

# Level 3 - With HATEOAS links
curl http://127.0.0.1:5000/level3/users
```

**Comparison table to complete together:**

| Operation | Level 0 | Level 1 | Level 2 | Level 3 |
|-----------|---------|---------|---------|---------|
| List users | POST /service action=list | ? | ? | ? |
| Create user | ? | ? | ? | ? |
| Update user | ? | ? | ? | ? |
| Delete user | ? | ? | ? | ? |

#### 🔍 Post-Exercise Reflection (P2)

Discuss with your partner before moving on:
1. Which REST level do most APIs you've used implement?
2. What are the benefits of Level 3 (HATEOAS)? What are the downsides?
3. Why might a team choose Level 2 over Level 3?

---

### Exercise P3: DNS Query Analysis
**Objective:** Understand DNS query/response structure using dig
**Estimated time:** 20 min

#### ✅ Success Criteria

Before moving on, verify:

| Criterion | Check |
|-----------|-------|
| Successfully queried at least 3 different domains | ☐ |
| Can identify ANSWER section in dig output | ☐ |
| Compared UDP vs TCP query (output difference noted) | ☐ |
| Observed NXDOMAIN response for non-existent domain | ☐ |
| Both partners can explain what TTL means | ☐ |

**Driver tasks:**
1. Query the lab DNS server for different record types
2. Compare UDP vs TCP queries
3. Query for non-existent domains

**Navigator tasks:**
1. Identify query and response sections in dig output
2. Explain the TTL values
3. Research: What does the +trace option show?

**Swap point:** After querying three different domains

**Prediction prompts:**
- 💭 "What IP will `web.lab.local` resolve to?"
- 💭 "What happens when we query a domain that doesn't exist?"

```bash
# Basic queries to the lab DNS server
dig @127.0.0.1 -p 5353 web.lab.local
dig @127.0.0.1 -p 5353 ssh.lab.local
dig @127.0.0.1 -p 5353 myservice.lab.local

# Query type variations
dig @127.0.0.1 -p 5353 web.lab.local A
dig @127.0.0.1 -p 5353 web.lab.local +short

# TCP vs UDP
dig @127.0.0.1 -p 5353 web.lab.local +tcp
dig @127.0.0.1 -p 5353 web.lab.local +notcp

# Non-existent domain
dig @127.0.0.1 -p 5353 nonexistent.lab.local
```

#### 🔍 Post-Exercise Reflection (P3)

Discuss with your partner before moving on:
1. Why does DNS use UDP by default instead of TCP?
2. When would DNS switch to TCP?
3. What happens if a DNS cache has stale (expired) data?

---

### Exercise P4: SSH and FTP Service Testing
**Objective:** Test SSH and FTP services from the debug container
**Estimated time:** 20 min

#### ✅ Success Criteria

Before moving on, verify:

| Criterion | Check |
|-----------|-------|
| Successfully connected to SSH server | ☐ |
| Executed at least one command via SSH | ☐ |
| Successfully connected to FTP server | ☐ |
| Listed files on FTP server | ☐ |
| Both partners can explain control vs data channel | ☐ |
| (Optional) Observed traffic in Wireshark | ☐ |

**Driver tasks:**
1. Connect to SSH server and execute commands
2. Connect to FTP server and list files
3. Transfer a test file via FTP

**Navigator tasks:**
1. Monitor connections in Wireshark
2. Identify the FTP control vs data channels
3. Compare encrypted (SSH) vs unencrypted (FTP) traffic

**Swap point:** After successful SSH connection, swap for FTP testing

**Prediction prompts:**
- 💭 "How many TCP connections will FTP establish?"
- 💭 "Can we see FTP credentials in Wireshark? What about SSH?"

```bash
# SSH from host
ssh -p 2222 labuser@localhost
# Password: labpass

# Or use the debug container
docker exec -it week10_debug bash
ssh labuser@ssh-server
# Password: labpass

# FTP connection
docker exec -it week10_debug bash
ftp ftp-server 2121
# User: labftp, Password: labftp
ftp> ls
ftp> pwd
ftp> quit
```

#### 🔍 Post-Exercise Reflection (P4)

Discuss with your partner before moving on:
1. Why is SSH preferred over Telnet for remote access?
2. What are the security implications of FTP's plaintext authentication?
3. What modern alternatives to FTP exist (SFTP, FTPS, SCP)?

---

## Communication Phrases

### Navigator to Driver

- "What's your plan for this part?"
- "Could you explain that line?"
- "I think there might be an issue with..."
- "The documentation says..."
- "What do you expect to happen when...?"
- "Let me look up the syntax for that..."
- "Should we test that edge case?"

### Driver to Navigator

- "I'm going to try..."
- "Does this look right?"
- "I'm stuck on..."
- "Can you check what [command/function] does?"
- "Before I run this, what do you predict will happen?"
- "I'm not sure about this approach, what do you think?"

---

## Troubleshooting Together

When stuck:

1. **Driver:** Explain your current understanding out loud
2. **Navigator:** Ask clarifying questions
3. **Both:** Re-read the error message carefully
4. **Navigator:** Search documentation or troubleshooting guide
5. **If still stuck after 5 min:** Ask the instructor

**Common issues this week:**

| Problem | Quick fix |
|---------|-----------|
| "Connection refused" | Check if service is running: `docker ps` |
| Certificate errors | Use `curl -k` for self-signed certs |
| DNS timeout | Verify DNS container: `docker logs week10_dns` |
| FTP passive mode fails | Check port range 30000-30009 is mapped |

---

## 📝 End-of-Session Reflection

### Partner Discussion (5 minutes)

Discuss with your partner:

1. **Challenge:** What was the most challenging part of today's exercises?
2. **Support:** What did your partner do that helped you understand better?
3. **Improvement:** What would you do differently in the next pair session?
4. **Misconception:** Which misconception from the misconceptions.md did you encounter?

### Individual Reflection

Rate your understanding (1-5) on each topic:

| Topic | Before | After |
|-------|--------|-------|
| HTTPS/TLS certificates | ☐ 1 ☐ 2 ☐ 3 ☐ 4 ☐ 5 | ☐ 1 ☐ 2 ☐ 3 ☐ 4 ☐ 5 |
| REST maturity levels | ☐ 1 ☐ 2 ☐ 3 ☐ 4 ☐ 5 | ☐ 1 ☐ 2 ☐ 3 ☐ 4 ☐ 5 |
| DNS query structure | ☐ 1 ☐ 2 ☐ 3 ☐ 4 ☐ 5 | ☐ 1 ☐ 2 ☐ 3 ☐ 4 ☐ 5 |
| SSH vs FTP security | ☐ 1 ☐ 2 ☐ 3 ☐ 4 ☐ 5 | ☐ 1 ☐ 2 ☐ 3 ☐ 4 ☐ 5 |

### Action Items for Next Session

- [ ] Review any topic where confidence < 3
- [ ] Read the misconceptions.md for areas of confusion
- [ ] Practice with the exercises independently
- [ ] Prepare questions for the instructor

---

## Quick Reference: All Exercises

| Exercise | Time | Key Skill | Success Metric |
|----------|------|-----------|----------------|
| P1: HTTPS | 25 min | TLS certificates | Successful curl -k request |
| P2: REST Levels | 30 min | Richardson Model | Completed comparison table |
| P3: DNS | 20 min | dig queries | Identify all dig sections |
| P4: SSH/FTP | 20 min | Remote protocols | Both connections successful |

**Total estimated time:** 95 minutes (including reflections)

---

*Computer Networks — Week 10 | ASE, CSIE Bucharest*
*Pair programming guide by ing. dr. Antonio Clim*
