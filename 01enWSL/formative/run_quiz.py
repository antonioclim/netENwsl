#!/usr/bin/env python3
"""
Quiz Runner — Week 1 Formative Assessment
==========================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

A standalone quiz runner that works with both YAML and JSON formats.
Supports interactive mode and LMS export (Moodle/Canvas compatible).

Usage:
    python run_quiz.py                      # Interactive quiz (all questions)
    python run_quiz.py --section pre_lab    # Run specific section
    python run_quiz.py --list-sections      # Show available sections
    python run_quiz.py --validate           # Validate quiz file
    python run_quiz.py --export-json        # Export to LMS-compatible JSON
    python run_quiz.py --export-moodle      # Export to Moodle XML
    python run_quiz.py --stats              # Show quiz statistics

Requirements:
    - Python 3.8+
    - PyYAML (pip install pyyaml)
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

QUIZ_DIR = Path(__file__).parent
DEFAULT_QUIZ_YAML = QUIZ_DIR / "quiz.yaml"
DEFAULT_QUIZ_JSON = QUIZ_DIR / "quiz.json"


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ LOADER
# ═══════════════════════════════════════════════════════════════════════════════

def load_quiz(path: Path | None = None) -> dict[str, Any]:
    """Load quiz from YAML or JSON file."""
    if path is None:
        if DEFAULT_QUIZ_YAML.exists() and YAML_AVAILABLE:
            path = DEFAULT_QUIZ_YAML
        elif DEFAULT_QUIZ_JSON.exists():
            path = DEFAULT_QUIZ_JSON
        else:
            raise FileNotFoundError("No quiz file found. Expected quiz.yaml or quiz.json")

    with open(path, encoding="utf-8") as f:
        if path.suffix in (".yaml", ".yml"):
            if not YAML_AVAILABLE:
                raise ImportError("PyYAML required. Install: pip install pyyaml")
            return yaml.safe_load(f)
        return json.load(f)


def save_quiz_json(quiz: dict[str, Any], path: Path) -> None:
    """Save quiz to JSON format."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(quiz, f, indent=2, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def build_question_index(quiz: dict[str, Any]) -> dict[str, dict[str, Any]]:
    bank = quiz.get("questions") or []
    index: dict[str, dict[str, Any]] = {}
    if isinstance(bank, list):
        for q in bank:
            if isinstance(q, dict) and q.get("id"):
                index[str(q["id"])] = q
    elif isinstance(bank, dict):
        for k, v in bank.items():
            if isinstance(v, dict):
                index[str(k)] = v
    return index


def iter_questions(quiz: dict[str, Any], section: str | None = None):
    """Yield (section_id, question_dict) pairs, resolving question references."""
    q_index = build_question_index(quiz)
    sections = quiz.get("sections", [])
    if isinstance(sections, dict):
        items = [(str(k), v) for k, v in sections.items()]
    elif isinstance(sections, list):
        items = [(str(s.get("id") or s.get("name") or ""), s) for s in sections if isinstance(s, dict)]
    else:
        items = []

    for sec_id, sec in items:
        if section and sec_id != section:
            continue
        refs = sec.get("questions", []) or []
        for ref in refs:
            if isinstance(ref, dict):
                yield sec_id, ref
                continue
            qid = str(ref)
            q = q_index.get(qid)
            if q is not None:
                yield sec_id, q

def normalise_options(options: Any) -> list[dict[str, Any]]:
    """Return options as a list of {key, text} dicts."""
    if options is None:
        return []
    if isinstance(options, dict):
        return [{"key": k, "text": str(v)} for k, v in options.items()]
    if isinstance(options, list):
        return _normalise_list_options(options)
    return []


def _normalise_list_options(options: list[Any]) -> list[dict[str, Any]]:
    if not options:
        return []
    if all(isinstance(x, str) for x in options):
        return _options_from_strings(options)
    if all(isinstance(x, dict) for x in options):
        return _options_from_dicts(options)
    return []


