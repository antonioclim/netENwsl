#!/usr/bin/env python3
"""
Formative Quiz Runner — Week 9: Session and Presentation Layers
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

This script supports:
- Interactive runs in the terminal
- Basic filtering (Learning Objective and difficulty)
- A validation mode for CI and local sanity checks
- Export to a simple LMS-friendly JSON structure

Usage:

    # Run full quiz interactively
    python formative/run_quiz.py

    # Run with randomised question order
    python formative/run_quiz.py --random

    # Limit to N questions
    python formative/run_quiz.py --limit 5

    # Filter by Learning Objective
    python formative/run_quiz.py --lo LO2

    # Validate quiz file (for CI)
    python formative/run_quiz.py --validate

    # Export quiz to JSON
    python formative/run_quiz.py --export json
"""

from __future__ import annotations

import argparse
import json
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
EXPORT_JSON_DEFAULT = Path(__file__).parent / "quiz_lms.json"
VERSION = "1.1.0"


# ═══════════════════════════════════════════════════════════════════════════════
# YAML LOADER
# ═══════════════════════════════════════════════════════════════════════════════

def load_yaml(path: Path) -> dict[str, Any]:
    """Load YAML file with a clear error if PyYAML is missing."""
    try:
        import yaml  # type: ignore
    except ImportError as e:
        raise SystemExit(
            "PyYAML is required for the quiz.\n"
            "Install with: pip install pyyaml\n"
            "or run: pip install -r setup/requirements.txt"
        ) from e

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError("quiz.yaml must contain a top level mapping")
    return data


