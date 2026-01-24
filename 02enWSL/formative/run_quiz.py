#!/usr/bin/env python3
"""
Formative Quiz Runner — Week 2: Architectural Models and Socket Programming

Interactive quiz system for self-assessment of learning objectives.
Supports multiple question types: multiple choice, fill-in-blank and code output.

Usage:
    python formative/run_quiz.py                    # Run full quiz
    python formative/run_quiz.py --random           # Randomise question order
    python formative/run_quiz.py --limit 5          # Only 5 questions
    python formative/run_quiz.py --level 2          # Only Bloom level 2 (Understand)
    python formative/run_quiz.py --review           # Review mode (show answers)

NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim
"""

from __future__ import annotations

import argparse
import random
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# Handle YAML import gracefully
try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed.")
    print("Fix:   pip install pyyaml")
    sys.exit(1)


@dataclass
class QuizResult:
    """Stores results from a quiz attempt."""

    total_questions: int = 0
    correct_answers: int = 0
    wrong_answers: list = field(default_factory=list)
    skipped: int = 0

    @property
    def score_percentage(self) -> float:
        if self.total_questions == 0:
            return 0.0
        return (self.correct_answers / self.total_questions) * 100

    @property
    def passed(self) -> bool:
        return self.score_percentage >= 70


