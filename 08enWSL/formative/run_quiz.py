#!/usr/bin/env python3
"""
Formative Assessment Quiz Runner — Week 8: Transport Layer & HTTP
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

This quiz runner was designed through extensive brainstorming with Andrei T.
and incorporates pedagogical principles from the DPPD module at Universitatea
Politehnica București.

Usage:
    python formative/run_quiz.py                      # Run full quiz
    python formative/run_quiz.py --random             # Randomise question order
    python formative/run_quiz.py --lo LO3             # Filter by Learning Objective
    python formative/run_quiz.py --difficulty basic   # Filter by difficulty
    python formative/run_quiz.py --limit 5            # Limit to N questions
    python formative/run_quiz.py --review             # Review mode (show answers)
    python formative/run_quiz.py --export json        # Export results to JSON

Author: ing. dr. Antonio Clim
Contributors: Andrei T. (pedagogical review)
Course: Computer Networks - ASE, CSIE
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
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with:")
    print("  pip install pyyaml --break-system-packages")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# ANSI COLOURS (for terminal output)
# ═══════════════════════════════════════════════════════════════════════════════

class Colours:
    """ANSI colour codes for terminal output."""
    
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"
    
    @classmethod
    def disable(cls) -> None:
        """Disable colours (for non-terminal output)."""
        cls.GREEN = cls.RED = cls.YELLOW = cls.BLUE = ""
        cls.CYAN = cls.MAGENTA = cls.BOLD = cls.DIM = cls.RESET = ""


# ═══════════════════════════════════════════════════════════════════════════════
# DATA CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Question:
    """Represents a single quiz question."""
    
    id: str
    lo_ref: str
    bloom_level: str
    difficulty: str
    question_type: str
    stem: str
    correct: str | list[str]
    explanation: str
    points: int
    options: Optional[dict[str, str]] = None
    misconception_ref: Optional[str] = None
    
    def display(self, index: int, total: int) -> None:
        """Display the question to the user."""
        difficulty_colours = {
            "basic": Colours.GREEN,
            "intermediate": Colours.YELLOW,
            "advanced": Colours.RED,
        }
        diff_colour = difficulty_colours.get(self.difficulty, "")
        
        print(f"\n{'═' * 70}")
        print(f"{Colours.BOLD}Question {index}/{total}{Colours.RESET} "
              f"[{diff_colour}{self.difficulty.upper()}{Colours.RESET}] "
              f"[{Colours.CYAN}{self.lo_ref}{Colours.RESET}] "
              f"({self.points} pts)")
        print(f"{'═' * 70}")
        print()
        print(self.stem.strip())
        
        if self.options:
            print()
            for key, value in self.options.items():
                print(f"  {Colours.BOLD}{key}){Colours.RESET} {value}")
    
    def check_answer(self, user_answer: str) -> bool:
        """Check if the user's answer is correct."""
        user_answer = user_answer.strip().lower()
        
        if isinstance(self.correct, list):
            return any(user_answer == c.lower() for c in self.correct)
        return user_answer == self.correct.lower()
    
    def show_feedback(self, correct: bool) -> None:
        """Display feedback after answering."""
        if correct:
            print(f"\n{Colours.GREEN}✓ Correct!{Colours.RESET}")
        else:
            print(f"\n{Colours.RED}✗ Incorrect{Colours.RESET}")
            if isinstance(self.correct, list):
                print(f"  Accepted answers: {', '.join(self.correct)}")
            else:
                print(f"  Correct answer: {self.correct}")
        
        print(f"\n{Colours.DIM}Explanation:{Colours.RESET}")
        for line in self.explanation.strip().split('\n'):
            print(f"  {line}")


