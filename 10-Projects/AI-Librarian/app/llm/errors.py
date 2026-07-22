"""Error types for the LLM layer."""

from __future__ import annotations


class LLMError(Exception):
    """Base exception for LLM layer failures."""


class LLMConfigurationError(LLMError):
    """Raised when LLM configuration is invalid."""


class LLMProviderError(LLMError):
    """Raised when a provider fails to fulfill a request."""


class LLMRateLimitError(LLMError):
    """Raised when a request exceeds the provider rate limit."""


class LLMTimeoutError(LLMError):
    """Raised when a request times out."""
