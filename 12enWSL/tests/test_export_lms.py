#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_DOCSTRING
# ═══════════════════════════════════════════════════════════════════════════════
"""
Unit Tests for LMS Export Tool — Week 12
========================================
Computer Networks - ASE, CSIE | by ing. dr. Antonio Clim

Tests for formative/export_lms.py functionality.

Run with: pytest tests/test_export_lms.py -v
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from formative.export_lms import (
    load_quiz,
    validate_quiz,
    export_moodle_xml,
    export_canvas_qti,
    export_csv,
    _get_csv_headers,
    _question_to_csv_row,
)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_FIXTURES
# ═══════════════════════════════════════════════════════════════════════════════
@pytest.fixture
def sample_quiz():
    """Create a minimal valid quiz structure."""
    return {
        "metadata": {
            "week": 12,
            "topic": "Email Protocols and RPC",
            "version": "1.0.0"
        },
        "questions": [
            {
                "id": "q1",
                "type": "multiple_choice",
                "lo_ref": "LO1",
                "difficulty": "basic",
                "bloom_level": "remember",
                "stem": "What response code does SMTP DATA return?",
                "options": {
                    "a": "250 OK",
                    "b": "354 Start mail input",
                    "c": "220 Service ready",
                    "d": "221 Bye"
                },
                "correct": "b",
                "explanation": "DATA returns 354 to signal readiness for message content.",
                "points": 1
            },
            {
                "id": "q2",
                "type": "fill_blank",
                "lo_ref": "LO2",
                "difficulty": "intermediate",
                "bloom_level": "understand",
                "stem": "The RPC serialisation format used by gRPC is called ______.",
                "correct": ["Protocol Buffers", "protobuf", "Protobuf"],
                "explanation": "gRPC uses Protocol Buffers for binary serialisation.",
                "points": 1
            }
        ]
    }


@pytest.fixture
def quiz_json_file(sample_quiz, tmp_path):
    """Create a temporary quiz JSON file."""
    quiz_path = tmp_path / "test_quiz.json"
    with open(quiz_path, "w", encoding="utf-8") as f:
        json.dump(sample_quiz, f)
    return quiz_path


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════
class TestValidation:
    """Tests for quiz validation."""
    
    def test_valid_quiz_passes(self, sample_quiz):
        """A well-formed quiz should pass validation."""
        errors = validate_quiz(sample_quiz)
        assert errors == [], f"Expected no errors, got: {errors}"
    
    def test_missing_metadata_fails(self, sample_quiz):
        """Quiz without metadata should fail."""
        del sample_quiz["metadata"]
        errors = validate_quiz(sample_quiz)
        assert "Missing 'metadata' section" in errors
    
    def test_missing_questions_fails(self, sample_quiz):
        """Quiz without questions should fail."""
        del sample_quiz["questions"]
        errors = validate_quiz(sample_quiz)
        assert "Missing 'questions' section" in errors
    
    def test_missing_question_id_fails(self, sample_quiz):
        """Question without id should fail."""
        del sample_quiz["questions"][0]["id"]
        errors = validate_quiz(sample_quiz)
        assert any("missing 'id'" in e for e in errors)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_MOODLE_EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
class TestMoodleExport:
    """Tests for Moodle XML export."""
    
    def test_export_creates_valid_xml(self, sample_quiz, tmp_path):
        """Exported Moodle XML should be valid and parsable."""
        output = tmp_path / "test_moodle.xml"
        export_moodle_xml(sample_quiz, output)
        
        assert output.exists()
        tree = ET.parse(output)
        root = tree.getroot()
        assert root.tag == "quiz"
    
    def test_export_contains_all_questions(self, sample_quiz, tmp_path):
        """All questions should appear in the export."""
        output = tmp_path / "test_moodle.xml"
        export_moodle_xml(sample_quiz, output)
        
        tree = ET.parse(output)
        root = tree.getroot()
        questions = [q for q in root.findall("question") if q.get("type") != "category"]
        assert len(questions) == len(sample_quiz["questions"])
    
    def test_mcq_has_correct_answer_marked(self, sample_quiz, tmp_path):
        """Multiple choice questions should have correct answer marked."""
        output = tmp_path / "test_moodle.xml"
        export_moodle_xml(sample_quiz, output)
        
        tree = ET.parse(output)
        root = tree.getroot()
        mcq = root.find(".//question[@type='multichoice']")
        assert mcq is not None
        
        answers = mcq.findall("answer")
        correct_count = sum(1 for a in answers if a.get("fraction") == "100")
        assert correct_count == 1, "Exactly one answer should be marked correct"


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_CANVAS_EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
class TestCanvasExport:
    """Tests for Canvas QTI export."""
    
    def test_export_creates_valid_xml(self, sample_quiz, tmp_path):
        """Exported Canvas QTI should be valid and parsable."""
        output = tmp_path / "test_canvas.xml"
        export_canvas_qti(sample_quiz, output)
        
        assert output.exists()
        tree = ET.parse(output)
        root = tree.getroot()
        assert root.tag == "questestinterop"
    
    def test_export_has_assessment(self, sample_quiz, tmp_path):
        """Export should contain assessment element."""
        output = tmp_path / "test_canvas.xml"
        export_canvas_qti(sample_quiz, output)
        
        tree = ET.parse(output)
        root = tree.getroot()
        assessment = root.find("assessment")
        assert assessment is not None
        assert "Week 12" in assessment.get("title", "")
    
    def test_export_contains_items(self, sample_quiz, tmp_path):
        """All questions should appear as items."""
        output = tmp_path / "test_canvas.xml"
        export_canvas_qti(sample_quiz, output)
        
        tree = ET.parse(output)
        root = tree.getroot()
        items = root.findall(".//item")
        assert len(items) == len(sample_quiz["questions"])


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_CSV_EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
class TestCSVExport:
    """Tests for CSV export."""
    
    def test_export_creates_file(self, sample_quiz, tmp_path):
        """CSV export should create a file."""
        output = tmp_path / "test_quiz.csv"
        export_csv(sample_quiz, output)
        assert output.exists()
    
    def test_csv_has_correct_headers(self):
        """CSV headers should match expected columns."""
        headers = _get_csv_headers()
        assert "id" in headers
        assert "stem" in headers
        assert "correct" in headers
        assert "lo_ref" in headers
    
    def test_csv_has_correct_row_count(self, sample_quiz, tmp_path):
        """CSV should have header + one row per question."""
        output = tmp_path / "test_quiz.csv"
        export_csv(sample_quiz, output)
        
        with open(output, "r", encoding="utf-8") as f:
            lines = f.readlines()
        assert len(lines) == len(sample_quiz["questions"]) + 1
    
    def test_csv_encoding_utf8(self, sample_quiz, tmp_path):
        """CSV should be UTF-8 encoded."""
        sample_quiz["questions"][0]["stem"] = "Test with UTF-8: äöü"
        output = tmp_path / "test_quiz.csv"
        export_csv(sample_quiz, output)
        
        content = output.read_text(encoding="utf-8")
        assert "äöü" in content
    
    def test_question_to_row_mcq(self, sample_quiz):
        """MCQ should convert to correct row format."""
        q = sample_quiz["questions"][0]
        row = _question_to_csv_row(q)
        assert row[0] == "q1"
        assert row[10] == "b"


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_LOAD_QUIZ
# ═══════════════════════════════════════════════════════════════════════════════
class TestLoadQuiz:
    """Tests for quiz loading."""
    
    def test_load_from_json(self, quiz_json_file, sample_quiz):
        """Should load quiz from JSON file correctly."""
        loaded = load_quiz(quiz_json_file)
        assert loaded["metadata"]["week"] == sample_quiz["metadata"]["week"]
        assert len(loaded["questions"]) == len(sample_quiz["questions"])
    
    def test_load_nonexistent_file_raises(self, tmp_path):
        """Loading non-existent file should raise error."""
        with pytest.raises(FileNotFoundError):
            load_quiz(tmp_path / "nonexistent.json")


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
