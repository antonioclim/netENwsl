#!/usr/bin/env python3
"""
Docker Management Utilities
===========================
Computer Networks - Week 6 (WSL Environment)
ASE Bucharest | by ing. dr. Antonio Clim

Provides helper functions for Docker container and compose management.
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════

import subprocess
import time
from pathlib import Path
from typing import Optional

from .logger import setup_logger

logger = setup_logger("docker_utils")


# ═══════════════════════════════════════════════════════════════════════════════
# DOCKER_MANAGER_CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class DockerManager:
    """
    Manages Docker Compose operations for the laboratory environment.
    
    This class provides a high-level interface for starting, stopping
    and managing Docker containers used in the networking lab.
    """
    
    # ─────────────────────────────────────────────────────────────────────────
    # Initialisation
    # ─────────────────────────────────────────────────────────────────────────
    
    def __init__(self, compose_dir: Path):
        """
        Initialise the Docker manager.
        
        Args:
            compose_dir: Path to directory containing docker-compose.yml
            
        Raises:
            FileNotFoundError: If docker-compose.yml not found
        """
        self.compose_dir = Path(compose_dir)
        self.compose_file = self.compose_dir / "docker-compose.yml"
        
        if not self.compose_file.exists():
            raise FileNotFoundError(f"docker-compose.yml not found in {compose_dir}")
    
    # ─────────────────────────────────────────────────────────────────────────
    # Internal helpers
    # ─────────────────────────────────────────────────────────────────────────
    
    def _run_compose(
        self,
        *args: str,
        capture_output: bool = False,
        check: bool = True
    ) -> subprocess.CompletedProcess:
        """
        Run a docker compose command.
        
        Args:
            *args: Command arguments
            capture_output: Whether to capture stdout/stderr
            check: Whether to raise on non-zero exit
            
        Returns:
            CompletedProcess result
        """
        cmd = ["docker", "compose", "-f", str(self.compose_file)] + list(args)
        logger.debug(f"Running: {' '.join(cmd)}")
        
        return subprocess.run(
            cmd,
            cwd=self.compose_dir,
            capture_output=capture_output,
            text=True,
            check=check
        )
    
    # ─────────────────────────────────────────────────────────────────────────
    # Build operations
    # ─────────────────────────────────────────────────────────────────────────
    
    def compose_build(self, service: Optional[str] = None, no_cache: bool = False) -> bool:
        """
        Build Docker images.
        
        Args:
            service: Specific service to build (None for all)
            no_cache: Whether to build without cache
            
        Returns:
            True if successful
        """
        args = ["build"]
        if no_cache:
            args.append("--no-cache")
        if service:
            args.append(service)
        
        try:
            self._run_compose(*args)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Build failed: {e}")
            return False
    
    # ─────────────────────────────────────────────────────────────────────────
    # Start operations
    # ─────────────────────────────────────────────────────────────────────────
    
    def compose_up(
        self,
        services: Optional[list[str]] = None,
        detach: bool = True,
        profiles: Optional[list[str]] = None
    ) -> bool:
        """
        Start Docker Compose services.
        
        Args:
            services: List of services to start (None for all)
            detach: Run in detached mode
            profiles: List of profiles to activate
            
        Returns:
            True if successful
        """
        args = []
        
        if profiles:
            for profile in profiles:
                args.extend(["--profile", profile])
        
        args.append("up")
        
        if detach:
            args.append("-d")
        
        if services:
            args.extend(services)
        
        try:
            self._run_compose(*args)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to start services: {e}")
            return False
    
    # ─────────────────────────────────────────────────────────────────────────
    # Stop operations
    # ─────────────────────────────────────────────────────────────────────────
    
    def compose_down(
        self,
        volumes: bool = False,
        remove_orphans: bool = True,
        dry_run: bool = False
    ) -> bool:
        """
        Stop and remove Docker Compose services.
        
        Args:
            volumes: Also remove volumes
            remove_orphans: Remove orphaned containers
            dry_run: Only print what would be done
            
        Returns:
            True if successful
        """
        if dry_run:
            logger.info("[DRY RUN] Would run: docker compose down")
            return True
        
        args = ["down"]
        
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
    
    # ─────────────────────────────────────────────────────────────────────────
    # Status operations
    # ─────────────────────────────────────────────────────────────────────────
    
    def compose_ps(self) -> dict[str, dict]:
        """
        Get status of compose services.
        
        Returns:
            Dictionary of service name to status info
        """
        try:
            result = self._run_compose("ps", "--format", "json", capture_output=True)
            import json
            services = {}
            for line in result.stdout.strip().split('\n'):
                if line:
                    try:
                        svc = json.loads(line)
                        services[svc.get('Service', svc.get('Name', 'unknown'))] = svc
                    except json.JSONDecodeError:
                        pass
            return services
        except Exception as e:
            logger.error(f"Failed to get service status: {e}")
            return {}
    
    def show_status(self, expected_services: dict) -> None:
        """
        Display status of expected services.
        
        Args:
            expected_services: Dictionary of service configurations
        """
        running = self.compose_ps()
        
        print("\nService Status:")
        print("-" * 60)
        
        for name, config in expected_services.items():
            container = config.get("container", name)
            port = config.get("port", "N/A")
            
            if container in running:
                status = running[container].get("State", "unknown")
                if status == "running":
                    print(f"  [✓] {name:<20} Port: {port:<8} Status: {status}")
                else:
                    print(f"  [!] {name:<20} Port: {port:<8} Status: {status}")
            else:
                print(f"  [✗] {name:<20} Port: {port:<8} Status: not running")
        
        print("-" * 60)
    
    # ─────────────────────────────────────────────────────────────────────────
    # Health verification
    # ─────────────────────────────────────────────────────────────────────────
    
    def verify_services(
        self,
        services: dict,
        timeout: int = 30
    ) -> bool:
        """
        Verify all services are healthy.
        
        Args:
            services: Dictionary of service configurations
            timeout: Maximum time to wait for services
            
        Returns:
            True if all services are healthy
        """
        import requests
        
        start_time = time.time()
        all_healthy = True
        
        for name, config in services.items():
            health_check = config.get("health_check")
            startup_time = config.get("startup_time", 5)
            port = config.get("port")
            
            logger.info(f"Checking {name}...")
            
            # Wait for startup time
            time.sleep(min(startup_time, timeout - (time.time() - start_time)))
            
            if health_check and port:
                url = f"http://localhost:{port}{health_check}"
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code < 500:
                        logger.info(f"  ✓ {name} is healthy")
                    else:
                        logger.warning(f"  ! {name} returned status {response.status_code}")
                        all_healthy = False
                except requests.RequestException as e:
                    logger.warning(f"  ! {name} health check failed: {e}")
                    # Not necessarily unhealthy, just no HTTP endpoint
            else:
                # No health check defined, assume OK if container is running
                running = self.compose_ps()
                container = config.get("container", name)
                if container in running and running[container].get("State") == "running":
                    logger.info(f"  ✓ {name} is running")
                else:
                    logger.error(f"  ✗ {name} is not running")
                    all_healthy = False
        
        return all_healthy
    
    # ─────────────────────────────────────────────────────────────────────────
    # Resource cleanup
    # ─────────────────────────────────────────────────────────────────────────
    
    def remove_by_prefix(self, prefix: str, dry_run: bool = False) -> None:
        """
        Remove containers, networks and volumes with a given prefix.
        
        Args:
            prefix: Prefix to match
            dry_run: Only print what would be done
        """
        # Remove containers
        result = subprocess.run(
            ["docker", "ps", "-a", "--filter", f"name={prefix}", "--format", "{{.Names}}"],
            capture_output=True,
            text=True
        )
        containers = result.stdout.strip().split('\n')
        containers = [c for c in containers if c]
        
        for container in containers:
            if dry_run:
                logger.info(f"[DRY RUN] Would remove container: {container}")
            else:
                logger.info(f"Removing container: {container}")
                subprocess.run(["docker", "rm", "-f", container], capture_output=True)
        
        # Remove networks
        result = subprocess.run(
            ["docker", "network", "ls", "--filter", f"name={prefix}", "--format", "{{.Name}}"],
            capture_output=True,
            text=True
        )
        networks = result.stdout.strip().split('\n')
        networks = [n for n in networks if n and n != "bridge" and n != "host" and n != "none"]
        
        for network in networks:
            if dry_run:
                logger.info(f"[DRY RUN] Would remove network: {network}")
            else:
                logger.info(f"Removing network: {network}")
                subprocess.run(["docker", "network", "rm", network], capture_output=True)
        
        # Remove volumes
        result = subprocess.run(
            ["docker", "volume", "ls", "--filter", f"name={prefix}", "--format", "{{.Name}}"],
            capture_output=True,
            text=True
        )
        volumes = result.stdout.strip().split('\n')
        volumes = [v for v in volumes if v]
        
        for volume in volumes:
            if dry_run:
                logger.info(f"[DRY RUN] Would remove volume: {volume}")
            else:
                logger.info(f"Removing volume: {volume}")
                subprocess.run(["docker", "volume", "rm", volume], capture_output=True)
    
    def system_prune(self, all_unused: bool = False) -> None:
        """
        Prune unused Docker resources.
        
        Args:
            all_unused: Remove all unused images, not just dangling ones
        """
        args = ["docker", "system", "prune", "-f"]
        if all_unused:
            args.append("-a")
        
        subprocess.run(args)

if __name__ == "__main__":
    # Module loaded directly - display module info
    print(f"Module {__name__} loaded successfully.")
    print(f"This module provides utility functions for the networking laboratory.")
