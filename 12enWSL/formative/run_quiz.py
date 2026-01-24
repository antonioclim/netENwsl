#!/usr/bin/env python3
"""
Formative Quiz Runner — Week 12
===============================
Computer Networks - ASE, CSIE | by ing. dr. Antonio Clim

Interactive quiz runner for self-assessment.

Usage:
    python formative/run_quiz.py                    # Run all questions
    python formative/run_quiz.py --random           # Randomise question order
    python formative/run_quiz.py --limit 5          # Run only 5 questions
    python formative/run_quiz.py --lo LO1 LO2       # Filter by Learning Objectives
    python formative/run_quiz.py --difficulty basic # Filter by difficulty
    make quiz                                       # Via Makefile
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init()
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    class Fore:
        GREEN = RED = YELLOW = CYAN = BLUE = MAGENTA = WHITE = RESET = ""
    class Style:
        BRIGHT = RESET_ALL = ""


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
SCRIPT_DIR = Path(__file__).parent
QUIZ_YAML_PATH = SCRIPT_DIR / "quiz.yaml"
QUIZ_JSON_PATH = SCRIPT_DIR / "quiz.json"


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_LOADER
# ═══════════════════════════════════════════════════════════════════════════════
def load_quiz(path: Optional[Path] = None) -> Dict[str, Any]:
    """Load quiz from YAML or JSON file."""
    if path is not None:
        quiz_path = path
    elif YAML_AVAILABLE and QUIZ_YAML_PATH.exists():
        quiz_path = QUIZ_YAML_PATH
    elif QUIZ_JSON_PATH.exists():
        quiz_path = QUIZ_JSON_PATH
    else:
        raise FileNotFoundError(
            f"Quiz file not found. Expected: {QUIZ_YAML_PATH} or {QUIZ_JSON_PATH}"
        )
    
    with open(quiz_path, "r", encoding="utf-8") as f:
        if quiz_path.suffix in (".yaml", ".yml"):
            if not YAML_AVAILABLE:
                raise ImportError("PyYAML not installed. Run: pip install pyyaml")
            return yaml.safe_load(f)
        return json.load(f)


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_FILTER
# ═══════════════════════════════════════════════════════════════════════════════
def filter_questions(
    questions: List[Dict[str, Any]],
    lo_filter: Optional[List[str]] = None,
    difficulty_filter: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Filter questions by LO or difficulty."""
    filtered = questions
    if lo_filter:
        filtered = [q for q in filtered if q.get("lo_ref") in lo_filter]
    if difficulty_filter:
        filtered = [q for q in filtered if q.get("difficulty") == difficulty_filter]
    return filtered


# ═══════════════════════════════════════════════════════════════════════════════
# QUESTION_DISPLAY
# ═══════════════════════════════════════════════════════════════════════════════
def display_question(q: Dict[str, Any], index: int, total: int) -> None:
    """Display a single question."""
    print(f"\n{Fore.CYAN}{'═' * 70}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Question {index}/{total}{Style.RESET_ALL} "
          f"[{q.get('lo_ref', '?')}] [{q.get('difficulty', '?')}] "
          f"[{q.get('bloom_level', '?')}]")
    print(f"{Fore.CYAN}{'─' * 70}{Style.RESET_ALL}")
    print(f"\n{Style.BRIGHT}{q['stem']}{Style.RESET_ALL}\n")
    
    if q["type"] == "multiple_choice":
        for key, text in q["options"].items():
            print(f"  {Fore.BLUE}{key}){Style.RESET_ALL} {text}")
    elif q["type"] == "fill_blank" and "hint" in q:
        print(f"  {Fore.MAGENTA}Hint: {q['hint']}{Style.RESET_ALL}")


def get_answer(q: Dict[str, Any]) -> str:
    """Get user answer for a question."""
    if q["type"] == "multiple_choice":
        while True:
            answer = input(f"\n{Fore.WHITE}Your answer (a/b/c/d): {Style.RESET_ALL}").strip().lower()
            if answer in ["a", "b", "c", "d"]:
                return answer
            print(f"{Fore.RED}Invalid input. Please enter a, b, c or d.{Style.RESET_ALL}")
    return input(f"\n{Fore.WHITE}Your answer: {Style.RESET_ALL}").strip()


def check_answer(q: Dict[str, Any], answer: str) -> bool:
    """Check if answer is correct."""
    if q["type"] == "multiple_choice":
        return answer == q["correct"]
    return answer in q["correct"]


