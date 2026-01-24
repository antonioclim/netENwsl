#!/usr/bin/env python3
"""
Formative Quiz Runner — Week 9: Session and Presentation Layers
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

═══════════════════════════════════════════════════════════════════════════════
USAGE:
═══════════════════════════════════════════════════════════════════════════════

    # Run full quiz interactively
    python formative/run_quiz.py
    
    # Run with randomised question order
    python formative/run_quiz.py --random
    
    # Limit to N questions
    python formative/run_quiz.py --limit 5
    
    # Filter by Learning Objective
    python formative/run_quiz.py --lo LO2
    
    # Filter by difficulty
    python formative/run_quiz.py --difficulty basic
    
    # Non-interactive mode (for CI)
    python formative/run_quiz.py --non-interactive --answers b,b,b,a,b,...
    
    # Show quiz statistics without running
    python formative/run_quiz.py --stats

═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import argparse
import random
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

QUIZ_FILE = Path(__file__).parent / "quiz.yaml"
VERSION = "1.0.0"


# ═══════════════════════════════════════════════════════════════════════════════
# YAML_LOADER (with fallback)
# ═══════════════════════════════════════════════════════════════════════════════

def load_yaml(path: Path) -> dict[str, Any]:
    """Load YAML file with graceful fallback if PyYAML not installed."""
    try:
        import yaml
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except ImportError:
        print("⚠️  PyYAML not installed. Install with: pip install pyyaml")
        print("    Attempting basic YAML parsing (limited support)...")
        return _basic_yaml_parse(path)


def _basic_yaml_parse(path: Path) -> dict[str, Any]:
    """Very basic YAML parser for simple structures (fallback only)."""
    # This is a minimal fallback - real implementation should use PyYAML
    raise SystemExit(
        "❌ PyYAML required for quiz functionality.\n"
        "   Install with: pip install pyyaml\n"
        "   Or run: pip install -r setup/requirements.txt"
    )


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_STRUCTURES
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
    options: dict[str, str] = field(default_factory=dict)
    hint: str = ""
    misconception_ref: str = ""
    time_seconds: int = 60
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Question":
        """Create Question from YAML dictionary."""
        return cls(
            id=data.get("id", "unknown"),
            lo_ref=data.get("lo_ref", ""),
            bloom_level=data.get("bloom_level", ""),
            difficulty=data.get("difficulty", "intermediate"),
            question_type=data.get("type", "multiple_choice"),
            stem=data.get("stem", "").strip(),
            options=data.get("options", {}),
            correct=data.get("correct", ""),
            explanation=data.get("explanation", "").strip(),
            hint=data.get("hint", ""),
            misconception_ref=data.get("misconception_ref", ""),
            time_seconds=data.get("time_seconds", 60),
        )


@dataclass
class QuizResult:
    """Stores results of a quiz attempt."""
    total_questions: int = 0
    correct_answers: int = 0
    incorrect_answers: int = 0
    skipped: int = 0
    time_elapsed_seconds: float = 0.0
    lo_scores: dict[str, tuple[int, int]] = field(default_factory=dict)
    
    @property
    def score_percent(self) -> float:
        """Calculate percentage score."""
        if self.total_questions == 0:
            return 0.0
        return (self.correct_answers / self.total_questions) * 100
    
    @property
    def passed(self) -> bool:
        """Check if quiz was passed (≥70%)."""
        return self.score_percent >= 70.0


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class QuizEngine:
    """Main quiz execution engine."""
    
    def __init__(self, quiz_path: Path = QUIZ_FILE):
        self.quiz_path = quiz_path
        self.quiz_data: dict[str, Any] = {}
        self.questions: list[Question] = []
        self.metadata: dict[str, Any] = {}
        
    def load(self) -> None:
        """Load quiz from YAML file."""
        if not self.quiz_path.exists():
            raise FileNotFoundError(f"Quiz file not found: {self.quiz_path}")
        
        self.quiz_data = load_yaml(self.quiz_path)
        self.metadata = self.quiz_data.get("metadata", {})
        
        raw_questions = self.quiz_data.get("questions", [])
        self.questions = [Question.from_dict(q) for q in raw_questions]
        
    def filter_questions(
        self,
        lo: Optional[str] = None,
        difficulty: Optional[str] = None,
        bloom_level: Optional[str] = None,
    ) -> list[Question]:
        """Filter questions by criteria."""
        filtered = self.questions
        
        if lo:
            filtered = [q for q in filtered if q.lo_ref == lo]
        if difficulty:
            filtered = [q for q in filtered if q.difficulty == difficulty]
        if bloom_level:
            filtered = [q for q in filtered if q.bloom_level == bloom_level]
            
        return filtered
    
    def run_interactive(
        self,
        questions: list[Question],
        randomise: bool = False,
        limit: Optional[int] = None,
    ) -> QuizResult:
        """Run quiz interactively in terminal."""
        if randomise:
            questions = questions.copy()
            random.shuffle(questions)
        
        if limit and limit < len(questions):
            questions = questions[:limit]
        
        result = QuizResult(total_questions=len(questions))
        start_time = time.time()
        
        self._print_header()
        
        for i, question in enumerate(questions, 1):
            print(f"\n{'─' * 70}")
            print(f"Question {i}/{len(questions)} [{question.lo_ref}] [{question.difficulty}]")
            print(f"{'─' * 70}")
            
            is_correct = self._ask_question(question)
            
            if is_correct:
                result.correct_answers += 1
                print("✅ Correct!")
            else:
                result.incorrect_answers += 1
                print(f"❌ Incorrect. The correct answer is: {question.correct}")
            
            # Show explanation
            print(f"\n📖 Explanation: {question.explanation}")
            
            # Track LO scores
            lo = question.lo_ref
            if lo not in result.lo_scores:
                result.lo_scores[lo] = (0, 0)
            correct, total = result.lo_scores[lo]
            result.lo_scores[lo] = (correct + (1 if is_correct else 0), total + 1)
            
            # Pause between questions
            if i < len(questions):
                input("\nPress Enter for next question...")
        
        result.time_elapsed_seconds = time.time() - start_time
        self._print_results(result)
        
        return result
    
    def _print_header(self) -> None:
        """Print quiz header."""
        title = self.metadata.get("title", "Quiz")
        print("\n" + "═" * 70)
        print(f"  📝 {title}")
        print(f"  Week {self.metadata.get('week', '?')} | "
              f"Questions: {len(self.questions)} | "
              f"Pass: {self.metadata.get('passing_score_percent', 70)}%")
        print("═" * 70)
    
    def _ask_question(self, question: Question) -> bool:
        """Ask a single question and return if answer is correct."""
        print(f"\n{question.stem}")
        
        if question.question_type == "multiple_choice":
            for key, value in sorted(question.options.items()):
                print(f"   {key}) {value}")
            
            answer = input("\nYour answer (a/b/c/d): ").strip().lower()
            return answer == question.correct
            
        elif question.question_type == "fill_blank":
            if question.hint:
                print(f"💡 Hint: {question.hint}")
            
            answer = input("\nYour answer: ").strip()
            
            if isinstance(question.correct, list):
                return answer in question.correct
            return answer == question.correct
            
        elif question.question_type == "code_trace":
            for key, value in sorted(question.options.items()):
                print(f"   {key}) {value}")
            
            answer = input("\nYour answer (a/b/c/d): ").strip().lower()
            return answer == question.correct
        
        return False
    
    def _print_results(self, result: QuizResult) -> None:
        """Print quiz results summary."""
        print("\n" + "═" * 70)
        print("  📊 QUIZ RESULTS")
        print("═" * 70)
        
        print(f"\n  Score: {result.correct_answers}/{result.total_questions} "
              f"({result.score_percent:.1f}%)")
        print(f"  Time: {result.time_elapsed_seconds:.1f} seconds")
        print(f"  Status: {'✅ PASSED' if result.passed else '❌ NEEDS REVIEW'}")
        
        # LO breakdown
        print("\n  Learning Objective Coverage:")
        for lo, (correct, total) in sorted(result.lo_scores.items()):
            pct = (correct / total * 100) if total > 0 else 0
            bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
            print(f"    {lo}: {bar} {correct}/{total} ({pct:.0f}%)")
        
        # Feedback message
        feedback = self.quiz_data.get("feedback", {})
        messages = feedback.get("messages", {})
        
        if result.score_percent >= 90:
            msg = messages.get("excellent", "Excellent work!")
        elif result.score_percent >= 70:
            msg = messages.get("good", "Good job!")
        elif result.score_percent >= 50:
            msg = messages.get("needs_improvement", "Keep practicing!")
        else:
            msg = messages.get("below_threshold", "Review the materials.")
        
        print(f"\n  {msg}")
        print("\n" + "═" * 70)
    
    def print_stats(self) -> None:
        """Print quiz statistics without running."""
        print("\n" + "═" * 70)
        print("  📊 QUIZ STATISTICS")
        print("═" * 70)
        
        print(f"\n  Title: {self.metadata.get('title', 'Unknown')}")
        print(f"  Week: {self.metadata.get('week', '?')}")
        print(f"  Total Questions: {len(self.questions)}")
        print(f"  Estimated Time: {self.metadata.get('estimated_time_minutes', '?')} minutes")
        print(f"  Passing Score: {self.metadata.get('passing_score_percent', 70)}%")
        
        # Count by difficulty
        difficulties = {}
        for q in self.questions:
            difficulties[q.difficulty] = difficulties.get(q.difficulty, 0) + 1
        
        print("\n  Questions by Difficulty:")
        for diff, count in sorted(difficulties.items()):
            print(f"    {diff}: {count}")
        
        # Count by LO
        los = {}
        for q in self.questions:
            los[q.lo_ref] = los.get(q.lo_ref, 0) + 1
        
        print("\n  Questions by Learning Objective:")
        for lo, count in sorted(los.items()):
            print(f"    {lo}: {count}")
        
        # Count by Bloom level
        blooms = {}
        for q in self.questions:
            blooms[q.bloom_level] = blooms.get(q.bloom_level, 0) + 1
        
        print("\n  Questions by Bloom Level:")
        for bloom, count in sorted(blooms.items()):
            print(f"    {bloom}: {count}")
        
        print("\n" + "═" * 70)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run formative quiz for Week 9 laboratory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                      Run full quiz
  %(prog)s --random --limit 5   Random 5 questions
  %(prog)s --lo LO2             Filter by Learning Objective
  %(prog)s --stats              Show statistics only
        """
    )
    
    parser.add_argument(
        "--quiz", "-q",
        type=Path,
        default=QUIZ_FILE,
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
        type=str,
        help="Filter by Learning Objective (e.g., LO1, LO2)"
    )
    parser.add_argument(
        "--difficulty", "-d",
        choices=["basic", "intermediate", "advanced"],
        help="Filter by difficulty level"
    )
    parser.add_argument(
        "--stats", "-s",
        action="store_true",
        help="Show quiz statistics without running"
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"%(prog)s {VERSION}"
    )
    
    args = parser.parse_args()
    
    # Initialise engine
    engine = QuizEngine(args.quiz)
    
    try:
        engine.load()
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Error loading quiz: {e}")
        return 1
    
    # Stats mode
    if args.stats:
        engine.print_stats()
        return 0
    
    # Filter questions
    questions = engine.filter_questions(
        lo=args.lo,
        difficulty=args.difficulty,
    )
    
    if not questions:
        print("❌ No questions match the specified filters.")
        return 1
    
    # Run quiz
    try:
        result = engine.run_interactive(
            questions=questions,
            randomise=args.random,
            limit=args.limit,
        )
        return 0 if result.passed else 1
    except KeyboardInterrupt:
        print("\n\n⚠️  Quiz interrupted by user.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
