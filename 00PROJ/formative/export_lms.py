#!/usr/bin/env python3
"""
LMS Export Tool — Convert YAML Quizzes to Moodle/Canvas Format.

Exports formative quizzes to LMS-compatible formats:
- Moodle XML (GIFT format)
- Canvas QTI (IMS Question and Test Interoperability)
- Generic JSON (for custom LMS integration)

Usage:
    python export_lms.py quiz_p01.yaml --format moodle
    python export_lms.py quiz_p01.yaml --format canvas
    python export_lms.py quiz_p01.yaml --format json
    python export_lms.py --all --format moodle

Author: Computer Networks Course Team
Institution: ASE Bucharest - CSIE
Version: 1.0
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from xml.etree import ElementTree as ET

try:
    import yaml
except ImportError:
    print("❌ PyYAML required. Install with: pip install pyyaml")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
VERSION = "1.0.0"
QUIZ_DIR = Path(__file__).parent
EXPORTS_DIR = QUIZ_DIR / "exports"

SUPPORTED_FORMATS = ["moodle", "canvas", "json"]


# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def load_quiz(path: Path) -> Optional[Dict[str, Any]]:
    """Load quiz data from YAML file."""
    if not path.exists():
        if not path.suffix:
            path = path.with_suffix(".yaml")
        if not path.exists():
            return None
    
    try:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"❌ YAML parsing error: {e}")
        return None


def escape_html(text: str) -> str:
    """Escape HTML special characters."""
    return html.escape(str(text))


def clean_text(text: str) -> str:
    """Clean and normalise text for export."""
    # Remove leading/trailing whitespace from each line
    lines = [line.strip() for line in text.strip().split("\n")]
    return "\n".join(lines)


def generate_uuid() -> str:
    """Generate a unique identifier."""
    return str(uuid.uuid4())


# ═══════════════════════════════════════════════════════════════════════════════
# MOODLE XML EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
def export_moodle_xml(quiz_data: Dict, output_path: Path) -> None:
    """
    Export quiz to Moodle XML format.
    
    Args:
        quiz_data: Quiz dictionary from YAML
        output_path: Path for output XML file
    """
    project = quiz_data.get("project", {})
    metadata = quiz_data.get("metadata", {})
    questions = project.get("questions", [])
    lms_config = quiz_data.get("lms_export", {}).get("moodle", {})
    
    # Create XML structure
    quiz = ET.Element("quiz")
    
    # Add category
    category_text = lms_config.get(
        "category", 
        f"$course$/Computer Networks/{project.get('id', 'Quiz')}"
    )
    
    category_q = ET.SubElement(quiz, "question")
    category_q.set("type", "category")
    category = ET.SubElement(category_q, "category")
    category_text_elem = ET.SubElement(category, "text")
    category_text_elem.text = category_text
    
    # Export each question
    for i, q in enumerate(questions, 1):
        q_type = q.get("type", "multiple_choice")
        
        if q_type in ["multiple_choice", "scenario", "code_trace"]:
            export_moodle_multichoice(quiz, q, i)
        elif q_type == "multiple_select":
            export_moodle_multiselect(quiz, q, i)
        elif q_type == "fill_blank":
            export_moodle_shortanswer(quiz, q, i)
        elif q_type == "ordering":
            export_moodle_ordering(quiz, q, i)
        elif q_type == "matching":
            export_moodle_matching(quiz, q, i)
    
    # Write XML file
    tree = ET.ElementTree(quiz)
    ET.indent(tree, space="  ")
    
    with open(output_path, "wb") as f:
        tree.write(f, encoding="UTF-8", xml_declaration=True)
    
    print(f"✅ Moodle XML exported: {output_path}")
    print(f"   Questions: {len(questions)}")


def export_moodle_multichoice(parent: ET.Element, q: Dict, index: int) -> None:
    """Export multiple choice question to Moodle format."""
    question = ET.SubElement(parent, "question")
    question.set("type", "multichoice")
    
    # Name
    name = ET.SubElement(question, "name")
    name_text = ET.SubElement(name, "text")
    name_text.text = f"{q.get('lo_ref', 'Q')}-{index}: {q.get('id', f'q{index}')}"
    
    # Question text
    qtext = ET.SubElement(question, "questiontext")
    qtext.set("format", "html")
    qtext_text = ET.SubElement(qtext, "text")
    qtext_text.text = f"<![CDATA[<p>{escape_html(clean_text(q['stem']))}</p>]]>"
    
    # General feedback
    if "explanation" in q:
        gfeedback = ET.SubElement(question, "generalfeedback")
        gfeedback.set("format", "html")
        gf_text = ET.SubElement(gfeedback, "text")
        gf_text.text = f"<![CDATA[<p>{escape_html(q['explanation'])}</p>]]>"
    
    # Default grade
    defaultgrade = ET.SubElement(question, "defaultgrade")
    defaultgrade.text = str(q.get("points", 1))
    
    # Penalty
    penalty = ET.SubElement(question, "penalty")
    penalty.text = "0.3333333"
    
    # Single answer
    single = ET.SubElement(question, "single")
    single.text = "true"
    
    # Shuffle answers
    shuffleanswers = ET.SubElement(question, "shuffleanswers")
    shuffleanswers.text = "true"
    
    # Answers
    options = q.get("options", {})
    correct_key = q.get("correct", "")
    feedback = q.get("feedback", {})
    
    for key, value in options.items():
        answer = ET.SubElement(question, "answer")
        answer.set("fraction", "100" if key == correct_key else "0")
        answer.set("format", "html")
        
        ans_text = ET.SubElement(answer, "text")
        ans_text.text = f"<![CDATA[<p>{escape_html(value)}</p>]]>"
        
        # Answer feedback
        ans_feedback = ET.SubElement(answer, "feedback")
        ans_feedback.set("format", "html")
        fb_text = ET.SubElement(ans_feedback, "text")
        if key == correct_key:
            fb_text.text = f"<![CDATA[<p>{escape_html(feedback.get('correct', 'Correct!'))}</p>]]>"
        else:
            fb_text.text = f"<![CDATA[<p>{escape_html(feedback.get('incorrect', 'Incorrect.'))}</p>]]>"


def export_moodle_multiselect(parent: ET.Element, q: Dict, index: int) -> None:
    """Export multiple select question to Moodle format."""
    question = ET.SubElement(parent, "question")
    question.set("type", "multichoice")
    
    # Name
    name = ET.SubElement(question, "name")
    name_text = ET.SubElement(name, "text")
    name_text.text = f"{q.get('lo_ref', 'Q')}-{index}: {q.get('id', f'q{index}')}"
    
    # Question text
    qtext = ET.SubElement(question, "questiontext")
    qtext.set("format", "html")
    qtext_text = ET.SubElement(qtext, "text")
    qtext_text.text = f"<![CDATA[<p>{escape_html(clean_text(q['stem']))}</p>]]>"
    
    # Multiple answers allowed
    single = ET.SubElement(question, "single")
    single.text = "false"
    
    # Answers with partial credit
    options = q.get("options", {})
    correct_keys = set(q.get("correct", []))
    num_correct = len(correct_keys)
    
    for key, value in options.items():
        answer = ET.SubElement(question, "answer")
        if key in correct_keys:
            fraction = 100 / num_correct
        else:
            fraction = -50  # Penalty for wrong selection
        answer.set("fraction", str(fraction))
        answer.set("format", "html")
        
        ans_text = ET.SubElement(answer, "text")
        ans_text.text = f"<![CDATA[<p>{escape_html(value)}</p>]]>"


def export_moodle_shortanswer(parent: ET.Element, q: Dict, index: int) -> None:
    """Export fill-in-blank question to Moodle short answer format."""
    question = ET.SubElement(parent, "question")
    question.set("type", "shortanswer")
    
    # Name
    name = ET.SubElement(question, "name")
    name_text = ET.SubElement(name, "text")
    name_text.text = f"{q.get('lo_ref', 'Q')}-{index}: {q.get('id', f'q{index}')}"
    
    # Question text
    qtext = ET.SubElement(question, "questiontext")
    qtext.set("format", "html")
    qtext_text = ET.SubElement(qtext, "text")
    qtext_text.text = f"<![CDATA[<p>{escape_html(clean_text(q['stem']))}</p>]]>"
    
    # Case sensitivity
    usecase = ET.SubElement(question, "usecase")
    usecase.text = "0"  # Case insensitive
    
    # Accepted answers
    correct_answers = q.get("correct", [])
    if isinstance(correct_answers, str):
        correct_answers = [correct_answers]
    
    for correct in correct_answers:
        answer = ET.SubElement(question, "answer")
        answer.set("fraction", "100")
        answer.set("format", "plain_text")
        
        ans_text = ET.SubElement(answer, "text")
        ans_text.text = correct


def export_moodle_ordering(parent: ET.Element, q: Dict, index: int) -> None:
    """Export ordering question (as description with manual grading note)."""
    # Moodle doesn't have native ordering - export as description
    question = ET.SubElement(parent, "question")
    question.set("type", "essay")
    
    name = ET.SubElement(question, "name")
    name_text = ET.SubElement(name, "text")
    name_text.text = f"{q.get('lo_ref', 'Q')}-{index}: Ordering"
    
    qtext = ET.SubElement(question, "questiontext")
    qtext.set("format", "html")
    
    # Build question with items
    items_html = "<ol>"
    for item in q.get("items", []):
        items_html += f"<li>{escape_html(item['text'])}</li>"
    items_html += "</ol>"
    
    qtext_text = ET.SubElement(qtext, "text")
    qtext_text.text = f"<![CDATA[<p>{escape_html(clean_text(q['stem']))}</p>{items_html}<p><em>Enter the correct order (e.g., 3,1,2,4,5)</em></p>]]>"


def export_moodle_matching(parent: ET.Element, q: Dict, index: int) -> None:
    """Export matching question to Moodle format."""
    question = ET.SubElement(parent, "question")
    question.set("type", "matching")
    
    name = ET.SubElement(question, "name")
    name_text = ET.SubElement(name, "text")
    name_text.text = f"{q.get('lo_ref', 'Q')}-{index}: Matching"
    
    qtext = ET.SubElement(question, "questiontext")
    qtext.set("format", "html")
    qtext_text = ET.SubElement(qtext, "text")
    qtext_text.text = f"<![CDATA[<p>{escape_html(clean_text(q['stem']))}</p>]]>"
    
    # Subquestions (pairs)
    for pair in q.get("pairs", []):
        subq = ET.SubElement(question, "subquestion")
        subq.set("format", "html")
        
        subq_text = ET.SubElement(subq, "text")
        subq_text.text = f"<![CDATA[<p>{escape_html(pair['left'])}</p>]]>"
        
        subq_answer = ET.SubElement(subq, "answer")
        ans_text = ET.SubElement(subq_answer, "text")
        ans_text.text = pair["right"]


# ═══════════════════════════════════════════════════════════════════════════════
# CANVAS QTI EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
def export_canvas_qti(quiz_data: Dict, output_path: Path) -> None:
    """
    Export quiz to Canvas QTI format.
    
    Args:
        quiz_data: Quiz dictionary from YAML
        output_path: Path for output XML file
    """
    project = quiz_data.get("project", {})
    questions = project.get("questions", [])
    
    # QTI namespace
    ns = {
        "": "http://www.imsglobal.org/xsd/ims_qtiasiv1p2",
    }
    
    # Create assessment
    assessment = ET.Element("questestinterop")
    assessment.set("xmlns", ns[""])
    
    assess = ET.SubElement(assessment, "assessment")
    assess.set("ident", generate_uuid())
    assess.set("title", project.get("title", "Quiz"))
    
    # Assessment metadata
    qtimetadata = ET.SubElement(assess, "qtimetadata")
    
    # Add sections
    section = ET.SubElement(assess, "section")
    section.set("ident", "root_section")
    
    for i, q in enumerate(questions, 1):
        q_type = q.get("type", "multiple_choice")
        
        if q_type in ["multiple_choice", "scenario", "code_trace"]:
            export_qti_multichoice(section, q, i)
        elif q_type == "fill_blank":
            export_qti_shortanswer(section, q, i)
    
    # Write XML
    tree = ET.ElementTree(assessment)
    ET.indent(tree, space="  ")
    
    with open(output_path, "wb") as f:
        tree.write(f, encoding="UTF-8", xml_declaration=True)
    
    print(f"✅ Canvas QTI exported: {output_path}")
    print(f"   Questions: {len(questions)}")


def export_qti_multichoice(parent: ET.Element, q: Dict, index: int) -> None:
    """Export multiple choice to QTI format."""
    item = ET.SubElement(parent, "item")
    item.set("ident", q.get("id", f"q{index}"))
    item.set("title", f"Question {index}")
    
    # Item metadata
    itemmetadata = ET.SubElement(item, "itemmetadata")
    qtimetadata = ET.SubElement(itemmetadata, "qtimetadata")
    
    # Question type
    qtimetadatafield = ET.SubElement(qtimetadata, "qtimetadatafield")
    fieldlabel = ET.SubElement(qtimetadatafield, "fieldlabel")
    fieldlabel.text = "question_type"
    fieldentry = ET.SubElement(qtimetadatafield, "fieldentry")
    fieldentry.text = "multiple_choice_question"
    
    # Presentation
    presentation = ET.SubElement(item, "presentation")
    
    material = ET.SubElement(presentation, "material")
    mattext = ET.SubElement(material, "mattext")
    mattext.set("texttype", "text/html")
    mattext.text = clean_text(q["stem"])
    
    # Response
    response_lid = ET.SubElement(presentation, "response_lid")
    response_lid.set("ident", "response1")
    response_lid.set("rcardinality", "Single")
    
    render_choice = ET.SubElement(response_lid, "render_choice")
    
    options = q.get("options", {})
    for key, value in options.items():
        response_label = ET.SubElement(render_choice, "response_label")
        response_label.set("ident", key)
        
        material = ET.SubElement(response_label, "material")
        mattext = ET.SubElement(material, "mattext")
        mattext.set("texttype", "text/plain")
        mattext.text = value
    
    # Response processing
    resprocessing = ET.SubElement(item, "resprocessing")
    outcomes = ET.SubElement(resprocessing, "outcomes")
    decvar = ET.SubElement(outcomes, "decvar")
    decvar.set("maxvalue", str(q.get("points", 1)))
    decvar.set("minvalue", "0")
    decvar.set("varname", "SCORE")
    decvar.set("vartype", "Decimal")
    
    # Correct response
    respcondition = ET.SubElement(resprocessing, "respcondition")
    respcondition.set("continue", "No")
    
    conditionvar = ET.SubElement(respcondition, "conditionvar")
    varequal = ET.SubElement(conditionvar, "varequal")
    varequal.set("respident", "response1")
    varequal.text = q.get("correct", "")
    
    setvar = ET.SubElement(respcondition, "setvar")
    setvar.set("action", "Set")
    setvar.set("varname", "SCORE")
    setvar.text = str(q.get("points", 1))


def export_qti_shortanswer(parent: ET.Element, q: Dict, index: int) -> None:
    """Export short answer to QTI format."""
    item = ET.SubElement(parent, "item")
    item.set("ident", q.get("id", f"q{index}"))
    item.set("title", f"Question {index}")
    
    # Presentation
    presentation = ET.SubElement(item, "presentation")
    
    material = ET.SubElement(presentation, "material")
    mattext = ET.SubElement(material, "mattext")
    mattext.set("texttype", "text/html")
    mattext.text = clean_text(q["stem"])
    
    response_str = ET.SubElement(presentation, "response_str")
    response_str.set("ident", "response1")
    response_str.set("rcardinality", "Single")
    
    render_fib = ET.SubElement(response_str, "render_fib")
    response_label = ET.SubElement(render_fib, "response_label")
    response_label.set("ident", "answer1")


# ═══════════════════════════════════════════════════════════════════════════════
# JSON EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
def export_json(quiz_data: Dict, output_path: Path) -> None:
    """
    Export quiz to generic JSON format.
    
    Args:
        quiz_data: Quiz dictionary from YAML
        output_path: Path for output JSON file
    """
    project = quiz_data.get("project", {})
    metadata = quiz_data.get("metadata", {})
    questions = project.get("questions", [])
    
    # Build clean export structure
    export_data = {
        "metadata": {
            "format_version": "1.0",
            "exported_at": datetime.now().isoformat(),
            "source": "Computer Networks Quiz System",
            "course": metadata.get("course", "Computer Networks"),
            "institution": metadata.get("institution", "ASE Bucharest"),
        },
        "quiz": {
            "id": project.get("id", "unknown"),
            "title": project.get("title", "Quiz"),
            "description": project.get("description", ""),
            "passing_score": metadata.get("passing_score", 70),
            "time_limit_minutes": metadata.get("time_limit_minutes", 15),
            "shuffle_questions": metadata.get("shuffle_questions", True),
        },
        "learning_objectives": project.get("learning_objectives", []),
        "questions": [],
    }
    
    # Export questions
    for q in questions:
        q_export = {
            "id": q.get("id"),
            "type": q.get("type", "multiple_choice"),
            "lo_ref": q.get("lo_ref"),
            "bloom_level": q.get("bloom_level"),
            "difficulty": q.get("difficulty"),
            "points": q.get("points", 1),
            "stem": clean_text(q.get("stem", "")),
        }
        
        # Type-specific fields
        if q.get("options"):
            q_export["options"] = q["options"]
        if q.get("correct"):
            q_export["correct"] = q["correct"]
        if q.get("items"):
            q_export["items"] = q["items"]
        if q.get("pairs"):
            q_export["pairs"] = q["pairs"]
        if q.get("correct_order"):
            q_export["correct_order"] = q["correct_order"]
        
        # Feedback and explanation
        if q.get("feedback"):
            q_export["feedback"] = q["feedback"]
        if q.get("explanation"):
            q_export["explanation"] = q["explanation"]
        if q.get("hint"):
            q_export["hint"] = q["hint"]
        
        export_data["questions"].append(q_export)
    
    # Write JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ JSON exported: {output_path}")
    print(f"   Questions: {len(questions)}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Export YAML quizzes to LMS formats (Moodle/Canvas/JSON)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python export_lms.py quiz_p01.yaml --format moodle
    python export_lms.py quiz_p01.yaml --format canvas
    python export_lms.py quiz_p01.yaml --format json
    python export_lms.py --all --format moodle
        """,
    )
    
    parser.add_argument(
        "quiz",
        nargs="?",
        type=Path,
        help="Path to quiz YAML file",
    )
    
    parser.add_argument(
        "--format", "-f",
        choices=SUPPORTED_FORMATS,
        default="json",
        help="Export format (default: json)",
    )
    
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output file path (auto-generated if not specified)",
    )
    
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Export all quizzes in the formative directory",
    )
    
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"%(prog)s {VERSION}",
    )
    
    args = parser.parse_args()
    
    EXPORTS_DIR.mkdir(exist_ok=True)
    
    if args.all:
        quiz_files = list(QUIZ_DIR.glob("quiz_*.yaml"))
        if not quiz_files:
            print("❌ No quiz files found.")
            return 1
        
        for quiz_file in quiz_files:
            quiz_data = load_quiz(quiz_file)
            if quiz_data:
                output_name = quiz_file.stem
                if args.format == "moodle":
                    output_path = EXPORTS_DIR / f"{output_name}_moodle.xml"
                    export_moodle_xml(quiz_data, output_path)
                elif args.format == "canvas":
                    output_path = EXPORTS_DIR / f"{output_name}_canvas.xml"
                    export_canvas_qti(quiz_data, output_path)
                else:
                    output_path = EXPORTS_DIR / f"{output_name}.json"
                    export_json(quiz_data, output_path)
        
        return 0
    
    if not args.quiz:
        parser.print_help()
        return 1
    
    quiz_path = args.quiz
    if not quiz_path.is_absolute() and not quiz_path.exists():
        quiz_path = QUIZ_DIR / quiz_path
    
    quiz_data = load_quiz(quiz_path)
    if not quiz_data:
        print(f"❌ Could not load quiz: {quiz_path}")
        return 1
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        output_name = quiz_path.stem
        if args.format == "moodle":
            output_path = EXPORTS_DIR / f"{output_name}_moodle.xml"
        elif args.format == "canvas":
            output_path = EXPORTS_DIR / f"{output_name}_canvas.xml"
        else:
            output_path = EXPORTS_DIR / f"{output_name}.json"
    
    # Export
    if args.format == "moodle":
        export_moodle_xml(quiz_data, output_path)
    elif args.format == "canvas":
        export_canvas_qti(quiz_data, output_path)
    else:
        export_json(quiz_data, output_path)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
