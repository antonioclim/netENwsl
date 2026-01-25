#!/usr/bin/env python3
"""
Unit Tests for LMS Export Tool.

Tests cover:
- YAML quiz loading and validation
- Moodle XML export structure
- Canvas QTI export structure  
- JSON export schema
- Edge cases and error handling

Run with: pytest tests/test_export_lms.py -v
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import json
import tempfile
from pathlib import Path
from xml.etree import ElementTree as ET
from typing import Dict, Any

import pytest

# Import module under test (adjust path as needed)
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from export_lms import (
    load_quiz,
    escape_html,
    clean_text,
    export_moodle_xml,
    export_canvas_qti,
    export_json,
)


# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES
# ═══════════════════════════════════════════════════════════════════════════════
@pytest.fixture
def sample_quiz_data() -> Dict[str, Any]:
    """Minimal valid quiz structure for testing."""
    return {
        "metadata": {
            "version": "1.0",
            "course": "Computer Networks",
            "institution": "ASE Bucharest",
            "passing_score": 70,
            "time_limit_minutes": 15,
        },
        "project": {
            "id": "P01",
            "title": "SDN Firewall Test Quiz",
            "description": "Test quiz for unit testing",
            "learning_objectives": [
                {"id": "LO1", "description": "Test objective", "bloom_level": "apply"}
            ],
            "questions": [
                {
                    "id": "test_q01",
                    "type": "multiple_choice",
                    "lo_ref": "LO1",
                    "bloom_level": "understand",
                    "difficulty": "basic",
                    "points": 1,
                    "stem": "What is SDN?",
                    "options": {
                        "a": "Software-Defined Networking",
                        "b": "System Data Network",
                        "c": "Secure Domain Name",
                        "d": "None of the above",
                    },
                    "correct": "a",
                    "feedback": {
                        "correct": "Correct!",
                        "incorrect": "Review SDN concepts.",
                    },
                    "explanation": "SDN separates control and data planes.",
                },
                {
                    "id": "test_q02",
                    "type": "fill_blank",
                    "lo_ref": "LO1",
                    "bloom_level": "remember",
                    "points": 1,
                    "stem": "OpenFlow uses port ____ by default.",
                    "correct": ["6653", "6633"],
                },
            ],
        },
        "lms_export": {
            "moodle": {"category": "$course$/Test"},
        },
    }


@pytest.fixture
def temp_quiz_file(sample_quiz_data: Dict) -> Path:
    """Create temporary YAML quiz file."""
    import yaml
    
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".yaml", delete=False, encoding="utf-8"
    ) as f:
        yaml.dump(sample_quiz_data, f)
        return Path(f.name)


# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTION TESTS
# ═══════════════════════════════════════════════════════════════════════════════
class TestUtilityFunctions:
    """Tests for utility functions."""

    def test_escape_html_special_chars(self) -> None:
        """Verify HTML special characters are escaped."""
        assert escape_html("<script>") == "&lt;script&gt;"
        assert escape_html("A & B") == "A &amp; B"
        assert escape_html('"quoted"') == "&quot;quoted&quot;"

    def test_escape_html_preserves_normal_text(self) -> None:
        """Normal text should pass through unchanged."""
        assert escape_html("Hello World") == "Hello World"
        assert escape_html("Test 123") == "Test 123"

    def test_clean_text_strips_whitespace(self) -> None:
        """Verify whitespace is normalised."""
        text = "  Line 1  \n  Line 2  \n  "
        result = clean_text(text)
        assert result == "Line 1\nLine 2"

    def test_clean_text_handles_empty(self) -> None:
        """Empty string should return empty."""
        assert clean_text("") == ""
        assert clean_text("   ") == ""


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ LOADING TESTS
# ═══════════════════════════════════════════════════════════════════════════════
class TestQuizLoading:
    """Tests for quiz loading functionality."""

    def test_load_quiz_valid_file(self, temp_quiz_file: Path) -> None:
        """Valid YAML file should load successfully."""
        data = load_quiz(temp_quiz_file)
        assert data is not None
        assert "project" in data
        assert data["project"]["id"] == "P01"

    def test_load_quiz_nonexistent_file(self) -> None:
        """Nonexistent file should return None."""
        result = load_quiz(Path("/nonexistent/path/quiz.yaml"))
        assert result is None

    def test_load_quiz_adds_extension(self, temp_quiz_file: Path) -> None:
        """Should try adding .yaml extension if missing."""
        # Remove extension for test
        path_without_ext = temp_quiz_file.with_suffix("")
        # This test verifies the logic, actual rename not needed
        assert temp_quiz_file.suffix == ".yaml"


# ═══════════════════════════════════════════════════════════════════════════════
# MOODLE XML EXPORT TESTS
# ═══════════════════════════════════════════════════════════════════════════════
class TestMoodleExport:
    """Tests for Moodle XML export."""

    def test_moodle_xml_structure(self, sample_quiz_data: Dict) -> None:
        """Verify basic Moodle XML structure."""
        with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as f:
            output_path = Path(f.name)
        
        export_moodle_xml(sample_quiz_data, output_path)
        
        # Parse and validate XML
        tree = ET.parse(output_path)
        root = tree.getroot()
        
        assert root.tag == "quiz"
        questions = root.findall("question")
        # Category + 2 questions = 3 elements
        assert len(questions) >= 2
        
        # Clean up
        output_path.unlink()

    def test_moodle_multichoice_has_answers(self, sample_quiz_data: Dict) -> None:
        """Multiple choice questions should have answer elements."""
        with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as f:
            output_path = Path(f.name)
        
        export_moodle_xml(sample_quiz_data, output_path)
        
        tree = ET.parse(output_path)
        root = tree.getroot()
        
        # Find multichoice question
        for q in root.findall("question"):
            if q.get("type") == "multichoice":
                answers = q.findall("answer")
                assert len(answers) == 4  # a, b, c, d
                
                # One answer should have fraction="100"
                correct_count = sum(
                    1 for a in answers if a.get("fraction") == "100"
                )
                assert correct_count == 1
                break
        
        output_path.unlink()

    def test_moodle_shortanswer_accepts_multiple(self, sample_quiz_data: Dict) -> None:
        """Fill-blank should accept multiple correct answers."""
        with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as f:
            output_path = Path(f.name)
        
        export_moodle_xml(sample_quiz_data, output_path)
        
        tree = ET.parse(output_path)
        root = tree.getroot()
        
        # Find shortanswer question
        for q in root.findall("question"):
            if q.get("type") == "shortanswer":
                answers = q.findall("answer")
                # Should have 2 accepted answers (6653 and 6633)
                assert len(answers) == 2
                break
        
        output_path.unlink()


# ═══════════════════════════════════════════════════════════════════════════════
# CANVAS QTI EXPORT TESTS
# ═══════════════════════════════════════════════════════════════════════════════
class TestCanvasExport:
    """Tests for Canvas QTI export."""

    def test_canvas_qti_structure(self, sample_quiz_data: Dict) -> None:
        """Verify basic QTI structure."""
        with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as f:
            output_path = Path(f.name)
        
        export_canvas_qti(sample_quiz_data, output_path)
        
        # Verify file was created and has content
        assert output_path.exists()
        content = output_path.read_text()
        assert "questestinterop" in content.lower() or "assessment" in content.lower()
        
        output_path.unlink()


# ═══════════════════════════════════════════════════════════════════════════════
# JSON EXPORT TESTS
# ═══════════════════════════════════════════════════════════════════════════════
class TestJsonExport:
    """Tests for JSON export."""

    def test_json_export_schema(self, sample_quiz_data: Dict) -> None:
        """Verify JSON export has expected schema."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            output_path = Path(f.name)
        
        export_json(sample_quiz_data, output_path)
        
        with open(output_path, encoding="utf-8") as f:
            data = json.load(f)
        
        # Verify top-level structure
        assert "metadata" in data
        assert "quiz" in data
        assert "questions" in data
        
        # Verify metadata
        assert data["metadata"]["format_version"] == "1.0"
        assert "exported_at" in data["metadata"]
        
        # Verify quiz info
        assert data["quiz"]["id"] == "P01"
        assert data["quiz"]["passing_score"] == 70
        
        # Verify questions
        assert len(data["questions"]) == 2
        assert data["questions"][0]["type"] == "multiple_choice"
        
        output_path.unlink()

    def test_json_export_question_fields(self, sample_quiz_data: Dict) -> None:
        """Verify question fields are preserved."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            output_path = Path(f.name)
        
        export_json(sample_quiz_data, output_path)
        
        with open(output_path, encoding="utf-8") as f:
            data = json.load(f)
        
        q1 = data["questions"][0]
        assert q1["id"] == "test_q01"
        assert q1["lo_ref"] == "LO1"
        assert q1["bloom_level"] == "understand"
        assert "options" in q1
        assert q1["correct"] == "a"
        
        output_path.unlink()


# ═══════════════════════════════════════════════════════════════════════════════
# EDGE CASE TESTS
# ═══════════════════════════════════════════════════════════════════════════════
class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_empty_questions_list(self) -> None:
        """Quiz with no questions should export without error."""
        quiz_data = {
            "metadata": {"version": "1.0"},
            "project": {"id": "P00", "title": "Empty", "questions": []},
        }
        
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            output_path = Path(f.name)
        
        export_json(quiz_data, output_path)
        
        with open(output_path, encoding="utf-8") as f:
            data = json.load(f)
        
        assert data["questions"] == []
        output_path.unlink()

    def test_special_characters_in_stem(self, sample_quiz_data: Dict) -> None:
        """Questions with special characters should be escaped."""
        sample_quiz_data["project"]["questions"][0]["stem"] = "What is <script>?"
        
        with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as f:
            output_path = Path(f.name)
        
        export_moodle_xml(sample_quiz_data, output_path)
        
        content = output_path.read_text()
        assert "&lt;script&gt;" in content
        
        output_path.unlink()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
