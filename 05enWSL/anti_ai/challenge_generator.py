#!/usr/bin/env python3
"""
Week 5 Anti-AI challenge generator.

Usage
-----
    python -m anti_ai.challenge_generator --student-id ABC123
    python -m anti_ai.challenge_generator --student-id ABC123 --output artifacts/anti_ai/challenge_ABC123.yaml

The challenge includes:
- an individualised VLSM problem instance (organisation block and department requirements)
- an individualised IPv6 dataset for analysis and transition planning
- per-task tokens that must be embedded in the submitted JSON artefacts
"""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import secrets
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

from anti_ai.challenge import DepartmentSpec, DualStackHostSpec, Week5Challenge, save_challenge, utc_now_iso


DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[1] / "artifacts" / "anti_ai"
DEFAULT_VALID_HOURS = 24


def _sanitise_student_id(student_id: str) -> str:
    cleaned = "".join(c for c in student_id.strip() if c.isalnum() or c in "-_")
    if len(cleaned) < 3:
        raise ValueError("Student ID must be at least 3 characters after sanitisation")
    return cleaned[:32]


def _seed_from(student_id: str, session_token: str) -> int:
    payload = (student_id + "::" + session_token).encode("utf-8")
    return int(hashlib.sha256(payload).hexdigest()[:16], 16)


def _next_pow2(n: int) -> int:
    if n <= 1:
        return 1
    p = 1
    while p < n:
        p <<= 1
    return p


def _prefix_for_hosts(hosts: int) -> int:
    # usable hosts = 2^(32-prefix) - 2
    needed = hosts + 2
    size = _next_pow2(needed)
    prefix = 32 - (size.bit_length() - 1)
    return int(prefix)


def _generate_departments(rng_seed: int) -> List[DepartmentSpec]:
    # Stable list of names to preserve pedagogical intent, but host counts vary.
    templates: List[Tuple[str, int, str]] = [
        ("Engineering", 50, "Development workstations and build servers"),
        ("Sales", 25, "Sales laptops, mobiles and VoIP handsets"),
        ("HR", 10, "Human resources workstations"),
        ("Management", 5, "Executive offices"),
        ("IT_Infrastructure", 12, "Servers, switches, access points and monitoring"),
        ("Guest_WiFi", 30, "Visitor wireless access"),
    ]

    # Derive per-department jitter from the seed without using global RNG state.
    depts: List[DepartmentSpec] = []
    for i, (name, base_hosts, desc) in enumerate(templates):
        jitter_src = hashlib.sha256(f"{rng_seed}:{name}:{i}".encode("utf-8")).hexdigest()
        jitter = int(jitter_src[:2], 16) % 9  # 0..8
        # Alternate +/- jitter for variety.
        signed = jitter if (int(jitter_src[2:4], 16) % 2 == 0) else -jitter
        hosts = max(2, base_hosts + signed)
        depts.append(DepartmentSpec(name=name, required_hosts=int(hosts), description=desc))
    return depts


def _choose_organisation_block(rng_seed: int, departments: List[DepartmentSpec]) -> str:
    # Compute the minimum block size that can hold the VLSM allocation if we allocate one subnet per department.
    sizes = [2 ** (32 - _prefix_for_hosts(d.required_hosts)) for d in departments]
    total = sum(sizes)
    block_size = _next_pow2(total)

    # Avoid overly large blocks in a Week 5 context.
    if block_size > 4096:
        block_size = 4096

    base_prefix = 32 - (block_size.bit_length() - 1)
    # Use the 10.5.0.0/16 teaching range to keep examples consistent across the kit.
    pool = ipaddress.IPv4Network("10.5.0.0/16")
    blocks = pool.num_addresses // block_size
    if blocks < 1:
        raise ValueError("Internal error: cannot allocate organisation block inside 10.5.0.0/16")

    idx = rng_seed % blocks
    start_int = int(pool.network_address) + idx * block_size
    block = ipaddress.IPv4Network((start_int, base_prefix))
    return str(block)


