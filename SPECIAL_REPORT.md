# Computer Networks Teaching Materials at Top Universities
## An Independent Comparative Analysis

---

<div align="center">

**Comparative Study: Computer Networks Curricula**  
*Top 100 QS/THE/ARWU Faculties vs. the CLIM&TOMA/ASE-CSIE Project*

---

*"If you want to truly learn something, try teaching it."*  
— Richard Feynman (probably over coffee, much like us)

</div>

---

## Disclaimer and Conflict of Interest

This report was written by the authors of the CLIM&TOMA/ASE-CSIE materials, which creates an obvious conflict of interest. We acknowledge that absolute objectivity is an ideal we strive towards rather than a certainty we possess. Readers are encouraged to verify the cited sources independently and form their own opinions.

In other words: yes, we are showing off a bit, but we are trying to be fair about it.

---

## 1. Introduction and Methodology

### 1.1. Research Context

The **CLIM&TOMA/ASE-CSIE** project (hereafter referred to as the *reference project*) emerged from a collaboration between **ing. dr. Antonio CLIM** and **conf. dr. Andrei TOMA** at the Bucharest University of Economic Studies, Faculty of Economic Cybernetics, Statistics and Informatics (ASE-CSIE).

The initial concept, base scripts and countless brainstorming sessions (mostly held at **The Dose** coffee shop in Bucharest — a place that deserves credit for the sheer volume of caffeine invested in this endeavour) led to developing a laboratory kit for the *Computer Networks* course that attempts to combine:

- Academic rigour with practical accessibility
- Modern technologies (Docker, WSL2) with evidence-based pedagogy
- Comprehensiveness with... well, more comprehensiveness

Conf. dr. Andrei TOMA brings a rare talent to this project: the ability to reduce complicated concepts to their actual essence — a skill that, in our experience, is worth more than any sophisticated framework.

### 1.2. Methodology

We analysed **over 20 networking courses** from Top 100 universities (according to QS World University Rankings, Times Higher Education and ARWU), focusing on materials publicly available on GitHub and open educational platforms.

**Evaluation criteria:**

| Code | Dimension | Description |
|:---:|:-----------|:----------|
| **C1** | Comprehensiveness | Number of weeks, topic coverage |
| **C2** | Code Quality | Type hints, docstrings, standards |
| **C3** | Pedagogical Sophistication | Evidence-based methods (peer instruction, misconceptions) |
| **C4** | Infrastructure | Docker, virtualisation, environment verification |
| **C5** | Documentation | README files, guides, cheatsheets, glossaries |
| **C6** | Projects | Variety, scale, teamwork |
| **C7** | Interactive Elements | HTML presentations, quizzes, demos |

---

## 2. The Academic Landscape: Who Does What and How

### 2.1. Universities and Courses Analysed

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    GEOGRAPHY OF ANALYSED COURSES                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   🇺🇸 USA                           🇪🇺 Europe                          │
│   ├── Stanford CS144               ├── ETH Zürich (227-0120-00L)       │
│   ├── UC Berkeley CS168            ├── EPFL (COM-208)                  │
│   ├── CMU 15-441/641               ├── TU München                      │
│   ├── MIT 6.829                    ├── UCLouvain CNP3                  │
│   ├── Princeton COS 461            └── Imperial College                │
│   ├── U. Michigan EECS 489                                             │
│   ├── UIUC ECE 438                 🇦🇸 Asia                            │
│   ├── Georgia Tech CS 6250         ├── KAIST CS341                     │
│   ├── Johns Hopkins EN.601.414     ├── NUS CS2105                      │
│   └── UT Austin                    ├── Tsinghua                        │
│                                    ├── CUHK CSCI 4430                  │
│   🇷🇴 Romania                       └── Peking University               │
│   └── ASE-CSIE (CLIM&TOMA)                                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2. Main Comparison Table

