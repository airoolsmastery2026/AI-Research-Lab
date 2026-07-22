"""Provider factory and selection logic."""

from __future__ import annotations

from .errors import LLMConfigurationError
from .provider_base import BaseProvider
from .providers import AnthropicProvider, GeminiProvider, OllamaProvider, OpenAIProvider, OpenRouterProvider


class ProviderFactory:
    """Create providers based on configuration."""

    @staticmethod
    def create(provider_name: str, config: dict[str, object] | None = None) -> BaseProvider:
        provider_name = provider_name.lower()
        config = config or {}

        providers = {
            "openai": OpenAIProvider,
            "gemini": GeminiProvider,
            "openrouter": OpenRouterProvider,
            "anthropic": AnthropicProvider,
            "ollama": OllamaProvider,
        }
        provider_cls = providers.get(provider_name)
        if provider_cls is None:
            raise LLMConfigurationError(f"Unsupported provider: {provider_name}")
        return provider_cls(config)
