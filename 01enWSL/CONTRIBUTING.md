# 🤝 Contributing to netENwsl Week 1
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## For Students

### Reporting Issues

Before reporting an issue:

1. **Check existing documentation first:**
   - `docs/troubleshooting.md` — Decision tree for common problems
   - `docs/misconceptions.md` — Common misunderstandings
   - `README.md` — Setup instructions

2. **Run diagnostics:**
   ```bash
   python tests/smoke_test.py
   python setup/verify_environment.py
   ```

3. **Include in your report:**
   - Operating system and version
   - Docker version (`docker --version`)
   - Python version (`python --version`)
   - Complete error message
   - Steps to reproduce

### Suggesting Improvements

- Open an issue with `[SUGGESTION]` prefix
- Include:
  - What you're trying to accomplish
  - Why current approach doesn't work
  - Proposed solution (if you have one)
  - Examples from your experience

---

## For Instructors

### Adding Exercises

Follow this pattern for new exercises:

1. **Naming Convention:**
   ```
   src/exercises/ex_N_MM_description.py
   ```
   - `N` = Week number (1-14)
   - `MM` = Exercise number within week (01, 02, ...)
   - `description` = Brief snake_case description

2. **Required Structure:**
   ```python
   #!/usr/bin/env python3
   """
   Exercise N.MM: Title
   ====================
   Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim
   
   **Objectives:**
   - LO1: First learning objective
   - LO2: Second learning objective
   
   **Prerequisites:**
   - Completed exercises N.01 through N.MM-1
   - Docker environment running
   
   **Pair Programming Notes:**
   - Driver: Types code, explains reasoning
   - Navigator: Reviews, suggests improvements
   - Switch roles every 15 minutes
   
   **Estimated Time:** XX minutes
   **Difficulty Level:** Basic/Intermediate/Advanced
   """
   
   # SETUP_ENVIRONMENT section
   # DATA_STRUCTURES section (dataclasses)
   # PREDICTION_PROMPT function
   # EXECUTE function
   # PARSE_OUTPUT function
   # OUTPUT_RESULTS with interpretation
   # MAIN orchestration
   ```

3. **Add Corresponding Test:**
   ```python
   # In tests/test_exercises.py
   def test_exercise_MM():
       """Test ex_N_MM functionality."""
       pass
   ```

4. **Update Traceability:**
   - Add entry to `docs/learning_objectives.md`
   - Link from relevant sections

### Adding Quiz Questions

1. **Edit `formative/quiz.yaml`:**
   ```yaml
   - id: qNN  # Sequential ID
     type: multiple_choice  # or fill_blank, true_false, etc.
     lo_ref: LOX  # Learning objective reference
     bloom_level: understand  # remember, understand, apply, analyze, evaluate, create
     difficulty: intermediate
     points: 2
     stem: "Question text here"
     options:
       a: "Option A"
       b: "Option B"
       c: "Option C"
       d: "Option D"
     correct: b
     explanation: "Why B is correct"
     misconception_ref: "docs/misconceptions.md#misconception-X"
   ```

2. **Add to Section:**
   ```yaml
   sections:
     - id: during_lab
       questions: [q06, q07, q08, q09, q10, qNN]  # Add new ID
   ```

3. **Validate:**
   ```bash
   python formative/run_quiz.py --list-sections
   make quiz-validate
   ```

### Adding Misconceptions

Follow the pattern in `docs/misconceptions.md`:

```markdown
## Misconception N: Title

### The Wrong Mental Model

Students believe: [incorrect understanding]

### The Correct Understanding

Actually: [correct explanation]

### Why This Matters

[Practical implications]

### Verification Commands

```bash
# Commands to prove the correct understanding
```

### Related

- Quiz: qXX
- Exercise: ex_N_MM
- LO: LOX
```

### Adding Parsons Problems

Follow the pattern in `docs/parsons_problems.md`:

```markdown
## Problem PN: Title

### Learning Objective
LOX: [Objective description]

### Scrambled Code
[Shuffled lines with distractors marked]

### Distractor Analysis
- Line X: [Why it's wrong]

### Solution
[Correctly ordered code]

### Explanation
[Why this order is correct]
```

---

## Code Quality Standards

### Python Style

- **Formatter:** ruff
- **Type hints:** Required for all function signatures
- **Docstrings:** Required for all public functions
- **Line length:** 100 characters maximum

Run before committing:
```bash
make lint
make format
```

### Documentation Style

- **Headers:** Use emoji prefixes (📝, 🔍, 🎯, etc.)
- **Code blocks:** Always specify language
- **Tables:** Align columns for readability
- **Links:** Use relative paths within repository

### Commit Messages

```
type(scope): subject

body (optional)

footer (optional)
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
```
feat(quiz): add code tracing questions for LO2
docs(misconceptions): add #12 about UDP reliability
fix(ex_1_02): handle connection timeout gracefully
```

---

## Testing

### Running Tests

```bash
# All tests
make test

# Quick smoke test
make smoke

# Specific test file
python -m pytest tests/test_exercises.py -v

# With coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Writing Tests

```python
import pytest

def test_feature_name():
    """Test description linking to LO."""
    # Arrange
    input_data = ...
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected
```

---

## Pull Request Checklist

Before submitting:

- [ ] Code passes `make lint`
- [ ] All tests pass `make test`
- [ ] Quiz validates `make quiz-validate`
- [ ] Documentation updated if needed
- [ ] Commit messages follow convention
- [ ] LO traceability matrix updated (if applicable)

---

## Questions?

- Check `docs/troubleshooting.md` first
- Review `docs/misconceptions.md` for common issues
- Contact: antonio.clim@example.com

---

*NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim*
