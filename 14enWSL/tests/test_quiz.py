#!/usr/bin/env python3
"""
test_quiz.py — Quiz Validation Tests (Week 14)

NETWORKING class — ASE, CSIE | Computer Networks Laboratory
by ing. dr. Antonio Clim

Purpose
- Validate that the quiz files exist and can be parsed
- Validate that core pedagogical metadata is present
- Validate that question fields are well-formed

Design note
Week 14 contains several open-ended question types (design and scenario tasks).
Those are validated structurally rather than by a single 'correct answer' key.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Set

import pytest
import yaml

QUIZ_DIR = Path(__file__).parent.parent / "formative"

# The kit uses these filenames throughout Makefile targets and formative tooling
QUIZ_YAML = QUIZ_DIR / "quiz.yaml"
QUIZ_JSON = QUIZ_DIR / "quiz.json"

VALID_BLOOM_LEVELS: Set[str] = {
    "Remember",
    "Understand",
    "Apply",
    "Analyze",
    "Analyse",
    "Evaluate",
    "Create",
}

# Week 14 includes a small number of 'expert' items for differentiation
VALID_DIFFICULTIES: Set[str] = {"basic", "intermediate", "advanced", "expert"}

# Week 14 extends the question taxonomy beyond MCQ and fill-in
VALID_QUESTION_TYPES: Set[str] = {
    "multiple_choice",
    "fill_blank",
    "true_false",
    "matching",
    "scenario_analysis",
    "design_task",
    "architecture_design",
    "troubleshooting_design",
}

VALID_LO_REFS: Set[str] = {f"LO{i}" for i in range(1, 7)}  # LO1-LO6


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
def questions_yaml(quiz_yaml: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract questions from YAML quiz."""
    return quiz_yaml.get("questions", [])


@pytest.fixture
def questions_json(quiz_json: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract questions from JSON quiz."""
    return quiz_json.get("questions", [])


class TestFileStructure:
    """Tests for quiz file existence and basic parseability."""

    def test_yaml_file_exists(self) -> None:
        assert QUIZ_YAML.exists(), f"Missing quiz YAML file: {QUIZ_YAML}"

    def test_json_file_exists(self) -> None:
        assert QUIZ_JSON.exists(), f"Missing quiz JSON file: {QUIZ_JSON}"


class TestQuizMetadata:
    """Validate top-level metadata fields."""

    def test_metadata_present(self, quiz_yaml: Dict[str, Any]) -> None:
        assert "metadata" in quiz_yaml, "Quiz must include top-level 'metadata'"

    def test_metadata_has_week_and_topic(self, quiz_yaml: Dict[str, Any]) -> None:
        md = quiz_yaml["metadata"]
        assert md.get("week") in (14, "14", "Week 14"), "Metadata must specify week 14"
        assert isinstance(md.get("topic", ""), str) and md.get("topic"), "Metadata must specify topic"

    def test_metadata_has_learning_objectives(self, quiz_yaml: Dict[str, Any]) -> None:
        md = quiz_yaml["metadata"]
        lo = md.get("learning_objectives")

        assert lo, "Metadata must include learning objectives"

        # Accept either a list (simple enumeration) or a dict (structured LO map)
        assert isinstance(lo, (list, dict)), "learning_objectives must be a list or a dict"

        if isinstance(lo, dict):
            # Expect LO keys such as LO1..LO6
            assert set(lo.keys()).issuperset(VALID_LO_REFS), "learning_objectives dict must include LO1..LO6"


class TestQuestionSchema:
    """Validate question entries in both YAML and JSON."""

    def test_questions_non_empty(self, questions_yaml: List[Dict[str, Any]]) -> None:
        assert questions_yaml, "Quiz must contain at least one question"

    def test_questions_count_matches_metadata(self, quiz_yaml: Dict[str, Any]) -> None:
        md = quiz_yaml.get("metadata", {})
        expected = md.get("question_count")
        if isinstance(expected, int):
            assert len(quiz_yaml.get("questions", [])) == expected

    @pytest.mark.parametrize("field", ["id", "type", "bloom_level", "lo_ref", "difficulty", "points", "stem"])
    def test_required_fields_present(self, questions_yaml: List[Dict[str, Any]], field: str) -> None:
        for q in questions_yaml:
            assert field in q, f"Question {q.get('id', '<missing id>')} missing required field: {field}"

    def test_bloom_levels_valid(self, questions_yaml: List[Dict[str, Any]]) -> None:
        for q in questions_yaml:
            assert q["bloom_level"] in VALID_BLOOM_LEVELS, f"Invalid bloom_level: {q['bloom_level']}"

    def test_lo_refs_valid(self, questions_yaml: List[Dict[str, Any]]) -> None:
        for q in questions_yaml:
            assert q["lo_ref"] in VALID_LO_REFS, f"Invalid lo_ref: {q['lo_ref']}"

    def test_difficulty_valid(self, questions_yaml: List[Dict[str, Any]]) -> None:
        for q in questions_yaml:
            assert q["difficulty"] in VALID_DIFFICULTIES, f"Invalid difficulty: {q['difficulty']}"

    def test_question_types_valid(self, questions_yaml: List[Dict[str, Any]]) -> None:
        for q in questions_yaml:
            assert q["type"] in VALID_QUESTION_TYPES, f"Invalid question type: {q['type']}"

    def test_multiple_choice_has_options(self, questions_yaml: List[Dict[str, Any]]) -> None:
        for q in questions_yaml:
            if q["type"] == "multiple_choice":
                assert isinstance(q.get("options"), dict) and q["options"], "MCQ must include non-empty options"
                assert "correct" in q, "MCQ must include 'correct'"

    def test_fill_blank_has_answer(self, questions_yaml: List[Dict[str, Any]]) -> None:
        for q in questions_yaml:
            if q["type"] == "fill_blank":
                # Week 14 uses 'correct' (string or list) for fill-in items to allow multiple accepted variants
                assert ("answer" in q) or ("correct" in q), "fill_blank must include 'answer' or 'correct'"

    def test_open_ended_has_rubric(self, questions_yaml: List[Dict[str, Any]]) -> None:
        open_types = {"scenario_analysis", "design_task", "architecture_design", "troubleshooting_design"}
        for q in questions_yaml:
            if q["type"] in open_types:
                has_guidance = any(
                    key in q
                    for key in ("rubric", "expected_elements", "grading_guidance", "evaluation_criteria")
                ) or (
                    ("correct" in q) and ("explanation" in q)
                )
                assert has_guidance, (
                    f"Open-ended question {q.get('id')} should include rubric or evaluation guidance"
                )


class TestYamlJsonParity:
    """Ensure YAML and JSON represent the same quiz."""

    def test_same_question_ids(self, questions_yaml: List[Dict[str, Any]], questions_json: List[Dict[str, Any]]) -> None:
        ids_yaml = {q.get("id") for q in questions_yaml}
        ids_json = {q.get("id") for q in questions_json}
        assert ids_yaml == ids_json, "YAML and JSON quiz must contain the same question IDs"
