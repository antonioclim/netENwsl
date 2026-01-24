#!/usr/bin/env python3
"""
Public Basic Tests — Week 1
===========================
Computer Networks - ASE Bucharest | by ing. dr. Antonio Clim

These tests are PUBLIC and visible to students. They provide immediate
feedback on basic functionality without revealing grading edge cases.

Students can run these tests locally to verify their solutions:
    python -m pytest tests/public/test_basic.py -v

Tests are intentionally simple to encourage exploration without
giving away complete solutions.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest


# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# ═══════════════════════════════════════════════════════════════════════════════
# EXERCISE FILE EXISTENCE TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestFileStructure:
    """Verify expected file structure exists."""

    def test_exercise_files_exist(self) -> None:
        """All exercise files should be present."""
        exercises = [
            "src/exercises/ex_1_01_ping_latency.py",
            "src/exercises/ex_1_02_tcp_server_client.py",
            "src/exercises/ex_1_03_parse_csv.py",
            "src/exercises/ex_1_04_pcap_stats.py",
            "src/exercises/ex_1_05_transmission_delay.py",
        ]

        for exercise in exercises:
            path = PROJECT_ROOT / exercise
            assert path.exists(), f"Missing exercise file: {exercise}"

    def test_homework_files_exist(self) -> None:
        """Homework exercise files should be present."""
        homework = [
            "homework/exercises/hw_1_01_network_report.py",
            "homework/exercises/hw_1_02_pcap_analyser.py",
        ]

        for hw in homework:
            path = PROJECT_ROOT / hw
            assert path.exists(), f"Missing homework file: {hw}"

    def test_documentation_files_exist(self) -> None:
        """Key documentation files should be present."""
        docs = [
            "README.md",
            "docs/troubleshooting.md",
            "docs/glossary.md",
            "docs/learning_objectives.md",
        ]

        for doc in docs:
            path = PROJECT_ROOT / doc
            assert path.exists(), f"Missing documentation: {doc}"


# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestImports:
    """Verify modules can be imported without errors."""

    def test_import_net_utils(self) -> None:
        """src.utils.net_utils should be importable."""
        from src.utils import net_utils

        assert hasattr(net_utils, "format_bytes")

    def test_import_exercises(self) -> None:
        """Exercise modules should be importable."""
        # This tests basic syntax correctness
        from src.exercises import ex_1_01_ping_latency, ex_1_02_tcp_server_client, ex_1_03_parse_csv

        assert callable(getattr(ex_1_01_ping_latency, "main", None))
        assert callable(getattr(ex_1_02_tcp_server_client, "main", None))


# ═══════════════════════════════════════════════════════════════════════════════
# BASIC FUNCTIONALITY TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestBasicFunctionality:
    """Test basic functionality without revealing solutions."""

    def test_format_bytes_basic(self) -> None:
        """format_bytes should handle simple cases."""
        from src.utils.net_utils import format_bytes

        # Basic cases
        assert "B" in format_bytes(100)
        assert "KB" in format_bytes(1024) or "KiB" in format_bytes(1024)
        assert "MB" in format_bytes(1024 * 1024) or "MiB" in format_bytes(1024 * 1024)

    def test_format_bytes_zero(self) -> None:
        """format_bytes should handle zero."""
        from src.utils.net_utils import format_bytes

        result = format_bytes(0)
        assert "0" in result

    def test_transmission_delay_formula(self) -> None:
        """Verify transmission delay calculation concept."""
        # Students should understand: delay = packet_size / bandwidth
        # This tests the concept, not the implementation

        packet_size_bits = 1500 * 8  # 1500 bytes in bits
        bandwidth_bps = 100_000_000  # 100 Mbps

        expected_delay_seconds = packet_size_bits / bandwidth_bps
        expected_delay_ms = expected_delay_seconds * 1000

        # Should be approximately 0.12 ms
        assert 0.1 < expected_delay_ms < 0.15


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ VALIDATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestQuizStructure:
    """Verify quiz file structure is valid."""

    def test_quiz_yaml_loadable(self) -> None:
        """Quiz YAML should be parseable."""
        import yaml

        quiz_path = PROJECT_ROOT / "formative" / "quiz.yaml"
        assert quiz_path.exists(), "quiz.yaml not found"

        with open(quiz_path) as f:
            quiz = yaml.safe_load(f)

        assert "metadata" in quiz
        assert "questions" in quiz
        assert "sections" in quiz

    def test_quiz_has_minimum_questions(self) -> None:
        """Quiz should have at least 15 questions."""
        import yaml

        quiz_path = PROJECT_ROOT / "formative" / "quiz.yaml"
        with open(quiz_path) as f:
            quiz = yaml.safe_load(f)

        questions = quiz.get("questions", [])
        assert len(questions) >= 15, f"Expected >=15 questions, found {len(questions)}"

    def test_quiz_questions_have_required_fields(self) -> None:
        """Each question should have required fields."""
        import yaml

        quiz_path = PROJECT_ROOT / "formative" / "quiz.yaml"
        with open(quiz_path) as f:
            quiz = yaml.safe_load(f)

        required_fields = {"id", "type", "stem"}

        for q in quiz.get("questions", []):
            missing = required_fields - set(q.keys())
            assert not missing, f"Question {q.get('id', '?')} missing: {missing}"


# ═══════════════════════════════════════════════════════════════════════════════
# DOCKER CONFIGURATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestDockerConfig:
    """Verify Docker configuration files."""

    def test_docker_compose_exists(self) -> None:
        """docker-compose.yml should exist."""
        compose_path = PROJECT_ROOT / "docker" / "docker-compose.yml"
        assert compose_path.exists()

    def test_dockerfile_exists(self) -> None:
        """Dockerfile should exist."""
        dockerfile_path = PROJECT_ROOT / "docker" / "Dockerfile.lab"
        assert dockerfile_path.exists()

    def test_docker_compose_valid_yaml(self) -> None:
        """docker-compose.yml should be valid YAML."""
        import yaml

        compose_path = PROJECT_ROOT / "docker" / "docker-compose.yml"
        with open(compose_path) as f:
            config = yaml.safe_load(f)

        assert "services" in config, "docker-compose.yml should define services"


# ═══════════════════════════════════════════════════════════════════════════════
# RUN TESTS
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
