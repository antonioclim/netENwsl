#!/usr/bin/env python3
"""
Docker Management Utilities — Week 6: NAT/PAT & SDN Laboratory
==============================================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Provides helper functions for Docker container and Docker Compose management.

Usage:
    from scripts.utils.docker_utils import DockerManager
    
    manager = DockerManager(Path("docker"))
    manager.compose_up()
    manager.show_status(EXPECTED_SERVICES)
    manager.compose_down()
"""

from __future__ import annotations

import json
import subprocess
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Union

from .logger import setup_logger

logger = setup_logger("docker_utils")


# ═══════════════════════════════════════════════════════════════════════════════
# EXCEPTIONS
# ═══════════════════════════════════════════════════════════════════════════════

class DockerError(Exception):
    """Base exception for Docker-related errors."""
    pass


class DockerNotRunningError(DockerError):
    """Raised when Docker daemon is not running."""
    pass


class ComposeFileNotFoundError(DockerError):
    """Raised when docker-compose.yml is not found."""
    pass


class ServiceNotFoundError(DockerError):
    """Raised when a specified service does not exist."""
    pass


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

class ContainerState(Enum):
    """Docker container states."""
    RUNNING = "running"
    EXITED = "exited"
    PAUSED = "paused"
    RESTARTING = "restarting"
    DEAD = "dead"
    CREATED = "created"
    UNKNOWN = "unknown"
    
    @classmethod
    def from_string(cls, value: str) -> "ContainerState":
        """Parse state from string."""
        try:
            return cls(value.lower())
        except ValueError:
            return cls.UNKNOWN


@dataclass
class ServiceConfig:
    """Configuration for an expected service."""
    name: str
    container: str
    port: Optional[int] = None
    health_check: Optional[str] = None
    startup_time: int = 5
    required: bool = True


@dataclass
class ServiceStatus:
    """Status information for a running service."""
    name: str
    container_id: str
    state: ContainerState
    health: Optional[str] = None
    ports: Optional[str] = None
    
    @property
    def is_healthy(self) -> bool:
        """Check if service is in a healthy state."""
        return self.state == ContainerState.RUNNING


