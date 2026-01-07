#!/usr/bin/env python3
"""
Homework Exercise 7.02: Network Failure Analysis Report
NETWORKING class - ASE, Informatics | by Revolvix

Objective:
Develop systematic diagnostic skills by analysing packet captures to determine
the root cause of simulated network failures.

Scenario:
You are a network administrator. Users are reporting that certain services are
unreachable. Your task is to capture traffic, analyse the results, and produce
a professional incident report.

Requirements:
1. Run the failure simulation scenarios below
2. Capture traffic for each scenario using Wireshark
3. Identify the packet-level evidence that reveals the failure type
4. Produce a formal incident report for each scenario

Deliverables:
- Three PCAP files (one per scenario)
- A written incident report (1000-1500 words) containing:
  - Executive summary
  - Methodology (how you captured and analysed traffic)
  - Findings for each scenario with packet-level evidence
  - Root cause analysis
  - Recommendations

Scenarios:
1. TCP service suddenly unreachable (REJECT behaviour)
2. UDP service becomes unresponsive (DROP behaviour)  
3. Application-layer filtering blocks specific content
"""

from __future__ import annotations

import argparse
import socket
import subprocess
import sys
import time
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def run_scenario_1() -> tuple[bool, str]:
    """
    Scenario 1: TCP REJECT
    
    This simulates a firewall rule that REJECTs TCP connections.
    The student should observe:
    - TCP SYN sent
    - TCP RST received (or ICMP port unreachable)
    - Connection immediately fails
    """
    print("\n" + "=" * 50)
    print("SCENARIO 1: TCP Service Unreachable")
    print("=" * 50)
    print()
    print("Simulating: Firewall REJECT rule on TCP port 9090")
    print()
    print("Instructions:")
    print("1. Start Wireshark capture on the Docker network interface")
    print("2. Apply filter: tcp.port == 9090")
    print("3. Observe the connection attempt below")
    print("4. Save capture as: pcap/hw_scenario_1.pcap")
    print()
    
    input("Press Enter when ready to begin capture...")
    
    # Attempt connection that will be rejected
    print("\nAttempting TCP connection to localhost:9090...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex(("localhost", 9090))
        sock.close()
        
        if result == 0:
            return True, "Connection succeeded (expected if no filter active)"
        else:
            return False, f"Connection failed with errno {result}"
    
    except ConnectionRefusedError:
        return False, "Connection refused (RST received - REJECT behaviour)"
    except socket.timeout:
        return False, "Connection timed out (possible DROP instead of REJECT)"
    except Exception as e:
        return False, f"Error: {e}"


def run_scenario_2() -> tuple[bool, str]:
    """
    Scenario 2: UDP DROP
    
    This simulates a firewall rule that silently DROPs UDP packets.
    The student should observe:
    - UDP datagram sent
    - No response received
    - Sender cannot distinguish between DROP and packet loss
    """
    print("\n" + "=" * 50)
    print("SCENARIO 2: UDP Service Unresponsive")
    print("=" * 50)
    print()
    print("Simulating: Firewall DROP rule on UDP port 9091")
    print()
    print("Instructions:")
    print("1. Start/continue Wireshark capture")
    print("2. Apply filter: udp.port == 9091")
    print("3. Observe the datagram below")
    print("4. Note: You should see outgoing UDP but NO response")
    print("5. Save capture as: pcap/hw_scenario_2.pcap")
    print()
    
    input("Press Enter when ready to begin capture...")
    
    # Send UDP datagram that will be dropped
    print("\nSending UDP datagram to localhost:9091...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(3)
        
        msg = b"test_homework_scenario_2"
        sock.sendto(msg, ("localhost", 9091))
        
        print("Datagram sent. Waiting for response (will likely timeout)...")
        
        try:
            response, addr = sock.recvfrom(1024)
            return True, f"Received response: {response}"
        except socket.timeout:
            return False, "No response (consistent with DROP behaviour)"
        finally:
            sock.close()
    
    except Exception as e:
        return False, f"Error: {e}"


def run_scenario_3() -> tuple[bool, str]:
    """
    Scenario 3: Application-Layer Filtering
    
    This simulates content-based filtering at the application layer.
    The student should observe:
    - TCP connection succeeds
    - Some requests work, others are blocked
    - Filtering happens after connection establishment
    """
    print("\n" + "=" * 50)
    print("SCENARIO 3: Application-Layer Content Filter")
    print("=" * 50)
    print()
    print("Simulating: Proxy that blocks certain keywords")
    print()
    print("Instructions:")
    print("1. Start/continue Wireshark capture")
    print("2. Apply filter: tcp.port == 8888")
    print("3. Observe both allowed and blocked requests")
    print("4. Note: Connection succeeds but some content is filtered")
    print("5. Save capture as: pcap/hw_scenario_3.pcap")
    print()
    
    input("Press Enter when ready to begin capture...")
    
    results = []
    
    # Test 1: Allowed content
    print("\nTest 1: Sending allowed content...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(("localhost", 8888))
        sock.sendall(b"GET /normal HTTP/1.0\r\n\r\n")
        response = sock.recv(4096)
        sock.close()
        results.append(("Allowed content", True, response[:50].decode(errors="ignore")))
    except Exception as e:
        results.append(("Allowed content", False, str(e)))
    
    time.sleep(1)
    
    # Test 2: Blocked content
    print("Test 2: Sending blocked keyword...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(("localhost", 8888))
        sock.sendall(b"GET /malware HTTP/1.0\r\n\r\n")
        response = sock.recv(4096)
        sock.close()
        results.append(("Blocked content", response == b"", response[:50].decode(errors="ignore")))
    except Exception as e:
        results.append(("Blocked content", False, str(e)))
    
    # Summarise
    summary_parts = []
    for name, success, detail in results:
        summary_parts.append(f"{name}: {'Passed' if success else 'Check result'} - {detail}")
    
    return True, "\n  ".join(summary_parts)


def print_report_template():
    """Print the incident report template."""
    template = """
================================================================================
INCIDENT REPORT TEMPLATE
================================================================================

Copy this template and fill in your findings:

---

# Network Incident Report: Week 7 Homework

**Author:** [Your Name]
**Date:** [Date]
**Lab Session:** Computer Networks, Week 7

## Executive Summary

[2-3 sentences summarising the investigation and key findings]

## Methodology

### Tools Used
- Wireshark version: [version]
- Docker environment: [describe setup]

### Capture Procedure
[Describe how you captured traffic for each scenario]

## Findings

### Scenario 1: TCP Service Unreachable

**Observation:**
[What did you see in the PCAP?]

**Packet Evidence:**
- Packet #X: [description of relevant packet]
- Packet #Y: [description of response/lack of response]

**Diagnosis:**
[What type of filtering was applied? How do you know?]

### Scenario 2: UDP Service Unresponsive

**Observation:**
[What did you see in the PCAP?]

**Packet Evidence:**
- Packet #X: [description of outgoing UDP]
- Response: [describe what was or wasn't received]

**Diagnosis:**
[Distinguish between DROP and network failure]

### Scenario 3: Application-Layer Filtering

**Observation:**
[What did you see in the PCAP?]

**Packet Evidence:**
- Connection establishment: [describe TCP handshake]
- Allowed request: [describe flow]
- Blocked request: [describe what happened]

**Diagnosis:**
[How does application-layer filtering differ from network-layer?]

## Root Cause Analysis

[Summarise the root cause for each scenario]

## Recommendations

[What would you recommend to resolve these issues in a real environment?]

---
"""
    print(template)


def main():
    """Run homework scenarios."""
    parser = argparse.ArgumentParser(
        description="Week 7 Homework: Network Failure Analysis"
    )
    parser.add_argument(
        "--scenario", "-s",
        type=int,
        choices=[1, 2, 3],
        help="Run a specific scenario (1, 2, or 3)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all scenarios sequentially"
    )
    parser.add_argument(
        "--template",
        action="store_true",
        help="Print the incident report template"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("Homework 7.02: Network Failure Analysis")
    print("NETWORKING class - ASE, Informatics")
    print("=" * 60)

    if args.template:
        print_report_template()
        return 0

    if not args.scenario and not args.all:
        print()
        print("Usage:")
        print("  python hw_7_02.py --scenario 1   # Run scenario 1")
        print("  python hw_7_02.py --scenario 2   # Run scenario 2")
        print("  python hw_7_02.py --scenario 3   # Run scenario 3")
        print("  python hw_7_02.py --all          # Run all scenarios")
        print("  python hw_7_02.py --template     # Show report template")
        print()
        print("Before running scenarios:")
        print("1. Ensure lab is running: python scripts/start_lab.py")
        print("2. Start Wireshark on the Docker network interface")
        return 0

    scenarios = {
        1: run_scenario_1,
        2: run_scenario_2,
        3: run_scenario_3,
    }

    if args.all:
        for num in [1, 2, 3]:
            success, message = scenarios[num]()
            print(f"\nResult: {message}")
            print()
            if num < 3:
                input("Press Enter to continue to next scenario...")
    else:
        success, message = scenarios[args.scenario]()
        print(f"\nResult: {message}")

    print()
    print("=" * 60)
    print("Remember to:")
    print("1. Save your PCAP files to the pcap/ directory")
    print("2. Use --template to see the report format")
    print("3. Write your analysis in a separate document")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    exit(main())
