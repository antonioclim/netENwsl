#!/usr/bin/env python3
"""
Submission Validator — Verifies Real Lab Interaction
=====================================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Validates that students have genuinely interacted with the laboratory
environment by checking challenge completions against the running
Docker containers.

Usage:
    python -m anti_cheat.submission_validator --challenge challenge.yaml
    python -m anti_cheat.submission_validator --challenge challenge.yaml --verbose
    python -m anti_cheat.submission_validator --challenge challenge.yaml --report report.json

Validation checks:
    - Timestamp validity (not expired)
    - DNS challenge completion
    - HTTPS server responsiveness
    - PCAP content verification
    - Environment fingerprint matching
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
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
CHALLENGE_VALIDITY_HOURS = 4
REQUIRED_CONTAINERS = {'week10_web', 'week10_dns', 'week10_ssh', 'week10_ftp'}
ARTIFACTS_DIR = Path(__file__).parent.parent / "artifacts"


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_CLASSES
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class ValidationResult:
    """Result of a single validation check."""
    name: str
    passed: bool
    message: str
    details: Optional[Dict[str, Any]] = None


@dataclass
class ValidationReport:
    """Complete validation report for a submission."""
    student_id: str
    session_token: str
    timestamp: str
    results: List[ValidationResult] = field(default_factory=list)
    
    @property
    def passed_count(self) -> int:
        """Number of passed validations."""
        return sum(1 for r in self.results if r.passed)
    
    @property
    def failed_count(self) -> int:
        """Number of failed validations."""
        return sum(1 for r in self.results if not r.passed)
    
    @property
    def total_count(self) -> int:
        """Total number of validations."""
        return len(self.results)
    
    @property
    def all_passed(self) -> bool:
        """Whether all validations passed."""
        return self.failed_count == 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary."""
        return {
            'student_id': self.student_id,
            'session_token': self.session_token[:16] + '...',
            'validated_at': datetime.now().isoformat(),
            'summary': {
                'passed': self.passed_count,
                'failed': self.failed_count,
                'total': self.total_count,
                'status': 'PASS' if self.all_passed else 'FAIL'
            },
            'results': [
                {
                    'name': r.name,
                    'passed': r.passed,
                    'message': r.message,
                    'details': r.details
                }
                for r in self.results
            ]
        }
    
    def to_json(self) -> str:
        """Convert report to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


# ═══════════════════════════════════════════════════════════════════════════════
# SUBMISSION_VALIDATOR
# ═══════════════════════════════════════════════════════════════════════════════
class SubmissionValidator:
    """
    Validates student submissions against generated challenges.
    
    Performs multiple validation checks to ensure the student has
    genuinely interacted with the laboratory environment.
    
    Attributes:
        challenge_file: Path to the challenge YAML file
        challenge_data: Loaded challenge data
        verbose: Whether to print detailed output
    """
    
    def __init__(self, challenge_file: Path, verbose: bool = False):
        """
        Initialise the validator.
        
        Args:
            challenge_file: Path to the challenge YAML file
            verbose: Print detailed validation output
            
        Raises:
            FileNotFoundError: If challenge file doesn't exist
            ValueError: If challenge file is invalid
        """
        if not challenge_file.exists():
            raise FileNotFoundError(f"Challenge file not found: {challenge_file}")
        
        with open(challenge_file, 'r', encoding='utf-8') as f:
            self.challenge_data = yaml.safe_load(f)
        
        if not self.challenge_data or 'metadata' not in self.challenge_data:
            raise ValueError("Invalid challenge file format")
        
        self.challenge_file = challenge_file
        self.verbose = verbose
        self.report: Optional[ValidationReport] = None
    
    def _log(self, message: str) -> None:
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(message)
    
    def validate_all(self) -> ValidationReport:
        """
        Run all validation checks.
        
        Returns:
            ValidationReport with all results
        """
        metadata = self.challenge_data['metadata']
        
        self.report = ValidationReport(
            student_id=metadata['student_id'],
            session_token=metadata['session_token'],
            timestamp=metadata['generated_at']
        )
        
        # Run all validations
        validations = [
            self._validate_timestamp,
            self._validate_hash_integrity,
            self._validate_dns_challenge,
            self._validate_https_challenge,
            self._validate_pcap_challenge,
            self._validate_environment_fingerprint,
        ]
        
        for validation in validations:
            try:
                result = validation()
                self.report.results.append(result)
                
                status = "✅ PASS" if result.passed else "❌ FAIL"
                self._log(f"  {status}: {result.name} — {result.message}")
                
            except Exception as e:
                self.report.results.append(ValidationResult(
                    name=validation.__name__.replace('_validate_', ''),
                    passed=False,
                    message=f"Validation error: {e}"
                ))
                self._log(f"  ❌ ERROR: {validation.__name__} — {e}")
        
        return self.report
    
    def _validate_timestamp(self) -> ValidationResult:
        """Validate that the challenge has not expired."""
        generated_str = self.challenge_data['metadata']['generated_at']
        valid_hours = self.challenge_data['metadata'].get('valid_hours', CHALLENGE_VALIDITY_HOURS)
        
        try:
            generated = datetime.fromisoformat(generated_str)
        except ValueError:
            return ValidationResult(
                name="timestamp",
                passed=False,
                message="Invalid timestamp format"
            )
        
        now = datetime.now()
        expiry = generated + timedelta(hours=valid_hours)
        
        if now > expiry:
            return ValidationResult(
                name="timestamp",
                passed=False,
                message=f"Challenge expired (generated {generated_str}, valid for {valid_hours}h)"
            )
        
        if generated > now:
            return ValidationResult(
                name="timestamp",
                passed=False,
                message="Invalid timestamp (in the future)"
            )
        
        remaining = expiry - now
        return ValidationResult(
            name="timestamp",
            passed=True,
            message=f"Valid ({remaining.seconds // 3600}h {(remaining.seconds % 3600) // 60}m remaining)",
            details={'generated': generated_str, 'expires': expiry.isoformat()}
        )
    
    def _validate_hash_integrity(self) -> ValidationResult:
        """Validate the challenge file integrity hash."""
        metadata = self.challenge_data['metadata']
        stored_hash = metadata.get('verification_hash', '')
        
        # Recompute hash
        data = f"{metadata['student_id']}:{metadata['session_token']}:{metadata['generated_at']}"
        computed_hash = hashlib.sha256(data.encode()).hexdigest()[:16]
        
        if stored_hash != computed_hash:
            return ValidationResult(
                name="hash_integrity",
                passed=False,
                message="Challenge file has been tampered with"
            )
        
        return ValidationResult(
            name="hash_integrity",
            passed=True,
            message="File integrity verified"
        )
    
    def _validate_dns_challenge(self) -> ValidationResult:
        """Validate that DNS challenge has been completed."""
        challenges = self.challenge_data.get('challenges', {})
        dns = challenges.get('dns')
        
        if not dns:
            return ValidationResult(
                name="dns_challenge",
                passed=False,
                message="No DNS challenge in file"
            )
        
        domain = dns['domain']
        expected_txt = dns['expected_txt']
        port = dns.get('port', 5353)
        
        try:
            result = subprocess.run(
                ['dig', f'@127.0.0.1', '-p', str(port), domain, 'TXT', '+short'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            actual = result.stdout.strip().strip('"')
            
            if expected_txt in actual:
                return ValidationResult(
                    name="dns_challenge",
                    passed=True,
                    message=f"DNS TXT record verified for {domain}",
                    details={'domain': domain, 'response': actual}
                )
            else:
                return ValidationResult(
                    name="dns_challenge",
                    passed=False,
                    message=f"DNS response mismatch: expected '{expected_txt}', got '{actual}'"
                )
                
        except subprocess.TimeoutExpired:
            return ValidationResult(
                name="dns_challenge",
                passed=False,
                message="DNS query timed out — is the DNS container running?"
            )
        except FileNotFoundError:
            return ValidationResult(
                name="dns_challenge",
                passed=False,
                message="dig command not found — install dnsutils"
            )
        except Exception as e:
            return ValidationResult(
                name="dns_challenge",
                passed=False,
                message=f"DNS validation failed: {e}"
            )
    
    def _validate_https_challenge(self) -> ValidationResult:
        """Validate that HTTPS challenge server is running."""
        challenges = self.challenge_data.get('challenges', {})
        https = challenges.get('https')
        
        if not https:
            return ValidationResult(
                name="https_challenge",
                passed=False,
                message="No HTTPS challenge in file"
            )
        
        port = https['port']
        endpoint = https['endpoint']
        
        try:
            import urllib.request
            import ssl
            
            # Create context that doesn't verify certificates (self-signed)
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            url = f"https://127.0.0.1:{port}{endpoint}"
            
            with urllib.request.urlopen(url, timeout=5, context=context) as response:
                if response.getcode() == 200:
                    return ValidationResult(
                        name="https_challenge",
                        passed=True,
                        message=f"HTTPS server responding on port {port}",
                        details={'port': port, 'endpoint': endpoint}
                    )
                    
        except Exception as e:
            pass
        
        return ValidationResult(
            name="https_challenge",
            passed=False,
            message=f"HTTPS server not responding on port {port} — start the exercise server"
        )
    
    def _validate_pcap_challenge(self) -> ValidationResult:
        """Validate that PCAP contains the required header."""
        challenges = self.challenge_data.get('challenges', {})
        pcap = challenges.get('pcap')
        
        if not pcap:
            return ValidationResult(
                name="pcap_challenge",
                passed=False,
                message="No PCAP challenge in file"
            )
        
        expected_header = pcap.get('full_header', '')
        
        # Search for PCAP files in artifacts directory
        pcap_files = list(ARTIFACTS_DIR.glob('*.pcap')) + list(ARTIFACTS_DIR.glob('*.pcapng'))
        
        if not pcap_files:
            return ValidationResult(
                name="pcap_challenge",
                passed=False,
                message=f"No PCAP files found in {ARTIFACTS_DIR}"
            )
        
        for pcap_file in pcap_files:
            try:
                result = subprocess.run(
                    ['strings', str(pcap_file)],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if expected_header in result.stdout:
                    return ValidationResult(
                        name="pcap_challenge",
                        passed=True,
                        message=f"Header found in {pcap_file.name}",
                        details={'file': str(pcap_file), 'header': expected_header}
                    )
                    
            except Exception:
                continue
        
        return ValidationResult(
            name="pcap_challenge",
            passed=False,
            message=f"Required header not found in any PCAP file"
        )
    
    def _validate_environment_fingerprint(self) -> ValidationResult:
        """Validate that required Docker containers are running."""
        try:
            result = subprocess.run(
                ['docker', 'ps', '--filter', 'name=week10', '--format', '{{.Names}}'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            running = set(result.stdout.strip().split('\n'))
            running.discard('')  # Remove empty strings
            
            missing = REQUIRED_CONTAINERS - running
            
            if not missing:
                return ValidationResult(
                    name="environment_fingerprint",
                    passed=True,
                    message=f"All {len(REQUIRED_CONTAINERS)} required containers running",
                    details={'running': list(running)}
                )
            else:
                return ValidationResult(
                    name="environment_fingerprint",
                    passed=False,
                    message=f"Missing containers: {', '.join(missing)}"
                )
                
        except FileNotFoundError:
            return ValidationResult(
                name="environment_fingerprint",
                passed=False,
                message="Docker command not found — is Docker installed?"
            )
        except Exception as e:
            return ValidationResult(
                name="environment_fingerprint",
                passed=False,
                message=f"Environment check failed: {e}"
            )
    
    def print_report(self) -> None:
        """Print a formatted validation report."""
        if not self.report:
            print("[ERROR] No validation has been run yet")
            return
        
        status_colour = "\033[92m" if self.report.all_passed else "\033[91m"
        reset = "\033[0m"
        
        print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  SUBMISSION VALIDATION REPORT                                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Student ID:     {self.report.student_id:<59} ║
║  Session:        {self.report.session_token[:32]}...                        ║
║  Validated at:   {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<59} ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  RESULTS:                                                                     ║""")
        
        for result in self.report.results:
            status = "✅" if result.passed else "❌"
            name = result.name[:20].ljust(20)
            msg = result.message[:50]
            print(f"║    {status} {name} {msg:<50} ║")
        
        overall = "PASS" if self.report.all_passed else "FAIL"
        print(f"""╠══════════════════════════════════════════════════════════════════════════════╣
║  OVERALL: {status_colour}{overall}{reset}  ({self.report.passed_count}/{self.report.total_count} checks passed)                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")


# ═══════════════════════════════════════════════════════════════════════════════
# COMMAND_LINE_INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate student submission against anti-AI challenges",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--challenge', '-c',
        type=Path,
        required=True,
        help='Path to the challenge YAML file'
    )
    
    parser.add_argument(
        '--report', '-r',
        type=Path,
        default=None,
        help='Output validation report to JSON file'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Print detailed validation progress'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Only output pass/fail status'
    )
    
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point."""
    args = parse_args(argv)
    
    try:
        validator = SubmissionValidator(args.challenge, verbose=args.verbose)
        
        if args.verbose:
            print("\n[INFO] Running validation checks...\n")
        
        report = validator.validate_all()
        
        if not args.quiet:
            validator.print_report()
        
        if args.report:
            with open(args.report, 'w', encoding='utf-8') as f:
                f.write(report.to_json())
            print(f"[OK] Report saved to: {args.report}")
        
        return 0 if report.all_passed else 1
        
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        return 1
    except ValueError as e:
        print(f"[ERROR] {e}")
        return 1
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
