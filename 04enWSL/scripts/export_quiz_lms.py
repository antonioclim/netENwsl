#!/usr/bin/env python3
"""
LMS Quiz Export Script — Week 4
================================

NETWORKING class - ASE, Informatics | Computer Networks Laboratory
by ing. dr. Antonio Clim

Exports formative/quiz.yaml to LMS-compatible JSON formats for
Moodle and Canvas import.

Usage:
    python scripts/export_quiz_lms.py --format moodle --output quiz_moodle.json
    python scripts/export_quiz_lms.py --format canvas --output quiz_canvas.json
    python scripts/export_quiz_lms.py --format all

Supported formats:
    - moodle: Moodle GIFT-compatible JSON structure
    - canvas: Canvas QTI-compatible JSON structure
    - all: Export both formats

Exit codes:
    0 - Export successful
    1 - Export failed
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

PROJECT_ROOT = Path(__file__).parent.parent
QUIZ_PATH = PROJECT_ROOT / "formative" / "quiz.yaml"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "formative" / "exports"


# ═══════════════════════════════════════════════════════════════════════════════
# YAML LOADING
# ═══════════════════════════════════════════════════════════════════════════════

def load_yaml(path: Path) -> Dict[str, Any]:
    """Load YAML file."""
    try:
        import yaml
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except ImportError:
        print("ERROR: PyYAML not installed. Run: pip install pyyaml")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Failed to load {path}: {e}")
        sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# MOODLE EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

def export_to_moodle(quiz: Dict[str, Any]) -> Dict[str, Any]:
    """
    Export quiz to Moodle-compatible JSON format.
    
    Moodle expects a structure compatible with GIFT import or
    Question Bank XML. This generates a JSON that can be converted.
    """
    metadata = quiz.get("metadata", {})
    questions = quiz.get("questions", [])
    
    moodle_quiz = {
        "quiz": {
            "name": f"Week {metadata.get('week', '?')}: {metadata.get('topic', 'Unknown')}",
            "intro": f"Formative assessment for Week {metadata.get('week', '?')}. "
                     f"Estimated time: {metadata.get('estimated_time', '15 minutes')}. "
                     f"Passing score: {metadata.get('passing_score', 70)}%.",
            "timeLimit": _parse_time_minutes(metadata.get("estimated_time", "15 minutes")),
            "passingGrade": metadata.get("passing_score", 70),
            "shuffleAnswers": True,
            "questions": []
        },
        "metadata": {
            "exportFormat": "moodle",
            "exportDate": datetime.now().isoformat(),
            "sourceFile": str(QUIZ_PATH),
            "version": metadata.get("version", "1.0"),
            "loMapping": metadata.get("lo_coverage", [])
        }
    }
    
    for q in questions:
        moodle_q = _convert_question_moodle(q)
        if moodle_q:
            moodle_quiz["quiz"]["questions"].append(moodle_q)
    
    return moodle_quiz


def _convert_question_moodle(q: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Convert a single question to Moodle format."""
    q_type = q.get("type", "")
    
    if q_type == "multiple_choice":
        return {
            "type": "multichoice",
            "name": q.get("id", ""),
            "questiontext": q.get("stem", ""),
            "generalfeedback": q.get("explanation", ""),
            "defaultgrade": 1.0,
            "penalty": 0.33,
            "single": True,
            "shuffleanswers": True,
            "answernumbering": "abc",
            "answers": _build_moodle_answers(q),
            "tags": [
                f"lo:{q.get('lo_ref', '')}",
                f"bloom:{q.get('bloom_level', '')}",
                f"difficulty:{q.get('difficulty', '')}"
            ]
        }
    
    elif q_type == "true_false":
        return {
            "type": "truefalse",
            "name": q.get("id", ""),
            "questiontext": q.get("stem", ""),
            "generalfeedback": q.get("explanation", ""),
            "defaultgrade": 1.0,
            "correctanswer": q.get("correct", False),
            "tags": [
                f"lo:{q.get('lo_ref', '')}",
                f"bloom:{q.get('bloom_level', '')}"
            ]
        }
    
    elif q_type == "fill_blank":
        return {
            "type": "shortanswer",
            "name": q.get("id", ""),
            "questiontext": q.get("stem", ""),
            "generalfeedback": q.get("explanation", ""),
            "defaultgrade": 1.0,
            "usecase": False,
            "answers": _build_moodle_shortanswer(q),
            "tags": [
                f"lo:{q.get('lo_ref', '')}",
                f"bloom:{q.get('bloom_level', '')}"
            ]
        }
    
    return None


