#!/usr/bin/env python3
"""
Tests for Anti-Cheat System
===========================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Unit tests for the challenge generator, submission validator
and environment fingerprinting modules.

Run with: pytest tests/test_anti_cheat.py -v
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import yaml
except ImportError:
    pytest.skip("PyYAML not installed", allow_module_level=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_FIXTURES
# ═══════════════════════════════════════════════════════════════════════════════
@pytest.fixture
def sample_student_id() -> str:
    """Sample student ID for testing."""
    return "TEST123"


@pytest.fixture
def challenge_output_dir(tmp_path: Path) -> Path:
    """Temporary directory for challenge outputs."""
    return tmp_path / "challenges"


@pytest.fixture
def valid_challenge_file(tmp_path: Path) -> Path:
    """Create a valid challenge file for testing."""
    challenge_data = {
        'metadata': {
            'student_id': 'TEST123',
            'session_token': 'abcdef1234567890' * 2,
            'generated_at': datetime.now().isoformat(),
            'valid_hours': 4,
            'verification_hash': ''  # Will be computed
        },
        'challenges': {
            'dns': {
                'domain': 'verify-abcdef12.lab.local',
                'expected_txt': 'proof-TEST123-abcdef123456',
                'port': 5353,
                'type': 'TXT'
            },
            'https': {
                'port': 8542,
                'endpoint': '/verify/abcdef1234567890',
                'expected_response': {'status': 'verified'}
            },
            'pcap': {
                'header_name': 'X-Student-Verify',
                'header_value': 'TEST123-abcdef123456',
                'full_header': 'X-Student-Verify: TEST123-abcdef123456'
            }
        }
    }
    
    # Compute verification hash
    import hashlib
    data = f"{challenge_data['metadata']['student_id']}:{challenge_data['metadata']['session_token']}:{challenge_data['metadata']['generated_at']}"
    challenge_data['metadata']['verification_hash'] = hashlib.sha256(data.encode()).hexdigest()[:16]
    
    path = tmp_path / "test_challenge.yaml"
    with open(path, 'w') as f:
        yaml.dump(challenge_data, f)
    
    return path


@pytest.fixture
def expired_challenge_file(tmp_path: Path) -> Path:
    """Create an expired challenge file for testing."""
    challenge_data = {
        'metadata': {
            'student_id': 'TEST123',
            'session_token': 'expired12345678' * 2,
            'generated_at': (datetime.now() - timedelta(hours=5)).isoformat(),
            'valid_hours': 4,
            'verification_hash': 'dummy'
        },
        'challenges': {}
    }
    
    path = tmp_path / "expired_challenge.yaml"
    with open(path, 'w') as f:
        yaml.dump(challenge_data, f)
    
    return path


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_SESSION_CHALLENGE
# ═══════════════════════════════════════════════════════════════════════════════
class TestSessionChallenge:
    """Tests for SessionChallenge class."""
    
    def test_import(self) -> None:
        """Test that the module can be imported."""
        try:
            from anti_cheat.challenge_generator import SessionChallenge
            assert SessionChallenge is not None
        except ImportError:
            pytest.skip("anti_cheat module not available")
    
    def test_session_creation(self, sample_student_id: str) -> None:
        """Test basic session creation."""
        try:
            from anti_cheat.challenge_generator import SessionChallenge
        except ImportError:
            pytest.skip("anti_cheat module not available")
        
        session = SessionChallenge(student_id=sample_student_id)
        
        assert session.student_id == sample_student_id
        assert len(session.session_token) == 32  # 16 bytes = 32 hex chars
        assert session.timestamp is not None
    
    def test_session_uniqueness(self, sample_student_id: str) -> None:
        """Test that two sessions have different tokens."""
        try:
            from anti_cheat.challenge_generator import SessionChallenge
        except ImportError:
            pytest.skip("anti_cheat module not available")
        
        session1 = SessionChallenge(student_id=sample_student_id)
        session2 = SessionChallenge(student_id=sample_student_id)
        
        assert session1.session_token != session2.session_token
    
    def test_invalid_student_id(self) -> None:
        """Test that invalid student IDs are rejected."""
        try:
            from anti_cheat.challenge_generator import SessionChallenge
        except ImportError:
            pytest.skip("anti_cheat module not available")
        
        with pytest.raises(ValueError):
            SessionChallenge(student_id="AB")  # Too short
        
        with pytest.raises(ValueError):
            SessionChallenge(student_id="")  # Empty
    
    def test_student_id_sanitisation(self) -> None:
        """Test that student IDs are sanitised."""
        try:
            from anti_cheat.challenge_generator import SessionChallenge
        except ImportError:
            pytest.skip("anti_cheat module not available")
        
        session = SessionChallenge(student_id="Test@Student#123!")
        
        # Should only contain alphanumeric and -_
        assert "@" not in session.student_id
        assert "#" not in session.student_id
        assert "!" not in session.student_id
    
    def test_dns_challenge_generation(self, sample_student_id: str) -> None:
        """Test DNS challenge generation."""
        try:
            from anti_cheat.challenge_generator import SessionChallenge
        except ImportError:
            pytest.skip("anti_cheat module not available")
        
        session = SessionChallenge(student_id=sample_student_id)
        challenge = session.generate_dns_challenge()
        
        assert challenge.domain.endswith('.lab.local')
        assert sample_student_id in challenge.expected_txt
        assert 'dns' in session.challenges
    
    def test_https_challenge_port_range(self, sample_student_id: str) -> None:
        """Test HTTPS challenge port is in valid range."""
        try:
            from anti_cheat.challenge_generator import SessionChallenge
        except ImportError:
            pytest.skip("anti_cheat module not available")
        
        session = SessionChallenge(student_id=sample_student_id)
        challenge = session.generate_https_challenge()
        
        assert 8500 <= challenge.port < 8600
        assert challenge.endpoint.startswith('/verify/')
    
    def test_all_challenges_generation(self, sample_student_id: str) -> None:
        """Test generation of all challenges."""
        try:
            from anti_cheat.challenge_generator import SessionChallenge
        except ImportError:
            pytest.skip("anti_cheat module not available")
        
        session = SessionChallenge(student_id=sample_student_id)
        challenges = session.generate_all_challenges()
        
        assert 'dns' in challenges
        assert 'https' in challenges
        assert 'ftp' in challenges
        assert 'pcap' in challenges
    
    def test_verification_hash(self, sample_student_id: str) -> None:
        """Test verification hash computation."""
        try:
            from anti_cheat.challenge_generator import SessionChallenge
        except ImportError:
            pytest.skip("anti_cheat module not available")
        
        session = SessionChallenge(student_id=sample_student_id)
        hash1 = session.compute_verification_hash()
        hash2 = session.compute_verification_hash()
        
        assert hash1 == hash2  # Should be deterministic
        assert len(hash1) == 16  # 16 hex chars
    
    def test_yaml_export(self, sample_student_id: str, tmp_path: Path) -> None:
        """Test export to YAML file."""
        try:
            from anti_cheat.challenge_generator import SessionChallenge
        except ImportError:
            pytest.skip("anti_cheat module not available")
        
        session = SessionChallenge(student_id=sample_student_id)
        session.generate_all_challenges()
        
        output_path = tmp_path / "challenge.yaml"
        session.export_to_yaml(output_path)
        
        assert output_path.exists()
        
        # Verify it's valid YAML
        with open(output_path) as f:
            data = yaml.safe_load(f)
        
        assert 'metadata' in data
        assert 'challenges' in data
        assert data['metadata']['student_id'] == sample_student_id


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_SUBMISSION_VALIDATOR
# ═══════════════════════════════════════════════════════════════════════════════
class TestSubmissionValidator:
    """Tests for SubmissionValidator class."""
    
    def test_import(self) -> None:
        """Test that the module can be imported."""
        try:
            from anti_cheat.submission_validator import SubmissionValidator
            assert SubmissionValidator is not None
        except ImportError:
            pytest.skip("anti_cheat module not available")
    
    def test_validator_creation(self, valid_challenge_file: Path) -> None:
        """Test validator creation with valid file."""
        try:
            from anti_cheat.submission_validator import SubmissionValidator
        except ImportError:
            pytest.skip("anti_cheat module not available")
        
        validator = SubmissionValidator(valid_challenge_file)
        assert validator.challenge_data is not None
    
    def test_invalid_file_path(self, tmp_path: Path) -> None:
        """Test error handling for missing file."""
        try:
            from anti_cheat.submission_validator import SubmissionValidator
        except ImportError:
            pytest.skip("anti_cheat module not available")
        
        with pytest.raises(FileNotFoundError):
            SubmissionValidator(tmp_path / "nonexistent.yaml")
    
    def test_timestamp_validation_valid(self, valid_challenge_file: Path) -> None:
        """Test timestamp validation with recent challenge."""
        try:
            from anti_cheat.submission_validator import SubmissionValidator
        except ImportError:
            pytest.skip("anti_cheat module not available")
        
        validator = SubmissionValidator(valid_challenge_file)
        result = validator._validate_timestamp()
        
        assert result.passed is True
        assert "Valid" in result.message
    
    def test_timestamp_validation_expired(self, expired_challenge_file: Path) -> None:
        """Test timestamp validation with expired challenge."""
        try:
            from anti_cheat.submission_validator import SubmissionValidator
        except ImportError:
            pytest.skip("anti_cheat module not available")
        
        validator = SubmissionValidator(expired_challenge_file)
        result = validator._validate_timestamp()
        
        assert result.passed is False
        assert "expired" in result.message.lower()
    
    def test_validation_report_structure(self, valid_challenge_file: Path) -> None:
        """Test that validation report has correct structure."""
        try:
            from anti_cheat.submission_validator import SubmissionValidator
        except ImportError:
            pytest.skip("anti_cheat module not available")
        
        validator = SubmissionValidator(valid_challenge_file)
        report = validator.validate_all()
        
        assert report.student_id == "TEST123"
        assert len(report.results) > 0
        assert hasattr(report, 'passed_count')
        assert hasattr(report, 'failed_count')
    
    def test_report_json_export(self, valid_challenge_file: Path) -> None:
        """Test report JSON export."""
        try:
            from anti_cheat.submission_validator import SubmissionValidator
        except ImportError:
            pytest.skip("anti_cheat module not available")
        
        validator = SubmissionValidator(valid_challenge_file)
        report = validator.validate_all()
        
        json_str = report.to_json()
        data = json.loads(json_str)
        
        assert 'summary' in data
        assert 'results' in data
        assert data['summary']['total'] > 0


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_FINGERPRINT
# ═══════════════════════════════════════════════════════════════════════════════
class TestFingerprint:
    """Tests for fingerprint module."""
    
    def test_import(self) -> None:
        """Test that the module can be imported."""
        try:
            from anti_cheat.fingerprint import get_environment_fingerprint
            assert get_environment_fingerprint is not None
        except ImportError:
            pytest.skip("anti_cheat module not available")
    
    def test_fingerprint_generation(self) -> None:
        """Test basic fingerprint generation."""
        try:
            from anti_cheat.fingerprint import get_environment_fingerprint
        except ImportError:
            pytest.skip("anti_cheat module not available")
        
        fp = get_environment_fingerprint()
        
        assert fp.username is not None
        assert fp.hostname is not None
        assert fp.date is not None
        assert len(fp.fingerprint_hash) == 12
    
    def test_fingerprint_consistency(self) -> None:
        """Test that fingerprints are consistent within same session."""
        try:
            from anti_cheat.fingerprint import get_environment_fingerprint
        except ImportError:
            pytest.skip("anti_cheat module not available")
        
        fp1 = get_environment_fingerprint()
        fp2 = get_environment_fingerprint()
        
        # Same date means same hash (process ID might differ)
        assert fp1.date == fp2.date
        assert fp1.hostname == fp2.hostname
    
    def test_dynamic_port_calculation(self) -> None:
        """Test dynamic port calculation."""
        try:
            from anti_cheat.fingerprint import get_dynamic_port
        except ImportError:
            pytest.skip("anti_cheat module not available")
        
        port = get_dynamic_port(8000)
        
        assert 8000 <= port < 8100
    
    def test_unique_header_generation(self) -> None:
        """Test unique header generation."""
        try:
            from anti_cheat.fingerprint import get_unique_header
        except ImportError:
            pytest.skip("anti_cheat module not available")
        
        header = get_unique_header()
        
        assert header.startswith("X-Lab-Verify:")
        assert len(header) > 15
    
    def test_session_proof_generation(self) -> None:
        """Test session proof generation."""
        try:
            from anti_cheat.fingerprint import generate_session_proof
        except ImportError:
            pytest.skip("anti_cheat module not available")
        
        proof = generate_session_proof()
        
        assert "SESSION PROOF" in proof
        assert "Timestamp:" in proof
        assert "Proof Hash:" in proof


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════════
class TestIntegration:
    """Integration tests for the complete anti-cheat workflow."""
    
    def test_full_challenge_workflow(self, tmp_path: Path) -> None:
        """Test complete challenge generation and validation workflow."""
        try:
            from anti_cheat.challenge_generator import SessionChallenge
            from anti_cheat.submission_validator import SubmissionValidator
        except ImportError:
            pytest.skip("anti_cheat module not available")
        
        # Generate challenge
        session = SessionChallenge(student_id="INTEGRATION_TEST")
        session.generate_all_challenges()
        
        challenge_path = tmp_path / "challenge.yaml"
        session.export_to_yaml(challenge_path)
        
        # Validate (will fail DNS/HTTPS checks without lab, but structure should work)
        validator = SubmissionValidator(challenge_path)
        report = validator.validate_all()
        
        # Timestamp and hash integrity should pass
        timestamp_result = next(
            (r for r in report.results if r.name == "timestamp"),
            None
        )
        hash_result = next(
            (r for r in report.results if r.name == "hash_integrity"),
            None
        )
        
        assert timestamp_result is not None
        assert timestamp_result.passed is True
        
        assert hash_result is not None
        assert hash_result.passed is True


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
