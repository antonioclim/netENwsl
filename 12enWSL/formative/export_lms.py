#!/usr/bin/env python3
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

from __future__ import annotations

import argparse
import json
import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path
from typing import Dict, Any
import html
import sys

SCRIPT_DIR = Path(__file__).parent
DEFAULT_QUIZ_PATH = SCRIPT_DIR / "quiz.json"


def load_quiz(path: Path) -> Dict[str, Any]:
    """Load quiz from JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def export_moodle_xml(quiz: Dict[str, Any], output_path: Path) -> None:
    """Export quiz to Moodle XML format."""
    root = ET.Element("quiz")
    
    category = ET.SubElement(root, "question")
    category.set("type", "category")
    cat_text = ET.SubElement(category, "category")
    cat_text_content = ET.SubElement(cat_text, "text")
    cat_text_content.text = f"$course$/Week {quiz['metadata']['week']} - {quiz['metadata']['topic']}"
    
    for q in quiz["questions"]:
        question = ET.SubElement(root, "question")
        
        if q["type"] == "multiple_choice":
            question.set("type", "multichoice")
            name = ET.SubElement(question, "name")
            name_text = ET.SubElement(name, "text")
            name_text.text = f"{q['id']} - {q['lo_ref']}"
            
            qtext = ET.SubElement(question, "questiontext")
            qtext.set("format", "html")
            qtext_content = ET.SubElement(qtext, "text")
            qtext_content.text = f"<![CDATA[<p>{html.escape(q['stem'])}</p>]]>"
            
            if "explanation" in q:
                feedback = ET.SubElement(question, "generalfeedback")
                feedback.set("format", "html")
                fb_text = ET.SubElement(feedback, "text")
                fb_text.text = f"<![CDATA[<p>{html.escape(q['explanation'])}</p>]]>"
            
            grade = ET.SubElement(question, "defaultgrade")
            grade.text = str(q.get("points", 1))
            
            single = ET.SubElement(question, "single")
            single.text = "true"
            
            shuffle = ET.SubElement(question, "shuffleanswers")
            shuffle.text = "true"
            
            for key, text in q["options"].items():
                answer = ET.SubElement(question, "answer")
                answer.set("fraction", "100" if key == q["correct"] else "0")
                answer.set("format", "html")
                ans_text = ET.SubElement(answer, "text")
                ans_text.text = f"<![CDATA[<p>{html.escape(text)}</p>]]>"
        
        elif q["type"] == "fill_blank":
            question.set("type", "shortanswer")
            name = ET.SubElement(question, "name")
            name_text = ET.SubElement(name, "text")
            name_text.text = f"{q['id']} - {q['lo_ref']}"
            
            qtext = ET.SubElement(question, "questiontext")
            qtext.set("format", "html")
            qtext_content = ET.SubElement(qtext, "text")
            qtext_content.text = f"<![CDATA[<p>{html.escape(q['stem'])}</p>]]>"
            
            grade = ET.SubElement(question, "defaultgrade")
            grade.text = str(q.get("points", 1))
            
            usecase = ET.SubElement(question, "usecase")
            usecase.text = "0"
            
            for correct_answer in q["correct"]:
                answer = ET.SubElement(question, "answer")
                answer.set("fraction", "100")
                answer.set("format", "plain_text")
                ans_text = ET.SubElement(answer, "text")
                ans_text.text = correct_answer
    
    xml_str = ET.tostring(root, encoding="unicode")
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="  ")
    lines = [line for line in pretty_xml.split("\n") if line.strip()]
    final_xml = "\n".join(lines)
    
    output_path.write_text(final_xml, encoding="utf-8")
    print(f"✓ Exported {len(quiz['questions'])} questions to Moodle XML: {output_path}")


def export_csv(quiz: Dict[str, Any], output_path: Path) -> None:
    """Export quiz to CSV format."""
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "id", "type", "lo_ref", "difficulty", "bloom_level",
            "stem", "option_a", "option_b", "option_c", "option_d",
            "correct", "explanation", "points"
        ])
        
        for q in quiz["questions"]:
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
            writer.writerow(row)
    
    print(f"✓ Exported {len(quiz['questions'])} questions to CSV: {output_path}")


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
    
    xml_str = ET.tostring(root, encoding="unicode")
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="  ")
    output_path.write_text(pretty_xml, encoding="utf-8")
    print(f"✓ Exported {len(quiz['questions'])} questions to Canvas QTI: {output_path}")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Export Week 12 quiz to LMS formats")
    parser.add_argument("--format", "-f", choices=["moodle", "canvas", "csv"], default="moodle")
    parser.add_argument("--input", "-i", type=Path, default=DEFAULT_QUIZ_PATH)
    parser.add_argument("--output", "-o", type=Path)
    args = parser.parse_args()
    
    if not args.input.exists():
        print(f"Error: Quiz file not found: {args.input}")
        return 1
    
    quiz = load_quiz(args.input)
    
    if args.output is None:
        if args.format == "moodle":
            args.output = SCRIPT_DIR / "quiz_moodle.xml"
        elif args.format == "canvas":
            args.output = SCRIPT_DIR / "quiz_canvas_qti.xml"
        else:
            args.output = SCRIPT_DIR / "quiz_export.csv"
    
    if args.format == "moodle":
        export_moodle_xml(quiz, args.output)
    elif args.format == "canvas":
        export_canvas_qti(quiz, args.output)
    elif args.format == "csv":
        export_csv(quiz, args.output)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
