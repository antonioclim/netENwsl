#!/usr/bin/env python3
"""
Homework Exercise 7.02: Network Failure Analysis Report
=======================================================
Computer Networks - Week 7 (WSL Environment)
ASE Bucharest, CSIE | by ing. dr. Antonio Clim

Objective:
Develop systematic diagnostic skills by analysing packet captures to determine
the root cause of simulated network failures.

Scenario:
You are a network administrator. Users are reporting that certain services are
unreachable. Your task is to capture traffic, analyse the results and produce
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

Level: Intermediate
Estimated time: 90-120 minutes

Pair Programming Notes:
- Driver: Execute scenarios and capture traffic
- Navigator: Guide Wireshark filter application, document observations
- Swap after: Each scenario completion
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import socket
import sys
import time
from pathlib import Path
from typing import Tuple, List

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# ═══════════════════════════════════════════════════════════════════════════════
# PREDICTION_PROMPTS
# ═══════════════════════════════════════════════════════════════════════════════
def prompt_prediction_scenario_1() -> str:
    """
    Prediction prompt for TCP REJECT scenario.
    
    Implements Brown & Wilson Principle 4: Predictions.
    Students learn more effectively when they commit to a prediction
    before seeing the result.
    """
    print()
    print("💭 PREDICTION: Before running Scenario 1, answer these questions:")
    print("   1. When a firewall REJECTs a TCP connection, what packet will the client receive?")
    print("      (a) Nothing  (b) TCP RST  (c) ICMP unreachable  (d) TCP FIN")
    print("   2. How long will the client wait before reporting failure?")
    print("      (a) Instantly  (b) 3 seconds  (c) Until timeout  (d) Forever")
    print("   3. What Wireshark filter will show the relevant packets?")
    print()
    prediction = input("   Write your answers (e.g., 'b, a, tcp.port==9090'): ")
    print()
    return prediction


def prompt_prediction_scenario_2() -> str:
    """
    Prediction prompt for UDP DROP scenario.
    
    Implements Brown & Wilson Principle 4: Predictions.
    """
    print()
    print("💭 PREDICTION: Before running Scenario 2, answer these questions:")
    print("   1. When a firewall DROPs a UDP packet, what will the sender observe?")
    print("      (a) Error message  (b) Nothing - appears successful  (c) ICMP response")
    print("   2. How can you distinguish DROP from actual packet loss?")
    print("      (a) You can't  (b) Check sender logs  (c) Multiple consistent tests")
    print("   3. In Wireshark, how many packets will you see for the UDP send?")
    print("      (a) 0  (b) 1 (outgoing only)  (c) 2 (request + response)")
    print()
    prediction = input("   Write your answers (e.g., 'b, c, b'): ")
    print()
    return prediction


def prompt_prediction_scenario_3() -> str:
    """
    Prediction prompt for application-layer filtering scenario.
    
    Implements Brown & Wilson Principle 4: Predictions.
    """
    print()
    print("💭 PREDICTION: Before running Scenario 3, answer these questions:")
    print("   1. Will the TCP handshake succeed for blocked content?")
    print("      (a) Yes - filtering happens after connection  (b) No - connection refused")
    print("   2. At which OSI layer does this filtering occur?")
    print("      (a) Layer 3 (Network)  (b) Layer 4 (Transport)  (c) Layer 7 (Application)")
    print("   3. What evidence in the PCAP shows application-layer filtering?")
    print("      (a) No SYN-ACK  (b) TCP RST after handshake  (c) Connection succeeds, content blocked")
    print()
    prediction = input("   Write your answers (e.g., 'a, c, c'): ")
    print()
    return prediction


def verify_prediction(scenario: int, prediction: str) -> None:
    """
    Display the correct answers after scenario completion.
    
    Args:
        scenario: Scenario number (1, 2, or 3)
        prediction: Student's prediction string
    """
    answers = {
        1: ("b or c (TCP RST or ICMP)", "a (instantly)", "tcp.port == 9090"),
        2: ("b (appears successful)", "c (multiple tests)", "b (1 outgoing packet)"),
        3: ("a (yes, filtering after connection)", "c (Layer 7)", "c (connection succeeds)"),
    }
    
    print()
    print("📝 CORRECT ANSWERS:")
    print(f"   1. {answers[scenario][0]}")
    print(f"   2. {answers[scenario][1]}")
    print(f"   3. {answers[scenario][2]}")
    print()
    print(f"   Your prediction was: {prediction}")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# SCENARIO_1_TCP_REJECT
# ═══════════════════════════════════════════════════════════════════════════════
def run_scenario_1(skip_prediction: bool = False) -> Tuple[bool, str]:
    """
    Scenario 1: TCP REJECT
    
    This simulates a firewall rule that REJECTs TCP connections.
    The student should observe:
    - TCP SYN sent
    - TCP RST received (or ICMP port unreachable)
    - Connection immediately fails
    
    Args:
        skip_prediction: If True, skip the prediction prompt
        
    Returns:
        Tuple of (success, message)
    """
    # ═══════════════════════════════════════════════════════════════════════════
    # DISPLAY_SCENARIO_HEADER
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 60)
    print("SCENARIO 1: TCP Service Unreachable (REJECT Behaviour)")
    print("=" * 60)
    print()
    print("Simulating: Firewall REJECT rule on TCP port 9090")
    print()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # COLLECT_PREDICTION
    # ═══════════════════════════════════════════════════════════════════════════
    prediction = ""
    if not skip_prediction:
        prediction = prompt_prediction_scenario_1()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # DISPLAY_INSTRUCTIONS
    # ═══════════════════════════════════════════════════════════════════════════
    print("Instructions:")
    print("1. Start Wireshark capture on the Docker network interface")
    print("2. Apply filter: tcp.port == 9090")
    print("3. Observe the connection attempt below")
    print("4. Save capture as: pcap/hw_scenario_1.pcap")
    print()
    
    input("Press Enter when Wireshark is ready...")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # EXECUTE_TCP_CONNECTION_TEST
    # ═══════════════════════════════════════════════════════════════════════════
    print("\nAttempting TCP connection to localhost:9090...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex(("localhost", 9090))
        sock.close()
        
        if result == 0:
            outcome = (True, "Connection succeeded (no filter active or service running)")
        else:
            outcome = (False, f"Connection failed with errno {result}")
    
    except ConnectionRefusedError:
        outcome = (False, "Connection refused (RST received - REJECT behaviour)")
    except socket.timeout:
        outcome = (False, "Connection timed out (possible DROP instead of REJECT)")
    except Exception as e:
        outcome = (False, f"Error: {e}")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # VERIFY_PREDICTION
    # ═══════════════════════════════════════════════════════════════════════════
    if not skip_prediction and prediction:
        verify_prediction(1, prediction)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ANALYSIS_PROMPTS
    # ═══════════════════════════════════════════════════════════════════════════
    print("📋 ANALYSIS CHECKLIST:")
    print("   □ Did you see a TCP SYN packet in Wireshark?")
    print("   □ What was the response? (RST, ICMP, or nothing?)")
    print("   □ How long did the client wait before reporting failure?")
    print("   □ Note the packet numbers for your report")
    print()
    
    return outcome


# ═══════════════════════════════════════════════════════════════════════════════
# SCENARIO_2_UDP_DROP
# ═══════════════════════════════════════════════════════════════════════════════
def run_scenario_2(skip_prediction: bool = False) -> Tuple[bool, str]:
    """
    Scenario 2: UDP DROP
    
    This simulates a firewall rule that silently DROPs UDP packets.
    The student should observe:
    - UDP datagram sent
    - No response received
    - Sender cannot distinguish between DROP and packet loss
    
    Args:
        skip_prediction: If True, skip the prediction prompt
        
    Returns:
        Tuple of (success, message)
    """
    # ═══════════════════════════════════════════════════════════════════════════
    # DISPLAY_SCENARIO_HEADER
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 60)
    print("SCENARIO 2: UDP Service Unresponsive (DROP Behaviour)")
    print("=" * 60)
    print()
    print("Simulating: Firewall DROP rule on UDP port 9091")
    print()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # COLLECT_PREDICTION
    # ═══════════════════════════════════════════════════════════════════════════
    prediction = ""
    if not skip_prediction:
        prediction = prompt_prediction_scenario_2()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # DISPLAY_INSTRUCTIONS
    # ═══════════════════════════════════════════════════════════════════════════
    print("Instructions:")
    print("1. Start/continue Wireshark capture")
    print("2. Apply filter: udp.port == 9091")
    print("3. Observe the datagram below")
    print("4. Note: You should see outgoing UDP but NO response")
    print("5. Save capture as: pcap/hw_scenario_2.pcap")
    print()
    
    input("Press Enter when Wireshark is ready...")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # EXECUTE_UDP_SEND_TEST
    # ═══════════════════════════════════════════════════════════════════════════
    print("\nSending UDP datagram to localhost:9091...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(3)
        
        msg = b"test_homework_scenario_2"
        sock.sendto(msg, ("localhost", 9091))
        
        print("Datagram sent. Waiting for response (will likely timeout)...")
        
        try:
            response, addr = sock.recvfrom(1024)
            outcome = (True, f"Received response: {response}")
        except socket.timeout:
            outcome = (False, "No response received (consistent with DROP behaviour)")
        finally:
            sock.close()
    
    except Exception as e:
        outcome = (False, f"Error: {e}")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # VERIFY_PREDICTION
    # ═══════════════════════════════════════════════════════════════════════════
    if not skip_prediction and prediction:
        verify_prediction(2, prediction)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ANALYSIS_PROMPTS
    # ═══════════════════════════════════════════════════════════════════════════
    print("📋 ANALYSIS CHECKLIST:")
    print("   □ Did you see the outgoing UDP packet in Wireshark?")
    print("   □ Was there any response packet?")
    print("   □ How does this differ from TCP REJECT behaviour?")
    print("   □ Could you distinguish DROP from network packet loss?")
    print()
    
    return outcome


# ═══════════════════════════════════════════════════════════════════════════════
# SCENARIO_3_APPLICATION_LAYER_FILTER
# ═══════════════════════════════════════════════════════════════════════════════
def run_scenario_3(skip_prediction: bool = False) -> Tuple[bool, str]:
    """
    Scenario 3: Application-Layer Filtering
    
    This simulates content-based filtering at the application layer.
    The student should observe:
    - TCP connection succeeds
    - Some requests work, others are blocked
    - Filtering happens after connection establishment
    
    Args:
        skip_prediction: If True, skip the prediction prompt
        
    Returns:
        Tuple of (success, message)
    """
    # ═══════════════════════════════════════════════════════════════════════════
    # DISPLAY_SCENARIO_HEADER
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 60)
    print("SCENARIO 3: Application-Layer Content Filter")
    print("=" * 60)
    print()
    print("Simulating: Proxy that blocks certain keywords")
    print()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # COLLECT_PREDICTION
    # ═══════════════════════════════════════════════════════════════════════════
    prediction = ""
    if not skip_prediction:
        prediction = prompt_prediction_scenario_3()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # DISPLAY_INSTRUCTIONS
    # ═══════════════════════════════════════════════════════════════════════════
    print("Instructions:")
    print("1. Start/continue Wireshark capture")
    print("2. Apply filter: tcp.port == 8888")
    print("3. Observe both allowed and blocked requests")
    print("4. Note: Connection succeeds but some content is filtered")
    print("5. Save capture as: pcap/hw_scenario_3.pcap")
    print()
    
    input("Press Enter when Wireshark is ready...")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # EXECUTE_ALLOWED_CONTENT_TEST
    # ═══════════════════════════════════════════════════════════════════════════
    results: List[Tuple[str, bool, str]] = []
    
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
    
    # ═══════════════════════════════════════════════════════════════════════════
    # EXECUTE_BLOCKED_CONTENT_TEST
    # ═══════════════════════════════════════════════════════════════════════════
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
    
    # ═══════════════════════════════════════════════════════════════════════════
    # VERIFY_PREDICTION
    # ═══════════════════════════════════════════════════════════════════════════
    if not skip_prediction and prediction:
        verify_prediction(3, prediction)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ANALYSIS_PROMPTS
    # ═══════════════════════════════════════════════════════════════════════════
    print("📋 ANALYSIS CHECKLIST:")
    print("   □ Did the TCP handshake complete for both requests?")
    print("   □ At what point did the filtering occur?")
    print("   □ How does this differ from network-layer filtering?")
    print("   □ What are the security implications of each approach?")
    print()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # FORMAT_RESULTS
    # ═══════════════════════════════════════════════════════════════════════════
    summary_parts = []
    for name, success, detail in results:
        summary_parts.append(f"{name}: {'Passed' if success else 'Check result'} - {detail}")
    
    return True, "\n  ".join(summary_parts)


# ═══════════════════════════════════════════════════════════════════════════════
# REPORT_TEMPLATE
# ═══════════════════════════════════════════════════════════════════════════════
def print_report_template() -> None:
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


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """
    Run homework scenarios.
    
    Returns:
        Exit code (0 = success)
    """
    # ═══════════════════════════════════════════════════════════════════════════
    # PARSE_ARGUMENTS
    # ═══════════════════════════════════════════════════════════════════════════
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
    parser.add_argument(
        "--skip-predictions",
        action="store_true",
        help="Skip prediction prompts (for quick testing)"
    )
    args = parser.parse_args()

    # ═══════════════════════════════════════════════════════════════════════════
    # DISPLAY_HEADER
    # ═══════════════════════════════════════════════════════════════════════════
    print("=" * 60)
    print("Homework 7.02: Network Failure Analysis")
    print("Computer Networks - Week 7 | ASE Bucharest, CSIE")
    print("=" * 60)

    # ═══════════════════════════════════════════════════════════════════════════
    # HANDLE_TEMPLATE_REQUEST
    # ═══════════════════════════════════════════════════════════════════════════
    if args.template:
        print_report_template()
        return 0

    # ═══════════════════════════════════════════════════════════════════════════
    # DISPLAY_USAGE_IF_NO_ARGS
    # ═══════════════════════════════════════════════════════════════════════════
    if not args.scenario and not args.all:
        print()
        print("Usage:")
        print("  python hw_7_02_troubleshoot_scenarios.py --scenario 1   # Run scenario 1")
        print("  python hw_7_02_troubleshoot_scenarios.py --scenario 2   # Run scenario 2")
        print("  python hw_7_02_troubleshoot_scenarios.py --scenario 3   # Run scenario 3")
        print("  python hw_7_02_troubleshoot_scenarios.py --all          # Run all scenarios")
        print("  python hw_7_02_troubleshoot_scenarios.py --template     # Show report template")
        print()
        print("Before running scenarios:")
        print("1. Ensure lab is running: python scripts/start_lab.py")
        print("2. Start Wireshark on the Docker network interface")
        return 0

    # ═══════════════════════════════════════════════════════════════════════════
    # RUN_SELECTED_SCENARIOS
    # ═══════════════════════════════════════════════════════════════════════════
    scenarios = {
        1: run_scenario_1,
        2: run_scenario_2,
        3: run_scenario_3,
    }

    if args.all:
        for num in [1, 2, 3]:
            success, message = scenarios[num](skip_prediction=args.skip_predictions)
            print(f"\nResult: {message}")
            print()
            if num < 3:
                input("Press Enter to continue to next scenario...")
    else:
        success, message = scenarios[args.scenario](skip_prediction=args.skip_predictions)
        print(f"\nResult: {message}")

    # ═══════════════════════════════════════════════════════════════════════════
    # DISPLAY_CLOSING_REMINDERS
    # ═══════════════════════════════════════════════════════════════════════════
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
