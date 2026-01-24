#!/usr/bin/env python3
"""
export_moodle.py — Export Quiz to LMS Formats.

NETWORKING class — ASE, CSIE | Computer Networks Laboratory
by ing. dr. Antonio Clim

Exports quiz.yaml to various LMS formats:
- Moodle XML (GIFT format alternative)
- Canvas QTI
- JSON (universal)

Usage:
    python formative/export_moodle.py                      # Export to Moodle XML
    python formative/export_moodle.py --format json        # Export to JSON
    python formative/export_moodle.py --format canvas      # Export to Canvas QTI
    python formative/export_moodle.py --output my_quiz.xml # Custom output file
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import html
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

try:
    import yaml
except ImportError:
    print("Error: PyYAML required. Install with: pip install pyyaml")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ LOADING
# ═══════════════════════════════════════════════════════════════════════════════
def load_quiz(path: Path) -> Dict[str, Any]:
    """Load quiz from YAML file."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ═══════════════════════════════════════════════════════════════════════════════
# MOODLE XML EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
def export_moodle_xml(quiz: Dict[str, Any], output_path: Path) -> None:
    """
    Export quiz to Moodle XML format.

    Moodle XML structure:
    <quiz>
      <question type="category">...</question>
      <question type="multichoice">...</question>
      <question type="shortanswer">...</question>
      <question type="essay">...</question>
    </quiz>
    """
    meta = quiz["metadata"]
    questions = quiz["questions"]
    export_config = quiz.get("export", {}).get("moodle", {})

    # Create root element
    root = Element("quiz")

    # Add category question
    category = SubElement(root, "question", type="category")
    cat_text = SubElement(category, "category")
    cat_text_content = SubElement(cat_text, "text")
    cat_text_content.text = export_config.get(
        "category", f"$course$/Computer Networks/Week {meta.get('week', '?')}"
    )

    # Add each question
    for q in questions:
        q_type = q.get("type", "multiple_choice")

        if q_type == "multiple_choice":
            _add_moodle_multichoice(root, q, export_config)
        elif q_type in ("fill_blank", "short_answer"):
            _add_moodle_shortanswer(root, q, export_config)
        elif q_type in ("design_task", "architecture_design", "troubleshooting_design", "scenario_analysis"):
            # Scenario analysis with options → multichoice
            if "options" in q:
                _add_moodle_multichoice(root, q, export_config)
            else:
                _add_moodle_essay(root, q, export_config)

    # Format and write XML
    xml_str = tostring(root, encoding="unicode")
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")

    # Remove extra blank lines
    lines = [line for line in pretty_xml.split("\n") if line.strip()]
    clean_xml = "\n".join(lines)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(clean_xml)

    print(f"Exported {len(questions)} questions to {output_path}")


def _add_moodle_multichoice(
    root: Element, q: Dict[str, Any], config: Dict[str, Any]
) -> None:
    """Add a multiple choice question to Moodle XML."""
    question = SubElement(root, "question", type="multichoice")

    # Name
    name = SubElement(question, "name")
    name_text = SubElement(name, "text")
    name_text.text = q["id"]

    # Question text
    qtext = SubElement(question, "questiontext", format="html")
    qtext_text = SubElement(qtext, "text")

    stem = q["stem"]
    if q.get("hint"):
        stem += f"\n\n<em>Hint: {q['hint']}</em>"
    qtext_text.text = f"<![CDATA[<p>{html.escape(stem)}</p>]]>"

    # Default grade
    grade = SubElement(question, "defaultgrade")
    grade.text = str(q.get("points", 1))

    # Penalty
    penalty = SubElement(question, "penalty")
    penalty.text = str(config.get("penalty_factor", 0.25))

    # Single answer
    single = SubElement(question, "single")
    single.text = "true"

    # Shuffle answers
    shuffle = SubElement(question, "shuffleanswers")
    shuffle.text = str(config.get("shuffle_answers", True)).lower()

    # Answer numbering
    numbering = SubElement(question, "answernumbering")
    numbering.text = "abc"

    # Answers
    correct_key = q.get("correct", "").lower()
    options = q.get("options", {})

    for key, value in sorted(options.items()):
        is_correct = key.lower() == correct_key
        fraction = "100" if is_correct else "0"

        answer = SubElement(question, "answer", fraction=fraction, format="html")
        answer_text = SubElement(answer, "text")
        answer_text.text = f"<![CDATA[{html.escape(value)}]]>"

        # Feedback for correct answer
        if is_correct and q.get("explanation"):
            feedback = SubElement(answer, "feedback", format="html")
            fb_text = SubElement(feedback, "text")
            fb_text.text = f"<![CDATA[{html.escape(q['explanation'][:500])}]]>"


