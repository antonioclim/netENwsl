#!/usr/bin/env python3
"""
Formative Quiz Runner - Week 3: Network Programming
NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim

Usage:
    python run_quiz.py              # Interactive quiz
    python run_quiz.py --validate   # Validate structure
    python run_quiz.py --export-lms moodle  # Export to Moodle GIFT
    python run_quiz.py --export-lms canvas  # Export to Canvas JSON
"""
from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import json
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: pip install pyyaml --break-system-packages")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
QUIZ_FILE = Path(__file__).parent / "quiz.yaml"


class Colours:
    """Terminal colour codes for output formatting."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'


# ═══════════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════════════════════════
def load_quiz(path: Path) -> dict[str, Any]:
    """Load quiz from YAML file."""
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════
def validate_quiz(quiz: dict[str, Any]) -> list[str]:
    """
    Validate quiz structure against schema requirements.
    
    Returns list of error messages (empty if valid).
    """
    errors = []
    if 'metadata' not in quiz:
        errors.append("Missing metadata section")
    if 'questions' not in quiz:
        errors.append("Missing questions section")
        return errors
    
    required_fields = ['id', 'lo_ref', 'bloom_level', 'type', 'stem', 'correct']
    for q in quiz.get('questions', []):
        qid = q.get('id', '?')
        for field in required_fields:
            if field not in q:
                errors.append(f"Question {qid}: missing '{field}'")
    return errors


def _check_answer(question: dict, user_answer: str) -> bool:
    """Check if user answer matches correct answer."""
    if question['type'] == 'multiple_choice':
        return user_answer.lower() == question['correct'].lower()
    else:
        correct_list = question['correct']
        if not isinstance(correct_list, list):
            correct_list = [correct_list]
        return user_answer in correct_list


def _display_question(question: dict, index: int, total: int) -> None:
    """Display a single question with options."""
    print(f"\n{Colours.CYAN}Q{index}/{total}{Colours.END} "
          f"[{question['bloom_level']}] [{question['lo_ref']}]")
    print(question['stem'].strip())
    
    if question['type'] == 'multiple_choice':
        for key, val in sorted(question.get('options', {}).items()):
            print(f"  {Colours.YELLOW}{key}){Colours.END} {val}")


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ RUNNER
# ═══════════════════════════════════════════════════════════════════════════════
def run_quiz(
    quiz: dict[str, Any],
    randomise: bool = False,
    limit: int | None = None
) -> dict[str, Any]:
    """
    Run interactive quiz session.
    
    Args:
        quiz: Loaded quiz data
        randomise: Shuffle question order
        limit: Maximum number of questions
        
    Returns:
        Results dictionary with score and per-question outcomes
    """
    questions = quiz['questions'].copy()
    if randomise:
        random.shuffle(questions)
    if limit:
        questions = questions[:limit]
    
    # Header
    meta = quiz['metadata']
    print(f"\n{Colours.BOLD}{'=' * 60}{Colours.END}")
    print(f"{Colours.BOLD}  {meta['title']}{Colours.END}")
    print(f"{Colours.BOLD}{'=' * 60}{Colours.END}")
    print(f"  Questions: {len(questions)} | Passing: {meta.get('passing_score', 70)}%\n")
    
    results = {'correct': 0, 'total': len(questions), 'answers': []}
    
    for idx, q in enumerate(questions, 1):
        _display_question(q, idx, len(questions))
        
        answer = input(f"\n{Colours.GREEN}Answer: {Colours.END}").strip()
        is_correct = _check_answer(q, answer)
        
        if is_correct:
            print(f"{Colours.GREEN}✓ Correct!{Colours.END}")
            results['correct'] += 1
        else:
            print(f"{Colours.RED}✗ Incorrect. Answer: {q['correct']}{Colours.END}")
        
        if 'explanation' in q:
            expl = q['explanation'][:200]
            print(f"{Colours.CYAN}Explanation:{Colours.END} {expl}...")
        
        results['answers'].append({'id': q['id'], 'correct': is_correct})
    
    # Summary
    pct = round(results['correct'] / results['total'] * 100, 1) if results['total'] else 0
    passed = pct >= meta.get('passing_score', 70)
    
    print(f"\n{Colours.BOLD}{'=' * 60}{Colours.END}")
    print(f"  Score: {results['correct']}/{results['total']} ({pct}%)")
    status_colour = Colours.GREEN if passed else Colours.RED
    status_text = 'PASSED' if passed else 'NEEDS REVIEW'
    print(f"  Status: {status_colour}{status_text}{Colours.END}")
    print(f"{Colours.BOLD}{'=' * 60}{Colours.END}\n")
    
    return results


# ═══════════════════════════════════════════════════════════════════════════════
# LMS EXPORT — MOODLE GIFT FORMAT
# ═══════════════════════════════════════════════════════════════════════════════
def export_moodle(quiz: dict[str, Any], output: Path) -> None:
    """Export quiz to Moodle GIFT format."""
    lines = [
        f"// {quiz['metadata']['title']}",
        f"// Generated: {datetime.now().isoformat()}",
        "$CATEGORY: Week3_NetworkProgramming",
        ""
    ]
    
    for q in quiz['questions']:
        if q['type'] != 'multiple_choice':
            continue
        stem = q['stem'].replace('\n', ' ').replace('{', '\\{').strip()
        lines.append(f"::{q['id']}::{stem} {{")
        for key, val in sorted(q.get('options', {}).items()):
            prefix = "=" if key == q['correct'] else "~"
            lines.append(f"  {prefix}{val}")
        lines.append("}")
        lines.append("")
    
    output.write_text('\n'.join(lines), encoding='utf-8')
    print(f"{Colours.GREEN}✓ Exported to Moodle GIFT: {output}{Colours.END}")


# ═══════════════════════════════════════════════════════════════════════════════
# LMS EXPORT — JSON (Canvas/Generic)
# ═══════════════════════════════════════════════════════════════════════════════
def export_json(quiz: dict[str, Any], output: Path) -> None:
    """Export quiz to JSON format for Canvas or generic LMS import."""
    data = {
        'metadata': quiz['metadata'],
        'questions': quiz['questions'],
        'exported': datetime.now().isoformat(),
        'format_version': '1.0'
    }
    output.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding='utf-8'
    )
    print(f"{Colours.GREEN}✓ Exported to JSON: {output}{Colours.END}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main(argv: list[str] | None = None) -> int:
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Formative quiz runner with LMS export",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--quiz', type=Path, default=QUIZ_FILE,
                        help="Path to quiz YAML file")
    parser.add_argument('--random', action='store_true',
                        help="Randomise question order")
    parser.add_argument('--limit', type=int,
                        help="Limit number of questions")
    parser.add_argument('--validate', action='store_true',
                        help="Validate quiz structure only")
    parser.add_argument('--export-lms', choices=['moodle', 'canvas', 'json'],
                        help="Export to LMS format")
    args = parser.parse_args(argv)
    
    quiz = load_quiz(args.quiz)
    
    if args.validate:
        errors = validate_quiz(quiz)
        if errors:
            print(f"{Colours.RED}Validation errors:{Colours.END}")
            for err in errors:
                print(f"  • {err}")
            return 1
        print(f"{Colours.GREEN}✓ Quiz structure is valid{Colours.END}")
        print(f"  Questions: {len(quiz['questions'])}")
        return 0
    
    if args.export_lms:
        out_dir = args.quiz.parent
        if args.export_lms == 'moodle':
            export_moodle(quiz, out_dir / 'quiz_moodle.gift')
        elif args.export_lms in ('json', 'canvas'):
            export_json(quiz, out_dir / f'quiz_lms_export.json')
        return 0
    
    results = run_quiz(quiz, args.random, args.limit)
    passing = results['correct'] / results['total'] >= 0.7
    return 0 if passing else 1


if __name__ == "__main__":
    sys.exit(main())