> **Legend**: ✅ Fully implemented | ⚠️ Partial/Community-based | ❌ Absent/Undocumented

| University | Course | Weeks | Docker | Interactive Slides | Explicit Pedagogy | Projects | Auto-test |
|:-----------|:-------|:-----:|:------:|:------------------:|:-----------------:|:--------:|:---------:|
| **🇷🇴 ASE-CSIE** | **CLIM&TOMA** | **14** | ✅ | ✅ HTML/CSS | ✅ Peer Instr., Misconc. | **15+ group** | ✅ |
| 🇺🇸 Stanford | CS144 | 10 | ⚠️ | ❌ PDF | ⚠️ Lab hints | 8 individual | ✅ |
| 🇨🇭 ETH Zürich | Comm. Networks | 15 | ✅ | ❌ Traditional | ❌ | 2 group | ⚠️ |
| 🇺🇸 Michigan | EECS 489 | 14-15 | ⚠️ | ❌ PDF slides | ⚠️ Quizzes | 4 group | ✅ |
| 🇺🇸 CMU | 15-441/641 | ~14 | ✅ | ❌ | ❌ | 3 multi-week | ✅ |
| 🇺🇸 Berkeley | CS168 | 17 | ⚠️ | ⚠️ Google Slides | ❌ | 3 projects | ✅ |
| 🇺🇸 Princeton | COS 461 | 12 | ⚠️ | ❌ Flipped video | ❌ | 5 labs | ✅ |
| 🇰🇷 KAIST | CS341 (KENSv3) | 16 | ✅ | ❌ | ✅ PCAP/Wireshark | 4 individual | ✅ |
| 🇧🇪 UCLouvain | CNP3 | Var. | ✅ | ❌ PPT/Keynote | ✅ INGInious | Multiple | ✅ |
| 🇺🇸 NPS | Labtainers | Modular | ✅ | ❌ PDF manuals | ✅ Individualised | 50+ labs | ✅ |

---

## 3. Detailed Analysis by Dimension

### 3.1. Dimension C1: Comprehensiveness

```
Number of Course Weeks

Berkeley CS168     ████████████████████████████████░░  17 weeks
KAIST CS341        ███████████████████████████████░░░  16 weeks
ETH Zürich         █████████████████████████████░░░░░  15 weeks
Michigan EECS 489  ████████████████████████████░░░░░░  14-15 weeks
CLIM&TOMA/ASE-CSIE ███████████████████████████░░░░░░░  14 weeks  ◄── Reference project
CMU 15-441         ███████████████████████████░░░░░░░  ~14 weeks
Princeton COS 461  ███████████████████████░░░░░░░░░░░  12 weeks
Stanford CS144     ████████████████████░░░░░░░░░░░░░░  10 weeks (quarter system)
```

**Observation**: Berkeley CS168 leads in terms of sheer breadth (17 weeks), though Stanford's quarter format (10 weeks) compensates through density. The CLIM&TOMA/ASE-CSIE course sits in the upper range alongside Michigan and CMU.

**Topic coverage comparison:**

| Topic | Stanford | ETH | Michigan | Berkeley | CLIM&TOMA |
|:------|:--------:|:---:|:--------:|:--------:|:---------:|
| TCP/IP Fundamentals | ✅ | ✅ | ✅ | ✅ | ✅ |
| Socket Programming | ✅ | ✅ | ✅ | ✅ | ✅ |
| HTTP/REST | ✅ | ⚠️ | ✅ | ✅ | ✅ |
| DNS Deep Dive | ⚠️ | ✅ | ✅ | ✅ | ✅ |
| Routing (OSPF, BGP) | ⚠️ | ✅ | ✅ | ✅ | ✅ |
| SDN/OpenFlow | ❌ | ⚠️ | ✅ | ✅ | ✅ |
| Load Balancing | ❌ | ⚠️ | ⚠️ | ✅ | ✅ |
| IoT/MQTT | ❌ | ❌ | ❌ | ❌ | ✅ |
| gRPC/Modern RPC | ❌ | ❌ | ⚠️ | ⚠️ | ✅ |
| Security (TLS, VPN) | ⚠️ | ✅ | ⚠️ | ✅ | ✅ |

