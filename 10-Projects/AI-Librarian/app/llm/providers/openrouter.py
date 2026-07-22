"""OpenRouter provider implementation."""

from __future__ import annotations

from ..errors import LLMProviderError
from ..models import CompletionRequest, CompletionResponse
from .base import BaseProvider


class OpenRouterProvider(BaseProvider):
    name = "openrouter"

    def __init__(self, config: dict[str, object] | None = None) -> None:
        self.config = config or {}

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        if not request.prompt:
            raise LLMProviderError("Prompt is required")
        return CompletionResponse(
            text=f"OpenRouter stub response for: {request.prompt}",
            model=request.model,
            provider=self.name,
            prompt_tokens=10,
            completion_tokens=8,
            total_tokens=18,
            metadata={"provider": self.name},
        )

    def stream(self, request: CompletionRequest):
        return iter([self.complete(request)])