def _options_from_strings(items: list[str]) -> list[dict[str, Any]]:
    keys = [chr(ord("A") + i) for i in range(len(items))]
    return [{"key": k, "text": t} for k, t in zip(keys, items)]


def _options_from_dicts(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for item in items:
        key = str(item.get("key") or item.get("id") or item.get("label") or "")
        text = str(item.get("text") or item.get("value") or "")
        out.append({"key": key, "text": text})
    return out

def quiz_title(quiz: dict[str, Any]) -> str:
    meta = quiz.get("metadata", {})
    return str(meta.get("title") or "Week 1 Formative Quiz")



def _et_text(parent, tag: str, text: str, attrs: dict[str, str] | None = None):
    import xml.etree.ElementTree as ET
    el = ET.SubElement(parent, tag, attrs or {})
    el_text = ET.SubElement(el, "text")
    el_text.text = text
    return el

def validate_quiz(quiz: dict[str, Any]) -> tuple[bool, list[str]]:
    """Validate quiz structure, section references and question fields."""
    errors: list[str] = []
    errors.extend(_validate_top_level(quiz))

    q_index = build_question_index(quiz)
    errors.extend(_validate_question_bank(q_index))

    for sec_name, sec in _iter_sections(quiz):
        errors.extend(_validate_section(sec_name, sec))
        errors.extend(_validate_section_refs(sec_name, sec, q_index))

    return (len(errors) == 0), errors


def _validate_question_bank(q_index: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    if not q_index:
        errors.append("Question bank is empty or missing ids")
        return errors
    for qid, q in q_index.items():
        errors.extend(_validate_question("bank", qid, q))
    return errors


def _validate_section_refs(section: str, sec: dict[str, Any], q_index: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    refs = sec.get("questions", []) or []
    for idx, ref in enumerate(refs, start=1):
        if isinstance(ref, dict):
            continue
        qid = str(ref)
        if qid not in q_index:
            errors.append(f"{section} ref{idx}: unknown question id '{qid}'")
    return errors

def _validate_top_level(quiz: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if "metadata" not in quiz:
        errors.append("Missing top-level key: metadata")
    if "sections" not in quiz:
        errors.append("Missing top-level key: sections")
    if "questions" not in quiz:
        errors.append("Missing top-level key: questions")
    sections = quiz.get("sections")
    if sections is not None and not isinstance(sections, (list, dict)):
        errors.append("Invalid sections: must be a list or dict")
    bank = quiz.get("questions")
    if bank is not None and not isinstance(bank, (list, dict)):
        errors.append("Invalid questions: must be a list or dict")
    return errors

def _iter_sections(quiz: dict[str, Any]):
    sections = quiz.get("sections") or []
    if isinstance(sections, dict):
        for name, sec in sections.items():
            yield str(name), sec
    elif isinstance(sections, list):
        for sec in sections:
            if not isinstance(sec, dict):
                continue
            sec_id = str(sec.get("id") or sec.get("name") or "")
            yield sec_id, sec


def _validate_section(name: str, sec: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(sec, dict):
        return [f"Section {name}: section must be a mapping"]
    if "questions" not in sec or not isinstance(sec.get("questions"), list):
        errors.append(f"Section {name}: missing or invalid questions list")
    return errors


def _validate_question(section: str, idx: int, q: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    prefix = f"{section} q{idx}"
    if not isinstance(q, dict):
        return [f"{prefix}: question must be a mapping"]
    qtype = str(q.get("type") or "").strip()
    stem = str(q.get("stem") or q.get("question") or "").strip()
    if not qtype:
        errors.append(f"{prefix}: missing type")
    if not stem:
        errors.append(f"{prefix}: missing stem")
    if qtype in {"multiple_choice", "mcq"}:
        errors.extend(_validate_mcq(prefix, q))
    elif qtype == "ordering":
        errors.extend(_validate_ordering(prefix, q))
    elif qtype in {"true_false", "fill_blank", "numeric"}:
        errors.extend(_validate_simple_answer(prefix, q))
    else:
        if qtype:
            errors.append(f"{prefix}: unsupported type '{qtype}'")
    return errors


def _validate_mcq(prefix: str, q: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    opts = normalise_options(q.get("options"))
    if len(opts) < 2:
        errors.append(f"{prefix}: multiple_choice needs at least 2 options")
        return errors
    correct = q.get("correct")
    keys = {o.get("key") for o in opts if o.get("key")}
    if correct is None:
        errors.append(f"{prefix}: missing correct option key")
    elif str(correct) not in keys:
        errors.append(f"{prefix}: correct '{correct}' not in options keys")
    return errors


def _validate_ordering(prefix: str, q: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    items_raw = q.get("items")
    order_raw = q.get("correct_order")

    items = _ordering_tokens(items_raw)
    correct_order = _ordering_tokens(order_raw)

    if len(items) < 2:
        errors.append(f"{prefix}: ordering needs items list (>=2)")
    if len(correct_order) < 2:
        errors.append(f"{prefix}: ordering needs correct_order list (>=2)")
    if items and correct_order and set(items) != set(correct_order):
        errors.append(f"{prefix}: correct_order must be a permutation of items")
    return errors


def _ordering_tokens(raw: Any) -> list[str]:
    if not isinstance(raw, list):
        return []
    out: list[str] = []
    for x in raw:
        if isinstance(x, dict):
            out.append(str(x.get("id") or x.get("text") or x.get("value") or ""))
        else:
            out.append(str(x))
    return [t for t in out if t]

def _validate_simple_answer(prefix: str, q: dict[str, Any]) -> list[str]:
    if "answer" in q or "correct" in q:
        return []
    return [f"{prefix}: missing answer/correct value"]

def export_to_canvas_json(quiz: dict[str, Any], output_path: Path) -> None:
    """Export quiz to a Canvas-friendly JSON payload."""
    payload = {
        "title": quiz_title(quiz),
        "exported_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "questions": [],
    }

    for sec_name, q in iter_questions(quiz):
        item = _canvas_map_question(sec_name, q)
        if item:
            payload["questions"].append(item)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def _canvas_map_question(section: str, q: dict[str, Any]) -> dict[str, Any] | None:
    qtype = str(q.get("type") or "").strip()
    stem = str(q.get("stem") or q.get("question") or "").strip()
    if not qtype or not stem:
        return None

    if qtype == "true_false":
        opts = [{"key": "A", "text": "True"}, {"key": "B", "text": "False"}]
        correct = "A" if bool(q.get("correct")) else "B"
        return _canvas_mcq_payload(section, stem, opts, correct)

    if qtype in {"multiple_choice", "mcq"}:
        opts = normalise_options(q.get("options"))
        correct = str(q.get("correct") or "").strip()
        if not opts or not correct:
            return None
        return _canvas_mcq_payload(section, stem, opts, correct)

    return None


def _canvas_mcq_payload(section: str, stem: str, opts: list[dict[str, Any]], correct: str) -> dict[str, Any]:
    return {
        "section": section,
        "type": "multiple_choice",
        "stem": stem,
        "options": [{"id": o["key"], "text": o["text"]} for o in opts],
        "correct": correct,
    }

def run_interactive_quiz(quiz: dict[str, Any], section: str | None = None, limit: int | None = None, randomise: bool = True) -> None:
    """Run the quiz in interactive mode."""
    questions = _collect_questions_for_run(quiz, section, limit, randomise)
    if not questions:
        print("No questions found for the selected section.")
        return

    print(f"Quiz: {quiz_title(quiz)}")
    print(f"Questions: {len(questions)}")
    print("-" * 60)

    results = _run_question_loop(questions)
    _print_quiz_summary(results)


def _collect_questions_for_run(quiz: dict[str, Any], section: str | None, limit: int | None, randomise: bool) -> list[dict[str, Any]]:
    pool = [q for _, q in iter_questions(quiz, section)]
    if randomise:
        random.shuffle(pool)
    if limit is not None:
        return pool[: max(0, int(limit))]
    return pool


def _run_question_loop(questions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for idx, q in enumerate(questions, start=1):
        outcome = _ask_single_question(idx, q)
        if outcome is not None:
            results.append(outcome)
    return results


def _ask_single_question(number: int, q: dict[str, Any]) -> dict[str, Any] | None:
    qtype = str(q.get("type") or "").strip()
    stem = str(q.get("stem") or q.get("question") or "").strip()
    if not qtype or not stem:
        return None

    print()
    print(f"Q{number}. {stem}")
    grader = _GRADERS.get(qtype)
    if grader is None and qtype in {"mcq"}:
        grader = _GRADERS.get("multiple_choice")
    if grader is None:
        print("Unsupported question type.")
        return {"type": qtype, "correct": False}
    return {"type": qtype, "correct": grader(q)}


def _grade_mcq(q: dict[str, Any]) -> bool:
    correct = str(q.get("correct") or "")
    answer = _ask_multiple_choice(normalise_options(q.get("options")))
    return answer == correct


def _grade_fill_blank(q: dict[str, Any]) -> bool:
    answer = _ask_fill_blank()
    target = str(q.get("answer", "")).strip().lower()
    return answer.strip().lower() == target


def _grade_true_false(q: dict[str, Any]) -> bool:
    answer = _ask_true_false()
    return bool(answer) == bool(q.get("correct"))


def _grade_numeric(q: dict[str, Any]) -> bool:
    answer = _ask_numeric()
    return _numeric_ok(answer, q)


def _grade_ordering(q: dict[str, Any]) -> bool:
    items = q.get("items") or []
    answer = _ask_ordering(items)
    return answer == (q.get("correct_order") or [])


_GRADERS = {
    "multiple_choice": _grade_mcq,
    "mcq": _grade_mcq,
    "fill_blank": _grade_fill_blank,
    "true_false": _grade_true_false,
    "numeric": _grade_numeric,
    "ordering": _grade_ordering,
}

def _numeric_ok(answer: float | None, q: dict[str, Any]) -> bool:
    if answer is None:
        return False
    target = q.get("answer")
    tol = float(q.get("tolerance", 0))
    try:
        target_f = float(target)
    except (TypeError, ValueError):
        return False
    return abs(answer - target_f) <= tol


def _print_quiz_summary(results: list[dict[str, Any]]) -> None:
    total = len(results)
    correct = sum(1 for r in results if r.get("correct"))
    print()
    print("=" * 60)
    print(f"Score: {correct}/{total}")
    print("=" * 60)

def _collect_questions_for_run(quiz: dict[str, Any], section: str | None, limit: int | None) -> list[dict[str, Any]]:
    pool = [q for _, q in iter_questions(quiz, section)]
    random.shuffle(pool)
    if limit is not None:
        return pool[: max(0, int(limit))]
    return pool


def _run_question_loop(questions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for idx, q in enumerate(questions, start=1):
        outcome = _ask_single_question(idx, q)
        if outcome is not None:
            results.append(outcome)
    return results


def _ask_single_question(number: int, q: dict[str, Any]) -> dict[str, Any] | None:
    qtype = str(q.get("type") or "").strip()
    stem = str(q.get("stem") or q.get("question") or "").strip()
    if not qtype or not stem:
        return None

    print()
    print(f"Q{number}. {stem}")
    grader = _GRADERS.get(qtype)
    if grader is None and qtype in {"mcq"}:
        grader = _GRADERS.get("multiple_choice")
    if grader is None:
        print("Unsupported question type.")
        return {"type": qtype, "correct": False}
    return {"type": qtype, "correct": grader(q)}


def _grade_mcq(q: dict[str, Any]) -> bool:
    correct = str(q.get("correct") or "")
    answer = _ask_multiple_choice(normalise_options(q.get("options")))
    return answer == correct


def _grade_fill_blank(q: dict[str, Any]) -> bool:
    answer = _ask_fill_blank()
    target = str(q.get("answer", "")).strip().lower()
    return answer.strip().lower() == target


def _grade_true_false(q: dict[str, Any]) -> bool:
    answer = _ask_true_false()
    return bool(answer) == bool(q.get("correct"))


def _grade_numeric(q: dict[str, Any]) -> bool:
    answer = _ask_numeric()
    return _numeric_ok(answer, q)


def _grade_ordering(q: dict[str, Any]) -> bool:
    items = q.get("items") or []
    answer = _ask_ordering(items)
    return answer == (q.get("correct_order") or [])


_GRADERS = {
    "multiple_choice": _grade_mcq,
    "mcq": _grade_mcq,
    "fill_blank": _grade_fill_blank,
    "true_false": _grade_true_false,
    "numeric": _grade_numeric,
    "ordering": _grade_ordering,
}

def _numeric_ok(answer: float | None, q: dict[str, Any]) -> bool:
    if answer is None:
        return False
    target = q.get("answer")
    tol = float(q.get("tolerance", 0))
    try:
        target_f = float(target)
    except (TypeError, ValueError):
        return False
    return abs(answer - target_f) <= tol


def _print_quiz_summary(results: list[dict[str, Any]]) -> None:
    total = len(results)
    correct = sum(1 for r in results if r.get("correct"))
    print()
    print("=" * 60)
    print(f"Score: {correct}/{total}")
    print("=" * 60)

def _ask_multiple_choice(q: dict) -> bool:
    """Handle multiple choice question."""
    options = q.get("options", {})
    if isinstance(options, list):
        for opt in options:
            print(f"    {opt['key']}) {opt['text']}")
    else:
        for key, text in options.items():
            print(f"    {key}) {text}")

    answer = input("\n  Your answer: ").strip().lower()
    correct = q.get("correct", q.get("correct_answer", "")).lower()
    return answer == correct


def _ask_fill_blank(q: dict) -> bool:
    """Handle fill-in-the-blank question."""
    if q.get("hint"):
        print(f"  💡 Hint: {q['hint']}")

    answer = input("  Your answer: ").strip()
    correct_answers = q.get("correct", q.get("correct_answers", []))

    if not isinstance(correct_answers, list):
        correct_answers = [correct_answers]

    if q.get("case_sensitive", False):
        return answer in correct_answers
    return answer.lower() in [str(c).lower() for c in correct_answers]


def _ask_true_false(q: dict) -> bool:
    """Handle true/false question."""
    print("    T) True")
    print("    F) False")

    answer = input("\n  Your answer (T/F): ").strip().upper()
    correct = q.get("correct", q.get("correct_answer"))

    user_bool = answer in ("T", "TRUE", "YES", "1")
    return user_bool == correct


def _ask_numeric(q: dict) -> bool:
    """Handle numeric question."""
    if q.get("hint"):
        print(f"  💡 Hint: {q['hint']}")

    try:
        answer = float(input("  Your answer: ").strip())
    except ValueError:
        return False

    correct = float(q.get("correct", q.get("correct_answer", 0)))
    tolerance = float(q.get("tolerance", 0))

    return abs(answer - correct) <= tolerance


def _ask_ordering(q: dict) -> bool:
    """Handle ordering question."""
    items = q.get("items", [])
    for item in items:
        print(f"    {item['id']}) {item['text']}")

    print("\n  Enter the correct order (e.g. d,b,a,c):")
    answer = input("  Your answer: ").strip().lower()
    answer_list = [x.strip() for x in answer.replace(" ", "").split(",")]

    correct_order = q.get("correct_order", [])
    return answer_list == [x.lower() for x in correct_order]


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def export_to_moodle_xml(quiz: dict[str, Any], output_path: Path) -> None:
    """Export quiz to Moodle XML format."""
    import xml.etree.ElementTree as ET

    root_xml = ET.Element("quiz")
    for sec_name, q in iter_questions(quiz):
        qtype = str(q.get("type") or "").strip()
        if qtype in {"multiple_choice", "mcq"}:
            root_xml.append(_moodle_multichoice(sec_name, q))
        elif qtype == "true_false":
            root_xml.append(_moodle_truefalse(sec_name, q))
        elif qtype == "fill_blank":
            root_xml.append(_moodle_shortanswer(sec_name, q))

    tree = ET.ElementTree(root_xml)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)

def _moodle_multichoice(section: str, q: dict[str, Any]):
    import xml.etree.ElementTree as ET

    stem = str(q.get("stem") or q.get("question") or "").strip()
    correct = str(q.get("correct") or "").strip()
    opts = normalise_options(q.get("options"))

    question = ET.Element("question", {"type": "multichoice"})
    _et_text(question, "name", f"{section}: {stem[:60]}")
    _moodle_question_text(question, stem)
    _moodle_mcq_settings(question)

    for o in opts:
        question.append(_moodle_answer(o["text"], o["key"] == correct))

    return question


def _moodle_question_text(question, stem: str) -> None:
    import xml.etree.ElementTree as ET
    qtext = ET.SubElement(question, "questiontext", {"format": "html"})
    ET.SubElement(qtext, "text").text = stem


def _moodle_mcq_settings(question) -> None:
    import xml.etree.ElementTree as ET
    ET.SubElement(question, "single").text = "true"
    ET.SubElement(question, "shuffleanswers").text = "true"
    ET.SubElement(question, "answernumbering").text = "ABCD"


def _moodle_answer(text: str, is_correct: bool):
    import xml.etree.ElementTree as ET
    fraction = "100" if is_correct else "0"
    ans = ET.Element("answer", {"fraction": fraction, "format": "html"})
    ET.SubElement(ans, "text").text = text
    fb = ET.SubElement(ans, "feedback", {"format": "html"})
    ET.SubElement(fb, "text").text = ""
    return ans

def _moodle_truefalse(section: str, q: dict[str, Any]):
    import xml.etree.ElementTree as ET

    stem = str(q.get("stem") or q.get("question") or "").strip()
    correct = bool(q.get("correct"))
    question = ET.Element("question", {"type": "truefalse"})

    name = ET.SubElement(question, "name")
    ET.SubElement(name, "text").text = f"{section}: {stem[:60]}"

    qtext = ET.SubElement(question, "questiontext", {"format": "html"})
    ET.SubElement(qtext, "text").text = stem

    for text, is_true in (("true", True), ("false", False)):
        fraction = "100" if (is_true == correct) else "0"
        ans = ET.SubElement(question, "answer", {"fraction": fraction, "format": "html"})
        ET.SubElement(ans, "text").text = text
        fb = ET.SubElement(ans, "feedback", {"format": "html"})
        ET.SubElement(fb, "text").text = ""

    return question

def _moodle_shortanswer(section: str, q: dict[str, Any]):
    import xml.etree.ElementTree as ET

    stem = str(q.get("stem") or q.get("question") or "").strip()
    answer = str(q.get("answer") or q.get("correct") or "").strip()

    question = ET.Element("question", {"type": "shortanswer"})
    name = ET.SubElement(question, "name")
    ET.SubElement(name, "text").text = f"{section}: {stem[:60]}"

    qtext = ET.SubElement(question, "questiontext", {"format": "html"})
    ET.SubElement(qtext, "text").text = stem

    ans = ET.SubElement(question, "answer", {"fraction": "100", "format": "html"})
    ET.SubElement(ans, "text").text = answer
    fb = ET.SubElement(ans, "feedback", {"format": "html"})
    ET.SubElement(fb, "text").text = ""
    return question

def show_statistics(quiz: dict[str, Any]) -> None:
    """Print quick quiz statistics."""
    sections = quiz.get("sections") or {}
    total_q = sum(len(sec.get("questions", [])) for sec in sections.values())
    by_type = _count_by_type(quiz)

    print(f"Quiz: {quiz_title(quiz)}")
    print(f"Sections: {len(sections)}")
    print(f"Questions: {total_q}")
    print("-" * 60)
    for t, n in sorted(by_type.items(), key=lambda x: (-x[1], x[0])):
        print(f"{t:16s} {n}")


def _count_by_type(quiz: dict[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for _, q in iter_questions(quiz):
        t = str(q.get("type") or "unknown").strip()
        counts[t] = counts.get(t, 0) + 1
    return counts

def main() -> int:
    """Command-line entry point."""
    args = _build_parser().parse_args()

    try:
        quiz = load_quiz(args.quiz)
    except Exception as e:
        print(f"Error loading quiz: {e}")
        return 1

    if args.list_sections:
        _print_sections(quiz)
        return 0

    if args.validate:
        return _run_validation(quiz)

    if args.stats:
        show_statistics(quiz)
        return 0

    if args.export_json or args.export_canvas or args.export_moodle:
        return _run_exports(quiz, args)

    return _run_default(quiz, args)


def _run_default(quiz: dict[str, Any], args: argparse.Namespace) -> int:
    run_interactive_quiz(quiz, section=args.section, limit=args.limit, randomise=args.random)
    return 0

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Week 1 Formative Quiz Runner")
    parser.add_argument("--quiz", type=Path, help="Quiz file path")
    parser.add_argument("--section", help="Run a single section")
    parser.add_argument("--random", action="store_true", help="Shuffle questions")
    parser.add_argument("--limit", type=int, help="Limit number of questions")
    parser.add_argument("--list-sections", action="store_true", help="List available sections")
    parser.add_argument("--validate", action="store_true", help="Validate quiz file")
    parser.add_argument("--export-json", action="store_true", help="Export to JSON format")
    parser.add_argument("--export-moodle", action="store_true", help="Export to Moodle XML")
    parser.add_argument("--export-canvas", action="store_true", help="Export Canvas quiz JSON")
    parser.add_argument("--stats", action="store_true", help="Show quiz statistics")
    return parser


def _print_sections(quiz: dict[str, Any]) -> None:
    sections = quiz.get("sections") or []
    print("Available sections:")
    if isinstance(sections, dict):
        for name, sec in sections.items():
            count = len(sec.get("questions", []))
            title = sec.get("title") or sec.get("name") or name
            print(f"  {name}: {title} ({count} questions)")
        return
    for sec in sections:
        if not isinstance(sec, dict):
            continue
        sec_id = sec.get("id") or sec.get("name") or "?"
        title = sec.get("name") or sec.get("title") or sec_id
        count = len(sec.get("questions", []))
        print(f"  {sec_id}: {title} ({count} questions)")

def _run_validation(quiz: dict[str, Any]) -> int:
    ok, errors = validate_quiz(quiz)
    if ok:
        print("Quiz validation passed.")
        return 0
    print("Quiz validation failed:")
    for err in errors:
        print(f"  - {err}")
    return 1


def _run_exports(quiz: dict[str, Any], args: argparse.Namespace) -> int:
    if args.export_json:
        save_quiz_json(quiz, QUIZ_DIR / "quiz_lms_export.json")
    if args.export_canvas:
        export_to_canvas_json(quiz, QUIZ_DIR / "quiz_canvas.json")
    if args.export_moodle:
        export_to_moodle_xml(quiz, QUIZ_DIR / "quiz_moodle.xml")
    return 0

