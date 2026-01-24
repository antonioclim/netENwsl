#!/usr/bin/env python3
"""
Formative Quiz Runner — Week 5: IP Addressing, Subnetting, VLSM
================================================================
Interactive CLI for running self-assessment quizzes from YAML definitions.

Usage:
    python formative/run_quiz.py                    # Run full quiz
    python formative/run_quiz.py --random           # Randomize question order
    python formative/run_quiz.py --limit 5          # Run only 5 questions
    python formative/run_quiz.py --category apply   # Filter by Bloom level
    python formative/run_quiz.py --review           # Show answers after each question
    python formative/run_quiz.py --export report.md # Export results to markdown

Learning Objectives:
    - Reinforce concepts through active recall
    - Identify knowledge gaps via immediate feedback
    - Track progress across multiple attempts

Author: ing. dr. Antonio Clim, ASE-CSIE Bucharest
Version: 1.0.0 (January 2026)
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import random
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# DEFINE_COLOUR_CODES
# ═══════════════════════════════════════════════════════════════════════════════
class Colours:
    """ANSI colour codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'


def colourise(text: str, colour: str) -> str:
    """Apply colour formatting if stdout is a terminal."""
    if sys.stdout.isatty():
        return f"{colour}{text}{Colours.END}"
    return text


# ═══════════════════════════════════════════════════════════════════════════════
# DEFINE_DATA_STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class QuizResult:
    """Result of a single question attempt."""
    question_id: str
    correct: bool
    user_answer: str
    correct_answer: str
    points_earned: int
    points_possible: int
    time_seconds: float
    bloom_level: str
    lo_ref: str


@dataclass
class QuizSession:
    """Complete quiz session data."""
    quiz_topic: str
    start_time: datetime
    end_time: Optional[datetime] = None
    results: List[QuizResult] = field(default_factory=list)
    total_points: int = 0
    max_points: int = 0
    
    @property
    def score_percentage(self) -> float:
        """Calculate percentage score."""
        if self.max_points == 0:
            return 0.0
        return (self.total_points / self.max_points) * 100
    
    @property
    def duration_minutes(self) -> float:
        """Calculate quiz duration in minutes."""
        if not self.end_time:
            return 0.0
        delta = self.end_time - self.start_time
        return delta.total_seconds() / 60


