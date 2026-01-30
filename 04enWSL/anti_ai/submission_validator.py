#!/usr/bin/env python3
"""anti_ai.submission_validator

Validates a Week 4 submission against a challenge and evidence file.

What is checked:
- evidence.json structure and file hashes (determinism)
- challenge validity window (TTL)
- presence of per-challenge tokens inside protocol-correct network traffic

The validator is intentionally conservative:
it prefers false negatives over accepting unverified submissions.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import struct
import sys
import zlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from anti_ai.challenge import load_challenge, normalise_challenge_dict
from anti_ai.pcap_tools import iter_tcp_from_pcap, iter_udp_from_pcap


class ValidationError(Exception):
    pass


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _canonical_payload(payload: Dict[str, Any]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def verify_challenge_signature(ch: Dict[str, Any], require_signature: bool = False) -> Tuple[bool, str]:
    tag = str(ch.get("integrity_tag", ""))
    if tag == "UNSIGNED":
        if require_signature:
            return False, "Challenge is unsigned"
        return True, "Challenge is unsigned (allowed)"

    if not tag.startswith("hmac-sha256:"):
        return False, "Unsupported integrity_tag format"

    secret = os.environ.get("ANTI_AI_SIGNING_SECRET", "").strip()
    if not secret:
        if require_signature:
            return False, "ANTI_AI_SIGNING_SECRET not set but signature verification required"
        return True, "Signature present but ANTI_AI_SIGNING_SECRET not set (cannot verify)"

    payload = dict(ch)
    payload.pop("integrity_tag", None)
    payload.pop("instructions", None)

    expected = hmac.new(secret.encode("utf-8"), _canonical_payload(payload), hashlib.sha256).hexdigest()
    got = tag.split(":", 1)[1]
    ok = hmac.compare_digest(expected, got)
    return ok, "Signature verified" if ok else "Signature mismatch"


def verify_ttl(ch: Dict[str, Any], now: Optional[datetime] = None) -> Tuple[bool, str]:
    now = now or _utc_now()
    issued = ch["issued_at_utc"]
    ttl = int(ch["ttl_seconds"])
    delta = (now - issued).total_seconds()
    if delta < 0:
        return False, "Challenge issued_at is in the future"
    if delta > ttl:
        return False, f"Challenge expired (age={int(delta)}s > ttl={ttl}s)"
    return True, f"Challenge valid (age={int(delta)}s, ttl={ttl}s)"


def load_evidence(path: str | Path) -> Dict[str, Any]:
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Evidence must be a JSON object")
    return data


def verify_evidence_hashes(evidence: Dict[str, Any], base_dir: Path) -> Tuple[bool, str, List[str]]:
    errors: List[str] = []
    artefacts = evidence.get("artefacts", [])
    if not isinstance(artefacts, list) or not artefacts:
        return False, "Evidence contains no artefacts", ["No artefacts listed"]

    for a in artefacts:
        if not isinstance(a, dict):
            errors.append("Invalid artefact entry (not an object)")
            continue
        rel = a.get("path")
        sha = a.get("sha256")
        if not rel or not sha:
            errors.append("Artefact missing path or sha256")
            continue
        p = (base_dir / rel).resolve()
        if not p.exists():
            errors.append(f"Missing artefact file: {rel}")
            continue
        actual = _sha256_file(p)
        if actual != sha:
            errors.append(f"Checksum mismatch: {rel}")
    if errors:
        return False, "Artefact hash verification failed", errors
    return True, "Artefact hashes verified", []


def _collect_tcp_payload_stream(pcappath: Path, dst_port: int) -> bytes:
    chunks: List[bytes] = []
    for tcp in iter_tcp_from_pcap(pcappath):
        # Focus on client->server direction for determinism
        if tcp.dst_port == dst_port and tcp.payload:
            chunks.append(tcp.payload)
    return b"".join(chunks)


def _check_text_token(pcappath: Path, text_port: int, token: str) -> bool:
    stream = _collect_tcp_payload_stream(pcappath, text_port)
    needle = f"SET anti_ai {token}".encode("utf-8")
    return needle in stream


BIN_HDR_FMT = "!2sBBHII"
BIN_HDR_LEN = struct.calcsize(BIN_HDR_FMT)
BIN_HDR_WO_CRC_FMT = "!2sBBHI"

TYPE_PUT_REQ = 3

def _bin_crc32(data: bytes) -> int:
    return zlib.crc32(data) & 0xFFFFFFFF


def _scan_binary_put_with_token(stream: bytes, token: str) -> bool:
    tok_b = token.encode("utf-8")
    i = 0
    while True:
        i = stream.find(b"NP", i)
        if i == -1:
            return False
        if i + BIN_HDR_LEN > len(stream):
            return False
        try:
            magic, ver, mtype, plen, seq, crc = struct.unpack(BIN_HDR_FMT, stream[i:i+BIN_HDR_LEN])
        except struct.error:
            i += 2
            continue
        if magic != b"NP" or ver != 1:
            i += 2
            continue
        end = i + BIN_HDR_LEN + plen
        if end > len(stream):
            # Not enough bytes in this stream, continue searching in case this is a false positive
            i += 2
            continue
        payload = stream[i+BIN_HDR_LEN:end]
        hdr_wo_crc = struct.pack(BIN_HDR_WO_CRC_FMT, magic, ver, mtype, plen, seq)
        if _bin_crc32(hdr_wo_crc + payload) != crc:
            i += 2
            continue
        if mtype != TYPE_PUT_REQ:
            i = end
            continue
        # Decode PUT payload: klen(1) + key + value
        if not payload:
            i = end
            continue
        klen = payload[0]
        if len(payload) < 1 + klen:
            i = end
            continue
        key = payload[1:1+klen].decode("utf-8", errors="replace")
        value = payload[1+klen:]
        if key == "anti_ai" and tok_b in value:
            return True
        i = end


def _check_binary_token(pcappath: Path, binary_port: int, token: str) -> bool:
    stream = _collect_tcp_payload_stream(pcappath, binary_port)
    return _scan_binary_put_with_token(stream, token)


UDP_FMT_WO_CRC = "!BIf10s"
UDP_FMT = "!BIf10sI"
UDP_LEN = struct.calcsize(UDP_FMT)

def _parse_udp_sensor(payload: bytes) -> Optional[Tuple[int, int, float, str]]:
    if len(payload) != UDP_LEN:
        return None
    ver, sensor_id, temp_c, loc_b, crc = struct.unpack(UDP_FMT, payload)
    base = struct.pack(UDP_FMT_WO_CRC, ver, sensor_id, temp_c, loc_b)
    if _bin_crc32(base) != crc:
        return None
    loc = loc_b.decode("utf-8", errors="replace").rstrip("\x00")
    return ver, sensor_id, temp_c, loc


def _check_udp_token(pcappath: Path, udp_port: int, sensor_id_expected: int, loc_expected: str) -> bool:
    for udp in iter_udp_from_pcap(pcappath):
        if udp.dst_port != udp_port:
            continue
        parsed = _parse_udp_sensor(udp.payload)
        if not parsed:
            continue
        ver, sensor_id, _temp, loc = parsed
        if ver != 1:
            continue
        if sensor_id == sensor_id_expected and loc == loc_expected:
            return True
    return False


def find_pcap_files(evidence: Dict[str, Any], base_dir: Path) -> List[Path]:
    pcaps: List[Path] = []
    for a in evidence.get("artefacts", []):
        if not isinstance(a, dict):
            continue
        p = a.get("path", "")
        if isinstance(p, str) and p.lower().endswith(".pcap"):
            pp = (base_dir / p).resolve()
            if pp.exists():
                pcaps.append(pp)
    # Deduplicate while preserving order
    out: List[Path] = []
    seen = set()
    for p in pcaps:
        if str(p) not in seen:
            seen.add(str(p))
            out.append(p)
    return out


def validate_tokens(ch: Dict[str, Any], pcaps: List[Path]) -> Tuple[bool, List[str]]:
    errs: List[str] = []
    if not pcaps:
        return False, ["No PCAP files found in evidence artefacts"]

    text_ok = any(_check_text_token(p, ch["text_port"], ch["text_token"]) for p in pcaps)
    if not text_ok:
        errs.append("TEXT token not found in client->server payloads (SET anti_ai <token>)")

    bin_ok = any(_check_binary_token(p, ch["binary_port"], ch["binary_token"]) for p in pcaps)
    if not bin_ok:
        errs.append("BINARY token not found in a valid PUT_REQ (CRC-verified)")

    udp_ok = any(
        _check_udp_token(p, ch["udp_port"], ch["udp_sensor_id"], ch["udp_location_tag"]) for p in pcaps
    )
    if not udp_ok:
        errs.append("UDP token not found in a valid sensor datagram (CRC-verified)")

    return not errs, errs


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Week 4 anti-AI submission evidence")
    parser.add_argument("--challenge", required=True, help="Challenge YAML path")
    parser.add_argument("--evidence", required=True, help="Evidence JSON path")
    parser.add_argument("--base-dir", default=".", help="Project root directory (default: .)")
    parser.add_argument(
        "--require-signature",
        action="store_true",
        help="Fail if the challenge signature cannot be verified",
    )
    parser.add_argument(
        "--skip-hash-check",
        action="store_true",
        help="Skip artefact hash verification (not recommended)",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()

    ch_raw = load_challenge(args.challenge)
    ch = normalise_challenge_dict(ch_raw)

    ok_sig, sig_msg = verify_challenge_signature(ch_raw, require_signature=args.require_signature)
    ok_ttl, ttl_msg = verify_ttl(ch)

    if args.verbose:
        print(f"[challenge] {sig_msg}")
        print(f"[challenge] {ttl_msg}")

    if not ok_sig:
        print(f"FAIL: {sig_msg}")
        return 1
    if not ok_ttl:
        print(f"FAIL: {ttl_msg}")
        return 1

    evidence = load_evidence(args.evidence)

    if not args.skip_hash_check:
        ok_hash, hash_msg, hash_errs = verify_evidence_hashes(evidence, base_dir)
        if args.verbose:
            print(f"[evidence] {hash_msg}")
        if not ok_hash:
            print("FAIL: evidence hash verification failed")
            for e in hash_errs[:50]:
                print(f"  - {e}")
            return 1

    pcaps = find_pcap_files(evidence, base_dir)
    ok_tokens, token_errs = validate_tokens(ch, pcaps)

    if not ok_tokens:
        print("FAIL: token validation failed")
        for e in token_errs:
            print(f"  - {e}")
        return 1

    print("PASS: submission evidence validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
