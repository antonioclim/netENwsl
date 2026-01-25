#!/usr/bin/env python3
"""
LMS Quiz Export Tool — Week 2 Laboratory Kit

Converts quiz.yaml to various LMS-compatible formats:
- Moodle XML (GIFT format alternative)
- Canvas QTI
- JSON (generic LMS import)
- GIFT (text format)

Usage:
    python export_quiz_to_lms.py --format moodle --output quiz_moodle.xml
    python export_quiz_to_lms.py --format canvas --output quiz_canvas.zip
    python export_quiz_to_lms.py --format json --output quiz_export.json
    python export_quiz_to_lms.py --format gift --output quiz.gift

NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim
"""

from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
from xml.dom import minidom

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed.")
    print("Fix:   pip install pyyaml")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class ExportConfig:
    """Configuration for quiz export."""
    input_file: Path
    output_file: Path
    format: str
    category: str = "Week 02 - Sockets"
    shuffle_answers: bool = True


# ═══════════════════════════════════════════════════════════════════════════════
# YAML LOADER
# ═══════════════════════════════════════════════════════════════════════════════
def load_quiz_yaml(quiz_path: Path) -> Dict[str, Any]:
    """
    Load quiz from YAML file.
    
    Args:
        quiz_path: Path to quiz.yaml
    
    Returns:
        Parsed quiz dictionary
    
    Raises:
        FileNotFoundError: If file does not exist
        yaml.YAMLError: If YAML is malformed
    """
    if not quiz_path.exists():
        raise FileNotFoundError(f"Quiz file not found: {quiz_path}")

    with open(quiz_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


# Alias for backward compatibility
load_quiz = load_quiz_yaml


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATOR
# ═══════════════════════════════════════════════════════════════════════════════
def validate_quiz_structure(quiz: Dict[str, Any]) -> List[str]:
    """
    Validate quiz structure and return list of errors.
    
    Args:
        quiz: Parsed quiz dictionary
    
    Returns:
        List of error messages (empty if valid)
    """
    errors: List[str] = []
    
    # Check metadata
    if "metadata" not in quiz:
        errors.append("Missing 'metadata' section")
    
    # Check questions
    if "questions" not in quiz:
        errors.append("Missing 'questions' section")
        return errors
    
    questions = quiz.get("questions", [])
    if not questions:
        errors.append("Questions list is empty")
        return errors
    
    # Validate each question
    for i, q in enumerate(questions):
        q_id = q.get("id", f"question_{i}")
        
        if "id" not in q:
            errors.append(f"Question {i}: missing 'id' field")
        
        if "stem" not in q and "question_text" not in q:
            errors.append(f"Question {q_id}: missing 'stem' or 'question_text'")
        
        if "correct" not in q:
            errors.append(f"Question {q_id}: missing 'correct' answer")
        
        if "options" in q:
            correct = q.get("correct", "")
            if correct not in q["options"]:
                errors.append(f"Question {q_id}: correct answer '{correct}' not in options")
    
    return errors


# ═══════════════════════════════════════════════════════════════════════════════
# QUESTION FORMATTER
# ═══════════════════════════════════════════════════════════════════════════════
def format_question_for_export(question: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format a single question for LMS export.
    
    Args:
        question: Raw question dictionary from YAML
    
    Returns:
        Formatted question dictionary
    """
    formatted = {
        "id": question.get("id", "unknown"),
        "type": question.get("type", "multiple_choice"),
        "stem": question.get("stem", question.get("question_text", "")),
        "points": question.get("points", 1),
    }
    
    # Format options with correct indicator
    if "options" in question:
        correct = question.get("correct", "")
        formatted["options"] = []
        for key, text in question["options"].items():
            formatted["options"].append({
                "key": key,
                "text": text,
                "correct": key == correct
            })
    
    # Include metadata
    if "explanation" in question:
        formatted["feedback"] = question["explanation"]
    
    if "lo_ref" in question:
        formatted["learning_objective"] = question["lo_ref"]
    
    if "difficulty" in question:
        formatted["difficulty"] = question["difficulty"]
    
    return formatted


# ═══════════════════════════════════════════════════════════════════════════════
# JSON EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
def export_to_json(quiz: Dict[str, Any]) -> Dict[str, Any]:
    """
    Export quiz to JSON format for generic LMS import.
    
    Args:
        quiz: Parsed quiz dictionary
    
    Returns:
        JSON-serialisable dictionary
    """
    metadata = quiz.get("metadata", {})
    questions = quiz.get("questions", [])
    
    exported = {
        "metadata": {
            "week": metadata.get("week", 0),
            "topic": metadata.get("topic", ""),
            "version": metadata.get("version", "1.0.0"),
            "total_questions": len(questions),
            "exported_by": "export_quiz_to_lms.py",
        },
        "questions": [format_question_for_export(q) for q in questions]
    }
    
    return exported


def _write_json(data: Dict[str, Any], output_path: Path) -> None:
    """Write JSON data to file."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════════════════════════
# MOODLE XML EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
def _create_moodle_category(root: ET.Element, category: str) -> None:
    """Add category element to Moodle XML."""
    cat_q = ET.SubElement(root, "question")
    cat_q.set("type", "category")
    cat_elem = ET.SubElement(cat_q, "category")
    cat_text = ET.SubElement(cat_elem, "text")
    cat_text.text = f"$course$/top/{category}"


def _create_moodle_question(root: ET.Element, q: Dict[str, Any], 
                            shuffle: bool) -> None:
    """Add single question to Moodle XML."""
    question = ET.SubElement(root, "question")
    question.set("type", "multichoice")
    
    # Name
    name = ET.SubElement(question, "name")
    name_text = ET.SubElement(name, "text")
    name_text.text = q["id"]
    
    # Question text
    qtext = ET.SubElement(question, "questiontext")
    qtext.set("format", "html")
    qtext_text = ET.SubElement(qtext, "text")
    stem = q["stem"].replace("\n", "<br/>")
    qtext_text.text = f"<![CDATA[<p>{stem}</p>]]>"
    
    # Grade and settings
    ET.SubElement(question, "defaultgrade").text = str(q.get("points", 1))
    ET.SubElement(question, "shuffleanswers").text = "1" if shuffle else "0"
    ET.SubElement(question, "single").text = "true"
    
    # Answers
    correct = q.get("correct", "")
    for key, text in q.get("options", {}).items():
        answer = ET.SubElement(question, "answer")
        answer.set("fraction", "100" if key == correct else "0")
        answer.set("format", "html")
        ans_text = ET.SubElement(answer, "text")
        ans_text.text = f"<![CDATA[{text}]]>"


def export_to_moodle_xml(quiz: Dict[str, Any], config: ExportConfig) -> str:
    """Export quiz to Moodle XML format."""
    root = ET.Element("quiz")
    
    _create_moodle_category(root, config.category)
    
    for q in quiz.get("questions", []):
        if q.get("type") in ("multiple_choice", "code_output"):
            _create_moodle_question(root, q, config.shuffle_answers)
    
    # Pretty print
    xml_str = ET.tostring(root, encoding="unicode")
    dom = minidom.parseString(xml_str)
    return dom.toprettyxml(indent="  ")


# ═══════════════════════════════════════════════════════════════════════════════
# GIFT FORMAT EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
def _format_gift_question(q: Dict[str, Any]) -> str:
    """Format single question in GIFT format."""
    lines = []
    
    # Title
    lines.append(f"::{q['id']}::")
    
    # Stem
    stem = q["stem"].replace("{", "\\{").replace("}", "\\}")
    lines.append(stem)
    
    # Answers
    lines.append("{")
    correct = q.get("correct", "")
    for key, text in q.get("options", {}).items():
        prefix = "=" if key == correct else "~"
        text_escaped = text.replace("{", "\\{").replace("}", "\\}")
        lines.append(f"  {prefix}{text_escaped}")
    lines.append("}")
    
    return "\n".join(lines)


def export_to_gift(quiz: Dict[str, Any], config: ExportConfig) -> str:
    """Export quiz to GIFT text format."""
    sections = []
    sections.append(f"// Quiz: {config.category}")
    sections.append(f"// Questions: {len(quiz.get('questions', []))}")
    sections.append("")
    
    for q in quiz.get("questions", []):
        if q.get("type") in ("multiple_choice", "code_output"):
            sections.append(_format_gift_question(q))
            sections.append("")
    
    return "\n".join(sections)


# ═══════════════════════════════════════════════════════════════════════════════
# CANVAS QTI EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
def _create_qti_item(q: Dict[str, Any], index: int) -> ET.Element:
    """Create QTI item element for single question."""
    item = ET.Element("item")
    item.set("ident", q["id"])
    item.set("title", f"Question {index + 1}")
    
    # Question text
    presentation = ET.SubElement(item, "presentation")
    material = ET.SubElement(presentation, "material")
    mattext = ET.SubElement(material, "mattext")
    mattext.set("texttype", "text/html")
    mattext.text = q["stem"]
    
    # Response options
    response = ET.SubElement(presentation, "response_lid")
    response.set("ident", "response1")
    render = ET.SubElement(response, "render_choice")
    
    correct = q.get("correct", "")
    for key, text in q.get("options", {}).items():
        choice = ET.SubElement(render, "response_label")
        choice.set("ident", key)
        mat = ET.SubElement(choice, "material")
        mt = ET.SubElement(mat, "mattext")
        mt.text = text
    
    # Correct answer processing
    resprocessing = ET.SubElement(item, "resprocessing")
    outcomes = ET.SubElement(resprocessing, "outcomes")
    decvar = ET.SubElement(outcomes, "decvar")
    decvar.set("maxvalue", str(q.get("points", 1)))
    decvar.set("minvalue", "0")
    decvar.set("varname", "SCORE")
    decvar.set("vartype", "Decimal")
    
    respcondition = ET.SubElement(resprocessing, "respcondition")
    respcondition.set("continue", "No")
    conditionvar = ET.SubElement(respcondition, "conditionvar")
    varequal = ET.SubElement(conditionvar, "varequal")
    varequal.set("respident", "response1")
    varequal.text = correct
    setvar = ET.SubElement(respcondition, "setvar")
    setvar.set("action", "Set")
    setvar.set("varname", "SCORE")
    setvar.text = str(q.get("points", 1))
    
    return item


def export_to_canvas_qti(quiz: Dict[str, Any], config: ExportConfig) -> str:
    """Export quiz to Canvas QTI format."""
    root = ET.Element("questestinterop")
    root.set("xmlns", "http://www.imsglobal.org/xsd/ims_qtiasiv1p2")
    
    assessment = ET.SubElement(root, "assessment")
    assessment.set("ident", f"week2_quiz_{quiz.get('metadata', {}).get('week', 2)}")
    assessment.set("title", config.category)
    
    section = ET.SubElement(assessment, "section")
    section.set("ident", "root_section")
    
    for i, q in enumerate(quiz.get("questions", [])):
        if q.get("type") in ("multiple_choice", "code_output"):
            item = _create_qti_item(q, i)
            section.append(item)
    
    xml_str = ET.tostring(root, encoding="unicode")
    dom = minidom.parseString(xml_str)
    return dom.toprettyxml(indent="  ")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN EXPORT DISPATCHER
# ═══════════════════════════════════════════════════════════════════════════════
def export_quiz(config: ExportConfig) -> None:
    """
    Export quiz to specified format.
    
    Args:
        config: Export configuration
    """
    # Load and validate
    quiz = load_quiz_yaml(config.input_file)
    errors = validate_quiz_structure(quiz)
    
    if errors:
        print("Validation errors:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    
    # Export
    if config.format == "moodle":
        content = export_to_moodle_xml(quiz, config)
    elif config.format == "gift":
        content = export_to_gift(quiz, config)
    elif config.format == "canvas":
        content = export_to_canvas_qti(quiz, config)
    elif config.format == "json":
        data = export_to_json(quiz)
        _write_json(data, config.output_file)
        print(f"✓ Exported {len(quiz['questions'])} questions to {config.output_file}")
        return
    else:
        raise ValueError(f"Unknown format: {config.format}")
    
    # Write output
    with open(config.output_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✓ Exported {len(quiz['questions'])} questions to {config.output_file}")


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Export quiz.yaml to LMS formats",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python export_quiz_to_lms.py --format moodle --output quiz.xml
  python export_quiz_to_lms.py --format gift --output quiz.gift
  python export_quiz_to_lms.py --format json --output quiz.json
        """
    )
    
    parser.add_argument(
        "--input", "-i",
        type=Path,
        default=Path(__file__).parent / "quiz.yaml",
        help="Input quiz.yaml file"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        required=True,
        help="Output file path"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["moodle", "gift", "canvas", "json"],
        required=True,
        help="Export format"
    )
    parser.add_argument(
        "--category",
        default="Week 02 - Sockets",
        help="Quiz category name"
    )
    parser.add_argument(
        "--no-shuffle",
        action="store_true",
        help="Disable answer shuffling"
    )
    
    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()
    
    config = ExportConfig(
        input_file=args.input,
        output_file=args.output,
        format=args.format,
        category=args.category,
        shuffle_answers=not args.no_shuffle
    )
    
    try:
        export_quiz(config)
        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Export failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