# ═══════════════════════════════════════════════════════════════════════════════
# LOAD_QUIZ_DATA
# ═══════════════════════════════════════════════════════════════════════════════
def load_quiz(path: Path) -> Dict[str, Any]:
    """
    Load quiz definition from YAML file.
    
    Args:
        path: Path to quiz YAML file
        
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


# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY_QUESTION
# ═══════════════════════════════════════════════════════════════════════════════
def display_question(q: Dict[str, Any], index: int, total: int) -> None:
    """Display a single question with formatting."""
    print()
    print(colourise("─" * 60, Colours.DIM))
    
    # Header with metadata
    difficulty_colours = {
        'basic': Colours.GREEN,
        'intermediate': Colours.YELLOW,
        'advanced': Colours.RED
    }
    diff = q.get('difficulty', 'unknown')
    diff_colour = difficulty_colours.get(diff, Colours.CYAN)
    
    print(f"  Question {colourise(f'{index}/{total}', Colours.BOLD)}"
          f"  [{colourise(diff.upper(), diff_colour)}]"
          f"  {colourise(f'LO: {q.get(\"lo_ref\", \"?\")}', Colours.DIM)}"
          f"  {colourise(f'{q.get(\"points\", 1)} pts', Colours.CYAN)}")
    print()
    
    # Question stem
    stem = q.get('stem', '').strip()
    for line in stem.split('\n'):
        print(f"  {line}")
    print()
    
    # Options for multiple choice
    if q.get('type') == 'multiple_choice':
        options = q.get('options', {})
        for key, value in sorted(options.items()):
            print(f"    {colourise(key.upper(), Colours.CYAN)}) {value}")
        print()


def display_feedback(q: Dict[str, Any], user_answer: str, correct: bool, 
                     show_review: bool = False) -> None:
    """Display feedback after answering."""
    if correct:
        print(colourise("  ✅ Correct!", Colours.GREEN))
    else:
        correct_answer = q.get('correct', '?')
        if isinstance(correct_answer, list):
            correct_answer = ', '.join(correct_answer)
        print(colourise(f"  ❌ Incorrect. Correct answer: {correct_answer}", Colours.RED))
    
    if show_review or not correct:
        explanation = q.get('explanation', '').strip()
        if explanation:
            print()
            print(colourise("  📖 Explanation:", Colours.YELLOW))
            for line in explanation.split('\n'):
                print(f"     {line}")
        
        # Show verification command if available
        verification = q.get('verification_cmd')
        if verification:
            print()
            print(colourise(f"  🔍 Verify: {verification}", Colours.DIM))


# ═══════════════════════════════════════════════════════════════════════════════
# GET_USER_ANSWER
# ═══════════════════════════════════════════════════════════════════════════════
def get_user_answer(q: Dict[str, Any]) -> str:
    """Get and validate user input based on question type."""
    q_type = q.get('type', 'multiple_choice')
    
    if q_type == 'multiple_choice':
        valid_options = list(q.get('options', {}).keys())
        while True:
            answer = input(colourise("  Your answer: ", Colours.CYAN)).strip().lower()
            if answer in valid_options:
                return answer
            if answer == 'q':
                return 'quit'
            if answer == 's':
                return 'skip'
            if answer == 'h' and q.get('hint'):
                print(colourise(f"  💡 Hint: {q['hint']}", Colours.YELLOW))
                continue
            print(f"  Please enter one of: {', '.join(valid_options)} (or 'h' for hint, 's' to skip, 'q' to quit)")
    
    elif q_type == 'fill_blank':
        answer = input(colourise("  Your answer: ", Colours.CYAN)).strip()
        if answer.lower() == 'q':
            return 'quit'
        if answer.lower() == 's':
            return 'skip'
        if answer.lower() == 'h' and q.get('hint'):
            print(colourise(f"  💡 Hint: {q['hint']}", Colours.YELLOW))
            return get_user_answer(q)  # Recursively ask again
        return answer
    
    return input(colourise("  Your answer: ", Colours.CYAN)).strip()


def check_answer(q: Dict[str, Any], user_answer: str) -> bool:
    """Check if user's answer is correct."""
    correct = q.get('correct')
    
    if isinstance(correct, list):
        # Multiple acceptable answers (fill_blank)
        return user_answer.lower() in [str(c).lower() for c in correct]
    else:
        # Single correct answer
        return user_answer.lower() == str(correct).lower()


