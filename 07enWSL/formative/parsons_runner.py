#!/usr/bin/env python3
"""
Parsons Problems Runner — Week 7
================================
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Interactive runner for Parsons problems (code reordering exercises).
Loads problems from JSON files and provides an interactive solving experience.

Usage:
    python3 formative/parsons_runner.py                      # Run all problems
    python3 formative/parsons_runner.py --problem P1         # Run specific problem
    python3 formative/parsons_runner.py --random             # Random order
    python3 formative/parsons_runner.py --hint               # Show hints

Exit codes:
    0 - All problems solved correctly
    1 - Some problems incorrect
    2 - Error (file not found, invalid JSON, etc.)
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import json
import random
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


# ═══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class ParsonsBlock:
    """Represents a single code block in a Parsons problem."""
    id: int
    code: str
    indent: int = 0
    is_distractor: bool = False


@dataclass
class ParsonsProblem:
    """Represents a complete Parsons problem."""
    id: str
    week: int
    lo_ref: str
    title: str
    instructions: str
    language: str
    blocks: list[ParsonsBlock]
    correct_order: list[int]
    distractors: list[int]
    explanation: str


@dataclass
class ProblemResult:
    """Stores the result of a problem attempt."""
    problem_id: str
    correct: bool
    user_order: list[int]
    correct_order: list[int]
    identified_distractors: bool


# ═══════════════════════════════════════════════════════════════════════════════
# PROBLEM LOADER
# ═══════════════════════════════════════════════════════════════════════════════
def load_problems_from_markdown(md_path: Path) -> list[ParsonsProblem]:
    """
    Extract Parsons problems from the existing parsons_problems.md file.
    
    This parser extracts the structured problems from the markdown documentation.
    For production use, problems should be stored in JSON format.
    
    Args:
        md_path: Path to parsons_problems.md
        
    Returns:
        List of ParsonsProblem objects
    """
    # Default problems embedded (extracted from docs/parsons_problems.md)
    default_problems = [
        ParsonsProblem(
            id="P1",
            week=7,
            lo_ref="LO1",
            title="TCP Port Probe with Timeout",
            instructions="Create a function that probes a TCP port and returns 'open', 'closed', or 'filtered'.",
            language="python",
            blocks=[
                ParsonsBlock(1, 'return "open"', 2),
                ParsonsBlock(2, 'def probe_port(host: str, port: int) -> str:', 0),
                ParsonsBlock(3, 'sock.settimeout(2)', 1),
                ParsonsBlock(4, 'sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)', 1),
                ParsonsBlock(5, 'result = sock.connect_ex((host, port))', 1),
                ParsonsBlock(6, 'if result == 0:', 1),
                ParsonsBlock(7, 'sock.close()\n    return "closed"', 1),
                ParsonsBlock(8, 'sock.bind(("", 0))', 1, is_distractor=True),
                ParsonsBlock(9, 'except socket.timeout:\n        return "filtered"', 1),
                ParsonsBlock(10, 'try:', 1),
                ParsonsBlock(11, 'sock.listen(1)', 1, is_distractor=True),
            ],
            correct_order=[2, 10, 4, 3, 5, 6, 1, 7, 9],
            distractors=[8, 11],
            explanation="Block H (sock.bind) is for servers, not clients. Block K (sock.listen) is for accepting connections, not probing."
        ),
        ParsonsProblem(
            id="P2",
            week=7,
            lo_ref="LO3",
            title="Parse iptables Rule Output",
            instructions="Create a function that parses iptables -L -n output and extracts action, protocol, and port.",
            language="python",
            blocks=[
                ParsonsBlock(1, 'return {"action": parts[0], "protocol": parts[1], "dport": dport}', 1),
                ParsonsBlock(2, 'def parse_iptables_line(line: str) -> dict:', 0),
                ParsonsBlock(3, 'parts = line.split()', 1),
                ParsonsBlock(4, 'if "dpt:" in line:\n        dport_part = [p for p in parts if p.startswith("dpt:")]\n        dport = int(dport_part[0].split(":")[1]) if dport_part else None', 1),
                ParsonsBlock(5, 'subprocess.run(["iptables", "-L", "-n"])', 1, is_distractor=True),
                ParsonsBlock(6, 'else:\n        dport = None', 1),
                ParsonsBlock(7, 'sock = socket.socket(socket.AF_INET, socket.SOCK_RAW)', 1, is_distractor=True),
            ],
            correct_order=[2, 3, 4, 6, 1],
            distractors=[5, 7],
            explanation="Block E runs iptables (we're parsing existing output). Block G creates a raw socket (unrelated to text parsing)."
        ),
        ParsonsProblem(
            id="P3",
            week=7,
            lo_ref="LO2",
            title="UDP Send with Error Handling",
            instructions="Create a function that sends UDP and returns (True, response) or (False, 'timeout').",
            language="python",
            blocks=[
                ParsonsBlock(1, 'except socket.timeout:\n        return (False, "timeout")', 1),
                ParsonsBlock(2, 'def udp_send_recv(host: str, port: int, message: bytes) -> tuple:', 0),
                ParsonsBlock(3, 'sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)', 1),
                ParsonsBlock(4, 'sock.settimeout(3)', 1),
                ParsonsBlock(5, 'try:', 1),
                ParsonsBlock(6, 'sock.sendto(message, (host, port))', 2),
                ParsonsBlock(7, 'response, addr = sock.recvfrom(1024)\n        return (True, response)', 2),
                ParsonsBlock(8, 'sock.connect((host, port))', 2, is_distractor=True),
                ParsonsBlock(9, 'finally:\n        sock.close()', 1),
                ParsonsBlock(10, 'sock.accept()', 2, is_distractor=True),
            ],
            correct_order=[2, 3, 4, 5, 6, 7, 1, 9],
            distractors=[8, 10],
            explanation="Block H (connect) is optional for UDP. Block J (accept) is TCP server-only."
        ),
        ParsonsProblem(
            id="P4",
            week=7,
            lo_ref="LO3",
            title="Apply Firewall Profile from JSON",
            instructions="Create a function that loads a JSON firewall profile and applies each rule with iptables.",
            language="python",
            blocks=[
                ParsonsBlock(1, 'return count', 1),
                ParsonsBlock(2, 'def apply_profile(profile_path: str) -> int:', 0),
                ParsonsBlock(3, 'with open(profile_path) as f:\n        profile = json.load(f)', 1),
                ParsonsBlock(4, 'count = 0\n    for rule in profile["rules"]:', 1),
                ParsonsBlock(5, 'cmd = ["iptables", "-A", "INPUT", "-p", rule["protocol"], "--dport", str(rule["port"]), "-j", rule["action"]]', 2),
                ParsonsBlock(6, 'subprocess.run(cmd, check=True)\n        count += 1', 2),
                ParsonsBlock(7, 'sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)', 2, is_distractor=True),
                ParsonsBlock(8, 'profile = yaml.safe_load(f)', 1, is_distractor=True),
            ],
            correct_order=[2, 3, 4, 5, 6, 1],
            distractors=[7, 8],
            explanation="Block G sets socket options (unrelated). Block H uses YAML (task specifies JSON)."
        ),
        ParsonsProblem(
            id="P5",
            week=7,
            lo_ref="LO4",
            title="Capture Traffic Summary",
            instructions="Create a function that uses tshark to count TCP, UDP, and ICMP packets in a pcap file.",
            language="python",
            blocks=[
                ParsonsBlock(1, 'return summary', 1),
                ParsonsBlock(2, 'def analyse_pcap(pcap_path: str) -> dict:', 0),
                ParsonsBlock(3, 'summary = {"tcp": 0, "udp": 0, "icmp": 0}', 1),
                ParsonsBlock(4, 'result = subprocess.run(["tshark", "-r", pcap_path, "-T", "fields", "-e", "ip.proto"], capture_output=True, text=True)', 1),
                ParsonsBlock(5, 'for line in result.stdout.strip().split("\\n"):\n        proto = line.strip()\n        if proto == "6": summary["tcp"] += 1\n        elif proto == "17": summary["udp"] += 1\n        elif proto == "1": summary["icmp"] += 1', 1),
                ParsonsBlock(6, 'sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)', 1, is_distractor=True),
                ParsonsBlock(7, 'wireshark.open(pcap_path)', 1, is_distractor=True),
            ],
            correct_order=[2, 3, 4, 5, 1],
            distractors=[6, 7],
            explanation="Block F creates raw socket (for live capture, not file analysis). Block G uses non-existent wireshark module."
        ),
    ]
    
    return default_problems


def load_problems_from_json(json_path: Path) -> list[ParsonsProblem]:
    """
    Load Parsons problems from JSON file.
    
    Args:
        json_path: Path to JSON file with problems
        
    Returns:
        List of ParsonsProblem objects
    """
    if not json_path.exists():
        return []
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    problems = []
    for p in data.get("problems", []):
        blocks = [
            ParsonsBlock(
                id=b["id"],
                code=b["code"],
                indent=b.get("indent", 0),
                is_distractor=b.get("id") in p.get("distractors", [])
            )
            for b in p.get("blocks", [])
        ]
        
        problems.append(ParsonsProblem(
            id=p["id"],
            week=p.get("week", 7),
            lo_ref=p.get("lo_ref", "?"),
            title=p.get("title", "Untitled"),
            instructions=p.get("instructions", ""),
            language=p.get("language", "python"),
            blocks=blocks,
            correct_order=p.get("correct_order", []),
            distractors=p.get("distractors", []),
            explanation=p.get("explanation", "")
        ))
    
    return problems


# ═══════════════════════════════════════════════════════════════════════════════
# PROBLEM RUNNER
# ═══════════════════════════════════════════════════════════════════════════════
def display_problem(problem: ParsonsProblem, show_hint: bool = False) -> None:
    """Display a Parsons problem for solving."""
    print()
    print("═" * 70)
    print(f"  Problem {problem.id}: {problem.title}")
    print(f"  LO: {problem.lo_ref}  │  Language: {problem.language}")
    print("═" * 70)
    print()
    print(f"📋 {problem.instructions}")
    print()
    
    if show_hint:
        print(f"💡 HINT: There are {len(problem.distractors)} distractor block(s) that should NOT be used.")
        print()
    
    print("📦 Available blocks (in scrambled order):")
    print("─" * 50)
    
    # Shuffle blocks for display
    display_blocks = problem.blocks.copy()
    random.shuffle(display_blocks)
    
    for block in display_blocks:
        distractor_mark = " [DISTRACTOR?]" if show_hint and block.is_distractor else ""
        indent = "    " * block.indent
        code_lines = block.code.split("\n")
        print(f"\n  Block {block.id}:{distractor_mark}")
        for line in code_lines:
            print(f"    {indent}{line}")
    
    print()
    print("─" * 50)


def solve_problem(problem: ParsonsProblem, show_hint: bool = False) -> ProblemResult:
    """
    Interactive problem solving.
    
    Args:
        problem: The Parsons problem to solve
        show_hint: Whether to show hints about distractors
        
    Returns:
        ProblemResult with the attempt details
    """
    display_problem(problem, show_hint)
    
    print("Enter your solution:")
    print("  - List block numbers in correct order, separated by commas")
    print("  - Omit distractor blocks")
    print(f"  - Example: 2,4,3,1 (for {len(problem.correct_order)} blocks)")
    print()
    
    user_input = input("Your order: ").strip()
    
    try:
        user_order = [int(x.strip()) for x in user_input.split(",")]
    except ValueError:
        print("⚠️  Invalid input. Please enter numbers separated by commas.")
        return ProblemResult(
            problem_id=problem.id,
            correct=False,
            user_order=[],
            correct_order=problem.correct_order,
            identified_distractors=False
        )
    
    # Check if user correctly excluded distractors
    used_distractors = [b for b in user_order if b in problem.distractors]
    excluded_correct = [b for b in problem.correct_order if b not in user_order]
    
    is_correct = user_order == problem.correct_order
    identified_distractors = len(used_distractors) == 0 and len(excluded_correct) == 0
    
    print()
    if is_correct:
        print("✅ CORRECT! Perfect order.")
    else:
        print("❌ INCORRECT.")
        print()
        print(f"   Your order:    {' → '.join(map(str, user_order))}")
        print(f"   Correct order: {' → '.join(map(str, problem.correct_order))}")
        
        if used_distractors:
            print(f"   ⚠️  You included distractor(s): {used_distractors}")
        if excluded_correct:
            print(f"   ⚠️  You missed required block(s): {excluded_correct}")
    
    print()
    print(f"📖 Explanation: {problem.explanation}")
    
    return ProblemResult(
        problem_id=problem.id,
        correct=is_correct,
        user_order=user_order,
        correct_order=problem.correct_order,
        identified_distractors=identified_distractors
    )


def run_session(
    problems: list[ParsonsProblem],
    problem_filter: Optional[str] = None,
    randomize: bool = False,
    show_hint: bool = False
) -> list[ProblemResult]:
    """
    Run a complete Parsons problems session.
    
    Args:
        problems: List of problems to run
        problem_filter: Specific problem ID to run (or None for all)
        randomize: Shuffle problem order
        show_hint: Show hints about distractors
        
    Returns:
        List of ProblemResult for each attempted problem
    """
    if problem_filter:
        problems = [p for p in problems if p.id == problem_filter]
        if not problems:
            print(f"⚠️  Problem {problem_filter} not found.")
            return []
    
    if randomize:
        random.shuffle(problems)
    
    print()
    print("╔" + "═" * 68 + "╗")
    print(f"║  {'PARSONS PROBLEMS — Week 7':^64}  ║")
    print(f"║  {'Code Reordering Exercises':^64}  ║")
    print("╠" + "═" * 68 + "╣")
    print(f"║  Problems: {len(problems):<5}  │  Hints: {'ON' if show_hint else 'OFF':<5}{' ' * 37}║")
    print("╚" + "═" * 68 + "╝")
    
    results = []
    for i, problem in enumerate(problems, 1):
        print(f"\n[{i}/{len(problems)}]", end="")
        result = solve_problem(problem, show_hint)
        results.append(result)
        
        if i < len(problems):
            input("\nPress Enter for next problem...")
    
    return results


def display_summary(results: list[ProblemResult]) -> None:
    """Display session summary."""
    correct = sum(1 for r in results if r.correct)
    total = len(results)
    
    print()
    print("╔" + "═" * 68 + "╗")
    print(f"║  {'SESSION COMPLETE':^64}  ║")
    print("╠" + "═" * 68 + "╣")
    print(f"║  Correct: {correct}/{total} ({100*correct/total:.0f}%){' ' * 45}║")
    print("╟" + "─" * 68 + "╢")
    
    for r in results:
        status = "✅" if r.correct else "❌"
        print(f"║  {status} Problem {r.problem_id}{' ' * 55}║")
    
    print("╚" + "═" * 68 + "╝")


# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════
def build_parser() -> argparse.ArgumentParser:
    """Build command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Parsons Problems Runner for Week 7",
        epilog="Exit codes: 0=all correct, 1=some incorrect, 2=error"
    )
    
    parser.add_argument(
        "--problem", "-p",
        help="Run specific problem by ID (e.g., P1, P2)"
    )
    
    parser.add_argument(
        "--random", "-r",
        action="store_true",
        help="Randomize problem order"
    )
    
    parser.add_argument(
        "--hint",
        action="store_true",
        help="Show hints about distractors"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available problems and exit"
    )
    
    return parser


def main() -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args()
    
    # Load problems
    problems = load_problems_from_markdown(Path("docs/parsons_problems.md"))
    
    if args.list:
        print("\nAvailable Parsons Problems:")
        print("─" * 40)
        for p in problems:
            print(f"  {p.id}: {p.title} ({p.lo_ref})")
        return 0
    
    results = run_session(
        problems,
        problem_filter=args.problem,
        randomize=args.random,
        show_hint=args.hint
    )
    
    if results:
        display_summary(results)
        return 0 if all(r.correct for r in results) else 1
    
    return 2


if __name__ == "__main__":
    sys.exit(main())
