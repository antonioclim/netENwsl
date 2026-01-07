#!/usr/bin/env python3
"""
start_lab.py - Week 14 Laboratory Launcher
NETWORKING class - ASE, Informatics | by Revolvix

This script starts all Docker containers and verifies the laboratory environment.

Usage:
    python scripts/start_lab.py           # Start all services
    python scripts/start_lab.py --status  # Check status only
    python scripts/start_lab.py --rebuild # Force rebuild images
"""

from __future__ import annotations

import subprocess
import sys
import time
import argparse
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DOCKER_DIR = PROJECT_ROOT / "docker"
COMPOSE_FILE = DOCKER_DIR / "docker-compose.yml"


class Colours:
    """ANSI colour codes for terminal output."""
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def log(level: str, message: str) -> None:
    """Print timestamped log message."""
    ts = datetime.now().strftime("%H:%M:%S")
    colours = {
        "INFO": Colours.BLUE,
        "OK": Colours.GREEN,
        "WARN": Colours.YELLOW,
        "ERROR": Colours.RED,
    }
    colour = colours.get(level, Colours.RESET)
    print(f"[{ts}] {colour}[{level}]{Colours.RESET} {message}")


def run_command(cmd: list, capture: bool = True, timeout: int = 120) -> tuple:
    """Run a command and return (success, stdout, stderr)."""
    try:
        if capture:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=PROJECT_ROOT
            )
            return result.returncode == 0, result.stdout, result.stderr
        else:
            result = subprocess.run(
                cmd,
                timeout=timeout,
                cwd=PROJECT_ROOT
            )
            return result.returncode == 0, "", ""
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


def docker_compose(*args, capture: bool = True) -> tuple:
    """Run docker compose command."""
    cmd = ["docker", "compose", "-f", str(COMPOSE_FILE)] + list(args)
    return run_command(cmd, capture=capture)


def get_container_status() -> Dict[str, Dict[str, Any]]:
    """Get status of all week14 containers."""
    success, stdout, _ = run_command([
        "docker", "ps", "-a",
        "--filter", "label=week=14",
        "--format", "{{json .}}"
    ])

    containers = {}
    if success and stdout.strip():
        for line in stdout.strip().split("\n"):
            try:
                data = json.loads(line)
                name = data.get("Names", "unknown")
                containers[name] = {
                    "status": data.get("Status", "unknown"),
                    "ports": data.get("Ports", ""),
                    "state": data.get("State", "unknown"),
                }
            except json.JSONDecodeError:
                continue

    return containers


def check_health(container: str, timeout: int = 5) -> bool:
    """Check if a container is healthy."""
    success, stdout, _ = run_command([
        "docker", "inspect",
        "--format", "{{.State.Health.Status}}",
        container
    ], timeout=timeout)

    if success:
        status = stdout.strip()
        return status == "healthy"
    return False


def wait_for_healthy(containers: list, timeout: int = 60) -> bool:
    """Wait for containers to become healthy."""
    start_time = time.time()
    pending = set(containers)

    while pending and (time.time() - start_time) < timeout:
        for container in list(pending):
            if check_health(container):
                log("OK", f"{container} is healthy")
                pending.remove(container)

        if pending:
            time.sleep(2)

    if pending:
        for container in pending:
            log("WARN", f"{container} did not become healthy in time")
        return False

    return True


