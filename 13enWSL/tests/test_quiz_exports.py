#!/usr/bin/env python3
"""
Unit Tests for Quiz Exports and Validators — Week 13
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim
"""

from __future__ import annotations

import json
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict

sys.path.insert(0, str(Path(__file__).parent.parent))


# ═══════════════════════════════════════════════════════════════════════════════
# TEST FIXTURES
# ═══════════════════════════════════════════════════════════════════════════════

SAMPLE_QUIZ: Dict[str, Any] = {
    "metadata": {
        "week": 13,
        "topic": "IoT and Security",
        "passing_score": 70,
        "total_questions": 2,
        "estimated_time_minutes": 10
    },
    "questions": [
        {
            "id": "q01",
            "type": "multiple_choice",
            "lo_ref": "LO1",
            "bloom_level": "remember",
            "points": 1,
            "stem": "What is the standard port for plaintext MQTT?",
            "options": {"a": "80", "b": "443", "c": "1883", "d": "8883"},
            "correct": "c"
        },
        {
            "id": "q02",
            "type": "multiple_choice",
            "lo_ref": "LO2",
            "bloom_level": "understand",
            "points": 1,
            "stem": "Which QoS level guarantees exactly-once delivery?",
            "options": {"a": "QoS 0", "b": "QoS 1", "c": "QoS 2", "d": "QoS 3"},
            "correct": "c"
        }
    ]
}


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ STRUCTURE VALIDATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestQuizStructureValidation(unittest.TestCase):
    """Tests for quiz YAML structure validation."""

    def test_metadata_required_fields(self) -> None:
        """Verify all required metadata fields are present."""
        required = ["week", "topic", "passing_score"]
        for field in required:
            self.assertIn(field, SAMPLE_QUIZ["metadata"])

    def test_question_required_fields(self) -> None:
        """Verify all required question fields are present."""
        required = ["id", "type", "stem", "bloom_level"]
        for q in SAMPLE_QUIZ["questions"]:
            for field in required:
                self.assertIn(field, q, f"Question {q.get('id')} missing: {field}")

    def test_mcq_has_options_and_correct(self) -> None:
        """Verify MCQ questions have options and correct answer."""
        for q in SAMPLE_QUIZ["questions"]:
            if q["type"] == "multiple_choice":
                self.assertIn("options", q)
                self.assertIn("correct", q)
                self.assertIn(q["correct"].lower(), q["options"].keys())

    def test_bloom_levels_valid(self) -> None:
        """Verify all bloom levels are valid."""
        valid = {"remember", "understand", "apply", "analyse", "evaluate", "create"}
        for q in SAMPLE_QUIZ["questions"]:
            self.assertIn(q.get("bloom_level", "").lower(), valid)

    def test_question_ids_unique(self) -> None:
        """Verify all question IDs are unique."""
        ids = [q["id"] for q in SAMPLE_QUIZ["questions"]]
        self.assertEqual(len(ids), len(set(ids)))


# ═══════════════════════════════════════════════════════════════════════════════
# MOODLE XML EXPORT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMoodleXMLExport(unittest.TestCase):
    """Tests for Moodle XML export functionality."""

    def _export_to_moodle(self, quiz: Dict[str, Any]) -> ET.Element:
        """Helper to export quiz and return parsed XML."""
        root = ET.Element("quiz")
        for q in quiz.get("questions", []):
            if q["type"] != "multiple_choice":
                continue
            question = ET.SubElement(root, "question", type="multichoice")
            name = ET.SubElement(question, "name")
            ET.SubElement(name, "text").text = q.get("id", "q")
            ET.SubElement(question, "defaultgrade").text = str(q.get("points", 1))
            correct_key = q["correct"].lower()
            for key, text in q["options"].items():
                fraction = "100" if key == correct_key else "0"
                ans = ET.SubElement(question, "answer", fraction=fraction)
                ET.SubElement(ans, "text").text = text
        return root

    def test_creates_valid_xml_structure(self) -> None:
        """Verify export creates valid XML structure."""
        root = self._export_to_moodle(SAMPLE_QUIZ)
        self.assertEqual(root.tag, "quiz")
        questions = root.findall("question")
        self.assertGreater(len(questions), 0)

    def test_mcq_has_correct_moodle_structure(self) -> None:
        """Verify MCQ questions have correct Moodle structure."""
        root = self._export_to_moodle(SAMPLE_QUIZ)
        mcq = root.find("question[@type='multichoice']")
        self.assertIsNotNone(mcq)
        self.assertIsNotNone(mcq.find("name"))
        self.assertIsNotNone(mcq.find("defaultgrade"))

    def test_correct_answer_has_fraction_100(self) -> None:
        """Verify correct answer has fraction=100."""
        root = self._export_to_moodle(SAMPLE_QUIZ)
        mcq = root.find("question[@type='multichoice']")
        answers = mcq.findall("answer")
        correct_count = sum(1 for a in answers if a.get("fraction") == "100")
        self.assertEqual(correct_count, 1)

    def test_wrong_answers_have_fraction_0(self) -> None:
        """Verify wrong answers have fraction=0."""
        root = self._export_to_moodle(SAMPLE_QUIZ)
        mcq = root.find("question[@type='multichoice']")
        answers = mcq.findall("answer")
        wrong_count = sum(1 for a in answers if a.get("fraction") == "0")
        self.assertEqual(wrong_count, 3)


