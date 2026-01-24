#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  Formative Quiz Runner — Week 3: Network Programming                         ║
║  NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

DESCRIPTION:
    Interactive quiz runner for formative assessment. Loads questions from
    quiz.yaml, presents them interactively, tracks scores per Learning Objective,
    and provides targeted feedback.

USAGE:
    python formative/run_quiz.py                    # Run full quiz
    python formative/run_quiz.py --random           # Randomize question order
    python formative/run_quiz.py --limit 5          # Only 5 questions
    python formative/run_quiz.py --lo LO1 LO2       # Filter by LO
    python formative/run_quiz.py --bloom remember   # Filter by Bloom level
    python formative/run_quiz.py --export results.json  # Export results

REQUIREMENTS:
    pip install pyyaml (already in setup/requirements.txt)

PEDAGOGICAL NOTES:
    - Implements immediate feedback (Brown & Wilson Principle 5)
    - Tracks misconceptions for targeted remediation
    - Provides LO-specific study recommendations
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)


# ════════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ════════════════════════════════════════════════════════════════════════════════

QUIZ_FILE = Path(__file__).parent / "quiz.yaml"
VERSION = "1.0.0"

# ANSI Colors for terminal output
class Colors:
    """ANSI color codes for terminal formatting."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    @classmethod
    def disable(cls) -> None:
        """Disable colors for non-terminal output."""
        cls.HEADER = cls.BLUE = cls.CYAN = cls.GREEN = ''
        cls.YELLOW = cls.RED = cls.BOLD = cls.UNDERLINE = cls.END = ''


# ════════════════════════════════════════════════════════════════════════════════
# QUIZ LOADER
# ════════════════════════════════════════════════════════════════════════════════

def load_quiz(path: Path) -> dict[str, Any]:
    """
    Load quiz from YAML file.
    
    Args:
        path: Path to quiz.yaml file
        
    Returns:
        Parsed quiz dictionary
        
    Raises:
        FileNotFoundError: If quiz file doesn't exist
        yaml.YAMLError: If YAML is malformed
    """
    if not path.exists():
        raise FileNotFoundError(f"Quiz file not found: {path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def filter_questions(
    questions: list[dict],
    lo_filter: list[str] | None = None,
    bloom_filter: str | None = None,
    limit: int | None = None,
    randomize: bool = False
) -> list[dict]:
    """
    Filter and optionally randomize questions.
    
    Args:
        questions: List of question dictionaries
        lo_filter: Only include questions for these LOs
        bloom_filter: Only include questions at this Bloom level
        limit: Maximum number of questions
        randomize: Whether to shuffle questions
        
    Returns:
        Filtered list of questions
    """
    filtered = questions.copy()
    
    if lo_filter:
        filtered = [q for q in filtered if q.get('lo_ref') in lo_filter]
    
    if bloom_filter:
        filtered = [q for q in filtered if q.get('bloom_level') == bloom_filter]
    
    if randomize:
        random.shuffle(filtered)
    
    if limit:
        filtered = filtered[:limit]
    
    return filtered


# ════════════════════════════════════════════════════════════════════════════════
# QUESTION PRESENTER
# ════════════════════════════════════════════════════════════════════════════════

def present_multiple_choice(question: dict, q_num: int, total: int) -> tuple[bool, str]:
    """
    Present a multiple choice question and get answer.
    
    Args:
        question: Question dictionary
        q_num: Current question number
        total: Total questions
        
    Returns:
        Tuple of (is_correct, user_answer)
    """
    c = Colors
    
    print(f"\n{c.BOLD}{'═' * 70}{c.END}")
    print(f"{c.CYAN}Question {q_num}/{total}{c.END} │ "
          f"{c.YELLOW}[{question['bloom_level'].upper()}]{c.END} │ "
          f"{c.BLUE}{question['lo_ref']}{c.END} │ "
          f"Points: {question['points']}")
    print(f"{'─' * 70}")
    
    # Display stem
    print(f"\n{question['stem'].strip()}\n")
    
    # Display options
    for key, value in question['options'].items():
        print(f"  {c.BOLD}{key}){c.END} {value}")
    
    # Get answer
    print()
    while True:
        answer = input(f"{c.CYAN}Your answer (a/b/c/d): {c.END}").strip().lower()
        if answer in question['options']:
            break
        print(f"{c.RED}Invalid option. Please enter a, b, c, or d.{c.END}")
    
    # Check answer
    is_correct = answer == question['correct']
    
    return is_correct, answer


def present_fill_blank(question: dict, q_num: int, total: int) -> tuple[bool, str]:
    """
    Present a fill-in-the-blank question.
    
    Args:
        question: Question dictionary
        q_num: Current question number
        total: Total questions
        
    Returns:
        Tuple of (is_correct, user_answer)
    """
    c = Colors
    
    print(f"\n{c.BOLD}{'═' * 70}{c.END}")
    print(f"{c.CYAN}Question {q_num}/{total}{c.END} │ "
          f"{c.YELLOW}[{question['bloom_level'].upper()}]{c.END} │ "
          f"{c.BLUE}{question['lo_ref']}{c.END} │ "
          f"Points: {question['points']}")
    print(f"{'─' * 70}")
    
    # Display stem
    print(f"\n{question['stem'].strip()}\n")
    
    # Display hint if available
    if 'hint' in question:
        print(f"{c.YELLOW}💡 Hint: {question['hint']}{c.END}\n")
    
    # Get answer
    answer = input(f"{c.CYAN}Your answer: {c.END}").strip()
    
    # Check answer (case-insensitive, multiple correct answers possible)
    correct_answers = [a.lower() for a in question['correct']]
    is_correct = answer.lower() in correct_answers
    
    return is_correct, answer


def show_feedback(question: dict, is_correct: bool, user_answer: str) -> None:
    """
    Display immediate feedback for a question.
    
    Args:
        question: Question dictionary
        is_correct: Whether the answer was correct
        user_answer: The user's answer
    """
    c = Colors
    
    print()
    if is_correct:
        print(f"{c.GREEN}✓ CORRECT!{c.END} +{question['points']} points")
    else:
        print(f"{c.RED}✗ INCORRECT{c.END}")
        if question['type'] == 'multiple_choice':
            print(f"  Correct answer: {c.BOLD}{question['correct']}{c.END})")
        else:
            print(f"  Accepted answers: {c.BOLD}{', '.join(question['correct'])}{c.END}")
    
    # Show explanation
    if 'explanation' in question:
        print(f"\n{c.CYAN}📖 Explanation:{c.END}")
        for line in question['explanation'].strip().split('\n'):
            print(f"   {line.strip()}")
    
    # Show misconception reference
    if not is_correct and 'misconception_ref' in question:
        print(f"\n{c.YELLOW}📚 See also: {question['misconception_ref']}{c.END}")
    
    print()
    input(f"{c.CYAN}Press Enter to continue...{c.END}")


# ════════════════════════════════════════════════════════════════════════════════
# QUIZ RUNNER
# ════════════════════════════════════════════════════════════════════════════════

class QuizSession:
    """Manages a quiz session with scoring and analytics."""
    
    def __init__(self, quiz: dict[str, Any], questions: list[dict]):
        """
        Initialize quiz session.
        
        Args:
            quiz: Full quiz dictionary with metadata
            questions: Filtered list of questions to present
        """
        self.quiz = quiz
        self.questions = questions
        self.metadata = quiz['metadata']
        self.scoring = quiz['scoring']
        
        # Session state
        self.start_time: float = 0
        self.end_time: float = 0
        self.total_points = 0
        self.earned_points = 0
        self.results: list[dict] = []
        
        # Analytics
        self.lo_scores: dict[str, dict] = {}  # {LO: {earned, total, questions}}
        self.bloom_scores: dict[str, dict] = {}
        self.misconceptions_hit: list[str] = []
    
    def run(self) -> dict[str, Any]:
        """
        Run the interactive quiz session.
        
        Returns:
            Session results dictionary
        """
        c = Colors
        
        # Header
        self._print_header()
        
        # Confirm start
        input(f"\n{c.CYAN}Press Enter to begin the quiz...{c.END}")
        self.start_time = time.time()
        
        # Present each question
        for i, question in enumerate(self.questions, 1):
            self.total_points += question['points']
            
            # Present based on type
            if question['type'] == 'multiple_choice':
                is_correct, answer = present_multiple_choice(question, i, len(self.questions))
            elif question['type'] == 'fill_blank':
                is_correct, answer = present_fill_blank(question, i, len(self.questions))
            else:
                print(f"{c.RED}Unknown question type: {question['type']}{c.END}")
                continue
            
            # Show feedback
            show_feedback(question, is_correct, answer)
            
            # Record result
            if is_correct:
                self.earned_points += question['points']
            
            self._record_result(question, is_correct, answer)
        
        self.end_time = time.time()
        
        # Show final results
        return self._show_results()
    
    def _print_header(self) -> None:
        """Print quiz header with metadata."""
        c = Colors
        m = self.metadata
        
        print(f"\n{c.BOLD}{'═' * 70}{c.END}")
        print(f"{c.HEADER}╔══════════════════════════════════════════════════════════════════════╗{c.END}")
        print(f"{c.HEADER}║  FORMATIVE QUIZ — {m['title'][:50]:<50} ║{c.END}")
        print(f"{c.HEADER}╠══════════════════════════════════════════════════════════════════════╣{c.END}")
        print(f"{c.HEADER}║  Institution: {m['institution']:<54} ║{c.END}")
        print(f"{c.HEADER}║  Course: {m['course']:<59} ║{c.END}")
        print(f"{c.HEADER}║  Author: {m['author']:<59} ║{c.END}")
        print(f"{c.HEADER}╠══════════════════════════════════════════════════════════════════════╣{c.END}")
        print(f"{c.HEADER}║  Questions: {len(self.questions):<10} Estimated time: {m['estimated_time_minutes']} min{' ' * 26}║{c.END}")
        print(f"{c.HEADER}║  Passing score: {m['passing_score']}%{' ' * 51}║{c.END}")
        print(f"{c.HEADER}╚══════════════════════════════════════════════════════════════════════╝{c.END}")
    
    def _record_result(self, question: dict, is_correct: bool, answer: str) -> None:
        """Record question result for analytics."""
        lo = question.get('lo_ref', 'Unknown')
        bloom = question.get('bloom_level', 'unknown')
        points = question['points']
        
        # Record to results list
        self.results.append({
            'id': question['id'],
            'lo_ref': lo,
            'bloom_level': bloom,
            'points': points,
            'earned': points if is_correct else 0,
            'correct': is_correct,
            'user_answer': answer,
            'correct_answer': question.get('correct')
        })
        
        # Update LO scores
        if lo not in self.lo_scores:
            self.lo_scores[lo] = {'earned': 0, 'total': 0, 'count': 0}
        self.lo_scores[lo]['total'] += points
        self.lo_scores[lo]['count'] += 1
        if is_correct:
            self.lo_scores[lo]['earned'] += points
        
        # Update Bloom scores
        if bloom not in self.bloom_scores:
            self.bloom_scores[bloom] = {'earned': 0, 'total': 0, 'count': 0}
        self.bloom_scores[bloom]['total'] += points
        self.bloom_scores[bloom]['count'] += 1
        if is_correct:
            self.bloom_scores[bloom]['earned'] += points
        
        # Track misconceptions
        if not is_correct and 'misconception_ref' in question:
            self.misconceptions_hit.append(question['misconception_ref'])
    
    def _show_results(self) -> dict[str, Any]:
        """Display final results and return summary."""
        c = Colors
        
        duration = self.end_time - self.start_time
        percentage = (self.earned_points / self.total_points * 100) if self.total_points > 0 else 0
        passed = percentage >= self.metadata['passing_score']
        
        # Determine grade
        grade = "Insuficient"
        feedback = ""
        for band in self.scoring['grade_bands']:
            if band['range'][0] <= self.earned_points <= band['range'][1]:
                grade = band['grade']
                feedback = band['feedback']
                break
        
        # Print results
        print(f"\n{c.BOLD}{'═' * 70}{c.END}")
        print(f"{c.HEADER}╔══════════════════════════════════════════════════════════════════════╗{c.END}")
        print(f"{c.HEADER}║                         QUIZ RESULTS                                 ║{c.END}")
        print(f"{c.HEADER}╚══════════════════════════════════════════════════════════════════════╝{c.END}")
        
        print(f"\n{c.BOLD}Score:{c.END} {self.earned_points}/{self.total_points} points ({percentage:.1f}%)")
        print(f"{c.BOLD}Grade:{c.END} {grade}")
        print(f"{c.BOLD}Time:{c.END} {duration:.0f} seconds")
        
        if passed:
            print(f"\n{c.GREEN}{'═' * 70}{c.END}")
            print(f"{c.GREEN}✓ PASSED — Congratulations!{c.END}")
            print(f"{c.GREEN}{'═' * 70}{c.END}")
        else:
            print(f"\n{c.RED}{'═' * 70}{c.END}")
            print(f"{c.RED}✗ NOT PASSED — Review required{c.END}")
            print(f"{c.RED}{'═' * 70}{c.END}")
        
        print(f"\n{c.CYAN}Feedback:{c.END} {feedback}")
        
        # LO breakdown
        print(f"\n{c.BOLD}Performance by Learning Objective:{c.END}")
        print(f"{'─' * 50}")
        for lo, data in sorted(self.lo_scores.items()):
            lo_pct = (data['earned'] / data['total'] * 100) if data['total'] > 0 else 0
            bar = '█' * int(lo_pct / 10) + '░' * (10 - int(lo_pct / 10))
            status = c.GREEN + '✓' if lo_pct >= 70 else c.RED + '✗'
            print(f"  {lo}: [{bar}] {lo_pct:5.1f}% ({data['earned']}/{data['total']}) {status}{c.END}")
        
        # Bloom breakdown
        print(f"\n{c.BOLD}Performance by Bloom Level:{c.END}")
        print(f"{'─' * 50}")
        for bloom in ['remember', 'understand', 'apply', 'analyze']:
            if bloom in self.bloom_scores:
                data = self.bloom_scores[bloom]
                pct = (data['earned'] / data['total'] * 100) if data['total'] > 0 else 0
                bar = '█' * int(pct / 10) + '░' * (10 - int(pct / 10))
                print(f"  {bloom.capitalize():12}: [{bar}] {pct:5.1f}%")
        
        # Recommendations
        if self.misconceptions_hit or not passed:
            print(f"\n{c.YELLOW}📚 Recommended Study:{c.END}")
            weak_los = [lo for lo, data in self.lo_scores.items() 
                       if (data['earned'] / data['total'] * 100) < 70]
            for lo in weak_los:
                if lo in self.scoring.get('lo_feedback', {}):
                    print(f"  • {lo}: {self.scoring['lo_feedback'][lo]}")
            
            if self.misconceptions_hit:
                print(f"\n{c.YELLOW}📖 Review these misconceptions:{c.END}")
                for ref in set(self.misconceptions_hit):
                    print(f"  • {ref}")
        
        print(f"\n{c.BOLD}{'═' * 70}{c.END}")
        
        # Return summary
        return {
            'timestamp': datetime.now().isoformat(),
            'score': self.earned_points,
            'total': self.total_points,
            'percentage': percentage,
            'passed': passed,
            'grade': grade,
            'duration_seconds': duration,
            'lo_scores': self.lo_scores,
            'bloom_scores': self.bloom_scores,
            'misconceptions_hit': list(set(self.misconceptions_hit)),
            'results': self.results
        }


# ════════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ════════════════════════════════════════════════════════════════════════════════

def build_parser() -> argparse.ArgumentParser:
    """Build argument parser."""
    parser = argparse.ArgumentParser(
        prog="run_quiz.py",
        description="Formative Quiz Runner for Week 3 Network Programming",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_quiz.py                      # Full quiz
  python run_quiz.py --random --limit 5   # 5 random questions
  python run_quiz.py --lo LO1 LO2         # Only LO1 and LO2 questions
  python run_quiz.py --bloom remember     # Only 'remember' level
  python run_quiz.py --export report.json # Save results to file
        """
    )
    
    parser.add_argument(
        '--quiz', '-q',
        type=Path,
        default=QUIZ_FILE,
        help=f"Path to quiz YAML file (default: {QUIZ_FILE})"
    )
    
    parser.add_argument(
        '--random', '-r',
        action='store_true',
        help="Randomize question order"
    )
    
    parser.add_argument(
        '--limit', '-n',
        type=int,
        help="Maximum number of questions"
    )
    
    parser.add_argument(
        '--lo',
        nargs='+',
        help="Filter by Learning Objectives (e.g., --lo LO1 LO2)"
    )
    
    parser.add_argument(
        '--bloom',
        choices=['remember', 'understand', 'apply', 'analyze'],
        help="Filter by Bloom level"
    )
    
    parser.add_argument(
        '--export', '-e',
        type=Path,
        help="Export results to JSON file"
    )
    
    parser.add_argument(
        '--no-color',
        action='store_true',
        help="Disable colored output"
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version=f"%(prog)s {VERSION}"
    )
    
    return parser


def main(argv: list[str] | None = None) -> int:
    """
    Main entry point.
    
    Args:
        argv: Command line arguments (uses sys.argv if None)
        
    Returns:
        Exit code (0 for pass, 1 for fail, 2 for error)
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    
    # Disable colors if requested
    if args.no_color:
        Colors.disable()
    
    try:
        # Load quiz
        quiz = load_quiz(args.quiz)
        
        # Filter questions
        questions = filter_questions(
            quiz['questions'],
            lo_filter=args.lo,
            bloom_filter=args.bloom,
            limit=args.limit,
            randomize=args.random
        )
        
        if not questions:
            print(f"{Colors.RED}No questions match the specified filters.{Colors.END}")
            return 2
        
        # Run quiz
        session = QuizSession(quiz, questions)
        results = session.run()
        
        # Export if requested
        if args.export:
            with open(args.export, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\n{Colors.GREEN}Results exported to: {args.export}{Colors.END}")
        
        # Return exit code based on pass/fail
        return 0 if results['passed'] else 1
        
    except FileNotFoundError as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")
        return 2
    except yaml.YAMLError as e:
        print(f"{Colors.RED}Error parsing YAML: {e}{Colors.END}")
        return 2
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Quiz cancelled.{Colors.END}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