# ═══════════════════════════════════════════════════════════════════════════════
# DATA MODEL
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

    # Auto-graded questions use `correct`.
    # open_response questions may omit it.
    correct: str | list[str] = ""
    explanation: str = ""

    options: dict[str, str] = field(default_factory=dict)
    hint: str = ""
    misconception_ref: str = ""
    time_seconds: int = 60
    points: int = 1

    # Optional fields for open_response questions
    rubric: list[str] = field(default_factory=list)
    sample_answer: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Question":
        """Create a Question from a YAML dictionary."""
        return cls(
            id=str(data.get("id", "unknown")).strip(),
            lo_ref=str(data.get("lo_ref", "")).strip(),
            bloom_level=str(data.get("bloom_level", "")).strip(),
            difficulty=str(data.get("difficulty", "intermediate")).strip(),
            question_type=str(data.get("type", "multiple_choice")).strip(),
            stem=str(data.get("stem", "")).strip(),
            options=data.get("options", {}) or {},
            correct=data.get("correct", "") or "",
            explanation=str(data.get("explanation", "")).strip(),
            hint=str(data.get("hint", "")).strip(),
            misconception_ref=str(data.get("misconception_ref", "")).strip(),
            time_seconds=int(data.get("time_seconds", 60) or 60),
            points=int(data.get("points", 1) or 1),
            rubric=list(data.get("rubric", []) or []),
            sample_answer=str(data.get("sample_answer", "")).strip(),
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
        if self.total_questions <= 0:
            return 0.0
        return (self.correct_answers / self.total_questions) * 100

    @property
    def passed(self) -> bool:
        return self.score_percent >= 70.0


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ ENGINE
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
        self.metadata = self.quiz_data.get("metadata", {}) or {}
        raw_questions = self.quiz_data.get("questions", []) or []
        self.questions = [Question.from_dict(q) for q in raw_questions]

    def validate(self) -> tuple[bool, list[str]]:
        """Validate quiz structure. Returns (ok, messages)."""
        msgs: list[str] = []
        ok = True

        if not isinstance(self.quiz_data, dict):
            return False, ["Top level YAML value must be a mapping"]

        if "metadata" not in self.quiz_data:
            ok = False
            msgs.append("Missing key: metadata")

        if "questions" not in self.quiz_data:
            ok = False
            msgs.append("Missing key: questions")
            return ok, msgs

        if not isinstance(self.quiz_data["questions"], list):
            ok = False
            msgs.append("questions must be a list")
            return ok, msgs

        # Question-level checks
        seen_ids: set[str] = set()
        supported_types = {"multiple_choice", "fill_blank", "code_trace", "open_response"}

        for idx, q in enumerate(self.quiz_data["questions"], 1):
            if not isinstance(q, dict):
                ok = False
                msgs.append(f"Question {idx}: must be a mapping")
                continue

            qid = str(q.get("id", "")).strip()
            if not qid:
                ok = False
                msgs.append(f"Question {idx}: missing id")
            elif qid in seen_ids:
                ok = False
                msgs.append(f"Duplicate question id: {qid}")
            else:
                seen_ids.add(qid)

            qtype = str(q.get("type", "multiple_choice")).strip()
            if qtype not in supported_types:
                ok = False
                msgs.append(f"Question {qid or idx}: unsupported type '{qtype}'")

            stem = str(q.get("stem", "")).strip()
            if not stem:
                ok = False
                msgs.append(f"Question {qid or idx}: missing stem")

            if qtype in {"multiple_choice", "code_trace"}:
                options = q.get("options", {})
                if not isinstance(options, dict) or len(options) < 2:
                    ok = False
                    msgs.append(f"Question {qid or idx}: invalid options mapping")
                if "correct" not in q:
                    ok = False
                    msgs.append(f"Question {qid or idx}: missing correct answer")

            if qtype == "fill_blank" and "correct" not in q:
                ok = False
                msgs.append(f"Question {qid or idx}: missing correct answer")

        # Metadata consistency check
        md = self.quiz_data.get("metadata", {}) or {}
        declared_total = md.get("total_questions")
        if isinstance(declared_total, int) and declared_total != len(self.quiz_data["questions"]):
            msgs.append(
                f"metadata.total_questions is {declared_total} but questions contains {len(self.quiz_data['questions'])}"
            )

        if ok:
            msgs.append(f"Quiz OK: {len(self.quiz_data['questions'])} questions")
        return ok, msgs

    def export_json(self, output_path: Path = EXPORT_JSON_DEFAULT) -> Path:
        """Export quiz to a simple JSON file (LMS-friendly structure)."""
        payload = {
            "metadata": self.quiz_data.get("metadata", {}),
            "questions": self.quiz_data.get("questions", []),
            "note": "Generated by formative/run_quiz.py --export json",
        }
        output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return output_path

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
        """Run quiz interactively in the terminal."""
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

            if question.question_type == "open_response":
                # open_response is self-marked for formative use
                if is_correct:
                    result.correct_answers += 1
                    print("✅ Marked as satisfactory")
                else:
                    result.incorrect_answers += 1
                    print("❌ Marked as needing improvement")
            else:
                if is_correct:
                    result.correct_answers += 1
                    print("✅ Correct!")
                else:
                    result.incorrect_answers += 1
                    print(f"❌ Incorrect. The correct answer is: {question.correct}")

            # Explanation / feedback
            if question.explanation:
                print(f"\n📖 Explanation: {question.explanation}")
            elif question.sample_answer:
                print("\n📖 Sample answer:")
                print(question.sample_answer)

            # Track LO scores
            lo = question.lo_ref
            if lo not in result.lo_scores:
                result.lo_scores[lo] = (0, 0)
            correct, total = result.lo_scores[lo]
            result.lo_scores[lo] = (correct + (1 if is_correct else 0), total + 1)

            if i < len(questions):
                input("\nPress Enter for next question...")

        result.time_elapsed_seconds = time.time() - start_time
        self._print_results(result)
        return result

    def _print_header(self) -> None:
        title = self.metadata.get("title", "Quiz")
        week = self.metadata.get("week", "")
        print("\n" + "═" * 70)
        print(f"  📝 {title}")
        if week:
            print(f"  Week {week}")
        print("═" * 70)

    def _ask_question(self, question: Question) -> bool:
        """Ask a single question and return whether it is correct."""
        print(f"\n{question.stem}")

        if question.question_type in {"multiple_choice", "code_trace"}:
            for key, value in sorted(question.options.items()):
                print(f"   {key}) {value}")

            answer = input("\nYour answer (a/b/c/d): ").strip().lower()
            return answer == question.correct

        if question.question_type == "fill_blank":
            if question.hint:
                print(f"Hint: {question.hint}")

            answer = input("\nYour answer: ").strip()
            if isinstance(question.correct, list):
                return answer in question.correct
            return answer == question.correct

        if question.question_type == "open_response":
            if question.rubric:
                print("\nMarking rubric:")
                for item in question.rubric:
                    print(f"  - {item}")

            _ = input("\nWrite your response then press Enter: ").strip()

            if question.sample_answer:
                print("\nSample answer for comparison:")
                print(question.sample_answer)

            mark = input("\nSelf-mark (y/n): ").strip().lower()
            return mark == "y"

        return False

    def _print_results(self, result: QuizResult) -> None:
        print("\n" + "═" * 70)
        print("  📊 QUIZ RESULTS")
        print("═" * 70)

        print(
            f"\n  Score: {result.correct_answers}/{result.total_questions} "
            f"({result.score_percent:.1f}%)"
        )
        print(f"  Time: {result.time_elapsed_seconds:.1f} seconds")
        print(f"  Status: {'✅ PASSED' if result.passed else '❌ NEEDS REVIEW'}")

        print("\n  Learning Objective coverage:")
        for lo, (correct, total) in sorted(result.lo_scores.items()):
            pct = (correct / total * 100) if total > 0 else 0
            bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
            print(f"    {lo}: {bar} {correct}/{total} ({pct:.0f}%)")


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run formative quiz for Week 9 laboratory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                      Run full quiz
  %(prog)s --random --limit 5   Random 5 questions
  %(prog)s --lo LO2             Filter by Learning Objective
  %(prog)s --validate           Validate quiz.yaml structure
  %(prog)s --export json        Export quiz to JSON
        """,
    )

    parser.add_argument(
        "--quiz",
        "-q",
        type=Path,
        default=QUIZ_FILE,
        help="Path to quiz YAML file",
    )
    parser.add_argument(
        "--random",
        "-r",
        action="store_true",
        help="Randomise question order",
    )
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        help="Limit number of questions",
    )
    parser.add_argument(
        "--lo",
        type=str,
        help="Filter by Learning Objective (e.g. LO1, LO2)",
    )
    parser.add_argument(
        "--difficulty",
        "-d",
        choices=["basic", "intermediate", "advanced"],
        help="Filter by difficulty level",
    )
    parser.add_argument(
        "--stats",
        "-s",
        action="store_true",
        help="Show quiz statistics only",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate quiz structure and exit",
    )
    parser.add_argument(
        "--export",
        choices=["json"],
        help="Export quiz to a supported format",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=EXPORT_JSON_DEFAULT,
        help="Export output path (default: formative/quiz_lms.json)",
    )
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"%(prog)s {VERSION}",
    )

    args = parser.parse_args()

    engine = QuizEngine(args.quiz)

    try:
        engine.load()
    except Exception as e:
        print(f"Error loading quiz: {e}")
        return 1

    if args.validate:
        ok, messages = engine.validate()
        for m in messages:
            print(m)
        return 0 if ok else 1

    if args.export == "json":
        out_path = engine.export_json(args.output)
        print(f"Exported JSON to: {out_path}")
        return 0

    if args.stats:
        # A lightweight stats view based on loaded data
        total = len(engine.questions)
        by_lo: dict[str, int] = {}
        by_type: dict[str, int] = {}
        for q in engine.questions:
            by_lo[q.lo_ref] = by_lo.get(q.lo_ref, 0) + 1
            by_type[q.question_type] = by_type.get(q.question_type, 0) + 1

        print(f"Questions: {total}")
        print("By LO:")
        for k in sorted(by_lo):
            print(f"  {k}: {by_lo[k]}")
        print("By type:")
        for k in sorted(by_type):
            print(f"  {k}: {by_type[k]}")
        return 0

    questions = engine.filter_questions(
        lo=args.lo,
        difficulty=args.difficulty,
    )

    if not questions:
        print("No questions match the specified filters.")
        return 1

    try:
        result = engine.run_interactive(
            questions=questions,
            randomise=args.random,
            limit=args.limit,
        )
        return 0 if result.passed else 1
    except KeyboardInterrupt:
        print("\nQuiz interrupted by user.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
