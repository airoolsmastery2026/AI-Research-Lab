"""High-level manager for selecting providers and processing requests."""

from __future__ import annotations

from .context import ConversationContext
from .errors import LLMConfigurationError, LLMProviderError
from .models import CompletionRequest, CompletionResponse, ProviderConfig
from .provider_factory import ProviderFactory
from .registry import ModelRegistry
from .tokenizer import count_tokens


class LLMManager:
    """Coordinates provider selection, configuration, and request execution."""

    def __init__(self, providers: dict[str, ProviderConfig] | None = None, registry: ModelRegistry | None = None) -> None:
        self.providers = providers or {}
        self.registry = registry or ModelRegistry()
        self._provider_instances: dict[str, object] = {}

    def register_provider(self, provider_name: str, config: ProviderConfig) -> None:
        self.providers[provider_name] = config

    def register_model(self, model_name: str, provider_name: str, max_tokens: int = 4096, cost_per_1k_tokens: float = 0.0) -> None:
        self.registry.register(type("ModelConfig", (), {
            "name": model_name,
            "provider": provider_name,
            "max_tokens": max_tokens,
            "cost_per_1k_tokens": cost_per_1k_tokens,
        })())

    def get_provider(self, provider_name: str) -> object:
        provider_name = provider_name.lower()
        if provider_name in self._provider_instances:
            return self._provider_instances[provider_name]
        if provider_name not in self.providers:
            raise LLMConfigurationError(f"Provider not configured: {provider_name}")
        provider = ProviderFactory.create(provider_name, {"config": self.providers[provider_name]})
        self._provider_instances[provider_name] = provider
        return provider

    def complete(self, request: CompletionRequest, provider_name: str | None = None) -> CompletionResponse:
        provider_name = provider_name or self._resolve_provider(request.model)
        if provider_name is None:
            raise LLMConfigurationError("No provider configured for request")
        provider = self.get_provider(provider_name)
        response = provider.complete(request)
        if response.total_tokens <= 0:
            response.total_tokens = count_tokens(request.prompt) + count_tokens(response.text)
        return response

    def stream(self, request: CompletionRequest, provider_name: str | None = None):
        provider_name = provider_name or self._resolve_provider(request.model)
        if provider_name is None:
            raise LLMConfigurationError("No provider configured for request")
        provider = self.get_provider(provider_name)
        return provider.stream(request)

    def build_context(self) -> ConversationContext:
        return ConversationContext()

    def _resolve_provider(self, model_name: str) -> str | None:
        model = self.registry.get(model_name)
        if model is None:
            return None
        return model.provider
