# 👥 Pair Programming Guide — Week 5
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> IP Addressing, Subnetting and VLSM

---

## Roles and Responsibilities

| Role | Responsibilities | Focus |
|------|-----------------|-------|
| **Driver** | Types commands, controls keyboard | Execution, syntax accuracy |
| **Navigator** | Reviews output, checks documentation, suggests next steps | Strategy, error detection |

**SWAP roles every 10-15 minutes** or after completing each exercise phase.

---

## Session Structure

### Phase 1: Setup (5 minutes)

- [ ] Both partners have Ubuntu terminal open
- [ ] Docker is running (`sudo service docker start`)
- [ ] Lab containers are up (`python3 scripts/start_lab.py --status`)
- [ ] Decide who drives first
- [ ] Review exercise objectives together

### Phase 2: Implementation (40-50 minutes)

Work through exercises with regular role swaps:
- Driver types commands and code
- Navigator watches for typos and logical errors
- Navigator keeps documentation open for reference
- Both discuss predictions before running commands

### Phase 3: Review (10 minutes)

- [ ] Both partners can explain every calculation
- [ ] Verify results match expected outputs
- [ ] Discuss alternative approaches
- [ ] Document any questions for instructor

---

## This Week's Pair Exercises

### Exercise P1: CIDR Analysis Challenge (15 minutes)

**Objective:** Analyse three different CIDR addresses and verify understanding.

**Setup:**
```bash
docker exec -it week5_python bash
cd /app/src/exercises
```

**Driver task (7 minutes):**
```bash
# Analyse these three addresses
python ex_5_01_cidr_flsm.py analyse 10.45.128.200/19 --verbose
python ex_5_01_cidr_flsm.py analyse 172.16.95.1/22 --verbose
python ex_5_01_cidr_flsm.py analyse 192.168.1.100/28 --verbose
```

**Navigator task:**
- Before each command, predict: network address, broadcast, usable hosts
- After output, verify predictions were correct
- Note any surprises or misconceptions

**SWAP at 7 minutes**

**New Driver task:**
- Run `binary` command for each address
- Explain the network/host bit boundary to Navigator

**Discussion points:**
1. Which address has the most usable hosts?
2. Which network boundary was hardest to predict?
3. What pattern do you see in the binary output?

---

### Exercise P2: Corporate VLSM Design (20 minutes)

**Objective:** Design an addressing scheme for a fictional company using VLSM.

**Scenario:**
TechStart SRL needs IP addresses from `172.20.0.0/22` for:
- Development team: 120 workstations
- Sales department: 45 workstations
- Server room: 25 servers
- Management: 12 offices
- Guest Wi-Fi: 30 devices
- Point-to-point link to ISP: 2 addresses

**Phase 1 — Planning (Driver A, 5 minutes):**
```bash
# First, calculate what we have available
python ex_5_01_cidr_flsm.py analyse 172.20.0.0/22
```

**Navigator task:** Write down on paper:
- Total addresses available
- Requirements sorted largest to smallest
- Predicted prefix for each requirement

**SWAP**

**Phase 2 — Implementation (Driver B, 7 minutes):**
```bash
# Run VLSM allocation
python ex_5_02_vlsm_ipv6.py vlsm 172.20.0.0/22 120 45 25 12 30 2
```

**Navigator task:**
- Compare output with paper predictions
- Calculate total efficiency
- Check if any address space remains

**SWAP**

**Phase 3 — Verification (Driver A, 5 minutes):**
```bash
# Verify each allocated subnet
python ex_5_01_cidr_flsm.py analyse 172.20.0.0/25
python ex_5_01_cidr_flsm.py analyse 172.20.0.128/26
# Continue for each subnet from VLSM output
```

**Discussion points:**
1. Why did Development get /25 instead of /26?
2. What is the overall address efficiency?
3. How many addresses remain for future growth?
4. What would happen if we added a 200-workstation department?

---

### Exercise P3: IPv6 Subnetting Challenge (15 minutes)

**Objective:** Work with IPv6 addresses and create a subnet plan.

**Scenario:**
Your organisation receives `2001:db8:acad::/48` from the ISP. Design subnets for:
- Building A (3 floors, each needing a /64)
- Building B (2 floors, each needing a /64)
- Data centre (4 server VLANs, each /64)
- Future expansion (reserve space)

