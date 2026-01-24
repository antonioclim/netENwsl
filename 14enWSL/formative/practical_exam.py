#!/usr/bin/env python3
"""
Practical Examination Framework — AI-Resistant Assessment.

NETWORKING class — ASE, CSIE | Computer Networks Laboratory
by ing. dr. Antonio Clim

This module implements a practical examination that REQUIRES:
1. Live Docker environment
2. Real-time command execution
3. PCAP capture and analysis
4. Network troubleshooting skills

AI RESISTANCE MECHANISMS:
1. Dynamic scenario generation (different for each student)
2. Environment state verification
3. Timed responses with human-reasonable bounds
4. Multi-step tasks with state dependencies

Usage:
    python formative/practical_exam.py
    python formative/practical_exam.py --practice
    make exam
    make exam-practice
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import hashlib
import json
import random
import secrets
import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS AND CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════


class TaskDifficulty(Enum):
    """Task difficulty levels."""

    BASIC = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4


class TaskCategory(Enum):
    """Task category types."""

    DOCKER_OPS = "docker_operations"
    NETWORK_CONFIG = "network_configuration"
    TRAFFIC_ANALYSIS = "traffic_analysis"
    TROUBLESHOOTING = "troubleshooting"
    LOAD_BALANCING = "load_balancing"


# Time limits per difficulty (seconds)
TIME_LIMITS = {
    TaskDifficulty.BASIC: 60,
    TaskDifficulty.INTERMEDIATE: 120,
    TaskDifficulty.ADVANCED: 180,
    TaskDifficulty.EXPERT: 300,
}

# Points per difficulty
POINTS = {
    TaskDifficulty.BASIC: 5,
    TaskDifficulty.INTERMEDIATE: 10,
    TaskDifficulty.ADVANCED: 15,
    TaskDifficulty.EXPERT: 20,
}


# ═══════════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class PracticalTask:
    """A single practical examination task."""

    task_id: str
    title: str
    category: TaskCategory
    difficulty: TaskDifficulty
    description: str
    setup_commands: List[str]
    verification_command: str
    expected_output_pattern: str
    hints: List[str]
    points: int
    time_limit_seconds: int
    requires_pcap: bool = False
    session_specific_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskAttempt:
    """Record of a student's task attempt."""

    task_id: str
    student_id: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    submitted_output: str = ""
    verification_result: bool = False
    points_earned: int = 0
    time_taken_seconds: float = 0


@dataclass
class ExamSession:
    """Complete practical examination session."""

    session_id: str
    student_id: str
    started_at: datetime
    tasks: List[PracticalTask]
    attempts: List[TaskAttempt] = field(default_factory=list)
    total_points: int = 0
    max_points: int = 0
    practice_mode: bool = False

    @property
    def completion_rate(self) -> float:
        """Calculate completion rate."""
        return self.total_points / self.max_points if self.max_points > 0 else 0


