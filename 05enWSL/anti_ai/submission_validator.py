#!/usr/bin/env python3
"""
Week 5 submission validator (anti-AI).

This validator is designed for automated marking pipelines and for local
pre-submission checks by students.

It verifies:
- the challenge integrity and validity window
- evidence.json structure and file hashes
- subnet plan JSON validity against the VLSM challenge
- IPv6 report JSON validity against the IPv6 challenge

Usage
-----
    python -m anti_ai.submission_validator \
        --challenge artifacts/anti_ai/challenge_ABC123.yaml \
        --evidence evidence_ABC123.json \
        --base-dir . \
        --verbose
"""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

from anti_ai.challenge import Week5Challenge, load_challenge, parse_utc_iso


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _format_errors(errors: List[str]) -> str:
    return "\n".join(f"- {e}" for e in errors)


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Validate a Week 5 anti-AI submission.")
    p.add_argument("--challenge", type=Path, required=True, help="Path to the challenge YAML")
    p.add_argument("--evidence", type=Path, required=True, help="Path to evidence.json")
    p.add_argument("--base-dir", type=Path, default=Path("."), help="Base directory for resolving artefact paths")
    p.add_argument("--ignore-expiry", action="store_true", help="Ignore challenge validity window (for debugging)")
    p.add_argument("--verbose", action="store_true", help="Print detailed validation output")
    return p


def _load_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}: {e}") from e


def _validate_time_window(challenge: Week5Challenge, *, ignore_expiry: bool) -> List[str]:
    errors: List[str] = []
    try:
        issued = parse_utc_iso(challenge.issued_at_utc)
    except ValueError as e:
        return [f"Challenge issued_at_utc is invalid: {e}"]

    if ignore_expiry:
        return errors

    age = _now_utc() - issued
    if age.total_seconds() < 0:
        errors.append("Challenge issued_at_utc is in the future")
        return errors

    max_age = challenge.valid_for_hours * 3600
    if age.total_seconds() > max_age:
        errors.append(
            f"Challenge expired: age is {int(age.total_seconds()//3600)} hours but valid_for_hours is {challenge.valid_for_hours}"
        )
    return errors


def _validate_evidence(evidence_path: Path, base_dir: Path, challenge: Week5Challenge) -> Tuple[List[Dict[str, str]], List[str]]:
    errors: List[str] = []
    evidence = _load_json(evidence_path)

    meta = evidence.get("meta", {})
    if meta.get("week") != challenge.week:
        errors.append("Evidence meta.week does not match the challenge week")
    if str(meta.get("student_id", "")) != challenge.student_id:
        errors.append("Evidence meta.student_id does not match the challenge student_id")
    if str(meta.get("challenge_sha256", "")) != challenge.compute_integrity():
        errors.append("Evidence meta.challenge_sha256 does not match the challenge integrity hash")

    artefacts = evidence.get("artefacts")
    if not isinstance(artefacts, list) or not artefacts:
        errors.append("Evidence artefacts list is missing or empty")
        return [], errors

    validated: List[Dict[str, str]] = []
    for a in artefacts:
        if not isinstance(a, dict):
            errors.append("Evidence artefacts entry is not an object")
            continue
        rel_path = a.get("path")
        expected_hash = a.get("sha256")
        if not rel_path or not expected_hash:
            errors.append("Evidence artefacts entry must contain path and sha256")
            continue

        abs_path = (base_dir / rel_path).resolve()
        if not abs_path.exists():
            errors.append(f"Missing artefact file: {rel_path}")
            continue
        actual_hash = sha256_file(abs_path)
        if actual_hash != expected_hash:
            errors.append(f"Hash mismatch for {rel_path}")
            continue
        validated.append({"path": rel_path, "sha256": actual_hash})

    return validated, errors


def _expected_usable_hosts(network: ipaddress.IPv4Network) -> int:
    # For teaching purposes we assume classic subnet semantics.
    if network.prefixlen >= 31:
        return 0
    return network.num_addresses - 2


