"""Error types for the storage layer."""

from __future__ import annotations


class StorageError(Exception):
    """Base exception for storage layer failures."""


class StorageNotFoundError(StorageError):
    """Raised when a requested record is not present."""


class StorageIntegrityError(StorageError):
    """Raised when a database or cache state appears inconsistent."""


class StorageMigrationError(StorageError):
    """Raised when migrations fail."""
