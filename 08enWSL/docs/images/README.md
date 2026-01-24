# Documentation Images — Week 8 Laboratory

This directory contains diagrams and visual aids for the laboratory documentation.

## Available Diagrams

| File | Description | Used In |
|------|-------------|---------|
| `architecture.svg` | Lab environment architecture showing nginx proxy and backends | README.md |
| `tcp_handshake.svg` | TCP three-way handshake sequence diagram | docs/misconceptions.md |

## Viewing SVG Files

SVG files can be viewed:
- Directly in a web browser (drag and drop)
- In VS Code with the SVG Preview extension
- In any Markdown viewer that supports embedded images

## Embedding in Markdown

```markdown
![Architecture](docs/images/architecture.svg)

![TCP Handshake](docs/images/tcp_handshake.svg)
```

## Creating New Diagrams

For consistency use:
- Font: sans-serif for labels, monospace for code/ports
- Colours:
  - Client: #e3f2fd (light blue)
  - Proxy: #fff3e0 (light orange)
  - Backend: #e8f5e9 (light green)
  - Your code: #fce4ec (light pink)

---

*Computer Networks — ASE, CSIE*