def _validate_subnet_plan(plan_path: Path, challenge: Week5Challenge) -> List[str]:
    errors: List[str] = []
    plan = _load_json(plan_path)

    # Token checks
    meta = plan.get("meta", {}) if isinstance(plan.get("meta"), dict) else {}
    token = meta.get("subnet_plan_token") or plan.get("subnet_plan_token")
    if token != challenge.tokens.get("subnet_plan_token"):
        errors.append("Subnet plan token does not match the challenge token")

    org_block = plan.get("organisation_block")
    expected_block = challenge.vlsm_task.get("organisation_block")
    if org_block != expected_block:
        errors.append("Subnet plan organisation_block does not match the challenge organisation_block")

    allocations = plan.get("allocations")
    if not isinstance(allocations, list) or not allocations:
        errors.append("Subnet plan allocations list is missing or empty")
        return errors

    # Department requirements
    dept_specs = {
        d["name"]: int(d["required_hosts"])
        for d in challenge.vlsm_task.get("departments", [])
        if isinstance(d, dict) and "name" in d and "required_hosts" in d
    }
    if not dept_specs:
        errors.append("Challenge does not contain department specifications")
        return errors

    seen_departments: set[str] = set()
    networks: List[ipaddress.IPv4Network] = []

    parent = ipaddress.IPv4Network(expected_block, strict=True)

    for entry in allocations:
        if not isinstance(entry, dict):
            errors.append("Subnet plan allocations contains a non-object entry")
            continue

        dept = entry.get("department")
        if not dept or not isinstance(dept, str):
            errors.append("Subnet allocation is missing department name")
            continue

        if dept not in dept_specs:
            errors.append(f"Unknown department in allocations: {dept}")
            continue

        if dept in seen_departments:
            errors.append(f"Duplicate allocation for department: {dept}")
            continue
        seen_departments.add(dept)

        try:
            prefix = int(entry.get("prefix_length"))
            net_addr = str(entry.get("network_address"))
            net = ipaddress.IPv4Network(f"{net_addr}/{prefix}", strict=True)
        except Exception:
            errors.append(f"Invalid network/prefix for department {dept}")
            continue

        if not net.subnet_of(parent):
            errors.append(f"Allocation for {dept} is outside the organisation block")
            continue

        # Basic field consistency
        if str(net.broadcast_address) != str(entry.get("broadcast_address")):
            errors.append(f"Broadcast address mismatch for {dept}")
        if str(net.netmask) != str(entry.get("subnet_mask")):
            errors.append(f"Subnet mask mismatch for {dept}")

        expected_hosts = _expected_usable_hosts(net)
        if int(entry.get("usable_hosts", -1)) != expected_hosts:
            errors.append(f"Usable host count mismatch for {dept}")

        if expected_hosts > 0:
            if str(ipaddress.IPv4Address(int(net.network_address) + 1)) != str(entry.get("first_usable")):
                errors.append(f"First usable address mismatch for {dept}")
            if str(ipaddress.IPv4Address(int(net.broadcast_address) - 1)) != str(entry.get("last_usable")):
                errors.append(f"Last usable address mismatch for {dept}")

        # Requirement satisfaction
        required = dept_specs[dept]
        if expected_hosts < required:
            errors.append(f"Allocated subnet for {dept} does not satisfy required_hosts ({required})")

        # Utilisation
        if expected_hosts > 0:
            expected_util = round((required / expected_hosts) * 100, 1)
            reported = entry.get("utilisation_percent")
            try:
                if float(reported) != expected_util:
                    errors.append(f"Utilisation percent mismatch for {dept}")
            except Exception:
                errors.append(f"Utilisation percent is invalid for {dept}")

        networks.append(net)

    # Coverage check
    missing = sorted(set(dept_specs.keys()) - seen_departments)
    if missing:
        errors.append(f"Missing allocations for departments: {', '.join(missing)}")

    # Overlap check
    for i in range(len(networks)):
        for j in range(i + 1, len(networks)):
            if networks[i].overlaps(networks[j]):
                errors.append("Subnet allocations overlap")
                break

    return errors


def _classify_ipv6(addr: ipaddress.IPv6Address) -> str:
    global_unicast = ipaddress.IPv6Network("2000::/3")
    unique_local = ipaddress.IPv6Network("fc00::/7")

    if addr.is_unspecified:
        return "Unspecified"
    if addr.ipv4_mapped is not None:
        return "IPv4-mapped"
    if addr.is_loopback:
        return "Loopback"
    if addr.is_link_local:
        return "Link-local"
    if addr.is_multicast:
        return "Multicast"
    if addr in unique_local:
        return "Unique Local (ULA)"
    if addr in global_unicast:
        return "Global Unicast"
    return "Other"


def _eui64_from_mac(mac: str) -> str:
    mac_clean = mac.replace(":", "").replace("-", "").lower()
    if len(mac_clean) != 12:
        raise ValueError("Invalid MAC address format")
    first_half = mac_clean[:6]
    second_half = mac_clean[6:]
    eui64 = first_half + "fffe" + second_half
    first_byte = int(eui64[:2], 16) ^ 0x02  # flip U/L bit
    eui64 = f"{first_byte:02x}" + eui64[2:]
    return f"{eui64[0:4]}:{eui64[4:8]}:{eui64[8:12]}:{eui64[12:16]}"


