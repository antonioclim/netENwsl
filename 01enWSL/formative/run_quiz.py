#!/usr/bin/env python3
"""
Quiz Runner — Week 1 Formative Assessment
==========================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

A standalone quiz runner that works with both YAML and JSON formats.
Supports interactive mode and LMS export (Moodle/Canvas compatible).

Usage:
    python run_quiz.py                      # Interactive quiz (all questions)
    python run_quiz.py --section pre_lab    # Run specific section
    python run_quiz.py --list-sections      # Show available sections
    python run_quiz.py --validate           # Validate quiz file
    python run_quiz.py --export-json        # Export to LMS-compatible JSON
    python run_quiz.py --export-moodle      # Export to Moodle XML
    python run_quiz.py --stats              # Show quiz statistics

Requirements:
    - Python 3.8+
    - PyYAML (pip install pyyaml)
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

QUIZ_DIR = Path(__file__).parent
DEFAULT_QUIZ_YAML = QUIZ_DIR / "quiz.yaml"
DEFAULT_QUIZ_JSON = QUIZ_DIR / "quiz.json"


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ LOADER
# ═══════════════════════════════════════════════════════════════════════════════

def load_quiz(path: Path | None = None) -> dict[str, Any]:
    """Load quiz from YAML or JSON file."""
    if path is None:
        if DEFAULT_QUIZ_YAML.exists() and YAML_AVAILABLE:
            path = DEFAULT_QUIZ_YAML
        elif DEFAULT_QUIZ_JSON.exists():
            path = DEFAULT_QUIZ_JSON
        else:
            raise FileNotFoundError("No quiz file found. Expected quiz.yaml or quiz.json")

    with open(path, encoding="utf-8") as f:
        if path.suffix in (".yaml", ".yml"):
            if not YAML_AVAILABLE:
                raise ImportError("PyYAML required. Install: pip install pyyaml")
            return yaml.safe_load(f)
        return json.load(f)


def save_quiz_json(quiz: dict[str, Any], path: Path) -> None:
    """Save quiz to JSON format."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(quiz, f, indent=2, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

def validate_quiz(quiz: dict[str, Any]) -> tuple[bool, list[str]]:
    """Validate quiz structure and content."""
    errors = []

    required_keys = ["metadata", "questions"]
    for key in required_keys:
        if key not in quiz:
            errors.append(f"Missing required key: {key}")

    if errors:
        return False, errors

    meta = quiz.get("metadata", {})
    for key in ["week", "topic", "total_questions"]:
        if key not in meta:
            errors.append(f"Metadata missing: {key}")

    questions = quiz.get("questions", [])
    question_ids = set()

    for i, q in enumerate(questions):
        q_id = q.get("id", f"question_{i}")

        if q_id in question_ids:
            errors.append(f"Duplicate question ID: {q_id}")
        question_ids.add(q_id)

        for field in ["id", "type", "stem"]:
            if field not in q:
                errors.append(f"Question {q_id} missing field: {field}")

        if "correct" not in q and "correct_answer" not in q and "correct_answers" not in q:
            errors.append(f"Question {q_id} missing correct answer")

    for section in quiz.get("sections", []):
        for qid in section.get("questions", []):
            if qid not in question_ids:
                errors.append(f"Section '{section.get('id')}' references unknown question: {qid}")

    declared_count = meta.get("total_questions", 0)
    actual_count = len(questions)
    if declared_count != actual_count:
        errors.append(f"Metadata declares {declared_count} questions but found {actual_count}")

    return len(errors) == 0, errors