def _generate_ipv6_dataset(rng_seed: int) -> Dict[str, Any]:
    # Unique but stable hextets derived from the seed.
    h1 = (rng_seed >> 0) & 0xFFFF
    h2 = (rng_seed >> 16) & 0xFFFF
    h3 = (rng_seed >> 32) & 0xFFFF

    global_prefix = f"2001:db8:{h1:04x}::/48"
    ula_prefix = f"fd{(h2 >> 8) & 0xFF:02x}:{h2:04x}:{h3:04x}::/48"

    sample_addresses = [
        f"2001:db8:{h1:04x}::1",
        f"2001:db8:{h1:04x}:1::{(h2 % 65535):x}",
        "fe80::1",
        "::1",
        f"{ula_prefix.split('/')[0]}10",
        "ff02::1",
        "::ffff:192.168.1.1",
    ]

    hosts = [
        DualStackHostSpec(
            hostname="web-server-01",
            ipv4_address="192.168.1.10",
            ipv6_global=f"2001:db8:{h1:04x}:10::10",
            ipv6_link_local="fe80::1",
            description="Primary web server",
        ),
        DualStackHostSpec(
            hostname="db-server-01",
            ipv4_address="192.168.1.20",
            ipv6_global=f"2001:db8:{h1:04x}:10::20",
            ipv6_link_local="fe80::2",
            description="Database server",
        ),
        DualStackHostSpec(
            hostname="app-server-01",
            ipv4_address="192.168.1.30",
            ipv6_global=f"2001:db8:{h1:04x}:10::30",
            ipv6_link_local="fe80::3",
            description="Application backend",
        ),
    ]

    # Deterministic MAC address for EUI-64 task
    mac = f"02:{(h1 >> 8) & 0xFF:02x}:{h1 & 0xFF:02x}:{(h2 >> 8) & 0xFF:02x}:{h2 & 0xFF:02x}:{(h3 >> 8) & 0xFF:02x}"

    return {
        "global_prefix": global_prefix,
        "ula_prefix": ula_prefix,
        "sample_addresses": sample_addresses,
        "organisation_hosts": [asdict(h) for h in hosts],
        "eui64_mac": mac,
    }


def generate_week5_challenge(student_id: str, *, valid_for_hours: int = DEFAULT_VALID_HOURS) -> Week5Challenge:
    student_id = _sanitise_student_id(student_id)
    session_token = secrets.token_hex(16)
    seed = _seed_from(student_id, session_token)

    departments = _generate_departments(seed)
    org_block = _choose_organisation_block(seed, departments)

    ipv6_task = _generate_ipv6_dataset(seed)

    tokens = {
        "subnet_plan_token": f"W5-SUB-{secrets.token_hex(8)}",
        "ipv6_report_token": f"W5-IPV6-{secrets.token_hex(8)}",
    }

    outputs = {
        "subnet_plan_json": f"subnet_plan_{student_id}.json",
        "ipv6_report_json": f"ipv6_report_{student_id}.json",
        "evidence_json": f"evidence_{student_id}.json",
    }

    vlsm_task: Dict[str, Any] = {
        "organisation_block": org_block,
        "departments": [asdict(d) for d in departments],
        "allocation_rules": {
            "strategy": "largest-first",
            "packing": "lowest-address-first",
            "note": "Alternative correct allocations may exist, but the validator expects a valid non-overlapping plan within the organisation block.",
        },
    }

    challenge = Week5Challenge(
        version=1,
        week=5,
        student_id=student_id,
        issued_at_utc=utc_now_iso(),
        valid_for_hours=int(valid_for_hours),
        session_token=session_token,
        tokens=tokens,
        outputs=outputs,
        vlsm_task=vlsm_task,
        ipv6_task=ipv6_task,
        integrity={},
    )
    # Integrity is computed on serialisation.
    return challenge


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Generate a Week 5 anti-AI challenge YAML file.")
    p.add_argument("--student-id", required=True, help="Student identifier (letters, digits, - and _ are allowed)")
    p.add_argument("--output", type=Path, default=None, help="Output YAML file path")
    p.add_argument("--valid-hours", type=int, default=DEFAULT_VALID_HOURS, help="Challenge validity window in hours")
    return p


def main() -> int:
    args = build_arg_parser().parse_args()
    challenge = generate_week5_challenge(args.student_id, valid_for_hours=args.valid_hours)

    out = args.output
    if out is None:
        out = DEFAULT_OUTPUT_DIR / f"challenge_{challenge.student_id}.yaml"

    save_challenge(challenge, out)
    print(f"[OK] Challenge written to: {out}")
    print(f"[OK] Required outputs: {challenge.outputs['subnet_plan_json']} and {challenge.outputs['ipv6_report_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
