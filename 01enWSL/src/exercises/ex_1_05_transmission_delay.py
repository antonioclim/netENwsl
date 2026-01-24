#!/usr/bin/env python3
"""
Exercise 1.05: Transmission Delay Calculator
============================================
Computer Networks - Week 1 (WSL Environment)
ASE Bucharest | by ing. dr. Antonio Clim

Objectives:
- Explain the difference between transmission delay and propagation delay
- Apply the transmission delay formula
- Evaluate how link speed affects network performance

Prerequisites:
- Understanding of bits vs bytes (1 byte = 8 bits)
- Understanding of metric prefixes (mega = 10^6)

Level: Beginner
Estimated time: 10 minutes

Pair Programming Notes:
- Driver: Calculate the delay for given parameters
- Navigator: Verify unit conversions are correct
- Swap after: First calculation, before varying parameters

Formula:
    transmission_delay = packet_size_bits / link_rate_bits_per_second

Key Insight:
    Transmission delay is how long to PUSH bits onto the wire.
    Propagation delay is how long bits take to TRAVEL the wire.
    Total delay = transmission + propagation + processing + queuing
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations
from typing import Optional, List, Dict, Tuple, Any

import argparse
import sys


# ═══════════════════════════════════════════════════════════════════════════════
# PREDICTION_PROMPT
# ═══════════════════════════════════════════════════════════════════════════════
def prompt_prediction(size_bytes: int, rate_mbps: float) -> None:
    """
    Ask student to predict transmission delay (Brown & Wilson Principle 4).
    """
    print("\n" + "=" * 60)
    print("💭 PREDICTION: TRANSMISSION DELAY")
    print("=" * 60)
    print(f"  Packet size: {size_bytes} bytes")
    print(f"  Link rate: {rate_mbps} Mbps")
    print()
    print("Before calculating, predict:")
    print("  1. Will the delay be in microseconds, milliseconds or seconds?")
    print("  2. How would doubling the link rate affect the delay?")
    print("     (double / halve / no change)")
    print("  3. How would doubling the packet size affect the delay?")
    print("     (double / halve / no change)")
    print()
    print("Hints:")
    print("  - 1 byte = 8 bits")
    print("  - 1 Mbps = 1,000,000 bits per second")
    print("  - Ethernet MTU is typically 1500 bytes")
    print("=" * 60)
    input("Press Enter to continue...")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# CALCULATE_DELAY
# ═══════════════════════════════════════════════════════════════════════════════
def calculate_transmission_delay(size_bytes: int, rate_mbps: float) -> dict:
    """
    Calculate transmission delay with unit conversions.
    
    Transmission delay = (packet bits) / (link bits per second)
    
    Args:
        size_bytes: Packet size in bytes
        rate_mbps: Link rate in megabits per second
        
    Returns:
        Dictionary with calculation steps and results
    """
    # Convert to consistent units
    size_bits = size_bytes * 8
    rate_bps = rate_mbps * 1_000_000.0
    
    # Calculate delay
    delay_seconds = size_bits / rate_bps
    delay_ms = delay_seconds * 1_000.0
    delay_us = delay_seconds * 1_000_000.0
    
    return {
        "size_bytes": size_bytes,
        "size_bits": size_bits,
        "rate_mbps": rate_mbps,
        "rate_bps": rate_bps,
        "delay_s": delay_seconds,
        "delay_ms": delay_ms,
        "delay_us": delay_us,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# OUTPUT_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def display_results(calc: dict) -> None:
    """
    Display calculation with step-by-step explanation.
    """
    print("\n" + "=" * 60)
    print("📊 TRANSMISSION DELAY CALCULATION")
    print("=" * 60)
    
    # Show step by step
    print("\n📝 STEP-BY-STEP:")
    print(f"  1. Convert packet size to bits:")
    print(f"     {calc['size_bytes']} bytes × 8 = {calc['size_bits']} bits")
    print()
    print(f"  2. Convert link rate to bits per second:")
    print(f"     {calc['rate_mbps']} Mbps × 1,000,000 = {calc['rate_bps']:,.0f} bps")
    print()
    print(f"  3. Apply formula: delay = size / rate")
    print(f"     {calc['size_bits']} bits / {calc['rate_bps']:,.0f} bps = {calc['delay_s']:.9f} seconds")
    
    print("\n📏 RESULT:")
    print(f"  {calc['delay_s']:.9f} seconds")
    print(f"  = {calc['delay_ms']:.6f} milliseconds")
    print(f"  = {calc['delay_us']:.2f} microseconds")
    
    # Interpretation
    print("\n💡 INTERPRETATION:")
    if calc['delay_us'] < 100:
        print("  ⚡ Very fast - typical for modern high-speed links")
    elif calc['delay_us'] < 1000:
        print("  🟢 Fast - minimal transmission delay")
    elif calc['delay_ms'] < 10:
        print("  🟡 Moderate - noticeable for real-time applications")
    else:
        print("  🔴 Slow - significant transmission delay")
    
    # Comparison table
    print("\n📊 COMPARISON (for {0} byte packet):".format(calc['size_bytes']))
    print("  ┌──────────────┬────────────────┐")
    print("  │ Link Speed   │ Trans. Delay   │")
    print("  ├──────────────┼────────────────┤")
    
    for rate in [10, 100, 1000, 10000]:
        delay_us = (calc['size_bytes'] * 8) / (rate * 1_000_000) * 1_000_000
        marker = " ◀" if rate == calc['rate_mbps'] else ""
        print(f"  │ {rate:6d} Mbps │ {delay_us:10.2f} µs │{marker}")
    
    print("  └──────────────┴────────────────┘")
    print("=" * 60)


# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGUMENTS
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    ap = argparse.ArgumentParser(
        description="Compute transmission delay for a packet on a link.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 ex_1_05_transmission_delay.py --size-bytes 1500 --rate-mbps 100
  python3 ex_1_05_transmission_delay.py --size-bytes 64 --rate-mbps 1000
  python3 ex_1_05_transmission_delay.py --no-predict
        """
    )
    ap.add_argument("--size-bytes", type=int, default=1500, 
                    help="Packet size in bytes (default: 1500, Ethernet MTU)")
    ap.add_argument("--rate-mbps", type=float, default=100.0, 
                    help="Link rate in megabits per second (default: 100)")
    ap.add_argument("--no-predict", action="store_true",
                    help="Skip prediction prompt")
    return ap.parse_args()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """
    Main entry point.
    
    Returns:
        Exit code (0 for success)
    """
    args = parse_args()
    
    # Validation
    if args.size_bytes <= 0:
        print("❌ Packet size must be positive")
        return 1
    if args.rate_mbps <= 0:
        print("❌ Link rate must be positive")
        return 1
    
    # Prediction prompt
    if not args.no_predict:
        prompt_prediction(args.size_bytes, args.rate_mbps)
    
    # Calculate
    calc = calculate_transmission_delay(args.size_bytes, args.rate_mbps)
    
    # Display
    display_results(calc)
    
    # Legacy format for test compatibility
    print(f"\nTX_DELAY size_bytes={args.size_bytes} rate_mbps={args.rate_mbps} delay_us={calc['delay_us']:.2f}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
