#!/usr/bin/env python3
"""
run_quiz.py — Interactive Quiz Runner for Week 14.

NETWORKING class — ASE, CSIE | Computer Networks Laboratory
by ing. dr. Antonio Clim

Runs formative assessment quizzes from YAML format with:
- Interactive CLI interface
- Immediate feedback per question
- Score tracking and LO coverage analysis
- Export capabilities (JSON, Moodle XML)
- Support for all question types including design tasks

Usage:
    python formative/run_quiz.py                    # Interactive mode
    python formative/run_quiz.py --random           # Randomise question order
    python formative/run_quiz.py --limit 5          # Limit to N questions
    python formative/run_quiz.py --lo LO1 LO2       # Filter by Learning Objectives
    python formative/run_quiz.py --export json      # Export to JSON
    python formative/run_quiz.py --no-prediction    # Skip score prediction
    python formative/run_quiz.py --help             # Show all options
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import json
import random
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError:
    print("Error: PyYAML required. Install with: pip install pyyaml")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════
class Colours:
    """ANSI colour codes for terminal output."""

    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ENDC = "\033[0m"

    @classmethod
    def disable(cls) -> None:
        """Disable colours for non-terminal output."""
        for attr in dir(cls):
            if not attr.startswith("_") and attr.isupper():
                setattr(cls, attr, "")


def print_banner(text: str, char: str = "═", width: int = 70) -> None:
    """Print a banner with decorative borders."""
    print(f"\n{Colours.CYAN}{char * width}{Colours.ENDC}")
    print(f"{Colours.BOLD}  {text}{Colours.ENDC}")
    print(f"{Colours.CYAN}{char * width}{Colours.ENDC}\n")


def print_box(lines: List[str], title: str = "") -> None:
    """Print content in a box."""
    width = max(len(line) for line in lines) + 4
    width = max(width, len(title) + 4)

    print(f"╔{'═' * width}╗")
    if title:
        print(f"║ {Colours.BOLD}{title}{Colours.ENDC}{' ' * (width - len(title) - 1)}║")
        print(f"╠{'═' * width}╣")
    for line in lines:
        print(f"║ {line}{' ' * (width - len(line) - 1)}║")
    print(f"╚{'═' * width}╝")


# ═══════════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class QuestionResult:
    """Result of answering a single question."""

    question_id: str
    lo_ref: str
    bloom_level: str
    points_possible: int
    points_earned: int
    correct: bool
    user_answer: str
    correct_answer: str


@dataclass
class QuizResult:
    """Complete quiz result with statistics."""

    student_id: str
    quiz_version: str
    started_at: datetime
    finished_at: Optional[datetime] = None
    question_results: List[QuestionResult] = field(default_factory=list)
    predicted_score: Optional[int] = None

    @property
    def total_questions(self) -> int:
        """Return total number of questions answered."""
        return len(self.question_results)

    @property
    def correct_count(self) -> int:
        """Return number of correct answers."""
        return sum(1 for r in self.question_results if r.correct)

    @property
    def total_points(self) -> int:
        """Return total possible points."""
        return sum(r.points_possible for r in self.question_results)

    @property
    def earned_points(self) -> int:
        """Return total earned points."""
        return sum(r.points_earned for r in self.question_results)

    @property
    def percentage(self) -> float:
        """Return percentage score."""
        return (self.earned_points / self.total_points * 100) if self.total_points > 0 else 0

    @property
    def lo_scores(self) -> Dict[str, Dict[str, int]]:
        """Return scores broken down by Learning Objective."""
        scores: Dict[str, Dict[str, int]] = {}
        for r in self.question_results:
            lo = r.lo_ref
            if lo not in scores:
                scores[lo] = {"earned": 0, "possible": 0}
            scores[lo]["earned"] += r.points_earned
            scores[lo]["possible"] += r.points_possible
        return scores


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ LOADING
# ═══════════════════════════════════════════════════════════════════════════════
def load_quiz(path: Path) -> Dict[str, Any]:
    """Load quiz from YAML file."""
    with open(path, encoding="utf-8") as f:
        quiz = yaml.safe_load(f)

    # Validate required fields
    if "metadata" not in quiz:
        raise ValueError("Quiz missing 'metadata' section")
    if "questions" not in quiz:
        raise ValueError("Quiz missing 'questions' section")

    return quiz


def filter_questions(
    questions: List[Dict],
    lo_filter: Optional[List[str]] = None,
    bloom_filter: Optional[List[str]] = None,
    limit: Optional[int] = None,
    randomise: bool = False,
) -> List[Dict]:
    """Filter and optionally randomise questions."""
    filtered = questions.copy()

    # Filter by LO
    if lo_filter:
        filtered = [q for q in filtered if q.get("lo_ref") in lo_filter]

    # Filter by Bloom level
    if bloom_filter:
        filtered = [q for q in filtered if q.get("bloom_level") in bloom_filter]

    # Randomise
    if randomise:
        random.shuffle(filtered)

    # Limit
    if limit and limit < len(filtered):
        filtered = filtered[:limit]

    return filtered


# ═══════════════════════════════════════════════════════════════════════════════
# QUESTION HANDLERS
# ═══════════════════════════════════════════════════════════════════════════════
def ask_multiple_choice(question: Dict, index: int, total: int) -> QuestionResult:
    """Present and score a multiple choice question."""
    q_id = question["id"]
    lo_ref = question.get("lo_ref", "")
    bloom = question.get("bloom_level", "")
    points = question.get("points", 1)
    stem = question["stem"].strip()
    options = question["options"]
    correct = question["correct"]
    hint = question.get("hint", "")
    explanation = question.get("explanation", "")

    # Display question
    print(f"\n{Colours.CYAN}Question {index}/{total}{Colours.ENDC} ", end="")
    print(f"[{Colours.DIM}{q_id} | {bloom} | {lo_ref} | {points}pts{Colours.ENDC}]")
    print(f"\n{stem}\n")

    # Display options
    for key, value in sorted(options.items()):
        print(f"  {Colours.BOLD}{key}){Colours.ENDC} {value}")

    if hint:
        print(f"\n{Colours.DIM}Hint: {hint}{Colours.ENDC}")

    # Get answer
    while True:
        answer = input(f"\nYour answer ({'/'.join(sorted(options.keys()))}): ").strip().lower()
        if answer in options:
            break
        print(f"{Colours.YELLOW}Invalid option. Please enter one of: {', '.join(sorted(options.keys()))}{Colours.ENDC}")

    # Check answer
    is_correct = answer == correct.lower()

    # Display result
    if is_correct:
        print(f"\n{Colours.GREEN}✓ Correct!{Colours.ENDC}")
        points_earned = points
    else:
        print(f"\n{Colours.RED}✗ Incorrect. The answer is: {correct}{Colours.ENDC}")
        points_earned = 0

    if explanation:
        print(f"\n{Colours.CYAN}Explanation:{Colours.ENDC}")
        print(f"{Colours.DIM}{explanation.strip()}{Colours.ENDC}")

    return QuestionResult(
        question_id=q_id,
        lo_ref=lo_ref,
        bloom_level=bloom,
        points_possible=points,
        points_earned=points_earned,
        correct=is_correct,
        user_answer=answer,
        correct_answer=correct,
    )


def ask_fill_blank(question: Dict, index: int, total: int) -> QuestionResult:
    """Present and score a fill-in-the-blank question."""
    q_id = question["id"]
    lo_ref = question.get("lo_ref", "")
    bloom = question.get("bloom_level", "")
    points = question.get("points", 1)
    stem = question["stem"].strip()
    correct_answers = question["correct"]  # List of acceptable answers
    case_sensitive = question.get("case_sensitive", False)
    hint = question.get("hint", "")
    explanation = question.get("explanation", "")

    # Display question
    print(f"\n{Colours.CYAN}Question {index}/{total}{Colours.ENDC} ", end="")
    print(f"[{Colours.DIM}{q_id} | {bloom} | {lo_ref} | {points}pts{Colours.ENDC}]")
    print(f"\n{stem}\n")

    if hint:
        print(f"{Colours.DIM}Hint: {hint}{Colours.ENDC}")

    # Get answer
    answer = input("\nYour answer: ").strip()

    # Check answer
    if case_sensitive:
        is_correct = answer in correct_answers
    else:
        is_correct = answer.lower() in [a.lower() for a in correct_answers]

    # Display result
    if is_correct:
        print(f"\n{Colours.GREEN}✓ Correct!{Colours.ENDC}")
        points_earned = points
    else:
        print(f"\n{Colours.RED}✗ Incorrect. Acceptable answers: {', '.join(correct_answers)}{Colours.ENDC}")
        points_earned = 0

    if explanation:
        print(f"\n{Colours.CYAN}Explanation:{Colours.ENDC}")
        print(f"{Colours.DIM}{explanation.strip()}{Colours.ENDC}")

    return QuestionResult(
        question_id=q_id,
        lo_ref=lo_ref,
        bloom_level=bloom,
        points_possible=points,
        points_earned=points_earned,
        correct=is_correct,
        user_answer=answer,
        correct_answer=correct_answers[0] if correct_answers else "",
    )


def ask_design_task(question: Dict, index: int, total: int) -> QuestionResult:
    """Present a design/essay task (self-evaluated or manual grading)."""
    q_id = question["id"]
    lo_ref = question.get("lo_ref", "")
    bloom = question.get("bloom_level", "")
    points = question.get("points", 5)
    stem = question["stem"].strip()
    rubric = question.get("rubric", {})
    model_answer = question.get("model_answer", "")
    code_template = question.get("code_template", "")

    # Display question
    print(f"\n{Colours.CYAN}Question {index}/{total}{Colours.ENDC} ", end="")
    print(f"[{Colours.DIM}{q_id} | {bloom} | {lo_ref} | {points}pts{Colours.ENDC}]")
    print(f"\n{stem}\n")

    if code_template:
        print(f"{Colours.CYAN}Code Template:{Colours.ENDC}")
        print(f"{Colours.DIM}{code_template.strip()}{Colours.ENDC}\n")

    # Display rubric
    if rubric:
        print(f"{Colours.CYAN}Evaluation Criteria:{Colours.ENDC}")
        for score, desc in sorted(rubric.items(), reverse=True):
            print(f"  {Colours.BOLD}{score} pts:{Colours.ENDC} {desc}")

    print("\n" + "─" * 50)
    print(f"{Colours.YELLOW}This is a design task requiring manual evaluation.{Colours.ENDC}")
    print("Write your answer below (press Enter twice to finish):")
    print("─" * 50)

    # Collect multi-line input
    lines = []
    while True:
        line = input()
        if line == "":
            if lines and lines[-1] == "":
                break
        lines.append(line)

    answer = "\n".join(lines).strip()

    # Show model answer
    if model_answer:
        print(f"\n{Colours.CYAN}Model Answer:{Colours.ENDC}")
        print(f"{Colours.DIM}{model_answer.strip()}{Colours.ENDC}")

    # Self-evaluation
    print(f"\n{Colours.YELLOW}Self-evaluate your answer:{Colours.ENDC}")
    while True:
        try:
            self_score = int(input(f"Score (0-{points}): "))
            if 0 <= self_score <= points:
                break
            print(f"Please enter a value between 0 and {points}")
        except ValueError:
            print("Please enter a number")

    return QuestionResult(
        question_id=q_id,
        lo_ref=lo_ref,
        bloom_level=bloom,
        points_possible=points,
        points_earned=self_score,
        correct=self_score >= points * 0.7,  # 70% threshold
        user_answer=answer[:200] + "..." if len(answer) > 200 else answer,
        correct_answer="[Design task - see model answer]",
    )


def ask_question(question: Dict, index: int, total: int) -> QuestionResult:
    """Route question to appropriate handler based on type."""
    q_type = question.get("type", "multiple_choice")

    if q_type == "multiple_choice":
        return ask_multiple_choice(question, index, total)
    elif q_type in ("fill_blank", "short_answer"):
        return ask_fill_blank(question, index, total)
    elif q_type in ("design_task", "architecture_design", "troubleshooting_design", "scenario_analysis"):
        return ask_design_task(question, index, total)
    else:
        # Default to multiple choice for unknown types
        if "options" in question:
            return ask_multiple_choice(question, index, total)
        else:
            return ask_design_task(question, index, total)


# ═══════════════════════════════════════════════════════════════════════════════
# SCORING AND RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def prompt_prediction(total_questions: int, total_points: int) -> Optional[int]:
    """Ask for score prediction (metacognitive exercise)."""
    print(f"\n{Colours.CYAN}Before starting, predict your score:{Colours.ENDC}")
    print(f"  Total questions: {total_questions}")
    print(f"  Total points: {total_points}")

    while True:
        try:
            prediction = input(f"\nPredicted score (0-{total_points}): ").strip()
            if not prediction:
                return None
            pred_int = int(prediction)
            if 0 <= pred_int <= total_points:
                return pred_int
            print(f"Please enter a value between 0 and {total_points}")
        except ValueError:
            print("Please enter a number or press Enter to skip")


def display_results(result: QuizResult, quiz: Dict) -> None:
    """Display comprehensive quiz results."""
    print_banner("QUIZ RESULTS")

    # Score summary
    percentage = result.percentage
    if percentage >= 70:
        colour = Colours.GREEN
        status = "PASS"
    else:
        colour = Colours.RED
        status = "FAIL"

    print(f"  Score: {colour}{result.earned_points}/{result.total_points} ({percentage:.1f}%) - {status}{Colours.ENDC}")
    print(f"  Correct: {result.correct_count}/{result.total_questions} questions")

    # Prediction accuracy
    if result.predicted_score is not None:
        diff = result.earned_points - result.predicted_score
        print(f"  Prediction: {result.predicted_score} (Difference: {diff:+d})")

    # LO breakdown
    print(f"\n{Colours.CYAN}Learning Objective Scores:{Colours.ENDC}")
    for lo, scores in sorted(result.lo_scores.items()):
        pct = (scores["earned"] / scores["possible"] * 100) if scores["possible"] > 0 else 0
        bar_len = int(pct / 5)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        print(f"  {lo}: [{bar}] {scores['earned']}/{scores['possible']} ({pct:.0f}%)")

    # Bloom level breakdown
    print(f"\n{Colours.CYAN}Bloom Level Performance:{Colours.ENDC}")
    bloom_scores: Dict[str, Dict[str, int]] = {}
    for r in result.question_results:
        bl = r.bloom_level
        if bl not in bloom_scores:
            bloom_scores[bl] = {"earned": 0, "possible": 0}
        bloom_scores[bl]["earned"] += r.points_earned
        bloom_scores[bl]["possible"] += r.points_possible

    for bl in ["Remember", "Understand", "Apply", "Analyse", "Evaluate", "Create"]:
        if bl in bloom_scores:
            scores = bloom_scores[bl]
            pct = (scores["earned"] / scores["possible"] * 100) if scores["possible"] > 0 else 0
            print(f"  {bl}: {scores['earned']}/{scores['possible']} ({pct:.0f}%)")

    # Feedback
    feedback = quiz.get("feedback", {})
    if percentage >= 70:
        msg = feedback.get("on_pass", "Well done! You have passed the quiz.")
    else:
        msg = feedback.get("on_fail", "More study needed. Review the learning materials.")

    print(f"\n{Colours.CYAN}Feedback:{Colours.ENDC}")
    print(f"  {msg.strip()}")


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def export_to_json(quiz: Dict, output_path: Path) -> None:
    """Export quiz to JSON format for LMS import."""
    export_config = quiz.get("export", {}).get("json", {})

    export_data = {
        "metadata": quiz["metadata"],
        "questions": [],
    }

    include_explanations = export_config.get("include_explanations", True)
    include_hints = export_config.get("include_hints", True)

    for q in quiz["questions"]:
        q_export = {
            "id": q["id"],
            "type": q.get("type", "multiple_choice"),
            "bloom_level": q.get("bloom_level"),
            "lo_ref": q.get("lo_ref"),
            "points": q.get("points", 1),
            "stem": q["stem"],
        }

        if "options" in q:
            q_export["options"] = q["options"]
        q_export["correct"] = q.get("correct")

        if include_explanations and "explanation" in q:
            q_export["explanation"] = q["explanation"]
        if include_hints and "hint" in q:
            q_export["hint"] = q["hint"]

        export_data["questions"].append(q_export)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    print(f"Exported to {output_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN QUIZ RUNNER
# ═══════════════════════════════════════════════════════════════════════════════
def run_quiz(
    quiz_path: Path,
    randomise: bool = False,
    limit: Optional[int] = None,
    lo_filter: Optional[List[str]] = None,
    show_prediction: bool = True,
) -> QuizResult:
    """Run the interactive quiz."""
    # Load quiz
    quiz = load_quiz(quiz_path)
    meta = quiz["metadata"]

    # Display header
    print_banner(f"Formative Quiz — Week {meta.get('week', '?')}: {meta.get('topic', 'Assessment')}")

    print(f"  Version: {meta.get('version', '1.0')}")
    print(f"  Questions: {len(quiz['questions'])}")
    print(f"  Estimated time: {meta.get('estimated_time_minutes', '?')} minutes")
    print(f"  Passing score: {meta.get('passing_score_percent', 70)}%")

    # Filter questions
    questions = filter_questions(
        quiz["questions"],
        lo_filter=lo_filter,
        limit=limit,
        randomise=randomise,
    )

    if not questions:
        print(f"\n{Colours.RED}No questions match the filter criteria{Colours.ENDC}")
        sys.exit(1)

    # Calculate total points
    total_points = sum(q.get("points", 1) for q in questions)

    # Start quiz
    print(f"\n{Colours.YELLOW}Starting quiz with {len(questions)} questions ({total_points} points)...{Colours.ENDC}")

    # Prediction (metacognitive)
    predicted = None
    if show_prediction:
        predicted = prompt_prediction(len(questions), total_points)

    input(f"\n{Colours.CYAN}Press Enter to begin...{Colours.ENDC}")

    # Create result tracker
    result = QuizResult(
        student_id="interactive",
        quiz_version=meta.get("version", "1.0"),
        started_at=datetime.now(),
        predicted_score=predicted,
    )

    # Run each question
    for i, question in enumerate(questions, 1):
        q_result = ask_question(question, i, len(questions))
        result.question_results.append(q_result)

    result.finished_at = datetime.now()

    # Display results
    display_results(result, quiz)

    return result


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run formative assessment quiz",
        epilog="NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim",
    )

    parser.add_argument(
        "--quiz",
        type=Path,
        default=Path(__file__).parent / "quiz.yaml",
        help="Path to quiz YAML file (default: formative/quiz.yaml)",
    )
    parser.add_argument(
        "--random",
        action="store_true",
        help="Randomise question order",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit to N questions",
    )
    parser.add_argument(
        "--lo",
        nargs="+",
        help="Filter by Learning Objectives (e.g., --lo LO1 LO2)",
    )
    parser.add_argument(
        "--no-prediction",
        action="store_true",
        help="Skip score prediction prompt",
    )
    parser.add_argument(
        "--export",
        choices=["json"],
        help="Export quiz format instead of running",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file for export",
    )
    parser.add_argument(
        "--no-colour",
        action="store_true",
        help="Disable coloured output",
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()

    if args.no_colour:
        Colours.disable()

    if args.export:
        quiz = load_quiz(args.quiz)
        output = args.output or Path(f"quiz_export.{args.export}")
        if args.export == "json":
            export_to_json(quiz, output)
        return 0

    try:
        run_quiz(
            args.quiz,
            randomise=args.random,
            limit=args.limit,
            lo_filter=args.lo,
            show_prediction=not args.no_prediction,
        )
        return 0
    except KeyboardInterrupt:
        print(f"\n\n{Colours.YELLOW}Quiz cancelled.{Colours.ENDC}")
        return 1
    except FileNotFoundError as e:
        print(f"{Colours.RED}Error: {e}{Colours.ENDC}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
