#!/usr/bin/env python3
"""
Docker Management Utilities
NETWORKING class - ASE, Informatics | by Revolvix

Provides Docker Compose management functions for Week 13 laboratory.
"""

import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
import socket


class DockerManager:
    """Manages Docker Compose operations for the laboratory environment."""
    
    def __init__(self, docker_dir: Path):
        """
        Initialise Docker manager.
        
        Args:
            docker_dir: Path to directory containing docker-compose.yml
        """
        self.docker_dir = docker_dir
        self.compose_file = docker_dir / "docker-compose.yml"
        self.env_file = docker_dir / ".env"
    
    def _run_compose(
        self,
        args: List[str],
        capture: bool = True,
        timeout: int = 120
    ) -> subprocess.CompletedProcess:
        """Execute a docker compose command."""
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
    
    def compose_up(self, detach: bool = True, build: bool = False) -> bool:
        """
        Start Docker Compose services.
        
        Args:
            detach: Run in detached mode
            build: Rebuild images before starting
        
        Returns:
            True if successful
        """
        args = ["up"]
        if detach:
            args.append("-d")
        if build:
            args.append("--build")
        args.append("--remove-orphans")
        
        result = self._run_compose(args, capture=False)
        return result.returncode == 0
    
    def compose_down(self, volumes: bool = False, dry_run: bool = False) -> bool:
        """
        Stop and remove Docker Compose services.
        
        Args:
            volumes: Also remove volumes
            dry_run: Only show what would be done
        
        Returns:
            True if successful
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
    
    def compose_build(self) -> bool:
        """Build Docker Compose images."""
        result = self._run_compose(["build"], capture=False)
        return result.returncode == 0
    
    def compose_ps(self) -> str:
        """Get status of Docker Compose services."""
        result = self._run_compose(["ps"])
        return result.stdout if result.returncode == 0 else ""
    
    def compose_logs(self, service: Optional[str] = None, tail: int = 50) -> str:
        """Get logs from Docker Compose services."""
        args = ["logs", "--tail", str(tail)]
        if service:
            args.append(service)
        result = self._run_compose(args)
        return result.stdout if result.returncode == 0 else ""
    
    def is_service_running(self, container_name: str) -> bool:
        """Check if a specific container is running."""
        try:
            result = subprocess.run(
                ["docker", "inspect", "-f", "{{.State.Running}}", container_name],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout.strip().lower() == "true"
        except Exception:
            return False
    
    def get_container_health(self, container_name: str) -> str:
        """Get health status of a container."""
        try:
            result = subprocess.run(
                ["docker", "inspect", "-f", "{{.State.Health.Status}}", container_name],
                capture_output=True,
                text=True,
                timeout=10
            )
            status = result.stdout.strip()
            return status if status else "unknown"
        except Exception:
            return "unknown"
    
    def verify_services(self, services: Dict[str, Dict[str, Any]]) -> bool:
        """
        Verify all services are running and healthy.
        
        Args:
            services: Dict mapping service names to their config
                      (container, port, health_check, startup_time)
        
        Returns:
            True if all services are healthy
        """
        all_healthy = True
        
        for name, config in services.items():
            container = config.get("container", f"week13_{name}")
            port = config.get("port")
            startup_time = config.get("startup_time", 5)
            
            # Check container is running
            if not self.is_service_running(container):
                print(f"  [FAIL] {name}: Container not running")
                all_healthy = False
                continue
            
            # Check health status
            health = self.get_container_health(container)
            if health not in ("healthy", "unknown", ""):
                print(f"  [WARN] {name}: Health status is {health}")
            
            # Check port connectivity
            if port and not self._check_port(port):
                print(f"  [WARN] {name}: Port {port} not responding")
            else:
                print(f"  [OK] {name}: Running on port {port}")
        
        return all_healthy
    
    def _check_port(self, port: int, host: str = "127.0.0.1", timeout: float = 2.0) -> bool:
        """Check if a port is accepting connections."""
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except Exception:
            return False
    
    def show_status(self, services: Dict[str, Dict[str, Any]]) -> None:
        """Display status of all services."""
        print("\nService Status:")
        print("-" * 50)
        
        for name, config in services.items():
            container = config.get("container", f"week13_{name}")
            port = config.get("port")
            
            running = self.is_service_running(container)
            health = self.get_container_health(container)
            port_ok = self._check_port(port) if port else None
            
            status_parts = []
            if running:
                status_parts.append("Running")
            else:
                status_parts.append("Stopped")
            
            if health and health != "unknown":
                status_parts.append(f"Health: {health}")
            
            if port_ok is not None:
                status_parts.append(f"Port {port}: {'OK' if port_ok else 'FAIL'}")
            
            print(f"  {name}: {' | '.join(status_parts)}")
        
        print("-" * 50)
    
    def remove_by_prefix(self, prefix: str, dry_run: bool = False) -> None:
        """Remove containers, networks and volumes matching a prefix."""
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
                subprocess.run(["docker", "rm", "-f"] + containers, capture_output=True)
        
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
                    subprocess.run(["docker", "network", "rm", net], capture_output=True)
        
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
                subprocess.run(["docker", "volume", "rm"] + volumes, capture_output=True)
    
    def system_prune(self) -> None:
        """Prune unused Docker resources."""
        subprocess.run(
            ["docker", "system", "prune", "-f"],
            capture_output=True
        )