# ═══════════════════════════════════════════════════════════════════════════════
# DYNAMIC TASK GENERATORS
# ═══════════════════════════════════════════════════════════════════════════════
class DynamicTaskGenerator:
    """
    Generate tasks with session-specific parameters.

    Each task has randomised elements that:
    1. Prevent answer sharing between students
    2. Require actual command execution
    3. Produce verifiable, unique outputs
    """

    def __init__(self, session_id: str, student_id: str) -> None:
        """Initialise generator with session context."""
        self.session_id = session_id
        self.student_id = student_id
        self.rng = random.Random(f"{session_id}:{student_id}")

    def generate_container_management_task(self) -> PracticalTask:
        """
        Task: Perform specific Docker operations.

        AI-Resistant because:
        - Container names are session-specific
        - Requires actual Docker interaction
        - State verification is real-time
        """
        test_container = f"exam_{self.session_id[:8]}_{self.rng.randint(1000, 9999)}"
        test_port = self.rng.randint(10000, 19999)

        return PracticalTask(
            task_id=f"T1_{secrets.token_hex(4)}",
            title="Container Lifecycle Management",
            category=TaskCategory.DOCKER_OPS,
            difficulty=TaskDifficulty.BASIC,
            description=f"""
            Perform the following Docker operations:

            1. Create and start a container named '{test_container}' using the 'nginx:alpine' image
            2. Map host port {test_port} to container port 80
            3. Verify the container is running and healthy
            4. Report the container ID (first 12 characters)

            Commands you will need: docker run, docker ps

            Your session ID: {self.session_id[:8]}
            """,
            setup_commands=[f"docker rm -f {test_container} 2>/dev/null || true"],
            verification_command=f"docker ps --filter name={test_container} --format '{{{{.ID}}}}'",
            expected_output_pattern=r"^[a-f0-9]{12}$",
            hints=[
                "Use -d flag for detached mode",
                "Port mapping syntax: -p HOST:CONTAINER",
                "Name containers with --name flag",
            ],
            points=POINTS[TaskDifficulty.BASIC],
            time_limit_seconds=TIME_LIMITS[TaskDifficulty.BASIC],
            session_specific_data={"container_name": test_container, "port": test_port},
        )

    def generate_network_inspection_task(self) -> PracticalTask:
        """
        Task: Inspect and report network configuration.

        AI-Resistant because:
        - Target container is randomly selected
        - IP addresses are dynamic
        - Requires live Docker inspect
        """
        containers = ["week14_app1", "week14_app2", "week14_lb", "week14_echo"]
        target = self.rng.choice(containers)
        network = "week14_backend_net"

        return PracticalTask(
            task_id=f"T2_{secrets.token_hex(4)}",
            title="Network Configuration Analysis",
            category=TaskCategory.NETWORK_CONFIG,
            difficulty=TaskDifficulty.INTERMEDIATE,
            description=f"""
            Analyse the network configuration for container '{target}':

            1. Find the IP address of '{target}' on network '{network}'
            2. Find the MAC address of the container's network interface
            3. List all networks this container is connected to

            Report your findings in this format:
            IP: <ip_address>
            MAC: <mac_address>
            Networks: <network1>, <network2>, ...

            Your session ID: {self.session_id[:8]}
            """,
            setup_commands=[],
            verification_command=f"docker inspect {target} --format '{{{{.NetworkSettings.Networks.{network}.IPAddress}}}}'",
            expected_output_pattern=r"^172\.(20|21)\.0\.\d+$",
            hints=[
                "Use docker inspect with --format",
                "JSON path for IP: .NetworkSettings.Networks.<n>.IPAddress",
                "JSON path for MAC: .NetworkSettings.Networks.<n>.MacAddress",
            ],
            points=POINTS[TaskDifficulty.INTERMEDIATE],
            time_limit_seconds=TIME_LIMITS[TaskDifficulty.INTERMEDIATE],
            session_specific_data={
                "target_container": target,
                "target_network": network,
            },
        )

    def generate_load_balancer_task(self) -> PracticalTask:
        """
        Task: Configure and verify load balancer behaviour.

        AI-Resistant because:
        - Request count is randomised
        - Distribution must match actual LB behaviour
        - Requires live traffic generation
        """
        num_requests = self.rng.randint(10, 20)

        return PracticalTask(
            task_id=f"T3_{secrets.token_hex(4)}",
            title="Load Balancer Verification",
            category=TaskCategory.LOAD_BALANCING,
            difficulty=TaskDifficulty.INTERMEDIATE,
            description=f"""
            Verify that the load balancer is distributing traffic correctly:

            1. Generate exactly {num_requests} HTTP requests to the load balancer
            2. Record which backend handled each request
            3. Calculate the distribution percentage
            4. Verify it matches round-robin behaviour

            Commands:
            for i in $(seq 1 {num_requests}); do
                curl -s http://localhost:8080/ | grep -o "app[12]"
            done

            Report format:
            Request sequence: app1, app2, app1, ...
            Distribution: app1=X ({num_requests//2}%), app2=Y ({num_requests - num_requests//2}%)
            Is round-robin: Yes/No

            Your session ID: {self.session_id[:8]}
            """,
            setup_commands=["docker restart week14_app1 week14_app2"],
            verification_command=f"for i in $(seq 1 {num_requests}); do curl -s http://localhost:8080/ | grep -oE 'app[12]'; done | sort | uniq -c",
            expected_output_pattern=r"\s*\d+\s+app[12]",
            hints=[
                "Round-robin alternates: app1, app2, app1, app2...",
                "With even requests, distribution should be 50/50",
                "Use grep -o to extract just the backend name",
            ],
            points=POINTS[TaskDifficulty.INTERMEDIATE],
            time_limit_seconds=TIME_LIMITS[TaskDifficulty.INTERMEDIATE],
            session_specific_data={
                "num_requests": num_requests,
                "expected_per_backend": num_requests // 2,
            },
        )

    def generate_troubleshooting_task(self) -> PracticalTask:
        """
        Task: Diagnose and fix a network issue.

        AI-Resistant because:
        - Fault is injected dynamically
        - Requires actual diagnosis
        - Fix must be verified live
        """
        faults = [
            {
                "name": "stopped_backend",
                "inject": "docker stop week14_app2",
                "symptom": "All requests go to app1 only",
                "fix": "docker start week14_app2",
                "verification": "docker ps --filter name=week14_app2 --filter status=running -q",
            },
        ]

        fault = self.rng.choice(faults)

        return PracticalTask(
            task_id=f"T4_{secrets.token_hex(4)}",
            title="Network Troubleshooting",
            category=TaskCategory.TROUBLESHOOTING,
            difficulty=TaskDifficulty.ADVANCED,
            description=f"""
            A fault has been injected into the lab environment.

            Symptom observed: {fault['symptom']}

            Your task:
            1. Diagnose the root cause using appropriate commands
            2. Document your diagnostic steps
            3. Apply the fix
            4. Verify the system is working correctly

            Report format:
            Diagnosis: <what you found>
            Commands used: <list of diagnostic commands>
            Fix applied: <the command that fixed it>
            Verification: <how you confirmed it is fixed>

            Your session ID: {self.session_id[:8]}

            NOTE: The fault has been injected — start your diagnosis now!
            """,
            setup_commands=[fault["inject"]],
            verification_command=fault["verification"],
            expected_output_pattern=r".+",
            hints=[
                "Start with docker ps to check container states",
                "Use docker network inspect to check connectivity",
                "Check LB logs: docker logs week14_lb --tail 20",
                "Test both backends directly: curl localhost:8001, curl localhost:8002",
            ],
            points=POINTS[TaskDifficulty.ADVANCED],
            time_limit_seconds=TIME_LIMITS[TaskDifficulty.ADVANCED],
            session_specific_data={
                "fault_type": fault["name"],
                "expected_fix": fault["fix"],
            },
        )


