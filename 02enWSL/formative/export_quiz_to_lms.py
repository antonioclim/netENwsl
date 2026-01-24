#!/usr/bin/env python3
"""
LMS Quiz Export Tool — Week 2 Laboratory Kit

Converts quiz.yaml to various LMS-compatible formats:
- Moodle XML (GIFT format alternative)
- Canvas QTI
- JSON (generic LMS import)

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
from typing import Any
from xml.dom import minidom

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed.")
    print("Fix:   pip install pyyaml")
    sys.exit(1)


@dataclass
class ExportConfig:
    """Configuration for quiz export."""

    input_file: Path
    output_file: Path
    format: str
    category: str = "Week 02 - Sockets"
    shuffle_answers: bool = True


def load_quiz(quiz_path: Path) -> dict[str, Any]:
    """Load quiz from YAML file."""
    if not quiz_path.exists():
        raise FileNotFoundError(f"Quiz file not found: {quiz_path}")

    with open(quiz_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def export_to_moodle_xml(quiz: dict[str, Any], config: ExportConfig) -> str:
    """Export quiz to Moodle XML format.

    Reference: https://docs.moodle.org/en/Moodle_XML_format
    """
    root = ET.Element("quiz")

    # Add category
    category = ET.SubElement(root, "question")
    category.set("type", "category")
    cat_elem = ET.SubElement(category, "category")
    cat_text = ET.SubElement(cat_elem, "text")
    cat_text.text = f"$course$/top/{config.category}"

    for q in quiz.get("questions", []):
        question = ET.SubElement(root, "question")

        if q["type"] in ("multiple_choice", "code_output"):
            question.set("type", "multichoice")

            # Question name
            name = ET.SubElement(question, "name")
            name_text = ET.SubElement(name, "text")
            name_text.text = q["id"]

            # Question text
            qtext = ET.SubElement(question, "questiontext")
            qtext.set("format", "html")
            qtext_text = ET.SubElement(qtext, "text")
            stem = q["stem"].replace("\n", "<br/>")
            qtext_text.text = f"<![CDATA[<p>{stem}</p>]]>"

            # Default grade
            grade = ET.SubElement(question, "defaultgrade")
            grade.text = str(q.get("points", 1))

            # Shuffle answers
            shuffle = ET.SubElement(question, "shuffleanswers")
            shuffle.text = "1" if config.shuffle_answers else "0"

            # Single answer
            single = ET.SubElement(question, "single")
            single.text = "true"

            # Answers
            correct_key = q["correct"]
            for key, text in q.get("options", {}).items():
                answer = ET.SubElement(question, "answer")
                answer.set("fraction", "100" if key == correct_key else "0")
                answer.set("format", "html")
                ans_text = ET.SubElement(answer, "text")
                ans_text.text = f"<![CDATA[{text}]]>"

                # Feedback
                feedback = ET.SubElement(answer, "feedback")
                feedback.set("format", "html")
                fb_text = ET.SubElement(feedback, "text")
                if key == correct_key:
                    fb_text.text = f"<![CDATA[Correct! {q.get('explanation', '')}]]>"
                else:
                    fb_text.text = "<![CDATA[Incorrect. Please review the material.]]>"

            # General feedback
            gen_feedback = ET.SubElement(question, "generalfeedback")
            gen_feedback.set("format", "html")
            gf_text = ET.SubElement(gen_feedback, "text")
            gf_text.text = f"<![CDATA[{q.get('explanation', '')}]]>"

            # Tags
            tags = ET.SubElement(question, "tags")
            for tag in q.get("tags", []):
                tag_elem = ET.SubElement(tags, "tag")
                tag_text = ET.SubElement(tag_elem, "text")
                tag_text.text = tag

        elif q["type"] == "fill_blank":
            question.set("type", "shortanswer")

            name = ET.SubElement(question, "name")
            name_text = ET.SubElement(name, "text")
            name_text.text = q["id"]

            qtext = ET.SubElement(question, "questiontext")
            qtext.set("format", "html")
            qtext_text = ET.SubElement(qtext, "text")
            qtext_text.text = f"<![CDATA[<p>{q['stem']}</p>]]>"

            grade = ET.SubElement(question, "defaultgrade")
            grade.text = str(q.get("points", 1))

            usecase = ET.SubElement(question, "usecase")
            usecase.text = "0"  # Case insensitive

            for accepted in q.get("correct", []):
                answer = ET.SubElement(question, "answer")
                answer.set("fraction", "100")
                answer.set("format", "plain_text")
                ans_text = ET.SubElement(answer, "text")
                ans_text.text = accepted

    # Pretty print
    xml_str = ET.tostring(root, encoding="unicode")
    dom = minidom.parseString(xml_str)
    return dom.toprettyxml(indent="  ")


def export_to_gift(quiz: dict[str, Any], config: ExportConfig) -> str:
    """Export quiz to GIFT format (simple text format for Moodle).

    Reference: https://docs.moodle.org/en/GIFT_format
    """
    lines = []
    lines.append(f"$CATEGORY: {config.category}\n")

    for q in quiz.get("questions", []):
        # Question title
        lines.append(f"// Question: {q['id']}")
        lines.append(f"// LO: {q.get('lo_ref', 'N/A')}")
        lines.append(f"// Bloom: {q.get('bloom_level', 1)}")
        lines.append("")

        stem = q["stem"].replace("\n", "\\n").replace("~", "\\~").replace("=", "\\=")

        if q["type"] in ("multiple_choice", "code_output"):
            lines.append(f"::{q['id']}::{stem} {{")
            correct_key = q["correct"]
            for key, text in q.get("options", {}).items():
                prefix = "=" if key == correct_key else "~"
                text_escaped = text.replace("~", "\\~").replace("=", "\\=")
                lines.append(f"  {prefix}{text_escaped}")
            lines.append("}")

        elif q["type"] == "fill_blank":
            answers = q.get("correct", [])
            answer_str = "=".join(answers)
            lines.append(f"::{q['id']}::{stem} {{={answer_str}}}")

        lines.append("")

    return "\n".join(lines)


def export_to_canvas_qti(quiz: dict[str, Any], config: ExportConfig) -> str:
    """Export quiz to Canvas QTI format.

    Note: Full QTI export requires ZIP packaging with manifest.
    This generates the assessment XML component.
    """
    root = ET.Element("questestinterop")

    assessment = ET.SubElement(root, "assessment")
    assessment.set("ident", f"quiz_{quiz['metadata']['week']}")
    assessment.set("title", quiz["metadata"]["topic"])

    # Assessment metadata
    qtimetadata = ET.SubElement(assessment, "qtimetadata")
    meta_field = ET.SubElement(qtimetadata, "qtimetadatafield")
    label = ET.SubElement(meta_field, "fieldlabel")
    label.text = "cc_maxattempts"
    entry = ET.SubElement(meta_field, "fieldentry")
    entry.text = "3"

    # Section containing items
    section = ET.SubElement(assessment, "section")
    section.set("ident", "root_section")

    for q in quiz.get("questions", []):
        item = ET.SubElement(section, "item")
        item.set("ident", q["id"])
        item.set("title", q["id"])

        # Item metadata
        itemmetadata = ET.SubElement(item, "itemmetadata")
        qtimeta = ET.SubElement(itemmetadata, "qtimetadata")

        qtype_field = ET.SubElement(qtimeta, "qtimetadatafield")
        qtype_label = ET.SubElement(qtype_field, "fieldlabel")
        qtype_label.text = "question_type"
        qtype_entry = ET.SubElement(qtype_field, "fieldentry")

        if q["type"] in ("multiple_choice", "code_output"):
            qtype_entry.text = "multiple_choice_question"
        else:
            qtype_entry.text = "short_answer_question"

        points_field = ET.SubElement(qtimeta, "qtimetadatafield")
        points_label = ET.SubElement(points_field, "fieldlabel")
        points_label.text = "points_possible"
        points_entry = ET.SubElement(points_field, "fieldentry")
        points_entry.text = str(q.get("points", 1))

        # Presentation
        presentation = ET.SubElement(item, "presentation")
        material = ET.SubElement(presentation, "material")
        mattext = ET.SubElement(material, "mattext")
        mattext.set("texttype", "text/html")
        mattext.text = q["stem"]

        if q["type"] in ("multiple_choice", "code_output"):
            response = ET.SubElement(presentation, "response_lid")
            response.set("ident", "response1")
            response.set("rcardinality", "Single")

            render = ET.SubElement(response, "render_choice")
            for key, text in q.get("options", {}).items():
                resp_label = ET.SubElement(render, "response_label")
                resp_label.set("ident", key)
                mat = ET.SubElement(resp_label, "material")
                mt = ET.SubElement(mat, "mattext")
                mt.set("texttype", "text/plain")
                mt.text = text

    xml_str = ET.tostring(root, encoding="unicode")
    dom = minidom.parseString(xml_str)
    return dom.toprettyxml(indent="  ")


def export_to_json(quiz: dict[str, Any], config: ExportConfig) -> str:
    """Export quiz to generic JSON format."""
    output = {
        "metadata": quiz.get("metadata", {}),
        "questions": [],
    }

    for q in quiz.get("questions", []):
        question = {
            "id": q["id"],
            "type": q["type"],
            "loRef": q.get("lo_ref"),
            "difficulty": q.get("difficulty"),
            "bloomLevel": q.get("bloom_level"),
            "points": q.get("points", 1),
            "stem": q["stem"],
            "explanation": q.get("explanation"),
            "tags": q.get("tags", []),
        }

        if q["type"] in ("multiple_choice", "code_output"):
            question["choices"] = [
                {"id": k, "text": v, "correct": k == q["correct"]}
                for k, v in q.get("options", {}).items()
            ]
        elif q["type"] == "fill_blank":
            question["acceptedAnswers"] = q.get("correct", [])
            question["hint"] = q.get("hint")

        output["questions"].append(question)

    return json.dumps(output, indent=2, ensure_ascii=False)


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Export quiz to LMS-compatible formats",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python export_quiz_to_lms.py --format moodle
  python export_quiz_to_lms.py --format gift --output quiz.gift
  python export_quiz_to_lms.py --format canvas
  python export_quiz_to_lms.py --format json
        """,
    )

    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        default=Path("formative/quiz.yaml"),
        help="Input quiz YAML file (default: formative/quiz.yaml)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Output file path (auto-generated if not specified)",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["moodle", "gift", "canvas", "json"],
        default="json",
        help="Export format (default: json)",
    )
    parser.add_argument(
        "--category",
        "-c",
        default="Week 02 - Sockets",
        help="Quiz category for LMS (default: Week 02 - Sockets)",
    )
    parser.add_argument(
        "--no-shuffle",
        action="store_true",
        help="Disable answer shuffling",
    )

    args = parser.parse_args()

    # Determine output filename
    if args.output is None:
        extensions = {
            "moodle": ".xml",
            "gift": ".gift",
            "canvas": ".xml",
            "json": ".json",
        }
        args.output = Path(f"quiz_export_{args.format}{extensions[args.format]}")

    config = ExportConfig(
        input_file=args.input,
        output_file=args.output,
        format=args.format,
        category=args.category,
        shuffle_answers=not args.no_shuffle,
    )

    print(f"Loading quiz from: {config.input_file}")

    try:
        quiz = load_quiz(config.input_file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1

    print(f"Found {len(quiz.get('questions', []))} questions")
    print(f"Exporting to {config.format} format...")

    exporters = {
        "moodle": export_to_moodle_xml,
        "gift": export_to_gift,
        "canvas": export_to_canvas_qti,
        "json": export_to_json,
    }

    output = exporters[config.format](quiz, config)

    with open(config.output_file, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"✓ Exported to: {config.output_file}")
    print(f"  Size: {len(output)} bytes")

    return 0


if __name__ == "__main__":
    sys.exit(main())
