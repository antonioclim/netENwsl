# 📚 Further Reading — Week 2: Architectural Models and Socket Programming

> NETWORKING class — ASE, CSIE Bucharest  
> Computer Networks Laboratory | by ing. dr. Antonio Clim

Curated resources for deeper understanding of socket programming and network architecture.

---

## Difficulty Legend

| Rating | Meaning | Suitable For |
|--------|---------|--------------|
| ★☆☆ | Introductory | First-time learners |
| ★★☆ | Intermediate | After completing lab exercises |
| ★★★ | Advanced | Deep dive, reference |

---

## Essential Reading

These resources directly support the lab exercises.

### Official Documentation

| Resource | Difficulty | Time | Notes |
|----------|------------|------|-------|
| [Python socket module](https://docs.python.org/3/library/socket.html) | ★★☆ | 30 min | Official reference — keep open during coding |
| [Python threading module](https://docs.python.org/3/library/threading.html) | ★★☆ | 20 min | For concurrent server implementation |
| [Wireshark User's Guide](https://www.wireshark.org/docs/wsug_html/) | ★★☆ | 1 hr | Chapters 3-6 most relevant |

### Textbook Chapters

| Resource | Difficulty | Time | Notes |
|----------|------------|------|-------|
| Kurose & Ross, Ch. 1.5: Protocol layers | ★☆☆ | 45 min | OSI and TCP/IP models |
| Kurose & Ross, Ch. 3.1-3.3: Transport layer | ★★☆ | 1 hr | TCP and UDP fundamentals |
| Stevens, Ch. 4: Elementary TCP Sockets | ★★★ | 2 hr | Definitive socket programming reference |

---

## Deep Dive Resources

For students who want to go beyond lab requirements.

### TCP/IP Internals

| Resource | Difficulty | Time | Topic |
|----------|------------|------|-------|
| [RFC 793](https://www.rfc-editor.org/rfc/rfc793.html) | ★★★ | 2 hr | Original TCP specification |
| [RFC 768](https://www.rfc-editor.org/rfc/rfc768.html) | ★★☆ | 15 min | UDP specification (very short!) |
| [TCP/IP Illustrated](https://www.amazon.com/TCP-Illustrated-Vol-Addison-Wesley-Professional/dp/0201633469) by Stevens | ★★★ | N/A | The classic reference |
| [Beej's Guide to Network Programming](https://beej.us/guide/bgnet/) | ★★☆ | 3 hr | Excellent C tutorial (concepts apply to Python) |

### Socket Programming Tutorials

| Resource | Difficulty | Time | Language |
|----------|------------|------|----------|
| [Real Python: Socket Programming](https://realpython.com/python-sockets/) | ★★☆ | 1 hr | Python |
| [GeeksforGeeks: Socket Programming](https://www.geeksforgeeks.org/socket-programming-python/) | ★☆☆ | 30 min | Python |
| [IBM: Sockets programming](https://developer.ibm.com/tutorials/l-sock/) | ★★★ | 1 hr | C/Linux |

### Concurrent Programming

| Resource | Difficulty | Time | Topic |
|----------|------------|------|-------|
| [Python Concurrency](https://realpython.com/python-concurrency/) | ★★☆ | 1 hr | Threading vs async |
| [C10K Problem](http://www.kegel.com/c10k.html) | ★★★ | 45 min | Historical context for scalability |
| [GIL Explained](https://realpython.com/python-gil/) | ★★★ | 30 min | Python threading limitations |

---

## Video Resources

For visual learners.

| Resource | Difficulty | Duration | Topic |
|----------|------------|----------|-------|
| [Computerphile: TCP/IP](https://www.youtube.com/watch?v=PpsEaqJV_A0) | ★☆☆ | 12 min | TCP/IP basics |
| [Computerphile: UDP](https://www.youtube.com/watch?v=Vdc8TCESIg8) | ★☆☆ | 8 min | UDP explained |
| [Ben Eater: Networking Tutorial](https://www.youtube.com/playlist?list=PLowKtXNTBypH19whXTVoG3oKSuOcw_XeW) | ★★☆ | 2 hr | Building network from scratch |
| [MIT 6.829: Computer Networks](https://ocw.mit.edu/courses/6-829-computer-networks-fall-2002/) | ★★★ | Course | Full MIT course |

---

## Wireshark Resources

| Resource | Difficulty | Time | Notes |
|----------|------------|------|-------|
| [Wireshark Tutorial](https://www.youtube.com/watch?v=TkCSr30UojM) | ★☆☆ | 20 min | Beginner introduction |
| [Display Filter Reference](https://www.wireshark.org/docs/dfref/) | ★★☆ | Ref | Filter syntax reference |
| [Sample Captures](https://wiki.wireshark.org/SampleCaptures) | ★★☆ | N/A | Practice with pre-recorded traffic |
| [Practical Packet Analysis](https://nostarch.com/packetanalysis3) | ★★★ | Book | Thorough Wireshark book |

---

## Docker and Container Networking

| Resource | Difficulty | Time | Topic |
|----------|------------|------|-------|
| [Docker Networking Overview](https://docs.docker.com/network/) | ★★☆ | 30 min | Official documentation |
| [Container Networking Deep Dive](https://www.youtube.com/watch?v=6v_BDHIgOY8) | ★★★ | 45 min | Linux namespaces |
| [Docker Compose Networking](https://docs.docker.com/compose/networking/) | ★★☆ | 20 min | Multi-container networking |

---

## WSL2 Resources

| Resource | Difficulty | Time | Topic |
|----------|------------|------|-------|
| [WSL2 Networking](https://docs.microsoft.com/en-us/windows/wsl/networking) | ★★☆ | 20 min | Official networking guide |
| [WSL2 Networking Limitations](https://github.com/microsoft/WSL/issues/4150) | ★★★ | N/A | Known issues and workarounds |
| [Accessing Windows from WSL](https://docs.microsoft.com/en-us/windows/wsl/filesystems) | ★☆☆ | 10 min | File system access |

---

## Academic Papers

For research-oriented students.

| Paper | Difficulty | Topic |
|-------|------------|-------|
| [End-to-End Arguments in System Design](https://web.mit.edu/Saltzer/www/publications/endtoend/endtoend.pdf) | ★★★ | Why TCP is end-to-end |
| [A Protocol for Packet Network Intercommunication](https://www.cs.princeton.edu/courses/archive/fall06/cos561/papers/cerf74.pdf) | ★★★ | Original TCP/IP paper |
| [Congestion Avoidance and Control](https://ee.lbl.gov/papers/congavoid.pdf) | ★★★ | TCP congestion control |

---

## Books (Full References)

### Highly Recommended

1. **Computer Networking: A Top-Down Approach** (8th ed.)
   - Authors: Kurose, J. & Ross, K.
   - Publisher: Pearson, 2021
   - Rating: ★★☆
   - Notes: Course textbook, excellent diagrams

2. **UNIX Network Programming, Vol. 1** (3rd ed.)
   - Authors: Stevens, W. R., Fenner, B., & Rudoff, A.
   - Publisher: Addison-Wesley, 2004
   - Rating: ★★★
   - Notes: The definitive socket programming reference (C-focused)

### Additional Resources

3. **TCP/IP Illustrated, Vol. 1** (2nd ed.)
   - Author: Fall, K. & Stevens, W. R.
   - Publisher: Addison-Wesley, 2011
   - Rating: ★★★
   - Notes: Protocol internals with Wireshark examples

4. **Effective Python** (2nd ed.)
   - Author: Slatkin, B.
   - Publisher: Addison-Wesley, 2019
   - Rating: ★★☆
   - Notes: Items 52-56 cover concurrency

---

## Quick Reference Cards

| Resource | Format | Notes |
|----------|--------|-------|
| [TCP/IP Cheat Sheet](https://packetlife.net/library/cheat-sheets/) | PDF | Port numbers, header formats |
| [Wireshark Cheat Sheet](https://packetlife.net/media/library/13/Wireshark_Display_Filters.pdf) | PDF | Display filter syntax |
| [Python socket Cheat Sheet](https://www.pythonsheets.com/notes/python-socket.html) | Web | Quick function reference |

---

## Reading Path Recommendations

### Path 1: "I want to understand the theory" (3-4 hours)

1. Kurose & Ross, Ch. 1.5 (45 min) — Models
2. Computerphile TCP video (12 min) — Visual explanation
3. RFC 768 (15 min) — See how simple UDP is
4. Beej's Guide, Ch. 1-3 (1 hr) — Socket concepts

### Path 2: "I want to code better" (2-3 hours)

1. Python socket docs (30 min) — Official reference
2. Real Python sockets tutorial (1 hr) — Practical examples
3. Python threading docs (20 min) — Concurrency basics
4. Python GIL article (30 min) — Why threading has limits

### Path 3: "I want to debug better" (2 hours)

1. Wireshark tutorial video (20 min) — Basic capture
2. Sample captures practice (30 min) — Real traffic
3. Display filter reference (30 min) — Finding needles
4. Practical Packet Analysis, Ch. 1-3 (40 min) — Methodology

---

## Week 3 Preparation

If you have extra time, preview these for next week (UDP Broadcast/Multicast):

| Resource | Difficulty | Time |
|----------|------------|------|
| [Multicast Overview](https://en.wikipedia.org/wiki/Multicast) | ★☆☆ | 15 min |
| [Python Multicast](https://pymotw.com/3/socket/multicast.html) | ★★☆ | 30 min |
| RFC 1112: Host Extensions for IP Multicasting | ★★★ | 1 hr |

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