**Phase 1 — Understanding (Driver A, 5 minutes):**
```bash
# Explore IPv6 basics
python ex_5_02_vlsm_ipv6.py ipv6-types

# Compress and expand practice
python ex_5_02_vlsm_ipv6.py ipv6 2001:0db8:acad:0000:0000:0000:0000:0001
python ex_5_02_vlsm_ipv6.py ipv6-expand 2001:db8:acad::1
```

**Navigator task:**
- Explain compression rules to Driver
- Verify the compressed form is correct

**SWAP**

**Phase 2 — Subnet Generation (Driver B, 5 minutes):**
```bash
# Generate subnets for our needs (3+2+4 = 9 subnets minimum)
python ex_5_02_vlsm_ipv6.py ipv6-subnets 2001:db8:acad::/48 64 12
```

**Navigator task:**
- Assign subnets to locations on paper:
  - :0000::/64 through :0002::/64 → Building A floors
  - :0003::/64 through :0004::/64 → Building B floors
  - :0010::/64 through :0013::/64 → Data centre VLANs
- Note: we skip some for logical grouping!

**SWAP**

**Phase 3 — Documentation (Driver A, 5 minutes):**

Create addressing table together:

| Location | Subnet | Gateway |
|----------|--------|---------|
| Building A, Floor 1 | 2001:db8:acad:0::/64 | 2001:db8:acad::1 |
| Building A, Floor 2 | 2001:db8:acad:1::/64 | 2001:db8:acad:1::1 |
| ... | ... | ... |

**Discussion points:**
1. How many /64 subnets can we create from a /48?
2. Why did we skip subnet numbers for logical grouping?
3. What is the gateway convention (::1)?
4. How does this compare to IPv4 planning?

---

## Communication Phrases

### Navigator to Driver

| Situation | Phrase |
|-----------|--------|
| Before execution | "What do you expect this to output?" |
| Spotting error | "Hold on, I think there's a typo in the third octet" |
| Suggesting check | "Can we verify that with the analyse command?" |
| Confusion | "I'm not sure why we got /25 — can you explain?" |
| Documentation | "The cheatsheet says the syntax is..." |

### Driver to Navigator

| Situation | Phrase |
|-----------|--------|
| Planning | "I'm going to run the VLSM command with these values..." |
| Uncertainty | "Does this prefix look right to you?" |
| Requesting help | "What's the formula for usable hosts again?" |
| Verification | "The output shows 62 hosts — does that match your prediction?" |

---

## Troubleshooting Together

When stuck, follow this sequence:

1. **Driver:** Explain current understanding aloud
2. **Navigator:** Ask clarifying questions
3. **Both:** Re-read the error message carefully (every word matters!)
4. **Navigator:** Check `docs/troubleshooting.md` or `docs/commands_cheatsheet.md`
5. **Driver:** Try a simpler version of the command
6. **Both:** If stuck for more than 5 minutes, call instructor

### Common Week 5 Issues

| Problem | Quick Fix |
|---------|-----------|
| "Invalid network address" | Use network address (e.g., .0), not host address |
| VLSM "insufficient space" | Check total requirements vs available addresses |
| IPv6 "invalid address" | Check for multiple :: or invalid hex digits |
| "Module not found" | Run from `/app/src/exercises` directory |

---

## Swap Schedule Template

| Time | Driver | Navigator | Activity |
|------|--------|-----------|----------|
| 0:00 | Partner A | Partner B | Exercise P1 start |
| 0:07 | Partner B | Partner A | Exercise P1 continue |
| 0:15 | Partner A | Partner B | Exercise P2 start |
| 0:22 | Partner B | Partner A | Exercise P2 continue |
| 0:29 | Partner A | Partner B | Exercise P2 verify |
| 0:35 | Partner B | Partner A | Exercise P3 start |
| 0:42 | Partner A | Partner B | Exercise P3 continue |
| 0:50 | Both | Both | Review and discuss |

---

## Reflection Questions (End of Session)

Answer together:

1. What was the most surprising thing you learned today?
2. Which concept is still unclear?
3. What would you do differently next time?
4. How did pair programming help (or hinder) your learning?

---

*Week 5: IP Addressing, Subnetting, VLSM — Pair Programming Guide*
*Computer Networks Laboratory — ASE, CSIE Bucharest*
