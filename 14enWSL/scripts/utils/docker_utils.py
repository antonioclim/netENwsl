#!/usr/bin/env python3
"""
Docker Management Utilities for Week 14 Laboratory.

NETWORKING class - ASE, Informatics | by Revolvix

This module provides a comprehensive interface for managing Docker
containers, networks, and volumes within the laboratory environment.
"""

import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

from .logger import get_logger

logger = get_logger(__name__)


class ContainerState(Enum):
    """Enumeration of possible container states."""
    RUNNING = "running"
    EXITED = "exited"
    PAUSED = "paused"
    RESTARTING = "restarting"
    CREATED = "created"
    REMOVING = "removing"
    DEAD = "dead"
    UNKNOWN = "unknown"


class HealthStatus(Enum):
    """Enumeration of container health check statuses."""
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    STARTING = "starting"
    NONE = "none"


@dataclass
class ContainerInfo:
    """Data class representing container information."""
    name: str
    id: str
    state: ContainerState
    health: HealthStatus
    ports: Dict[str, str]
    image: str
    labels: Dict[str, str]
    networks: List[str]
    created: str
    started: Optional[str] = None


class DockerError(Exception):
    """Exception raised for Docker-related errors."""
    pass


class DockerManager:
    """
    Manages Docker operations for the laboratory environment.
    
    Provides methods for building, starting, stopping, and inspecting
    Docker containers using docker-compose orchestration.
    
    Attributes:
        compose_dir: Path to directory containing docker-compose.yml
        project_name: Docker Compose project name (default: week14)
    """
    
    def __init__(
        self,
        compose_dir: Path,
        project_name: str = "week14"
    ):
        """
        Initialise the Docker manager.
        
        Args:
            compose_dir: Directory containing docker-compose.yml
            project_name: Docker Compose project name for resource isolation
        """
        self.compose_dir = Path(compose_dir)
        self.project_name = project_name
        self.compose_file = self.compose_dir / "docker-compose.yml"
        
        if not self.compose_file.exists():
            logger.warning(f"Compose file not found: {self.compose_file}")
    
    def _run_command(
        self,
        args: List[str],
        capture: bool = True,
        check: bool = True,
        timeout: int = 300
    ) -> subprocess.CompletedProcess:
        """
        Execute a command and return the result.
        
        Args:
            args: Command arguments as a list
            capture: Whether to capture stdout/stderr
            check: Whether to raise exception on non-zero exit
            timeout: Command timeout in seconds
            
        Returns:
            CompletedProcess instance with execution results
            
        Raises:
            DockerError: If command execution fails
        """
        try:
            result = subprocess.run(
                args,
                capture_output=capture,
                text=True,
                timeout=timeout,
                check=check
            )
            return result
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if e.stderr else str(e)
            raise DockerError(f"Command failed: {' '.join(args)}\n{error_msg}")
        except subprocess.TimeoutExpired:
            raise DockerError(f"Command timed out after {timeout}s: {' '.join(args)}")
        except FileNotFoundError:
            raise DockerError(f"Command not found: {args[0]}")
    
    def _compose_command(self, *args: str) -> List[str]:
        """Build a docker compose command with project settings."""
        return [
            "docker", "compose",
            "-p", self.project_name,
            "-f", str(self.compose_file),
            *args
        ]
    
    def is_docker_running(self) -> bool:
        """
        Check if the Docker daemon is accessible.
        
        Returns:
            True if Docker daemon is running and accessible
        """
        try:
            self._run_command(["docker", "info"], timeout=10)
            return True
        except DockerError:
            return False
    
    def compose_build(self, no_cache: bool = False) -> bool:
        """
        Build Docker images defined in docker-compose.yml.
        
        Args:
            no_cache: If True, build without using cache
            
        Returns:
            True if build succeeded
        """
        logger.info("Building Docker images...")
        args = self._compose_command("build")
        if no_cache:
            args.append("--no-cache")
        
        try:
            self._run_command(args, capture=False, timeout=600)
            logger.info("Build completed successfully")
            return True
        except DockerError as e:
            logger.error(f"Build failed: {e}")
            return False
    
    def compose_up(
        self,
        detach: bool = True,
        build: bool = False,
        wait: bool = True,
        timeout: int = 60
    ) -> bool:
        """
        Start containers defined in docker-compose.yml.
        
        Args:
            detach: Run containers in background
            build: Build images before starting
            wait: Wait for health checks to pass
            timeout: Maximum wait time for health checks
            
        Returns:
            True if all containers started successfully
        """
        logger.info("Starting containers...")
        args = self._compose_command("up")
        
        if detach:
            args.append("-d")
        if build:
            args.append("--build")
        if wait:
            args.extend(["--wait", "--wait-timeout", str(timeout)])
        
        try:
            self._run_command(args, capture=False, timeout=timeout + 120)
            logger.info("Containers started successfully")
            return True
        except DockerError as e:
            logger.error(f"Failed to start containers: {e}")
            return False
    
    def compose_down(
        self,
        volumes: bool = False,
        remove_orphans: bool = True,
        timeout: int = 30,
        dry_run: bool = False
    ) -> bool:
        """
        Stop and remove containers defined in docker-compose.yml.
        
        Args:
            volumes: Also remove named volumes
            remove_orphans: Remove containers not defined in compose file
            timeout: Shutdown timeout per container
            dry_run: Print actions without executing
            
        Returns:
            True if shutdown succeeded
        """
        if dry_run:
            logger.info("[DRY RUN] Would stop and remove containers")
            return True
        
        logger.info("Stopping containers...")
        args = self._compose_command("down", "-t", str(timeout))
        
        if volumes:
            args.append("-v")
        if remove_orphans:
            args.append("--remove-orphans")
        
        try:
            self._run_command(args, timeout=timeout + 60)
            logger.info("Containers stopped and removed")
            return True
        except DockerError as e:
            logger.error(f"Failed to stop containers: {e}")
            return False
    
    def compose_stop(self, timeout: int = 30) -> bool:
        """
        Stop containers without removing them.
        
        Args:
            timeout: Shutdown timeout per container
            
        Returns:
            True if stop succeeded
        """
        logger.info("Stopping containers...")
        args = self._compose_command("stop", "-t", str(timeout))
        
        try:
            self._run_command(args, timeout=timeout + 60)
            logger.info("Containers stopped")
            return True
        except DockerError as e:
            logger.error(f"Failed to stop containers: {e}")
            return False
    
    def get_container_info(self, name: str) -> Optional[ContainerInfo]:
        """
        Get detailed information about a container.
        
        Args:
            name: Container name or ID
            
        Returns:
            ContainerInfo instance or None if not found
        """
        try:
            result = self._run_command([
                "docker", "inspect",
                "--format", "{{json .}}",
                name
            ])
            
            data = json.loads(result.stdout)
            
            # Parse state
            state_str = data.get("State", {}).get("Status", "unknown")
            try:
                state = ContainerState(state_str)
            except ValueError:
                state = ContainerState.UNKNOWN
            
            # Parse health
            health_data = data.get("State", {}).get("Health", {})
            health_str = health_data.get("Status", "none") if health_data else "none"
            try:
                health = HealthStatus(health_str)
            except ValueError:
                health = HealthStatus.NONE
            
            # Parse ports
            ports = {}
            port_bindings = data.get("HostConfig", {}).get("PortBindings", {})
            for container_port, bindings in port_bindings.items():
                if bindings:
                    host_port = bindings[0].get("HostPort", "")
                    ports[container_port] = host_port
            
            # Parse networks
            networks = list(data.get("NetworkSettings", {}).get("Networks", {}).keys())
            
            return ContainerInfo(
                name=data.get("Name", "").lstrip("/"),
                id=data.get("Id", "")[:12],
                state=state,
                health=health,
                ports=ports,
                image=data.get("Config", {}).get("Image", ""),
                labels=data.get("Config", {}).get("Labels", {}),
                networks=networks,
                created=data.get("Created", ""),
                started=data.get("State", {}).get("StartedAt")
            )
            
        except (DockerError, json.JSONDecodeError, KeyError):
            return None
    
    def list_containers(
        self,
        all_containers: bool = False,
        filter_label: Optional[str] = None
    ) -> List[ContainerInfo]:
        """
        List containers matching criteria.
        
        Args:
            all_containers: Include stopped containers
            filter_label: Filter by label (e.g., "week=14")
            
        Returns:
            List of ContainerInfo objects
        """
        args = ["docker", "ps", "--format", "{{.Names}}"]
        
        if all_containers:
            args.append("-a")
        if filter_label:
            args.extend(["--filter", f"label={filter_label}"])
        
        try:
            result = self._run_command(args)
            names = [n.strip() for n in result.stdout.strip().split("\n") if n.strip()]
            
            containers = []
            for name in names:
                info = self.get_container_info(name)
                if info:
                    containers.append(info)
            
            return containers
            
        except DockerError:
            return []
    
    def verify_services(
        self,
        services: Dict[str, Dict[str, Any]],
        timeout: int = 60
    ) -> bool:
        """
        Verify that all services are healthy and accessible.
        
        Args:
            services: Dictionary mapping service names to configuration
                      Expected keys: container, port, health_check, startup_time
            timeout: Maximum time to wait for services
            
        Returns:
            True if all services are healthy
        """
        logger.info("Verifying services...")
        start_time = time.time()
        all_healthy = True
        
        for name, config in services.items():
            container_name = config.get("container", name)
            expected_port = config.get("port")
            
            # Check container state
            info = self.get_container_info(container_name)
            
            if info is None:
                logger.error(f"  {name}: Container not found")
                all_healthy = False
                continue
            
            if info.state != ContainerState.RUNNING:
                logger.error(f"  {name}: State is {info.state.value}")
                all_healthy = False
                continue
            
            if info.health == HealthStatus.UNHEALTHY:
                logger.error(f"  {name}: Health check failing")
                all_healthy = False
                continue
            
            if info.health == HealthStatus.STARTING:
                # Wait for health check
                elapsed = time.time() - start_time
                remaining = timeout - elapsed
                
                if remaining > 0:
                    logger.info(f"  {name}: Waiting for health check...")
                    time.sleep(min(5, remaining))
                    info = self.get_container_info(container_name)
                    
                    if info and info.health == HealthStatus.HEALTHY:
                        logger.info(f"  {name}: Healthy on port {expected_port}")
                    else:
                        logger.warning(f"  {name}: Health check still pending")
                else:
                    logger.warning(f"  {name}: Health check timeout")
            else:
                logger.info(f"  {name}: Healthy on port {expected_port}")
        
        return all_healthy
    
    def show_status(self, services: Optional[Dict[str, Dict[str, Any]]] = None) -> None:
        """
        Display current status of laboratory containers.
        
        Args:
            services: Optional service configuration for detailed status
        """
        containers = self.list_containers(
            all_containers=True,
            filter_label="week=14"
        )
        
        if not containers:
            logger.info("No Week 14 containers found")
            return
        
        logger.info("\nContainer Status:")
        logger.info("-" * 70)
        
        for c in containers:
            state_icon = "●" if c.state == ContainerState.RUNNING else "○"
            health_str = f"[{c.health.value}]" if c.health != HealthStatus.NONE else ""
            
            ports_str = ", ".join(
                f"{hp}→{cp.split('/')[0]}"
                for cp, hp in c.ports.items()
            ) if c.ports else "no ports"
            
            logger.info(f"  {state_icon} {c.name:25} {c.state.value:10} {health_str:12} {ports_str}")
        
        logger.info("-" * 70)
    
    def remove_by_prefix(
        self,
        prefix: str,
        dry_run: bool = False
    ) -> Tuple[int, int, int]:
        """
        Remove Docker resources matching a prefix.
        
        Args:
            prefix: Resource name prefix to match
            dry_run: Print actions without executing
            
        Returns:
            Tuple of (containers_removed, networks_removed, volumes_removed)
        """
        containers_removed = 0
        networks_removed = 0
        volumes_removed = 0
        
        # Remove containers
        try:
            result = self._run_command([
                "docker", "ps", "-aq",
                "--filter", f"name={prefix}"
            ])
            container_ids = [c.strip() for c in result.stdout.strip().split("\n") if c.strip()]
            
            for cid in container_ids:
                if dry_run:
                    logger.info(f"[DRY RUN] Would remove container: {cid}")
                else:
                    self._run_command(["docker", "rm", "-f", cid])
                    logger.info(f"Removed container: {cid}")
                containers_removed += 1
        except DockerError:
            pass
        
        # Remove networks
        try:
            result = self._run_command([
                "docker", "network", "ls", "-q",
                "--filter", f"name={prefix}"
            ])
            network_ids = [n.strip() for n in result.stdout.strip().split("\n") if n.strip()]
            
            for nid in network_ids:
                if dry_run:
                    logger.info(f"[DRY RUN] Would remove network: {nid}")
                else:
                    try:
                        self._run_command(["docker", "network", "rm", nid])
                        logger.info(f"Removed network: {nid}")
                        networks_removed += 1
                    except DockerError:
                        pass  # Network might be in use
        except DockerError:
            pass
        
        # Remove volumes
        try:
            result = self._run_command([
                "docker", "volume", "ls", "-q",
                "--filter", f"name={prefix}"
            ])
            volume_ids = [v.strip() for v in result.stdout.strip().split("\n") if v.strip()]
            
            for vid in volume_ids:
                if dry_run:
                    logger.info(f"[DRY RUN] Would remove volume: {vid}")
                else:
                    try:
                        self._run_command(["docker", "volume", "rm", vid])
                        logger.info(f"Removed volume: {vid}")
                        volumes_removed += 1
                    except DockerError:
                        pass  # Volume might be in use
        except DockerError:
            pass
        
        return containers_removed, networks_removed, volumes_removed
    
    def system_prune(self, volumes: bool = False) -> bool:
        """
        Remove unused Docker resources.
        
        Args:
            volumes: Also prune unused volumes
            
        Returns:
            True if prune succeeded
        """
        logger.info("Pruning unused Docker resources...")
        args = ["docker", "system", "prune", "-f"]
        
        if volumes:
            args.append("--volumes")
        
        try:
            self._run_command(args, timeout=120)
            logger.info("Prune completed")
            return True
        except DockerError as e:
            logger.error(f"Prune failed: {e}")
            return False
    
    def get_logs(
        self,
        container: str,
        tail: int = 100,
        follow: bool = False
    ) -> str:
        """
        Get container logs.
        
        Args:
            container: Container name or ID
            tail: Number of lines from end
            follow: Stream logs continuously
            
        Returns:
            Log output as string
        """
        args = ["docker", "logs", "--tail", str(tail)]
        
        if follow:
            args.append("-f")
        
        args.append(container)
        
        try:
            result = self._run_command(args, timeout=10)
            return result.stdout + result.stderr
        except DockerError:
            return ""
    
    def exec_command(
        self,
        container: str,
        command: List[str],
        interactive: bool = False
    ) -> Tuple[int, str, str]:
        """
        Execute a command in a running container.
        
        Args:
            container: Container name or ID
            command: Command to execute as list of arguments
            interactive: Run in interactive mode
            
        Returns:
            Tuple of (exit_code, stdout, stderr)
        """
        args = ["docker", "exec"]
        
        if interactive:
            args.extend(["-it"])
        
        args.append(container)
        args.extend(command)
        
        try:
            result = self._run_command(args, check=False)
            return result.returncode, result.stdout, result.stderr
        except DockerError as e:
            return 1, "", str(e)


# Convenience function for quick Docker checks
def quick_docker_check() -> bool:
    """Quick check if Docker is available and running."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False