### 3.2. Dimension C2: Code Quality

We must be honest here: **Stanford CS144** sets the standard for C++ code with clang-tidy linting, ASan/UBSan sanitisers, modern CMake and an explicit coding style guide.

**Michigan EECS 489** offers the most consistent Python code (85.6% of the repository).

The **CLIM&TOMA** project uses Python with type hints (partial coverage), extensive docstrings and a standardised modular structure across weeks.

> *Self-criticism*: Stanford taught us that automated linting is not a luxury but a necessity. We are still working on full integration.

### 3.3. Dimension C3: Pedagogical Sophistication (THE CRITICAL ZONE)

This is where the differences become most visible:

```
┌──────────────────────────────────────────────────────────────────────────┐
│              EVIDENCE-BASED PEDAGOGICAL ELEMENTS                        │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Element                        Present in university courses?           │
│  ─────────────────────────────────────────────────────────────────       │
│                                                                          │
│  Peer Instruction Questions     CLIM&TOMA ✅ | Rest ❌                   │
│  (Mazur-style, 5 steps)                                                  │
│                                                                          │
│  Documented Misconceptions      CLIM&TOMA ✅ | Rest ❌                   │
│  (per topic, with corrections)                                           │
│                                                                          │
│  Prediction Prompts             CLIM&TOMA ✅ | Rest ❌                   │
│  (Brown & Wilson Principle 4)                                            │
│                                                                          │
│  Parsons Problems               CLIM&TOMA ✅ | Rest ❌                   │
│  (code arrangement exercises)                                            │
│                                                                          │
│  Code Tracing Exercises         CLIM&TOMA ✅ | KAIST ⚠️ | Rest ❌       │
│  (step-by-step execution)                                                │
│                                                                          │
│  Pair Programming Guides        CLIM&TOMA ✅ | Rest ❌                   │
│  (Driver/Navigator rotation)                                             │
│                                                                          │
│  Concept Analogies Doc          CLIM&TOMA ✅ | Rest ❌                   │
│  (networking concepts mapped                                             │
│   to everyday experiences)                                               │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

**Closest alternatives:**
- **UCLouvain CNP3**: INGInious platform for auto-graded exercises
- **KAIST KENSv3**: PCAP generation for Wireshark analysis
- **Labtainers (NPS)**: Individualised parameters per student

> *Note*: The near-total absence of explicit pedagogical methods in elite curricula surprised us. Or perhaps it should not have — there is a difference between being an excellent networking researcher and being a pedagogue informed by educational research.

### 3.4. Dimension C4: Docker Infrastructure

```
                        INFRASTRUCTURE MATURITY

          Nothing   Basic VM    Mininet    Docker    Full Stack
            │         │          │          │           │
Stanford ───┼─────────┼──────────┼────⚫─────┼───────────┤  (community images)
            │         │          │          │           │
ETH Zürich ─┼─────────┼──────────┼──────────┼─────────⚫─┤  (mini-Internet!)
            │         │          │          │           │
Michigan ───┼─────────┼────⚫─────┼──────────┼───────────┤  (Mininet focus)
            │         │          │          │           │
CMU ────────┼─────────┼──────────┼──────────┼────⚫──────┤  (official Dockerfiles)
            │         │          │          │           │
Berkeley ───┼─────────┼────⚫─────┼──────────┼───────────┤  (limited)
            │         │          │          │           │
CLIM&TOMA ──┼─────────┼──────────┼──────────┼────⚫──────┤  (per-week compose)
            │         │          │          │           │
Labtainers ─┼─────────┼──────────┼──────────┼─────────⚫─┤  (50+ lab containers)
            │         │          │          │           │
