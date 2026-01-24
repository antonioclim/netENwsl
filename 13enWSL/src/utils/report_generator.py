#!/usr/bin/env python3
"""
Week 13 — Report Generator
==========================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

This utility reads artefacts produced by the laboratory kit and generates
a Markdown summary report suitable for submission or review.

Inputs (best effort — missing files are handled gracefully):
- artifacts/scan_results.json
- artifacts/vuln_*.json
- artifacts/validation.txt

Output:
- artifacts/report.md

USAGE:
    python3 src/utils/report_generator.py
    python3 src/utils/report_generator.py --output custom_report.md
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT_DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

ARTIFACTS_DIR = Path(__file__).resolve().parents[2] / "artifacts"
SCAN_JSON = ARTIFACTS_DIR / "scan_results.json"
VALIDATION_TXT = ARTIFACTS_DIR / "validation.txt"
DEFAULT_REPORT = ARTIFACTS_DIR / "report.md"


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ScanSummary:
    """Summary of a port scan result."""
    target: str
    total_scanned: int
    open_count: int
    closed_count: int
    filtered_count: int
    open_ports: List[Dict[str, Any]]


@dataclass
class VulnSummary:
    """Summary of a vulnerability scan."""
    target: str
    service: str
    port: int
    findings_high: int
    findings_medium: int
    findings_low: int
    findings_info: int


# ═══════════════════════════════════════════════════════════════════════════════
# FILE_LOADING
# ═══════════════════════════════════════════════════════════════════════════════

def load_scan_results() -> Optional[Dict[str, Any]]:
    """
    Load port scan results from JSON file.
    
    Returns:
        Parsed JSON data or None if file doesn't exist or is empty
    """
    if not SCAN_JSON.exists():
        return None
    
    try:
        content = SCAN_JSON.read_text(encoding="utf-8")
        if not content.strip():
            return None
        data = json.loads(content)
        return data.get("scan_report", data)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not load {SCAN_JSON}: {e}", file=sys.stderr)
        return None


def load_validation_results() -> List[str]:
    """
    Load validation results from text file.
    
    Returns:
        List of validation result lines, empty if file doesn't exist
    """
    if not VALIDATION_TXT.exists():
        return []
    
    try:
        content = VALIDATION_TXT.read_text(encoding="utf-8")
        return [line.strip() for line in content.splitlines() if line.strip()]
    except IOError as e:
        print(f"Warning: Could not load {VALIDATION_TXT}: {e}", file=sys.stderr)
        return []


def load_vuln_reports() -> List[Dict[str, Any]]:
    """
    Load all vulnerability reports from artifacts directory.
    
    Returns:
        List of parsed vulnerability report dictionaries
    """
    reports = []
    
    for json_file in ARTIFACTS_DIR.glob("vuln_*.json"):
        try:
            content = json_file.read_text(encoding="utf-8")
            data = json.loads(content)
            reports.append(data.get("vulnerability_report", data))
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load {json_file}: {e}", file=sys.stderr)
    
    return reports


# ═══════════════════════════════════════════════════════════════════════════════
# REPORT_FORMATTING
# ═══════════════════════════════════════════════════════════════════════════════

def format_scan_section(scan_data: Optional[Dict[str, Any]]) -> List[str]:
    """
    Format port scan results into Markdown lines.
    
    Args:
        scan_data: Parsed scan results or None
    
    Returns:
        List of Markdown-formatted lines
    """
    lines = ["## Port Scan Results", ""]
    
    if not scan_data:
        lines.append("_No scan results found in artifacts/scan_results.json_")
        return lines
    
    hosts = scan_data.get("hosts", [])
    if not hosts:
        lines.append("_Scan completed but no hosts in results._")
        return lines
    
    for host in hosts:
        target = host.get("target", host.get("ip", "unknown"))
        stats = host.get("statistics", {})
        open_ports = host.get("open_ports", [])
        
        lines.append(f"### Target: {target}")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Total scanned | {stats.get('total_scanned', 'N/A')} |")
        lines.append(f"| Open | {stats.get('open', len(open_ports))} |")
        lines.append(f"| Closed | {stats.get('closed', 'N/A')} |")
        lines.append(f"| Filtered | {stats.get('filtered', 'N/A')} |")
        lines.append("")
        
        if open_ports:
            lines.append("**Open Ports:**")
            lines.append("")
            lines.append("| Port | Service | Banner |")
            lines.append("|------|---------|--------|")
            for port_info in open_ports:
                port = port_info.get("port", "?")
                service = port_info.get("service", "unknown")
                banner = port_info.get("banner", "-")
                if banner and len(banner) > 40:
                    banner = banner[:37] + "..."
                lines.append(f"| {port} | {service} | {banner or '-'} |")
            lines.append("")
    
    return lines


def format_vuln_section(vuln_reports: List[Dict[str, Any]]) -> List[str]:
    """
    Format vulnerability reports into Markdown lines.
    
    Args:
        vuln_reports: List of vulnerability report dictionaries
    
    Returns:
        List of Markdown-formatted lines
    """
    lines = ["## Vulnerability Assessment", ""]
    
    if not vuln_reports:
        lines.append("_No vulnerability reports found (vuln_*.json)_")
        return lines
    
    for report in vuln_reports:
        target = report.get("target", "unknown")
        service = report.get("service", "unknown")
        port = report.get("port", "?")
        findings = report.get("findings", [])
        summary = report.get("summary", {})
        
        lines.append(f"### {service.upper()} ({target}:{port})")
        lines.append("")
        
        if summary:
            lines.append(f"**Summary:** High: {summary.get('high', 0)} | "
                        f"Medium: {summary.get('medium', 0)} | "
                        f"Low: {summary.get('low', 0)} | "
                        f"Info: {summary.get('info', 0)}")
            lines.append("")
        
        if findings:
            for finding in findings:
                severity = finding.get("severity", "info").upper()
                title = finding.get("title", "Untitled finding")
                evidence = finding.get("evidence", "")
                
                lines.append(f"- **[{severity}]** {title}")
                if evidence:
                    lines.append(f"  - Evidence: `{evidence[:60]}{'...' if len(evidence) > 60 else ''}`")
            lines.append("")
    
    return lines


def format_validation_section(validation: List[str]) -> List[str]:
    """
    Format validation results into Markdown lines.
    
    Args:
        validation: List of validation result strings
    
    Returns:
        List of Markdown-formatted lines
    """
    lines = ["## Environment Validation", ""]
    
    if not validation:
        lines.append("_No validation results found._")
        return lines
    
    for item in validation:
        lines.append(f"- {item}")
    lines.append("")
    
    return lines


# ═══════════════════════════════════════════════════════════════════════════════
# REPORT_GENERATION
# ═══════════════════════════════════════════════════════════════════════════════

def generate_report(output_path: Path) -> int:
    """
    Generate the complete Markdown report.
    
    Args:
        output_path: Path where report will be written
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    # Ensure artifacts directory exists
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load all data sources
    scan_data = load_scan_results()
    validation = load_validation_results()
    vuln_reports = load_vuln_reports()
    
    # Build report
    md_lines: List[str] = []
    
    # Header
    md_lines.append("# Week 13 Laboratory Report")
    md_lines.append("")
    md_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    
    # Sections
    md_lines.extend(format_validation_section(validation))
    md_lines.extend(format_scan_section(scan_data))
    md_lines.extend(format_vuln_section(vuln_reports))
    
    # Footer
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("*Report generated by Week 13 Laboratory Kit*")
    md_lines.append("")
    md_lines.append("*Computer Networks — ASE, CSIE*")
    
    # Write report
    try:
        output_path.write_text("\n".join(md_lines), encoding="utf-8")
        print(f"Report written to: {output_path}")
        return 0
    except IOError as e:
        print(f"Error writing report: {e}", file=sys.stderr)
        return 1


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Generate Week 13 laboratory report from artifacts"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=DEFAULT_REPORT,
        help=f"Output file path (default: {DEFAULT_REPORT})"
    )
    
    args = parser.parse_args()
    return generate_report(args.output)


if __name__ == "__main__":
    sys.exit(main())
