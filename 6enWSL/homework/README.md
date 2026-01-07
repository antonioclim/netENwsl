# Week 6 Homework Assignments

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by Revolvix

## Overview

These homework exercises extend the concepts explored during the laboratory session on NAT/PAT and Software-Defined Networking. Complete these assignments to consolidate your understanding of network address translation mechanisms and OpenFlow-based traffic policies.

---

## Assignment 1: Extended NAT Analysis

**Objective:** Analyse the behaviour of NAT translations under various traffic patterns.

**Tasks:**

1. Modify `topo_nat.py` to add a fourth host (h4) on the private network with IP 192.168.1.40/24
2. Generate simultaneous TCP connections from h1, h2, and h4 to h3 using `nat_observer.py`
3. Capture the traffic on rnat-eth1 (public interface) using tcpdump
4. Document the PAT translation table entries observed

**Deliverables:**
- Modified topology file
- Packet capture (PCAP) showing translations
- Written analysis (300-500 words) explaining observed behaviour

**Evaluation Criteria:**
- Correct topology modification (25%)
- Complete packet capture (25%)
- Accurate analysis of PAT behaviour (50%)

---

## Assignment 2: SDN Policy Implementation

**Objective:** Design and implement custom OpenFlow policies using OS-Ken.

**Tasks:**

1. Extend the SDN topology to include a fourth host (h4: 10.0.6.14/24)
2. Implement the following policy rules:
   - h1 ↔ h2: PERMIT all traffic
   - h1 ↔ h3: PERMIT ICMP only, DROP TCP/UDP
   - h1 → h4: PERMIT TCP port 80 only
   - h4 → h1: DROP all traffic (asymmetric policy)
3. Test each policy with appropriate traffic generators

**Deliverables:**
- Modified topology file with h4
- Updated controller with new policies
- Test script demonstrating each policy
- Documentation of flow table entries

**Evaluation Criteria:**
- Correct topology extension (20%)
- Policy implementation accuracy (40%)
- Comprehensive testing (25%)
- Documentation quality (15%)

---

## Assignment 3: Comparative Analysis

**Objective:** Compare traditional NAT with SDN-based approaches to network address management.

**Tasks:**

1. Research and document at least three SDN-based alternatives to traditional NAT
2. Implement a simple example of one alternative using Mininet/OS-Ken
3. Compare performance and complexity metrics

**Deliverables:**
- Research document (800-1000 words)
- Working implementation
- Comparison table with metrics

**Evaluation Criteria:**
- Research depth and accuracy (35%)
- Implementation functionality (40%)
- Analysis quality (25%)

---

## Submission Guidelines

- Submit all files as a single ZIP archive named `hw6_<student_id>.zip`
- Include a `README.txt` with your name, student ID, and any special instructions
- Ensure all Python files have valid syntax before submission
- Include packet captures in PCAP format (not screenshots)

**Deadline:** Consult the course schedule on the university portal

---

## Resources

- Course slides: NAT/PAT and SDN Components
- Laboratory guide: Week 6 documentation
- RFC 3022: Traditional IP Network Address Translator (Traditional NAT)
- OpenFlow Specification 1.3.5

---

*NETWORKING class - ASE, Informatics | by Revolvix*