```

**ETH Zürich mini-Internet** deserves special mention: each student group operates an Autonomous System (AS) with real FRRouting for BGP/OSPF, MPLS and RPKI support. It has 219 stars on GitHub.

**The CLIM&TOMA project** provides a standardised `docker-compose.yml` per week, Portainer (port 9000) for visual management, consistent IP schemes (172.20.X.0/24) and utility scripts (`start_lab.py` / `stop_lab.py` / `cleanup.py`).

### 3.5. Dimension C5: Documentation

| Element | Stanford | Berkeley | Michigan | UCLouvain | CLIM&TOMA |
|:--------|:--------:|:--------:|:--------:|:---------:|:---------:|
| Comprehensive README | ✅ | ✅ | ✅ | ✅ | ✅ |
| Troubleshooting Guide | ⚠️ | ⚠️ | ⚠️ | ✅ | ✅ |
| Commands Cheatsheet | ❌ | ❌ | ❌ | ❌ | ✅ |
| Glossary of terms | ❌ | ✅* | ❌ | ✅* | ✅ |
| Instructor Guide | ❌ | ❌ | ❌ | ✅ | ✅ |
| Further Reading | ⚠️ | ✅ | ⚠️ | ✅ | ✅ |

*\* Within the textbook*

**Berkeley CS168** wins when it comes to the **open textbook** — a complete, professionally edited networking textbook available free under CC BY-SA 4.0 at `textbook.cs168.io`. This is probably the most valuable open-source networking resource for self-learners.

### 3.6. Dimension C6: Projects

```
Number and Type of Projects

CLIM&TOMA/ASE-CSIE  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  15+ group projects
                    ▒▒▒▒▒▒▒▒▒▒                        + 5 individual reserve

Labtainers (NPS)    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  50+ labs
                    (modular, security focus)

Stanford CS144      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                  8 checkpoints
                    (progressive TCP/IP stack)

KAIST KENSv3        ▓▓▓▓▓▓▓▓                          4 TCP projects
                    (full implementation)

Michigan EECS 489   ▓▓▓▓▓▓▓▓                          4 assignments
                    (sockets → datacenter)

CMU 15-441          ▓▓▓▓▓▓                            3 large projects
                    (multi-week each)
```

**Stanford CS144** wins on narrative coherence — the 8 checkpoints incrementally build a complete TCP/IP stack, culminating in real end-to-end connectivity through relay servers.

**The CLIM&TOMA project** emphasises variety and teamwork (SDN, microservices, IDS/IPS, IoT, etc.).

### 3.7. Dimension C7: Interactive Elements

This is probably the clearest differentiator:

```
┌─────────────────────────────────────────────────────────────────────┐
│              INTERACTIVE HTML/CSS/JS PRESENTATIONS                   │
│                                                                      │
│    ┌─────────────────────────────────────────────────────────┐      │
│    │                                                         │      │
│    │   ╔═══════════════════════════════════════════════╗     │      │
│    │   ║  Progress Bar  ████████████░░░░░  Slide 7/14  ║     │      │
│    │   ╠═══════════════════════════════════════════════╣     │      │
│    │   ║                                               ║     │      │
│    │   ║    Week 3: TCP Tunnelling                     ║     │      │
│    │   ║                                               ║     │      │
│    │   ║    [Interactive Diagram]  [Quiz Button]       ║     │      │
│    │   ║                                               ║     │      │
│    │   ║    ◄ Prev    [ToC]    [⛶ Fullscreen]   Next ► ║     │      │
│    │   ╚═══════════════════════════════════════════════╝     │      │
│    │                                                         │      │
│    │   Features: copy-to-clipboard, keyboard nav,            │      │
│    │   reveal animations, responsive design                  │      │
│    │                                                         │      │
│    └─────────────────────────────────────────────────────────┘      │
│                                                                      │
│    Courses that offer this:  CLIM&TOMA/ASE-CSIE                     │
│    Courses that do NOT:      All others analysed                    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

