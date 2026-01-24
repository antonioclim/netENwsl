#!/usr/bin/env python3
"""
Parsons Problem Runner — Week 7
================================
NETWORKING class - ASE, Informatics | Computer Networks Laboratory

Interactive runner for Parsons problems (code arrangement exercises).
Parsons problems help develop understanding of procedural logic without
the cognitive load of writing syntax from scratch.

Usage:
    python3 formative/parsons_runner.py              # Interactive mode
    python3 formative/parsons_runner.py --problem P1 # Specific problem
    python3 formative/parsons_runner.py --hints      # Enable hints
    python3 formative/parsons_runner.py --review     # Show all solutions

Theory:
    Parsons problems were introduced by Dale Parsons and Patricia Haden (2006)
    as a way to assess programming knowledge while reducing extraneous cognitive load.
"""

from __future__ import annotations

import argparse
import random
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    class Fore:
        GREEN = RED = YELLOW = BLUE = CYAN = MAGENTA = ""
    class Style:
        BRIGHT = RESET_ALL = ""


# ═══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class CodeBlock:
    """A single block of code in a Parsons problem."""
    id: str
    code: str
    is_distractor: bool = False
    hint: str = ""


@dataclass
class ParsonsProblem:
    """A complete Parsons problem with blocks and solution."""
    id: str
    title: str
    description: str
    lo_ref: str
    difficulty: str
    blocks: list[CodeBlock]
    correct_order: list[str]
    explanation: str = ""
    
    @property
    def solution_blocks(self) -> list[CodeBlock]:
        """Get blocks in solution order (excluding distractors)."""
        block_map = {b.id: b for b in self.blocks}
        return [block_map[bid] for bid in self.correct_order if bid in block_map]
    
    @property
    def distractor_blocks(self) -> list[CodeBlock]:
        """Get distractor blocks."""
        return [b for b in self.blocks if b.is_distractor]


@dataclass
class AttemptResult:
    """Result of a problem attempt."""
    correct: bool
    message: str
    correct_positions: list[bool] = field(default_factory=list)
    hints: list[str] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════════════════════
# PROBLEM DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════════

