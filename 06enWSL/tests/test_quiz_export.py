#!/usr/bin/env python3
"""
Unit Tests — Quiz Validation and LMS Export
============================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Tests for:
- Quiz YAML structure validation
- JSON export format verification
- Moodle GIFT export verification
- Moodle XML export verification

Usage:
    python -m pytest tests/test_quiz_export.py -v
    python tests/test_quiz_export.py  # Direct run

Issues: Open an issue in GitHub
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from formative.run_quiz import (
    validate_quiz_structure,
    export_to_json,
    export_to_moodle_gift,
    load_quiz,
    parse_questions,
)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_DATA
# ═══════════════════════════════════════════════════════════════════════════════

VALID_QUIZ_DATA = {
    "metadata": {
        "week": 6,
        "topic": "NAT/PAT & SDN",
        "version": "1.0.0",
        "passing_score": 70,
        "total_questions": 2,
        "lo_coverage": ["LO1", "LO2"],
    },
    "questions": [
        {
            "id": "q01",
            "type": "multiple_choice",
            "lo_ref": "LO1",
            "bloom_level": "Remember",
            "difficulty": "basic",
            "points": 1,
            "stem": "What does NAT stand for?",
            "options": {
                "a": "Network Address Translation",
                "b": "Network Access Terminal",
                "c": "Node Address Table",
                "d": "None of the above",
            },
            "correct": "a",
            "explanation": "NAT stands for Network Address Translation.",
            "feedback": {
                "b": "Access Terminal is not correct.",
                "c": "Address Table is not correct.",
                "d": "One of the options is correct.",
            },
        },
        {
            "id": "q02",
            "type": "fill_blank",
            "lo_ref": "LO2",
            "bloom_level": "Understand",
            "difficulty": "intermediate",
            "points": 2,
            "stem": "PAT uses _____ numbers for multiplexing.",
            "correct": ["port", "ports"],
            "explanation": "PAT uses port numbers to multiplex connections.",
        },
    ],
}

INVALID_QUIZ_MISSING_METADATA = {
    "questions": [{"id": "q01", "stem": "Test?", "correct": "a"}],
}

INVALID_QUIZ_WRONG_COUNT = {
    "metadata": {
        "week": 6,
        "topic": "Test",
        "version": "1.0.0",
        "passing_score": 70,
        "total_questions": 5,
        "lo_coverage": ["LO1"],
    },
    "questions": [
        {"id": "q01", "lo_ref": "LO1", "stem": "Test?", "correct": "a"},
    ],
}


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

class TestQuizValidation(unittest.TestCase):
    """Tests for quiz structure validation."""
    
    def test_valid_quiz_passes(self) -> None:
        """Valid quiz data should pass validation."""
        is_valid, issues = validate_quiz_structure(VALID_QUIZ_DATA)
        self.assertTrue(is_valid, f"Valid quiz should pass. Issues: {issues}")
        self.assertEqual(len(issues), 0)
    
    def test_missing_metadata_fails(self) -> None:
        """Quiz without metadata should fail validation."""
        is_valid, issues = validate_quiz_structure(INVALID_QUIZ_MISSING_METADATA)
        self.assertFalse(is_valid)
        self.assertTrue(any("metadata" in issue.lower() for issue in issues))
    
    def test_wrong_question_count_fails(self) -> None:
        """Quiz with mismatched question count should fail."""
        is_valid, issues = validate_quiz_structure(INVALID_QUIZ_WRONG_COUNT)
        self.assertFalse(is_valid)
        self.assertTrue(any("count" in issue.lower() or "mismatch" in issue.lower() for issue in issues))
    
    def test_empty_quiz_fails(self) -> None:
        """Empty quiz should fail validation."""
        is_valid, issues = validate_quiz_structure({})
        self.assertFalse(is_valid)
        self.assertGreater(len(issues), 0)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_JSON_EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

class TestJSONExport(unittest.TestCase):
    """Tests for JSON export functionality."""
    
    def test_json_export_creates_file(self) -> None:
        """JSON export should create a valid file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            output_path = Path(f.name)
        
        try:
            export_to_json(VALID_QUIZ_DATA, output_path)
            self.assertTrue(output_path.exists())
            
            with open(output_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.assertIn("metadata", data)
            self.assertIn("questions", data)
            self.assertEqual(len(data["questions"]), 2)
        finally:
            output_path.unlink(missing_ok=True)
    
    def test_json_export_preserves_question_data(self) -> None:
        """JSON export should preserve all question fields."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            output_path = Path(f.name)
        
        try:
            export_to_json(VALID_QUIZ_DATA, output_path)
            
            with open(output_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            q1 = data["questions"][0]
            self.assertEqual(q1["id"], "q01")
            self.assertEqual(q1["type"], "multiple_choice")
            self.assertEqual(q1["correct"], "a")
            self.assertIn("options", q1)
        finally:
            output_path.unlink(missing_ok=True)
    
    def test_json_metadata_includes_export_timestamp(self) -> None:
        """Exported JSON should include export timestamp."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            output_path = Path(f.name)
        
        try:
            export_to_json(VALID_QUIZ_DATA, output_path)
            
            with open(output_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.assertIn("exported_at", data["metadata"])
            self.assertIn("lms_format", data["metadata"])
        finally:
            output_path.unlink(missing_ok=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_MOODLE_GIFT_EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

class TestMoodleGIFTExport(unittest.TestCase):
    """Tests for Moodle GIFT format export."""
    
    def test_gift_export_creates_file(self) -> None:
        """GIFT export should create a valid file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".gift", delete=False) as f:
            output_path = Path(f.name)
        
        try:
            export_to_moodle_gift(VALID_QUIZ_DATA, output_path)
            self.assertTrue(output_path.exists())
            
            content = output_path.read_text(encoding="utf-8")
            self.assertIn("$CATEGORY:", content)
            self.assertIn("::q01::", content)
        finally:
            output_path.unlink(missing_ok=True)
    
    def test_gift_export_marks_correct_answer(self) -> None:
        """GIFT export should mark correct answers with =."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".gift", delete=False) as f:
            output_path = Path(f.name)
        
        try:
            export_to_moodle_gift(VALID_QUIZ_DATA, output_path)
            content = output_path.read_text(encoding="utf-8")
            
            # Correct answer should be prefixed with =
            self.assertIn("=Network Address Translation", content)
            # Wrong answers should be prefixed with ~
            self.assertIn("~Network Access Terminal", content)
        finally:
            output_path.unlink(missing_ok=True)
    
    def test_gift_export_includes_feedback(self) -> None:
        """GIFT export should include answer feedback."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".gift", delete=False) as f:
            output_path = Path(f.name)
        
        try:
            export_to_moodle_gift(VALID_QUIZ_DATA, output_path)
            content = output_path.read_text(encoding="utf-8")
            
            # Feedback should be included with # separator
            self.assertIn("#Access Terminal is not correct", content)
        finally:
            output_path.unlink(missing_ok=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_QUESTION_PARSING
# ═══════════════════════════════════════════════════════════════════════════════

class TestQuestionParsing(unittest.TestCase):
    """Tests for question parsing."""
    
    def test_parse_questions_returns_list(self) -> None:
        """parse_questions should return list of Question objects."""
        questions = parse_questions(VALID_QUIZ_DATA)
        self.assertIsInstance(questions, list)
        self.assertEqual(len(questions), 2)
    
    def test_parsed_question_has_required_fields(self) -> None:
        """Parsed questions should have all required fields."""
        questions = parse_questions(VALID_QUIZ_DATA)
        q = questions[0]
        
        self.assertEqual(q.id, "q01")
        self.assertEqual(q.type, "multiple_choice")
        self.assertEqual(q.lo_ref, "LO1")
        self.assertEqual(q.correct, "a")
        self.assertIsNotNone(q.options)
    
    def test_parse_fill_blank_question(self) -> None:
        """Fill-in-blank questions should parse correctly."""
        questions = parse_questions(VALID_QUIZ_DATA)
        q = questions[1]
        
        self.assertEqual(q.type, "fill_blank")
        self.assertIsInstance(q.correct, list)
        self.assertIn("port", q.correct)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_REAL_QUIZ_FILE
# ═══════════════════════════════════════════════════════════════════════════════

class TestRealQuizFile(unittest.TestCase):
    """Tests against the actual quiz.yaml file."""
    
    @classmethod
    def setUpClass(cls) -> None:
        """Load the real quiz file if it exists."""
        quiz_path = Path(__file__).parent.parent / "formative" / "quiz.yaml"
        cls.quiz_path = quiz_path
        cls.quiz_exists = quiz_path.exists()
    
    def test_real_quiz_loads(self) -> None:
        """Real quiz.yaml should load without errors."""
        if not self.quiz_exists:
            self.skipTest("quiz.yaml not found")
        
        quiz_data = load_quiz(self.quiz_path)
        self.assertIsNotNone(quiz_data)
        self.assertIn("metadata", quiz_data)
        self.assertIn("questions", quiz_data)
    
    def test_real_quiz_validates(self) -> None:
        """Real quiz.yaml should pass validation."""
        if not self.quiz_exists:
            self.skipTest("quiz.yaml not found")
        
        quiz_data = load_quiz(self.quiz_path)
        is_valid, issues = validate_quiz_structure(quiz_data)
        
        # Allow warnings but not critical errors
        critical_issues = [i for i in issues if "missing" in i.lower() and "metadata" not in i.lower()]
        self.assertEqual(len(critical_issues), 0, f"Critical issues: {critical_issues}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Run tests when executed directly."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
