# 📊 Diagrams — Week 2: Architectural Models and Socket Programming

> NETWORKING class — ASE, CSIE Bucharest  
> Computer Networks Laboratory | by ing. dr. Antonio Clim

This folder contains SVG diagrams for Week 2 laboratory materials.

---

## Available Diagrams

| Diagram | Description | Usage |
|---------|-------------|-------|
| `osi_tcpip_model.svg` | OSI 7-layer vs TCP/IP 4-layer model comparison | Theory introduction |
| `tcp_handshake.svg` | TCP three-way handshake sequence diagram | Before Exercise 1 |
| `tcp_vs_udp.svg` | TCP and UDP characteristics comparison | Protocol selection |
| `socket_api_flow.svg` | Socket API call sequence for TCP and UDP | Coding reference |

---

## Diagram Previews

### 1. OSI vs TCP/IP Model (`osi_tcpip_model.svg`)

Shows the mapping between the 7-layer OSI reference model and the 4-layer TCP/IP practical model:
- Layer mapping (which OSI layers combine in TCP/IP)
- Protocol examples at each layer
- PDU (Protocol Data Unit) names

**Use in class:** When introducing architectural models in theory section.

---

### 2. TCP Three-Way Handshake (`tcp_handshake.svg`)

Illustrates the connection establishment sequence:
- SYN → SYN-ACK → ACK packet exchange
- Client and server state transitions
- Socket API correlation (connect/accept)

**Use in class:** Before running Exercise 1, to predict Wireshark output.

---

### 3. TCP vs UDP Comparison (`tcp_vs_udp.svg`)

Side-by-side comparison of transport protocols:
- Characteristics (reliable, ordered, overhead)
- Use cases for each protocol
- Packet count comparison

**Use in class:** When discussing protocol selection for applications.

---

### 4. Socket API Flow (`socket_api_flow.svg`)

Shows the sequence of socket API calls:
- TCP server/client call sequence
- UDP server/client call sequence
- Blocking points highlighted
- Key differences noted

**Use in class:** As coding reference during exercises.

---

## How to Use

### In Markdown Documents

```markdown
![OSI vs TCP/IP Model](docs/images/osi_tcpip_model.svg)
```

### In HTML

```html
<img src="docs/images/osi_tcpip_model.svg" alt="OSI vs TCP/IP Model" width="700">
```

### In Presentations

SVG files can be:
- Embedded directly in HTML-based presentations
- Converted to PNG for PowerPoint (use browser screenshot or Inkscape)
- Opened and edited in Inkscape or Adobe Illustrator

---

## Colour Scheme

| Colour | Hex | Usage |
|--------|-----|-------|
| Blue | `#3498db` | TCP, Application layer |
| Orange | `#e67e22` | UDP |
| Green | `#2ecc71` | Success, data transfer, Transport layer |
| Purple | `#9b59b6` | Blocking operations, Session/Presentation |
| Red | `#e74c3c` | Errors, SYN flag, Application layer |
| Yellow | `#f39c12` | Network layer |
| Teal | `#1abc9c` | Data Link layer |
| Grey | `#95a5a6` | Physical layer, neutral |

---

## Editing Diagrams

These SVG files can be edited with:
- **Inkscape** (free, open source) — recommended
- **Adobe Illustrator**
- Any text editor (SVG is XML-based)

When editing:
1. Maintain the colour scheme for consistency
2. Keep font family as Arial for cross-platform compatibility
3. Update the version number in the footer if making significant changes

---

## File Sizes

| File | Size | Complexity |
|------|------|------------|
| `osi_tcpip_model.svg` | ~5 KB | Medium |
| `tcp_handshake.svg` | ~4 KB | Simple |
| `tcp_vs_udp.svg` | ~5 KB | Medium |
| `socket_api_flow.svg` | ~6 KB | Complex |

All files are optimised for web display and print.

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
