#!/usr/bin/env python3
"""
export_moodle.py — Moodle XML Quiz Exporter
NETWORKING class — ASE, CSIE | Computer Networks Laboratory
by ing. dr. Antonio Clim

Exports quiz from YAML format to Moodle XML format for LMS import.

Usage:
    python formative/export_moodle.py                           # Default output
    python formative/export_moodle.py -o quiz_moodle.xml        # Custom output
    python formative/export_moodle.py --category "Week 14"      # Set category
    python formative/export_moodle.py --shuffle                  # Shuffle answers

Moodle Import:
    1. Go to Question Bank → Import
    2. Select "Moodle XML format"
    3. Upload generated file
    4. Review and categorize questions
"""

from __future__ import annotations

import argparse
import html
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
from xml.etree import ElementTree as ET

try:
    import yaml
except ImportError:
    print("Error: PyYAML required. Install with: pip install pyyaml")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# DATA CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class MoodleExportConfig:
    """Configuration for Moodle export."""
    category: str = "Computer Networks / Week 14"
    shuffle_answers: bool = True
    single_answer: bool = True
    penalty_factor: float = 0.3333333
    default_grade: int = 1
    include_feedback: bool = True
    include_hints: bool = True


# ═══════════════════════════════════════════════════════════════════════════════
# XML BUILDERS
# ═══════════════════════════════════════════════════════════════════════════════

def create_cdata_element(parent: ET.Element, tag: str, text: str) -> ET.Element:
    """Create an element with CDATA content."""
    elem = ET.SubElement(parent, tag, format="html")
    # We'll handle CDATA in the final output
    elem.text = text
    return elem


def build_category_question(category: str) -> ET.Element:
    """Build Moodle category question element."""
    question = ET.Element("question", type="category")
    
    cat = ET.SubElement(question, "category")
    cat_text = ET.SubElement(cat, "text")
    cat_text.text = f"$course$/{category}"
    
    info = ET.SubElement(question, "info", format="html")
    info_text = ET.SubElement(info, "text")
    info_text.text = ""
    
    return question


