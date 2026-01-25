#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_DOCSTRING
# ═══════════════════════════════════════════════════════════════════════════════
"""
LMS Quiz Export Tool — Week 12
==============================
Computer Networks - ASE, CSIE | by ing. dr. Antonio Clim

Exports formative quiz to LMS-compatible formats:
- Moodle XML (GIFT format)
- Canvas QTI
- Generic CSV

Usage:
    python formative/export_lms.py --format moodle --output quiz_moodle.xml
    python formative/export_lms.py --format canvas --output quiz_canvas.zip
    python formative/export_lms.py --format csv --output quiz.csv
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import json
import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path
from typing import Dict, Any, List
import html
import sys

SCRIPT_DIR = Path(__file__).parent
DEFAULT_QUIZ_PATH = SCRIPT_DIR / "quiz.json"


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_LOADING
# ═══════════════════════════════════════════════════════════════════════════════
def load_quiz(path: Path) -> Dict[str, Any]:
    """Load quiz from JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_quiz(quiz: Dict[str, Any]) -> List[str]:
    """Validate quiz structure and return list of errors."""
    errors = []
    if "metadata" not in quiz:
        errors.append("Missing 'metadata' section")
    else:
        for field in ["week", "topic"]:
            if field not in quiz["metadata"]:
                errors.append(f"Missing metadata field: {field}")
    
    if "questions" not in quiz:
        errors.append("Missing 'questions' section")
    else:
        for i, q in enumerate(quiz["questions"]):
            if "id" not in q:
                errors.append(f"Question {i}: missing 'id'")
            if "type" not in q:
                errors.append(f"Question {i}: missing 'type'")
            if "stem" not in q:
                errors.append(f"Question {i}: missing 'stem'")
    
    return errors


# ═══════════════════════════════════════════════════════════════════════════════
# MOODLE_HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def _build_moodle_category(root: ET.Element, quiz: Dict[str, Any]) -> None:
    """Build Moodle category element."""
    category = ET.SubElement(root, "question")
    category.set("type", "category")
    cat_text = ET.SubElement(category, "category")
    cat_text_content = ET.SubElement(cat_text, "text")
    cat_text_content.text = f"$course$/Week {quiz['metadata']['week']} - {quiz['metadata']['topic']}"


def _build_moodle_mcq(parent: ET.Element, q: Dict[str, Any]) -> None:
    """Build Moodle multiple choice question element."""
    question = ET.SubElement(parent, "question")
    question.set("type", "multichoice")
    
    name = ET.SubElement(question, "name")
    ET.SubElement(name, "text").text = f"{q['id']} - {q['lo_ref']}"
    
    qtext = ET.SubElement(question, "questiontext")
    qtext.set("format", "html")
    ET.SubElement(qtext, "text").text = f"<![CDATA[<p>{html.escape(q['stem'])}</p>]]>"
    
    if "explanation" in q:
        feedback = ET.SubElement(question, "generalfeedback")
        feedback.set("format", "html")
        ET.SubElement(feedback, "text").text = f"<![CDATA[<p>{html.escape(q['explanation'])}</p>]]>"
    
    ET.SubElement(question, "defaultgrade").text = str(q.get("points", 1))
    ET.SubElement(question, "single").text = "true"
    ET.SubElement(question, "shuffleanswers").text = "true"
    
    for key, text in q["options"].items():
        answer = ET.SubElement(question, "answer")
        answer.set("fraction", "100" if key == q["correct"] else "0")
        answer.set("format", "html")
        ET.SubElement(answer, "text").text = f"<![CDATA[<p>{html.escape(text)}</p>]]>"


def _build_moodle_shortanswer(parent: ET.Element, q: Dict[str, Any]) -> None:
    """Build Moodle short answer question element."""
    question = ET.SubElement(parent, "question")
    question.set("type", "shortanswer")
    
    name = ET.SubElement(question, "name")
    ET.SubElement(name, "text").text = f"{q['id']} - {q['lo_ref']}"
    
    qtext = ET.SubElement(question, "questiontext")
    qtext.set("format", "html")
    ET.SubElement(qtext, "text").text = f"<![CDATA[<p>{html.escape(q['stem'])}</p>]]>"
    
    ET.SubElement(question, "defaultgrade").text = str(q.get("points", 1))
    ET.SubElement(question, "usecase").text = "0"
    
    for correct_answer in q["correct"]:
        answer = ET.SubElement(question, "answer")
        answer.set("fraction", "100")
        answer.set("format", "plain_text")
        ET.SubElement(answer, "text").text = correct_answer


