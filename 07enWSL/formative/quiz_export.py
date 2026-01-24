#!/usr/bin/env python3
"""
Quiz Export Utility — Week 7
============================
NETWORKING class - ASE, Informatics | Computer Networks Laboratory

Exports the formative quiz to various Learning Management System formats
including Moodle XML, Canvas JSON and generic JSON for API integration.

Usage:
    python3 formative/quiz_export.py --format moodle --output quiz_moodle.xml
    python3 formative/quiz_export.py --format canvas --output quiz_canvas.json
    python3 formative/quiz_export.py --format json --output quiz_api.json
    python3 formative/quiz_export.py --format all --output-dir exports/

Supported Formats:
    - moodle: Moodle XML import format (GIFT-compatible)
    - canvas: Canvas LMS JSON format (QTI-compatible)
    - json: Generic JSON for custom LMS integration
    - all: Export to all formats

Requirements:
    pip install pyyaml
"""

from __future__ import annotations

import argparse
import html
import json
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from xml.dom import minidom

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(2)


# ═══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ExportedQuestion:
    """Normalised question format for export."""
    id: str
    type: str
    stem: str
    points: int
    correct_answer: Any
    options: Optional[dict[str, str]] = None
    explanation: str = ""
    lo_ref: str = ""
    difficulty: str = ""
    feedback_correct: str = ""
    feedback_incorrect: str = ""
    acceptable_variants: list[Any] = field(default_factory=list)


@dataclass
class ExportedQuiz:
    """Normalised quiz format for export."""
    title: str
    description: str
    time_limit: int
    passing_score: int
    questions: list[ExportedQuestion]
    metadata: dict[str, Any] = field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ LOADER
# ═══════════════════════════════════════════════════════════════════════════════

