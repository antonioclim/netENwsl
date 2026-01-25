#!/usr/bin/env python3
"""
Unit Tests for Quiz Exports and Validators — Week 10
=====================================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Tests for Moodle XML, Canvas QTI and JSON LMS exports.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import json
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

# Add parent directories to path for imports
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "formative"))


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_FIXTURES
# ═══════════════════════════════════════════════════════════════════════════════
SAMPLE_QUIZ = {
    "metadata": {
        "week": 10,
        "topic": "Application Layer Protocols",
        "passing_score": 70,
    },
    "questions": [
        {
            "id": "q1",
            "type": "mcq",
            "lo_ref": "LO1",
            "bloom_level": "understand",
            "difficulty": "basic",
            "points": 1,
            "stem": "What does TLS stand for?",
            "options": {
                "A": "Transport Layer Security",
                "B": "Transfer Layer System",
                "C": "Transmission Link Security",
                "D": "Transport Link System",
            },
            "correct": "A",
            "explanation": "TLS stands for Transport Layer Security.",
        },
        {
            "id": "q2",
            "type": "mcq",
            "lo_ref": "LO2",
            "bloom_level": "apply",
            "difficulty": "intermediate",
            "points": 2,
            "stem": "Which HTTP method is idempotent?",
            "options": {
                "A": "POST",
                "B": "PUT",
                "C": "PATCH",
                "D": "None of the above",
            },
            "correct": "B",
            "explanation": "PUT is idempotent; multiple identical requests have the same effect.",
        },
        {
            "id": "q3",
            "type": "live_verification",
            "lo_ref": "LO3",
            "stem": "Run dig @127.0.0.1 -p 5353 web.lab.local",
            "verification_cmd": "dig @127.0.0.1 -p 5353 web.lab.local +short",
            "expected_pattern": r"172\.20\.0\.\d+",
        },
    ],
}


# ═══════════════════════════════════════════════════════════════════════════════
# JSON_EXPORT_TESTS
# ═══════════════════════════════════════════════════════════════════════════════
class TestJSONExport(unittest.TestCase):
    """Tests for JSON LMS export format."""

    def setUp(self) -> None:
        """Create temporary directory for test outputs."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_path = Path(self.temp_dir) / "quiz_export.json"

    def test_json_export_creates_file(self) -> None:
        """JSON export should create a valid file."""
        from run_quiz import export_json

        export_json(SAMPLE_QUIZ, self.output_path)
        self.assertTrue(self.output_path.exists())

    def test_json_export_valid_structure(self) -> None:
        """Exported JSON should have correct structure."""
        from run_quiz import export_json

        export_json(SAMPLE_QUIZ, self.output_path)

        with open(self.output_path, "r") as f:
            data = json.load(f)

        self.assertIn("metadata", data)
        self.assertIn("questions", data)
        self.assertEqual(data["metadata"]["title"], "Week 10 Formative Assessment")

    def test_json_export_excludes_live_verification(self) -> None:
        """Live verification questions should be excluded from export."""
        from run_quiz import export_json

        export_json(SAMPLE_QUIZ, self.output_path)

        with open(self.output_path, "r") as f:
            data = json.load(f)

        # Should have 2 questions (q1 and q2), not 3
        self.assertEqual(len(data["questions"]), 2)

        # Verify no live_verification type
        for q in data["questions"]:
            self.assertNotEqual(q.get("type"), "live_verification")

    def test_json_export_preserves_question_data(self) -> None:
        """Exported questions should preserve all relevant fields."""
        from run_quiz import export_json

        export_json(SAMPLE_QUIZ, self.output_path)

        with open(self.output_path, "r") as f:
            data = json.load(f)

        q1 = data["questions"][0]
        self.assertEqual(q1["id"], "q1")
        self.assertEqual(q1["learning_objective"], "LO1")
        self.assertEqual(q1["correct_answer"], "A")
        self.assertIn("A", q1["options"])