def load_quiz(quiz_path: Path) -> dict:
    """
    Load quiz from YAML file.

    Args:
        quiz_path: Path to the quiz YAML file

    Returns:
        Parsed quiz dictionary

    Raises:
        FileNotFoundError: If quiz file does not exist
        yaml.YAMLError: If YAML parsing fails
    """
    if not quiz_path.exists():
        raise FileNotFoundError(f"Quiz file not found: {quiz_path}")

    with open(quiz_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def display_question(question: dict, number: int, total: int) -> None:
    """Display a single question with formatting."""
    difficulty_stars = {"basic": "★☆☆", "intermediate": "★★☆", "advanced": "★★★"}
    bloom_names = {
        1: "Remember",
        2: "Understand",
        3: "Apply",
        4: "Analyse",
        5: "Evaluate",
        6: "Create",
    }

    diff = difficulty_stars.get(question.get("difficulty", "basic"), "★☆☆")
    bloom = bloom_names.get(question.get("bloom_level", 1), "Remember")

    print()
    print("=" * 70)
    print(f"  Question {number}/{total}  |  {diff}  |  Bloom: {bloom}")
    print("=" * 70)
    print()

    # Display stem (question text)
    stem = question["stem"].strip()
    print(stem)
    print()

    # Display options for multiple choice
    if question["type"] in ("multiple_choice", "code_output"):
        for key, value in question.get("options", {}).items():
            print(f"    {key}) {value}")
        print()


def get_user_answer(question: dict) -> Optional[str]:
    """
    Get and validate user input for a question.

    Returns:
        User's answer string, or None if skipped
    """
    q_type = question["type"]

    if q_type in ("multiple_choice", "code_output"):
        valid_options = list(question.get("options", {}).keys())
        prompt = f"Your answer ({'/'.join(valid_options)}, or 's' to skip): "

        while True:
            answer = input(prompt).strip().lower()

            if answer == "s":
                return None
            if answer in valid_options:
                return answer

            print(f"  Invalid input. Please enter one of: {', '.join(valid_options)}")

    elif q_type == "fill_blank":
        prompt = "Your answer (or 's' to skip): "
        answer = input(prompt).strip()

        if answer.lower() == "s":
            return None
        return answer

    return None


def check_answer(question: dict, user_answer: str) -> bool:
    """
    Check if user's answer is correct.

    Args:
        question: The question dictionary
        user_answer: User's submitted answer

    Returns:
        True if correct, False otherwise
    """
    correct = question["correct"]

    if question["type"] in ("multiple_choice", "code_output"):
        return user_answer.lower() == correct.lower()

    elif question["type"] == "fill_blank":
        # Fill-blank may have multiple acceptable answers
        if isinstance(correct, list):
            return user_answer.lower() in [c.lower() for c in correct]
        return user_answer.lower() == correct.lower()

    return False


def display_feedback(question: dict, user_answer: Optional[str], is_correct: bool) -> None:
    """Display feedback after answering."""
    if user_answer is None:
        print("  ⏭️  Skipped")
        return

    if is_correct:
        print("  ✅ Correct!")
    else:
        correct = question["correct"]
        if isinstance(correct, list):
            correct = correct[0]
        print(f"  ❌ Incorrect. The answer is: {correct}")

    # Show explanation
    explanation = question.get("explanation", "")
    if explanation:
        print()
        print(f"  📖 {explanation}")

    # Show hint for wrong fill-blank answers
    if not is_correct and question["type"] == "fill_blank":
        hint = question.get("hint", "")
        if hint:
            print(f"  💡 Hint was: {hint}")


def display_results(result: QuizResult, quiz_meta: dict) -> None:
    """Display final quiz results with grade."""
    print()
    print("=" * 70)
    print("                        QUIZ COMPLETE")
    print("=" * 70)
    print()
    print(f"  Score: {result.correct_answers}/{result.total_questions} "
          f"({result.score_percentage:.1f}%)")
    print()

    # Determine grade
    pct = result.score_percentage
    boundaries = quiz_meta.get("scoring", {}).get("grade_boundaries", {})

    if pct >= boundaries.get("excellent", 90):
        grade = "A (Excellent)"
        emoji = "🌟"
    elif pct >= boundaries.get("good", 75):
        grade = "B (Good)"
        emoji = "👍"
    elif pct >= boundaries.get("satisfactory", 60):
        grade = "C (Satisfactory)"
        emoji = "✔️"
    elif pct >= boundaries.get("passing", 50):
        grade = "D (Passing)"
        emoji = "📝"
    else:
        grade = "F (Needs Review)"
        emoji = "📚"

    print(f"  Grade: {emoji} {grade}")
    print()

    if result.passed:
        print("  ✅ You have demonstrated understanding of the learning objectives.")
    else:
        print("  ⚠️  Review the materials and try again.")
        print("      See: docs/theory_summary.md and docs/misconceptions.md")

    # List topics to review
    if result.wrong_answers:
        print()
        print("  Topics to review:")
        seen_refs = set()
        for q in result.wrong_answers:
            ref = q.get("misconception_ref")
            if ref and ref not in seen_refs:
                print(f"    • {ref}")
                seen_refs.add(ref)
            lo = q.get("lo_ref", "")
            if lo:
                print(f"    • Learning objective: {lo}")

    print()
    print("=" * 70)


def run_quiz(
    quiz: dict,
    randomise: bool = False,
    limit: Optional[int] = None,
    bloom_level: Optional[int] = None,
    review_mode: bool = False,
) -> QuizResult:
    """
    Run the interactive quiz.

    Args:
        quiz: Parsed quiz dictionary
        randomise: Shuffle question order
        limit: Maximum number of questions
        bloom_level: Filter to specific Bloom level
        review_mode: Show correct answers immediately

    Returns:
        QuizResult with scores and feedback
    """
    meta = quiz.get("metadata", {})
    questions = quiz.get("questions", [])

    # Filter by Bloom level if specified
    if bloom_level is not None:
        questions = [q for q in questions if q.get("bloom_level") == bloom_level]
        if not questions:
            print(f"No questions found for Bloom level {bloom_level}")
            sys.exit(1)

    # Randomise if requested
    if randomise:
        questions = questions.copy()
        random.shuffle(questions)

    # Limit questions
    if limit is not None:
        questions = questions[:limit]

    # Display header
    print()
    print("=" * 70)
    print(f"  {meta.get('topic', 'Quiz')}")
    print(f"  Week {meta.get('week', '?')} | {len(questions)} questions | "
          f"Passing: {meta.get('passing_score', 70)}%")
    print("=" * 70)
    print()
    print("  Instructions:")
    print("  • For multiple choice, enter the letter (a, b, c, d)")
    print("  • For fill-in-blank, type your answer")
    print("  • Enter 's' to skip a question")
    print()
    input("  Press Enter to begin... ")

    result = QuizResult(total_questions=len(questions))

    for i, question in enumerate(questions, 1):
        display_question(question, i, len(questions))

        if review_mode:
            # In review mode, show answer immediately
            correct = question["correct"]
            if isinstance(correct, list):
                correct = correct[0]
            print(f"  📋 Answer: {correct}")
            print()
            explanation = question.get("explanation", "")
            if explanation:
                print(f"  📖 {explanation}")
            print()
            input("  Press Enter for next question... ")
            continue

        user_answer = get_user_answer(question)

        if user_answer is None:
            result.skipped += 1
            display_feedback(question, None, False)
        else:
            is_correct = check_answer(question, user_answer)
            if is_correct:
                result.correct_answers += 1
            else:
                result.wrong_answers.append(question)
            display_feedback(question, user_answer, is_correct)

        print()
        if i < len(questions):
            input("  Press Enter for next question... ")

    if not review_mode:
        display_results(result, quiz)

    return result


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Week 2 Formative Quiz Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python formative/run_quiz.py                # Full quiz
  python formative/run_quiz.py --random       # Randomised order
  python formative/run_quiz.py --limit 5      # Quick 5-question quiz
  python formative/run_quiz.py --level 3      # Only Apply-level questions
  python formative/run_quiz.py --review       # Study mode (shows answers)
        """,
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
        metavar="N",
        help="Limit to N questions",
    )
    parser.add_argument(
        "--level",
        type=int,
        choices=[1, 2, 3, 4, 5, 6],
        metavar="L",
        help="Filter by Bloom level (1=Remember ... 6=Create)",
    )
    parser.add_argument(
        "--review",
        action="store_true",
        help="Review mode — show answers without scoring",
    )

    args = parser.parse_args()

    try:
        quiz = load_quiz(args.quiz)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except yaml.YAMLError as e:
        print(f"Error parsing quiz file: {e}")
        return 1

    result = run_quiz(
        quiz,
        randomise=args.random,
        limit=args.limit,
        bloom_level=args.level,
        review_mode=args.review,
    )

    # Return 0 if passed, 1 if failed (useful for CI)
    if args.review:
        return 0
    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
