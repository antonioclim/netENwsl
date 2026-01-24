#!/usr/bin/env python3
"""
Homework 12.2: RPC Protocol Comparison and Benchmarking
=======================================================
Computer Networks - Week 12 (WSL Environment)
ASE Bucharest, CSIE | by ing. dr. Antonio Clim

Objectives:
- Compare XML-RPC, JSON-RPC and gRPC protocols
- Analyse payload sizes and encoding overhead
- Understand trade-offs for different use cases

Level: Intermediate (⭐⭐⭐)
Estimated time: 75-90 minutes
"""

from __future__ import annotations
import json
import sys
from dataclasses import dataclass
from typing import Dict, List

# ═══════════════════════════════════════════════════════════════════════════════
# DATA_STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class BenchmarkResult:
    """Results from a benchmark run."""
    protocol: str
    avg_latency_ms: float
    throughput_ops: float
    avg_payload_bytes: int

# ═══════════════════════════════════════════════════════════════════════════════
# PAYLOAD_COMPARISON
# ═══════════════════════════════════════════════════════════════════════════════
def compare_payload_sizes() -> Dict[str, int]:
    """Compare payload sizes for the same operation."""
    a, b = 42, 58
    
    # XML-RPC
    xml_request = f"""<?xml version="1.0"?>
<methodCall>
<methodName>add</methodName>
<params>
<param><value><int>{a}</int></value></param>
<param><value><int>{b}</int></value></param>
</params>
</methodCall>"""
    
    # JSON-RPC
    json_request = {"jsonrpc": "2.0", "method": "add", "params": [a, b], "id": 1}
    
    return {
        "XML-RPC": len(xml_request),
        "JSON-RPC": len(json.dumps(json_request)),
        "gRPC": 6  # Protocol Buffers estimate
    }

def display_payload_comparison(sizes: Dict[str, int]) -> None:
    """Display payload size comparison."""
    print("\n" + "=" * 50)
    print("PAYLOAD SIZE COMPARISON")
    print("=" * 50)
    
    sorted_sizes = sorted(sizes.items(), key=lambda x: x[1])
    smallest = sorted_sizes[0][1]
    
    for protocol, size in sorted_sizes:
        ratio = size / smallest
        bar = "█" * int(ratio * 10)
        print(f"{protocol:<12} {size:>5} bytes  {bar} ({ratio:.1f}x)")

def display_comparison_table(results: List[BenchmarkResult]) -> None:
    """Display benchmark results."""
    print("\n" + "=" * 80)
    print("BENCHMARK COMPARISON (simulated)")
    print("=" * 80)
    print(f"{'Protocol':<12} {'Avg (ms)':<12} {'Ops/sec':<12} {'Payload':<12}")
    print("-" * 80)
    for r in results:
        print(f"{r.protocol:<12} {r.avg_latency_ms:<12.2f} {r.throughput_ops:<12.1f} {r.avg_payload_bytes:<12}")

def print_protocol_comparison() -> None:
    """Print educational comparison."""
    print("""
┌──────────────┬──────────────┬──────────────┬─────────────────────────────┐
│ Aspect       │ XML-RPC      │ JSON-RPC     │ gRPC                        │
├──────────────┼──────────────┼──────────────┼─────────────────────────────┤
│ Encoding     │ XML          │ JSON         │ Protocol Buffers (binary)   │
│ Transport    │ HTTP         │ HTTP         │ HTTP/2                      │
│ Readability  │ Verbose      │ Readable     │ Binary (not human-readable) │
│ Performance  │ Slowest      │ Medium       │ Fastest                     │
│ Streaming    │ No           │ No           │ Yes (bidirectional)         │
├──────────────┼──────────────┼──────────────┼─────────────────────────────┤
│ Best for     │ Legacy       │ Web APIs     │ Microservices               │
└──────────────┴──────────────┴──────────────┴─────────────────────────────┘
    """)

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    print("=" * 70)
    print("Homework 12.2: RPC Protocol Comparison")
    print("Computer Networks - Week 12 | ASE Bucharest, CSIE")
    print("=" * 70)
    
    print_protocol_comparison()
    
    sizes = compare_payload_sizes()
    display_payload_comparison(sizes)
    
    # Simulated benchmark results
    results = [
        BenchmarkResult("XML-RPC", 8.5, 117.6, sizes["XML-RPC"]),
        BenchmarkResult("JSON-RPC", 4.2, 238.1, sizes["JSON-RPC"]),
        BenchmarkResult("gRPC", 1.1, 909.1, sizes["gRPC"]),
    ]
    display_comparison_table(results)
    
    print("\n📊 Key Findings:")
    print(f"   • gRPC is ~{results[0].avg_latency_ms / results[2].avg_latency_ms:.1f}x faster than XML-RPC")
    print(f"   • gRPC payload is ~{sizes['XML-RPC'] / sizes['gRPC']:.0f}x smaller than XML-RPC")
    
    print("\n📝 When to use each:")
    print("   • XML-RPC: Legacy system integration")
    print("   • JSON-RPC: Web services, debugging")
    print("   • gRPC: Microservices, mobile backends")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
