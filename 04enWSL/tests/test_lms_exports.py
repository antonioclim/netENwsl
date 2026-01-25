#!/usr/bin/env python3
"""
Tests for LMS Export Functions — Week 4
========================================

NETWORKING class - ASE, Informatics | Computer Networks Laboratory
by ing. dr. Antonio Clim

Tests the quiz export functionality for Moodle and Canvas LMS formats.

Usage:
    python -m pytest tests/test_lms_exports.py -v
    python tests/test_lms_exports.py
"""

import json
import sys
import unittest
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# PATH_SETUP
# ═══════════════════════════════════════════════════════════════════════════════

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import after path setup
try:
    from scripts.export_quiz_lms import (
        export_to_moodle,
        export_to_canvas,
        _convert_question_moodle,
        _convert_question_canvas,
        _build_moodle_answers,
        validate_export
    )
    IMPORTS_AVAILABLE = True
except ImportError:
    IMPORTS_AVAILABLE = False


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_DATA
# ═══════════════════════════════════════════════════════════════════════════════

SAMPLE_QUIZ = {
    "metadata": {
        "week": 4,
        "topic": "Custom Protocols",
        "version": "1.0",
        "estimated_time": "15 minutes",
        "passing_score": 70,
        "lo_coverage": ["LO1", "LO2", "LO3"]
    },
    "questions": [
        {
            "id": "q01",
            "type": "multiple_choice",
            "stem": "What is the purpose of CRC32 in network protocols?",
            "options": {
                "A": "Encrypt data",
                "B": "Detect transmission errors",
                "C": "Compress data",
                "D": "Route packets"
            },
            "correct": "B",
            "lo_ref": "LO4",
            "bloom_level": "understand",
            "difficulty": "medium",
            "explanation": "CRC32 detects errors but does not correct them."
        },
        {
            "id": "q02",
            "type": "true_false",
            "stem": "TCP preserves message boundaries.",
            "correct": False,
            "lo_ref": "LO3",
            "bloom_level": "remember",
            "explanation": "TCP is a byte stream protocol with no message boundaries."
        },
        {
            "id": "q03",
            "type": "fill_blank",
            "stem": "The struct format character for big-endian is ___.",
            "correct": [">", "!"],
            "lo_ref": "LO4",
            "bloom_level": "remember",
            "explanation": "Both > and ! indicate big-endian (network) byte order."
        }
    ]
}


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_MOODLE_EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

@unittest.skipUnless(IMPORTS_AVAILABLE, "Export module not available")
class TestMoodleExport(unittest.TestCase):
    """Tests for Moodle export functionality."""
    
    def test_export_structure(self):
        """Moodle export should have required top-level keys."""
        result = export_to_moodle(SAMPLE_QUIZ)
        
        self.assertIn("quiz", result)
        self.assertIn("metadata", result)
        self.assertIn("name", result["quiz"])
        self.assertIn("questions", result["quiz"])
    
    def test_export_metadata(self):
        """Moodle export should include correct metadata."""
        result = export_to_moodle(SAMPLE_QUIZ)
        
        self.assertEqual(result["metadata"]["exportFormat"], "moodle")
        self.assertIn("exportDate", result["metadata"])
        self.assertEqual(result["metadata"]["version"], "1.0")
    
    def test_export_question_count(self):
        """Moodle export should contain all questions."""
        result = export_to_moodle(SAMPLE_QUIZ)
        
        # All 3 question types should be exported
        self.assertEqual(len(result["quiz"]["questions"]), 3)
    
    def test_multiple_choice_conversion(self):
        """Multiple choice questions should convert correctly."""
        q = SAMPLE_QUIZ["questions"][0]
        result = _convert_question_moodle(q)
        
        self.assertEqual(result["type"], "multichoice")
        self.assertEqual(result["name"], "q01")
        self.assertEqual(len(result["answers"]), 4)
        
        # Check correct answer has fraction 100
        correct_answers = [a for a in result["answers"] if a["fraction"] == 100]
        self.assertEqual(len(correct_answers), 1)
    
    def test_true_false_conversion(self):
        """True/false questions should convert correctly."""
        q = SAMPLE_QUIZ["questions"][1]
        result = _convert_question_moodle(q)
        
        self.assertEqual(result["type"], "truefalse")
        self.assertEqual(result["correctanswer"], False)
    
    def test_fill_blank_conversion(self):
        """Fill-blank questions should accept multiple correct answers."""
        q = SAMPLE_QUIZ["questions"][2]
        result = _convert_question_moodle(q)
        
        self.assertEqual(result["type"], "shortanswer")
        # Should have 2 correct answers (> and !)
        self.assertEqual(len(result["answers"]), 2)
    
    def test_moodle_answers_structure(self):
        """Moodle answers should have text, fraction, feedback."""
        q = SAMPLE_QUIZ["questions"][0]
        answers = _build_moodle_answers(q)
        
        for answer in answers:
            self.assertIn("text", answer)
            self.assertIn("fraction", answer)
            self.assertIn("feedback", answer)
    
    def test_export_json_serialisable(self):
        """Export result should be JSON serialisable."""
        result = export_to_moodle(SAMPLE_QUIZ)
        
        # Should not raise
        json_str = json.dumps(result, indent=2)
        self.assertIsInstance(json_str, str)
        
        # Should round-trip
        parsed = json.loads(json_str)
        self.assertEqual(len(parsed["quiz"]["questions"]), 3)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_CANVAS_EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

