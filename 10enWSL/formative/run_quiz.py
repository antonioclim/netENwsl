#!/usr/bin/env python3
"""
Week 10 Formative Assessment Quiz Runner
========================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Interactive quiz runner for self-assessment of Week 10 learning objectives.

Usage:
    python formative/run_quiz.py                    # Run all questions
    python formative/run_quiz.py --random           # Shuffle questions
    python formative/run_quiz.py --limit 5          # First 5 questions
    python formative/run_quiz.py --lo LO1           # Filter by Learning Objective
    python formative/run_quiz.py --difficulty basic # Filter by difficulty
    python formative/run_quiz.py --review           # Review mode (show answers)

Prerequisites:
    pip install pyyaml
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError:
    print("[ERROR] PyYAML is required: pip install pyyaml")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
SCRIPT_DIR = Path(__file__).parent
DEFAULT_QUIZ = SCRIPT_DIR / "quiz.yaml"

# ANSI colour codes for terminal output
COLOURS = {
    "green": "\033[92m",
    "red": "\033[91m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "bold": "\033[1m",
    "reset": "\033[0m",
}


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_LOADER
# ═══════════════════════════════════════════════════════════════════════════════
def load_quiz(path: Path) -> Dict[str, Any]:
    """Load quiz from YAML file."""
    if not path.exists():
        raise FileNotFoundError(f"Quiz file not found: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def filter_questions(
    questions: List[Dict[str, Any]],
    lo_filter: Optional[str] = None,
    difficulty_filter: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Filter questions by Learning Objective or difficulty."""
    filtered = questions
    
    if lo_filter:
        filtered = [q for q in filtered if q.get("lo_ref") == lo_filter.upper()]
    
    if difficulty_filter:
        filtered = [q for q in filtered if q.get("difficulty") == difficulty_filter.lower()]
    
    return filtered


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_DISPLAY
# ═══════════════════════════════════════════════════════════════════════════════
def colour(text: str, colour_name: str) -> str:
    """Apply ANSI colour to text."""
    return f"{COLOURS.get(colour_name, '')}{text}{COLOURS['reset']}"


def display_question(q: Dict[str, Any], index: int, total: int) -> None:
    """Display a single question."""
    print(f"\n{'─' * 70}")
    print(colour(f"Question {index}/{total}", "bold"), end="")
    print(f"  [{q.get('lo_ref', '?')}] [{q.get('difficulty', '?')}] [{q.get('bloom_level', '?')}]")
    print(f"{'─' * 70}")
    
    # Display stem (may be multiline)
    stem = q.get("stem", "").strip()
    print(f"\n{stem}\n")
    
    # Display options
    options = q.get("options", {})
    for key in sorted(options.keys()):
        print(f"  {key}) {options[key]}")


