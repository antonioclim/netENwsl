#!/usr/bin/env python3
"""
Formative Quiz Runner — Week 7
==============================
NETWORKING class - ASE, Informatics | Computer Networks Laboratory

Interactive quiz runner for self-assessment on packet capture and filtering concepts.
Supports multiple modes: full quiz, random sampling, LO-specific and review mode.

Usage:
    python3 formative/run_quiz.py                    # Full quiz
    python3 formative/run_quiz.py --random --limit 5 # 5 random questions
    python3 formative/run_quiz.py --lo LO1           # LO1 questions only
    python3 formative/run_quiz.py --review           # Show answers
    python3 formative/run_quiz.py --export-json      # Export results to JSON

Requirements:
    pip install pyyaml colorama
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
from typing import Any, Optional

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(2)

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    # Stub colour codes
    class Fore:
        GREEN = RED = YELLOW = CYAN = BLUE = MAGENTA = WHITE = ""
    class Style:
        BRIGHT = RESET_ALL = ""


# ═══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Question:
    """Represents a single quiz question."""
    id: str
    type: str
    stem: str
    points: int
    correct_answer: Any
    lo_ref: str
    bloom_level: str
    difficulty: str
    options: Optional[dict[str, str]] = None
    explanation: str = ""
    verify_command: str = ""
    
    def display(self, show_answer: bool = False) -> None:
        """Display the question to the terminal."""
        print()
        print(f"{Fore.CYAN}╔{'═' * 68}╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.YELLOW}[{self.id}]{Style.RESET_ALL} {self.stem[:60]}")
        if len(self.stem) > 60:
            for line in [self.stem[i:i+66] for i in range(60, len(self.stem), 66)]:
                print(f"{Fore.CYAN}║{Style.RESET_ALL}        {line}")
        print(f"{Fore.CYAN}╟{'─' * 68}╢{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} LO: {self.lo_ref} | Bloom: {self.bloom_level} | Points: {self.points}")
        print(f"{Fore.CYAN}╚{'═' * 68}╝{Style.RESET_ALL}")
        
        if self.type == "multiple_choice" and self.options:
            print()
            for key, text in self.options.items():
                marker = f"{Fore.GREEN}►" if show_answer and key == self.correct_answer else " "
                print(f"  {marker} {key}) {text}{Style.RESET_ALL}")
        
        if show_answer:
            print()
            print(f"{Fore.GREEN}✓ Correct answer: {self.correct_answer}{Style.RESET_ALL}")
            if self.explanation:
                print(f"\n{Fore.CYAN}Explanation:{Style.RESET_ALL}")
                for line in self.explanation.strip().split('\n'):
                    print(f"  {line}")


@dataclass
class QuizSession:
    """Tracks a quiz session."""
    questions: list[Question]
    answers: dict[str, Any] = field(default_factory=dict)
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    
    def start(self) -> None:
        """Mark session start."""
        self.start_time = time.time()
    
    def finish(self) -> None:
        """Mark session end."""
        self.end_time = time.time()
    
    @property
    def duration_seconds(self) -> float:
        """Get session duration in seconds."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0
    
    @property
    def score(self) -> tuple[int, int]:
        """Calculate score as (earned, possible)."""
        earned = 0
        possible = sum(q.points for q in self.questions)
        
        for q in self.questions:
            if q.id in self.answers:
                user_answer = self.answers[q.id]
                if self._check_answer(q, user_answer):
                    earned += q.points
        
        return earned, possible
    
    def _check_answer(self, question: Question, answer: Any) -> bool:
        """Check if answer is correct."""
        if question.type == "multiple_choice":
            return str(answer).lower() == str(question.correct_answer).lower()
        elif question.type == "fill_blank":
            if isinstance(question.correct_answer, list):
                # For fill-blank, check each blank
                if isinstance(answer, list):
                    return all(
                        str(a).lower() == str(c).lower()
                        for a, c in zip(answer, question.correct_answer)
                    )
            return str(answer).lower() == str(question.correct_answer).lower()
        elif question.type == "ordering":
            return answer == question.correct_answer
        elif question.type == "true_false":
            return str(answer).lower() in ("true", "t", "1") if question.correct_answer else str(answer).lower() in ("false", "f", "0")
        return False
    
    def to_dict(self) -> dict[str, Any]:
        """Convert session to dictionary for JSON export."""
        earned, possible = self.score
        return {
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": self.duration_seconds,
            "questions_attempted": len(self.answers),
            "questions_total": len(self.questions),
            "score_earned": earned,
            "score_possible": possible,
            "percentage": round(earned / possible * 100, 1) if possible > 0 else 0,
            "answers": {
                q.id: {
                    "user_answer": self.answers.get(q.id),
                    "correct_answer": q.correct_answer,
                    "correct": self._check_answer(q, self.answers.get(q.id)) if q.id in self.answers else False,
                    "points": q.points,
                    "lo_ref": q.lo_ref,
                }
                for q in self.questions
            },
            "lo_breakdown": self._get_lo_breakdown(),
        }
    
    def _get_lo_breakdown(self) -> dict[str, dict[str, int]]:
        """Get score breakdown by Learning Objective."""
        breakdown = {}
        for q in self.questions:
            lo = q.lo_ref
            if lo not in breakdown:
                breakdown[lo] = {"earned": 0, "possible": 0}
            breakdown[lo]["possible"] += q.points
            if q.id in self.answers and self._check_answer(q, self.answers[q.id]):
                breakdown[lo]["earned"] += q.points
        return breakdown


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ LOADER
# ═══════════════════════════════════════════════════════════════════════════════