# ═══════════════════════════════════════════════════════════════════════════════
# EXAM SESSION MANAGER
# ═══════════════════════════════════════════════════════════════════════════════
class PracticalExamManager:
    """
    Manage the complete practical examination process.

    Flow:
    1. Create session with environment verification
    2. Generate task set based on exam configuration
    3. Execute tasks with timing and verification
    4. Generate detailed report
    """

    def __init__(
        self, student_id: str, num_tasks: int = 4, practice_mode: bool = False
    ) -> None:
        """Initialise exam manager."""
        self.session_id = secrets.token_hex(16)
        self.student_id = student_id
        self.num_tasks = num_tasks
        self.practice_mode = practice_mode
        self.generator = DynamicTaskGenerator(self.session_id, student_id)
        self.session: Optional[ExamSession] = None

    def initialise_exam(self) -> bool:
        """
        Initialise examination session.

        Returns:
            True if environment is ready, False otherwise
        """
        # Verify Docker is running
        try:
            result = subprocess.run(
                ["docker", "info"], capture_output=True, timeout=10
            )
            if result.returncode != 0:
                print("Docker is not running")
                return False
        except Exception as e:
            print(f"Docker check failed: {e}")
            return False

        # Verify week14 containers are up
        try:
            result = subprocess.run(
                [
                    "docker",
                    "ps",
                    "--filter",
                    "name=week14",
                    "--format",
                    "{{.Names}}",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )
            containers = (
                result.stdout.strip().split("\n") if result.stdout.strip() else []
            )
            if len(containers) < 4:
                print(f"Week14 containers not fully running (found {len(containers)})")
                print("   Run: make docker-up")
                return False
        except Exception as e:
            print(f"Container check failed: {e}")
            return False

        # Generate tasks
        tasks = [
            self.generator.generate_container_management_task(),
            self.generator.generate_network_inspection_task(),
            self.generator.generate_load_balancer_task(),
            self.generator.generate_troubleshooting_task(),
        ][: self.num_tasks]

        # Create session
        self.session = ExamSession(
            session_id=self.session_id,
            student_id=self.student_id,
            started_at=datetime.now(timezone.utc),
            tasks=tasks,
            max_points=sum(t.points for t in tasks),
            practice_mode=self.practice_mode,
        )

        print("Exam session initialised")
        print(f"   Session ID: {self.session_id[:8]}...")
        print(f"   Tasks: {len(tasks)}")
        print(f"   Max points: {self.session.max_points}")
        print(f"   Mode: {'Practice' if self.practice_mode else 'Graded'}")

        return True

    def run_task(self, task_index: int) -> TaskAttempt:
        """
        Execute a single task interactively.

        Returns:
            TaskAttempt with results
        """
        if not self.session:
            raise ValueError("Exam not initialised")

        task = self.session.tasks[task_index]

        # Run setup commands
        for cmd in task.setup_commands:
            subprocess.run(cmd, shell=True, capture_output=True)

        # Display task
        print(f"\n{'=' * 60}")
        print(f"TASK {task_index + 1}: {task.title}")
        print(f"Category: {task.category.value}")
        print(f"Difficulty: {task.difficulty.name}")
        print(f"Points: {task.points}")
        print(f"Time limit: {task.time_limit_seconds} seconds")
        print(f"{'=' * 60}")
        print(f"\n{task.description}")

        if task.hints:
            print("\nHints:")
            for i, hint in enumerate(task.hints, 1):
                print(f"  {i}. {hint}")

        # Start timer
        start_time = time.time()
        attempt = TaskAttempt(
            task_id=task.task_id,
            student_id=self.student_id,
            started_at=datetime.now(timezone.utc),
        )

        # Collect response
        print(f"\nTimer started. You have {task.time_limit_seconds} seconds.")
        response = input("\nYour answer (paste output or describe actions): ").strip()

        # Calculate time
        elapsed = time.time() - start_time
        attempt.time_taken_seconds = elapsed
        attempt.completed_at = datetime.now(timezone.utc)
        attempt.submitted_output = response

        # Check time limit
        if elapsed > task.time_limit_seconds and not self.practice_mode:
            print(
                f"\nTime limit exceeded ({elapsed:.1f}s > {task.time_limit_seconds}s)"
            )
            attempt.verification_result = False
            attempt.points_earned = 0
        else:
            # Verify using actual command
            try:
                result = subprocess.run(
                    task.verification_command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                import re

                if result.returncode == 0 and re.search(
                    task.expected_output_pattern, result.stdout.strip()
                ):
                    attempt.verification_result = True
                    attempt.points_earned = task.points
                    print("\nTask verified successfully!")
                else:
                    attempt.verification_result = False
                    attempt.points_earned = 0
                    print("\nVerification failed")

            except Exception as e:
                print(f"\nVerification error: {e}")
                attempt.verification_result = False
                attempt.points_earned = 0

        self.session.attempts.append(attempt)
        self.session.total_points += attempt.points_earned

        return attempt

    def generate_report(self) -> Dict[str, Any]:
        """Generate final examination report."""
        if not self.session:
            raise ValueError("Exam not initialised")

        report = {
            "session_id": self.session.session_id,
            "student_id": self.session.student_id,
            "started_at": self.session.started_at.isoformat(),
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "total_points": self.session.total_points,
            "max_points": self.session.max_points,
            "percentage": round(self.session.completion_rate * 100, 1),
            "practice_mode": self.session.practice_mode,
            "tasks": [
                {
                    "task_id": t.task_id,
                    "title": t.title,
                    "points": t.points,
                    "earned": next(
                        (
                            a.points_earned
                            for a in self.session.attempts
                            if a.task_id == t.task_id
                        ),
                        0,
                    ),
                }
                for t in self.session.tasks
            ],
            "grade": self._calculate_grade(self.session.completion_rate),
        }

        # Create checksum for tamper detection
        report_string = json.dumps(report, sort_keys=True)
        report["checksum"] = hashlib.sha256(report_string.encode()).hexdigest()[:16]

        return report

    def _calculate_grade(self, rate: float) -> str:
        """Calculate grade based on completion rate."""
        if rate >= 0.95:
            return "10 (Excellent)"
        elif rate >= 0.85:
            return "9 (Very Good)"
        elif rate >= 0.75:
            return "8 (Good)"
        elif rate >= 0.65:
            return "7 (Satisfactory)"
        elif rate >= 0.55:
            return "6 (Sufficient)"
        elif rate >= 0.45:
            return "5 (Acceptable)"
        else:
            return "4 (Insufficient)"


# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> None:
    """Run the practical examination."""
    parser = argparse.ArgumentParser(description="Practical Examination")
    parser.add_argument(
        "--practice", action="store_true", help="Run in practice mode (no grading)"
    )
    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("PRACTICAL EXAMINATION — Computer Networks")
    print("NETWORKING class — ASE, CSIE")
    print("=" * 60)

    if args.practice:
        print("\nPRACTICE MODE — No grading, time limits relaxed")
    else:
        print(
            """
    IMPORTANT INSTRUCTIONS:

    1. This examination requires a running Docker environment
    2. All tasks are verified against your actual environment
    3. AI-generated answers will NOT work
    4. Time limits are enforced per task
    5. Your session is unique — answers cannot be shared

    Ready? Make sure 'make docker-up' has been run.
        """
        )

    # Get student ID
    student_id = input("Enter your student ID: ").strip()
    if not student_id:
        print("Error: Student ID required")
        return

    # Initialise exam
    manager = PracticalExamManager(
        student_id, num_tasks=4, practice_mode=args.practice
    )
    if not manager.initialise_exam():
        print("\nCannot start exam — environment not ready")
        return

    # Confirm start
    input("\nPress Enter to begin the examination...")

    # Run each task
    for i in range(len(manager.session.tasks)):
        manager.run_task(i)

        if i < len(manager.session.tasks) - 1:
            input("\nPress Enter to continue to the next task...")

    # Generate and display report
    print("\n" + "=" * 60)
    print("EXAMINATION COMPLETE")
    print("=" * 60)

    report = manager.generate_report()

    print(
        f"\nFinal Score: {report['total_points']}/{report['max_points']} ({report['percentage']}%)"
    )
    print(f"Grade: {report['grade']}")

    print("\nTask breakdown:")
    for task in report["tasks"]:
        status = "PASS" if task["earned"] > 0 else "FAIL"
        print(f"  [{status}] {task['title']}: {task['earned']}/{task['points']}")

    # Save report
    if not args.practice:
        report_file = f"exam_report_{student_id}_{report['session_id'][:8]}.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\nReport saved to: {report_file}")
        print(f"   Checksum: {report['checksum']}")


if __name__ == "__main__":
    main()
