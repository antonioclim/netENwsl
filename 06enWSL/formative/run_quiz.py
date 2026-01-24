#!/usr/bin/env python3
"""
Formative Quiz Runner — Week 6: NAT/PAT & SDN
=============================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Interactive CLI quiz for self-assessment before laboratory sessions.

Usage:
    python formative/run_quiz.py                    # Run full quiz
    python formative/run_quiz.py --random           # Randomise question order
    python formative/run_quiz.py --limit 5          # Limit to 5 questions
    python formative/run_quiz.py --lo LO1 LO2       # Filter by Learning Objectives
    python formative/run_quiz.py --difficulty basic # Filter by difficulty
    python formative/run_quiz.py --review           # Review mode (show answers)
    python formative/run_quiz.py --export results.json  # Export results

Requirements:
    pip install pyyaml --break-system-packages
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

DEFAULT_QUIZ_PATH = Path(__file__).parent / "quiz.yaml"
PASSING_SCORE = 70  # percent


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Question:
    """Represents a single quiz question."""
    id: str
    type: str
    lo_ref: str
    bloom_level: str
    difficulty: str
    stem: str
    correct: Any
    explanation: str
    options: Optional[Dict[str, str]] = None
    hint: Optional[str] = None
    misconception_ref: Optional[str] = None


@dataclass
class QuizResult:
    """Stores quiz attempt results."""
    timestamp: str
    total_questions: int
    correct_answers: int
    score_percent: float
    passed: bool
    time_taken_seconds: float
    questions_answered: List[Dict[str, Any]] = field(default_factory=list)
    lo_performance: Dict[str, Dict[str, int]] = field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════════════════════
# YAML_LOADING
# ═══════════════════════════════════════════════════════════════════════════════

def load_quiz(path: Path) -> Dict[str, Any]:
    """
    Load quiz from YAML file.
    
    Args:
        path: Path to quiz.yaml file
        
    Returns:
        Parsed quiz dictionary
        
    Raises:
        FileNotFoundError: If quiz file doesn't exist
        ValueError: If YAML parsing fails
    """
    try:
        import yaml
    except ImportError:
        print("ERROR: PyYAML not installed.")
        print("Install with: pip install pyyaml --break-system-packages")
        sys.exit(1)
    
    if not path.exists():
        raise FileNotFoundError(f"Quiz file not found: {path}")
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in quiz file: {e}")


def parse_questions(quiz_data: Dict[str, Any]) -> List[Question]:
    """Parse raw quiz data into Question objects."""
    questions = []
    for q in quiz_data.get("questions", []):
        questions.append(Question(
            id=q["id"],
            type=q["type"],
            lo_ref=q["lo_ref"],
            bloom_level=q["bloom_level"],
            difficulty=q["difficulty"],
            stem=q["stem"].strip(),
            correct=q["correct"],
            explanation=q["explanation"],
            options=q.get("options"),
            hint=q.get("hint"),
            misconception_ref=q.get("misconception_ref"),
        ))
    return questions


# ═══════════════════════════════════════════════════════════════════════════════
# FILTERING
# ═══════════════════════════════════════════════════════════════════════════════

def filter_questions(
    questions: List[Question],
    lo_filter: Optional[Set[str]] = None,
    difficulty_filter: Optional[str] = None,
) -> List[Question]:
    """Filter questions by Learning Objective and/or difficulty."""
    filtered = questions
    
    if lo_filter:
        filtered = [q for q in filtered if q.lo_ref in lo_filter]
    
    if difficulty_filter:
        filtered = [q for q in filtered if q.difficulty == difficulty_filter]
    
    return filtered


# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def print_header(quiz_data: Dict[str, Any]) -> None:
    """Print quiz header with metadata."""
    metadata = quiz_data.get("metadata", {})
    
    print()
    print("═" * 70)
    print("  FORMATIVE QUIZ — Week 6: NAT/PAT & SDN")
    print("  Computer Networks — ASE, CSIE")
    print("═" * 70)
    print()
    print(f"  Topic:         {metadata.get('topic', 'Unknown')}")
    print(f"  Questions:     {metadata.get('total_questions', '?')}")
    print(f"  Time estimate: {metadata.get('estimated_time', '?')}")
    print(f"  Passing score: {metadata.get('passing_score', 70)}%")
    print()
    print("  Instructions:")
    print("  • Answer each question by typing the letter (a/b/c/d) or text")
    print("  • Press Enter to submit your answer")
    print("  • Type 'hint' for a hint (if available)")
    print("  • Type 'skip' to skip a question")
    print("  • Type 'quit' to exit early")
    print()
    print("═" * 70)
    print()


def display_question(q: Question, number: int, total: int) -> None:
    """Display a single question."""
    print(f"\n{'─' * 70}")
    print(f"Question {number}/{total}  [{q.lo_ref}] [{q.difficulty.upper()}] [{q.bloom_level}]")
    print(f"{'─' * 70}")
    print()
    print(q.stem)
    print()
    
    if q.type == "multiple_choice" and q.options:
        for key, value in sorted(q.options.items()):
            print(f"   {key}) {value}")
        print()


def display_feedback(
    q: Question,
    user_answer: str,
    is_correct: bool,
    show_explanation: bool = True,
) -> None:
    """Display feedback after answering."""
    if is_correct:
        print("\n✅ CORRECT!")
    else:
        print("\n❌ INCORRECT")
        if q.type == "multiple_choice":
            print(f"   Correct answer: {q.correct}")
        else:
            correct_list = q.correct if isinstance(q.correct, list) else [q.correct]
            print(f"   Accepted answers: {', '.join(correct_list)}")
    
    if show_explanation:
        print(f"\n📖 {q.explanation}")
        
        if q.misconception_ref:
            print(f"\n⚠️  Related misconception: {q.misconception_ref}")


def display_results(result: QuizResult, quiz_data: Dict[str, Any]) -> None:
    """Display final quiz results."""
    print()
    print("═" * 70)
    print("  QUIZ RESULTS")
    print("═" * 70)
    print()
    print(f"  Score:    {result.correct_answers}/{result.total_questions} "
          f"({result.score_percent:.1f}%)")
    print(f"  Status:   {'✅ PASSED' if result.passed else '❌ NEEDS REVIEW'}")
    print(f"  Time:     {result.time_taken_seconds:.0f} seconds")
    print()
    
    # LO breakdown
    print("  Performance by Learning Objective:")
    for lo, stats in sorted(result.lo_performance.items()):
        correct = stats.get("correct", 0)
        total = stats.get("total", 0)
        pct = (correct / total * 100) if total > 0 else 0
        bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
        print(f"    {lo}: {bar} {correct}/{total} ({pct:.0f}%)")
    
    print()
    print("═" * 70)
    
    # Post-quiz guidance
    post_quiz = quiz_data.get("post_quiz", {})
    if result.passed:
        guidance = post_quiz.get("if_above_passing", "")
    else:
        guidance = post_quiz.get("if_below_passing", "")
    
    if guidance:
        print("\n📚 Recommended next steps:")
        for line in guidance.strip().split("\n"):
            print(f"   {line}")
        print()


# ═══════════════════════════════════════════════════════════════════════════════
# ANSWER_CHECKING
# ═══════════════════════════════════════════════════════════════════════════════

def check_answer(q: Question, user_answer: str) -> bool:
    """
    Check if user's answer is correct.
    
    Args:
        q: Question object
        user_answer: User's input (stripped and lowercased)
        
    Returns:
        True if correct, False otherwise
    """
    user_answer = user_answer.strip().lower()
    
    if q.type == "multiple_choice":
        return user_answer == q.correct.lower()
    
    elif q.type == "fill_blank":
        correct_answers = q.correct if isinstance(q.correct, list) else [q.correct]
        return user_answer in [a.lower() for a in correct_answers]
    
    return False


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def run_quiz(
    questions: List[Question],
    quiz_data: Dict[str, Any],
    randomize: bool = False,
    limit: Optional[int] = None,
    review_mode: bool = False,
) -> QuizResult:
    """
    Run the interactive quiz.
    
    Args:
        questions: List of Question objects to ask
        quiz_data: Full quiz data for metadata
        randomize: Whether to shuffle question order
        limit: Maximum number of questions to ask
        review_mode: Show correct answers immediately
        
    Returns:
        QuizResult with attempt statistics
    """
    if randomize:
        questions = questions.copy()
        random.shuffle(questions)
    
    if limit and limit < len(questions):
        questions = questions[:limit]
    
    total = len(questions)
    correct = 0
    answered = []
    lo_stats: Dict[str, Dict[str, int]] = {}
    
    start_time = time.time()
    
    for i, q in enumerate(questions, 1):
        display_question(q, i, total)
        
        # Initialise LO stats
        if q.lo_ref not in lo_stats:
            lo_stats[q.lo_ref] = {"correct": 0, "total": 0}
        lo_stats[q.lo_ref]["total"] += 1
        
        while True:
            user_input = input("Your answer: ").strip()
            
            if user_input.lower() == "quit":
                print("\n⚠️  Quiz ended early.")
                break
            
            if user_input.lower() == "skip":
                print("⏭️  Skipped")
                answered.append({
                    "question_id": q.id,
                    "user_answer": None,
                    "correct": False,
                    "skipped": True,
                })
                break
            
            if user_input.lower() == "hint" and q.hint:
                print(f"\n💡 Hint: {q.hint}\n")
                continue
            
            if not user_input:
                print("Please enter an answer (or 'skip'/'quit')")
                continue
            
            # Check answer
            is_correct = check_answer(q, user_input)
            
            if is_correct:
                correct += 1
                lo_stats[q.lo_ref]["correct"] += 1
            
            display_feedback(q, user_input, is_correct, show_explanation=True)
            
            answered.append({
                "question_id": q.id,
                "user_answer": user_input,
                "correct": is_correct,
                "skipped": False,
            })
            break
        
        if user_input.lower() == "quit":
            break
    
    end_time = time.time()
    
    # Calculate results
    score_pct = (correct / total * 100) if total > 0 else 0
    passing = quiz_data.get("metadata", {}).get("passing_score", PASSING_SCORE)
    
    result = QuizResult(
        timestamp=datetime.now().isoformat(),
        total_questions=total,
        correct_answers=correct,
        score_percent=score_pct,
        passed=score_pct >= passing,
        time_taken_seconds=end_time - start_time,
        questions_answered=answered,
        lo_performance=lo_stats,
    )
    
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def export_results(result: QuizResult, path: Path) -> None:
    """Export quiz results to JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": result.timestamp,
            "total_questions": result.total_questions,
            "correct_answers": result.correct_answers,
            "score_percent": result.score_percent,
            "passed": result.passed,
            "time_taken_seconds": result.time_taken_seconds,
            "questions_answered": result.questions_answered,
            "lo_performance": result.lo_performance,
        }, f, indent=2)
    
    print(f"\n📁 Results exported to: {path}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Formative Quiz Runner — Week 6: NAT/PAT & SDN",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_quiz.py                     # Run full quiz
  python run_quiz.py --random --limit 5  # 5 random questions
  python run_quiz.py --lo LO1 LO2        # Only LO1 and LO2 questions
  python run_quiz.py --difficulty basic  # Only basic questions
        """
    )
    
    parser.add_argument(
        "--quiz", "-q",
        type=Path,
        default=DEFAULT_QUIZ_PATH,
        help="Path to quiz YAML file"
    )
    parser.add_argument(
        "--random", "-r",
        action="store_true",
        help="Randomise question order"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        help="Limit number of questions"
    )
    parser.add_argument(
        "--lo",
        nargs="+",
        help="Filter by Learning Objectives (e.g., --lo LO1 LO2)"
    )
    parser.add_argument(
        "--difficulty", "-d",
        choices=["basic", "intermediate", "advanced"],
        help="Filter by difficulty level"
    )
    parser.add_argument(
        "--review",
        action="store_true",
        help="Review mode (show answers without input)"
    )
    parser.add_argument(
        "--export", "-e",
        type=Path,
        help="Export results to JSON file"
    )
    
    args = parser.parse_args()
    
    # Load quiz
    try:
        quiz_data = load_quiz(args.quiz)
    except (FileNotFoundError, ValueError) as e:
        print(f"ERROR: {e}")
        return 1
    
    # Parse and filter questions
    questions = parse_questions(quiz_data)
    
    if args.lo:
        lo_filter = set(args.lo)
        questions = filter_questions(questions, lo_filter=lo_filter)
    
    if args.difficulty:
        questions = filter_questions(questions, difficulty_filter=args.difficulty)
    
    if not questions:
        print("ERROR: No questions match the specified filters.")
        return 1
    
    # Print header and run quiz
    print_header(quiz_data)
    
    input("Press Enter to start the quiz...")
    
    result = run_quiz(
        questions=questions,
        quiz_data=quiz_data,
        randomize=args.random,
        limit=args.limit,
        review_mode=args.review,
    )
    
    # Display results
    display_results(result, quiz_data)
    
    # Export if requested
    if args.export:
        export_results(result, args.export)
    
    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
