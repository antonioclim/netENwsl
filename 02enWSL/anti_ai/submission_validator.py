"""Validate a Week 2 anti‑AI submission.

The validator checks:
- challenge expiry and signature (if master key is available)
- evidence.json structure and artefact hashes
- proof logs contain the expected per‑student payload token
- basic protocol expectations (TCP includes 'OK:' and UDP returns uppercase token)

This is deliberately conservative. If validation fails, the report should explain why.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

from anti_ai.challenge import Challenge, get_master_key_from_env
from anti_ai.evidence_collector import sha256_file


class ValidationError(Exception):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValidationError(f"Failed to parse JSON {path}: {exc}") from exc


def normalise_path(p: str) -> str:
    return p.replace("\\", "/")


def validate_challenge(ch: Challenge, allow_unsigned: bool) -> None:
    if ch.schema_version != 1 or ch.week_id != 2:
        raise ValidationError("Challenge schema_version or week_id mismatch")

    if ch.is_expired():
        raise ValidationError("Challenge has expired (TTL exceeded)")

    key = get_master_key_from_env()
    if key is None:
        # No key available, we cannot verify signature.
        if ch.signature and ch.signature.startswith("hmac-sha256:"):
            # Signed challenge but no key to verify. Accept, but warn via stderr in CLI.
            return
        if not allow_unsigned:
            raise ValidationError("Challenge is unsigned and ANTI_AI_MASTER_KEY is not set (use --allow-unsigned for practice)")
        return

    if not ch.signature:
        if not allow_unsigned:
            raise ValidationError("Challenge is unsigned but a master key is configured (refuse by default)")
        return

    if not ch.verify_signature(key):
        raise ValidationError("Challenge signature is invalid")


def validate_evidence_meta(evidence: dict[str, Any], ch: Challenge) -> None:
    meta = evidence.get("meta") or {}
    if meta.get("week_id") != 2:
        raise ValidationError("Evidence meta.week_id mismatch")
    if meta.get("challenge_id") != ch.challenge_id:
        raise ValidationError("Evidence meta.challenge_id mismatch")
    if meta.get("student_id") != ch.student_id:
        raise ValidationError("Evidence meta.student_id mismatch")
    if meta.get("challenge_payload_sha256") != ch.stable_hash():
        raise ValidationError("Evidence meta.challenge_payload_sha256 mismatch")


def validate_artefacts(evidence: dict[str, Any], base_dir: Path) -> list[Path]:
    artefacts = evidence.get("artefacts")
    if not isinstance(artefacts, list) or not artefacts:
        raise ValidationError("Evidence must include a non-empty artefacts list")

    rel_paths: list[Path] = []
    for entry in artefacts:
        if not isinstance(entry, dict):
            raise ValidationError("Invalid artefact entry type")
        path = entry.get("path")
        sha = entry.get("sha256")
        if not path or not sha:
            raise ValidationError("Artefact entry missing path or sha256")

        rel = Path(normalise_path(str(path)))
        abs_path = (base_dir / rel).resolve()
        if not abs_path.exists():
            raise ValidationError(f"Missing artefact file: {rel}")

        actual = sha256_file(abs_path)
        if actual != sha:
            raise ValidationError(f"SHA256 mismatch for {rel}")

        rel_paths.append(rel)

    return rel_paths


def read_text_safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def validate_proof_logs(base_dir: Path, artefact_paths: list[Path], token: str) -> None:
    # Require at least these proof logs.
    required = {"tcp_client.txt", "udp_client.txt"}
    present = {p.name for p in artefact_paths}
    missing = sorted(required - present)
    if missing:
        raise ValidationError(f"Missing required proof logs: {', '.join(missing)}")

    tcp_text = read_text_safe((base_dir / next(p for p in artefact_paths if p.name == "tcp_client.txt")).resolve())
    udp_text = read_text_safe((base_dir / next(p for p in artefact_paths if p.name == "udp_client.txt")).resolve())

    token_upper = token.upper()

    if "OK:" not in tcp_text:
        raise ValidationError("TCP client log does not include expected 'OK:' response")

    if token_upper not in tcp_text.upper():
        raise ValidationError("TCP client log does not include the payload token")

    if token_upper not in udp_text.upper():
        raise ValidationError("UDP client log does not include the payload token")

    # UDP client prints RX line for responses.
    if "RX:" not in udp_text:
        raise ValidationError("UDP client log does not include an RX line")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Validate Week 2 anti‑AI submission")
    p.add_argument("--challenge", required=True, help="Challenge YAML path")
    p.add_argument("--evidence", required=True, help="Evidence JSON path")
    p.add_argument("--base-dir", default=".", help="Base directory for artefacts")
    p.add_argument("--allow-unsigned", action="store_true", help="Allow unsigned challenges (practice mode)")
    p.add_argument("--verbose", action="store_true", help="Verbose output")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    ch = Challenge.load_yaml(args.challenge)
    base_dir = Path(args.base_dir).resolve()
    evidence_path = Path(args.evidence).resolve()

    if not evidence_path.exists():
        print(f"✗ Missing evidence file: {evidence_path}")
        return 2

    try:
        validate_challenge(ch, allow_unsigned=bool(args.allow_unsigned))
    except ValidationError as exc:
        print(f"✗ Challenge validation failed: {exc}")
        return 3

    evidence = load_json(evidence_path)

    try:
        validate_evidence_meta(evidence, ch)
        artefact_paths = validate_artefacts(evidence, base_dir)
        validate_proof_logs(base_dir, artefact_paths, ch.payload_token)
    except ValidationError as exc:
        print(f"✗ Submission validation failed: {exc}")
        return 4

    if args.verbose:
        print("✓ Challenge and evidence validated")
        print(f"  Artefacts: {len(artefact_paths)}")
        print(f"  Token: {ch.payload_token}")

    print("✓ Submission PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
