# 🎯 Learning Objectives Traceability Matrix — Week 9

> Session Layer (L5) and Presentation Layer (L6)
> NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

---

## Overview

| LO | Description | Bloom Level | Primary Exercise | Quiz Coverage |
|----|-------------|-------------|------------------|---------------|
| LO1 | Identify connection vs session | Understand | ex_9_02, ex_9_03 | q01, q02 |
| LO2 | Explain endianness mechanisms | Apply | ex_9_01 | q03, q04, q05 |
| LO3 | Implement binary framing | Apply | ex_9_01, hw_9_01 | q06, q07 |
| LO4 | Demonstrate FTP sessions | Apply | ex_9_03, ex_9_04 | q08, q09 |
| LO5 | Analyse packet captures | Analyse | capture_traffic.py | q10, q13 |
| LO6 | Design checkpoint-recovery | Create | hw_9_02 | q11, q12, q14, q15 |

---

## Detailed Coverage Matrix

| Resource Type | LO1 | LO2 | LO3 | LO4 | LO5 | LO6 | Coverage |
|---------------|-----|-----|-----|-----|-----|-----|----------|
| Theory Summary | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100% |
| Exercises (4) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100% |
| Homework (2) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100% |
| Tests | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100% |
| Quiz (15 Q) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100% |
| Peer Instruction | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100% |
| Misconceptions | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100% |
| Parsons (5) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100% |
| Code Tracing | ✅ | ✅ | ✅ | - | - | - | 50% |

---

## LO → Artifact Mapping

### LO1: Identify connection vs session

| Artifact | Location | Verification |
|----------|----------|--------------|
| Theory | `docs/theory_summary.md` §Session Layer | Read and understand |
| Exercise | `ex_9_02_implement_pseudo_ftp.py` | Run `--selftest` |
| Exercise | `ex_9_03_ftp_client_demo.py` | Complete FTP session |
| Quiz | q01, q02 | `python formative/run_quiz.py --lo LO1` |
| Misconception | #1 "TCP connection IS session" | Review docs/misconceptions.md |
| Peer Instruction | Question 3 | Classroom activity |
| Parsons | P2 (FTP Session Setup) | Complete ordering |

### LO2: Explain endianness mechanisms

| Artifact | Location | Verification |
|----------|----------|--------------|
| Theory | `docs/theory_summary.md` §Endianness | Read and understand |
| Exercise | `ex_9_01_demonstrate_endianness.py` | Run `--demo --selftest` |
| Quiz | q03, q04, q05 | `python formative/run_quiz.py --lo LO2` |
| Misconception | #5 "My computer uses big-endian" | Review docs/misconceptions.md |
| Peer Instruction | Question 1 | Classroom activity |
| Parsons | P1 (Pack Network Message) | Complete ordering |
| Code Tracing | T1, T2 | Complete tables |

### LO3: Implement binary framing

| Artifact | Location | Verification |
|----------|----------|--------------|
| Theory | `docs/theory_summary.md` §Protocol Header | Read and understand |
| Exercise | `ex_9_01_demonstrate_endianness.py` | Implement framing |
| Homework | `hw_9_01_binary_fragmentation.py` | Complete homework |
| Quiz | q06, q07 | `python formative/run_quiz.py --lo LO3` |
| Misconception | #7 "struct.pack preserves boundaries" | Review docs/misconceptions.md |
| Parsons | P1 (Pack Network Message) | Complete ordering |
| Code Tracing | T2 | Complete table |

### LO4: Demonstrate FTP sessions

| Artifact | Location | Verification |
|----------|----------|--------------|
| Theory | `docs/theory_summary.md` §FTP | Read and understand |
| Exercise | `ex_9_03_ftp_client_demo.py` | Connect to FTP server |
| Exercise | `ex_9_04_ftp_server_demo.py` | Start local server |
| Docker | `docker/docker-compose.yml` | `make start` |
| Quiz | q08, q09 | `python formative/run_quiz.py --lo LO4` |
| Misconception | #2 "FTP uses one connection" | Review docs/misconceptions.md |
| Peer Instruction | Question 2 | Classroom activity |
| Parsons | P2, P4 | Complete ordering |

### LO5: Analyse packet captures

| Artifact | Location | Verification |
|----------|----------|--------------|
| Theory | `docs/theory_summary.md` §Packet Analysis | Read and understand |
| Script | `scripts/capture_traffic.py` | Capture FTP traffic |
| Wireshark | Native Windows app | Filter: `tcp.port == 2121` |
| Quiz | q10, q13 | `python formative/run_quiz.py --lo LO5` |
| Peer Instruction | Question 8 | Classroom activity |
| Parsons | P5 (Wireshark Filter) | Complete filter |

### LO6: Design checkpoint-recovery

| Artifact | Location | Verification |
|----------|----------|--------------|
| Theory | `docs/theory_summary.md` §Checkpoints | Read and understand |
| Exercise | `ex_9_02_implement_pseudo_ftp.py` | Review state machine |
| Homework | `hw_9_02_checkpoint_recovery.py` | Complete homework |
| Quiz | q11, q12, q14, q15 | `python formative/run_quiz.py --lo LO6` |
| Misconception | #4 "Session survives reconnect" | Review docs/misconceptions.md |
| Parsons | P3 (Checkpoint State Machine) | Complete ordering |

---

## Verification Commands

```bash
# Run formative quiz filtered by LO
python formative/run_quiz.py --lo LO1 --stats
python formative/run_quiz.py --lo LO2 --stats
python formative/run_quiz.py --lo LO3 --stats
python formative/run_quiz.py --lo LO4 --stats
python formative/run_quiz.py --lo LO5 --stats
python formative/run_quiz.py --lo LO6 --stats

# Run all tests
make test

# Run specific exercise selftests
python src/exercises/ex_9_01_demonstrate_endianness.py --selftest
python src/exercises/ex_9_02_implement_pseudo_ftp.py --selftest

# Validate quiz structure
python formative/run_quiz.py --validate
```

---

## Self-Assessment Checklist

After completing Week 9, you should be able to:

- [ ] **LO1:** Explain why FTP session state is lost when TCP reconnects
- [ ] **LO2:** Convert a 32-bit integer to network byte order using struct.pack
- [ ] **LO3:** Design a protocol header with magic bytes, length field and CRC
- [ ] **LO4:** Start Docker environment and observe FTP control/data channels
- [ ] **LO5:** Capture FTP traffic with tcpdump/Wireshark and identify packets
- [ ] **LO6:** Describe checkpoint-based recovery and implement a basic scheme

---

## Bloom Taxonomy Distribution

| Level | Questions | Target | Actual |
|-------|-----------|--------|--------|
| Remember | q01, q03 | 10-15% | 13% |
| Understand | q02, q04, q08, q11 | 20-25% | 27% |
| Apply | q05, q06, q07, q09, q10, q12 | 30-35% | 40% |
| Analyse | q13 | 15-20% | 7% |
| Evaluate | q15 | 5-10% | 7% |
| Create | q14 | 5-10% | 7% |

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Week 9: Session Layer and Presentation Layer*
*Last updated: 2026-01-25*