def build_multichoice_question(
    q: Dict[str, Any], 
    config: MoodleExportConfig
) -> ET.Element:
    """Build Moodle multiple choice question element."""
    question = ET.Element("question", type="multichoice")
    
    # Name
    name = ET.SubElement(question, "name")
    name_text = ET.SubElement(name, "text")
    name_text.text = q.get("id", "Question")
    
    # Question text
    qtext = ET.SubElement(question, "questiontext", format="html")
    qtext_text = ET.SubElement(qtext, "text")
    
    # Build question stem with Bloom level tag
    stem = q.get("stem", "").strip()
    bloom = q.get("bloom_level", "")
    lo_ref = q.get("lo_ref", "")
    
    formatted_stem = f"<p>{html.escape(stem)}</p>"
    if bloom or lo_ref:
        tags = []
        if bloom:
            tags.append(f"[{bloom}]")
        if lo_ref:
            tags.append(f"[{lo_ref}]")
        formatted_stem += f"<p><small><em>{' '.join(tags)}</em></small></p>"
    
    qtext_text.text = formatted_stem
    
    # General feedback (explanation)
    if config.include_feedback and q.get("explanation"):
        genfeed = ET.SubElement(question, "generalfeedback", format="html")
        genfeed_text = ET.SubElement(genfeed, "text")
        genfeed_text.text = f"<p>{html.escape(q['explanation'])}</p>"
    
    # Default grade
    points = q.get("points", config.default_grade)
    ET.SubElement(question, "defaultgrade").text = str(points)
    
    # Penalty
    ET.SubElement(question, "penalty").text = str(config.penalty_factor)
    
    # Hidden (not hidden)
    ET.SubElement(question, "hidden").text = "0"
    
    # Single answer
    ET.SubElement(question, "single").text = "true" if config.single_answer else "false"
    
    # Shuffle answers
    ET.SubElement(question, "shuffleanswers").text = "true" if config.shuffle_answers else "false"
    
    # Answer numbering
    ET.SubElement(question, "answernumbering").text = "abc"
    
    # Correct feedback
    cfeed = ET.SubElement(question, "correctfeedback", format="html")
    cfeed_text = ET.SubElement(cfeed, "text")
    cfeed_text.text = "<p>Corect!</p>"
    
    # Partially correct feedback
    pcfeed = ET.SubElement(question, "partiallycorrectfeedback", format="html")
    pcfeed_text = ET.SubElement(pcfeed, "text")
    pcfeed_text.text = "<p>Parțial corect.</p>"
    
    # Incorrect feedback
    icfeed = ET.SubElement(question, "incorrectfeedback", format="html")
    icfeed_text = ET.SubElement(icfeed, "text")
    icfeed_text.text = "<p>Incorect.</p>"
    
    # Answers
    options = q.get("options", {})
    correct_key = q.get("correct", "").lower()
    
    for key, value in sorted(options.items()):
        is_correct = key.lower() == correct_key
        fraction = "100" if is_correct else "0"
        
        answer = ET.SubElement(question, "answer", fraction=fraction, format="html")
        ans_text = ET.SubElement(answer, "text")
        ans_text.text = f"<p>{html.escape(str(value))}</p>"
        
        # Individual answer feedback
        feedback = ET.SubElement(answer, "feedback", format="html")
        feed_text = ET.SubElement(feedback, "text")
        feed_text.text = ""
    
    # Hint (if available)
    if config.include_hints and q.get("hint"):
        hint = ET.SubElement(question, "hint", format="html")
        hint_text = ET.SubElement(hint, "text")
        hint_text.text = f"<p>💡 {html.escape(q['hint'])}</p>"
    
    # Tags
    tags_elem = ET.SubElement(question, "tags")
    for tag in q.get("tags", []):
        tag_elem = ET.SubElement(tags_elem, "tag")
        tag_text = ET.SubElement(tag_elem, "text")
        tag_text.text = tag
    
    # Add Bloom level as tag
    if bloom:
        tag_elem = ET.SubElement(tags_elem, "tag")
        tag_text = ET.SubElement(tag_elem, "text")
        tag_text.text = f"bloom:{bloom.lower()}"
    
    # Add LO as tag
    if lo_ref:
        tag_elem = ET.SubElement(tags_elem, "tag")
        tag_text = ET.SubElement(tag_elem, "text")
        tag_text.text = lo_ref
    
    return question


def build_shortanswer_question(
    q: Dict[str, Any],
    config: MoodleExportConfig
) -> ET.Element:
    """Build Moodle short answer (fill blank) question element."""
    question = ET.Element("question", type="shortanswer")
    
    # Name
    name = ET.SubElement(question, "name")
    name_text = ET.SubElement(name, "text")
    name_text.text = q.get("id", "Question")
    
    # Question text
    qtext = ET.SubElement(question, "questiontext", format="html")
    qtext_text = ET.SubElement(qtext, "text")
    
    stem = q.get("stem", "").strip()
    qtext_text.text = f"<p>{html.escape(stem)}</p>"
    
    # General feedback
    if config.include_feedback and q.get("explanation"):
        genfeed = ET.SubElement(question, "generalfeedback", format="html")
        genfeed_text = ET.SubElement(genfeed, "text")
        genfeed_text.text = f"<p>{html.escape(q['explanation'])}</p>"
    
    # Default grade
    points = q.get("points", config.default_grade)
    ET.SubElement(question, "defaultgrade").text = str(points)
    
    # Penalty
    ET.SubElement(question, "penalty").text = str(config.penalty_factor)
    
    # Hidden
    ET.SubElement(question, "hidden").text = "0"
    
    # Use case
    case_sensitive = q.get("case_sensitive", False)
    ET.SubElement(question, "usecase").text = "1" if case_sensitive else "0"
    
    # Answers (can be multiple correct answers)
    correct_answers = q.get("correct", [])
    if isinstance(correct_answers, str):
        correct_answers = [correct_answers]
    
    for i, ans in enumerate(correct_answers):
        # First answer gets 100%, others could be partial
        fraction = "100" if i == 0 else "100"
        
        answer = ET.SubElement(question, "answer", fraction=fraction, format="plain_text")
        ans_text = ET.SubElement(answer, "text")
        ans_text.text = ans
        
        feedback = ET.SubElement(answer, "feedback", format="html")
        feed_text = ET.SubElement(feedback, "text")
        feed_text.text = ""
    
    # Hint
    if config.include_hints and q.get("hint"):
        hint = ET.SubElement(question, "hint", format="html")
        hint_text = ET.SubElement(hint, "text")
        hint_text.text = f"<p>💡 {html.escape(q['hint'])}</p>"
    
    return question


