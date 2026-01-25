#!/usr/bin/env python3
"""
Unit Tests for Quiz Validation and LMS Export — Week 11
NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim

Tests cover:
- Quiz YAML structure validation
- Quiz JSON (LMS) export format
- Question completeness checks
- Answer validation
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from typing import Any, Dict

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


def load_quiz_yaml() -> Dict[str, Any]:
    """Load quiz.yaml file."""
    quiz_path = PROJECT_ROOT / "formative" / "quiz.yaml"
    if not quiz_path.exists():
        raise FileNotFoundError(f"Quiz YAML not found: {quiz_path}")
    with open(quiz_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_quiz_json() -> Dict[str, Any]:
    """Load quiz.json file (LMS export)."""
    quiz_path = PROJECT_ROOT / "formative" / "quiz.json"
    if not quiz_path.exists():
        raise FileNotFoundError(f"Quiz JSON not found: {quiz_path}")
    with open(quiz_path, "r", encoding="utf-8") as f:
        return json.load(f)


@unittest.skipUnless(YAML_AVAILABLE, "PyYAML not installed")
class TestQuizYAMLStructure(unittest.TestCase):
    """Test quiz.yaml structure and completeness."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.quiz = load_quiz_yaml()

    def test_has_metadata_section(self) -> None:
        self.assertIn("metadata", self.quiz)

    def test_has_questions_section(self) -> None:
        self.assertIn("questions", self.quiz)
        self.assertGreater(len(self.quiz["questions"]), 0)

    def test_question_required_fields(self) -> None:
        required = ["id", "type", "stem", "correct"]
        for i, q in enumerate(self.quiz["questions"]):
            for field in required:
                self.assertIn(field, q)

    def test_question_ids_unique(self) -> None:
        ids = [q["id"] for q in self.quiz["questions"]]
        self.assertEqual(len(ids), len(set(ids)))


class TestQuizJSONExport(unittest.TestCase):
    """Test quiz.json LMS export format."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.quiz = load_quiz_json()

    def test_has_metadata(self) -> None:
        self.assertIn("metadata", self.quiz)

    def test_has_questions(self) -> None:
        self.assertIn("questions", self.quiz)

    def test_lms_compatibility_declared(self) -> None:
        metadata = self.quiz["metadata"]
        self.assertIn("lms_compatibility", metadata)


def main() -> None:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestQuizYAMLStructure))
    suite.addTests(loader.loadTestsFromTestCase(TestQuizJSONExport))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
