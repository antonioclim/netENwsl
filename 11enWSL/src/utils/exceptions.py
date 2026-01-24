#!/usr/bin/env python3
"""
exceptions.py — Custom Exceptions for Week 11 Lab Kit
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim
"""
from __future__ import annotations
from typing import Optional, Any


class LabError(Exception):
    """Base exception for all Week 11 lab kit errors."""
    def __init__(self, message: str, details: Optional[Any] = None,
                 suggestion: Optional[str] = None) -> None:
        self.message = message
        self.details = details
        self.suggestion = suggestion
        parts = [message]
        if details:
            parts.append(f"Details: {details}")
        if suggestion:
            parts.append(f"Suggestion: {suggestion}")
        super().__init__(" | ".join(parts))


class NetworkError(LabError):
    """Base exception for network-related errors."""
    pass


class ConnectionRefusedError(NetworkError):
    """Raised when a connection is actively refused."""
    def __init__(self, host: str, port: int) -> None:
        super().__init__(
            f"Connection refused to {host}:{port}",
            details={"host": host, "port": port},
            suggestion=f"Start the service on port {port} or check firewall"
        )


class ConnectionTimeoutError(NetworkError):
    """Raised when a connection times out."""
    def __init__(self, host: str, port: int, timeout: float) -> None:
        super().__init__(
            f"Connection to {host}:{port} timed out after {timeout}s",
            details={"host": host, "port": port, "timeout": timeout},
            suggestion="Check network connectivity or increase timeout"
        )


class DNSResolutionError(NetworkError):
    """Raised when DNS resolution fails."""
    def __init__(self, domain: str) -> None:
        super().__init__(
            f"Failed to resolve domain: {domain}",
            suggestion="Verify the domain exists or try a different DNS server"
        )


class ConfigurationError(LabError):
    """Raised for configuration or setup errors."""
    pass


class MissingConfigError(ConfigurationError):
    """Raised when a required configuration file is missing."""
    def __init__(self, config_path: str) -> None:
        super().__init__(
            f"Required configuration file not found: {config_path}",
            suggestion="Create the file or copy from template"
        )


class ValidationError(LabError):
    """Raised for input validation errors."""
    pass


class InvalidPortError(ValidationError):
    """Raised when a port number is invalid."""
    def __init__(self, port: Any, reason: str = "out of range") -> None:
        super().__init__(
            f"Invalid port: {port} ({reason})",
            details={"port": port, "valid_range": "1024-65535"},
            suggestion="Use a port number between 1024 and 65535"
        )


class InvalidHostnameError(ValidationError):
    """Raised when a hostname is invalid."""
    def __init__(self, hostname: str) -> None:
        super().__init__(
            f"Invalid hostname: {hostname}",
            suggestion="Use a valid hostname or IP address"
        )


class PathTraversalError(ValidationError):
    """Raised when path traversal is detected."""
    def __init__(self, path: str) -> None:
        super().__init__(
            "Potential path traversal detected",
            details={"path": path},
            suggestion="Use absolute paths without '..' or special characters"
        )


class DockerError(LabError):
    """Base exception for Docker-related errors."""
    pass


class DockerNotRunningError(DockerError):
    """Raised when Docker daemon is not running."""
    def __init__(self) -> None:
        super().__init__(
            "Docker daemon is not running",
            suggestion="Start Docker with: sudo service docker start"
        )


class ContainerNotFoundError(DockerError):
    """Raised when a required container is not found."""
    def __init__(self, container_name: str) -> None:
        super().__init__(
            f"Container not found: {container_name}",
            suggestion="Start the lab environment: make lab"
        )


class QuizError(LabError):
    """Base exception for quiz-related errors."""
    pass


class QuizFileError(QuizError):
    """Raised when quiz file is invalid."""
    def __init__(self, path: str, parse_error: Optional[str] = None) -> None:
        super().__init__(
            f"Failed to load quiz file: {path}",
            details={"parse_error": parse_error} if parse_error else None,
            suggestion="Validate YAML syntax"
        )


__all__ = [
    "LabError", "NetworkError", "ConnectionRefusedError", "ConnectionTimeoutError",
    "DNSResolutionError", "ConfigurationError", "MissingConfigError",
    "ValidationError", "InvalidPortError", "InvalidHostnameError",
    "PathTraversalError", "DockerError", "DockerNotRunningError",
    "ContainerNotFoundError", "QuizError", "QuizFileError",
]