> *This is not a joke*: We searched through over 20 repositories and course websites. PDFs, PowerPoints, Google Slides, video recordings — but interactive HTML presentations with quizzes, animations and keyboard navigation? None.

---

## 4. Case Studies: What Others Do Well

To avoid sounding like we are just patting ourselves on the back, here is what we learnt from others:

### 4.1. Stanford CS144: The Implementation Master

**What they do brilliantly:**
- Perfect pedagogical progression: ByteStream → TCPReceiver → TCPSender → Router
- Automated tests with `make check_labN`
- High-quality documentation for each lab
- Video lectures publicly available

**What they lack:**
- Official Docker infrastructure (only community images)
- Explicit pedagogical methodology
- Group projects

**Lesson learnt**: Narrative coherence in projects matters enormously.

### 4.2. ETH Zürich: The Infrastructure King

**What they do brilliantly:**
- mini-Internet project: Internet-scale simulation
- Professional Docker orchestration
- Students operate real Autonomous Systems
- RPKI, MPLS, BGP — current technologies

**What they lack:**
- Explicit pedagogical materials
- Interactive presentations
- Variety in project types

**Lesson learnt**: Scale matters — operating an AS is different from writing a socket client.

### 4.3. Berkeley CS168: The Open Textbook

**What they do brilliantly:**
- Free textbook, professionally edited, CC BY-SA 4.0
- 17 weeks of content
- Modern coverage (datacenter networking, ML collective ops)
- Comprehensive glossary

**What they lack:**
- Lab infrastructure
- Practical coding exercises
- Interactive presentations

**Lesson learnt**: A good textbook is worth a thousand PowerPoint slides.

### 4.4. KAIST KENSv3: The Educational Framework

**What they do brilliantly:**
- Custom framework for TCP implementation
- PCAP logging for Wireshark debugging
- Reference binaries for incremental testing
- POSIX-compatible API

**What they lack:**
- Pedagogical documentation
- Thematic variety
- Interactive presentations

**Lesson learnt**: A dedicated educational framework can be more valuable than industrial tooling.

---

## 5. Summary of Findings

### 5.1. Final Evaluation Matrix

| Course | C1 Compr. | C2 Code | C3 Pedag. | C4 Docker | C5 Docs | C6 Proj. | C7 Interact. | TOTAL |
|:-------|:---------:|:-------:|:---------:|:---------:|:-------:|:--------:|:------------:|:-----:|
| **CLIM&TOMA/ASE-CSIE** | 8 | 7 | 10 | 8 | 9 | 9 | 10 | **61/70** |
| Stanford CS144 | 7 | 10 | 4 | 5 | 8 | 9 | 2 | 45/70 |
| ETH Zürich | 9 | 7 | 3 | 10 | 7 | 6 | 2 | 44/70 |
| Berkeley CS168 | 10 | 5 | 3 | 4 | 10 | 5 | 3 | 40/70 |
| Michigan EECS 489 | 8 | 8 | 4 | 5 | 8 | 7 | 2 | 42/70 |
| CMU 15-441 | 8 | 8 | 2 | 8 | 6 | 7 | 2 | 41/70 |
| KAIST KENSv3 | 9 | 6 | 6 | 8 | 5 | 6 | 2 | 42/70 |
| Labtainers (NPS) | 7 | 5 | 7 | 10 | 8 | 10 | 2 | 49/70 |

*Scores 1-10 per dimension, subjectively evaluated by the authors (with all associated biases)*

### 5.2. Main Conclusions

1. **The Pedagogical Gap**: Evidence-based teaching methods (peer instruction, misconceptions, Parsons problems) are practically absent from publicly available elite university curricula. This is the main opportunity the CLIM&TOMA project attempts to exploit.