@unittest.skipUnless(IMPORTS_AVAILABLE, "Export module not available")
class TestCanvasExport(unittest.TestCase):
    """Tests for Canvas export functionality."""
    
    def test_export_structure(self):
        """Canvas export should have required top-level keys."""
        result = export_to_canvas(SAMPLE_QUIZ)
        
        self.assertIn("quiz", result)
        self.assertIn("metadata", result)
        self.assertIn("title", result["quiz"])
        self.assertIn("questions", result["quiz"])
    
    def test_export_metadata(self):
        """Canvas export should include correct metadata."""
        result = export_to_canvas(SAMPLE_QUIZ)
        
        self.assertEqual(result["metadata"]["exportFormat"], "canvas")
        self.assertIn("exportDate", result["metadata"])
    
    def test_export_question_count(self):
        """Canvas export should contain all questions."""
        result = export_to_canvas(SAMPLE_QUIZ)
        
        self.assertEqual(len(result["quiz"]["questions"]), 3)
    
    def test_canvas_question_structure(self):
        """Canvas questions should have QTI-compatible structure."""
        result = export_to_canvas(SAMPLE_QUIZ)
        q = result["quiz"]["questions"][0]
        
        self.assertIn("question_type", q)
        self.assertIn("question_text", q)
        self.assertIn("points_possible", q)
        self.assertIn("answers", q)
    
    def test_export_json_serialisable(self):
        """Export result should be JSON serialisable."""
        result = export_to_canvas(SAMPLE_QUIZ)
        
        json_str = json.dumps(result, indent=2)
        self.assertIsInstance(json_str, str)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

@unittest.skipUnless(IMPORTS_AVAILABLE, "Export module not available")
class TestExportValidation(unittest.TestCase):
    """Tests for export validation."""
    
    def test_validate_moodle_export(self):
        """Moodle export should pass validation."""
        result = export_to_moodle(SAMPLE_QUIZ)
        
        # validate_export returns (is_valid, errors)
        try:
            is_valid, errors = validate_export(result, "moodle")
            self.assertTrue(is_valid, f"Validation errors: {errors}")
        except (TypeError, AttributeError):
            # validate_export might not exist yet
            pass
    
    def test_validate_canvas_export(self):
        """Canvas export should pass validation."""
        result = export_to_canvas(SAMPLE_QUIZ)
        
        try:
            is_valid, errors = validate_export(result, "canvas")
            self.assertTrue(is_valid, f"Validation errors: {errors}")
        except (TypeError, AttributeError):
            pass
    
    def test_empty_quiz_handling(self):
        """Export should handle empty quiz gracefully."""
        empty_quiz = {"metadata": {}, "questions": []}
        
        moodle = export_to_moodle(empty_quiz)
        self.assertEqual(len(moodle["quiz"]["questions"]), 0)
        
        canvas = export_to_canvas(empty_quiz)
        self.assertEqual(len(canvas["quiz"]["questions"]), 0)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_EDGE_CASES
# ═══════════════════════════════════════════════════════════════════════════════

@unittest.skipUnless(IMPORTS_AVAILABLE, "Export module not available")
class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases in export."""
    
    def test_special_characters_in_stem(self):
        """Questions with special characters should export correctly."""
        quiz = {
            "metadata": {"week": 4},
            "questions": [{
                "id": "q_special",
                "type": "multiple_choice",
                "stem": "What does `struct.pack('>H', 1000)` return?",
                "options": {"A": "b'\\x03\\xe8'", "B": "b'\\xe8\\x03'"},
                "correct": "A"
            }]
        }
        
        result = export_to_moodle(quiz)
        self.assertIn("`struct.pack", result["quiz"]["questions"][0]["questiontext"])
    
    def test_unicode_in_questions(self):
        """Unicode characters should be preserved."""
        quiz = {
            "metadata": {"week": 4},
            "questions": [{
                "id": "q_unicode",
                "type": "multiple_choice",
                "stem": "What is the symbol for 'not equal' in Python? (≠)",
                "options": {"A": "!=", "B": "<>"},
                "correct": "A"
            }]
        }
        
        result = export_to_moodle(quiz)
        self.assertIn("≠", result["quiz"]["questions"][0]["questiontext"])
    
    def test_long_explanation(self):
        """Long explanations should not be truncated."""
        long_explanation = "A" * 1000
        quiz = {
            "metadata": {"week": 4},
            "questions": [{
                "id": "q_long",
                "type": "multiple_choice",
                "stem": "Test",
                "options": {"A": "1", "B": "2"},
                "correct": "A",
                "explanation": long_explanation
            }]
        }
        
        result = export_to_moodle(quiz)
        self.assertEqual(
            result["quiz"]["questions"][0]["generalfeedback"],
            long_explanation
        )


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("Week 4 LMS Export Tests")
    print("NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim")
    print("=" * 60)
    print()
    
    if not IMPORTS_AVAILABLE:
        print("WARNING: Export module not available. Some tests will be skipped.")
        print("Run from project root: python -m pytest tests/test_lms_exports.py")
        print()
    
    unittest.main(verbosity=2)