# ═══════════════════════════════════════════════════════════════════════════════
# INTERACTIVE QUIZ RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def run_interactive_quiz(
    quiz: dict[str, Any],
    section_id: str | None = None,
    randomise: bool = False,
    limit: int | None = None
) -> float:
    """Run interactive quiz in terminal."""
    questions = quiz.get("questions", [])

    if section_id:
        section = next((s for s in quiz.get("sections", []) if s["id"] == section_id), None)
        if not section:
            print(f"Error: Section '{section_id}' not found")
            return 0.0
        section_qids = set(section.get("questions", []))
        questions = [q for q in questions if q["id"] in section_qids]

    if not questions:
        print("No questions to run")
        return 0.0

    if randomise:
        random.shuffle(questions)
    if limit:
        questions = questions[:limit]

    meta = quiz.get("metadata", {})
    print("\n" + "=" * 70)
    print(f"  QUIZ: {meta.get('topic', 'Unknown Topic')}")
    print(f"  Week {meta.get('week', '?')} | Questions: {len(questions)}")
    print(f"  Passing Score: {meta.get('passing_score', 70)}%")
    print("=" * 70)

    correct = 0
    total_points = 0
    earned_points = 0

    for i, q in enumerate(questions, 1):
        points = q.get("points", 1)
        total_points += points

        print(f"\n{'─' * 70}")
        print(f"Q{i}/{len(questions)} [{q.get('lo_ref', '?')}] [{q.get('difficulty', '?')}] ({points} pts)")
        print(f"\n{q['stem']}\n")

        q_type = q.get("type", "multiple_choice")
        user_correct = False

        if q_type == "multiple_choice":
            user_correct = _ask_multiple_choice(q)
        elif q_type == "fill_blank":
            user_correct = _ask_fill_blank(q)
        elif q_type == "true_false":
            user_correct = _ask_true_false(q)
        elif q_type == "numeric":
            user_correct = _ask_numeric(q)
        elif q_type == "ordering":
            user_correct = _ask_ordering(q)
        else:
            print(f"  [Skipped: Unsupported question type '{q_type}']")
            continue

        if user_correct:
            correct += 1
            earned_points += points
            print("  ✅ Correct!")
        else:
            correct_answer = q.get("correct", q.get("correct_answer", "?"))
            print(f"  ❌ Incorrect. Answer: {correct_answer}")

        if "explanation" in q:
            explanation = q["explanation"]
            if isinstance(explanation, str):
                print(f"\n  📖 {explanation[:200]}...")

    score = (earned_points / total_points * 100) if total_points > 0 else 0
    passed = score >= meta.get("passing_score", 70)

    print("\n" + "=" * 70)
    print("  RESULTS")
    print(f"  Correct: {correct}/{len(questions)}")
    print(f"  Points: {earned_points}/{total_points}")
    print(f"  Score: {score:.1f}%")
    print(f"  Status: {'✅ PASSED' if passed else '❌ NEEDS REVIEW'}")
    print("=" * 70 + "\n")

    return score


def _ask_multiple_choice(q: dict) -> bool:
    """Handle multiple choice question."""
    options = q.get("options", {})
    if isinstance(options, list):
        for opt in options:
            print(f"    {opt['key']}) {opt['text']}")
    else:
        for key, text in options.items():
            print(f"    {key}) {text}")

    answer = input("\n  Your answer: ").strip().lower()
    correct = q.get("correct", q.get("correct_answer", "")).lower()
    return answer == correct


def _ask_fill_blank(q: dict) -> bool:
    """Handle fill-in-the-blank question."""
    if q.get("hint"):
        print(f"  💡 Hint: {q['hint']}")

    answer = input("  Your answer: ").strip()
    correct_answers = q.get("correct", q.get("correct_answers", []))

    if not isinstance(correct_answers, list):
        correct_answers = [correct_answers]

    if q.get("case_sensitive", False):
        return answer in correct_answers
    return answer.lower() in [str(c).lower() for c in correct_answers]


def _ask_true_false(q: dict) -> bool:
    """Handle true/false question."""
    print("    T) True")
    print("    F) False")

    answer = input("\n  Your answer (T/F): ").strip().upper()
    correct = q.get("correct", q.get("correct_answer"))

    user_bool = answer in ("T", "TRUE", "YES", "1")
    return user_bool == correct


def _ask_numeric(q: dict) -> bool:
    """Handle numeric question."""
    if q.get("hint"):
        print(f"  💡 Hint: {q['hint']}")

    try:
        answer = float(input("  Your answer: ").strip())
    except ValueError:
        return False

    correct = float(q.get("correct", q.get("correct_answer", 0)))
    tolerance = float(q.get("tolerance", 0))

    return abs(answer - correct) <= tolerance


