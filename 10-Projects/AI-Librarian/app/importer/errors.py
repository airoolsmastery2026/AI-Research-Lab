"""Exception types for the import pipeline."""

from __future__ import annotations


class ImportError(Exception):
    """Base class for import pipeline failures."""


class ImportValidationError(ImportError):
    """Raised when a document fails validation."""


class ImportQueueError(ImportError):
    """Raised when queue operations fail."""


class ImportResumeError(ImportError):
    """Raised when resume state cannot be restored."""