# ═══════════════════════════════════════════════════════════════════════════════
# MOODLE_EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
def export_moodle_xml(quiz: Dict[str, Any], output_path: Path) -> None:
    """Export quiz to Moodle XML format."""
    root = ET.Element("quiz")
    _build_moodle_category(root, quiz)
    
    for q in quiz["questions"]:
        if q["type"] == "multiple_choice":
            _build_moodle_mcq(root, q)
        elif q["type"] == "fill_blank":
            _build_moodle_shortanswer(root, q)
    
    xml_str = _prettify_xml(root)
    output_path.write_text(xml_str, encoding="utf-8")
    print(f"✓ Exported {len(quiz['questions'])} questions to Moodle XML: {output_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# CSV_EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
def _get_csv_headers() -> List[str]:
    """Return CSV column headers."""
    return [
        "id", "type", "lo_ref", "difficulty", "bloom_level",
        "stem", "option_a", "option_b", "option_c", "option_d",
        "correct", "explanation", "points"
    ]


def _question_to_csv_row(q: Dict[str, Any]) -> List[Any]:
    """Convert a question to a CSV row."""
    row = [
        q["id"], q["type"], q["lo_ref"],
        q.get("difficulty", ""), q.get("bloom_level", ""), q["stem"],
    ]
    
    if q["type"] == "multiple_choice":
        row.extend([
            q["options"].get("a", ""), q["options"].get("b", ""),
            q["options"].get("c", ""), q["options"].get("d", ""),
        ])
    else:
        row.extend(["", "", "", ""])
    
    if q["type"] == "fill_blank":
        row.append("|".join(q["correct"]))
    else:
        row.append(q["correct"])
    
    row.append(q.get("explanation", ""))
    row.append(q.get("points", 1))
    return row


def export_csv(quiz: Dict[str, Any], output_path: Path) -> None:
    """Export quiz to CSV format."""
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(_get_csv_headers())
        for q in quiz["questions"]:
            writer.writerow(_question_to_csv_row(q))
    
    print(f"✓ Exported {len(quiz['questions'])} questions to CSV: {output_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# CANVAS_HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def _build_canvas_metadata(item: ET.Element, q: Dict[str, Any]) -> None:
    """Build Canvas QTI metadata for a question."""
    itemmetadata = ET.SubElement(item, "itemmetadata")
    qtimetadata = ET.SubElement(itemmetadata, "qtimetadata")
    
    field = ET.SubElement(qtimetadata, "qtimetadatafield")
    ET.SubElement(field, "fieldlabel").text = "question_type"
    ET.SubElement(field, "fieldentry").text = (
        "multiple_choice_question" if q["type"] == "multiple_choice"
        else "short_answer_question"
    )
    
    field2 = ET.SubElement(qtimetadata, "qtimetadatafield")
    ET.SubElement(field2, "fieldlabel").text = "points_possible"
    ET.SubElement(field2, "fieldentry").text = str(q.get("points", 1))


def _build_canvas_presentation(item: ET.Element, q: Dict[str, Any]) -> None:
    """Build Canvas QTI presentation element."""
    presentation = ET.SubElement(item, "presentation")
    material = ET.SubElement(presentation, "material")
    mattext = ET.SubElement(material, "mattext")
    mattext.set("texttype", "text/html")
    mattext.text = f"<p>{html.escape(q['stem'])}</p>"
    
    if q["type"] == "multiple_choice":
        response = ET.SubElement(presentation, "response_lid")
        response.set("ident", "response1")
        response.set("rcardinality", "Single")
        render = ET.SubElement(response, "render_choice")
        for key, text in q["options"].items():
            label = ET.SubElement(render, "response_label")
            label.set("ident", key)
            mat = ET.SubElement(label, "material")
            mattext2 = ET.SubElement(mat, "mattext")
            mattext2.set("texttype", "text/plain")
            mattext2.text = text


# ═══════════════════════════════════════════════════════════════════════════════
# CANVAS_EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
def export_canvas_qti(quiz: Dict[str, Any], output_path: Path) -> None:
    """Export quiz to Canvas QTI format."""
    root = ET.Element("questestinterop")
    assessment = ET.SubElement(root, "assessment")
    assessment.set("title", f"Week {quiz['metadata']['week']}: {quiz['metadata']['topic']}")
    assessment.set("ident", f"week{quiz['metadata']['week']}_quiz")
    
    section = ET.SubElement(assessment, "section")
    section.set("ident", "root_section")
    
    for q in quiz["questions"]:
        item = ET.SubElement(section, "item")
        item.set("ident", q["id"])
        item.set("title", f"{q['id']} - {q['lo_ref']}")
        
        _build_canvas_metadata(item, q)
        _build_canvas_presentation(item, q)
    
    xml_str = _prettify_xml(root)
    output_path.write_text(xml_str, encoding="utf-8")
    print(f"✓ Exported {len(quiz['questions'])} questions to Canvas QTI: {output_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# XML_UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════
def _prettify_xml(root: ET.Element) -> str:
    """Convert XML element to pretty-printed string."""
    xml_str = ET.tostring(root, encoding="unicode")
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="  ")
    lines = [line for line in pretty_xml.split("\n") if line.strip()]
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# CLI_INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════
def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Export Week 12 quiz to LMS formats")
    parser.add_argument("--format", "-f", choices=["moodle", "canvas", "csv"], default="moodle")
    parser.add_argument("--input", "-i", type=Path, default=DEFAULT_QUIZ_PATH)
    parser.add_argument("--output", "-o", type=Path)
    parser.add_argument("--validate", action="store_true", help="Validate quiz structure only")
    return parser.parse_args()


def get_default_output(fmt: str) -> Path:
    """Get default output path for format."""
    if fmt == "moodle":
        return SCRIPT_DIR / "quiz_moodle.xml"
    elif fmt == "canvas":
        return SCRIPT_DIR / "quiz_canvas_qti.xml"
    return SCRIPT_DIR / "quiz_export.csv"


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    args = parse_arguments()
    
    if not args.input.exists():
        print(f"Error: Quiz file not found: {args.input}")
        return 1
    
    quiz = load_quiz(args.input)
    
    if args.validate:
        errors = validate_quiz(quiz)
        if errors:
            print("Validation errors:")
            for e in errors:
                print(f"  - {e}")
            return 1
        print("✓ Quiz validation passed")
        return 0
    
    output = args.output or get_default_output(args.format)
    
    exporters = {
        "moodle": export_moodle_xml,
        "canvas": export_canvas_qti,
        "csv": export_csv,
    }
    exporters[args.format](quiz, output)
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    sys.exit(main())
