#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  Expected Outputs — Week 3 Network Programming                               ║
║  NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

DESCRIPTION:
    Executable expected outputs for automated test verification.
    Each entry defines a command, expected output patterns and exit codes.

USAGE:
    from tests.expected_outputs import EXPECTED_OUTPUTS
    
    for test_name, spec in EXPECTED_OUTPUTS.items():
        result = run_command(spec['command'])
        assert spec['exit_code'] == result.returncode
        for pattern in spec['contains']:
            assert pattern in result.stdout
"""
from __future__ import annotations

from typing import TypedDict


class OutputSpec(TypedDict, total=False):
    """Specification for expected output."""
    command: str
    description: str
    contains: list[str]
    not_contains: list[str]
    exit_code: int
    timeout_seconds: int
    requires_docker: bool


# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 1: UDP Broadcast
# ═══════════════════════════════════════════════════════════════════════════════

BROADCAST_OUTPUTS: dict[str, OutputSpec] = {
    "broadcast_sender_single": {
        "command": "python src/exercises/ex_3_01_udp_broadcast.py send --count 1 --no-predict",
        "description": "Send single broadcast message",
        "contains": [
            "SEND",
            "bytes",
            "255.255.255.255:5007"
        ],
        "not_contains": [
            "ERROR",
            "Traceback"
        ],
        "exit_code": 0,
        "timeout_seconds": 10,
        "requires_docker": True
    },
    
    "broadcast_sender_multiple": {
        "command": "python src/exercises/ex_3_01_udp_broadcast.py send --count 5 --interval 0.1 --no-predict",
        "description": "Send multiple broadcast messages",
        "contains": [
            "SEND",
            "[1/5]",
            "[5/5]"
        ],
        "exit_code": 0,
        "timeout_seconds": 15,
        "requires_docker": True
    },
    
    "broadcast_receiver_start": {
        "command": "timeout 3 python src/exercises/ex_3_01_udp_broadcast.py recv --no-predict || true",
        "description": "Start broadcast receiver (timeout expected)",
        "contains": [
            "Listening",
            "5007"
        ],
        "exit_code": 0,  # timeout returns non-zero but we catch with || true
        "timeout_seconds": 5,
        "requires_docker": True
    },
    
    "broadcast_help": {
        "command": "python src/exercises/ex_3_01_udp_broadcast.py --help",
        "description": "Show help message",
        "contains": [
            "usage:",
            "send",
            "recv",
            "--count"
        ],
        "exit_code": 0,
        "requires_docker": False
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 2: UDP Multicast
# ═══════════════════════════════════════════════════════════════════════════════

MULTICAST_OUTPUTS: dict[str, OutputSpec] = {
    "multicast_sender_single": {
        "command": "python src/exercises/ex_3_02_udp_multicast.py send --count 1 --no-predict",
        "description": "Send single multicast message",
        "contains": [
            "SEND",
            "239.1.1.1:5008"
        ],
        "not_contains": [
            "ERROR",
            "Traceback"
        ],
        "exit_code": 0,
        "timeout_seconds": 10,
        "requires_docker": True
    },
    
    "multicast_sender_with_ttl": {
        "command": "python src/exercises/ex_3_02_udp_multicast.py send --count 1 --ttl 32 --no-predict",
        "description": "Send multicast with TTL=32",
        "contains": [
            "TTL",
            "32"
        ],
        "exit_code": 0,
        "timeout_seconds": 10,
        "requires_docker": True
    },
    
    "multicast_help": {
        "command": "python src/exercises/ex_3_02_udp_multicast.py --help",
        "description": "Show help message",
        "contains": [
            "usage:",
            "send",
            "recv",
            "--ttl",
            "--group"
        ],
        "exit_code": 0,
        "requires_docker": False
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 3: TCP Tunnel
# ═══════════════════════════════════════════════════════════════════════════════

TUNNEL_OUTPUTS: dict[str, OutputSpec] = {
    "tunnel_echo_test": {
        "command": "echo 'hello' | nc -w 2 localhost 9090",
        "description": "Echo through tunnel",
        "contains": [
            "hello"
        ],
        "exit_code": 0,
        "timeout_seconds": 10,
        "requires_docker": True
    },
    
    "tunnel_direct_echo": {
        "command": "echo 'test' | nc -w 2 172.20.0.10 8080",
        "description": "Direct echo to server",
        "contains": [
            "test"
        ],
        "exit_code": 0,
        "timeout_seconds": 10,
        "requires_docker": True
    },
    
    "tunnel_help": {
        "command": "python src/exercises/ex_3_03_tcp_tunnel.py --help",
        "description": "Show help message",
        "contains": [
            "usage:",
            "--listen-port",
            "--target-host",
            "--target-port"
        ],
        "exit_code": 0,
        "requires_docker": False
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# Environment Checks
# ═══════════════════════════════════════════════════════════════════════════════

ENVIRONMENT_OUTPUTS: dict[str, OutputSpec] = {
    "python_version": {
        "command": "python --version",
        "description": "Check Python version",
        "contains": [
            "Python 3.1"  # 3.10, 3.11, 3.12
        ],
        "exit_code": 0,
        "requires_docker": False
    },
    
    "docker_available": {
        "command": "docker --version",
        "description": "Check Docker availability",
        "contains": [
            "Docker version"
        ],
        "exit_code": 0,
        "requires_docker": False
    },
    
    "tcpdump_available": {
        "command": "which tcpdump || echo 'not found'",
        "description": "Check tcpdump availability",
        "contains": [
            "tcpdump"
        ],
        "exit_code": 0,
        "requires_docker": True
    },
    
    "containers_running": {
        "command": "docker ps --format '{{.Names}}' | grep -c week3 || echo '0'",
        "description": "Check week3 containers running",
        "contains": [],  # Just check exit code
        "exit_code": 0,
        "requires_docker": True
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# Quiz and Formative Assessment
# ═══════════════════════════════════════════════════════════════════════════════

QUIZ_OUTPUTS: dict[str, OutputSpec] = {
    "quiz_validate": {
        "command": "python formative/run_quiz.py --validate",
        "description": "Validate quiz structure",
        "contains": [
            "Quiz structure is valid",
            "Questions:"
        ],
        "exit_code": 0,
        "requires_docker": False
    },
    
    "quiz_export_json": {
        "command": "python formative/run_quiz.py --export-lms json",
        "description": "Export quiz to JSON",
        "contains": [
            "Exported to JSON format"
        ],
        "exit_code": 0,
        "requires_docker": False
    },
    
    "quiz_export_moodle": {
        "command": "python formative/run_quiz.py --export-lms moodle",
        "description": "Export quiz to Moodle GIFT",
        "contains": [
            "Exported to Moodle GIFT format"
        ],
        "exit_code": 0,
        "requires_docker": False
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# Combined Output Specifications
# ═══════════════════════════════════════════════════════════════════════════════

EXPECTED_OUTPUTS: dict[str, OutputSpec] = {
    **BROADCAST_OUTPUTS,
    **MULTICAST_OUTPUTS,
    **TUNNEL_OUTPUTS,
    **ENVIRONMENT_OUTPUTS,
    **QUIZ_OUTPUTS
}


def get_docker_required_tests() -> list[str]:
    """Return list of test names that require Docker."""
    return [
        name for name, spec in EXPECTED_OUTPUTS.items()
        if spec.get("requires_docker", False)
    ]


def get_standalone_tests() -> list[str]:
    """Return list of test names that can run without Docker."""
    return [
        name for name, spec in EXPECTED_OUTPUTS.items()
        if not spec.get("requires_docker", False)
    ]


if __name__ == "__main__":
    # Print summary when run directly
    print("Expected Outputs Summary")
    print("=" * 60)
    print(f"Total tests: {len(EXPECTED_OUTPUTS)}")
    print(f"Docker required: {len(get_docker_required_tests())}")
    print(f"Standalone: {len(get_standalone_tests())}")
    print()
    print("Tests by category:")
    print(f"  Broadcast: {len(BROADCAST_OUTPUTS)}")
    print(f"  Multicast: {len(MULTICAST_OUTPUTS)}")
    print(f"  Tunnel: {len(TUNNEL_OUTPUTS)}")
    print(f"  Environment: {len(ENVIRONMENT_OUTPUTS)}")
    print(f"  Quiz: {len(QUIZ_OUTPUTS)}")
