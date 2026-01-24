#!/usr/bin/env python3
"""
Exercise 5.03 – Interactive Quiz Generator
===========================================
Generates questions for CIDR, VLSM and IPv6 practice.

Usage:
    python ex_5_03_quiz_generator.py --count 5
    python ex_5_03_quiz_generator.py --interactive
    python ex_5_03_quiz_generator.py --type cidr --count 3

Learning Objectives:
    - Reinforce CIDR analysis through self-assessment
    - Practice FLSM and VLSM calculations under time pressure
    - Verify understanding of IPv6 addressing concepts

Pair Programming Notes:
    - Driver: Answer the questions
    - Navigator: Verify calculations, provide hints if stuck
    - Swap roles after each complete quiz round

Author: ing. dr. Antonio Clim, ASE-CSIE Bucharest
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import ipaddress
import random
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURE_MODULE_PATH
# ═══════════════════════════════════════════════════════════════════════════════
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT_UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════
from src.utils.net_utils import analyze_ipv4_interface, ipv4_host_range


# ═══════════════════════════════════════════════════════════════════════════════
# DEFINE_COLOUR_CODES
# ═══════════════════════════════════════════════════════════════════════════════
class Colours:
    """ANSI colour codes for terminal output."""
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


def colourise(text: str, colour: str) -> str:
    """
    Apply colour formatting if stdout is a terminal.
    
    Args:
        text: The text to colourise
        colour: ANSI colour code from Colours class
        
    Returns:
        Coloured text if terminal, plain text otherwise
    """
    if sys.stdout.isatty():
        return f"{colour}{text}{Colours.END}"
    return text


# ═══════════════════════════════════════════════════════════════════════════════
# DEFINE_DATA_STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class QuizQuestion:
    """Structure for a quiz question."""
    question: str
    correct_answer: str
    hint: Optional[str] = None
    explanation: Optional[str] = None
    category: str = "general"


# ═══════════════════════════════════════════════════════════════════════════════
# GENERATE_CIDR_QUESTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def generate_cidr_question() -> QuizQuestion:
    """
    Generate a question about CIDR analysis.
    
    Creates random IPv4 addresses with various prefix lengths
    and asks about network parameters.
    
    Returns:
        QuizQuestion with CIDR-related content
    """
    # Generate random address
    octets = [random.randint(1, 254) for _ in range(4)]
    prefix = random.choice([24, 25, 26, 27, 28, 29, 30])
    
    ip = '.'.join(map(str, octets))
    cidr = f"{ip}/{prefix}"
    
    # Calculate the answer
    info = analyze_ipv4_interface(cidr)
    
    # Choose question type
    q_type = random.choice([
        "network", "broadcast", "hosts", "first_host", "last_host", "netmask"
    ])
    
    if q_type == "network":
        question = f"What is the network address for {cidr}?"
        answer = str(info.network.network_address)
        explanation = f"The network address is obtained by setting all host bits to 0. For /{prefix}, we have {32-prefix} host bits."
    elif q_type == "broadcast":
        question = f"What is the broadcast address for {cidr}?"
        answer = str(info.broadcast)
        explanation = "The broadcast address is obtained by setting all host bits to 1."
    elif q_type == "hosts":
        question = f"How many usable hosts does the network {cidr} have?"
        answer = str(info.usable_hosts)
        explanation = f"Hosts = 2^{32-prefix} - 2 = {info.usable_hosts} (we subtract network and broadcast addresses)"
    elif q_type == "first_host":
        question = f"What is the first usable host address in {cidr}?"
        answer = str(info.first_host)
        explanation = "First host = network address + 1"
    elif q_type == "last_host":
        question = f"What is the last usable host address in {cidr}?"
        answer = str(info.last_host)
        explanation = "Last host = broadcast address - 1"
    else:  # netmask
        question = f"What is the network mask for prefix /{prefix}?"
        answer = str(info.netmask)
        explanation = f"The mask is obtained by setting the first {prefix} bits to 1 and the rest to 0"
    
    return QuizQuestion(
        question=question,
        correct_answer=answer,
        explanation=explanation,
        category="cidr"
    )


# ═══════════════════════════════════════════════════════════════════════════════
# GENERATE_FLSM_QUESTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def generate_flsm_question() -> QuizQuestion:
    """
    Generate a question about FLSM subnetting.
    
    Creates scenarios involving fixed-length subnet mask calculations.
    
    Returns:
        QuizQuestion with FLSM-related content
    """
    # Base network
    base_prefixes = [16, 20, 22, 24]
    base_prefix = random.choice(base_prefixes)
    
    first_octet = random.choice([10, 172, 192])
    if first_octet == 10:
        ip = f"10.{random.randint(0,255)}.0.0"
    elif first_octet == 172:
        ip = f"172.{random.randint(16,31)}.0.0"
    else:
        ip = f"192.168.{random.randint(0,255)}.0"
    
    base_cidr = f"{ip}/{base_prefix}"
    
    # Number of subnets
    num_subnets = random.choice([2, 4, 8, 16])
    bits_needed = num_subnets.bit_length() - 1
    new_prefix = base_prefix + bits_needed
    
    q_type = random.choice(["new_prefix", "num_hosts", "increment"])
    
    if q_type == "new_prefix":
        question = f"If we divide {base_cidr} into {num_subnets} equal subnets, what will be the new prefix?"
        answer = f"/{new_prefix}"
        explanation = f"We borrow log₂({num_subnets}) = {bits_needed} bits. New prefix = {base_prefix} + {bits_needed} = {new_prefix}"
    elif q_type == "num_hosts":
        hosts_per_subnet = 2**(32-new_prefix) - 2
        question = f"How many usable hosts will each subnet have if we divide {base_cidr} into {num_subnets} parts?"
        answer = str(hosts_per_subnet)
        explanation = f"Each subnet has prefix /{new_prefix}, so {32-new_prefix} host bits: 2^{32-new_prefix} - 2 = {hosts_per_subnet}"
    else:  # increment
        increment = 2**(32-new_prefix)
        question = f"What is the increment between subnets resulting from dividing {base_cidr} into {num_subnets}?"
        answer = str(increment)
        explanation = f"Increment = 2^(32 - {new_prefix}) = {increment}"
    
    return QuizQuestion(
        question=question,
        correct_answer=answer,
        explanation=explanation,
        category="flsm"
    )


# ═══════════════════════════════════════════════════════════════════════════════
# GENERATE_VLSM_QUESTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def generate_vlsm_question() -> QuizQuestion:
    """
    Generate a question about VLSM.
    
    Focuses on calculating minimum prefix for host requirements.
    
    Returns:
        QuizQuestion with VLSM-related content
    """
    # Host requirement
    hosts_needed = random.choice([5, 10, 20, 30, 50, 60, 100, 120])
    
    # Calculate prefix
    import math
    host_bits = math.ceil(math.log2(hosts_needed + 2))
    prefix = 32 - host_bits
    usable = 2**host_bits - 2
    
    question = f"What is the minimum CIDR prefix needed to host {hosts_needed} hosts?"
    answer = f"/{prefix}"
    explanation = f"We need {hosts_needed}+2 = {hosts_needed+2} addresses. The smallest power of 2 >= {hosts_needed+2} is {2**host_bits}, so {host_bits} host bits → prefix /{prefix} (provides {usable} usable hosts)"
    
    return QuizQuestion(
        question=question,
        correct_answer=answer,
        explanation=explanation,
        category="vlsm"
    )


# ═══════════════════════════════════════════════════════════════════════════════
# GENERATE_IPV6_QUESTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def generate_ipv6_question() -> QuizQuestion:
    """
    Generate a question about IPv6.
    
    Covers compression, expansion and address type identification.
    
    Returns:
        QuizQuestion with IPv6-related content
    """
    q_type = random.choice(["compress", "expand", "type"])
    
    if q_type == "compress":
        # Generate a long address
        groups = []
        zero_start = random.randint(1, 5)
        zero_count = random.randint(2, 4)
        
        for i in range(8):
            if zero_start <= i < zero_start + zero_count:
                groups.append("0000")
            else:
                # Generate group with leading zeros
                val = random.randint(0, 255)
                groups.append(f"00{val:02x}" if random.random() < 0.5 else f"{val:04x}")
        
        full_addr = ':'.join(groups)
        compressed = str(ipaddress.IPv6Address(full_addr))
        
        question = f"Compress the IPv6 address: {full_addr}"
        answer = compressed
        explanation = "Remove leading zeros from each group and use :: for the longest sequence of zeros"
        
    elif q_type == "expand":
        # Known short addresses
        short_addrs = [
            ("2001:db8::1", "2001:0db8:0000:0000:0000:0000:0000:0001"),
            ("fe80::1", "fe80:0000:0000:0000:0000:0000:0000:0001"),
            ("::1", "0000:0000:0000:0000:0000:0000:0000:0001"),
            ("2001:db8:10::cafe", "2001:0db8:0010:0000:0000:0000:0000:cafe"),
        ]
        short, full = random.choice(short_addrs)
        
        question = f"Expand the IPv6 address: {short}"
        answer = full
        explanation = "Replace :: with the corresponding zero sequence and pad each group to 4 digits"
        
    else:  # type
        type_questions = [
            ("fe80::1", "link-local"),
            ("2001:db8::1", "global unicast"),
            ("::1", "loopback"),
            ("ff02::1", "multicast"),
            ("fc00::1", "unique local"),
        ]
        addr, addr_type = random.choice(type_questions)
        
        question = f"What type of IPv6 address is {addr}?"
        answer = addr_type
        explanation = f"The prefix {addr.split('::')[0] if '::' in addr else addr.split(':')[0]} indicates the {addr_type} type"
    
    return QuizQuestion(
        question=question,
        correct_answer=answer,
        explanation=explanation,
        category="ipv6"
    )


# ═══════════════════════════════════════════════════════════════════════════════
# GENERATE_QUESTION_SET
# ═══════════════════════════════════════════════════════════════════════════════
def generate_questions(count: int, q_type: Optional[str] = None) -> List[QuizQuestion]:
    """
    Generate a list of quiz questions.
    
    Args:
        count: Number of questions to generate
        q_type: Optional filter for question category
        
    Returns:
        List of QuizQuestion objects
    """
    generators = {
        "cidr": generate_cidr_question,
        "flsm": generate_flsm_question,
        "vlsm": generate_vlsm_question,
        "ipv6": generate_ipv6_question,
    }
    
    questions = []
    for _ in range(count):
        if q_type and q_type in generators:
            gen = generators[q_type]
        else:
            gen = random.choice(list(generators.values()))
        
        questions.append(gen())
    
    return questions


# ═══════════════════════════════════════════════════════════════════════════════
# RUN_BATCH_MODE
# ═══════════════════════════════════════════════════════════════════════════════
def run_quiz_batch(count: int, q_type: Optional[str] = None) -> int:
    """
    Run a quiz in batch mode (prints all questions with answers).
    
    Args:
        count: Number of questions
        q_type: Optional filter for question category
        
    Returns:
        Exit code (0 for success)
    """
    questions = generate_questions(count, q_type)
    
    print()
    print(colourise("═" * 60, Colours.BLUE))
    print(colourise("  Subnetting Quiz - Question Set", Colours.BOLD))
    print(colourise("═" * 60, Colours.BLUE))
    print()
    
    for i, q in enumerate(questions, 1):
        category_colour = {
            "cidr": Colours.CYAN,
            "flsm": Colours.GREEN,
            "vlsm": Colours.YELLOW,
            "ipv6": Colours.RED,
        }.get(q.category, Colours.BLUE)
        
        print(f"  {colourise(f'Question {i}', Colours.BOLD)} [{colourise(q.category.upper(), category_colour)}]")
        print(f"  {q.question}")
        print()
        print(f"  {colourise('Answer:', Colours.GREEN)} {q.correct_answer}")
        if q.explanation:
            print(f"  {colourise('Explanation:', Colours.CYAN)} {q.explanation}")
        print(colourise("─" * 60, Colours.BLUE))
        print()
    
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# RUN_INTERACTIVE_MODE
# ═══════════════════════════════════════════════════════════════════════════════
def run_quiz_interactive(count: int = 5, q_type: Optional[str] = None) -> int:
    """
    Run an interactive quiz with user input.
    
    Args:
        count: Number of questions
        q_type: Optional filter for question category
        
    Returns:
        Exit code (0 for success)
    """
    questions = generate_questions(count, q_type)
    
    print()
    print(colourise("═" * 60, Colours.BLUE))
    print(colourise("  Interactive Subnetting Quiz", Colours.BOLD))
    print(colourise("═" * 60, Colours.BLUE))
    print()
    print(f"  You will receive {count} questions. Enter your answer or press Enter to skip.")
    print("  Type 'quit' to exit.")
    print()
    
    correct = 0
    skipped = 0
    
    for i, q in enumerate(questions, 1):
        category_colour = {
            "cidr": Colours.CYAN,
            "flsm": Colours.GREEN,
            "vlsm": Colours.YELLOW,
            "ipv6": Colours.RED,
        }.get(q.category, Colours.BLUE)
        
        print(colourise("─" * 60, Colours.BLUE))
        print(f"  {colourise(f'Question {i}/{count}', Colours.BOLD)} [{colourise(q.category.upper(), category_colour)}]")
        print(f"  {q.question}")
        print()
        
        try:
            answer = input(f"  {colourise('Your answer:', Colours.CYAN)} ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        
        if answer.lower() == 'quit':
            break
        
        if not answer:
            skipped += 1
            print(f"  {colourise('Skipped.', Colours.YELLOW)} Correct answer: {colourise(q.correct_answer, Colours.GREEN)}")
        elif answer.lower().replace('/', '').replace(' ', '') == q.correct_answer.lower().replace('/', '').replace(' ', ''):
            correct += 1
            print(f"  {colourise('✓ Correct!', Colours.GREEN)}")
        else:
            print(f"  {colourise('✗ Wrong.', Colours.RED)} Correct answer: {colourise(q.correct_answer, Colours.GREEN)}")
        
        if q.explanation:
            print(f"  {colourise('Explanation:', Colours.CYAN)} {q.explanation}")
        print()
    
    # ─────────────────────────────────────────────────────────────────────────
    # DISPLAY_FINAL_RESULTS
    # ─────────────────────────────────────────────────────────────────────────
    answered = count - skipped
    percentage = (correct / answered * 100) if answered > 0 else 0
    
    print(colourise("═" * 60, Colours.BLUE))
    print(colourise("  Final Result", Colours.BOLD))
    print(colourise("═" * 60, Colours.BLUE))
    print()
    print(f"  Correct answers: {colourise(str(correct), Colours.GREEN)}/{answered}")
    print(f"  Questions skipped: {skipped}")
    print(f"  Score:             {colourise(f'{percentage:.0f}%', Colours.YELLOW)}")
    print()
    
    if percentage >= 80:
        print(f"  {colourise('Excellent! You have mastered subnetting!', Colours.GREEN)}")
    elif percentage >= 60:
        print(f"  {colourise('Good! Keep practising for perfection.', Colours.YELLOW)}")
    else:
        print(f"  {colourise('More work needed. Review the theory and try again.', Colours.RED)}")
    print()
    
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD_ARGUMENT_PARSER
# ═══════════════════════════════════════════════════════════════════════════════
def build_parser() -> argparse.ArgumentParser:
    """
    Build the command-line argument parser.
    
    Returns:
        Configured ArgumentParser with all options
    """
    parser = argparse.ArgumentParser(
        description="Interactive Quiz Generator for Subnetting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --count 5                    5 random questions
  %(prog)s --interactive                Interactive quiz
  %(prog)s --type cidr --count 3        3 CIDR-only questions
  %(prog)s --type vlsm --interactive    Interactive VLSM quiz
"""
    )
    
    parser.add_argument(
        "--count", "-n",
        type=int,
        default=5,
        help="Number of questions (default: 5)"
    )
    
    parser.add_argument(
        "--type", "-t",
        choices=["cidr", "flsm", "vlsm", "ipv6"],
        help="Question type (default: all)"
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Interactive mode (answer questions)"
    )
    
    return parser


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main(argv: Optional[List[str]] = None) -> int:
    """
    Main entry point for the quiz generator.
    
    Args:
        argv: Command-line arguments (defaults to sys.argv)
        
    Returns:
        Exit code (0 for success)
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    
    if args.interactive:
        return run_quiz_interactive(args.count, args.type)
    else:
        return run_quiz_batch(args.count, args.type)


if __name__ == "__main__":
    sys.exit(main())