PROBLEMS = [
    ParsonsProblem(
        id="P1",
        title="TCP Port Probe Implementation",
        description="Arrange the code blocks to implement a function that probes a TCP port and returns its state (open, closed or filtered).",
        lo_ref="LO1",
        difficulty="intermediate",
        blocks=[
            CodeBlock("A", 'def probe_tcp_port(host: str, port: int, timeout: float = 2.0) -> str:'),
            CodeBlock("B", '    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)'),
            CodeBlock("C", '    sock.settimeout(timeout)'),
            CodeBlock("D", '    try:'),
            CodeBlock("E", '        result = sock.connect_ex((host, port))'),
            CodeBlock("F", '        if result == 0:\n            return "open"'),
            CodeBlock("G", '        else:\n            return "closed"'),
            CodeBlock("H", '    except socket.timeout:\n        return "filtered"'),
            CodeBlock("I", '    finally:\n        sock.close()'),
            CodeBlock("X", '    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)', is_distractor=True, hint="SOCK_DGRAM is for UDP, not TCP"),
            CodeBlock("Y", '        sock.connect((host, port))\n        return "open"', is_distractor=True, hint="connect() raises exception; connect_ex() returns error code"),
            CodeBlock("Z", '        return "timeout"', is_distractor=True, hint='"timeout" is not a standard port state'),
        ],
        correct_order=["A", "B", "C", "D", "E", "F", "G", "H", "I"],
        explanation="TCP socket probing uses connect_ex() which returns 0 on success. Timeout indicates filtered (firewall DROP).",
    ),
    ParsonsProblem(
        id="P2",
        title="Parse iptables Output",
        description="Arrange the code blocks to parse iptables output and extract rule information.",
        lo_ref="LO3",
        difficulty="intermediate",
        blocks=[
            CodeBlock("A", 'def parse_iptables_rules(output: str) -> list[dict]:'),
            CodeBlock("B", '    rules = []'),
            CodeBlock("C", "    lines = output.strip().split('\\n')"),
            CodeBlock("D", '    for line in lines[2:]:  # Skip header lines'),
            CodeBlock("E", '        if not line.strip():\n            continue'),
            CodeBlock("F", '        parts = line.split()'),
            CodeBlock("G", '        if len(parts) >= 4:'),
            CodeBlock("H", "            rule = {\n                'target': parts[0],\n                'protocol': parts[1],\n                'source': parts[3],\n            }"),
            CodeBlock("I", '            rules.append(rule)'),
            CodeBlock("J", '    return rules'),
            CodeBlock("X", '    for line in lines:  # Includes headers', is_distractor=True, hint="Would include 'Chain INPUT' and column headers"),
            CodeBlock("Y", "        rule = {'target': parts[0]}\n        rules.append(rule)", is_distractor=True, hint="Missing fields and validation"),
        ],
        correct_order=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
        explanation="Skip first two lines (chain name and column headers). Validate line has enough parts before parsing.",
    ),
    ParsonsProblem(
        id="P3",
        title="UDP Send with Error Handling",
        description="Arrange the blocks to send a UDP datagram with proper error handling that acknowledges UDP's fire-and-forget nature.",
        lo_ref="LO2",
        difficulty="basic",
        blocks=[
            CodeBlock("A", 'def send_udp_message(host: str, port: int, message: str) -> tuple[bool, str]:'),
            CodeBlock("B", '    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)'),
            CodeBlock("C", '    try:'),
            CodeBlock("D", "        sock.sendto(message.encode('utf-8'), (host, port))"),
            CodeBlock("E", '        # Note: Success only means packet was sent, not delivered\n        return (True, "Datagram sent (delivery not confirmed)")'),
            CodeBlock("F", '    except OSError as e:\n        return (False, f"Send failed: {e}")'),
            CodeBlock("G", '    finally:\n        sock.close()'),
            CodeBlock("X", '        return (True, "Message delivered successfully")', is_distractor=True, hint="UDP cannot confirm delivery"),
            CodeBlock("Y", "        sock.connect((host, port))\n        sock.send(message.encode('utf-8'))", is_distractor=True, hint="connect() not needed for UDP (and misleading)"),
            CodeBlock("Z", '    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)', is_distractor=True, hint="SOCK_STREAM is TCP, not UDP"),
        ],
        correct_order=["A", "B", "C", "D", "E", "F", "G"],
        explanation="UDP is connectionless; sendto() succeeds when packet is sent, not when delivered.",
    ),
    ParsonsProblem(
        id="P4",
        title="Apply Firewall Profile from JSON",
        description="Arrange the blocks to load a firewall profile from JSON and apply the rules using iptables commands.",
        lo_ref="LO5",
        difficulty="advanced",
        blocks=[
            CodeBlock("A", 'def apply_firewall_profile(profile_path: str, profile_name: str) -> bool:'),
            CodeBlock("B", "    with open(profile_path, 'r') as f:\n        profiles = json.load(f)"),
            CodeBlock("C", '    if profile_name not in profiles:\n        print(f"Profile \'{profile_name}\' not found")\n        return False'),
            CodeBlock("D", '    profile = profiles[profile_name]'),
            CodeBlock("E", "    # Clear existing rules in chain\n    subprocess.run(['iptables', '-F', 'FORWARD'], check=True)"),
            CodeBlock("F", "    # Set default policy\n    policy = profile.get('forward_policy', 'ACCEPT')\n    subprocess.run(['iptables', '-P', 'FORWARD', policy], check=True)"),
            CodeBlock("G", "    # Apply rules in order (first match wins)\n    for rule in profile.get('rules', []):"),
            CodeBlock("H", "        cmd = ['iptables', '-A', rule.get('chain', 'FORWARD')]\n        if 'proto' in rule:\n            cmd.extend(['-p', rule['proto']])\n        if 'dport' in rule:\n            cmd.extend(['--dport', str(rule['dport'])])\n        cmd.extend(['-j', rule.get('action', 'ACCEPT')])"),
            CodeBlock("I", '        subprocess.run(cmd, check=True)'),
            CodeBlock("J", '    return True'),
            CodeBlock("X", "    subprocess.run(['iptables', '-F'], check=True)  # Clears ALL chains", is_distractor=True, hint="-F without chain clears ALL chains including INPUT"),
            CodeBlock("Z", "    for rule in reversed(profile.get('rules', [])):  # Wrong order!", is_distractor=True, hint="Rules must be applied in order (first match wins)"),
            CodeBlock("W", '        cmd = f"iptables -A FORWARD {rule}"\n        os.system(cmd)', is_distractor=True, hint="Shell injection vulnerability and deprecated os.system"),
        ],
        correct_order=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
        explanation="Clear specific chain, set policy, then apply rules IN ORDER. Use list for subprocess to avoid shell injection.",
    ),
    ParsonsProblem(
        id="P5",
        title="Analyse PCAP with tshark",
        description="Arrange the blocks to analyse a PCAP file and extract TCP connection statistics.",
        lo_ref="LO4",
        difficulty="intermediate",
        blocks=[
            CodeBlock("A", 'def analyse_tcp_connections(pcap_path: str) -> dict:'),
            CodeBlock("B", "    cmd = [\n        'tshark', '-r', pcap_path,\n        '-q', '-z', 'conv,tcp'\n    ]"),
            CodeBlock("C", '    result = subprocess.run(cmd, capture_output=True, text=True)'),
            CodeBlock("D", "    if result.returncode != 0:\n        return {'error': result.stderr}"),
            CodeBlock("E", "    stats = {\n        'total_connections': 0,\n        'total_bytes': 0,\n        'connections': []\n    }"),
            CodeBlock("F", "    for line in result.stdout.split('\\n'):"),
            CodeBlock("G", "        if '<->' in line:  # Connection line format"),
            CodeBlock("H", "            parts = line.split()\n            if len(parts) >= 10:\n                stats['connections'].append({\n                    'endpoints': f\"{parts[0]} <-> {parts[2]}\",\n                    'frames': int(parts[4]) + int(parts[7]),\n                    'bytes': int(parts[5]) + int(parts[8])\n                })\n                stats['total_connections'] += 1"),
            CodeBlock("I", '    return stats'),
            CodeBlock("X", "    cmd = ['tshark', '-r', pcap_path, '-z', 'conv,tcp']  # Verbose output", is_distractor=True, hint="Without -q, output includes packet details making parsing harder"),
            CodeBlock("Y", "        stats['connections'].append(line)  # Raw line, not parsed", is_distractor=True, hint="Storing raw lines loses structured data"),
        ],
        correct_order=["A", "B", "C", "D", "E", "F", "G", "H", "I"],
        explanation="Use -q for quiet mode, check errors, then parse conversation statistics line by line.",
    ),
]


