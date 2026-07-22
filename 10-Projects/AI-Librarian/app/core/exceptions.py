"""Custom exception types for the core foundation module."""

from __future__ import annotations


class CoreError(Exception):
    """Base exception for core module failures."""


class ConfigurationError(CoreError):
    """Raised when configuration values are invalid or missing."""


class PathResolutionError(CoreError):
    """Raised when a filesystem path cannot be resolved safely."""


class FileSystemError(CoreError):
    """Raised when filesystem operations fail unexpectedly."""


class LoggingError(CoreError):
    """Raised when logging cannot be configured properly."""
