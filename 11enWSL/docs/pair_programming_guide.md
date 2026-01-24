# 👥 Pair Programming Guide — Week 11
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Roles

| Role | Responsibilities | Focus |
|------|-----------------|-------|
| **Driver** | Types code, controls keyboard and mouse | Implementation details, syntax |
| **Navigator** | Reviews, suggests, checks documentation | Strategy, correctness, edge cases |

**⚠️ SWAP roles every 10-15 minutes!**

The Navigator is not passive — actively review every line, ask questions and suggest improvements.

---

## Session Structure

### Phase 1: Setup (5 minutes)

- [ ] Both partners have access to the WSL terminal
- [ ] Docker is running (`docker ps` shows Portainer)
- [ ] Both can see the shared screen or sit side-by-side
- [ ] Decide who drives first (flip a coin, or whoever arrived second starts)
- [ ] Review the exercise objectives together

### Phase 2: Implementation (50-60 minutes)

Follow the Driver/Navigator pattern:
- Driver types, Navigator reviews in real-time
- Navigator should:
  - Check for typos before Enter is pressed
  - Suggest improvements ("What if we add error handling here?")
  - Look up documentation when stuck
  - Ask "What if..." questions about edge cases
  - Keep track of time for role swaps

### Phase 3: Review (10 minutes)

- [ ] Both partners can explain every line of code
- [ ] Test edge cases together (What happens if a backend fails?)
- [ ] Discuss alternative approaches
- [ ] Document any discoveries or surprises

---

## This Week's Pair Exercises

### Exercise P1: Backend Deployment and Testing

**Objective:** Deploy three HTTP backends and verify load balancing

**Estimated time:** 15 minutes

**Setup:**
- Driver has terminal open
- Navigator has README.md and troubleshooting.md visible

**Driver Task (first 7 minutes):**
```bash
# Start Backend 1
python3 src/exercises/ex_11_01_backend.py --id 1 --port 8081 -v

# (In second terminal) Start Backend 2
python3 src/exercises/ex_11_01_backend.py --id 2 --port 8082 -v

# (In third terminal) Start Backend 3
python3 src/exercises/ex_11_01_backend.py --id 3 --port 8083 -v
```

**Navigator Task:**
- Verify each backend starts successfully (look for "Listening on" message)
- Check ports are not already in use
- Note the process ID for each backend

**🔄 SWAP after all three backends are running**

**Driver Task (next 8 minutes):**
```bash
# Test individual backends
curl http://localhost:8081/
curl http://localhost:8082/
curl http://localhost:8083/

# Start load balancer
python3 src/exercises/ex_11_02_loadbalancer.py \
    --backends localhost:8081,localhost:8082,localhost:8083 \
    --listen 0.0.0.0:8080 --algo rr

# Test distribution
for i in {1..9}; do curl -s http://localhost:8080/; done
```

**Navigator Task:**
- Verify each backend returns different ID
- Count distribution: should be roughly 3-3-3
- Watch for any error messages

---

### Exercise P2: Failover Testing

**Objective:** Observe load balancer behaviour when a backend fails

**Estimated time:** 15 minutes

**💭 PREDICTION (both partners):** What will happen when we stop Backend 2?

**Driver Task (first 7 minutes):**
```bash
# Establish baseline - send 6 requests
for i in {1..6}; do curl -s http://localhost:8080/; done

# Stop Backend 2 (Ctrl+C in its terminal, or:)
# Find PID and kill
ps aux | grep "ex_11_01_backend.*8082"
kill <PID>

# Send more requests
for i in {1..6}; do curl -s http://localhost:8080/; done
```

**Navigator Task:**
- Record which backends received traffic before failure
- Note any 502 errors (first request to dead backend)
- Count new distribution (should be alternating between 1 and 3)

**🔄 SWAP**

**Driver Task (next 8 minutes):**
```bash
# Restart Backend 2
python3 src/exercises/ex_11_01_backend.py --id 2 --port 8082 -v

# Wait for fail_timeout to expire (default 10s)
sleep 15

# Test recovery
for i in {1..9}; do curl -s http://localhost:8080/; done
```

**Navigator Task:**
- Verify Backend 2 rejoins the rotation
- Check distribution returns to 3-3-3
- Document the recovery time observed

---

### Exercise P3: DNS Client Analysis

**Objective:** Understand DNS packet structure through the educational client

**Estimated time:** 20 minutes

**Driver Task (first 10 minutes):**
```bash
# Query A record with verbose output
python3 src/exercises/ex_11_03_dns_client.py --query google.com --type A --verbose

# Query MX records
python3 src/exercises/ex_11_03_dns_client.py --query google.com --type MX

# Query non-existent domain
python3 src/exercises/ex_11_03_dns_client.py --query thisdomaindoesnotexist12345.com --type A
```

