# Learning Objectives Traceability Matrix — Week 3

> NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim

## Learning Objectives Summary

| ID | Description | Bloom Level |
|----|-------------|-------------|
| **LO1** | Recall unicast/broadcast/multicast differences and socket options | Remember |
| **LO2** | Explain broadcast L2 constraints, multicast IGMP and TTL | Understand |
| **LO3** | Implement UDP broadcast/multicast using Python sockets | Apply |
| **LO4** | Construct a TCP tunnel with bidirectional forwarding | Apply |
| **LO5** | Analyse captured traffic (UDP, IGMP, TCP handshakes) | Analyse |
| **LO6** | Evaluate appropriateness of communication modes | Evaluate |

## Traceability Matrix

### LO1: Recall Communication Modes
- README.md (theory section)
- docs/theory_summary.md
- docs/glossary.md
- src/exercises/ex_3_01_udp_broadcast.py
- formative/quiz.yaml (Q01-Q04)
- docs/misconceptions.md (#1, #2, #6)
- **Coverage: 11/10** ✅

### LO2: Explain L2 Constraints and IGMP
- README.md (broadcast vs multicast)
- docs/theory_summary.md
- src/exercises/ex_3_02_udp_multicast.py
- formative/quiz.yaml (Q05-Q08)
- docs/misconceptions.md (#1, #4, #5)
- docs/images/broadcast_vs_multicast.svg
- **Coverage: 12/10** ✅

### LO3: Implement UDP Broadcast/Multicast
- src/exercises/ex_3_01_udp_broadcast.py
- src/exercises/ex_3_02_udp_multicast.py
- homework/exercises/hw_3_01_broadcast_statistics.py
- homework/exercises/hw_3_02_multicast_chat.py
- formative/quiz.yaml (Q09-Q10)
- docs/parsons_problems.md (P1-P3)
- **Coverage: 11/10** ✅

### LO4: Construct TCP Tunnel
- src/exercises/ex_3_03_tcp_tunnel.py
- src/apps/tcp_tunnel.py
- homework/exercises/hw_3_03_tunnel_logging.py
- formative/quiz.yaml (Q11-Q12)
- docs/misconceptions.md (#7, #8)
- docs/parsons_problems.md (P4-P5)
- docs/images/tcp_tunnel_architecture.svg
- **Coverage: 13/10** ✅

### LO5: Analyse Captured Traffic
- README.md (Wireshark section)
- scripts/capture_traffic.py
- pcap/README.md
- formative/quiz.yaml (Q13-Q14)
- tests/expected_outputs.py
- **Coverage: 10/10** ✅

### LO6: Evaluate Communication Mode Appropriateness
- docs/case_study_communication_modes.md
- docs/concept_analogies.md
- formative/quiz.yaml (Q15-Q17)
- docs/peer_instruction.md
- **Coverage: 10/10** ✅

## Overall Coverage: 67/30 = 223% ✅

---
*Week 3: Network Programming — Broadcast, Multicast and TCP Tunnelling*
