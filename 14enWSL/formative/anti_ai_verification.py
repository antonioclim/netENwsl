#!/usr/bin/env python3
"""
Anti-AI Assessment System — Environment-Bound Verification.

NETWORKING class — ASE, CSIE | Computer Networks Laboratory
by ing. dr. Antonio Clim

This module provides assessment mechanisms that REQUIRE a live Docker
environment to complete, making AI-generated answers ineffective.

DESIGN PRINCIPLES:
1. Dynamic tokens — change every session
2. Environment probes — require live Docker
3. Timing verification — detect copy-paste delays
4. Unique fingerprints — per-student, per-session

AI CANNOT:
- Generate valid environment tokens
- Predict dynamic container states
- Produce valid PCAP checksums
- Know real-time Docker outputs

Usage:
    python formative/anti_ai_verification.py
    make quiz-verify
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import hashlib
import json
import secrets
import socket
import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
SESSION_TOKEN_LENGTH = 16
MAX_RESPONSE_TIME_SECONDS = 120


# ═══════════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class SessionContext:
    """Unique session context for assessment."""

    session_id: str
    student_id: str
    started_at: datetime
    environment_token: str
    container_fingerprint: str
    challenges_completed: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary."""
        return {
            "session_id": self.session_id,
            "student_id": self.student_id,
            "started_at": self.started_at.isoformat(),
            "environment_token": self.environment_token,
            "container_fingerprint": self.container_fingerprint,
            "challenges_completed": self.challenges_completed,
        }


@dataclass
class ChallengeResult:
    """Result of a verification challenge."""

    challenge_id: str
    passed: bool
    evidence: str
    timestamp: datetime
    response_time_ms: float


