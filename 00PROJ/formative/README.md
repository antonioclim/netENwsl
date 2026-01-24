# Formative Assessment System

> **Purpose:** Self-assessment tools for Computer Networks projects  
> **Formats:** YAML (Python runnable) + JSON (LMS export)  
> **Course:** Computer Networks, ASE Bucharest - CSIE

---

## Overview

This directory contains formative assessment materials to help you evaluate your understanding of project concepts before submission. The system supports:

- **Interactive quizzes** with immediate feedback
- **Parsons problems** for code ordering practice
- **LMS export** for Moodle and Canvas integration

---

## Quick Start

### Run a Quiz

```bash
# Run the default quiz
python run_quiz.py quiz_template.yaml

# Practice mode (shows hints)
python run_quiz.py quiz_template.yaml --practice

# Filter by Learning Objective
python run_quiz.py quiz_template.yaml --lo LO2

# Randomise question order
python run_quiz.py quiz_template.yaml --random

# Limit number of questions
python run_quiz.py quiz_template.yaml --limit 5
```

### List Available Quizzes

```bash
python run_quiz.py --list
```

### Export to LMS

```bash
# Export to Moodle XML
python export_lms.py quiz_template.yaml --format moodle

# Export to Canvas QTI
python export_lms.py quiz_template.yaml --format canvas

# Export to generic JSON
python export_lms.py quiz_template.yaml --format json

# Export all quizzes
python export_lms.py --all --format moodle
```

---

## Directory Structure

```
formative/
├── README.md              # This file
├── run_quiz.py            # Quiz runner script
├── export_lms.py          # LMS export script
├── quiz_template.yaml     # Master quiz template with P01 example
├── parsons/
│   └── parsons_problems.json   # Code ordering exercises
├── results/               # Quiz results (auto-created)
│   └── *.json            # Individual attempt records
└── exports/               # LMS exports (auto-created)
    ├── *_moodle.xml      # Moodle format
    ├── *_canvas.xml      # Canvas QTI format
    └── *.json            # Generic JSON format
```

---

## Quiz File Format

Quiz files use YAML format with the following structure:

```yaml
metadata:
  version: "1.0"
  course: "Computer Networks"
  passing_score: 70
  time_limit_minutes: 15

project:
  id: "P01"
  title: "SDN Firewall with Mininet"
  
  learning_objectives:
    - id: LO1
      description: "Explain SDN architecture"
      bloom_level: understand
  
  questions:
    - id: p01_q01
      type: multiple_choice
      lo_ref: LO1
      bloom_level: understand
      difficulty: basic
      points: 1
      stem: "Question text here"
      options:
        a: "Option A"
        b: "Option B"
        c: "Option C"
        d: "Option D"
      correct: b
      feedback:
        correct: "Feedback for correct answer"
        incorrect: "Feedback for incorrect answer"
      explanation: "Detailed explanation"
```

### Supported Question Types

| Type | Description | Example Use |
|------|-------------|-------------|
| `multiple_choice` | Single correct answer | Concept understanding |
| `multiple_select` | Multiple correct answers | Identify all that apply |
| `fill_blank` | Text input | Technical terms |
| `code_trace` | Predict code output | Debugging skills |
| `scenario` | Real-world problem | Applied knowledge |
| `ordering` | Arrange in sequence | Process understanding |
| `matching` | Match pairs | Concept mapping |

---

## Parsons Problems

Parsons problems are code ordering exercises where you arrange scrambled code blocks into the correct sequence. They include **distractors** (incorrect code lines) to test deeper understanding.

### File Format (JSON)

```json
{
  "problems": [
    {
      "id": "parsons_001",
      "title": "Install OpenFlow Drop Rule",
      "instructions": "Arrange the code lines...",
      "blocks": [
        {"id": 1, "code": "msg = of.ofp_flow_mod()", "is_distractor": false},
        {"id": 2, "code": "msg.action = 'DROP'", "is_distractor": true}
      ],
      "correct_order": [1, 3, 4],
      "explanation": "Explanation of the solution"
    }
  ]
}
```

