#!/usr/bin/env python3
"""
Docker utilities for Week 9 Laboratory
NETWORKING class - ASE, Informatics | by Revolvix

Provides helper functions for managing Docker containers, networks,
and volumes used in the laboratory environment.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Any

from .logger import setup_logger

logger = setup_logger("docker_utils")



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class DockerManager:
    """
    Manager class for Docker operations.
    
    Wraps Docker CLI commands with error handling and logging.
    Supports both Docker Compose v1 (docker-compose) and v2 (docker compose).
    """
    

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
    def __init__(self, compose_dir: Path):
        """
        Initialise Docker manager.
        
        Args:
            compose_dir: Path to directory containing docker-compose.yml
        """
        self.compose_dir = Path(compose_dir)
        self.compose_file = self.compose_dir / "docker-compose.yml"
        self._compose_cmd = self._detect_compose_command()
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def _detect_compose_command(self) -> List[str]:
        """Detect available Docker Compose command."""
        # Try docker compose (v2) first
        try:
            result = subprocess.run(
                ["docker", "compose", "version"],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                return ["docker", "compose"]
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        
        # Fall back to docker-compose (v1)
        try:
            result = subprocess.run(
                ["docker-compose", "--version"],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                return ["docker-compose"]
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        
        logger.warning("Docker Compose not found, using default command")
        return ["docker", "compose"]
    

# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def _run_compose(
        self,
        args: List[str],
        capture: bool = False,
        check: bool = True
    ) -> subprocess.CompletedProcess:
        """
        Run a Docker Compose command.
        
        Args:
            args: Arguments to pass to compose command
            capture: Whether to capture output
            check: Whether to raise on non-zero exit
        
        Returns:
            CompletedProcess instance
        """
        cmd = self._compose_cmd + ["-f", str(self.compose_file)] + args
        
        logger.debug(f"Running: {' '.join(cmd)}")
        
        return subprocess.run(
            cmd,
            cwd=self.compose_dir,
            capture_output=capture,
            text=True,
            check=check
        )
    

# ═══════════════════════════════════════════════════════════════════════════════
# RESOURCE_CREATION
# ═══════════════════════════════════════════════════════════════════════════════
    def compose_build(self, no_cache: bool = False) -> bool:
        """
        Build Docker images defined in compose file.
        
        Args:
            no_cache: If True, build without using cache
        
        Returns:
            True if build succeeded
        """
        logger.info("Building Docker images...")
        
        args = ["build"]
        if no_cache:
            args.append("--no-cache")
        
        try:
            self._run_compose(args)
            logger.info("Build completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Build failed: {e}")
            return False
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def compose_up(self, detach: bool = True, build: bool = False) -> bool:
        """
        Start containers defined in compose file.
        
        Args:
            detach: Run in background
            build: Build images before starting
        
        Returns:
            True if startup succeeded
        """
        logger.info("Starting containers...")
        
        args = ["up"]
        if detach:
            args.append("-d")
        if build:
            args.append("--build")
        
        try:
            self._run_compose(args)
            logger.info("Containers started")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to start containers: {e}")
            return False
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def compose_down(
        self,
        volumes: bool = False,
        remove_orphans: bool = True,
        dry_run: bool = False
    ) -> bool:
        """
        Stop and remove containers.
        
        Args:
            volumes: Also remove volumes
            remove_orphans: Remove containers not defined in compose file
            dry_run: If True, only log what would be done
        
        Returns:
            True if successful
        """
        args = ["down"]
        if volumes:
            args.append("-v")
        if remove_orphans:
            args.append("--remove-orphans")
        
        if dry_run:
            logger.info(f"[DRY RUN] Would run: docker compose {' '.join(args)}")
            return True
        
        try:
            self._run_compose(args)
            logger.info("Containers stopped and removed")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to stop containers: {e}")
            return False
    

# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
    def compose_logs(
        self,
        service: Optional[str] = None,
        follow: bool = False,
        tail: int = 100
    ) -> str:
        """
        Get logs from containers.
        
        Args:
            service: Specific service name (None for all)
            follow: Stream logs (blocking)
            tail: Number of lines to show
        
        Returns:
            Log output as string
        """
        args = ["logs", f"--tail={tail}"]
        if follow:
            args.append("-f")
        if service:
            args.append(service)
        
        try:
            result = self._run_compose(args, capture=True, check=False)
            return result.stdout + result.stderr
        except subprocess.SubprocessError as e:
            return f"Error getting logs: {e}"
    

# ═══════════════════════════════════════════════════════════════════════════════
# CONTAINER_MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════
    def get_container_status(self) -> List[Dict[str, Any]]:
        """
        Get status of all compose containers.
        
        Returns:
            List of container info dictionaries
        """
        try:
            result = self._run_compose(
                ["ps", "--format", "json"],
                capture=True,
                check=False
            )
            
            if result.returncode != 0:
                return []
            
            # Parse JSON output (one JSON object per line)
            containers = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    try:
                        containers.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
            
            return containers
            
        except subprocess.SubprocessError:
            return []
    

# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
    def verify_services(
        self,
        services: Dict[str, Dict[str, Any]],
        timeout: int = 60
    ) -> bool:
        """
        Verify that all services are healthy.
        
        Args:
            services: Dict of service definitions with health check info
            timeout: Maximum seconds to wait for services
        
        Returns:
            True if all services are healthy
        """
        start_time = time.time()
        all_healthy = False
        
        while time.time() - start_time < timeout:
            containers = self.get_container_status()
            running_count = sum(
                1 for c in containers
                if c.get('State') == 'running' or c.get('Status', '').startswith('Up')
            )
            
            if running_count >= len(services):
                all_healthy = True
                break
            
            logger.debug(f"Waiting for services... ({running_count}/{len(services)})")
            time.sleep(2)
        
        if all_healthy:
            logger.info(f"All {len(services)} services are running")
        else:
            logger.warning("Not all services started within timeout")
        
        return all_healthy
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def show_status(self, services: Dict[str, Dict[str, Any]]) -> None:
        """Display status of services in a formatted table."""
        containers = self.get_container_status()
        
        print("\n" + "=" * 60)
        print("Container Status")
        print("=" * 60)
        
        if not containers:
            print("No containers running")
        else:
            for c in containers:
                name = c.get('Name', c.get('Names', 'Unknown'))
                state = c.get('State', c.get('Status', 'Unknown'))
                print(f"  {name:30} {state}")
        
        print("=" * 60 + "\n")
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def remove_by_prefix(
        self,
        prefix: str,
        dry_run: bool = False
    ) -> None:
        """
        Remove containers, networks and volumes by name prefix.
        
        Args:
            prefix: Prefix to match (e.g., "week9")
            dry_run: If True, only log what would be done
        """
        # Remove containers
        try:
            result = subprocess.run(
                ["docker", "ps", "-a", "--format", "{{.Names}}"],
                capture_output=True,
                text=True
            )
            
            for name in result.stdout.strip().split('\n'):
                if name.startswith(prefix):
                    if dry_run:
                        logger.info(f"[DRY RUN] Would remove container: {name}")
                    else:
                        subprocess.run(
                            ["docker", "rm", "-f", name],
                            capture_output=True
                        )
                        logger.debug(f"Removed container: {name}")
        except subprocess.SubprocessError:
            pass
        
        # Remove networks
        try:
            result = subprocess.run(
                ["docker", "network", "ls", "--format", "{{.Name}}"],
                capture_output=True,
                text=True
            )
            
            for name in result.stdout.strip().split('\n'):
                if name.startswith(prefix):
                    if dry_run:
                        logger.info(f"[DRY RUN] Would remove network: {name}")
                    else:
                        subprocess.run(
                            ["docker", "network", "rm", name],
                            capture_output=True
                        )
                        logger.debug(f"Removed network: {name}")
        except subprocess.SubprocessError:
            pass
    

# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def system_prune(self, volumes: bool = False) -> None:
        """
        Clean up unused Docker resources.
        
        Args:
            volumes: Also remove unused volumes
        """
        args = ["docker", "system", "prune", "-f"]
        if volumes:
            args.append("--volumes")
        
        try:
            subprocess.run(args, capture_output=True)
            logger.info("Docker system pruned")
        except subprocess.SubprocessError as e:
            logger.warning(f"Prune failed: {e}")



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_docker_running() -> bool:
    """
    Check if Docker daemon is running.
    
    Returns:
        True if Docker is available
    """
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# CONTAINER_MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════
def get_docker_version() -> Optional[str]:
    """
    Get Docker version string.
    
    Returns:
        Version string or None if unavailable
    """
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            # Parse "Docker version X.Y.Z, ..."
            return result.stdout.strip().split(',')[0].replace('Docker version ', '')
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    return None


# =============================================================================
# Module test
# =============================================================================

if __name__ == "__main__":
    print("Docker Utilities Test")
    print("=" * 40)
    
    print(f"Docker running: {check_docker_running()}")
    print(f"Docker version: {get_docker_version()}")