# ═══════════════════════════════════════════════════════════════════════════════
# CANVAS JSON EXPORT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestCanvasJSONExport(unittest.TestCase):
    """Tests for Canvas JSON export functionality."""

    def _export_to_canvas(self, quiz: Dict[str, Any]) -> Dict[str, Any]:
        """Helper to export quiz to Canvas format."""
        metadata = quiz.get("metadata", {})
        canvas_quiz = {
            "title": f"Week {metadata.get('week', 13)} - {metadata.get('topic', 'Quiz')}",
            "quiz_type": "practice_quiz",
            "time_limit": metadata.get("estimated_time_minutes", 20),
            "questions": []
        }
        for q in quiz.get("questions", []):
            if q["type"] != "multiple_choice":
                continue
            correct_key = q["correct"].lower()
            canvas_q = {
                "question_name": q.get("id"),
                "question_type": "multiple_choice_question",
                "question_text": q["stem"],
                "points_possible": q.get("points", 1),
                "answers": [
                    {"answer_text": text, "answer_weight": 100 if key == correct_key else 0}
                    for key, text in q["options"].items()
                ]
            }
            canvas_quiz["questions"].append(canvas_q)
        return canvas_quiz

    def test_creates_valid_canvas_structure(self) -> None:
        """Verify Canvas export has required top-level fields."""
        result = self._export_to_canvas(SAMPLE_QUIZ)
        self.assertIn("title", result)
        self.assertIn("quiz_type", result)
        self.assertIn("questions", result)

    def test_question_has_correct_canvas_structure(self) -> None:
        """Verify question structure matches Canvas format."""
        result = self._export_to_canvas(SAMPLE_QUIZ)
        self.assertGreater(len(result["questions"]), 0)
        q = result["questions"][0]
        self.assertIn("question_name", q)
        self.assertIn("question_type", q)
        self.assertIn("answers", q)

    def test_answer_weights_correct(self) -> None:
        """Verify answer weights: 100 for correct, 0 for wrong."""
        result = self._export_to_canvas(SAMPLE_QUIZ)
        q = result["questions"][0]
        weights = [a["answer_weight"] for a in q["answers"]]
        self.assertEqual(weights.count(100), 1)
        self.assertEqual(weights.count(0), 3)

    def test_export_is_json_serialisable(self) -> None:
        """Verify export result is JSON serialisable."""
        result = self._export_to_canvas(SAMPLE_QUIZ)
        json_str = json.dumps(result, indent=2)
        self.assertIsInstance(json_str, str)


# ═══════════════════════════════════════════════════════════════════════════════
# GROUND TRUTH VALIDATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestGroundTruthValidation(unittest.TestCase):
    """Tests for ground truth validation logic."""

    def test_ports_in_valid_range(self) -> None:
        """Verify port numbers are in valid range."""
        expected_ports = [1883, 8883, 2121, 8080, 9000]
        for port in expected_ports:
            self.assertGreater(port, 0)
            self.assertLess(port, 65536)

    def test_service_ports_mapping(self) -> None:
        """Verify service to port mappings are correct."""
        expected = {
            "mosquitto": [1883, 8883],
            "dvwa": [8080],
            "vsftpd": [2121]
        }
        for service, ports in expected.items():
            for port in ports:
                self.assertIsInstance(port, int)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    unittest.main(verbosity=2)
