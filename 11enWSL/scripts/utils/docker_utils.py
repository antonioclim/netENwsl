#!/usr/bin/env python3
"""
Docker management utilities for Week 11 Laboratory.
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Provides Docker Compose orchestration and health checking functions.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import subprocess
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
import urllib.request
import urllib.error

from .logger import setup_logger

logger = setup_logger("docker_utils")



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class DockerManager:
    """Manages Docker Compose operations for the laboratory environment."""
    

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
    def __init__(self, compose_dir: Path):
        """
        Initialise the Docker manager.
        
        Args:
            compose_dir: Path to directory containing docker-compose.yml
        """
        self.compose_dir = Path(compose_dir)
        self.compose_file = self.compose_dir / "docker-compose.yml"
        
        if not self.compose_file.exists():
            raise FileNotFoundError(f"docker-compose.yml not found in {compose_dir}")
    

# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def _run_compose(self, 
                     args: List[str], 
                     capture_output: bool = False,
                     check: bool = True) -> subprocess.CompletedProcess:
        """
        Execute a docker compose command.
        
        Args:
            args: Command arguments after 'docker compose'
            capture_output: Whether to capture stdout/stderr
            check: Whether to raise on non-zero exit
        
        Returns:
            CompletedProcess instance
        """
        cmd = ["docker", "compose", "-f", str(self.compose_file)] + args
        logger.debug(f"Running: {' '.join(cmd)}")
        
        return subprocess.run(
            cmd,
            cwd=str(self.compose_dir),
            capture_output=capture_output,
            text=True,
            check=check
        )
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def compose_up(self, 
                   detach: bool = True, 
                   build: bool = False,
                   services: Optional[List[str]] = None) -> bool:
        """
        Start Docker Compose services.
        
        Args:
            detach: Run in detached mode
            build: Force rebuild images
            services: Specific services to start (None for all)
        
        Returns:
            True if successful
        """
        args = ["up"]
        if detach:
            args.append("-d")
        if build:
            args.append("--build")
        if services:
            args.extend(services)
        
        try:
            self._run_compose(args)
            logger.info("Docker Compose stack started successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to start Docker stack: {e}")
            return False
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def compose_down(self, 
                     volumes: bool = False, 
                     dry_run: bool = False) -> bool:
        """
        Stop Docker Compose services.
        
        Args:
            volumes: Also remove volumes
            dry_run: Only show what would be done
        
        Returns:
            True if successful
        """
        if dry_run:
            logger.info("[DRY RUN] Would run: docker compose down" + 
                       (" -v" if volumes else ""))
            return True
        
        args = ["down"]
        if volumes:
            args.append("-v")
        
        try:
            self._run_compose(args)
            logger.info("Docker Compose stack stopped")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to stop Docker stack: {e}")
            return False
    

# ═══════════════════════════════════════════════════════════════════════════════
# RESOURCE_CREATION
# ═══════════════════════════════════════════════════════════════════════════════
    def compose_build(self, 
                      no_cache: bool = False,
                      services: Optional[List[str]] = None) -> bool:
        """
        Build Docker Compose images.
        
        Args:
            no_cache: Build without using cache
            services: Specific services to build
        
        Returns:
            True if successful
        """
        args = ["build"]
        if no_cache:
            args.append("--no-cache")
        if services:
            args.extend(services)
        
        try:
            self._run_compose(args)
            logger.info("Docker images built successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to build images: {e}")
            return False
    

# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def get_running_containers(self) -> List[str]:
        """Get list of running container names."""
        try:
            result = self._run_compose(
                ["ps", "--format", "json"],
                capture_output=True,
                check=False
            )
            if result.returncode != 0:
                return []
            
            containers = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    try:
                        data = json.loads(line)
                        if data.get('State') == 'running':
                            containers.append(data.get('Name', ''))
                    except json.JSONDecodeError:
                        continue
            return containers
        except Exception:
            return []
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def show_status(self, services: Dict[str, Any]) -> None:
        """
        Display status of all services.
        
        Args:
            services: Dictionary of service definitions with ports
        """
        running = self.get_running_containers()
        
        print("\nService Status:")
        print("-" * 50)
        
        for name, config in services.items():
            container = config.get('container', '')
            port = config.get('port', '')
            status = "RUNNING" if container in running else "STOPPED"
            colour = "\033[32m" if status == "RUNNING" else "\033[31m"
            reset = "\033[0m"
            print(f"  {name:20} {colour}{status:10}{reset} :{port}")
        
        print("-" * 50)
    

# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
    def verify_services(self, 
                        services: Dict[str, Any],
                        timeout: int = 30) -> bool:
        """
        Verify all services are healthy.
        
        Args:
            services: Dictionary of service definitions
            timeout: Maximum wait time in seconds
        
        Returns:
            True if all services are healthy
        """
        start_time = time.time()
        all_healthy = True
        
        for name, config in services.items():
            port = config.get('port')
            health_check = config.get('health_check')
            startup_time = config.get('startup_time', 5)
            
            # Wait for startup
            time.sleep(min(startup_time, 2))
            
            if health_check:
                url = f"http://localhost:{port}{health_check}"
                healthy = self._check_http_health(url, timeout=10)
            else:
                healthy = self._check_port_open(port, timeout=10)
            
            if healthy:
                logger.info(f"  ✓ {name} is healthy (port {port})")
            else:
                logger.error(f"  ✗ {name} is NOT healthy (port {port})")
                all_healthy = False
        
        return all_healthy
    

# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
    def _check_http_health(self, url: str, timeout: int = 5) -> bool:
        """Check if HTTP endpoint responds with 2xx status."""
        try:
            req = urllib.request.Request(url, method='GET')
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return 200 <= response.status < 300
        except Exception:
            return False
    

# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
    def _check_port_open(self, port: int, timeout: int = 5) -> bool:
        """Check if a TCP port is accepting connections."""
        import socket
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex(('localhost', port))
                return result == 0
        except Exception:
            return False
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def remove_by_prefix(self, prefix: str, dry_run: bool = False) -> None:
        """
        Remove Docker resources matching a prefix.
        
        Args:
            prefix: Prefix to match (e.g., 'week11')
            dry_run: Only show what would be removed
        """
        # Remove containers
        try:
            result = subprocess.run(
                ["docker", "ps", "-a", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                check=True
            )
            containers = [c for c in result.stdout.strip().split('\n') 
                         if c.startswith(prefix)]
            
            for container in containers:
                if dry_run:
                    logger.info(f"[DRY RUN] Would remove container: {container}")
                else:
                    subprocess.run(
                        ["docker", "rm", "-f", container],
                        capture_output=True,
                        check=False
                    )
                    logger.info(f"Removed container: {container}")
        except Exception as e:
            logger.warning(f"Error cleaning containers: {e}")
        
        # Remove networks
        try:
            result = subprocess.run(
                ["docker", "network", "ls", "--format", "{{.Name}}"],
                capture_output=True,
                text=True,
                check=True
            )
            networks = [n for n in result.stdout.strip().split('\n') 
                       if n.startswith(prefix)]
            
            for network in networks:
                if dry_run:
                    logger.info(f"[DRY RUN] Would remove network: {network}")
                else:
                    subprocess.run(
                        ["docker", "network", "rm", network],
                        capture_output=True,
                        check=False
                    )
                    logger.info(f"Removed network: {network}")
        except Exception as e:
            logger.warning(f"Error cleaning networks: {e}")
    

# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def system_prune(self) -> None:
        """Prune unused Docker resources."""
        try:
            subprocess.run(
                ["docker", "system", "prune", "-f"],
                capture_output=True,
                check=True
            )
            logger.info("Docker system pruned")
        except Exception as e:
            logger.warning(f"Error pruning Docker: {e}")
    

# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
    def get_logs(self, 
                 service: Optional[str] = None,
                 tail: int = 100) -> str:
        """
        Get logs from Docker Compose services.
        
        Args:
            service: Specific service (None for all)
            tail: Number of lines to show
        
        Returns:
            Log output as string
        """
        args = ["logs", "--tail", str(tail)]
        if service:
            args.append(service)
        
        try:
            result = self._run_compose(args, capture_output=True, check=False)
            return result.stdout + result.stderr
        except Exception as e:
            return f"Error fetching logs: {e}"


# ing. dr. Antonio Clim

if __name__ == "__main__":
    # Module loaded directly - display module info
    print(f"Module {__name__} loaded successfully.")
    print(f"This module provides utility functions for the networking laboratory.")
