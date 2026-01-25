# Documentation Images

**Week 13: IoT and Security**

This directory contains visual assets for the Week 13 laboratory materials.

## Contents

| File | Description | Format |
|------|-------------|--------|
| `architecture_week13.md` | Mermaid diagram definitions | Markdown/Mermaid |

## Diagram Types

The architecture document includes:

1. **MQTT Pub/Sub Architecture** — Publisher, broker, subscriber relationships
2. **QoS Handshakes** — Sequence diagrams for QoS 0, 1, 2
3. **Lab Environment Topology** — Docker container network layout
4. **TLS Certificate Chain** — CA, server, and client certificate relationships
5. **OWASP IoT Distribution** — Pie chart of vulnerability categories
6. **Defence-in-Depth Layers** — Security layer hierarchy
7. **Exercise Workflow** — Dependencies between laboratory exercises

## Rendering

Diagrams are defined in Mermaid syntax and can be rendered via:

- GitHub Markdown preview (automatic)
- VS Code with Mermaid extension
- Mermaid Live Editor (https://mermaid.live/)
- PDF export via pandoc with mermaid-filter

## Export Commands

```bash
# Install Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# Export individual diagram to PNG
mmdc -i architecture_week13.md -o mqtt_architecture.png

# Export with custom theme
mmdc -i architecture_week13.md -o diagram.png -t dark
```

---

*Document version: 2.0 | Language: en-GB*
