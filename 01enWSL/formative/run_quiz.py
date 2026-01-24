#!/usr/bin/env python3
"""
Formative Quiz Runner — Week 1
==============================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Interactive quiz runner that loads questions from YAML and provides
immediate feedback with scoring and recommendations.

Usage:
    python formative/run_quiz.py                    # Full quiz
    python formative/run_quiz.py --section pre_lab  # Specific section
    python formative/run_quiz.py --random --limit 5 # Random 5 questions
    python formative/run_quiz.py --review           # Review mode (show answers)
    python formative/run_quiz.py --list-sections    # Show available sections

Exit Codes:
    0: Quiz passed (score >= passing threshold)
    1: Quiz failed or error occurred
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import random
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional

try:
    import yaml
except ImportError:
    print("❌ PyYAML not installed.")
    print("   Run: pip install pyyaml --break-system-packages")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class QuizResult:
    """Container for quiz attempt results."""
    total_questions: int = 0
    correct_answers: int = 0
    total_points: int = 0
    earned_points: int = 0
    score_percentage: float = 0.0
    time_taken_seconds: float = 0.0
    section_scores: dict = field(default_factory=dict)
    lo_coverage: dict = field(default_factory=dict)
    lo_total: dict = field(default_factory=dict)
    weak_areas: list = field(default_factory=list)
    question_results: list = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_LOADER
# ═══════════════════════════════════════════════════════════════════════════════
def load_quiz(path: Path) -> dict:
    """
    Load quiz from YAML file with validation.
    
    Args:
        path: Path to quiz YAML file
        
    Returns:
        Parsed quiz dictionary
        
    Raises:
        FileNotFoundError: If quiz file doesn't exist
        ValueError: If quiz is missing required keys
    """
    if not path.exists():
        raise FileNotFoundError(f"Quiz file not found: {path}")
    
    with open(path, encoding="utf-8") as f:
        quiz = yaml.safe_load(f)
    
    # Basic validation
    required_keys = ["metadata", "questions"]
    for key in required_keys:
        if key not in quiz:
            raise ValueError(f"Quiz missing required key: {key}")
    
    # Validate questions have required fields
    for q in quiz["questions"]:
        if "id" not in q or "type" not in q or "stem" not in q:
            raise ValueError(f"Question missing required fields: {q.get('id', 'unknown')}")
    
    return quiz


# ═══════════════════════════════════════════════════════════════════════════════
# QUESTION_HANDLERS
# ═══════════════════════════════════════════════════════════════════════════════
def ask_multiple_choice(q: dict) -> tuple[bool, str]:
    """Handle multiple choice question."""
    print(f"\n{q['stem']}\n")
    for key, val in q["options"].items():
        print(f"  {key}) {val}")
    
    while True:
        answer = input("\nYour answer (a/b/c/d): ").strip().lower()
        if answer in q["options"]:
            break
        print("  ⚠️ Please enter a, b, c, or d")
    
    correct = answer == q["correct"].lower()
    return correct, answer


def ask_fill_blank(q: dict) -> tuple[bool, str]:
    """Handle fill-in-the-blank question."""
    print(f"\n{q['stem']}\n")
    
    if q.get("hint"):
        print(f"💡 Hint: {q['hint']}")
    
    answer = input("\nYour answer: ").strip()
    
    # Check against all valid answers
    correct_answers = q["correct"]
    case_sensitive = q.get("case_sensitive", False)
    
    check_answer = answer if case_sensitive else answer.lower()
    check_correct = correct_answers if case_sensitive else [a.lower() for a in correct_answers]
    
    correct = check_answer in check_correct
    return correct, answer


def ask_true_false(q: dict) -> tuple[bool, str]:
    """Handle true/false question."""
    print(f"\n{q['stem']}\n")
    
    while True:
        answer = input("Your answer (true/false or t/f): ").strip().lower()
        if answer in ["true", "false", "t", "f", "yes", "no", "y", "n", "1", "0"]:
            break
        print("  ⚠️ Please enter true/false or t/f")
    
    user_answer = answer in ["true", "t", "yes", "y", "1"]
    correct = user_answer == q["correct"]
    return correct, str(user_answer)


def ask_numeric(q: dict) -> tuple[bool, str]:
    """Handle numeric question."""
    print(f"\n{q['stem']}\n")
    
    if q.get("hint"):
        print(f"💡 Hint: {q['hint']}")
    
    while True:
        try:
            answer_str = input("\nYour answer: ").strip()
            answer = float(answer_str)
            break
        except ValueError:
            print("  ⚠️ Please enter a number")
    
    tolerance = q.get("tolerance", 0)
    correct = abs(answer - q["correct"]) <= tolerance
    return correct, answer_str


def ask_command(q: dict) -> tuple[bool, str]:
    """Handle command/code question."""
    print(f"\n{q['stem']}\n")
    
    answer = input("Your command: ").strip()
    
    # Check against valid answers or regex
    correct = False
    if "validation_regex" in q:
        correct = bool(re.match(q["validation_regex"], answer, re.IGNORECASE))
    else:
        correct = answer.lower() in [a.lower() for a in q["correct"]]
    
    return correct, answer


def ask_code_trace(q: dict) -> tuple[bool, str]:
    """Handle code tracing question."""
    print(f"\n{q['stem']}")
    
    answer = input("\nWhat will be printed? ").strip()
    correct = answer.upper() in [a.upper() for a in q["correct"]]
    return correct, answer


def ask_matching(q: dict) -> tuple[bool, str]:
    """Handle matching question (simplified for CLI)."""
    print(f"\n{q['stem']}\n")
    
    # Display left items with numbers
    print("Items to match:")
    for i, pair in enumerate(q["pairs"], 1):
        print(f"  {i}. {pair['left']}")
    
    print("\nOptions:")
    rights = [p["right"] for p in q["pairs"]]
    shuffled_indices = list(range(len(rights)))
    random.shuffle(shuffled_indices)
    
    letter_map = {}
    for i, idx in enumerate(shuffled_indices):
        letter = chr(65 + i)  # A, B, C, D...
        letter_map[letter] = rights[idx]
        print(f"  {letter}. {rights[idx]}")
    
    print("\n(Enter your matches as: 1A 2B 3C 4D)")
    answer = input("Your matches: ").strip().upper()
    
    # Parse and check matches
    correct_count = 0
    for pair_match in answer.split():
        if len(pair_match) >= 2:
            try:
                num = int(pair_match[0]) - 1
                letter = pair_match[1]
                if 0 <= num < len(q["pairs"]) and letter in letter_map:
                    expected_right = q["pairs"][num]["right"]
                    if letter_map[letter] == expected_right:
                        correct_count += 1
            except (ValueError, IndexError):
                continue
    
    correct = correct_count == len(q["pairs"])
    return correct, answer


def ask_short_answer(q: dict) -> tuple[bool, str]:
    """Handle short answer question with keyword checking."""
    print(f"\n{q['stem']}\n")
    
    answer = input("Your answer: ").strip()
    
    keywords_found = sum(1 for kw in q["keywords"] if kw.lower() in answer.lower())
    min_required = q.get("min_keywords", 1)
    correct = keywords_found >= min_required
    
    return correct, answer


# Question type dispatcher
QUESTION_HANDLERS: dict[str, Callable[[dict], tuple[bool, str]]] = {
    "multiple_choice": ask_multiple_choice,
    "fill_blank": ask_fill_blank,
    "true_false": ask_true_false,
    "numeric": ask_numeric,
    "command": ask_command,
    "code_trace": ask_code_trace,
    "matching": ask_matching,
    "short_answer": ask_short_answer,
}


# ═══════════════════════════════════════════════════════════════════════════════
# FEEDBACK_DISPLAY
# ═══════════════════════════════════════════════════════════════════════════════
def show_feedback(q: dict, correct: bool, user_answer: str) -> None:
    """Display feedback after answering a question."""
    if correct:
        feedback = q.get("feedback", {}).get("correct", "✅ Correct!")
        print(f"\n{feedback}")
    else:
        feedback = q.get("feedback", {}).get("incorrect", "❌ Incorrect.")
        print(f"\n{feedback}")
        
        # Show correct answer
        if q["type"] == "multiple_choice":
            correct_opt = q["correct"]
            print(f"   Correct answer: {correct_opt}) {q['options'][correct_opt]}")
        elif q["type"] == "true_false":
            print(f"   Correct answer: {q['correct']}")
        elif q["type"] in ["fill_blank", "command", "code_trace"]:
            if isinstance(q["correct"], list):
                print(f"   Accepted answers: {', '.join(q['correct'][:3])}")
            else:
                print(f"   Correct answer: {q['correct']}")
        
        # Show explanation
        if q.get("explanation"):
            explanation = q["explanation"].strip()
            if len(explanation) > 200:
                explanation = explanation[:200] + "..."
            print(f"   📖 {explanation}")
        
        # Reference to misconception
        if q.get("misconception_ref"):
            print(f"   📚 See: {q['misconception_ref']}")


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_RUNNER
# ═══════════════════════════════════════════════════════════════════════════════
def run_quiz(
    quiz: dict,
    section: Optional[str] = None,
    randomize: bool = False,
    limit: Optional[int] = None,
    review_mode: bool = False
) -> QuizResult:
    """
    Run interactive quiz session.
    
    Args:
        quiz: Loaded quiz dictionary
        section: Specific section to run (None = all)
        randomize: Shuffle question order
        limit: Maximum number of questions
        review_mode: Show answers without asking
    
    Returns:
        QuizResult with scores and analysis
    """
    result = QuizResult()
    start_time = time.time()
    
    # Build question list
    questions = []
    question_map = {q["id"]: q for q in quiz["questions"]}
    
    if section:
        # Find section and get its questions
        for sec in quiz.get("sections", []):
            if sec["id"] == section:
                questions = [question_map[qid] for qid in sec["questions"] if qid in question_map]
                break
        if not questions:
            print(f"⚠️ Section '{section}' not found or empty")
            return result
    else:
        questions = quiz["questions"]
    
    if randomize:
        questions = questions.copy()
        random.shuffle(questions)
    
    if limit:
        questions = questions[:limit]
    
    # Print header
    meta = quiz["metadata"]
    print("\n" + "=" * 70)
    print(f"📝 QUIZ: {meta['topic']} — Week {meta['week']}")
    print(f"   Questions: {len(questions)} | Passing: {meta['passing_score']}%")
    if section:
        for sec in quiz.get("sections", []):
            if sec["id"] == section:
                print(f"   Section: {sec['name']}")
                break
    print("=" * 70)
    
    if review_mode:
        print("\n📖 REVIEW MODE — Answers will be shown\n")
    
    # Ask each question
    for i, q in enumerate(questions, 1):
        points = q.get("points", 1)
        result.total_questions += 1
        result.total_points += points
        
        # Track LO
        lo = q.get("lo_ref", "Unknown")
        result.lo_total[lo] = result.lo_total.get(lo, 0) + 1
        
        print(f"\n{'─' * 60}")
        difficulty_emoji = {"basic": "🟢", "intermediate": "🟡", "advanced": "🔴"}.get(
            q.get("difficulty", ""), "⚪"
        )
        print(f"Question {i}/{len(questions)} {difficulty_emoji} [{q.get('difficulty', '?')}] "
              f"[{lo}] [{points}pt{'s' if points > 1 else ''}]")
        
        if review_mode:
            # Review mode - just show question and answer
            print(f"\n{q['stem']}")
            if q["type"] == "multiple_choice":
                for key, val in q["options"].items():
                    marker = "✓" if key == q["correct"] else " "
                    print(f"  [{marker}] {key}) {val}")
            elif q["type"] == "true_false":
                print(f"  Answer: {q['correct']}")
            elif q["type"] in ["fill_blank", "command", "code_trace"]:
                answers = q["correct"] if isinstance(q["correct"], list) else [q["correct"]]
                print(f"  Answer: {answers[0]}")
            elif q["type"] == "matching":
                print("  Correct matches:")
                for pair in q["pairs"]:
                    print(f"    {pair['left']} → {pair['right']}")
            
            if q.get("explanation"):
                print(f"\n  📖 Explanation: {q['explanation'][:300]}...")
            
            input("\nPress Enter for next question...")
            continue
        
        # Interactive mode - ask question
        handler = QUESTION_HANDLERS.get(q["type"])
        if handler:
            try:
                correct, user_answer = handler(q)
            except KeyboardInterrupt:
                print("\n\n⚠️ Quiz interrupted by user")
                break
            
            if correct:
                result.correct_answers += 1
                result.earned_points += points
                result.lo_coverage[lo] = result.lo_coverage.get(lo, 0) + 1
            
            result.question_results.append({
                "id": q["id"],
                "correct": correct,
                "user_answer": user_answer,
                "lo": lo
            })
            
            show_feedback(q, correct, user_answer)
        else:
            print(f"⚠️ Unknown question type: {q['type']}")
    
    # Calculate results
    result.time_taken_seconds = time.time() - start_time
    if result.total_points > 0:
        result.score_percentage = (result.earned_points / result.total_points) * 100
    
    # Calculate LO coverage percentages and identify weak areas
    for lo in result.lo_total:
        correct_count = result.lo_coverage.get(lo, 0)
        total_count = result.lo_total[lo]
        pct = (correct_count / total_count) * 100 if total_count > 0 else 0
        result.lo_coverage[lo] = pct
        if pct < 70:
            result.weak_areas.append(lo)
    
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# OUTPUT_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def display_results(result: QuizResult, quiz: dict) -> None:
    """Display quiz results with recommendations."""
    print("\n" + "=" * 70)
    print("📊 QUIZ RESULTS")
    print("=" * 70)
    
    # Score summary
    print(f"\n  Questions: {result.correct_answers}/{result.total_questions} correct")
    print(f"  Points:    {result.earned_points}/{result.total_points} ({result.score_percentage:.1f}%)")
    print(f"  Time:      {result.time_taken_seconds:.0f} seconds")
    
    # Determine grade
    grading = quiz.get("grading_scale", [])
    grade_info = None
    for gi in grading:
        low, high = gi["range"]
        if low <= result.score_percentage <= high:
            grade_info = gi
            break
    
    if grade_info:
        print(f"\n  {grade_info['emoji']} Grade: {grade_info['grade']}")
        print(f"     {grade_info['message']}")
        if grade_info.get("recommendation"):
            print(f"     💡 {grade_info['recommendation']}")
    
    # LO Coverage breakdown
    if result.lo_coverage:
        print("\n  Learning Objective Coverage:")
        for lo in sorted(result.lo_coverage.keys()):
            pct = result.lo_coverage[lo]
            bar_filled = int(pct // 10)
            bar = "█" * bar_filled + "░" * (10 - bar_filled)
            status = "✅" if pct >= 70 else "⚠️" if pct >= 50 else "❌"
            print(f"    {status} {lo}: {bar} {pct:.0f}%")
    
    # Weak areas recommendations
    if result.weak_areas:
        print("\n  📚 Areas Needing Review:")
        for lo in result.weak_areas:
            print(f"    • {lo}: See docs/theory_summary.md and docs/misconceptions.md")
    
    # Pass/Fail determination
    passing = quiz["metadata"]["passing_score"]
    print("\n" + "─" * 70)
    if result.score_percentage >= passing:
        print(f"  ✅ PASSED (threshold: {passing}%)")
        print("     You may proceed to homework assignments.")
    else:
        print(f"  ❌ NEEDS REVIEW (threshold: {passing}%)")
        print("     Review the materials and retake the quiz.")
    
    print("\n" + "=" * 70)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """
    Main entry point for the quiz runner.
    
    Returns:
        0 if quiz passed, 1 if failed or error
    """
    parser = argparse.ArgumentParser(
        description="Run formative quiz for Week 1 - Network Fundamentals",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python formative/run_quiz.py                     # Full quiz
  python formative/run_quiz.py --section pre_lab   # Pre-lab section only
  python formative/run_quiz.py --section exit_ticket  # Exit ticket only
  python formative/run_quiz.py --random --limit 5  # Random 5 questions
  python formative/run_quiz.py --review            # Review mode (see answers)
  python formative/run_quiz.py --list-sections     # List available sections

Section IDs:
  pre_lab      - Pre-Lab Quick Check (5 questions, 5 min)
  during_lab   - During-Lab Checkpoints (5 questions)
  exit_ticket  - Exit Ticket (5 questions, 10 min)
        """
    )
    parser.add_argument(
        "--quiz", "-q",
        type=Path,
        default=None,
        help="Path to quiz YAML file (default: formative/quiz.yaml)"
    )
    parser.add_argument(
        "--section", "-s",
        help="Run specific section (pre_lab, during_lab, exit_ticket)"
    )
    parser.add_argument(
        "--random", "-r",
        action="store_true",
        help="Randomize question order"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        help="Limit number of questions"
    )
    parser.add_argument(
        "--review",
        action="store_true",
        help="Review mode - show answers without asking"
    )
    parser.add_argument(
        "--list-sections",
        action="store_true",
        help="List available sections and exit"
    )
    
    args = parser.parse_args()
    
    # Determine quiz file path
    if args.quiz:
        quiz_path = args.quiz
    else:
        # Try relative to script location first
        script_dir = Path(__file__).parent
        quiz_path = script_dir / "quiz.yaml"
        if not quiz_path.exists():
            # Try current directory
            quiz_path = Path("formative/quiz.yaml")
    
    # Load quiz
    try:
        quiz = load_quiz(quiz_path)
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("   Make sure you're in the correct directory or specify --quiz path")
        return 1
    except ValueError as e:
        print(f"❌ Invalid quiz file: {e}")
        return 1
    except yaml.YAMLError as e:
        print(f"❌ YAML parsing error: {e}")
        return 1
    
    # List sections mode
    if args.list_sections:
        print("\n📋 Available Quiz Sections:\n")
        for sec in quiz.get("sections", []):
            q_count = len(sec.get("questions", []))
            time_limit = sec.get("time_limit_minutes", 0)
            time_str = f"{time_limit} min" if time_limit else "No limit"
            print(f"  {sec['id']:15} — {sec['name']}")
            print(f"                    {q_count} questions, {time_str}")
            if sec.get("description"):
                print(f"                    {sec['description']}")
            print()
        return 0
    
    # Run quiz
    try:
        result = run_quiz(
            quiz,
            section=args.section,
            randomize=args.random,
            limit=args.limit,
            review_mode=args.review
        )
    except KeyboardInterrupt:
        print("\n\n⚠️ Quiz cancelled by user")
        return 1
    
    # Display results (skip in review mode)
    if not args.review and result.total_questions > 0:
        display_results(result, quiz)
    
    # Return exit code based on pass/fail
    passing = quiz["metadata"]["passing_score"]
    return 0 if result.score_percentage >= passing else 1


if __name__ == "__main__":
    sys.exit(main())
