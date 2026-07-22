"""Base provider interface for LLM integrations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .models import CompletionRequest, CompletionResponse


class BaseProvider(ABC):
    """Abstract provider interface used by the manager."""

    name: str = "base"

    @abstractmethod
    def complete(self, request: CompletionRequest) -> CompletionResponse:
        """Return a completion for the request."""

    @abstractmethod
    def stream(self, request: CompletionRequest) -> Any:
        """Stream completion chunks for the request."""
