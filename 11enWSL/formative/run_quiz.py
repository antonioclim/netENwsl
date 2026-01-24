#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
  run_quiz.py — Interactive Quiz Runner for Week 11
═══════════════════════════════════════════════════════════════════════════════

NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

USAGE:
  python formative/run_quiz.py                    # Run full quiz
  python formative/run_quiz.py --random           # Randomize question order
  python formative/run_quiz.py --limit 5          # Run only 5 questions
  python formative/run_quiz.py --topic DNS        # Filter by topic
  python formative/run_quiz.py --difficulty basic # Filter by difficulty
  python formative/run_quiz.py --review           # Show all answers without quiz

DEPENDENCIES:
  pip install pyyaml

═══════════════════════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import argparse
import random
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

COLORS = {
    'green': '\033[92m',
    'red': '\033[91m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'cyan': '\033[96m',
    'bold': '\033[1m',
    'reset': '\033[0m'
}

def colorize(text: str, color: str) -> str:
    """Apply ANSI color to text."""
    return f"{COLORS.get(color, '')}{text}{COLORS['reset']}"


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ LOADER
# ═══════════════════════════════════════════════════════════════════════════════

def load_quiz(path: Path) -> Dict[str, Any]:
    """Load quiz from YAML file."""
    if not path.exists():
        print(f"Error: Quiz file not found: {path}")
        sys.exit(1)
    
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def filter_questions(
    questions: List[Dict],
    topic: Optional[str] = None,
    difficulty: Optional[str] = None,
    lo_ref: Optional[str] = None
) -> List[Dict]:
    """Filter questions by criteria."""
    filtered = questions
    
    if topic:
        filtered = [q for q in filtered if topic.lower() in q.get('topic', '').lower()]
    
    if difficulty:
        filtered = [q for q in filtered if q.get('difficulty', '').lower() == difficulty.lower()]
    
    if lo_ref:
        filtered = [q for q in filtered if lo_ref.upper() in q.get('lo_ref', '').upper()]
    
    return filtered


# ═══════════════════════════════════════════════════════════════════════════════
# QUESTION HANDLERS
# ═══════════════════════════════════════════════════════════════════════════════

def ask_multiple_choice(question: Dict, index: int) -> bool:
    """Ask a multiple choice question. Returns True if correct."""
    print(f"\n{colorize(f'Q{index}', 'cyan')} [{question.get('difficulty', '?')}] {question.get('topic', '')}")
    print(f"{colorize('─' * 60, 'blue')}")
    
    # Handle multiline stems
    stem = question['stem']
    if '\n' in stem:
        print(stem)
    else:
        print(f"  {stem}")
    
    print()
    for key, value in question['options'].items():
        print(f"    {colorize(key.upper(), 'bold')}) {value}")
    
    print()
    answer = input("  Your answer (a/b/c/d): ").strip().lower()
    
    correct = question['correct'].lower()
    is_correct = answer == correct
    
    if is_correct:
        print(colorize("  ✓ Correct!", 'green'))
    else:
        print(colorize(f"  ✗ Wrong. Correct answer: {correct.upper()}", 'red'))
    
    # Show explanation
    if 'explanation' in question:
        print(f"  {colorize('📖', 'yellow')} {question['explanation']}")
    
    return is_correct


def ask_fill_blank(question: Dict, index: int) -> bool:
    """Ask a fill-in-the-blank question. Returns True if correct."""
    print(f"\n{colorize(f'Q{index}', 'cyan')} [{question.get('difficulty', '?')}] {question.get('topic', '')}")
    print(f"{colorize('─' * 60, 'blue')}")
    print(f"  {question['stem']}")
    
    if 'hint' in question:
        print(f"  {colorize('💡 Hint:', 'yellow')} {question['hint']}")
    
    print()
    answer = input("  Your answer: ").strip()
    
    # Check against all accepted answers (case-insensitive)
    correct_answers = [a.lower() for a in question['correct']]
    is_correct = answer.lower() in correct_answers
    
    if is_correct:
        print(colorize("  ✓ Correct!", 'green'))
    else:
        print(colorize(f"  ✗ Wrong. Accepted answers: {', '.join(question['correct'])}", 'red'))
    
    return is_correct


def ask_question(question: Dict, index: int) -> bool:
    """Ask a question based on its type."""
    q_type = question.get('type', 'multiple_choice')
    
    if q_type == 'multiple_choice':
        return ask_multiple_choice(question, index)
    elif q_type == 'fill_blank':
        return ask_fill_blank(question, index)
    else:
        print(f"Unknown question type: {q_type}")
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def print_banner(quiz: Dict) -> None:
    """Print quiz header."""
    meta = quiz.get('metadata', {})
    
    print()
    print(colorize("═" * 60, 'blue'))
    print(colorize(f"  Week {meta.get('week', '?')} Quiz: {meta.get('topic', 'Unknown')}", 'bold'))
    print(colorize("═" * 60, 'blue'))
    print(f"  Questions: {meta.get('total_questions', '?')}")
    print(f"  Estimated time: {meta.get('estimated_time', '?')}")
    print(f"  Passing score: {meta.get('passing_score', 70)}%")
    print(colorize("═" * 60, 'blue'))


def run_quiz(
    quiz: Dict,
    randomize: bool = False,
    limit: Optional[int] = None,
    topic: Optional[str] = None,
    difficulty: Optional[str] = None
) -> float:
    """Run the interactive quiz. Returns score percentage."""
    
    print_banner(quiz)
    
    questions = quiz.get('questions', [])
    questions = filter_questions(questions, topic=topic, difficulty=difficulty)
    
    if not questions:
        print("\nNo questions match the specified filters.")
        return 0.0
    
    if randomize:
        random.shuffle(questions)
    
    if limit and limit < len(questions):
        questions = questions[:limit]
    
    print(f"\n  Starting quiz with {len(questions)} questions...")
    print("  Press Ctrl+C to exit early.\n")
    input("  Press Enter to begin...")
    
    correct = 0
    total = len(questions)
    start_time = time.time()
    
    try:
        for i, question in enumerate(questions, 1):
            if ask_question(question, i):
                correct += 1
    except KeyboardInterrupt:
        print("\n\n  Quiz interrupted.")
        total = i - 1 if i > 1 else 1
    
    elapsed = time.time() - start_time
    score = (correct / total) * 100 if total > 0 else 0
    
    # Print results
    print()
    print(colorize("═" * 60, 'blue'))
    print(colorize("  QUIZ RESULTS", 'bold'))
    print(colorize("═" * 60, 'blue'))
    print(f"  Score: {correct}/{total} ({score:.1f}%)")
    print(f"  Time: {elapsed:.1f} seconds")
    
    # Determine feedback
    passing = quiz.get('metadata', {}).get('passing_score', 70)
    if score >= 90:
        status = colorize("EXCELLENT", 'green')
        feedback = quiz.get('scoring', {}).get('feedback', {}).get('excellent', {}).get('message', '')
    elif score >= passing:
        status = colorize("PASSED", 'green')
        feedback = quiz.get('scoring', {}).get('feedback', {}).get('good', {}).get('message', '')
    elif score >= 50:
        status = colorize("NEEDS REVIEW", 'yellow')
        feedback = quiz.get('scoring', {}).get('feedback', {}).get('needs_review', {}).get('message', '')
    else:
        status = colorize("NEEDS HELP", 'red')
        feedback = quiz.get('scoring', {}).get('feedback', {}).get('needs_help', {}).get('message', '')
    
    print(f"  Status: {status}")
    if feedback:
        print(f"  {feedback}")
    print(colorize("═" * 60, 'blue'))
    print()
    
    return score


def show_review(quiz: Dict) -> None:
    """Show all questions with answers (study mode)."""
    print_banner(quiz)
    print("\n  REVIEW MODE - All questions with answers\n")
    
    for i, q in enumerate(quiz.get('questions', []), 1):
        print(f"\n{colorize(f'Q{i}', 'cyan')} [{q.get('difficulty', '?')}] {q.get('topic', '')}")
        print(f"  {q['stem']}")
        
        if q.get('type') == 'multiple_choice':
            for key, value in q['options'].items():
                marker = colorize('→', 'green') if key == q['correct'] else ' '
                print(f"    {marker} {key.upper()}) {value}")
        else:
            print(f"    Answer: {colorize(', '.join(q['correct']), 'green')}")
        
        if 'explanation' in q:
            print(f"  {colorize('📖', 'yellow')} {q['explanation']}")
        
        if 'misconception_ref' in q:
            print(f"  {colorize('⚠️', 'red')} See: {q['misconception_ref']}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Interactive Quiz Runner for Week 11",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                         Run full quiz
  %(prog)s --random                Randomize questions
  %(prog)s --limit 5               Run only 5 questions
  %(prog)s --topic DNS             Only DNS questions
  %(prog)s --difficulty basic      Only basic questions
  %(prog)s --review                Study mode (show all answers)
        """
    )
    
    parser.add_argument("--quiz", type=Path, 
                        default=Path(__file__).parent / "quiz.yaml",
                        help="Path to quiz YAML file")
    parser.add_argument("--random", action="store_true",
                        help="Randomize question order")
    parser.add_argument("--limit", type=int,
                        help="Limit number of questions")
    parser.add_argument("--topic", type=str,
                        help="Filter by topic (DNS, FTP, SSH, Load Balancing, Nginx)")
    parser.add_argument("--difficulty", type=str,
                        choices=['basic', 'intermediate', 'advanced'],
                        help="Filter by difficulty")
    parser.add_argument("--review", action="store_true",
                        help="Review mode: show all answers")
    
    args = parser.parse_args()
    
    quiz = load_quiz(args.quiz)
    
    if args.review:
        show_review(quiz)
        return 0
    
    score = run_quiz(
        quiz,
        randomize=args.random,
        limit=args.limit,
        topic=args.topic,
        difficulty=args.difficulty
    )
    
    passing = quiz.get('metadata', {}).get('passing_score', 70)
    return 0 if score >= passing else 1


if __name__ == "__main__":
    sys.exit(main())


# Revolvix&Hypotheticalandrei