def show_status() -> int:
    """Show current status of laboratory containers."""
    print()
    print("=" * 60)
    print(f"  {Colours.BOLD}Week 14 Laboratory Status{Colours.RESET}")
    print("=" * 60)
    print()

    containers = get_container_status()

    if not containers:
        log("INFO", "No Week 14 containers found")
        print("\nRun 'python scripts/start_lab.py' to start the laboratory.\n")
        return 0

    # Display container status
    print(f"{'Container':<20} {'State':<12} {'Status':<30}")
    print("-" * 62)

    for name, info in sorted(containers.items()):
        state = info.get("state", "unknown")
        status = info.get("status", "unknown")

        if state == "running":
            state_display = f"{Colours.GREEN}{state}{Colours.RESET}"
        elif state == "exited":
            state_display = f"{Colours.RED}{state}{Colours.RESET}"
        else:
            state_display = f"{Colours.YELLOW}{state}{Colours.RESET}"

        print(f"{name:<20} {state_display:<22} {status:<30}")

    print()

    # Check health status
    healthy_containers = ["week14_app1", "week14_app2", "week14_lb", "week14_echo"]
    all_healthy = True

    print(f"{Colours.BOLD}Health Checks:{Colours.RESET}")
    for container in healthy_containers:
        if container in containers:
            healthy = check_health(container)
            status = f"{Colours.GREEN}healthy{Colours.RESET}" if healthy else f"{Colours.RED}unhealthy{Colours.RESET}"
            print(f"  {container}: {status}")
            if not healthy:
                all_healthy = False

    print()

    # Show access points
    print(f"{Colours.BOLD}Access Points:{Colours.RESET}")
    print(f"  Load Balancer:  http://localhost:8080/")
    print(f"  LB Status:      http://localhost:8080/lb-status")
    print(f"  Backend 1:      http://localhost:8001/info")
    print(f"  Backend 2:      http://localhost:8002/info")
    print(f"  TCP Echo:       localhost:9000")
    print()

    return 0 if all_healthy else 1


def start_lab(rebuild: bool = False, detach: bool = True) -> int:
    """Start the laboratory environment."""
    print()
    print("=" * 60)
    print(f"  {Colours.BOLD}Starting Week 14 Laboratory Environment{Colours.RESET}")
    print("=" * 60)
    print()

    # Check Docker is running
    success, _, _ = run_command(["docker", "info"], timeout=10)
    if not success:
        log("ERROR", "Docker is not running. Please start Docker Desktop.")
        return 1

    # Check compose file exists
    if not COMPOSE_FILE.exists():
        log("ERROR", f"Compose file not found: {COMPOSE_FILE}")
        return 1

    # Build images
    if rebuild:
        log("INFO", "Building Docker images (forced rebuild)...")
        success, stdout, stderr = docker_compose("build", "--no-cache")
    else:
        log("INFO", "Building Docker images (if needed)...")
        success, stdout, stderr = docker_compose("build")

    if not success:
        log("ERROR", f"Failed to build images: {stderr}")
        return 1

    log("OK", "Docker images ready")

    # Start containers
    log("INFO", "Starting containers...")
    if detach:
        success, stdout, stderr = docker_compose("up", "-d")
    else:
        success, stdout, stderr = docker_compose("up", capture=False)
        return 0 if success else 1

    if not success:
        log("ERROR", f"Failed to start containers: {stderr}")
        return 1

    log("OK", "Containers started")

    # Wait for health checks
    log("INFO", "Waiting for services to initialise...")
    time.sleep(5)

    containers_to_check = ["week14_app1", "week14_app2", "week14_lb", "week14_echo"]
    all_healthy = wait_for_healthy(containers_to_check, timeout=60)

    print()
    print("=" * 60)

    if all_healthy:
        print(f"  {Colours.GREEN}{Colours.BOLD}Laboratory environment is ready!{Colours.RESET}")
    else:
        print(f"  {Colours.YELLOW}{Colours.BOLD}Laboratory started with warnings{Colours.RESET}")

    print("=" * 60)
    print()
    print(f"{Colours.BOLD}Access Points:{Colours.RESET}")
    print(f"  Load Balancer:  http://localhost:8080/")
    print(f"  LB Status:      http://localhost:8080/lb-status")
    print(f"  Backend 1:      http://localhost:8001/info")
    print(f"  Backend 2:      http://localhost:8002/info")
    print(f"  TCP Echo:       localhost:9000")
    print()
    print(f"{Colours.BOLD}Useful Commands:{Colours.RESET}")
    print(f"  View logs:      docker compose -f docker/docker-compose.yml logs -f")
    print(f"  Shell access:   docker compose -f docker/docker-compose.yml exec client bash")
    print(f"  Stop lab:       python scripts/stop_lab.py")
    print()

    return 0 if all_healthy else 1


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Start Week 14 Laboratory Environment"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Check status only, do not start"
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Force rebuild Docker images"
    )
    parser.add_argument(
        "--attach", "-a",
        action="store_true",
        help="Run in attached mode (see all logs)"
    )

    args = parser.parse_args()

    if args.status:
        return show_status()

    return start_lab(rebuild=args.rebuild, detach=not args.attach)


if __name__ == "__main__":
    sys.exit(main())