def load_quiz(path: Path) -> tuple[dict[str, Any], list[Question]]:
    """
    Load quiz from YAML file.
    
    Args:
        path: Path to quiz.yaml
        
    Returns:
        Tuple of (metadata, questions)
    """
    if not path.exists():
        raise FileNotFoundError(f"Quiz file not found: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    metadata = data.get("metadata", {})
    questions = []
    
    for q_data in data.get("questions", []):
        question = Question(
            id=q_data.get("id", ""),
            type=q_data.get("type", "multiple_choice"),
            stem=q_data.get("stem", ""),
            points=q_data.get("points", 1),
            correct_answer=q_data.get("correct") or q_data.get("correct_order", ""),
            lo_ref=q_data.get("lo_ref", ""),
            bloom_level=q_data.get("bloom_level", ""),
            difficulty=q_data.get("difficulty", ""),
            options=q_data.get("options"),
            explanation=q_data.get("explanation", ""),
            verify_command=q_data.get("verify_command", ""),
        )
        questions.append(question)
    
    return metadata, questions


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def run_interactive_quiz(session: QuizSession) -> None:
    """Run interactive quiz session."""
    session.start()
    
    print()
    print(f"{Fore.CYAN}{'═' * 70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  FORMATIVE QUIZ — Week 7: Packet Interception and Filtering{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'═' * 70}{Style.RESET_ALL}")
    print(f"\n  Questions: {len(session.questions)}")
    print(f"  Total points: {sum(q.points for q in session.questions)}")
    print(f"  Passing: 70%")
    print(f"\n  Type your answer and press Enter. Type 'quit' to exit early.\n")
    
    for i, question in enumerate(session.questions, 1):
        print(f"\n{Fore.MAGENTA}Question {i} of {len(session.questions)}{Style.RESET_ALL}")
        question.display()
        
        print()
        try:
            answer = input(f"{Fore.WHITE}Your answer: {Style.RESET_ALL}").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nQuiz interrupted.")
            break
        
        if answer.lower() == "quit":
            print("\nQuiz ended early.")
            break
        
        session.answers[question.id] = answer
        
        # Immediate feedback
        if session._check_answer(question, answer):
            print(f"{Fore.GREEN}✓ Correct!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ Incorrect.{Style.RESET_ALL}")
            print(f"  Correct answer: {Fore.GREEN}{question.correct_answer}{Style.RESET_ALL}")
    
    session.finish()
    display_results(session)


def display_results(session: QuizSession) -> None:
    """Display quiz results summary."""
    earned, possible = session.score
    percentage = round(earned / possible * 100, 1) if possible > 0 else 0
    
    print()
    print(f"{Fore.CYAN}{'═' * 70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  QUIZ RESULTS{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'═' * 70}{Style.RESET_ALL}")
    
    # Score bar
    bar_width = 40
    filled = int(bar_width * percentage / 100)
    bar = "█" * filled + "░" * (bar_width - filled)
    
    colour = Fore.GREEN if percentage >= 70 else Fore.YELLOW if percentage >= 50 else Fore.RED
    print(f"\n  Score: {colour}{earned}/{possible} ({percentage}%){Style.RESET_ALL}")
    print(f"  [{bar}]")
    
    # Pass/Fail
    if percentage >= 70:
        print(f"\n  {Fore.GREEN}✓ PASSED{Style.RESET_ALL}")
    else:
        print(f"\n  {Fore.RED}✗ NOT PASSED (70% required){Style.RESET_ALL}")
    
    # Time
    if session.duration_seconds > 0:
        minutes = int(session.duration_seconds // 60)
        seconds = int(session.duration_seconds % 60)
        print(f"\n  Time: {minutes}m {seconds}s")
    
    # LO Breakdown
    print(f"\n  {Fore.CYAN}Learning Objective Breakdown:{Style.RESET_ALL}")
    breakdown = session._get_lo_breakdown()
    for lo, scores in sorted(breakdown.items()):
        lo_pct = round(scores["earned"] / scores["possible"] * 100) if scores["possible"] > 0 else 0
        lo_colour = Fore.GREEN if lo_pct >= 70 else Fore.RED
        print(f"    {lo}: {lo_colour}{scores['earned']}/{scores['possible']} ({lo_pct}%){Style.RESET_ALL}")
    
    print()
    print(f"{Fore.CYAN}{'═' * 70}{Style.RESET_ALL}")


def run_review_mode(questions: list[Question]) -> None:
    """Display all questions with answers."""
    print()
    print(f"{Fore.CYAN}{'═' * 70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  QUIZ REVIEW MODE — All answers shown{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'═' * 70}{Style.RESET_ALL}")
    
    for i, question in enumerate(questions, 1):
        print(f"\n{Fore.MAGENTA}Question {i}{Style.RESET_ALL}")
        question.display(show_answer=True)
        
        if question.verify_command:
            print(f"\n{Fore.YELLOW}Verify: {question.verify_command}{Style.RESET_ALL}")
        
        print()
        input(f"{Fore.WHITE}Press Enter for next question...{Style.RESET_ALL}")


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def build_parser() -> argparse.ArgumentParser:
    """Build command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Week 7 Formative Quiz Runner",
        epilog="Run without arguments for full interactive quiz."
    )
    
    parser.add_argument(
        "--quiz", "-q",
        type=Path,
        default=Path(__file__).parent / "quiz.yaml",
        help="Path to quiz YAML file"
    )
    
    parser.add_argument(
        "--random", "-r",
        action="store_true",
        help="Randomise question order"
    )
    
    parser.add_argument(
        "--limit", "-n",
        type=int,
        help="Limit number of questions"
    )
    
    parser.add_argument(
        "--lo",
        type=str,
        help="Filter by Learning Objective (e.g., LO1)"
    )
    
    parser.add_argument(
        "--difficulty",
        choices=["basic", "intermediate", "advanced"],
        help="Filter by difficulty"
    )
    
    parser.add_argument(
        "--review",
        action="store_true",
        help="Review mode (show all answers)"
    )
    
    parser.add_argument(
        "--export-json",
        type=Path,
        help="Export results to JSON file"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all questions without running quiz"
    )
    
    return parser


def main() -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args()
    
    try:
        metadata, questions = load_quiz(args.quiz)
    except Exception as e:
        print(f"{Fore.RED}Error loading quiz: {e}{Style.RESET_ALL}")
        return 2
    
    # Apply filters
    if args.lo:
        questions = [q for q in questions if q.lo_ref == args.lo]
    
    if args.difficulty:
        questions = [q for q in questions if q.difficulty == args.difficulty]
    
    if not questions:
        print(f"{Fore.RED}No questions match the specified filters.{Style.RESET_ALL}")
        return 1
    
    # Apply randomisation
    if args.random:
        random.shuffle(questions)
    
    # Apply limit
    if args.limit and args.limit < len(questions):
        questions = questions[:args.limit]
    
    # List mode
    if args.list:
        print(f"\n{Fore.CYAN}Quiz Questions ({len(questions)} total):{Style.RESET_ALL}\n")
        for q in questions:
            print(f"  [{q.id}] {q.lo_ref} | {q.bloom_level} | {q.points}pts")
            print(f"        {q.stem[:60]}...")
            print()
        return 0
    
    # Review mode
    if args.review:
        run_review_mode(questions)
        return 0
    
    # Interactive quiz
    session = QuizSession(questions=questions)
    run_interactive_quiz(session)
    
    # Export results if requested
    if args.export_json:
        results = session.to_dict()
        with open(args.export_json, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nResults exported to: {args.export_json}")
    
    # Return exit code based on pass/fail
    earned, possible = session.score
    percentage = earned / possible * 100 if possible > 0 else 0
    return 0 if percentage >= 70 else 1


if __name__ == "__main__":
    sys.exit(main())