# ═══════════════════════════════════════════════════════════════════════════════
# RUN_QUIZ_SESSION
# ═══════════════════════════════════════════════════════════════════════════════
def run_quiz(quiz: Dict[str, Any], randomize: bool = False, limit: Optional[int] = None,
             category: Optional[str] = None, show_review: bool = False) -> QuizSession:
    """
    Run an interactive quiz session.
    
    Args:
        quiz: Loaded quiz dictionary
        randomize: Whether to shuffle questions
        limit: Maximum number of questions to ask
        category: Filter by Bloom level (remember, understand, apply, analyze)
        show_review: Show explanations even for correct answers
        
    Returns:
        QuizSession with results
    """
    metadata = quiz.get('metadata', {})
    questions = quiz.get('questions', [])
    
    # Filter by Bloom level if specified
    if category:
        questions = [q for q in questions if q.get('bloom_level', '').lower() == category.lower()]
    
    # Randomize if requested
    if randomize:
        questions = questions.copy()
        random.shuffle(questions)
    
    # Limit number of questions
    if limit and limit < len(questions):
        questions = questions[:limit]
    
    # Initialize session
    session = QuizSession(
        quiz_topic=metadata.get('topic', 'Unknown'),
        start_time=datetime.now()
    )
    
    # Display header
    print()
    print(colourise("═" * 60, Colours.BLUE))
    print(colourise(f"  📝 QUIZ: {metadata.get('topic', 'Unknown')}", Colours.BOLD))
    print(colourise("═" * 60, Colours.BLUE))
    print()
    print(f"  Questions: {len(questions)}")
    print(f"  Passing score: {metadata.get('passing_score', 70)}%")
    print(f"  Estimated time: {metadata.get('estimated_time_minutes', '?')} minutes")
    print()
    print(colourise("  Commands: 'h' = hint, 's' = skip, 'q' = quit", Colours.DIM))
    print()
    input(colourise("  Press Enter to begin...", Colours.CYAN))
    
    # Run through questions
    for i, q in enumerate(questions, 1):
        q_start = time.time()
        
        display_question(q, i, len(questions))
        user_answer = get_user_answer(q)
        
        q_time = time.time() - q_start
        
        if user_answer == 'quit':
            print(colourise("\n  Quiz ended early.", Colours.YELLOW))
            break
        
        if user_answer == 'skip':
            result = QuizResult(
                question_id=q.get('id', f'q{i}'),
                correct=False,
                user_answer='[SKIPPED]',
                correct_answer=str(q.get('correct', '?')),
                points_earned=0,
                points_possible=q.get('points', 1),
                time_seconds=q_time,
                bloom_level=q.get('bloom_level', 'unknown'),
                lo_ref=q.get('lo_ref', 'unknown')
            )
        else:
            correct = check_answer(q, user_answer)
            points = q.get('points', 1) if correct else 0
            
            result = QuizResult(
                question_id=q.get('id', f'q{i}'),
                correct=correct,
                user_answer=user_answer,
                correct_answer=str(q.get('correct', '?')),
                points_earned=points,
                points_possible=q.get('points', 1),
                time_seconds=q_time,
                bloom_level=q.get('bloom_level', 'unknown'),
                lo_ref=q.get('lo_ref', 'unknown')
            )
            
            display_feedback(q, user_answer, correct, show_review)
        
        session.results.append(result)
        session.total_points += result.points_earned
        session.max_points += result.points_possible
    
    session.end_time = datetime.now()
    return session


# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def display_results(session: QuizSession, quiz: Dict[str, Any]) -> None:
    """Display final quiz results and feedback."""
    print()
    print(colourise("═" * 60, Colours.BLUE))
    print(colourise("  📊 QUIZ RESULTS", Colours.BOLD))
    print(colourise("═" * 60, Colours.BLUE))
    print()
    
    # Score
    score = session.score_percentage
    if score >= 90:
        score_colour = Colours.GREEN
    elif score >= 70:
        score_colour = Colours.YELLOW
    else:
        score_colour = Colours.RED
    
    print(f"  Score: {colourise(f'{session.total_points}/{session.max_points}', score_colour)}"
          f" ({colourise(f'{score:.1f}%', score_colour)})")
    print(f"  Time: {session.duration_minutes:.1f} minutes")
    print()
    
    # Results by question
    print(colourise("  Question Results:", Colours.CYAN))
    for r in session.results:
        status = colourise("✅", Colours.GREEN) if r.correct else colourise("❌", Colours.RED)
        print(f"    {status} {r.question_id}: {r.points_earned}/{r.points_possible} pts "
              f"({r.bloom_level}, {r.lo_ref})")
    print()
    
    # Breakdown by Bloom level
    bloom_stats: Dict[str, Dict[str, int]] = {}
    for r in session.results:
        level = r.bloom_level
        if level not in bloom_stats:
            bloom_stats[level] = {'correct': 0, 'total': 0}
        bloom_stats[level]['total'] += 1
        if r.correct:
            bloom_stats[level]['correct'] += 1
    
    print(colourise("  Performance by Bloom Level:", Colours.CYAN))
    for level in ['remember', 'understand', 'apply', 'analyze']:
        if level in bloom_stats:
            stats = bloom_stats[level]
            pct = (stats['correct'] / stats['total']) * 100 if stats['total'] > 0 else 0
            print(f"    {level.capitalize():12} {stats['correct']}/{stats['total']} ({pct:.0f}%)")
    print()
    
    # Feedback based on score
    feedback = quiz.get('feedback', {})
    passing = quiz.get('metadata', {}).get('passing_score', 70)
    
    if score >= 90:
        print(colourise("  " + feedback.get('score_90_100', '🏆 Excellent work!'), Colours.GREEN))
    elif score >= 70:
        print(colourise("  " + feedback.get('score_70_89', '✅ Good job!'), Colours.YELLOW))
    elif score >= 50:
        print(colourise("  " + feedback.get('score_50_69', '⚠️ Needs improvement.'), Colours.YELLOW))
    else:
        print(colourise("  " + feedback.get('score_below_50', '📚 Please review the materials.'), Colours.RED))
    
    print()
    if score >= passing:
        print(colourise(f"  ✅ PASSED (≥{passing}%)", Colours.GREEN))
    else:
        print(colourise(f"  ❌ NOT PASSED (<{passing}%)", Colours.RED))
    
    print()
    print(colourise("═" * 60, Colours.BLUE))


