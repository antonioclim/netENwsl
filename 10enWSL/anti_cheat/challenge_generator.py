#!/usr/bin/env python3
"""
Anti-AI Challenge Generator
===========================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Generates unique per-session challenges that require real interaction
with the laboratory environment. These challenges cannot be solved
by AI systems without access to the running Docker containers.

Usage:
    python -m anti_cheat.challenge_generator --student-id ABC123
    python -m anti_cheat.challenge_generator --student-id ABC123 --output challenge.yaml

The generated challenges include:
    - DNS challenges: Add a unique TXT record to the DNS server
    - HTTPS challenges: Start server on a unique port
    - FTP challenges: Create a file with unique content
    - PCAP challenges: Capture traffic with unique headers
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import hashlib
import secrets
import socket
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    print("[ERROR] PyYAML is required: pip install pyyaml")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
DEFAULT_OUTPUT_DIR = Path(__file__).parent.parent / "artifacts"
CHALLENGE_VALIDITY_HOURS = 4
DNS_PORT = 5353
HTTPS_PORT_RANGE = (8500, 8599)
FTP_PORT = 2121


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_CLASSES
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class DNSChallenge:
    """DNS challenge requiring TXT record addition."""
    domain: str
    expected_txt: str
    instructions: str


@dataclass
class HTTPSChallenge:
    """HTTPS challenge requiring server on specific port."""
    port: int
    endpoint: str
    expected_response: Dict[str, Any]


@dataclass
class FTPChallenge:
    """FTP challenge requiring file creation."""
    filename: str
    content: str
    remote_path: str


@dataclass
class PCAPChallenge:
    """PCAP challenge requiring traffic capture with unique header."""
    custom_header: str
    header_value: str
    verification_hint: str


# ═══════════════════════════════════════════════════════════════════════════════
# SESSION_CHALLENGE
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class SessionChallenge:
    """
    Generates unique challenges for a student session.
    
    Each challenge requires real interaction with the lab environment
    and cannot be solved by AI systems without access to running containers.
    
    Attributes:
        student_id: Unique identifier for the student
        session_token: Randomly generated token for this session
        timestamp: When the session was created
        challenges: Dictionary of generated challenges
    """
    
    student_id: str
    session_token: str = field(default_factory=lambda: secrets.token_hex(16))
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    challenges: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self) -> None:
        """Validate student_id format."""
        if not self.student_id or len(self.student_id) < 3:
            raise ValueError("Student ID must be at least 3 characters")
        
        # Sanitise student_id for use in domains/filenames
        self.student_id = "".join(
            c for c in self.student_id if c.isalnum() or c in "-_"
        )[:20]
    
    def generate_dns_challenge(self) -> DNSChallenge:
        """
        Generate a unique DNS challenge.
        
        The student must add a TXT record to the DNS server configuration
        and verify it responds correctly.
        
        Returns:
            DNSChallenge with domain and expected TXT value
        """
        # Create unique domain and value
        domain = f"verify-{self.session_token[:8]}.lab.local"
        challenge_value = f"proof-{self.student_id}-{self.session_token[:12]}"
        
        instructions = f"""
═══════════════════════════════════════════════════════════════════
DNS CHALLENGE — Proof of Lab Interaction
═══════════════════════════════════════════════════════════════════

1. Edit docker/dns-server/dns_server.py and add this TXT record:
   
   In the RECORDS dictionary, add:
   '{domain}': '{challenge_value}'

2. Restart the DNS container:
   docker restart week10_dns

3. Verify your change works:
   dig @127.0.0.1 -p {DNS_PORT} {domain} TXT +short
   
   Expected output: "{challenge_value}"

4. Include the dig output in your submission.