# ═══════════════════════════════════════════════════════════════════════════════
# PROBLEM RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

class ParsonsRunner:
    """Interactive Parsons problem runner."""
    
    def __init__(self, hints_enabled: bool = False):
        self.hints_enabled = hints_enabled
        self.problems = {p.id: p for p in PROBLEMS}
        self.results: dict[str, bool] = {}
    
    def run_problem(self, problem: ParsonsProblem) -> bool:
        """
        Run a single Parsons problem interactively.
        
        Returns:
            True if solved correctly
        """
        self._print_header(problem)
        
        # Shuffle blocks for presentation
        all_blocks = problem.blocks.copy()
        random.shuffle(all_blocks)
        
        # Display shuffled blocks
        self._print_blocks(all_blocks)
        
        # Get user answer
        print(f"\n{Fore.CYAN}Enter the correct order of block IDs (e.g., A B C D E):{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Tip: Exclude distractor blocks that don't belong in the solution.{Style.RESET_ALL}")
        
        try:
            answer = input(f"\n{Fore.GREEN}Your answer: {Style.RESET_ALL}").strip().upper()
        except (EOFError, KeyboardInterrupt):
            print("\n\nSkipped.")
            return False
        
        # Parse answer
        user_order = answer.replace(",", " ").split()
        
        # Check answer
        result = self._check_answer(problem, user_order)
        
        # Display result
        self._print_result(problem, result)
        
        return result.correct
    
    def _print_header(self, problem: ParsonsProblem) -> None:
        """Print problem header."""
        print(f"\n{'═' * 70}")
        print(f"{Fore.BLUE}{Style.BRIGHT}Problem {problem.id}: {problem.title}{Style.RESET_ALL}")
        print(f"{'═' * 70}")
        print(f"\n{Fore.WHITE}Learning Objective: {problem.lo_ref}")
        print(f"Difficulty: {problem.difficulty.title()}{Style.RESET_ALL}")
        print(f"\n{problem.description}")
    
    def _print_blocks(self, blocks: list[CodeBlock]) -> None:
        """Print code blocks."""
        print(f"\n{Fore.YELLOW}{'─' * 70}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}AVAILABLE BLOCKS (some may be distractors):{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'─' * 70}{Style.RESET_ALL}\n")
        
        for block in blocks:
            marker = f"{Fore.MAGENTA}[DISTRACTOR?]{Style.RESET_ALL}" if self.hints_enabled and block.is_distractor else ""
            print(f"{Fore.CYAN}[{block.id}]{Style.RESET_ALL} {marker}")
            for line in block.code.split('\n'):
                print(f"    {line}")
            if self.hints_enabled and block.hint:
                print(f"    {Fore.YELLOW}Hint: {block.hint}{Style.RESET_ALL}")
            print()
    
    def _check_answer(self, problem: ParsonsProblem, user_order: list[str]) -> AttemptResult:
        """Check if user's answer is correct."""
        correct_order = problem.correct_order
        
        # Check if answer matches
        if user_order == correct_order:
            return AttemptResult(
                correct=True,
                message="Perfect! All blocks are in the correct order."
            )
        
        # Detailed feedback
        hints = []
        correct_positions = []
        
        # Check for distractors included
        distractor_ids = {b.id for b in problem.blocks if b.is_distractor}
        included_distractors = [bid for bid in user_order if bid in distractor_ids]
        if included_distractors:
            hints.append(f"You included distractor block(s): {', '.join(included_distractors)}")
        
        # Check for missing blocks
        missing = set(correct_order) - set(user_order)
        if missing:
            hints.append(f"Missing required block(s): {', '.join(sorted(missing))}")
        
        # Check position correctness
        for i, bid in enumerate(user_order):
            if i < len(correct_order) and bid == correct_order[i]:
                correct_positions.append(True)
            else:
                correct_positions.append(False)
        
        correct_count = sum(correct_positions)
        total = len(correct_order)
        
        return AttemptResult(
            correct=False,
            message=f"Not quite right. {correct_count}/{total} blocks in correct position.",
            correct_positions=correct_positions,
            hints=hints,
        )
    
    def _print_result(self, problem: ParsonsProblem, result: AttemptResult) -> None:
        """Print result and feedback."""
        print(f"\n{'─' * 70}")
        
        if result.correct:
            print(f"{Fore.GREEN}{Style.BRIGHT}✓ CORRECT!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{result.message}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}{Style.BRIGHT}✗ INCORRECT{Style.RESET_ALL}")
            print(f"{Fore.RED}{result.message}{Style.RESET_ALL}")
            
            for hint in result.hints:
                print(f"{Fore.YELLOW}  • {hint}{Style.RESET_ALL}")
        
        # Show correct answer
        print(f"\n{Fore.CYAN}Correct order: {' → '.join(problem.correct_order)}{Style.RESET_ALL}")
        
        # Show explanation
        if problem.explanation:
            print(f"\n{Fore.WHITE}Explanation:{Style.RESET_ALL}")
            print(f"  {problem.explanation}")
    
    def run_all(self) -> dict[str, bool]:
        """Run all problems and return results."""
        print(f"\n{Fore.BLUE}{Style.BRIGHT}{'═' * 70}")
        print("PARSONS PROBLEMS — Week 7")
        print(f"{'═' * 70}{Style.RESET_ALL}")
        print(f"\nTotal problems: {len(PROBLEMS)}")
        if self.hints_enabled:
            print(f"{Fore.YELLOW}Hints are ENABLED{Style.RESET_ALL}")
        
        for problem in PROBLEMS:
            self.results[problem.id] = self.run_problem(problem)
            
            print(f"\n{Fore.CYAN}Press Enter to continue (or 'q' to quit)...{Style.RESET_ALL}")
            try:
                response = input()
                if response.lower() == 'q':
                    break
            except (EOFError, KeyboardInterrupt):
                break
        
        self._print_summary()
        return self.results
    
    def run_single(self, problem_id: str) -> bool:
        """Run a single problem by ID."""
        if problem_id not in self.problems:
            print(f"{Fore.RED}Problem '{problem_id}' not found.{Style.RESET_ALL}")
            print(f"Available: {', '.join(self.problems.keys())}")
            return False
        
        return self.run_problem(self.problems[problem_id])
    
    def _print_summary(self) -> None:
        """Print session summary."""
        print(f"\n{'═' * 70}")
        print(f"{Fore.BLUE}{Style.BRIGHT}SESSION SUMMARY{Style.RESET_ALL}")
        print(f"{'═' * 70}")
        
        correct = sum(1 for v in self.results.values() if v)
        total = len(self.results)
        
        for pid, passed in self.results.items():
            status = f"{Fore.GREEN}✓{Style.RESET_ALL}" if passed else f"{Fore.RED}✗{Style.RESET_ALL}"
            print(f"  {status} Problem {pid}")
        
        print(f"\n{Fore.CYAN}Score: {correct}/{total}{Style.RESET_ALL}")
        
        if correct == total:
            print(f"{Fore.GREEN}Excellent! All problems solved correctly.{Style.RESET_ALL}")
        elif correct >= total * 0.6:
            print(f"{Fore.YELLOW}Good progress! Review the missed problems.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}More practice needed. Review the code tracing exercises.{Style.RESET_ALL}")
    
    def show_review(self) -> None:
        """Show all solutions without interaction."""
        print(f"\n{Fore.BLUE}{Style.BRIGHT}{'═' * 70}")
        print("PARSONS PROBLEMS — Review Mode")
        print(f"{'═' * 70}{Style.RESET_ALL}")
        
        for problem in PROBLEMS:
            print(f"\n{Fore.CYAN}Problem {problem.id}: {problem.title}{Style.RESET_ALL}")
            print(f"LO: {problem.lo_ref} | Difficulty: {problem.difficulty}")
            print(f"\nCorrect order: {' → '.join(problem.correct_order)}")
            
            print(f"\n{Fore.GREEN}Solution code:{Style.RESET_ALL}")
            for block in problem.solution_blocks:
                for line in block.code.split('\n'):
                    print(f"  {line}")
            
            print(f"\n{Fore.YELLOW}Distractors:{Style.RESET_ALL}")
            for block in problem.distractor_blocks:
                print(f"  [{block.id}] {block.hint}")
            
            if problem.explanation:
                print(f"\n{Fore.WHITE}Explanation: {problem.explanation}{Style.RESET_ALL}")
            
            print(f"\n{'─' * 70}")


# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def build_parser() -> argparse.ArgumentParser:
    """Build command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Interactive Parsons problem runner for Week 7",
        epilog="Run without arguments for interactive mode"
    )
    
    parser.add_argument(
        "--problem", "-p",
        choices=[p.id for p in PROBLEMS],
        help="Run specific problem"
    )
    
    parser.add_argument(
        "--hints", "-H",
        action="store_true",
        help="Enable hints (marks distractors)"
    )
    
    parser.add_argument(
        "--review", "-r",
        action="store_true",
        help="Review mode (show all solutions)"
    )
    
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available problems"
    )
    
    return parser


def main() -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args()
    
    if args.list:
        print("Available Parsons Problems:")
        for p in PROBLEMS:
            print(f"  {p.id}: {p.title} ({p.lo_ref}, {p.difficulty})")
        return 0
    
    runner = ParsonsRunner(hints_enabled=args.hints)
    
    if args.review:
        runner.show_review()
        return 0
    
    if args.problem:
        success = runner.run_single(args.problem)
        return 0 if success else 1
    
    # Interactive mode
    results = runner.run_all()
    correct = sum(1 for v in results.values() if v)
    return 0 if correct >= len(results) * 0.6 else 1


if __name__ == "__main__":
    sys.exit(main())
