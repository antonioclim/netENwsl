# 🧩 Parsons Problems — Formative Assessment
## Computer Networks Projects — ASE Bucharest, CSIE

> **Purpose:** Code reordering exercises to build understanding without syntax burden.  
> **Method:** Students arrange scrambled code blocks into correct order.

---

## What Are Parsons Problems?

Parsons problems present code blocks in random order. Your task is to arrange them correctly. This tests your understanding of:

- Logical sequence of operations
- Code structure and flow
- Common patterns without typing

Research shows Parsons problems are highly effective for learning programming concepts with lower cognitive load than writing from scratch.

---

## How to Use

### Interactive Mode (recommended)

```bash
python run_quiz.py quiz_template.yaml --type parsons
```

### Paper-Based

Print problems from `parsons_problems.json` and solve on paper before checking.

---

## Problem Format

Each problem in `parsons_problems.json` follows this structure:

```json
{
  "id": "parsons_001",
  "project": "P01",
  "lo_ref": "LO2",
  "title": "OpenFlow Drop Rule",
  "description": "Arrange blocks to create a flow rule that drops packets",
  "blocks": [
    {"id": "A", "code": "match = parser.OFPMatch(eth_type=0x0800)", "indent": 0},
    {"id": "B", "code": "actions = []  # Empty actions = drop", "indent": 0},
    {"id": "C", "code": "inst = [parser.OFPInstructionActions(...)]", "indent": 0},
    {"id": "D", "code": "mod = parser.OFPFlowMod(...)", "indent": 0},
    {"id": "E", "code": "datapath.send_msg(mod)", "indent": 0}
  ],
  "correct_order": ["A", "B", "C", "D", "E"],
  "distractors": [
    {"id": "X", "code": "actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]", "reason": "This floods, not drops"}
  ]
}
```

### Fields Explained

| Field | Description |
|-------|-------------|
| `blocks` | Code fragments to arrange |
| `correct_order` | Correct sequence of block IDs |
| `distractors` | Extra blocks that should NOT be included |
| `indent` | Indentation level (0 = no indent, 1 = one level) |

---

## Available Problems

| ID | Project | Topic | Difficulty |
|----|---------|-------|------------|
| parsons_001 | P01 | OpenFlow drop rule | ★★☆ |
| parsons_002 | P08 | TCP server socket setup | ★★☆ |
| parsons_003 | P10 | Docker Compose service | ★☆☆ |
| parsons_004 | P13 | gRPC server implementation | ★★★ |
| parsons_005 | P15 | MQTT publish with QoS | ★★☆ |

---

## Tips for Solving

1. **Identify the goal** — What should the code accomplish?
2. **Find the start** — Imports, setup, or function definition
3. **Find the end** — Return statement, send, or cleanup
4. **Trace dependencies** — Which variables must exist before use?
5. **Watch for distractors** — Some blocks don't belong

---

## Creating New Problems

When adding problems for your project:

1. Choose a key code snippet (10-20 lines)
2. Split into logical blocks (4-8 blocks ideal)
3. Add 1-2 plausible distractors
4. Test that the correct order actually works
5. Add to `parsons_problems.json`

---

## Integration with Quiz System

Parsons problems can be mixed with other question types in quizzes:

```yaml
- id: p01_parsons_01
  type: ordering
  lo_ref: LO2
  bloom_level: apply
  stem: "Arrange these blocks to create an OpenFlow rule that drops all HTTP traffic"
  items:
    - "match = parser.OFPMatch(eth_type=0x0800, ip_proto=6, tcp_dst=80)"
    - "actions = []"
    - "inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]"
    - "mod = parser.OFPFlowMod(datapath=dp, priority=10, match=match, instructions=inst)"
    - "datapath.send_msg(mod)"
  correct_order: [0, 1, 2, 3, 4]
```

---

*Parsons Problems v1.0 — Computer Networks Projects*  
*ASE Bucharest, CSIE — January 2026*
