"""Error types for the parser engine."""

from __future__ import annotations


class ParserError(Exception):
    """Base exception for parser failures."""


class ParserValidationError(ParserError):
    """Raised when a parsing request is invalid."""