def _validate_ipv6_report(report_path: Path, challenge: Week5Challenge) -> List[str]:
    errors: List[str] = []
    report = _load_json(report_path)

    meta = report.get("meta", {}) if isinstance(report.get("meta"), dict) else {}
    token = meta.get("ipv6_report_token") or report.get("ipv6_report_token")
    if token != challenge.tokens.get("ipv6_report_token"):
        errors.append("IPv6 report token does not match the challenge token")

    sample_addrs = challenge.ipv6_task.get("sample_addresses")
    if not isinstance(sample_addrs, list) or not sample_addrs:
        errors.append("Challenge does not contain sample_addresses")
        return errors

    analysis = report.get("analysis")
    if not isinstance(analysis, list) or not analysis:
        errors.append("IPv6 report analysis list is missing or empty")
        return errors

    by_addr: Dict[str, Dict[str, Any]] = {}
    for row in analysis:
        if isinstance(row, dict) and "address" in row:
            by_addr[str(row["address"])] = row

    for addr_str in sample_addrs:
        if addr_str not in by_addr:
            errors.append(f"Missing analysis for address: {addr_str}")
            continue
        row = by_addr[addr_str]
        try:
            addr = ipaddress.IPv6Address(addr_str.split("/")[0])
        except ValueError:
            errors.append(f"Challenge address is invalid: {addr_str}")
            continue

        expected_type = _classify_ipv6(addr)
        actual_type = str(row.get("address_type", ""))
        if actual_type != expected_type:
            errors.append(f"Address type mismatch for {addr_str}")

        expected_comp = str(addr)
        expected_full = addr.exploded
        if str(row.get("compressed_form", "")) != expected_comp:
            errors.append(f"Compressed form mismatch for {addr_str}")
        if str(row.get("full_form", "")) != expected_full:
            errors.append(f"Full form mismatch for {addr_str}")

    # EUI-64 check
    expected_mac = str(challenge.ipv6_task.get("eui64_mac", "")).strip()
    if expected_mac:
        eui_section = report.get("eui64")
        if not isinstance(eui_section, dict):
            errors.append("IPv6 report is missing eui64 section")
        else:
            reported_iid = str(eui_section.get("iid", "")).strip()
            try:
                expected_iid = _eui64_from_mac(expected_mac)
                if reported_iid != expected_iid:
                    errors.append("EUI-64 IID does not match the expected value for the challenge MAC address")
            except ValueError:
                errors.append("Challenge contains an invalid eui64_mac value")

    return errors


def main() -> int:
    args = build_arg_parser().parse_args()
    base_dir = args.base_dir.resolve()

    errors: List[str] = []

    try:
        challenge = load_challenge(args.challenge)
    except Exception as e:
        raise SystemExit(f"[ERROR] Cannot load challenge: {e}") from e

    errors.extend(_validate_time_window(challenge, ignore_expiry=args.ignore_expiry))

    evidence_path = (base_dir / args.evidence).resolve() if not args.evidence.is_absolute() else args.evidence.resolve()
    if not evidence_path.exists():
        errors.append(f"Missing evidence file: {args.evidence}")
        print("[FAIL]")
        print(_format_errors(errors))
        return 2

    artefacts, ev_errors = _validate_evidence(evidence_path, base_dir, challenge)
    errors.extend(ev_errors)

    # Locate required outputs (prefer challenge outputs, but fall back to evidence paths)
    subnet_plan = base_dir / challenge.outputs["subnet_plan_json"]
    ipv6_report = base_dir / challenge.outputs["ipv6_report_json"]

    if not subnet_plan.exists():
        errors.append(f"Missing subnet plan output: {challenge.outputs['subnet_plan_json']}")
    else:
        errors.extend(_validate_subnet_plan(subnet_plan, challenge))

    if not ipv6_report.exists():
        errors.append(f"Missing IPv6 report output: {challenge.outputs['ipv6_report_json']}")
    else:
        errors.extend(_validate_ipv6_report(ipv6_report, challenge))

    if errors:
        print("[FAIL]")
        print(_format_errors(errors))
        return 2

    if args.verbose:
        print("[OK] Challenge integrity and time window validated")
        print(f"[OK] Evidence hashes validated for {len(artefacts)} artefacts")
        print("[OK] Subnet plan validated")
        print("[OK] IPv6 report validated")

    print("[PASS]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