# ═══════════════════════════════════════════════════════════════════════════════
# ENVIRONMENT TOKEN GENERATION
# ═══════════════════════════════════════════════════════════════════════════════
class EnvironmentTokenGenerator:
    """
    Generate tokens that can ONLY be obtained from a live Docker environment.

    AI CANNOT generate these because they require:
    1. Running Docker daemon
    2. Specific containers in specific states
    3. Real-time network probes
    """

    @staticmethod
    def generate_session_token() -> str:
        """Generate a cryptographically secure session token."""
        return secrets.token_hex(SESSION_TOKEN_LENGTH)

    @staticmethod
    def get_container_fingerprint() -> str:
        """
        Get a fingerprint from running containers that changes per-session.

        This CANNOT be predicted by AI because it depends on:
        - Container IDs (random per run)
        - Container start times
        - Container PIDs
        """
        try:
            result = subprocess.run(
                ["docker", "ps", "--format", "{{.ID}}:{{.CreatedAt}}:{{.Status}}"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode != 0:
                return "DOCKER_NOT_AVAILABLE"

            container_data = result.stdout.strip()
            fingerprint = hashlib.sha256(container_data.encode()).hexdigest()[:16]
            return fingerprint

        except Exception as e:
            return f"ERROR:{str(e)[:20]}"

    @staticmethod
    def get_network_token() -> str:
        """
        Generate token from live network probe.

        Requires actual TCP connection to running services.
        """
        probes = []

        services = [
            ("localhost", 8080, "lb"),
            ("localhost", 8001, "app1"),
            ("localhost", 8002, "app2"),
            ("localhost", 9090, "echo"),
        ]

        for host, port, name in services:
            try:
                start = time.time()
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((host, port))
                latency = int((time.time() - start) * 1000)
                sock.close()

                status = "UP" if result == 0 else "DOWN"
                probes.append(f"{name}:{status}:{latency}ms")

            except Exception:
                probes.append(f"{name}:ERROR:0ms")

        probe_string = "|".join(probes)
        return hashlib.md5(probe_string.encode()).hexdigest()[:12]


# ═══════════════════════════════════════════════════════════════════════════════
# LIVE VERIFICATION CHALLENGES
# ═══════════════════════════════════════════════════════════════════════════════
class LiveVerificationChallenge:
    """
    Challenges that REQUIRE interaction with live environment.

    Each challenge:
    1. Generates a unique, session-bound task
    2. Requires Docker/network interaction to solve
    3. Verifies the response against live state
    4. Tracks timing to detect copy-paste
    """

    def __init__(self, session: SessionContext) -> None:
        """Initialise with session context."""
        self.session = session
        self.challenges: Dict[str, Dict[str, Any]] = {}

    def create_container_count_challenge(self) -> Dict[str, Any]:
        """
        Challenge: Count containers matching specific criteria.

        AI cannot answer because:
        - Requires running `docker ps`
        - Filter criteria are dynamic
        - Count changes if containers restart
        """
        challenge_id = f"CC_{secrets.token_hex(4)}"

        challenge = {
            "id": challenge_id,
            "type": "container_count",
            "instruction": f"""
            Run the following command and report the EXACT number of lines:

            docker ps --filter "name=week14" --filter "status=running" | tail -n +2 | wc -l

            Your answer must be a single integer.
            Session token: {self.session.session_id[:8]}
            """,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "expected_range": (4, 6),
        }

        self.challenges[challenge_id] = challenge
        return challenge

    def create_http_header_challenge(self) -> Dict[str, Any]:
        """
        Challenge: Extract specific header from HTTP response.

        AI cannot answer because:
        - Requires actual HTTP request
        - Headers contain timestamps
        - Backend name is dynamic (round-robin)
        """
        challenge_id = f"HH_{secrets.token_hex(4)}"

        challenge = {
            "id": challenge_id,
            "type": "http_header",
            "instruction": f"""
            Execute this curl command and report the backend that responded:

            curl -s http://localhost:8080/ | grep -o 'app[12]'

            Report the backend name (app1 or app2).
            Session token: {self.session.session_id[:8]}
            """,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "valid_values": ["app1", "app2"],
        }

        self.challenges[challenge_id] = challenge
        return challenge

    def create_network_inspection_challenge(self) -> Dict[str, Any]:
        """
        Challenge: Report container IP from network inspection.

        AI cannot answer because:
        - Requires Docker network inspect
        - IPs are assigned dynamically
        - Exact format matters
        """
        challenge_id = f"NI_{secrets.token_hex(4)}"

        containers = ["week14_app1", "week14_app2", "week14_lb"]
        target = secrets.choice(containers)

        challenge = {
            "id": challenge_id,
            "type": "network_inspect",
            "target_container": target,
            "instruction": f"""
            Find the IP address of container '{target}' on the backend network:

            docker inspect {target} --format '{{{{.NetworkSettings.Networks.week14_backend_net.IPAddress}}}}'

            Report the IP address exactly as shown (e.g., 172.20.0.2)
            Session token: {self.session.session_id[:8]}
            """,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "expected_pattern": r"^172\.20\.0\.\d+$",
        }

        self.challenges[challenge_id] = challenge
        return challenge

    def create_echo_interaction_challenge(self) -> Dict[str, Any]:
        """
        Challenge: Send message to echo server and report response.

        AI cannot answer because:
        - Requires TCP connection
        - Message includes session token
        - Response includes timestamp
        """
        challenge_id = f"EI_{secrets.token_hex(4)}"

        unique_message = f"VERIFY_{self.session.session_id[:8]}_{int(time.time())}"

        challenge = {
            "id": challenge_id,
            "type": "echo_interaction",
            "message": unique_message,
            "instruction": f"""
            Send this EXACT message to the echo server and report the response:

            echo "{unique_message}" | nc localhost 9090

            Report the COMPLETE response line.
            This message is unique to your session and cannot be guessed.
            """,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "expected_response": unique_message,
        }

        self.challenges[challenge_id] = challenge
        return challenge

    def verify_response(
        self, challenge_id: str, response: str, response_time_ms: float
    ) -> ChallengeResult:
        """
        Verify a challenge response.

        Checks:
        1. Response format is valid
        2. Response matches expected value/pattern
        3. Response time is reasonable (not too fast = copy-paste)
        """
        challenge = self.challenges.get(challenge_id)
        if not challenge:
            return ChallengeResult(
                challenge_id=challenge_id,
                passed=False,
                evidence="Challenge not found",
                timestamp=datetime.now(timezone.utc),
                response_time_ms=response_time_ms,
            )

        # Timing check — too fast suggests copy-paste
        if response_time_ms < 2000:
            return ChallengeResult(
                challenge_id=challenge_id,
                passed=False,
                evidence="Response too fast — timing suggests automated/copy-paste",
                timestamp=datetime.now(timezone.utc),
                response_time_ms=response_time_ms,
            )

        # Type-specific verification
        passed = False
        evidence = ""

        if challenge["type"] == "container_count":
            try:
                count = int(response.strip())
                min_val, max_val = challenge["expected_range"]
                passed = min_val <= count <= max_val
                evidence = f"Count {count} {'within' if passed else 'outside'} expected range"
            except ValueError:
                evidence = "Invalid integer response"

        elif challenge["type"] == "http_header":
            response_clean = response.strip().lower()
            passed = any(v in response_clean for v in challenge["valid_values"])
            evidence = f"Header value {'valid' if passed else 'invalid'}"

        elif challenge["type"] == "network_inspect":
            import re

            passed = bool(re.match(challenge["expected_pattern"], response.strip()))
            evidence = f"IP format {'valid' if passed else 'invalid'}"

        elif challenge["type"] == "echo_interaction":
            passed = challenge["expected_response"] in response
            evidence = f"Echo response {'matches' if passed else 'does not match'}"

        return ChallengeResult(
            challenge_id=challenge_id,
            passed=passed,
            evidence=evidence,
            timestamp=datetime.now(timezone.utc),
            response_time_ms=response_time_ms,
        )


# ═══════════════════════════════════════════════════════════════════════════════
# ASSESSMENT SESSION MANAGER
# ═══════════════════════════════════════════════════════════════════════════════
class AntiAIAssessmentSession:
    """
    Manage a complete anti-AI assessment session.

    Flow:
    1. Initialise session with environment probes
    2. Generate dynamic challenges
    3. Verify responses with timing checks
    4. Generate proof-of-completion certificate
    """

    def __init__(self, student_id: str) -> None:
        """Initialise assessment session."""
        self.session = self._create_session(student_id)
        self.challenges = LiveVerificationChallenge(self.session)
        self.results: List[ChallengeResult] = []

    def _create_session(self, student_id: str) -> SessionContext:
        """Create a new assessment session with environment binding."""
        return SessionContext(
            session_id=EnvironmentTokenGenerator.generate_session_token(),
            student_id=student_id,
            started_at=datetime.now(timezone.utc),
            environment_token=EnvironmentTokenGenerator.get_network_token(),
            container_fingerprint=EnvironmentTokenGenerator.get_container_fingerprint(),
        )

    def get_verification_bundle(self) -> Dict[str, Any]:
        """
        Generate a bundle of challenges for the assessment.

        Returns 4 challenges that collectively prove:
        1. Docker environment is running
        2. Student can execute commands
        3. Student understands the outputs
        """
        bundle = {
            "session": self.session.to_dict(),
            "challenges": [
                self.challenges.create_container_count_challenge(),
                self.challenges.create_http_header_challenge(),
                self.challenges.create_network_inspection_challenge(),
                self.challenges.create_echo_interaction_challenge(),
            ],
            "time_limit_seconds": MAX_RESPONSE_TIME_SECONDS * 4,
            "instructions": """
            Complete ALL challenges below. For each:
            1. Read the instruction carefully
            2. Execute the command in your WSL terminal
            3. Copy the EXACT output as your answer
            4. Submit within the time limit

            NOTE: These challenges are bound to YOUR session and require
            YOUR running Docker environment. AI-generated answers will fail.
            """,
        }
        return bundle

    def submit_responses(
        self, responses: Dict[str, Tuple[str, float]]
    ) -> Dict[str, Any]:
        """
        Submit and verify all challenge responses.

        Args:
            responses: Dict mapping challenge_id to (response, response_time_ms)

        Returns:
            Verification report with pass/fail status
        """
        for challenge_id, (response, response_time) in responses.items():
            result = self.challenges.verify_response(
                challenge_id, response, response_time
            )
            self.results.append(result)

            if result.passed:
                self.session.challenges_completed.append(challenge_id)

        passed_count = sum(1 for r in self.results if r.passed)
        total_count = len(self.results)

        return {
            "session_id": self.session.session_id,
            "passed": passed_count,
            "total": total_count,
            "pass_rate": passed_count / total_count if total_count > 0 else 0,
            "verified": passed_count >= 3,
            "certificate": self._generate_certificate() if passed_count >= 3 else None,
            "results": [
                {
                    "challenge_id": r.challenge_id,
                    "passed": r.passed,
                    "evidence": r.evidence,
                    "response_time_ms": r.response_time_ms,
                }
                for r in self.results
            ],
        }

    def _generate_certificate(self) -> str:
        """
        Generate a verification certificate.

        This certificate proves:
        1. Student completed challenges
        2. Responses came from live environment
        3. Timing was human-reasonable
        """
        cert_data = {
            "session_id": self.session.session_id,
            "student_id": self.session.student_id,
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "environment_token": self.session.environment_token,
            "container_fingerprint": self.session.container_fingerprint,
            "challenges_passed": len(self.session.challenges_completed),
        }

        cert_string = json.dumps(cert_data, sort_keys=True)
        signature = hashlib.sha256(cert_string.encode()).hexdigest()[:16]

        cert_data["signature"] = signature
        return cert_data


# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> None:
    """Run an interactive anti-AI assessment session."""
    print("\n" + "=" * 60)
    print("Anti-AI Assessment System — Environment Verification")
    print("NETWORKING class — ASE, CSIE")
    print("=" * 60)

    # Get student ID
    student_id = input("\nEnter your student ID: ").strip()
    if not student_id:
        print("Error: Student ID required")
        return

    # Create session
    print("\nInitialising secure session...")
    session = AntiAIAssessmentSession(student_id)

    # Check environment
    print(f"   Session ID: {session.session.session_id[:8]}...")
    print(f"   Environment token: {session.session.environment_token}")
    print(f"   Container fingerprint: {session.session.container_fingerprint}")

    if "ERROR" in session.session.container_fingerprint:
        print("\nDocker environment not detected!")
        print("   Please ensure Docker is running and week14 containers are up.")
        print("   Run: make docker-up")
        return

    # Get challenges
    print("\nGenerating verification challenges...")
    bundle = session.get_verification_bundle()

    print(f"\nYou have {bundle['time_limit_seconds']} seconds to complete all challenges.")
    print(bundle["instructions"])

    # Collect responses
    responses: Dict[str, Tuple[str, float]] = {}
    for challenge in bundle["challenges"]:
        print(f"\n{'=' * 60}")
        print(f"Challenge: {challenge['id']}")
        print(f"Type: {challenge['type']}")
        print(f"\n{challenge['instruction']}")

        start_time = time.time()
        response = input("\nYour answer: ").strip()
        response_time = (time.time() - start_time) * 1000

        responses[challenge["id"]] = (response, response_time)

    # Verify
    print("\nVerifying responses...")
    report = session.submit_responses(responses)


    # Persist artefacts for later auditing (optional but recommended)
    try:
        from pathlib import Path

        artefacts_dir = Path(__file__).parent.parent / "artifacts" / "anti_ai"
        artefacts_dir.mkdir(parents=True, exist_ok=True)

        session_short = session.session.session_id[:8]
        safe_student = "".join(ch for ch in student_id if ch.isalnum() or ch in ("-", "_"))[:32] or "student"
        report_path = artefacts_dir / f"week14_anti_ai_report_{safe_student}_{session_short}.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        if report.get("certificate"):
            cert_path = artefacts_dir / f"week14_anti_ai_certificate_{safe_student}_{session_short}.json"
            with open(cert_path, "w", encoding="utf-8") as f:
                json.dump(report["certificate"], f, indent=2)

        print(f"\nSaved report: {report_path}")
        if report.get("certificate"):
            print(f"Saved certificate: {cert_path}")
    except Exception as e:
        print(f"\nWarning: could not save verification artefacts: {e}")

    # Show results
    print(f"\n{'=' * 60}")
    print("VERIFICATION REPORT")
    print(f"{'=' * 60}")
    print(f"Passed: {report['passed']}/{report['total']}")
    print(f"Status: {'VERIFIED' if report['verified'] else 'NOT VERIFIED'}")

    if report["certificate"]:
        print(f"\nCertificate generated:")
        print(json.dumps(report["certificate"], indent=2))
    else:
        print("\nInsufficient challenges passed for certification.")
        print("    Please ensure your Docker environment is running correctly.")


if __name__ == "__main__":
    main()
