# Documentation Images — Week 14: Integration and Review

> **NETWORKING** Laboratory — ASE-CSIE, Bucharest
>
> by ing. dr. Antonio Clim

---

## Directory Purpose

This directory contains diagrams, screenshots and visual aids supporting Week 14 documentation. Images help illustrate the integration concepts covered in the final laboratory session.

---

## Directory Structure

```
images/
├── architecture/          # System and network architecture diagrams
│   ├── full_stack.png
│   └── container_network.png
├── screenshots/           # Portainer and Wireshark screenshots
│   ├── portainer_overview.png
│   └── wireshark_capture.png
├── diagrams/              # Protocol flow and sequence diagrams
│   ├── tcp_handshake.png
│   └── http_session.png
└── README.md              # This file
```

---

## Image Specifications

| Format | Recommended Use | Maximum Size |
|--------|-----------------|--------------|
| `.png` | Screenshots, diagrams with text | 500 KB |
| `.svg` | Vector diagrams (scalable) | 100 KB |
| `.jpg` | Photographs (if needed) | 300 KB |
| `.mermaid` | Source for generated diagrams | 10 KB |

---

## Adding New Images

### Workflow

1. Create the image using appropriate tools:
   - **draw.io** for architecture diagrams
   - **Mermaid** for sequence diagrams
   - **Screenshot tool** for application captures

2. Save with descriptive filename following the pattern:
   ```
   component_action_detail.png
   ```
   Examples: `tcp_three_way_handshake.png`, `portainer_container_list.png`

3. Optimise file size before adding to repository

4. Reference in documentation using relative paths:
   ```markdown
   ![TCP Handshake](images/diagrams/tcp_handshake.png)
   ```

---

## Current Image Inventory

| Filename | Description | Used In |
|----------|-------------|---------|
| *(Add entries as images are created)* | | |

---

## Image Creation Guidelines

### Visual Consistency

- Use Docker blue (#2496ED) for container elements
- Use network green (#28A745) for connectivity
- Use warning orange (#FFC107) for important notes
- Maintain consistent font sizes (minimum 12pt)

### Accessibility

- Include descriptive alt-text for all images
- Ensure sufficient colour contrast (WCAG 2.1 AA)
- Provide text alternatives for complex diagrams

### Quality Standards

- Verify text remains readable at 100% zoom
- Include legends for diagrams with multiple elements
- Crop screenshots to show only relevant areas

---

*Visual documentation enhances understanding — create images that clarify, not confuse.*
