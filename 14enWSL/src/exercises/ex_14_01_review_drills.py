#!/usr/bin/env python3
"""ex_14_01_review_drills.py — Review drills for Week 14.

Computer Networks — Week 14 (WSL Environment)
ASE Bucharest, CSIE | by ing. dr. Antonio Clim

Objectives:
- Recall key networking concepts from the entire course
- Identify correct answers for protocol and layer questions
- Verify understanding through self-assessment

Level: Beginner to Intermediate
Estimated time: 20-30 minutes

Pair Programming Notes:
- Driver: Read questions aloud, type answers
- Navigator: Verify answers, look up explanations
- Swap after: Every 5 questions

Usage:
  python3 ex_14_01_review_drills.py --selftest
  python3 ex_14_01_review_drills.py --quiz 10
  python3 ex_14_01_review_drills.py --quiz 10 --out q.json
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations
import argparse
import json
import random
from typing import Dict, List, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# QUESTION_BANK
# ═══════════════════════════════════════════════════════════════════════════════
QUESTIONS: List[Tuple[str, List[str], int, str]] = [
    ("Which OSI layer is responsible for logical addressing (IP)?",
     ["Link (2)", "Network (3)", "Transport (4)", "Application (7)"], 1,
     "The Network layer (3) manages IP addressing and routing."),
    ("What PDU does the Transport layer use for TCP?",
     ["Frame", "Packet", "Segment", "Message"], 2,
     "TCP uses segments; UDP uses datagrams."),
    ("A MAC address has...",
     ["32 bits", "48 bits", "64 bits", "128 bits"], 1,
     "MAC addresses have 48 bits (6 bytes)."),
    ("What protocol resolves IP → MAC in local networks?",
     ["DNS", "DHCP", "ARP", "ICMP"], 2,
     "ARP maps IPs to MAC addresses."),
    ("Which TCP flag initiates a new connection?",
     ["ACK", "FIN", "SYN", "RST"], 2,
     "SYN starts the 3-way TCP handshake."),
    ("On which standard port does HTTP listen?",
     ["22", "53", "80", "443"], 2,
     "HTTP uses port 80; HTTPS uses 443."),
    ("What HTTP code indicates success?",
     ["200", "301", "404", "500"], 0,
     "200 OK = success."),
    ("What command checks which ports are listening on host?",
     ["ping localhost", "ss -lntp", "ip addr", "tcpdump -i lo"], 1,
     "ss -lntp shows TCP sockets in LISTEN."),
    ("How many usable IP addresses does a /24 network have?",
     ["254", "255", "256", "512"], 0,
     "/24 = 256 addresses, but 2 reserved → 254 usable."),
]

# ═══════════════════════════════════════════════════════════════════════════════
# PREDICTION_PROMPT
# ═══════════════════════════════════════════════════════════════════════════════
def prompt_prediction() -> None:
    """Ask student to predict their score before starting."""
    print("\n💭 PREDICTION: How many questions do you expect to answer correctly?")
    try:
        prediction = input(f"   Your prediction (0-{len(QUESTIONS)}): ").strip()
        if prediction:
            print(f"   You predicted: {prediction}/{len(QUESTIONS)}. Let's see!\n")
    except (EOFError, KeyboardInterrupt):
        print("\n")

# ═══════════════════════════════════════════════════════════════════════════════
# SELFTEST_RUNNER
# ═══════════════════════════════════════════════════════════════════════════════
def run_selftest() -> Tuple[int, int]:
    """Run interactive self-test."""
    print("\n" + "=" * 60)
    print("  Self-Test Review — Week 14")
    print("=" * 60)
    prompt_prediction()
    
    questions = QUESTIONS.copy()
    random.shuffle(questions)
    correct = 0
    
    for i, (question, options, answer_idx, explanation) in enumerate(questions, 1):
        print(f"\nQuestion {i}/{len(questions)}:\n  {question}\n")
        for j, opt in enumerate(options):
            print(f"    {j + 1}. {opt}")
        
        while True:
            try:
                user_input = input("\nAnswer (1-4, or 'q' to quit): ").strip()
                if user_input.lower() == 'q':
                    return correct, i - 1
                user_answer = int(user_input) - 1
                if 0 <= user_answer < len(options):
                    break
            except ValueError:
                pass
            print("Enter a valid number.")
        
        if user_answer == answer_idx:
            print("✓ Correct!")
            correct += 1
        else:
            print(f"✗ Wrong. Answer: {answer_idx + 1}. {options[answer_idx]}")
        print(f"  Explanation: {explanation}")
    
    return correct, len(questions)

# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════
def generate_quiz(n: int) -> List[Dict]:
    """Generate quiz with N random questions."""
    questions = random.sample(QUESTIONS, min(n, len(QUESTIONS)))
    return [{"question": q, "options": opts, "correct_index": ans_idx,
             "correct_answer": opts[ans_idx], "explanation": expl}
            for q, opts, ans_idx, expl in questions]

# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGUMENTS
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Review drills — Week 14")
    parser.add_argument("--selftest", action="store_true", help="Run interactive test")
    parser.add_argument("--quiz", type=int, help="Generate quiz with N questions")
    parser.add_argument("--out", help="Output file for quiz (JSON)")
    parser.add_argument("--list", action="store_true", help="List all questions")
    return parser.parse_args()

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    args = parse_args()
    
    if args.selftest:
        correct, total = run_selftest()
        print("\n" + "=" * 60)
        print(f"  Final score: {correct}/{total} ({100 * correct // total if total else 0}%)")
        print("=" * 60)
        print("\n💭 REFLECTION: Compare your score to your prediction.\n")
        return 0 if correct == total else 1
    elif args.quiz:
        quiz = generate_quiz(args.quiz)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                json.dump(quiz, f, indent=2, ensure_ascii=False)
            print(f"Quiz saved to: {args.out}")
        else:
            print(json.dumps(quiz, indent=2, ensure_ascii=False))
        return 0
    elif args.list:
        for i, (q, opts, ans_idx, _) in enumerate(QUESTIONS, 1):
            print(f"{i}. {q}\n   Answer: {opts[ans_idx]}\n")
        return 0
    else:
        print("Usage: python3 ex_14_01_review_drills.py --selftest")
        return 0

if __name__ == "__main__":
    raise SystemExit(main())