def _ask_ordering(q: dict) -> bool:
    """Handle ordering question."""
    items = q.get("items", [])
    for item in items:
        print(f"    {item['id']}) {item['text']}")

    print("\n  Enter the correct order (e.g. d,b,a,c):")
    answer = input("  Your answer: ").strip().lower()
    answer_list = [x.strip() for x in answer.replace(" ", "").split(",")]

    correct_order = q.get("correct_order", [])
    return answer_list == [x.lower() for x in correct_order]


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def export_to_moodle_xml(quiz: dict[str, Any], output_path: Path) -> None:
    """Export quiz to Moodle XML format."""
    meta = quiz.get("metadata", {})

    xml_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<quiz>',
        f'  <!-- Week {meta.get("week")} - {meta.get("topic")} -->',
        f'  <!-- Exported: {datetime.now().isoformat()} -->',
    ]

    for q in quiz.get("questions", []):
        q_type = q.get("type", "multiple_choice")

        if q_type == "multiple_choice":
            xml_parts.append(_moodle_multichoice(q))
        elif q_type == "true_false":
            xml_parts.append(_moodle_truefalse(q))
        elif q_type in ("fill_blank", "numeric"):
            xml_parts.append(_moodle_shortanswer(q))

    xml_parts.append('</quiz>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(xml_parts))

    print(f"Exported to Moodle XML: {output_path}")


def _moodle_multichoice(q: dict) -> str:
    """Generate Moodle XML for multiple choice question."""
    lines = [
        '  <question type="multichoice">',
        f'    <name><text>{q["id"]}</text></name>',
        f'    <questiontext format="html"><text><![CDATA[{q["stem"]}]]></text></questiontext>',
        '    <shuffleanswers>true</shuffleanswers>',
        '    <single>true</single>',
    ]

    correct = q.get("correct", q.get("correct_answer", ""))
    options = q.get("options", {})

    if isinstance(options, list):
        for opt in options:
            fraction = "100" if opt["key"] == correct else "0"
            lines.append(f'    <answer fraction="{fraction}" format="html">')
            lines.append(f'      <text><![CDATA[{opt["text"]}]]></text>')
            lines.append('    </answer>')
    else:
        for key, text in options.items():
            fraction = "100" if key == correct else "0"
            lines.append(f'    <answer fraction="{fraction}" format="html">')
            lines.append(f'      <text><![CDATA[{text}]]></text>')
            lines.append('    </answer>')

    if "explanation" in q:
        exp = q["explanation"] if isinstance(q["explanation"], str) else str(q["explanation"])
        lines.append(f'    <generalfeedback format="html"><text><![CDATA[{exp}]]></text></generalfeedback>')

    lines.append('  </question>')
    return "\n".join(lines)


def _moodle_truefalse(q: dict) -> str:
    """Generate Moodle XML for true/false question."""
    correct = q.get("correct", q.get("correct_answer", True))
    true_fraction = "100" if correct else "0"
    false_fraction = "0" if correct else "100"

    return f"""  <question type="truefalse">
    <name><text>{q["id"]}</text></name>
    <questiontext format="html"><text><![CDATA[{q["stem"]}]]></text></questiontext>
    <answer fraction="{true_fraction}" format="html"><text>true</text></answer>
    <answer fraction="{false_fraction}" format="html"><text>false</text></answer>
  </question>"""


def _moodle_shortanswer(q: dict) -> str:
    """Generate Moodle XML for short answer question."""
    correct = q.get("correct", q.get("correct_answers", q.get("correct_answer", "")))
    if not isinstance(correct, list):
        correct = [str(correct)]

    lines = [
        '  <question type="shortanswer">',
        f'    <name><text>{q["id"]}</text></name>',
        f'    <questiontext format="html"><text><![CDATA[{q["stem"]}]]></text></questiontext>',
        f'    <usecase>{1 if q.get("case_sensitive") else 0}</usecase>',
    ]

    for ans in correct:
        lines.append(f'    <answer fraction="100" format="html"><text>{ans}</text></answer>')

    lines.append('  </question>')
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# STATISTICS
# ═══════════════════════════════════════════════════════════════════════════════

def show_statistics(quiz: dict[str, Any]) -> None:
    """Display quiz statistics."""
    meta = quiz.get("metadata", {})
    questions = quiz.get("questions", [])

    print("\n" + "=" * 60)
    print(f"  QUIZ STATISTICS: {meta.get('topic', 'Unknown')}")
    print("=" * 60)

    print(f"\n  Total Questions: {len(questions)}")
    print(f"  Passing Score: {meta.get('passing_score', 70)}%")
    print(f"  Estimated Time: {meta.get('estimated_time_minutes', '?')} minutes")

    type_counts: dict[str, int] = {}
    for q in questions:
        qt = q.get("type", "unknown")
        type_counts[qt] = type_counts.get(qt, 0) + 1

    print("\n  By Type:")
    for qt, count in sorted(type_counts.items()):
        print(f"    {qt}: {count}")

    lo_counts: dict[str, int] = {}
    for q in questions:
        lo = q.get("lo_ref", "unspecified")
        lo_counts[lo] = lo_counts.get(lo, 0) + 1

    print("\n  By Learning Objective:")
    for lo, count in sorted(lo_counts.items()):
        bar = "█" * count
        print(f"    {lo}: {bar} ({count})")

    diff_counts: dict[str, int] = {}
    for q in questions:
        diff = q.get("difficulty", "unspecified")
        diff_counts[diff] = diff_counts.get(diff, 0) + 1

    print("\n  By Difficulty:")
    for diff, count in sorted(diff_counts.items()):
        print(f"    {diff}: {count}")

    bloom_counts: dict[str, int] = {}
    for q in questions:
        bloom = q.get("bloom_level", "unspecified")
        bloom_counts[bloom] = bloom_counts.get(bloom, 0) + 1

    print("\n  By Bloom Level:")
    for bloom, count in sorted(bloom_counts.items()):
        print(f"    {bloom}: {count}")

    print("\n  Sections:")
    for section in quiz.get("sections", []):
        q_count = len(section.get("questions", []))
        print(f"    {section['id']}: {q_count} questions")

    print("\n" + "=" * 60 + "\n")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Week 1 Formative Quiz Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_quiz.py                      # Run full quiz
    python run_quiz.py --section pre_lab    # Run pre-lab section
    python run_quiz.py --random --limit 5   # Random 5 questions
    python run_quiz.py --validate           # Validate quiz file
    python run_quiz.py --export-json        # Export to JSON
    python run_quiz.py --export-moodle      # Export to Moodle XML
    python run_quiz.py --stats              # Show statistics
        """
    )

    parser.add_argument("--quiz", type=Path, help="Quiz file path")
    parser.add_argument("--section", help="Run specific section only")
    parser.add_argument("--random", action="store_true", help="Randomise question order")
    parser.add_argument("--limit", type=int, help="Limit number of questions")
    parser.add_argument("--list-sections", action="store_true", help="List available sections")
    parser.add_argument("--validate", action="store_true", help="Validate quiz file")
    parser.add_argument("--export-json", action="store_true", help="Export to JSON format")
    parser.add_argument("--export-moodle", action="store_true", help="Export to Moodle XML")
    parser.add_argument("--stats", action="store_true", help="Show quiz statistics")

    args = parser.parse_args()

    try:
        quiz = load_quiz(args.quiz)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Error loading quiz: {e}")
        return 1

    if args.validate:
        is_valid, errors = validate_quiz(quiz)
        if is_valid:
            print("✅ Quiz validation passed!")
            return 0
        print("❌ Quiz validation failed:")
        for err in errors:
            print(f"  - {err}")
        return 1

    if args.list_sections:
        print("\nAvailable sections:")
        for section in quiz.get("sections", []):
            q_count = len(section.get("questions", []))
            time_limit = section.get("time_limit_minutes", "unlimited")
            print(f"  {section['id']}: {section.get('name', '?')} ({q_count} questions, {time_limit} min)")
        print()
        return 0

    if args.stats:
        show_statistics(quiz)
        return 0

    if args.export_json:
        output = QUIZ_DIR / "quiz_lms_export.json"
        save_quiz_json(quiz, output)
        print(f"Exported to JSON: {output}")
        return 0

    if args.export_moodle:
        output = QUIZ_DIR / "quiz_moodle.xml"
        export_to_moodle_xml(quiz, output)
        return 0

    run_interactive_quiz(quiz, args.section, args.random, args.limit)
    return 0


if __name__ == "__main__":
    sys.exit(main())
