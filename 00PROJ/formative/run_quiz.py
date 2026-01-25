#!/usr/bin/env python3
"""
Quiz Runner — Formative Assessment for Computer Networks Projects.

A standalone script to run YAML-based quizzes for self-assessment.
Supports multiple question types, LO tracking and progress saving.

Usage:
    python run_quiz.py quiz_p01.yaml              # Run P01 quiz
    python run_quiz.py quiz_p01.yaml --random     # Randomise questions
    python run_quiz.py quiz_p01.yaml --lo LO2     # Filter by LO
    python run_quiz.py quiz_p01.yaml --practice   # Practice mode (hints)
    python run_quiz.py --list                     # List available quizzes

Author: Computer Networks Course Team
Institution: ASE Bucharest - CSIE
Version: 1.0
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    print("❌ PyYAML required. Install with: pip install pyyaml")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
VERSION = "1.0.0"
QUIZ_DIR = Path(__file__).parent
RESULTS_DIR = QUIZ_DIR / "results"
EXPORTS_DIR = QUIZ_DIR / "exports"

# ANSI colour codes for terminal output
COLOURS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "cyan": "\033[96m",
}

# Bloom taxonomy level descriptions
BLOOM_LEVELS = {
    "remember": "Recall facts and basic concepts",
    "understand": "Explain ideas or concepts",
    "apply": "Use information in new situations",
    "analyse": "Draw connections among ideas",
    "evaluate": "Justify decisions or actions",
    "create": "Produce new or original work",
}


# ═══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class QuestionResult:
    """Result of a single question attempt."""
    question_id: str
    lo_ref: str
    bloom_level: str
    correct: bool
    points_earned: float
    points_possible: float
    time_seconds: float
    answer_given: str
    correct_answer: str


@dataclass
class QuizResult:
    """Complete quiz attempt result."""
    quiz_id: str
    project_id: str
    timestamp: str
    total_questions: int
    correct_answers: int
    total_points: float
    points_earned: float
    score_percentage: float
    time_seconds: float
    passed: bool
    grade_label: str
    lo_breakdown: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    question_results: List[QuestionResult] = field(default_factory=list)
    weak_areas: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def colour(text: str, colour_name: str) -> str:
    """Apply ANSI colour to text if terminal supports it."""
    if sys.stdout.isatty():
        return f"{COLOURS.get(colour_name, '')}{text}{COLOURS['reset']}"
    return text


def print_header(title: str, char: str = "═") -> None:
    """Print a formatted section header."""
    width = 60
    print(f"\n{char * width}")
    print(f"  {title}")
    print(f"{char * width}")


def print_progress_bar(current: int, total: int, width: int = 40) -> None:
    """Display a progress bar."""
    filled = int(width * current / total)
    bar = "█" * filled + "░" * (width - filled)
    percentage = current / total * 100
    print(f"\r[{bar}] {current}/{total} ({percentage:.0f}%)", end="", flush=True)


def load_quiz(path: Path) -> Optional[Dict[str, Any]]:
    """
    Load quiz data from YAML file.
    
    Args:
        path: Path to quiz YAML file
        
    Returns:
        Quiz data dictionary or None if not found
    """
    if not path.exists():
        # Try with .yaml extension
        if not path.suffix:
            path = path.with_suffix(".yaml")
        if not path.exists():
            return None
    
    try:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(colour(f"❌ YAML parsing error: {e}", "red"))
        return None


def save_result(result: QuizResult) -> Path:
    """
    Save quiz result to JSON file.
    
    Args:
        result: QuizResult to save
        
    Returns:
        Path to saved file
    """
    RESULTS_DIR.mkdir(exist_ok=True)
    
    timestamp = result.timestamp.replace(":", "-").replace(".", "-")
    filename = f"{result.project_id}_{timestamp}.json"
    filepath = RESULTS_DIR / filename
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(asdict(result), f, indent=2, ensure_ascii=False)
    
    return filepath


# ═══════════════════════════════════════════════════════════════════════════════
# QUESTION HANDLERS
# ═══════════════════════════════════════════════════════════════════════════════
def ask_multiple_choice(question: Dict, practice_mode: bool = False) -> Tuple[bool, str]:
    """
    Present a multiple choice question.
    
    Args:
        question: Question dictionary
        practice_mode: Whether to show hints
        
    Returns:
        Tuple of (is_correct, answer_given)
    """
    print(f"\n{question['stem']}\n")
    
    options = question.get("options", {})
    option_keys = list(options.keys())
    
    for key in option_keys:
        print(f"  {colour(key + ')', 'cyan')} {options[key]}")
    
    if practice_mode and "hint" in question:
        print(f"\n  💡 Hint: {question['hint']}")
    
    while True:
        answer = input(f"\n{colour('Your answer', 'bold')} ({'/'.join(option_keys)}): ").strip().lower()
        if answer in option_keys:
            break
        print(colour("  Please enter a valid option.", "yellow"))
    
    correct = answer == question["correct"]
    return correct, answer


def ask_multiple_select(question: Dict, practice_mode: bool = False) -> Tuple[bool, str]:
    """Present a multiple select question (multiple correct answers)."""
    print(f"\n{question['stem']}\n")
    print(colour("  (Select ALL that apply, separate with commas)", "yellow"))
    
    options = question.get("options", {})
    option_keys = list(options.keys())
    
    for key in option_keys:
        print(f"  {colour(key + ')', 'cyan')} {options[key]}")
    
    answer = input(f"\n{colour('Your answers', 'bold')} (e.g., a,c,e): ").strip().lower()
    selected = set(a.strip() for a in answer.split(",") if a.strip())
    correct_set = set(question["correct"])
    
    # Full credit for exact match, partial credit available
    if question.get("partial_credit", False):
        correct_selected = selected & correct_set
        score = len(correct_selected) / len(correct_set) if correct_set else 0
        is_correct = score >= 0.5  # At least 50% for partial credit
    else:
        is_correct = selected == correct_set
    
    return is_correct, answer


def ask_fill_blank(question: Dict, practice_mode: bool = False) -> Tuple[bool, str]:
    """Present a fill-in-the-blank question."""
    print(f"\n{question['stem']}\n")
    
    if practice_mode and "hint" in question:
        print(f"  💡 Hint: {question['hint']}")
    
    answer = input(f"\n{colour('Your answer', 'bold')}: ").strip()
    
    # Check against all acceptable answers
    correct_answers = question.get("correct", [])
    if isinstance(correct_answers, str):
        correct_answers = [correct_answers]
    
    # Case-insensitive comparison with trimming
    is_correct = any(
        answer.lower().strip() == ca.lower().strip() 
        for ca in correct_answers
    )
    
    return is_correct, answer


def ask_code_trace(question: Dict, practice_mode: bool = False) -> Tuple[bool, str]:
    """Present a code tracing question."""
    print(f"\n{question['stem']}\n")
    
    options = question.get("options", {})
    for key, val in options.items():
        print(f"  {colour(key + ')', 'cyan')} {val}")
    
    answer = input(f"\n{colour('Your answer', 'bold')}: ").strip().lower()
    correct = answer == question["correct"]
    
    return correct, answer


def ask_scenario(question: Dict, practice_mode: bool = False) -> Tuple[bool, str]:
    """Present a scenario-based question."""
    return ask_multiple_choice(question, practice_mode)


def ask_ordering(question: Dict, practice_mode: bool = False) -> Tuple[bool, str]:
    """Present an ordering question."""
    print(f"\n{question['stem']}\n")
    
    items = question.get("items", [])
    # Display in random order
    display_items = items.copy()
    random.shuffle(display_items)
    
    for i, item in enumerate(display_items, 1):
        print(f"  {i}. {item['text']}")
    
    print(colour("\n  Enter the correct order using item numbers (e.g., 3,1,2,4,5)", "yellow"))
    
    answer = input(f"\n{colour('Your order', 'bold')}: ").strip()
    
    try:
        given_order = [int(x.strip()) for x in answer.split(",")]
        # Map display positions to original IDs
        given_ids = [display_items[i-1]["id"] for i in given_order]
        correct = given_ids == question["correct_order"]
    except (ValueError, IndexError):
        correct = False
    
    return correct, answer


def ask_matching(question: Dict, practice_mode: bool = False) -> Tuple[bool, str]:
    """Present a matching question."""
    print(f"\n{question['stem']}\n")
    
    pairs = question.get("pairs", [])
    distractors = question.get("distractors", [])
    
    # Display left column
    print(colour("  Items:", "bold"))
    for i, pair in enumerate(pairs, 1):
        print(f"    {i}. {pair['left']}")
    
    # Display right column (shuffled with distractors)
    all_right = [p["right"] for p in pairs] + distractors
    random.shuffle(all_right)
    
    print(colour("\n  Options:", "bold"))
    for i, opt in enumerate(all_right):
        print(f"    {chr(65+i)}. {opt}")
    
    print(colour("\n  Match items to options (e.g., 1A,2C,3B,4D)", "yellow"))
    
    answer = input(f"\n{colour('Your matches', 'bold')}: ").strip().upper()
    
    # Parse and check matches
    try:
        matches = {}
        for match in answer.split(","):
            match = match.strip()
            if len(match) >= 2:
                item_num = int(match[0])
                option_letter = match[1]
                option_idx = ord(option_letter) - 65
                matches[item_num] = all_right[option_idx]
        
        correct_count = sum(
            1 for i, pair in enumerate(pairs, 1)
            if matches.get(i) == pair["right"]
        )
        is_correct = correct_count == len(pairs)
    except (ValueError, IndexError):
        is_correct = False
    
    return is_correct, answer


# Question type dispatcher
QUESTION_HANDLERS = {
    "multiple_choice": ask_multiple_choice,
    "multiple_select": ask_multiple_select,
    "fill_blank": ask_fill_blank,
    "code_trace": ask_code_trace,
    "scenario": ask_scenario,
    "ordering": ask_ordering,
    "matching": ask_matching,
}


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ RUNNER
# ═══════════════════════════════════════════════════════════════════════════════
def run_quiz(
    quiz_path: Path,
    randomise: bool = False,
    lo_filter: Optional[str] = None,
    limit: Optional[int] = None,
    practice_mode: bool = False,
) -> QuizResult:
    """
    Run an interactive quiz session.
    
    Args:
        quiz_path: Path to quiz YAML file
        randomise: Whether to randomise question order
        lo_filter: Filter questions by Learning Objective
        limit: Maximum number of questions
        practice_mode: Show hints and explanations during quiz
        
    Returns:
        QuizResult with complete session data
    """
    quiz_data = load_quiz(quiz_path)
    
    if not quiz_data:
        print(colour(f"❌ Could not load quiz: {quiz_path}", "red"))
        sys.exit(1)
    
    project = quiz_data.get("project", {})
    metadata = quiz_data.get("metadata", {})
    questions = project.get("questions", [])
    grading = quiz_data.get("grading", {})
    
    # Apply filters
    if lo_filter:
        questions = [q for q in questions if q.get("lo_ref") == lo_filter]
    
    if not questions:
        print(colour("❌ No questions match the criteria.", "red"))
        sys.exit(1)
    
    if randomise:
        random.shuffle(questions)
    
    if limit:
        questions = questions[:limit]
    
    # Display quiz header
    print_header(f"QUIZ: {project.get('title', 'Unknown')}")
    print(f"\n  📋 Project: {project.get('id', 'N/A')}")
    print(f"  📝 Questions: {len(questions)}")
    print(f"  ⏱️  Time limit: {metadata.get('time_limit_minutes', 15)} minutes")
    print(f"  ✅ Passing score: {metadata.get('passing_score', 70)}%")
    
    if lo_filter:
        print(f"  🎯 Filtered by: {lo_filter}")
    
    if practice_mode:
        print(colour("\n  💡 Practice mode: Hints enabled", "yellow"))
    
    input(colour("\n  Press ENTER to begin...", "cyan"))
    
    # Run quiz
    start_time = time.time()
    correct_count = 0
    total_points = 0
    points_earned = 0
    question_results: List[QuestionResult] = []
    lo_stats: Dict[str, Dict[str, Any]] = {}
    
    for i, q in enumerate(questions, 1):
        q_start = time.time()
        
        # Display question header
        q_type = q.get("type", "multiple_choice")
        q_lo = q.get("lo_ref", "N/A")
        q_bloom = q.get("bloom_level", "N/A")
        q_points = q.get("points", 1)
        q_difficulty = q.get("difficulty", "N/A")
        
        print(f"\n{'─' * 60}")
        print(f"  Question {i}/{len(questions)} | {colour(q_lo, 'cyan')} | "
              f"{q_bloom.capitalize()} | {q_difficulty.capitalize()} | "
              f"{q_points} {'point' if q_points == 1 else 'points'}")
        print(f"{'─' * 60}")
        
        # Get handler for question type
        handler = QUESTION_HANDLERS.get(q_type, ask_multiple_choice)
        is_correct, answer = handler(q, practice_mode)
        
        q_time = time.time() - q_start
        total_points += q_points
        
        # Track LO statistics
        if q_lo not in lo_stats:
            lo_stats[q_lo] = {"correct": 0, "total": 0, "points": 0, "max_points": 0}
        lo_stats[q_lo]["total"] += 1
        lo_stats[q_lo]["max_points"] += q_points
        
        if is_correct:
            correct_count += 1
            points_earned += q_points
            lo_stats[q_lo]["correct"] += 1
            lo_stats[q_lo]["points"] += q_points
            print(colour("\n  ✅ CORRECT!", "green"))
        else:
            print(colour("\n  ❌ INCORRECT", "red"))
            correct_answer = q.get("correct", "N/A")
            if isinstance(correct_answer, list):
                correct_answer = ", ".join(str(a) for a in correct_answer)
            print(f"  Correct answer: {correct_answer}")
        
        # Show feedback
        feedback = q.get("feedback", {})
        if is_correct and "correct" in feedback:
            print(f"  {feedback['correct']}")
        elif not is_correct and "incorrect" in feedback:
            print(f"  {feedback['incorrect']}")
        
        # Show explanation (always in practice mode or after incorrect)
        if practice_mode or not is_correct:
            if "explanation" in q:
                print(f"\n  📖 {q['explanation']}")
            if "misconception" in q:
                print(f"  ⚠️  Common misconception: {q['misconception']}")
        
        # Record result
        question_results.append(QuestionResult(
            question_id=q.get("id", f"q{i}"),
            lo_ref=q_lo,
            bloom_level=q_bloom,
            correct=is_correct,
            points_earned=q_points if is_correct else 0,
            points_possible=q_points,
            time_seconds=q_time,
            answer_given=str(answer),
            correct_answer=str(q.get("correct", "")),
        ))
        
        if i < len(questions):
            input(colour("\n  Press ENTER for next question...", "cyan"))
    
    # Calculate final results
    elapsed = time.time() - start_time
    score_pct = (points_earned / total_points * 100) if total_points > 0 else 0
    passing_score = metadata.get("passing_score", 70)
    passed = score_pct >= passing_score
    
    # Determine grade label
    grade_bands = grading.get("grade_bands", [])
    grade_label = "Unknown"
    for band in grade_bands:
        low, high = band["range"]
        if low <= score_pct <= high:
            grade_label = band["label"]
            break
    
    # Identify weak areas
    weak_areas = []
    recommendations = []
    for lo, stats in lo_stats.items():
        if stats["total"] > 0:
            lo_pct = (stats["correct"] / stats["total"]) * 100
            if lo_pct < 60:
                weak_areas.append(f"{lo} ({lo_pct:.0f}%)")
                # Find LO description
                for lo_def in project.get("learning_objectives", []):
                    if lo_def.get("id") == lo:
                        recommendations.append(
                            f"Review {lo}: {lo_def.get('description', 'N/A')}"
                        )
                        break
    
    result = QuizResult(
        quiz_id=quiz_path.stem,
        project_id=project.get("id", "Unknown"),
        timestamp=datetime.now().isoformat(),
        total_questions=len(questions),
        correct_answers=correct_count,
        total_points=total_points,
        points_earned=points_earned,
        score_percentage=score_pct,
        time_seconds=elapsed,
        passed=passed,
        grade_label=grade_label,
        lo_breakdown=lo_stats,
        question_results=question_results,
        weak_areas=weak_areas,
        recommendations=recommendations,
    )
    
    # Display results
    display_results(result, grading)
    
    # Save results
    saved_path = save_result(result)
    print(f"\n  💾 Results saved: {saved_path}")
    
    return result


def display_results(result: QuizResult, grading: Dict) -> None:
    """Display formatted quiz results."""
    print_header("QUIZ RESULTS", "═")
    
    # Summary
    print(f"\n  📋 Project: {result.project_id}")
    print(f"  📊 Score: {result.correct_answers}/{result.total_questions} "
          f"({result.score_percentage:.1f}%)")
    print(f"  🏆 Points: {result.points_earned:.1f}/{result.total_points:.1f}")
    print(f"  ⏱️  Time: {result.time_seconds:.1f} seconds")
    
    # Pass/fail status
    if result.passed:
        print(colour(f"\n  ✅ PASSED — {result.grade_label}", "green"))
    else:
        print(colour(f"\n  ❌ NOT PASSED — {result.grade_label}", "red"))
    
    # Grade feedback
    for band in grading.get("grade_bands", []):
        if band["label"] == result.grade_label:
            print(f"  {band.get('feedback', '')}")
            break
    
    # LO breakdown
    print(colour("\n  📈 Learning Objective Breakdown:", "bold"))
    for lo, stats in result.lo_breakdown.items():
        if stats["total"] > 0:
            pct = (stats["correct"] / stats["total"]) * 100
            bar_filled = int(pct / 10)
            bar = "█" * bar_filled + "░" * (10 - bar_filled)
            status = colour("✓", "green") if pct >= 60 else colour("✗", "red")
            print(f"    {lo}: [{bar}] {pct:.0f}% {status}")
    
    # Weak areas
    if result.weak_areas:
        print(colour("\n  ⚠️  Areas Needing Review:", "yellow"))
        for area in result.weak_areas:
            print(f"    • {area}")
    
    # Recommendations
    if result.recommendations:
        print(colour("\n  📚 Recommendations:", "cyan"))
        for rec in result.recommendations:
            print(f"    → {rec}")
    
    print("\n" + "═" * 60)


def list_quizzes() -> None:
    """List all available quizzes in the formative directory."""
    print_header("Available Quizzes")
    
    quiz_files = list(QUIZ_DIR.glob("quiz_*.yaml"))
    
    if not quiz_files:
        print("  No quizzes found in", QUIZ_DIR)
        return
    
    for quiz_file in sorted(quiz_files):
        quiz_data = load_quiz(quiz_file)
        if quiz_data:
            project = quiz_data.get("project", {})
            print(f"\n  📝 {quiz_file.name}")
            print(f"     Project: {project.get('id', 'N/A')} — {project.get('title', 'N/A')}")
            print(f"     Questions: {len(project.get('questions', []))}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Quiz Runner for Computer Networks Projects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_quiz.py quiz_p01.yaml
    python run_quiz.py quiz_p01.yaml --random --limit 5
    python run_quiz.py quiz_p01.yaml --lo LO2 --practice
    python run_quiz.py --list
        """,
    )
    
    parser.add_argument(
        "quiz",
        nargs="?",
        type=Path,
        help="Path to quiz YAML file",
    )
    
    parser.add_argument(
        "--random", "-r",
        action="store_true",
        help="Randomise question order",
    )
    
    parser.add_argument(
        "--lo",
        type=str,
        help="Filter by Learning Objective (e.g., LO2)",
    )
    
    parser.add_argument(
        "--limit", "-n",
        type=int,
        help="Limit number of questions",
    )
    
    parser.add_argument(
        "--practice", "-p",
        action="store_true",
        help="Practice mode with hints",
    )
    
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available quizzes",
    )
    
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"%(prog)s {VERSION}",
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_quizzes()
        return 0
    
    if not args.quiz:
        parser.print_help()
        return 1
    
    # Resolve quiz path
    quiz_path = args.quiz
    if not quiz_path.is_absolute():
        # Check in current directory first, then formative directory
        if not quiz_path.exists():
            quiz_path = QUIZ_DIR / quiz_path
    
    result = run_quiz(
        quiz_path=quiz_path,
        randomise=args.random,
        lo_filter=args.lo,
        limit=args.limit,
        practice_mode=args.practice,
    )
    
    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