def load_quiz(path: Path) -> dict[str, Any]:
    """Load quiz from YAML file."""
    if not path.exists():
        raise FileNotFoundError(f"Quiz file not found: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def normalise_quiz(raw_quiz: dict[str, Any]) -> ExportedQuiz:
    """Convert raw YAML quiz to normalised export format."""
    metadata = raw_quiz.get("metadata", {})
    questions = []
    
    for q in raw_quiz.get("questions", []):
        lms_feedback = q.get("lms_feedback", {})
        
        # Handle different question types
        if q["type"] == "multiple_choice":
            correct_answer = q.get("correct", "")
        elif q["type"] == "fill_blank":
            correct_answer = q.get("correct", [])
        elif q["type"] == "ordering":
            correct_answer = q.get("correct_order", [])
        elif q["type"] == "true_false":
            correct_answer = q.get("correct", True)
        else:
            correct_answer = q.get("correct", "")
        
        exported = ExportedQuestion(
            id=q.get("id", ""),
            type=q.get("type", "multiple_choice"),
            stem=q.get("stem", ""),
            points=q.get("points", 1),
            correct_answer=correct_answer,
            options=q.get("options"),
            explanation=q.get("explanation", "").strip(),
            lo_ref=q.get("lo_ref", ""),
            difficulty=q.get("difficulty", ""),
            feedback_correct=lms_feedback.get("correct", "Correct!"),
            feedback_incorrect=lms_feedback.get("incorrect", "Incorrect."),
            acceptable_variants=q.get("acceptable_variants", []),
        )
        questions.append(exported)
    
    return ExportedQuiz(
        title=f"Week {metadata.get('week', '?')}: {metadata.get('topic', 'Quiz')}",
        description=f"Formative assessment for {metadata.get('topic', 'networking concepts')}",
        time_limit=metadata.get("estimated_time", "15 minutes").replace(" minutes", ""),
        passing_score=metadata.get("passing_score", 70),
        questions=questions,
        metadata=metadata,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# MOODLE XML EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

def export_moodle_xml(quiz: ExportedQuiz, output_path: Path) -> None:
    """
    Export quiz to Moodle XML format.
    
    This format can be imported directly into Moodle via:
    Site Administration > Question Bank > Import
    
    Args:
        quiz: Normalised quiz data
        output_path: Path to write XML file
    """
    root = ET.Element("quiz")
    
    # Add category question (Moodle convention)
    category = ET.SubElement(root, "question", type="category")
    cat_text = ET.SubElement(category, "category")
    cat_text_content = ET.SubElement(cat_text, "text")
    cat_text_content.text = f"$course$/Week 7 - Packet Filtering"
    
    for q in quiz.questions:
        if q.type == "multiple_choice":
            _add_moodle_multichoice(root, q)
        elif q.type == "fill_blank":
            _add_moodle_shortanswer(root, q)
        elif q.type == "ordering":
            _add_moodle_ordering(root, q)
        elif q.type == "true_false":
            _add_moodle_truefalse(root, q)
    
    # Pretty print XML
    xml_str = ET.tostring(root, encoding="unicode")
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="  ", encoding="UTF-8")
    
    with open(output_path, "wb") as f:
        f.write(pretty_xml)


def _add_moodle_multichoice(root: ET.Element, q: ExportedQuestion) -> None:
    """Add a multiple choice question to Moodle XML."""
    question = ET.SubElement(root, "question", type="multichoice")
    
    # Name
    name = ET.SubElement(question, "name")
    name_text = ET.SubElement(name, "text")
    name_text.text = f"{q.id}: {q.stem[:50]}..."
    
    # Question text
    qtext = ET.SubElement(question, "questiontext", format="html")
    qtext_text = ET.SubElement(qtext, "text")
    qtext_text.text = f"<![CDATA[<p>{html.escape(q.stem)}</p>]]>"
    
    # General feedback
    feedback = ET.SubElement(question, "generalfeedback", format="html")
    feedback_text = ET.SubElement(feedback, "text")
    feedback_text.text = f"<![CDATA[<p>{html.escape(q.explanation)}</p>]]>"
    
    # Default grade
    grade = ET.SubElement(question, "defaultgrade")
    grade.text = str(q.points)
    
    # Penalty
    penalty = ET.SubElement(question, "penalty")
    penalty.text = "0.3333333"
    
    # Single answer
    single = ET.SubElement(question, "single")
    single.text = "true"
    
    # Shuffle answers
    shuffle = ET.SubElement(question, "shuffleanswers")
    shuffle.text = "true"
    
    # Answer numbering
    numbering = ET.SubElement(question, "answernumbering")
    numbering.text = "abc"
    
    # Answers
    if q.options:
        for key, text in q.options.items():
            fraction = "100" if key == q.correct_answer else "0"
            answer = ET.SubElement(question, "answer", fraction=fraction, format="html")
            answer_text = ET.SubElement(answer, "text")
            answer_text.text = f"<![CDATA[<p>{html.escape(text)}</p>]]>"
            
            # Feedback per answer
            ans_feedback = ET.SubElement(answer, "feedback", format="html")
            ans_feedback_text = ET.SubElement(ans_feedback, "text")
            if key == q.correct_answer:
                ans_feedback_text.text = f"<![CDATA[<p>{html.escape(q.feedback_correct)}</p>]]>"
            else:
                ans_feedback_text.text = f"<![CDATA[<p>{html.escape(q.feedback_incorrect)}</p>]]>"
    
    # Tags (LO reference)
    if q.lo_ref:
        tags = ET.SubElement(question, "tags")
        tag = ET.SubElement(tags, "tag")
        tag_text = ET.SubElement(tag, "text")
        tag_text.text = q.lo_ref


def _add_moodle_shortanswer(root: ET.Element, q: ExportedQuestion) -> None:
    """Add a short answer (fill blank) question to Moodle XML."""
    question = ET.SubElement(root, "question", type="shortanswer")
    
    name = ET.SubElement(question, "name")
    name_text = ET.SubElement(name, "text")
    name_text.text = f"{q.id}: Fill in the blank"
    
    qtext = ET.SubElement(question, "questiontext", format="html")
    qtext_text = ET.SubElement(qtext, "text")
    # Convert template to Moodle format
    stem_html = html.escape(q.stem)
    if hasattr(q, "template") and q.template:
        stem_html += f"<br/><code>{html.escape(q.template)}</code>"
    qtext_text.text = f"<![CDATA[<p>{stem_html}</p>]]>"
    
    grade = ET.SubElement(question, "defaultgrade")
    grade.text = str(q.points)
    
    # Add correct answers
    if isinstance(q.correct_answer, list):
        for i, ans in enumerate(q.correct_answer):
            answer = ET.SubElement(question, "answer", fraction="100" if i == 0 else "100", format="moodle_auto_format")
            answer_text = ET.SubElement(answer, "text")
            answer_text.text = str(ans)
    
    # Add acceptable variants
    for variant in q.acceptable_variants:
        if isinstance(variant, list):
            for v in variant:
                answer = ET.SubElement(question, "answer", fraction="100", format="moodle_auto_format")
                answer_text = ET.SubElement(answer, "text")
                answer_text.text = str(v)


def _add_moodle_ordering(root: ET.Element, q: ExportedQuestion) -> None:
    """Add an ordering question to Moodle XML (as description with manual grading)."""
    question = ET.SubElement(root, "question", type="description")
    
    name = ET.SubElement(question, "name")
    name_text = ET.SubElement(name, "text")
    name_text.text = f"{q.id}: Ordering"
    
    # Build ordering question text
    items_html = "<ol>"
    if q.options:
        for item_id, item_text in q.options.items():
            items_html += f"<li>[{item_id}] {html.escape(item_text)}</li>"
    items_html += "</ol>"
    
    qtext = ET.SubElement(question, "questiontext", format="html")
    qtext_text = ET.SubElement(qtext, "text")
    qtext_text.text = f"<![CDATA[<p>{html.escape(q.stem)}</p>{items_html}<p><em>Correct order: {q.correct_answer}</em></p>]]>"


def _add_moodle_truefalse(root: ET.Element, q: ExportedQuestion) -> None:
    """Add a true/false question to Moodle XML."""
    question = ET.SubElement(root, "question", type="truefalse")
    
    name = ET.SubElement(question, "name")
    name_text = ET.SubElement(name, "text")
    name_text.text = f"{q.id}: True/False"
    
    qtext = ET.SubElement(question, "questiontext", format="html")
    qtext_text = ET.SubElement(qtext, "text")
    qtext_text.text = f"<![CDATA[<p>{html.escape(q.stem)}</p>]]>"
    
    grade = ET.SubElement(question, "defaultgrade")
    grade.text = str(q.points)
    
    # True answer
    true_frac = "100" if q.correct_answer else "0"
    true_ans = ET.SubElement(question, "answer", fraction=true_frac, format="moodle_auto_format")
    true_text = ET.SubElement(true_ans, "text")
    true_text.text = "true"
    
    # False answer
    false_frac = "0" if q.correct_answer else "100"
    false_ans = ET.SubElement(question, "answer", fraction=false_frac, format="moodle_auto_format")
    false_text = ET.SubElement(false_ans, "text")
    false_text.text = "false"


# ═══════════════════════════════════════════════════════════════════════════════
# CANVAS JSON EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

def export_canvas_json(quiz: ExportedQuiz, output_path: Path) -> None:
    """
    Export quiz to Canvas LMS JSON format.
    
    This format can be used with Canvas API or imported via QTI conversion.
    
    Args:
        quiz: Normalised quiz data
        output_path: Path to write JSON file
    """
    canvas_quiz = {
        "quiz": {
            "title": quiz.title,
            "description": f"<p>{quiz.description}</p>",
            "quiz_type": "practice_quiz",
            "time_limit": int(quiz.time_limit) if quiz.time_limit.isdigit() else 15,
            "shuffle_answers": True,
            "hide_results": None,
            "show_correct_answers": True,
            "show_correct_answers_last_attempt": True,
            "allowed_attempts": 3,
            "scoring_policy": "keep_highest",
            "one_question_at_a_time": False,
            "cant_go_back": False,
            "access_code": None,
            "ip_filter": None,
            "due_at": None,
            "lock_at": None,
            "unlock_at": None,
            "published": False,
            "one_time_results": False,
            "only_visible_to_overrides": False,
        },
        "questions": []
    }
    
    for q in quiz.questions:
        canvas_q = _convert_to_canvas_question(q)
        if canvas_q:
            canvas_quiz["questions"].append(canvas_q)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(canvas_quiz, f, indent=2, ensure_ascii=False)


def _convert_to_canvas_question(q: ExportedQuestion) -> Optional[dict[str, Any]]:
    """Convert a question to Canvas format."""
    base = {
        "question_name": q.id,
        "question_text": f"<p>{q.stem}</p>",
        "points_possible": q.points,
        "question_type": "",
        "answers": [],
        "neutral_comments_html": f"<p>{q.explanation}</p>" if q.explanation else "",
    }
    
    if q.type == "multiple_choice":
        base["question_type"] = "multiple_choice_question"
        if q.options:
            for key, text in q.options.items():
                base["answers"].append({
                    "answer_text": text,
                    "answer_weight": 100 if key == q.correct_answer else 0,
                    "answer_comments_html": q.feedback_correct if key == q.correct_answer else q.feedback_incorrect,
                })
    
    elif q.type == "fill_blank":
        base["question_type"] = "short_answer_question"
        if isinstance(q.correct_answer, list):
            for ans in q.correct_answer:
                base["answers"].append({
                    "answer_text": str(ans),
                    "answer_weight": 100,
                })
    
    elif q.type == "true_false":
        base["question_type"] = "true_false_question"
        base["answers"] = [
            {"answer_text": "True", "answer_weight": 100 if q.correct_answer else 0},
            {"answer_text": "False", "answer_weight": 0 if q.correct_answer else 100},
        ]
    
    elif q.type == "ordering":
        # Canvas doesn't have native ordering - convert to essay
        base["question_type"] = "essay_question"
        base["question_text"] += f"<p><em>Arrange in correct order: {q.correct_answer}</em></p>"
        base["answers"] = []
    
    else:
        return None
    
    return base


# ═══════════════════════════════════════════════════════════════════════════════
# GENERIC JSON EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

def export_generic_json(quiz: ExportedQuiz, output_path: Path) -> None:
    """
    Export quiz to generic JSON format for API integration.
    
    This format is suitable for custom LMS integration or programmatic access.
    
    Args:
        quiz: Normalised quiz data
        output_path: Path to write JSON file
    """
    export_data = {
        "export_metadata": {
            "format": "generic_json",
            "version": "1.0",
            "exported_at": datetime.now().isoformat(),
            "source": "Week 7 Formative Quiz",
        },
        "quiz": {
            "title": quiz.title,
            "description": quiz.description,
            "time_limit_minutes": int(quiz.time_limit) if str(quiz.time_limit).isdigit() else 15,
            "passing_score_percent": quiz.passing_score,
            "total_questions": len(quiz.questions),
            "total_points": sum(q.points for q in quiz.questions),
            "metadata": quiz.metadata,
        },
        "questions": []
    }
    
    for q in quiz.questions:
        q_data = {
            "id": q.id,
            "type": q.type,
            "stem": q.stem,
            "points": q.points,
            "learning_objective": q.lo_ref,
            "difficulty": q.difficulty,
            "correct_answer": q.correct_answer,
            "explanation": q.explanation,
            "feedback": {
                "correct": q.feedback_correct,
                "incorrect": q.feedback_incorrect,
            },
        }
        
        if q.options:
            q_data["options"] = q.options
        
        if q.acceptable_variants:
            q_data["acceptable_variants"] = q.acceptable_variants
        
        export_data["questions"].append(q_data)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def build_parser() -> argparse.ArgumentParser:
    """Build command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Export formative quiz to LMS formats",
        epilog="Supported formats: moodle, canvas, json, all"
    )
    
    parser.add_argument(
        "--quiz", "-q",
        type=Path,
        default=Path(__file__).parent / "quiz.yaml",
        help="Path to quiz YAML file (default: formative/quiz.yaml)"
    )
    
    parser.add_argument(
        "--format", "-f",
        choices=["moodle", "canvas", "json", "all"],
        default="json",
        help="Export format (default: json)"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output file path (auto-generated if not specified)"
    )
    
    parser.add_argument(
        "--output-dir", "-d",
        type=Path,
        default=Path("."),
        help="Output directory for 'all' format (default: current directory)"
    )
    
    return parser


def main() -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args()
    
    try:
        raw_quiz = load_quiz(args.quiz)
        quiz = normalise_quiz(raw_quiz)
    except Exception as e:
        print(f"Error loading quiz: {e}")
        return 2
    
    print(f"Loaded quiz: {quiz.title}")
    print(f"Questions: {len(quiz.questions)}")
    print()
    
    if args.format == "all":
        args.output_dir.mkdir(parents=True, exist_ok=True)
        
        moodle_path = args.output_dir / "quiz_moodle.xml"
        export_moodle_xml(quiz, moodle_path)
        print(f"Exported Moodle XML: {moodle_path}")
        
        canvas_path = args.output_dir / "quiz_canvas.json"
        export_canvas_json(quiz, canvas_path)
        print(f"Exported Canvas JSON: {canvas_path}")
        
        json_path = args.output_dir / "quiz_api.json"
        export_generic_json(quiz, json_path)
        print(f"Exported Generic JSON: {json_path}")
        
    else:
        if args.output:
            output_path = args.output
        else:
            ext = "xml" if args.format == "moodle" else "json"
            output_path = Path(f"quiz_{args.format}.{ext}")
        
        if args.format == "moodle":
            export_moodle_xml(quiz, output_path)
        elif args.format == "canvas":
            export_canvas_json(quiz, output_path)
        else:
            export_generic_json(quiz, output_path)
        
        print(f"Exported to: {output_path}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