def _add_moodle_shortanswer(
    root: Element, q: Dict[str, Any], config: Dict[str, Any]
) -> None:
    """Add a short answer question to Moodle XML."""
    question = SubElement(root, "question", type="shortanswer")

    # Name
    name = SubElement(question, "name")
    name_text = SubElement(name, "text")
    name_text.text = q["id"]

    # Question text
    qtext = SubElement(question, "questiontext", format="html")
    qtext_text = SubElement(qtext, "text")
    qtext_text.text = f"<![CDATA[<p>{html.escape(q['stem'])}</p>]]>"

    # Default grade
    grade = SubElement(question, "defaultgrade")
    grade.text = str(q.get("points", 1))

    # Case sensitivity
    usecase = SubElement(question, "usecase")
    usecase.text = "1" if q.get("case_sensitive", False) else "0"

    # Answers
    correct_answers = q.get("correct", [])
    if isinstance(correct_answers, str):
        correct_answers = [correct_answers]

    for ans in correct_answers:
        answer = SubElement(question, "answer", fraction="100", format="plain")
        answer_text = SubElement(answer, "text")
        answer_text.text = ans

        if q.get("explanation"):
            feedback = SubElement(answer, "feedback", format="html")
            fb_text = SubElement(feedback, "text")
            fb_text.text = f"<![CDATA[{html.escape(q['explanation'][:500])}]]>"


def _add_moodle_essay(
    root: Element, q: Dict[str, Any], config: Dict[str, Any]
) -> None:
    """Add an essay question to Moodle XML."""
    question = SubElement(root, "question", type="essay")

    # Name
    name = SubElement(question, "name")
    name_text = SubElement(name, "text")
    name_text.text = q["id"]

    # Question text
    qtext = SubElement(question, "questiontext", format="html")
    qtext_text = SubElement(qtext, "text")

    stem = q["stem"]
    if q.get("code_template"):
        stem += f"\n\n<pre>{html.escape(q['code_template'])}</pre>"
    qtext_text.text = f"<![CDATA[<p>{stem}</p>]]>"

    # Default grade
    grade = SubElement(question, "defaultgrade")
    grade.text = str(q.get("points", 5))

    # Response format
    response_format = SubElement(question, "responseformat")
    response_format.text = "editor"

    # Grader info (rubric)
    if q.get("rubric"):
        grader = SubElement(question, "graderinfo", format="html")
        grader_text = SubElement(grader, "text")
        rubric_html = "<ul>"
        for score, desc in q["rubric"].items():
            rubric_html += f"<li><strong>{score}:</strong> {html.escape(str(desc))}</li>"
        rubric_html += "</ul>"
        grader_text.text = f"<![CDATA[{rubric_html}]]>"