2. **Fragmented Excellence**: No single course excels across all dimensions. Stanford dominates implementation, ETH dominates infrastructure, Berkeley dominates documentation, KAIST dominates educational frameworks. Our project attempts to integrate the strengths from each.

3. **Absence of Interactive Presentations**: Apart from the reference project, all courses analysed use static formats (PDF, PPT, video). This is a surprisingly large unexplored niche.

4. **Docker as Emerging Standard**: Containerisation is becoming the norm, but implementation varies enormously — from community images (Stanford) to sophisticated orchestrations (ETH, Labtainers).

### 5.3. Limitations of This Analysis

- **Author bias**: Obviously, we are evaluating our own project.
- **Private materials**: Many universities do not publish all materials; we analysed only what is publicly available.
- **Temporal snapshot**: Curricula evolve; this analysis reflects the state as of January 2025.
- **Subjectivity in scores**: Weights and scores reflect our priorities.

---

## 6. Recommendations and Future Directions

### 6.1. What We Learnt for the CLIM&TOMA Project

| From | To adopt |
|:-----|:---------|
| Stanford | Narrative coherence in projects; C++ coding standards |
| ETH Zürich | Infrastructure scale (mini-Internet) |
| Berkeley | Open textbook as parallel resource |
| KAIST | Dedicated educational framework |
| Labtainers | Per-student parameterisation |

### 6.2. Proposed Roadmap

```
2025 Q1  ─────► Automated linting integration (flake8, mypy strict)
              │
2025 Q2  ─────► Complete RO ↔ EN materials translation
              │
2025 Q3  ─────► Mini SDN project at scale (ETH-inspired)
              │
2025 Q4  ─────► Open textbook companion (Berkeley-inspired)
              │
2026+    ─────► KENS-style framework for TCP implementation
```

---

## 7. Acknowledgements

This project would not exist without:

- **conf. dr. Andrei TOMA** — for the initial ideas, base scripts and endless discussions at The Dose that transformed vague concepts into concrete architecture
- **The Dose, Bucharest** — for the coffee that fuelled this project (literally)
- **The Open Source Community** — for all the resources we studied and learnt from
- **ASE-CSIE Students** — for their patience in being guinea pigs for early versions

---

## References and Resources

### Courses Analysed (in order of citation)

| # | University | Course | URL |
|:-:|:-----------|:-------|:----|
| 1 | Stanford | CS144 | `cs144.github.io` / `github.com/CS144` |
| 2 | ETH Zürich | 227-0120-00L | `comm-net.ethz.ch` |
| 3 | U. Michigan | EECS 489 | `github.com/mosharaf/eecs489` |
| 4 | CMU | 15-441/641 | `computer-networks.github.io` |
| 5 | UC Berkeley | CS168 | `textbook.cs168.io` |
| 6 | Princeton | COS 461 | `cs.princeton.edu/courses/archive/fall21/cos461` |
| 7 | KAIST | CS341 | `anlab-kaist.github.io/KENSv3` |
| 8 | UCLouvain | CNP3 | `inl.info.ucl.ac.be/CNP3` |
| 9 | NPS | Labtainers | `nps.edu/web/c3o/labtainers` |
| 10 | Johns Hopkins | EN.601.414 | `github.com/xinjin/course-net` |
| 11 | CUHK | CSCI 4430 | `github.com/henryhxu/CSCI4430` |

### Pedagogical Methodology

- Brown, N. C. C. & Wilson, G. (2018). *Ten Quick Tips for Teaching Programming*
- Mazur, E. (1997). *Peer Instruction: A User's Manual*
- Parsons, D. & Haden, P. (2006). *Parson's Programming Puzzles*

---

<div align="center">

**CLIM&TOMA/ASE-CSIE Networking Project**  
*Bucharest University of Economic Studies*  
*Faculty of Economic Cybernetics, Statistics and Informatics*

---

*Last updated: January 2025*  
*Document version: 1.0*

</div>
