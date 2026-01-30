"""Week 12 anti-AI validation helpers.

The Week 12 kit contains exercises that are easy to *describe* without running
any software. To keep the assessment authentic, this package provides an
evidence-based workflow:

1. Issue a short-lived challenge containing unique tokens.
2. Perform the required SMTP and RPC interactions.
3. Capture traffic (PCAP or PCAPNG).
4. Validate the submission by searching for challenge tokens in the capture.

Nothing here is intended to be adversarial towards students. The goal is to
reward real protocol interaction and discourage purely synthetic submissions.
"""

from __future__ import annotations

from .challenge import Week12Challenge
from .validator import Week12SubmissionValidator

__all__ = [
    "Week12Challenge",
    "Week12SubmissionValidator",
]

__version__ = "1.0.0"
