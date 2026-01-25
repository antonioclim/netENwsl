# Documentation Images — Week 4

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

This folder contains visual diagrams supporting Week 4 laboratory materials.

## Available Diagrams

### Protocol Structure Diagrams

| File | Description | Used In |
|------|-------------|---------|
| `binary_header_structure.svg` | 14-byte binary protocol header layout | README.md, theory_summary.md |
| `text_framing.svg` | Length-prefix framing for TEXT protocol | misconceptions.md, theory_summary.md |
| `udp_sensor_datagram.svg` | 23-byte UDP sensor datagram structure | exercises, expected_outputs.md |

### Conceptual Diagrams

| File | Description | Used In |
|------|-------------|---------|
| `protocol_stack.svg` | Week 4 protocol stack overview (OSI layers) | concept_analogies.md, README.md |
| `tcp_no_boundaries.svg` | TCP stream misconception (no message boundaries) | misconceptions.md, peer_instruction.md |
| `endianness.svg` | Big-endian vs little-endian byte order | code_tracing.md, misconceptions.md |
| `tcp_handshake.svg` | TCP 3-way handshake sequence | theory_summary.md |

### Process Flow Diagrams

| File | Description | Used In |
|------|-------------|---------|
| `struct_pack_flow.svg` | Python struct.pack() workflow | code_tracing.md, exercises |
| `crc32_verification.svg` | CRC32 integrity check process | peer_instruction.md, exercises |
| `crc32_flow.svg` | CRC32 calculation steps | theory_summary.md |

### Environment Diagrams

| File | Description | Used In |
|------|-------------|---------|
| `lab_architecture.svg` | WSL2 + Docker + Portainer setup | README.md, troubleshooting.md |

## Diagram Conventions

- **Blue** (#3498db): Data fields, sender components
- **Green** (#2ecc71): Header/control fields, receiver components, success states
- **Orange** (#e67e22): CRC/checksum fields, format strings
- **Red** (#e74c3c): Error states, little-endian (when contrasting)
- **Purple** (#9b59b6): Special/delimiter fields
- **Grey** (#95a5a6): Optional/variable fields, network/wire

## Usage in Markdown

Reference diagrams in documentation:

```markdown
![Binary Header Structure](images/binary_header_structure.svg)

See the [protocol stack diagram](images/protocol_stack.svg) for layer overview.
```

## Regenerating Diagrams

These diagrams are SVG (XML-based vector graphics). To modify:

1. Edit the `.svg` file directly (any text editor)
2. Or use vector graphics tools:
   - Inkscape (free, open source)
   - Figma (web-based)
   - Adobe Illustrator

### Design Guidelines

- Maximum width: 700px for full-width diagrams
- Font: Sans-serif for labels, Monospace for code
- Keep text readable at 50% zoom
- Use consistent colour palette (see conventions above)
- Include legends for complex diagrams

## File Sizes

All diagrams are optimised SVG files under 5KB each for fast loading.

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Version 1.6.0 — Last updated: 2026-01-25*
