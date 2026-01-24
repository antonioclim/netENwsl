#!/usr/bin/env python3
"""
Week 10 - Homework Assignment 1: HTTPS Traffic Analysis
========================================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

This template helps you complete the HTTPS traffic analysis assignment.
It automates the process of starting servers and making requests.

Usage:
    python3 hw_10_01_https_analysis.py http    # Make HTTP requests
    python3 hw_10_01_https_analysis.py https   # Make HTTPS requests
    python3 hw_10_01_https_analysis.py both    # Both protocols

While this script runs, capture traffic in Wireshark.

TODO (Student):
1. Run this script while capturing in Wireshark
2. Save captures as wireshark_http.pcapng and wireshark_https.pcapng
3. Complete the analysis in analysis.md
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any

try:
    import requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except ImportError:
    print("[ERROR] requests library required: pip install requests")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
HTTP_URL = "http://localhost:8000/"
HTTPS_URL = "https://127.0.0.1:8443/"

# Number of requests to make for visibility in Wireshark
NUM_REQUESTS = 5


# ═══════════════════════════════════════════════════════════════════════════════
# HTTP_REQUESTS
# ═══════════════════════════════════════════════════════════════════════════════
def make_http_requests() -> None:
    """
    Make HTTP requests for Wireshark capture.
    
    💭 PREDICTION: What HTTP methods will be visible in the capture?
    💭 PREDICTION: Can you read the request/response body in Wireshark?
    """
    print(f"\n[INFO] Making {NUM_REQUESTS} HTTP requests to {HTTP_URL}")
    print("[INFO] Start Wireshark capture NOW on loopback interface")
    print("[INFO] Filter: tcp.port == 8000")
    
    time.sleep(3)  # Give time to start capture
    
    for i in range(NUM_REQUESTS):
        try:
            r = requests.get(HTTP_URL, timeout=5)
            print(f"  [{i+1}] GET {HTTP_URL} → {r.status_code}")
        except requests.RequestException as e:
            print(f"  [{i+1}] ERROR: {e}")
        time.sleep(0.5)
    
    print("\n[INFO] HTTP requests complete. Stop Wireshark capture.")
    print("[INFO] Save as: wireshark_http.pcapng")


# ═══════════════════════════════════════════════════════════════════════════════
# HTTPS_REQUESTS
# ═══════════════════════════════════════════════════════════════════════════════
def make_https_requests() -> None:
    """
    Make HTTPS requests for Wireshark capture.
    
    💭 PREDICTION: Will you be able to read the HTTP method in the capture?
    💭 PREDICTION: What TLS handshake messages will you see?
    
    TODO (Student): Fill in your predictions before running
    - TLS handshake messages expected: _____________________
    - Application data visibility: _________________________
    """
    print(f"\n[INFO] Making {NUM_REQUESTS} HTTPS requests to {HTTPS_URL}")
    print("[INFO] Start Wireshark capture NOW on loopback interface")
    print("[INFO] Filter: tcp.port == 8443")
    
    time.sleep(3)  # Give time to start capture
    
    for i in range(NUM_REQUESTS):
        try:
            # verify=False because we use self-signed certificate
            r = requests.get(HTTPS_URL, timeout=5, verify=False)
            print(f"  [{i+1}] GET {HTTPS_URL} → {r.status_code}")
        except requests.RequestException as e:
            print(f"  [{i+1}] ERROR: {e}")
        time.sleep(0.5)
    
    print("\n[INFO] HTTPS requests complete. Stop Wireshark capture.")
    print("[INFO] Save as: wireshark_https.pcapng")


# ═══════════════════════════════════════════════════════════════════════════════
# ANALYSIS_TEMPLATE
# ═══════════════════════════════════════════════════════════════════════════════
ANALYSIS_TEMPLATE = """# HTTPS Traffic Analysis — Week 10 Homework

## Student: [YOUR NAME HERE]
## Date: [DATE]

---

## 1. HTTP Capture Analysis

### Request Details Observed
- HTTP Method: [e.g., GET]
- URL Path: [e.g., /]
- Headers visible: [list headers you could read]

### Response Details Observed
- Status Code: [e.g., 200 OK]
- Content-Type: [e.g., text/html]
- Body visible: [yes/no, describe what you saw]

---

## 2. HTTPS Capture Analysis

### TLS Handshake Messages Observed
1. [Message 1, e.g., Client Hello]
2. [Message 2]
3. [Message 3]
4. [continue...]

### SNI (Server Name Indication)
- Domain visible in SNI: [yes/no, what domain]
- Why is SNI visible? [your explanation]

### Application Data
- Could you read HTTP method? [yes/no]
- Could you read response body? [yes/no]
- What did you see instead? [encrypted data description]

---

## 3. Comparison Table

| Aspect | HTTP | HTTPS |
|--------|------|-------|
| Request method visible | [yes/no] | [yes/no] |
| URL path visible | [yes/no] | [yes/no] |
| Headers visible | [yes/no] | [yes/no] |
| Body visible | [yes/no] | [yes/no] |
| Domain visible | [yes/no] | [yes/no] |

---

## 4. Conclusions

[Write 100-200 words about what you learned from this analysis.
Include: why HTTPS is important, what it protects, what it doesn't protect.]

---

*Word count: [XXX]*
"""


def generate_analysis_template() -> None:
    """Generate the analysis.md template file."""
    output_path = Path("analysis.md")
    if output_path.exists():
        print(f"[WARNING] {output_path} already exists, not overwriting")
        return
    
    output_path.write_text(ANALYSIS_TEMPLATE)
    print(f"[INFO] Created template: {output_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    parser = argparse.ArgumentParser(description="Week 10 HTTPS Analysis Helper")
    parser.add_argument(
        "mode",
        choices=["http", "https", "both", "template"],
        help="Which requests to make, or 'template' to generate analysis.md"
    )
    args = parser.parse_args()
    
    if args.mode == "template":
        generate_analysis_template()
        return 0
    
    print("=" * 60)
    print("Week 10 Homework — HTTPS Traffic Analysis")
    print("=" * 60)
    print("\n[INFO] Make sure the appropriate server is running:")
    print("  - HTTP:  Lab web container on port 8000")
    print("  - HTTPS: Exercise 1 server on port 8443")
    
    if args.mode in ("http", "both"):
        make_http_requests()
    
    if args.mode in ("https", "both"):
        make_https_requests()
    
    print("\n" + "=" * 60)
    print("Next steps:")
    print("1. Open your Wireshark captures")
    print("2. Run: python3 hw_10_01_https_analysis.py template")
    print("3. Fill in analysis.md with your observations")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