def _build_moodle_answers(q: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build Moodle answer array for multiple choice."""
    answers = []
    options = q.get("options", {})
    correct = q.get("correct", "")
    
    for key, text in options.items():
        answers.append({
            "text": text,
            "fraction": 100 if key == correct else 0,
            "feedback": "Correct!" if key == correct else ""
        })
    
    return answers


def _build_moodle_shortanswer(q: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build Moodle answer array for short answer."""
    correct = q.get("correct", [])
    if isinstance(correct, str):
        correct = [correct]
    
    return [{"text": ans, "fraction": 100} for ans in correct]


# ═══════════════════════════════════════════════════════════════════════════════
# CANVAS EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

def export_to_canvas(quiz: Dict[str, Any]) -> Dict[str, Any]:
    """
    Export quiz to Canvas-compatible JSON format.
    
    Canvas uses QTI (Question and Test Interoperability) format.
    This generates a JSON that can be converted to QTI.
    """
    metadata = quiz.get("metadata", {})
    questions = quiz.get("questions", [])
    
    canvas_quiz = {
        "quiz": {
            "title": f"Week {metadata.get('week', '?')}: {metadata.get('topic', 'Unknown')}",
            "description": f"<p>Formative assessment for Week {metadata.get('week', '?')}.</p>"
                          f"<p>Estimated time: {metadata.get('estimated_time', '15 minutes')}</p>",
            "quiz_type": "practice_quiz",
            "time_limit": _parse_time_minutes(metadata.get("estimated_time", "15 minutes")),
            "shuffle_answers": True,
            "scoring_policy": "keep_highest",
            "allowed_attempts": -1,  # Unlimited for formative
            "one_question_at_a_time": False,
            "show_correct_answers": True,
            "show_correct_answers_last_attempt": True,
            "questions": []
        },
        "metadata": {
            "exportFormat": "canvas",
            "exportDate": datetime.now().isoformat(),
            "sourceFile": str(QUIZ_PATH),
            "version": metadata.get("version", "1.0"),
            "loMapping": metadata.get("lo_coverage", [])
        }
    }
    
    for i, q in enumerate(questions):
        canvas_q = _convert_question_canvas(q, i + 1)
        if canvas_q:
            canvas_quiz["quiz"]["questions"].append(canvas_q)
    
    return canvas_quiz


def _convert_question_canvas(q: Dict[str, Any], position: int) -> Optional[Dict[str, Any]]:
    """Convert a single question to Canvas format."""
    q_type = q.get("type", "")
    
    base = {
        "question_name": q.get("id", f"q{position:02d}"),
        "position": position,
        "points_possible": 1.0,
        "question_text": f"<p>{q.get('stem', '')}</p>",
        "neutral_comments_html": f"<p>{q.get('explanation', '')}</p>",
        "tags": {
            "learning_objective": q.get("lo_ref", ""),
            "bloom_level": q.get("bloom_level", ""),
            "difficulty": q.get("difficulty", "")
        }
    }
    
    if q_type == "multiple_choice":
        base["question_type"] = "multiple_choice_question"
        base["answers"] = _build_canvas_answers(q)
        return base
    
    elif q_type == "true_false":
        base["question_type"] = "true_false_question"
        base["answers"] = [
            {"text": "True", "weight": 100 if q.get("correct") else 0},
            {"text": "False", "weight": 0 if q.get("correct") else 100}
        ]
        return base
    
    elif q_type == "fill_blank":
        base["question_type"] = "short_answer_question"
        base["answers"] = _build_canvas_shortanswer(q)
        return base
    
    return None


def _build_canvas_answers(q: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build Canvas answer array for multiple choice."""
    answers = []
    options = q.get("options", {})
    correct = q.get("correct", "")
    
    for key, text in options.items():
        answers.append({
            "text": text,
            "weight": 100 if key == correct else 0,
            "comments_html": "<p>Correct!</p>" if key == correct else ""
        })
    
    return answers


def _build_canvas_shortanswer(q: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build Canvas answer array for short answer."""
    correct = q.get("correct", [])
    if isinstance(correct, str):
        correct = [correct]
    
    return [{"text": ans, "weight": 100} for ans in correct]


# ═══════════════════════════════════════════════════════════════════════════════
# UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

def _parse_time_minutes(time_str: str) -> int:
    """Parse time string like '15 minutes' to integer minutes."""
    try:
        parts = time_str.lower().replace("minutes", "").replace("minute", "").strip()
        return int(parts)
    except (ValueError, AttributeError):
        return 15


def save_json(data: Dict[str, Any], path: Path) -> None:
    """Save data as formatted JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════════════════════════


def validate_export(data: Dict[str, Any], format_type: str) -> tuple:
    """
    Validate exported quiz data for LMS compatibility.
    
    Args:
        data: Exported quiz data
        format_type: 'moodle' or 'canvas'
    
    Returns:
        Tuple of (is_valid: bool, errors: list)
    """
    errors = []
    
    # Check top-level structure
    if "quiz" not in data:
        errors.append("Missing 'quiz' key in export")
        return (False, errors)
    
    if "metadata" not in data:
        errors.append("Missing 'metadata' key in export")
    
    quiz = data["quiz"]
    
    # Check required quiz fields
    if format_type == "moodle":
        required = ["name", "questions"]
    else:
        required = ["title", "questions"]
    
    for field in required:
        if field not in quiz:
            errors.append(f"Missing required field: {field}")
    
    # Validate questions
    questions = quiz.get("questions", [])
    for i, q in enumerate(questions):
        if "type" not in q and "question_type" not in q:
            errors.append(f"Question {i}: missing type field")
        
        # Check for question text
        text_field = "questiontext" if format_type == "moodle" else "question_text"
        if text_field not in q:
            errors.append(f"Question {i}: missing {text_field}")
    
    return (len(errors) == 0, errors)

# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main export function."""
    parser = argparse.ArgumentParser(
        description="Export quiz.yaml to LMS-compatible JSON formats"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["moodle", "canvas", "all"],
        default="all",
        help="Export format (default: all)"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output file path (for single format) or directory (for all)"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress output messages"
    )
    
    args = parser.parse_args()
    
    # Load quiz
    if not QUIZ_PATH.exists():
        print(f"ERROR: Quiz file not found: {QUIZ_PATH}")
        return 1
    
    quiz = load_yaml(QUIZ_PATH)
    
    if not args.quiet:
        print("\n" + "─" * 60)
        print("  LMS Quiz Export")
        print("─" * 60)
        print(f"\n  Source: {QUIZ_PATH.name}")
        print(f"  Questions: {len(quiz.get('questions', []))}")
    
    # Determine output paths
    if args.format == "all":
        output_dir = args.output or DEFAULT_OUTPUT_DIR
        moodle_path = output_dir / "quiz_moodle.json"
        canvas_path = output_dir / "quiz_canvas.json"
        
        # Export both
        moodle_data = export_to_moodle(quiz)
        canvas_data = export_to_canvas(quiz)
        
        save_json(moodle_data, moodle_path)
        save_json(canvas_data, canvas_path)
        
        if not args.quiet:
            print(f"\n  ✓ Exported to Moodle: {moodle_path}")
            print(f"  ✓ Exported to Canvas: {canvas_path}")
    
    else:
        output_path = args.output or (DEFAULT_OUTPUT_DIR / f"quiz_{args.format}.json")
        
        if args.format == "moodle":
            data = export_to_moodle(quiz)
        else:
            data = export_to_canvas(quiz)
        
        save_json(data, output_path)
        
        if not args.quiet:
            print(f"\n  ✓ Exported to {args.format.title()}: {output_path}")
    
    if not args.quiet:
        print("\n" + "─" * 60)
        print("  Export complete")
        print("─" * 60 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
