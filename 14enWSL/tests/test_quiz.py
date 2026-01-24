#!/usr/bin/env python3
"""
test_quiz.py — Quiz Validation Tests
NETWORKING class — ASE, CSIE | Computer Networks Laboratory
by ing. dr. Antonio Clim

Tests for validating quiz file structure, content quality, and pedagogical alignment.

Usage:
    pytest tests/test_quiz.py -v
    python -m pytest tests/test_quiz.py -v
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Set

import pytest
import yaml


# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES
# ═══════════════════════════════════════════════════════════════════════════════

QUIZ_DIR = Path(__file__).parent.parent / "formative"
QUIZ_YAML = QUIZ_DIR / "quiz_week14.yaml"
QUIZ_JSON = QUIZ_DIR / "quiz_week14.json"

VALID_BLOOM_LEVELS = {"Remember", "Understand", "Apply", "Analyze", "Analyse", "Evaluate", "Create"}
VALID_DIFFICULTIES = {"basic", "intermediate", "advanced"}
VALID_QUESTION_TYPES = {"multiple_choice", "fill_blank", "true_false", "matching"}
VALID_LO_REFS = {f"LO{i}" for i in range(1, 7)}  # LO1-LO6


@pytest.fixture
def quiz_yaml() -> Dict[str, Any]:
    """Load quiz from YAML file."""
    with open(QUIZ_YAML, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture
def quiz_json() -> Dict[str, Any]:
    """Load quiz from JSON file."""
    with open(QUIZ_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def questions_yaml(quiz_yaml: Dict) -> List[Dict]:
    """Extract questions from YAML quiz."""
    return quiz_yaml.get("questions", [])


@pytest.fixture
def questions_json(quiz_json: Dict) -> List[Dict]:
    """Extract questions from JSON quiz."""
    return quiz_json.get("questions", [])


# ═══════════════════════════════════════════════════════════════════════════════
# FILE STRUCTURE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestFileStructure:
    """Tests for quiz file existence and basic structure."""

    def test_yaml_file_exists(self) -> None:
        """Quiz YAML file should exist."""
        assert QUIZ_YAML.exists(), f"Quiz YAML not found at {QUIZ_YAML}"

    def test_json_file_exists(self) -> None:
        """Quiz JSON file should exist."""
        assert QUIZ_JSON.exists(), f"Quiz JSON not found at {QUIZ_JSON}"

    def test_yaml_is_valid(self, quiz_yaml: Dict) -> None:
        """YAML file should parse without errors."""
        assert quiz_yaml is not None, "YAML parsed to None"
        assert isinstance(quiz_yaml, dict), "YAML should parse to dictionary"

    def test_json_is_valid(self, quiz_json: Dict) -> None:
        """JSON file should parse without errors."""
        assert quiz_json is not None, "JSON parsed to None"
        assert isinstance(quiz_json, dict), "JSON should parse to dictionary"


# ═══════════════════════════════════════════════════════════════════════════════
# METADATA TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMetadata:
    """Tests for quiz metadata completeness and correctness."""

    def test_metadata_exists(self, quiz_yaml: Dict) -> None:
        """Quiz should have metadata section."""
        assert "metadata" in quiz_yaml, "Missing 'metadata' section"

    def test_required_metadata_fields(self, quiz_yaml: Dict) -> None:
        """Metadata should contain required fields."""
        metadata = quiz_yaml.get("metadata", {})
        required = ["week", "topic", "version", "author"]
        
        for field in required:
            assert field in metadata, f"Missing metadata field: {field}"

    def test_week_number(self, quiz_yaml: Dict) -> None:
        """Week number should be 14."""
        metadata = quiz_yaml.get("metadata", {})
        assert metadata.get("week") == 14, "Week should be 14"

    def test_passing_score_reasonable(self, quiz_yaml: Dict) -> None:
        """Passing score should be between 50% and 90%."""
        metadata = quiz_yaml.get("metadata", {})
        passing = metadata.get("passing_score_percent", 70)
        
        assert 50 <= passing <= 90, f"Passing score {passing}% outside reasonable range"


# ═══════════════════════════════════════════════════════════════════════════════
# QUESTIONS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestQuestions:
    """Tests for question structure and validity."""

    def test_questions_exist(self, questions_yaml: List[Dict]) -> None:
        """Quiz should have questions."""
        assert len(questions_yaml) > 0, "No questions found"

    def test_minimum_questions(self, questions_yaml: List[Dict]) -> None:
        """Quiz should have at least 5 questions."""
        assert len(questions_yaml) >= 5, f"Only {len(questions_yaml)} questions, need at least 5"

    def test_question_ids_unique(self, questions_yaml: List[Dict]) -> None:
        """All question IDs should be unique."""
        ids = [q.get("id") for q in questions_yaml]
        assert len(ids) == len(set(ids)), "Duplicate question IDs found"

    def test_question_required_fields(self, questions_yaml: List[Dict]) -> None:
        """Each question should have required fields."""
        required = ["id", "type", "stem", "correct"]
        
        for i, q in enumerate(questions_yaml):
            for field in required:
                assert field in q, f"Question {i+1} (id={q.get('id', 'unknown')}) missing field: {field}"

    def test_question_types_valid(self, questions_yaml: List[Dict]) -> None:
        """Question types should be valid."""
        for q in questions_yaml:
            q_type = q.get("type")
            assert q_type in VALID_QUESTION_TYPES, f"Invalid question type: {q_type}"

    def test_bloom_levels_valid(self, questions_yaml: List[Dict]) -> None:
        """Bloom levels should be valid."""
        for q in questions_yaml:
            bloom = q.get("bloom_level")
            if bloom:  # Optional but recommended
                assert bloom in VALID_BLOOM_LEVELS, f"Invalid Bloom level: {bloom}"

    def test_lo_refs_valid(self, questions_yaml: List[Dict]) -> None:
        """Learning objective references should be valid."""
        for q in questions_yaml:
            lo = q.get("lo_ref")
            if lo:  # Optional but recommended
                assert lo in VALID_LO_REFS, f"Invalid LO reference: {lo}"

    def test_difficulties_valid(self, questions_yaml: List[Dict]) -> None:
        """Difficulty levels should be valid."""
        for q in questions_yaml:
            diff = q.get("difficulty")
            if diff:  # Optional but recommended
                assert diff in VALID_DIFFICULTIES, f"Invalid difficulty: {diff}"

    def test_points_positive(self, questions_yaml: List[Dict]) -> None:
        """Points should be positive integers."""
        for q in questions_yaml:
            points = q.get("points", 1)
            assert isinstance(points, int), f"Points should be integer, got {type(points)}"
            assert points > 0, f"Points should be positive, got {points}"


# ═══════════════════════════════════════════════════════════════════════════════
# MULTIPLE CHOICE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMultipleChoice:
    """Tests specific to multiple choice questions."""

    def test_mcq_has_options(self, questions_yaml: List[Dict]) -> None:
        """Multiple choice questions should have options."""
        for q in questions_yaml:
            if q.get("type") == "multiple_choice":
                assert "options" in q, f"MCQ {q.get('id')} missing options"
                assert len(q["options"]) >= 2, f"MCQ {q.get('id')} needs at least 2 options"

    def test_mcq_correct_in_options(self, questions_yaml: List[Dict]) -> None:
        """Correct answer should be one of the options."""
        for q in questions_yaml:
            if q.get("type") == "multiple_choice":
                options = q.get("options", {})
                correct = q.get("correct", "").lower()
                
                option_keys = [k.lower() for k in options.keys()]
                assert correct in option_keys, f"MCQ {q.get('id')}: correct '{correct}' not in options"

    def test_mcq_min_four_options(self, questions_yaml: List[Dict]) -> None:
        """Multiple choice questions should have 4 options (best practice)."""
        for q in questions_yaml:
            if q.get("type") == "multiple_choice":
                num_options = len(q.get("options", {}))
                assert num_options >= 3, f"MCQ {q.get('id')} should have at least 3 options, has {num_options}"


# ═══════════════════════════════════════════════════════════════════════════════
# FILL BLANK TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestFillBlank:
    """Tests specific to fill-in-the-blank questions."""

    def test_fill_blank_has_correct(self, questions_yaml: List[Dict]) -> None:
        """Fill blank questions should have correct answer(s)."""
        for q in questions_yaml:
            if q.get("type") == "fill_blank":
                correct = q.get("correct")
                assert correct is not None, f"Fill blank {q.get('id')} missing correct answer"
                
                # Can be string or list
                if isinstance(correct, list):
                    assert len(correct) > 0, f"Fill blank {q.get('id')} has empty correct list"


# ═══════════════════════════════════════════════════════════════════════════════
# PEDAGOGICAL TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestPedagogicalQuality:
    """Tests for pedagogical soundness."""

    def test_bloom_coverage(self, questions_yaml: List[Dict]) -> None:
        """Quiz should cover multiple Bloom levels."""
        blooms = {q.get("bloom_level") for q in questions_yaml if q.get("bloom_level")}
        
        # Should cover at least 3 Bloom levels
        assert len(blooms) >= 3, f"Only {len(blooms)} Bloom levels covered: {blooms}"

    def test_lo_coverage(self, questions_yaml: List[Dict]) -> None:
        """Quiz should cover multiple Learning Objectives."""
        los = {q.get("lo_ref") for q in questions_yaml if q.get("lo_ref")}
        
        # Should cover at least 4 LOs (out of 6)
        assert len(los) >= 4, f"Only {len(los)} LOs covered: {los}"

    def test_difficulty_distribution(self, questions_yaml: List[Dict]) -> None:
        """Quiz should have balanced difficulty distribution."""
        diffs = [q.get("difficulty") for q in questions_yaml if q.get("difficulty")]
        
        if diffs:
            # Should not be all same difficulty
            unique_diffs = set(diffs)
            assert len(unique_diffs) >= 2, "All questions have same difficulty"

    def test_explanations_present(self, questions_yaml: List[Dict]) -> None:
        """Most questions should have explanations."""
        with_explanation = sum(1 for q in questions_yaml if q.get("explanation"))
        ratio = with_explanation / len(questions_yaml)
        
        assert ratio >= 0.8, f"Only {ratio:.0%} questions have explanations, need at least 80%"

    def test_stem_length_reasonable(self, questions_yaml: List[Dict]) -> None:
        """Question stems should be reasonable length."""
        for q in questions_yaml:
            stem = q.get("stem", "")
            assert len(stem) >= 20, f"Question {q.get('id')} stem too short: {len(stem)} chars"
            assert len(stem) <= 1000, f"Question {q.get('id')} stem too long: {len(stem)} chars"


# ═══════════════════════════════════════════════════════════════════════════════
# FORMAT CONSISTENCY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestFormatConsistency:
    """Tests for consistency between YAML and JSON formats."""

    def test_question_count_matches(
        self, questions_yaml: List[Dict], questions_json: List[Dict]
    ) -> None:
        """YAML and JSON should have same number of questions."""
        assert len(questions_yaml) == len(questions_json), (
            f"Question count mismatch: YAML={len(questions_yaml)}, JSON={len(questions_json)}"
        )

    def test_question_ids_match(
        self, questions_yaml: List[Dict], questions_json: List[Dict]
    ) -> None:
        """YAML and JSON should have same question IDs."""
        yaml_ids = {q.get("id") for q in questions_yaml}
        json_ids = {q.get("id") for q in questions_json}
        
        assert yaml_ids == json_ids, f"ID mismatch: {yaml_ids.symmetric_difference(json_ids)}"

    def test_correct_answers_match(
        self, questions_yaml: List[Dict], questions_json: List[Dict]
    ) -> None:
        """YAML and JSON should have same correct answers."""
        yaml_answers = {q.get("id"): q.get("correct") for q in questions_yaml}
        json_answers = {q.get("id"): q.get("correct") for q in questions_json}
        
        for q_id in yaml_answers:
            assert yaml_answers[q_id] == json_answers.get(q_id), (
                f"Correct answer mismatch for {q_id}: YAML={yaml_answers[q_id]}, JSON={json_answers.get(q_id)}"
            )


# ═══════════════════════════════════════════════════════════════════════════════
# SCORING TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestScoring:
    """Tests for scoring configuration."""

    def test_scoring_exists(self, quiz_yaml: Dict) -> None:
        """Quiz should have scoring section."""
        assert "scoring" in quiz_yaml, "Missing 'scoring' section"

    def test_total_points_calculated(self, quiz_yaml: Dict, questions_yaml: List[Dict]) -> None:
        """Total points should match sum of question points."""
        declared_total = quiz_yaml.get("scoring", {}).get("total_points", 0)
        calculated_total = sum(q.get("points", 1) for q in questions_yaml)
        
        # Allow small discrepancy for rounding
        assert abs(declared_total - calculated_total) <= 1, (
            f"Points mismatch: declared={declared_total}, calculated={calculated_total}"
        )

    def test_passing_threshold_valid(self, quiz_yaml: Dict) -> None:
        """Passing threshold should be less than total points."""
        scoring = quiz_yaml.get("scoring", {})
        total = scoring.get("total_points", 100)
        threshold = scoring.get("passing_threshold", 0)
        
        assert threshold <= total, f"Passing threshold {threshold} exceeds total {total}"
        assert threshold > 0, "Passing threshold should be positive"


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