def display_result(q: Dict[str, Any], is_correct: bool) -> None:
    """Display result for a single question."""
    if is_correct:
        print(f"\n{Fore.GREEN}✓ Correct!{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}✗ Incorrect.{Style.RESET_ALL}")
        if q["type"] == "multiple_choice":
            correct_text = q["options"].get(q["correct"], q["correct"])
            print(f"  {Fore.YELLOW}Correct answer: {q['correct']}) {correct_text}{Style.RESET_ALL}")
        else:
            print(f"  {Fore.YELLOW}Accepted answers: {', '.join(q['correct'])}{Style.RESET_ALL}")
    
    if "explanation" in q:
        print(f"\n  {Fore.CYAN}📖 {q['explanation']}{Style.RESET_ALL}")
    if "misconception_ref" in q:
        print(f"  {Fore.MAGENTA}📚 See: {q['misconception_ref']}{Style.RESET_ALL}")


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_RUNNER
# ═══════════════════════════════════════════════════════════════════════════════
def run_quiz(
    quiz: Dict[str, Any],
    randomise: bool = False,
    limit: Optional[int] = None,
    lo_filter: Optional[List[str]] = None,
    difficulty_filter: Optional[str] = None
) -> float:
    """Run interactive quiz and return score percentage."""
    questions = filter_questions(
        quiz.get("questions", []),
        lo_filter=lo_filter,
        difficulty_filter=difficulty_filter
    )
    
    if not questions:
        print(f"{Fore.RED}No questions match the selected filters.{Style.RESET_ALL}")
        return 0.0
    
    if randomise:
        random.shuffle(questions)
    if limit and limit < len(questions):
        questions = questions[:limit]
    
    total = len(questions)
    correct = 0
    metadata = quiz.get("metadata", {})
    
    print(f"\n{Fore.CYAN}{'═' * 70}{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}WEEK {metadata.get('week', '?')} FORMATIVE QUIZ{Style.RESET_ALL}")
    print(f"{metadata.get('topic', 'Unknown Topic')}")
    print(f"{Fore.CYAN}{'═' * 70}{Style.RESET_ALL}")
    print(f"\nQuestions: {total}")
    print(f"Passing score: {metadata.get('passing_score', 70)}%")
    
    if lo_filter:
        print(f"Filtered by LOs: {', '.join(lo_filter)}")
    if difficulty_filter:
        print(f"Filtered by difficulty: {difficulty_filter}")
    
    input(f"\n{Fore.WHITE}Press Enter to start...{Style.RESET_ALL}")
    
    for i, q in enumerate(questions, 1):
        display_question(q, i, total)
        answer = get_answer(q)
        is_correct = check_answer(q, answer)
        if is_correct:
            correct += 1
        display_result(q, is_correct)
        if i < total:
            input(f"\n{Fore.WHITE}Press Enter for next question...{Style.RESET_ALL}")
    
    score = (correct / total) * 100 if total > 0 else 0
    passing = metadata.get("passing_score", 70)
    passed = score >= passing
    
    print(f"\n{Fore.CYAN}{'═' * 70}{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}FINAL RESULTS{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'═' * 70}{Style.RESET_ALL}")
    print(f"\nScore: {correct}/{total} ({score:.1f}%)")
    
    if passed:
        print(f"\n{Fore.GREEN}✓ PASSED{Style.RESET_ALL}")
        feedback = quiz.get("feedback", {})
        if score >= 90:
            print(f"\n{feedback.get('excellent', 'Excellent work!')}")
        else:
            print(f"\n{feedback.get('good', 'Good work!')}")
    else:
        print(f"\n{Fore.RED}✗ NEEDS REVIEW{Style.RESET_ALL}")
        print(f"\n{quiz.get('feedback', {}).get('needs_review', 'Please review the material.')}")
    
    print(f"\n{Fore.CYAN}{'═' * 70}{Style.RESET_ALL}")
    return score


# ═══════════════════════════════════════════════════════════════════════════════
# CLI_INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Week 12 Formative Quiz Runner")
    parser.add_argument("--quiz", "-q", type=Path, help="Path to quiz file")
    parser.add_argument("--random", "-r", action="store_true", help="Randomise order")
    parser.add_argument("--limit", "-n", type=int, help="Max questions")
    parser.add_argument("--lo", nargs="+", help="Filter by LOs (e.g. --lo LO1 LO2)")
    parser.add_argument("--difficulty", "-d", choices=["basic", "intermediate", "advanced"])
    parser.add_argument("--list-lo", action="store_true", help="List LOs and exit")
    return parser.parse_args()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    args = parse_args()
    
    try:
        quiz = load_quiz(args.quiz)
    except FileNotFoundError as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}Error loading quiz: {e}{Style.RESET_ALL}")
        return 1
    
    if args.list_lo:
        los = set(q.get("lo_ref") for q in quiz.get("questions", []))
        print("\nAvailable Learning Objectives:")
        for lo in sorted(los):
            count = sum(1 for q in quiz["questions"] if q.get("lo_ref") == lo)
            print(f"  {lo}: {count} question(s)")
        return 0
    
    try:
        score = run_quiz(
            quiz,
            randomise=args.random,
            limit=args.limit,
            lo_filter=args.lo,
            difficulty_filter=args.difficulty
        )
        return 0 if score >= quiz.get("metadata", {}).get("passing_score", 70) else 1
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Quiz cancelled.{Style.RESET_ALL}")
        return 130


if __name__ == "__main__":
    sys.exit(main())
