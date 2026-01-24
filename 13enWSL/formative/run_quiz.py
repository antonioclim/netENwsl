#!/usr/bin/env python3
"""
Formative Quiz Runner — Week 13: IoT and Security
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

LEARNING OBJECTIVES:
- Self-assessment of knowledge retention
- Identification of misconceptions
- Bloom taxonomy level awareness

USAGE:
    python formative/run_quiz.py                      # Full quiz
    python formative/run_quiz.py --random --limit 5   # Random 5 questions
    python formative/run_quiz.py --bloom apply        # Only Apply level
    python formative/run_quiz.py --export results.json # Export results
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError:
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║  ERROR: PyYAML not installed                                   ║")
    print("║  Run: pip install pyyaml                                       ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class QuestionResult:
    """Result for a single question."""
    question_id: str
    bloom_level: str
    lo_ref: str
    correct: bool
    time_seconds: float
    user_answer: str
    correct_answer: str


@dataclass
class QuizResult:
    """Complete quiz attempt result."""
    timestamp: str
    total_questions: int
    correct_answers: int
    score_percent: float
    passed: bool
    duration_seconds: float
    by_bloom_level: Dict[str, Dict[str, int]] = field(default_factory=dict)
    by_lo: Dict[str, Dict[str, int]] = field(default_factory=dict)
    question_results: List[QuestionResult] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════════════════════
# TERMINAL COLORS
# ═══════════════════════════════════════════════════════════════════════════════

class Colors:
    """ANSI color codes for terminal output."""
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


# Disable colors if not TTY
if not sys.stdout.isatty():
    Colors.GREEN = Colors.RED = Colors.YELLOW = ""
    Colors.BLUE = Colors.CYAN = Colors.BOLD = Colors.RESET = ""


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ LOADING
# ═══════════════════════════════════════════════════════════════════════════════

def load_quiz(quiz_path: Path) -> Dict[str, Any]:
    """
    Load quiz from YAML file.
    
    Args:
        quiz_path: Path to quiz YAML file
        
    Returns:
        Parsed quiz dictionary
        
    Raises:
        FileNotFoundError: If quiz file doesn't exist
        yaml.YAMLError: If YAML is malformed
    """
    with open(quiz_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ═══════════════════════════════════════════════════════════════════════════════
# QUESTION HANDLERS
# ═══════════════════════════════════════════════════════════════════════════════

def ask_multiple_choice(question: Dict[str, Any]) -> tuple[bool, str, str]:
    """
    Present multiple choice question and get answer.
    
    Returns:
        Tuple of (is_correct, user_answer, correct_answer)
    """
    for key, val in question["options"].items():
        print(f"  {Colors.CYAN}{key}){Colors.RESET} {val}")
    
    answer = input(f"\n{Colors.BOLD}→ Your answer (a/b/c/d):{Colors.RESET} ").strip().lower()
    correct = question["correct"].lower()
    
    return (answer == correct, answer, correct)


def ask_fill_blank(question: Dict[str, Any]) -> tuple[bool, str, str]:
    """
    Present fill-in-the-blank question and get answer.
    
    Returns:
        Tuple of (is_correct, user_answer, correct_answer_display)
    """
    if "hint" in question:
        print(f"  {Colors.YELLOW}💡 Hint: {question['hint']}{Colors.RESET}")
    
    answer = input(f"\n{Colors.BOLD}→ Your answer:{Colors.RESET} ").strip()
    
    correct_answers = question["correct"]
    
    # Handle multiple correct formats
    if isinstance(correct_answers[0], list):
        # Multiple parts expected
        is_correct = any(
            all(part.lower() in answer.lower() for part in combo)
            for combo in correct_answers
        )
        correct_display = " | ".join([", ".join(c) for c in correct_answers])
    else:
        # Single answer with multiple acceptable forms
        is_correct = any(
            answer.lower() == a.lower() or answer.lower() in a.lower()
            for a in correct_answers
        )
        correct_display = ", ".join(correct_answers)
    
    return (is_correct, answer, correct_display)


def ask_short_answer(question: Dict[str, Any]) -> tuple[bool, str, str]:
    """
    Present short answer question with self-evaluation.
    
    Returns:
        Tuple of (is_correct, user_answer, rubric_summary)
    """
    print(f"\n  {Colors.YELLOW}📝 Rubric (self-evaluate):{Colors.RESET}")
    for i, criterion in enumerate(question.get("rubric", []), 1):
        print(f"     {i}. {criterion}")
    
    print(f"\n  {Colors.CYAN}Write your answer below (or type it mentally):{Colors.RESET}")
    input("  Press Enter when ready to self-evaluate...")
    
    if "example_answer" in question:
        print(f"\n  {Colors.GREEN}Example answer:{Colors.RESET}")
        for line in question["example_answer"].strip().split("\n"):
            print(f"    {line}")
    
    try:
        score = int(input(f"\n{Colors.BOLD}→ Self-score (0-3):{Colors.RESET} ").strip())
        is_correct = score >= 2  # Consider "passing" if 2+ points
    except ValueError:
        is_correct = False
        score = 0
    
    return (is_correct, f"self-score: {score}", "See rubric above")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN QUIZ RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def run_interactive_quiz(
    quiz: Dict[str, Any],
    randomize: bool = False,
    limit: Optional[int] = None,
    bloom_filter: Optional[str] = None
) -> QuizResult:
    """
    Run interactive quiz session.
    
    Args:
        quiz: Loaded quiz dictionary
        randomize: Shuffle question order
        limit: Maximum number of questions
        bloom_filter: Only questions at this Bloom level
    
    Returns:
        QuizResult with comprehensive statistics
    """
    questions = quiz.get("questions", [])
    metadata = quiz.get("metadata", {})
    
    # Apply Bloom filter
    if bloom_filter:
        questions = [
            q for q in questions 
            if q.get("bloom_level", "").lower() == bloom_filter.lower()
        ]
    
    # Randomize if requested
    if randomize:
        random.shuffle(questions)
    
    # Apply limit
    if limit and limit < len(questions):
        questions = questions[:limit]
    
    if not questions:
        print(f"{Colors.RED}No questions match the criteria.{Colors.RESET}")
        return QuizResult(
            timestamp=datetime.now().isoformat(),
            total_questions=0,
            correct_answers=0,
            score_percent=0.0,
            passed=False,
            duration_seconds=0.0
        )
    
    # Quiz header
    print(f"\n{Colors.BOLD}{'═' * 64}{Colors.RESET}")
    print(f"{Colors.BOLD}  📝 QUIZ: {metadata.get('topic', 'Unknown')}{Colors.RESET}")
    print(f"  Questions: {len(questions)} | Passing: {metadata.get('passing_score', 70)}%")
    print(f"  Estimated time: {metadata.get('estimated_time_minutes', '?')} minutes")
    print(f"{Colors.BOLD}{'═' * 64}{Colors.RESET}")
    input(f"\n{Colors.CYAN}Press Enter to start...{Colors.RESET}")
    
    start_time = time.time()
    correct = 0
    bloom_stats: Dict[str, Dict[str, int]] = {}
    lo_stats: Dict[str, Dict[str, int]] = {}
    question_results: List[QuestionResult] = []
    
    for i, q in enumerate(questions, 1):
        q_start = time.time()
        
        bloom = q.get("bloom_level", "unknown")
        lo = q.get("lo_ref", "unknown")
        
        # Initialize stats
        if bloom not in bloom_stats:
            bloom_stats[bloom] = {"total": 0, "correct": 0}
        if lo not in lo_stats:
            lo_stats[lo] = {"total": 0, "correct": 0}
        
        bloom_stats[bloom]["total"] += 1
        lo_stats[lo]["total"] += 1
        
        # Question header
        print(f"\n{Colors.BOLD}{'─' * 64}{Colors.RESET}")
        print(f"{Colors.BOLD}Q{i}/{len(questions)}{Colors.RESET} "
              f"[{Colors.YELLOW}{q.get('difficulty', '?')}{Colors.RESET}] "
              f"[Bloom: {Colors.BLUE}{bloom.upper()}{Colors.RESET}] "
              f"[{Colors.CYAN}{lo}{Colors.RESET}]")
        print(f"{'─' * 64}")
        
        # Display stem (question text)
        stem = q["stem"].strip()
        print(f"\n{stem}\n")
        
        # Handle by question type
        if q["type"] == "multiple_choice":
            is_correct, user_ans, correct_ans = ask_multiple_choice(q)
        elif q["type"] == "fill_blank":
            is_correct, user_ans, correct_ans = ask_fill_blank(q)
        elif q["type"] == "short_answer":
            is_correct, user_ans, correct_ans = ask_short_answer(q)
        else:
            print(f"{Colors.RED}Unknown question type: {q['type']}{Colors.RESET}")
            continue
        
        # Record result
        q_time = time.time() - q_start
        
        if is_correct:
            print(f"\n{Colors.GREEN}✅ CORRECT!{Colors.RESET}")
            correct += 1
            bloom_stats[bloom]["correct"] += 1
            lo_stats[lo]["correct"] += 1
        else:
            print(f"\n{Colors.RED}❌ Wrong.{Colors.RESET} Correct: {Colors.GREEN}{correct_ans}{Colors.RESET}")
        
        # Show explanation if available
        if "explanation" in q:
            print(f"\n{Colors.CYAN}📖 {q['explanation'].strip()}{Colors.RESET}")
        
        question_results.append(QuestionResult(
            question_id=q.get("id", f"q{i}"),
            bloom_level=bloom,
            lo_ref=lo,
            correct=is_correct,
            time_seconds=round(q_time, 2),
            user_answer=user_ans,
            correct_answer=correct_ans
        ))
    
    # Calculate final results
    duration = time.time() - start_time
    score = (correct / len(questions)) * 100 if questions else 0
    passed = score >= metadata.get("passing_score", 70)
    
    # Results summary
    print(f"\n{Colors.BOLD}{'═' * 64}{Colors.RESET}")
    print(f"{Colors.BOLD}  📊 RESULTS{Colors.RESET}")
    print(f"{'═' * 64}")
    print(f"  Score: {Colors.BOLD}{correct}/{len(questions)} ({score:.1f}%){Colors.RESET}")
    
    if passed:
        print(f"  Status: {Colors.GREEN}✅ PASSED{Colors.RESET}")
    else:
        print(f"  Status: {Colors.RED}❌ NEEDS REVIEW{Colors.RESET}")
    
    print(f"  Time: {duration:.1f}s ({duration/60:.1f} min)")
    
    # Bloom level breakdown
    print(f"\n  {Colors.BOLD}By Bloom Level:{Colors.RESET}")
    for level in ["remember", "understand", "apply", "analyze", "evaluate", "create"]:
        if level in bloom_stats:
            stats = bloom_stats[level]
            pct = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
            bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
            color = Colors.GREEN if pct >= 70 else Colors.YELLOW if pct >= 50 else Colors.RED
            print(f"    {level.capitalize():12s}: {color}{bar} {stats['correct']}/{stats['total']} ({pct:.0f}%){Colors.RESET}")
    
    # LO breakdown
    print(f"\n  {Colors.BOLD}By Learning Objective:{Colors.RESET}")
    for lo, stats in sorted(lo_stats.items()):
        pct = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
        status = "✅" if pct >= 70 else "⚠️" if pct >= 50 else "❌"
        print(f"    {lo}: {status} {stats['correct']}/{stats['total']}")
    
    print(f"{Colors.BOLD}{'═' * 64}{Colors.RESET}\n")
    
    return QuizResult(
        timestamp=datetime.now().isoformat(),
        total_questions=len(questions),
        correct_answers=correct,
        score_percent=round(score, 2),
        passed=passed,
        duration_seconds=round(duration, 2),
        by_bloom_level=bloom_stats,
        by_lo=lo_stats,
        question_results=question_results
    )


def export_results(result: QuizResult, output_path: Path) -> None:
    """Export quiz results to JSON file."""
    # Convert dataclasses to dicts
    data = asdict(result)
    data["question_results"] = [asdict(qr) for qr in result.question_results]
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"{Colors.GREEN}Results exported to: {output_path}{Colors.RESET}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Formative Quiz Runner — Week 13: IoT and Security",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                        Run full quiz
  %(prog)s --random --limit 5     Random 5 questions
  %(prog)s --bloom apply          Only 'Apply' level questions
  %(prog)s --export results.json  Export results to JSON
        """
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
        metavar="N",
        help="Limit to N questions"
    )
    parser.add_argument(
        "--bloom", "-b",
        choices=["remember", "understand", "apply", "analyze", "evaluate", "create"],
        help="Filter by Bloom taxonomy level"
    )
    parser.add_argument(
        "--export", "-e",
        type=Path,
        metavar="FILE",
        help="Export results to JSON file"
    )
    
    args = parser.parse_args()
    
    # Validate quiz file exists
    if not args.quiz.exists():
        print(f"{Colors.RED}ERROR: Quiz file not found: {args.quiz}{Colors.RESET}")
        return 1
    
    try:
        quiz = load_quiz(args.quiz)
    except yaml.YAMLError as e:
        print(f"{Colors.RED}ERROR: Invalid YAML: {e}{Colors.RESET}")
        return 1
    
    # Run quiz
    result = run_interactive_quiz(
        quiz,
        randomize=args.random,
        limit=args.limit,
        bloom_filter=args.bloom
    )
    
    # Export if requested
    if args.export:
        export_results(result, args.export)
    
    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