def export_results(session: QuizSession, path: Path) -> None:
    """Export quiz results to markdown file."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"# Quiz Results: {session.quiz_topic}\n\n")
        f.write(f"**Date**: {session.start_time.strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**Score**: {session.total_points}/{session.max_points} ({session.score_percentage:.1f}%)\n")
        f.write(f"**Duration**: {session.duration_minutes:.1f} minutes\n\n")
        
        f.write("## Question Results\n\n")
        f.write("| Question | Correct | Points | Bloom | LO |\n")
        f.write("|----------|---------|--------|-------|----|\n")
        for r in session.results:
            status = "✅" if r.correct else "❌"
            f.write(f"| {r.question_id} | {status} | {r.points_earned}/{r.points_possible} | "
                    f"{r.bloom_level} | {r.lo_ref} |\n")
    
    print(f"\nResults exported to: {path}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for quiz runner."""
    parser = argparse.ArgumentParser(
        description="Week 5 Formative Quiz Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          Run full quiz
  %(prog)s --random                 Randomize questions
  %(prog)s --limit 5                Run only 5 questions
  %(prog)s --category apply         Filter by Bloom level
  %(prog)s --review                 Show explanations for all answers
  %(prog)s --export results.md      Export results to file
  %(prog)s --quiz custom.yaml       Use custom quiz file
"""
    )
    
    parser.add_argument(
        '--quiz', '-q',
        type=Path,
        default=Path(__file__).parent / 'quiz.yaml',
        help='Path to quiz YAML file (default: formative/quiz.yaml)'
    )
    parser.add_argument(
        '--random', '-r',
        action='store_true',
        help='Randomize question order'
    )
    parser.add_argument(
        '--limit', '-l',
        type=int,
        help='Maximum number of questions'
    )
    parser.add_argument(
        '--category', '-c',
        choices=['remember', 'understand', 'apply', 'analyze'],
        help='Filter by Bloom taxonomy level'
    )
    parser.add_argument(
        '--review',
        action='store_true',
        help='Show explanations even for correct answers'
    )
    parser.add_argument(
        '--export', '-e',
        type=Path,
        help='Export results to markdown file'
    )
    
    args = parser.parse_args(argv)
    
    # Load quiz
    try:
        quiz = load_quiz(args.quiz)
    except FileNotFoundError as e:
        print(colourise(f"Error: {e}", Colours.RED))
        return 1
    except yaml.YAMLError as e:
        print(colourise(f"Error parsing quiz file: {e}", Colours.RED))
        return 1
    
    # Run quiz
    try:
        session = run_quiz(
            quiz,
            randomize=args.random,
            limit=args.limit,
            category=args.category,
            show_review=args.review
        )
    except KeyboardInterrupt:
        print(colourise("\n\nQuiz cancelled.", Colours.YELLOW))
        return 1
    
    # Display results
    display_results(session, quiz)
    
    # Export if requested
    if args.export:
        export_results(session, args.export)
    
    # Return exit code based on pass/fail
    passing = quiz.get('metadata', {}).get('passing_score', 70)
    return 0 if session.score_percentage >= passing else 1


if __name__ == "__main__":
    sys.exit(main())
