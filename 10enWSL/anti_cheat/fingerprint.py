#!/usr/bin/env python3
"""
Environment Fingerprinting
==========================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Generates unique fingerprints based on the local environment to ensure
submissions are created on the student's own machine with the lab running.

This module is used by homework templates to generate dynamic values
that cannot be predicted without running the actual lab environment.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import hashlib
import os
import socket
import subprocess
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional


# ═══════════════════════════════════════════════════════════════════════════════
# FINGERPRINT_DATA
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class EnvironmentFingerprint:
    """
    Environment fingerprint data.
    
    Contains information about the local environment that can be used
    to verify the submission was created on a specific machine.
    """
    username: str
    hostname: str
    date: str
    process_id: int
    docker_running: bool
    container_count: int
    fingerprint_hash: str
    
    def to_dict(self) -> Dict[str, str | int | bool]:
        """Convert to dictionary."""
        return {
            'username': self.username,
            'hostname': self.hostname,
            'date': self.date,
            'process_id': self.process_id,
            'docker_running': self.docker_running,
            'container_count': self.container_count,
            'fingerprint_hash': self.fingerprint_hash
        }


# ═══════════════════════════════════════════════════════════════════════════════
# FINGERPRINT_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def get_environment_fingerprint() -> EnvironmentFingerprint:
    """
    Generate a fingerprint of the current environment.
    
    Returns:
        EnvironmentFingerprint containing environment details
    """
    username = os.environ.get('USER', os.environ.get('USERNAME', 'unknown'))
    hostname = socket.gethostname()
    date = datetime.now().strftime('%Y-%m-%d')
    process_id = os.getpid()
    
    # Check Docker status
    docker_running = False
    container_count = 0
    
    try:
        result = subprocess.run(
            ['docker', 'ps', '--filter', 'name=week10', '-q'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            docker_running = True
            containers = result.stdout.strip().split('\n')
            container_count = len([c for c in containers if c])
    except Exception:
        pass
    
    # Generate hash
    components = [username, hostname, date, str(process_id)]
    fingerprint_hash = hashlib.md5(':'.join(components).encode()).hexdigest()[:12]
    
    return EnvironmentFingerprint(
        username=username,
        hostname=hostname,
        date=date,
        process_id=process_id,
        docker_running=docker_running,
        container_count=container_count,
        fingerprint_hash=fingerprint_hash
    )


def get_dynamic_port(base_port: int, fingerprint: Optional[str] = None) -> int:
    """
    Calculate a dynamic port based on environment fingerprint.
    
    Args:
        base_port: Base port number (e.g. 8000)
        fingerprint: Optional fingerprint hash (generates one if not provided)
        
    Returns:
        Port number in range [base_port, base_port + 99]
    """
    if fingerprint is None:
        fingerprint = get_environment_fingerprint().fingerprint_hash
    
    offset = int(fingerprint[:2], 16) % 100
    return base_port + offset


def get_unique_header(prefix: str = "X-Lab-Verify") -> str:
    """
    Generate a unique HTTP header for PCAP verification.
    
    Args:
        prefix: Header name prefix
        
    Returns:
        Complete header string (name: value)
    """
    fp = get_environment_fingerprint()
    return f"{prefix}: {fp.fingerprint_hash}-{fp.hostname[:8]}"


def generate_session_proof() -> str:
    """
    Generate a session proof string for submission verification.
    
    This proof includes environment-specific information that can
    only be obtained by running the lab locally.
    
    Returns:
        Formatted session proof string
    """
    fp = get_environment_fingerprint()
    timestamp = int(datetime.now().timestamp())
    
    # Query DNS to get real IP (requires lab running)
    dns_response = "FAILED"
    try:
        result = subprocess.run(
            ['dig', '@127.0.0.1', '-p', '5353', 'web.lab.local', '+short'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            dns_response = result.stdout.strip() or "NO_RESPONSE"
    except Exception:
        pass
    
    # Create proof hash
    proof_data = f"{timestamp}:{dns_response}:{fp.hostname}:{fp.fingerprint_hash}"
    proof_hash = hashlib.sha256(proof_data.encode()).hexdigest()[:20]
    
    return f"""
══════════════════════════════════════════════════════════════════
SESSION PROOF — Include this in your submission
══════════════════════════════════════════════════════════════════
Timestamp:      {timestamp}
Date/Time:      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Hostname:       {fp.hostname}
DNS Response:   {dns_response}
Docker Status:  {'Running' if fp.docker_running else 'Not Running'} ({fp.container_count} containers)
Fingerprint:    {fp.fingerprint_hash}
Proof Hash:     {proof_hash}
══════════════════════════════════════════════════════════════════
"""


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print(generate_session_proof())