def display_feedback(
    q: Dict[str, Any],
    user_answer: str,
    is_correct: bool,
    show_explanation: bool = True,
) -> None:
    """Display feedback after answering."""
    correct_answer = q.get("correct", "")
    
    if is_correct:
        print(colour("\n✓ Correct!", "green"))
    else:
        print(colour(f"\n✗ Incorrect. The correct answer is: {correct_answer}", "red"))
    
    if show_explanation and "explanation" in q:
        print(colour("\n📖 Explanation:", "blue"))
        explanation = q["explanation"].strip()
        for line in explanation.split("\n"):
            print(f"   {line.strip()}")
    
    if "verify_command" in q:
        print(colour("\n🔧 Verify:", "yellow"))
        print(f"   {q['verify_command']}")
    
    if "misconception_ref" in q:
        print(colour(f"\n📚 See: {q['misconception_ref']}", "blue"))


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_RUNNER
# ═══════════════════════════════════════════════════════════════════════════════
def run_quiz(
    quiz: Dict[str, Any],
    randomise: bool = False,
    limit: Optional[int] = None,
    lo_filter: Optional[str] = None,
    difficulty_filter: Optional[str] = None,
    review_mode: bool = False,
) -> float:
    """
    Run interactive quiz and return score percentage.
    
    💭 PREDICTION: What score would indicate mastery of the material?
    """
    metadata = quiz.get("metadata", {})
    questions = quiz.get("questions", [])
    
    # Apply filters
    questions = filter_questions(questions, lo_filter, difficulty_filter)
    
    if not questions:
        print("[WARNING] No questions match the specified filters.")
        return 0.0
    
    if randomise:
        random.shuffle(questions)
    
    if limit and limit > 0:
        questions = questions[:limit]
    
    # Display header
    print("\n" + "═" * 70)
    print(colour(f"  Week {metadata.get('week', '?')} Formative Quiz", "bold"))
    print(f"  Topic: {metadata.get('topic', 'Unknown')}")
    print(f"  Questions: {len(questions)} | Passing: {metadata.get('passing_score', 70)}%")
    if lo_filter:
        print(f"  Filter: {lo_filter}")
    if review_mode:
        print(colour("  Mode: REVIEW (answers shown)", "yellow"))
    print("═" * 70)
    
    correct_count = 0
    total = len(questions)
    
    for i, q in enumerate(questions, 1):
        display_question(q, i, total)
        
        if review_mode:
            # In review mode, show answer immediately
            correct = q.get("correct", "?")
            print(colour(f"\n  Answer: {correct}", "green"))
            display_feedback(q, correct, True, show_explanation=True)
            input("\n  Press Enter to continue...")
        else:
            # Interactive mode
            valid_options = list(q.get("options", {}).keys())
            
            while True:
                try:
                    answer = input(f"\nYour answer ({'/'.join(valid_options)}): ").strip().lower()
                    if answer in valid_options:
                        break
                    if answer == "q":
                        print("\n[INFO] Quiz aborted.")
                        return (correct_count / i) * 100 if i > 0 else 0.0
                    print(f"  Invalid. Enter one of: {', '.join(valid_options)} (or 'q' to quit)")
                except (KeyboardInterrupt, EOFError):
                    print("\n[INFO] Quiz aborted.")
                    return (correct_count / total) * 100 if total > 0 else 0.0
            
            is_correct = answer == q.get("correct", "").lower()
            if is_correct:
                correct_count += 1
            
            display_feedback(q, answer, is_correct)
    
    # Calculate and display results
    score = (correct_count / total) * 100 if total > 0 else 0.0
    passing = metadata.get("passing_score", 70)
    passed = score >= passing
    
    print("\n" + "═" * 70)
    print(colour("  RESULTS", "bold"))
    print("═" * 70)
    print(f"  Score: {correct_count}/{total} ({score:.1f}%)")
    
    if passed:
        print(colour(f"  Status: ✓ PASSED (threshold: {passing}%)", "green"))
    else:
        print(colour(f"  Status: ✗ NEEDS REVIEW (threshold: {passing}%)", "red"))
    
    # LO breakdown
    if not review_mode:
        print("\n  Performance by Learning Objective:")
        lo_scores: Dict[str, List[bool]] = {}
        for i, q in enumerate(questions):
            lo = q.get("lo_ref", "Unknown")
            if lo not in lo_scores:
                lo_scores[lo] = []
            # This is approximate since we don't track individual answers
        print("  (Run with --review to see detailed LO coverage)")
    
    print("═" * 70 + "\n")
    
    return score


# ═══════════════════════════════════════════════════════════════════════════════
# CLI_INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args(argv: List[str]) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Week 10 Formative Assessment Quiz",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_quiz.py                    Run all questions
  python run_quiz.py --random           Shuffle question order
  python run_quiz.py --limit 5          Only first 5 questions
  python run_quiz.py --lo LO1           Filter by Learning Objective
  python run_quiz.py --difficulty basic Filter by difficulty
  python run_quiz.py --review           Review mode (show answers)
        """,
    )
    
    parser.add_argument(
        "--quiz", "-q",
        type=Path,
        default=DEFAULT_QUIZ,
        help="Path to quiz YAML file",
    )
    parser.add_argument(
        "--random", "-r",
        action="store_true",
        help="Randomise question order",
    )
    parser.add_argument(
        "--limit", "-n",
        type=int,
        default=None,
        help="Limit to N questions",
    )
    parser.add_argument(
        "--lo",
        type=str,
        default=None,
        help="Filter by Learning Objective (e.g., LO1, LO2)",
    )
    parser.add_argument(
        "--difficulty", "-d",
        type=str,
        choices=["basic", "intermediate", "advanced"],
        default=None,
        help="Filter by difficulty level",
    )
    parser.add_argument(
        "--review",
        action="store_true",
        help="Review mode — show answers immediately",
    )
    
    return parser.parse_args(argv)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main(argv: List[str]) -> int:
    """Main entry point."""
    args = parse_args(argv)
    
    try:
        quiz = load_quiz(args.quiz)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        return 1
    except yaml.YAMLError as e:
        print(f"[ERROR] Invalid YAML: {e}")
        return 1
    
    score = run_quiz(
        quiz,
        randomise=args.random,
        limit=args.limit,
        lo_filter=args.lo,
        difficulty_filter=args.difficulty,
        review_mode=args.review,
    )
    
    # Return 0 if passed, 1 if failed
    passing = quiz.get("metadata", {}).get("passing_score", 70)
    return 0 if score >= passing else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