def build_question(q: Dict[str, Any], config: MoodleExportConfig) -> Optional[ET.Element]:
    """Build appropriate Moodle question element based on type."""
    q_type = q.get("type", "multiple_choice")
    
    if q_type == "multiple_choice":
        return build_multichoice_question(q, config)
    elif q_type == "fill_blank":
        return build_shortanswer_question(q, config)
    else:
        print(f"Warning: Unsupported question type '{q_type}', skipping {q.get('id')}")
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN EXPORT FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════

def export_to_moodle(
    quiz: Dict[str, Any],
    output_path: Path,
    config: Optional[MoodleExportConfig] = None
) -> None:
    """Export quiz to Moodle XML format.
    
    Args:
        quiz: Quiz dictionary loaded from YAML/JSON
        output_path: Path to write XML file
        config: Export configuration options
    """
    if config is None:
        config = MoodleExportConfig()
    
    # Create root element
    root = ET.Element("quiz")
    
    # Add category
    metadata = quiz.get("metadata", {})
    category = metadata.get("moodle_category", config.category)
    root.append(build_category_question(category))
    
    # Add questions
    questions = quiz.get("questions", [])
    exported = 0
    
    for q in questions:
        question_elem = build_question(q, config)
        if question_elem is not None:
            root.append(question_elem)
            exported += 1
    
    # Write to file
    tree = ET.ElementTree(root)
    
    # Add XML declaration
    with open(output_path, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        tree.write(f, encoding="unicode")
    
    print(f"✓ Exported {exported} questions to: {output_path}")
    print(f"  Category: {category}")
    print(f"  Shuffle answers: {config.shuffle_answers}")


def load_quiz(path: Path) -> Dict[str, Any]:
    """Load quiz from YAML or JSON file."""
    if path.suffix in (".yaml", ".yml"):
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    elif path.suffix == ".json":
        import json
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Export quiz to Moodle XML format",
        epilog="NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim"
    )
    
    parser.add_argument(
        "--input", "-i",
        type=Path,
        default=Path(__file__).parent / "quiz_week14.yaml",
        help="Input quiz file (YAML or JSON)"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=Path(__file__).parent / "quiz_week14_moodle.xml",
        help="Output Moodle XML file"
    )
    
    parser.add_argument(
        "--category", "-c",
        type=str,
        default="Computer Networks / Week 14",
        help="Moodle question category"
    )
    
    parser.add_argument(
        "--shuffle",
        action="store_true",
        default=True,
        help="Shuffle answer options"
    )
    
    parser.add_argument(
        "--no-shuffle",
        dest="shuffle",
        action="store_false",
        help="Don't shuffle answer options"
    )
    
    parser.add_argument(
        "--no-feedback",
        action="store_true",
        help="Exclude explanations from export"
    )
    
    parser.add_argument(
        "--no-hints",
        action="store_true",
        help="Exclude hints from export"
    )
    
    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()
    
    # Load quiz
    try:
        quiz = load_quiz(args.input)
    except FileNotFoundError:
        print(f"Error: Quiz file not found: {args.input}")
        return 1
    except Exception as e:
        print(f"Error loading quiz: {e}")
        return 1
    
    # Configure export
    config = MoodleExportConfig(
        category=args.category,
        shuffle_answers=args.shuffle,
        include_feedback=not args.no_feedback,
        include_hints=not args.no_hints
    )
    
    # Export
    try:
        export_to_moodle(quiz, args.output, config)
        return 0
    except Exception as e:
        print(f"Error exporting quiz: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