# ═══════════════════════════════════════════════════════════════════════════════
# JSON EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
def export_json(quiz: Dict[str, Any], output_path: Path) -> None:
    """Export quiz to JSON format."""
    export_config = quiz.get("export", {}).get("json", {})

    export_data = {
        "metadata": {
            **quiz["metadata"],
            "exported_at": datetime.now().isoformat(),
            "format_version": export_config.get("format_version", "2.0"),
        },
        "questions": [],
    }

    include_explanations = export_config.get("include_explanations", True)
    include_hints = export_config.get("include_hints", True)
    include_verification = export_config.get("include_verification", False)

    for q in quiz["questions"]:
        q_export: Dict[str, Any] = {
            "id": q["id"],
            "type": q.get("type", "multiple_choice"),
            "bloom_level": q.get("bloom_level"),
            "lo_ref": q.get("lo_ref"),
            "difficulty": q.get("difficulty"),
            "points": q.get("points", 1),
            "stem": q["stem"].strip(),
        }

        if "options" in q:
            q_export["options"] = q["options"]

        if "correct" in q:
            q_export["correct"] = q["correct"]

        if include_explanations and q.get("explanation"):
            q_export["explanation"] = q["explanation"].strip()

        if include_hints and q.get("hint"):
            q_export["hint"] = q["hint"]

        if include_verification and q.get("verification"):
            q_export["verification"] = q["verification"]

        if q.get("rubric"):
            q_export["rubric"] = q["rubric"]

        if q.get("model_answer"):
            q_export["model_answer"] = q["model_answer"].strip()

        export_data["questions"].append(q_export)

    # Add scoring info
    if "scoring" in quiz:
        export_data["scoring"] = quiz["scoring"]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    print(f"Exported {len(quiz['questions'])} questions to {output_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# CANVAS QTI EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
def export_canvas_qti(quiz: Dict[str, Any], output_path: Path) -> None:
    """
    Export quiz to Canvas QTI format.

    Note: Simplified QTI 1.2 format for Canvas import.
    """
    meta = quiz["metadata"]
    questions = quiz["questions"]
    export_config = quiz.get("export", {}).get("canvas", {})

    # Create QTI manifest
    root = Element(
        "questestinterop",
        xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2",
    )

    # Assessment
    assessment = SubElement(root, "assessment", ident=f"week{meta.get('week', '?')}_quiz")
    assessment.set("title", f"Week {meta.get('week', '?')}: {meta.get('topic', 'Quiz')}")

    # Assessment metadata
    qtimetadata = SubElement(assessment, "qtimetadata")

    # Points possible
    points_field = SubElement(qtimetadata, "qtimetadatafield")
    label = SubElement(points_field, "fieldlabel")
    label.text = "points_possible"
    entry = SubElement(points_field, "fieldentry")
    entry.text = str(export_config.get("points_possible", meta.get("total_points", 42)))

    # Quiz type
    type_field = SubElement(qtimetadata, "qtimetadatafield")
    type_label = SubElement(type_field, "fieldlabel")
    type_label.text = "quiz_type"
    type_entry = SubElement(type_field, "fieldentry")
    type_entry.text = export_config.get("quiz_type", "practice_quiz")

    # Section for questions
    section = SubElement(assessment, "section", ident="root_section")

    # Add questions
    for i, q in enumerate(questions, 1):
        q_type = q.get("type", "multiple_choice")

        if q_type == "multiple_choice" or "options" in q:
            _add_canvas_multiple_choice(section, q, i)
        elif q_type in ("fill_blank", "short_answer"):
            _add_canvas_short_answer(section, q, i)
        else:
            _add_canvas_essay(section, q, i)

    # Format and write
    xml_str = tostring(root, encoding="unicode")
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    print(f"Exported {len(questions)} questions to {output_path} (Canvas QTI)")


def _add_canvas_multiple_choice(section: Element, q: Dict[str, Any], index: int) -> None:
    """Add a multiple choice item to Canvas QTI."""
    item = SubElement(section, "item", ident=q["id"])
    item.set("title", f"Question {index}")

    # Item metadata
    itemmetadata = SubElement(item, "itemmetadata")
    qtimetadata = SubElement(itemmetadata, "qtimetadata")

    # Question type
    qtype_field = SubElement(qtimetadata, "qtimetadatafield")
    qtype_label = SubElement(qtype_field, "fieldlabel")
    qtype_label.text = "question_type"
    qtype_entry = SubElement(qtype_field, "fieldentry")
    qtype_entry.text = "multiple_choice_question"

    # Points
    pts_field = SubElement(qtimetadata, "qtimetadatafield")
    pts_label = SubElement(pts_field, "fieldlabel")
    pts_label.text = "points_possible"
    pts_entry = SubElement(pts_field, "fieldentry")
    pts_entry.text = str(q.get("points", 1))

    # Presentation
    presentation = SubElement(item, "presentation")
    material = SubElement(presentation, "material")
    mattext = SubElement(material, "mattext", texttype="text/html")
    mattext.text = q["stem"]

    # Response
    response_lid = SubElement(
        presentation, "response_lid", ident="response1", rcardinality="Single"
    )
    render_choice = SubElement(response_lid, "render_choice")

    correct_key = q.get("correct", "").lower()
    options = q.get("options", {})

    for key, value in sorted(options.items()):
        response_label = SubElement(render_choice, "response_label", ident=key)
        mat = SubElement(response_label, "material")
        matt = SubElement(mat, "mattext")
        matt.text = value

    # Response processing
    resprocessing = SubElement(item, "resprocessing")
    outcomes = SubElement(resprocessing, "outcomes")
    SubElement(outcomes, "decvar", maxvalue="100", minvalue="0", varname="SCORE", vartype="Decimal")

    # Correct answer condition
    respcondition = SubElement(resprocessing, "respcondition", attrib={"continue": "No"})
    conditionvar = SubElement(respcondition, "conditionvar")
    varequal = SubElement(conditionvar, "varequal", respident="response1")
    varequal.text = correct_key
    setvar = SubElement(respcondition, "setvar", action="Set", varname="SCORE")
    setvar.text = "100"


def _add_canvas_short_answer(section: Element, q: Dict[str, Any], index: int) -> None:
    """Add a short answer item to Canvas QTI."""
    item = SubElement(section, "item", ident=q["id"])
    item.set("title", f"Question {index}")

    # Metadata
    itemmetadata = SubElement(item, "itemmetadata")
    qtimetadata = SubElement(itemmetadata, "qtimetadata")

    qtype_field = SubElement(qtimetadata, "qtimetadatafield")
    qtype_label = SubElement(qtype_field, "fieldlabel")
    qtype_label.text = "question_type"
    qtype_entry = SubElement(qtype_field, "fieldentry")
    qtype_entry.text = "short_answer_question"

    # Presentation
    presentation = SubElement(item, "presentation")
    material = SubElement(presentation, "material")
    mattext = SubElement(material, "mattext", texttype="text/html")
    mattext.text = q["stem"]

    SubElement(presentation, "response_str", ident="response1", rcardinality="Single")


def _add_canvas_essay(section: Element, q: Dict[str, Any], index: int) -> None:
    """Add an essay item to Canvas QTI."""
    item = SubElement(section, "item", ident=q["id"])
    item.set("title", f"Question {index}")

    # Metadata
    itemmetadata = SubElement(item, "itemmetadata")
    qtimetadata = SubElement(itemmetadata, "qtimetadata")

    qtype_field = SubElement(qtimetadata, "qtimetadatafield")
    qtype_label = SubElement(qtype_field, "fieldlabel")
    qtype_label.text = "question_type"
    qtype_entry = SubElement(qtype_field, "fieldentry")
    qtype_entry.text = "essay_question"

    # Presentation
    presentation = SubElement(item, "presentation")
    material = SubElement(presentation, "material")
    mattext = SubElement(material, "mattext", texttype="text/html")
    mattext.text = q["stem"]

    SubElement(presentation, "response_str", ident="response1", rcardinality="Single")


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Export quiz to LMS formats",
        epilog="NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim",
    )

    parser.add_argument(
        "--quiz",
        type=Path,
        default=Path(__file__).parent / "quiz.yaml",
        help="Path to quiz YAML file",
    )
    parser.add_argument(
        "--format",
        choices=["moodle", "json", "canvas"],
        default="moodle",
        help="Export format (default: moodle)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file path",
    )

    args = parser.parse_args()

    try:
        quiz = load_quiz(args.quiz)

        if args.format == "moodle":
            output = args.output or Path("quiz_moodle.xml")
            export_moodle_xml(quiz, output)
        elif args.format == "json":
            output = args.output or Path("quiz_export.json")
            export_json(quiz, output)
        elif args.format == "canvas":
            output = args.output or Path("quiz_canvas_qti.xml")
            export_canvas_qti(quiz, output)

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Export failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
