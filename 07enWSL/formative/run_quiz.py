#!/usr/bin/env python3
"""
Formative Quiz Runner — Week 7
==============================
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Interactive quiz runner for self-assessment of packet capture and filtering concepts.

Usage:
    python3 formative/run_quiz.py                    # Run full quiz
    python3 formative/run_quiz.py --random           # Randomize question order
    python3 formative/run_quiz.py --limit 5          # Limit to 5 questions
    python3 formative/run_quiz.py --lo LO1 LO2       # Filter by learning objectives
    python3 formative/run_quiz.py --difficulty basic # Filter by difficulty
    python3 formative/run_quiz.py --review           # Review mode (show answers)
    python3 formative/run_quiz.py --export results.json  # Export results

Exit codes:
    0 - Quiz passed (score >= passing threshold)
    1 - Quiz failed (score < passing threshold)
    2 - Error (file not found, invalid YAML, etc.)
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import json
import random
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(2)


# ═══════════════════════════════════════════════════════════════════════════════
# DATA CLASSES
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class QuizResult:
    """Stores the result of a single question attempt."""
    question_id: str
    lo_ref: str
    difficulty: str
    points_possible: int
    points_earned: int
    correct: bool
    user_answer: str
    correct_answer: str
    time_taken: float


@dataclass
class QuizSession:
    """Stores the complete quiz session data."""
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    results: list[QuizResult] = field(default_factory=list)
    total_points: int = 0
    earned_points: int = 0
    
    @property
    def score_percentage(self) -> float:
        """Calculate score as percentage."""
        if self.total_points == 0:
            return 0.0
        return (self.earned_points / self.total_points) * 100
    
    @property
    def duration_seconds(self) -> float:
        """Calculate total quiz duration."""
        if self.end_time is None:
            return 0.0
        return (self.end_time - self.start_time).total_seconds()
    
    def to_dict(self) -> dict[str, Any]:
        """Convert session to dictionary for JSON export."""
        return {
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": self.duration_seconds,
            "total_points": self.total_points,
            "earned_points": self.earned_points,
            "score_percentage": self.score_percentage,
            "results": [
                {
                    "question_id": r.question_id,
                    "lo_ref": r.lo_ref,
                    "difficulty": r.difficulty,
                    "points_possible": r.points_possible,
                    "points_earned": r.points_earned,
                    "correct": r.correct,
                    "user_answer": r.user_answer,
                    "correct_answer": r.correct_answer,
                    "time_taken": r.time_taken
                }
                for r in self.results
            ]
        }


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ LOADER
# ═══════════════════════════════════════════════════════════════════════════════
def load_quiz(path: Path) -> dict[str, Any]:
    """
    Load quiz from YAML file.
    
    Args:
        path: Path to quiz YAML file
        
    Returns:
        Parsed quiz dictionary
        
    Raises:
        FileNotFoundError: If quiz file doesn't exist
        yaml.YAMLError: If YAML parsing fails
    """
    if not path.exists():
        raise FileNotFoundError(f"Quiz file not found: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def filter_questions(
    questions: list[dict],
    lo_filter: Optional[list[str]] = None,
    difficulty_filter: Optional[str] = None
) -> list[dict]:
    """
    Filter questions by learning objective and/or difficulty.
    
    Args:
        questions: List of question dictionaries
        lo_filter: List of LO IDs to include (e.g., ["LO1", "LO2"])
        difficulty_filter: Difficulty level ("basic", "intermediate", "advanced")
        
    Returns:
        Filtered list of questions
    """
    filtered = questions
    
    if lo_filter:
        filtered = [q for q in filtered if q.get("lo_ref") in lo_filter]
    
    if difficulty_filter:
        filtered = [q for q in filtered if q.get("difficulty") == difficulty_filter]
    
    return filtered


# ═══════════════════════════════════════════════════════════════════════════════
# QUESTION HANDLERS
# ═══════════════════════════════════════════════════════════════════════════════
def display_question_header(index: int, total: int, question: dict) -> None:
    """Display question header with metadata."""
    print()
    print("═" * 70)
    print(f"  Question {index}/{total}  │  {question.get('lo_ref', '?')}  │  "
          f"{question.get('difficulty', '?').upper()}  │  "
          f"{question.get('points', 1)} pts")
    print("═" * 70)
    print()


def handle_multiple_choice(question: dict, review_mode: bool = False) -> tuple[str, bool]:
    """
    Handle multiple choice question.
    
    Args:
        question: Question dictionary
        review_mode: If True, show correct answer immediately
        
    Returns:
        Tuple of (user_answer, is_correct)
    """
    print(f"📝 {question['stem']}")
    print()
    
    options = question.get("options", {})
    for key, value in sorted(options.items()):
        print(f"   {key}) {value}")
    
    print()
    
    if review_mode:
        correct = question.get("correct", "?")
        print(f"   ✅ Correct answer: {correct}")
        print()
        if "explanation" in question:
            print(f"   📖 {question['explanation'].strip()}")
        return correct, True
    
    while True:
        answer = input("   Your answer (a/b/c/d): ").strip().lower()
        if answer in options:
            break
        print("   ⚠️  Invalid option. Please enter a, b, c, or d.")
    
    correct = question.get("correct", "").lower()
    is_correct = answer == correct
    
    if is_correct:
        print("   ✅ Correct!")
    else:
        print(f"   ❌ Incorrect. Correct answer: {correct}")
    
    if "explanation" in question:
        print()
        print(f"   📖 {question['explanation'].strip()}")
    
    return answer, is_correct


def handle_fill_blank(question: dict, review_mode: bool = False) -> tuple[str, bool]:
    """
    Handle fill-in-the-blank question.
    
    Args:
        question: Question dictionary
        review_mode: If True, show correct answer immediately
        
    Returns:
        Tuple of (user_answer, is_correct)
    """
    print(f"📝 {question['stem']}")
    print()
    
    if "template" in question:
        print(f"   Template: {question['template']}")
        print()
    
    correct_answers = question.get("correct", [])
    if isinstance(correct_answers, str):
        correct_answers = [correct_answers]
    
    if review_mode:
        print(f"   ✅ Correct answer(s): {', '.join(correct_answers)}")
        if "explanation" in question:
            print()
            print(f"   📖 {question['explanation'].strip()}")
        return correct_answers[0], True
    
    # For multi-blank questions
    if isinstance(correct_answers[0], list) or len(correct_answers) > 1:
        user_answers = []
        for i, _ in enumerate(correct_answers):
            answer = input(f"   Blank {i+1}: ").strip()
            user_answers.append(answer)
        
        # Check if all blanks match
        is_correct = all(
            ua.lower() == ca.lower() 
            for ua, ca in zip(user_answers, correct_answers)
        )
        user_answer = ", ".join(user_answers)
    else:
        user_answer = input("   Your answer: ").strip()
        # Check against acceptable variants
        acceptable = question.get("acceptable_variants", [])
        all_correct = [correct_answers[0]] + [v[0] if isinstance(v, list) else v for v in acceptable]
        is_correct = user_answer.lower() in [a.lower() for a in all_correct]
    
    if is_correct:
        print("   ✅ Correct!")
    else:
        print(f"   ❌ Incorrect. Correct answer: {correct_answers}")
    
    if "explanation" in question:
        print()
        print(f"   📖 {question['explanation'].strip()}")
    
    return user_answer, is_correct


def handle_ordering(question: dict, review_mode: bool = False) -> tuple[str, bool]:
    """
    Handle ordering/sequencing question.
    
    Args:
        question: Question dictionary
        review_mode: If True, show correct answer immediately
        
    Returns:
        Tuple of (user_answer, is_correct)
    """
    print(f"📝 {question['stem']}")
    print()
    print("   Items to order:")
    
    items = question.get("items", [])
    for item in items:
        print(f"   {item['id']}) {item['text']}")
    
    print()
    
    correct_order = question.get("correct_order", [])
    
    if review_mode:
        print(f"   ✅ Correct order: {' → '.join(correct_order)}")
        if "explanation" in question:
            print()
            print(f"   📖 {question['explanation'].strip()}")
        return ",".join(correct_order), True
    
    user_input = input("   Your order (e.g., A,C,B): ").strip().upper()
    user_order = [x.strip() for x in user_input.split(",")]
    
    is_correct = user_order == correct_order
    
    if is_correct:
        print("   ✅ Correct!")
    else:
        print(f"   ❌ Incorrect. Correct order: {' → '.join(correct_order)}")
    
    if "explanation" in question:
        print()
        print(f"   📖 {question['explanation'].strip()}")
    
    return user_input, is_correct


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN QUIZ RUNNER
# ═══════════════════════════════════════════════════════════════════════════════
def run_quiz(
    quiz: dict,
    randomize: bool = False,
    limit: Optional[int] = None,
    lo_filter: Optional[list[str]] = None,
    difficulty_filter: Optional[str] = None,
    review_mode: bool = False
) -> QuizSession:
    """
    Run the interactive quiz session.
    
    Args:
        quiz: Parsed quiz dictionary
        randomize: Shuffle question order
        limit: Maximum number of questions
        lo_filter: Filter by learning objectives
        difficulty_filter: Filter by difficulty
        review_mode: Show answers without requiring input
        
    Returns:
        QuizSession with results
    """
    session = QuizSession()
    
    # Get and filter questions
    questions = quiz.get("questions", [])
    questions = filter_questions(questions, lo_filter, difficulty_filter)
    
    if not questions:
        print("⚠️  No questions match the specified filters.")
        return session
    
    if randomize:
        random.shuffle(questions)
    
    if limit and limit < len(questions):
        questions = questions[:limit]
    
    # Display header
    metadata = quiz.get("metadata", {})
    print()
    print("╔" + "═" * 68 + "╗")
    print(f"║  {'FORMATIVE QUIZ — Week 7':^64}  ║")
    print(f"║  {metadata.get('topic', 'Packet Interception and Filtering'):^64}  ║")
    print("╠" + "═" * 68 + "╣")
    print(f"║  Questions: {len(questions):<5}  │  Passing: {metadata.get('passing_score', 70)}%  │  "
          f"Time: ~{metadata.get('estimated_time', '15 min'):<10}  ║")
    print("╚" + "═" * 68 + "╝")
    
    if not review_mode:
        print()
        input("Press Enter to start...")
    
    # Process each question
    handlers = {
        "multiple_choice": handle_multiple_choice,
        "fill_blank": handle_fill_blank,
        "ordering": handle_ordering,
    }
    
    for i, question in enumerate(questions, 1):
        display_question_header(i, len(questions), question)
        
        q_type = question.get("type", "multiple_choice")
        handler = handlers.get(q_type, handle_multiple_choice)
        
        start_time = time.time()
        user_answer, is_correct = handler(question, review_mode)
        elapsed = time.time() - start_time
        
        points = question.get("points", 1)
        earned = points if is_correct else 0
        
        result = QuizResult(
            question_id=question.get("id", f"q{i}"),
            lo_ref=question.get("lo_ref", "?"),
            difficulty=question.get("difficulty", "?"),
            points_possible=points,
            points_earned=earned,
            correct=is_correct,
            user_answer=str(user_answer),
            correct_answer=str(question.get("correct", "?")),
            time_taken=elapsed
        )
        
        session.results.append(result)
        session.total_points += points
        session.earned_points += earned
        
        if not review_mode:
            print()
            input("Press Enter for next question...")
    
    session.end_time = datetime.now()
    return session


def display_results(session: QuizSession, quiz: dict) -> None:
    """Display final quiz results and feedback."""
    print()
    print("╔" + "═" * 68 + "╗")
    print(f"║  {'QUIZ COMPLETE':^64}  ║")
    print("╠" + "═" * 68 + "╣")
    
    score_pct = session.score_percentage
    duration = session.duration_seconds
    
    print(f"║  Score: {session.earned_points}/{session.total_points} "
          f"({score_pct:.1f}%)  │  Time: {duration:.0f} seconds{' ' * 20}║")
    
    # Determine grade
    scoring = quiz.get("scoring", {})
    grade_boundaries = scoring.get("grade_boundaries", {"A": 90, "B": 80, "C": 70, "D": 60, "F": 0})
    
    grade = "F"
    for g, threshold in sorted(grade_boundaries.items(), key=lambda x: -x[1]):
        if score_pct >= threshold:
            grade = g
            break
    
    passing = quiz.get("metadata", {}).get("passing_score", 70)
    passed = score_pct >= passing
    
    status = "✅ PASSED" if passed else "❌ NEEDS REVIEW"
    print(f"║  Grade: {grade}  │  Status: {status}{' ' * 35}║")
    
    print("╠" + "═" * 68 + "╣")
    
    # LO breakdown
    print(f"║  {'Performance by Learning Objective':^64}  ║")
    print("╟" + "─" * 68 + "╢")
    
    lo_stats: dict[str, dict[str, int]] = {}
    for r in session.results:
        if r.lo_ref not in lo_stats:
            lo_stats[r.lo_ref] = {"correct": 0, "total": 0}
        lo_stats[r.lo_ref]["total"] += 1
        if r.correct:
            lo_stats[r.lo_ref]["correct"] += 1
    
    for lo, stats in sorted(lo_stats.items()):
        pct = (stats["correct"] / stats["total"]) * 100 if stats["total"] > 0 else 0
        bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
        status_icon = "✅" if pct >= 70 else "⚠️" if pct >= 50 else "❌"
        print(f"║  {lo}: {bar} {pct:5.1f}% ({stats['correct']}/{stats['total']}) {status_icon}{' ' * 20}║")
    
    print("╠" + "═" * 68 + "╣")
    
    # Feedback message
    feedback = quiz.get("feedback_messages", {})
    if score_pct >= 90:
        msg = feedback.get("excellent", "Excellent work!")
    elif score_pct >= 70:
        msg = feedback.get("good", "Good job!")
    elif score_pct >= 50:
        msg = feedback.get("needs_work", "Review the material.")
    else:
        msg = feedback.get("insufficient", "Please study again.")
    
    # Word wrap feedback
    words = msg.split()
    lines = []
    current = ""
    for word in words:
        if len(current) + len(word) + 1 <= 62:
            current = current + " " + word if current else word
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    
    for line in lines:
        print(f"║  {line:<64}  ║")
    
    print("╚" + "═" * 68 + "╝")


# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════
def build_parser() -> argparse.ArgumentParser:
    """Build command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Formative Quiz Runner for Week 7",
        epilog="Exit codes: 0=passed, 1=failed, 2=error"
    )
    
    parser.add_argument(
        "--quiz", "-q",
        type=Path,
        default=Path(__file__).parent / "quiz.yaml",
        help="Path to quiz YAML file (default: formative/quiz.yaml)"
    )
    
    parser.add_argument(
        "--random", "-r",
        action="store_true",
        help="Randomize question order"
    )
    
    parser.add_argument(
        "--limit", "-n",
        type=int,
        help="Maximum number of questions"
    )
    
    parser.add_argument(
        "--lo",
        nargs="+",
        help="Filter by learning objectives (e.g., --lo LO1 LO2)"
    )
    
    parser.add_argument(
        "--difficulty", "-d",
        choices=["basic", "intermediate", "advanced"],
        help="Filter by difficulty level"
    )
    
    parser.add_argument(
        "--review",
        action="store_true",
        help="Review mode - show answers without input"
    )
    
    parser.add_argument(
        "--export", "-e",
        type=Path,
        help="Export results to JSON file"
    )
    
    return parser


def main() -> int:
    """
    Main entry point.
    
    Returns:
        Exit code: 0 if passed, 1 if failed, 2 if error
    """
    parser = build_parser()
    args = parser.parse_args()
    
    try:
        quiz = load_quiz(args.quiz)
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        return 2
    except yaml.YAMLError as e:
        print(f"ERROR: Invalid YAML: {e}")
        return 2
    
    session = run_quiz(
        quiz,
        randomize=args.random,
        limit=args.limit,
        lo_filter=args.lo,
        difficulty_filter=args.difficulty,
        review_mode=args.review
    )
    
    display_results(session, quiz)
    
    if args.export:
        try:
            with open(args.export, "w", encoding="utf-8") as f:
                json.dump(session.to_dict(), f, indent=2)
            print(f"\n📄 Results exported to: {args.export}")
        except IOError as e:
            print(f"\n⚠️  Failed to export results: {e}")
    
    passing = quiz.get("metadata", {}).get("passing_score", 70)
    return 0 if session.score_percentage >= passing else 1


if __name__ == "__main__":
    sys.exit(main())