═══════════════════════════════════════════════════════════════════
"""
        
        challenge = DNSChallenge(
            domain=domain,
            expected_txt=challenge_value,
            instructions=instructions
        )
        
        self.challenges['dns'] = {
            'domain': domain,
            'expected_txt': challenge_value,
            'port': DNS_PORT,
            'type': 'TXT'
        }
        
        return challenge
    
    def generate_https_challenge(self) -> HTTPSChallenge:
        """
        Generate a unique HTTPS challenge.
        
        The student must start an HTTPS server on a specific port
        that responds to a unique endpoint.
        
        Returns:
            HTTPSChallenge with port and endpoint details
        """
        # Calculate unique port from session token
        port_offset = int(self.session_token[:4], 16) % 100
        port = HTTPS_PORT_RANGE[0] + port_offset
        
        endpoint = f"/verify/{self.session_token[:16]}"
        expected_response = {
            'status': 'verified',
            'student': self.student_id,
            'token': self.session_token[:16]
        }
        
        challenge = HTTPSChallenge(
            port=port,
            endpoint=endpoint,
            expected_response=expected_response
        )
        
        self.challenges['https'] = {
            'port': port,
            'endpoint': endpoint,
            'expected_response': expected_response
        }
        
        return challenge
    
    def generate_ftp_challenge(self) -> FTPChallenge:
        """
        Generate a unique FTP challenge.
        
        The student must create a file with specific content
        on the FTP server.
        
        Returns:
            FTPChallenge with filename and content details
        """
        filename = f"proof_{self.student_id}_{self.session_token[:8]}.txt"
        content = f"VERIFIED:{self.student_id}:{self.timestamp}:{self.session_token[:16]}"
        remote_path = f"/home/labftp/{filename}"
        
        challenge = FTPChallenge(
            filename=filename,
            content=content,
            remote_path=remote_path
        )
        
        self.challenges['ftp'] = {
            'filename': filename,
            'content': content,
            'remote_path': remote_path,
            'port': FTP_PORT
        }
        
        return challenge
    
    def generate_pcap_challenge(self) -> PCAPChallenge:
        """
        Generate a unique PCAP challenge.
        
        The student must capture traffic containing a unique HTTP header.
        
        Returns:
            PCAPChallenge with header details
        """
        header_name = "X-Student-Verify"
        header_value = f"{self.student_id}-{self.session_token[:12]}"
        
        challenge = PCAPChallenge(
            custom_header=header_name,
            header_value=header_value,
            verification_hint=f'Search PCAP for: "{header_name}: {header_value}"'
        )
        
        self.challenges['pcap'] = {
            'header_name': header_name,
            'header_value': header_value,
            'full_header': f"{header_name}: {header_value}"
        }
        
        return challenge
    
    def generate_all_challenges(self) -> Dict[str, Any]:
        """
        Generate all challenge types.
        
        Returns:
            Dictionary containing all challenges
        """
        self.generate_dns_challenge()
        self.generate_https_challenge()
        self.generate_ftp_challenge()
        self.generate_pcap_challenge()
        
        return self.challenges
    
    def compute_verification_hash(self) -> str:
        """
        Compute a verification hash for integrity checking.
        
        Returns:
            16-character hex hash
        """
        data = f"{self.student_id}:{self.session_token}:{self.timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def export_to_yaml(self, output_path: Path) -> None:
        """
        Export challenges to a YAML file.
        
        Args:
            output_path: Path for the output YAML file
        """
        export_data = {
            'metadata': {
                'student_id': self.student_id,
                'session_token': self.session_token,
                'generated_at': self.timestamp,
                'valid_hours': CHALLENGE_VALIDITY_HOURS,
                'verification_hash': self.compute_verification_hash()
            },
            'challenges': self.challenges,
            'instructions': {
                'overview': 'Complete ALL challenges below to prove lab interaction.',
                'submission': 'Include this file and all proof artifacts in your submission.',
                'expiry': f'Challenges expire {CHALLENGE_VALIDITY_HOURS} hours after generation.'
            }
        }
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(export_data, f, default_flow_style=False, allow_unicode=True)
        
        print(f"[OK] Challenges exported to: {output_path}")
    
    def print_summary(self) -> None:
        """Print a summary of all challenges to stdout."""
        print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  SESSION CHALLENGE SUMMARY                                                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Student ID:      {self.student_id:<58} ║
║  Session Token:   {self.session_token[:32]}...                       ║
║  Generated:       {self.timestamp[:19]:<58} ║
║  Valid for:       {CHALLENGE_VALIDITY_HOURS} hours                                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  CHALLENGES TO COMPLETE:                                                      ║
║                                                                              ║""")
        
        if 'dns' in self.challenges:
            dns = self.challenges['dns']
            print(f"║  1. DNS:   Add TXT record for {dns['domain']:<40} ║")
        
        if 'https' in self.challenges:
            https = self.challenges['https']
            print(f"║  2. HTTPS: Start server on port {https['port']:<41} ║")
        
        if 'ftp' in self.challenges:
            ftp = self.challenges['ftp']
            print(f"║  3. FTP:   Create file {ftp['filename']:<48} ║")
        
        if 'pcap' in self.challenges:
            pcap = self.challenges['pcap']
            print(f"║  4. PCAP:  Capture traffic with header {pcap['header_name']:<31} ║")
        
        print(f"""║                                                                              ║
║  Verification Hash: {self.compute_verification_hash():<52} ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")


# ═══════════════════════════════════════════════════════════════════════════════
# COMMAND_LINE_INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate unique anti-AI challenges for Week 10 lab",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python -m anti_cheat.challenge_generator --student-id ABC123
    python -m anti_cheat.challenge_generator --student-id ABC123 --output my_challenge.yaml
    python -m anti_cheat.challenge_generator --student-id ABC123 --dns-only
"""
    )
    
    parser.add_argument(
        '--student-id', '-s',
        required=True,
        help='Your student ID (minimum 3 characters)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=Path,
        default=None,
        help='Output YAML file path (default: artifacts/challenge_<student_id>.yaml)'
    )
    
    parser.add_argument(
        '--dns-only',
        action='store_true',
        help='Generate only DNS challenge'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Minimal output (no summary)'
    )
    
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point."""
    args = parse_args(argv)
    
    try:
        session = SessionChallenge(student_id=args.student_id)
        
        if args.dns_only:
            session.generate_dns_challenge()
        else:
            session.generate_all_challenges()
        
        # Determine output path
        if args.output:
            output_path = args.output
        else:
            output_path = DEFAULT_OUTPUT_DIR / f"challenge_{session.student_id}.yaml"
        
        # Export and optionally print summary
        session.export_to_yaml(output_path)
        
        if not args.quiet:
            session.print_summary()
        
        return 0
        
    except ValueError as e:
        print(f"[ERROR] Invalid input: {e}")
        return 1
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
