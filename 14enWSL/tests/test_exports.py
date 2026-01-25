#!/usr/bin/env python3
"""Unit tests for quiz export functionality.

NETWORKING class — ASE, CSIE | Computer Networks Laboratory
by ing. dr. Antonio Clim

Tests for Moodle XML and Canvas JSON export functions.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from typing import Any, Dict, List
from xml.etree import ElementTree as ET

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# ═══════════════════════════════════════════════════════════════════════════════
# SAMPLE_DATA
# ═══════════════════════════════════════════════════════════════════════════════
SAMPLE_QUESTION: Dict[str, Any] = {
    "id": "q01",
    "type": "multiple_choice",
    "bloom_level": "Remember",
    "points": 1,
    "stem": "Which OSI layer handles IP addressing?",
    "options": {"a": "Data Link (Layer 2)", "b": "Network (Layer 3)", "c": "Transport (Layer 4)", "d": "Application (Layer 7)"},
    "correct": "b",
    "explanation": "The Network Layer (Layer 3) manages IP addressing.",
}

SAMPLE_QUIZ: Dict[str, Any] = {
    "metadata": {"week": 14, "topic": "Integrated Recap", "version": "2.0.0", "author": "ing. dr. Antonio Clim", "question_count": 1},
    "questions": [SAMPLE_QUESTION],
}


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def export_to_moodle_xml(quiz: Dict[str, Any]) -> str:
    """Export quiz to Moodle XML format."""
    root = ET.Element("quiz")
    for q in quiz.get("questions", []):
        question = ET.SubElement(root, "question")
        question.set("type", "multichoice")
        name = ET.SubElement(question, "name")
        ET.SubElement(name, "text").text = q.get("id", "unknown")
        qtext = ET.SubElement(question, "questiontext")
        qtext.set("format", "html")
        ET.SubElement(qtext, "text").text = q.get("stem", "")
        ET.SubElement(question, "defaultgrade").text = str(q.get("points", 1))
        correct_key = q.get("correct", "")
        for key, option_text in q.get("options", {}).items():
            answer = ET.SubElement(question, "answer")
            answer.set("fraction", "100" if key == correct_key else "0")
            ET.SubElement(answer, "text").text = option_text
    return ET.tostring(root, encoding="unicode")


def export_to_canvas_json(quiz: Dict[str, Any]) -> str:
    """Export quiz to Canvas-compatible JSON format."""
    canvas_quiz = {
        "quiz": {
            "title": f"Week {quiz['metadata'].get('week', 0)} Quiz",
            "description": quiz["metadata"].get("topic", ""),
            "quiz_type": "practice_quiz",
            "points_possible": sum(q.get("points", 1) for q in quiz.get("questions", [])),
        },
        "questions": [],
    }
    for q in quiz.get("questions", []):
        canvas_q = {
            "question_name": q.get("id", ""),
            "question_text": q.get("stem", ""),
            "question_type": "multiple_choice_question",
            "points_possible": q.get("points", 1),
            "answers": [],
        }
        correct_key = q.get("correct", "")
        for key, option_text in q.get("options", {}).items():
            canvas_q["answers"].append({"answer_text": option_text, "answer_weight": 100 if key == correct_key else 0})
        canvas_quiz["questions"].append(canvas_q)
    return json.dumps(canvas_quiz, indent=2, ensure_ascii=False)


def validate_moodle_xml(xml_string: str) -> List[str]:
    """Validate Moodle XML structure."""
    errors = []
    try:
        root = ET.fromstring(xml_string)
    except ET.ParseError as e:
        return [f"XML parse error: {e}"]
    if root.tag != "quiz":
        errors.append(f"Root element should be 'quiz', got '{root.tag}'")
    questions = root.findall("question")
    if not questions:
        errors.append("No questions found in quiz")
    for i, q in enumerate(questions):
        if q.get("type") != "multichoice":
            errors.append(f"Question {i+1}: expected type 'multichoice'")
        answers = q.findall("answer")
        if len(answers) < 2:
            errors.append(f"Question {i+1}: needs at least 2 answers")
        correct_count = sum(1 for a in answers if a.get("fraction") == "100")
        if correct_count != 1:
            errors.append(f"Question {i+1}: expected 1 correct answer, got {correct_count}")
    return errors


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_CASES
# ═══════════════════════════════════════════════════════════════════════════════
class TestMoodleExport(unittest.TestCase):
    """Tests for Moodle XML export."""

    def test_export_produces_valid_xml(self) -> None:
        xml_output = export_to_moodle_xml(SAMPLE_QUIZ)
        root = ET.fromstring(xml_output)
        self.assertEqual(root.tag, "quiz")

    def test_export_contains_question(self) -> None:
        xml_output = export_to_moodle_xml(SAMPLE_QUIZ)
        root = ET.fromstring(xml_output)
        self.assertEqual(len(root.findall("question")), 1)

    def test_validate_moodle_xml_passes(self) -> None:
        xml_output = export_to_moodle_xml(SAMPLE_QUIZ)
        errors = validate_moodle_xml(xml_output)
        self.assertEqual(errors, [], f"Validation errors: {errors}")


class TestCanvasExport(unittest.TestCase):
    """Tests for Canvas JSON export."""

    def test_export_produces_valid_json(self) -> None:
        json_output = export_to_canvas_json(SAMPLE_QUIZ)
        data = json.loads(json_output)
        self.assertIn("quiz", data)
        self.assertIn("questions", data)

    def test_export_contains_question(self) -> None:
        json_output = export_to_canvas_json(SAMPLE_QUIZ)
        data = json.loads(json_output)
        self.assertEqual(len(data["questions"]), 1)

    def test_points_calculation(self) -> None:
        json_output = export_to_canvas_json(SAMPLE_QUIZ)
        data = json.loads(json_output)
        self.assertEqual(data["quiz"]["points_possible"], 1)


class TestQuizFileIntegrity(unittest.TestCase):
    """Tests for quiz file integrity."""

    def test_quiz_yaml_exists(self) -> None:
        quiz_file = PROJECT_ROOT / "formative" / "quiz.yaml"
        self.assertTrue(quiz_file.exists(), "formative/quiz.yaml not found")

    def test_quiz_json_exists(self) -> None:
        quiz_file = PROJECT_ROOT / "formative" / "quiz.json"
        self.assertTrue(quiz_file.exists(), "formative/quiz.json not found")


if __name__ == "__main__":
    unittest.main(verbosity=2)
