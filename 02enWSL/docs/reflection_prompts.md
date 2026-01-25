# 🪞 Reflection Prompts — Week 2: Architectural Models and Socket Programming

> NETWORKING class — ASE, CSIE Bucharest  
> Computer Networks Laboratory | by ing. dr. Antonio Clim

Complete these reflection questions after finishing the laboratory exercises. Reflection deepens learning by connecting new knowledge to prior experience and future applications.

**Time required:** 10-15 minutes

---

## Individual Reflection

Answer these questions in your lab journal or personal notes.

### 1. Connection to Prior Knowledge

**Question:** Before this lab, how did you think data was sent between two programs on different computers? How has your understanding changed?

**Guidance:**
- Consider what you knew about client-server communication
- Think about the role of the operating system
- Reflect on the difference between "sending a message" and "sending bytes"

---

### 2. Most Surprising Discovery

**Question:** What aspect of socket programming or network protocols surprised you most? Why?

**Common discoveries students report:**
- TCP doesn't preserve message boundaries
- UDP can receive replies on the same socket
- The three-way handshake happens only once
- Threading dramatically affects server responsiveness

---

### 3. Difficulty Analysis

**Question:** Which exercise was most challenging? What made it difficult, and how did you overcome the obstacle?

**Reflection framework:**
- Was the difficulty conceptual (understanding WHY) or procedural (understanding HOW)?
- Did Wireshark help clarify what was happening?
- Would pair programming have helped?

---

### 4. Real-World Connection

**Question:** Identify one application you use daily that relies on TCP and one that uses UDP. Explain why each protocol is appropriate for that application.

**Examples to consider:**
- Web browsing, email, file downloads (TCP)
- Video calls, online games, DNS lookups (UDP)
- What would happen if they used the opposite protocol?

---

### 5. Teaching Test

**Question:** If you had to explain the TCP three-way handshake to someone who has never programmed, what analogy would you use?

**Analogy criteria:**
- Should be relatable to everyday experience
- Should capture the bidirectional nature
- Should explain WHY both sides need to confirm

---

## Pair/Group Discussion

Discuss these questions with a classmate or study group.

### 6. Design Decision

**Question:** You're building a chat application. Would you use TCP or UDP? What are the trade-offs?

**Consider:**
- Message delivery guarantees
- Message ordering
- Real-time responsiveness
- Multi-user scenarios

---

### 7. Error Analysis

**Question:** Share the most frustrating error you encountered. How did you diagnose it? What would you do differently next time?

**Common errors:**
- "Address already in use"
- "Connection refused"
- Receiving merged/split messages
- Server not accessible from containers

---

### 8. Wireshark Insights

**Question:** What did Wireshark reveal that you couldn't see from the code alone? How might this change how you debug network issues in future?

**Observable phenomena:**
- Actual packet timing vs assumed timing
- TCP retransmissions
- Segment sizes vs send() sizes
- Connection state transitions

---

## Forward-Looking Reflection

### 9. Week 3 Preparation

**Question:** Based on this week's experience, what questions do you have about UDP broadcasting and multicasting (Week 3 topics)?

**Consider:**
- How does broadcast differ from sending to multiple individual addresses?
- Can TCP do broadcast?
- What happens when a multicast packet is lost?

---

### 10. Skill Self-Assessment

Rate your confidence (1-5) on each skill after this lab:

| Skill | Before Lab | After Lab | Goal |
|-------|------------|-----------|------|
| Explain TCP vs UDP differences | | | 5 |
| Implement a TCP server | | | 4 |
| Implement a UDP server | | | 4 |
| Use Wireshark to analyse traffic | | | 4 |
| Debug "Address already in use" | | | 5 |
| Choose TCP vs UDP for scenarios | | | 4 |

**Action plan:** For any skill rated below 3, what specific practice will you do before next week?

---

## Metacognitive Reflection

### 11. Learning Strategy Evaluation

**Question:** What learning strategy worked best for you in this lab?

- [ ] Reading theory first, then coding
- [ ] Diving into code, then reading theory
- [ ] Pair programming throughout
- [ ] Solo work with occasional questions
- [ ] Following along with instructor demo
- [ ] Experimenting beyond the exercises

---

### 12. Misconception Check

**Question:** Review the [misconceptions document](misconceptions.md). Which misconception did you hold before this lab? How did you discover it was wrong?

---

## Submission Checklist

Before leaving lab, confirm:

- [ ] All three exercises completed
- [ ] At least 3 individual reflection questions answered
- [ ] At least 1 pair discussion completed
- [ ] Wireshark captures saved to `pcap/`
- [ ] Self-assessment table completed
- [ ] Questions for Week 3 noted

---

## Instructor Use

These reflections can be used for:
- Entry/exit tickets
- Discussion starters
- Formative assessment data
- Identifying struggling students

**Suggested integration:**
- Q1-Q5: Exit ticket (last 10 min of lab)
- Q6-Q8: Start of next session (review)
- Q9-Q10: Pre-lab preparation check

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
