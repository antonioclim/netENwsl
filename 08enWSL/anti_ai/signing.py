"""Optional signing helpers.

In a strict deployment, the secret key should live only in CI.
For local self-checks, signing can be omitted.
"""

from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any, Dict, Optional


def canonical_json(data: Dict[str, Any]) -> bytes:
    """Serialise a dict deterministically."""
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )


def sign_dict(data: Dict[str, Any], secret: str) -> str:
    """Return a hex HMAC-SHA256 signature for a dict."""
    msg = canonical_json(data)
    return hmac.new(secret.encode("utf-8"), msg, hashlib.sha256).hexdigest()


def verify_signature(data: Dict[str, Any], secret: str, signature: Optional[str]) -> bool:
    """Verify a signature if provided."""
    if not signature:
        return False
    expected = sign_dict(data, secret)
    return hmac.compare_digest(expected, signature)