---

## Grading and Feedback

### Score Calculation

- Each question has a point value (default: 1)
- Total score = sum of correct answers × point values
- Percentage = (earned / possible) × 100

### Grade Bands

| Range | Label | Meaning |
|-------|-------|---------|
| 90-100% | Excellent | Outstanding understanding |
| 80-89% | Very Good | Strong grasp with minor gaps |
| 70-79% | Satisfactory | Adequate understanding |
| 60-69% | Needs Improvement | Significant gaps |
| 0-59% | Unsatisfactory | Major review needed |

### Learning Objective Tracking

Quiz results include a breakdown by Learning Objective:

```
📈 Learning Objective Breakdown:
  LO1: [██████████] 100% ✓
  LO2: [████████░░] 80% ✓
  LO3: [██████░░░░] 60% ✗

⚠️ Areas Needing Review: LO3 (60%)
```

---

## Results and Progress Tracking

Quiz results are automatically saved to `results/` as JSON files:

```json
{
  "project_id": "P01",
  "timestamp": "2026-01-24T14:30:00",
  "score_percentage": 85.0,
  "passed": true,
  "lo_breakdown": {
    "LO1": {"correct": 3, "total": 3},
    "LO2": {"correct": 2, "total": 3}
  },
  "weak_areas": ["LO3"],
  "recommendations": ["Review LO3: Configure virtual network topologies"]
}
```

---

## LMS Integration

### Moodle Import

1. Export quiz: `python export_lms.py quiz_p01.yaml --format moodle`
2. In Moodle, go to **Question bank** → **Import**
3. Select format: **Moodle XML format**
4. Upload the `*_moodle.xml` file

### Canvas Import

1. Export quiz: `python export_lms.py quiz_p01.yaml --format canvas`
2. In Canvas, go to **Settings** → **Import Course Content**
3. Select content type: **QTI .zip file**
4. Upload the `*_canvas.xml` file

---

## Creating New Quizzes

### Step 1: Copy Template

```bash
cp quiz_template.yaml quiz_p12.yaml
```

### Step 2: Edit Metadata

Update the project section:

```yaml
project:
  id: "P12"
  title: "Docker Microservices with Load Balancing"
  description: "Self-assessment for load balancing project"
```

### Step 3: Define Learning Objectives

List all LOs from your project specification:

```yaml
  learning_objectives:
    - id: LO1
      description: "Implement load balancing algorithms"
      bloom_level: apply
```

### Step 4: Add Questions

Ensure 2-3 questions per LO:

```yaml
  questions:
    - id: p12_q01
      type: multiple_choice
      lo_ref: LO1
      # ... rest of question
```

### Step 5: Validate

```bash
python run_quiz.py quiz_p12.yaml --limit 1
```

---

## Best Practices

### For Students

1. **Take quizzes before submission** to identify knowledge gaps
2. **Review weak areas** using theory materials
3. **Retry in practice mode** to see hints and explanations
4. **Track your progress** over multiple attempts

### For Instructors

1. **Ensure LO coverage** — each LO should have 2-3 questions
2. **Include distractors** in Parsons problems for better assessment
3. **Provide detailed explanations** for learning value
4. **Export to LMS** for formal formative assessments

---

## Troubleshooting

### Quiz Won't Load

```bash
# Check YAML syntax
python -c "import yaml; yaml.safe_load(open('quiz_p01.yaml'))"
```

### Missing Dependencies

```bash
pip install pyyaml
```

### Export Fails

Ensure the `exports/` directory exists or will be created automatically.

---

## Requirements

- Python 3.10+
- PyYAML (`pip install pyyaml`)

---

*Formative Assessment System v1.0*  
*Computer Networks — ASE Bucharest CSIE*
