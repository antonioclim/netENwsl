# 📊 Visual Learning Resources — Week 2

> NETWORKING class — ASE, CSIE Bucharest  
> Computer Networks Laboratory | by ing. dr. Antonio Clim

---

## Overview

This directory contains SVG diagrams designed to support visual learning for Week 2 concepts. All diagrams are vector-based (SVG) for crisp rendering at any scale.

---

## Available Diagrams

| File | Description | Related LOs |
|------|-------------|-------------|
| `tcp_handshake.svg` | TCP three-way handshake sequence | U2, U5 |
| `tcp_vs_udp.svg` | Comparison of TCP and UDP features | U1, U4, E1 |
| `osi_tcpip_model.svg` | OSI 7-layer vs TCP/IP 4-layer models | R1, R2 |

---

## Diagram Details

### 1. TCP Three-Way Handshake (`tcp_handshake.svg`)

**Purpose:** Visualise the TCP connection establishment process.

**Key Elements:**
- Client and server timelines
- SYN, SYN-ACK and ACK packets
- Sequence number progression
- State transitions (SYN_SENT, SYN_RECEIVED, ESTABLISHED)

**When to Use:**
- Explaining TCP connection setup
- Before Wireshark capture exercises
- Peer instruction Q4

**Correlation with Lab:**
- Exercise 1: Observe in Wireshark after running TCP server/client
- PCAP: `pcap/week02_tcp_handshake_echo.pcap`

---

### 2. TCP vs UDP Comparison (`tcp_vs_udp.svg`)

**Purpose:** Side-by-side comparison of the two transport protocols.

**Key Elements:**
- Connection characteristics
- Reliability features
- Ordering guarantees
- Use case examples
- Header size comparison

**When to Use:**
- Introducing transport layer concepts
- Protocol selection discussions
- Peer instruction Q5

**Correlation with Lab:**
- Exercise 1 (TCP) vs Exercise 2 (UDP)
- Quiz questions q06, q08, q15

---

### 3. OSI vs TCP/IP Model (`osi_tcpip_model.svg`)

**Purpose:** Compare the two networking reference models.

**Key Elements:**
- All 7 OSI layers with examples
- 4 TCP/IP layers with mapping
- Layer-to-layer correspondence
- PDU (Protocol Data Unit) names
- Week 2 focus indicator (Transport Layer)

**When to Use:**
- Course introduction
- Layer identification exercises
- Quiz questions q01, q03, q05

**Correlation with Lab:**
- Theory summary in `docs/theory_summary.md`
- Wireshark layer inspection

---

## Usage Guidelines

### In Presentations

```html
<!-- Embed in HTML slides -->
<img src="docs/images/tcp_handshake.svg" alt="TCP Handshake" width="600">
```

### In Markdown Documents

```markdown
![TCP vs UDP Comparison](docs/images/tcp_vs_udp.svg)
```

### Printing

SVG files can be converted to PDF for high-quality printing:

```bash
# Using Inkscape (if installed)
inkscape tcp_handshake.svg --export-pdf=tcp_handshake.pdf

# Using rsvg-convert (if installed)
rsvg-convert -f pdf -o tcp_handshake.pdf tcp_handshake.svg
```

---

## Diagram Conventions

### Colour Coding

| Colour | Meaning |
|--------|---------|
| Blue (#1976d2, #4a90d9) | TCP-related, Client |
| Green (#4caf50, #5cb85c) | Server, Success, Established |
| Orange (#f57c00, #f39c12) | UDP-related, Warning |
| Red (#e74c3c) | SYN packets, Errors |

### Typography

- **Titles:** Arial/sans-serif, 16-20px, bold
- **Labels:** Arial/sans-serif, 12-14px
- **Notes:** Arial/sans-serif, 10-11px, grey

---

## Contributing New Diagrams

When adding new diagrams:

1. **Format:** Use SVG for scalability
2. **Size:** Viewbox ~500-600px width for consistency
3. **Colours:** Follow the colour coding above
4. **Footer:** Include "Week X — Topic | NETWORKING class"
5. **Naming:** Use `lowercase_with_underscores.svg`

### Template Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- Diagram Title -->
<!-- NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 400" width="500" height="400">
  <!-- Background -->
  <rect width="500" height="400" fill="#fafafa"/>
  
  <!-- Title -->
  <text x="250" y="30" text-anchor="middle" ...>Title</text>
  
  <!-- Content here -->
  
  <!-- Footer -->
  <text x="250" y="385" text-anchor="middle" ...>Week X — Topic | NETWORKING class</text>
</svg>
```

---

## Related Resources

| Resource | Location |
|----------|----------|
| Theory Summary | `docs/theory_summary.md` |
| PCAP Guide | `pcap/PCAP_ANALYSIS_GUIDE.md` |
| Peer Instruction | `docs/peer_instruction.md` |
| Quiz | `formative/quiz.yaml` |

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