**Navigator Task:**
- In verbose mode, identify the Header, Question and Answer sections
- Note the Transaction ID (should be random)
- Observe TTL values in responses
- Verify NXDOMAIN response for non-existent domain

**🔄 SWAP**

**Driver Task (next 10 minutes):**
```bash
# Compare with system dig
dig google.com A +short
dig google.com MX +short

# Try different DNS server
python3 src/exercises/ex_11_03_dns_client.py --query ase.ro --type A --server 1.1.1.1
python3 src/exercises/ex_11_03_dns_client.py --query ase.ro --type A --server 8.8.8.8
```

**Navigator Task:**
- Compare output format between Python client and dig
- Note any differences in results from different DNS servers
- Record TTL values and discuss caching implications

---

### Exercise P4: Nginx Docker Deployment

**Objective:** Deploy production-style load balancer using Docker Compose

**Estimated time:** 20 minutes

**Driver Task (first 10 minutes):**
```bash
# Stop any running Python components first
# (Ctrl+C or kill processes)

# Start Nginx stack
cd /mnt/d/NETWORKING/WEEK11/11enWSL
docker compose -f docker/docker-compose.yml up -d

# Verify containers
docker compose -f docker/docker-compose.yml ps

# Test load balancing
for i in {1..6}; do curl -s http://localhost:8080/; done
```

**Navigator Task:**
- Check all 4 containers are running (nginx + 3 backends)
- Verify health check status in Portainer (http://localhost:9000)
- Note container names for later reference

**🔄 SWAP**

**Driver Task (next 10 minutes):**
```bash
# Check Nginx configuration
docker exec s11_nginx_lb cat /etc/nginx/nginx.conf

# View access logs
docker compose logs -f nginx

# Simulate backend failure
docker stop s11_backend_2

# Test behaviour
for i in {1..6}; do curl -s http://localhost:8080/; done

# Restore backend
docker start s11_backend_2
```

**Navigator Task:**
- Identify upstream configuration in nginx.conf
- Watch logs for 502 errors when backend fails
- Compare behaviour with Python load balancer

---

## Communication Phrases

### Navigator to Driver

**Strategic guidance:**
- "What's your plan for this part?"
- "Before we run that, let's think about what we expect to happen."
- "Could you explain your reasoning for that approach?"

**Spotting issues:**
- "I think there might be an issue with..."
- "Should that be 8081 or 8082?"
- "The documentation says it should be..."

**Suggestions:**
- "What if we tried..."
- "Could we add error handling for..."
- "Let's check the logs before continuing."

### Driver to Navigator

**Explaining intent:**
- "I'm going to start by..."
- "My plan is to first X, then Y, then Z."
- "I think this will work because..."

**Seeking input:**
- "Does this look right to you?"
- "I'm stuck on... can you check the docs?"
- "What do you think about this approach?"

**Handoff:**
- "I've finished this section, want to swap?"
- "This is a good stopping point for a swap."

---

## Troubleshooting Together

When stuck, follow this protocol:

1. **Driver:** Explain your current understanding aloud
2. **Navigator:** Ask clarifying questions (not accusations)
3. **Both:** Re-read the error message carefully, word by word
4. **Navigator:** Search documentation or troubleshooting.md
5. **Driver:** Try the suggested fix
6. **If stuck > 5 minutes:** Call instructor for guidance

### Common Issues This Week

| Symptom | First Check | Solution |
|---------|-------------|----------|
| Port already in use | `netstat -tlnp \| grep PORT` | Kill existing process |
| Backend not responding | Is terminal still running? | Restart backend script |
| 502 Bad Gateway | `docker ps` - backends running? | Restart Docker stack |
| DNS timeout | Internet connectivity | Try different server (8.8.8.8) |
| Permission denied | Running in correct directory? | `cd` to 11enWSL folder |

---

## Pair Programming Best Practices

### Do ✅

- Communicate constantly — narrate your thinking
- Ask questions — "Why?" is always valid
- Take breaks together — both step away
- Celebrate small wins — "That worked!"
- Admit confusion — "I don't understand this"

### Don't ❌

- Grab the keyboard from your partner
- Stay silent while navigating
- Check phone/email during pairing
- Say "You're wrong" — say "I see it differently"
- Skip role swaps — both roles are educational

---

## Reflection Questions (End of Session)

Discuss with your partner:

1. What was the most surprising thing you learned today?
2. Which role (Driver/Navigator) did you find more challenging?
3. What would you do differently next time?
4. What concept still feels unclear?

---

*NETWORKING class - ASE, Informatics | Computer Networks Laboratory*
*Week 11: Application Protocols — FTP, DNS, SSH and Load Balancing*
