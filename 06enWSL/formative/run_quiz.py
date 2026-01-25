#!/usr/bin/env python3
"""
Formative Quiz Runner — Week 6: NAT/PAT & SDN
=============================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Interactive CLI quiz for self-assessment with LMS export capabilities.

Usage:
    python formative/run_quiz.py                    # Run full quiz
    python formative/run_quiz.py --random           # Randomise question order
    python formative/run_quiz.py --limit 5          # Limit to 5 questions
    python formative/run_quiz.py --lo LO1 LO2       # Filter by Learning Objectives
    python formative/run_quiz.py --difficulty basic # Filter by difficulty
    python formative/run_quiz.py --review           # Review mode (show answers)
    python formative/run_quiz.py --export json      # Export to LMS-compatible JSON
    python formative/run_quiz.py --export moodle    # Export to Moodle GIFT format
    python formative/run_quiz.py --export canvas    # Export to Canvas QTI format
    python formative/run_quiz.py --validate         # Validate quiz structure

Requirements:
    pip install pyyaml --break-system-packages

Issues: Open an issue in GitHub
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from xml.dom import minidom


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

DEFAULT_QUIZ_PATH = Path(__file__).parent / "quiz.yaml"
PASSING_SCORE = 70
VERSION = "1.3.0"


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Question:
    """Represents a single quiz question."""
    id: str
    type: str
    lo_ref: str
    bloom_level: str
    difficulty: str
    stem: str
    correct: Any
    explanation: str
    points: int = 1
    options: Optional[Dict[str, str]] = None
    hint: Optional[str] = None
    misconception_ref: Optional[str] = None
    feedback: Optional[Dict[str, str]] = None
    anti_ai_note: Optional[str] = None


@dataclass
class QuizResult:
    """Stores quiz attempt results."""
    timestamp: str
    total_questions: int
    correct_answers: int
    score_percent: float
    points_earned: int
    total_points: int
    passed: bool
    time_taken_seconds: float
    questions_answered: List[Dict[str, Any]] = field(default_factory=list)
    lo_performance: Dict[str, Dict[str, int]] = field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════════════════════
# YAML_LOADING
# ═══════════════════════════════════════════════════════════════════════════════

def _import_yaml() -> Any:
    """Import PyYAML with helpful error message if missing."""
    try:
        import yaml
        return yaml
    except ImportError:
        print("Error: PyYAML not installed.")
        print("Install with: pip install pyyaml --break-system-packages")
        sys.exit(1)


def load_quiz(path: Path) -> Dict[str, Any]:
    """Load quiz from YAML file."""
    yaml = _import_yaml()
    if not path.exists():
        raise FileNotFoundError(f"Quiz file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_questions(quiz_data: Dict[str, Any]) -> List[Question]:
    """Parse questions from quiz data into Question objects."""
    questions = []
    for q in quiz_data.get("questions", []):
        questions.append(Question(
            id=q.get("id", "unknown"),
            type=q.get("type", "multiple_choice"),
            lo_ref=q.get("lo_ref", ""),
            bloom_level=q.get("bloom_level", ""),
            difficulty=q.get("difficulty", "intermediate"),
            stem=q.get("stem", ""),
            correct=q.get("correct"),
            explanation=q.get("explanation", ""),
            points=q.get("points", 1),
            options=q.get("options"),
            hint=q.get("hint"),
            misconception_ref=q.get("misconception_ref"),
            feedback=q.get("feedback"),
            anti_ai_note=q.get("anti_ai_note"),
        ))
    return questions


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_DISPLAY_HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def _print_quiz_header(metadata: Dict[str, Any], question_count: int, review_mode: bool) -> None:
    """Display quiz header with session info."""
    print()
    print("═" * 64)
    print(f"  {metadata.get('topic', 'Quiz')}")
    print("═" * 64)
    print(f"  Questions: {question_count} | Passing: {metadata.get('passing_score', 70)}%")
    if review_mode:
        print("  Mode: REVIEW (answers shown after each question)")
    print("═" * 64)
    print()


def _display_question_header(index: int, q: Question) -> None:
    """Display question number and metadata."""
    print(f"\n{'─' * 64}")
    print(f"Q{index}. [{q.difficulty.upper()}] [{q.lo_ref}] [{q.bloom_level}] ({q.points} pt)")
    print(f"{'─' * 64}")
    print(f"\n{q.stem.strip()}\n")


def _display_mc_options(options: Dict[str, str]) -> None:
    """Display multiple choice options."""
    for key, val in options.items():
        print(f"   {key}) {val}")
    print()


def _collect_mc_answer() -> str:
    """Collect multiple choice answer from user."""
    return input("Your answer (a/b/c/d): ").strip().lower()


def _show_mc_result(is_correct: bool, correct_answer: str, feedback: Optional[Dict], user_answer: str) -> None:
    """Display result for multiple choice question."""
    if is_correct:
        print("\n✅ Correct!")
    else:
        print(f"\n❌ Incorrect. Correct answer: {correct_answer}")
        if feedback and user_answer in feedback:
            print(f"   💡 {feedback[user_answer]}")


def _show_explanation(q: Question, review_mode: bool, is_correct: bool) -> None:
    """Show explanation when appropriate."""
    if review_mode or not is_correct:
        print(f"\n📖 Explanation: {q.explanation}")
        if q.misconception_ref:
            print(f"   📚 See: {q.misconception_ref}")


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_ANSWER_PROCESSING
# ═══════════════════════════════════════════════════════════════════════════════

def _process_mc_question(q: Question) -> Tuple[bool, str]:
    """Process a multiple choice question. Returns (is_correct, user_answer)."""
    if not q.options:
        return False, ""
    _display_mc_options(q.options)
    user_answer = _collect_mc_answer()
    is_correct = user_answer == q.correct
    _show_mc_result(is_correct, q.correct, q.feedback, user_answer)
    return is_correct, user_answer


def _process_fill_blank_question(q: Question) -> Tuple[bool, str]:
    """Process a fill-in-the-blank question."""
    if q.hint:
        print(f"   Hint: {q.hint}")
    user_answer = input("Your answer: ").strip()
    correct_answers = q.correct if isinstance(q.correct, list) else [q.correct]
    is_correct = user_answer.lower() in [str(a).lower() for a in correct_answers]
    if is_correct:
        print("\n✅ Correct!")
    else:
        print(f"\n❌ Incorrect. Accepted answers: {', '.join(str(a) for a in correct_answers)}")
    return is_correct, user_answer


def _update_lo_stats(lo_perf: Dict, lo_ref: str, is_correct: bool, points: int) -> None:
    """Update learning objective performance statistics."""
    if lo_ref not in lo_perf:
        lo_perf[lo_ref] = {"correct": 0, "total": 0, "points": 0}
    lo_perf[lo_ref]["total"] += 1
    if is_correct:
        lo_perf[lo_ref]["correct"] += 1
        lo_perf[lo_ref]["points"] += points


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════

def _calculate_score(correct: int, total: int, points_earned: int, total_points: int) -> float:
    """Calculate percentage score."""
    if total_points == 0:
        return 0.0
    return round((points_earned / total_points) * 100, 1)


def _print_results_summary(result: QuizResult, passing_score: int) -> None:
    """Display final quiz results."""
    print("\n" + "═" * 64)
    print("  RESULTS")
    print("═" * 64)
    print(f"  Score: {result.score_percent}% ({result.correct_answers}/{result.total_questions})")
    print(f"  Points: {result.points_earned}/{result.total_points}")
    print(f"  Time: {result.time_taken_seconds:.0f} seconds")
    status = "✅ PASSED" if result.passed else "❌ NOT PASSED"
    print(f"  Status: {status} (required: {passing_score}%)")
    print("═" * 64)


def _print_lo_breakdown(lo_perf: Dict[str, Dict[str, int]]) -> None:
    """Display performance breakdown by learning objective."""
    if not lo_perf:
        return
    print("\n  Performance by Learning Objective:")
    for lo, stats in sorted(lo_perf.items()):
        pct = round((stats["correct"] / stats["total"]) * 100) if stats["total"] > 0 else 0
        bar = "█" * (pct // 10) + "░" * (10 - pct // 10)
        print(f"    {lo}: {bar} {pct}% ({stats['correct']}/{stats['total']})")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_QUIZ_RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def run_interactive_quiz(
    questions: List[Question],
    metadata: Dict[str, Any],
    randomise: bool = False,
    limit: Optional[int] = None,
    review_mode: bool = False,
) -> QuizResult:
    """
    Run interactive quiz session.
    
    In previous cohorts, students who scored below 50% on the first attempt
    typically benefited from reviewing docs/misconceptions.md before retrying.
    """
    if randomise:
        questions = questions.copy()
        random.shuffle(questions)
    if limit:
        questions = questions[:limit]
    
    correct = 0
    points_earned = 0
    total_points = sum(q.points for q in questions)
    answered: List[Dict[str, Any]] = []
    lo_perf: Dict[str, Dict[str, int]] = {}
    passing = metadata.get("passing_score", PASSING_SCORE)
    
    start_time = time.time()
    _print_quiz_header(metadata, len(questions), review_mode)
    
    for i, q in enumerate(questions, 1):
        _display_question_header(i, q)
        
        is_correct = False
        user_answer = ""
        
        if q.type == "multiple_choice" and q.options:
            is_correct, user_answer = _process_mc_question(q)
        elif q.type == "fill_blank":
            is_correct, user_answer = _process_fill_blank_question(q)
        else:
            print(f"  [Question type '{q.type}' - manual review needed]")
            user_answer = input("Your answer: ").strip()
        
        if is_correct:
            correct += 1
            points_earned += q.points
        
        _update_lo_stats(lo_perf, q.lo_ref, is_correct, q.points if is_correct else 0)
        _show_explanation(q, review_mode, is_correct)
        
        answered.append({
            "question_id": q.id,
            "user_answer": user_answer,
            "correct": is_correct,
            "points": q.points if is_correct else 0,
        })
    
    elapsed = time.time() - start_time
    score = _calculate_score(correct, len(questions), points_earned, total_points)
    
    result = QuizResult(
        timestamp=datetime.now().isoformat(),
        total_questions=len(questions),
        correct_answers=correct,
        score_percent=score,
        points_earned=points_earned,
        total_points=total_points,
        passed=score >= passing,
        time_taken_seconds=elapsed,
        questions_answered=answered,
        lo_performance=lo_perf,
    )
    
    _print_results_summary(result, passing)
    _print_lo_breakdown(lo_perf)
    
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

def validate_quiz_structure(quiz_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate quiz YAML structure and content.
    
    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues: List[str] = []
    meta = quiz_data.get("metadata", {})
    questions = quiz_data.get("questions", [])
    
    # Check metadata
    if not meta:
        issues.append("Missing metadata section")
    else:
        required_meta = ["week", "topic", "version", "passing_score"]
        for field in required_meta:
            if field not in meta:
                issues.append(f"Missing metadata field: {field}")
    
    # Check questions
    if not questions:
        issues.append("No questions found")
    else:
        declared_count = meta.get("total_questions", 0)
        if declared_count != len(questions):
            issues.append(f"Question count mismatch: declared {declared_count}, actual {len(questions)}")
        
        lo_covered = set()
        for i, q in enumerate(questions):
            q_id = q.get("id", f"question_{i}")
            if not q.get("stem"):
                issues.append(f"{q_id}: Missing stem")
            if not q.get("correct"):
                issues.append(f"{q_id}: Missing correct answer")
            if not q.get("lo_ref"):
                issues.append(f"{q_id}: Missing lo_ref")
            else:
                lo_covered.add(q.get("lo_ref"))
        
        # Check LO coverage
        declared_los = set(meta.get("lo_coverage", []))
        if declared_los and lo_covered != declared_los:
            missing = declared_los - lo_covered
            if missing:
                issues.append(f"LOs declared but not covered: {missing}")
    
    return len(issues) == 0, issues


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT_JSON
# ═══════════════════════════════════════════════════════════════════════════════

def _build_json_question(q: Dict[str, Any]) -> Dict[str, Any]:
    """Build a single question for JSON export."""
    return {
        "id": q.get("id"),
        "type": q.get("type"),
        "lo_ref": q.get("lo_ref"),
        "bloom_level": q.get("bloom_level"),
        "difficulty": q.get("difficulty"),
        "points": q.get("points", 1),
        "stem": q.get("stem"),
        "options": q.get("options"),
        "correct": q.get("correct"),
        "explanation": q.get("explanation"),
        "feedback": q.get("feedback"),
    }


def export_to_json(quiz_data: Dict[str, Any], output_path: Path) -> None:
    """Export quiz to LMS-compatible JSON format."""
    export_data = {
        "metadata": {
            "title": f"Week {quiz_data.get('metadata', {}).get('week', '?')}: "
                     f"{quiz_data.get('metadata', {}).get('topic', 'Quiz')}",
            "version": quiz_data.get("metadata", {}).get("version", "1.0.0"),
            "exported_at": datetime.now().isoformat(),
            "passing_score": quiz_data.get("metadata", {}).get("passing_score", 70),
            "total_questions": len(quiz_data.get("questions", [])),
            "lms_format": "generic_json_v1",
        },
        "questions": [_build_json_question(q) for q in quiz_data.get("questions", [])],
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Exported to JSON: {output_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT_MOODLE_GIFT
# ═══════════════════════════════════════════════════════════════════════════════

def _escape_gift_text(text: str) -> str:
    """Escape special characters for GIFT format."""
    return text.replace("\n", " ").replace("{", "\\{").replace("}", "\\}")


def _build_gift_mc_question(q: Dict[str, Any]) -> List[str]:
    """Build GIFT format for multiple choice question."""
    lines = []
    q_id = q.get("id", "q")
    stem = _escape_gift_text(q.get("stem", ""))
    
    lines.append(f"// {q_id} - {q.get('lo_ref', '')} - {q.get('difficulty', '')}")
    lines.append(f"::{q_id}::{stem} {{")
    
    for key, val in q.get("options", {}).items():
        val_escaped = _escape_gift_text(val)
        if key == q.get("correct"):
            lines.append(f"  ={val_escaped}")
        else:
            fb = q.get("feedback", {}).get(key, "")
            if fb:
                lines.append(f"  ~{val_escaped}#{fb}")
            else:
                lines.append(f"  ~{val_escaped}")
    lines.append("}")
    lines.append("")
    return lines


def _build_gift_fill_blank(q: Dict[str, Any]) -> List[str]:
    """Build GIFT format for fill-in-blank question."""
    lines = []
    q_id = q.get("id", "q")
    stem = _escape_gift_text(q.get("stem", ""))
    correct = q.get("correct", [])
    
    lines.append(f"// {q_id} - {q.get('lo_ref', '')} - {q.get('difficulty', '')}")
    if isinstance(correct, list):
        answers = " ".join(f"={a}" for a in correct)
    else:
        answers = f"={correct}"
    lines.append(f"::{q_id}::{stem} {{{answers}}}")
    lines.append("")
    return lines


def export_to_moodle_gift(quiz_data: Dict[str, Any], output_path: Path) -> None:
    """Export quiz to Moodle GIFT format."""
    lines = [
        "// Week 6: NAT/PAT & SDN - Moodle GIFT Format",
        "// Generated by run_quiz.py",
        f"// {datetime.now().isoformat()}",
        "",
        "$CATEGORY: Week 6 - NAT/PAT & SDN",
        "",
    ]
    
    for q in quiz_data.get("questions", []):
        if q.get("type") == "multiple_choice" and q.get("options"):
            lines.extend(_build_gift_mc_question(q))
        elif q.get("type") == "fill_blank":
            lines.extend(_build_gift_fill_blank(q))
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    print(f"✅ Exported to Moodle GIFT: {output_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT_MOODLE_XML
# ═══════════════════════════════════════════════════════════════════════════════

def _add_xml_question_base(root: ET.Element, q: Dict[str, Any]) -> ET.Element:
    """Add base question element with common fields."""
    q_type = q.get("type", "multiple_choice")
    xml_type = {"multiple_choice": "multichoice", "fill_blank": "shortanswer"}.get(q_type, "essay")
    
    question = ET.SubElement(root, "question", type=xml_type)
    
    name = ET.SubElement(question, "name")
    ET.SubElement(name, "text").text = q.get("id", "Question")
    
    qtext = ET.SubElement(question, "questiontext", format="html")
    ET.SubElement(qtext, "text").text = f"<![CDATA[<p>{q.get('stem', '').strip()}</p>]]>"
    
    gfb = ET.SubElement(question, "generalfeedback", format="html")
    ET.SubElement(gfb, "text").text = f"<![CDATA[<p>{q.get('explanation', '')}</p>]]>"
    
    ET.SubElement(question, "defaultgrade").text = str(q.get("points", 1))
    
    return question


def _add_xml_mc_answers(question: ET.Element, q: Dict[str, Any]) -> None:
    """Add multiple choice answers to XML question."""
    ET.SubElement(question, "single").text = "true"
    ET.SubElement(question, "shuffleanswers").text = "true"
    
    for key, val in q.get("options", {}).items():
        fraction = "100" if key == q.get("correct") else "0"
        answer = ET.SubElement(question, "answer", fraction=fraction, format="html")
        ET.SubElement(answer, "text").text = f"<![CDATA[<p>{val}</p>]]>"
        fb = q.get("feedback", {}).get(key, "")
        afb = ET.SubElement(answer, "feedback", format="html")
        ET.SubElement(afb, "text").text = f"<![CDATA[<p>{fb}</p>]]>" if fb else ""


def _add_xml_fill_blank_answers(question: ET.Element, q: Dict[str, Any]) -> None:
    """Add fill-in-blank answers to XML question."""
    ET.SubElement(question, "usecase").text = "0"
    correct = q.get("correct", [])
    if not isinstance(correct, list):
        correct = [correct]
    for ans in correct:
        answer = ET.SubElement(question, "answer", fraction="100", format="plain_text")
        ET.SubElement(answer, "text").text = str(ans)


def export_to_moodle_xml(quiz_data: Dict[str, Any], output_path: Path) -> None:
    """Export quiz to Moodle XML format."""
    root = ET.Element("quiz")
    
    cat = ET.SubElement(root, "question", type="category")
    cat_text = ET.SubElement(cat, "category")
    ET.SubElement(cat_text, "text").text = "$course$/Week 6 - NAT/PAT & SDN"
    
    for q in quiz_data.get("questions", []):
        question = _add_xml_question_base(root, q)
        q_type = q.get("type", "multiple_choice")
        
        if q_type == "multiple_choice" and q.get("options"):
            _add_xml_mc_answers(question, q)
        elif q_type == "fill_blank":
            _add_xml_fill_blank_answers(question, q)
    
    xml_str = ET.tostring(root, encoding="unicode")
    dom = minidom.parseString(xml_str)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(dom.toprettyxml(indent="  "))
    
    print(f"✅ Exported to Moodle XML: {output_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# CLI_ARGUMENT_PARSING
# ═══════════════════════════════════════════════════════════════════════════════

def _create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="Week 6 Formative Quiz Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_quiz.py                     # Full quiz
    python run_quiz.py --random --limit 5  # 5 random questions
    python run_quiz.py --lo LO1 LO2        # Only LO1 and LO2
    python run_quiz.py --export json       # Export to JSON
    python run_quiz.py --validate          # Validate quiz structure

Issues: Open an issue in GitHub
        """
    )
    parser.add_argument("--quiz", "-q", type=Path, default=DEFAULT_QUIZ_PATH,
                        help="Path to quiz YAML file")
    parser.add_argument("--random", "-r", action="store_true",
                        help="Randomise question order")
    parser.add_argument("--limit", "-l", type=int, help="Limit number of questions")
    parser.add_argument("--lo", nargs="+", help="Filter by Learning Objectives")
    parser.add_argument("--difficulty", "-d", choices=["basic", "intermediate", "advanced"],
                        help="Filter by difficulty")
    parser.add_argument("--review", action="store_true",
                        help="Review mode: show answers after each question")
    parser.add_argument("--export", "-e", choices=["json", "moodle", "moodle-xml", "gift"],
                        help="Export quiz to LMS format")
    parser.add_argument("--output", "-o", type=Path,
                        help="Output file for export (default: auto-generated)")
    parser.add_argument("--validate", action="store_true",
                        help="Validate quiz structure without running")
    parser.add_argument("--version", "-v", action="version", version=f"Quiz Runner v{VERSION}")
    return parser