# ═══════════════════════════════════════════════════════════════════════════════
# MOODLE_EXPORT_TESTS
# ═══════════════════════════════════════════════════════════════════════════════
class TestMoodleXMLExport(unittest.TestCase):
    """Tests for Moodle XML export format."""

    def setUp(self) -> None:
        """Create temporary directory for test outputs."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_path = Path(self.temp_dir) / "quiz_moodle.xml"

    def test_moodle_export_creates_file(self) -> None:
        """Moodle export should create a valid XML file."""
        from run_quiz import export_moodle_xml

        export_moodle_xml(SAMPLE_QUIZ, self.output_path)
        self.assertTrue(self.output_path.exists())

    def test_moodle_export_valid_xml(self) -> None:
        """Exported file should be valid XML."""
        from run_quiz import export_moodle_xml

        export_moodle_xml(SAMPLE_QUIZ, self.output_path)

        # Should parse without error
        tree = ET.parse(self.output_path)
        root = tree.getroot()
        self.assertEqual(root.tag, "quiz")

    def test_moodle_export_has_category(self) -> None:
        """Moodle export should include category question."""
        from run_quiz import export_moodle_xml

        export_moodle_xml(SAMPLE_QUIZ, self.output_path)

        tree = ET.parse(self.output_path)
        root = tree.getroot()

        categories = root.findall(".//question[@type='category']")
        self.assertEqual(len(categories), 1)

    def test_moodle_export_correct_answer_fraction(self) -> None:
        """Correct answers should have fraction='100'."""
        from run_quiz import export_moodle_xml

        export_moodle_xml(SAMPLE_QUIZ, self.output_path)

        tree = ET.parse(self.output_path)
        root = tree.getroot()

        # Find first multichoice question
        mcq = root.find(".//question[@type='multichoice']")
        self.assertIsNotNone(mcq)

        # Check that exactly one answer has fraction="100"
        answers = mcq.findall(".//answer")
        correct_count = sum(1 for a in answers if a.get("fraction") == "100")
        self.assertEqual(correct_count, 1)


# ═══════════════════════════════════════════════════════════════════════════════
# CANVAS_EXPORT_TESTS
# ═══════════════════════════════════════════════════════════════════════════════
class TestCanvasQTIExport(unittest.TestCase):
    """Tests for Canvas QTI export format."""

    def setUp(self) -> None:
        """Create temporary directory for test outputs."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_path = Path(self.temp_dir) / "quiz_canvas.xml"

    def test_canvas_export_creates_file(self) -> None:
        """Canvas export should create a valid file."""
        from run_quiz import export_canvas_qti

        export_canvas_qti(SAMPLE_QUIZ, self.output_path)
        self.assertTrue(self.output_path.exists())

    def test_canvas_export_valid_xml(self) -> None:
        """Exported file should be valid XML."""
        from run_quiz import export_canvas_qti

        export_canvas_qti(SAMPLE_QUIZ, self.output_path)

        tree = ET.parse(self.output_path)
        root = tree.getroot()
        self.assertEqual(root.tag, "questestinterop")


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATOR_TESTS
# ═══════════════════════════════════════════════════════════════════════════════
class TestSubmissionValidator(unittest.TestCase):
    """Tests for anti-cheat submission validator."""

    def test_fingerprint_generation(self) -> None:
        """Fingerprint should be generated consistently."""
        try:
            from anti_cheat.fingerprint import generate_fingerprint

            fp1 = generate_fingerprint("test_data")
            fp2 = generate_fingerprint("test_data")

            # Same input should produce same fingerprint
            self.assertEqual(fp1, fp2)

            # Different input should produce different fingerprint
            fp3 = generate_fingerprint("different_data")
            self.assertNotEqual(fp1, fp3)
        except ImportError:
            self.skipTest("anti_cheat module not available")

    def test_challenge_structure(self) -> None:
        """Generated challenges should have required fields."""
        try:
            from anti_cheat.challenge_generator import generate_challenge

            challenge = generate_challenge()

            self.assertIn("challenge_id", challenge)
            self.assertIn("timestamp", challenge)
            self.assertIn("tasks", challenge)
            self.assertIsInstance(challenge["tasks"], list)
        except ImportError:
            self.skipTest("anti_cheat module not available")


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_LOADER_TESTS
# ═══════════════════════════════════════════════════════════════════════════════
class TestQuizLoader(unittest.TestCase):
    """Tests for quiz YAML loading."""

    def test_load_quiz_file_not_found(self) -> None:
        """Should raise FileNotFoundError for missing file."""
        from run_quiz import load_quiz

        with self.assertRaises(FileNotFoundError):
            load_quiz(Path("/nonexistent/quiz.yaml"))

    def test_load_actual_quiz(self) -> None:
        """Should load the actual quiz.yaml file."""
        from run_quiz import load_quiz

        quiz_path = PROJECT_ROOT / "formative" / "quiz.yaml"
        if quiz_path.exists():
            quiz = load_quiz(quiz_path)
            self.assertIn("metadata", quiz)
            self.assertIn("questions", quiz)
        else:
            self.skipTest("quiz.yaml not found")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    unittest.main(verbosity=2)