# ═══════════════════════════════════════════════════════════════════════════════
# DOCKER_MANAGER_CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class DockerManager:
    """
    Manages Docker Compose operations for the laboratory environment.
    
    This class provides a high-level interface for starting, stopping,
    and managing Docker containers used in the networking lab.
    
    Attributes:
        compose_dir: Path to directory containing docker-compose.yml
        compose_file: Path to the docker-compose.yml file
        
    Example:
        >>> manager = DockerManager(Path("docker"))
        >>> manager.compose_up(profiles=["controller"])
        >>> manager.show_status(services)
        >>> manager.compose_down()
    """
    
    def __init__(self, compose_dir: Union[Path, str]) -> None:
        """
        Initialise the Docker manager.
        
        Args:
            compose_dir: Path to directory containing docker-compose.yml
            
        Raises:
            ComposeFileNotFoundError: If docker-compose.yml not found
        """
        self.compose_dir = Path(compose_dir)
        self.compose_file = self.compose_dir / "docker-compose.yml"
        
        if not self.compose_file.exists():
            raise ComposeFileNotFoundError(
                f"docker-compose.yml not found in {compose_dir}"
            )
    
    # ─────────────────────────────────────────────────────────────────────────
    # Internal Helpers
    # ─────────────────────────────────────────────────────────────────────────
    
    def _run_compose(
        self,
        *args: str,
        capture_output: bool = False,
        check: bool = True,
        timeout: Optional[int] = None,
    ) -> subprocess.CompletedProcess[str]:
        """
        Run a docker compose command.
        
        Args:
            *args: Command arguments
            capture_output: Whether to capture stdout/stderr
            check: Whether to raise on non-zero exit
            timeout: Command timeout in seconds
            
        Returns:
            CompletedProcess result
            
        Raises:
            DockerNotRunningError: If Docker daemon is not running
            subprocess.CalledProcessError: If command fails and check=True
        """
        cmd = ["docker", "compose", "-f", str(self.compose_file)] + list(args)
        logger.debug(f"Running: {' '.join(cmd)}")
        
        try:
            return subprocess.run(
                cmd,
                cwd=self.compose_dir,
                capture_output=capture_output,
                text=True,
                check=check,
                timeout=timeout,
            )
        except FileNotFoundError:
            raise DockerNotRunningError(
                "Docker command not found. Is Docker installed and in PATH?"
            )
        except subprocess.CalledProcessError as e:
            if "Cannot connect to the Docker daemon" in str(e.stderr):
                raise DockerNotRunningError(
                    "Docker daemon is not running. Please start Docker Desktop."
                )
            raise
    
    def _is_docker_running(self) -> bool:
        """Check if Docker daemon is running."""
        try:
            result = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                timeout=5,
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    # ─────────────────────────────────────────────────────────────────────────
    # Build Operations
    # ─────────────────────────────────────────────────────────────────────────
    
    def compose_build(
        self,
        service: Optional[str] = None,
        no_cache: bool = False,
        pull: bool = False,
    ) -> bool:
        """
        Build Docker images.
        
        Args:
            service: Specific service to build (None for all)
            no_cache: Whether to build without cache
            pull: Always pull base images
            
        Returns:
            True if successful, False otherwise
        """
        args: List[str] = ["build"]
        
        if no_cache:
            args.append("--no-cache")
        if pull:
            args.append("--pull")
        if service:
            args.append(service)
        
        try:
            self._run_compose(*args)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Build failed: {e}")
            return False
    
    # ─────────────────────────────────────────────────────────────────────────
    # Start Operations
    # ─────────────────────────────────────────────────────────────────────────
    
    def compose_up(
        self,
        services: Optional[Sequence[str]] = None,
        detach: bool = True,
        profiles: Optional[Sequence[str]] = None,
        build: bool = False,
        remove_orphans: bool = True,
    ) -> bool:
        """
        Start Docker Compose services.
        
        Args:
            services: List of services to start (None for all)
            detach: Run in detached mode
            profiles: List of profiles to activate
            build: Build images before starting
            remove_orphans: Remove orphaned containers
            
        Returns:
            True if successful, False otherwise
        """
        args: List[str] = []
        
        if profiles:
            for profile in profiles:
                args.extend(["--profile", profile])
        
        args.append("up")
        
        if detach:
            args.append("-d")
        if build:
            args.append("--build")
        if remove_orphans:
            args.append("--remove-orphans")
        
        if services:
            args.extend(services)
        
        try:
            self._run_compose(*args)
            return True
        except (subprocess.CalledProcessError, DockerNotRunningError) as e:
            logger.error(f"Failed to start services: {e}")
            return False
    
    # ─────────────────────────────────────────────────────────────────────────
    # Stop Operations
    # ─────────────────────────────────────────────────────────────────────────
    
    def compose_down(
        self,
        volumes: bool = False,
        remove_orphans: bool = True,
        timeout: int = 10,
        dry_run: bool = False,
    ) -> bool:
        """
        Stop and remove Docker Compose services.
        
        Args:
            volumes: Also remove volumes
            remove_orphans: Remove orphaned containers
            timeout: Shutdown timeout in seconds
            dry_run: Only print what would be done
            
        Returns:
            True if successful, False otherwise
        """
        if dry_run:
            logger.info("[DRY RUN] Would run: docker compose down")
            return True
        
        args: List[str] = ["down", "-t", str(timeout)]
        
        if volumes:
            args.append("-v")
        if remove_orphans:
            args.append("--remove-orphans")
        
        try:
            self._run_compose(*args)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to stop services: {e}")
            return False
    
    def compose_stop(
        self,
        services: Optional[Sequence[str]] = None,
        timeout: int = 10,
    ) -> bool:
        """
        Stop services without removing containers.
        
        Args:
            services: Services to stop (None for all)
            timeout: Shutdown timeout in seconds
            
        Returns:
            True if successful, False otherwise
        """
        args: List[str] = ["stop", "-t", str(timeout)]
        
        if services:
            args.extend(services)
        
        try:
            self._run_compose(*args)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to stop services: {e}")
            return False
    
    # ─────────────────────────────────────────────────────────────────────────
    # Status Operations
    # ─────────────────────────────────────────────────────────────────────────
    
    def compose_ps(self) -> Dict[str, ServiceStatus]:
        """
        Get status of compose services.
        
        Returns:
            Dictionary mapping service name to ServiceStatus
        """
        try:
            result = self._run_compose("ps", "--format", "json", capture_output=True)
            services: Dict[str, ServiceStatus] = {}
            
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    name = data.get('Service', data.get('Name', 'unknown'))
                    services[name] = ServiceStatus(
                        name=name,
                        container_id=data.get('ID', ''),
                        state=ContainerState.from_string(data.get('State', '')),
                        health=data.get('Health'),
                        ports=data.get('Ports'),
                    )
                except json.JSONDecodeError:
                    logger.debug(f"Failed to parse service status: {line}")
            
            return services
            
        except (subprocess.CalledProcessError, DockerNotRunningError) as e:
            logger.error(f"Failed to get service status: {e}")
            return {}
    
    def is_service_running(self, service: str) -> bool:
        """
        Check if a specific service is running.
        
        Args:
            service: Service name to check
            
        Returns:
            True if service is running, False otherwise
        """
        status = self.compose_ps()
        return service in status and status[service].is_healthy
    
    def show_status(self, expected_services: Dict[str, Dict[str, Any]]) -> None:
        """
        Display status of expected services.
        
        Args:
            expected_services: Dictionary of service configurations with keys:
                - container: Container name
                - port: Port number (optional)
        """
        running = self.compose_ps()
        
        print("\n" + "═" * 65)
        print("  SERVICE STATUS")
        print("═" * 65)
        print(f"  {'Service':<20} {'Port':<10} {'State':<15} {'Health':<10}")
        print("─" * 65)
        
        for name, config in expected_services.items():
            container = config.get("container", name)
            port = str(config.get("port", "N/A"))
            
            if container in running:
                status = running[container]
                state = status.state.value
                health = status.health or "—"
                
                if status.is_healthy:
                    icon = "✓"
                else:
                    icon = "!"
                    
                print(f"  [{icon}] {name:<18} {port:<10} {state:<15} {health:<10}")
            else:
                print(f"  [✗] {name:<18} {port:<10} {'not found':<15} {'—':<10}")
        
        print("═" * 65)
    
    # ─────────────────────────────────────────────────────────────────────────
    # Health Verification
    # ─────────────────────────────────────────────────────────────────────────
    
    def verify_services(
        self,
        services: Dict[str, Dict[str, Any]],
        timeout: int = 30,
        retry_interval: int = 2,
    ) -> bool:
        """
        Verify all services are healthy.
        
        Args:
            services: Dictionary of service configurations
            timeout: Maximum time to wait for services
            retry_interval: Seconds between retries
            
        Returns:
            True if all required services are healthy
        """
        start_time = time.time()
        required_services = [
            name for name, cfg in services.items() 
            if cfg.get("required", True)
        ]
        
        while time.time() - start_time < timeout:
            running = self.compose_ps()
            all_healthy = True
            
            for name in required_services:
                container = services[name].get("container", name)
                
                if container not in running:
                    logger.debug(f"Service {name} not found yet")
                    all_healthy = False
                elif not running[container].is_healthy:
                    logger.debug(f"Service {name} not healthy: {running[container].state}")
                    all_healthy = False
            
            if all_healthy:
                logger.info("All required services are healthy")
                return True
            
            time.sleep(retry_interval)
        
        # Final check with detailed output
        running = self.compose_ps()
        unhealthy = []
        
        for name in required_services:
            container = services[name].get("container", name)
            if container not in running or not running[container].is_healthy:
                unhealthy.append(name)
        
        if unhealthy:
            logger.error(f"Services not healthy after {timeout}s: {', '.join(unhealthy)}")
            return False
        
        return True
    
    def wait_for_service(
        self,
        service: str,
        timeout: int = 30,
    ) -> bool:
        """
        Wait for a specific service to become healthy.
        
        Args:
            service: Service name to wait for
            timeout: Maximum time to wait
            
        Returns:
            True if service becomes healthy within timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.is_service_running(service):
                return True
            time.sleep(1)
        
        return False
    
    # ─────────────────────────────────────────────────────────────────────────
    # Resource Cleanup
    # ─────────────────────────────────────────────────────────────────────────
    
    def remove_by_prefix(
        self,
        prefix: str,
        dry_run: bool = False,
    ) -> Dict[str, int]:
        """
        Remove containers, networks and volumes with a given prefix.
        
        Args:
            prefix: Prefix to match
            dry_run: Only print what would be done
            
        Returns:
            Dictionary with counts of removed resources
        """
        removed = {"containers": 0, "networks": 0, "volumes": 0}
        
        # Remove containers
        result = subprocess.run(
            ["docker", "ps", "-a", "--filter", f"name={prefix}", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
        )
        containers = [c for c in result.stdout.strip().split('\n') if c]
        
        for container in containers:
            if dry_run:
                logger.info(f"[DRY RUN] Would remove container: {container}")
            else:
                logger.info(f"Removing container: {container}")
                subprocess.run(["docker", "rm", "-f", container], capture_output=True)
            removed["containers"] += 1
        
        # Remove networks
        result = subprocess.run(
            ["docker", "network", "ls", "--filter", f"name={prefix}", "--format", "{{.Name}}"],
            capture_output=True,
            text=True,
        )
        networks = [n for n in result.stdout.strip().split('\n') 
                   if n and n not in ("bridge", "host", "none")]
        
        for network in networks:
            if dry_run:
                logger.info(f"[DRY RUN] Would remove network: {network}")
            else:
                logger.info(f"Removing network: {network}")
                subprocess.run(["docker", "network", "rm", network], capture_output=True)
            removed["networks"] += 1
        
        # Remove volumes
        result = subprocess.run(
            ["docker", "volume", "ls", "--filter", f"name={prefix}", "--format", "{{.Name}}"],
            capture_output=True,
            text=True,
        )
        volumes = [v for v in result.stdout.strip().split('\n') if v]
        
        for volume in volumes:
            if dry_run:
                logger.info(f"[DRY RUN] Would remove volume: {volume}")
            else:
                logger.info(f"Removing volume: {volume}")
                subprocess.run(["docker", "volume", "rm", volume], capture_output=True)
            removed["volumes"] += 1
        
        return removed
    
    def system_prune(
        self,
        all_unused: bool = False,
        volumes: bool = False,
    ) -> None:
        """
        Prune unused Docker resources.
        
        Args:
            all_unused: Remove all unused images, not just dangling ones
            volumes: Also prune volumes
        """
        args = ["docker", "system", "prune", "-f"]
        
        if all_unused:
            args.append("-a")
        if volumes:
            args.append("--volumes")
        
        subprocess.run(args)


# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Module {__name__} loaded successfully.")
    print("This module provides Docker management utilities for the networking laboratory.")
    print()
    print("Available classes:")
    print("  - DockerManager: High-level Docker Compose management")
    print("  - ServiceStatus: Container status information")
    print("  - ServiceConfig: Service configuration dataclass")