def _handle_export(args: argparse.Namespace, quiz_data: Dict[str, Any]) -> int:
    """Handle quiz export to various formats."""
    base_name = args.quiz.stem
    
    if args.export == "json":
        output = args.output or Path(f"{base_name}_export.json")
        export_to_json(quiz_data, output)
    elif args.export in ("moodle", "gift"):
        output = args.output or Path(f"{base_name}_moodle.gift")
        export_to_moodle_gift(quiz_data, output)
    elif args.export == "moodle-xml":
        output = args.output or Path(f"{base_name}_moodle.xml")
        export_to_moodle_xml(quiz_data, output)
    return 0


def _handle_validation(quiz_data: Dict[str, Any]) -> int:
    """Handle quiz validation."""
    is_valid, issues = validate_quiz_structure(quiz_data)
    if is_valid:
        print("✅ Quiz structure is valid")
        return 0
    else:
        print("❌ Quiz validation failed:")
        for issue in issues:
            print(f"   - {issue}")
        return 1


def _filter_questions(questions: List[Question], args: argparse.Namespace) -> List[Question]:
    """Apply filters to question list."""
    if args.lo:
        lo_set = set(args.lo)
        questions = [q for q in questions if q.lo_ref in lo_set]
    if args.difficulty:
        questions = [q for q in questions if q.difficulty == args.difficulty]
    return questions


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point."""
    parser = _create_argument_parser()
    args = parser.parse_args()
    
    try:
        quiz_data = load_quiz(args.quiz)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Error loading quiz: {e}")
        return 1
    
    if args.validate:
        return _handle_validation(quiz_data)
    
    if args.export:
        return _handle_export(args, quiz_data)
    
    questions = parse_questions(quiz_data)
    questions = _filter_questions(questions, args)
    
    if not questions:
        print("No questions match the specified filters.")
        return 1
    
    result = run_interactive_quiz(
        questions=questions,
        metadata=quiz_data.get("metadata", {}),
        randomise=args.random,
        limit=args.limit,
        review_mode=args.review,
    )
    
    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