@dataclass
class QuizResult:
    """Stores the result of a quiz attempt."""
    
    timestamp: str
    total_questions: int
    correct_answers: int
    total_points: int
    earned_points: int
    percentage: float
    grade: str
    time_taken_seconds: float
    lo_breakdown: dict[str, dict[str, int]] = field(default_factory=dict)
    question_results: list[dict] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON export."""
        return {
            "timestamp": self.timestamp,
            "total_questions": self.total_questions,
            "correct_answers": self.correct_answers,
            "total_points": self.total_points,
            "earned_points": self.earned_points,
            "percentage": round(self.percentage, 1),
            "grade": self.grade,
            "time_taken_seconds": round(self.time_taken_seconds, 1),
            "lo_breakdown": self.lo_breakdown,
            "question_results": self.question_results,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ RUNNER CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class QuizRunner:
    """
    Interactive quiz runner for formative assessment.
    
    Designed with pedagogical principles from the DPPD module:
    - Immediate feedback after each question
    - Explanations that address misconceptions
    - Learning objective tracking for targeted review
    
    Example:
        >>> runner = QuizRunner("formative/quiz.yaml")
        >>> result = runner.run()
        >>> print(f"Score: {result.percentage}%")
    """
    
    def __init__(self, quiz_path: str | Path) -> None:
        """
        Initialise the quiz runner.
        
        Args:
            quiz_path: Path to the quiz YAML file
            
        Raises:
            FileNotFoundError: If quiz file doesn't exist
            yaml.YAMLError: If quiz file is malformed
        """
        self.quiz_path = Path(quiz_path)
        
        if not self.quiz_path.exists():
            raise FileNotFoundError(f"Quiz file not found: {self.quiz_path}")
        
        with open(self.quiz_path, encoding="utf-8") as f:
            self.quiz_data = yaml.safe_load(f)
        
        self.metadata = self.quiz_data.get("metadata", {})
        self.scoring = self.quiz_data.get("scoring", {})
        self.questions = self._parse_questions()
    
    def _parse_questions(self) -> list[Question]:
        """Parse raw question data into Question objects."""
        questions = []
        
        for q_data in self.quiz_data.get("questions", []):
            questions.append(Question(
                id=q_data["id"],
                lo_ref=q_data["lo_ref"],
                bloom_level=q_data["bloom_level"],
                difficulty=q_data["difficulty"],
                question_type=q_data["question_type"],
                stem=q_data["stem"],
                options=q_data.get("options"),
                correct=q_data["correct"],
                explanation=q_data["explanation"],
                points=q_data.get("points", 5),
                misconception_ref=q_data.get("misconception_ref"),
            ))
        
        return questions
    
    def filter_questions(
        self,
        lo: Optional[str] = None,
        difficulty: Optional[str] = None,
        bloom_level: Optional[str] = None,
    ) -> list[Question]:
        """
        Filter questions by Learning Objective, difficulty or Bloom level.
        
        Args:
            lo: Learning Objective (e.g., "LO3")
            difficulty: Difficulty level (basic/intermediate/advanced)
            bloom_level: Bloom's taxonomy level (remember/understand/apply/analyse/evaluate)
            
        Returns:
            Filtered list of questions
        """
        filtered = self.questions.copy()
        
        if lo:
            filtered = [q for q in filtered if q.lo_ref.upper() == lo.upper()]
        
        if difficulty:
            filtered = [q for q in filtered if q.difficulty.lower() == difficulty.lower()]
        
        if bloom_level:
            filtered = [q for q in filtered if q.bloom_level.lower() == bloom_level.lower()]
        
        return filtered
    
    def run(
        self,
        questions: Optional[list[Question]] = None,
        randomise: bool = False,
        limit: Optional[int] = None,
        review_mode: bool = False,
    ) -> QuizResult:
        """
        Run the interactive quiz.
        
        Args:
            questions: Specific questions to use (default: all)
            randomise: Shuffle question order
            limit: Maximum number of questions
            review_mode: Show correct answers without prompting
            
        Returns:
            QuizResult with scores and breakdown
        """
        questions = questions or self.questions.copy()
        
        if randomise:
            random.shuffle(questions)
        
        if limit and limit < len(questions):
            questions = questions[:limit]
        
        self._print_header(len(questions))
        
        start_time = time.time()
        correct_count = 0
        earned_points = 0
        total_points = sum(q.points for q in questions)
        lo_stats: dict[str, dict[str, int]] = {}
        question_results: list[dict] = []
        
        for i, question in enumerate(questions, 1):
            # Initialise LO tracking
            if question.lo_ref not in lo_stats:
                lo_stats[question.lo_ref] = {"correct": 0, "total": 0, "points": 0}
            lo_stats[question.lo_ref]["total"] += 1
            
            # Display question
            question.display(i, len(questions))
            
            if review_mode:
                # Review mode: just show the answer
                print(f"\n{Colours.CYAN}Answer: {question.correct}{Colours.RESET}")
                question.show_feedback(True)
                input(f"\n{Colours.DIM}Press Enter to continue...{Colours.RESET}")
                correct_count += 1
                earned_points += question.points
                lo_stats[question.lo_ref]["correct"] += 1
                lo_stats[question.lo_ref]["points"] += question.points
                question_results.append({
                    "id": question.id,
                    "correct": True,
                    "points": question.points,
                })
            else:
                # Interactive mode
                print()
                user_answer = input(f"{Colours.BOLD}Your answer: {Colours.RESET}").strip()
                
                is_correct = question.check_answer(user_answer)
                question.show_feedback(is_correct)
                
                if is_correct:
                    correct_count += 1
                    earned_points += question.points
                    lo_stats[question.lo_ref]["correct"] += 1
                    lo_stats[question.lo_ref]["points"] += question.points
                
                question_results.append({
                    "id": question.id,
                    "user_answer": user_answer,
                    "correct": is_correct,
                    "points": question.points if is_correct else 0,
                })
                
                input(f"\n{Colours.DIM}Press Enter to continue...{Colours.RESET}")
        
        elapsed_time = time.time() - start_time
        percentage = (earned_points / total_points * 100) if total_points > 0 else 0
        grade = self._determine_grade(earned_points)
        
        result = QuizResult(
            timestamp=datetime.now().isoformat(),
            total_questions=len(questions),
            correct_answers=correct_count,
            total_points=total_points,
            earned_points=earned_points,
            percentage=percentage,
            grade=grade,
            time_taken_seconds=elapsed_time,
            lo_breakdown=lo_stats,
            question_results=question_results,
        )
        
        self._print_summary(result)
        
        return result
    
    def _determine_grade(self, points: int) -> str:
        """Determine grade based on points earned."""
        boundaries = self.scoring.get("grade_boundaries", {})
        
        if points >= boundaries.get("excellent", 100):
            return "Excellent"
        elif points >= boundaries.get("good", 85):
            return "Good"
        elif points >= boundaries.get("satisfactory", 70):
            return "Satisfactory"
        else:
            return "Needs Improvement"
    
    def _print_header(self, question_count: int) -> None:
        """Print quiz header."""
        print()
        print(f"{Colours.BOLD}{'═' * 70}{Colours.RESET}")
        print(f"{Colours.BOLD}  FORMATIVE QUIZ — Week {self.metadata.get('week', '?')}{Colours.RESET}")
        print(f"  {self.metadata.get('topic', 'Unknown Topic')}")
        print(f"{Colours.BOLD}{'═' * 70}{Colours.RESET}")
        print()
        print(f"  Questions: {question_count}")
        print(f"  Estimated time: {self.metadata.get('estimated_time_minutes', '?')} minutes")
        print(f"  Passing score: {self.metadata.get('passing_score', 70)}%")
        print()
        print(f"{Colours.DIM}  Tip: For multiple choice, enter the letter (a, b, c or d).{Colours.RESET}")
        print(f"{Colours.DIM}  Tip: For fill-in-the-blank, type your answer exactly.{Colours.RESET}")
        print()
        input(f"{Colours.BOLD}Press Enter to begin...{Colours.RESET}")
    
    def _print_summary(self, result: QuizResult) -> None:
        """Print quiz summary and feedback."""
        print()
        print(f"\n{Colours.BOLD}{'═' * 70}{Colours.RESET}")
        print(f"{Colours.BOLD}  QUIZ COMPLETE{Colours.RESET}")
        print(f"{'═' * 70}")
        print()
        
        # Score display with colour
        if result.percentage >= 70:
            score_colour = Colours.GREEN
        elif result.percentage >= 50:
            score_colour = Colours.YELLOW
        else:
            score_colour = Colours.RED
        
        print(f"  Score: {score_colour}{result.earned_points}/{result.total_points} "
              f"({result.percentage:.1f}%){Colours.RESET}")
        print(f"  Grade: {Colours.BOLD}{result.grade}{Colours.RESET}")
        print(f"  Time: {result.time_taken_seconds:.0f} seconds")
        print()
        
        # LO breakdown
        print(f"  {Colours.BOLD}Learning Objective Breakdown:{Colours.RESET}")
        for lo, stats in sorted(result.lo_breakdown.items()):
            lo_pct = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
            bar = "█" * int(lo_pct / 10) + "░" * (10 - int(lo_pct / 10))
            colour = Colours.GREEN if lo_pct >= 70 else (Colours.YELLOW if lo_pct >= 50 else Colours.RED)
            print(f"    {lo}: {colour}{bar}{Colours.RESET} {stats['correct']}/{stats['total']} "
                  f"({lo_pct:.0f}%)")
        
        print()
        
        # Feedback message
        feedback_messages = self.scoring.get("feedback_messages", {})
        feedback_key = result.grade.lower().replace(" ", "_")
        feedback = feedback_messages.get(feedback_key, "")
        
        if feedback:
            print(f"  {Colours.CYAN}Feedback:{Colours.RESET}")
            for line in feedback.strip().split('\n'):
                print(f"    {line.strip()}")
        
        print()
        print(f"{'═' * 70}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """
    Main entry point for the quiz runner.
    
    Returns:
        Exit code (0 for success)
    """
    parser = argparse.ArgumentParser(
        description="Formative Assessment Quiz Runner — Week 8",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python formative/run_quiz.py                      # Run full quiz
  python formative/run_quiz.py --random --limit 5   # Random 5 questions
  python formative/run_quiz.py --lo LO3             # Only LO3 questions
  python formative/run_quiz.py --difficulty basic   # Only basic questions
  python formative/run_quiz.py --review             # Review mode (shows answers)
  python formative/run_quiz.py --export results.json  # Save results to file

Developed by ing. dr. Antonio Clim with contributions from Andrei T.
Pedagogical design informed by DPPD module, Universitatea Politehnica București.
        """
    )
    
    parser.add_argument(
        "--quiz",
        default="formative/quiz.yaml",
        help="Path to quiz YAML file (default: formative/quiz.yaml)"
    )
    parser.add_argument(
        "--random",
        action="store_true",
        help="Randomise question order"
    )
    parser.add_argument(
        "--limit",
        type=int,
        metavar="N",
        help="Limit to N questions"
    )
    parser.add_argument(
        "--lo",
        metavar="LOx",
        help="Filter by Learning Objective (e.g., LO3)"
    )
    parser.add_argument(
        "--difficulty",
        choices=["basic", "intermediate", "advanced"],
        help="Filter by difficulty level"
    )
    parser.add_argument(
        "--bloom",
        choices=["remember", "understand", "apply", "analyse", "evaluate"],
        help="Filter by Bloom's taxonomy level"
    )
    parser.add_argument(
        "--review",
        action="store_true",
        help="Review mode — show answers without prompting"
    )
    parser.add_argument(
        "--export",
        metavar="FILE",
        help="Export results to JSON file"
    )
    parser.add_argument(
        "--no-colour",
        action="store_true",
        help="Disable coloured output"
    )
    parser.add_argument(
        "--list-questions",
        action="store_true",
        help="List all questions without running quiz"
    )
    
    args = parser.parse_args()
    
    if args.no_colour:
        Colours.disable()
    
    # Find quiz file relative to script location or current directory
    quiz_path = Path(args.quiz)
    if not quiz_path.exists():
        # Try relative to script location
        script_dir = Path(__file__).parent.parent
        quiz_path = script_dir / args.quiz
    
    if not quiz_path.exists():
        print(f"{Colours.RED}Error: Quiz file not found: {args.quiz}{Colours.RESET}")
        print("Make sure you're running from the lab kit directory.")
        return 1
    
    try:
        runner = QuizRunner(quiz_path)
    except Exception as e:
        print(f"{Colours.RED}Error loading quiz: {e}{Colours.RESET}")
        return 1
    
    # Filter questions
    questions = runner.filter_questions(
        lo=args.lo,
        difficulty=args.difficulty,
        bloom_level=args.bloom,
    )
    
    if not questions:
        print(f"{Colours.YELLOW}No questions match your filters.{Colours.RESET}")
        return 1
    
    # List mode
    if args.list_questions:
        print(f"\n{Colours.BOLD}Available Questions ({len(questions)}):{Colours.RESET}\n")
        for q in questions:
            print(f"  {q.id}: [{q.lo_ref}] [{q.difficulty}] [{q.bloom_level}] ({q.points} pts)")
        return 0
    
    # Run quiz
    try:
        result = runner.run(
            questions=questions,
            randomise=args.random,
            limit=args.limit,
            review_mode=args.review,
        )
    except KeyboardInterrupt:
        print(f"\n\n{Colours.YELLOW}Quiz interrupted. Your progress was not saved.{Colours.RESET}")
        return 1
    
    # Export results
    if args.export:
        export_path = Path(args.export)
        with open(export_path, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2)
        print(f"\n{Colours.GREEN}Results exported to: {export_path}{Colours.RESET}")
    
    # Return code based on pass/fail
    return 0 if result.percentage >= runner.metadata.get("passing_score", 70) else 1


if __name__ == "__main__":
    sys.exit(main())
