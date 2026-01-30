#!/usr/bin/env python3
"""
Quiz Schema Validation Script — Week 4

Validates formative/quiz.yaml for structural correctness.
The validator is intentionally lightweight and does not require internet access.

This script is used by:
  - make validate-quiz
  - GitHub Actions CI
  - pre-commit
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml


PROJECT_ROOT = Path(__file__).parent.parent


def _fail(msg: str) -> None:
    raise ValueError(msg)


def _validate_multiple_choice(q: Dict[str, Any]) -> None:
    options = q.get("options")
    correct = q.get("correct")
    if not isinstance(options, dict) or not options:
        _fail(f"{q.get('id')}: multiple_choice requires non-empty options mapping")
    if correct not in options:
        _fail(f"{q.get('id')}: correct option must be one of {sorted(options.keys())}")


def _validate_fill_blank(q: Dict[str, Any]) -> None:
    correct = q.get("correct")
    if not isinstance(correct, list) or not correct:
        _fail(f"{q.get('id')}: fill_blank requires a non-empty list under 'correct'")


def validate_quiz(quiz: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors: List[str] = []

    if not isinstance(quiz, dict):
        return False, ["quiz.yaml must contain a YAML mapping at top level"]

    meta = quiz.get("metadata")
    if not isinstance(meta, dict):
        errors.append("metadata must be a mapping")
    else:
        for k in ["week", "topic", "version", "estimated_time", "passing_score", "lo_coverage"]:
            if k not in meta:
                errors.append(f"metadata missing key: {k}")

    questions = quiz.get("questions")
    if not isinstance(questions, list) or not questions:
        errors.append("questions must be a non-empty list")
        return False, errors

    seen_ids = set()
    for q in questions:
        if not isinstance(q, dict):
            errors.append("Each question must be a mapping")
            continue

        qid = q.get("id")
        if not isinstance(qid, str) or not qid.strip():
            errors.append("Question missing id")
            continue
        if qid in seen_ids:
            errors.append(f"Duplicate question id: {qid}")
        seen_ids.add(qid)

        for k in ["type", "lo_ref", "bloom_level", "difficulty", "stem"]:
            if k not in q:
                errors.append(f"{qid}: missing key: {k}")

        qtype = q.get("type")
        try:
            if qtype == "multiple_choice":
                _validate_multiple_choice(q)
            elif qtype == "fill_blank":
                _validate_fill_blank(q)
            else:
                # Other types are allowed if they at least include a 'correct' field
                if "correct" not in q:
                    errors.append(f"{qid}: type {qtype!r} requires a 'correct' field")
        except ValueError as e:
            errors.append(str(e))

    return not errors, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate formative/quiz.yaml structure")
    parser.add_argument("--path", default="formative/quiz.yaml", help="Quiz YAML path (default: formative/quiz.yaml)")
    parser.add_argument("--quiet", action="store_true", help="Quiet mode (exit code only)")
    args = parser.parse_args()

    quiz_path = (PROJECT_ROOT / args.path).resolve()
    if not quiz_path.exists():
        print(f"ERROR: quiz file not found: {args.path}")
        return 1

    quiz = yaml.safe_load(quiz_path.read_text(encoding="utf-8"))
    ok, errs = validate_quiz(quiz)

    if ok:
        if not args.quiet:
            print("✓ quiz.yaml validation passed")
        return 0

    if not args.quiet:
        print("✗ quiz.yaml validation failed:")
        for e in errs:
            print(f"  - {e}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
