#!/usr/bin/env python3
"""
Docker Management Utilities
===========================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Provides Docker Compose management functions for Week 13 laboratory.
These utilities handle container lifecycle, health checks and cleanup.

Classes:
    DockerManager: Main class for Docker Compose operations

Example:
    >>> manager = DockerManager(Path("docker"))
    >>> manager.compose_up(detach=True)
    >>> manager.verify_services(SERVICES)
    >>> manager.compose_down()
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT_DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════════
import socket
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


# ═══════════════════════════════════════════════════════════════════════════════
# DOCKER_MANAGER_CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class DockerManager:
    """
    Manages Docker Compose operations for the laboratory environment.
    
    This class provides a Pythonic interface to Docker Compose commands,
    with additional utilities for health checking and service verification.
    
    Attributes:
        docker_dir: Path to directory containing docker-compose.yml
        compose_file: Full path to docker-compose.yml
        env_file: Full path to .env file (if exists)
    
    Example:
        >>> from pathlib import Path
        >>> manager = DockerManager(Path("docker"))
        >>> manager.compose_up()
        True
    """
    
    def __init__(self, docker_dir: Path) -> None:
        """
        Initialise Docker manager.
        
        Args:
            docker_dir: Path to directory containing docker-compose.yml
        
        Raises:
            FileNotFoundError: If docker-compose.yml does not exist
        """
        self.docker_dir = docker_dir
        self.compose_file = docker_dir / "docker-compose.yml"
        self.env_file = docker_dir / ".env"
        
        if not self.compose_file.exists():
            raise FileNotFoundError(f"docker-compose.yml not found in {docker_dir}")
    
    # ───────────────────────────────────────────────────────────────────────────
    # INTERNAL_HELPERS
    # ───────────────────────────────────────────────────────────────────────────
    
    def _run_compose(
        self,
        args: List[str],
        capture: bool = True,
        timeout: int = 120
    ) -> subprocess.CompletedProcess:
        """
        Execute a docker compose command.
        
        Args:
            args: Arguments to pass to docker compose
            capture: Whether to capture stdout/stderr
            timeout: Command timeout in seconds
        
        Returns:
            CompletedProcess instance with return code and output
        """
        cmd = ["docker", "compose"]
        
        if self.env_file.exists():
            cmd.extend(["--env-file", str(self.env_file)])
        
        cmd.extend(["-f", str(self.compose_file)])
        cmd.extend(args)
        
        return subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            timeout=timeout,
            cwd=str(self.docker_dir)
        )
    
    def _check_port(
        self,
        port: int,
        host: str = "127.0.0.1",
        timeout: float = 2.0
    ) -> bool:
        """
        Check if a port is accepting TCP connections.
        
        Args:
            port: Port number to check
            host: Host address (default: localhost)
            timeout: Connection timeout in seconds
        
        Returns:
            True if port is accepting connections
        """
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False
    
    # ───────────────────────────────────────────────────────────────────────────
    # COMPOSE_LIFECYCLE
    # ───────────────────────────────────────────────────────────────────────────
    
    def compose_up(
        self,
        detach: bool = True,
        build: bool = False
    ) -> bool:
        """
        Start Docker Compose services.
        
        Args:
            detach: Run containers in background (default: True)
            build: Rebuild images before starting (default: False)
        
        Returns:
            True if command succeeded, False otherwise
        """
        args = ["up"]
        
        if detach:
            args.append("-d")
        if build:
            args.append("--build")
        
        args.append("--remove-orphans")
        
        result = self._run_compose(args, capture=False)
        return result.returncode == 0
    
    def compose_down(
        self,
        volumes: bool = False,
        dry_run: bool = False
    ) -> bool:
        """
        Stop and remove Docker Compose services.
        
        Args:
            volumes: Also remove named volumes (default: False)
            dry_run: Only show what would be done (default: False)
        
        Returns:
            True if command succeeded (or dry_run), False otherwise
        """
        if dry_run:
            print("[DRY RUN] Would run: docker compose down")
            return True
        
        args = ["down"]
        
        if volumes:
            args.append("-v")
        
        args.append("--remove-orphans")
        
        result = self._run_compose(args, capture=False)
        return result.returncode == 0
    
    def compose_build(self, no_cache: bool = False) -> bool:
        """
        Build Docker Compose images.
        
        Args:
            no_cache: Build without using cache (default: False)
        
        Returns:
            True if build succeeded, False otherwise
        """
        args = ["build"]
        
        if no_cache:
            args.append("--no-cache")
        
        result = self._run_compose(args, capture=False)
        return result.returncode == 0
    
    def compose_ps(self) -> str:
        """
        Get status of Docker Compose services.
        
        Returns:
            String output from docker compose ps, or empty if failed
        """
        result = self._run_compose(["ps"])
        return result.stdout if result.returncode == 0 else ""
    
    def compose_logs(
        self,
        service: Optional[str] = None,
        tail: int = 50
    ) -> str:
        """
        Get logs from Docker Compose services.
        
        Args:
            service: Specific service name, or None for all services
            tail: Number of lines to retrieve (default: 50)
        
        Returns:
            Log output string, or empty if failed
        """
        args = ["logs", "--tail", str(tail)]
        
        if service:
            args.append(service)
        
        result = self._run_compose(args)
        return result.stdout if result.returncode == 0 else ""
    
    # ───────────────────────────────────────────────────────────────────────────
    # CONTAINER_INSPECTION
    # ───────────────────────────────────────────────────────────────────────────
    
    def is_service_running(self, container_name: str) -> bool:
        """
        Check if a specific container is running.
        
        Args:
            container_name: Name of the Docker container
        
        Returns:
            True if container is running, False otherwise
        """
        try:
            result = subprocess.run(
                ["docker", "inspect", "-f", "{{.State.Running}}", container_name],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout.strip().lower() == "true"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def get_container_health(self, container_name: str) -> str:
        """
        Get health status of a container.
        
        Args:
            container_name: Name of the Docker container
        
        Returns:
            Health status string ("healthy", "unhealthy", "starting", "unknown")
        """
        try:
            result = subprocess.run(
                ["docker", "inspect", "-f", "{{.State.Health.Status}}", container_name],
                capture_output=True,
                text=True,
                timeout=10
            )
            status = result.stdout.strip()
            return status if status else "unknown"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return "unknown"
    
    # ───────────────────────────────────────────────────────────────────────────
    # SERVICE_VERIFICATION
    # ───────────────────────────────────────────────────────────────────────────
    
    def verify_services(self, services: Dict[str, Dict[str, Any]]) -> bool:
        """
        Verify all services are running and healthy.
        
        This method checks each service's container status and port
        connectivity, printing results to stdout.
        
        Args:
            services: Dictionary mapping service names to their config.
                      Each config should have: container, port(s), startup_time
        
        Returns:
            True if all services are healthy, False if any failed
        
        Example:
            >>> services = {
            ...     "mqtt": {"container": "week13_mosquitto", "port": 1883}
            ... }
            >>> manager.verify_services(services)
            True
        """
        all_healthy = True
        
        for name, config in services.items():
            container = config.get("container", f"week13_{name}")
            ports = config.get("ports", [config.get("port")])
            
            # Check container is running
            if not self.is_service_running(container):
                print(f"  [FAIL] {name}: Container not running")
                all_healthy = False
                continue
            
            # Check health status if available
            health = self.get_container_health(container)
            if health not in ("healthy", "unknown", ""):
                print(f"  [WARN] {name}: Health status is {health}")
            
            # Check port connectivity
            ports_ok = True
            for port in ports:
                if port and not self._check_port(port):
                    print(f"  [WARN] {name}: Port {port} not responding")
                    ports_ok = False
            
            if ports_ok and ports:
                port_str = ", ".join(str(p) for p in ports if p)
                print(f"  [OK] {name}: Running on port(s) {port_str}")
        
        return all_healthy
    
    def show_status(self, services: Dict[str, Dict[str, Any]]) -> None:
        """
        Display formatted status of all services.
        
        Args:
            services: Dictionary of service configurations
        """
        print("\nService Status:")
        print("-" * 50)
        
        for name, config in services.items():
            container = config.get("container", f"week13_{name}")
            ports = config.get("ports", [config.get("port")])
            
            running = self.is_service_running(container)
            health = self.get_container_health(container)
            
            status_parts = []
            status_parts.append("Running" if running else "Stopped")
            
            if health and health != "unknown":
                status_parts.append(f"Health: {health}")
            
            for port in ports:
                if port:
                    port_ok = self._check_port(port) if running else False
                    status_parts.append(f"Port {port}: {'OK' if port_ok else 'FAIL'}")
            
            print(f"  {name}: {' | '.join(status_parts)}")
        
        print("-" * 50)
    
    # ───────────────────────────────────────────────────────────────────────────
    # CLEANUP_UTILITIES
    # ───────────────────────────────────────────────────────────────────────────
    
    def remove_by_prefix(self, prefix: str, dry_run: bool = False) -> None:
        """
        Remove containers, networks and volumes matching a prefix.
        
        ⚠️ WARNING: This is a destructive operation. Use with caution.
        
        Args:
            prefix: Prefix to match (e.g., "week13")
            dry_run: Only show what would be removed
        """
        # Remove containers
        result = subprocess.run(
            ["docker", "ps", "-a", "-q", "--filter", f"name={prefix}"],
            capture_output=True,
            text=True
        )
        containers = result.stdout.strip().split()
        
        if containers and containers[0]:
            if dry_run:
                print(f"[DRY RUN] Would remove containers: {containers}")
            else:
                subprocess.run(
                    ["docker", "rm", "-f"] + containers,
                    capture_output=True
                )
        
        # Remove networks
        result = subprocess.run(
            ["docker", "network", "ls", "-q", "--filter", f"name={prefix}"],
            capture_output=True,
            text=True
        )
        networks = result.stdout.strip().split()
        
        if networks and networks[0]:
            if dry_run:
                print(f"[DRY RUN] Would remove networks: {networks}")
            else:
                for net in networks:
                    subprocess.run(
                        ["docker", "network", "rm", net],
                        capture_output=True
                    )
        
        # Remove volumes
        result = subprocess.run(
            ["docker", "volume", "ls", "-q", "--filter", f"name={prefix}"],
            capture_output=True,
            text=True
        )
        volumes = result.stdout.strip().split()
        
        if volumes and volumes[0]:
            if dry_run:
                print(f"[DRY RUN] Would remove volumes: {volumes}")
            else:
                subprocess.run(
                    ["docker", "volume", "rm"] + volumes,
                    capture_output=True
                )
    
    def system_prune(self) -> None:
        """
        Prune unused Docker resources (containers, networks, images).
        
        This runs `docker system prune -f` to clean up dangling resources.
        Does not remove volumes (use -v flag manually if needed).
        """
        subprocess.run(
            ["docker", "system", "prune", "-f"],
            capture_output=True
        )


# ═══════════════════════════════════════════════════════════════════════════════
# SELF_TEST
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Docker Utilities — Module loaded successfully")
    print("Use: from scripts.utils.docker_utils import DockerManager")
