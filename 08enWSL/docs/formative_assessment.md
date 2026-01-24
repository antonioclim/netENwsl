# 📊 Formative Assessment Guide — Week 8
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Formative assessment is about learning, not grading.
> Use these tools to identify what you understand and what needs more work.

---

## What is Formative Assessment?

Unlike summative assessment (exams, final grades), formative assessment helps you
**during** the learning process. It answers:

- "Do I understand this concept well enough?"
- "Which topics should I review before the exam?"
- "Where are my misconceptions?"

**Key principle:** There is no penalty for wrong answers. Every mistake is a
learning opportunity.

---

## Available Assessment Tools

### 1. Interactive Quiz (`make quiz`)

**Location:** `formative/quiz.yaml` + `formative/run_quiz.py`

A 15-question quiz covering all six Learning Objectives with immediate feedback.

```bash
# Full quiz
make quiz

# Or directly
python formative/run_quiz.py

# Specific options
python formative/run_quiz.py --random           # Randomise order
python formative/run_quiz.py --lo LO3           # Only LO3 questions
python formative/run_quiz.py --difficulty basic # Only basic questions
python formative/run_quiz.py --review           # See answers (study mode)
python formative/run_quiz.py --limit 5          # Quick 5-question check
```

**Features:**
- Immediate feedback with explanations
- Links to misconceptions documentation
- Learning Objective tracking
- Bloom's taxonomy level indicators

**Scoring:**
| Grade | Points | Meaning |
|-------|--------|---------|
| Excellent | 100+ (87%+) | Ready for homework and exams |
| Good | 85-99 (74-86%) | Minor gaps — review specific LOs |
| Satisfactory | 70-84 (61-73%) | Need more practice — use other resources |
| Needs Improvement | <70 (<61%) | Start from theory, work through gradually |

---

### 2. Peer Instruction Questions (`docs/peer_instruction.md`)

Five ConcepTest-style questions designed for classroom discussion.

**Protocol:**
1. Read question individually (1 min)
2. Vote your answer — no discussion (30 sec)
3. Discuss with your neighbour — convince them! (2 min)
4. Re-vote — you may change your answer (30 sec)
5. Instructor explains correct answer (2 min)

**Best for:** Identifying misconceptions, practising argumentation, collaborative learning

---

### 3. Parsons Problems (`docs/parsons_problems.md`)

Six code reordering exercises where you arrange scrambled blocks into working code.

**Best for:** Understanding code structure without syntax burden, identifying dependencies

**Topics covered:**
- P1: TCP server setup sequence
- P2: HTTP response construction
- P3: Round-robin selection
- P4: Path safety validation
- P5: Request forwarding
- P6: Proxy header injection

---

### 4. Code Tracing Exercises (`docs/code_tracing.md`)

Five exercises where you trace variable values through code execution.

**Best for:** Building mental models of how code actually works

**How to use:**
1. Read the code without running it
2. Fill in the trace table with expected values
3. Verify by running the code
4. If wrong, identify where your mental model diverged

---

### 5. Automated Tests (`make test`)

Unit tests for your exercise implementations with pedagogical feedback.

```bash
make test         # All tests
make test-ex1     # Exercise 1 only
make test-ex2     # Exercise 2 only
make smoke        # Quick environment check
```

---

## Recommended Assessment Workflow

### Before Starting Exercises

1. **Take the quiz in basic mode:**
   ```bash
   make quiz-basic
   ```
   This checks foundational knowledge. If you score <70%, review theory first.

2. **Read relevant misconceptions:**
   ```bash
   cat docs/misconceptions.md
   ```
   Know what mistakes to avoid before you make them.

### After Completing Each Exercise

1. **Run the tests:**
   ```bash
   make test-ex1   # or test-ex2
   ```

2. **Do the related Code Tracing exercise:**
   - Exercise 1 → T1, T2, T4
   - Exercise 2 → T3, T5

### Before Submitting Homework

1. **Take the full quiz:**
   ```bash
   make quiz
   ```

2. **Review any LOs where you scored <70%:**
   ```bash
   make quiz-lo LO=3   # Example: if LO3 was weak
   ```

3. **Check the smoke tests pass:**
   ```bash
   make smoke
   ```

---

## Question Types Explained

### Multiple Choice

Select one answer from options a, b, c, d.

```yaml
question_type: multiple_choice
options:
  a: "First option"
  b: "Second option"
  ...
```

**Tip:** Read ALL options before answering. Distractors are designed to catch
common misconceptions.

### Fill in the Blank

Type the exact answer (case-insensitive, multiple accepted answers possible).

```yaml
question_type: fill_blank
correct:
  - "answer1"
  - "alternative_answer"
```

**Tip:** If you're unsure of exact syntax, think about what the code needs to do.

---

## Understanding Your Results

### LO Breakdown

After completing the quiz, you'll see a breakdown like:

```
Learning Objective Breakdown:
  LO1: ████████░░ 2/3 (67%)
  LO2: ██████████ 3/3 (100%)
  LO3: ██████░░░░ 2/4 (50%)
  ...
```

**Interpretation:**
- ≥70%: You understand this LO well
- 50-69%: Review the specific artefacts in `docs/learning_objectives.md`
- <50%: Go back to theory and work through exercises again

### Question Difficulty

| Level | Bloom Taxonomy | What It Tests |
|-------|----------------|---------------|
| Basic | Remember, Understand | Definitions, concepts, simple recall |
| Intermediate | Apply | Using knowledge in familiar situations |
| Advanced | Analyse, Evaluate | Complex scenarios, security analysis |

If you struggle with basic questions, focus on theory.
If you ace basic but struggle with advanced, focus on exercises.

---

## Tips for Effective Self-Assessment

### Do

✅ Take quizzes before you feel "ready" — that's when they're most valuable
✅ Read explanations even for questions you got right
✅ Track which LOs need work and target your review
✅ Discuss wrong answers with peers — teaching helps learning
✅ Retake quizzes after 24-48 hours of practice

### Don't

❌ Memorise answers — the quiz is for learning, not high scores
❌ Skip the explanation when you get something wrong
❌ Only do assessment once — spaced repetition is powerful
❌ Ignore LOs where you scored well — reinforce strengths too

---

## Connecting Assessment to Resources

| If you struggle with... | Review these resources |
|------------------------|------------------------|
| TCP/UDP basics | `docs/glossary.md`, `docs/theory_summary.md` |
| Three-way handshake | `docs/peer_instruction.md` Q1, Demo: `make demo-handshake` |
| HTTP parsing | `docs/code_tracing.md` T1, T4 |
| Path security | `docs/parsons_problems.md` P4, `docs/misconceptions.md` |
| Round-robin | `docs/code_tracing.md` T3, `docs/parsons_problems.md` P3 |
| Packet analysis | `README.md` Wireshark filters section |

---

## Acknowledgments

The formative assessment system was designed with contributions from:

- **Andrei T.** (ASE colleague) — Question design, misconception identification
  and extensive brainstorming sessions on what makes assessment effective

- **DPPD Module, Universitatea Politehnica București** — Pedagogical framework
  for constructive alignment between LOs, activities and assessment.
  (ASE's psychopedagogy programme doesn't accept engineers — but UPB does,
  and the principles transfer well!)

The quiz format draws on ConcepTest research (Mazur, 1997) and deliberate
practice principles (Ericsson, 2008).

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*

*"Assessment should reveal understanding, not conceal it."*
