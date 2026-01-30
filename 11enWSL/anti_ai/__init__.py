"""Anti-AI challenge and validation utilities for the NETWORKING kit.

The anti-AI mechanism used in this kit is based on time-limited challenges
(token, seed and TTL) plus evidence that is hard to fabricate convincingly
without actually running the laboratory tasks.

Week 11 focuses on load balancing and DNS therefore validation is primarily
performed against captured traffic (pcap) plus an evidence JSON.
"""

from .challenge import generate_challenge, verify_challenge_signature
from .week11_validator import validate_week11

__all__ = [
    "generate_challenge",
    "verify_challenge_signature",
    "validate_week11",
]
